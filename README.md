# SORG · Organic Reaction Atlas

A responsive, English-language teaching atlas of organic reaction mechanisms. The published site contains 31 reaction entries and 69 listed mechanistic events (including three explicitly grouped stages).

Each reaction panel presents the stated substrate, reagents, scoped sequential equations and intermediates, specific electron-flow prose, orbital and geometry notes, a reviewed credited image or explicit pending-illustration notice, and source and scope information. Reference images have separate exact/representative/partial/pending match and coverage fields. Images with unconfirmed reuse permission are withheld while their source and attribution remain recorded. Four original SVGs replace broken or unsuitable references. Solvent-mediated proton relays may be grouped as net teaching events. The in-page SVGs show local motifs, whereas the step sequence describes the named example.

Search, same-event S/O/R/G filters, saved items, and deep links such as `#reaction/sn2` work in the browser. Every reaction has an electronic-structure section that distinguishes proposed observables from literature findings and missing calculations.

Current release work: v0.3.7 adds a reproducible butadiene + ethylene Diels–Alder electronic-structure case alongside the retained SN2 and carbonyl cases. See [V037_AUDIT.md](V037_AUDIT.md) and [reproduction instructions](research/diels-alder/README.md) for actual calculations and limitations. The [r1 verification follow-up](V037_FOLLOWUP_AUDIT.md) replaces the initially partially relaxed 1.9 Å point with an independently checked constrained geometry and regenerated electronic fields. Earlier release notes below describe their historical scope.

The [r2 scientific validation audit](V037_R2_AUDIT.md) records newly checkpointed bidirectional IRC attempts, independent endpoint/path checks and targeted method diagnostics. The v0.3.7-r2 report records a failed product-endpoint minimum check and interruption of remaining computations; the laboratory retains the original constrained series and exposes the interruption and verified source records. A “Validated IRC” series requires separate path, endpoint and electronic-field verification.

## Classification and evidence

SORG is a provisional project teaching index, not an IUPAC taxonomy or a validated quantum-mechanical invariant. A code belongs to one mechanistic event. Different events and named reactions can share a code, and the four axes describe related aspects rather than independent physical properties.

| Axis | Values | Boundary |
|---|---|---|
| S: electronic state | 1 paired; 2 open shell; 3 excited/state change | Describes participants in an event, not necessarily its final product. |
| O: principal orbital interaction | 1 donor–acceptor; 2 singly occupied; 3 cyclic concerted; 4 electron-transfer coupling | Requires a declared orbital basis and subspace convention; it is not an invariant orbital count. |
| R: prominent bond reorganization | 1 formation/cleavage; 2 replacement; 3 multiple-bond redistribution; 4 electron transfer | A label for prominent change, not a full bond-change inventory or absolute bond-order threshold. |
| G: nuclear geometry | 1 approach/separation; 2 approach/departure; 3 collective rearrangement | Coarse geometric grouping; some boundaries remain candidates. |

Codes `1111`, `1122`, `2211`, and `1333` are inherited from the project's prior teaching convention. `1113`, `1133`, and `2222` are candidates. “Inherited” does not mean experimentally established. A prior two-component toy basis-rotation check changed a participation ratio from about 2 to 1; it demonstrates representation dependence, **not** an ab initio calculation for SN2, Diels–Alder, or any entry. The proposed S/O/R/G assignment needs explicit conventions and further validation.

The SN2 entry transcribes published gas-phase σ* energies and activation-strain interaction energies for a defined model series. The Diels–Alder entry transcribes published fragment EDA, orbital overlap, and electron-transfer analysis for butadiene plus neutral or ionized acrolein. All numbers have a named substrate, method, geometry, table or figure, and source. The SN2 model uses `Cl⁻ + A–Cl`, including `Cl⁻ + CH₃Cl`, whereas the teaching card uses `HO⁻ + CH₃Br`; numerical results cannot be transferred to it. The Diels–Alder numerical comparison uses acrolein, whereas the teaching mechanism uses ethene. Other entries distinguish literature conclusions from proposed measurements. Published model findings now cover microsolvated SN2/E2 competition, the solvation-sensitive SN1/SN2 boundary, the carbonyl attack trajectory, the parent Claisen rearrangement's electron-density evolution, and benzene nitration in solvent. Each is attached to a card with its actual calculated model, method, primary source and transfer limit. All 31 reaction cards contain a reaction-family-specific proposed protocol; these protocols have not been executed. EDA orbital stabilization, overlap, and transferred charge must not be relabeled as a single invariant coupling matrix element. A useful coupling value must define donor/acceptor fragments, diabatic states, electronic state, geometry, method, and basis. Reaction rates are not calculated. Independently Atlas-computed model systems are now supplied in the Reaction Orbital Laboratory, with their own methods, outputs and limitations; they are separate from the retained published literature evidence.

