# Reporting Templates

Load through `../reporting.md` when writing exact user-facing replies.

## Real Generate / Edit

```text
已完成：<生成/编辑结果已保存>
输出：<path(s)>
预览：<preview path>
<Markdown image preview when local preview exists>
实际分辨率：<resolution(s)>
尺寸比例：<aspect_ratio(s)>
Run：<run-id>
Route：<route>

Original Prompt：<current user request or summary>
Final Prompt：<prompt.txt path or short final prompt>
Method：<direct-generation / edit / reverse-prompting / method label>，<one-line reason>
验证：<job/result/output/preview/media checks actually performed>
```

## Batch

```text
已完成：批量任务 <batch-id> 已结束，成功 <succeeded>/<total>。
输出：<batch state or representative output paths>
预览：<batch contact-sheet path or unavailable reason>
<Markdown image preview when local preview exists>
实际分辨率：<unique resolutions or representative per-item values>
尺寸比例：<unique aspect ratios or representative per-item values>
Batch：<batch-id>

Method：batch-generate，manifest-driven batch through existing generate/edit routes.
验证：status=<status>，counts=<counts>，state.json=<path>，summary.json=<path>。
```

If the batch has failures, use the failure template and include the failed count.

## Transparent Output

```text
已完成：已生成真实透明 PNG。
输出：<transparent png path>
预览：<preview path if created>
<Markdown image preview when local preview exists>
实际分辨率：<resolution>
尺寸比例：<aspect_ratio>
源图：<chroma source path>

Original Prompt：<user request>
Final Prompt：<source-generation prompt path if generated, otherwise not applicable>
Method：transparent-output，先生成/使用纯色背景源图，再通过 imagen transparent 后处理 alpha。
验证：PNG 带 alpha，alpha bbox=<bbox>，metadata=<metadata path>。
```

## Dry-Run / Payload Dry-Run

```text
已完成：已写入 dry-run artifact，未提交 provider，未生成图片。
输出：未生成图片
预览：无
实际分辨率：不适用
尺寸比例：不适用
Run：<run-id>
Route：dry-run / payload-dry-run

Original Prompt：<user request>
Final Prompt：<prompt.txt path or prompt draft>
Method：dry-run，artifact-only validation.
验证：provider_api_call=false，artifact=<summary/request path>。
```

## Advisor Reference Pack

advisor mode 专用。用于回应「参考模式 / 我自己去跑 / 不要生成 / 只要素材包」等触发场景；本卡片不调用 `imagen generate|edit|batches run` 非 dry-run 命令，也不声称已生成图片。

```text
已完成：已输出参考包，未调用 provider，未生成图片。
模式：advisor mode（参考模式）
目标平台：<MJ / Sora / Flux / SD ComfyUI / 即梦 / 可灵 / ... 按用户指定>

Original Prompt：<user request>
Master Prompt（中性主提示词）：<不绑定任何平台语法的描述>

平台适配变体：
- MJ：<MJ 语法版本，含 --ar / --v / --sd|--hd / --style / --sref 等需要时；不需要的字段不填占位>
- Sora：<Sora 语法版本，含镜头/时长/相机运动等需要时>
- Flux：<Flux/Replicate/Krea 等接受的自然语言提示词版本>
- SD ComfyUI：<正向 prompt + 负向 prompt + 关键节点建议>
- <其他用户指定平台>：<对应语法版本>

参考图收集 checklist：
- 结构 / 构图：<建议参考素材类型>
- 风格 / 笔触：<建议参考素材类型>
- 配色 / 光照：<建议参考素材类型>
- 材质 / 细节：<建议参考素材类型>
- 角色 / 主体（如适用）：<建议参考素材类型>

评判 checklist（出图回来后用以下维度判断）：
- <维度 1：例如主体识别度>
- <维度 2：例如光线方向一致性>
- <维度 3：例如构图比例还原>
- <维度 N>

可选证据：<imagen plan / --dry-run-payload artifact 路径，或「未生成证据 artifact」>
Method：advisor，资产 + 方法论交付；不提交 provider，不写 outputs。
验证：provider_api_call=false；artifact=<plan/payload artifact 路径或「无」>。
```

## Inspection / Config / Doctor

```text
已完成：已读取当前运行状态。
状态：<active model / route / job status / config state>
路径：<config path / run dir / batch dir / artifact path>
预览：<preview path if this inspection found one>
<Markdown image preview when local preview exists>

Method：runtime-inspect，读取本机配置或已保存 artifact，不提交 provider。
验证：<exact command and facts checked; secrets are masked>
```

## Failure

```text
未完成：<one-line failure>
失败层：<config / input / CLI / route / provider / post-process / validation>
Run / Batch：<id if available>
已保存：<artifact path if available>

Original Prompt：<user request or summary>
Final Prompt：<prompt.txt path if it exists, otherwise "未形成最终 prompt">
Method：<chosen method before failure>
下一步：<one concrete corrective action>
```
