#!/usr/bin/env python3
"""Create an empty academic evidence register CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIELDS = [
    "evidence_id",
    "source_id",
    "source_path",
    "source_type",
    "location",
    "heading",
    "claim_or_finding",
    "method_context",
    "limitation",
    "target_chapter",
    "citation_key",
    "verification_state",
    "quality",
    "notes",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an empty evidence register CSV.")
    parser.add_argument("output", help="Path to the CSV file to create.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing file.")
    args = parser.parse_args()

    output = Path(args.output)
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()

    print(f"Created evidence register: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
