# Advisor Mode Reference

> Load when: 用户说「参考模式 / 我自己去 Sora|Veo3|Kling|Runway|Pixverse|Hailuo|Pika|即梦|Vidu 跑 / 只要 prompt / 给我素材包 / 不要生成」时。
> Avoid: 用户在 guide mode 下问"这个 Skill 怎么用"（这是 guide-mode.md 的范围）；用户已经明确要真实生成（这是默认 executor mode）。
> Pairs with: `../../video-gen-pro/SKILL.md` 的 `## Execution Modes` 定义三档模式；`../../video-gen-pro/references/completion.md` 的 Advisor Reference Pack 模板是回复格式；`../../video-gen-pro/references/interaction.md` 的 Advisor Mode 越界确认处理模式切换。

`advisor mode` 是「参考模式」的运行时入口。用户的诉求是：把 Skill 当成军师和资产管理员，让它输出可执行的视频参考包，自己拿到任意视频生成平台（Sora、Veo3、Kling、Runway、Pixverse、Hailuo MiniMax、Pika、即梦、Vidu 等）去跑，**不要本 Skill 调火山方舟 API 真实出片**。

它与 guide mode 不同：guide mode 解释 Skill 能力，不出活；advisor mode 出活——出参考包，但不调真实 API。

## Hard Rules

- 必须明确这是 advisor mode（参考模式），不会调用火山方舟 API，不会生成视频，不会下载 MP4。
- 禁止调用：`text-to-video` / `first-frame` / `first-last` / `omni` / `edit` / `extend`（非 `--dry-run-payload`）、`generate`（非 dry-run）、`wait` / `status`（这两个针对已提交任务，advisor mode 下没有已提交任务）。
- 允许调用：`config list` / `config get` / `doctor` / `project list` / `project show` / `asset search` / `asset list` / `asset show` / `script show` / `style show` / `storyboard show` / `history list` / `history show`，以及任何 6 个创建命令的 `--dry-run-payload` 形式（用于落证据 artifact）。
- 不要求用户先配置 API Key；advisor mode 全程不依赖火山方舟连接。
- 不声称已经生成、提交、等待或下载任何视频。
- 如果用户在 advisor mode 中明确切到 executor mode（"开始生成 / 现在出视频 / 真实跑 / 执行 / run it"），先复述请求要求一次明确确认，再按 `../../video-gen-pro/SKILL.md` 的强制执行协议从头走。

## Trigger Phrases

用户消息中任一出现即进入 advisor mode，不要追问确认：

- 「参考模式」/「advisor mode」/「advisor 模式」
- 「不要生成」/「别生成」/「不要调 API」/「不要调火山」/「不要出视频」
- 「我自己去跑」/「我自己用 Sora 跑」/「我自己用 Veo3 跑」/「我自己用 Kling 跑」/「我自己用 Runway 跑」/「我自己用 Pixverse 跑」/「我自己用 Hailuo 跑」/「我自己用 MiniMax 跑」/「我自己用 Pika 跑」/「我自己用即梦跑」/「我自己用 Vidu 跑」
- 「只要 prompt」/「只给提示词」/「只要素材包」/「给我素材包」/「给我参考包」/「给我资产」

触发词冲突时以最后一条用户消息为准。

## Required Workflow

1. 读 `../../video-gen-pro/references/interaction.md` 判断是否需要追问目标平台、画幅、时长、有声/无声、镜头数、是否长视频；advisor mode 下追问仍遵循"一次最多 3 个、只问会改变包内容的问题"。
2. 按需读 `../../video-gen-pro/references/router.md` 收束任务类型；advisor mode 下不进入 API 操作分支。
3. 按需读 `../../video-gen-director/references/director-method.md` / `../../video-gen-pro/references/scenes.md` / `../../video-gen-pro/references/methods.md` 形成镜头方案；复杂任务可读 `../../video-gen-assets/references/assets.md`、`../../video-gen-storyboard/references/visual-storyboard.md`、`../../video-gen-pro/references/sound-design.md`、`../../video-gen-script/references/multi-segment-continuity.md` 形成完整资产 brief 和拆段建议。
4. 选择性调用允许的只读 CLI 命令：例如用 `asset search` 检索本地已有角色/场景卡，写进参考包；用 `--dry-run-payload` 落证据。
5. 按 `../../video-gen-pro/references/completion.md` 的 Advisor Reference Pack 模板渲染回复。
6. 不要做"执行前确认卡"——advisor mode 不真实执行；但要在模式越界时按 `../../video-gen-pro/references/interaction.md` 的 Advisor Mode 越界确认处理。

## Reference Pack Contents

advisor 模式必须至少给出以下七项（用户明确说"只要 prompt 不要镜头清单"等局部要求时可削减；但不能默认偷工）：

1. **镜头清单 Shot List**：每个镜头给时长、画幅、镜头运动、主体动作；多段视频说明拆段方案（按 `../../video-gen-script/references/multi-segment-continuity.md` 的 Intelligent Orchestration Gate 思路判断）。
2. **Master Prompt**：中性主提示词，按镜头组织，不绑定任何平台语法，描述视觉事实和动作。
3. **平台变体 Platform Variants**：按用户提到的目标平台逐个产出；用户未指定时默认列 Sora / Veo3 / Kling / Runway Gen-3 四档。每个变体只写该平台需要的语法字段（Sora 的相机运动写法、Veo3 的 sound/dialogue 字段、Kling 的 motion control、Runway 的 motion brush 建议等），不要套通用模板。
4. **资产 brief**：角色卡 / 场景卡 / 道具/产品卡 / 故事板母图各自的描述性 prompt（让用户自己去图像平台生），并说明每张资产解决什么一致性问题。
5. **声音 brief**：音乐风格/情绪/BPM、环境音、动作音效、对白/旁白/无说话人声、字幕/标题文字。
6. **多段连续性建议**（如果是长视频）：拆段方案、连续性锚点（角色/场景/道具/光线）、段间衔接方式（硬切 / 尾帧硬衔接 / 延续运镜 / extend）。
7. **评判 checklist**：出片回来后用什么维度判断是否合格（主体识别度、镜头运动准确性、角色一致性、场景一致性、声画同步、字幕命中等）。

可选证据：`seedance2 <mode> ... --dry-run-payload` 留下的 artifact 路径（参考包配套，证明该路线在 Seedance 上也能跑；用户不需要时可省）。

## Do Not

- 不要在 advisor mode 输出"已生成视频"或"已提交任务"。
- 不要要求用户先给 API Key 才能拿到参考包。
- 不要在 advisor mode 调用 6 个创建命令的非 dry-run 形式、`generate`、`wait`、`status`。
- 不要只给 Master Prompt 就声称完成——平台变体、镜头清单、资产 brief、声音 brief、评判 checklist 是必给项。
- 不要静默切回 executor mode；用户没有明确"现在生成 / 真实跑 / 执行"时，advisor mode 持续生效。
- 不要把 advisor mode 输出的资产 brief 当作"已生成的角色卡/场景卡"登记进项目库——它们只是 prompt 描述。
