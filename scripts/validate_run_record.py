from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency. Install with: python -m pip install jsonschema") from exc


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python scripts/validate_run_record.py <run-record.json>", file=sys.stderr)
        return 2
    schema = json.loads((ROOT / "schemas" / "run-record.schema.json").read_text(encoding="utf-8"))
    data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    jsonschema.validate(data, schema)
    print(f"validated run record: {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
