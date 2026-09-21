# 👥 10 · 虚拟团队（角色子智能体）

> 把 00~09 闭环规范从「纸上规范」变成「有人执行」：产品经理、架构设计师、开发工程师、测试工程师四个角色子智能体，以**交接物为接口**沿闭环协作。单人项目 = 一个编排者（主会话）+ 四个专家。

## 🗺️ 角色地图

| 角色 | 负责阶段 | 核心交付物 | 角色文档 | 子智能体定义 |
| --- | --- | --- | --- | --- |
| 📣 产品经理 | [01 需求管理](/project-development/01-requirements/index.md) | 冻结需求 + PRD | [product-manager.md](/project-development/10-virtual-team/product-manager.md) | `.zcode/agents/product-manager.md` |
| 🏛️ 架构设计师 | [02 设计架构](/project-development/02-design/index.md) | 技术方案 + ADR + 任务拆解 | [architect.md](/project-development/10-virtual-team/architect.md) | `.zcode/agents/architect.md` |
| 💻 开发工程师 | [03 编码](/project-development/03-coding-standards/index.md) + [05 评审](/project-development/05-code-review/index.md) | 合入主干的代码 + 测试 | [developer.md](/project-development/10-virtual-team/developer.md) | `.zcode/agents/developer.md` |
| 🧪 测试工程师 | [04 测试规范](/project-development/04-testing/index.md) | 测试报告 + 缺陷单 + Go/No-Go | [tester.md](/project-development/10-virtual-team/tester.md) | `.zcode/agents/tester.md` |

## 🔄 协作流程（交接物即接口）

```
主链路（沿闭环正向流动）：
原始诉求 → [PM] 冻结需求+PRD → [架构] 技术方案+ADR+任务拆解
        → [开发] 编码+自测+PR → [测试] 用例矩阵+测试报告
        → [评审] 合入主干（链路收口）
        → 问题/改进项记入 06 待办项 → 转需求池 → 回到 [PM]（闭环）

打回通道（逆向，凭交付物说话）：
  测试 → 开发：缺陷单（按 SLA 修复）
  测试 → PM  ：需求歧义单（验收标准不清）
  开发 → 架构：方案不可行单（更新 ADR 后继续）
  架构 → PM  ：需求退回单（验收标准不可测/依赖不明）
```

> 原则：**角色之间不闲聊，只交换交付物**——每份交付物都有模板、DoD 和存放位置，下游只认过 DoD 的东西。

## ⚖️ RACI 职责矩阵

> R=执行　C=被咨询　I=被告知

| 阶段 | 📣 PM | 🏛️ 架构 | 💻 开发 | 🧪 测试 |
| --- | --- | --- | --- | --- |
| 01 需求 | **R** | C（可行性） | C（工作量） | C（可测性） |
| 02 设计 | C（范围边界） | **R** | C（实现可行性） | C（可测性） |
| 03 编码 | I | C（方案答疑） | **R** | I |
| 04 测试 | C（验收标准澄清） | I | C（缺陷修复） | **R** |
| 05 评审 | I | C | **R** | C |
| 06 待办项 | C（转需求） | C | **R**（随手记） | C |

## 📦 交接物契约（每一步的接口定义）