The site's computational workflow explains model definition, conformer and solvent choices, stationary-point optimization, frequency and IRC validation, higher-level checks, activation-strain/EDA, ELF and charge/spin/bond-order analyses, and how a diabatic coupling differs from orbital overlap. Specific methods in literature records describe what the cited authors actually used; the card protocols describe what to calculate next and do not assert that a DFT or CCSD(T) run has been performed for the teaching substrate.

## Run and edit

Open `dist/index.html` in a modern browser, or serve it locally:

```sh
python3 -m http.server 8000 --directory dist
```

The app and structured data load locally. Embedded mechanism images and cited sources use external URLs and need network access. Saved items stay in browser storage.

`build_data.py` defines the original entries and classifications; `english_content.py` contains the specific English editorial text for each event; `quantum_literature.py` holds literature tables and their scope notes. `qc_review.py` applies the documented v0.2.6 corrections and review metadata; `v028_content.py` adds reaction-specific scientific copy without changing numeric codes. `build_figures.py` generates the four earlier SVGs, and `v028_figures.py` generates the five new mechanism sheets. The separate `dist/learning.js` holds four guided exercises, explicitly curated event features, optional nonnumeric descriptors, and three evidence narratives; it does not alter reaction records. See `AUDIT.md` and `audit/` for all 70 original event dispositions, figure reviews and link requests. Change the relevant files, then regenerate and validate:

```sh
python3 build_data.py
npm ci --ignore-scripts
npm test
python3 package_source.py
node --check dist/app.js
node --check dist/learning.js
node --check dist/diagrams.js
```

The build produces both `dist/data.json` and `dist/data.js`; keep them synchronized. The source archive is `dist/sorg-atlas-source.zip`.

The GitHub Actions workflow in `.github/workflows/pages.yml` publishes `dist/` to GitHub Pages on pushes to `main` or `master` and manual dispatch. Relative URLs support project Pages hosting.

## Sources and limits

Each reaction links its chemistry references. They support the mechanism and chemistry, not the SORG assignment. The cited OpenStax textbook is John McMurry, *Organic Chemistry* (2023); other entries refer to Chemistry LibreTexts or credited image publishers. The credited online images remain subject to their own source terms. Educational text in the app states CC BY-NC-SA 4.0; inspect each source page for image rights.

The previous generic energy sketch was removed because a listed stage does not establish a transition-state count or relative energy. The work-up and solvent-relay descriptions define the scope of their pathway. Complex reaction networks, metal aggregation equilibria, and explicit solvent trajectories are not fully modeled.

## v0.2.7 quality-control release

All 31 entry IDs and the seven codebook definitions are preserved. The acid-promoted epoxide entry now has two valid events: the former third event followed an atom/charge-inconsistent oxonium. The inventory therefore changes from 70 to 69 listed events without adding or deleting a reaction. Read [the complete audit](AUDIT.md) for remaining scientific uncertainty and image gaps.

`npm test` runs structural and DOM integration checks using jsdom. It does not test CSS rendering, mobile touch, native dialog behavior, network image loading or real-browser console errors. Those checks remain untested in this session because the managed environment did not expose the supported control-browser skill. No quantum-chemical calculations were performed.

## v0.2.8 content and comparison release

For the newer event-focused comparison, navigation, clarified candidate-code boundaries and published-value visualizations, see [V029_AUDIT.md](V029_AUDIT.md).

The atlas now embeds original, equation-matched mechanisms for E2, Diels–Alder, generic carbonyl addition, Fischer esterification, and acetone/methylamine imine formation. The five new illustrations have an event-by-event visual and charge audit in [V028_AUDIT.md](V028_AUDIT.md). Seventeen reviewed figures are embedded; 14 remain withheld pending further image and permissions work.

The “Same code, different chemistry” interface compares two events from different reactions with the same SORG code. It shows the common coding convention alongside each equation, electron flow, orbital interaction, geometry, and uncertainty. Codes 1133 and 1113 remain provisional where the audited codebook examples do not cover every use.

Published numerical cases on SN2 and Diels–Alder and the CN⁻/acetone angle study are identified by their actual models and methods; no quantum-chemical calculations were performed by this project. The test suite covers comparison selection and the earlier atlas interactions. Real desktop/mobile browser layout, native dialogs, touch, network image loads, and browser console remain untested in this managed environment.

## v0.3.0 reasoning release

The guided mode asks five reaction-specific questions each for SN2, E2, carbonyl nucleophilic addition, and neutral Diels–Alder. Incorrect options explain the mechanistic distinction. The event-centered map makes all 69 listed stages selectable; a solid edge means an identical four-digit code, while a dashed edge requires membership in an explicitly described feature group. Its local view pages through large neighborhoods and does not infer similarity from one coincident digit. A node can open its existing step-specific modal route.

