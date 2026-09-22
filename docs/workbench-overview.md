# Workbench overview

For the Global Finals, the team built two related workbenches:

- the **Story Production Workbench**, which turns source material into an
  interactive story through writing, image and voice planning, assembly and
  review;
- the **Poetry Route Workbench**, which researches the relationship between
  poets, poems and places before producing cultural routes and learning
  material.

Because the original packages include team code, generated media, local
configuration and external services, they are not published here. Instead,
this repository recreates the main workflow with small synthetic examples and
standalone Python scripts.

## What is included

| Area | Public artifact | What it demonstrates |
| --- | --- | --- |
| Route research | `candidates.example.json` | Each candidate records its evidence, confidence and review status |
| Route synthesis | `route.example.json` | A route references candidates instead of duplicating claims |
| Learning content | `cards.example.json` and `handbook.example.md` | Downstream outputs remain traceable to stops and sources |
| Story production | Story data, manifest and synthetic final HTML | Pages, cards, media plans, freeze, assembly and QA remain inspectable |
| Validation | `scripts/validate_examples.py` | Cross-file identifiers and common publication mistakes are checked |
| Small runnable demo | `scripts/create_route_prototype.py` | A deterministic offline draft can be generated from the examples |
| Agent guidance | `.codebuddy/` | Provides project context and instructions for WorkBuddy and CodeBuddy |

## What is not included

- Teammates' production source packages and internal prompt libraries
- API keys, tokens, local absolute paths and machine-specific launch scripts
- Licensed or ownership-unclear generated images, audio and fonts
- A knowledge-graph server implementation
- Claims of current opening hours, prices, coordinates or travel time

## How to read the demo

1. Start with [the competition workbench map](competition-workbench-map.md) for
   the two workflows and their public equivalents.
2. Use [the compact architecture](architecture.md) for the data contracts, then
   inspect the JSON examples and follow their IDs across stages.
3. Run the strict validator and route generator, then compare the generated
   draft with `route.example.json`.
4. Optionally open the project in WorkBuddy or CodeBuddy to explain or extend
   the examples.

## Maturity statement

This demo focuses on workflow structure rather than reproducing the full
competition system. The validator checks the consistency of the example data;
historical interpretation and live venue information still require separate
review.
