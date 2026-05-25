# Workflow

Load when: 用户要规划演示文稿、PPT、PPTX、slides 或 deck 的生成流程。
Avoid: 不要把本文件当成真实生成或导出实现。
Pairs with: `route-introduction.md`, `usage.md`, `router.md`, `reporting.md`

## Router Workflow

1. Clarify audience, goal, context, duration, language, output format, and source materials.
2. Load `route-introduction.md`, then present the three route options: image-first PPT, web/HTML PPT, and SVG PPT.
3. Recommend one route based on deliverable, editability, visual fidelity, and presentation context.
4. Ask the user to choose or accept the recommendation.
5. Load `usage.md`, then check/install the selected extension if needed.
6. Open the selected extension's explicit Skill entry path and delegate the detailed generation workflow to that Skill.
7. Report selected route, output paths, and verification.

## 当前边界

`ppt-gen-pro` 本身不实现 native PPT renderer。真实生成由已安装的外部扩展执行，本 Skill 负责强触发、路由、安装检查、选择确认和委托。
