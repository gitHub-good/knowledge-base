# 🧱 后端技术栈

> 后端默认选型与工程基线，**默认轻量级：全内嵌中间件，`java -jar` 单包即起，零外部服务部署**。目标：新项目 10 分钟内定完技术栈；非功能问题先查 [通用设计方案库](../02-design/solution-catalog.md) 再自研。

## 🧭 一、选型基线

> **默认走轻量级路线**：中间件全部本地内嵌，`java -jar` 单包即可启动，不依赖任何外部服务部署；触发升级线再换重量级组件，偏离默认记 [ADR](../02-design/adr-template.md)。

**开发组件**（不分档）：

| 场景 | 默认选型 | 备选 | 说明 |
| --- | --- | --- | --- |
| 主语言 | Java 21 LTS | Python 3.12 + FastAPI（轻服务/脚本） | 企业级/长生命周期项目用 Java；快速原型用 FastAPI |
| 框架 | Spring Boot 3.x（内嵌 Tomcat） | — | 交付形态 = 可执行单包 jar |
| ORM | MyBatis-Plus（Java，`DbType.SQLITE`） | JPA / Prisma / SQLAlchemy | SQL 可控优先；复杂查询写 XML |
| 连接池 | HikariCP（SB 默认） | — | SQLite 用小池：maximum-pool-size 1~5（单写者模型）；超时 5s |
| API 文档 | springdoc-openapi | — | 契约先行：接口先定文档再实现 |
| 测试 | JUnit 5 + Mockito + Testcontainers | — | 分层与覆盖率标准见 [04 测试规范](../04-testing/index.md) |
| 规范 | CheckStyle/Spotless | — | 格式交工具，提交前 0 error |

**中间件分档**（轻量级 = 默认，零部署）：

| 场景 | 轻量级（默认 · 本地内嵌） | 重量级（升级线） | 升级触发 |
| --- | --- | --- | --- |
| 数据库 | SQLite 3（文件库；专属基线见第四节） | PostgreSQL 16 / MySQL 8 | 多人并发写 / 单表千万级 / 多端网络访问 |
| 缓存 | Caffeine（进程内；红线见第三节） | Redis 7 | 多实例共享 / 需持久化缓存 |
| 消息/异步 | Spring `ApplicationEvent` + `@Async`（进程内事件） | RabbitMQ / Kafka（对比见 [方案库·MQ](../02-design/solution-catalog.md)） | 跨进程事件 / 削峰填谷 / 多组消费者 |
| 定时任务 | Spring `@Scheduled` / Quartz 内嵌 | XXL-Job | 多实例调度 / 可视化运维 |
| 文件存储 | 本地磁盘（应用数据目录） | MinIO / OSS | 多实例共享文件 / CDN 分发 |
| 全文搜索 | SQLite FTS5 | Elasticsearch | 复杂分词 / 千万级文档 |
| 认证 | JWT 无状态 + 本地用户表 | Keycloak / 企业 SSO | 统一身份认证 |
| 日志 | Logback 滚动文件 | ELK / Loki | 多实例集中检索 |

## 🏗️ 二、工程约定

1. **分层**：`controller → service → repository` 三层；controller 只做参数校验与编排，业务规则全在 service；跨 service 复用走领域组件，禁止互相注入循环依赖。
2. **统一响应**：`{code, msg, data}`；错误码分段——`0` 成功、`1xxx` 通用、`2xxx` 参数、`3xxx` 业务、`5xxx` 系统；错误码表单独维护一份文档。
3. **异常**：业务异常抛 `BizException(code, msg)` 全局拦截；**不吞异常**——catch 必须记日志或上抛（见 [03 编码规范](./index.md)）。
4. **配置**：`application-{env}.yml` 三套；数据库密码、AK/SK 用环境变量注入，**永不写进文件**（红线）。
5. **日志**：分级使用（ERROR 带堆栈 / WARN 可自愈 / INFO 关键路径 / DEBUG 开发期）；每条请求带 traceId。

## ⚡ 三、非功能基线（先查方案库，再写代码）

- 超时与重试：所有跨进程调用配 [弹性四件套](../02-design/solution-catalog.md#resilience)（超时/重试/熔断/降级）；重试必须配 [幂等](../02-design/solution-catalog.md#idempotency)。
- 缓存：默认本地 Caffeine——本质是带 TTL / 容量 / 淘汰策略的高级 Map（裸 `ConcurrentHashMap` 只用于无需过期的本地状态）；穿透/击穿/雪崩解法直接抄 [方案库](../02-design/solution-catalog.md)。
- 本地缓存红线：必须同时设 `maximumSize` 与 `expireAfterWrite`（防 OOM、防陈旧数据）；禁止当持久层用（重启即清空）；出现多实例部署或跨进程共享需求 → 升级 Redis。
- 慢 SQL：单条 > 200ms 记 WARN 并进待办优化；深分页用游标或子查询定位。
- 资金/订单写操作必有幂等键；第三方交互必有 [对账](../02-design/solution-catalog.md#reconciliation)。

## 🗄️ 四、数据库基线

- 命名：表/字段小写下划线；每表三字段 `created_at` / `updated_at` / `version`。
- 索引：WHERE/ORDER BY 高频列建索引；单表索引 ≤ 5 个；大字段拆附表。
- 变更：DDL 走迁移脚本（Flyway 支持 SQLite），**任何表结构变更附回滚脚本**（见 [02 数据库设计规范](../02-design/index.md#db-standards)）。

**SQLite 专属基线**（默认库，Java 侧驱动 `org.xerial:sqlite-jdbc`）：

- 连接即开三件 PRAGMA：`journal_mode=WAL`（读写不互斥）、`foreign_keys=ON`（外键默认关，必须显式开）、`busy_timeout=5000`（写锁等待 5s）。
- **单写者模型**：写并发靠排队不靠加池——连接池 1~5；禁止长事务，写事务控制在百毫秒量级。
- 库文件放应用数据目录，**不进 git**；备份用 `VACUUM INTO 'backup.db'`，持续流备份用 Litestream。
- 类型亲和：日期存 ISO-8601 文本、布尔存 0/1——跨语言读取不歧义；自增主键用 `INTEGER PRIMARY KEY`（即 rowid）。
- 升级触发线：出现多人并发写 / 单表超千万行 / 需要多端网络访问 → 迁 PostgreSQL，走导出导入 + [对账](../02-design/solution-catalog.md#reconciliation) 核数。

## ✅ 检查清单

- [ ] 轻量级基线：`java -jar` 单包启动成功，无任何外部中间件依赖
- [ ] 分层清晰，controller 无业务逻辑
- [ ] 统一响应 + 全局异常 + 错误码表三件套齐
- [ ] 跨进程调用配齐超时/重试/幂等
- [ ] 敏感配置环境变量注入，仓库无密钥
- [ ] Flyway 迁移脚本 + 回滚脚本成对
- [ ] 踩坑已进 [踩坑记录](../../personal-assistant/lessons-learned/pitfall-records.md)
