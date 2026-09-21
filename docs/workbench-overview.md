# Workbench overview

## Why this public demo exists

During the competition, the team explored two related workbench ideas:

- a **Story Production Workbench** that coordinates research, writing, image
  planning, voice planning and assembly;
- a **Poetry Route Workbench** that turns a city or poet query into a
  research-backed cultural sequence and learning material.

The original packages were built by multiple contributors and contain local
configuration, generated assets and external-service assumptions. They are not
copied into this repository. This public demo instead documents the reusable
ideas through newly authored schemas, small synthetic examples and
dependency-free scripts.

## What is included

| Area | Public artifact | What it demonstrates |
| --- | --- | --- |
| Route research | candidates.example.json | Evidence, confidence and review status live beside each candidate |
| Route synthesis | route.example.json | A route references candidates instead of duplicating claims |
| Learning content | cards.example.json and handbook.example.md | Downstream outputs remain traceable to stops and sources |
| Story production | story data, manifest and synthetic final HTML | Pages, cards, media plans, freeze, assembly and QA remain inspectable |
| Validation | scripts/validate_examples.py | Cross-file identifiers and publication hazards are checked |
| Small runnable demo | scripts/create_route_prototype.py | A deterministic offline draft can be generated from the examples |
| Agent guidance | .codebuddy/ | WorkBuddy and CodeBuddy receive the same safety and provenance rules |

## What is intentionally excluded

- Teammates' production source packages and internal prompt libraries
- API keys, tokens, local absolute paths and machine-specific launch scripts
- Licensed or ownership-unclear generated images, audio and fonts
- A knowledge-graph server implementation
- Claims of current opening hours, prices, coordinates or travel time
- A second presentation UI

The existing game screenshots already communicate the visual result. A second
UI would add maintenance cost without making the workbench logic easier to
inspect. For a public technical portfolio, small contracts, runnable scripts
and visible review boundaries are more useful.

## How to read the demo

1. Read [the competition workbench map](competition-workbench-map.md) for the
   audited architecture and public substitutions.
2. Read [the compact architecture](architecture.md) for the public data
   contracts.
3. Inspect the JSON examples and follow their IDs.
4. Run the strict validator.
5. Generate a route draft and compare it with route.example.json.
6. Use the project skill in WorkBuddy or CodeBuddy to explain or extend the
   demo without inventing missing facts.

## Maturity statement

This is a **public teaching prototype**, not a hosted product. The included
scripts prove that the example contracts are internally consistent. They do
not prove that a cultural claim is historically definitive, that a live venue
is open, or that the original competition pipeline remains reproducible.
