# Ochem Atlas v0.3.7-r3 — IRC recovery and validation

Scientific status: **IRC validation incomplete**. Stage A recovery and Stage B
forward-endpoint diagnosis are complete. Stage C has started, but no converged
backward branch or complete minimum-to-minimum IRC is claimed at this checkpoint.
Stages D–F remain pending; no r3 release deployment is claimed.

## Stage A — recovered and independently checked

Recovery ran on 2026-10-25 from baseline
`d2abc2355505c4b30dc9d91917c80aad8ee34d0e`. All retained r2 ZIP/NPZ archives passed
CRC checks, and numerical arrays were finite. The independent Node reconstruction
passed 31 wavefunctions and 145 documented accepted IRC points, including orbital
metric normalization, electron counts, density-matrix Hermiticity and four
negative directional energy curvatures. All 373 protected original scientific
payload hashes matched. All 31 reactions, 69 events, SORG assignments, mechanisms,
lessons, citations and original datasets remain preserved.

Inventory and SHA256 hashes: `audit/V037_R3_RECOVERY.json`.

- Forward: 45 archived trials, 39 documented accepted IRC points; historical
  driver convergence retained. Latest wavefunction matches archived evaluation45.
- Backward: 112 archived trial JSON records, 106 documented accepted IRC points;
  the historical report counted111 evaluations. Last documented accepted point
  is evaluation111, forming distances3.9255223898/4.1335775794 Angstrom.
- Backward latest-wavefunction geometry matches no archived trial. It has no
  accepted-point provenance and is not used as a verified IRC continuation point.
- No full r2 optimizer/internal-coordinate/BFGS/IRC state was retained. A faithful
  continuation from the last coordinates alone is unsupported. Historical status
  files are not evidence of currently running jobs.
- Seven complete method-comparison analyses remain retained. They are not
  repeated or extended for this connectivity investigation.

## Stage B — completed: forward endpoint has a conformational instability

The original forward endpoint remains unchanged: E=-234.6348399934745 Eh,
maximum full-response force7.797064832e-6 Eh/bohr, stable internal/external
SCF tests, and one imaginary vibrational mode. Independent symmetrized-Hessian
reconstruction gives31.7901851921i cm^-1. Ring torsional derivatives identify a
ring-puckering/twisting direction (`audit/V037_R3_MODE.json`). R2 retained actual
finite-energy probes with negative curvature at grids3 and5; the small frequency
was not discarded as harmless.

Separate starting geometries used +/-0.15 Angstrom total Cartesian-norm
 displacements along the retained normalized imaginary mode. These are ordinary
unconstrained endpoint relaxations, not additional IRC points.

| Relaxation | Electronic energy / Eh | Max full-response force / Eh bohr^-1 | Lowest vibration / cm^-1 | Minimum check |
| --- | ---: | ---: | ---: | --- |
| plus | -234.643965021640 | 4.06047e-06 | 166.94186317 | verified |
| minus-retry1 | -234.643964947088 | 3.89906e-06 | 166.94439636 | verified |

Both have positive projected vibrational frequencies, stable internal/external
SCF solutions and correct mapped cyclohexene carbon/hydrogen connectivity.
Optimization used46 positive-displacement SCF/gradient evaluations and48 in the
negative retry, plus independent final verification calculations.

The initial negative run stopped after two converged evaluations because the
checkpoint pickle round-trip encountered recursion in geomeTRIC Molecule
serialization. This was a workflow failure, not chemical convergence failure.
Its failure record and outputs are preserved in `endpoint-minus`. Explicit
Molecule state serialization fixed the failure. `endpoint-minus-retry1` is a
new ordinary optimization from that saved geometry/density, not a claimed
faithful continuation of its old optimizer state.

Independent comparisons (`audit/V037_R3_STAGE_B.json`):

