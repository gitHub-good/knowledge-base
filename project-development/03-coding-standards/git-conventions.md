# 🌿 Git 提交与分支规范

> 基线：[Conventional Commits 1.0.0](https://www.conventionalcommits.org/zh-hans/) + GitHub Flow。目标：**提交历史可读、可追溯、可自动生成 CHANGELOG**。

<a id="commit-spec"></a>

## 📝 一、提交信息规范（Conventional Commits）

格式：

```
<类型>(<范围>): <简短描述>

[可选正文：动机与背景]

[可选脚注：BREAKING CHANGE 说明 / 关联编号]
```

### 🏷️ 类型（type）

| 类型 | 用途 | 对应版本变化（SemVer） |
| --- | --- | --- |
| feat | 新功能 | MINOR |
| fix | 缺陷修复 | PATCH |
| docs | 仅文档变更 | — |
| style | 不影响语义的格式调整 | — |
| refactor | 既非新增也非修复的重构 | — |
| perf | 性能优化 | PATCH/MINOR |
| test | 补充/修改测试 | — |
| build | 构建系统或依赖变更 | — |
| ci | CI 配置变更 | — |
| chore | 其他杂务 | — |

### ✅❌ 示例（好 vs 坏）

```
✅ feat(退保): 支持部分金额退保
✅ fix(guarantee): 修复并发下保函编号重复 #REQ-20260901-03
✅ feat(api)!: 重构响应结构为统一 code/message/data 格式

   BREAKING CHANGE: 响应体从裸数据改为 {code,message,data} 包装，调用方需同步升级。

❌ 修改bug
❌ 更新
❌ fix 了一下退保的问题，顺便改了下格式和依赖版本
```

规则：
1. 描述行 ≤72 字符，用祈使句（"修复…"而不是"修复了…"），不加句号。
2. **一个提交只做一件事**——顺手改的格式/依赖拆成独立提交。
3. 破坏性变更：类型后加 `!`，或脚注 `BREAKING CHANGE:`（对应 SemVer 的 MAJOR 升版）。
4. 关联编号放描述或脚注：`#REQ-20260901-03`、`Closes #12`。

### 🛠️ 工具保障

- `commitlint` + `husky`（或 `lefthook`）：提交前校验格式，不合规拒绝提交。
- `commitizen`（`git cz` 交互式生成提交信息）。

## 🧭 二、分支模型选型

| 模型 | 适用场景 | 复杂度 |
| --- | --- | --- |
| **GitHub Flow**（推荐默认） | 持续交付、单人/小团队：main 常绿 + 短命 feature 分支 + PR | ★ |
| Trunk-Based Development | 高频部署大团队：所有人小步直合主干，靠特性开关隐藏未完成功能 | ★★ |
| Git Flow | 有固定版本发布周期的传统软件（maintain/release/hotfix 多分支） | ★★★ |

**个人项目直接用 GitHub Flow**：main 分支永远可发布，一切变更走 PR 合入。

## 🔖 三、分支命名规范

```
feature/REQ-20260901-03-部分退保      # 新功能
fix/BUG-207-保函编号重复              # 缺陷修复
hotfix/PROD-1024-支付回调超时          # 线上紧急修复（从 main 拉）
refactor/订单模块去重校验逻辑          # 重构
chore/升级依赖到安全版本              # 杂务
docs/补充退保链路文档                 # 文档
```

规则：`类型/编号-简短描述`；分支是**短命的**（存活 ≤3 天），做完即合即删。

## 🔀 四、合并规范（PR/MR）

1. **PR ≤400 行 diff**：大了就拆——大 PR 等于没人评审（依据 [05 评审流程与时效](../05-code-review/index.md#review-process)）。
2. 合并前 rebase 或 merge 最新 main，保证可编译可部署。
3. 合并方式统一：**Squash and Merge**（一个 PR 压成一个干净提交，类型沿用 PR 首条提交信息）。
4. PR 描述模板：

```markdown
## 做了什么 / 为什么
（关联需求编号）

## 改动点
-

## 自测情况
- [ ] 主路径
- [ ] 边界/异常
- [ ] 已跑测试 / 覆盖率

## 风险与回滚方案
```

## ⛔ 五、历史保护规则（红线）

| 场景 | 正确做法 | 禁止 |
| --- | --- | --- |
| 本地未推送的提交写错了 | `git commit --amend` | — |
| 已推送到共享分支 | 追加新提交修正 | ❌ force push 共享分支 |
| main 需要回退 | `git revert`（生成反向提交） | ❌ reset 已发布历史 |
| 救命 | `git reflog` 找回一切（详见命令速查） | ❌ 慌了乱敲命令 |

## 🪝 六、常用钩子与约定

- `.gitignore` 项目第一天就配齐（模板见仓库根 [.gitignore](../../.gitignore)）；密钥、`.env`、构建产物永不入库。
- 每次开新分支前先同步主干：`git checkout main && git pull`。
- 每天结束前推送 feature 分支到远端——**本地不是备份**。
