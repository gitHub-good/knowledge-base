---
name: virtual-team-setup
description: 一键安装/重装/更新「虚拟团队」四角色子智能体（product-manager/architect/developer/tester）到用户级 ZCode 配置。Triggers on "换电脑", "新电脑", "重装虚拟团队", "恢复虚拟团队", "安装虚拟团队", "子智能体不见了", "virtual team setup".
---

# 虚拟团队安装（换机一键恢复）

> 个人知识库的虚拟团队 = 仓库级装载器（随仓库走）+ 用户级配置（`~/.zcode/agents/` 与 `~/.zcode/AGENTS.md`，只在本机生效）。换电脑后用户级配置为空——跑本技能即可重建；幂等可重入，重复执行只刷新内容。

## 何时用

- 新电脑/重装系统后，知识库已就位，要恢复虚拟团队
- 知识库迁移了位置（如 D 盘挪到 E 盘）——把知识库放回约定位置 `~/knowledge-base` 即零配置；放在别处则跑本技能自动补建家目录链接
- 改过角色装载器模板后，把更新刷到用户级

## 前置条件

1. 知识库仓库已在新机就位（本技能随仓库 `.zcode/skills/virtual-team-setup/` 一起迁移，能被调用即已就位）。
2. 已安装 ZCode 客户端与 Python 3。
3. 完整换机流程（Python/Git 安装、知识库克隆与校验、装后验收）见知识库 `personal-assistant/templates/new-machine-setup.md`，本技能是其第三步。

## 步骤

1. 确认仓库根 = 本技能目录的上三级目录（特征：含 `AGENTS.md`、`project-development/`、`personal-assistant/`）。若技能目录不在这样的仓库内，先纠正位置再装。
2. 执行安装脚本：

   ```bash
   python <仓库根>/.zcode/skills/virtual-team-setup/install.py
   ```

   可先加 `--dry-run` 预览。脚本自动完成：① 复制四个装载器到 `~/.zcode/agents/`（引用约定位置 `~/knowledge-base`，**不含盘符绝对路径、零环境变量**）；② 在 `~/.zcode/AGENTS.md` 幂等插入/替换「虚拟团队子智能体」与「编辑文件规范（指向 `~/knowledge-base` 下规范原文）」两章节，并把「知识库位置」行统一为约定位置指引；③ 确保家目录约定位置 `~/knowledge-base` 指向本仓库（缺失时自动创建：Windows 用 junction，Unix 用软链接）；④ 自检 frontmatter、BOM、无盘符路径、角色文档在位、约定位置可访问。
3. 核对脚本输出：应列出 4 个装载器写入结果、AGENTS.md 更新方式（新增/替换/无变化）、自检全过。出现 FAIL 逐条修复后重跑。
4. 告知用户：**重启 ZCode 会话生效**，「设置 → 子智能体」应显示四个角色；之后在任意项目工作区下达开发任务，主会话按 `~/.zcode/AGENTS.md` 的路由规则自动调度。

## 改了角色规则之后

权威来源是 `<仓库根>/project-development/10-virtual-team/` 的角色文档。若改动涉及装载器内容（职责速记/协作规则/输出要求），同步两处：仓库级 `.zcode/agents/` 与本技能 `templates/`，再重跑 `install.py` 刷到用户级。
