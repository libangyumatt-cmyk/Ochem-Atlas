# v0.3.7 r1 — constrained-point verification follow-up

This supplements [the original v0.3.7 audit](V037_AUDIT.md). The original release
(commit 2563ff690412fbdb243cf8339e6de573364d8b16) correctly labeled its 1.9 Å
input partially relaxed. This update replaces that input with an independently
verified constrained geometry. The original coordinates and SCF guess remain
in short-distance-seed.xyz / short-distance-seed-scf.npz and the original full
release remains available in Git history. No reaction, event, SORG assignment,
lesson, citation or pre-v0.3.7 quantum dataset is removed.

## Calculation actually completed

Same neutral singlet C6H10, 46 electrons, gas-phase restricted B3LYP (VWN-RPA)/
6-31G(d), PySCF 2.14.0; same level-3 integration grid and common display grid.
SLSQP optimized Cartesian coordinates with two C–C distances fixed at 1.9 Å.
Centroid translation and linear Eckart rotation gauges fixed the laboratory
frame. Every trial used a fresh SCF object and rebuilt atom-centered grid;
optimization gradients included full moving-grid response. SCF trial tolerances
were 1e-11 Eh / 3e-7 orbital-gradient norm.

The recorded optimizer used ftol=1e-12 and maxiter=80. After completed evaluations
had a projected moving-grid gradient below 1e-5 Eh/bohr, the latest genuine SCF
checkpoint was retained and independently verified. **No SciPy optimizer-success
status is claimed for that interrupted run.** Acceptance rests on fresh final
SCFs and both independent projected-gradient conventions, not termination text.
The stored candidate permits exact input reproduction. The default rerun script
has an explicit force stop; --original-options restores the original optimizer
options. The remaining SCF tolerances, method and constraints are documented in
the source and machine-readable refinement record.

After alignment to the unchanged TS skeleton, an independent SCF and gradients
gave:

- Default PySCF projected nuclear gradient: **2.28652287e-05 Eh/bohr**.
- Full moving-grid-response projected gradient: **4.40074946e-06 Eh/bohr**.
- Maximum distance-constraint error: **6.68431532e-10 Å**.
- Original independent acceptance target: 3e-4 Eh/bohr, unchanged.

Both conventions now meet that target. This is a constrained point, **not a
stationary point, transition state or IRC**. The cause of the initial optimizer/
independent-force discrepancy is not uniquely established by this improvement.
No grid/basis/functional convergence or multireference benchmark is added.

| Frame | E / Eh | Distance-projected gradient / Eh bohr⁻¹ | Becke electrons |
| --- | ---: | ---: | ---: |
| approach | -234.5641659546 | 1.111751e-04 | 46.00000263 |
| pre-ts | -234.5466974672 | 1.507430e-04 | 45.99999843 |
| ts | -234.5393639484 | 7.700899e-06 | 46.00000012 |
| post-ts | -234.5818063032 | 2.286523e-05 | 45.99999740 |
| product | -234.6439706983 | 1.952053e-05 | 46.00000134 |

## Updated fields and correspondence

The 1.9 Å SCF, total density, geometry-referenced density difference, frozen-
fragment deformation density, bond distances and Mayer/Löwdin Wiberg indices were
recomputed. Canonical orbital assignment was rebuilt from the unchanged TS
parent through the new short-distance geometry to the product. Product fields
were evaluated consistently with that correspondence. No orbital, density or
energy interpolation is substituted for calculation.

The original approach, 2.5 Å and TS wavefunctions/fields, symmetry teaching
surfaces, TS Hessian and independently verified product coordinates, energy,
wavefunction and Hessian are protected by audit/V037_R1_PRESERVED_DATA.json.
The 31 reactions / 69 events and all earlier-system datasets remain protected by
the original preservation tests. The two-distance projected force is
`g_free = g − Jᵀ(JJᵀ)⁻¹Jg`, where J has the two Cartesian distance Jacobian rows.
Both default and full moving-grid-response gradients are retained in the updated SCF NPZ.

Unchanged reference conventions: rho(current) − rho(approach) on the same aligned
Cartesian grid includes nuclear displacement; deformation subtracts same-geometry
neutral singlet fragments in their own bases, no ghosts. Signed colors denote
field sign, not electrical charge. Restricted frozen-fragment instabilities remain
reported and warned; they are not erased by this geometry improvement.

## Verification and interface

The independent validator reconstructs AO field samples, electron and orbital
normalizations, bond distances, both bond-index definitions, both projected-force
checks, symmetry checks and retained Hessian frequencies. Its result is **pass**.
All three constrained points now meet the original independent force target, so
the partial-relaxation warning is removed. Scientific limitations about IRC,
fragment references, correlation and numerical grids remain. Small gradient
values display in scientific notation rather than rounding to 0.0000.

A new Node-only archive check tests complete ZIP directories, decompression,
NPY headers and CRCs for every NPZ under reaction-lab and orbital-files. It also
rejects deliberately truncated and corrupted temporary test archives. This was
motivated by a truncated local working copy, restored from the verified published
Git blob; no public dataset corruption is inferred. Volumetric regeneration now
writes through a temporary file and atomic replacement, retaining the last complete
file if generation is interrupted.

Automated regression tests, source packaging and actual-coordinate/mesh visual
checks accompany this update. Desktop controls are checked after publication.
Native hardware WebGL and mobile touch are not certified by cloud-browser static
projection or DOM tests. **No IRC was performed.**

## Reproduction

```sh
OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 python research/diels-alder/refine_short_distance.py --checkpoint
OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 python research/diels-alder/fields.py --refresh-tail
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/diels-alder/enrich.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/diels-alder/validate.py
python build_reaction_systems.py
npm test
```

To optimize anew from the preserved original input, omit --checkpoint. To repeat
the original optimizer options, use --original-options. The selected published
geometry is explicitly retained independently of optimizer iteration history.
