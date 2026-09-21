# Architecture and data contracts

## Poetry Route Workbench

~~~mermaid
flowchart LR
    Q[City / poet / duration] --> C[Candidate places]
    C --> E[Evidence and review labels]
    E --> R[Cultural sequence]
    R --> K[Learning cards]
    K --> H[Handbook]
    R -. live check .-> M[Maps and venue information]
    E -. optional .-> G[Authorized knowledge graph MCP]
~~~

The public implementation is deliberately data-first:

| Stage | Contract | Required trace |
| --- | --- | --- |
| Candidate collection | candidates.example.json | Candidate → evidence source |
| Selection | route.example.json | Stop → candidate |
| Enrichment | cards.example.json | Card → stop, candidate and source |
| Presentation | handbook.example.md | Section → stop identifier |

The sample order is a cultural/editorial sequence. A production itinerary must
still obtain current coordinates, opening hours, accessibility information and
travel time from authorized live sources.

## Story Production Workbench

~~~mermaid
flowchart LR
    P[Topic or quoted line] --> S[Source research]
    S --> T[Story structure]
    T --> W[Scene text]
    W --> MP[Image / voice media plan]
    MP --> A[Assembly]
    S --> HR[Human review]
    W --> HR
    MP --> HR
    HR --> A
~~~

The public story contract separates:

- **source notes** — what a cited text supports;
- **editorial interpretation** — a defensible reading that should not be
  presented as the source's exact wording;
- **creative adaptation** — dialogue, pacing or staging invented for the
  narrative;
- **media tasks** — descriptions of assets that have not been generated;
- **review gates** — decisions that remain human responsibilities.

## Reliability model

An output is not considered reliable merely because a model generated it. The
pipeline should preserve four things:

1. **Provenance:** each material claim points to a source identifier.
2. **Claim strength:** primary text, later tradition, editorial inference and
   live venue fact are not treated as equivalent.
3. **Abstention:** unavailable coordinates or uncertain historical links stay
   empty or marked for review.
4. **Human responsibility:** publication, historical framing, child-safety,
   media rights and current travel advice require named review gates.

## Responsibility by layer

| Layer | Responsibility | Not responsible for |
| --- | --- | --- |
| Agent orchestration | Move work between contracts, preserve references, expose uncertainty | Turning generated text into verified fact |
| MCP data access | Retrieve structured poetry, person, place or allusion records from an authorized source | Granting publication rights or resolving every historical dispute |
| Workbench UI | Show state, previews, review status and selected artifacts | Serving as the evidence source |
| Human review | Decide source adequacy, historical framing, travel currency, pedagogy and media rights | Being silently replaced by a model confidence score |

## Portability boundary

The JSON examples and Python scripts are portable and offline. External
knowledge graphs, web search, maps, image generation and speech services are
adapters outside the public core. The config template describes where an
authorized MCP adapter could connect; it does not bundle or license one.
