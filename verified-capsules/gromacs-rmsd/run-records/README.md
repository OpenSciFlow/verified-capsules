# Run Records

No successful run records are included yet.

`blocked-local-windows-no-gmx.json` records a local smoke-test readiness block where `gmx --version` could not run because GROMACS was not available on PATH.

When execution starts, write one JSON run record per attempt. Failed or blocked attempts are useful if they capture the command, return code, logs, environment, and known failure match.
