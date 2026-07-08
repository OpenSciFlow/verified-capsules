from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency. Install with: python -m pip install pyyaml") from exc


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python scripts/summarize_verified_envs.py <verified-envs.yaml>", file=sys.stderr)
        return 2
    data = yaml.safe_load(Path(argv[1]).read_text(encoding="utf-8"))
    counts = Counter(item["status"] for item in data.get("matrix", []))
    for status in ["passed", "failed", "blocked", "untested"]:
        print(f"{status}: {counts.get(status, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
