# Release Checklist

Use this before tagging an OpenSciFlow Verified Capsules release.

## Required

- `opensciflow-capsule validate verified-capsules/mdanalysis-rmsd` passes.
- `opensciflow-capsule validate verified-capsules/gromacs-rmsd` passes.
- `opensciflow-capsule summary verified-capsules/mdanalysis-rmsd` matches the committed readiness claim.
- `opensciflow-capsule summary verified-capsules/gromacs-rmsd` matches the committed readiness claim.
- GitHub Actions `validate` passes.
- GitHub Actions `mdanalysis-rmsd-example` passes.
- GitHub Actions `gromacs-rmsd-smoke` passes.
- GitHub Actions `gromacs-rmsd-example` passes.
- README readiness table matches `verified-envs.yaml`.
- No capsule claims evidence beyond the verified environment matrix.

## Current v0.1 Boundary

- `mdanalysis-rmsd`: R6, tiny example only.
- `gromacs-rmsd`: R5, tiny example only.
- No HPC, GPU, clinical, drug-discovery, or scientific truth-validation claim.
- No claim of partnership with GROMACS, MDAnalysis, or any listed project.
