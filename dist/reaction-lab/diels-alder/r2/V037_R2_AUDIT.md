# Ochem Atlas v0.3.7-r2 — Diels–Alder scientific validation

**Scientific status: INCOMPLETE: endpoint/path verification pending or failed.**
Audit generated 2026-10-22T20:16:24.242897+00:00; this is an explicit
checkpoint of actual files, not a promise that pending calculations completed.
The original five displayed geometries remain separately calculated constrained
study/saddle/minimum data. No new “Validated IRC” selector has been exposed.

## Retention and recovery

All 31 reactions, 69 events, mechanisms, lessons, citations and SORG assignments
are preserved. The original r1 scientific inputs are from
ac2271ddefd16cc0823a961e8c6a65ea30c60ed0. The manifest protects 373 scientific
payload files, including prior SN2, carbonyl and Diels–Alder data and orbital
datasets; mutable Diels–Alder/index adapter wrappers are excluded.

The previous uncommitted r2 workspace was removed by automated maintenance.
Library recovery found no r2 output archive. Earlier chat-reported calculations
are not counted as recoverable release evidence. Every result tabulated below
comes from the newly retained restart-20261022 files. Code and actual early
outputs were committed before waiting for complete path validation.

## IRC calculations actually recorded

Neutral singlet C6H10, 46 electrons, ground-state restricted B3LYP (VWN-RPA),
6-31G(d), gas phase, integration grid3. No solvent, dispersion, zero-point or
thermal/free-energy corrections. Atom mapping is unchanged: diene C1–C4,
ethylene C5–C6, then H7–H16. Forming pairs C1–C5 and C4–C6.

geomeTRIC1.1.1 Gonzalez–Schlegel mass-weighted internal-coordinate IRC;
PySCF2.14.0; two separately run directions from the retained r1 verified saddle.
Each trial rebuilds its integration grid with a fresh SCF object; SCF tolerance
1e-10 Eh, orbital-gradient threshold1e-6, maximum120 SCF cycles. Full moving-grid-
response analytic nuclear gradients are used. The initial all-coordinate
analytic Hessian is retained from r1 and uses its default grid-response
approximation; subsequent BFGS updates do not constitute a newly computed
full-response Hessian.

DLC coordinates, no forming-bond constraints; initial/maximum trust0.05Å,
minimum0.005Å, maximum160 driver iterations. Convergence: energy1e-7Eh,
RMS/max force3e-5/8e-5Eh/bohr, RMS/max displacement0.0006/0.001Å.
Masses and cumulative coordinate convention are retained in path-validation.json:
geomeTRIC element masses (amu), Cartesian bohr, metric sqrt(sum m|delta r|²).
The reported cumulative chord length sums actual accepted point separations;
it is not an exact continuous arc length or an interpolated trajectory.
The initial step scale uses trust in bohr times ||sqrt(mass)*normalized
imaginary Cartesian mode||. Separate direction labels follow an arbitrary
mode sign, not a predefined chemical identity.

| Branch | Driver complete / converged | SCF-gradient evaluations | Accepted IRC points | Largest accepted energy increment / Eh | Last accepted forming distances / Å |
| --- | --- | ---: | ---: | ---: | --- |
| forward | False / False | 40 | 35 | 6.231678639778693e-08 | [1.5495974134474493, 1.5495240188278236] |
| backward | False / False | 41 | 39 | -0.00015182843003458402 | [3.416890970321173, 3.415692899316016] |

An independent numerical descent check permits at most3e-6Eh positive change.
Accepted/rejected steps are distinguished using retained program coordinates,
and each accepted point must match an actual SCF trial within1e-8bohr.
The driver's ordinary endpoint-optimization steps are explicitly excluded from
IRC samples. Driver convergence alone does not establish valid connectivity.

## Independent endpoint checks

