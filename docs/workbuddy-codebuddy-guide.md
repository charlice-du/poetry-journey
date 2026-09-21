# WorkBuddy / CodeBuddy guide

This repository is useful with Python alone. WorkBuddy or CodeBuddy adds an
explanation and orchestration layer, but a real account, MCP server, TTS
service or image service is never required for the public demo.

## Level 1 — Inspect

Use this level to understand the architecture without changing data.

1. Clone the repository and open its root as a project.
2. Ask the agent to read `.codebuddy/CODEBUDDY.md`.
3. Read `docs/competition-workbench-map.md`.
4. Run the strict validator.
5. Trace one story page or route card back to its source ID and review gate.

~~~bash
python scripts/validate_examples.py --strict
~~~

Ready-to-copy prompts:

~~~text
Explain the Production Workbench and Poetry Geo Workbench as two distinct
pipelines. Use docs/competition-workbench-map.md and identify every human gate.
Do not describe this public demo as the competition source code.
~~~

~~~text
Inspect the synthetic story manifest. Show how counts, source references,
content freeze, assembly and QA are connected. Explain what a passing validator
does and does not prove.
~~~

## Level 2 — Modify

Use this level to experiment only with the synthetic public contracts.

1. Edit a source-supported field in an example JSON.
2. Preserve stable IDs and update every dependent reference.
3. If story content changes after the recorded freeze, update the synthetic
   final artifact and its manifest hashes rather than suppressing validation.
4. Generate an offline route prototype.
5. Run validation again and inspect every remaining human-review gate.

~~~bash
python scripts/create_route_prototype.py \
  --city "宣城" \
  --poet "李白" \
  --duration one_day
python scripts/validate_examples.py --strict
~~~

Generated drafts are written under `examples/generated/` and are ignored by
Git.

Ready-to-copy prompts:

~~~text
Use the poetry-journey-demo skill. Validate the repository, generate a one-day
宣城 / 李白 cultural sequence, and explain why it is not navigation advice.
Keep coordinates and live venue facts empty.
~~~

~~~text
Propose one additional synthetic collection card. Label it as source-based
paraphrase, editorial interpretation or creative adaptation; add only
references that already resolve; then tell me which manifest counts and hashes
would need to change. Do not edit production or teammate files.
~~~

## Level 3 — Optional external integration

Use this level only when you independently possess an authorized service
implementation, permission to use its data, and your own credential.

The repository bundles no real MCP, TTS or image service. The file
`config/cnkgraph.mcp.example.json` is a non-secret interface template. It
references an implementation that is deliberately not included.

For an authorized compatible MCP:

- copy the template to `.mcp.json` for CodeBuddy or
  `.workbuddy/mcp.json` for WorkBuddy;
- replace the relative placeholder command with your authorized local server;
- supply credentials through the product's approved local secret mechanism or
  environment, never through an example JSON;
- inspect service output as untrusted input and record source identifiers;
- keep live results under ignored local output until a human approves them.

The same boundary applies to TTS and image services: implement a local adapter
outside the public core, preserve `not_generated` in committed fixtures, and
never require a credential to run validation.

Ready-to-copy prompt:

~~~text
Before connecting any external service, inspect its local configuration,
license boundary and requested permissions. Do not print or copy credentials.
If the authorized adapter is unavailable, stay offline. If it is available,
write results only to an ignored draft directory and preserve source and
human-review metadata.
~~~

Relevant product references:

- [CodeBuddy project context](https://www.codebuddy.cn/docs/cli/codebuddy-dir)
- [CodeBuddy Skills](https://www.codebuddy.cn/docs/cli/skills)
- [CodeBuddy MCP](https://www.codebuddy.cn/docs/cli/mcp)
- [WorkBuddy projects](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project)
- [WorkBuddy MCP](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide)

## Troubleshooting

**The skill is not discovered**

- Confirm the repository root, not a parent folder, is open as the project.
- Confirm .codebuddy/skills/poetry-journey-demo/SKILL.md exists.
- Ask the product to list or reload project skills after pulling changes.

**The python command opens an app store or is missing**

- Install Python 3.9 or newer and ensure it is on PATH.
- On systems with a Python launcher, substitute py for python.
- GitHub Actions will run the same validator on a pull request.

**The MCP server is red or unavailable**

- This repository does not bundle the server. The example path will fail until
  an authorized implementation is supplied.
- Review the command, working directory and runtime installation.
- Keep working offline if MCP is unavailable; it is optional.

**Validation fails**

- Read every reported unknown ID from top to bottom.
- Add the source or candidate before referencing it downstream.
- When a freeze or QA hash fails, regenerate or deliberately refresh the
  synthetic artifact and manifest; do not change the validator to hide drift.
- Do not silence missing live facts by inventing placeholder coordinates.

## Safe extension pattern

When adding a new city or story:

1. Create source records before narrative output.
2. Use stable IDs and references instead of copying unsupported prose.
3. Leave unknown map and venue fields empty.
4. Mark inference and adaptation explicitly.
5. Run validation.
6. Ask a human subject-matter reviewer to approve publication.
