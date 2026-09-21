<!-- virtual-team:start -->
## 虚拟团队子智能体（所有工作区生效）

四个角色子智能体定义在用户级 `~/.zcode/agents/`（product-manager / architect / developer / tester），角色规则的唯一权威来源是个人知识库的角色文档。**知识库约定位置 = `~/knowledge-base`**（家目录下，Windows/Mac 通用；家目录的链接由 `.zcode/skills/virtual-team-setup/install.py` 自动维护）。派发子智能体时把该路径写进任务提示。接到开发类任务时按场景自动调度，不必等点名：

- 新想法/需求整理、需求池、PRD、功能验收 → `product-manager`
- 需求转方案、技术选型、接口/表设计、任务拆解 → `architect`
- 实现任务、修 bug、补测试、规范提交、P0 热修复 → `developer`
- 测试用例设计与执行、缺陷定级、回归/冒烟、上线 Go/No-Go → `tester`

完整功能默认沿交接物链 **PM → 架构 → 开发 → 测试** 推进（主会话任编排者，交接物契约与打回机制见 `~/knowledge-base/project-development/10-virtual-team/index.md`）；单步任务直接调度对应角色。知识库迁移后放回约定位置即零配置（跑安装脚本可自动补建家目录链接）；勿在任何文件里硬编码盘符绝对路径。改角色规则：先改知识库角色文档，再同步两份装载器（知识库 `.zcode/agents/` 与技能 `templates/`），重跑 `install.py` 完成安装。
<!-- virtual-team:end -->
