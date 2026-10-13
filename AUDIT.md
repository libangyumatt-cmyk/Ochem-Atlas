# v0.2.6 quality-control audit

Baseline: `bc35b03`. Scope: all 31 existing entries and their original 70 listed events. No new reaction entries or SORG categories are authorized by this pass.

## Initial audit and implementation priorities

1. Correct acid-promoted propylene oxide opening: the chloride-attack equation creates an extra H and positive charge; the third event is spurious. The cited OpenStax section identifies the other regioisomer as the major product with HCl/ether. Correct the conditions and product together. The corrected inventory must be 31 entries / 69 listed events, rather than preserving an erroneous count.
2. Preserve the seven codebook entries and numeric definitions. Record event-specific boundaries for bromonium formation, aromatic substitution, iminium dehydration, coordination models and grouped solvent/work-up stages. Do not describe a grouped stage as a verified elementary event.
3. Audit every reference illustration against the card. Distinguish substrate match from pathway coverage and reuse permission. Broken, chemically misleading or unreviewed illustrations must not appear as exact mechanisms. Preserve original URLs and attribution in the audit record.
4. Check both numerical literature tables, seven mapped literature conclusions, and the proposed protocols. Correct substrate-transfer statements and missing computational details. Separate actual source-content review from HTTP reachability.
5. Retain the buildless frontend, filters, storage key, deep links and design. Add regression checks for scientific corrections and DOM interactions. Browser rendering, mobile visual QA and real-browser console checks cannot be claimed: the managed environment has no supported control-browser skill.

This plan was recorded before substantial implementation. Detailed results follow in the completed audit and machine-readable ledgers.

## Completed review

Reviewed on 2026-10-13 UTC (2026-10-12 in Los Angeles). Baseline deployed `data.json` was fetched and matched the repository at `bc35b03` exactly. The corrected release is v0.2.7. No reactions were added. This is an editorial and functional QC pass, not a claim that the whole atlas is independently computationally validated.

### What was fixed

- **Acid-promoted epoxide opening:** corrected the HCl/ether model to the primary-site major product, 1-chloropropan-2-ol. Chloride attack gives neutral alcohol directly. Removed the impossible extra deprotonation and distinguished acid consumption from catalysis. Added an exact original mechanism. The original 70-event ledger therefore maps to **69 current events in 31 entries**.
- **Nitration:** specified nitric-acid hydroxyl protonation, the electron pair forming the second N=O on water loss, and N=O π-electron displacement on arene attack to preserve nitrogen’s octet. Removed misleading carbonyl/alkene local-diagram mappings.
- **Base-promoted epoxide opening:** hydronium work-up now agrees with its equation. **Halohydrin:** aqueous ionic net equation now equals the sum of the displayed steps. **Aldol addition:** explicit enolate formula replaces an unspecified intermediate. **SN2:** clarified that methyl bromide has no ordinary E2 competitor.
- **Fischer esterification and imine formation:** replaced donation into a nonexistent π* orbital of the tetrahedral intermediate with lone-pair formation of the product π bond coupled to leaving-group cleavage. Iminium charge notation is explicit.
- **Hydride/Grignard/Fischer pathways:** identified three grouped stages. Aluminum precoordination is provisional and the hydride pathway no longer claims a complete molecular mechanism. SORG codes on grouped stages denote component/dominant processes only.
- **Illustrations:** added exact original SVGs for proton transfer, Lewis association, methyl-radical recombination and corrected acid-promoted epoxide opening. Every figure now records match, coverage, visual-review status, reuse terms and a specific explanation. Prior source/credit metadata is retained for replaced references.
- **Evidence:** checked both existing numerical tables; added charge/spin and fragment conventions; completed the carbonyl-angle computational protocol and clarified small-angle Pauli repulsion versus large-angle deformation. Corrected the SN1-core literature transfer note (the card is generic, not tert-butyl bromide). Incomplete method checks remain labeled incomplete.
- **Frontend:** event-specific S/O/R/G explanations; provisional/grouped notices; illustration scope/rights captions; graceful image-load failure; all 1–6-event filter options; ASCII/subscript-equivalent search; deduplication of saved IDs; narrow-screen wrapping safeguards. Removed the automatically generated one-peak-per-listed-stage energy curve, which implied unsupported barrier counts and downhill thermodynamics. Existing tabs, grid, colors, storage key and deep links are preserved.
- **Sources:** corrected the broken bromination citation and acyl/carbonyl illustration page links. Replaced blanket “Checked” dates with explicit review scopes. A 200 response alone is never recorded as scientific verification.

