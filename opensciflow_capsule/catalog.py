from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TextIO

import yaml

from opensciflow_capsule.summary import summarize_verified_envs


@dataclass(frozen=True)
class CapsuleCatalogItem:
    capsule_id: str
    name: str
    declared_readiness: str
    verification_status: str
    passed: int
    failed: int
    blocked: int
    untested: int
    path: str


def load_yaml_object(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def discover_capsules(root: Path) -> list[CapsuleCatalogItem]:
    capsules_root = root / "verified-capsules"
    items: list[CapsuleCatalogItem] = []
    for manifest_path in sorted(capsules_root.glob("*/opensciflow.yaml")):
        capsule_dir = manifest_path.parent
        manifest = load_yaml_object(manifest_path)
        counts = summarize_verified_envs(capsule_dir / "verified-envs.yaml")
        items.append(
            CapsuleCatalogItem(
                capsule_id=str(manifest.get("capsule_id", capsule_dir.name)),
                name=str(manifest.get("name", capsule_dir.name)),
                declared_readiness=str(manifest.get("declared_readiness", "unknown")),
                verification_status=str(manifest.get("verification_status", "unknown")),
                passed=counts.get("passed", 0),
                failed=counts.get("failed", 0),
                blocked=counts.get("blocked", 0),
                untested=counts.get("untested", 0),
                path=str(capsule_dir.relative_to(root).as_posix()),
            )
        )
    return items


def print_catalog_table(items: list[CapsuleCatalogItem], stream: TextIO) -> None:
    headers = ["capsule", "ready", "status", "passed", "blocked", "untested"]
    rows = [
        [
            item.capsule_id,
            item.declared_readiness,
            item.verification_status,
            str(item.passed),
            str(item.blocked),
            str(item.untested),
        ]
        for item in items
    ]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows)) if rows else len(header)
        for index, header in enumerate(headers)
    ]
    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)), file=stream)
    print("  ".join("-" * width for width in widths), file=stream)
    for row in rows:
        print("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)), file=stream)


def print_catalog_json(items: list[CapsuleCatalogItem], stream: TextIO) -> None:
    print(json.dumps([asdict(item) for item in items], indent=2), file=stream)
