from __future__ import annotations

from pathlib import Path

from opensciflow_capsule.cli import main


ROOT = Path(__file__).resolve().parents[1]


def test_summary_command_runs_for_mdanalysis() -> None:
    assert main(["summary", "verified-capsules/mdanalysis-rmsd"]) == 0


def test_validate_command_runs_for_gromacs() -> None:
    assert main(["validate", "verified-capsules/gromacs-rmsd"]) == 0


def test_validate_supports_explicit_repo_root_from_other_cwd(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    assert main([
        "validate",
        "verified-capsules/mdanalysis-rmsd",
        "--repo-root",
        str(ROOT),
    ]) == 0