### SORG audit and proposed clarification

All seven numeric codebook definitions are **unchanged** and are compared against the baseline snapshot by the regression suite. Every original event is recorded in `audit/events.json`, including its original equation/code, disposition, current equation/code, four-axis rationale and limitation. Retained codes have not been promoted to quantum-mechanically proven categories.

The following issues merit a later codebook discussion; no taxonomy change is implemented here:

| Existing code | Concrete boundary | Proposed clarification for a later revision |
|---|---|---|
| 1133 | Used for bromonium formation, arene attack and E1cB loss, although its rationale mentions a base and C–H/C–X/C=C changes. | Clarify whether the definition intentionally covers broader polar π-bond redistribution; retain these as candidates meanwhile. |
| 1113 | Iminium dehydration restores C=N rather than a carbonyl. | Decide whether tetrahedral-to-planar C=N formation is an explicit analog of carbonyl elimination. |
| 1122 | A solvent relay or metal-alkoxide work-up can contain more than one microscopic event. | Keep the elementary proton-transfer code, but split resolved microscopic stages only when evidence supports them; do not invent stages to preserve a count. |
| 1111 / G1 | Coordination and alkene protonation include local rehybridization or additional bond changes. | Preserve the existing dominant-motion/dominant-bond convention; expose the omitted changes in the event rationale. |

### Reaction-by-reaction findings

The image labels below describe the current reference, not a promise that every image is embedded. “Withheld” means a review, chemical-quality or reuse issue remains.

