# Reporting

Load when: S5 五维 critique 完成、向用户做完工汇报时。
Avoid: 不要在产物未通过完整性 sanity check 时写汇报；不要让汇报本身代替 critique。
Pairs with: `critique.md`, `flows.md`, `usage.md`, `verify.md`

## 完工汇报模板

完工时按以下结构汇报，每一段都要填实，不允许留空：

```text
## 路线与美学方向

- 路线：{landing-page | app-frontend | existing-project-optimize | style-mockup}
- 气质：{vibe_description}
- 受众：{audience}
- 一句话差异化：{unique_angle}
- 是否调用 extension：{ui-ux-pro-max | taste-skill / <子 Skill 名> | 未调用（existing-project-optimize 路线）}

## 改动文件

{list of files changed; for existing-project-optimize use the project repo paths, otherwise list _work/html_runs/<slug>/* paths}

- 新增：…
- 修改：…
- 删除：…

## 五维 critique 结论

详细自查见 critique.md；本汇报只列结论一句：

- 视觉冲击：{Pass | Partial | Fail} — {一句话}
- 信息层级：{Pass | Partial | Fail} — {一句话}
- 交互细节：{Pass | Partial | Fail} — {一句话}
- 工程质量：{Pass | Partial | Fail} — {一句话}
- **差异化记忆点**：{必填} — {这页面凭什么和别的不一样，1-2 句话}

## 预览方式

- 浏览器打开：{file:// 路径 或 dev server 地址}
- 视觉验证（可选）：{是否走 Playwright MCP；走的话写命令；没走说原因}

## 残余风险

- {至少 1 条；如真无风险也要写"无显著残余风险，依据 …"}
- 已知限制：…
- 待办（如有）：…

## 接力建议

- 合规审查：是否建议接 web-design-guidelines？
- 可访问性深度审查：是否需要走专门 a11y audit？
- 视觉验证：是否建议用户用 Playwright MCP 截图回贴？
- 关联资产：是否要联动 image-gen-pro 出主视觉 / video-gen-pro 出 hero 动画？
```

## 路线特有补充字段

### `landing-page`

加 "行业 + industry rules 调用情况"：

```text
- 行业：{SaaS | 电商 | 内容 | 工具 | 教育 | 医疗 | 金融 | 房产 | 招聘 | 其他}
- 调用的 industry rules：{从 ui-ux-pro-max 的 161 条里选了哪几条}
- 选用的 palette + font pairing：{palette name + font pairing name}
```

### `app-frontend`

加 "信息密度 + 使用的 UX guidelines 大类"：

```text
- 信息密度：{dense | spacious | 平衡}
- 调用的 UX guidelines 大类：{从 99 条里覆盖了哪些大类，如 "navigation" / "empty states" / "error feedback" / "accessibility"}
- 默认技术栈是否被覆盖：{Vite + React + Tailwind | 切换到 {用户指定栈}}
```

### `existing-project-optimize`

加 "原生栈 + 业务逻辑零侵入证明"：

```text
- 项目原生栈：{见 package.json 摘要}
- 设计系统是否兼容：{是 / 否；不兼容时如何处理}
- 业务逻辑是否被改动：**不应** 被改动；如有改动须用户书面确认
- 改动的视觉/组件文件：{逐项列出}
- 提交目标仓库：{该项目仓库的 commit / 不是 html-gen-pro 仓库的 commit}
```

### `style-mockup`

加 "风格纯粹度 + extension 分支 + 全局风格 Skill 链入"：

```text
- 风格：{claymorphism | glassmorphism | liquid-glass | neubrutalism | brutalist | swiss | magazine | editorial | 杂志风 | 终端风 | Y2K | cyber | vaporwave | luxury(soft) | ...}
- extension 分支：{ui-ux-pro-max（默认 / 67 styles 库）| taste-skill / brutalist-skill（brutalist · swiss）| taste-skill / soft-skill（luxury(soft)）}
- 是否链入全局风格 Skill：{是 / 否；是则列出 Skill 名（仅 ui-ux-pro-max 分支可能需要；taste-skill 分支沿用子 Skill 自持立场）}
- ui-ux-pro-max 分支：67 styles 库调用 = {从 ui-ux-pro-max 的 67 styles 里取了哪一条}
- taste-skill 分支：dials 设定 = {DESIGN_VARIANCE: x / MOTION_INTENSITY: y / VISUAL_DENSITY: z}
- mockup 限制：{desktop-only | 含响应式演示}
```

## 汇报立场（反 AI 收尾习惯）

- **不要假装看了截图**：除非确实启动了 Playwright MCP 或用户回贴了截图。
- **不要给"全 Pass"自评**：五维至少一维应该有可改进点；如真全 Pass 必须给出"为什么这次能全 Pass"的具体证据。
- **不要给"差异化记忆点"打模糊牌**：如"现代简约 / 视觉简洁 / 用户友好"是 AI slop 词汇，不算差异化。要能说出"这页面用了 X 元素 / Y 排版手法 / Z 文案钩子，所以和别的 SaaS Landing 不一样"。
- **不要在汇报里宣传 extension 的能力**：用户不关心 ui-ux-pro-max 有多少条 industry rules、taste-skill 的 dials 有多精细；他只关心你产出了什么、靠什么决策。
