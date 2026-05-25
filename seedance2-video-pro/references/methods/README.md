# Director Methods

> Load when: 已确定场景，但需要选择场记板、分镜或不使用方法。
> Avoid: 用户只要轻量一句 prompt、API 参数说明或反馈修正。
> Pairs with: `../scenes.md` 提供场景信号；`../director.md` 将选中的方法转为 prompt 字段。

本目录分开存储可复用导演方法。`SKILL.md` 和 `director.md` 只负责选择方法，不把所有方法融合成一份大模板。

## Method Index

| Method | File | Primary scenes | Use When | Do Not Use When |
|--------|------|----------------|----------|-----------------|
| 场记板 / Slate | `clapperboard.md` | Character Action / Atmosphere / Video Edit / Reference-Driven | 用户需要镜头执行清晰、素材/声音/限制较多、需要像拍摄通告一样控场 | 用户需要多节拍叙事、短剧转折、广告起承转合 |
| 分镜 / Storyboard | `storyboard.md` | Product / Short Drama / Social Short | 用户需要多镜头、起承转合、短剧/广告/产品展示节奏 | 用户明确只要一个连续镜头、克制氛围或严格素材控场 |

## Selection Rule

先读 `../scenes.md` 判断场景，再选择方法：

```text
场景明确 -> 选择一个最轻的方法 -> 只填会影响生成结果的字段 -> 写入 Seedance prompt
```

不要把多个方法完整叠加到一个 prompt。可以吸收多个方法的思路，但输出必须服务用户当前场景。
