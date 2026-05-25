# References

运行时按需加载下列文件，不要一次性复制所有内容到回复里。

| 文件 | Load when | Avoid | Pairs with |
| ---- | ---- | ---- | ---- |
| [`workflow.md`](workflow.md) | 用户要规划 PPT / deck 工作流 | 不要当成已实现执行流程 | `router.md` |
| [`route-introduction.md`](route-introduction.md) | 用户要生成真实 PPT 前，需要介绍三种路线并推荐 | 不要跳过选择门直接生成 | `router.md`, `reporting.md` |
| [`usage.md`](usage.md) | 用户选择路线后，需要明确安装检查、外部 Skill 入口和委托顺序 | 不要猜外部 Skill 路径 | `install.md`, `extensions.md` |
| [`router.md`](router.md) | 需要判断图片 / 网页 / SVG PPT 路线 | 不要在用户未选择前直接生成 | `extensions.md` |
| [`extensions.md`](extensions.md) | 需要说明三种外部扩展来源和委托规则 | 不要复制外部仓库实现 | `install.md` |
| [`install.md`](install.md) | 用户安装、首次使用或本地缺扩展 | 不要静默跳过安装检查 | `extensions.md` |
| [`reporting.md`](reporting.md) | 需要汇报路由选择、输出和验证 | 不要编造生成结果 | `workflow.md` |
| [`cli.md`](cli.md) | 用户问 CLI 或安装执行 | 不要假装存在原生 PPT renderer | `install.md` |
| [`capability-matrix.md`](capability-matrix.md) | 用户对比四条路线能力 / 选型决策需要结构化辅证 | 不要拿本表替代 `router.md` 触发判定 | `router.md`, `route-introduction.md`, `extensions.md` |
