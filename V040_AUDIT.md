# v0.4.0 — reaction-library expansion

Baseline:31 entries,69 events. Complete records are retained in audit/V040_BASELINE.json;
quantum binary/archive hashes are in audit/V040_QUANTUM_HASHES.json. No quantum calculation
is authorized or performed in this release.

The deduplicated inventory (content/v040/inventory.json) targets69 additions in
24/24/21-entry batches, yielding100 entries. Names/aliases are separate from entries;
reverse ester hydrolysis is not counted again as a new Fischer reaction. Existing
SN1 and aldol overlaps retain their identifiers. Proposed additions distinguish
functional transformations and consequential mechanistic variants, not reagent synonyms.

Existing architecture:build_data.py constructs the catalog; app/core/diagrams.js
render/search/filter events; v035_mechanisms.py authors mapped structural SVGs.
The codebook has eight inherited/candidate codes. Undefined surface, metal-redox,
SET and excited-state events must remain explicitly unassigned rather than receive
invented closed-shell codes. Every new event will retain its explanation and boundary.

Dependency constraint:the local RDKit install is unavailable. New diagrams use
original code-native condensed structural SVGs with explicit atom/bond arrow anchors,
formal charges and intermediate structures. They are teaching representations, not
computed geometries or a claim that grouped stages are verified elementary events.
External image reuse is unnecessary. External reference reachability must not be
claimed without a completed check. Bibliographic references and topic locators are
kept distinct from experimental proof of a particular microscopic mechanism.

Implementation, review results, final counts and remaining gaps are recorded below
only after the corresponding batch passes validation.

## Batch1 completed

24 new entries /84 listed events; catalog55 entries /153 events. Full npm regression
passed after adapting count/version assertions and map-pagination tests to the larger
catalog. Original31-record deep equality, codebook equality and quantum hashes pass.
Review corrected local arene charge/atom representations and an acetylide H anchor.
Representative mechanism review covered neighboring participation, E2 geometry,
boron oxidation/migration, mercury/radical limitations, surface hydrogenation,
alkyne tautomerization, EAS/SNAr and diazonium SET. Not every microscopic redox stage
is established; grouped stages and undefined SORG boundaries are explicit.
SVG XML/arrow inventories passed. A rasterized aromatic-step sample was inspected;
this is not a claim of full native/mobile browser testing. Actual log:
audit/V040_BATCH1_TESTS.log.
