# HPC And Slurm Notes

HPC execution is site-specific. A capsule should not invent:

- partition names;
- account names;
- module names;
- GPU resource syntax;
- walltime limits;
- container runtime availability;
- shared filesystem paths.

For Slurm, a capsule may provide reviewed wrapper templates, but the target site still needs local review before execution.
