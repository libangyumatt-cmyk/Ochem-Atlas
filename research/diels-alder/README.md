# Diels–Alder electronic structure (v0.3.7)

System: neutral singlet 1,3-butadiene + ethylene → cyclohexene, C6H10,
46 electrons, gas phase. Fixed atom mapping: diene C1–C4, ethylene C5–C6;
diene H7–H12, ethylene H13–H16. New bonds C1–C5 and C4–C6.

## Reproduction

Python 3.12, PySCF 2.14.0, geomeTRIC 1.1.1, NumPy 2.3.5, SciPy 1.17.0,
scikit-image 0.25.2, RDKit 2026.9.1. Install pinned dependencies, then from repo root:

```sh
OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 python research/diels-alder/locate.py
OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 python research/diels-alder/endpoints.py
OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 python research/diels-alder/scan.py
OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 python research/diels-alder/study.py
OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 python research/diels-alder/fields.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/diels-alder/enrich.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/diels-alder/validate.py
python build_reaction_systems.py
npm test
```

The published outputs in `dist/reaction-lab/diels-alder` are retained actual
calculations. Deployment packages these records; it does not rerun quantum
chemistry. Optimization is not guaranteed to converge identically with different
software/grid/linear-algebra versions. See `V037_AUDIT.md` for actual results.

## Method and path labels

