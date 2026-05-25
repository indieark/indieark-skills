# Install

Load when: 首次使用、用户要求安装、扩展缺失或需要更新三种 PPT 路线。
Avoid: 不要手动复制外部仓库内容；不要把 `extensions/` 提交到本仓库。
Pairs with: `extensions.md`, `cli.md`

## Install Rule

安装 `ppt-gen-pro` 后，AI 在首次执行 PPT 生成前应检查并安装三种扩展。之后每次需要刷新扩展时重复运行同一命令即可更新上游：

```powershell
python scripts\install_extensions.py
```

该命令的语义是 install-or-update：

- 缺失时：`git clone --depth 1 <repo> extensions/<name>`。
- 已存在且是 Git checkout 时：在对应目录执行 `git pull --ff-only`。
- 已存在但不是 Git checkout 时：失败并提示，不覆盖用户文件。
- 不要求用户手动进入三个目录逐个更新上游。

## Install And Usage Paths

| Route | Checkout path | Skill entry to read after selection |
| ---- | ---- | ---- |
| `image-first-ppt` | `extensions/ppt-image-first` | `extensions/ppt-image-first/SKILL.md` |
| `web-html-ppt` | `extensions/guizang-ppt-skill` | `extensions/guizang-ppt-skill/SKILL.md` |
| `svg-ppt` | `extensions/ppt-master` | `extensions/ppt-master/skills/ppt-master/SKILL.md` |
| `academic-image-ppt` | `extensions/literature-report-ppt-builder` | `extensions/literature-report-ppt-builder/academic-slide-minimalist/SKILL.md` |

安装脚本的 JSON 输出包含 `path` 和 `skill_entry` 字段。`path` 是完整上游 checkout，用于更新；`skill_entry` 是运行时委托时应读取的 Skill 入口。

只检查不联网变更：

```powershell
python scripts\install_extensions.py --check-only
```

只安装某一路线：

```powershell
python scripts\install_extensions.py --route image-first-ppt
python scripts\install_extensions.py --route web-html-ppt
python scripts\install_extensions.py --route svg-ppt
python scripts\install_extensions.py --route academic-image-ppt
```

## Validation

每个扩展至少检查：

- `README.md`
- route-specific Skill entry and references directory

`svg-ppt` 的 `hugohe3/ppt-master` 也支持 `npx skills add hugohe3/ppt-master`，但本仓库当前仍以 `scripts/install_extensions.py` 作为统一检查入口，以保留完整上游 checkout 和后续 `git pull --ff-only` 更新能力。除非后续明确切到 skill-manager，否则不要混用另一套安装产物作为运行时入口。

## Local Storage

扩展默认放在：

```text
extensions/
```

该目录用于本地安装态，不进入 Git。

不要删除扩展目录内的 `.git`，否则会失去自动更新能力。
