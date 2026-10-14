# v0.3.2 — Quantum Foundations & Visualization audit

## Baseline and preservation

Inspected v0.3.1 source, deployed `?v=0.3.1#research`, and [V031_AUDIT.md](V031_AUDIT.md). The prior site displayed 31 reactions, 69 listed events and a three-point published-data SN2 viewer. This release changes the educational interface and version metadata, **not** reaction/event content, codebook digits, mechanisms, figures, source records or evidence values. `dist/data.json` differs from v0.3.1 only in `version`; `research/evidence.json` is unchanged. SORG remains a provisional interpretation layer, not a quantum invariant.

## Content and original models

Five ordered lessons now precede SORG: many-electron electronic states and spin; LCAO and orbital coupling; phase, orbital probability and total/difference density; fixed-nuclei PES and stationary points; the deliberately non-fundamental SORG mapping. Each includes an equation rendered as native MathML, symbols/units, one organic example, a visual, a direct axis link and an assumptions disclosure. OpenStax [quantum theory](https://openstax.org/books/chemistry/pages/6-3-development-of-quantum-theory) and [organic orbitals](https://openstax.org/books/organic-chemistry/pages/1-2-atomic-structure-orbitals) provide introductory context. Q-Chem's [PES/manual](https://manual.q-chem.com/4.1/) describes molecular stationary-point and path methods. The existing SN2 primary study remains Kubelka & Bickelhaupt, *J. Phys. Chem. A* **121** (2017), 885–891, DOI [10.1021/acs.jpca.6b12240](https://doi.org/10.1021/acs.jpca.6b12240); all specific tabular values and conventions remain those recorded in V031.

| Visual | Exact definition and scientific boundary |
|---|---|
| Paired/open-shell occupancy | Conceptual ↑↓ / ↑ symbols denote opposite or unpaired spin projections, not calculated orbitals, full spin eigenfunctions or curved arrows. |
| Two-state coupling | Original orthonormal Hermitian 2×2 model with εD=0, Δ=εA−εD≥0 and real |V| in eV. E±=Δ/2±√[(Δ/2)²+|V|²]; lower-state acceptor weight = [1−Δ/√(Δ²+4|V|²)]/2 except the exact zero/zero degeneracy, where it is undefined. Analytic values and discrete energy levels update from sliders. No SN2 orbital energies/couplings are inserted. |
| Orbital phase / density | Normalized 1D p-like ψp(x)=√[2/√π]x exp(−x²/2) has signed phase and nonnegative |ψp|². Two Gaussian functions gA,gB centered at ±1.15 with width 0.85 give overlap exp(−1.15²/0.85²) and normalized bonding φ+=(gA+gB)/√[2(1+S)]. The two-electron model ρbond=2|φ+|², reference ρref=|gA|²+|gB|², and Δρ=ρbond−ρref integrate to 2, 2 and 0 respectively over dimensionless x. These are one-dimensional constructed functions, **not** molecular orbital isosurfaces or SN2 density data. Colors encode phase sign or reference-relative difference only, never positive/negative electronic charge. |
| PES | Original U(x,y)=A(x²−1)²+0.6y² in eV for dimensionless x,y, with A=0.4–2 eV. Minima (±1,0) have energy 0 and positive Hessian eigenvalues; (0,0) is a first-order saddle with energy/barrier A and Hessian diagonal (−4A,1.2) eV per squared model coordinate. The interactive y=0 cut is a declared analytic teaching path, **not** a molecular IRC, free-energy profile or dynamics. |
| Published SN2 energy points | The existing separated reactant 0, RC −9.2 and TS −0.3 kcal mol⁻¹ now appear as **unconnected discrete points** on a common vertical scale. Horizontal spacing is categorical, not coordinate distance. The TS fragment strain +31.6 and interaction −31.9 kcal mol⁻¹ appear as signed labeled magnitude bars, with Cl⁻/CH₃Cl fragment convention. Bond lengths and explicit missing fields persist. No Cartesian structure, interpolated point, orbital surface or continuous trajectory was added. |

The axes now disclose concept, possible evidence method, typical SN2/Diels–Alder assignment, omitted information and provisional status. SN2 `1122` and thermal Diels–Alder `1333` retain their old assignments. Their comparisons do not assert that a two-state model derives the O code. `dist/foundations.js` exports pure analytic model functions for tests, but does not produce quantum chemistry results.

## Validation

- `python3 build_data.py` regenerated the unchanged 31/69 payload with version 0.3.2; `python3 build_research.py` validated the pre-existing record and three points. No Atlas electronic-structure calculation was run.
- `npm test` includes the prior structural and 283-case DOM regression and `verify-foundations.cjs`: 4,038 analytic/grid checks of matrix trace/determinant and level splitting, mixing bounds/degeneracy, PES finite-difference gradients and Hessian signs, phase parity, density normalization and signed-zero difference integral. UI tests exercise sliders, switches, lessons, research point selection, modal paths, filters, search and saved state in jsdom. These are mathematics/DOM checks, not independent scientific validation of the primary publication.
- Desktop browser, responsive/mobile checks, MathML rendering, model control interactions and GitHub Pages deployment results are recorded after publication below.

## Limits and next steps

Native MathML is used without an external CDN; unsupported older browser engines may require a fallback. The electron-density model is one-dimensional; the PES and level diagrams are constructed mathematics, not molecular calculations. The research viewer still lacks verified Cartesian coordinates and numeric IRC samples from the supplement, so its atom-label glyph is intentionally not to scale. Published energy values are electronic, not solution free energies; the 8.9 kcal mol⁻¹ RC-to-TS difference is derived by subtraction. Obtain source SI structures with atom mapping and frequency evidence before any real geometry rendering. Matched-grid density/bond-order analyses, solvent effects and cross-reaction descriptor validation remain unperformed.

## Release verification

Pending final commit and deployed-browser check.
