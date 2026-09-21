#!/usr/bin/env python3
"""Validate the sanitized Poetry Journey public demo with the standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
ROUTE_DIR = ROOT / "examples" / "poetry-route"
STORY_DIR = ROOT / "examples" / "story-production"
GENERATED_DIR = ROOT / "examples" / "generated"
MAX_PUBLIC_FILE_BYTES = 1_000_000

WINDOWS_DRIVE_ABSOLUTE = re.compile(
    r"(?i)(?<![A-Za-z0-9])[A-Z]:[\\/]"
)
WINDOWS_UNC_ABSOLUTE = re.compile(
    r"\\\\[A-Za-z0-9._$ -]+\\[A-Za-z0-9._$ -]+"
)
UNIX_LOCAL_ABSOLUTE = re.compile(
    r"(?<![:A-Za-z0-9])/(?:Users|home|Volumes|private|tmp|var/tmp|mnt)/[^\s\"']+"
)
SECRET_ASSIGNMENT = re.compile(
    r"""(?ix)
    ["']?(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|
    secret[_-]?key|password)["']?
    \s*[:=]\s*
    ["']([^"']{8,})["']
    """
)
SECRET_FILENAME = re.compile(
    r"(?i)(?:api.?key|access.?token|secret|password).*.(?:txt|json|env|ini|yaml|yml)$"
)
KNOWN_SECRET_LITERALS = (
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
TEXT_SUFFIXES = {
    "",
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
YAML_MAPPING_LINE = re.compile(
    r"""^(?:[A-Za-z0-9_.-]+|"[^"]+"|'[^']+')\s*:(?:\s.*)?$"""
)


