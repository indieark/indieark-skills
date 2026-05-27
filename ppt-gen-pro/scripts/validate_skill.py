from __future__ import annotations

import json
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


def fail(message: str) -> int:
    print(f"validate_skill: {message}", file=sys.stderr)
    return 1


def main() -> int:
    skill_path = SKILL_DIR / "SKILL.md"
    if not skill_path.exists():
        return fail("missing SKILL.md")
    skill_text = skill_path.read_text(encoding="utf-8")
    if not skill_text.startswith("---\nname: ppt-gen-pro\n"):
        return fail("invalid SKILL.md frontmatter")
    for phrase in [
        "必须触发本 Skill",
        "三种内置路线",
        "SVG PPT",
        "图片 PPT",
        "网页 PPT",
        "默认推荐策略",
        "标准 PPT 优先推荐图片 PPT",
        "只有用户明确强调可编辑",
        "不在用户未选择 L1 路线前直接进入某个扩展生成",
    ]:
        if phrase not in skill_text:
            return fail(f"SKILL.md missing route phrase: {phrase}")

    metadata = json.loads((SKILL_DIR / "skill.json").read_text(encoding="utf-8"))
    if metadata.get("name") != "ppt-gen-pro":
        return fail("skill.json name must be ppt-gen-pro")
    if metadata.get("version") != "0.1.0":
        return fail("skill.json version must be 0.1.0")
    if metadata.get("status") != "router-alpha":
        return fail("skill.json status must be router-alpha")
    for capability in [
        "mandatory_ppt_generation_trigger",
        "route_intro_before_generation",
        "user_route_choice_gate",
        "extension_install_check",
    ]:
        if capability not in metadata.get("capabilities", []):
            return fail(f"skill.json missing capability: {capability}")

    for rel in [
        "references/README.md",
        "references/workflow.md",
        "references/route-introduction.md",
        "references/usage.md",
        "references/router.md",
        "references/extensions.md",
        "references/install.md",
        "references/reporting.md",
        "references/cli.md",
        "agents/openai.yaml",
    ]:
        if not (SKILL_DIR / rel).exists():
            return fail(f"missing {rel}")

    router = (SKILL_DIR / "references/router.md").read_text(encoding="utf-8")
    for phrase in [
        "Mandatory Trigger Rule",
        "Route Menu",
        "Choice Gate",
        "`svg-ppt`",
        "`image-first-ppt`",
        "`web-html-ppt`",
        "推荐 `image-first-ppt`",
        "推荐 `web-html-ppt`",
        "推荐 `svg-ppt`",
        "不要默认推 SVG",
        "好看",
        "可编辑",
    ]:
        if phrase not in router:
            return fail(f"router.md missing route phrase: {phrase}")

    introduction = (SKILL_DIR / "references/route-introduction.md").read_text(encoding="utf-8")
    for phrase in [
        "Standard User Introduction",
        "图片 PPT（默认推荐）",
        "网页 PPT",
        "SVG PPT / 可编辑 PPT",
        "hugohe3/ppt-master",
        "链路更复杂",
        "按推荐来",
        "不要把 SVG / design 描述成更高级的默认路线",
    ]:
        if phrase not in introduction:
            return fail(f"route-introduction.md missing phrase: {phrase}")

    extensions = (SKILL_DIR / "references/extensions.md").read_text(encoding="utf-8")
    for phrase in [
        "https://github.com/hugohe3/ppt-master",
        "https://github.com/NyxTides/ppt-image-first",
        "https://github.com/op7418/guizang-ppt-skill",
        "Runtime Skill entry",
        "extensions/ppt-master/skills/ppt-master/SKILL.md",
        "live Git checkouts",
        "git pull --ff-only",
        "Delegation Contract",
    ]:
        if phrase not in extensions:
            return fail(f"extensions.md missing phrase: {phrase}")

    usage = (SKILL_DIR / "references/usage.md").read_text(encoding="utf-8")
    for phrase in [
        "One-Line Contract",
        "Runtime Sequence",
        "Route To Entry Map",
        "extensions/ppt-image-first/SKILL.md",
        "extensions/guizang-ppt-skill/SKILL.md",
        "extensions/ppt-master/skills/ppt-master/SKILL.md",
        "检查输出里的 `skill_entry` 字段",
        "不要猜外部 Skill 路径",
    ]:
        if phrase not in usage:
            return fail(f"usage.md missing phrase: {phrase}")

    install = (SKILL_DIR / "references/install.md").read_text(encoding="utf-8")
    for phrase in [
        "python scripts\\install_extensions.py",
        "install-or-update",
        "Install And Usage Paths",
        "skill_entry",
        "extensions/ppt-master/skills/ppt-master/SKILL.md",
        "git pull --ff-only",
        "不要删除扩展目录内的 `.git`",
    ]:
        if phrase not in install:
            return fail(f"install.md missing install/update phrase: {phrase}")

    installer_path = SKILL_DIR / "scripts/install_extensions.py"
    if not installer_path.exists():
        installer_path = SKILL_DIR.parents[1] / "scripts/install_extensions.py"
    installer = installer_path.read_text(encoding="utf-8")
    if "git\", \"pull\", \"--ff-only" not in installer:
        return fail("install_extensions.py must update existing checkouts with git pull --ff-only")
    if "https://github.com/hugohe3/ppt-master" not in installer:
        return fail("install_extensions.py must register hugohe3/ppt-master for svg-ppt")
    if "skill_entry" not in installer:
        return fail("install_extensions.py must expose extension skill_entry")

    print("validate_skill: OK (0 warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
