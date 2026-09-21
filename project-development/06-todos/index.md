# 📌 06 · 待办项

> 值得跟踪的事情都在这落地：**单文件单待办，状态自动流转 + 汇总看板**。闭环各阶段遗留的问题、改进想法、临时任务统一在此登记跟踪。

## 🧭 闭环中的位置

五阶段闭环的横切枢纽：任何阶段发现的问题、产生的改进想法随手登记在此；有价值的条目转进 [01 需求管理](/project-development/01-requirements/index.md) 的需求池，开启下一轮迭代（见 [00 · 改进环](/project-development/00-process-overview.md#improve-loop)）。

## 📐 约定

1. **单文件单待办**：命名 `TB-YYYYMMDD-NN-标题.md`（NN 为当日序号 01~99），统一存放在本目录 `todo/` 子目录（校验会把遗留在根目录的待办计为问题）；编号即唯一 ID，可全局搜索。
2. **状态机**：`待办 → 进行中 → 已完成 / 已取消`，状态存于文件头 `status` 字段，四个合法值。
3. **必填字段**（文件头）：`status` / `优先级`（高、中、低）/ `创建日期`；`完成日期` 在完成时自动写入。
4. **必须有完成标准**（正文 DoD 节）——说不清"什么算完成"的事不登记。
5. **与需求池联动**：值得排期的改进用 `convert` 转需求（自动建 REQ、双向回写编号），待办随即记为已完成。

## 🔧 自动流转（tools/todo.py）

| 命令 | 作用 |
| --- | --- |
| `python tools/todo.py new "标题" [-p 高] [-d 一句话说明] [--dod 完成标准]…` | 自动编号建单（骨架文件），刷新汇总；`--dod` 可重复传多条，占位符未填会被校验点名 |
| `python tools/todo.py start TB-YYYYMMDD-NN` | 待办 → 进行中，追加进展记录 |
| `python tools/todo.py done TB-YYYYMMDD-NN` | → 已完成：自动写完成日期、追加进展记录、刷新汇总 |
| `python tools/todo.py cancel TB-YYYYMMDD-NN [原因]` | → 已取消（留档，不删除） |
| `python tools/todo.py convert TB-YYYYMMDD-NN [-p MoSCoW优先级]` | 转需求：自动在 [需求池](/project-development/01-requirements/backlog.md) 建 REQ 条目（来源=待办编号），待办关闭并回写 REQ 编号 |
| `python tools/todo.py sync` | 重新生成本页汇总区块（勿手改） |
| `python tools/todo.py`（无参数） | 校验全部待办文件（状态合法、字段齐全、一句话说明与完成标准已填、汇总未失同步），有问题退出码 1 |

在本仓任意会话中，完成一件待办只需跑 `done <编号>`：状态、日期、进展记录、汇总看板四件事一步自动完成。

## 📄 文件骨架

```
---
status: 待办
优先级: 中
创建日期: YYYY-MM-DD
---

# 📌 标题

> 一句话说明

## 📋 完成标准

- [ ] 达到什么程度算完成

## 📝 进展记录

- YYYY-MM-DD 创建。
```

## 📊 汇总看板

<!-- todos:begin -->
> 由 `python tools/todo.py sync` 自动生成，手改会被覆盖。

**统计**：待办 9 ｜ 进行中 0 ｜ 已完成 7 ｜ 已取消 0（共 16）

**未完成**（按创建日期，早的在前）：

| 编号 | 标题 | 优先级 | 状态 | 创建日期 |
| --- | --- | --- | --- | --- |
| [TB-20260921-06](/project-development/06-todos/todo/TB-20260921-06-setup-private-remote-and-push.md) | setup-private-remote-and-push | 高 | 待办 | 2026-09-21 |
| [TB-20260921-07](/project-development/06-todos/todo/TB-20260921-07-harden-todo-req-filename-sanitize.md) | harden-todo-req-filename-sanitize | 中 | 待办 | 2026-09-21 |
| [TB-20260921-08](/project-development/06-todos/todo/TB-20260921-08-check-links-enforce-conventions.md) | check-links-enforce-conventions | 中 | 待办 | 2026-09-21 |
| [TB-20260921-09](/project-development/06-todos/todo/TB-20260921-09-tools-tests-and-ci.md) | tools-tests-and-ci | 中 | 待办 | 2026-09-21 |
| [TB-20260921-10](/project-development/06-todos/todo/TB-20260921-10-loader-sync-consistency-check.md) | loader-sync-consistency-check | 中 | 待办 | 2026-09-21 |
| [TB-20260921-11](/project-development/06-todos/todo/TB-20260921-11-todo-skeleton-add-deadline-field.md) | todo-skeleton-add-deadline-field | 低 | 待办 | 2026-09-21 |
| [TB-20260921-12](/project-development/06-todos/todo/TB-20260921-12-index-trees-sync-missing-files.md) | index-trees-sync-missing-files | 低 | 待办 | 2026-09-21 |
| [TB-20260921-13](/project-development/06-todos/todo/TB-20260921-13-activate-convert-feedback-loop.md) | activate-convert-feedback-loop | 低 | 待办 | 2026-09-21 |
| [TB-20260921-15](/project-development/06-todos/todo/TB-20260921-15-req-new-fill-desc-and-gwt.md) | req-new-fill-desc-and-gwt | 低 | 待办 | 2026-09-21 |

**最近完成**（最新 5 条）：

| 编号 | 标题 | 完成日期 |
| --- | --- | --- |
| [TB-20260921-16](/project-development/06-todos/todo/TB-20260921-16-todo-items-move-to-subdir.md) | todo-items-move-to-subdir | 2026-09-21 |
| [TB-20260921-14](/project-development/06-todos/todo/TB-20260921-14-todo-new-fill-desc-and-dod.md) | todo-new-fill-desc-and-dod | 2026-09-21 |
| [TB-20260921-05](/project-development/06-todos/todo/TB-20260921-05-git-initial-commit.md) | git-initial-commit | 2026-09-21 |
| [TB-20260921-04](/project-development/06-todos/todo/TB-20260921-04-fix-root-index-naming-rule.md) | fix-root-index-naming-rule | 2026-09-21 |
| [TB-20260921-03](/project-development/06-todos/todo/TB-20260921-03-fix-install-add-standards-section.md) | fix-install-add-standards-section | 2026-09-21 |
<!-- todos:end -->