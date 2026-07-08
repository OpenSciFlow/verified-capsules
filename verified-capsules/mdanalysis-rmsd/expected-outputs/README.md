# Expected Outputs

The R5 example run should produce:

- `outputs/rmsd.csv`
- `outputs/rmsd-conda.csv`
- `run-records/r5-local-windows-python313-mdanalysis210.json`
- `run-records/r5-local-windows-conda-python313-mdanalysis210.json`

Expected CSV shape:

```text
frame,time_ps,rmsd_angstrom
0,0.0,0.0
1,1.0,0.03872982785105705
2,2.0,0.07937253266572952
```

The exact RMSD values are produced by MDAnalysis 2.10.0 in the recorded environment.

The `rmsd.csv` and `rmsd-conda.csv` files should contain the same rows for this tiny example.

MDAnalysis warns that the PDB reader has no `dt` information and assigns `1.0 ps`. This is acceptable for this tiny execution check; the example does not make scientific timing claims.
