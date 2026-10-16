> **Follow-up:** the 1.9 Å point now meets the independent force target. See [V037_FOLLOWUP_AUDIT.md](V037_FOLLOWUP_AUDIT.md) for current checks and regenerated fields. The original-release audit below is retained as a historical record.

# Ochem Atlas v0.3.7 audit

## Scope and preservation

Adds one independently computed 1,3-butadiene + ethylene → cyclohexene case to
the same Reaction Orbital Laboratory. No reaction or taxonomy expansion:
31 reactions, 69 events. SN2, carbonyl, isolated-orbital datasets, conventional
mechanisms, lessons, scientific citations and assignments are retained.
`audit/V037_PRESERVED_DATA.json` records SHA256 of every pre-existing tracked
scientific file under research, reaction-lab, orbitals and mechanisms. Tests check
these bytes. The routing registry is intentionally extended; its original two
system records are compared against V037_SYSTEM_REGISTRY_BASELINE.json. Catalog
arrays/codebook/axes/sources were compared with v0.3.6.
29 conventional mechanisms remain complete, LAH partial and Grignard representative.

## Calculations actually performed

Neutral C6H10, charge 0, multiplicity 1, 46 electrons; restricted singlet
Kohn–Sham B3LYP (PySCF VWN-RPA convention)/6-31G(d), isolated gas phase.
Approximate exchange/correlation, no dispersion correction, solvent or counterion.
PySCF 2.14.0, geomeTRIC 1.1.1, NumPy 2.3.5, SciPy 1.17.0.
SCF energy tolerance 1e-10 Eh, orbital-gradient tolerance 1e-6; integration grid
level 3. Full Cartesian analytic nuclear gradients are evaluated; default PySCF
DFT atom-centered-grid response approximation is retained. Nuclear Hessians are
full analytic RKS Hessians, not a subset of selected coordinates. Numerical-grid
convergence was not established; do not infer spectroscopic frequency accuracy.
Stationary validation tolerance: max Cartesian force <2e-4 Eh/bohr plus full
vibrational analysis, with actual residuals reported below.

Independent unconstrained ethylene, butadiene and cyclohexene optimizations and
full Hessians were completed. The published product was rigidly aligned to the
TS before a final SCF and recomputed full Hessian. The initial direct TS search
was abandoned after it moved toward fragment separation; retained diagnostic
trajectory/logs are not a verified TS. A relaxed 2.25 Å two-distance constrained
seed was then used for an unconstrained full-dimensional saddle search.
The constrained seed itself is not a TS.

Verified saddle: max |Cartesian gradient| **1.032788e-05
Eh/bohr**, 1 imaginary vibrational mode(s),
frequency **-525.52 cm⁻¹** (negative denotes imaginary),
41 positive vibrational modes.
Verified product: max |Cartesian gradient| **2.047491e-05
Eh/bohr**, 42 positive modes, lowest
**166.53 cm⁻¹**.

Three other displayed geometries fix both forming distances at 3.0, 2.5 or 1.9 Å.
The 3.0/2.5 Å points meet the independent projected-gradient target of 3e-4
Eh/bohr. The 1.9 Å point does NOT: its independently recomputed projected
residual is about 7.90e-4 Eh/bohr despite optimizer termination. It is explicitly
retained as a partially relaxed constrained input, with a prominent UI warning,
not a fully optimized constrained point. The cause of that optimizer/final-check
discrepancy was not resolved. Actual SCF fields at its documented coordinates
remain valid as fixed-geometry model results. **No IRC or dynamics was performed.**
These points are not stationary points or independently verified minimum-energy
path frames. Equal-distance constraints impose synchronous bond distances;
they are not evidence that all Diels–Alder reactions are synchronous. The saddle's
unconstrained distance and bond-index asymmetry are checked independently.
Full endpoint connectivity has not been verified by IRC.

| Geometry | E / Eh | Forming distances / Å | Forming Mayer indices | Becke electrons | Internal / external stable |
| --- | ---: | --- | --- | ---: | --- |
| approach | -234.5641659546 | 3.00000 / 3.00000 | 0.02676 / 0.02676 | 46.0000026 | True / True |
| pre-ts | -234.5466974672 | 2.50000 / 2.50000 | 0.14213 / 0.14209 | 45.9999984 | True / True |
| ts | -234.5393639484 | 2.27348 / 2.27348 | 0.36124 / 0.36124 | 46.0000001 | True / True |
| post-ts | -234.5817705211 | 1.90000 / 1.90000 | 0.87383 / 0.87382 | 45.9999976 | True / True |
| product | -234.6439706983 | 1.53765 / 1.53762 | 1.01299 / 1.01298 | 46.0000013 | True / True |

Sum of optimized isolated-reactant electronic energies:
-234.5747035040 Eh. Saddle minus this sum:
22.176 kcal/mol; product minus sum:
-43.466 kcal/mol. These are model
electronic differences, not activation free energies, not experimental rates,
and not energies relative to the viewer's first constrained-complex reference.

