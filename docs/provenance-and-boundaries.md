# Provenance and publication boundaries

## Decision record

The reviewed team bundles demonstrate that a fuller workbench was assembled
and locally exercised. They are not copied into this public repository because
the review found no explicit redistribution license for the team packages,
found machine-specific absolute paths, and found at least one non-placeholder
credential-like value. Publishing the bundles unchanged would therefore create
ownership, security and portability risks.

No secret value is reproduced here. The credential should be treated as
compromised if it was ever shared outside its intended audience: revoke or
rotate it in the relevant service.

## Included and excluded material

| Source component | Apparent author / owner | Redistribution evidence | Safe to include? | Treatment |
| --- | --- | --- | --- | --- |
| Existing README and hosted showcase screenshots | Existing public repository / team project | Already present in this public repository | Retain only | Preserved with attribution context |
| Team production skills and launch scripts | Multiple team contributors | No package-level LICENSE or NOTICE found in the reviewed bundle | No direct copy | Describe the workflow only |
| Original Poetry Route Workbench source | Team contributor material | No public redistribution permission established | No direct copy | Replace with new contracts and synthetic examples |
| CNKGraph MCP adapter | Team or external contributor; exact ownership unresolved | No redistributable server license established | Config only | Publish a non-secret template; omit implementation |
| Generated image and audio bundles | Mixed team input and external generation services | Rights and service terms vary | No | Keep local; publish no copied media |
| Public-demo docs, JSON and Python scripts | Newly authored for this repository | Original material created in this staging change | Yes, subject to repository policy | Include without claiming it is competition output |
| MCP configuration example | Newly authored interface template | Contains no server code or credential | Yes | Include disabled by default |

## Data provenance in the examples

The example cultural records are intentionally small and are not copied from
the team packages. They demonstrate a provenance shape rather than a complete
scholarly dataset.

Source entries identify a classical work and locator. They do not reproduce
long passages. URLs are left null when a stable, reviewed digital edition has
not been selected. Modern venue fields that need current verification are
explicitly null or marked requires_live_map_check.

## Licensing posture

There is currently no repository-wide license. That is deliberate: the
repository mixes an existing team-project showcase with newly authored public
demo material, and not every original asset has a confirmed reusable license.
Absence of a license does not grant permission to reuse, modify or redistribute
the material.

If the team later agrees on publication terms, add:

1. a LICENSE covering only material the team is entitled to license;
2. a NOTICE or asset manifest for exceptions;
3. explicit third-party attribution and model/service terms;
4. contributor consent for any team-authored code being published.

## Claims that should not be made

Do not describe this repository as the complete competition codebase, a
production-ready travel planner, a fully open-source dataset, or proof that all
external services remain available. It is a transparent, runnable
representation of the workflow and its quality controls.
