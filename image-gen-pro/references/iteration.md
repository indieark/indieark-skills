# Iteration Reference

> Load when: 用户对结果不满意，要求修改、重做、加强一致性或分析失败原因。
> Avoid: 第一次生成且需求已经明确。
> Pairs with: `director.md` 修改 prompt；`api.md` 判断是否需要 edit 或重新 generate。

目标是把反馈映射成最小修改，不重新发散。

## Feedback Mapping

| Feedback | Action |
| --- | --- |
| 主体不对 | 修正 Subject，必要时要求参考图 |
| 风格不对 | 修正 Style，保留原 Subject / Composition |
| 构图不对 | 修正 Composition，不重写全部 prompt |
| 细节多余 | 加 Constraints / Do not include |
| 角色不一致 | 进入 consistency 方法，要求或复用参考图 |
| 局部需要改 | 判断是否走 edit / mask，而不是重新 generate |
| 画幅或格式不对 | 只改 API/CLI 参数，不改创意 prompt |

## Revision Contract

每次迭代先写：

```text
Keep:
- ...

Change:
- ...

Reason:
- ...
```

然后再决定是重新生成、编辑输入图，还是只更新 prompt / payload。

## Guardrails

- 不把一次失败解释成所有 provider 都不适合。
- 不因为局部反馈重写完整创意方向。
- 不承诺无法验证的完全一致性。
- 如果用户要求保留大量细节，优先建议使用输入图编辑路径。
