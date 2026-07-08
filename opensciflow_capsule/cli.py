from __future__ import annotations

import argparse
import sys
from pathlib import Path

from opensciflow_capsule.catalog import discover_capsules, print_catalog_json, print_catalog_table
from opensciflow_capsule.smoke import run_smoke_test
from opensciflow_capsule.summary import print_summary, summarize_verified_envs
from opensciflow_capsule.validation import validate_capsule


def resolve_repo_root(repo_root: Path | None) -> Path:
    root = (repo_root or Path.cwd()).resolve()
    if not (root / "schemas").exists() or not (root / "verified-capsules").exists():
        raise SystemExit(
            f"{root} does not look like the verified-capsules repository root. "
            "Run from the repository root or pass --repo-root."
        )
    return root


def resolve_capsule_dir(root: Path, capsule_dir: Path) -> Path:
    if capsule_dir.is_absolute():
        return capsule_dir
    return root / capsule_dir


def capsule_verified_envs(capsule_dir: Path) -> Path:
    path = capsule_dir / "verified-envs.yaml"
    if not path.exists():
        raise SystemExit(f"Missing verified environment matrix: {path}")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and inspect OpenSciFlow verified capsules.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Path to the verified-capsules repository root. Defaults to the current directory.",
    )

    validate = subparsers.add_parser("validate", parents=[common], help="Validate a capsule directory.")
    validate.add_argument("capsule_dir", type=Path)

    smoke = subparsers.add_parser("smoke", parents=[common], help="Inspect or run a declared smoke test.")
    smoke.add_argument("capsule_dir", type=Path)
    smoke.add_argument("--smoke-test-id", default=None)
    smoke.add_argument("--execute", action="store_true")

    summary = subparsers.add_parser("summary", parents=[common], help="Summarize a capsule verified-env matrix.")
    summary.add_argument("capsule_dir", type=Path)

    catalog = subparsers.add_parser("list", parents=[common], help="List available capsules.")
    catalog.add_argument("--format", choices=["table", "json"], default="table")

    args = parser.parse_args(argv)

    try:
        root = resolve_repo_root(args.repo_root)

        if args.command == "validate":
            capsule_dir = resolve_capsule_dir(root, args.capsule_dir)
            validate_capsule(capsule_dir, root / "schemas")
            print(f"validated capsule: {capsule_dir}")
            return 0

        if args.command == "smoke":
            capsule_dir = resolve_capsule_dir(root, args.capsule_dir)
            return run_smoke_test(capsule_dir, args.smoke_test_id, args.execute)

        if args.command == "summary":
            capsule_dir = resolve_capsule_dir(root, args.capsule_dir)
            counts = summarize_verified_envs(capsule_verified_envs(capsule_dir))
            print_summary(counts, sys.stdout)
            return 0

        if args.command == "list":
            items = discover_capsules(root)
            if args.format == "json":
                print_catalog_json(items, sys.stdout)
            else:
                print_catalog_table(items, sys.stdout)
            return 0
    except SystemExit:
        raise
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    raise AssertionError(args.command)
