"""Agent-HTML review artifacts for final input and result recap gates."""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from seedance2.constants import DEFAULT_MODEL
from seedance2.errors import SeedanceError
from seedance2.project_store import ProjectStore, read_json, storyboard_image_source, storyboard_video_prompt, write_json
from seedance2.settings import Settings


AGENT_HTML_COMPONENT_SOURCE = "https://github.com/Sayhi-bzb/Agent-HTML"


def build_final_input_review_state(
    store: ProjectStore,
    args: argparse.Namespace,
) -> dict[str, Any]:
    project = store.require_project(args.project)
    storyboard = store.load_storyboard(args.project, args.storyboard)
    settings = Settings(args)
    dimensions = {
        "model": args.model or settings.model or DEFAULT_MODEL,
        "ratio": args.ratio or settings.default_ratio,
        "resolution": args.resolution or settings.default_resolution,
        "duration_seconds": args.duration or settings.default_duration,
        "generate_audio": (
            args.generate_audio
            if args.generate_audio is not None
            else settings.default_generate_audio
        ),
        "watermark": (
            args.watermark
            if args.watermark is not None
            else settings.default_watermark
        ),
    }
    run_id = args.run_id or f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    references = _final_input_references(storyboard, args)
    state = {
        "schema_version": 1,
        "workflow_stage": "final_input_review",
        "review_gate": "before_video_generation",
        "review_scope": "final input confirmation only",
        "approval": "pending",
        "created_at": _now(),
        "project": _project_summary(project),
        "storyboard": _storyboard_summary(storyboard),
        "assets": _project_assets(store, args.project),
        "dimensions": dimensions,
        "references": references,
        "prompts": _storyboard_prompts(storyboard),
        "command": _planned_generate_command(args, dimensions, run_id),
        "output": {
            "run_id": run_id,
            "run_dir": str(store.generations_root(args.project) / run_id),
            "wait": bool(args.wait),
            "download": args.download,
        },
        "requested_changes": [],
    }
    return state


