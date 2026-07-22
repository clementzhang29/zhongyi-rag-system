# 开源前端 / 动效 / Rust-TS 技术参考栈

生成时间：2026-07-22 Asia/Shanghai

## 目标审美

统一采用 **Lumia Graphite Workbench / 序光工作台**：克制、平面、工业文档感、Apple 式层级，不走 AI 蓝紫渐变、不做卡片墙、不做重霓虹 HUD。

## 推荐技术栈

### 1. UI 控件底座

- Radix UI Primitives：无样式、可完全自定义、重点负责无障碍、键盘交互、Dialog/Popover/Accordion/Toast/Select 等基础行为。适合做“高端克制”的自有组件系统，而不是直接套模板。
  - https://www.radix-ui.com/primitives
  - https://www.radix-ui.com/primitives/docs/guides/styling
  - https://www.radix-ui.com/primitives/docs/components/dialog
- TanStack Query / Router / Table / Virtual：用于数据获取、路由、表格、虚拟滚动；适合你的 agent 平台、OCR 工作台、RAG 证据账本、任务执行台账。
  - https://tanstack.dev/router/latest/docs
  - https://tanstack.dev/router/latest/docs/integrations/query

### 2. 动效与空间体验

- Motion：React/JS 动效库，用于开屏细线动效、面板进入、命令轨状态切换、鼠标跟随微动效；注意只做 120–240ms 的系统级微交互，不做 AI 炫光。
  - https://github.com/motiondivision/motion
- Lenis：平滑滚动、滚动同步、长文档/日志/证据流体验；适合“滚动屏展示”和文档软件。
  - https://github.com/darkroomengineering/lenis
- React Three Fiber / Three.js：只建议用于少量“开屏数字孪生/仿真世界”或算法演示，不应用于全部后台页面。
  - https://www.npmjs.com/package/@react-three/fiber

### 3. Rust / 本地桌面 / 高性能外壳

- Tauri：Rust 后端 + Web 前端，适合把 OCR、RAG、机器视觉仿真、Agent 工具台封装成轻量桌面端。
  - https://github.com/tauri-apps/tauri
  - https://tauri.app/reference/javascript/api/namespacewebview/
- Dioxus：Rust 全栈 UI，可做 Web/Desktop/Mobile 的统一 Rust UI 产品，但生态与前端自由度需要权衡。
  - https://github.com/DioxusLabs/dioxus
  - https://dioxuslabs.com/
- Leptos：Rust 全栈 Web 框架，适合重性能、细粒度响应式 Web，但和现有 TS/React/Vue 项目混用时建议先做独立模块。
  - https://github.com/leptos-rs/leptos
  - https://www.leptos.dev/

## 对你的所有产品的统一落地方式

1. **产品外壳统一**：`AppShell + CommandRail + WorkbenchMain + InspectorPanel`。
2. **页面结构统一**：取消卡片堆叠，改为 `SectionBand / LedgerRows / SplitPane / FlatSheet`。
3. **数据控件统一**：任务、文件、证据、模型、日志统一进入 `MetricLedger / EvidenceLedger / CommandConsole`。
4. **动效统一**：开屏为“线性装载 + 低透明呼吸”，滚动为平滑但不眩晕，鼠标动效只在命令按钮/分割线/操作热区出现。
5. **后端事件统一**：长任务全部抽象为 `job -> stage -> event -> artifact`，前端统一用 SSE/WebSocket/轮询之一渲染到执行台账。
6. **主题令牌统一**：warm graphite、paper gray、ink black、muted amber/green/red 状态色；禁止大面积蓝紫渐变。

## 分产品改造优先级

- OCR/RAG/文档类：先改 `EvidenceLedger + OutputSurface + CommandConsole`。
- Agent/Skill 平台：先改 `CommandRail + Skill Runtime Inspector + Tool Invocation Ledger`。
- 机器视觉/仿真：先改 `Simulation Timeline + Parameter Rows + Artifact Compare Surface`。
- 个人网站/展示类：先改首屏开场动画、长滚动叙事、项目索引，不要卡片瀑布流。

