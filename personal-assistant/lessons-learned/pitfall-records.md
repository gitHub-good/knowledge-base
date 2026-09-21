# 🧨 踩坑记录

> 排查前先在这里搜一遍（`grep -ri "关键词"`），别二刷同款坑。**一坑一条、当天记录、按时间倒序**。格式五要素：现象 / 根因 / 解决 / 预防 / 耗时——"耗时"能帮你判断哪些坑最值得写预防。

## 📋 记录格式

```markdown
### PIT-YYYYMMDD-NN：<一句话标题>
- 🏷️ 场景/环境：（什么系统、什么操作触发）
- 🔍 现象：（看到的报错/异常行为，原样贴关键报错——方便搜索引擎命中）
- 🧭 排查过程：（走了哪些弯路，简短）
- 🎯 根因：（真正的原因，一层就够，别写"改了就好了"）
- ✅ 解决：（具体怎么修的，命令/配置/代码）
- 🛡️ 预防：（怎么保证不再犯——能固化到规范/工具的，回写 project-development 对应阶段）
- ⏱️ 耗时：X 小时
- 🔑 关键词：`逗号分隔` `便于检索`
```

## 💡 示例（演示条目，可删）

### PIT-20260909-01：Docker 容器内连不上宿主机 MySQL
- 🏷️ 场景/环境：Win11 + Docker Desktop，容器里的 Spring Boot 连本机 MySQL
- 🔍 现象：`Communications link failure`，容器内 `telnet host.docker.internal:3306` 不通
- 🧭 排查过程：容器互 ping 正常 → 怀疑镜像问题绕了远路
- 🎯 根因：MySQL 只监听 127.0.0.1，未对 Docker 网段开放，且账号未授权该网段
- ✅ 解决：`bind-address = 0.0.0.0` + `GRANT ... TO user@'172.17.0.%'`；容器内统一用 `host.docker.internal`
- 🛡️ 预防：本地依赖统一写 `host.docker.internal` 进 compose 默认配置（已补进 Docker 速查的排查场景表）
- ⏱️ 耗时：1.5 小时
- 🔑 关键词：`docker` `mysql` `连接拒绝` `host.docker.internal`

---

<!-- 新记录从这里往下追加（保持时间倒序，最新的在最上面） -->
