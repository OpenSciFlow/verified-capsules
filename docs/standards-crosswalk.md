# Standards Crosswalk

OpenSciFlow Verified Capsules should not compete with mature workflow, packaging, or agent-connection standards.

The intended role is narrower:

> agent-safe execution evidence for scientific tools.

## Position

| Existing standard or system | What it already does | OpenSciFlow should do |
|---|---|---|
| Common Workflow Language | Describes how to run command-line tools and connect them into workflows. | Map reviewed command templates to CWL `CommandLineTool` concepts when useful. Do not replace CWL. |
| RO-Crate | Packages research data with metadata. | Export capsule evidence as RO-Crate-compatible metadata where practical. |
| Workflow Run RO-Crate | Captures provenance of computational workflow executions. | Map OpenSciFlow run records to Workflow Run RO-Crate provenance fields. |
| Nextflow / Snakemake | Execute and scale workflows. | Provide tool-level evidence and run-record checks that workflow engines can consume. |
| MCP | Connects AI applications to external tools and data sources. | Expose checked capsule actions as agent tools, but keep execution restricted to reviewed command templates. |

## Non-Goal

OpenSciFlow should not become:

- another workflow engine;
- another package manager;
- another metadata standard with no runnable evidence;
- another general agent protocol.

## Practical Mapping

| OpenSciFlow artifact | Possible external mapping |
|---|---|
| `opensciflow.yaml` manifest | CWL tool metadata, RO-Crate computational tool metadata |
| reviewed command template | CWL `baseCommand` plus controlled inputs |
| environment spec | Conda, container metadata, or workflow-engine runtime profile |
| smoke test | workflow testing metadata or CI check |
| run record | Workflow Run RO-Crate provenance |
| verified environment matrix | additional execution evidence, not a portability guarantee |
| known failures | diagnostic extension; should remain explicit even if not mapped |

## Near-Term Rule

For the next phase, OpenSciFlow should prioritize one thing:

> make one small scientific tool execution inspectable, runnable, and recorded end to end.

The `mdanalysis-rmsd` capsule is the first R5 target. Cross-standard mapping should be added after the R5 evidence is stable, not before.