## Density and orbital provenance

Every displayed frame retains Cartesian XYZ, SCF log, float64 MO coefficients,
occupations, eigenvalues, AO overlap, density matrix and actual gradient; full
Hessians/normal modes for stationary claims; float32 volumetric NPZ grids;
phase-aligned coefficients; mesh triangles at three explicit thresholds.
Grid: 81 × 71 × 71, 0.28 bohr, origin (−10, −9, −7) bohr, C order/z fastest.
Meshes use Å. Energy is Eh, density electron/bohr³, amplitude bohr⁻³ᐟ².
No calculated field, energy or geometry is interpolated in playback.

Final SCFs occur after proper least-squares alignment of the six mapped carbons
to the TS geometry. Identities C1–C6 and H7–H16 remain fixed. Density difference
is rho(frame) − rho(approach) on the identical grid: includes nuclear displacement,
not unique electron transfer. Deformation = rho(complex) minus frozen neutral
singlet butadiene and ethylene at the same coordinates, own basis sets, no ghosts.
It is not a unique partition or a counterpoise-corrected energy decomposition.
Unstable frozen restricted references: post-ts/butadiene, product/butadiene, product/ethylene.
These diagnostic tests do not exclude all electronic states or static correlation.

Tr(PS), CᵀSC and independent level-5 Becke quadrature validate normalization.
The coarse uniform grid under-resolves nuclear cores; its sum is disclosed,
not rescaled or used for charge-transfer integration. Boundary fields must lie
below the lowest displayed isovalue. Signed teal/amber mean positive/negative
field value, never electrical charge. Amplitude, single-orbital probability
(no occupation), total density, geometry difference and deformation are distinct.

Complex occupied/virtual orbitals start from frozen diene HOMO/ethylene LUMO
projections. Sequential Hungarian maximum-absolute cross-geometry AO-metric
assignment is done independently in occupied and virtual spaces, then sign
aligned. The overlap, competing candidate and ambiguity are shown. Near-degenerate
canonical partners are flagged; no unique localization or subspace tracking is
claimed. Kohn–Sham orbitals/eigenvalues are auxiliary model quantities.

## Orbital symmetry and SORG

The dedicated educational view uses real isolated-fragment canonical fields at
the TS frozen geometry: s-cis butadiene occupied HOMO and ethylene virtual π*
LUMO. It is independent of the geometry selector and explicitly labeled.
Separate fields may be drawn together; their display is not a normalized complex
MO. Two midpoint phase products and the nonorthogonal interfragment overlap
are documented, with coordinate units/sign convention and arbitrary relative
phase choice. Matching phases at both regions support the thermal suprafacial–
suprafacial [4+2] symmetry account, not a coupling energy, bond order, unique
interacting-orbital decomposition or proof of concertedness.

Authoritative 1333 = **S1 / O3 / R3 / G3**. S1 is closed-shell electron pairs;
S3 is excited-state/state change, and is not silently reassigned. Codebook
status remains inherited; the existing event remains consistent-with-convention.
SORG does not encode correlation, energy, electron density, numerical bond orders,
orbital gauge, reference convention or temporal synchrony. The old acrolein/
radical-cation literature dataset is preserved and distinguished from this case.

## Interface and verification

Three-system selection preserves each system's geometry, field, orbital and
threshold and keeps the conventional selected event synchronized. Six DA bonds
(two forming, three original π and middle emerging π) have distances, Mayer and
Löwdin Wiberg indices; discrete synchronized distance/index plots complement
energy, geometry and actual electronic surfaces. Three-system comparison retains
independent energy references. Orbital symmetry has separate fragment/isovalue/
phase controls. Existing SN2 and carbonyl controls remain available.

`validate.py` independently reconstructs retained-grid samples from AO coefficients,
checks density-difference references, recomputes all claimed Hessian frequencies,
checks 46 electrons and orbital normalization by Becke quadrature, atom mapping,
force residuals, symmetry tolerances and fragment counts. Report: validation.json
(result pass). `npm test` covers prior regressions and the third-system
selector, selection retention, six-bond plots, signed imaginary-mode metadata,
SORG wording, fragment-view availability and all mesh topology/source files.
Actual structure and isosurface renderings are inspected in
`research/diels-alder/validation-structures.png` and `validation-surfaces.png`.
Native mobile touch and hardware WebGL cannot be certified by jsdom or these
renders; v0.3.6 user testing does not certify this release. Published desktop
interaction and Pages workflow completion are checked after commit.

## Reproduction and remaining work

See [calculation README](research/diels-alder/README.md). Source, exact inputs,
constraint files, optimization/SCF outputs, fragment wavefunctions, Hessians and
volumetric grids are in dist/reaction-lab/diels-alder. No unperformed calculation
is presented as complete. Remaining: IRC connectivity, grid/basis/functional
convergence, higher-level correlation/multireference diagnostics, competing
asynchronous paths, ZPE/free energies, additional fragment partitions and native
mobile/WebGL testing. E2 and radical reaction datasets are not implemented.