Ordinary unconstrained endpoint relaxation uses fresh full moving-grid-response
gradients. Energy threshold1e-8Eh, RMS/max forces1e-5/3e-5Eh/bohr,
RMS/max displacement0.0003/0.0005Å; maximum80 iterations. Fresh final SCF,
all-Cartesian analytic Hessian, harmonic analysis and internal/external
determinant-stability checks follow. The Hessian retains PySCF's default grid-
response approximation: no full moving-grid-response numerical Hessian is
claimed. Minimum verification requires positive vibrational modes, max full-
response force<2e-4Eh/bohr and stable reference. It remains model/numerics dependent.

| Endpoint | E / Eh | Max full-response gradient / Eh bohr⁻¹ | Lowest frequency / cm⁻¹ | Internal / external stability | Minimum verified |
| --- | ---: | ---: | ---: | --- | --- |
| forward | pending | pending | pending | pending | pending |
| backward | pending | pending | pending | pending | pending |

Endpoint frequencies are independently reconstructed from retained full
Hessians. Cartesian inputs, orbitals, AO overlap/density matrices and gradients
are retained. Explicit carbon (1.85Å) and C–H (1.30Å) diagnostic connectivity
cutoffs and proper-rotation fixed-map RMSD comparisons with independent r1
minima are recorded separately when available. Those cutoffs are not bond-order
definitions. Equivalent-H labels and diene conformers can increase fixed-label
RMSD. No new isolated-reactant optimization or global conformer search is claimed.
A finite-distance encounter region is never called infinitely separated reactants.

Current unresolved path checks:
- forward driver convergence incomplete
- forward independent endpoint verification missing
- backward driver convergence incomplete
- backward independent endpoint verification missing

## Method, basis and integration-grid sensitivity

Completed fixed-geometry cases: 6/12. Independent retained-array
consistency result: partial;
independently checked cases: 6.
These are the unchanged independently optimized r1 geometries, not optimized
alternative-method stationary points. No alternative-basis TS Hessian/IRC,
geometry-convergence, multireference or coupled-cluster claim is made.

| Level | Completed geometries | TS-geometry energy excess / kcal mol⁻¹ | Product−reactants / kcal mol⁻¹ | All references stable | Scope |
| --- | --- | ---: | ---: | --- | --- |
| grid5 | 2/4 | unavailable | unavailable | unavailable | rather than infer missing results |
| def2tzvp | 2/4 | unavailable | unavailable | unavailable | rather than infer missing results |
| ri-mp2-def2tzvp | 2/4 | unavailable | unavailable | unavailable | rather than infer missing results |

Electronic references are the independent isolated s-trans butadiene and
ethylene minima, not the reactive s-cis deformation fragments or a universal
experimental activation baseline. Unstable references remain diagnostics only.
B3LYP grid5 uses6-31G(d); def2TZVP uses grid3. Native RI-RMP2/def2-TZVP
correlates all electrons, with explicit MP2 fitting basis and recorded RHF JK
fitting basis. MP2 one-particle densities are unrelaxed; their HF canonical
reference orbitals are not correlated natural orbitals or Kohn–Sham orbitals.
Finite comparisons do not establish basis, correlation or grid convergence.

| Actual case | Electronic energy / Eh | Reference internal / external stability | Tr(PS) electrons |
| --- | ---: | --- | ---: |
| reactant-butadiene-def2tzvp | -156.0575841180 | True / True | 30.000000000 |
| reactant-butadiene-grid5 | -155.9888805912 | True / True | 30.000000000 |
| reactant-butadiene-ri-mp2-def2tzvp | -155.6838878633 | True / False | 30.000000000 |
| reactant-ethylene-def2tzvp | -78.6236596746 | True / True | 16.000000000 |
| reactant-ethylene-grid5 | -78.5858252355 | True / True | 16.000000000 |
| reactant-ethylene-ri-mp2-def2tzvp | -78.4239307409 | True / True | 16.000000000 |

