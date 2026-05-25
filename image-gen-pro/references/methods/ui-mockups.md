# UI Mockups Method

> Load when: App、dashboard、web UI、工具界面、游戏 UI 或设计系统 mockup 需要生成。
> Avoid: 要实现真实前端代码；那应转到代码实现流程。
> Pairs with: `structured-prompts.md` 管理页面规格；`typography.md` 控制界面文字。

## Core Idea

UI prompt 要像产品规格，不像氛围描述。先定义用户、任务、信息架构和组件密度。

## Required Fields

- Product/domain.
- Primary user task.
- View type: dashboard, editor, settings, profile, store page.
- Layout: nav, sidebar, content, inspector, toolbar.
- Component list.
- Density: compact operational vs spacious marketing.
- State: empty, loading, populated, error.

## Mini Template

```text
Create a UI mockup for [product/domain].
User task: [primary workflow].
Layout: [nav/sidebar/content/toolbar/panels].
Components: [tables/cards/forms/charts/buttons].
State: [populated/empty/error/loading].
Style: [design system mood], readable, production-grade.
Avoid: marketing hero layout, fake unreadable microtext, decorative clutter.
```

## IndieArk Bias

- 工具类产品优先密集、清晰、可扫描。
- 不做大面积营销 hero，除非用户明确要 landing page。
- 重要按钮和状态要可见。
- 表格、筛选、批量操作、历史记录这些工作流元素通常比装饰更重要。

## Debug

- 太像宣传页：增加工作区、导航、列表和操作控件。
- 太空：提高信息密度。
- 文字乱：减少精确文字，用可读占位或后期文字。
