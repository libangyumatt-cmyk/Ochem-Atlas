# Ochem Atlas v0.3.7-r2 — validation in progress

**Status: incomplete; no validated IRC or r2 release is claimed.**

The reproducible published starting point is commit
`ac2271ddefd16cc0823a961e8c6a65ea30c60ed0` (v0.3.7-r1).
All existing reactions, events, SORG assignments, mechanisms and calculated
datasets are retained. The original Diels–Alder series remains a constrained
study, with separately verified saddle/minimum structures. It is not an IRC.

## Recovery and missing prior outputs

On October 22, 2026 (America/Los_Angeles), continuation found the previous
uncommitted workspace removed by automated workspace maintenance. A Library
recovery search found no r2 calculation archive. Earlier chat reports of IRC
convergence, soft imaginary endpoint modes and method comparisons have **not**
been recovered as original inputs/outputs. Those reported numerical values are
not reproduced here as independently verifiable release evidence. Previously
completed calculations must be regenerated before being included in a release.
The original r1 repository was re-cloned unchanged.

## Restart protocol

`research/diels-alder/r2/irc.py` starts from the retained r1 verified saddle
and its full analytic Hessian. System: neutral singlet C6H10, 46 electrons,
restricted B3LYP (PySCF VWN-RPA)/6-31G(d), isolated gas phase, integration
grid level 3. No solvent, dispersion, ZPE or thermal correction is added.

The restart uses geomeTRIC 1.1.1 Gonzalez–Schlegel mass-weighted internal-
coordinate IRC with full moving-grid-response analytic nuclear gradients.
Each trial rebuilds the grid and uses a fresh SCF object. SCF energy convergence
1e-10 Eh, orbital-gradient threshold 1e-6, maximum 120 cycles.
Initial/maximum Cartesian trust radius 0.05 Å; minimum 0.005 Å; maximum
160 optimizer iterations per direction. DLC coordinates and BFGS Hessian
updates are used without forming-bond constraints. Nuclear convergence:
energy change 1e-7 Eh, RMS/max atomic force 3e-5/8e-5 Eh/bohr,
RMS/max displacement 0.0006/0.001 Å.

The mass metric is the program's element-mass-weighted Cartesian metric;
Cartesian displacements are in bohr and masses in amu. The initial step scale
is trust/bohr-per-angstrom times the norm of sqrt(mass) times the normalized
imaginary Cartesian mode. Accepted/rejected steps and the switch to ordinary
endpoint optimization are recorded separately. The initial Hessian retains
the r1 default grid-response approximation; a full moving-grid-response
Hessian has not been computed. Algorithmic convergence does not establish
minimum-to-minimum connectivity.

Every trial saves actual coordinates, energy, gradients, SCF status and electron
count. The latest full wavefunction is checkpointed; raw trial files are
retained in lossless CRC-checked ZIP archives every five evaluations. No
uncomputed geometries, energies or electron fields are interpolated or fabricated.

## Completed validation at this checkpoint

Repository recovery, source inspection, Python driver syntax checks and the
existing full `npm test` regression suite passed at this checkpoint. Two new
IRC jobs have been launched; their convergence and independent validation remain
**pending**. Independent endpoint Hessians, selected IRC electronic fields,
method/basis/grid sensitivity and r2 release deployment are also pending and
must be recorded individually when completed.
The protected-file manifest is `audit/V037_R2_PRESERVED_DATA.json`.

## Reproduction

Install PySCF 2.14.0 and geomeTRIC 1.1.1 in Python 3.12. From the repository:

```sh
export OCHEM_R2_OUTPUT=/tmp/ochem-r2-independent-restart
OCHEM_THREADS=3 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/irc.py forward
OCHEM_THREADS=3 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/irc.py backward
```

The driver refuses to overwrite an existing attempt. Ordinary endpoint
optimization records are not IRC samples. A finite-distance encounter complex
must not be labeled infinitely separated reactants. No “Validated IRC” series
will be exposed until independent endpoint and path verification passes.

SORG 1333 remains S1 paired, O3 cyclic cooperative organization, R3 multiple-
bond redistribution and G3 collective geometry. S3 denotes excited/state change.
Orbital symmetry teaching models remain distinct from path evidence. Concerted
and strictly synchronous bond formation are different assertions; neither a
single orbital picture nor an imposed equal-distance scan establishes both.

Remaining work includes stable endpoint connectivity, density/orbital field
generation and correspondence, defined bond indices, basis/correlation/grid
sensitivity, regression and published interaction checks. No overlap is
converted to an orbital interaction energy. A limited comparison cannot
establish method or basis convergence.

## Saved restart checkpoint

The first three ethylene fixed-geometry comparisons (B3LYP grid5,
B3LYP/def2-TZVP, RI-RMP2/def2-TZVP) completed with internally and externally
stable references. Independent coefficient normalization, AO electron-count,
density-matrix and correlation-energy reconstruction passed. Both IRC
branches remain running; their trial outputs and latest wavefunctions are
checkpointed, not validated laboratory frames. See checkpoint-state.json and
restart-20261022/comparisons/validation.json. The protected manifest covers 373
original scientific payloads; mutable Diels–Alder system/index wrappers are
excluded so later explanatory metadata can be updated without changing inputs.