def build_result_review_state(
    store: ProjectStore,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generation_result = store.show_generation(args.project, args.run_id)
    generation = generation_result["generation"]
    artifacts = generation.get("artifacts") or {}
    generation_log = _read_json_if_exists(artifacts.get("generation_log_path"))
    manifest = _read_json_if_exists(artifacts.get("manifest_path"))
    task_result = _read_json_if_exists(artifacts.get("task_result_path"))
    payload = _read_json_if_exists(artifacts.get("payload_path"))
    prompt_text = _read_text_if_exists(artifacts.get("prompt_path"))
    state = {
        "schema_version": 1,
        "workflow_stage": "result_review",
        "review_gate": "after_video_generation",
        "review_scope": "result recap and iteration decision only",
        "approval": "pending",
        "created_at": _now(),
        "project": _project_summary(store.require_project(args.project)),
        "generation": generation,
        "final_input": {
            "request": generation_log.get("request") if generation_log else None,
            "references": generation_log.get("references") if generation_log else [],
            "prompt": {
                "path": artifacts.get("prompt_path"),
                "text": prompt_text,
            },
            "project_context": generation_log.get("project_context") if generation_log else None,
        },
        "artifacts": {
            "record_path": generation_result.get("record_path"),
            "run_dir": generation.get("run_dir"),
            **artifacts,
            "files_present": _artifact_presence(artifacts),
        },
        "task": _task_summary(generation, task_result),
        "manifest": manifest,
        "payload": payload,
        "requested_changes": [],
    }
    return state


def write_review_bundle(
    state: dict[str, Any],
    *,
    output: str | None,
    default_dir: Path,
    stem: str,
    title: str,
) -> dict[str, Any]:
    html_path = Path(output).expanduser() if output else default_dir / f"{stem}.agent.html"
    if html_path.suffix.lower() != ".html":
        html_path = html_path.with_suffix(".agent.html")
    state_path = _review_sidecar_path(html_path, ".json")
    response_path = _review_sidecar_path(html_path, ".response.json")
    response_template = _review_response_template(state)
    state = {
        **state,
        "review_artifact": {
            "format": "agent-html",
            "component_source": AGENT_HTML_COMPONENT_SOURCE,
            "agent_html_path": str(html_path.resolve()),
            "state_path": str(state_path.resolve()),
            "response_template_path": str(response_path.resolve()),
            "contract": (
                "Agent-HTML semantic components only; no custom scripts, "
                "event handlers, or raw CSS."
            ),
        },
    }
    html_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(state_path, state)
    write_json(response_path, response_template)
    html_path.write_text(_render_agent_html(title, state, response_template), encoding="utf-8")
    return {
        "ok": True,
        "workflow_stage": state["workflow_stage"],
        "review_gate": state["review_gate"],
        "html_path": str(html_path.resolve()),
        "agent_html_path": str(html_path.resolve()),
        "state_path": str(state_path.resolve()),
        "response_template_path": str(response_path.resolve()),
        "state": state,
    }


def review_stem(prefix: str, run_id: str | None = None) -> str:
    suffix = run_id or datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{suffix}"


def _render_agent_html(
    title: str,
    state: dict[str, Any],
    response_template: dict[str, Any],
) -> str:
    stage_title = (
        "生成前最终输入确认"
        if state["workflow_stage"] == "final_input_review"
        else "生成结果复盘"
    )
    gate_note = (
        "只在真实调用视频生成前使用，用来确认即将提交给 Seedance 的最终输入。"
        if state["review_gate"] == "before_video_generation"
        else "只在一次生成或 dry-run 之后使用，用来复盘结果证据并决定是否迭代。"
    )
    summary_rows = _summary_rows(state)
    response_json = json.dumps(response_template, ensure_ascii=False, indent=2)
    full_state_json = json.dumps(state, ensure_ascii=False, indent=2)
    return "\n".join([
        '<meta-agent profile="review-dense" />',
        "",
        f'<page title="{_attr(title)}">',
        f'  <alert title="{_attr(stage_title)}" tone="neutral">{_text(gate_note)}</alert>',
        '  <card title="确认门边界">',
        '    <list variant="unordered">',
        "      <item>此 Agent-HTML 页面属于归档暂停实验；当前默认流程使用文本确认和结构化 JSON，不主动生成 HTML。</item>",
        "      <item>如用户明确要求重启该实验，本页面只用于生成前最终确认或生成结果复盘，不用于剧本、资产、故事板等中间阶段。</item>",
        "      <item>页面使用 Agent-HTML 语义组件；不包含自定义脚本、事件处理器或 raw CSS。</item>",
        "      <item>机器可读数据以同名 JSON sidecar 为准；用户修改意见填写到下方 response template 后交回 Agent。</item>",
        "    </list>",
        "  </card>",
        '  <card title="关键摘要">',
        "    <table>",
        '      <row kind="header"><cell>字段</cell><cell>值</cell></row>',
        *[
            f'      <row kind="body"><cell>{_text(key)}</cell><cell>{_text(value)}</cell></row>'
            for key, value in summary_rows
        ],
        "    </table>",
        "  </card>",
        '  <tabs default="decision">',
        '    <tab value="decision" label="确认与修改">',
        f'      <select label="确认结果" value="{_attr(response_template["approval"])}" description="选择本次确认门的决定。">',
        '        <option value="approved" label="通过">可以继续。</option>',
        '        <option value="revise" label="要求修改">需要修改后再确认。</option>',
        '        <option value="back" label="返回上一阶段">退回剧本、资产、故事板或 prompt 阶段。</option>',
        '        <option value="cancelled" label="取消">停止本次生成或复盘。</option>',
        "      </select>",
        f'      <select label="目标阶段" value="{_attr(response_template["target_stage"] or "none")}" description="如果需要修改，选择要退回或进入的阶段。">',
        '        <option value="none" label="不切换阶段">只记录决定；response template 中仍用 null 表示不切换。</option>',
        '        <option value="script" label="剧本">修改剧本或叙事结构。</option>',
        '        <option value="asset_plan" label="资产计划">修改角色、场景、道具或复用策略。</option>',
        '        <option value="storyboard_edit" label="故事板编辑">修改镜头顺序、构图或故事板母图。</option>',
        '        <option value="video_prompt" label="视频提示词">修改最终视频生成提示词。</option>',
        '        <option value="final_input_review" label="重新生成前确认">回到最终输入确认。</option>',
        '        <option value="result_review" label="重新结果复盘">回到结果复盘。</option>',
        "      </select>",
        '      <input label="修改字段" value="" description="示例：dimensions.resolution / references[1].usage / video_prompt" />',
        '      <textarea label="修改内容" value="" description="填写希望修改成什么，或粘贴结构化 JSON 片段。" />',
        '      <textarea label="补充说明" value="" description="可选，说明修改原因、参考依据或验收意见。" />',
        f'      <textarea label="Review Response JSON" value="{_attr(response_json)}" description="机器可读回复模板。复制并按需编辑后交回 Agent。" />',
        "    </tab>",
        '    <tab value="inputs" label="输入与证据">',
        *_agent_html_input_sections(state),
        "    </tab>",
        '    <tab value="state" label="完整 State">',
        f'      <textarea label="State JSON" value="{_attr(full_state_json)}" description="只读：CLI 写出的完整 review state。" />',
        "    </tab>",
        "  </tabs>",
        "</page>",
        "",
    ])


def _review_sidecar_path(html_path: Path, suffix: str) -> Path:
    name = html_path.name
    if name.endswith(".agent.html"):
        return html_path.with_name(f"{name[:-len('.agent.html')]}{suffix}")
    return html_path.with_suffix(suffix)


def _review_response_template(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "workflow_stage": state["workflow_stage"],
        "review_gate": state["review_gate"],
        "approval": "approved",
        "target_stage": None,
        "selected_project_id": state.get("project", {}).get("project_id"),
        "selected_storyboard_id": (
            state.get("storyboard", {}).get("storyboard_id")
            or state.get("generation", {}).get("storyboard_id")
        ),
        "selected_run_id": (
            state.get("output", {}).get("run_id")
            or state.get("generation", {}).get("run_id")
        ),
        "dimensions": state.get("dimensions") or state.get("final_input", {}).get("request"),
        "requested_changes": [],
    }


def _summary_rows(state: dict[str, Any]) -> list[tuple[str, str]]:
    rows = [
        ("workflow_stage", str(state.get("workflow_stage", ""))),
        ("review_gate", str(state.get("review_gate", ""))),
        ("project", str(state.get("project", {}).get("project_id") or "")),
        (
            "storyboard",
            str(
                state.get("storyboard", {}).get("storyboard_id")
                or state.get("generation", {}).get("storyboard_id")
                or ""
            ),
        ),
        (
            "run_id",
            str(
                state.get("output", {}).get("run_id")
                or state.get("generation", {}).get("run_id")
                or ""
            ),
        ),
    ]
    if state.get("dimensions"):
        dimensions = state["dimensions"]
        rows.append((
            "dimensions",
            (
                f'{dimensions.get("resolution")} / {dimensions.get("ratio")} / '
                f'{dimensions.get("duration_seconds")}s / audio='
                f'{dimensions.get("generate_audio")}'
            ),
        ))
    if state.get("task"):
        task = state["task"]
        rows.append((
            "task",
            f'{task.get("task_id") or ""} / {task.get("status") or ""} / dry_run={task.get("dry_run")}',
        ))
    return rows


def _agent_html_input_sections(state: dict[str, Any]) -> list[str]:
    sections: list[str] = []
    if state.get("references"):
        sections.extend([
            '      <card title="参考素材">',
            "        <table>",
            '          <row kind="header"><cell>编号</cell><cell>角色</cell><cell>来源</cell></row>',
        ])
        for item in state["references"]:
            sections.append(
                "          "
                f'<row kind="body"><cell>{_text(item.get("label"))}</cell>'
                f'<cell>{_text(item.get("role"))}</cell>'
                f'<cell>{_text(item.get("source"))}</cell></row>'
            )
        sections.extend(["        </table>", "      </card>"])
    if state.get("final_input", {}).get("references"):
        sections.extend([
            '      <card title="结果引用素材">',
            "        <table>",
            '          <row kind="header"><cell>编号</cell><cell>角色</cell><cell>来源</cell></row>',
        ])
        for item in state["final_input"]["references"]:
            sections.append(
                "          "
                f'<row kind="body"><cell>{_text(item.get("label"))}</cell>'
                f'<cell>{_text(item.get("role"))}</cell>'
                f'<cell>{_text(item.get("source"))}</cell></row>'
            )
        sections.extend(["        </table>", "      </card>"])
    prompt_text = (
        state.get("prompts", {}).get("video_prompt", {}).get("text")
        or state.get("final_input", {}).get("prompt", {}).get("text")
    )
    if prompt_text:
        sections.append(
            f'      <textarea label="视频提示词" value="{_attr(prompt_text)}" '
            'description="只读：本次确认门关联的视频生成提示词。" />'
        )
    artifact_files = state.get("artifacts", {}).get("files_present")
    if artifact_files:
        sections.extend([
            '      <card title="证据文件">',
            "        <table>",
            '          <row kind="header"><cell>文件</cell><cell>存在</cell></row>',
        ])
        for key, value in artifact_files.items():
            sections.append(
                f'          <row kind="body"><cell>{_text(key)}</cell><cell>{_text(value)}</cell></row>'
            )
        sections.extend(["        </table>", "      </card>"])
    return sections or ['      <alert title="输入摘要">暂无额外输入摘要。</alert>']


def _attr(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _text(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=False)


def _final_input_references(storyboard: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    references: list[dict[str, Any]] = []
    image_offset = 0
    storyboard_source = storyboard_image_source(storyboard)
    if args.storyboard_mode == "first-frame":
        references.append({
            "label": "首帧",
            "role": "first_frame",
            "source": storyboard_source,
            "usage": "storyboard image as first frame",
        })
    else:
        image_offset = 1
        references.append({
            "label": "参考图1",
            "role": "reference_image",
            "source": storyboard_source,
            "usage": "storyboard master image",
        })
    for index, source in enumerate(args.reference_image or [], start=1 + image_offset):
        references.append({
            "label": f"参考图{index}",
            "role": "reference_image",
            "source": source,
            "usage": "extra character, scene, prop, or product card",
        })
    for index, source in enumerate(args.reference_video or [], start=1):
        references.append({
            "label": f"参考视频{index}",
            "role": "reference_video",
            "source": source,
            "usage": "extra video reference",
        })
    for index, source in enumerate(args.reference_audio or [], start=1):
        references.append({
            "label": f"参考音频{index}",
            "role": "reference_audio",
            "source": source,
            "usage": "extra audio reference",
        })
    return references


def _planned_generate_command(
    args: argparse.Namespace,
    dimensions: dict[str, Any],
    run_id: str,
) -> dict[str, Any]:
    command = [
        "seedance2",
        "generate",
        "--project",
        args.project,
        "--storyboard",
        args.storyboard,
        "--storyboard-mode",
        args.storyboard_mode,
        "--model",
        dimensions["model"],
        "--resolution",
        dimensions["resolution"],
        "--ratio",
        dimensions["ratio"],
        "--duration",
        str(dimensions["duration_seconds"]),
        "--generate-audio",
        str(dimensions["generate_audio"]).lower(),
        "--run-id",
        run_id,
    ]
    for source in args.reference_image or []:
        command.extend(["--reference-image", source])
    for source in args.reference_video or []:
        command.extend(["--reference-video", source])
    for source in args.reference_audio or []:
        command.extend(["--reference-audio", source])
    if args.wait:
        command.append("--wait")
    if args.download:
        command.extend(["--download", args.download])
    return {
        "subcommand": "generate",
        "argv": command,
        "text": " ".join(_quote_arg(part) for part in command),
    }


def _project_summary(project: dict[str, Any]) -> dict[str, Any]:
    return {
        "project_id": project.get("project_id"),
        "title": project.get("title"),
        "intent": project.get("intent"),
        "platform": project.get("platform"),
        "ratio": project.get("ratio"),
        "duration": project.get("duration"),
        "project_assets": project.get("assets"),
        "storyboards": project.get("storyboards", []),
        "generations": project.get("generations", []),
    }


def _storyboard_summary(storyboard: dict[str, Any]) -> dict[str, Any]:
    return {
        "storyboard_id": storyboard.get("storyboard_id"),
        "layout": storyboard.get("layout"),
        "status": storyboard.get("status"),
        "approved": storyboard.get("approved"),
        "image": storyboard.get("image"),
        "storyboard_prompt": storyboard.get("storyboard_prompt"),
        "video_prompt": storyboard.get("video_prompt"),
        "storyboard_path": storyboard.get("storyboard_path"),
    }


def _storyboard_prompts(storyboard: dict[str, Any]) -> dict[str, Any]:
    storyboard_prompt = storyboard.get("storyboard_prompt") or {}
    video_prompt = storyboard.get("video_prompt") or {}
    return {
        "storyboard_prompt": {
            **storyboard_prompt,
            "text": _read_text_if_exists(storyboard_prompt.get("path")),
        },
        "video_prompt": {
            **video_prompt,
            "text": storyboard_video_prompt(storyboard),
        },
    }


def _project_assets(store: ProjectStore, project_id: str) -> dict[str, Any]:
    return {
        "characters": store.list_assets(project_id, "character")["assets"],
        "scenes": store.list_assets(project_id, "scene")["assets"],
    }


def _task_summary(generation: dict[str, Any], task_result: dict[str, Any]) -> dict[str, Any]:
    result = task_result or {}
    created = result.get("created") or {}
    return {
        "task_id": generation.get("task_id") or result.get("task_id") or created.get("task_id"),
        "status": generation.get("status") or result.get("status") or created.get("status"),
        "mode": generation.get("mode") or result.get("mode") or created.get("mode"),
        "dry_run": generation.get("dry_run"),
        "video_url": result.get("video_url"),
        "downloaded_path": result.get("downloaded_path"),
    }


def _artifact_presence(artifacts: dict[str, Any]) -> dict[str, bool]:
    return {
        key: bool(value and Path(value).expanduser().is_file())
        for key, value in artifacts.items()
        if key.endswith("_path")
    }


def _read_json_if_exists(path_text: str | None) -> dict[str, Any]:
    if not path_text:
        return {}
    path = Path(path_text).expanduser()
    if not path.is_file():
        return {}
    try:
        return read_json(path)
    except SeedanceError:
        return {}


def _read_text_if_exists(path_text: str | None) -> str | None:
    if not path_text:
        return None
    path = Path(path_text).expanduser()
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8-sig").rstrip("\r\n")
    except UnicodeDecodeError:
        return None


def _quote_arg(value: str) -> str:
    if not value or any(ch.isspace() for ch in value):
        return json.dumps(value, ensure_ascii=False)
    return value


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")
