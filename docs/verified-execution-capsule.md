# Verified Execution Capsule

A verified execution capsule is a directory that packages the evidence an agent needs before and after running a scientific tool.

Required pieces:

- manifest;
- environment spec;
- reviewed command templates;
- smoke tests;
- test inputs and expected outputs;
- run records;
- verified environment matrix;
- known failure records.

The word `verified` is bounded. A capsule is only verified for the environments and runs recorded in its evidence files.
