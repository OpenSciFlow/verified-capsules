from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("capsule_dir")
    parser.add_argument("--execute", action="store_true", help="Actually run smoke-test.sh")
    args = parser.parse_args()

    smoke_test = Path(args.capsule_dir) / "smoke-test.sh"
    if not smoke_test.exists():
        raise SystemExit(f"Missing smoke test: {smoke_test}")

    if not args.execute:
        print(f"Smoke test available but not executed: {smoke_test}")
        print("Use --execute only inside a prepared environment.")
        return 0

    return subprocess.call(["bash", str(smoke_test)])


if __name__ == "__main__":
    raise SystemExit(main())
