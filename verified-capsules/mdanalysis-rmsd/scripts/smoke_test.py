from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import MDAnalysis as mda


def main() -> int:
    capsule_dir = Path(__file__).resolve().parents[1]
    runner = capsule_dir / "scripts" / "run_mdanalysis_rmsd.py"
    result = subprocess.run(
        [sys.executable, str(runner), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    print(f"MDAnalysis {mda.__version__}")
    print("runner help OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
