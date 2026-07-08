# Known Failures

This file currently lists anticipated failure modes. They are not yet observed run records.

| ID | Category | Symptom | Likely Cause | Agent Action | Status |
|---|---|---|---|---|---|
| gmx-missing | environment | `gmx: command not found` | GROMACS is not installed or not on PATH. | Block execution and ask the user to activate the declared environment or provide a verified environment. | anticipated |
| input-missing | input | GROMACS reports missing `.tpr` or trajectory file. | Input paths were not provided or are not readable. | Refuse execution until required input metadata is present and files are readable. | anticipated |
| group-selection | input | `gmx rms` waits for interactive group selection. | The command needs non-interactive group selection or a reviewed wrapper. | Do not invent shell piping; require a reviewed command template or wrapper for group selection. | anticipated |
| hpc-module-missing | hpc | `module: command not found` or missing GROMACS module. | Site-specific module system differs from capsule assumption. | Mark environment mismatch and request local HPC module details. | anticipated |
| container-unavailable | environment | `apptainer: command not found` | Container runtime unavailable on the target system. | Use local Conda path if verified, or block container execution. | anticipated |
