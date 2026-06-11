# Scene Routing Reference

> Load when: 用户指定具体用途、场景、素材组合，或需要避免把请求强套成通用模板。
> Avoid: 用户只问 API 参数、任务状态、下载结果，或已进入单纯反馈修正。
> Pairs with: `methods.md` 在导演法/故事板法间选择；`../../video-gen-director/references/director-method.md` 把场景裁剪成三段式 prompt 字段（时序递进写在【画面内容】里）。

Seedance 2.0 导演链路必须先判断场景，再决定是否追问、怎么组织 prompt、用哪种 API 输入模式。不要把所有用户请求强行套进同一个公式。

## Core Rule

如果用户给了明确场景、用途或限制，先保留它，再补缺口。不要替用户改题。

```text
用户指定场景 -> 保持场景边界 -> 判断素材角色 -> 只追问会影响成片的关键缺口 -> 写适配该场景的导演 prompt
```

固定 prompt 结构只是检查工具，不是必须逐项输出的表格。没有参考素材时不要写“参考关系”；无声视频不要写声音段落；极短动作片不要塞复杂三幕剧。

## When to Ask vs Act

先追问：

- 用户只说“做个视频”“帮我生成一个广告”，没有主体、用途、画幅、时长或声音取向。
- 用户给了多个素材但没说明每个素材用途。
- 用户要高成本生成，但有 2 个以上方向都合理。
- 用户指定“像某个参考”但可能涉及角色一致性、版权、品牌或敏感素材边界。

直接收束并执行：

- 用户已经给出主体、场景、画幅、时长、声音和素材角色。
- 用户明确说“按这个图动起来”“用这段视频做动作参考”。
- 用户只缺少低风险参数，可用保守默认值并说明。

## Scene Types

### Product / Commercial

Use when: 产品展示、广告、品牌短片、电商视频。

Recommended method: `../../video-gen-director/references/director-method.md`，卖点递进写在【画面内容】里按时序推进；素材/参数强约束时收紧到单一连续动作。

Prioritize:

- 产品外观、材质、卖点和品牌调性。
- 镜头应服务信息传达：开场识别产品，中段展示功能，末尾留下记忆点。
- 声音可以是节奏、质感、环境音或一句短口播。

Avoid:

- 把产品变成背景道具。
- 塞复杂故事导致卖点不清。
- 加入未授权 logo 或文字。

### Short Drama / Narrative

Use when: 短剧、故事、人物冲突、剧情转折。

Recommended method: `../../video-gen-director/references/director-method.md`，情绪/动作转折写在【画面内容】里按时序推进，但 5-15 秒内只保留一个事件或转折。

Prioritize:

- 角色目标、情绪变化、一个可见动作转折。
- 5-15 秒内只做一个清楚事件。
- 镜头从场景建立转向情绪/动作结果。

Avoid:

- 一次讲完整长剧情。
- 多角色多地点跳切。
- 过度解释世界观。

### Character Action

Use when: 人物动作、舞蹈、跑步、打斗、姿态变化。

Recommended method: `../../video-gen-director/references/director-method.md` 用于主体一致性和动作路径控场；复杂舞蹈在【画面内容】里把动作按时序拆成几个阶段写清。

Prioritize:

- 主体一致性、动作路径、镜头跟随方式。
- 参考视频用于动作节奏时，要说明“不复制背景，只参考动作/节奏/运镜”。
- 时长短时分两段即可：准备 -> 完成动作。

Avoid:

- 同时要求多个复杂动作。
- 让镜头和人物运动方向冲突。
- 对参考图形象约束不清。

### Atmosphere / Mood Film

Use when: 氛围片、风景、情绪、抽象视觉、电影感片段。

Recommended method: `../../video-gen-director/references/director-method.md` 或不加载方法；避免无必要分镜。

Prioritize:

- 光线、天气、空间层次、慢速变化。
- 一个核心视觉变化，例如雾散、灯亮、风吹、镜头推近。
- 声音可作为情绪补强，不必有对白。

Avoid:

- 只有静态形容词，没有运动。
- 风格词堆叠过多。
- 把抽象概念写成不可见指令。

### Social Short / Viral Hook

Use when: 短视频开头、社媒、爆点、反差、节奏强。

Recommended method: `../../video-gen-director/references/director-method.md`，【画面内容】的时序递进首段（前 1-2 秒）必须承担钩子。

Prioritize:

- 前 1-2 秒就有可见吸引点。
- 动作和镜头更直接。
- 画幅通常优先 `9:16`，除非用户指定。

Avoid:

- 慢热铺垫。
- 太多旁白和字幕依赖。
- 把所有卖点塞进一个镜头。

### Video Edit / Extension

Use when: 用户给视频并要求替换、延长、改元素、继续叙事。

Recommended method: `../../video-gen-director/references/director-method.md`，重点写清保留 / 改变 / 延续边界。

Prioritize:

- 明确保留什么、改变什么、延长到哪里。
- 参考视频作为时间、动作、运镜和场景连续性来源。
- 不要无故改变主体身份、服装、空间方向。

Avoid:

- 把编辑任务当成全新文生视频。
- 没写清“保留/改变/延续”的边界。

### Reference-Driven Generation

Use when: 用户提供图片、视频、音频并要求综合参考。

Recommended method: `../../video-gen-director/references/director-method.md` 用于素材角色控场；如果素材服务于叙事递进，在【画面内容】里按时序展开。

Prioritize:

- 为每个素材编号并说明用途。
- 图片通常用于角色/产品/场景外观。
- 视频通常用于动作、节奏、运镜、空间运动。
- 音频通常用于节拍、情绪、音色、对白参考，不能单独作为唯一参考输入。

Avoid:

- “参考所有素材”这种笼统写法。
- 让参考素材之间互相冲突。

## Prompt Assembly Rules

按场景选模块，不必全量输出：

- 必选：成片目标、主体/场景、一个核心动作或变化。
- 有素材才写：参考关系。
- 有镜头要求才写：镜头设计。
- 有节奏要求才写：时间段。
- 有声才写：声音设计。
- 有硬限制才写：保持/禁止/不要。

最后用自检清理：

- 是否尊重了用户指定场景？
- 是否只追问了真正影响结果的问题？
- 是否有可见运动或变化？
- 是否没有把所有场景套成同一个产品广告/电影模板？