class Report:
    def __init__(self, strict: bool) -> None:
        self.strict = strict
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        if self.strict:
            self.errors.append(f"strict: {message}")
        else:
            self.warnings.append(message)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path, report: Report) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        report.error(f"{relative(path)}: cannot read valid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        report.error(f"{relative(path)}: top level must be an object")
        return {}
    return value


def require_keys(
    obj: dict[str, Any],
    keys: Iterable[str],
    label: str,
    report: Report,
) -> None:
    for key in keys:
        if key not in obj:
            report.error(f"{label}: missing required key '{key}'")


def collect_ids(
    records: Any,
    id_key: str,
    label: str,
    report: Report,
) -> set[str]:
    if not isinstance(records, list):
        report.error(f"{label}: expected a list")
        return set()
    result: set[str] = set()
    for index, record in enumerate(records):
        item_label = f"{label}[{index}]"
        if not isinstance(record, dict):
            report.error(f"{item_label}: expected an object")
            continue
        value = record.get(id_key)
        if not isinstance(value, str) or not value.strip():
            report.error(f"{item_label}: missing non-empty {id_key}")
            continue
        if value in result:
            report.error(f"{item_label}: duplicate {id_key} '{value}'")
        result.add(value)
    return result


def check_refs(
    refs: Any,
    known: set[str],
    label: str,
    report: Report,
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(refs, list) or (not refs and not allow_empty):
        report.error(f"{label}: expected {'a list' if allow_empty else 'at least one reference'}")
        return
    for ref in refs:
        if not isinstance(ref, str) or ref not in known:
            report.error(f"{label}: unknown reference '{ref}'")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_demo_path(
    base: Path,
    raw_path: Any,
    label: str,
    report: Report,
) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path.strip():
        report.error(f"{label}: expected a non-empty relative path")
        return None
    path = Path(raw_path)
    if path.is_absolute() or ".." in path.parts:
        report.error(f"{label}: path must stay relative to its example directory")
        return None
    resolved = (base / path).resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError:
        report.error(f"{label}: path escapes its example directory")
        return None
    if not resolved.is_file():
        report.error(f"{label}: referenced file does not exist: {raw_path}")
        return None
    return resolved


def validate_route(report: Report) -> tuple[int, int]:
    candidates = load_json(ROUTE_DIR / "candidates.example.json", report)
    route = load_json(ROUTE_DIR / "route.example.json", report)
    cards = load_json(ROUTE_DIR / "cards.example.json", report)

    require_keys(
        candidates,
        ["schema_version", "artifact_type", "query", "sources", "candidates"],
        "candidates.example.json",
        report,
    )
    source_ids = collect_ids(candidates.get("sources"), "id", "route sources", report)
    candidate_ids = collect_ids(
        candidates.get("candidates"), "id", "route candidates", report
    )

    for candidate in candidates.get("candidates", []):
        if not isinstance(candidate, dict):
            continue
        candidate_id = candidate.get("id", "<unknown>")
        require_keys(
            candidate,
            ["display_name", "modern_location", "relation", "review"],
            f"candidate {candidate_id}",
            report,
        )
        location = candidate.get("modern_location")
        if not isinstance(location, dict):
            report.error(f"candidate {candidate_id}: modern_location must be an object")
        elif location.get("coordinates") is not None:
            report.warn(
                f"candidate {candidate_id}: coordinates require an explicit live-source policy"
            )
        relation = candidate.get("relation")
        if isinstance(relation, dict):
            check_refs(
                relation.get("source_refs"),
                source_ids,
                f"candidate {candidate_id} relation.source_refs",
                report,
            )
        else:
            report.error(f"candidate {candidate_id}: relation must be an object")

    require_keys(
        route,
        ["schema_version", "artifact_type", "route_id", "query", "stops", "warnings"],
        "route.example.json",
        report,
    )
    if route.get("ordering_mode") != "cultural_sequence_not_navigation":
        report.error("route.example.json: ordering_mode must preserve navigation caveat")
    stop_ids = collect_ids(route.get("stops"), "stop_id", "route stops", report)
    orders: list[int] = []
    for stop in route.get("stops", []):
        if not isinstance(stop, dict):
            continue
        stop_id = stop.get("stop_id", "<unknown>")
        if stop.get("candidate_id") not in candidate_ids:
            report.error(
                f"stop {stop_id}: unknown candidate_id '{stop.get('candidate_id')}'"
            )
        check_refs(
            stop.get("source_refs"),
            source_ids,
            f"stop {stop_id} source_refs",
            report,
        )
        if isinstance(stop.get("order"), int):
            orders.append(stop["order"])
        else:
            report.error(f"stop {stop_id}: order must be an integer")
    if orders and sorted(orders) != list(range(1, len(orders) + 1)):
        report.error("route stops: order values must be contiguous starting at 1")

    require_keys(
        cards,
        ["schema_version", "artifact_type", "route_id", "cards"],
        "cards.example.json",
        report,
    )
    if cards.get("route_id") != route.get("route_id"):
        report.error("cards.example.json: route_id does not match route.example.json")
    card_ids = collect_ids(cards.get("cards"), "card_id", "route cards", report)
    for card in cards.get("cards", []):
        if not isinstance(card, dict):
            continue
        card_id = card.get("card_id", "<unknown>")
        if card.get("stop_id") not in stop_ids:
            report.error(f"card {card_id}: unknown stop_id '{card.get('stop_id')}'")
        if card.get("candidate_id") not in candidate_ids:
            report.error(
                f"card {card_id}: unknown candidate_id '{card.get('candidate_id')}'"
            )
        check_refs(
            card.get("source_refs"),
            source_ids,
            f"card {card_id} source_refs",
            report,
        )

    handbook_path = ROUTE_DIR / "handbook.example.md"
    try:
        handbook = handbook_path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(f"{relative(handbook_path)}: cannot read: {exc}")
        handbook = ""
    for stop_id in stop_ids:
        if stop_id not in handbook:
            report.error(f"handbook.example.md: missing stop ID '{stop_id}'")
    for card_id in card_ids:
        if card_id not in handbook:
            report.error(f"handbook.example.md: missing card ID '{card_id}'")

    return len(stop_ids), len(card_ids)


def validate_story(report: Report) -> tuple[int, int, int]:
    story_path = STORY_DIR / "story_data.example.json"
    manifest_path = STORY_DIR / "story_manifest.example.json"
    story = load_json(story_path, report)
    manifest = load_json(manifest_path, report)

    require_keys(
        story,
        [
            "schema_version",
            "artifact_type",
            "story_id",
            "sources",
            "characters",
            "pages",
            "collection_cards",
            "media_plan",
            "review_gates",
        ],
        "story_data.example.json",
        report,
    )
    source_ids = collect_ids(story.get("sources"), "id", "story sources", report)
    character_ids = collect_ids(
        story.get("characters"), "id", "story characters", report
    )
    page_ids = collect_ids(story.get("pages"), "page_id", "story pages", report)
    card_ids = collect_ids(
        story.get("collection_cards"),
        "card_id",
        "story collection cards",
        report,
    )
    media_ids = collect_ids(
        story.get("media_plan"), "task_id", "story media tasks", report
    )
    gate_ids = collect_ids(
        story.get("review_gates"), "gate_id", "story review gates", report
    )

    page_sequences: list[int] = []
    allowed_labels = {
        "source_based_paraphrase",
        "editorial_interpretation",
        "creative_adaptation",
    }
    for page in story.get("pages", []):
        if not isinstance(page, dict):
            continue
        page_id = page.get("page_id", "<unknown>")
        check_refs(
            page.get("source_refs"),
            source_ids,
            f"page {page_id} source_refs",
            report,
        )
        check_refs(
            page.get("character_refs"),
            character_ids,
            f"page {page_id} character_refs",
            report,
        )
        if page.get("creative_status") not in allowed_labels:
            report.error(f"page {page_id}: unknown creative_status")
        if isinstance(page.get("sequence"), int):
            page_sequences.append(page["sequence"])
        else:
            report.error(f"page {page_id}: sequence must be an integer")
    if page_sequences and sorted(page_sequences) != list(
        range(1, len(page_sequences) + 1)
    ):
        report.error("story pages: sequence values must be contiguous starting at 1")

    for card in story.get("collection_cards", []):
        if not isinstance(card, dict):
            continue
        card_id = card.get("card_id", "<unknown>")
        check_refs(
            card.get("page_refs"),
            page_ids,
            f"collection card {card_id} page_refs",
            report,
        )
        check_refs(
            card.get("source_refs"),
            source_ids,
            f"collection card {card_id} source_refs",
            report,
        )
        if card.get("creative_status") not in allowed_labels:
            report.error(f"collection card {card_id}: unknown creative_status")

    media_types: dict[str, int] = {"image": 0, "audio": 0}
    for task in story.get("media_plan", []):
        if not isinstance(task, dict):
            continue
        task_id = task.get("task_id", "<unknown>")
        check_refs(
            task.get("page_refs"), page_ids, f"media task {task_id} page_refs", report
        )
        check_refs(
            task.get("card_refs"), card_ids, f"media task {task_id} card_refs", report
        )
        check_refs(
            task.get("character_refs"),
            character_ids,
            f"media task {task_id} character_refs",
            report,
        )
        check_refs(
            task.get("source_refs"),
            source_ids,
            f"media task {task_id} source_refs",
            report,
        )
        media_type = task.get("media_type")
        if media_type not in media_types:
            report.error(f"media task {task_id}: media_type must be image or audio")
        else:
            media_types[media_type] += 1
        if task.get("status") != "not_generated":
            report.error(
                f"media task {task_id}: public fixtures must remain not_generated"
            )
    if not all(media_types.values()):
        report.error("story media plan: both image and audio tasks are required")

    for gate in story.get("review_gates", []):
        if isinstance(gate, dict) and gate.get("status") != "human_review_required":
            report.error(
                f"review gate {gate.get('gate_id', '<unknown>')}: "
                "public fixture must remain human_review_required"
            )

    require_keys(
        manifest,
        [
            "schema_version",
            "artifact_type",
            "story_id",
            "content_file",
            "expected_counts",
            "content_freeze",
            "assembly",
            "qa",
        ],
        "story_manifest.example.json",
        report,
    )
    if manifest.get("story_id") != story.get("story_id"):
        report.error("story manifest: story_id does not match story data")
    if manifest.get("content_file") != story_path.name:
        report.error("story manifest: content_file must point to story_data.example.json")

    actual_counts = {
        "sources": len(source_ids),
        "characters": len(character_ids),
        "pages": len(page_ids),
        "collection_cards": len(card_ids),
        "media_tasks": len(media_ids),
        "image_tasks": media_types["image"],
        "audio_tasks": media_types["audio"],
        "review_gates": len(gate_ids),
    }
    expected_counts = manifest.get("expected_counts")
    if not isinstance(expected_counts, dict):
        report.error("story manifest: expected_counts must be an object")
    else:
        for name, actual in actual_counts.items():
            if expected_counts.get(name) != actual:
                report.error(
                    f"story manifest: expected_counts.{name}="
                    f"{expected_counts.get(name)!r}, actual={actual}"
                )

    freeze = manifest.get("content_freeze")
    if not isinstance(freeze, dict):
        report.error("story manifest: content_freeze must be an object")
    else:
        if freeze.get("status") != "frozen_for_public_demo":
            report.error("story manifest: content freeze must be explicit")
        if freeze.get("frozen_file") != story_path.name:
            report.error("story manifest: frozen_file does not match story data")
        try:
            story_digest = sha256_file(story_path)
        except OSError as exc:
            report.error(f"story manifest: cannot hash story data: {exc}")
        else:
            if freeze.get("sha256") != story_digest:
                report.error(
                    "story manifest: content-freeze hash is stale; refresh the "
                    "manifest and final artifact deliberately"
                )

    assembly = manifest.get("assembly")
    final_path: Path | None = None
    final_digest: str | None = None
    if not isinstance(assembly, dict):
        report.error("story manifest: assembly must be an object")
    else:
        if assembly.get("status") != "assembled_synthetic_no_media":
            report.error("story manifest: unexpected assembly status")
        check_refs(
            assembly.get("input_page_refs"),
            page_ids,
            "story assembly input_page_refs",
            report,
        )
        check_refs(
            assembly.get("input_card_refs"),
            card_ids,
            "story assembly input_card_refs",
            report,
        )
        if set(assembly.get("input_page_refs", [])) != page_ids:
            report.error("story assembly: input_page_refs must cover every page")
        if set(assembly.get("input_card_refs", [])) != card_ids:
            report.error("story assembly: input_card_refs must cover every card")
        final_artifact = assembly.get("final_artifact")
        if not isinstance(final_artifact, dict):
            report.error("story manifest: final_artifact must be an object")
        else:
            final_path = resolve_demo_path(
                STORY_DIR,
                final_artifact.get("path"),
                "story assembly final_artifact.path",
                report,
            )
            if final_path is not None:
                final_digest = sha256_file(final_path)
                if final_artifact.get("sha256") != final_digest:
                    report.error("story assembly: final artifact hash is stale")

    qa = manifest.get("qa")
    if not isinstance(qa, dict):
        report.error("story manifest: qa must be an object")
    else:
        if qa.get("status") != "passed":
            report.error("story manifest: synthetic QA status must be passed")
        if final_path is not None and qa.get("checked_artifact") != final_path.name:
            report.error("story QA: checked_artifact is not the assembled final artifact")
        if final_digest is not None and qa.get("checked_sha256") != final_digest:
            report.error("story QA: checked_sha256 is stale")
        checks = qa.get("checks")
        if not isinstance(checks, dict) or not checks or not all(
            value is True for value in checks.values()
        ):
            report.error("story QA: every declared synthetic check must be true")
        check_refs(
            qa.get("remaining_human_gates"),
            gate_ids,
            "story QA remaining_human_gates",
            report,
        )
        if set(qa.get("remaining_human_gates", [])) != gate_ids:
            report.error("story QA: every human gate must remain visible")

    if final_path is not None:
        try:
            final_html = final_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            report.error(f"{relative(final_path)}: cannot read UTF-8 HTML: {exc}")
        else:
            if f'data-story-id="{story.get("story_id")}"' not in final_html:
                report.error("story final artifact: story ID is missing")
            for page_id in page_ids:
                if f'data-page-id="{page_id}"' not in final_html:
                    report.error(f"story final artifact: missing page ID '{page_id}'")
            for card_id in card_ids:
                if f'data-card-id="{card_id}"' not in final_html:
                    report.error(f"story final artifact: missing card ID '{card_id}'")
            if re.search(r"<(?:audio|img|source|video)\b", final_html, re.IGNORECASE):
                report.error("story final artifact: public fixture must not embed media")

    return len(page_ids), len(card_ids), len(media_ids)


def intended_public_files(report: Report) -> list[Path]:
    try:
        completed = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        names = [
            item.decode("utf-8", errors="strict")
            for item in completed.stdout.split(b"\0")
            if item
        ]
        return [ROOT / name for name in names]
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError) as exc:
        report.warn(f"git file inventory unavailable; using filesystem fallback: {exc}")
        result: list[Path] = []
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            parts = path.relative_to(ROOT).parts
            if ".git" in parts or "__pycache__" in parts:
                continue
            if path.is_relative_to(GENERATED_DIR):
                continue
            result.append(path)
        return result


def is_placeholder(value: str) -> bool:
    lowered = value.lower()
    markers = (
        "placeholder",
        "example",
        "replace_me",
        "replace-me",
        "changeme",
        "your_",
        "your-",
        "${",
        "<",
    )
    return any(marker in lowered for marker in markers)


def scan_public_inputs(files: list[Path], report: Report) -> None:
    for path in files:
        if not path.is_file():
            continue
        path_label = relative(path)
        try:
            size = path.stat().st_size
        except OSError as exc:
            report.error(f"{path_label}: cannot stat file: {exc}")
            continue
        if size > MAX_PUBLIC_FILE_BYTES:
            report.error(
                f"{path_label}: {size} bytes exceeds the public-demo limit "
                f"of {MAX_PUBLIC_FILE_BYTES} bytes"
            )
        if SECRET_FILENAME.search(path.name) and "example" not in path.name.lower():
            report.error(f"{path_label}: secret-like filename is not publishable")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            report.error(f"{path_label}: expected UTF-8 text")
            continue
        except OSError as exc:
            report.error(f"{path_label}: cannot read: {exc}")
            continue
        if (
            WINDOWS_DRIVE_ABSOLUTE.search(text)
            or WINDOWS_UNC_ABSOLUTE.search(text)
            or UNIX_LOCAL_ABSOLUTE.search(text)
        ):
            report.error(f"{path_label}: contains an absolute local path")
        for match in SECRET_ASSIGNMENT.finditer(text):
            if not is_placeholder(match.group(1)):
                report.error(f"{path_label}: contains a credential-like assignment")
                break
        if any(pattern.search(text) for pattern in KNOWN_SECRET_LITERALS):
            report.error(f"{path_label}: contains a known credential pattern")


def validate_generated_policy(files: list[Path], report: Report) -> None:
    gitignore_path = ROOT / ".gitignore"
    try:
        ignored_lines = {
            line.strip()
            for line in gitignore_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
    except OSError as exc:
        report.error(f".gitignore: cannot read generated-output policy: {exc}")
        ignored_lines = set()
    if "examples/generated/" not in ignored_lines:
        report.error(".gitignore: examples/generated/ must remain ignored")

    for path in files:
        try:
            path.relative_to(GENERATED_DIR)
        except ValueError:
            continue
        report.error(
            f"{relative(path)}: generated drafts must not be tracked or proposed for commit"
        )

    generator_path = ROOT / "scripts" / "create_route_prototype.py"
    try:
        generator_source = generator_path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(f"{relative(generator_path)}: cannot read: {exc}")
    else:
        if 'ROOT / "examples" / "generated"' not in generator_source:
            report.error(
                "create_route_prototype.py: default output must remain under "
                "examples/generated/"
            )


def validate_all_json(files: list[Path], report: Report) -> int:
    count = 0
    for path in files:
        if path.suffix.lower() != ".json":
            continue
        count += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            report.error(f"{relative(path)}: JSON parse failed: {exc}")
    return count


def validate_workflow_yaml(report: Report) -> int:
    """Validate the YAML subset used by the repository's GitHub workflow."""
    workflow_paths = sorted((ROOT / ".github" / "workflows").glob("*.y*ml"))
    for path in workflow_paths:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError) as exc:
            report.error(f"{relative(path)}: cannot read UTF-8 workflow YAML: {exc}")
            continue

        top_level_keys: set[str] = set()
        block_parent_indent: int | None = None
        for line_number, raw_line in enumerate(lines, start=1):
            if "\t" in raw_line:
                report.error(
                    f"{relative(path)}:{line_number}: YAML indentation must not use tabs"
                )
                continue
            content = raw_line.lstrip(" ")
            if not content or content.startswith("#"):
                continue
            indent = len(raw_line) - len(content)
            if indent % 2:
                report.error(
                    f"{relative(path)}:{line_number}: YAML indentation must use "
                    "two-space levels"
                )

            if block_parent_indent is not None:
                if indent > block_parent_indent:
                    continue
                block_parent_indent = None

            item_content = content[2:] if content.startswith("- ") else content
            if content.startswith("- ") and not item_content:
                report.error(
                    f"{relative(path)}:{line_number}: empty YAML sequence item"
                )
                continue

            is_mapping = bool(YAML_MAPPING_LINE.match(item_content))
            if not is_mapping and not content.startswith("- "):
                report.error(
                    f"{relative(path)}:{line_number}: expected a YAML mapping or "
                    "sequence item"
                )
                continue

            if indent == 0 and is_mapping:
                top_level_keys.add(item_content.split(":", 1)[0].strip("\"'"))
            if is_mapping:
                value = item_content.split(":", 1)[1].strip()
                if value in {"|", "|-", "|+", ">", ">-", ">+"}:
                    block_parent_indent = indent

        required = {"name", "on", "permissions", "jobs"}
        missing = required - top_level_keys
        if missing:
            report.error(
                f"{relative(path)}: missing top-level workflow keys "
                f"{sorted(missing)}"
            )
        text = "\n".join(lines)
        for required_fragment in (
            "runs-on:",
            "steps:",
            "scripts/validate_examples.py --strict",
            "scripts/create_route_prototype.py",
        ):
            if required_fragment not in text:
                report.error(
                    f"{relative(path)}: missing required workflow fragment "
                    f"'{required_fragment}'"
                )
    return len(workflow_paths)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat validator warnings as errors",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = Report(strict=args.strict)
    files = intended_public_files(report)
    json_count = validate_all_json(files, report)
    workflow_count = validate_workflow_yaml(report)
    route_stop_count, route_card_count = validate_route(report)
    story_page_count, story_card_count, media_task_count = validate_story(report)
    scan_public_inputs(files, report)
    validate_generated_policy(files, report)

    for warning in report.warnings:
        print(f"WARNING: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}")

    if report.errors:
        print(
            f"Validation failed: {len(report.errors)} error(s), "
            f"{len(report.warnings)} warning(s)."
        )
        return 1

    print(
        "Validation passed: "
        f"{len(files)} intended public files, {json_count} JSON files and "
        f"{workflow_count} workflow YAML file(s); "
        f"{route_stop_count} route stops and {route_card_count} route cards; "
        f"{story_page_count} story pages, {story_card_count} collection cards "
        f"and {media_task_count} media tasks; "
        "freeze, QA, publication-hazard and generated-draft checks passed; "
        f"{len(report.warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
