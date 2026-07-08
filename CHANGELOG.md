# Changelog

## v0.1.0-alpha - 2026-07-08

This is the first runnable alpha of OpenSciFlow Verified Capsules.

### Added

- Installable `opensciflow-capsule` CLI with:
  - `validate` for capsule schema and structure checks.
  - `summary` for verified environment matrix counts.
  - `smoke` for inspection-only or explicitly executed smoke tests.
  - `list` for capsule discovery in table or JSON format.
- `mdanalysis-rmsd` capsule with narrow R6 evidence for a tiny synthetic example across local Windows and GitHub Actions Ubuntu.
- `gromacs-rmsd` capsule with narrow R5 evidence for a tiny synthetic PDB example on GitHub Actions Ubuntu.
- CI coverage for CLI installation, capsule validation, environment summaries, catalog listing, and pytest.
- Separate GitHub Actions example workflows for MDAnalysis, GROMACS smoke, and GROMACS tiny RMSD execution.
- Product quickstart and release checklist.

### Boundaries

- No large-trajectory, GPU, HPC, or Slurm portability claim.
- No scientific correctness, clinical, drug-discovery, or benchmark-performance claim.
- No partnership or official affiliation claim with MDAnalysis, GROMACS, or any listed tool.
- R6 and R5 claims apply only to the recorded tiny examples and their verified environment matrix.
