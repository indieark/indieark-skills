# Install

Load when: 首次使用、用户要求安装、`ui-ux-pro-max` 或 `taste-skill` extension 缺失或需要更新。
Avoid: 不要手动复制外部仓库内容；不要把 `extensions/` 提交到本仓库；不要在 `existing-project-optimize` 路线下试图安装 extension。
Pairs with: `extensions.md`, `usage.md`, `flows.md`

## Install Rule

安装 `html-gen-pro` 后，AI 在首次执行 extension 委托前应检查并安装相应 extension：

- `ui-ux-pro-max`（默认）：所有 extension 路线（landing-page / app-frontend / style-mockup）都需要。
- `taste-skill`（按需）：仅 `style-mockup` 路线且气质命中 brutalist / swiss / luxury(soft) 时需要；其他风格命中 `ui-ux-pro-max` 即可。

`existing-project-optimize` 路线不绑 extension，不需要本步骤。

```bash
python scripts/install_extensions.py
```

该命令的语义是 install-or-update：

- 缺失时：`git clone --depth 1 <repo> extensions/<install_name>`。
- 已存在且是 Git checkout 时：在对应目录执行 `git pull --ff-only`。
- 已存在但不是 Git checkout 时：失败并提示，不覆盖用户文件。
- 不要求用户手动 pull 上游。

> Phase 3 起 `scripts/install_extensions.py` 落地；在此之前手动 `git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill extensions/ui-ux-pro-max`，并把 `extensions/` 加入 `.gitignore`。

## Install And Usage Paths

| Route + Aesthetic | Checkout path | Skill entry to read after selection |
| ---- | ---- | ---- |
| `landing-page` / `app-frontend` 全量 | `extensions/ui-ux-pro-max` | `extensions/ui-ux-pro-max/CLAUDE.md` |
| `style-mockup` · 默认（67 styles 覆盖范围内）| `extensions/ui-ux-pro-max` | `extensions/ui-ux-pro-max/CLAUDE.md` |
| `style-mockup` · brutalist / swiss | `extensions/taste-skill` | `extensions/taste-skill/skills/brutalist-skill/SKILL.md` |
| `style-mockup` · luxury(soft / calm-premium) | `extensions/taste-skill` | `extensions/taste-skill/skills/soft-skill/SKILL.md` |
| `existing-project-optimize` | — | — |

安装脚本的 JSON 输出包含 `path` 和 `skill_entry` 字段。`path` 是完整上游 checkout，用于更新；`skill_entry` 是运行时委托时应读取的 Skill 入口（taste-skill 的子 Skill 入口由 Agent 按上表挑选，不由脚本输出——脚本仅返回仓库根 `README.md` 作为入口提示）。

## CLI 标志

只检查不联网变更：

```bash
python scripts/install_extensions.py --check-only
```

只安装某一路线（v0.2.0-post-fuse 起：`style-mockup` 路线同时绑 `ui-ux-pro-max` + `taste-skill`，会一并安装；`landing-page` / `app-frontend` 仍只装 `ui-ux-pro-max`）：

```bash
python scripts/install_extensions.py --route landing-page
python scripts/install_extensions.py --route app-frontend
python scripts/install_extensions.py --route style-mockup
```

锁定版本（CI / 发版可复现）：

```bash
python scripts/install_extensions.py --locked
```

升级 lock 到当前 upstream（拿到 SHA 后手动写回 EXTENSIONS 与 `extensions.md` Registry 表）：

```bash
python scripts/install_extensions.py --update-lock
```

检查 lock 新鲜度（`verified_date` 距今 > 90 天 WARN，不阻塞退出码）：

```bash
python scripts/install_extensions.py --check-freshness
```

机器可读输出：

```bash
python scripts/install_extensions.py --format json
```

## 环境 Python 版本检查（本仓库特有）

`install_extensions.py` 在 clone 后会调用 `python --version`：

- Python < 3.9 → stderr WARN 但继续（不安装、不强制升级）。
- 找不到 `python` 可执行文件 → stderr ERROR，但 extension 安装本身不被阻塞（仅警告 Agent / 用户后续运行其他脚本时可能失败）。

理由：胶水的边界是"不动下游"；environment doctor 比 silent fail 友好，但不应擅自帮用户升 Python。

## Validation

每个 extension 至少检查：

- `README.md` 存在。
- route-specific Skill entry 存在（`ui-ux-pro-max` 是 `CLAUDE.md`；`taste-skill` 是 `README.md`，子 Skill 入口在 `skills/<child>/SKILL.md`，由 S4 阶段按美学方向加载，不由 install 脚本检查）。
- `.git` 目录存在（保证后续可 `git pull` 更新）。

## Local Storage

extension 默认放在：

```text
extensions/
```

该目录用于本地安装态，**不进入 Git**（Phase 3 起在 `.gitignore` 内）。

不要删除 extension 目录内的 `.git`，否则会失去自动更新能力。

## 失败处理

- `git clone` 失败（网络 / 认证）→ stderr 报错，给用户提示"检查网络 / 配置 GitHub 凭据"，退出码 1。
- `git pull --ff-only` 失败（非 fast-forward）→ stderr 报错，提示用户手动进入 `extensions/ui-ux-pro-max` 处理冲突，退出码 1。
- `--locked` 时 `locked_commit` 在 upstream 不存在 → stderr 报错，提示 SHA 已失效，退出码 1。
- 任何错误**不擅自删除** `extensions/<install_name>/`；保护用户的本地工作目录。
