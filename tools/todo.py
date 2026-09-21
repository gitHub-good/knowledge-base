#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""待办项管理：单文件单待办，状态自动流转。

用法（仓库根或任意子目录）：
    python tools/todo.py                            # 校验 + 统计
    python tools/todo.py new "标题" [-p 高|中|低] [-d 一句话说明] [--dod 完成标准]...
                                                    # 建待办（自动编号，刷新汇总；--dod 可重复传多条）
    python tools/todo.py start TB-YYYYMMDD-NN       # 待办 → 进行中
    python tools/todo.py done  TB-YYYYMMDD-NN       # → 已完成（自动写完成日期+进展+刷新汇总）
    python tools/todo.py cancel TB-YYYYMMDD-NN [原因] # → 已取消（留档）
    python tools/todo.py convert TB-YYYYMMDD-NN [-p 必须|应该|可以|暂不]
                                                    # 转需求：自动建 REQ 条目（来源=待办编号），
                                                    #   待办关闭并回写 REQ 编号（调用 tools/req.py）
    python tools/todo.py sync                       # 重新生成 06-todos/index.md 汇总区块

文件：project-development/06-todos/TB-YYYYMMDD-NN-标题.md；汇总区块在 index.md 的
<!-- todos:begin/end --> 标记之间。退出码：有问题 = 1，全过 = 0。
"""
import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
TODO_DIR = ROOT / "project-development" / "06-todos"
INDEX = TODO_DIR / "index.md"
BEGIN, END = "<!-- todos:begin -->", "<!-- todos:end -->"
STATUSES = ("待办", "进行中", "已完成", "已取消")
PRIORITIES = ("高", "中", "低")
FILE_RE = re.compile(r"^TB-(\d{8})-(\d{2})-(.+)\.md$")


def die(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def sanitize(title: str) -> str:
    return re.sub(r"[\s/\\:*?\"<>|]+", "-", title.strip()).strip("-")


def todos() -> list:
    if not TODO_DIR.is_dir():
        return []
    return sorted(p for p in TODO_DIR.iterdir() if p.is_file() and FILE_RE.match(p.name))


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
    hits = [p for p in todos() if p.name.startswith(f"{code}-")]
    if not hits:
        die(f"找不到待办 {code}（现有：{', '.join(p.name for p in todos()) or '无'}）")
    if len(hits) > 1:
        die(f"编号 {code} 命中多个文件：{[p.name for p in hits]}")
    return hits[0]


def title_of(path: Path) -> str:
    return FILE_RE.match(path.name).group(3)


def build_block() -> str:
    items = []
    for p in todos():
        d = load(p)
        f = d["fields"]
        m = FILE_RE.match(p.name)
        items.append({
            "path": p, "title": title_of(p), "code": f"TB-{m.group(1)}-{m.group(2)}",
            "status": f.get("status", ""), "priority": f.get("优先级", ""),
            "created": f.get("创建日期", ""), "finished": f.get("完成日期", ""),
        })
    counts = {s: sum(1 for i in items if i["status"] == s) for s in STATUSES}
    lines = ["> 由 `python tools/todo.py sync` 自动生成，手改会被覆盖。", ""]
    if not items:
        lines.append("暂无待办文件——用 `python tools/todo.py new \"标题\"` 创建第一条。")
        return "\n".join(lines) + "\n"
    lines.append(f"**统计**：待办 {counts['待办']} ｜ 进行中 {counts['进行中']} ｜ 已完成 {counts['已完成']} ｜ 已取消 {counts['已取消']}（共 {len(items)}）")
    pending = sorted((i for i in items if i["status"] in ("待办", "进行中")),
                     key=lambda i: (i["created"], i["path"].name))
    if pending:
        lines += ["", "**未完成**（按创建日期，早的在前）：", "",
                  "| 编号 | 标题 | 优先级 | 状态 | 创建日期 |", "| --- | --- | --- | --- | --- |"]
        for i in pending:
            lines.append(f"| [{i['code']}]({i['path'].name}) | {i['title']} | {i['priority']} | {i['status']} | {i['created']} |")
    done = sorted((i for i in items if i["status"] == "已完成"),
                  key=lambda i: (i["finished"], i["path"].name), reverse=True)[:5]
    if done:
        lines += ["", "**最近完成**（最新 5 条）：", "",
                  "| 编号 | 标题 | 完成日期 |", "| --- | --- | --- |"]
        for i in done:
            lines.append(f"| [{i['code']}]({i['path'].name}) | {i['title']} | {i['finished']} |")
    return "\n".join(lines) + "\n"


def sync() -> None:
    block = build_block()
    text = INDEX.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        die(f"{INDEX} 缺少 {BEGIN}/{END} 标记")
    pre, _, rest = text.partition(BEGIN)
    _, _, post = rest.partition(END)
    INDEX.write_text(pre.rstrip("\n") + "\n\n" + BEGIN + "\n" + block + END + post.lstrip("\n"),
                     encoding="utf-8", newline="\n")


def cmd_new(args) -> None:
    if args.priority not in PRIORITIES:
        die(f"优先级必须是 {'/'.join(PRIORITIES)}，收到：{args.priority}")
    today = date.today()
    prefix = f"TB-{today:%Y%m%d}-"
    seq = max((int(FILE_RE.match(p.name).group(2)) for p in todos() if p.name.startswith(prefix)), default=0) + 1
    title = sanitize(args.title)
    if not title:
        die("标题为空（或清洗后为空）")
    path = TODO_DIR / f"{prefix}{seq:02d}-{title}.md"
    desc = (args.desc or "一句话说明").strip()
    dod = [i.strip() for i in (args.dod or []) if i.strip()]
    dod_lines = "\n".join(f"- [ ] {i}" for i in dod) or "- [ ] 达到什么程度算完成"
    body = (
        f"# 📌 {args.title.strip()}\n\n"
        f"> {desc}\n\n"
        f"## 📋 完成标准\n\n"
        f"{dod_lines}\n\n"
        f"## 📝 进展记录\n\n"
        f"- {today.isoformat()} 创建。\n"
    )
    fm = f"status: 待办\n优先级: {args.priority}\n创建日期: {today.isoformat()}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8", newline="\n")
    sync()
    print(f"[新建] {path.name}")


def _transition(code: str, new_status: str, log_word: str) -> None:
    path = find(code)
    d = load(path)
    if d["raw"] is None:
        die(f"{path.name} 缺文件头（frontmatter）")
    today = date.today().isoformat()
    fm = set_field(d["raw"], "status", new_status)
    body = append_log(d["body"], f"{today} {log_word}。")
    if new_status == "已完成":
        fm = set_field(fm, "完成日期", today)
    save(path, fm, body)
    sync()
    print(f"[{new_status}] {path.name}")


def cmd_cancel(args) -> None:
    path = find(args.code)
    d = load(path)
    if d["raw"] is None:
        die(f"{path.name} 缺文件头（frontmatter）")
    reason = " ".join(args.reason).strip() or "主动取消"
    fm = set_field(d["raw"], "status", "已取消")
    body = append_log(d["body"], f"{date.today().isoformat()} 取消：{reason}。")
    save(path, fm, body)
    sync()
    print(f"[已取消] {path.name}")


REQ_PRIORITIES = ("必须", "应该", "可以", "暂不")


def cmd_convert(args) -> None:
    if args.priority not in REQ_PRIORITIES:
        die(f"转需求优先级必须是 {'/'.join(REQ_PRIORITIES)}（MoSCoW），收到：{args.priority}")
    path = find(args.code)
    d = load(path)
    if d["raw"] is None:
        die(f"{path.name} 缺文件头（frontmatter）")
    if d["fields"].get("status") in ("已完成", "已取消"):
        die(f"{path.name} 已是终态（{d['fields'].get('status')}），不能转需求")
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "req.py"), "new", title_of(path),
         "--from", args.code, "-p", args.priority, "--print-code"],
        capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        die(f"req.py 建需求失败：{(r.stdout + r.stderr).strip()}")
    req_code = r.stdout.strip().splitlines()[-1]
    today = date.today().isoformat()
    fm = set_field(set_field(d["raw"], "status", "已完成"), "完成日期", today)
    body = append_log(d["body"], f"{today} 转需求 {req_code}，由需求池跟踪。")
    save(path, fm, body)
    sync()
    print(f"[转需求] {path.name} → {req_code}（待办记为已完成，进展已回写编号）")


def validate() -> int:
    problems = []
    for p in todos():
        d = load(p)
        f = d["fields"]
        if d["raw"] is None:
            problems.append(f"{p.name}: 缺文件头")
            continue
        if f.get("status") not in STATUSES:
            problems.append(f"{p.name}: status 非法（{f.get('status', '缺失')}）")
        if f.get("优先级") not in PRIORITIES:
            problems.append(f"{p.name}: 优先级非法（{f.get('优先级', '缺失')}）")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", f.get("创建日期", "")):
            problems.append(f"{p.name}: 创建日期缺失或格式错")
        if f.get("status") == "已完成" and not f.get("完成日期"):
            problems.append(f"{p.name}: 已完成但缺完成日期")
        if f.get("status") != "已完成" and f.get("完成日期"):
            problems.append(f"{p.name}: 未完成却带完成日期")
        if "## 📋 完成标准" not in d["body"]:
            problems.append(f"{p.name}: 缺完成标准节")
        if re.search(r"^> 一句话说明$", d["body"], re.M):
            problems.append(f"{p.name}: 一句话说明未填写（new -d 或手工补）")
        if re.search(r"^- \[ \] 达到什么程度算完成$", d["body"], re.M):
            problems.append(f"{p.name}: 完成标准未填写（new --dod 或手工补）")
    if BEGIN not in INDEX.read_text(encoding="utf-8"):
        problems.append("index.md 缺汇总区块标记")
    elif build_block().rstrip("\n") not in INDEX.read_text(encoding="utf-8"):
        problems.append("汇总区块与文件状态不同步，请执行 python tools/todo.py sync")
    counts = {s: 0 for s in STATUSES}
    for p in todos():
        counts[load(p)["fields"].get("status", "?")] = counts.get(load(p)["fields"].get("status", "?"), 0) + 1
    print(f"待办文件: {len(todos())} | 待办 {counts['待办']} / 进行中 {counts['进行中']} / "
          f"已完成 {counts['已完成']} / 已取消 {counts['已取消']} | 问题: {len(problems)}")
    for x in problems:
        print("  " + x)
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="待办项管理：单文件单待办，状态自动流转")
    sub = ap.add_subparsers(dest="cmd")
    p_new = sub.add_parser("new", help="新建待办")
    p_new.add_argument("title", help="待办标题")
    p_new.add_argument("-p", "--priority", default="中", help="优先级：高/中/低")
    p_new.add_argument("-d", "--desc", help="一句话说明（缺省留占位符，校验会提示未填）")
    p_new.add_argument("--dod", action="append", metavar="标准",
                       help="完成标准一条，可重复传入；缺省留占位符")
    p_start = sub.add_parser("start", help="待办 → 进行中")
    p_start.add_argument("code", help="编号，如 TB-20260917-01")
    p_done = sub.add_parser("done", help="标记完成（自动写日期+进展+刷新汇总）")
    p_done.add_argument("code", help="编号，如 TB-20260918-01")
    p_cancel = sub.add_parser("cancel", help="取消（留档）")
    p_cancel.add_argument("code", help="编号，如 TB-20260918-01")
    p_cancel.add_argument("reason", nargs="*", help="取消原因")
    p_conv = sub.add_parser("convert", help="转需求：自动在需求池建 REQ 条目并双向回写编号")
    p_conv.add_argument("code", help="编号，如 TB-20260918-01")
    p_conv.add_argument("-p", "--priority", default="应该", help="需求优先级（MoSCoW）：必须/应该/可以/暂不")
    sub.add_parser("sync", help="重新生成汇总区块")
    args = ap.parse_args()
    if args.cmd == "new":
        cmd_new(args)
        return 0
    if args.cmd == "start":
        _transition(args.code, "进行中", "开始推进")
        return 0
    if args.cmd == "done":
        _transition(args.code, "已完成", "完成")
        return 0
    if args.cmd == "cancel":
        cmd_cancel(args)
        return 0
    if args.cmd == "convert":
        cmd_convert(args)
        return 0
    if args.cmd == "sync":
        sync()
        print("[已刷新] 06-todos/index.md 汇总区块")
        return 0
    return validate()


if __name__ == "__main__":
    sys.exit(main())
