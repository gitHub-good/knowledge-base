#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验个人知识库内所有 Markdown 的内部链接与显式锚点。

用法（在仓库任意位置）：
    python tools/check_links.py

规则：
- 跳过 http(s)/mailto 外链；只校验仓库内链接
- 链接目标支持相对当前文件的路径（./xxx、../xxx，编辑规范第 17 条）与旧仓库根相对路径（/xxx）
- 链接目标解析越出仓库根即报错（盘符绝对路径等）
- 指向目录的链接要求该目录含 index.md（编辑规范第 19 条）
- 带 #fragment 的链接，要求目标文件存在 <a id="fragment"></a>（围栏/行内代码中的不算数）
- 同一文件内 <a id> 不得重复
- 链接目标含空格视为问题（Markdown 解析会在空格处截断）
- 围栏代码块与行内代码中的"伪链接"不参与校验
- 退出码：发现真实问题 = 1，全绿 = 0（可直接接入 CI / 提交前钩子）
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
LOOSE_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
EXTERNAL = ("http://", "https://", "mailto:")


def extract_text(md_path: str) -> str:
    text = open(md_path, encoding="utf-8").read()
    text = re.sub(r"```.*?```", "", text, flags=re.S)   # 围栏代码块（含示例中的伪链接/伪锚点）
    text = re.sub(r"`[^`\n]*`", "", text)               # 行内代码
    return text


def main() -> int:
    mds = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != ".git"]
        mds += [os.path.join(dirpath, f) for f in files if f.endswith(".md")]

    broken, total, frag_total = [], 0, 0
    stripped_cache = {}

    def stripped(path: str) -> str:  # 去除代码块后的正文（锚点判定一律以此为准）
        if path not in stripped_cache:
            stripped_cache[path] = extract_text(path)
        return stripped_cache[path]

    for md in mds:
        rel = os.path.relpath(md, ROOT)
        text = stripped(md)
        # 同文件内锚点唯一性
        ids = re.findall(r'<a id="([^"]+)"', text)
        for i in sorted({x for x in ids if ids.count(x) > 1}):
            broken.append(f"[锚点重复] {rel} #{i}")
        # 含空格的链接目标（正常 LINK_RE 匹配不到，宽松正则单独检测）
        for m in LOOSE_LINK_RE.finditer(text):
            target = m.group(2)
            if not target.startswith(EXTERNAL) and re.search(r"\s", target):
                broken.append(f"[链接含空格] {rel} -> {target.strip()}")
        for m in LINK_RE.finditer(text):
            target = m.group(2)
            if target.startswith(EXTERNAL):
                continue
            total += 1
            path_part, _, fragment = target.partition("#")
            # 相对当前文件解析（编辑规范第 17 条）；/xxx 为旧根相对写法，仍兼容校验
            if path_part.startswith("/"):
                target_file = os.path.normpath(os.path.join(ROOT, path_part[1:]))
            elif not path_part:
                target_file = md
            else:
                target_file = os.path.normpath(os.path.join(os.path.dirname(md), path_part))
            if not (os.path.abspath(target_file) == os.path.abspath(ROOT)
                    or os.path.abspath(target_file).startswith(os.path.abspath(ROOT) + os.sep)):
                broken.append(f"[越出仓库] {rel} -> {target}")
                continue
            if os.path.isdir(target_file):
                if not os.path.isfile(os.path.join(target_file, "index.md")):
                    broken.append(f"[目录缺索引] {rel} -> {target}")
                continue
            if not os.path.exists(target_file):
                broken.append(f"[文件缺失] {rel} -> {target}")
                continue
            if fragment:
                frag_total += 1
                if f'id="{fragment}"' not in stripped(target_file):
                    broken.append(f"[锚点缺失] {rel} -> {target}")

    print(f"文件数: {len(mds)} | 内部链接: {total} | 锚点跳转: {frag_total} | 问题: {len(broken)}")
    for b in broken:
        print("  " + b)
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
