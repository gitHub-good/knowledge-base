#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""需求池管理：知识库自身的改进需求，单文件单需求，状态自动流转。

用法（仓库根或任意子目录）：
    python tools/req.py                              # 校验 + 统计
    python tools/req.py new "标题" [-t 类型] [-p 优先级] [--from TB-YYYYMMDD-NN]
                                [-d 一句话说明] [--gwt 验收标准]...   # --gwt 可重复传多条
    python tools/req.py start REQ-YYYYMMDD-NN        # 待评审 → 开发中
    python tools/req.py done  REQ-YYYYMMDD-NN        # → 已关闭（自动写完成日期+进展+刷新汇总）
    python tools/req.py reject REQ-YYYYMMDD-NN [原因] # → 已拒绝（留档）
    python tools/req.py sync                         # 重新生成 backlog.md（需求池）汇总区块

文件：project-development/01-requirements/REQ-YYYYMMDD-NN-标题.md；汇总区块在 backlog.md（需求池）的
<!-- reqpool:begin/end --> 标记之间。状态机为 01 方法论完整状态机的从简子集
（本池条目多为文档工作，无提测/发布环节）。退出码：有问题 = 1，全过 = 0。
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
REQ_DIR = ROOT / "project-development" / "01-requirements"
POOL = REQ_DIR / "backlog.md"
BEGIN, END = "<!-- reqpool:begin -->", "<!-- reqpool:end -->"
STATUSES = ("待评审", "开发中", "已关闭", "已拒绝")
TYPES = ("功能", "优化", "缺陷", "技术")
PRIORITIES = ("必须", "应该", "可以", "暂不")
FILE_RE = re.compile(r"^REQ-(\d{8})-(\d{2})-(.+)\.md$")


def die(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def sanitize(title: str) -> str:
    # 白名单清洗：仅保留中英文、数字、连字符；其余字符折叠为单个连字符（与 todo.py 同款，防 ~() 等破坏文件名与链接）
    s = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff-]+", "-", title.strip())
    return re.sub(r"-{2,}", "-", s).strip("-")


def reqs() -> list:
    if not REQ_DIR.is_dir():
        return []
    return sorted(p for p in REQ_DIR.iterdir() if p.is_file() and FILE_RE.match(p.name))


def load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {"raw": None, "fields": {}, "body": text}
    fields = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep:
            fields[k.strip()] = v.strip()
    return {"raw": m.group(1), "fields": fields, "body": text[m.end():]}


def set_field(fm_raw: str, key: str, value: str) -> str:
    lines, out, hit = fm_raw.splitlines(), [], False
    for line in lines:
        k, sep, _ = line.partition(":")
        if sep and k.strip() == key:
            out.append(f"{key}: {value}")
            hit = True
        else:
            out.append(line)
    if not hit:
        out.append(f"{key}: {value}")
    return "\n".join(out)


def save(path: Path, fm_raw: str, body: str) -> None:
    path.write_text(f"---\n{fm_raw}\n---\n{body}", encoding="utf-8", newline="\n")


def append_log(body: str, line: str) -> str:
    return body.rstrip("\n") + f"\n- {line}\n"


def find(code: str) -> Path:
    hits = [p for p in reqs() if p.name.startswith(f"{code}-")]
    if not hits:
        die(f"找不到需求 {code}（现有：{', '.join(p.name for p in reqs()) or '无'}）")
    if len(hits) > 1:
        die(f"编号 {code} 命中多个文件：{[p.name for p in hits]}")
    return hits[0]


def title_of(path: Path) -> str:
    return FILE_RE.match(path.name).group(3)


