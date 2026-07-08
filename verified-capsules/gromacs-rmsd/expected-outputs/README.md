# Expected Outputs

R4 smoke evidence should include:

- `gmx --version` return code;
- version string captured in the run log;
- smoke run record artifact.

The next R5 target should produce:

- `outputs/rmsd-github-actions-ubuntu.xvg`
- `run-records/r5-github-actions-ubuntu-gromacs-rmsd.json`

The `.xvg` file is expected to contain GROMACS metadata comments and a small number of RMSD rows for the synthetic tiny input.
