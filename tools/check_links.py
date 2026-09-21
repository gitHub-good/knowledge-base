#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验个人知识库内所有 Markdown 的内部链接与显式锚点。

用法（在仓库任意位置）：
    python tools/check_links.py

规则：
- 跳过 http(s)/mailto 外链；只校验仓库内相对链接
- 带 #fragment 的链接，要求目标文件存在 <a id="fragment"></a>
- 围栏代码块与行内代码中的"伪链接"不参与校验
- 退出码：发现真实问题 = 1，全绿 = 0（可直接接入 CI / 提交前钩子）
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")


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
    for md in mds:
        rel = os.path.relpath(md, ROOT)
        for m in LINK_RE.finditer(extract_text(md)):
            target = m.group(2)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            total += 1
            path_part, _, fragment = target.partition("#")
            # root-relative (/xxx) → resolve from ROOT; else relative to file dir
            if path_part.startswith("/"):
                target_file = os.path.normpath(os.path.join(ROOT, path_part[1:]))
            elif not path_part:
                target_file = md
            else:
                target_file = os.path.normpath(os.path.join(os.path.dirname(md), path_part))
            if not os.path.exists(target_file):
                broken.append(f"[文件缺失] {rel} -> {target}")
                continue
            if fragment:
                frag_total += 1
                if f'id="{fragment}"' not in open(target_file, encoding="utf-8").read():
                    broken.append(f"[锚点缺失] {rel} -> {target}")

    print(f"文件数: {len(mds)} | 内部链接: {total} | 锚点跳转: {frag_total} | 问题: {len(broken)}")
    for b in broken:
        print("  " + b)
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
