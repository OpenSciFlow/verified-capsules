from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git_commit(capsule_dir: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=capsule_dir.parents[1],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def workspace_dirty(capsule_dir: Path) -> bool | None:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=capsule_dir.parents[1],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return bool(result.stdout.strip())


def first_version_line(text: str) -> str | None:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return None


def write_record(
    *,
    run_record: Path,
    run_id: str,
    status: str,
    started_at: str,
    finished_at: str,
    rendered_command: str,
    return_code: int,
    structure: Path,
    trajectory: Path,
    output: Path,
    stdout: str,
    stderr: str,
) -> None:
    capsule_dir = Path(__file__).resolve().parents[1]
    version_result = subprocess.run(
        ["gmx", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    version_text = (version_result.stdout or "") + (version_result.stderr or "")
    record = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "capsule_id": "gromacs-rmsd",
        "status": status,
        "started_at": started_at,
        "finished_at": finished_at,
        "command_template_id": "gromacs-rmsd-reviewed-wrapper",
        "rendered_command": rendered_command,
        "environment": {
            "os": platform.platform(),
            "python_version": platform.python_version(),
            "gromacs_version_first_line": first_version_line(version_text),
            "git_commit": git_commit(capsule_dir),
            "workspace_dirty_at_run": workspace_dirty(capsule_dir),
        },
        "inputs": [
            {
                "name": "structure_or_tpr",
                "path": structure.as_posix(),
                "sha256": sha256(structure),
            },
            {
                "name": "trajectory",
                "path": trajectory.as_posix(),
                "sha256": sha256(trajectory),
            },
            {
                "name": "interactive_group_selection",
                "value": "0\\n0\\n",
                "meaning": "Use GROMACS group 0 twice for least-squares fit and RMSD calculation in the tiny test input.",
            },
        ],
        "outputs": [
            {
                "name": "rmsd_xvg",
                "path": output.as_posix(),
                "sha256": sha256(output),
            }
        ],
        "return_code": return_code,
        "logs": [
            {
                "level": "info",
                "stream": "stdout",
                "message": stdout[-4000:],
            },
            {
                "level": "error" if return_code else "info",
                "stream": "stderr",
                "message": stderr[-4000:],
            },
        ],
        "hashes": [
            {
                "path": structure.as_posix(),
                "sha256": sha256(structure),
            },
            {
                "path": trajectory.as_posix(),
                "sha256": sha256(trajectory),
            },
            {
                "path": output.as_posix(),
                "sha256": sha256(output),
            },
        ],
        "known_failure_matches": [] if return_code == 0 else ["group-selection"],
        "limitations": [
            "Tiny synthetic PDB input; execution evidence only.",
            "The wrapper uses reviewed non-interactive group selection for the tiny input.",
            "No large-trajectory or HPC claim is made.",
        ],
    }
    run_record.parent.mkdir(parents=True, exist_ok=True)
    run_record.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a reviewed GROMACS RMSD tiny example.")
    parser.add_argument("--structure", required=True, type=Path)
    parser.add_argument("--trajectory", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--run-record", required=True, type=Path)
    parser.add_argument("--run-id", default=f"gromacs-rmsd-{int(time.time())}")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rendered = (
        f"gmx rms -s {args.structure.as_posix()} "
        f"-f {args.trajectory.as_posix()} -o {args.output.as_posix()}"
    )
    started_at = iso_now()
    result = subprocess.run(
        ["gmx", "rms", "-s", str(args.structure), "-f", str(args.trajectory), "-o", str(args.output)],
        input="0\n0\n",
        check=False,
        capture_output=True,
        text=True,
    )
    finished_at = iso_now()
    write_record(
        run_record=args.run_record,
        run_id=args.run_id,
        status="passed" if result.returncode == 0 else "failed",
        started_at=started_at,
        finished_at=finished_at,
        rendered_command=rendered,
        return_code=result.returncode,
        structure=args.structure,
        trajectory=args.trajectory,
        output=args.output,
        stdout=result.stdout,
        stderr=result.stderr,
    )
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    print(f"wrote {args.output}")
    print(f"wrote {args.run_record}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