TS/product comparisons retain six Mayer and Löwdin-Wiberg bond indices,
same-geometry occupied/virtual canonical spatial matches, and actual density
differences on a0.56bohr Cartesian lattice: x[-10,12), y[-9,11), z[-7,13),
z fastest; electron bohr⁻³. Difference=current model minus r1 density at
identical nuclei/grid points; it measures method dependence at that geometry,
not unique transferred charge. This sampling under-resolves cores. Normalization
uses the AO metric. Spatial overlaps and phase choices are independently
reconstructed; no overlap is converted into an interaction energy. Full-response
nuclear gradients are retained only for cases explicitly containing that array;
other fixed-geometry diagnostics do not claim alternative-level stationarity.
The initial ethylene/diene grid5 cases and ethylene def2TZVP case also retained
optional gradients before that extra analysis was limited to TS cases. Add
`--gradient` to a single case command to reproduce an optional stored gradient;
this scheduling change does not alter the SCF model or energy/density analysis.

## Electronic-structure evolution and interface

New IRC trials retain coordinates, electronic energies, gradients, SCF status,
electron counts and latest-wavefunction checkpoints; they are not a completed
set of synchronized laboratory electronic-field frames. **New IRC volumetric
fields, per-selected-point Mayer/Löwdin descriptors and cross-IRC orbital tracking
are not yet generated or integrated.** Existing original density/amplitude,
difference/deformation fields, definitions, references and symmetry teaching
views remain unchanged. No constrained geometry is relabeled as an IRC point.

The old reference difference includes nuclear displacement and is not uniquely
electron transfer. Signed orbital amplitudes, total density, orbital probability,
geometry differences and frozen-fragment deformation density remain distinct.
The selected IRC-field implementation must pass its own independent validation
after path connectivity succeeds; no code availability is a claim of execution.

SORG1333 remains S1 paired state, O3 cyclic cooperative organization, R3 multiple-
bond redistribution and G3 collective geometry; S3 means excited/state change.
Qualitative classification omits numerical energies, density partition/reference,
orbital gauge, atom mapping, bond indices, timing and exact synchronicity.
Concerted and strictly synchronous are distinct assertions. A single canonical
surface or the old equal-distance constraint cannot establish a complete path.

## Reproduction, tests and limitations

Exact software versions: software-versions.json and research/diels-alder/r2/
requirements.txt. Use a new output directory; the driver refuses to overwrite
a previous attempt. Outputs of this restart are not guaranteed bitwise identical
on different linear-algebra/grid/software environments.

```sh
pip install -r research/diels-alder/r2/requirements.txt
export OCHEM_R2_OUTPUT=/tmp/ochem-r2-independent-restart
OCHEM_THREADS=3 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/irc.py forward
OCHEM_THREADS=3 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/irc.py backward
OCHEM_THREADS=3 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/endpoints.py forward
OCHEM_THREADS=3 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/endpoints.py backward
OCHEM_THREADS=2 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/compare.py --all
OCHEM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/validate_comparisons.py
OCHEM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/validate_path.py
OCHEM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/compare_endpoints.py
```

Baseline complete npm regression passed; baseline-regression.log retains actual
output. It covers31/69 catalog/event preservation, existing SN2/carbonyl/Diels–
Alder frames, orbital/density metadata, assets, asynchronous selector races and
DOM interaction. Subsequent release-specific regression and published browser
checks must be recorded separately before claiming completion. Native mobile
touch and WebGL cannot be certified from DOM or static projections.

All raw trial JSON/logs are retained in CRC-checked evaluations.zip archives,
updated every five evaluations and upon termination. Latest-wavefunction and
driver stdout snapshots are checkpoints, not complete per-trial orbital archives.
Remaining work: finish independent endpoint/connectivity checks; resolve any
failure with documented fresh attempts; then calculate/verify selected IRC
electronic fields and integrate only a verified series; complete regression,
published interaction checks and release deployment. No full success is claimed
while any required stage remains pending.

Implementation documentation: https://geometric.readthedocs.io/en/latest/irc.html
and https://pyscf.org/user/geomopt.html .
