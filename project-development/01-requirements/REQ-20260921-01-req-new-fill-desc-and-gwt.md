---
status: 已关闭
类型: 优化
优先级: 应该
创建日期: 2026-09-21
来源: TB-20260921-15
完成日期: 2026-09-21
---
# 📥 req-new-fill-desc-and-gwt

> req.py new 只接受标题，验收标准停留在 Given/When/Then 占位符；与 todo.py 已落地的 -d/--dod 能力不对齐（来源 TB-20260921-15）

## 📋 验收标准（Given/When/Then）

- [x] Given 知识库任意会话 When `python tools/req.py new "标题" -d "说明" --gwt "标准"` Then 生成文件的一句话说明与验收标准为所传内容
- [x] Given 存量含占位符的需求单 When 运行 `python tools/req.py` Then 占位符未填被点名、退出码 1
- [x] Given todo.py convert 转需求 When 待办已填描述与完成标准 Then 生成的 REQ 自动继承两者，不再是空壳

## 📝 进展记录

- 2026-09-21 创建（来源：TB-20260921-15）。
- 2026-09-21 开始推进。
- 2026-09-21 完成关闭。
