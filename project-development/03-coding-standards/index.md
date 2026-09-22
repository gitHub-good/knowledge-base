# ✍️ 03 · 编码规范

> 代码首先是写给人看的。本阶段聚合**业界最流行的编码规范**：通用原则来自 Clean Code 与 Google Style Guides，语言细则对齐《阿里巴巴 Java 开发手册》、Airbnb JavaScript 风格指南、PEP 8 等主流基线。配套的 [Git 提交与分支规范](./git-conventions.md) 保证协作历史可读可回溯。

## 📍 阶段定位

- 📥 **上游输入**：[02 设计架构](../02-design/index.md) 评审通过的方案与 ≤2 人天的任务拆解。
- 📤 **下游输出**：通过 lint + 本地自测的代码分支，进入 [04 测试规范](../04-testing/index.md)。

## 💡 一、通用设计原则（先于一切语言规范）

| 原则 | 一句话 | 反例信号 |
| --- | --- | --- |
| KISS | 保持简单直白 | 一段代码需要注释三层才能看懂 |
| DRY | 消除重复知识 | 同一段校验逻辑复制了三处 |
| YAGNI | 不做当前用不上的功能 | "以后可能要"型抽象 |
| 单一职责 | 一个类/函数只有一个变化的理由 | 改任何需求都要动这个类 |
| 高内聚低耦合 | 相关的放一起，无关的隔离开 | 改 A 模块把 B 模块改挂了 |
| SOLID | 面向对象五原则（SRP/OCP/LSP/ISP/DIP） | 依赖具体实现难以替换、难以测试 |

## 🏷️ 二、命名规范

通用规则：**见名知义、一致风格、避免缩写**（通用缩写如 id、url 除外）。

| 场景 | 惯例 | 示例 | 来源基线 |
| --- | --- | --- | --- |
| Java 类/方法/变量 | 大驼峰 / 小驼峰 | `GuaranteeService`、`refundOrder` | 阿里巴巴 Java 开发手册 |
| 常量 | 全大写下划线 | `MAX_RETRY_TIMES` | 通用 |
| Python 变量/函数 | 蛇形 | `refund_order` | PEP 8 |
| Python 类 | 大驼峰 | `OrderService` | PEP 8 |
| JS/TS 变量/函数 | 小驼峰；组件/类大驼峰 | `handleSubmit`、`OrderCard` | Airbnb 指南 |
| CSS 类名 | BEM：`块__元素--修饰符` | `card__title--active` | BEM 约定 |
| 数据库表/字段 | 小写下划线 | `guarantee_order` | 阿里巴巴 Java 开发手册 |
| 布尔命名 | is/has/can 前缀 | `isValid`、`hasPermission` | 通用 |

命名禁区：拼音与英文混用；`data1/data2`、`temp`、`test2`；与语言关键字冲突。

## 📐 三、函数规范

1. **短**：建议 ≤50 行（Python ≤30 行），一屏能读完；超过就拆。
2. **单一职责**：函数名说一件事，函数体只做这一件事。
3. **参数 ≤3 个**：多了就收拢成对象/结构体；禁止布尔旗标参数（`process(true)` 不如 `processAsync()`）。
4. **早返回（Guard Clause）**：异常分支先 return，主逻辑不嵌套超过 2 层。
5. **无副作用**：getter 就是 getter，别在读取时偷偷写库。

## 💬 四、注释规范

> 注释解释**为什么**（Why），代码表达**做什么**（What）。代码能自解释的，不需要注释。

- 每个对外公开的模块/类/函数写文档注释：Java 用 Javadoc、Python 用 docstring、JS/TS 用 JSDoc。
- TODO 格式统一：`// TODO(姓名): 事项 #关联需求号`，禁止无主 TODO。
- 删掉的代码直接删（git 会留历史），不要注释掉留着——注释掉的死代码是最大的谎言源。
- magic number 必须具名：`if (retry > 3)` → `if (retry > MAX_RETRY_TIMES)`。

