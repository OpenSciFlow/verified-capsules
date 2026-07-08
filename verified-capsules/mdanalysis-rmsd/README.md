# MDAnalysis RMSD Capsule

This capsule is the first OpenSciFlow R5 target: a tiny MDAnalysis RMSD run with real smoke-test evidence, a small redistributable input, output CSV files, and run records.

Scope:

- load a small multi-model PDB file with MDAnalysis;
- select `name CA`;
- compute RMSD against the first frame;
- write a CSV output;
- write a JSON run record.

Recorded local evidence:

- `r5-local-windows-python313-mdanalysis210.json`: Python venv on Windows.
- `r5-local-windows-conda-python313-mdanalysis210.json`: Conda environment on the same Windows host.

This is still R5, not R6. It does not validate scientific correctness beyond the tiny example, and it does not claim cross-OS or container portability. It only demonstrates the check-before-run and record-after-run contract.
