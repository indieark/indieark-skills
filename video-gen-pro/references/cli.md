# CLI Reference

> Load when: 需要写、解释或核对 `scripts/video_gen_pro.py` 命令行调用。
> Avoid: 只需要判断是否追问、写导演 prompt，或用户只问官方 API payload。
> Pairs with: `api.md` 确认参数语义；`examples/README.md` 查看端到端 prompt + payload 示例。

`videogen` 0.4.x 起包含项目资产库和视觉故事板工作流。顶层命令分为：配置（`setup` / `doctor` / `config`）、项目库（`project` / `asset` / `script` / `style` / `storyboard` / `history`）、故事板生成（`generate`）、6 个快速输入模式（`text-to-video` / `first-frame` / `first-last` / `omni` / `edit` / `extend`）、任务管理（`status` / `wait` / `list` / `delete`）和 2 个可选 callback 调试入口（`callback-server` / `callback-smoke`）。`asset` 支持登记、项目内筛选、单项查看、跨项目检索和复用，用于生成前判断是否已有可复用角色/场景素材，并在复用到当前项目时保留来源回溯。所有命令默认 JSON 输出；加 `--format markdown` 转人读。

## Auth & 配置

API key 解析顺序：`--api-key` > `ARK_API_KEY` > `SEEDANCE_API_KEY`（兼容）> 配置文件 `api_key`。

首次配置走交互式向导：

```bash
videogen setup
```

非交互（CI / 脚本）：

```bash
videogen setup \
  --non-interactive \
  --api-key "your-ark-api-key" \
  --model doubao-seedance-2-0-260128 \
  --default-ratio adaptive \
  --default-duration 5
```

健康检查（联通 API、显示当前来源 cli/env/config_file/default）：

```bash
videogen doctor
videogen doctor --skip-connectivity
```

`doctor` 还会输出可选本地工具矩阵。缺少这些工具不会让 `doctor` 失败，但当素材需要自动修复或本地视频需要临时 HTTPS 暴露时会变成明确阻断：

| Check | 什么时候需要 | 建议安装 | 可替代方法 |
|-------|--------------|----------|------------|
| `tool:pillow` | 图片格式、大小、尺寸、比例需要自动处理后再 Base64 上传 | `python -m pip install pillow` | 换合规图片，或提供 HTTPS/signed URL |
| `tool:ffmpeg` | 音频/视频需要转码、截断、缩放、补边或 FPS 规范化 | `winget install Gyan.FFmpeg` | 换合规素材，或提供 HTTPS/signed URL / `asset://` |
| `tool:ffprobe` | 需要提交前探测音频/视频时长、编码、FPS、尺寸和总时长 | `winget install Gyan.FFmpeg` | 不安装时不可探测字段写 manifest warning |
| `tool:cloudflared` | 本地 `reference_video` 要用 `--serve-local-assets cloudflare` 生成临时 HTTPS URL | `winget install Cloudflare.cloudflared` | 提供 HTTPS/signed video URL，或用 `asset://` |

查看与编辑配置（`api_key` 在所有读路径自动脱敏）：

```bash
videogen config path
videogen config list
videogen config get model
videogen config set default_ratio 9:16
videogen config unset default_watermark
```

创建命令省略 `--model`、`--resolution`、`--ratio`、`--duration`、`--generate-audio`、`--watermark` 时，会使用配置文件中的默认值；`config set` 会按键名保存布尔值和整数，不把 `false` / `8` 错存成字符串。

配置文件位置（`VIDEO_GEN_PRO_CONFIG_DIR` 可覆盖）：

| OS | Path |
|----|------|
| POSIX | `${XDG_CONFIG_HOME:-~/.config}/video-gen-pro/config.json` |
| Windows | `%APPDATA%\video-gen-pro\config.json` |

## Models

- `doubao-seedance-2-0-260128`：默认，质量优先。
- `doubao-seedance-2-0-fast-260128`：速度/成本优先。

不要回退 1.0 / 1.5 模型。


## Operations 总览

