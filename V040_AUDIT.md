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

## Batch2 completed

24 further entries /106 events; catalog79 entries /259 events. Full regression and
new integrity checks pass. Review corrected oxime/hydrazone nitrogen proton
inventories, distinguished iminium pi* from carbonyl pi*, and made Wittig/Swern
key bond-change arrows explicit. Ester aminolysis, saponification, DIBAL versus
LAH endpoints, selective NaBH4 reduction, chromate redox limitations, Claisen
product trapping and Michael/Robinson bond origins were checked at teaching-model
resolution. Actual log:audit/V040_BATCH2_TESTS.log. No new quantum data were created.

## Batch 3 completed

21 further entries / 79 listed stages bring the catalog to **100 reactions / 338
listed stages**, including 69 additions / 269 new stages. New coverage includes
six rearrangements, Cope/ene/dipolar/photochemical/electrocyclic transformations,
radical chains and cyclization, and four palladium-catalyzed couplings. The source
inventory gives every stable new ID and excluded aliases.

The final review also added representative substrate/product connectivity graphs
to all 69 new full mechanism sheets. A strict, deliberately limited SMILES reader
checks their graph syntax, ring closure and valence maxima. This is a connectivity
and drawing tool, not a conformer or electronic-structure calculation. Relative
E/Z drawing constraints are explicit for the selected reduction/olefination cases.
Condensed intermediate structures, formal charges, bond arrows and fishhooks
remain the event diagrams; grouped surface/metal/solvent stages use process arrows.

Editorial review corrected nitrogen proton inventories, SNAr/arene structures,
the ozone resonance form, peracid's five-arrow relay, benzyne ring accounting,
acetoacetate electrophile atom, and peroxide initiation. Photochemical cycloaddition
uses an enone triplet model, with separate excitation/spin conversion boundaries.
The scope is textbook teaching accuracy, not an independent experimental review.

## Coverage and deduplication

Families are navigation groups, named reactions are names/aliases, and entries
are scoped synthetic operations. Stages can be elementary models or explicitly
grouped processes. Neither resonance contributors nor individual directing-effect
positions count as entries. Existing SN1 and aldol overlaps remain preserved.
Acetal formation/hydrolysis is one reversible entry; acid ester hydrolysis is not
a new reverse-Fischer entry. PCC and Swern share an overall transformation but
retain distinct chromate-ester versus activated-sulfonium/ylide mechanisms.
Dieckmann is explicitly the ring-forming intramolecular Claisen variant.
Lindlar versus full hydrogenation and dissolving-metal reduction teach different
selectivity/physical mechanisms; simple borohydride reduction was not duplicated.
Automated normalized-name/alias collision checks complement this manual inventory;
no algorithm is claimed to prove that all possible chemical synonyms are absent.

| Family | Original | Added | Final |
|---|---:|---:|---:|
| Acid–base reactions | 2 | 0 | 2 |
| Alkene reactions | 4 | 5 | 9 |
| Alkyne reactions | 0 | 5 | 5 |
| Aromatic substitution | 1 | 7 | 8 |
| Carbonyl reactions | 9 | 6 | 15 |
| Carbon–carbon bond formation | 0 | 3 | 3 |
| Carboxylic acid derivatives | 0 | 6 | 6 |
| Elimination reactions | 3 | 2 | 5 |
| Enolate reactions | 0 | 6 | 6 |
| Organometallic reactions | 0 | 4 | 4 |
| Oxidation and reduction | 0 | 9 | 9 |
| Pericyclic reactions | 3 | 5 | 8 |
| Radical reactions | 3 | 3 | 6 |
| Rearrangements | 0 | 6 | 6 |
| Substitution reactions | 6 | 2 | 8 |

New entries by batch (accepted alternative names are stored as aliases, not IDs):

