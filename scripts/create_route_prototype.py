#!/usr/bin/env python3
"""Create an offline, evidence-linked cultural sequence from demo candidates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = ROOT / "examples" / "poetry-route" / "candidates.example.json"
DEFAULT_OUTPUT = ROOT / "examples" / "generated" / "route-prototype.json"
DURATION_LIMITS = {"half_day": 2, "one_day": 3, "two_day": 5}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--city", required=True, help="exact city name in the data")
    parser.add_argument("--poet", required=True, help="exact poet name in the data")
    parser.add_argument(
        "--duration",
        choices=sorted(DURATION_LIMITS),
        default="one_day",
    )
    parser.add_argument(
        "--max-stops",
        type=int,
        default=None,
        help="optional positive cap in addition to the duration cap",
    )
    parser.add_argument(
        "--candidate-file",
        type=Path,
        default=DEFAULT_CANDIDATES,
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_candidates(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("candidates"), list):
        raise ValueError("candidate file must contain a candidates list")
    return data


def main() -> int:
    args = parse_args()
    if args.max_stops is not None and args.max_stops < 1:
        print("ERROR: --max-stops must be positive", file=sys.stderr)
        return 2

    try:
        data = load_candidates(args.candidate_file)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: cannot load candidates: {exc}", file=sys.stderr)
        return 1

    matched = [
        item
        for item in data["candidates"]
        if isinstance(item, dict)
        and item.get("modern_location", {}).get("city") == args.city
        and args.poet in item.get("poets", [])
    ]
    matched.sort(key=lambda item: (-int(item.get("priority", 0)), item.get("id", "")))

    limit = DURATION_LIMITS[args.duration]
    if args.max_stops is not None:
        limit = min(limit, args.max_stops)
    selected = matched[:limit]
    if not selected:
        print(
            f"ERROR: no candidates for city={args.city!r}, poet={args.poet!r}",
            file=sys.stderr,
        )
        return 1

    stops = []
    for index, candidate in enumerate(selected, start=1):
        relation = candidate.get("relation", {})
        stops.append(
            {
                "stop_id": f"draft-stop-{index:02d}",
                "candidate_id": candidate["id"],
                "display_name": candidate["display_name"],
                "order": index,
                "source_refs": relation.get("source_refs", []),
                "evidence_status": relation.get("status"),
                "review": candidate.get("review"),
            }
        )

    result = {
        "schema_version": "1.0",
        "artifact_type": "poetry_route_prototype",
        "generator": "scripts/create_route_prototype.py",
        "query": {
            "city": args.city,
            "poet": args.poet,
            "duration": args.duration,
        },
        "status": "offline_draft",
        "ordering_mode": "priority_sequence_not_navigation",
        "stops": stops,
        "warnings": [
            "Selected from a small teaching dataset, not a complete search.",
            "No live maps, opening hours, prices or travel times were used.",
            "Human historical and travel-information review is required.",
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    try:
        display_path = args.output.resolve().relative_to(ROOT)
    except ValueError:
        display_path = args.output.resolve()
    print(f"Wrote {display_path} with {len(stops)} stop(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
