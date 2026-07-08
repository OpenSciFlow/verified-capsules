# Product Quickstart

This repository is now a small runnable product around verified execution capsules.

## Install

```bash
python -m pip install -e .
```

## Inspect The Included Capsules

```bash
opensciflow-capsule validate verified-capsules/mdanalysis-rmsd
opensciflow-capsule summary verified-capsules/mdanalysis-rmsd

opensciflow-capsule validate verified-capsules/gromacs-rmsd
opensciflow-capsule summary verified-capsules/gromacs-rmsd
```

If you call the CLI from another directory, pass the repository root:

```bash
opensciflow-capsule validate verified-capsules/gromacs-rmsd --repo-root /path/to/verified-capsules
```

Expected summaries:

- `mdanalysis-rmsd`: 3 passed environments.
- `gromacs-rmsd`: 1 passed, 1 blocked, 1 untested environment.

## Run Smoke Checks

Inspection-only smoke command:

```bash
opensciflow-capsule smoke verified-capsules/gromacs-rmsd
```

Execute smoke checks only inside a prepared environment:

```bash
opensciflow-capsule smoke verified-capsules/mdanalysis-rmsd --execute
```

## Current Evidence

| Capsule | Readiness | Evidence boundary |
|---|---:|---|
| `mdanalysis-rmsd` | R6 | Tiny synthetic example across local Windows and GitHub Actions Ubuntu. |
| `gromacs-rmsd` | R5 | Tiny synthetic example on GitHub Actions Ubuntu through a reviewed wrapper. |

Neither capsule validates scientific correctness. They validate execution discipline: requirements, reviewed commands, smoke/example execution, verified environment matrix, known failures, and run records.
