# MDAnalysis RMSD Capsule

This capsule is the first OpenSciFlow R5 target: a tiny MDAnalysis RMSD run with real smoke-test evidence, a small redistributable input, an output CSV, and a run record.

Scope:

- load a small multi-model PDB file with MDAnalysis;
- select `name CA`;
- compute RMSD against the first frame;
- write a CSV output;
- write a JSON run record.

This capsule does not validate scientific correctness beyond the tiny example. It only demonstrates the check-before-run and record-after-run contract.
