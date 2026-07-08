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


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def schema_store() -> dict[str, dict]:
    return {
        f"https://opensciflow.org/schemas/{path.name}": load_json(path)
        for path in SCHEMAS.glob("*.schema.json")
    }


def validate_with_schema(data: dict, schema_name: str) -> None:
    schema = load_json(SCHEMAS / schema_name)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        resolver = jsonschema.RefResolver.from_schema(schema, store=schema_store())
        jsonschema.validate(data, schema, resolver=resolver)


def require_path(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)


def validate_capsule(capsule_dir: Path) -> None:
    require_path(capsule_dir)
    require_path(capsule_dir / "opensciflow.yaml")
    require_path(capsule_dir / "test-inputs")
    require_path(capsule_dir / "expected-outputs")
    require_path(capsule_dir / "run-records")
    require_path(capsule_dir / "verified-envs.yaml")
    require_path(capsule_dir / "known-failures.md")

    manifest = load_yaml(capsule_dir / "opensciflow.yaml")
    validate_with_schema(manifest, "manifest.schema.json")

    for env_file in manifest.get("environment", {}).get("files", []):
        require_path(capsule_dir / env_file)

    for smoke_test in manifest.get("smoke_tests", []):
        require_path(capsule_dir / smoke_test["entrypoint"])

    verified_envs = load_yaml(capsule_dir / "verified-envs.yaml")
    validate_with_schema(verified_envs, "verified-envs.schema.json")

    if manifest["capsule_id"] != verified_envs["capsule_id"]:
        raise ValueError("capsule_id mismatch between opensciflow.yaml and verified-envs.yaml")

    run_records = sorted((capsule_dir / "run-records").glob("*.json"))
    for record_path in run_records:
        validate_with_schema(load_json(record_path), "run-record.schema.json")

    print(f"validated capsule: {capsule_dir}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python scripts/validate_capsule.py <capsule-dir>", file=sys.stderr)
        return 2
    validate_capsule(Path(argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