| Operation | Command Skeleton |
|-----------|------------------|
| 创建项目 | `videogen project create "用户原始想法"` |
| 检索资产 | `videogen asset search [--query ...] [--tag ...] [--type character|scene|prop|graphic|voice]` |
| 查看资产 | `videogen asset show <project_id> <asset_id>` |
| 复用资产 | `videogen asset reuse <target_project_id> <source_project_id> <source_asset_id>` |
| 登记资产 | `videogen asset add <project_id> --type character|scene|prop|graphic|voice --name ... --file image.png --tag ... --role ...` |
| 保存剧本/风格 | `script set <project_id> --file <script-file>` / `style set <project_id> --file <style-file>` |
| 故事板 | `storyboard plan/add/show/approve <project_id>` |
| 项目化生成 | `videogen generate --project <project_id> --storyboard <storyboard_id> [--reference-image <character-card>] [--reference-image <scene-background-card>] [--wait]` |
| 创建 (text-to-video) | `videogen text-to-video (--prompt "..." | --prompt-file prompt.txt) [--web-search] [--wait] [--download outputs]` |
| 创建 (first frame) | `videogen first-frame --first-frame frame.png [--prompt "..."] [--wait]` |
| 创建 (first+last) | `videogen first-last --first-frame start.png --last-frame end.png [--prompt "..."] [--wait]` |
| 创建 (omni) | `videogen omni [--prompt "..."] [--reference-image ...] [--reference-video https://...] [--reference-audio ...]` |
| 创建 (edit-intent) | `videogen edit --reference-video https://... [--prompt "..."] [--reference-image hint.png]` |
| 创建 (extend) | `videogen extend --reference-video https://... [--prompt "..."]` |
| 查询 | `videogen status <task_id>` |
| 等待 + 下载 | `videogen wait <task_id> --download outputs` |
| 列表 | `videogen list [--page-size 10] [--status running]` |
| 取消/删除 | `videogen delete <task_id>` |
| 生成历史 | `videogen history list <project_id>` |
| Callback receiver | `videogen callback-server --port 8787 --out-dir _work/seedance_callbacks` |
| Callback smoke test | `videogen callback-smoke http://127.0.0.1:8787/callback` |

每个创建命令都接受这些通用选项：`--prompt`、`--prompt-file`、`--model`、`--resolution`、`--ratio`、`--duration`、`--generate-audio`、`--watermark`、`--seed`、`--return-last-frame`、`--callback-url`、`--execution-expires-after`、`--service-tier`、`--safety-identifier`、`--wait`、`--interval`、`--timeout`、`--download`、`--format`、`--dry-run-payload`、`--run-dir`、`--run-id`、`--prepare-local-media`、`--serve-local-assets`、`--project`、`--storyboard`、`--projects-dir`、`--allow-unapproved-storyboard`。`--prompt-file` 按 UTF-8 读取导演 prompt，适合长中文分镜、含换行脚本或 Windows 终端参数编码不稳定的场景；不能和 `--prompt` 同时使用。`doubao-seedance-2-0-260128` 支持 `480p` / `720p` / `1080p`；`doubao-seedance-2-0-fast-260128` 不支持 `1080p`。Seedance 2.0 的内置默认 `ratio` 为 `adaptive`。

每个创建命令都会在提交前写入运行证据目录，默认位置为 `_work/seedance_upload/<timestamp>/`。如果传了 `--project` 且没有显式传 `--run-dir`，证据目录会改为 `_work/video_projects/<project-id>/generations/<run-id>/`。该目录包含 `prompt.txt`、`request-payload-redacted.json`、`media-manifest.json` 和汇总型 `generation-log.json`；项目化运行还会写 `project-generation.json`，项目目录下同步保存 `generation-record.json`；真实提交成功后还会写 `submit-summary.json`，`--wait` 完成后写 `task-result.json`。`media-manifest.json` 会记录本地素材 sha256、大小、MIME、图片尺寸、图片/音频预处理记录、`reference_index` 素材编号映射、`prompt_reference_warnings` 和 `project_context`；本机有 `ffprobe` 时还会记录视频/音频时长、编码、FPS、帧数等摘要。`generation-log.json` 会串起请求参数、prompt 指纹、项目/故事板、素材处理、URL 预检、CF tunnel、提交摘要和最终任务结果。`--dry-run-payload` 只构造并保存脱敏 payload，不访问火山 API。

当前生成前最终输入确认和生成后结果复盘使用标准文本格式 + 结构化 JSON 字段；CLI 参考不把历史 HTML 实验命令列为当前工作流入口。

私有本地视频实验可加 `--serve-local-assets cloudflare`。CLI 只会把本地 `reference_video` 复制到本次 run 目录的 `assets/`，启动只读本地 HTTP 服务，拉起 `cloudflared tunnel --url http://127.0.0.1:<port>`，把本地视频参数改写成临时 HTTPS URL，并在命令结束、失败或超时后关闭 HTTP 服务和 tunnel。本地图片/音频仍走 Base64 / `--prepare-local-media`，不会被暴露到 Cloudflare tunnel。该模式需要本机安装 `cloudflared`；如二进制不在 PATH，可用 `SEEDANCE_CLOUDFLARED_BIN` 指定。

