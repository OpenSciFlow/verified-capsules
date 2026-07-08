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


def test_list_command_shows_capsules(capsys) -> None:
    assert main(["list"]) == 0
    output = capsys.readouterr().out
    assert "mdanalysis-rmsd" in output
    assert "gromacs-rmsd" in output


def test_list_command_supports_json(capsys) -> None:
    assert main(["list", "--format", "json"]) == 0
    output = capsys.readouterr().out
    assert '"capsule_id": "mdanalysis-rmsd"' in output
    assert '"declared_readiness": "R6"' in output
