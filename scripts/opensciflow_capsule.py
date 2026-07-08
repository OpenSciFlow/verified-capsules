from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> int:
    return subprocess.call(args, cwd=ROOT)


def capsule_verified_envs(capsule_dir: Path) -> Path:
    path = capsule_dir / "verified-envs.yaml"
    if not path.exists():
        raise SystemExit(f"Missing verified environment matrix: {path}")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Small helper for OpenSciFlow verified capsules.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate a capsule directory.")
    validate.add_argument("capsule_dir", type=Path)

    smoke = subparsers.add_parser("smoke", help="Inspect or run a declared smoke test.")
    smoke.add_argument("capsule_dir", type=Path)
    smoke.add_argument("--smoke-test-id", default=None)
    smoke.add_argument("--execute", action="store_true")

    summary = subparsers.add_parser("summary", help="Summarize a capsule verified-env matrix.")
    summary.add_argument("capsule_dir", type=Path)

    args = parser.parse_args(argv)

    if args.command == "validate":
        return run([sys.executable, "scripts/validate_capsule.py", str(args.capsule_dir)])

    if args.command == "smoke":
        command = [sys.executable, "scripts/run_smoke_test.py", str(args.capsule_dir)]
        if args.smoke_test_id:
            command.extend(["--smoke-test-id", args.smoke_test_id])
        if args.execute:
            command.append("--execute")
        return run(command)

    if args.command == "summary":
        return run([
            sys.executable,
            "scripts/summarize_verified_envs.py",
            str(capsule_verified_envs(args.capsule_dir)),
        ])

    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