`callback_url` 是外部系统集成能力，不是 AI/Skill 默认生成路径。默认仍使用 `--wait` 轮询闭环。需要调试 callback 时，可先运行 `callback-server` 接收 POST 并保存原始 body/headers，再用 `callback-smoke` 发本地模拟 POST 验证 receiver；如果要接收火山真实回调，本地 receiver 还需要用 Cloudflare tunnel、ngrok 或固定公网 HTTPS 域名暴露。

## Creative Project Library

复杂视频任务默认先进入本地项目库。项目库默认根目录是 `_work/video_projects/`，可用 `--projects-dir` 覆盖；该目录被 Git 忽略。

生成前先检索，避免重复生成或重复登记已有角色/场景素材：

```bash
videogen project list
videogen asset search --query "小红帽"
videogen asset search --type character --tag fairy-tale
videogen asset list proj-redhood --query "小红帽"
videogen asset show proj-redhood char-redhood
```

跨项目命中候选后，先让用户确认复用哪一项。长期复用到当前项目时用 `asset reuse`，它会把本地素材复制到目标项目资产目录，或登记同一个外部 source，并写入 `reused_from` 记录来源项目、来源资产、来源路径和 hash：

```bash
videogen asset reuse proj-new-ad proj-redhood char-redhood \
  --asset-id char-redhood-main \
  --purpose "复用主角外观" \
  --tag campaign
```

只做一次快速试生成时，可以直接把 `asset show` 返回的 `material.stored_path` 或 `material.source` 传给 `--reference-image`；但这不是项目级长期复用，完成回复要说明未登记到当前项目。

```bash
videogen project create "小红帽走向森林小屋" \
  --project-id proj-redhood --title "小红帽测试" --ratio 9:16 --duration 4

videogen asset add proj-redhood \
  --type character --name "小红帽" --file redhood.png \
  --purpose "主角外观" --role protagonist --tag fairy-tale --tag red --alias "Red Hood"

videogen asset add proj-redhood \
  --type scene --name "森林小屋" --file cottage.png \
  --purpose "核心场景" --role location --tag forest

videogen asset add proj-redhood \
  --type prop --name "藤编篮子" --file basket.png \
  --purpose "关键道具锁定" --tag fairy-tale

videogen asset add proj-redhood \
  --type voice --name "小红帽声线" --role "小红帽" --file redhood-voice.wav \
  --purpose "角色音色锁定"

videogen script set proj-redhood --file script.md
videogen style set proj-redhood --file style.md
```

故事板流程不调用图片模型，只负责生成规划脚手架、登记故事板图片和确认状态。需要人物设定图、场景设定图或故事板母图时，Skill 先读 `../../video-gen-assets/references/assets.md` 写图像提示词；九宫格、四栏、8 镜头或制作设定板只作为故事板母图的版式选项。故事板图应为 4K 或更高，`storyboard-prompt.txt` 保存完整绘图提示词，`video-prompt.txt` 保存简短读图指令。CLI 只接收生成后的图片路径或 URL：

```bash
videogen storyboard plan proj-redhood --layout 3x3

videogen storyboard add proj-redhood \
  --storyboard-id sb-main \
  --image storyboard.png \
  --prompt storyboard-prompt.txt \
  --video-prompt video-prompt.txt

videogen storyboard approve proj-redhood sb-main
```

从已确认故事板生成：

```bash
videogen generate \
  --project proj-redhood \
  --storyboard sb-main \
  --duration 4 \
  --generate-audio false \
  --reference-image _work/video_projects/proj-redhood/characters/char-redhood/images/redhood.png \
  --reference-image _work/video_projects/proj-redhood/scenes/scene-cottage/images/cottage.png \
  --wait --download outputs
```

`generate` 默认把故事板图片作为 `omni` 的第一张 `reference_image`，并读取 `video-prompt.txt` 作为实际提交 prompt；命令行里的额外 `--reference-image` 会继续追加为 `参考图2`、`参考图3`。复杂任务不要只传故事板一张图：故事板主控镜头顺序和运动，角色卡负责人物一致性，场景/背景卡负责空间、背景层次和道具细节。`video-prompt.txt` 必须写清每张参考图编号用途，例如“参考图1是故事板，参考图2是角色卡，参考图3是场景/背景卡”。若要把故事板图当首帧，可加 `--storyboard-mode first-frame`，但这会和全能参考互斥，不适合作为多参考故事板默认路径。未 approved 的故事板默认会被拒绝；确实要快速抽样时才加 `--allow-unapproved-storyboard`。