| Reaction | Current code sequence | Illustration | Remaining research / scope |
|---|---|---|---|
| Proton transfer | 1122 | exact; complete; embedded | Solvent relay and pKa standard-state/temperature metadata are not a computed microscopic pathway. |
| Lewis acid–base association | 1111 | exact; complete; embedded | G1 is the inherited approach convention despite boron pyramidalization. |
| SN2 substitution | 1122 | exact; complete; embedded | Literature calculations concern chloride + A–Cl, not hydroxide + methyl bromide. |
| Williamson ether synthesis | 1122 | representative; complete; withheld | Exact substrate illustration and solution/counterion effects remain to be established. |
| SN1: ionization & capture | 1111 → 1111 | representative; complete; embedded | Generic core is a limiting model; explicit-solvent iPrCl literature does not establish this two-step pathway. |
| SN1 solvolysis | 1111 → 1111 → 1122 | exact; complete; embedded | Ion-pair structure and E1 competition are not resolved by the textbook mechanism. |
| Electrophilic HBr addition | 1111 → 1111 | exact; complete; withheld | 1111 retains the inherited dominant-bond convention despite accompanying H–Br cleavage and π redistribution. |
| Acid-catalyzed hydration | 1111 → 1111 → 1122 | partial; partial; withheld | Microscopic solvent participation and a corrected exact external figure remain open. |
| E2 elimination | 1133 | representative; complete; withheld | 1133 remains a candidate; anti/syn competition depends on actual conformers. |
| E1 elimination | 1111 → 1133 | representative; partial; embedded | 1133 is a candidate for deprotonation/π formation; solvent and ion pairs are unresolved. |
| Carbonyl nucleophilic addition | 1113 | representative; complete; withheld | Generic local event, not a complete neutral-product preparation; 1113 remains candidate. |
| Lithium aluminum hydride reduction | 1111 → 1113 → 1122 | partial; partial; withheld | Discrete AlH4− precoordination is an unvalidated schematic assumption. Aggregation and hydrolysis require research. |
| Grignard addition to an aldehyde | 1111 → 1113 → 1122 | representative; complete; embedded | Aggregation, Schlenk equilibria and grouped work-up are unresolved; the monomer contact model is provisional. |
| Cyanohydrin formation | 1113 → 1122 | representative; complete; withheld | Acetone attack-angle data are analogous, not benzaldehyde results. |
| Nucleophilic acyl substitution | 1113 → 1113 | representative; complete; embedded | A discrete tetrahedral intermediate for this highly reactive pair is a teaching assumption; check concerted alternatives. |
| Basic epoxide opening | 1122 → 1122 | representative; complete; withheld | Actual solvent and order of acid work-up must be retained when comparing paths. |
| Aldol addition | 1122 → 1113 → 1122 | representative; complete; withheld | 1122 for enolate formation is a dominant proton-transfer convention; delocalization is not encoded separately. |
| Radical alkene addition | 2211 | representative; complete; withheld | One propagation event only; spin density and initiation conditions are not computed. |
| Radical recombination | 2211 | exact; complete; embedded | Only a spin-compatible radical pair forms the singlet product directly. |
| Radical chlorination: propagation | 2222 → 2222 | representative; complete; withheld | Propagation only; initiation, termination and further chlorination are outside this card. |
| Diels–Alder cycloaddition | 1333 | exact; complete; withheld | Numerical model uses acrolein, not ethene; radical-cation data cannot inherit 1333. |
| Claisen rearrangement | 1333 | representative; complete; withheld | ELF conclusion checked at abstract level; full electronic method/basis still needs inspection. |
| Thermal electrocyclic closure | 1333 | representative; partial; withheld | Thermal symmetry rule retained; closure feasibility and equilibrium are separate questions. |
| E1cB dehydration | 1122 → 1133 | representative; partial; embedded | 1133 fits bond redistribution but the codebook example refers to base attack; here the leaving-group event starts from enolate. |
| Bromination of an alkene | 1133 → 1122 | representative; complete; embedded | 1133 is a retained candidate: polar bridging is not a pericyclic O3 process; codebook examples do not explicitly cover it. |
| Halohydrin formation | 1133 → 1122 → 1122 | pending; unreviewed; withheld | Same 1133 boundary as bromination; Br2/water must not be equated with an NBS scheme. |
| Nitration of benzene | 1122 → 1111 → 1133 → 1133 | pending; unreviewed; withheld | 1133 at arene attack/rearomatization is broader than the codebook examples; preserve candidate status pending codebook discussion. |
| Fischer esterification | 1122 → 1113 → 1122 → 1113 → 1122 | pending; unreviewed; withheld | The proton relay is grouped; its displayed 1122 refers to component proton transfers, not a verified single event. |
| Imine formation from a ketone | 1122 → 1113 → 1122 → 1122 → 1113 → 1122 | pending; unreviewed; withheld | 1113 for iminium dehydration extends the carbonyl-elimination analogy to C=N; retained as candidate, not a taxonomy change. |
| Base-catalyzed aldol condensation | 1122 → 1113 → 1122 → 1122 → 1133 | pending; unreviewed; withheld | Enolate and E1cB steps retain their convention/candidate boundaries; dehydration depends on conditions. |
| Acid-promoted epoxide opening | 1122 → 1122 | exact; complete; embedded | Corrected HCl/ether major pathway attacks primary carbon; do not generalize tertiary-epoxide selectivity to this substrate. |

### Illustration review limits

12 figures are embedded (four original SVGs and eight reviewed references with identified reuse terms); 19 references are withheld with an explicit pending notice. This reduces the number of external pictures visible compared with v0.2.6 and is intentional: the old interface implied that all were suitable complete mechanisms. Read `audit/figures.json` for the pictured substrate, reagent and coverage differences in every entry.

