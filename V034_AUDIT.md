# Ochem Atlas v0.3.4 — Orbital Diversity and Evolution

## Scope and preservation

Based on v0.3.3 commit `0dec1fe0d77e0a4d9d8b3357ed14f06f5c81d851` and `V033_AUDIT.md`. The deployed v0.3.3 laboratory was inspected in Chrome: its original three molecule options, scientific metadata, downloads and WebGL-unavailable static fallback were present. No reaction or event was added: **31 reactions / 69 events** remain. Existing mechanisms, SORG taxonomy and assignments, citations, evidence, quantum datasets, lessons and application features are retained. Reaction-data changes are only version/date metadata. Original `orbital-data.json` and v0.3.3 raw files are untouched.

## Reproducible calculations

`research/orbitals/generate_v034.py` independently solves eight gas-phase SCF problems with **PySCF 2.14.0 / STO-3G**, charge **0**. Closed-shell systems use **RHF, multiplicity 1**; allyl radical uses **ROHF, multiplicity 2**, with 12 alpha and 11 beta electrons. This is an actual open-shell determinant, not a closed-shell illustration. All coordinates are explicit in the script and corresponding `.xyz` files; none is optimized or experimental. Benzene uses a regular planar carbon hexagon of radius 1.397 Å, hydrogen radius 2.477 Å. Butadiene is planar s-trans; allyl is planar. Complete coordinates take precedence over these short descriptions.

