# v0.3.7-r4 — Diels–Alder IRC path repair

**Scientific outcome: 2 — connectivity supported but numerical integration remains unresolved.**
No strict IRC certification or new electronic-field series is claimed. This is a
diagnostic release; a complete independent TS-to-endpoint integration and endpoint
verification of the repaired tail remain incomplete.

## Backward failure: completed diagnosis

R3 state23 was strictly replayed through evaluations24–138:115 cached evaluations,
zero new SCFs and zero Cartesian residual at every requested geometry. This
reconstructs states135/138, including DLC coordinates, BFGS matrix, gradients,
trust radii and IRC state. They are reconstructed states, not directly retained
r3 snapshots. Pickles are version-specific executable trusted-local inputs.

The retained gradient trapezoid predicts +5.8120295606e-6 Eh for135→138, versus
the observed +5.8087003936e-6 Eh. Eight fresh tight-SCF probes independently
recalculated135/138 and +/-0.001 bohr total Cartesian displacements at138 along
the normalized135→138 direction:

| Grid | Recomputed uphill energy / Eh | Central difference minus analytic gradient / Eh bohr^-1 |
| --- | ---: | ---: |
| 3 | 5.8086988588e-6 | 6.10497e-10 |
| 5 | 5.6636159229e-6 | 1.60637e-9 |

SCF tolerances:1e-12 Eh and1e-7 orbital gradient; maximum120 cycles. Full moving-grid
response nuclear gradients; restricted B3LYP(VWN-RPA)/6-31G(d), neutral singlet
C6H10,46 electrons. Both grids reproduce a rise above the unchanged3e-6 Eh
validation threshold. Finite differences support the analytic gradients. Evidence
favors integration overshoot and minimum-radius forced acceptance, not random
SCF noise; coordinate-representation/BFGS effects are not separately isolated.
These comparisons do not establish grid or basis convergence.

## Smaller-step trials: completed local tests, incomplete global repair

All trials start from reconstructed accepted state135. A0.001 Angstrom trust cap
produces +6.6448507141e-8 Eh; a0.0005 cap produces -9.4835229447e-8 Eh. Both meet
the fixed external descent bound but are rejected by geomeTRIC's quality model.
Neither is silently substituted into the original path.

Continuation of the latter state, with minimum/maximum trust0.00005/0.0005 Angstrom,
accepts one step with -6.3504785430e-8 Eh and declares driver convergence. This
shows termination depends on the integration/stopping settings. The new terminal
geometry has not received an independent endpoint optimization/Hessian check.
It is not a certified replacement endpoint or complete repaired IRC. Original
r3 forced evaluation138 and all rejected trials remain preserved.

## Independent integration: bounded initial segment completed

An independent Cartesian mass-weighted normalized Euler integrator with Armijo
backtracking starts from the retained verified TS. Coordinates are
q_i=sqrt(m_i/amu) R_i/bohr; gradients g_q=g_R/sqrt(m_i/amu), using the retained
geomeTRIC element masses. The first displacement is0.0200000000000 bohr sqrt(amu)
along the negative mass-weighted Hessian eigenvector, oriented toward increasing
forming distances. Its independently reconstructed mode overlap is1.0000000000.
The exact r3 SCF geometry is reused at the starting TS rather than assigning its
energy to a slightly different unit-converted geometry.

Eight fresh grid3 SCF/gradient evaluations produce six accepted descending steps
and two rejected trials. Armijo coefficient1e-4; initial step0.02, halved to0.01
and0.005 bohr sqrt(amu). Both forming distances increase from approximately2.27644
to2.28067 Angstrom over the retained segment. Every accepted step lowers energy.
This is only a feasibility/initial-segment test. The reduced step illustrates
stiffness; full endpoint connectivity, step-refinement convergence and a complete
independent path comparison have **not** been calculated. No full-IRC conclusion
is inferred from these six steps.

The first SCF was recovered from its saved wavefunction after a NumPy-boolean
JSON serialization failure. Its geometry and log were checked; it was not
recomputed. Workflow failures are not chemical convergence failures.

## Forward conformational analysis

A targeted calculation at actual forward IRC evaluation7 (forming distances
2.0502386427/2.0457092267 Angstrom) transports the original endpoint's ring mode
by a proper-rotation Kabsch alignment with fixed atom mapping. Three tight-SCF
energies at0 and +/-0.01 Angstrom total Cartesian displacement give directional
curvature +0.00657500729168 Eh/bohr^2. The center energy reproduces the retained
IRC value within3.07e-12 Eh. The retained endpoint direction has negative curvature
at grids3/5 from r2, and r3 independently verified both relaxed cyclohexene minima.
Those completed minima were reused without recalculation.