多段连续视频使用同一个 `project_id`，每段一个故事板和一次生成记录。后一段的 `video-prompt.txt` 必须写明上一段 `end_state`、本段 `start_state` 和 `continuity_mode`。剧本拆分时先按剧情节拍和镜头边界切段，不把同一个镜头拆成两次生成。镜头切换时可以只承接剧情状态和资产锚点；需要硬衔接时，上一段生成可加 `--return-last-frame`，再把尾帧作为下一段 `first-frame`。同一长镜头跨段时才按长镜头延续处理，优先用 `extend`：

```bash
videogen storyboard add proj-redhood \
  --storyboard-id sb-sd01 \
  --image sd01-storyboard.png \
  --prompt sd01-storyboard-prompt.txt \
  --video-prompt sd01-video-prompt.txt

videogen generate \
  --project proj-redhood \
  --storyboard sb-sd01 \
  --reference-image _work/video_projects/proj-redhood/characters/char-redhood/images/redhood.png \
  --reference-image _work/video_projects/proj-redhood/scenes/scene-cottage/images/cottage.png \
  --wait

videogen storyboard add proj-redhood \
  --storyboard-id sb-sd02 \
  --image sd02-storyboard.png \
  --prompt sd02-storyboard-prompt.txt \
  --video-prompt sd02-video-prompt.txt

videogen generate \
  --project proj-redhood \
  --storyboard sb-sd02 \
  --reference-image _work/video_projects/proj-redhood/characters/char-redhood/images/redhood.png \
  --reference-image _work/video_projects/proj-redhood/scenes/scene-cottage/images/cottage.png \
  --wait
```

尾帧硬衔接时再使用：

```bash
videogen first-frame \
  --first-frame sd01-last-frame.png \
  --prompt-file sd02-video-prompt.txt \
  --duration 6 \
  --wait
```

查询项目和生成历史：

```bash
videogen project list
videogen project show proj-redhood
videogen storyboard show proj-redhood sb-main
videogen history list proj-redhood
videogen history show proj-redhood <run-id>
```

## Input Modes（按需路由）

### 文生视频 (`text-to-video`)

```bash
videogen text-to-video \
  --prompt "电影感写实，9:16，雨夜街头，镜头低角度跟拍..." \
  --ratio 9:16 --duration 8 --generate-audio true --wait
```

只有 text-to-video 允许 `--web-search`。

长中文或多行 prompt 推荐用 UTF-8 文件：

```bash
videogen text-to-video \
  --prompt-file prompt.txt \
  --ratio 9:16 --duration 8 --generate-audio true --wait
```

### 首帧图生视频 (`first-frame`)

```bash
videogen first-frame \
  --prompt "以首帧为开场，角色缓慢转身看向镜头，背景霓虹闪烁..." \
  --first-frame path/to/frame.png \
  --ratio adaptive --generate-audio false --wait
```

### 首尾帧 (`first-last`)

```bash
videogen first-last \
  --prompt "从首帧平滑过渡到尾帧，中间用慢速推镜和柔和光线连接..." \
  --first-frame start.png --last-frame end.png \
  --duration 6 --wait
```

### 全能参考 (`omni`)

```bash
videogen omni \
  --prompt "参考图1用于主角外观，参考视频1用于跑步动作节奏，参考音频1用于鼓点和紧张情绪..." \
  --reference-image character.png \
  --reference-video motion.mp4 \
  --reference-audio beat.mp3 \
  --serve-local-assets cloudflare \
  --generate-audio true --duration 8 --ratio 9:16 --wait
```

### 视频编辑意图 (`edit`)

`edit` 只是 `reference_video` + optional `reference_image` + prompt 的编辑意图封装。当前 payload 不包含 mask、inpaint、edit region、subject replacement 等强编辑字段；不要把它承诺成“强制换皮”或“区域重绘”。

```bash
videogen edit \
  --prompt "去掉广告牌、给街景加雨夜雾感、保持原镜头节奏..." \
  --reference-video https://example.com/source.mp4 \
  --reference-image color_target.png \
  --duration 6 --wait
```

### 视频延长 (`extend`)

```bash
videogen extend \
  --prompt "在原片基础上继续向前推 4 秒，保持角色和光线一致..." \
  --reference-video https://example.com/source.mp4 \
  --duration 4 --wait
```

## 任务管理

