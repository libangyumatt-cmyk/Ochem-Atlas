# SORG · Organic Reaction Atlas

A buildless, responsive teaching atlas of foundational organic reactions. Chinese navigation and explanations, English reaction names and scientific notation.

## Included

- 31 reaction entries, 69 coded mechanistic events, including aromatic substitution, E1cB, halohydrin formation, esterification and imine formation.
- Search by reaction name, Chinese keyword, orbital description or four-digit code.
- Independent S/O/R/G filters applied to the **same** event, step-count filters and local favorites.
- A complete pathway reader that shows every listed step, its full equation, electron flow and intermediate in sequence, plus step-specific SORG rationale and scope notes.
- Source-linked, attributed online mechanism figures for selected pathways. These figures supplement the written full mechanisms; generic in-page SVGs are explicitly labeled as local-step schematics.
- Data panels and interactive equilibrium, concentration-rate and relative-barrier calculators.
- Deep links such as `#reaction/sn2`, keyboard navigation and responsive layouts.

## SORG v0.1

This is a project-specific, provisional **teaching index**, not an IUPAC taxonomy or a validated quantum-mechanical invariant.

| Axis | Meaning | Values |
|---|---|---|
| S | Electronic state | 1 closed-shell / paired electrons; 2 open-shell / radical; 3 excited state or state change |
| O | Principal orbital interaction | 1 donor–acceptor; 2 singly occupied orbitals; 3 cyclic concerted interaction; 4 electron-transfer coupling |
| R | Principal bond reorganization | 1 formation/cleavage; 2 contact replacement; 3 multiple-bond redistribution; 4 electron transfer |
| G | Nuclear geometry | 1 approach/separation; 2 coupled approach/departure; 3 collective rearrangement |

Inherited project assignments: `1111`, `1122`, `2211`, `1333`. The carbonyl code `1113` retains an earlier candidate; `1133` and `2222` are explicitly marked as candidate extensions. “Inherited” means inherited from the project's earlier discussion, **not experimentally validated**. More than one reaction can have the same code.

Use one code for each event. Preserve repeated codes. Aqueous SN1 has ionization, water capture **and deprotonation**, whereas the anionic-capture core model has two events. The Grignard and hydride entries explicitly identify simplified metal speciation; their displayed events do not claim to enumerate every microscopic elementary step.

## Local use

Open `dist/index.html` directly in a modern browser. No npm dependencies or runtime network access are required. Optional local server:

```sh
python3 -m http.server 8000 --directory dist
```

Sources are external links, but diagrams, data, filtering, favorites and calculators work locally. Favorites are stored only in that browser. They are not synced between devices.

## Update the content

`build_data.py` is the canonical content source. Edit its codebook, source dictionary or reaction records, then run:

```sh
python3 build_data.py
node verify.cjs
```

This produces `dist/data.json` (downloadable structured data) and `dist/data.js` (the same data embedded for offline use). Do not edit only one generated copy.

## GitHub Pages

The included `.github/workflows/pages.yml` publishes `dist/` with GitHub Pages on pushes to `main` or `master`, or manual dispatch. After placing this project in a dedicated GitHub repository, select **Settings → Pages → Build and deployment → Source: GitHub Actions**. Repository policies and account features may affect availability. Relative asset URLs support project Pages URLs.

The `.openai/hosting.json` file belongs to the private Sites deployment and is intentionally excluded from the downloadable GitHub source package. GitHub Pages does not need it.

## Scientific provenance and limits

Mechanisms and pedagogical facts are checked against John McMurry, *Organic Chemistry*, OpenStax (2023), Chemistry LibreTexts, and IUPAC Gold Book. Each entry lists its own sources. These sources do not assign or validate the SORG codes.

- The E2 isotope-effect example is substrate-specific; the linked textbook does not fully report the experimental temperature and conditions. It is not assigned to the propyl-bromide model shown above it.
- The E1/SN1 64:36 example is for tert-butyl chloride at 65 °C in 80% aqueous ethanol.
- The acid calculator uses the textbook comparison values 4.76 and 9.31. Cross-solvent or inconsistent-standard-state pKa comparisons are invalid.
- Barrier differences are user-specified **hypothetical inputs**. No DFT/IRC/quantum-chemistry calculation has been performed.
- The relative-rate model assumes the same temperature, molecularity, standard states and transmission coefficients. It does not infer product ratios.
- Energy profiles are schematic and have no measured or computed height, depth, or net energy direction.
- Every reaction record marks its displayed pathway as complete for the named substrate and stated conditions. Some solvent-mediated proton relays or metal speciation are represented by their net teaching event and are called out in scope notes; alternate conditions can follow a different mechanism.
- Selected Commons image figures are hot-linked and credited with their file page and license next to each figure. They are supporting references; the step-by-step text remains the authoritative pathway for this specific example.
- The original in-page SVGs depict local electron-pushing motifs, not the whole substrate. They are no longer presented as substitutes for the complete step sequence shown above them.

## Validation

`node verify.cjs` checks data integrity, full-path metadata, image attribution fields, codebook and source references, same-event filtering, step counts, calculator units and invalid-input handling, local asset references and diagram coverage. JavaScript syntax is checked separately.

## Content attribution

Educational text and chemistry content: CC BY-NC-SA 4.0. Wikimedia Commons figures remain under the license shown on each Commons file page; author, source page and license are displayed under each figure. OpenStax attribution and license information is at https://openstax.org/books/organic-chemistry/pages/1-why-this-chapter and https://creativecommons.org/licenses/by-nc-sa/4.0/ . Source-code use is governed by the project license unless the owner later chooses a separate code license.