The curvature comparison supports changing ring conformational behavior along
the calculated branch, but it is one transported direction, not an eigenvalue
spectrum or localization of a valley–ridge bifurcation. No VRI claim is made.
The displaced probes and subsequent unconstrained optimizations are not IRC points.

## Interpretation and remaining work

The original TS, finite reactant encounter minimum and relaxed product minima
support the intended chemical regions. Strict reaction-path connectivity requires
successful integration and endpoint checks, not only a first-order saddle or
converged driver. Concertedness describes a mechanism without a discrete
intermediate; synchrony describes relative bond-formation progress. Neither is
established solely by equal-distance constraints or a few descending points.
SORG1333 remains unchanged; no orbital interaction energy is inferred from overlap.

Remaining work: independently follow both full branches with controlled integration
error; diagnose the DLC/BFGS quality-model rejection separately; verify the new
terminal geometry against retained minima; characterize forward path topology
with sufficient Hessian information if a bifurcation is proposed. Only after
those checks may selected IRC orbital/density/bond-index fields be generated.
Stage electronic-structure expansion is deferred in its entirety.

## Reproducibility and verification

Python3.12, PySCF2.14.0, geomeTRIC1.1.1, NumPy2.3.5, SciPy1.17.0; OpenBLAS1 thread,
OCHEM_THREADS2 for new calculations (strict replay used1). Atom map and electronic
energy conventions remain those of r3: C1–C4 diene, C5–C6 ethylene, H7–H16;
energies include nuclear repulsion, with no ZPE, free energy, solvent or dispersion
correction. All writes/checkpoints use temporary replacement and archive CRC checks.

New raw outputs are packaged in `reaction-lab/diels-alder/r4/calculations.zip`
with per-file SHA256 manifest. Extract it to the same r4 directory before running
validators. Existing successful cases are reused. To repeat a driver from scratch,
use an isolated checkout/output copy; scripts refuse conflicting existing inputs.

```sh
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=2 python research/diels-alder/r4/diagnose.py
OPENBLAS_NUM_THREADS=1 python research/diels-alder/r4/validate.py
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=1 python research/diels-alder/r4/reconstruct.py
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=2 python research/diels-alder/r4/repair.py .001
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=2 python research/diels-alder/r4/repair.py .0005
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=2 python research/diels-alder/r4/continue_repair.py
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=2 python research/diels-alder/r4/independent.py ts
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=2 python research/diels-alder/r4/forward.py
OPENBLAS_NUM_THREADS=1 python research/diels-alder/r4/validate_release.py
npm test
```

Independent checks passed for22 new wavefunctions: AO-metric orbital normalization,
46-electron counts, finite arrays, CRCs, stored energy/geometry matching, negative-mode
alignment, accepted-segment descent and forward curvature reconstruction. All364
retained Diels–Alder files match the r3 baseline byte for byte; the original373-file
preservation regression covers prior scientific payloads. All31 reactions,69 events,
SN2/carbonyl functionality, mechanisms, lessons and citations remain preserved.
Browser testing remains limited by the previously documented sandbox launch denial;
no new native/mobile/WebGL success is claimed. Release CI/deployment evidence will
be reported only after checks complete. No unfinished job is claimed to continue.

Release checks: the full existing npm suite passed after status integration. The
added dependency-free archive check validates every archived SHA256/CRC, inner NPZ
CRCs, bounded-segment descent, rejected trust trials, numerical-gradient checks
and all364 prior-data hashes. Actual regression output: audit/V037_R4_REGRESSION.log.
Full Pages build and deployment passed on 2026-11-01; confirmed evidence follows.

## Confirmed publication

Diagnostic release commit: `57ff2f3aa0a978823deacc7736cbda8f0ba9c533`.
Validation passed: https://github.com/libangyumatt-cmyk/Ochem-Atlas/actions/runs/41290465691 .
Pages build and deployment passed: https://github.com/libangyumatt-cmyk/Ochem-Atlas/actions/runs/41290465677 .
Published URL: https://libangyumatt-cmyk.github.io/Ochem-Atlas/?v=0.3.7-r4#reaction-lab .

These checks certify the release build, archive/preservation regressions and
deployment, not full independent IRC connectivity or native browser behavior.
The complete independent TS-to-endpoint path and repaired-terminal stationary-point
verification remain incomplete. No validated IRC electronic series is exposed.
