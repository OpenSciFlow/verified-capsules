# MDAnalysis RMSD Capsule

This capsule is the first OpenSciFlow R6 target: a tiny MDAnalysis RMSD run with real smoke-test evidence, a small redistributable input, output CSV files, local run records, and a GitHub Actions Ubuntu example-run artifact.

Scope:

- load a small multi-model PDB file with MDAnalysis;
- select `name CA`;
- compute RMSD against the first frame;
- write a CSV output;
- write a JSON run record.

Recorded local evidence:

- `r5-local-windows-python313-mdanalysis210.json`: Python venv on Windows.
- `r5-local-windows-conda-python313-mdanalysis210.json`: Conda environment on the same Windows host.

Recorded multi-environment evidence:

- GitHub Actions Ubuntu run: https://github.com/OpenSciFlow/verified-capsules/actions/runs/28941403846
- Artifact: `mdanalysis-rmsd-github-actions-ubuntu`

This R6 claim is narrow. It does not validate scientific correctness beyond the tiny example, and it does not claim HPC, GPU, container, or large-trajectory portability. It only demonstrates the check-before-run and record-after-run contract across one local Windows host and one GitHub Actions Ubuntu runner.
