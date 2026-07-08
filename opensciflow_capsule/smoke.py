from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


def load_manifest(capsule_dir: Path) -> dict:
    manifest_path = capsule_dir / "opensciflow.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing manifest: {manifest_path}")
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Manifest must be a YAML object: {manifest_path}")
    return data


def command_for_entrypoint(entrypoint: Path) -> list[str]:
    if entrypoint.suffix == ".py":
        return [sys.executable, str(entrypoint)]
    if entrypoint.suffix == ".sh":
        return ["bash", str(entrypoint)]
    return [str(entrypoint)]


def select_smoke_test(capsule_dir: Path, smoke_test_id: str | None = None) -> Path:
    manifest = load_manifest(capsule_dir)
    smoke_tests = manifest.get("smoke_tests", [])
    if smoke_test_id:
        smoke_tests = [item for item in smoke_tests if item.get("id") == smoke_test_id]
    if not smoke_tests:
        raise ValueError("No matching smoke tests declared in manifest.")

    smoke_test = capsule_dir / smoke_tests[0]["entrypoint"]
    if not smoke_test.exists():
        raise FileNotFoundError(f"Missing smoke test entrypoint: {smoke_test}")
    return smoke_test


def run_smoke_test(capsule_dir: Path, smoke_test_id: str | None, execute: bool) -> int:
    smoke_test = select_smoke_test(capsule_dir, smoke_test_id)
    if not execute:
        print(f"Smoke test available but not executed: {smoke_test}")
        print("Use --execute only inside a prepared environment.")
        return 0
    return subprocess.call(command_for_entrypoint(smoke_test))
