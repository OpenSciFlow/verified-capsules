from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import MDAnalysis as mda
import numpy as np


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git_commit(capsule_dir: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=capsule_dir.parents[1],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def workspace_dirty(capsule_dir: Path) -> bool | None:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=capsule_dir.parents[1],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return bool(result.stdout.strip())


def compute_rmsd(trajectory: Path, selection: str, output: Path) -> list[dict[str, float]]:
    universe = mda.Universe(str(trajectory))
    atoms = universe.select_atoms(selection)
    if len(atoms) == 0:
        raise ValueError(f"Selection matched no atoms: {selection}")

    reference = atoms.positions.copy()
    rows: list[dict[str, float]] = []
    for ts in universe.trajectory:
        delta = atoms.positions - reference
        value = float(np.sqrt(np.mean(np.sum(delta * delta, axis=1))))
        rows.append({"frame": int(ts.frame), "time_ps": float(ts.time), "rmsd_angstrom": value})

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["frame", "time_ps", "rmsd_angstrom"])
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_run_record(
    run_record: Path,
    run_id: str,
    started_at: str,
    finished_at: str,
    command: str,
    trajectory: Path,
    output: Path,
    selection: str,
    status: str,
    return_code: int,
    row_count: int,
    error: str | None = None,
) -> None:
    capsule_dir = Path(__file__).resolve().parents[1]
    record = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "capsule_id": "mdanalysis-rmsd",
        "status": status,
        "started_at": started_at,
        "finished_at": finished_at,
        "command_template_id": "mdanalysis-rmsd-example",
        "rendered_command": command,
        "return_code": return_code,
        "environment": {
            "os": platform.platform(),
            "python_version": platform.python_version(),
            "mdanalysis_version": mda.__version__,
            "git_commit": git_commit(capsule_dir),
            "workspace_dirty_at_run": workspace_dirty(capsule_dir),
        },
        "inputs": [
            {
                "name": "trajectory_pdb",
                "path": str(trajectory.as_posix()),
                "sha256": sha256(trajectory),
            },
            {
                "name": "selection",
                "value": selection,
            },
        ],
        "outputs": [
            {
                "name": "rmsd_csv",
                "path": str(output.as_posix()),
                "sha256": sha256(output) if output.exists() else None,
                "rows": row_count,
            }
        ],
        "logs": [],
        "hashes": [],
        "known_failure_matches": [],
        "limitations": [
            "Tiny synthetic PDB input; execution evidence only.",
            "No cross-environment verification is claimed.",
        ],
    }
    if error:
        record["logs"].append({"level": "error", "message": error})
    run_record.parent.mkdir(parents=True, exist_ok=True)
    run_record.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute a tiny MDAnalysis RMSD CSV and run record.")
    parser.add_argument("--trajectory", required=True, type=Path)
    parser.add_argument("--selection", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--run-record", required=True, type=Path)
    parser.add_argument("--run-id", default=f"mdanalysis-rmsd-{int(time.time())}")
    args = parser.parse_args()

    started_at = iso_now()
    command = " ".join(sys.argv)
    try:
        rows = compute_rmsd(args.trajectory, args.selection, args.output)
    except Exception as exc:
        finished_at = iso_now()
        write_run_record(
            args.run_record,
            args.run_id,
            started_at,
            finished_at,
            command,
            args.trajectory,
            args.output,
            args.selection,
            "failed",
            1,
            0,
            str(exc),
        )
        raise

    finished_at = iso_now()
    write_run_record(
        args.run_record,
        args.run_id,
        started_at,
        finished_at,
        command,
        args.trajectory,
        args.output,
        args.selection,
        "passed",
        0,
        len(rows),
    )
    print(f"wrote {args.output}")
    print(f"wrote {args.run_record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
