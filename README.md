# Poetry Journey (詩中行)

Poetry Journey is a browser-based interactive narrative game developed by a
three-person HKU team. The project received **2nd Prize at the Tencent “AI CAN
DO IT” Global Finals 2026**.

This repository now also contains a small, dependency-free public demo of the
team's workbench ideas. It shows how cultural-route research and story
production can be represented as inspectable data contracts, validated, and
explored with WorkBuddy or CodeBuddy.

> The public demo is a newly written, sanitized teaching prototype. It is not
> the competition production system, and it does not include teammates'
> unpublished packages, credentials, model outputs, or third-party services.

## What you can try

Two example pipelines are included:

1. **Poetry Route Workbench** — candidate places → evidence-marked route →
   cultural cards → handbook.
2. **Story Production Workbench** — cited sources → story pages and collection
   cards → content freeze → media plans → assembly and QA → human review gates.

The examples deliberately separate sourced facts, editorial interpretation,
creative adaptation, and claims that still need live verification.

### Quick start

Python 3.9 or newer is sufficient; there are no third-party dependencies.

~~~bash
python scripts/validate_examples.py --strict
python scripts/create_route_prototype.py --city "宣城" --poet "李白" --duration one_day
~~~

The second command creates an ignored draft under examples/generated/.
It is a cultural sequence, **not** a navigation route: coordinates, opening
hours, ticketing and travel times require current map or venue data.

## Use with WorkBuddy / CodeBuddy

Open this repository as a project, then ask:

~~~text
Explain the two public-demo pipelines and show where every output traces back
to evidence or a human-review gate.
~~~

~~~text
Use the poetry-journey-demo skill to validate the examples, then draft a
one-day 宣城 / 李白 cultural sequence. Do not invent map or venue facts.
~~~

Project guidance lives in [the CodeBuddy project context](.codebuddy/CODEBUDDY.md),
and the reusable project skill lives in
[the poetry-journey-demo skill](.codebuddy/skills/poetry-journey-demo/SKILL.md).
WorkBuddy can read the same project context. See the
[WorkBuddy / CodeBuddy guide](docs/workbuddy-codebuddy-guide.md) for setup and
the optional MCP template.

## Repository map

~~~text
.
├── .codebuddy/                   project context and reusable skill
├── .github/workflows/            validation in GitHub Actions
├── config/                       non-secret, disabled-by-default MCP template
├── docs/                         architecture, boundaries and usage
├── examples/
│   ├── poetry-route/             route pipeline example artifacts
│   └── story-production/         story pipeline example artifact
└── scripts/                      standard-library demo and validator
~~~

Start with:

- [Workbench overview](docs/workbench-overview.md)
- [Competition workbench map](docs/competition-workbench-map.md)
- [Architecture and data contracts](docs/architecture.md)
- [Verification guide](docs/verification.md)
- [Provenance and publication boundaries](docs/provenance-and-boundaries.md)

## Original project overview

The game combines classical Chinese poetry, interactive narrative, stylized
visual presentation, and AI-assisted experiences.

### My contributions

- Created the visual assets used in the preliminary round with generative image
  tools.
- For the Global Finals, researched and structured content/data for the team's
  Creative Workbench and helped establish its initial knowledge base.
- Contributed to the initial prototype and functionality of the Creative
  Workbench; additional features were later extended by the team lead.
- Participated in iterative testing, presentation preparation, and the final
  on-site showcase as part of the three-person team.

## Project showcase

### Game interface

<img width="1914" alt="Poetry Journey game interface" src="https://github.com/user-attachments/assets/a09c176f-c4c1-4178-be57-442a0ad8ec4c" />

Browser-based game interface and promotional visual for Poetry Journey.

### Global Finals

<img width="900" alt="Tencent AI CAN DO IT Global Finals" src="https://github.com/user-attachments/assets/56117440-2114-4d62-ac21-0bee50258a09" />

Team showcase at the Tencent “AI CAN DO IT” Global Finals in Shenzhen.

## Team and competition

Developed as a three-person team project.

- HK & Macau regional Top 10
- 2nd place at the regional roadshow
- 2nd Prize at the Global Finals

## Publication note

No repository-wide open-source license has been added. The public-demo files
are provided for inspection and portfolio demonstration; the original game,
team packages, media, external knowledge sources and service implementations
may have separate ownership or terms. See
[Provenance and publication boundaries](docs/provenance-and-boundaries.md)
before reusing material.

## Links

- [Play Online](https://poetryjourney.online)
- [Project Showcase](https://tch.cloud.tencent.com/works/307)
- [Competition Page](https://tch.cloud.tencent.com/contest/40)
