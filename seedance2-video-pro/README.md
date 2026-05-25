# seedance2-video-pro Skill Package

This is the canonical installable Skill package.

## Files

```text
SKILL.md
skill.json
CHANGELOG.md
agents/openai.yaml
scripts/seedance2_video.py        # API entrypoint
scripts/seedance2/                # modular CLI/API implementation
scripts/seedance2/review_pages.py # archived review artifact renderer
scripts/validate_skill.py         # local self-check (no network)
references/README.md              # canonical loading table
references/interaction.md
references/guide-mode.md
references/generation-workflow.md
references/router.md
references/scenes.md
references/methods/README.md
references/methods/clapperboard.md
references/methods/storyboard.md
references/visual-assets.md
references/visual-assets/README.md
references/visual-assets/principles.md
references/visual-assets/setting-director.md
references/visual-assets/character-sheet.md
references/visual-assets/scene-sheet.md
references/visual-assets/storyboard-board.md
references/visual-assets/script-composed-storyboard.md
references/visual-assets/grid-storyboard.md
references/visual-assets/four-column-storyboard.md
references/visual-assets/multi-segment-continuity.md
references/visual-assets/seedance-handoff.md
references/visual-storyboard.md
references/sound-design.md
references/director.md
references/api.md
references/cli.md
references/completion.md
references/iteration.md
examples/README.md
examples/prompts/
  first-frame.md
  omnireference-director.md
  iteration-revision.md
examples/payloads/
  first-frame.json
  omnireference.json
  iteration-revision.json
```

## Reference Routing

加载条件唯一权威表见 `references/README.md`。简要：

- `interaction.md`: 决定 ask / propose options / proceed。
- `guide-mode.md`: 功能介绍、使用向导、支持模式、准备事项和边界说明；不会调用 CLI 或生成视频。
- `generation-workflow.md`: 端到端生成流程、阶段提醒、剧本/资产/故事板确认、最终输入锁定、标准文本回复、结构化 JSON 修改意见和结果复盘。
- `router.md`: 任务类型、输入模式、场景、导演方法、API 操作和验证路径。
- `scenes.md`: Product / Drama / Action / Atmosphere / Social / Edit / Reference-Driven 场景边界。
- `references/methods/README.md`: 场记板（单镜头控场）vs 分镜（多节拍叙事），一次任务只选一个。
- `visual-assets.md`: 人物设定图、场景设定图、故事板母图、脚本拼版故事板、可选版式变体、智能编排、自动拆分和多段连续性方案的入口；二级索引见 `references/visual-assets/README.md`。
- `visual-storyboard.md`: 复杂任务的项目资产检索、视觉故事板、确认门和生成历史。
- `sound-design.md`: 有声/无声、音乐、环境音、动作音效、说话人声、字幕/标题文字、画面文字和参考音频用途。
- `director.md`: 导演 prompt、镜头、动作、声音和参考素材表达。
- `api.md`: 火山方舟 Seedance 2.0 API 入口、端点、互斥规则。
- `cli.md`: `scripts/seedance2_video.py` 和 `scripts/seedance2/` 的命令行模板与行为契约。
- `references/completion.md`: 生成完成后的标准用户回复，必须包含实际提示词、素材清单、结果、证据和验收结论。
- `iteration.md`: 反馈映射，1-3 处定向修改。

## Usage

First-time setup (saves config to `~/.config/seedance2/config.json` on POSIX or `%APPDATA%\seedance2\config.json` on Windows):

```bash
python scripts/seedance2_video.py setup
```

Complex tasks should search the project asset library before creating new character, scene, or storyboard assets:

```bash
python scripts/seedance2_video.py project list
python scripts/seedance2_video.py asset search --query "..."
python scripts/seedance2_video.py asset show <project-id> <asset-id>
python scripts/seedance2_video.py asset reuse <target-project-id> <source-project-id> <asset-id>
python scripts/seedance2_video.py project create "..."
python scripts/seedance2_video.py asset add <project-id> --type character --asset-id <character-id> --name <name> --file character-card.png
python scripts/seedance2_video.py asset add <project-id> --type scene --asset-id <scene-id> --name <name> --file scene-background-card.png
python scripts/seedance2_video.py storyboard add <project-id> --image storyboard.png --prompt storyboard-prompt.txt --video-prompt video-prompt.txt
python scripts/seedance2_video.py storyboard approve <project-id> <storyboard-id>
python scripts/seedance2_video.py generate --project <project-id> --storyboard <storyboard-id> --reference-image character-card.png --reference-image scene-background-card.png --wait
```

历史 review artifact renderer 仅用于归档实验复现；当前标准流程不使用它生成确认或复盘。

Six quick mode subcommands (text-to-video / first-frame / first-last / omni / edit / extend) remain compatible for quick samples. From this directory:

```bash
python scripts/seedance2_video.py text-to-video --prompt "..." --wait
```

From the repository root:

```bash
python skills/seedance2-video-pro/scripts/seedance2_video.py text-to-video --prompt "..." --wait
```

Full command index lives in `references/cli.md`.

## Self Check

修改 SKILL.md / references / examples 后跑：

```bash
python scripts/validate_skill.py
```

它不联网，只校验 frontmatter、加载表覆盖、内部链接、payload JSON。