def build_block() -> str:
    items = []
    for p in reqs():
        f = load(p)["fields"]
        m = FILE_RE.match(p.name)
        items.append({
            "path": p, "title": title_of(p), "code": f"REQ-{m.group(1)}-{m.group(2)}",
            "status": f.get("status", ""), "type": f.get("类型", ""), "priority": f.get("优先级", ""),
            "source": f.get("来源", ""), "created": f.get("创建日期", ""), "finished": f.get("完成日期", ""),
        })
    counts = {s: sum(1 for i in items if i["status"] == s) for s in STATUSES}
    lines = ["> 由 `python tools/req.py sync` 自动生成，手改会被覆盖。", ""]
    if not items:
        lines.append("暂无需求文件——用 `python tools/req.py new \"标题\"` 创建第一条。")
        return "\n".join(lines) + "\n"
    lines.append(f"**统计**：待评审 {counts['待评审']} ｜ 开发中 {counts['开发中']} ｜ 已关闭 {counts['已关闭']} ｜ 已拒绝 {counts['已拒绝']}（共 {len(items)}）")
    open_items = sorted((i for i in items if i["status"] in ("待评审", "开发中")),
                        key=lambda i: (i["created"], i["path"].name))
    if open_items:
        lines += ["", "**未关闭**（按创建日期，早的在前；优先级按 MoSCoW：必须 > 应该 > 可以 > 暂不）：", "",
                  "| 编号 | 标题 | 类型 | 优先级 | 状态 | 来源 | 创建日期 |", "| --- | --- | --- | --- | --- | --- | --- |"]
        for i in open_items:
            lines.append(f"| [{i['code']}]({i['path'].name}) | {i['title']} | {i['type']} | {i['priority']} | {i['status']} | {i['source']} | {i['created']} |")
    closed = sorted((i for i in items if i["status"] == "已关闭"),
                    key=lambda i: (i["finished"], i["path"].name), reverse=True)[:5]
    if closed:
        lines += ["", "**最近关闭**（最新 5 条）：", "",
                  "| 编号 | 标题 | 完成日期 |", "| --- | --- | --- |"]
        for i in closed:
            lines.append(f"| [{i['code']}]({i['path'].name}) | {i['title']} | {i['finished']} |")
    return "\n".join(lines) + "\n"


def sync() -> None:
    block = build_block()
    text = POOL.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        die(f"{POOL} 缺少 {BEGIN}/{END} 标记")
    pre, _, rest = text.partition(BEGIN)
    _, _, post = rest.partition(END)
    POOL.write_text(pre.rstrip("\n") + "\n\n" + BEGIN + "\n" + block + END + post.lstrip("\n"),
                    encoding="utf-8", newline="\n")


def cmd_new(args) -> str:
    if args.type not in TYPES:
        die(f"类型必须是 {'/'.join(TYPES)}，收到：{args.type}")
    if args.priority not in PRIORITIES:
        die(f"优先级必须是 {'/'.join(PRIORITIES)}，收到：{args.priority}")
    today = date.today()
    prefix = f"REQ-{today:%Y%m%d}-"
    seq = max((int(FILE_RE.match(p.name).group(2)) for p in reqs() if p.name.startswith(prefix)), default=0) + 1
    title = sanitize(args.title)
    if not title:
        die("标题为空（或清洗后为空）")
    path = REQ_DIR / f"{prefix}{seq:02d}-{title}.md"
    source = args.from_ or "原始诉求"
    origin_note = f"（来源：{args.from_}）" if args.from_ else ""
    desc = (args.desc or "一句话说明").strip()
    gwt = [i.strip() for i in (args.gwt or []) if i.strip()]
    gwt_lines = "\n".join(f"- [ ] {i}" for i in gwt) or "- [ ] Given <前置条件> When <操作> Then <期望结果>"
    body = (
        f"# 📥 {args.title.strip()}\n\n"
        f"> {desc}\n\n"
        f"## 📋 验收标准（Given/When/Then）\n\n"
        f"{gwt_lines}\n\n"
        f"## 📝 进展记录\n\n"
        f"- {today.isoformat()} 创建{origin_note}。\n"
    )
    fm = (f"status: 待评审\n类型: {args.type}\n优先级: {args.priority}\n"
          f"创建日期: {today.isoformat()}\n来源: {source}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8", newline="\n")
    sync()
    code = f"{prefix}{seq:02d}"
    if args.print_code:
        print(code)
    else:
        print(f"[新建] {path.name}")
    return code


def _transition(code: str, new_status: str, log_word: str) -> None:
    path = find(code)
    d = load(path)
    if d["raw"] is None:
        die(f"{path.name} 缺文件头（frontmatter）")
    today = date.today().isoformat()
    fm = set_field(d["raw"], "status", new_status)
    body = append_log(d["body"], f"{today} {log_word}。")
    if new_status == "已关闭":
        fm = set_field(fm, "完成日期", today)
    save(path, fm, body)
    sync()
    print(f"[{new_status}] {path.name}")


