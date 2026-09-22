# 🎨 前端技术栈

> 前端默认选型与工程基线：**React + Tailwind + shadcn/ui**。目标：页面**美观、操作顺手**——组件底子选好看的，交互细节按「体验基线」执行。

## 🧭 一、选型基线

| 场景 | 默认选型 | 备选 | 说明 |
| --- | --- | --- | --- |
| 框架 | React 18（函数组件 + Hooks） | Vue 3 | 同一项目不混用 |
| 语言 | TypeScript 5（`strict: true`） | — | 严格模式不妥协；`any` 必须带注释说明原因 |
| 构建 | Vite 5 | — | 新项目不用 webpack |
| 包管理 | pnpm | npm | 锁 `pnpm-lock.yaml`，CI 用 `pnpm i --frozen-lockfile` |
| 路由 | react-router 6 | vue-router 4（Vue 项目用） | 路由懒加载默认开启 |
| 客户端状态 | Zustand | Pinia（Vue 项目用） | 服务端数据优先 TanStack Query，不搬进全局 store |
| UI 组件库 | shadcn/ui（Radix 无障碍底座，美观且可深度定制） | Ant Design 5（重表格/复杂表单后台） | 禁止两套混用 |
| 样式 | Tailwind CSS（配 shadcn 主题变量） | CSS Modules | 原子类；主色/圆角/间距全走设计 token，不手写魔法值 |
| 请求 | axios | ky | 统一封装（见二） |
| 表单校验 | react-hook-form + zod | — | shadcn 表单默认搭档；schema 单份，前后端共用规则描述 |
| 单元测试 | Vitest + Testing Library | — | 组件测行为不测实现 |
| E2E 测试 | Playwright | — | 只覆盖主路径 ≤10 条 |
| 规范 | ESLint 9 + Prettier | — | 提交前 0 error，格式全交 Prettier |

## 🏗️ 二、工程骨架

```
src/
├── api/          # 按业务域分文件：user.ts、order.ts；统一实例 + 拦截器
├── components/   # 跨页面通用组件（≥2 处使用才进来）
├── hooks/          # 自定义 Hooks（Vue 项目对应 composables/）
├── stores/       # Pinia store，按域拆分
├── views/        # 页面级组件，与路由一一对应
├── router/       # 路由表 + 守卫
└── assets/       # 图标、全局样式变量
```

约定：
1. **请求层统一封装**：一个 axios 实例 + 拦截器做三件事——带 token、统一错误码映射成提示、超时 10s 自动取消；业务代码不直接 `import axios`。
2. **环境变量**：`VITE_` 前缀，三套环境（dev / test / prod）各一份 `.env.*`；密钥类永不进前端环境文件（前端无秘密）。
3. **接口约定**：跟后端统一响应结构 `{code, msg, data}`（见 [后端技术栈](./backend.md)）；分页固定 `page/pageSize/total`。

## ⚡ 三、性能基线（写进 CI 的数字）

- 首屏资源（gzip 后）≤ 300KB；单 chunk 超 500KB 报警。
- 路由级代码分割默认开启；组件库按需引入。
- Lighthouse 性能分 ≥ 90（桌面端）。
- 接口防抖：搜索类输入 300ms；按钮提交 loading 态防重复点击。

## 🎨 四、体验基线（美观与顺手的硬要求）

- **设计 token 统一**：主色 1 个、间距取 4px 倍数、圆角/字号只用固定几档——全部走 shadcn 主题变量（CSS variables）统一调，禁止页面里散落魔法值。
- **三态必处理**：加载（骨架屏，不用裸转圈）、空数据（给引导动作）、错误（给重试入口）——任何路由不允许白屏。
- **即时反馈**：hover/active 必有状态变化；提交类操作 300ms 内出 loading；列表增删用乐观更新，失败再回滚提示。
- **动效克制**：过渡 150~250ms ease-out；只给有意义的动作加动效（进入/退出/展开），不做装饰性动画。
- **响应式**：Tailwind 断点 sm/md/lg 三档覆盖手机到桌面；触控目标 ≥ 44px。
- **暗色模式**：跟随系统（html.dark 切换 + token 双套），第一天就配好，不要事后补。

## 🔗 五、联调约定

- 跨域本地走 Vite proxy，不改后端 CORS。
- 接口未就绪时用 MSW 或简单 mock 文件占位，联调日整体切换。
- 前后端字段变更走 [Git 提交与分支规范](./git-conventions.md#commit-spec)，契约变更先改接口文档再动代码。

## ✅ 检查清单

- [ ] 三态（加载/空/错误）全覆盖，无白屏
- [ ] 设计 token 统一，无散落魔法值；暗色模式可用
- [ ] TypeScript strict 开启，CI `vue-tsc --noEmit` 0 error
- [ ] ESLint + Prettier 接入提交检查，0 error
- [ ] 请求层统一封装，业务代码无裸 axios
- [ ] 首屏 ≤ 300KB，路由懒加载生效
- [ ] 踩坑已进 [踩坑记录](../../personal-assistant/lessons-learned/pitfall-records.md)
