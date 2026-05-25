# Examples

这些例子帮助 Agent 理解"完整导演链路 + API payload"的落地形态。每个例子至少包含 user intent、director prompt、CLI 形态，复杂的还附 payload JSON。

| Path | Input Mode | Purpose |
|------|------------|---------|
| `prompts/first-frame.md` | first frame | 单图 + 单镜头氛围片，无声 6 秒 |
| `payloads/first-frame.json` | first frame | 对应 payload，仅 `first_frame` 角色 |
| `prompts/omnireference-director.md` | omnireference | 同时使用参考图 / 参考视频 / 参考音频 |
| `payloads/omnireference.json` | omnireference | 对应 payload，三种 `reference_*` 角色 |
| `prompts/iteration-revision.md` | omnireference | 演示 R1 → R2 反馈映射，只改 1-3 处 |
| `payloads/iteration-revision.json` | omnireference | R2 修订后的 payload |

新增例子时同时说明：

- 用户意图是什么、目标场景类型。
- 哪些素材分别作为首帧、尾帧、参考图、参考视频或参考音频。
- prompt 如何显式引用参考内容（编号 + 用途）。
- payload 是否符合 `references/api.md` 的互斥规则（首尾帧不与 `reference_*` 混用；`reference_audio` 不单独）。

每次新增同时更新本表 + `references/cli.md`（如果引入新的 CLI 形态）。`scripts/validate_skill.py` 会校验所有 `payloads/*.json` 必须是合法 JSON 且包含 `model` 与 `content`。
