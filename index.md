# 🏠 个人知识库

> 个人工作与知识的单一信源（Single Source of Truth）：左边管「怎么做项目」，右边管「怎么高效工作」。

## 📦 仓库定位

| 板块 | 定位 | 一句话说明 |
| --- | --- | --- |
| 🏗️ [项目开发](./project-development/index.md) | 开发规范体系 | 以业界最流行的工程规范为基线，覆盖 **需求 → 设计 → 编码 → 测试 → 评审** 五阶段闭环，问题与改进项经待办项回流 |
| 🧰 [个人助手](./personal-assistant/index.md) | 个人工作知识库 | 工作中高频使用的命令速查、工作模板、踩坑记录，随用随查、随踩随记 |

## 🗂️ 目录结构

```
个人知识库/
├── index.md                  # 本文件：总览与导航
├── AGENTS.md                 # 仓库级 AI 指令：所有会话遵循《编辑文件规范》
├── .zcode/agents/            # 角色装载器（仓库级副本；用户级在 ~/.zcode/agents/）
├── .zcode/skills/            # 技能：virtual-team-setup（换机一键重装虚拟团队）
├── 🏗️ project-development/                  # ── 板块一：开发规范（闭环体系）──
│   ├── index.md              # 板块导航 + 闭环总图
│   ├── 00-process-overview.md      # 五阶段闭环详解：准入/准出/反馈回路
│   ├── 01-requirements/           # 需求收集、用户故事、优先级、需求池
│   ├── 02-design/           # 分层架构、C4、ADR、通用设计方案库
│   ├── 03-coding-standards/           # 通用编码规范 + Git 规范 + 前后端技术栈
│   ├── 04-testing/           # 测试金字塔、覆盖率标准、缺陷管理
│   ├── 05-code-review/           # PR 规范、评审清单、评审礼仪
│   ├── 06-todos/             # 单文件单待办：状态自动流转 + 汇总看板
│   └── 10-virtual-team/           # 6 角色子智能体（调研/PM/架构/UI/开发/测试）+ 协作机制
├── 🧰 personal-assistant/                  # ── 板块二：个人工作知识 ──
    ├── index.md              # 板块导航与使用约定
    ├── commands/              # Git / Linux / Windows / Docker 速查
    ├── templates/              # 周报、会议纪要、技术方案、新电脑环境清单
    ├── standards/              # 编辑文件规范（跨会话自动生效）
    └── lessons-learned/         # 踩坑记录（持续追加）
└── tools/
    ├── check_links.py        # 链接与锚点校验：python tools/check_links.py
    ├── req.py                # 需求池流转：python tools/req.py
    ├── todo.py               # 待办项流转：python tools/todo.py
    └── test_tools.py         # 工具自测（提交门禁/CI 同款）：python tools/test_tools.py
```

## 🚀 快速入口

- 🗺️ **启动一个新项目** → 从 [00-闭环流程总览](./project-development/00-process-overview.md#stage-map) 开始，按阶段走完[准入/准出矩阵](./project-development/00-process-overview.md#gating-matrix)
- ✍️ **写代码前** → [03-编码规范](./project-development/03-coding-standards/index.md) + [Git 提交与分支规范](./project-development/03-coding-standards/git-conventions.md)
- 🧪 **提测 / 提 PR 前** → [04 测试的检查清单](./project-development/04-testing/index.md#dod) + [05 评审的检查清单](./project-development/05-code-review/index.md#dod)
- 📌 **记/查待办** → [06-待办项](./project-development/06-todos/index.md)：单文件单待办，`python tools/todo.py` 新建/完成自动流转状态
- 💻 **忘了命令怎么写** → [Git](./personal-assistant/commands/git-commands.md) / [Linux](./personal-assistant/commands/linux-commands.md) / [Windows](./personal-assistant/commands/windows-commands.md) / [Docker](./personal-assistant/commands/docker-commands.md) 命令速查
- 📚 **技术选型 / 搭新项目** → [前后端技术栈](./project-development/03-coding-standards/index.md)：默认选型 + 工程基线（偏离默认记 ADR）
- 📅 **填周报 / 写方案** → [周报](./personal-assistant/templates/weekly-report.md) / [会议纪要](./personal-assistant/templates/meeting-minutes.md) / [技术方案](./personal-assistant/templates/technical-design.md) 模板
- ✏️ **要新建/改文件前** → 先读 [编辑文件规范](./personal-assistant/standards/editing-standards.md)（所有会话默认生效）
- 👥 **要拉起虚拟团队干活** → [10-虚拟团队](./project-development/10-virtual-team/index.md)：六角色子智能体 + 交接物契约

## 🔧 维护约定

1. ✍️ **随手更新**：解决一个新问题、踩一个新坑，当天就补进 `personal-assistant/lessons-learned/`，别攒。
2. 📏 **规范先行**：新学到的业界规范（如新版风格指南），先更新对应阶段文档再落地到项目。
3. ♻️ **闭环收口**：问题与复盘产生的改进项，随手登记进 [06-待办项](./project-development/06-todos/index.md) 跟踪，直至关闭。
4. 🏷️ **命名约定**：目录与文档统一英文命名（小写+连字符，正文中文）；目录用 `编号-名称` 保持排序——细则见 [编辑文件规范](./personal-assistant/standards/editing-standards.md)。
5. 🌿 **提交规范**：本仓库自身的提交也遵循 [Conventional Commits](./project-development/03-coding-standards/git-conventions.md#commit-spec)，例如 `docs: 新增Docker命令速查`。
