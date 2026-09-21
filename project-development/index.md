# 🏗️ 项目开发 · 开发规范体系

> 以业界最流行的工程规范为基线，把一个需求从提出到评审合入的完整生命周期做成**可检查、可追溯、可回流**的闭环。每个阶段都有：**准入条件（DoR）→ 核心规范 → 产出物 → 质量门禁（DoD）→ 衔接下一阶段**；问题与改进项经 [06 待办项](/project-development/06-todos/index.md) 回流。

## 🔄 闭环总图

```
          ┌──────────────────────────────────────────────────────────────┐
          │                ② 改进回流（长环，经 06 待办项）                  │
          │          问题/改进项登记待办项 → 转需求池 → 开启下一轮迭代         │
          ▼                                                              │
  ┌─ 01 需求管理 ─┐   ┌─ 02 设计架构 ─┐   ┌─ 03 编码规范 ─┐   ┌─ 04 测试规范 ─┐
  │ 需求池/评审    │ → │ 方案/ADR     │ → │ 编码+自测     │ → │ 分层测试     │
  └──────────────┘   └──────────────┘   └──────▲──────┘   └──────┬───────┘
                                             │ ① 打回：缺陷单/评审意见  │
                                             └───────────┐           ▼
                                                  ┌─ 05 代码评审 ─┐ ←────────┘
                                                  │ PR/清单      │
                                                  └──────┬───────┘
                                                         ▼
                                                  评审通过，合入主干（链路收口）
```

- **主链路**：01 → 02 → 03 → 04 → 05，每一步都有质量门禁，不达标不流入下一阶段；评审通过合入主干即链路收口。
- **打回环（短）**：04 测试缺陷单 / 05 评审意见 → 回到 03 编码修复（先补复现用例）。
- **改进环（长）**：问题与改进项登记进 [06 待办项](/project-development/06-todos/index.md)，有价值的转回 01 需求池，形成闭环。

## 🗺️ 阶段导航

| 阶段 | 文档 | 核心问题 | 关键产出 | 参考的主流规范 |
| --- | --- | --- | --- | --- |
| 00 🗺️ | [闭环流程总览](/project-development/00-process-overview.md) | 整个流程怎么转？ | 全景图、准入/准出矩阵 | Scrum |
| 01 📥 | [需求管理](/project-development/01-requirements/index.md) | 做什么？为什么做？ | 需求池、用户故事、验收标准 | 用户故事 / INVEST / RICE |
| 01+ 🗃️ | [需求池](/project-development/01-requirements/backlog.md) | 本仓自身的改进需求怎么跟踪？ | REQ 条目、状态流转、来源可溯 | 单文件单需求 / MoSCoW |
| 02 📐 | [设计架构](/project-development/02-design/index.md) | 怎么做？用什么做？ | 技术方案、ADR、接口契约 | C4 模型 / DDD 分层 / RESTful |
| 02+ 🧩 | [通用设计方案库](/project-development/02-design/solution-catalog.md) | 常见场景的成熟方案怎么选？ | 12 个方案货架 + 四套常用组合 | 幂等 / 缓存 / MQ / 状态机 / 对账 |
| 03 ✍️ | [编码规范](/project-development/03-coding-standards/index.md) | 怎么写得对、写得好看？ | 可维护的代码 | Clean Code / Google / 阿里手册 / PEP 8 / Airbnb |
| 03+ 🌿 | [Git 提交与分支规范](/project-development/03-coding-standards/git-conventions.md) | 怎么协作与留痕？ | 规范的提交历史 | Conventional Commits / GitHub Flow |
| 03+ 🧭 | [技术栈基线](/project-development/03-coding-standards/index.md#tech-stack) | 默认用什么做？ | 前后端选型基线、轻量/重量分档 | 单包即起 / 升级触发线 / ADR |
| 04 🧪 | [测试规范](/project-development/04-testing/index.md) | 怎么证明它是对的？ | 分层测试、覆盖率达标 | 测试金字塔 / FIRST / AAA |
| 05 👀 | [代码评审](/project-development/05-code-review/index.md) | 怎么守住质量与一致性？ | 通过评审的 PR | Google eng-practices |
| 06 📌 | [待办项](/project-development/06-todos/index.md) | 事情记在哪？怎么跟踪到关闭？ | 单文件单待办、状态自动流转、汇总看板 | 编号-状态-日期约定 / DoD |
| 10 👥 | [虚拟团队](/project-development/10-virtual-team/index.md) | 规范谁来执行？ | 4 角色子智能体 + 交接物契约 + 打回机制 | RACI / 契约式协作 |

## 📖 使用方式

1. **新项目启动**：从 00 总览通读一遍，把各阶段准入/准出清单作为项目管理基线。
2. **日常开发**：每次提交前过一遍 [03](/project-development/03-coding-standards/index.md#dod) / [04](/project-development/04-testing/index.md#dod) / [05](/project-development/05-code-review/index.md#dod) 的检查清单。
3. **记事与跟踪**：问题、改进项、临时任务一律进 [06 待办项](/project-development/06-todos/index.md)——`python tools/todo.py new "标题"` 建单，完成后 `python tools/todo.py done <编号>` 自动流转状态并刷新汇总；值得排期的改进 `python tools/todo.py convert <编号>` 自动转进 [需求池](/project-development/01-requirements/backlog.md)。
4. **单人项目**：流程不省略，只简化——评审可改为自评（隔天看自己的 diff）；或把四个角色交给子智能体执行（见 [10-虚拟团队](/project-development/10-virtual-team/index.md)）。
5. **规范冲突**：团队已有规范优先于本仓；本仓用于个人默认基线与无规范时的兜底。
