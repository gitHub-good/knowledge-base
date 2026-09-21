#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工具链自测：sanitize / 待办全流程 / convert 转需求 / 安装脚本幂等。

用法（在仓库任意位置）：
    python tools/test_tools.py          # 或 python3 -m unittest discover -s tools

只用标准库，不起真实仓库改动：待办流程跑在临时目录的迷你仓库里，
安装脚本跑在临时 HOME 里（install.py 经 Path.home() 读 HOME 环境变量）。
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
PY = sys.executable

sys.path.insert(0, str(TOOLS))
import todo  # noqa: E402
import req   # noqa: E402


def run(cwd: Path, *args: str, home: Path | None = None):
    env = dict(os.environ)
    if home is not None:
        env["HOME"] = str(home)
    return subprocess.run([PY, *args], cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", env=env)


def make_fake_repo(base: Path) -> Path:
    """最小可用的知识库骨架：tools 两脚本 + 两处汇总标记。"""
    fake = base / "repo"
    (fake / "tools").mkdir(parents=True)
    shutil.copy(TOOLS / "todo.py", fake / "tools" / "todo.py")
    shutil.copy(TOOLS / "req.py", fake / "tools" / "req.py")
    idx = fake / "project-development" / "06-todos" / "index.md"
    idx.parent.mkdir(parents=True)
    idx.write_text("# 📌 06 · 待办项\n\n## 📊 汇总看板\n\n<!-- todos:begin -->\n<!-- todos:end -->\n",
                   encoding="utf-8")
    pool = fake / "project-development" / "01-requirements" / "backlog.md"
    pool.parent.mkdir(parents=True)
    pool.write_text("# 🗃️ 需求池\n\n## 📊 汇总看板\n\n<!-- reqpool:begin -->\n<!-- reqpool:end -->\n",
                    encoding="utf-8")
    return fake


class TestSanitize(unittest.TestCase):
    def test_todo_req_同款白名单(self):
        for mod in (todo, req):
            self.assertEqual(mod.sanitize("修复 bug(紧急) ~x"), "修复-bug-紧急-x")
            self.assertEqual(mod.sanitize("  a///b::c  "), "a-b-c")
            self.assertEqual(mod.sanitize("需求：改~进（二）"), "需求-改-进-二")
            self.assertEqual(mod.sanitize("---t---"), "t")


class TestTodoFlow(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.fake = make_fake_repo(Path(self._tmp.name))
        self.todo = ["tools/todo.py"]

    def tearDown(self):
        self._tmp.cleanup()

    def code(self) -> str:
        out = run(self.fake, *self.todo, "new", "全流程验证-(x)", "-d", "验证建单到关闭的状态与目录流转",
                  "--dod", "文件落 pending/ 且字段齐全", "--dod", "流转后目录与状态一致")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        import re
        m = re.search(r"TB-\d{8}-\d{2}", out.stdout)
        self.assertTrue(m, out.stdout)
        return m.group(0)

    def test_建单_流转_校验(self):
        code = self.code()
        todo_dir = self.fake / "project-development" / "06-todos" / "todo"
        self.assertTrue((todo_dir / "pending" / f"{code}-全流程验证-x.md").is_file())
        body = (todo_dir / "pending" / f"{code}-全流程验证-x.md").read_text(encoding="utf-8")
        self.assertIn("> 验证建单到关闭的状态与目录流转", body)
        self.assertIn("- [ ] 文件落 pending/ 且字段齐全", body)

        self.assertEqual(run(self.fake, *self.todo, "start", code).returncode, 0)
        self.assertTrue((todo_dir / "doing" / f"{code}-全流程验证-x.md").is_file())
        self.assertEqual(run(self.fake, *self.todo, "done", code).returncode, 0)
        done_file = todo_dir / "done" / f"{code}-全流程验证-x.md"
        self.assertTrue(done_file.is_file())
        self.assertIn("完成日期:", done_file.read_text(encoding="utf-8"))

        out = run(self.fake, *self.todo)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("问题: 0", out.stdout)

    def test_期限字段与过期点名(self):
        out = run(self.fake, *self.todo, "new", "期限验证", "--deadline", "2000-01-01")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        out = run(self.fake, *self.todo)
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn("已过期限", out.stdout)

    def test_convert_转需求并回写(self):
        code = self.code()
        out = run(self.fake, *self.todo, "convert", code, "-p", "应该")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        req_dir = self.fake / "project-development" / "01-requirements"
        reqs = list(req_dir.glob("REQ-*.md"))
        self.assertEqual(len(reqs), 1)
        head = reqs[0].read_text(encoding="utf-8")
        self.assertIn(f"来源: {code}", head)
        self.assertIn("REQ-", out.stdout)
        done_file = (self.fake / "project-development" / "06-todos" / "todo" / "done"
                     / f"{code}-全流程验证-x.md")
        self.assertIn("转需求 REQ-", done_file.read_text(encoding="utf-8"))
        self.assertEqual(run(self.fake, "tools/req.py").returncode, 0)


class TestInstall(unittest.TestCase):
    def setUp(self):
        self._home = tempfile.TemporaryDirectory()

    def tearDown(self):
        self._tmp_home = Path(self._home.name)
        link = self._tmp_home / "knowledge-base"
        if link.is_symlink():
            link.unlink()  # TemporaryDirectory 清不掉指向仓库的软链接，先摘掉
        self._home.cleanup()

    def test_安装与幂等(self):
        home = Path(self._home.name)
        install = str(ROOT / ".zcode/skills/virtual-team-setup/install.py")
        first = run(ROOT, install, home=home)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        agents_md = home / ".zcode" / "AGENTS.md"
        text = agents_md.read_text(encoding="utf-8")
        self.assertIn("## 虚拟团队子智能体", text)
        self.assertIn("## 编辑文件规范", text)
        for role in ("product-manager", "architect", "developer", "tester"):
            self.assertTrue((home / ".zcode" / "agents" / f"{role}.md").is_file())
        self.assertTrue((home / "knowledge-base" / "AGENTS.md").is_file())

        second = run(ROOT, install, home=home)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(agents_md.read_text(encoding="utf-8"), text)  # 逐字节幂等
        self.assertIn("无变化", second.stdout)


class TestLoaderSync(unittest.TestCase):
    def test_装载器无漂移(self):
        """仓库级 .zcode/agents/ 与技能 templates/ 必须逐行对齐（路径策略差异豁免）。"""
        out = run(ROOT, str(ROOT / ".zcode/skills/virtual-team-setup/install.py"), "--check-sync")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
