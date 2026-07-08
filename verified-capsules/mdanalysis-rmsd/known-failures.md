# Known Failures

| ID | Category | Symptom | Likely Cause | Agent Action | Status |
|---|---|---|---|---|---|
| mda-missing | environment | `ModuleNotFoundError: No module named 'MDAnalysis'` | Environment is not active or MDAnalysis is not installed. | Block execution and ask the user to activate the capsule environment. | observed |
| empty-selection | input | `Selection matched no atoms` | The selection string does not match atoms in the input. | Refuse full execution until the selection is corrected or reviewed. | observed |
| malformed-pdb | input | MDAnalysis parser error or zero frames. | Input file is not a valid PDB trajectory-like file. | Block execution and ask for a valid input or conversion step. | anticipated |
| unsupported-python | environment | MDAnalysis cannot be installed for the Python version. | Python version lacks compatible wheels or build dependencies. | Use the declared environment or record a blocked environment entry. | anticipated |
