# Ochem Atlas v0.3.5 — Reaction Orbital Laboratory

## Release scope and preservation

Base: v0.3.4 commit `08de9d860aec835c4ee235a94bf3ebd015981e7a`. All **31 reactions and 69 listed events** retain their IDs, equations, steps, SORG assignments, sources, lessons, prior quantum data and working features. The taxonomy and reaction count are unchanged. The calculated chloride identity SN2 model is attached as a separately identified example of the existing `sn2:0` event, not a new catalog reaction. It is **not** the HO⁻ + CH₃Br teaching equation and does not reproduce the published ZORA-OLYP/TZ2P case.

## Exact mechanism inventory and original drawings

The complete reaction- and event-level inventory is [audit/V035_MECHANISM_INVENTORY.md](audit/V035_MECHANISM_INVENTORY.md), with machine-readable [dist/mechanism-inventory.json](dist/mechanism-inventory.json). It records every event equation/code, previous figure URL and review, visibility, coverage status, current image and unresolved scope limitations. A complete full-reaction overview does not imply that a prior event-specific picture existed; focused images are counted separately.

| Reviewed illustration status | Before v0.3.5 | After v0.3.5 |
|---|---:|---:|
| Complete | 11 | 29 |
| Partial | 3 | 1 |
| Representative | 12 | 1 |
| Missing/unreviewed figure (primary status) | 4 | 0 |
| Scientifically inconsistent | 1 | 0 |

These primary-status categories are mutually exclusive, not visibility totals. The partial LAH reference remains withheld from display; 30 of 31 entries now show an illustration. “Representative” references may also have been withheld from display. The inventory retains their independent `display` flag and explanation. The scientifically inconsistent propene-hydration drawing retained CH₂ where protonation requires CH₃; it is replaced. Prior sources, including representative or rejected ones, remain under `priorReference`, rather than being silently deleted.

`v035_mechanisms.py` authors **44 new catalog event SVGs across 20 reaction entries**, their full overviews, and one separately labeled chloride-model event SVG. RDKit **2026.9.1** supplies deterministic 2D chemical drawing coordinates, not reaction inference. Explicitly authored electron moves attach to mapped atoms or bond midpoints. Structural formulas, formal charges, atom identities and arrows are inspected; formula and net charge balance are independently checked by RDKit. Radical addition/propagation use three one-electron fishhooks per event; polar and pericyclic events use full two-electron heads. Mechanistic drawings are not electronic-structure calculations.

Coverage includes local SN2/Williamson, generic SN1 core, water solvolysis, HBr addition, corrected hydration, E1, cyanohydrin, acyl substitution, epoxide opening, aldol addition/condensation and E1cB, bromination/halohydrin, all four nitration events, radical addition/propagation, Claisen and electrocyclic closure. Nitration retains N⁺/O⁻ notation and the N=O-to-O arrow on aromatic attack to preserve nitrogen's octet. The arenium drawing is one resonance contributor, not several intermediates. Bromonium is cyclic, not a free Br⁺ intermediate. Anti/backside approach is stated; no enantiomer is selected for racemic products. Thermal unsubstituted electrocyclic closure is labeled conrotatory; the 2D connectivity drawing is not a computed torsional transition geometry. Generic R/X/Nu placeholders stay generic; methyl SN2 is achiral.

**Remaining conventional gaps:** LAH reduction remains **partial** (unvalidated discrete precoordination, metal speciation and grouped hydrolysis); Grignard remains **representative** (generic external substrate/metal-work-up model differs from the written benzaldehyde/methylmagnesium bromide stages). No file is promoted to complete merely because it exists. Previously reviewed original figures and external source attributions are retained. This release improves foundational coverage without claiming to resolve these metal-organic pathways.

## First computed reaction: calculation protocol