```bash
videogen status <task_id>
videogen wait <task_id> --download outputs
videogen list --status running --page-size 20
videogen delete <task_id>
```

## 退出码

| Code | 含义 | 何时出现 |
|------|------|----------|
| `0` | success | 命令完成，且业务 `ok=true` |
| `2` | usage error | argparse 拒绝（缺必填、未知子命令、互斥参数） |
| `3` | config error | 缺 API key、配置文件损坏、模式互斥（如 `omni` 单独传 audio） |
| `4` | api error | 上游 HTTP 4xx/5xx |
| `5` | runtime error | 网络中断、IO、`wait` 超时、任务状态变成 `failed/expired/cancelled` |

AI 调用方应据退出码选不同重试策略：`3` 多半是用户问题（让用户跑 setup 或补参数），`4` 是上游错误（看 `details.http_status` 决定重试或终止），`5` 可继续轮询或重新发起。

## Notes

- 本地图片/音频会被脚本转成 data URL；`reference_video` 必须是可访问的 Web URL。私有视频请先通过隔离目录 + 临时 HTTPS tunnel 或对象存储 signed URL 暴露，不要传本地路径。
- 长中文分镜或多行 prompt 推荐用 UTF-8 `--prompt-file`，避免 shell 参数编码、转义和长度限制影响提交内容。
- 多参考 prompt 应按同类素材输入顺序写清用途：`图片1/参考图1`、`图片2/参考图2`、`视频1/参考视频1`、`音频1/参考音频1`。manifest 会记录编号映射并提示漏写的引用。
- `--prepare-local-media auto` 是默认行为：本地图片/音频转 Base64 前会先检查大小和官方规格；超过目标或官方限制时尝试写入 `<run-dir>/<run-id>/prepared/`。图片格式/大小/尺寸/比例问题需要 Pillow 自动处理；音频格式/大小/时长问题需要 ffmpeg 自动处理；传 `--prepare-local-media off` 可关闭。视频不会转 Base64，只在 `--serve-local-assets cloudflare` 的本地 `reference_video` 场景用 ffmpeg 先规范化再暴露。
- 图片/音频 Base64 payload 会做 64MB request body 预算检查，超出时请压缩、拆分或改用 HTTPS/signed URL。
- 如果显式传 `--serve-local-assets cloudflare`，CLI 只会为本次运行的本地 `reference_video` 创建临时 HTTPS URL；默认不开启，避免意外暴露本地文件。图片和音频不会走 CF tunnel。
- 提交前会对 HTTP(S) 素材 URL 做 `HEAD`，必要时回退小范围 `GET`，验证可访问性并把响应头写入 `media-manifest.json`。
- `doubao-seedance-2-0-260128` 支持 `480p` / `720p` / `1080p`；Fast 模型不支持 `1080p`。
- `duration` 支持 `4-15` 的整数秒，或 `-1` 让模型自动选择；`seed` 支持 `-1` 到 `4294967295`。
- `callback_url` 必须是 HTTP(S)；`execution_expires_after` 支持 `3600-259200` 秒；`safety_identifier` 最长 64 字符，建议传入哈希后的稳定用户标识。
- `service_tier` 只应使用 `default`。本 skill 只覆盖 Seedance 2.0，而 Seedance 2.0 不支持离线/flex 推理，传 `flex` 会被本地拒绝。
- `list --status` 只允许官方列表过滤值：`queued` / `running` / `cancelled` / `succeeded` / `failed`。`expired` 仍可能作为任务返回状态出现。
- `list --page` / `--page-size` 取值范围都是 `1-500`。
- 图片最多 9 张；视频最多 3 个且总时长不超过 15 秒；音频最多 3 个。
- `--dry-run-payload --run-dir <dir> --run-id <id>` 可用于复盘 payload；该模式不需要 API key，也不会创建任务。
- 复杂任务优先使用 `project` / `asset` / `script` / `style` / `storyboard` / `generate`。简单任务或用户明确绕过时，继续使用 6 个快速创建子命令。
- 项目化运行会在 `media-manifest.json` 和 `generation-log.json` 写入 `project_context`，并在项目目录下写 `generation-record.json`，用于回溯使用的故事板、提示词和 run artifact。
- 改 API 参数前重新核对 `references/api.md` 与火山官方文档。
- 配置文件写入会自动 `chmod 600`（POSIX）。Windows 上无此操作。
- `videogen doctor` 默认会做一次 `GET /contents/generations/tasks?page_size=1` 联通检查；离线核对加 `--skip-connectivity`。