- Positive: forming distances1.5375065050/1.5375948020 Angstrom. Proper-rotation
  carbon RMSD to independent r1 product0.3955316942 Angstrom; same-carbon H
  permutations reduce all-atom RMSD from1.2000283612 to1.0443072704 Angstrom.
  Reflected-reference diagnostics give carbon RMSD0.0004680412 and equivalent-H
  all-atom RMSD0.0012201115 Angstrom, consistent with a mirror-related ring
  conformation. Reflection is reported separately and never counted as a proper
  rotation or hidden atom-map change.
- Negative: forming distances1.5376030957/1.5375060961 Angstrom; carbon RMSD
  0.0006376327 Angstrom. Equivalent-H all-atom RMSD0.0016158519 Angstrom, compared
  with raw fixed-H-label RMSD0.8782556601 Angstrom. Its reflected reference has
  a large RMSD, consistent with the opposite ring conformation.
- Energy excesses over independent r1 product are5.676702614e-6 and5.751253724e-6
  Eh, respectively. These limited comparisons do not establish grid convergence.

The two relaxed minima and retained negative energy curvature support a genuine
model-level ring conformational instability. The old forward IRC endpoint is
not relabeled as a minimum. Subsequent relaxations are not relabeled IRC
geometries. No precise valley–ridge bifurcation location has been calculated.
A first-order reaction saddle plus these relaxations does not by itself certify
a strict two-minimum IRC.

## Stage C — fresh backward driver; convergence pending

`research/diels-alder/r3/backward.py` starts a fresh driver at the verified TS.
It can reuse an actual r2 SCF/gradient evaluation only when the requested
geometry differs by at most1e-12 bohr per Cartesian component. Reused rows retain
the original coordinates, energy, gradient and source evaluation number. No new
wavefunction is claimed for a reused row. A cache miss performs a new calculation.

The TS evaluation was reused. The next requested geometry differed from r2 by
4.418273125e-8 bohr, so it failed the strict cache test and was freshly computed.
The tolerance was not relaxed to assign old electronic results to new geometries.
Initial forming-distance changes confirm the physical reactant direction; the
arbitrary imaginary-mode sign is not a chemical identifier.

The first independent checkpoint check passed descent, mapping/provenance,
electron counts, density-matrix Hermiticity and orbital normalization for
11 evaluated geometries (one reused, ten new). This is not a convergence claim.
Current outputs are under `r3/backward-attempt1/backward`; only saved, independently
checked milestones should be counted as retained evidence. No promise of continued
execution after an interruption is made. New SCF wavefunctions and full optimizer
states are saved atomically after meaningful evaluations.

## Model and numerical conventions

Neutral singlet C6H10,46 electrons; isolated gas-phase restricted B3LYP(VWN-RPA)/
6-31G(d). Atom map: dieneC1–C4, ethyleneC5–C6, H7–H16. Forming pairsC1–C5 and
C4–C6. Energies are Born–Oppenheimer electronic totals including nuclear repulsion,
in Eh. No solvent, dispersion, ZPE, thermal or free-energy correction is added.

PySCF2.14.0, geomeTRIC1.1.1, NumPy2.3.5, SciPy1.17.0; Python3.12.
Fresh level3 grids at every new SCF trial; SCF energy tolerance1e-10 Eh,
orbital-gradient threshold1e-6, maximum120 cycles. Optimization gradients include
full moving-grid response. Final full all-coordinate analytic Hessians use
PySCF's default grid-response approximation, not a full moving-grid-response
numerical Hessian. Frequencies are reconstructed from(H+H^T)/2 with external
translation/rotation projected out. Neither full Hessian-response nor grid/basis/
correlation convergence is claimed.

Endpoint DLC optimization: initial trust0.05 Angstrom, maximum0.1, maximum100
iterations; energy1e-9 Eh, RMS/max forces3e-6/1e-5 Eh/bohr, RMS/max displacement
0.0001/0.0003 Angstrom. All criteria must pass before final verification.
Positive run used three OpenMP threads, negative retry two, BLAS one.