Restricted Kohn–Sham B3LYP (PySCF's VWN-RPA convention), 6-31G(d), numerical
integration grid level 3; neutral singlet, SCF energy tolerance 1e-10 Eh and
orbital-gradient threshold 1e-6. This functional includes approximate correlation;
it is not a correlated-wavefunction benchmark. No dispersion correction, solvent,
ZPE, thermal/free-energy correction, functional or basis convergence study.

`locate.py` first relaxes a 2.25 Å constrained seed (not a TS), then searches a full-dimensional first-order saddle with analytic nuclear
gradients and initial analytic Hessian. Final nuclear gradients and all
vibrational modes are checked independently of optimizer success status.
`endpoints.py` independently optimizes reactants and product. `scan.py` fixes both forming C–C distances at 3.0, 2.5 and 1.9 Å and relaxes the
other coordinates. The product is rigidly aligned and its final full Hessian is recomputed. **These constraints do not define an IRC.** No IRC
or trajectory, complete endpoint connectivity, or general synchronicity is claimed.

Isolated reactant minima are distinct from reactive s-cis/frozen fragments.
Endpoint electronic energy differences are not experimental activation free
energies. The relaxed constrained seed is not itself labeled stationary. Full symmetry is not imposed in TS optimization; forming-bond
asymmetry is reported. The scan's equal-distance constraint imposes synchronous
bond distances, which cannot be used as independent evidence for synchronicity.

## Densities, bond orders and orbital identity

All actual SCF coefficients, occupations, AO overlaps, density matrices, Cartesian
coordinates and volumetric grids are retained. Densities are AO-evaluated at each
frame; neither densities nor orbital fields are interpolated. The common grid has
81 × 71 × 71 points, spacing 0.28 bohr, origin (−10, −9, −7) bohr, z fastest.
Coordinates are Å, energy Eh, density electron/bohr³, amplitude bohr⁻³ᐟ².
Grid fields are float32; wavefunctions are float64. No density rescaling is used.
The coarse grid under-resolves nuclear cores; normalization uses Tr(PS) and
independent level-5 atom-centered Becke quadrature. Display-grid sums are reported
rather than passed off as accurate electron counts.

Each geometry is rigidly aligned by proper least-squares rotation of the six
mapped carbons to the TS skeleton; its final SCF is performed after alignment.
Density difference = current density − `approach` density at identical Cartesian
nodes. Nuclear displacement contributes: this is not a unique electron-transfer
map. Deformation density = complex − frozen neutral singlet butadiene − frozen
neutral singlet ethylene, own basis sets, no ghost atoms, same exact geometry.
It is a stated reference convention, not counterpoise-corrected energy decomposition.
Internal/external determinant stability and electron quadrature are recorded for
complexes and frozen fragments. Instability of a frozen restricted reference does
not make it a verified ground state. Stability alone does not exclude static
correlation; no multireference diagnostics were performed.

Mayer index: sum (PS)μν(PS)νμ across AO atom blocks, occupation-weighted P.
Löwdin Wiberg: sum |S½PS½|² across atom blocks. Both are basis-dependent
indices, neither integer bond counts nor an NBO analysis. Six bond pairs include
the two forming bonds, three original π bonds and emerging middle π bond.

The first complex occupied and virtual orbital choices maximize projections from
frozen diene HOMO and ethylene LUMO respectively. Subsequent canonical orbitals
are assigned one-to-one within occupied/virtual blocks by absolute cross-geometry
AO-metric overlap (Hungarian assignment), then phase aligned. Low overlap or a
larger alternative is flagged. Near-degenerate canonical partners are gauge
dependent; no unique localized donor/acceptor or degenerate-subspace tracking is
claimed. Orbital probability |φ|² excludes the occupation factor; total density
sums all occupied contributions.

## Separate symmetry laboratory

Frozen neutral s-cis butadiene HOMO and ethylene π* LUMO are independently
computed at the TS geometry in their own fragment bases. Their actual grids,
coefficients, indices and selected two forming-region midpoint amplitudes are
stored in `symmetry-fields.npz` and metadata. A simultaneous display is a drawing
of two separate fields, not a normalized complex orbital. Relative phase is
chosen to make the first midpoint product positive; the second has the same sign.
A global sign reversal leaves observables unchanged. Midpoint products are local
amplitude samples (bohr⁻³), not a coupling energy or bond-order observable.
Whole interfragment orbital overlap is dimensionless and nonzero because the
fragment bases are not mutually orthogonal.

This supports a suprafacial–suprafacial thermal [4+2] orbital-symmetry account.
It does not by itself demonstrate concertedness, rates, selectivity or a complete
reaction path. Teal/amber distinguish field sign, never electrical charges.

SORG 1333 uses S1 (closed-shell electron pairs), O3 (concerted cyclic interaction),
R3 (multiple-bond reorganization), G3 (collective geometric reorganization).
S3 means excited state/state change in the authoritative codebook. Existing
inherited/consistent-with-convention assignment statuses remain unchanged.

Primary implementation documentation:
https://pyscf.org/user/dft.html
https://pyscf.org/user/geomopt.html
https://pyscf.org/pyscf_api_docs/pyscf.scf.html#module-pyscf.scf.stability
https://geometric.readthedocs.io/en/latest/transition.html

Stationary verification uses all Cartesian gradients (max component <2e-4 Eh/bohr) and full analytic RKS Hessians; actual residuals are reported in the audit. Default PySCF grid-response approximations are retained and no grid-convergence study is claimed. The imaginary Cartesian mode is scaled to Σ|v|²=1; r(s)=r(TS)+s v with s in Å defines reported dimensionless bond-distance derivatives. This local direction is not an IRC.

The idempotent enrich.py independently projects retained nuclear gradients off the two distance-constraint Jacobian rows: g_free = g − Jᵀ(JJᵀ)⁻¹Jg. Its max component is reported; no Hessian or energy is inferred by this projection.

File ids pre-ts/post-ts name the long-/short-distance constrained inputs relative to the saddle distance; they do not imply IRC endpoint connectivity. UI labels state actual constrained distances.

Original-release check: the 1.9 Å input had a projected residual about 7.90e-4 Eh/bohr and was labeled partially relaxed. The r1 follow-up replaces it with a fresh-grid independently checked constrained geometry; see V037_FOLLOWUP_AUDIT.md. This does not make the point stationary or establish IRC connectivity.

## r1 short-distance update

Recheck the exact retained candidate with `python research/diels-alder/refine_short_distance.py --checkpoint`, then run `fields.py --refresh-tail`, `enrich.py`, `validate.py`, `build_reaction_systems.py`, and `npm test`. Omit --checkpoint to optimize anew from short-distance-seed.xyz / short-distance-seed-scf.npz. The original recorded run used ftol=1e-12/maxiter=80 and was stopped after the physical force target was met; --original-options selects those original optimizer options. Default reruns use an explicit force stop. Full moving-grid gradients drive the new optimization; final acceptance also requires the original default-gradient target to pass after alignment. Method, basis, electron count, volumetric grid and references are unchanged. The historical frozen-fragment stability warnings remain applicable.