| # | 从 → 到 | 交付物 | 模板与规范出处 | 通过标准 |
| --- | --- | --- | --- | --- |
| ① | PM → 架构 | 冻结需求条目 + 轻量 PRD | [01 需求管理](/project-development/01-requirements/index.md)「五、轻量 PRD 模板」 | [01 检查清单](/project-development/01-requirements/index.md) 全过：验收标准可测、≤2 人天、风险有对策 |
| ② | 架构 → 开发 | 技术方案 + ADR + 接口契约 + 任务拆解表 | [技术方案模板](/personal-assistant/templates/technical-design.md) + [通用设计方案库](/project-development/02-design/solution-catalog.md) | [设计评审清单](/project-development/02-design/index.md#design-review) 全过 |
| ③ | 开发 → 测试 | 提测单 + 代码分支 + 自测报告 | [Git 提交与分支规范](/project-development/03-coding-standards/git-conventions.md#commit-spec) | [03 DoD](/project-development/03-coding-standards/index.md#dod)：lint 0 error、增量覆盖 ≥80%、主路径/边界/异常自测通过 |
| ④ | 测试 → 全员 | 测试报告 + 缺陷单 + 上线建议 | [04 测试规范](/project-development/04-testing/index.md) | [04 DoD](/project-development/04-testing/index.md#dod)：用例全执行、无 P0/P1 遗留、修复均有回归用例 |
| ⑤ | 全员 → PM | 问题/改进项（登记 [06 待办项](/project-development/06-todos/index.md)，转需求池） | [06 待办项](/project-development/06-todos/index.md) | 编号/状态/完成标准/期限四要素齐全，完成时自动流转留档 |

## ⏪ 打回与升级机制

**打回条件与 SLA：**

| 打回方向 | 触发条件 | 处理要求 |
| --- | --- | --- |
| 测试 → 开发 | 缺陷（按 P0~P3 定级） | P0 立即最小修复 + 精简评审 + 合回主干；P1 24h 内；P2 本迭代内 |
| 测试 → PM | 验收标准歧义/缺失 | 48h 内澄清并更新 PRD（版本化变更） |
| 开发 → 架构 | 方案与实现冲突/不可行 | 当日响应，更新 ADR 后开发继续 |
| 架构 → PM | 需求不可测、依赖不明 | 退回重写验收标准，冻结解除 |

**升级原则（争议拍板顺序）：**

1. 范围与优先级之争 → **PM 拍板**（做不做、何时做）
2. 技术选型与结构之争 → **架构拍板**（怎么做）
3. 质量红线 → **测试一票否决**（P0/P1 未清零 = No-Go，无人可 override）
4. 仍僵持 → 编排者（主会话）裁决，结论记入 ADR 留痕

## 📂 交付物目录约定

```
<项目仓库>/docs/
├── 01-需求/   PRD-*.md、backlog.md               ← PM 维护
├── 02-设计/   技术方案-*.md、adr/NNNN-*.md      ← 架构维护
└── 04-测试/   测试计划-*.md、测试报告-*.md       ← 测试维护
```

## 🚀 如何拉起团队（两种方式）

**方式一：子智能体（推荐）**——四个子智能体已安装在两处：① 用户级 `~/.zcode/agents/`（**所有项目工作区都可用**，做开发时主会话按描述自动路由或点名调用，调度规则见 `~/.zcode/AGENTS.md`）；② 本仓 `.zcode/agents/`（仓库级副本，工作区为本仓时生效）。装载器内统一引用约定位置 `~/knowledge-base`（家目录下，Windows/Mac 通用；编排者派发时附上该路径），不落盘符绝对路径、零环境变量——迁移后把知识库放回约定位置即零配置，跑安装脚本可自动补建链接。**换电脑或知识库迁移后**：在知识库工作区运行技能 `virtual-team-setup`（或 `python .zcode/skills/virtual-team-setup/install.py`）一键重装，幂等可重跑。

**方式二：手动编排**——主会话用通用子代理加载角色文档执行（路径均为**仓库根相对路径**，仓库根 = 含 `AGENTS.md`、`project-development/`、`personal-assistant/` 的目录），调用模板：

```
以《产品经理角色文档》project-development/10-virtual-team/product-manager.md 为准，处理：<原始诉求>
以《架构设计师角色文档》project-development/10-virtual-team/architect.md 为准，基于 docs/01-需求/ 下的冻结需求出方案
以《开发工程师角色文档》project-development/10-virtual-team/developer.md 为准，实现 docs/02-设计/ 技术方案中的任务：<任务编号>
以《测试工程师角色文档》project-development/10-virtual-team/tester.md 为准，对 <分支/版本> 提测执行测试
```

编排节奏照 [00 总览的迭代节奏](/project-development/00-process-overview.md)执行：需求梳理 → 方案评审 → 日常开发 → 提测回归 → 改进项记入待办。

## 🔧 维护约定

1. 角色规则的**唯一权威来源是本目录的角色文档**；装载器源有两处：本仓 `.zcode/agents/`（仓库相对路径）与技能模板 `.zcode/skills/virtual-team-setup/templates/`（用户级 `~/.zcode/agents/` 由其复制生成）——改规则先改文档、再同步两处装载器源，重跑 `install.py` 刷到用户级。
2. 若客户端「设置 → 子智能体」未发现这四个 agent，重启会话或核对 `.zcode/agents/` 目录。
3. 新增角色（如运维 SRE、DBA）按同样结构：角色文档 + 装载器 + 本 index.md 登记 RACI 与契约行。
