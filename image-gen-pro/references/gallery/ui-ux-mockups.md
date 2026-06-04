# UI/UX Mockups Gallery

> Load when: 需要 App、dashboard、网页、工具界面、设计系统或游戏 UI mockup 参考。
> Avoid: 要实现真实前端代码，或只需要图标/单个素材。
> Pairs with: `../methods/ui-mockups.md`、`../methods/structured-prompts.md`、`../methods/typography.md`。

Source: adapted from `gpt_image_2_skill` gallery category `UI/UX Mockups`; prompts are rewritten for local use.

## Patterns

### SaaS Dashboard

- Use when: 运营工具、分析后台、数据平台或管理控制台。
- Example canvas: `1536x1024`
- Quality: `high`
- Prompt skeleton:

```text
Create a production-grade SaaS dashboard mockup for [domain].
Layout: sidebar navigation, top toolbar, main data area, right-side detail panel if useful.
Components: tables, charts, filters, status badges, action buttons.
State: populated with believable placeholder data.
Style: clean, compact, readable, not a marketing landing page.
Avoid: oversized hero blocks, unreadable microtext, decorative clutter.
```

### Mobile App Screen

- Use when: 单屏移动应用、设置页、个人页、任务流或消费类 App。
- Example canvas: `1024x1536`
- Quality: `high`
- Prompt skeleton:

```text
Create a mobile app screen for [app purpose].
User task: [primary action].
Layout: top bar, content area, controls, bottom navigation if needed.
Components: [cards/list/form/map/media/player].
Style: native-feeling, accessible spacing, clear hierarchy.
Avoid: fake brand logos, tiny unreadable text, impossible controls.
```

### Web App Editor

- Use when: 图像、文档、视频、地图、设计或内容编辑器界面。
- Example canvas: `1536x1024`
- Quality: `high`
- Prompt skeleton:

```text
Create a web app editor interface for [workflow].
Layout: canvas/work area, toolbar, side inspector, asset panel, status bar.
Controls: familiar icons, toggles, sliders, menus, tabs.
State: realistic in-progress project with selected item.
Style: utilitarian, dense but organized.
Avoid: empty hero page, decorative cards inside cards, unreadable labels.
```

### Design System Snapshot

- Use when: 展示组件库、主题、tokens、UI kit。
- Example canvas: `1536x1024`
- Quality: `medium` or `high`
- Prompt skeleton:

```text
Create a design system board for [product/domain].
Content: buttons, inputs, tabs, cards, table row, modal, color swatches.
Layout: organized component grid with consistent spacing.
Style: [brand mood], accessible contrast.
Avoid: random decorative elements, inconsistent component states.
```