def validate() -> int:
    problems = []
    for p in reqs():
        d = load(p)
        f = d["fields"]
        if d["raw"] is None:
            problems.append(f"{p.name}: 缺文件头")
            continue
        if f.get("status") not in STATUSES:
            problems.append(f"{p.name}: status 非法（{f.get('status', '缺失')}）")
        if f.get("类型") not in TYPES:
            problems.append(f"{p.name}: 类型非法（{f.get('类型', '缺失')}）")
        if f.get("优先级") not in PRIORITIES:
            problems.append(f"{p.name}: 优先级非法（{f.get('优先级', '缺失')}）")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", f.get("创建日期", "")):
            problems.append(f"{p.name}: 创建日期缺失或格式错")
        if not f.get("来源"):
            problems.append(f"{p.name}: 来源缺失")
        if f.get("status") == "已关闭" and not f.get("完成日期"):
            problems.append(f"{p.name}: 已关闭但缺完成日期")
        if f.get("status") != "已关闭" and f.get("完成日期"):
            problems.append(f"{p.name}: 未关闭却带完成日期")
        if "## 📋 验收标准" not in d["body"]:
            problems.append(f"{p.name}: 缺验收标准节")
        if re.search(r"^> 一句话说明$", d["body"], re.M):
            problems.append(f"{p.name}: 一句话说明未填写（new -d 或手工补）")
        if re.search(r"^- \[ \] Given <前置条件> When <操作> Then <期望结果>$", d["body"], re.M):
            problems.append(f"{p.name}: 验收标准未填写（new --gwt 或手工补）")
    if not POOL.is_file():
        problems.append(f"缺 {POOL}")
    elif BEGIN not in POOL.read_text(encoding="utf-8"):
        problems.append("backlog.md 缺汇总区块标记")
    elif build_block().rstrip("\n") not in POOL.read_text(encoding="utf-8"):
        problems.append("汇总区块与文件状态不同步，请执行 python tools/req.py sync")
    counts = {s: 0 for s in STATUSES}
    for p in reqs():
        counts[load(p)["fields"].get("status", "?")] = counts.get(load(p)["fields"].get("status", "?"), 0) + 1
    print(f"需求文件: {len(reqs())} | 待评审 {counts['待评审']} / 开发中 {counts['开发中']} / "
          f"已关闭 {counts['已关闭']} / 已拒绝 {counts['已拒绝']} | 问题: {len(problems)}")
    for x in problems:
        print("  " + x)
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="需求池管理：单文件单需求，状态自动流转")
    sub = ap.add_subparsers(dest="cmd")
    p_new = sub.add_parser("new", help="新建需求")
    p_new.add_argument("title", help="需求标题")
    p_new.add_argument("-t", "--type", default="优化", help="类型：功能/优化/缺陷/技术")
    p_new.add_argument("-p", "--priority", default="应该", help="优先级（MoSCoW）：必须/应该/可以/暂不")
    p_new.add_argument("--from", dest="from_", default="", help="来源编号，如 TB-20260918-01")
    p_new.add_argument("-d", "--desc", help="一句话说明（缺省留占位符，校验会提示未填）")
    p_new.add_argument("--gwt", action="append", metavar="标准",
                       help="验收标准一条（Given/When/Then），可重复传入；缺省留占位符")
    p_new.add_argument("--print-code", action="store_true", help="只打印新编号（供 todo.py convert 调用）")
    p_start = sub.add_parser("start", help="待评审 → 开发中")
    p_start.add_argument("code", help="编号，如 REQ-20260918-01")
    p_done = sub.add_parser("done", help="标记关闭（自动写日期+进展+刷新汇总）")
    p_done.add_argument("code", help="编号，如 REQ-20260918-01")
    p_rej = sub.add_parser("reject", help="拒绝（留档）")
    p_rej.add_argument("code", help="编号，如 REQ-20260918-01")
    p_rej.add_argument("reason", nargs="*", help="拒绝原因")
    sub.add_parser("sync", help="重新生成汇总区块")
    args = ap.parse_args()
    if args.cmd == "new":
        cmd_new(args)
        return 0
    if args.cmd == "start":
        _transition(args.code, "开发中", "开始推进")
        return 0
    if args.cmd == "done":
        _transition(args.code, "已关闭", "完成关闭")
        return 0
    if args.cmd == "reject":
        reason = " ".join(args.reason).strip() or "不做"
        _transition(args.code, "已拒绝", f"拒绝：{reason}")
        return 0
    if args.cmd == "sync":
        sync()
        print("[已刷新] 01-requirements/backlog.md 汇总区块")
        return 0
    return validate()


if __name__ == "__main__":
    sys.exit(main())
