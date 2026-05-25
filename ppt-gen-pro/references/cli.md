# CLI

Load when: 用户问安装、命令、执行、打包或本机调用。
Avoid: 不要假装当前存在可用 CLI。
Pairs with: `router.md`, `reporting.md`

## 无自有 CLI 声明

**ppt-gen-pro 本身没有自有 CLI，不提供任何可直接调用的生成命令。**

所有 PPT 生成执行均通过所选扩展 Skill 的 CLI 完成：

| 路线                 | 执行入口                                                       |
| -------------------- | -------------------------------------------------------------- |
| `image-first-ppt`    | 见 `extensions/ppt-image-first/` 扩展的 CLI                    |
| `web-html-ppt`       | 见 `extensions/guizang-ppt-skill/` 扩展的 CLI                  |
| `svg-ppt`            | 见 `extensions/ppt-master/` 扩展的 CLI                         |
| `academic-image-ppt` | 见 `extensions/literature-report-ppt-builder/` 扩展的 CLI      |

不要凭空构造 `pptgen` 命令或调用不存在的本地脚本；用户选择路线后，打开对应扩展的 `Runtime Skill entry`，按扩展自身的 CLI 约定执行。

## 扩展安装脚本

仓库提供扩展安装/检查脚本（这是本 Skill 唯一的本地可执行命令）：

```powershell
python scripts\install_extensions.py --check-only
python scripts\install_extensions.py
python scripts\install_extensions.py --route image-first-ppt
python scripts\install_extensions.py --route web-html-ppt
python scripts\install_extensions.py --route svg-ppt
```

脚本把外部扩展克隆或更新到 `extensions/` 下。已有扩展通过 `git pull --ff-only` 更新；版本锁定时改为 `git checkout <commit>`，见 `extensions.md` 的版本锁定说明。

### 版本锁与新鲜度标志

| 标志 | 用途 |
| ---- | ---- |
| `--locked` | 按 `EXTENSIONS[].locked_commit` 做 fetch + checkout，跳过 `git pull --ff-only`。CI / 发版场景使用；未填 lock 的 route 仍跟 latest。 |
| `--update-lock` | 先 `git pull --ff-only` 拉到最新，再打印当前 commit SHA + 当日日期，供你手动写回 `scripts/install_extensions.py` 的 `EXTENSIONS` 列表和 `references/extensions.md` 表格。 |
| `--check-freshness` | 列出 `verified_date` 缺失或距今 > 90 天的 route，stderr 输出 `WARN` 但**不影响退出码**。Agent 在委托前应跑一次。 |

```powershell
python scripts\install_extensions.py --locked
python scripts\install_extensions.py --update-lock --route web-html-ppt
python scripts\install_extensions.py --check-only --check-freshness --format json
```

`--locked` 与 `--update-lock` 互斥；`--update-lock` 不能与 `--check-only` 组合。

## 未来自有 CLI 守则

若未来新增 `pptgen` 原生 CLI，必须保留本 Skill 的 route gate：先介绍三种路线、推荐、等待用户选择，再执行；不得绕过 route gate 直接生成。
