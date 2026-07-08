# Run Records

No successful RMSD example-run records are included yet.

The `gromacs-rmsd-smoke` workflow uploads a successful R4 smoke run record as an artifact:

- workflow: https://github.com/OpenSciFlow/verified-capsules/actions/workflows/gromacs-rmsd-smoke.yml
- artifact name: `gromacs-rmsd-smoke-github-actions-ubuntu`

`blocked-local-windows-no-gmx.json` records a local smoke-test readiness block where `gmx --version` could not run because GROMACS was not available on PATH.

When execution starts, write one JSON run record per attempt. Failed or blocked attempts are useful if they capture the command, return code, logs, environment, and known failure match.
