# Readiness Levels

Use readiness levels conservatively.

| Level | Meaning | Allowed claim |
|---|---|---|
| R0 | Project indexed only | Basic reference only. |
| R1 | Draft manifest | May reduce documentation inspection cost. |
| R2 | Schema-validated manifest | Fields are structured, not execution-tested. |
| R3 | Environment spec and command templates available | Execution assumptions are inspectable. |
| R4 | Smoke test passed in one environment | Minimal execution evidence for one environment. |
| R5 | Example run passed with run record | One real run has structured evidence. |
| R6 | Multi-environment verification | Some cross-environment evidence exists. |
| R7 | External reproduction | External user or machine reproduced the capsule. |

Do not claim reduced setup trial-and-error before R4. Do not claim cross-environment portability before R6.
