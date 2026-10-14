# v0.3.1 — quantum-chemistry foundation audit

## Baseline and scope

Inspected the v0.3.0 repository, [V030_AUDIT.md](V030_AUDIT.md), and the deployed `?v=0.3.0#map` site before editing. The site showed 31 reactions and 69 listed events. The SN2 teaching card is **HO⁻ + CH₃Br → CH₃OH + Br⁻**; the new research study is the distinct gas-phase **Cl⁻ + CH₃Cl identity reaction**. Existing reaction payloads, event order/statuses/codes, citations, mechanism figures, comparison, reasoning, filters and saved-reaction behavior were not deliberately modified. SORG remains a provisional educational index, not a validated quantum invariant.

## Evidence provenance and transcription

Primary source: Jan Kubelka and F. Matthias Bickelhaupt, “Activation Strain Analysis of SN2 Reactions at C, N, O, and F Centers,” *J. Phys. Chem. A* **121** (2017) 885–891, DOI [10.1021/acs.jpca.6b12240](https://doi.org/10.1021/acs.jpca.6b12240), freely readable [article](https://pmc.ncbi.nlm.nih.gov/articles/PMC5330660/). Methods §§2.1–2.2: ADF ZORA-OLYP/TZ2P, vibrational checks of optimized stationary points, IRC connectivity, PyFrag activation-strain analysis of Cl⁻ and CH₃Cl fragments. Gas phase, total charge −1, singlet. The paper reports the validation; Atlas did **not** repeat it.

| State or property | Published value | Exact location and convention |
|---|---:|---|
| Isolated CH₃Cl C–Cl length | 1.790 Å | Table 1, CH₃Cl, A–Cl (R) |
| RC C–Cl_out length; electronic ΔE | 1.835 Å; −9.2 kcal mol⁻¹ | Table 1, CH₃Cl, RC; relative to separated reactants |
| Symmetric TS C–Cl_out length; electronic ΔE | 2.351 Å; −0.3 kcal mol⁻¹ | Table 1, CH₃Cl, TS; relative to separated reactants |
| TS Cl_in–C length | 2.351 Å *derived from stated symmetry* | Table 1 TS length plus §3.1 symmetric Cl–C–Cl; not a second independent table cell |
| TS strain; total fragment interaction | +31.6; −31.9 kcal mol⁻¹ | Table 3, Cl⁻ + CH₃Cl; deformed fragments at TS; sum −0.3 |
| Isolated substrate σ*(C–Cl) energy; VDD carbon charge | −5.13 eV; −0.031 e | Table 4, CH₃Cl; orbital and VDD conventions, not RC/TS changes |
| TS Cl⁻ 3p / substrate σ* overlap | 0.215 dimensionless | Table 4 S, note e; **not** a diabatic electronic coupling |

The separated-reactant electronic-energy zero is a reference, not a computed activation barrier. Subtracting RC −9.2 from TS −0.3 gives **8.9 kcal mol⁻¹**, explicitly labeled derived, not a separately transcribed value or solution-phase free energy. The article's Table 2 separately reports 1 atm, 298.15 K Gibbs activation free energy; this viewer does not mix that thermodynamic quantity into the electronic-energy series. The authors' Fig. 2/3 curves are not digitized or recreated as a smooth path.

The paper links `jp6b12240_si_001.pdf` with Cartesian coordinates, ADF energies and imaginary-frequency counts. Access to that supplement failed in this session; no Cartesian structures, coordinate frames or frequency numbers were transcribed. The article's CC BY-NC-ND terms are recorded; no paper figure or supplement is redistributed. The Research viewer's labeled glyph is original and explicitly **not** a full geometry or a scaled molecular model.

## Implemented architecture and interface

| File | Role |
|---|---|
| `research/evidence.schema.json`, `research/evidence.json` | Versioned study contract and one published-data record: molecular identities and atom mapping; charge/spin/conformation/environment; method/basis/software; coordinate definition; per-quantity value, unit, status, convention and source location; explicit missing fields, artifacts and limitations. Literature and future Atlas calculations require distinct statuses. |
| `build_research.py`, `dist/research-data.json`, `dist/research-data.js` | Release-subset validator and deterministic static payload. The schema is machine-readable; the Python script enforces selected scientific invariants, **not** full JSON Schema validation or independent source verification. |
| `dist/research.js`, `dist/index.html`, `dist/styles.css` | Selectable R, RC and TS cards; exact tabular bond lengths and relative energies, supported point-specific descriptors, unavailable-value messages and a non-scaled atom-label glyph. No continuous curve, invented coordinates, orbital surfaces or similarity score. Research navigation and SN2 card link preserve the design language. |
| `research/README.md`, `research/workflows/sn2_psi4.py` | Source locations, limitations, staged reproduction instructions and an **unexecuted** B3LYP/aug-cc-pVDZ isolated-CH₃Cl optimization/frequency seed. The seed is not the published ADF protocol and does not claim RC, TS, IRC or a barrier. |

The optional descriptor registry defines orbital interaction, electron-density partition, bond order (unavailable), geometric distortion, spin/state, coordinate topology and activation-strain terms with methods, units, normalizations and applicability. `1122` captures coarse-grained closed-shell bond replacement; it omits geometry/energy magnitudes, reactant-complex stabilization, atom mapping, solvation, orbital conventions and entropy. No four-digit code or taxonomy definition changed.

## Verification performed

- `python3 build_research.py` validates one record, three tabulated states and nine descriptor definitions; `python3 build_data.py` rebuilds the 31/69 reaction payload. `npm test` checks original regressions and three viewer selections, quantities, descriptor counts, versioned assets, preserved event/code ledger, and the distinction between published and derived values. Tests are data/DOM checks, not quantum calculations.
- No Psi4, PySCF, xTB, ORCA, NWChem, ASE or RDKit executable/module was available in the runtime. **No Atlas electronic-structure calculation was run; no computed input/output is represented as results.**
- GitHub Pages workflow [run #20](https://github.com/libangyumatt-cmyk/Ochem-Atlas/actions/runs/38516408055) succeeded for commit [`4c06ef6`](https://github.com/libangyumatt-cmyk/Ochem-Atlas/commit/4c06ef60413bca40ae9f8a14211b35d6e112aa2c). In a real desktop cloud browser, the deployed [`?v=0.3.1#research`](https://libangyumatt-cmyk.github.io/Ochem-Atlas/?v=0.3.1#research) displayed v0.3.1, 31 reactions and 69 events. R, RC and TS selection produced the documented point-specific quantities; the descriptor disclosure opened; the SN2 teaching modal's Data button closed the modal and navigated to research. Search for `SN2` yielded 3 entries (including code-related matches); elimination-family filtering yielded 3; saving SN2 raised the saved count, the saved-only filter yielded 2 in that browser session, and the saved count persisted on reload. The research panel was visually inspected at desktop width. The sole captured console error was from a Chrome-extension content script (`chrome-extension://.../content-script.bundle.js`), not an Atlas asset; no page-script error was observed in that check. This is a sampled manual regression, not exhaustive browser coverage of every reaction/modal path.
- No mobile viewport/touch browser was available for this session; mobile responsiveness remains **untested**, though CSS responsive rules and static DOM tests were checked. Linked SI coordinates remained inaccessible; no visual verification of Cartesian structures or independently re-run stationary-point validation is claimed.

## Unresolved research questions

Obtain the legally distributable SI coordinates and validate atom order, full R/RC/TS geometries and imaginary frequencies against the source; then consider a true coordinate viewer. To add continuous IRC data, obtain numerical samples or independently calculate and archive them with software/version/input/output. Quantify bond-order and density redistribution under stated partitions at matched geometries. Reproduce frontside-versus-backside comparison, solvation and entropy at declared levels before making selectivity or solution-kinetic claims. Test descriptor comparability and the SORG 1122 boundary across substrates before any similarity metric. Fourteen existing non-SN2 illustrations remain withheld, and other prior candidate-code/relay-stage limitations remain as in V030.