The three case-study narratives link the already transcribed SN2, Diels–Alder and CN⁻/acetone evidence to geometry and classification limits. Source tables, model/method statements and transfer warnings remain authoritative. Optional descriptors name selected stereoelectronic or topological features without changing SORG digits. See [V030_AUDIT.md](V030_AUDIT.md) for this release's verification and limitations.

## v0.3.1 quantum-chemistry foundation

The new [Research & Methods](research/README.md) layer defines a versioned evidence schema, a primary-source transcription for gas-phase Cl⁻ + CH₃Cl, and a discrete three-state viewer. It deliberately does not reconstruct Cartesian coordinates or an IRC from partial tables. The teaching SN2 entry remains HO⁻ + CH₃Br; numerical quantities are labeled by their actual Cl⁻/CH₃Cl model, units, methods, fragment convention and table location. Optional descriptor definitions are separate from 1122. A Psi4 seed workflow is included but was **not executed** and does not validate a transition state. See [V031_AUDIT.md](V031_AUDIT.md) for provenance, checks and missing quantities.

## v0.3.2 learning layer

Quantum Foundations now comes before the SORG codebook: five linked lessons with native MathML and three original analytic visual models. `dist/foundations.js` contains the explicitly illustrative two-state Hamiltonian, normalized one-dimensional density, and double-well PES; `verify-foundations.cjs` checks their analytical identities. The SN2 research viewer adds an unconnected published-energy point chart, not an IRC. See [V032_AUDIT.md](V032_AUDIT.md) for assumptions, provenance, tests and limitations.

## v0.3.3 molecular laboratory

The Orbital Laboratory follows Quantum Foundations and uses seven newly **calculated** fixed-geometry RHF/STO-3G orbitals for H₂, ethylene and formaldehyde. Three.js renders the sampled signed wavefunction isosurfaces; downloadable cube grids, geometry inputs, MO coefficients, SCF logs and the regeneration script accompany them. The browser retains a static projection from the computed mesh if WebGL is unavailable. The separate scalar SCF iteration widget is an explicitly defined mathematical teaching model, not a molecular calculation. See [research/orbitals/README.md](research/orbitals/README.md) and [V033_AUDIT.md](V033_AUDIT.md).

## v0.3.4 orbital diversity and evolution

The laboratory adds open-shell allyl SOMO/spin density, all six benzene π orbitals, all four s-trans-butadiene π orbitals, and five independently calculated ethylene torsion frames. Inputs, outputs and coefficients are downloadable. See [V034_AUDIT.md](V034_AUDIT.md) for exact methods, identity/phase tracking, validation and the outstanding native WebGL/mobile tests. No reactions or SORG categories were added.

## v0.3.5 Reaction Orbital Laboratory

One selected event now connects conventional mechanisms to a separate calculated chloride SN2 case: five RHF/6-31+G(d) constrained geometries, a Hessian-verified central first-order saddle, canonical MO tracking, total density, same-grid density differences and same-geometry fragment deformation density. It is not an IRC. See [V035_AUDIT.md](V035_AUDIT.md) and the [31-reaction/69-event illustration inventory](audit/V035_MECHANISM_INVENTORY.md). Forty-four original catalog event SVGs improve complete teaching coverage to 29 entries; LAH remains partial and Grignard representative. New structural illustration regeneration requires `rdkit==2026.9.1`; existing numerical data and taxonomy are retained.

## v0.3.6 — Carbonyl reaction electronic structure

The Reaction Orbital Laboratory now selects independently calculated SN2 and
H− + formaldehyde systems using schema-2 records. Seven new carbonyl geometries
include a Hessian-verified methoxide minimum and a matched-distance three-angle
comparison. Actual orbitals, total/difference/deformation densities, two bond-index
conventions and pyramidalization stay synchronized. Original 31 reactions / 69
events, candidate carbonyl 1113 and all original quantum datasets are preserved.

Important: bare hydride is not bound against detachment at this HF level. The
public UI labels this finite-basis restricted addition branch explicitly; it is
not an IRC or verified physical gas-phase ground-state path. See [V036_AUDIT.md](V036_AUDIT.md),
[reproduction instructions](research/carbonyl/README.md), and [schema](research/carbonyl/SCHEMA.md).

## v0.3.7 — Diels–Alder electronic structure

The existing laboratory supports three computed systems. The Diels–Alder case
tracks two forming bonds, three original π bonds and the middle diene bond, with
actual canonical orbitals, total/difference/deformation density grids and separate
frozen-fragment symmetry controls. The constrained study is not an IRC; stationary
claims require full-gradient and Hessian checks recorded in V037_AUDIT.md.
SORG 1333 remains S1/O3/R3/G3 and all 31 reactions / 69 events are preserved.
