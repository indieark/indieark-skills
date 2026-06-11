# video-gen-pro Skill Package

This is the canonical installable Skill package — video-gen 技能族的 **hub**（执行器 + 路由枢纽）。方法论、剧本编排、资产与填料层参考已拆分到 7 个同级卫星 skill（`../video-gen-script` / `../video-gen-guide` / `../video-gen-advisor` / `../video-gen-director` / `../video-gen-storyboard` / `../video-gen-assets` / `../video-gen-cinematography`），CLI 与脚本全部留在本包。

## Files

```text
SKILL.md
skill.json
CHANGELOG.md
agents/openai.yaml
scripts/video_gen_pro.py        # API entrypoint
scripts/seedance2/                # modular CLI/API implementation
scripts/seedance2/review_pages.py # archived review artifact renderer
scripts/validate_skill.py         # local self-check (no network)
references/README.md              # canonical loading table
references/concepts.md
references/interaction.md
references/router.md
references/scenes.md
references/methods.md             # 方法选择门（导演法/故事板法细则在卫星）
references/sound-design.md
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

加载条件唯一权威表见 `references/README.md`。hub 留守文件简要：

- `concepts.md`: 剧本 / 资产 / 方法论三分概念与归类边界。
- `interaction.md`: 决定 ask / propose options / proceed；advisor mode 越界确认。
- `router.md`: 任务类型、输入模式、场景、导演方法、API 操作和验证路径。
- `scenes.md`: Product / Drama / Action / Atmosphere / Social / Edit / Reference-Driven 场景边界。
- `references/methods.md`: 导演法（文字为主、资产为辅直接控场、不另生成图像母图，用三段式骨架做单/少镜头控场）/ 故事板法（先用资产生成图像母图再主控）两种并列方法的选择门，一次任务只选一个主结构。
- `sound-design.md`: 有声/无声、音乐、环境音、动作音效、说话人声、字幕/标题文字、画面文字和参考音频用途。
- `api.md`: 火山方舟 Seedance 2.0 API 入口、端点、互斥规则。
- `cli.md`: `scripts/video_gen_pro.py` 和 `scripts/seedance2/` 的命令行模板与行为契约。
- `references/completion.md`: 生成完成后的标准用户回复，必须包含实际提示词、素材清单、结果、证据和验收结论。
- `iteration.md`: 反馈映射，1-3 处定向修改。

迁出参考的现归属见 `references/README.md` 的「卫星 references」表：guide-mode／advisor-mode／generation-workflow／multi-segment-continuity／director-method／故事板族／资产族／输入指南分别在对应卫星 skill。

## Usage

First-time setup (saves config to `~/.config/video-gen-pro/config.json` on POSIX or `%APPDATA%\video-gen-pro\config.json` on Windows):

```bash
videogen setup
```

Complex tasks should search the project asset library before creating new character, scene, or storyboard assets:

```bash
python scripts/video_gen_pro.py project list
python scripts/video_gen_pro.py asset search --query "..."
python scripts/video_gen_pro.py asset show <project-id> <asset-id>
python scripts/video_gen_pro.py asset reuse <target-project-id> <source-project-id> <asset-id>
python scripts/video_gen_pro.py project create "..."
python scripts/video_gen_pro.py asset add <project-id> --type character --asset-id <character-id> --name <name> --file character-card.png
python scripts/video_gen_pro.py asset add <project-id> --type scene --asset-id <scene-id> --name <name> --file scene-background-card.png
python scripts/video_gen_pro.py storyboard add <project-id> --image storyboard.png --prompt storyboard-prompt.txt --video-prompt video-prompt.txt
python scripts/video_gen_pro.py storyboard approve <project-id> <storyboard-id>
python scripts/video_gen_pro.py generate --project <project-id> --storyboard <storyboard-id> --reference-image character-card.png --reference-image scene-background-card.png --wait
```

历史 review artifact renderer 仅用于归档实验复现；当前标准流程不使用它生成确认或复盘。

Six quick mode subcommands (text-to-video / first-frame / first-last / omni / edit / extend) remain compatible for quick samples. From this directory:

```bash
python scripts/video_gen_pro.py text-to-video --prompt "..." --wait
```

From the repository root:

```bash
videogen text-to-video --prompt "..." --wait
```

Full command index lives in `references/cli.md`.

## Self Check

修改 SKILL.md / references / examples 后跑：

```bash
python scripts/validate_skill.py
```

它不联网，只校验 frontmatter、加载表覆盖、内部链接、payload JSON。
