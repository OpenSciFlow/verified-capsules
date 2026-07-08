# OpenSciFlow Verified Capsules

**Verified Capsules is an early OpenSciFlow repository for execution-facing evidence packages for AI for Science tools.**

It does not promise that scientific tools will run everywhere. A capsule records what a tool requires, what has been checked, where it has passed or failed, and what must be written after execution.

Core principle:

> OpenSciFlow does not eliminate scientific computing failures. It makes them explicit, checkable, diagnosable, and recordable.

## What This Repository Contains

- `verified-capsules/`: capsule examples and drafts.
- `schemas/`: JSON Schemas for manifests, environment specs, command templates, smoke tests, run records, verified environments, known failures, and capsule metadata.
- `scripts/`: local validation helpers.
- `docs/`: design notes for capsule structure, safety, readiness, and agent integration.

Start here:

- `docs/product-quickstart.md`
- `docs/release-checklist.md`

## What A Capsule Contains

A verified execution capsule should contain:

- `opensciflow.yaml`: manifest for one tool task.
- `environment.yml`, `apptainer.def`, or equivalent environment spec.
- Reviewed command templates.
- `smoke-test.sh` or another minimal smoke-test entrypoint.
- `test-inputs/`: small inputs or instructions for obtaining them.
- `expected-outputs/`: minimal expected outputs or shape checks.
- `run-records/`: real execution records when available.
- `verified-envs.yaml`: environment matrix recording pass, fail, blocked, or untested status.
- `known-failures.md`: known or anticipated failure modes.

## Current Capsules

| Capsule | Status | Readiness | Notes |
|---|---|---:|---|
| `mdanalysis-rmsd` | Multi-environment example runs recorded | R6 | Tiny MDAnalysis RMSD smoke/example runs in local Windows venv, local Windows Conda, and GitHub Actions Ubuntu. R6 applies only to the tiny example. |
| `gromacs-rmsd` | Example run recorded | R5 | Tiny `gmx rms` example passes on GitHub Actions Ubuntu through a reviewed wrapper. Local Windows remains blocked because `gmx` is not on PATH. No R6 claim. |

## Readiness Boundary

- R1/R2 artifacts can only reduce documentation inspection cost.
- R3 artifacts expose environment assumptions and reviewed command templates.
- R4/R5 artifacts may cautiously reduce setup trial-and-error in the verified environment.
- R6/R7 artifacts are needed before making bounded cross-environment migration claims.

## Validate Locally

Install the small validation dependencies:

```bash
python -m pip install -e .
```

Validate capsule skeletons and recorded examples:

```bash
opensciflow-capsule validate verified-capsules/gromacs-rmsd
opensciflow-capsule validate verified-capsules/mdanalysis-rmsd
```

List available capsules and their evidence matrix counts:

```bash
opensciflow-capsule list
opensciflow-capsule list --format json
```

Summarize environment evidence:

```bash
opensciflow-capsule summary verified-capsules/gromacs-rmsd
opensciflow-capsule summary verified-capsules/mdanalysis-rmsd
```

The legacy script entrypoint still works:

```bash
python scripts/opensciflow_capsule_cli.py validate verified-capsules/mdanalysis-rmsd
```

Run the MDAnalysis R5 example in a prepared environment:

```bash
python verified-capsules/mdanalysis-rmsd/scripts/smoke_test.py
python verified-capsules/mdanalysis-rmsd/scripts/run_mdanalysis_rmsd.py \
  --trajectory verified-capsules/mdanalysis-rmsd/test-inputs/tiny_ca_trajectory.pdb \
  --selection "name CA" \
  --output verified-capsules/mdanalysis-rmsd/outputs/rmsd.csv \
  --run-record verified-capsules/mdanalysis-rmsd/run-records/r5-local-windows-python313-mdanalysis210.json \
  --run-id r5-local-windows-python313-mdanalysis210
```

The same tiny example has also been rerun in a local Conda environment on Windows and recorded as `r5-local-windows-conda-python313-mdanalysis210.json`.

The `mdanalysis-rmsd-example` GitHub Actions workflow runs the same tiny example on Ubuntu and uploads the generated CSV and run record as CI artifacts. The successful run is recorded in `verified-envs.yaml` as narrow R6 evidence.

The `gromacs-rmsd-smoke` workflow installs GROMACS on GitHub Actions Ubuntu, runs `gmx --version`, validates a smoke run record, and uploads it as an artifact. This is recorded as R4 evidence in `verified-envs.yaml`.

The `gromacs-rmsd-example` workflow runs the tiny synthetic PDB example through a reviewed wrapper, validates the generated run record, and uploads the `.xvg` output and run-record artifact. This is recorded as R5 evidence in `verified-envs.yaml`.

## What This Is Not

- Not a run-anywhere promise.
- Not a replacement for Conda, Docker, Apptainer, Slurm, Nextflow, Snakemake, or package managers.
- Not a README replacement.
- Not a scientific truth or clinical decision system.
- Not a claim that listed tools are partners or officially associated with OpenSciFlow.

## Contribution Focus

Good first contributions:

- Correct a capsule field.
- Add a missing environment requirement.
- Add a known failure case.
- Provide smoke-test evidence.
- Add a failed run record with useful diagnostics.
- Review command-template safety.
- Add license or citation metadata.
