#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把个人知识库的「虚拟团队」安装到用户级 ZCode 配置。

零环境变量方案：知识库约定位置 = `~/knowledge-base`（家目录下，Windows/Mac 通用），
本脚本负责在家目录维护指向真实仓库的链接（Windows junction / Unix 软链接）。

用法（知识库任意位置，仓库根自动推导）：
    python .zcode/skills/virtual-team-setup/install.py            # 安装/更新
    python .zcode/skills/virtual-team-setup/install.py --dry-run  # 只预览不写

做什么：
1. ~/.zcode/agents/   复制 templates/ 下四个角色装载器（引用 `~/knowledge-base/...` 约定路径）
2. ~/.zcode/AGENTS.md 幂等插入/替换「虚拟团队子智能体」与「编辑文件规范」章节
   （各自标记内替换），并把「知识库位置」一行统一改写为约定位置指引
3. ~/knowledge-base       家目录链接：缺失则自动创建，指向本仓库；存在但指错则警告
4. 自检：frontmatter、无 BOM、无盘符绝对路径、角色文档在位、约定位置可访问

退出码：有 FAIL = 1，全过 = 0。
"""
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_DIR = Path(__file__).resolve().parent
KB_ROOT = SKILL_DIR.parents[2]                      # .zcode/skills/<本技能> → 仓库根
TEMPLATES = SKILL_DIR / "templates"
AGENTS_DIR = Path.home() / ".zcode" / "agents"
AGENTS_MD = Path.home() / ".zcode" / "AGENTS.md"
HOME_LINK = Path.home() / "knowledge-base"
SECTION_START = "<!-- virtual-team:start -->"
SECTION_END = "<!-- virtual-team:end -->"
HEADING = "## 虚拟团队子智能体（所有工作区生效）"
STD_START = "<!-- kb-standards:start -->"
STD_END = "<!-- kb-standards:end -->"
STD_HEADING = "## 编辑文件规范（所有工作区生效）"
KB_HINT = "知识库位置 = `~/knowledge-base`（家目录约定位置，Windows/Mac 通用；迁移后放回即零配置）"
SECTION_HINT = "知识库约定位置 = `~/knowledge-base`"  # 章节模板必含表述；自检以它为准（KB_HINT 仅为历史行改写目标）
ROLE_DOCS = ["product-manager.md", "architect.md", "developer.md", "tester.md"]
AGENT_NAMES = ["product-manager", "architect", "developer", "tester"]


def die(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def read_text(p: Path) -> str:
    return p.read_bytes().decode("utf-8-sig")


def ensure_home_link(dry: bool) -> bool:
    """确保 ~/knowledge-base 指向本仓库；返回约定位置是否可正常访问。"""
    if HOME_LINK.exists():
        if HOME_LINK.resolve() == KB_ROOT.resolve():
            print(f"[已就绪] 约定位置 {HOME_LINK} → 本仓库")
            return True
        print(f"[警告] {HOME_LINK} 已存在但不指向本仓库（现指向 {HOME_LINK.resolve()}），请手工处理")
        return False
    try:
        os.listdir(HOME_LINK)
    except OSError:
        try:
            os.rmdir(HOME_LINK)
            print(f"[清理] 悬空的家目录链接 {HOME_LINK}")
        except OSError:
            pass
    if dry:
        print(f"[将创建] 家目录链接 {HOME_LINK} → {KB_ROOT}")
        return False
    ok = False
    if sys.platform == "win32":
        # junction 不需要管理员权限；输出为 GBK，字节模式只看退出码
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(HOME_LINK), str(KB_ROOT)],
                           capture_output=True)
        ok = r.returncode == 0
    else:
        try:
            HOME_LINK.symlink_to(KB_ROOT, target_is_directory=True)
            ok = True
        except Exception as e:
            print(f"[提示] 创建软链接失败：{e}")
    if ok:
        print(f"[已创建] 家目录链接 {HOME_LINK} → {KB_ROOT}")
    else:
        print(f"[提示] 未能自动创建链接，请手动执行：mklink /J \"{HOME_LINK}\" \"{KB_ROOT}\""
              f"（Unix：ln -s \"{KB_ROOT}\" \"{HOME_LINK}\"）")
    return ok


def merge_section(current: str, body: str, start: str, end: str, heading: str) -> str:
    body = body.rstrip("\n")  # 模板尾换行统一由下面控制，保证重跑结果逐字节一致
    if start in current or end in current:
        pre, _, rest = current.partition(start)
        _, _, post = rest.partition(end)
        pre = pre.rstrip("\n") + "\n\n"
        after = post.strip("\n")
        result = pre + body + "\n"
        if after:  # 标记后还有别的章节，留一个空行分隔
            result += "\n" + after + "\n"
        return result
    legacy = re.compile(rf"^{re.escape(heading)}.*?(?=^## |\Z)", re.S | re.M)
    if legacy.search(current):
        return legacy.sub(lambda _: body + "\n", current)
    return current.rstrip("\n") + "\n\n" + body + "\n"


def update_agents_md(current: str, vt_section: str, std_section: str) -> str:
    # 「知识库位置」行统一为约定位置指引（兼容历史写法，幂等）
    current = re.sub(r"知识库默认位置\s*`[^`]+`，仓库迁移后更新这一行即可", lambda _: KB_HINT, current)
    current = re.sub(r"知识库位置 = `~/knowledge-base`（家目录约定位置，迁移后放回即零配置）", lambda _: KB_HINT, current)
    current = re.sub(r"知识库位置 = `~/个人知识库`（[^）]*）", lambda _: KB_HINT, current)
    current = re.sub(r"知识库位置 = 环境变量 `KB_ROOT`（[^）]*）", lambda _: KB_HINT, current)
    if len(re.findall(r"^## 虚拟团队子智能体", current, re.M)) > 1:
        die("~/.zcode/AGENTS.md 里「虚拟团队」章节出现多次，请先手工清理再重跑")
    current = merge_section(current, vt_section, SECTION_START, SECTION_END, HEADING)
    return merge_section(current, std_section, STD_START, STD_END, STD_HEADING)


def check_sync() -> int:
    """逐行比对仓库级装载器与安装模板；路径策略类语境差异豁免，其余不一致报漂移。"""
    divergence_keys = ("~/knowledge-base", "仓库根", "Glob", "知识库约定位置", "知识库根相对",
                       "install.py", "AGENTS.md", "check_links", "编辑文件规范",
                       "工作目录", "工作区", "软链接", "mklink", "环境变量", "放回约定位置")
    drift = []
    for name in AGENT_NAMES:
        repo_lines = read_text(KB_ROOT / ".zcode" / "agents" / f"{name}.md").splitlines()
        tpl_lines = read_text(TEMPLATES / f"{name}.md").splitlines()
        if len(repo_lines) != len(tpl_lines):
            drift.append(f"{name}: 行数不一致（仓库级 {len(repo_lines)} 行 / 模板 {len(tpl_lines)} 行），需人工对齐结构")
            continue
        for i, (a, b) in enumerate(zip(repo_lines, tpl_lines), 1):
            if a != b and not any(k in a or k in b for k in divergence_keys):
                drift.append(f"{name} 第 {i} 行疑似漂移：\n    仓库级: {a}\n    模板  : {b}")
    if drift:
        for d in drift:
            print(f"FAIL: {d}")
        print("路径策略类差异已自动豁免；以上为内容漂移，请先改角色文档再同步两处装载器。")
        return 1
    print("装载器一致性校验通过（仓库级 .zcode/agents/ 与技能 templates/ 逐行对齐，路径策略类差异已豁免）。")
    return 0


def main() -> int:
    dry = "--dry-run" in sys.argv

    if not (KB_ROOT / "AGENTS.md").is_file() or not (KB_ROOT / "project-development" / "10-virtual-team").is_dir():
        die(f"仓库根识别失败（应含 AGENTS.md 与 project-development/10-virtual-team/）：{KB_ROOT}")
    print(f"仓库根: {KB_ROOT}")

    if "--check-sync" in sys.argv:
        return check_sync()

    # ① 装载器（模板原样复制，引用 ~/knowledge-base 约定路径）
    for name in AGENT_NAMES:
        tpl = TEMPLATES / f"{name}.md"
        if not tpl.is_file():
            die(f"缺少模板: {tpl}")
        content = tpl.read_text(encoding="utf-8")
        if "{{" in content:
            die(f"模板含残留占位符: {tpl.name}（本安装器不做变量渲染，请清理模板）")
        if not content.startswith("---\n") or f"name: {name}\n" not in content.split("---")[1]:
            die(f"模板 frontmatter 异常: {tpl.name}（应为 name: {name}）")
        target = AGENTS_DIR / f"{name}.md"
        if target.exists() and read_text(target) == content:
            print(f"[无变化] {target}")
        else:
            action = "更新" if target.exists() else "新建"
            if not dry:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8", newline="\n")
            print(f"[{'将写入' if dry else '写入'}] {target}（{action}）")

    # ② AGENTS.md 章节（虚拟团队 + 编辑文件规范）
    section_tpl = TEMPLATES / "AGENTS-section.md"
    if not section_tpl.is_file():
        die(f"缺少模板: {section_tpl}")
    section = section_tpl.read_text(encoding="utf-8")
    if "{{" in section:
        die("AGENTS-section.md 模板含残留占位符，请清理")
    std_tpl = TEMPLATES / "standards-section.md"
    if not std_tpl.is_file():
        die(f"缺少模板: {std_tpl}")
    std_section = std_tpl.read_text(encoding="utf-8")
    if "{{" in std_section:
        die("standards-section.md 模板含残留占位符，请清理")
    if not dry and not AGENTS_MD.exists():
        AGENTS_MD.parent.mkdir(parents=True, exist_ok=True)
        AGENTS_MD.write_text("# 个人全局指令\n", encoding="utf-8", newline="\n")
    current = read_text(AGENTS_MD) if AGENTS_MD.exists() else "# 个人全局指令\n"
    updated = update_agents_md(current, section, std_section)
    if updated == current:
        print(f"[无变化] {AGENTS_MD}（章节与约定位置指引已是最新）")
    else:
        mode = "替换" if SECTION_START in current or HEADING in current else "追加"
        if not dry:
            AGENTS_MD.write_text(updated, encoding="utf-8", newline="\n")
        print(f"[{'将写入' if dry else '写入'}] {AGENTS_MD}（虚拟团队 + 编辑文件规范章节：{mode}；知识库位置指引：~/knowledge-base）")

    # ③ 家目录约定位置链接
    link_ok = ensure_home_link(dry)

    # ④ 自检（只读检查，dry-run 也执行文件在位检查）
    fails = []
    if not dry:
        for name in AGENT_NAMES:
            p = AGENTS_DIR / f"{name}.md"
            data = p.read_bytes()
            if data.startswith(b"\xef\xbb\xbf"):
                fails.append(f"{p.name} 带 BOM")
            if not data.decode("utf-8").startswith("---\n"):
                fails.append(f"{p.name} 缺 frontmatter")
            if re.search(r"[A-Za-z]:[/\\]", data.decode("utf-8")):
                fails.append(f"{p.name} 含盘符绝对路径（应引用 ~/knowledge-base 约定路径）")
        agents_md_text = read_text(AGENTS_MD)
        if SECTION_START not in agents_md_text or SECTION_END not in agents_md_text:
            fails.append("AGENTS.md 章节标记缺失")
        if len(re.findall(r"^## 虚拟团队子智能体", agents_md_text, re.M)) != 1:
            fails.append("AGENTS.md 虚拟团队章节数量不为一")
        if SECTION_HINT not in agents_md_text:
            fails.append("AGENTS.md 缺约定位置指引")
        if "KB_ROOT" in agents_md_text:
            fails.append("AGENTS.md 仍残留 KB_ROOT 旧指引")
        if STD_START not in agents_md_text or STD_END not in agents_md_text:
            fails.append("AGENTS.md 编辑规范章节标记缺失")
        if len(re.findall(r"^## 编辑文件规范", agents_md_text, re.M)) != 1:
            fails.append("AGENTS.md 编辑规范章节数量不为一")
        if not (HOME_LINK / "AGENTS.md").is_file():
            fails.append(f"约定位置 {HOME_LINK} 不可访问（链接未建立或指错）")
    for doc in ROLE_DOCS:
        if not (KB_ROOT / "project-development" / "10-virtual-team" / doc).is_file():
            fails.append(f"角色文档缺失: {doc}")

    print("-" * 46)
    if fails:
        for f in fails:
            print(f"FAIL: {f}")
        return 1
    print("自检全过。重启 ZCode 会话生效；「设置 → 子智能体」应显示四个角色。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
