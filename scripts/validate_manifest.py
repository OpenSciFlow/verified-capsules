from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

try:
    import jsonschema
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency. Install with: python -m pip install jsonschema pyyaml"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_store() -> dict[str, dict]:
    return {
        f"https://opensciflow.org/schemas/{path.name}": load_json(path)
        for path in SCHEMAS.glob("*.schema.json")
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python scripts/validate_manifest.py <opensciflow.yaml>", file=sys.stderr)
        return 2
    schema = load_json(SCHEMAS / "manifest.schema.json")
    data = yaml.safe_load(Path(argv[1]).read_text(encoding="utf-8"))
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        resolver = jsonschema.RefResolver.from_schema(schema, store=schema_store())
        jsonschema.validate(data, schema, resolver=resolver)
    print(f"validated manifest: {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
