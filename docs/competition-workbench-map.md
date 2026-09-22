# Competition workbench map

This document summarizes the two workbench architectures used during the
project. The diagrams were reconstructed from the team packages for
documentation; the original internal implementation is not published here.

The project used two separate workbenches. They share ideas such as source
tracking, status management and review steps, but serve different purposes.

## A. Production Workbench

The Production Workbench manages the path from source research to a playable
story. Besides writing the narrative, it tracks collection cards, revisions,
image and voice production, assembly and QA.

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

### How the stages fit together

- **Narrative research** records what the sources support and where
  interpretation begins.
- **Fast remix** provides a lighter editorial path but still goes through
  evidence review.
- **Revision** can change structure or presentation while preserving source
  references.
- **Content freeze** gives the image, audio and assembly branches a shared text
  version.
- **Image and dubbing branches** can run in parallel after the freeze, with
  separate rights and quality review.
- **Manifests and status** record artifact references, counts and the current
  state of each stage.
- **QA** refers to the exact final artifact rather than another build with a
  similar filename.

The public story example represents these stages with
`story_data.example.json`, `story_manifest.example.json` and a small
`final.example.html`. It contains no generated media.

## B. Poetry Geo Workbench

The Poetry Geo Workbench converts a poet, city or poem query into a
research-backed cultural route and handbook. Research comes before route
writing: a place is not accepted simply because a poem and a modern attraction
share a name.

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

In the original workflow, CNKGraph MCP supplied structured information about
poems, poets, places and related cultural entities. The public demo works
without it by using fixed example data. A fresh research run would still need
an authorized data source and current map and venue checks.

The public route contracts preserve the main hand-off:

~~~text
candidates.example.json
  -> route.example.json
  -> cards.example.json
  -> handbook.example.md
~~~

The result remains a cultural sequence until coordinates, travel times,
opening information and accessibility details have been checked.

## Shared workflow

~~~mermaid
flowchart LR
    WB[WorkBuddy or CodeBuddy] --> CT[Data contracts]
    CT --> ST[Status and manifests]
    ST --> HG[Human gates]
    HG --> VA[Validated public artifact]
    AD[Optional authorized adapters] -. external data or media .-> CT
~~~

WorkBuddy or CodeBuddy can help move between these stages, inspect the
artifacts and flag items that still need review. Historical claims, media
rights and live external data still need to be checked separately.

## Production artifact to public-example mapping

| Production concept | Public example | Public-demo approach |
| --- | --- | --- |
| Production narrative and collection-card files | `story_data.example.json` with three synthetic pages and two synthetic cards | Shows references and labels without copying team prose |
| Production and story manifests | `story_manifest.example.json` | Preserves counts, freeze, assembly and QA in a small example |
| Production final interactive book | Small `final.example.html` | Provides a QA target without production UI, images, audio or interaction code |
| Real image and audio assets | Media-plan records with `not_generated` status | Keeps workflow states visible without redistributing assets |
| Real image, TTS and voice-cloning services | Documented optional adapter boundary | The offline demo needs no service implementation or credential |
| Production status dashboard | JSON state plus validator output | Makes state inspectable without publishing orchestration code |
| CNKGraph queries and responses | Small offline source and candidate fixtures | Uses no benchmark or API response corpus |
| CNKGraph MCP implementation | Disabled-by-default config template | Shows the connection point without publishing the server |
| Completed multi-stop route run | Three-stop synthetic cultural sequence | Demonstrates lineage without making live travel claims |
| Handbook JSON/HTML/PDF pipeline | Route cards plus a Markdown handbook | Keeps the public example dependency-free and easy to inspect |
| Production coordinate and photo workflows | Null coordinates and explicit review fields | Leaves unverified map and rights details open for review |
| Private prompts and Skill implementations | Public CodeBuddy context and a demo Skill | Provides safe project guidance without redistributing team prompts |

## Scope of the public demo

The public demo checks that its example data is internally consistent, that
references resolve and that the offline generator works. It does not reproduce
the original private services or replace historical and live-data review.
