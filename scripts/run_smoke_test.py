from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency. Install with: python -m pip install pyyaml") from exc


def load_manifest(capsule_dir: Path) -> dict:
    manifest_path = capsule_dir / "opensciflow.yaml"
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest: {manifest_path}")
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"Manifest must be a YAML object: {manifest_path}")
    return data


def command_for_entrypoint(entrypoint: Path) -> list[str]:
    if entrypoint.suffix == ".py":
        return [sys.executable, str(entrypoint)]
    if entrypoint.suffix == ".sh":
        return ["bash", str(entrypoint)]
    return [str(entrypoint)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("capsule_dir")
    parser.add_argument("--smoke-test-id", default=None)
    parser.add_argument("--execute", action="store_true", help="Actually run the declared smoke test")
    args = parser.parse_args()

    capsule_dir = Path(args.capsule_dir)
    manifest = load_manifest(capsule_dir)
    smoke_tests = manifest.get("smoke_tests", [])
    if args.smoke_test_id:
        smoke_tests = [item for item in smoke_tests if item.get("id") == args.smoke_test_id]
    if not smoke_tests:
        raise SystemExit("No matching smoke tests declared in manifest.")

    smoke_test = capsule_dir / smoke_tests[0]["entrypoint"]
    if not smoke_test.exists():
        raise SystemExit(f"Missing smoke test entrypoint: {smoke_test}")

    if not args.execute:
        print(f"Smoke test available but not executed: {smoke_test}")
        print("Use --execute only inside a prepared environment.")
        return 0

    return subprocess.call(command_for_entrypoint(smoke_test))


if __name__ == "__main__":
    raise SystemExit(main())
