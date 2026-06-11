# Iteration Guide

> Load when: 用户反馈生成结果不满意，需要定位问题并定向修改 prompt / 参数。
> Avoid: 用户首次提出需求但尚未生成；先走 `interaction.md` / `router.md`。
> Pairs with: `../../video-gen-director/references/director-method.md` 修改 prompt 字段；`examples/prompts/iteration-revision.md` 查看 R1 → R2 示例。

Use this when the first result is not good enough.

## Diagnose First

Map user feedback to one or two concrete causes:

| Feedback | Likely Cause | Primary Fix |
|----------|--------------|-------------|
| Unlike the reference image | Reference role or prompt relationship is too weak | Strengthen `reference_image` usage and reduce style drift |
| Motion is wrong | Prompt overdescribes static appearance or lacks motion reference | Use `reference_video` or split motion into phases |
| Too slow | Too much setup or weak action verbs | Shorten duration or increase action density |
| Too chaotic | Too many goals or conflicting styles | Remove secondary details and pick one camera plan |
| Sound is wrong | Audio intent is vague | Clarify music, sound effects, dialogue, or `reference_audio` role |
| Sound is generic or weak | `generate_audio=true` but no audio brief | Read `sound-design.md`, then add music / ambience / action SFX / dialogue constraints |
| No narrative | Prompt describes a poster, not a change | Add a clear A-to-B transformation |

## Revision Rule

Change only 1-3 high-impact points per iteration. Do not rewrite everything unless the user changes the goal.

## Useful Patterns

Subject consistency:

```text
保持参考图1中角色的发型、服装主色和面部轮廓，不改变人物身份；只让姿态和表情发生变化。
```

Motion correction:

```text
参考视频1只用于动作节奏和身体重心变化，不复制视频背景；动作从慢到快，第二拍开始加速。
```

Sound correction:

```text
参考音频1用于鼓点节奏和紧张情绪，画面动作在每个重拍上有一次明显推进；不要生成对白。
```

Simplification:

```text
删掉复杂转场和多角色，只保留一个主体、一个动作、一个镜头运动和一个情绪变化。
```

## Example Route

完整的 R1 → 用户反馈 → 诊断表 → R2 修订示例见 `examples/prompts/iteration-revision.md`。如果用户只反馈一个问题，优先只改一个字段；不要为了显得完整而重写全部 prompt。