- Five original references could not be visually verified: halohydrin, nitration, Fischer esterification and aldol condensation were rate-limited/access-blocked; the downloaded imine SVG rendered with unreadable molecular labels. None is marked passed. File-page licenses were inspected separately from the image itself.
- Additional confirmed mismatches include bromine-atom transfer on the radical-recombination card, aromatic Claisen on the allyl vinyl ether card, and tertiary-epoxide regioselectivity on the propylene oxide card. The first and third now have original replacements; the Claisen difference is documented.
- The hydration image retains CH2 after alkene protonation where CH3 is required. The E2 slide’s prose miscounts electron arrows. Both are withheld.
- Local generic SVGs are **partial motifs**, not complete substrate-specific mechanisms. Chemically mismatched motifs have been replaced by pending notices, not by misleading arrows.
- No image-host access error is interpreted as proof that an image is permanently unavailable. Network image loading in an actual browser remains untested.

### Quantum-chemistry and source audit

| Record / primary source | Verification performed | Remaining limit |
|---|---|---|
| Kubelka & Bickelhaupt, JPCA 2017, [10.1021/acs.jpca.6b12240](https://doi.org/10.1021/acs.jpca.6b12240) | All 12 displayed numerical cells in Tables 3–4 agree; ZORA-OLYP/TZ2P and gas-phase model checked. | Related Cl−/A–Cl benchmark, not HO−/CH3Br; F is a transition complex rather than a TS. No calculation reproduced. |
| Vermeeren et al., Chem. Eur. J. 2022, [10.1002/chem.202200987](https://doi.org/10.1002/chem.202200987) | All eight displayed Table 1 cells, 2.203 Å geometry, two energy differences, 0.05 overlap and approximately 0.7-electron donation checked against article text; ZORA-(U)BP86/TZ2P confirmed. | Acrolein rather than ethene. Singlet neutral vs doublet cation pathways are distinct. EDA/overlap are not diabatic coupling. |
| Fernández et al., JCTC 2023, [10.1021/acs.jctc.3c00907](https://doi.org/10.1021/acs.jctc.3c00907) | 111° model angle and interpretation checked; M06-2X/6-311+G(d,p) scan and ZORA-M06-2X/TZ2P EDA added. | CN−/acetone is neither a universal carbonyl angle nor a result for benzaldehyde cyanohydrin. |
| Wu et al., PCCP 2024, [10.1039/D4CP00671B](https://doi.org/10.1039/D4CP00671B) | Microsolvated hydroperoxide/ethyl chloride model, SN2 preference and CCSD(T)/aug-cc-pVTZ//MP2/6-311++G(d,p) energy/geometry protocol checked in indexed primary text. | Full orbital/strain analysis settings not independently inspected. |
| Borderline substitution, RSC Adv. 2024, [10.1039/D4RA00066H](https://doi.org/10.1039/D4RA00066H) | iPrCl/water, M06-2X/aug-cc-pVDZ and loose SN2-like conclusion checked in indexed primary text. | Does not validate the generic card’s discrete-carbocation model. |
| Claisen ELF, PCCP 2018, [10.1039/C7CP07557J](https://doi.org/10.1039/C7CP07557J) | Primary abstract supports asynchronous density rearrangement in parent allyl vinyl ether. | Full method/basis/ELF settings not verified; no new numerical claim. |
| Nitration solvation, PCCP 2022, [10.1039/D2CP01699K](https://doi.org/10.1039/D2CP01699K) | Primary abstract supports the RISM-SCF-cSED solvent-dependent qualitative conclusion. | Full electronic method/basis and solvent composition details not verified. |
| Cave & Newton, CPL 1996, [10.1016/0009-2614(95)01310-5](https://doi.org/10.1016/0009-2614(95)01310-5) | Bibliographic identity confirmed through the authors’ institutional publication record. | Full methodological derivation not re-audited. |

Chemistry corrections use John McMurry’s OpenStax *Organic Chemistry*, especially [18.5](https://openstax.org/books/organic-chemistry/pages/18-5-reactions-of-epoxides-ring-opening) and [8.2](https://openstax.org/books/organic-chemistry/pages/8-2-halogenation-of-alkenes-addition-of-x2). OpenStax 2.9 contains the approximate pKa values 4.76 and 9.31; their equilibrium arithmetic is about 3.55 × 10⁴, not a measured equilibrium constant or quantum result. Temperature-specific thermodynamic provenance remains unspecified. Other mechanism references were link-checked; this is not represented as full independent review of every textbook page.

**Actual calculations performed:** none at the quantum-chemical level. This session performed data transformations, source comparisons, simple arithmetic checks, SVG rendering and software tests. All 31 proposed protocols remain unexecuted. `audit/quantum.json` distinguishes numerical literature, qualitative literature and proposed work; the project-performed quantum-results list is empty.

### Validation results

| Check | Result |
|---|---|
| Deployed v0.2.6 data vs baseline repository | Exact JSON equality before editing. |
| Build / structure / English content | 31 unique IDs, 69 current events, valid fields/references, synchronized data.js/data.json; passed. |
| Codebook / inventory regression | Seven code definitions unchanged; 70 original events accounted for, exactly one invalid event removed; passed. |
| Scientific regression checks | Epoxide product/step count, nitrate octet prose, original recombination figure, generic SN1 model caveat; passed. These tests do not independently prove chemistry. |
| DOM interaction suite | 188 parameterized cases plus saves/unsaves, corrupt/blocked storage, duplicate IDs, deep links, keyboard tabs, search shortcut and image error handler; passed. All 31 panels and 69 event readers exercised. |
| Filters / search | All families, seven existing full codes, impossible cross-axis combination, 1–6-event counts, provisional-only filter, Unicode/ASCII formulas, no-result and reset behavior; passed in DOM simulation. |
| Script / asset checks | JavaScript syntax, local referenced assets, source bundle contents and diff whitespace; passed. |
| Original SVGs | Four rasterized and visually inspected; legible equations, arrows and charges checked. Not browser screenshots. |
| HTTP/source/image requests | Recorded individually in audit/links.json; some 403/404/429 responses and two 200 challenge/redirect pages. Corrected links received HTTP 200. |
| Desktop / mobile rendering, touch, native dialog | **UNTESTED**: supported control-browser skill unavailable in the managed environment. CSS reviewed statically; wrapping safeguards are not a visual pass. |
| Real browser console / external image loads | **UNTESTED**. No errors occurred in the simulated DOM, which is a narrower claim. |
| Deployment | Release commit `249ab06e725ab822196226b7ca0df3631ade0cdb`: [GitHub Pages run 38350661234](https://github.com/libangyumatt-cmyk/Ochem-Atlas/actions/runs/38350661234) passed its build, tests and deploy steps. All 11 checked live HTML/JS/CSS/data/SVG files returned HTTP 200 and matched the committed bytes. The deployed source archive had identical member contents. These HTTP checks do not substitute for browser QA. |

### Files changed

- Build/editorial: `build_data.py`, new `qc_review.py`, new `build_figures.py`; generated `dist/data.json`, `dist/data.js`, four `dist/mechanisms/*.svg`.
- Frontend: `dist/app.js`, `dist/core.js`, `dist/diagrams.js`, `dist/index.html`, `dist/styles.css`.
- Regression/packaging: `verify.cjs`, new `verify-ui.cjs`, `package.json`, `package-lock.json`, `.gitignore`, `.github/workflows/pages.yml`, `package_source.py`, regenerated `dist/sorg-atlas-source.zip`.
- Documentation: `README.md`, `AUDIT.md`, `audit/events.json`, `audit/figures.json`, `audit/quantum.json`, `audit/links.json`, `audit/codebook-v0.2.6.json`.

### Recommended next batch

1. Run real desktop/mobile browser QA and verify the deployed image loads.
2. Restore the 19 withheld illustrations with checked, reusable exact or explicitly representative drawings; prioritize hydration, E2, nitration, halohydrin, imine, Fischer and aldol condensation.
3. Resolve the hydride/Grignard reagent model and split grouped stages only with adequate mechanistic evidence.
4. Inspect full method/SI details for Claisen ELF, nitration solvation and the microsolvation orbital analyses. Discuss the documented 1133/1113 codebook boundaries before any reclassification.
