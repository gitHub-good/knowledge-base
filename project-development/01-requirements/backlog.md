# 🗃️ 需求池

> 本仓自身的改进需求池：**单文件单需求，状态自动流转 + 汇总看板**。方法论（分类/用户故事/INVEST/MoSCoW/RICE/变更控制）见 [01 需求管理](./index.md#backlog)；开发项目的需求池放 `<项目仓库>/docs/01-需求/`，同一套约定。

## 📐 约定

1. **单文件单需求**：命名 `REQ-YYYYMMDD-NN-标题.md`（NN 为当日序号）；编号即唯一 ID。
2. **状态机（从简版）**：`待评审 → 开发中 → 已关闭 / 已拒绝（留档）`——01 方法论的完整状态机含提测/发布环节，适用于开发项目；本池条目多为文档/工具工作，故取子集。
3. **必填字段**（文件头）：`status` / `类型`（功能、优化、缺陷、技术，对应 01 四类分档）/ `优先级`（MoSCoW 中文：必须、应该、可以、暂不）/ `创建日期` / `来源`（原始诉求，或待办编号 TB-xxx）；`完成日期` 在关闭时自动写入。
4. **必须有验收标准**（正文 Given/When/Then）——验收标准会转化为"这条需求算完成"的检查点。
5. **与待办项联动**：待办里值得排期的改进用 `python tools/todo.py convert <待办编号>` 转入本池——自动建 REQ 条目（来源=待办编号）、待办关闭并在进展记录回写 REQ 编号。

## 🔧 自动流转（tools/req.py）

| 命令 | 作用 |
| --- | --- |
| `python tools/req.py new "标题" [-t 类型] [-p 优先级] [--from TB-编号] [-d 一句话说明] [--gwt 验收标准]…` | 自动编号建单（骨架文件），刷新汇总；`--gwt` 可重复传多条，占位符未填会被校验点名 |
| `python tools/req.py start REQ-YYYYMMDD-NN` | 待评审 → 进行中，追加进展记录 |
| `python tools/req.py done REQ-YYYYMMDD-NN` | → 已关闭：自动写完成日期、记进展、刷新汇总 |
| `python tools/req.py reject REQ-YYYYMMDD-NN [原因]` | → 已拒绝（留档，不删除） |
| `python tools/req.py sync` | 重新生成本页汇总区块（勿手改） |
| `python tools/req.py`（无参数） | 校验全部需求文件（状态/字段/一句话说明与验收标准已填/汇总同步），有问题退出码 1 |

## 📄 文件骨架

```
---
status: 待评审
类型: 优化
优先级: 应该
创建日期: YYYY-MM-DD
来源: 原始诉求
---

# 📥 标题

> 一句话说明

## 📋 验收标准（Given/When/Then）

- [ ] Given <前置条件> When <操作> Then <期望结果>

## 📝 进展记录

- YYYY-MM-DD 创建。
```

## 📊 汇总看板

<!-- reqpool:begin -->
> 由 `python tools/req.py sync` 自动生成，手改会被覆盖。

**统计**：待评审 0 ｜ 开发中 0 ｜ 已关闭 1 ｜ 已拒绝 0（共 1）

**最近关闭**（最新 5 条）：

| 编号 | 标题 | 完成日期 |
| --- | --- | --- |
| [REQ-20260921-01](REQ-20260921-01-req-new-fill-desc-and-gwt.md) | req-new-fill-desc-and-gwt | 2026-09-21 |
<!-- reqpool:end -->