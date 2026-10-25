# v0.3.7-r3 — IRC recovery

Scientific status: incomplete. No validated IRC series is authorized by current evidence.

## Stage A — recovery

Recovery executed 2026-10-25 against baseline d2abc2355505c4b30dc9d91917c80aad8ee34d0e.
See audit/V037_R3_RECOVERY.json for SHA256 inventory, archive checks and actual counts.
Independent Node reconstruction passed 31 wavefunctions and 145 documented accepted points, orbital metric normalization, electron counts, density Hermiticity and negative energy curvatures. All 373 protected scientific payloads retain their original hashes.

The archive contains 45 forward and 112 backward trial JSON records; the historical report uses 111 backward evaluations. Accepted-point counts remain 39/106. This discrepancy is retained explicitly. Forward latest wavefunction matches archived evaluation 45. Backward latest wavefunction matches no archived trial: it cannot be assigned accepted-point provenance. The incomplete backward driver has no serialized optimizer, internal-coordinate, BFGS or IRC state. A new backward attempt must start from the verified TS; ordinary optimization of the last geometry would not complete its IRC. No historical job is currently running.

## Stage B — forward endpoint

Mode reconstructed from symmetrized Hessian: 31.7901851921i cm^-1. Atom-mapped ring torsions identify ring twisting/puckering (see audit/V037_R3_MODE.json); this is a diagnostic assignment, not a verified conformational minimum. Positive 0.15 Angstrom total Cartesian-norm displacement relaxation started with SCF 1e-10 Eh, orbital-gradient threshold 1e-6, grid3 and full moving-grid-response gradients. Positive displacement minimum verified and independently reconstructed: E=-234.64396502163953 Eh; max full-response force=4.060472139e-6 Eh/bohr; lowest vibrational frequency=166.9418631681 cm^-1; internal/external SCF stability true. Both mapped carbon and hydrogen connectivity checks pass. Forming distances 1.5375065050 and 1.5375948020 Angstrom. Fixed-label carbon RMSD to r1 product=0.3955316942 Angstrom (different ring conformation); all-atom fixed-label RMSD=1.2000283612 Angstrom, reducing to 1.0443072704 with same-carbon equivalent-H exchanges. No improper reflection is used. Energy excess over r1 product=5.676702614e-6 Eh. This verifies a product-region minimum after relaxation from the forward endpoint, not a full two-branch IRC. Negative displacement relaxation started separately; minimum verification pending. Existing independent probes at grids 3 and 5 show negative energy curvature; the approximately 31.8i cm^-1 mode must not be discarded. Existing endpoint E=-234.6348399934745 Eh, maximum full-response force 7.797064832e-6 Eh/bohr; stable electronic determinant, nuclear minimum check failed. Raw Hessian uses PySCF default grid-response approximation. No new minimum or grid convergence claimed.

## Stages C–F

Not started. Connectivity unresolved. Electronic fields deferred until connectivity passes. Original laboratory frames and all SN2/carbonyl functionality preserved. No release deployment claimed.

## Regression verification

Full existing npm suite passed on 2026-10-25; actual output retained in audit/V037_R3_REGRESSION.log. Browser/native mobile behavior has not been retested.

## Reproduction

Run `python research/diels-alder/r3/recover.py` (NumPy required) and `node verify-diels-alder-r2-numerical.cjs` from repository root. Recovery reads r2 artifacts without changing them; its JSON inventory is atomically replaced. R2 computational model and provenance remain in V037_R2_AUDIT.md. New computations must use separate r3 output directories, full-response gradients, and explicitly distinguish endpoint relaxation from IRC integration.

Positive endpoint reconstruction: `OPENBLAS_NUM_THREADS=1 /workspace/ochem-venv/bin/python research/diels-alder/r3/validate_endpoint.py plus`. Start independent displaced runs with `python research/diels-alder/r3/endpoint.py plus` and `minus` in that order; existing input refuses overwrite. PySCF2.14.0, geomeTRIC1.1.1, NumPy2.3.5, SciPy1.17.0. The positive run used three OpenMP threads, the negative run two, BLAS one. Both use grid3 and full-response optimization gradients, with default-response all-Cartesian analytic Hessians. Negative-run optimizer-state pickle is a version-specific trusted-local artifact, round-trip checked after each evaluated step; successful cross-process continuation is not yet claimed.

### Checkpoint implementation failure and recovery

Initial negative-displacement optimization stopped after two converged SCF/gradient evaluations because pickle round-trip reconstruction triggered recursion in geomeTRIC Molecule.__getattr__. This was a checkpoint implementation failure, not chemical convergence failure. Its CRC-checked outputs and failure.json are preserved in endpoint-minus. Explicit Molecule state serialization fixes the recursion. An analytic H2 stretch interruption/continuation check passed (audit/V037_R3_RESTART_TEST.log); this is a workflow test, not electronic-structure validation. A distinct endpoint-minus-retry1 ordinary optimization starts from the retained second geometry and density matrix. It is not described as faithful continuation of the first optimizer state.