**System:** Cl(in)⁻ + CH₃Cl(out), total charge **−1**, multiplicity **1**, **44 electrons**, isolated gas phase without solvent/counterion. **RHF/6-31+G(d)** with PySCF **2.14.0**, 68 spherical Gaussian AOs. The basis includes diffuse functions appropriate to this anionic model but is not a converged benchmark; RHF omits electron correlation. SCF settings: energy tolerance `1e-11` Eh, orbital-gradient tolerance `1e-7`, maximum 150 iterations, Newton fallback if needed. All distributed frame and fragment SCF calculations converged.

Reproduce in Python 3.12.14 with the pinned [requirements](research/reaction-lab/requirements.txt): NumPy 2.3.5, SciPy 1.17.0, h5py 3.15.1, scikit-image 0.25.2, Matplotlib 3.10.8. As in earlier releases, a narrowly scoped workaround is used when the hosted environment lacks PySCF's `/proc` memory-estimation input; molecular integrals and electronic equations are unchanged.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r research/reaction-lab/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python research/reaction-lab/compute_sn2.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python research/reaction-lab/fields_sn2.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python research/reaction-lab/validate_sn2.py
python3 -m pip install rdkit==2026.9.1
python3 build_data.py
npm ci --ignore-scripts
npm test
python3 package_source.py
```

For reuse of an already computed center, `compute_sn2.py --reuse-center` reads the stored symmetric optimization/Hessian record; it does not manufacture or interpolate scan frames. Each frame is separately SCF solved. Field generation can reuse a fragment SCF archive only with matching geometry and its retained convergence log; field cache reuse requires the source wavefunction SHA-256 and matching tracking protocol. Numerical results can vary slightly across machines or degenerate canonical representations.

### Geometry provenance and first-order saddle

The central C is fixed at the origin, Cl(in) on −x and Cl(out) on +x. The symmetric structure is optimized over equal C–Cl distance and the three equal C–H radii, with H atoms in the yz plane at azimuths 0°, 120°, 240°. Optimized distances are **C–Cl = 2.3933753654 Å** and **C–H = 1.06148517 Å**. The full nuclear gradient is then checked, not merely the two optimization parameters.

Maximum Cartesian gradient is **2.8965 × 10⁻⁷ Eh/bohr**. The analytic RHF Hessian, with translations/rotations removed by PySCF's harmonic analysis, has **one imaginary vibrational frequency, 425.7285i cm⁻¹**, and eleven positive frequencies (lowest 198.6944 cm⁻¹). The negative mode changes the two C–Cl distances in opposite directions. This is a **verified first-order saddle at this method/basis**, not a transition-state initial guess. No IRC was computed, so connectivity to optimized reactant/product minima is not claimed from an IRC.

### Five-frame constrained scan — not an IRC

Let `rTS = 2.3933753654 Å` and `q = (rout − rin)/2`. The five frames use `q = −0.6, −0.3, 0, +0.3, +0.6 Å`, with `rin = rTS − q`, `rout = rTS + q`. C and both Cl atoms remain fixed at these prescribed coordinates. The common H radial distance and umbrella displacement along x are relaxed within C3v. These are constrained geometries, **not fully optimized stationary points**, except the separately Hessian-tested center. They are not separated reactants or measured reaction-coordinate samples.

| q / Å | C···Cl(in) / Å | C···Cl(out) / Å | Electronic energy / Eh | Mayer C/Cl(in) | Mayer C/Cl(out) |
|---:|---:|---:|---:|---:|---:|
| −0.60 | 2.993375 | 1.793375 | −958.641840901959 | 0.04995 | 0.88080 |
| −0.30 | 2.693375 | 2.093375 | −958.630408005235 | 0.15171 | 0.70783 |
| 0.00 | 2.393375 | 2.393375 | −958.620529364885 | 0.40121 | 0.40121 |
| +0.30 | 2.093375 | 2.693375 | −958.630408005236 | 0.70783 | 0.15171 |
| +0.60 | 1.793375 | 2.993375 | −958.641840901956 | 0.88080 | 0.04995 |

Browser energies are discrete points, in eV relative to frame 1, using **1 Eh = 27.211386245988 eV**. No smooth energy curve is fitted. These differences are not labeled as an experimental activation barrier or a separated-reactants barrier. Mayer indices use the closed-shell AO density `P`: `B_AB = Σ_(μ∈A,ν∈B) (PS)_μν (PS)_νμ`; they depend on basis/partition and are not bond-line assignments.

## Orbital identities and correspondence

Two full-complex **canonical** spatial orbitals are shown per frame: one occupied (occupation 2) and one virtual (occupation 0). They are not claimed to be localized donor/acceptor orbitals.

At frame 1, the occupied state is chosen by overlap with the incoming chloride fragment's occupied 3px-like MO (fragment MO9; full-complex MO20, projection magnitude 0.81338). The substrate virtual reference is selected by its maximal projection onto a normalized same-sign **C 2px + Cl(out) 3px** AO trial, an explicitly defined σ-antibonding heuristic. This selects substrate virtual MO21 (trial projection 0.53605), then full-complex virtual MO33 (projection 0.72738). It is **not assumed to be the LUMO**, and the trial does not define a unique localized acceptor. A trial-dependent projected canonical state supports interpretation, not a unique mechanism.

Consecutive correspondence uses the full cross-geometry AO metric `Cprevᵀ Scross Cnext` and Hungarian maximum-absolute-overlap one-to-one assignment in occupied and virtual blocks separately. The first-frame largest AO coefficient is positive; a matched state is globally sign reversed when needed for positive consecutive overlap. Raw/aligned overlaps, competing candidates, index changes and ambiguity flags are retained. Degenerate-subspace tracking and occupation-changing paths are not generalized by this example.

The selected occupied indices are **20→22→22→22→20**, and virtual indices **33→30→28→30→33**. Matched occupied overlaps are 0.71014–0.79149, virtual overlaps 0.86262–0.86481, exceeding their recorded next candidates. Actual sign reversals occur. This demonstrates why an orbital's canonical index alone is insufficient for correspondence. It does not establish that maximum-overlap matching resolves every avoided crossing.

## Electron-density evolution and references

All fields come from the calculated AO functions and stored SCF coefficients/density matrices, **not schematic clouds**. One common Cartesian display grid has shape **81 × 49 × 49**, origin **(−10, −6, −6) bohr**, spacing **0.25 bohr** in every direction, C order (z fastest). C remains at the origin and Cl labels/axes are fixed; no rotation, permutation or frame fit is performed. Mesh vertices are in Å, rounded to 0.001 Å for display only.

| Quantity | Definition | Units | Available isovalues |
|---|---|---|---|
| Total electron density | `ρ = Σ fᵢ φᵢ² = AO P AOᵀ` | e bohr⁻³ | 0.02, 0.05, 0.10 |
| Orbital amplitude | Signed real occupied/virtual canonical `φ` | bohr⁻³ᐟ² | ±0.025, ±0.040, ±0.060 |
| Orbital probability | `|φ_occ|²`, no occupation factor, normalized to one | bohr⁻³ | 0.000625, 0.001600, 0.003600 |
| Geometry density difference | `ρ(frame) − ρ(frame 1)` at the same grid coordinates | e bohr⁻³ | ±0.001, ±0.003, ±0.008 |
| Fragment deformation density | `ρcomplex − ρCl(in)− − ρCH3Cl(out)` at the same frame geometry | e bohr⁻³ | ±0.001, ±0.003, ±0.008 |

Probability surfaces are exactly the union of the `+√iso` and `−√iso` amplitude surfaces, rendered in one color; this is a mathematical conversion of the stored orbital, not another SCF calculation. Total density/probability are nonnegative and use one color. Signed orbital amplitude and density differences have distinct explanatory legends. **Teal positive / amber negative density differences mean electron-number accumulation/depletion relative to the stated reference, not positive/negative electrical charges.** Reversing an orbital's global phase changes no density and is disabled for density modes.

Geometry subtraction includes nuclear motion and the moving atomic cores. It is **not a unique electron-transfer density** and need not isolate bonding changes. Frame 1 minus itself is identically zero and has no invented surface. Deformation density instead subtracts separately SCF-computed fragments at each frame's exact coordinates: isolated singlet Cl(in)⁻ (18 electrons) and neutral singlet CH₃Cl(out) (26 electrons), each in its **own RHF/6-31+G(d) basis with no ghost functions**. Fragment membership stays fixed across the scan, including when the substrate C–Cl bond is stretched. This arbitrary but explicit partition is not counterpoise-corrected EDA, not a unique bonding density, and not proof of a fragment dissociation ground state. Fragment nuclear motion cancels in the reference construction, while basis-superposition/partition effects remain.

### Normalization and display-grid limitations

Full-complex AO-metric electron counts `Tr(PS)` equal 44 within numerical precision; maximum `|CᵀSC − I|` is below **4.5 × 10⁻¹³**. Independently evaluated PySCF **level-5 atom-centered Becke quadrature** integrates the total density to **43.999999963–44.000000188 electrons**. Each fragment similarly integrates to 18 or 26, checked to 5e-4 (actual records retain exact values). The continuous reference differences integrate to zero to the corresponding numerical tolerances. Each selected spatial orbital is normalized in the AO metric, so its probability integrates to one.

**The uniform display grid is not suitable for integrated electron populations.** It under-resolves the sharp chlorine cores: its simple voxel-sum electron estimates are about **44.929, 54.687, 86.766, 54.687, 44.929**. These large errors are explicitly reported rather than hidden or “corrected” by rescaling the density. The grids contain actual evaluated scalar values, while finite-grid isosurfaces use ordinary marching-cubes interpolation for rendering. Nuclear-core neighborhoods, fine nodal details, small density differences and isosurface resolution require grid convergence before quantitative spatial conclusions. The full float64 coefficients and density matrices provide the validated, reproducible continuous representation; float32 display arrays and rounded meshes are visual approximations. No integrated electron-transfer number is inferred from these coarse fields.

## Source files and retained numerical data

Under `dist/reaction-lab/`:

- `calculation.json` / `sn2.json`: model, method, geometry provenance, energies, descriptors, quadrature counts, references, tracking and surface levels.
- Five `.xyz` and full frame `.log` files; five `-scf.npz` files retaining all float64 canonical coefficients/energies/occupations, AO overlap, density matrix and coordinates.
- Five `-tracked.npz` files retaining phase-aligned full coefficient matrices and selected indices.
- Five `-fields.npz` files with total density, geometry difference, deformation density, occupied and virtual amplitudes, origin and spacing. These are volumetric arrays, not pictures; no uncomputed inter-frame field is inserted.
- Ten fragment SCF logs and ten fragment coefficient/density archives, sufficient to regenerate the same-geometry references.
- Five `-meshes.json` files containing the signed isosurfaces at three explicitly available levels per quantity.
- `symmetric-hessian.log` and `.npz`: full gradient, Hessian, frequencies and normal modes; the symmetric geometry is also frame 3's explicit `.xyz`.
- Distributed regeneration scripts mirror `research/reaction-lab/compute_sn2.py` and `fields_sn2.py`. `validate_sn2.py`, pinned requirements and the mesh-review script are retained in the source repository/downloadable source bundle.

## Interface and interpretation

A reusable `surface-viewer.js` renders actual meshes with synchronized geometry/frame state. The new `reaction-lab.js` retains one selected catalog event across conventional, quantum and side-by-side modes. All 69 events can be selected; only `sn2:0` has the separately identified calculated chloride case. Others show their actual illustration status and an explicit no-calculated-data message, with existing sourced evidence still available. Opening an event from the modal synchronizes it into the laboratory.

The two stages show molecular geometry and electronic surface together with energy points, C···Cl distances, Mayer indices, original conventional arrows, source downloads and SORG reasoning. Thresholds are adjustable among the three precomputed levels; no density is interpolated between frames. Discrete playback changes to separately calculated frames only. No atom tween, electron trajectory or physical time scale is asserted. WebGL gives rotation/pinch/zoom; if unavailable, Canvas2D projects the **same calculated mesh** at a fixed view, still allowing quantity/threshold/phase changes. Distance guides are dashed and not interpreted as bond orders. If data cannot load, a clear unavailable message is shown rather than a synthetic density cloud.

S1 is supported at the stated restricted-singlet model level; O1 is a conceptual donor–acceptor interpretation informed by the defined fragment projections and backside arrangement; R2/G2 are qualified by the exchanging distances and Mayer indices. Canonical surfaces alone do not uniquely determine these labels or the mechanism. SORG omits method, basis, correlation, solvent, energy, density fields, fragmentation and numerical barriers. Links to Quantum Foundations and the distinct published SN2 case preserve those differences.

## Verification and limitations

- **PASS:** `npm test`, including all earlier suites and `verify-reaction-lab.cjs`: 31 reactions/69 events, original lessons/evidence/filter/storage/modal behavior; full illustration inventory; new authored arrow types; scientific metadata and mesh topology; five constrained frames/Hessian records; 69-event selection; representation changes without losing the event; density/phase/probability modes, thresholds and modal-to-laboratory synchronization. jsdom is DOM integration, not native browser or WebGL proof.
- **PASS:** `validate_sn2.py` reconstructs molecular/fragment AO metrics and density matrices; checks full-complex energies, SCF orbital gradients, coordinates/distances, sampled raw density/orbital/deformation values against stored coefficients, density normalization records, cross-geometry Hungarian assignment and aligned overlaps. It verifies one imaginary Hessian mode with opposite C–Cl distance changes. This is reproducibility/numerical consistency, not an independent correlated benchmark.
- New structural SVGs were rendered for visual review, including substrate/product matching, intermediate charges, nitration octets, bromonium connectivity and radical fishhooks. Formula/charge tests supplement rather than replace this review. Existing v0.3.4 full-sheet reviews are explicitly inherited where no new drawing was made.
- Generated geometry/surface montages were inspected at the default thresholds; total density, zero first-frame difference, moving-core difference lobes, fragment-referenced redistribution and distinct MO phases are visible. No geometry relaxation or electron flow is inferred from a drawing alone.
- Native WebGL rotation, camera reset, touch/pinch and real-mobile layout for **this v0.3.5 interface** require browser/device testing. The user reported no abnormalities in v0.3.4 mobile controls; that does not certify this new viewer. The cloud browser historically has no WebGL context, so its fixed computed projection is a separate fallback test. Live deployment/browser evidence is reported separately when completed.
- No IRC, correlated energy, solvent, free energy, basis/grid-convergence study, HF internal/external stability analysis, selectivity, or unique charge-transfer partition is claimed. Metal-organic conventional coverage remains explicitly incomplete as listed above.

Method references: [PySCF SCF guide](https://pyscf.org/user/scf.html), [PySCF molecular/AO conventions](https://pyscf.org/user/gto.html), [PySCF harmonic-analysis API](https://pyscf.org/pyscf_api_docs/pyscf.hessian.html), [RDKit drawing API](https://www.rdkit.org/docs/source/rdkit.Chem.Draw.rdMolDraw2D.html); Sun et al., [WIREs Comput. Mol. Sci. 8, e1340 (2018)](https://doi.org/10.1002/wcms.1340). These describe methods; numerical SN2 results here were calculated by the Atlas, not copied from the published Research & Methods case.

## Publication packaging

The downloadable source ZIP is generated by `package_source.py` during the Pages build rather than tracked as a duplicate binary in Git. All calculation frames, wavefunction coefficients, volumetric arrays, meshes, logs and regeneration code remain tracked. The public source-download link is preserved.
