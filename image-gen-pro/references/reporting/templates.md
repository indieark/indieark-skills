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
