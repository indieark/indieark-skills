# References

这些文件是 Skill 运行时按需读取的参考，不是仓库维护文档。只加载当前任务真正需要的文件。

硬约束：执行型图片任务必须通过 `imagen` CLI 落地；reference 只负责路由、方法和边界，不替代 CLI 执行。

加载顺序约定：**入口决策 → 场景与方法 → Provider 边界 → 运行时与产物**。这四组与 `../SKILL.md` 的「决策管线」一一对应；同一组内一次最多读一个文件，不要把整组都塞进上下文。

## 入口决策（Entry & Routing）

判断是否追问、选哪条任务路线、当前用户偏好哪种执行 route，以及真实生成前的执行确认。

| File | Load When |
| --- | --- |
| `interaction.md` | 需要判断是否追问、给方向选项、执行前确认、或是否可以继续调用 CLI；只追问会改变路由、成本或输出的问题 |
| `router.md` | 复杂请求需要选择交付物、输入素材角色、任务子路线、执行模式、方法、API/CLI 操作或验证路径 |
| `routes.md` | 首次真实生成、config preflight、跳过/恢复配置、检查默认模型或 route readiness、切换 Codex CLI/API key 优先级、或解释 `--route auto` |

## 场景与方法（Scenes & Craft）

把用户意图收束到具体 scene → 选择方法论 → 渲染成 prompt。

| File | Load When |
| --- | --- |
| `scenes.md` | 用户指定具体用途、画面类型或交付物，需要避免套通用模板 |
| `methods/README.md` | 需要选择构图、角色一致性、商品视觉、风格控制或编辑方法 |
| `methods/selection.md` | 方法选择不清，或一个任务可能需要多个方法 |
| `methods/prompt-patterns.md` | 需要把方法论压成可执行 prompt 骨架 |
| `reverse-prompting.md` | 用户提供参考图并要求模仿、照着、借鉴、复现感觉、提取风格/构图/色彩/光照/材质，或多图融合生成新图 |
| `gallery.md` | 需要从已迁移的 prompt atlas 中选择参考类别或案例（运行时入口） |
| `gallery/README.md` | 需要维护或迁移 gallery category 文件（仅维护视角） |
| `director.md` | 需要把用户意图整理为图像 prompt 或生成方案 |

## Provider 边界（Provider Boundary）

`imagen` CLI / 通用 API 边界 / provider-specific 参数 / adapter 契约。

| File | Load When |
| --- | --- |
| `cli.md` | 需要写 `scripts/imagen.py` 的命令行调用模板 |
| `api.md` | 需要确认 provider 能力边界、payload、真实调用或 dry-run 规则 |
| `api/README.md` | 需要维护 provider-specific API 参考目录 |
| `api/model-capabilities.md` | 需要比较当前已实现模型能力、尺寸限制、参数映射或未实现边界 |
| `api/nano-banana.md` | 需要维护 NB 模型、env、`/v1/images/*` 兼容代理或 `image` multipart 字段 |
| `api/mj.md` | 需要维护 MJ `/mj/submit/imagine`、task polling、prompt 参数或 URL 输出处理 |
| `provider-adapter.md` | 需要新增或修改 provider adapter |

## 运行时与产物（Runtime & Artifacts）

本地媒体、job 状态、run artifact、结果回复、迭代、安全。

| File | Load When |
| --- | --- |
| `media.md` | 需要处理图生图、`edit --image/--mask` 本地图片校验、预处理或 media manifest |
| `transparent-output.md` | 用户需要透明 PNG、去底、抠图素材、sprite/icon/product cutout 或干净 alpha 边缘 |
| `batches.md` | 用户需要批量生成、多 prompt、多素材集合、批量 dry-run、恢复或查看批量任务状态 |
| `jobs.md` | 需要查看、等待或删除本地 job 状态，或解释没有远端进度/id 的边界 |
| `reporting.md` | `imagen` 执行、dry-run、透明后处理、run/job 检查或失败后的 Skill 用户回复格式入口；细节按需读 `reporting/common.md` / `reporting/templates.md` |
| `workflow.md` | 需要定义 run artifact、证据链或 core workflow |
| `iteration.md` | 用户反馈结果不满意，需要定向修正 |
| `safety.md` | 需要处理私有素材、secret、输出文件或日志风险 |

## 维护约定

- 新增 reference > 100 行时必须建子目录或拆分，并在本表与 `../SKILL.md` 同步登记一行。
- 同一组内只能有一个文件作为「运行时入口」（如 `gallery.md`、`methods/README.md`、`cli.md`、`api.md`），子目录 `README.md` 只承载维护视角，不重复运行时入口的内容。
- `reporting.md` 是回复规范入口；`reporting/` 子目录只承载共享规则和模板，不新增 CLI 执行入口。
