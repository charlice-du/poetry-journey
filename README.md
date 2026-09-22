# Poetry Journey (詩中行)

Poetry Journey is a browser-based interactive narrative game developed by a
three-person HKU team. It received **2nd Prize at the Tencent “AI CAN DO IT”
Global Finals 2026**.

[Play Online](https://poetryjourney.online) ·
[Project Showcase](https://tch.cloud.tencent.com/works/307)

<img width="1914" alt="Poetry Journey game interface" src="https://github.com/user-attachments/assets/a09c176f-c4c1-4178-be57-442a0ad8ec4c" />

## About the project

The game lets players explore classical Chinese poetry through the lives and
stories of different poets, using maps, narrative events and interactive
characters.

### My contributions

- Created the visual assets used in the preliminary round with generative image
  tools.
- For the Global Finals, researched and structured content for the team's
  Creative Workbench and helped build its initial prototype. Later features
  were extended by the team lead.
- Helped test the project, prepare the presentation and present it on-site as
  part of the three-person team.

## Technical demo

For the Global Finals, the team also developed two reusable workbench ideas:
one for producing interactive stories and another for researching
poetry-based cultural routes. This repository includes a lightweight public
version of those workflows, built from synthetic examples and a few validation
scripts.

The original competition workbenches contain team-owned code and production
assets, so this repository uses simplified examples rather than publishing the
full internal system.

### What you can try

1. **Poetry Route Workbench** — candidate places → evidence-linked route →
   cultural cards → handbook.
2. **Story Production Workbench** — source material → story pages and cards →
   image and audio planning → assembled output → QA.

The examples also show which parts come directly from sources, which are
interpretation or creative adaptation, and which still need manual review.

### Quick start

Python 3.9 or newer is sufficient; there are no third-party dependencies.

~~~bash
python scripts/validate_examples.py --strict
python scripts/create_route_prototype.py --city "宣城" --poet "李白" --duration one_day
~~~

The second command writes a draft to `examples/generated/`. It creates a
cultural sequence rather than turn-by-turn travel guidance; current venue and
map information is left for separate review.

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

The repository includes project-level CodeBuddy guidance and a reusable demo
skill; WorkBuddy can read the same project context. See the
[WorkBuddy / CodeBuddy guide](docs/workbuddy-codebuddy-guide.md) for setup and
optional MCP integration.

## Architecture and documentation

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

- [Workbench overview](docs/workbench-overview.md) — what the two workbenches do
- [Competition workbench map](docs/competition-workbench-map.md) — architecture
  and the mapping from the team workflow to the public examples
- [WorkBuddy / CodeBuddy guide](docs/workbuddy-codebuddy-guide.md) — how to try
  the demo

## Competition

<img width="900" alt="Tencent AI CAN DO IT Global Finals" src="https://github.com/user-attachments/assets/56117440-2114-4d62-ac21-0bee50258a09" />

Team showcase at the Tencent “AI CAN DO IT” Global Finals in Shenzhen.

- HK & Macau regional Top 10
- 2nd place at the regional roadshow
- 2nd Prize at the Global Finals
- [Competition Page](https://tch.cloud.tencent.com/contest/40)

## Publication note

This repository is shared for portfolio and demonstration purposes and does not
currently carry a repository-wide open-source license. See
[Provenance and publication boundaries](docs/provenance-and-boundaries.md) for
details on team-owned and third-party material.
