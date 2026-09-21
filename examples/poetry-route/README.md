# Poetry Route example

This folder demonstrates a traceable sequence:

1. candidates.example.json records cultural candidates, sources and uncertainty;
2. route.example.json selects candidates by ID;
3. cards.example.json links interpretation back to stops and sources;
4. handbook.example.md exposes the same stop and source IDs to the reader.

Run the validator from the repository root:

~~~bash
python scripts/validate_examples.py --strict
~~~

Generate a fresh deterministic draft:

~~~bash
python scripts/create_route_prototype.py --city "宣城" --poet "李白" --duration one_day
~~~

The generator does not call AI, maps or the internet. It cannot produce a
safe navigation itinerary. Its purpose is to make the artifact contract
concrete and testable.
