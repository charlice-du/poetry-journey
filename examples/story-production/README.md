# Story Production example

This folder is a fully synthetic, compact representation of the production
contract:

- `story_data.example.json` contains two source records, three story pages,
  two collection cards, four media-plan tasks and four human-review gates;
- `story_manifest.example.json` records expected counts, the content-freeze
  fingerprint, assembly state and QA fingerprint;
- `final.example.html` is a small self-contained artifact used to prove that
  the manifest and QA record point to the current output.

The source data keeps received text, modern interpretation, creative staging
and future media work in separate fields.

The example intentionally contains no generated image or audio. Media entries
are plans with status `not_generated`, so a reader cannot mistake a missing
asset for a completed deliverable. The HTML is not a replacement production
UI; it is a deterministic QA target for the public contract.

Useful review questions:

- Which source supports each page?
- Is the page a paraphrase, interpretation or adaptation?
- Does a textual passage establish historicity, or only what the text says?
- Who must approve the historical framing and media rights?
- Does the content-freeze hash still match the current story data?
- Does QA describe the same final artifact that is in this folder?