IRC: geomeTRIC Gonzalez–Schlegel mass-weighted internal-coordinate algorithm,
DLC, no forming-bond constraints, initial/maximum trust0.05 Angstrom, minimum
0.005, maximum160 iterations, subfrctor2; energy1e-7 Eh, RMS/max forces
3e-5/8e-5 Eh/bohr, RMS/max displacement0.0006/0.001 Angstrom. Initial r1 analytic
Hessian is retained with its default-response approximation; later BFGS updates
are not fresh exact Hessians. Masses and coordinate metric are retained in the
r2 path-validation convention and copied into r3 independent validation: Cartesian
bohr, element masses in amu, cumulative sum sqrt(sum_i m_i|delta r_i|^2).
This is a discrete chord length in bohr sqrt(amu), not exact continuous arc
length, interpolation, or a real-time trajectory. Ordinary endpoint-optimization
steps are excluded from accepted IRC samples. Descent tolerance is3e-6 Eh per
accepted step. Endpoint minimum/connectivity checks are separate.

## Reproducibility and checkpoint recovery

From repository root, create a separate Python3.12 environment:

```sh
python3.12 -m venv .venv
.venv/bin/pip install pyscf==2.14.0 geometric==1.1.1 numpy==2.3.5 scipy==1.17.0
python research/diels-alder/r3/recover.py
node verify-diels-alder-r2-numerical.cjs
OPENBLAS_NUM_THREADS=1 .venv/bin/python research/diels-alder/r3/check_restart.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python research/diels-alder/r3/check_replay.py
```

Use distinct new output directories; drivers refuse to overwrite existing inputs:

```sh
export OCHEM_R3_OUTPUT=/tmp/ochem-r3-independent-endpoints
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=2 .venv/bin/python research/diels-alder/r3/endpoint.py plus
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=2 .venv/bin/python research/diels-alder/r3/endpoint.py minus
OPENBLAS_NUM_THREADS=1 .venv/bin/python research/diels-alder/r3/validate_endpoint.py plus
OPENBLAS_NUM_THREADS=1 .venv/bin/python research/diels-alder/r3/validate_endpoint.py minus
export OCHEM_R3_BACKWARD_OUTPUT=/tmp/ochem-r3-independent-backward
OPENBLAS_NUM_THREADS=1 OCHEM_THREADS=2 .venv/bin/python research/diels-alder/r3/backward.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python research/diels-alder/r3/validate_backward.py
```

The published negative retry retains its actual restart history; an independent
fresh negative run need not reproduce that workflow failure. No bitwise
reproducibility across BLAS/grid/hardware implementations is guaranteed.

CRC-checked milestone ZIPs preserve completed trial JSON/logs and matching
wavefunctions. Important writes use temporary-file replacement. The corrected
workflow additionally preserves optimizer pickle plus SHA256 metadata after
examined steps; X/G/H, state, iteration, evaluation count and density matrix are
round-trip checked. A fresh-process interrupted analytic stretch test passed and
matched parent-process continuation (`audit/V037_R3_RESTART_TEST.log`). Strict
cache tests passed (`audit/V037_R3_REPLAY_TEST.log`). These are workflow checks,
not electronic-structure validation. Pickle is executable trusted-local input:
never load an untrusted file. Version-specific modules and original directory
layout are required for optimizer continuation; portable independent repeats
use the fresh-output commands above.

## Tests, scope and remaining work

Full original npm regression passed on2026-10-25; actual log:
`audit/V037_R3_REGRESSION.log`. It covers catalog/event preservation, scientific
assets and SN2/carbonyl/Diels–Alder DOM interactions. This does not certify native
mobile touch, WebGL rendering or published desktop behavior; those require
separate release checks. No new interface or orbital/density series has been
integrated at this checkpoint.

Remaining sequential work: finish backward convergence and independent endpoint
assessment; compare both chemical regions and classify strict IRC connectivity;
generate limited electronic fields only if those checks justify it; then compact
status integration, final regression and release verification. Finite-distance
encounter structures must not be called infinitely separated reactants.

SORG1333 remains unchanged. Concerted bond formation is distinct from strict
synchronicity, and a constrained equal-distance scan cannot establish either a
complete IRC or unique orbital interaction energies. No interaction energy is
inferred from overlap, and no uncomputed electronic fields are interpolated.