1. Neighboring sulfur participation (`neighboring-sulfur`); Hofmann elimination (`hofmann-elimination`); Acid-catalyzed alcohol dehydration (`alcohol-dehydration`); Alcohol tosylation (`tosylation`); Alkene hydroboration–oxidation (`hydroboration-oxidation`); Oxymercuration–demercuration (`oxymercuration`); Catalytic alkene hydrogenation (`catalytic-hydrogenation`); Peracid epoxidation (`peracid-epoxidation`); Osmium-catalyzed syn dihydroxylation (`syn-dihydroxylation`); Reductive ozonolysis (`ozonolysis`); Permanganate oxidative alkene cleavage (`oxidative-alkene-cleavage`); Mercury-catalyzed alkyne hydration (`alkyne-hydration`); Alkyne hydroboration–oxidation (`alkyne-hydroboration`); Lindlar partial alkyne hydrogenation (`lindlar-reduction`); Dissolving-metal alkyne reduction (`dissolving-metal-reduction`); Acetylide alkylation (`acetylide-alkylation`); Electrophilic aromatic bromination (`aromatic-bromination`); Aromatic sulfonation (`aromatic-sulfonation`); Friedel–Crafts alkylation (`friedel-crafts-alkylation`); Friedel–Crafts acylation (`friedel-crafts-acylation`); Activated nucleophilic aromatic substitution (`snar-addition-elimination`); Benzyne elimination–addition substitution (`benzyne-substitution`); Benzylic side-chain oxidation (`benzylic-oxidation`); Sandmeyer chlorination (`sandmeyer`).

2. Enamine formation (`enamine-formation`); Acetal formation and hydrolysis (`acetal-equilibrium`); Oxime formation (`oxime-formation`); Hydrazone formation (`hydrazone-formation`); Reductive amination (`reductive-amination`); Wittig olefination (`wittig`); Horner–Wadsworth–Emmons olefination (`horner-wadsworth-emmons`); Benzoin condensation (`benzoin`); Cannizzaro disproportionation (`cannizzaro`); Ester saponification (`ester-saponification`); Acid-catalyzed amide hydrolysis (`amide-hydrolysis`); Ester aminolysis (`ester-aminolysis`); Base-catalyzed transesterification (`transesterification`); Carboxylic acid conversion to acyl chloride (`acyl-chloride-formation`); Anhydride alcoholysis (`anhydride-alcoholysis`); DIBAL-H partial ester reduction (`dibal-ester-reduction`); Chemoselective borohydride ketone reduction (`selective-borohydride`); Lithium aluminum hydride ester reduction (`ester-lah-reduction`); PCC alcohol oxidation (`pcc-oxidation`); Jones oxidation of a primary alcohol (`jones-oxidation`); Swern oxidation (`swern-oxidation`); Claisen ester condensation (`claisen-condensation`); Michael conjugate addition (`michael-addition`); Robinson annulation (`robinson-annulation`).

3. Dieckmann cyclization (`dieckmann`); Malonic ester synthesis (`malonic-ester-synthesis`); Acetoacetic ester synthesis (`acetoacetic-ester-synthesis`); Pinacol rearrangement (`pinacol`); Beckmann rearrangement (`beckmann`); Baeyer–Villiger oxidation (`baeyer-villiger`); Wagner–Meerwein skeletal rearrangement (`wagner-meerwein`); Hofmann amide rearrangement (`hofmann-rearrangement`); Curtius rearrangement (`curtius`); Cope rearrangement (`cope-rearrangement`); Carbonyl–ene reaction (`ene-reaction`); Nitrone 1,3-dipolar cycloaddition (`dipolar-cycloaddition`); Triplet-sensitized enone [2+2] cycloaddition (`photochemical-cycloaddition`); Thermal 6π electrocyclic closure (`six-pi-electrocyclization`); Peroxide-initiated radical HBr addition (`radical-hbr`); NBS allylic bromination (`nbs-bromination`); 5-Hexenyl radical cyclization (`radical-cyclization`); Suzuki–Miyaura coupling (`suzuki-miyaura`); Mizoroki–Heck coupling (`heck`); Sonogashira coupling (`sonogashira`); Negishi coupling (`negishi`).

## SORG and evidence boundaries