The pinned environment is `research/orbitals/requirements.txt`: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, scikit-image 0.25.2, h5py 3.15.1, Matplotlib 3.10.8. Regeneration was rerun in this turn. A file-write robustness change subsequently writes and verifies complete deterministic gzip bytes before removing an intermediate cube; it does not change the calculated fields. This fixed an empty compressed torsion-00 MO9 file discovered during validation.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r research/orbitals/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python research/orbitals/generate_v034.py
.venv/bin/python research/orbitals/render_v034.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python research/orbitals/validate_v034.py
npm ci --ignore-scripts
npm test
python3 package_source.py
```

SCF tolerances are `conv_tol=1e-11`, `conv_tol_grad=1e-7`, maximum 200 cycles. The existing narrowly scoped `/proc` memory-estimation workaround is retained where needed. Distributed source and outputs are under `dist/orbital-files/v034/`: 8 `.xyz`, 8 full `.log`, 8 `-scf.npz` archives, 22 `.cube.gz`, 22 static `.png`, regeneration script and `summary.json`. `dist/orbital-diversity.json` contains the derived meshes. NPZ archives include all MO coefficients, occupations, orbital energies, AO overlap and Cartesian input coordinates, not just the displayed orbitals.

| Model | Electrons | Displayed canonical MOs (1-based) | Total energy / Eh |
|---|---:|---|---:|
| Allyl radical, ROHF doublet | 23 | SOMO 12; separate spin-density field | −115.008706794439 |
| Benzene, RHF singlet | 42 | π1–π6: 17, 20, 21, 22, 23, 24 | −227.890568878576 |
| s-trans-1,3-Butadiene, RHF singlet | 30 | π1–π4: 14, 15, 16, 17 | −153.001112561757 |

Grid: **44³**, three-bohr margin. Orbital surfaces: **ψ = ±0.035 bohr⁻³ᐟ²**. Spin-density surface: **ρα−ρβ = ±0.003 e bohr⁻³**. Marching cubes uses the actual sampled scalar fields; only display vertices are rounded to 0.001 Å. A negative surface is absent when the field never reaches the negative threshold; none is invented. Static PNGs render the same meshes.

ROHF gives **⟨S²⟩ = 0.75**, with zero spin contamination to numerical tolerance. Because the doubly occupied alpha/beta spatial orbitals coincide, this model's spin density equals `|SOMO|²`. It omits UHF spin polarization and beta-excess regions; spin density is not a signed orbital amplitude. Its phase reversal is disabled and its legend describes alpha/beta excess. ROHF canonical orbital eigenvalues use PySCF's effective-Fock convention; they are not experimental ionization energies or separately optimized alpha/beta eigenvalues.

Benzene has three occupied and three virtual π orbitals. The occupied pair (20,21) and virtual pair (22,23) are degenerate within 1e-8 Eh. D6h symmetry is recognized; displayed irreps belong to the computational Abelian subgroup. Degenerate partners can be orthogonally rotated: the individual displayed partner is not unique. Butadiene illustrates the 0/1/2/3 longitudinal-node interpretation plus the molecular-plane node; the s-trans model is not a Diels–Alder transition structure.

## Controlled orbital evolution

Five **separate computed geometries**, not deformations of one mesh, rigidly rotate the right ethylene CH₂ through 0°, 15°, 30°, 45°, 60°. C–C is 1.334 Å; bond lengths and all unrotated coordinates remain fixed. This is a **constrained rigid torsion scan, without relaxation**. It is neither an optimized scan nor an IRC, and no stationary-point/frequency calculation is claimed.

| Torsion | E(RHF) / Eh | Normalized local carbon p-AO overlap |
|---:|---:|---:|
| 0° | −77.072681711657 | 0.23981088 |
| 15° | −77.066431558234 | 0.23163952 |
| 30° | −77.047732641373 | 0.20768231 |
| 45° | −77.016756541448 | 0.16957190 |
| 60° | −76.973842115406 | 0.11990544 |

The overlap is between a left carbon 2pz AO and the rotated right `cos(θ)2pz−sin(θ)2py` AO, normalized in the AO metric. It is **not the overlap of distinct orthogonal canonical MOs**, a coupling energy or a bond order. The browser reports the selected orbital eigenvalue/symmetry, total energy, ΔE from the first constrained frame and this defined local overlap.

Correspondence uses `C(previous)ᵀ S(cross geometry) C(current)`, Hungarian maximum-absolute-overlap one-to-one assignment within occupied and virtual blocks separately. It does not identify orbitals from their indices. Matched coefficients are sign aligned so consecutive overlaps are positive; initial signs set the largest AO coefficient positive. Both occupied π-derived and virtual π*-derived tracks have overlaps **0.95893–0.98423**, exceeding all competing candidates (largest 0.25062). No index reordering or avoided crossing occurs here; the five-frame example is not evidence that this algorithm resolves arbitrary crossings. Occupied/virtual-block separation would need reconsideration for occupation changes; degenerate subspaces would require subspace tracking. No field interpolation is used. Molecular point groups change D2h→D2; subgroup labels depend on chosen axes and must not themselves be treated as tracking labels.

The scan deliberately stops at 60°. It presents the **restricted paired-electron RHF branch**, not a verified multireference ground state. SCF convergence alone does not establish internal/external HF stability; stability analysis was not performed. No energy difference is described as a reaction barrier, torsional barrier maximum, selectivity or experimental energy.

## Scientific checks and tests

- `research/orbitals/validate_v034.py`: **PASS for all eight models**. Independently reconstructs AO overlaps and density matrices from distributed coefficients; checks electron count, `CᵀSC`, coordinates, total energy, SCF orbital gradient, signed cube values, planar π parity, ROHF determinant S² and SOMO-density equivalence, benzene degeneracies, actual torsion angles, local AO overlaps and Hungarian assignments/phase alignment. Maximum orthogonality error is below 8.2e-14; orbital-gradient norms are below 2.3e-8. Cube precision is checked to 5.1e-6 absolute against recalculated wavefunctions.
- `npm test`: **PASS**, including all existing suites plus `verify-diversity.cjs`. New checks parse all 22 compressed grids, validate mesh topology, electron/spin records and scan correspondence; actual laboratory JavaScript executes in jsdom for all new molecule/orbital options, retained scan orbital selection, spin-density labels, download paths, reset, WebGL fallback and missing-extension-data recovery. jsdom is a DOM integration test, **not a native browser/WebGL/touch test**.
- All 22 new static projections were visually reviewed in a montage. Allyl SOMO shows opposite terminal phase; its spin-density plot is nonnegative. Benzene shows the six delocalized π patterns; butadiene shows the changing nodal patterns. Scan surfaces are different calculated fields. This visual review is not an independent high-level calculation.
- Original scientific assets and reaction content are preserved; only release version/date changes in reaction JSON. Existing reaction/SORG, mechanism, literature, lesson, storage/filter/modal suites remain passing. A distance-based rendering defect that omitted butadiene's central single bond was fixed using element-specific covalent-radius thresholds; these display sticks do not assign quantum bond orders. Camera fitting includes larger systems; scan stepping preserves camera and selected track.

## Browser evidence and remaining limits

The cloud Chrome instance cannot create a WebGL context and displays the calculated static fallback on deployed v0.3.3. A local Playwright Chromium installation was attempted, but the official browser download returned incomplete archives, so no local browser executable was available. **Actual 3D rotation, wheel/pinch zoom, rendered phase reversal, touch gestures and mobile-device/browser layout remain unverified in this environment.** Neither DOM tests nor mesh review are substituted for those checks. No mobile device is claimed tested. Deployment and post-publication fallback observations, if completed, are appended below.

## Interpretation and sources

Existing links connect allyl to S2/O2 and radical addition, benzene to delocalization and nitration, and butadiene to O3/Diels–Alder. An isolated molecule is not itself an elementary-event assignment. These models support orbital/spin/symmetry discussion; they do not establish barriers, regioselectivity, directing effects, aromatic stabilization or a transition-state pathway.

Method sources: [PySCF SCF user guide](https://pyscf.org/user/scf.html), including stability analysis; [PySCF cube API](https://pyscf.org/pyscf_api_docs/pyscf.tools.html); Sun et al., [WIREs Comput. Mol. Sci. 8, e1340 (2018)](https://doi.org/10.1002/wcms.1340). These explain methods; the numerical outputs are Atlas calculations, not numbers taken from those references. Existing sources and their qualifications are preserved.
