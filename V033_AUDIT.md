# Ochem Atlas v0.3.3 scientific and functional audit

## Scope and preservation

The release adds a molecular electronic-structure laboratory and an SCF teaching model. It retains 31 reaction entries, 69 listed elementary events, their SORG assignments, the previous mechanism figures, literature evidence and five Quantum Foundations lessons. The laboratory's seven orbitals are **new Atlas-generated fixed-geometry calculations**, not results from the published SN2 case, and no reaction pathway was calculated.

## Calculations and exact provenance

`research/orbitals/generate.py` and `research/orbitals/requirements.txt` reproduce neutral singlet gas-phase RHF/STO-3G calculations with PySCF 2.14.0, Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, h5py 3.15.1 and scikit-image 0.25.2. The input `.xyz`, complete SCF `.log`, `.npz` coefficients/energies/occupations/overlap, and seven compressed `.cube.gz` signed-amplitude grids are distributed under `dist/orbital-files/`; the meshes and their metadata are in `dist/orbital-data.json`. Static images were generated from the calculated meshes by `research/orbitals/render_fallback.py` with Matplotlib 3.10.8. The input coordinates are manually specified educational model geometries, **not optimized or experimental structures**. No solvent, geometry optimization, vibration, correlation correction, transition state, IRC or orbital-energy observable is claimed. See `research/orbitals/README.md` for the full coordinates, protocol, conventions and method references.

| Model | Electrons | Selected canonical MOs, 1-based | RHF total energy (hartree) |
|---|---:|---|---:|
| H₂, H at z=±0.370 Å | 2 | 1σg (1), 1σu* (2) | −1.1167593073964255 |
| C₂H₄, planar input geometry in `.xyz` | 16 | π HOMO (8), π* LUMO (9) | −77.07268171165666 |
| CH₂O, planar input geometry in `.xyz` | 16 | π(C=O) (7), n(O) HOMO (8), π*(C=O) LUMO (9) | −112.35385994748981 |

The sample grid is 44³ with a three-bohr margin; the browser mesh uses marching cubes at signed ψ=±0.035 bohr⁻³ᐟ², with vertex rounding to 0.001 Å only for rendering. The full cube grids are preserved. Occupied selected MOs have two electrons, virtual selected MOs zero. Electron counts and CᵀSC=I were checked to error below 3.1×10⁻¹⁵. The π and π* MOs have odd z parity for planar molecules; n(O) has even z parity. H₂ 1σg has no negative isosurface at this threshold, and none is drawn. Phase colors represent the sign of a *real orbital amplitude*, never electric charge; globally reversing the phase does not change density or nodes. Orbital shapes and eigenvalues depend on method, basis and canonical-orbital convention.

## Learning features

- A locally bundled Three.js 0.186.1 (MIT license) viewer shows calculated isosurfaces, labeled nuclei, orbital selection, rotation, zoom, reset and global phase-color reversal. Geometry, identity, RHF/STO-3G method, occupied electron count, eigenvalue and isovalue are presented next to the figure. PNG projections of the *same meshes* serve as the static fallback. Raw wavefunction grids and inputs/outputs are downloadable.
- A sixth Quantum Foundations lesson connects the electronic Hamiltonian to HF and Kohn–Sham DFT, finite basis functions, the generalized F(P)C=SCε eigenproblem, density updates, SCF convergence, correlation, geometry optimization and frequency analysis. Its damped scalar occupancy recurrence is an **explicitly defined illustrative logistic map**, not a molecular SCF output. The page states this distinction.
- Formaldehyde π and π* connect to carbonyl nucleophilic addition and cyanohydrin formation; ethylene π and π* connect orbital symmetry to Diels–Alder. A static isolated-molecule orbital alone gives neither activation barriers nor selectivity. H₂ illustrates the bonding/antibonding and global-phase basics. The prior five lessons and Research & Methods data remain accessible.

## Checks and evidence

- `npm test`: PASS. Existing reaction/data/foundation/UI suites pass, including 31 entries and 69 events. The new orbital suite parses all seven compressed Gaussian cube grids, checks mesh topology/index bounds, electron count, 1,109 z-parity grid values, global-phase invariance and 24 damped scalar recurrence steps. The UI suite includes new controls and navigation.
- Generated PNGs for all seven selected orbitals were inspected visually as a montage. H₂ 1σg shows one sign; 1σu* separates at the midpoint. The planar π orbitals show opposite signs above/below the molecular plane, and π* adds the relevant antibonding separation; the formaldehyde n(O) projection is in plane. These are visual/symmetry reviews of these model calculations, not independent high-level validation.
- `git diff --check`, JavaScript syntax checks and `python3 package_source.py`: PASS. The source ZIP includes the numerical grids, original output and reproducible scripts.

## Limitations and further research

RHF/STO-3G is deliberately small and does not establish quantitative organic selectivity. These are fixed, manually specified geometries with canonical MOs; no optimization, frequencies, correlated method, orbital interaction energy, SN2 path, carbonyl attack coordinate or Diels–Alder transition structure was computed. Isolated ethylene and formaldehyde MOs illustrate symmetry, not the full reacting pair. The viewport mesh is sampled and thresholded, not a complete wavefunction. Test the sensitivity to basis, geometry and orbital analysis before drawing numerical mechanistic conclusions. Touch/browser behavior and deployment evidence are recorded separately below.

## Publication and browser verification

The source tree of the published GitHub commit `f427b4cdcc3312743c9d7e077afbb426e0ef73ed` matches the locally tested tree. GitHub Pages subsequently served the v0.3.3 page, versioned reaction-data link, laboratory section, computed PNG and downloadable orbital links at `https://libangyumatt-cmyk.github.io/Ochem-Atlas/?v=0.3.3#lab`. (This audit update may be followed by a later documentation-only commit.) In the live Chrome cloud browser, choosing formaldehyde MO9 changed the displayed π* identity, method, occupation, orbital energy, image URL and explanation; the PNG loaded at its natural width. The SCF controls changed feedback to 2.00 eV and damping to 1.00; its displayed 24th-step residual was 7.73×10⁻¹ and correctly labeled unconverged. Search for “Diels” returned one entry; saving SN2 changed the saved count to one, opening/closing its mechanism modal worked, the saved-only filter returned one entry, reset restored 31, and the pericyclic family filter returned three.

**Environment limit:** This cloud browser returned `WebGL unavailable`; it showed the calculated static fallback and disabled the phase toggle. Actual 3D camera rotation, pinch/wheel zoom and phase-color reversal in a WebGL browser, as well as real mobile viewport/touch testing, remain **untested**. We inspected all seven generated static surface projections, but a browser screenshot of the fallback is not a 3D interaction test. Browser console output contained extension-origin metadata errors, with no site-origin exception observed during these checks. This does not establish absence of every possible page error or independent validation of the molecular method.