<a id="error-handling"></a>

## 🚨 五、错误处理规范

1. **不吞异常**：`catch` 里什么都不做是严重缺陷；至少记日志 + 上下文。
2. **fail fast**：启动期配置错误直接抛出终止，不要带病运行。
3. **统一错误分类**：业务异常（可预期，返回给用户友好提示）vs 系统异常（不可预期，记 ERROR + 告警）。
4. **日志分级纪律**：
   - `ERROR`：需要人介入的故障（误报会让 ERROR 失去意义）
   - `WARN`：可自动恢复的异常，需关注趋势
   - `INFO`：关键业务动作留痕（下单、支付、状态变更）
   - `DEBUG`：调试细节，生产默认关闭
5. 异常信息带上下文：订单号、参数、traceId——能凭日志定位，不用再复现。

## 📚 六、主流语言规范速查（对齐最流行基线）

| 语言 | 权威基线 | 强制工具链 |
| --- | --- | --- |
| Java | 《阿里巴巴 Java 开发手册》（最新版） | CheckStyle / SpotBugs |
| JavaScript/TypeScript | Airbnb JavaScript Style Guide + Google Style | ESLint + Prettier |
| Python | PEP 8 + Black 风格 | Black + Ruff（替代 flake8/isort） |
| Go | Effective Go + Uber Go Style Guide | gofmt / golangci-lint |
| CSS/HTML | Google HTML/CSS Style Guide + BEM | Stylelint |
| SQL | 各数据库官方规范 + 阿里手册数据库规约 | SQL 审核工具（如 Yearning/Archery） |

> 记忆技巧：**格式问题全部交给工具自动处理**（Prettier/Black/gofmt），人只负责结构性问题（命名、分层、职责）。项目第一天就把这些工具配上；项目若配了 CI，把这些检查接入流水线门禁。

<a id="tech-stack"></a>

## 🧭 七、技术栈基线（默认选型）

> 新项目从这里拿"无聊但成熟"的默认答案，选型方法论见 [02·技术选型评估](../02-design/index.md#tech-evaluation)。后端默认轻量级：全内嵌中间件，`java -jar` 单包即起。

| 文档 | 何时用 | 核心原则 |
| --- | --- | --- |
| [🎨 前端技术栈](./frontend.md) | 搭/改前端项目、定前端规范前 | 默认 React 18 + TS + Tailwind + shadcn/ui；美观与顺手是硬要求 |
| [🧱 后端技术栈](./backend.md) | 搭/改后端项目、定接口与数据规范前 | 默认轻量级：Java 21 + Spring Boot 3 + 全内嵌中间件 |

约定：默认基线不是唯一答案，偏离必须能说出理由（记 [ADR](../02-design/adr-template.md)）；版本号写具体；升级版本先记待办评估破坏性变更；踩到的坑进 [踩坑记录](../../personal-assistant/lessons-learned/pitfall-records.md) 并回写基线。

## 🔁 八、编码阶段工作流

```
领取任务(≤2人天) → 从最新主干拉 feature 分支（命名见 Git 规范）
  → 小步提交（每次提交可编译可运行）→ 本地 lint + 自测
  → 推送并创建 PR（≤400 行）→ 进入 04 测试 / 05 评审
```

<a id="dod"></a>

## ✅ 阶段检查清单（DoD）

- [ ] 遵循分层架构，依赖方向正确，无循环依赖
- [ ] 命名符合语言基线，无魔法数字与无主 TODO
- [ ] 函数短小单一职责，无深嵌套
- [ ] 异常不吞、日志分级正确、错误信息带上下文
- [ ] 格式化与静态检查工具全绿（lint 0 error 0 warning）
- [ ] 本地自测通过：主路径 + 边界 + 异常场景
- [ ] 提交信息符合 Conventional Commits → 进入 [04 测试规范](../04-testing/index.md)
