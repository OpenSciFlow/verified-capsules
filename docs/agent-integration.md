# Agent Integration

An agent using a capsule should:

1. Read the manifest and verified environment matrix.
2. Check whether the target environment matches known evidence.
3. Report relevant known failures.
4. Refuse if required metadata is missing.
5. Render only reviewed command templates.
6. Run smoke tests when available and approved.
7. Ask for approval before full execution.
8. Write a run record after execution starts.

The agent must not claim reproducibility beyond the verified environment matrix.