The eight-code project codebook and all four axes are unchanged. Of 269 new
stages, 186 receive existing codes and **83 remain unassigned** with explicit
boundaries. These 83 are marked grouped/model stages; the overall 338 count is
not a claim of 338 uniquely established elementary transitions. Undefined SET,
excited-state/spin conversion, surface and metal-redox/transmetalation processes
are not forced into closed-shell nucleophile/electrophile labels. Unassigned
stages display that status in cards, dialogs, sources and the laboratory event
selector; map edges do not equate two missing codes.

1113 extensions to iminium addition, 1122 substitutions at sulfur/bromine, and
1133 polar migrations remain candidate interpretations, with alternatives in
notes where relevant. Concerted pericyclic events use 1333 without invented
intermediates. Symmetry allowance does not prove strict synchronicity, rates,
quantitative orbital interaction energies, or IRC connectivity. The retained
Diels–Alder 1333 assignment and incomplete-IRC status are unchanged.

## Representative scientific review

| Area | Representative review and scoped conclusion |
|---|---|
| Substitution/elimination | Episulfonium formation/opening and carbon inversion; ammonium beta elimination and anti alignment; O-tosylation retains the alcohol C–O bond. Sulfur substitution timing is not fixed universally. |
| Alkene/alkyne | Boron migration/oxidation, mercurinium anti opening versus nonstereospecific demercuration, peracid oxygen transfer, Criegee sequence, enol tautomerization, Z surface versus E SET reduction. Metal oxide/surface microscopic details remain grouped. |
| Aromatic | Arenium rearomatization, nitro-activated Meisenheimer model versus aryne elimination/addition, directing effects and acylation limitations; Sandmeyer copper/radical redox boundaries. Concerted SNAr alternatives are acknowledged. |
| Carbonyl | N proton counts in oxime/hydrazone/enamine formation; reversible acetal proton inventory; iminium hydride transfer; Wittig oxaphosphetane versus condition-dependent betaine routes; cyanide umpolung. |
| Acyl substitution | Addition/collapse/proton transfers for saponification, amide hydrolysis, aminolysis and exchange; acid ammonium endpoint; SOCl2 activation model excludes the different DMF-mediated route. |
| Enolates/C–C | Claisen product trapping, Dieckmann ring size, malonate/beta-keto-acid decarboxylation, Michael 1,4 addition and Robinson cascade. Competing alkylation/elimination and self-condensation are stated. |
| Redox | Cold DIBAL versus LAH endpoints; bifunctional NaBH4 chemoselectivity; chromate versus Swern sulfur-ylide chemistry. No invented isolated hydride or unique chromate redox sequence. |
| Rearrangements | Pinacol/Wagner sigma migration, anti Beckmann migration, Criegee Baeyer–Villiger model, amide/azide-to-isocyanate migration without obligatory free nitrenes. |
| Pericyclic/radical | Cope six-center topology, ene H transfer, nitrone dipole closure, thermal 6pi disrotation; photochemical enone triplet model; HBr propagation, allylic resonance and 5-exo radical closure with fishhooks. |
| Organometallic | Oxidative addition, transmetalation, reductive elimination and Heck insertion/beta-H geometry. Sonogashira uses Cu-assisted activation rather than claiming amine alone makes free acetylide; catalyst speciation/resting states remain model dependent. |

## References, graphics and limitations

Each addition has a bibliography key and a topic locator displayed in Sources.
The new bibliography uses McMurry, *Organic Chemistry* (OpenStax, 2023);
Clayden/Greeves/Warren, 2nd ed. (2012); Hartwig (2010); the Nobel 2010 scientific
background for Heck/Negishi/Suzuki; and Chinchilla/Nájera, Chem. Rev. 107 (2007),
874–922, DOI 10.1021/cr050992x for Sonogashira. No invented page numbers, measured
selectivities or computed values are supplied. References support chemistry,
not SORG. The unused Hartwig bibliography entry is retained as further background.
Live external HTTP reachability was not verified in this run; `checked: null`
preserves that distinction. Textbook topic locators are not purported primary
experimental evidence for a unique microscopic pathway.

