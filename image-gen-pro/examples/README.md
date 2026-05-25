# Examples

本目录保存可复用的 Skill + CLI 工作流示例。示例只提交命令、预期 artifact 和注意事项；不要提交真实私有素材、API key、生成图片或 `_work/` 产物。

## Index

| Example | Use When |
| --- | --- |
| `first-setup.md` | 用户首次使用，需要初始化默认模型、route preset 和凭据保存方式 |
| `api-key-first.md` | 用户明确想优先使用 API key route |
| `codex-cli-only.md` | 用户只想使用本机 Codex CLI 订阅能力 |
| `edit-with-local-media.md` | 用户要用本地图片或 mask 做编辑 |
| `inspect-prior-run.md` | 用户要查看历史结果、job 状态或继续迭代 |

## Rules

- 命令使用 `python scripts\imagen.py ...`，Skill 安装后可替换为 `imagen ...`。
- 执行型请求仍必须走 `imagen` CLI；Skill 不绕过 CLI 直接调用 provider 或 Codex。
- 涉及额度消耗的真实生成示例只展示命令模板，不在示例里假设已经执行。
- `jobs` 示例只表示本地状态，不代表远端 provider task id。
