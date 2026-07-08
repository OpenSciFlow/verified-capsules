from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import TextIO

import yaml


def summarize_verified_envs(path: Path) -> Counter[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return Counter(item["status"] for item in data.get("matrix", []))


def print_summary(counts: Counter[str], stream: TextIO) -> None:
    for status in ["passed", "failed", "blocked", "untested"]:
        print(f"{status}: {counts.get(status, 0)}", file=stream)
