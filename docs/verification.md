# Verification guide

## What the validator checks

Run:

~~~bash
python scripts/validate_examples.py --strict
~~~

The validator uses only the Python standard library. It checks:

- all example JSON files parse;
- the GitHub Actions file passes a dependency-free structural check for the
  workflow YAML subset used here;
- required top-level fields and stable IDs exist;
- route stops reference known candidates;
- stops and cards preserve candidate and evidence-source lineage;
- the handbook contains every published stop ID;
- story pages, collection cards and media tasks resolve every source, character,
  page and card reference;
- story manifest counts match the current synthetic objects;
- the content-freeze digest matches the current story data;
- assembly records the same frozen story-input digest;
- assembly and QA both point to the current synthetic final artifact;
- intended public files contain no common absolute local paths or
  non-placeholder credential-like values;
- intended public files stay under the public-demo size limit;
- generated drafts remain under the ignored examples/generated/ directory.

GitHub Actions runs the same validation and also exercises route generation.
The generated CI route is passed back to the validator explicitly, so its
schema, query, candidate lineage, source lineage and review metadata are
checked rather than merely ignored as generated output.

## What the validator cannot prove

A green result means the repository's public contracts are internally
consistent. It does not establish:

- that a disputed historical event occurred exactly as narrated;
- that a quoted primary text proves the historicity of its scene;
- that a modern attraction is identical to an ancient location;
- that current opening hours, prices, coordinates or routes are correct;
- that an external model or MCP service will always return accurate material.

Those require source criticism, current authoritative data and human review.

## Earlier private-system checks

The private acceptance notes supplied for this repository reported that local
workbench flows, artifact generation and browser presentation had been
exercised before the public-demo work. That context motivated these contracts,
but the underlying team packages and raw reports are not published here.

Those earlier checks are not reproduced by this repository and should not be
treated as a current service-availability guarantee. The public verification
claim is narrower: the included examples parse, their references are
consistent, the offline generator runs, and the publication-hazard scan passes.

## Manual review checklist

- [ ] Each factual sentence has an appropriate source reference.
- [ ] Primary text, later commentary and modern tourism claims are separated.
- [ ] Adapted dialogue is labelled as adaptation.
- [ ] Uncertainty is visible to the reader rather than hidden.
- [ ] Rights for images, audio, fonts and quotations are documented.
- [ ] Live travel facts have been checked close to publication time.
- [ ] No key, token, personal path or private package is staged.

## Expected smoke test

The commands below should both exit with code 0:

~~~bash
python scripts/validate_examples.py --strict
python scripts/create_route_prototype.py --city "宣城" --poet "李白" --duration one_day
~~~

The generated route should contain only candidates already present in
candidates.example.json and should retain their review warnings.
