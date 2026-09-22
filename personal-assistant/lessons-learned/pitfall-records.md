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

### PIT-20260921-01：安装脚本自检串与章节模板表述漂移，首装必败
- 🏷️ 场景/环境：macOS + ZCode；知识库 virtual-team-setup 安装技能（换机重装场景）
- 🔍 现象：[install.py](../../.zcode/skills/virtual-team-setup/install.py) 首次安装自检 FAIL「AGENTS.md 缺约定位置指引」；`--dry-run` 在全新机器直接 `FileNotFoundError` 崩溃
- 🧭 排查过程：先怀疑家目录链接没建对，再比对生成的 AGENTS.md 内容，最后 diff 脚本常量与模板原文才定位
- 🎯 根因：自检用脚本内 `KB_HINT` 常量做精确匹配，而章节模板改版后表述已变成「知识库约定位置 = `~/knowledge-base`」——两处独立演化、无一致性校验；dry-run 分支还提前读了只在正式模式才创建的文件
- ✅ 解决：自检改为匹配模板必含表述（`SECTION_HINT`）；dry-run 对缺文件回退到"将创建的默认内容"
- 🛡️ 预防：跨文件强耦合的"魔法串"要一处定义、两处引用；`install.py --check-sync` 装载器漂移校验与 [test_tools.py](../../tools/test_tools.py) 安装幂等测试已纳入提交门禁，同类漂移会被自动拦下
- ⏱️ 耗时：0.5 小时
- 🔑 关键词：`install.py` `自检` `模板漂移` `幂等` `dry-run`
