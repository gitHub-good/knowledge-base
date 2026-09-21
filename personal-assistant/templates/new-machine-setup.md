# 📋 新电脑环境清单

> 换新电脑 / 重装系统后，从裸机到「知识库 + 虚拟团队全部可用」的落地清单——按序打勾，全绿即恢复完成。装完本页，把踩到的新坑补进 [踩坑记录](/personal-assistant/lessons-learned/pitfall-records.md)。

## 🧰 一、基础工具

- [ ] **Git**：`git --version` 有输出；配置 `git config --global user.name / user.email`
- [ ] **Python 3**：`python --version` ≥ 3.8（校验脚本用到的功能均为标准库，无需 pip 装包）
- [ ] **终端**：Git Bash 或 Windows Terminal（校验脚本按 UTF-8 输出中文）

## 💾 二、知识库落地

- [ ] **克隆私有仓**：`git clone git@github.com:gitHub-good/knowledge-base.git ~/knowledge-base`——**放对约定位置即零配置**（体系内所有引用都指向 `~/knowledge-base`；放别处也行，安装脚本会自动在家目录建链接指过去）
- [ ] **完整性校验**：在仓库根执行 `python tools/check_links.py`，问题数为 0
- [ ] **工具自检**：`python tools/todo.py` 与 `python tools/req.py` 各跑一遍，问题数为 0

## 🤖 三、ZCode 与虚拟团队

- [ ] **安装 ZCode** 并登录账号
- [ ] **恢复虚拟团队**：用 ZCode 打开知识库工作区，说「重装虚拟团队」（触发 `virtual-team-setup` 技能），或直接执行 `python .zcode/skills/virtual-team-setup/install.py`
- [ ] **重启会话**（子智能体在会话启动时注册），「设置 → 子智能体」应显示 product-manager / architect / developer / tester 四个角色
- [ ] **验证约定位置**：`ls ~/knowledge-base` 能看到 `AGENTS.md`、`project-development/` 等（安装脚本已在家目录自动建链接）
- [ ] **验证自动路由**：在任意项目工作区丢一句开发类任务（如"帮我整理一个新需求"），确认主会话自动调度对应角色

## ✅ 验收清单（DoD）

- [ ] `python tools/check_links.py` 全绿
- [ ] `python tools/todo.py`、`python tools/req.py` 校验全绿
- [ ] 四个子智能体可见且可调度
- [ ] `~/knowledge-base` 可访问（含 `AGENTS.md`、`project-development/`）

## 🧨 常见坑

- 装完技能仍调不到子智能体 → 十有八九是**没重启会话**（注册发生在会话启动时）
- 校验脚本报编码错 → 终端代码页问题，换 Git Bash 或 Windows Terminal
- 其余坑先 `grep -ri "关键词" personal-assistant/lessons-learned/pitfall-records.md`，二刷同款坑是记录的耻辱
