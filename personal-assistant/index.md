# 🧰 个人助手

> 个人工作中高频知识的快速入口。原则：**速查优先（30 秒找到）、踩坑必录（当天记录）、模板即用（复制就走）**。

## 🗺️ 分类导航

| 分类 | 内容 | 何时用 |
| --- | --- | --- |
| 💻 [常用命令](./commands/index.md) | Git / Linux / Windows / Docker 命令速查 | 手生、忘记参数时 |
| 📋 [工作模板](./templates/index.md) | 周报、会议纪要、技术方案、新电脑环境清单 | 周五写周报、开会、写方案、换电脑前 |
| 📏 [工作规范](./standards/index.md) | 编辑文件规范（跨会话自动生效） | 创建、编辑任何文件之前 |
| 🧠 [知识沉淀](./lessons-learned/index.md) | 踩坑记录（持续追加） | 排查问题前先搜一遍，避免二刷同款坑 |

## 🗂️ 目录

```
personal-assistant/
├── 💻 commands/
│   ├── index.md              # 速查索引：按场景挑文件
│   ├── git-commands.md        # 配置/日常/分支/撤销/救命
│   ├── linux-commands.md      # 文件/文本三剑客/进程/网络
│   ├── windows-commands.md        # PowerShell/CMD/GitBash 路径差异
│   └── docker-commands.md     # 镜像/容器/日志/清理/compose
├── 📋 templates/
│   ├── index.md              # 模板索引：复制即用
│   ├── weekly-report.md
│   ├── meeting-minutes.md
│   ├── new-machine-setup.md      # 新电脑环境清单（换机恢复流程）
│   └── technical-design.md       # 与 project-development/02-design 检查单对应
├── 📏 standards/
│   ├── index.md              # 规范索引：管"怎么做文件"
│   └── editing-standards.md       # 所有会话的文件创建/编辑统一规范
└── 🧠 lessons-learned/
    ├── index.md              # 沉淀入口与记录约定
    └── pitfall-records.md           # 一坑一条，按日期倒序追加
```

## 📖 使用约定

1. **先查后问**：遇到命令不确定、问题排查前，先在这里搜关键词（`grep -ri "关键词"` 或编辑器全局搜索）。
2. **当天记录**：每解决一个花掉超过 30 分钟的问题，就往 [踩坑记录](./lessons-learned/pitfall-records.md) 加一条——未来的自己会感谢现在的自己。
3. **模板不将就**：发现模板少了一栏、多了废话，当场改模板（提交信息用 `docs: 完善周报模板`）。
4. **链接回环**：踩坑记录里发现的流程性改进，回到 [项目开发](../project-development/index.md) 对应阶段去改规范——个人助手发现问题，项目开发固化规则。
