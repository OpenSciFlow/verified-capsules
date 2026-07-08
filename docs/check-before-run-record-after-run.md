# Check Before Run, Record After Run

OpenSciFlow uses a two-part execution discipline.

Before running:

- inspect capsule metadata;
- check inputs, outputs, environment, hardware, scheduler, weights, license, and citation;
- compare the target environment to the verified environment matrix;
- report relevant known failures;
- render a reviewed command template;
- request approval.

After running:

- record rendered command, timestamps, return code, logs, versions, inputs, outputs, hashes, and artifacts;
- record whether any known failure matched;
- record limitations and warnings;
- avoid upgrading readiness without evidence.
