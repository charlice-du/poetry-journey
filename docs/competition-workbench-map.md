# Competition workbench map

> This is a newly written architectural explanation based on a read-only audit
> of team packages. It is not copied production documentation, does not publish
> teammate source code, and does not claim that the private system is
> reproducible from this repository.

The audited material shows two complementary workbench families. They share
provenance, status tracking and human-review principles, but they solve
different problems and should remain distinct public-demo pipelines.

## A. Production Workbench

The Production Workbench coordinates a story from research through a
self-contained playable artifact. Narrative generation is only one branch of
the system: collection cards, revision, media production, manifests and final
QA are equally important.

~~~mermaid
flowchart TD
    Q[Topic, quotation or story brief] --> NR[Narrative research]
    NR --> SG[Story generation]
    SG --> CS[Collection cards]
    SG --> FR[Fast remix, when requested]
    SG --> RV[Revision and evidence review]
    CS --> RV
    FR --> RV
    RV --> CF{Content-freeze gate}
    CF -->|approved text| IM[Image branch]
    CF -->|approved script| DB[Dubbing branch]
    CF --> MS[Manifests and status]
    IM --> AS[HTML assembly]
    DB --> AS
    MS --> AS
    AS --> QA{QA and human release gate}
    QA -->|pass| FH[Self-contained final HTML]
    QA -->|issues| RV
~~~

Important boundaries:

- **Narrative research** records what a source supports and what remains
  interpretation.
- **Fast remix** is a lighter editorial path, not a substitute for evidence
  review.
- **Revision** preserves references while changing structure or presentation.
- **Content freeze** prevents image, audio and assembly branches from silently
  using different text versions.
- **Image and dubbing branches** can run in parallel after the freeze, but both
  still require rights and quality review.
- **Manifests and status** make counts, references, gates and current artifacts
  inspectable.
- **QA** must describe the exact final artifact, not an older build with a
  similar filename.

The public story example represents these controls with
`story_data.example.json`, `story_manifest.example.json` and a tiny
`final.example.html`. It intentionally contains no generated media.

## B. Poetry Geo Workbench

The Poetry Geo Workbench converts a poet, city or poem query into a
research-backed cultural route and handbook. A production run uses structured
research before route writing; a place is not accepted merely because a poem
and a modern attraction share a name.

~~~mermaid
flowchart TD
    Q[Poet, city, poem and duration] --> RS[Research]
    KG[Authorized CNKGraph MCP] -. structured poetry and place records .-> RS
    RS --> EG[Evidence grading and dispute notes]
    EG --> CA[Candidate places]
    CA --> RT[Editorial route]
    RT --> CD[Cultural cards]
    CD --> HJ[Handbook JSON]
    HJ --> HH[Handbook HTML]
    HJ --> HP[Handbook PDF]
    RT --> CR[Coordinate and map review]
    CD --> PR[Photo and rights review]
    LIVE[Authorized current map and venue sources] -. live facts .-> CR
    CR --> HR{Human travel-information gate}
    PR --> HR
    HH --> HR
    HP --> HR
~~~

The CNKGraph MCP was a substantive research adapter in the audited production
architecture. It is optional only for this repository's offline demo, which
uses fixed synthetic fixtures. A fresh production-style research run would
need an authorized data source plus separate current map and venue checks.

The public route contracts preserve the main hand-off:

~~~text
candidates.example.json
  -> route.example.json
  -> cards.example.json
  -> handbook.example.md
~~~

The result remains a cultural sequence until live coordinates, travel times,
opening information and accessibility details have been independently checked.

## Shared control plane

~~~mermaid
flowchart LR
    WB[WorkBuddy or CodeBuddy] --> CT[Data contracts]
    CT --> ST[Status and manifests]
    ST --> HG[Human gates]
    HG --> VA[Validated public artifact]
    AD[Optional authorized adapters] -. external data or media .-> CT
~~~

WorkBuddy or CodeBuddy can orchestrate these contracts and explain unresolved
gates. It does not turn model output into verified history, grant media rights,
or make an external service safe by itself.

## Production artifact to public-demo representation

| Audited production concept | Public-demo representation | Why it is intentionally different |
| --- | --- | --- |
| Production narrative and collection-card files | `story_data.example.json` with three synthetic pages and two synthetic cards | Demonstrates references and labels without copying teammate prose |
| `production_manifest.json` and story manifests | `story_manifest.example.json` | Keeps counts, freeze, assembly and QA contracts while using a newly authored schema |
| Production final interactive book | Small `final.example.html` | Provides a hashable QA target without production UI, images, audio or interaction code |
| Real image and audio assets | Media-plan records with `not_generated` status | Avoids ownership, service-term, voice and file-size risks |
| Real image, TTS and voice-cloning services | Documented optional adapter boundary | No service implementation or credential is required by the public demo |
| Production status dashboard | JSON state plus validator output | Makes state inspectable without publishing private orchestration code |
| CNKGraph queries and responses | Small offline source and candidate fixtures | Avoids redistributing benchmark/API responses or implying live completeness |
| CNKGraph MCP implementation | Disabled-by-default config template | Shows the connection boundary without publishing ownership-unclear server code |
| Completed multi-stop route run | Three-stop synthetic cultural sequence | Demonstrates lineage while avoiding copied production output and live travel advice |
| Handbook JSON/HTML/PDF pipeline | Route cards plus a Markdown handbook | Keeps the public core dependency-free and reviewable |
| Production coordinate and photo workflows | Null coordinates and explicit review fields | Prevents stale or unverified map and rights claims |
| Private prompts and Skill implementations | Public CodeBuddy context and a newly authored demo Skill | Teaches safe use without redistributing team prompt libraries |

## What this repository proves

The repository can prove that its public examples parse, cross-references
resolve, freeze and QA hashes match, an offline route draft can be generated,
and common publication hazards are absent.

It cannot prove that the original private services remain available, that all
historical interpretations are definitive, that live travel details are
current, or that the audited packages may be redistributed.
