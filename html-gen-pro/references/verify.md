# Verify (Playwright MCP 视觉验证接力)

Load when: S5 五维 critique 即将完成 / 用户要求"看一眼实际渲染" / 工程质量维度需要截图证据。
Avoid: 不要把"渲染对就是设计好"——视觉验证只能证否（明显坏掉），不能替代五维 critique；不要假装看了截图而没真启动 MCP。
Pairs with: `flows.md` (S5), `critique.md`, `reporting.md`

## 立场

视觉验证是**可选**接力步骤，不是 S5 的硬性门。它解决一类特定问题：

- 浏览器实际渲染是否和我描述的一致？
- 移动端断点是否真的工作？
- 字体 / 图片 / 资源路径是否正确加载？
- 有没有控制台报错？

它**不解决**的问题：

- 美学方向是否对（这是 S3 + 五维 critique 第一维的责任）。
- 差异化记忆点是否成立（这是 S5 第五维的责任）。
- 工程质量结构是否合理（这是 critique 第四维的责任）。

## 一行接入

```bash
claude mcp add @playwright/mcp
```

接入后会暴露浏览器自动化能力（导航 / 截图 / 设备模拟 / 控制台监听）。具体 MCP 工具名以 Claude Code 内 `/mcp` 列表为准；本文件不写死工具名以避免随上游变化失同步。

## 3 个 prompt 模板

### 模板 1 · 全屏截图（landing-page / style-mockup 默认）

```text
请用 Playwright MCP 打开 _work/html_runs/<slug>/index.html，做以下事：

1. 设置 viewport 为 1440×900（desktop 默认）。
2. 等待页面 networkidle。
3. 截一张 fullPage = true 的截图，保存到 _work/html_runs/<slug>/screenshots/desktop-fullpage.png。
4. 把 console 错误日志（如有）列出来。
5. 把 HTTP 4xx / 5xx 失败请求（如有）列出来。

截图回贴给我后我会做五维 critique 第一维（视觉冲击）和第四维（工程质量）的回炉。
```

### 模板 2 · Above-the-fold（landing-page 首屏对齐）

```text
请用 Playwright MCP 打开 _work/html_runs/<slug>/index.html，做以下事：

1. 设置 viewport 为 1440×900。
2. 等待 networkidle。
3. 截一张 fullPage = false 的截图（首屏），保存到 _work/html_runs/<slug>/screenshots/desktop-fold.png。
4. 用 page.evaluate 取 hero 区第一个 <h1> 的 textContent + computed font-size + computed color，列出来。
5. 把首屏内能看见的 CTA 按钮的文案 + computed background-color 列出来。

我要看的是 hero 信息层级是否在 fold 之上立得住。
```

### 模板 3 · 移动端模拟（landing-page / app-frontend 响应式必查）

```text
请用 Playwright MCP 打开 _work/html_runs/<slug>/index.html，做以下事：

1. 模拟 iPhone 14（device = iPhone 14, viewport = 390×844, deviceScaleFactor = 3）。
2. 等待 networkidle。
3. 截两张：fold 截图 + fullPage 截图，分别保存到 _work/html_runs/<slug>/screenshots/mobile-fold.png 和 mobile-fullpage.png。
4. 把以下三个检查结果列出来：
   - 是否有水平滚动条（document.body.scrollWidth > window.innerWidth）。
   - 主要 CTA 按钮是否在 viewport 内可见且最小高度 ≥ 44px（iOS HIG 触控目标）。
   - 字体大小是否 ≥ 14px（iOS Safari 自动 zoom 阈值 16px，<14 多半要 zoom）。

我要看的是 mobile-first 是否真的工作。
```

## 没装 MCP 时的 fallback

不要因为没装 MCP 就跳过验证。退化路径：

1. **本地 dev server**：

   ```bash
   cd _work/html_runs/<slug>
   python -m http.server 8000
   ```

   告诉用户在浏览器打开 `http://localhost:8000/`，自行截图回贴。

2. **明确告诉用户你看不到截图**：

   > 我没启动 Playwright MCP，所以以下视觉相关结论是基于 HTML/CSS 阅读推断，不是基于实际渲染。如果你能截一张 desktop 全屏 + mobile fold 截图回贴，我可以做一次回炉。

3. **不要写"看起来 OK"**：未渲染不评价渲染。

## app-frontend 路线的特殊处理

app-frontend 产物多数是 Vite + React，需要先 `npm run dev`：

```bash
cd _work/html_runs/<slug>
npm install
npm run dev
```

然后让 Playwright MCP 打开 `http://localhost:5173/`（Vite 默认）。模板 1-3 的"打开 file://"替换为"打开 http://localhost:5173/"即可。

## existing-project-optimize 路线的特殊处理

`existing-project-optimize` 的产物在用户的项目仓库里，运行链路跟随项目原生策略：

- 若项目是 Next.js → `npm run dev` 后 MCP 打开对应路由。
- 若项目是 Vite + React → 同 app-frontend 路线。
- 若项目是纯静态站点 → 同 landing-page 路线（file:// 或 http.server）。

如果项目运行链路未知，**先问用户**：dev server 怎么跑？URL 是什么？

## 反 AI 坏习惯清单

- ❌ "我用 Playwright 截图看了，没问题"——除非你真在工具调用日志里看到了 MCP 调用。
- ❌ "页面在 mobile 下也很好看"——除非你做了 device emulation。
- ❌ "控制台没有错误"——除非你调用过 MCP 的 console 监听。
- ❌ 把 critique 第四维（工程质量）的结论建立在"没截图但我推测应该 OK"上。

## 与 reporting.md 的衔接

S5 完工汇报里"预览方式"和"视觉验证（可选）"两段必填：

- 预览方式：写明 file:// 路径或 dev server URL。
- 视觉验证：走了 MCP → 写命令 + 截图路径；没走 → 写原因（"用户未要求" / "MCP 未安装" / "时间限制"），不允许糊弄。