All new SVGs are original authored illustrations with declared attribution and
license; no external mechanism image was copied. Full sheets include molecular
connectivity graphs plus the event sequence. Condensed formula drawings are not
fully atom-mapped molecular simulations. Some proton relays and complex work-up
steps have text-specified bond changes instead of every microscopic curved arrow;
metal/surface process arrows intentionally make no unique electron-arrow claim.
No new numerical quantum fields or interpolated electronic data were generated.

## Verification and reproducibility

- Baseline snapshot: `audit/V040_BASELINE.json` records all 31 original reactions,
  69 stages, original assignments and sources. Deep equality protects reaction
  objects and the SORG codebook.
- `audit/V040_QUANTUM_HASHES.json` hashes 180 **previously published** binary
  scientific assets/archives identified from the v0.3.7-r4 remote tree. Local
  unpacked scratch copies are excluded; original r2 numerical regression checks
  additionally protect 373 existing scientific payloads. No protected asset changed.
- `verify-v040.py` checks the exact inventory, IDs/names/aliases, required fields,
  source keys/HTTPS references, assignments or declared boundaries, all event/full
  SVG paths/XML/arrow inventories, representative graph syntax/valence, English
  additions, local index asset links, baseline equality and scientific hashes.
  The source ZIP is generated after tests and checked separately by packaging.
- Existing regression checks retain foundations, orbitals, event filters, every
  reaction dialog/event/tab, search/family navigation, map pagination, deep links,
  saved state, error paths, SN2, carbonyl and Diels–Alder scientific/lab checks.
  Fixed 31/69 assertions now apply to the preserved original subset; new totals
  have separate assertions. Sources/alias display and unassigned handling have
  additional DOM checks. These tests are structural/numerical archive checks,
  not new quantum calculations or experimental mechanism proof.
- All **338 new SVG files** (269 stages + 69 full sheets) successfully rasterized
  with Sharp. Representative aromatic, oxime, pinacol, Lindlar, Suzuki, Heck,
  ozone and peracid raster outputs were visually inspected. This does not prove
  every drawing's stereochemistry or every mobile layout.
- Native Chromium launch was attempted and failed before page load because the
  sandbox denied Crashpad `setsockopt` (Operation not permitted). Native desktop,
  mobile touch, CSS layout and published-site WebGL interaction are **not tested**
  in this environment. jsdom DOM coverage is reported separately.

Rebuild only the expansion without chemical drawing dependencies:

```sh
python3 build_v040.py --batches 3
npm ci --ignore-scripts
npm test
python3 package_source.py
```

For the complete existing pipeline use `python3 build_data.py`,
`python3 build_reaction_systems.py`, and `python3 build_research.py` before tests.
The existing CI installs its pinned RDKit dependency for the legacy drawings;
new SVG generation uses only Python's standard library. No quantum script should
be rerun for this release. `--batches 1` or `2` supports review of earlier
milestones; the release integrity checker intentionally requires all three.

## Remaining gaps and release status

Coverage is substantially broader, not an exhaustive encyclopedia. Future work
includes sulfur/nitrogen functional-group breadth, explicit protecting-group
networks, more heteroaromatics, asymmetric catalysis, organometallic speciation,
more primary-source-specific microscopic evidence, and independent chemistry
review. Existing withheld legacy reference images remain preserved rather than
silently replaced. Live source reachability and native desktop/mobile review
remain outstanding. The Diels–Alder IRC investigation is not resumed in v0.4.0.

All three authored batches are implemented. Release checks and deployment evidence
are recorded below after completion; no pending job is described as running after
this task ends.

## Completed release checks

`npm test` completed with exit 0 after the final content/renderer changes, including
1,107 parameterized DOM cases and all retained scientific archive regressions.
The exact output is in `audit/V040_FINAL_TESTS.log`; batch logs are retained too.
Python compilation, JavaScript syntax and `git diff --check` pass. All new SVGs
rasterized successfully. Source archive construction and remote deployment are
recorded separately below when confirmed.
