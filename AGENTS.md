# 个人知识库 · 会话指令

本仓库内创建、编辑任何文件，**必须遵循《编辑文件规范》**：[personal-assistant/standards/editing-standards.md](./personal-assistant/standards/editing-standards.md)

速记（细则以规范原文为准）：

- 新建：UTF-8、目录与文件英文命名（小写+连字符，正文中文）；`# 图标 标题` + 一句话定位开头；落地后三处同步（目录索引 index.md / 板块导航表 / 根目录树）。
- 编辑：最小改动、风格跟随原文件；删除内容前先全局反向搜引用。
- 待办与需求：问题/改进/临时任务用 `python tools/todo.py`（new/start/done/cancel/convert/sync）管理——单文件单待办（`project-development/06-todos/`），完成自动写日期、记进展、刷新汇总；值得排期的用 `convert` 转入需求池（[backlog.md](./project-development/01-requirements/backlog.md)，[req.py](./tools/req.py) 管理）；勿手工改两处汇总区块。
- 链接：统一用**相对当前文件的链接**（`../目录/文件.md` 或 `./文件.md`），任何预览器点击直达；指向具体章节追加锚点 `#英文id`；改完执行 `python tools/check_links.py`，真实问题 0 才算完成。
- 图标语义、命名、DoD 清单见规范原文。
