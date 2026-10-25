# v0.3.7-r3 — IRC recovery

Scientific status: incomplete. No validated IRC series is authorized by current evidence.

## Stage A — recovery

Recovery executed 2026-10-25 against baseline d2abc2355505c4b30dc9d91917c80aad8ee34d0e.
See audit/V037_R3_RECOVERY.json for SHA256 inventory, archive checks and actual counts.
Independent Node reconstruction passed 31 wavefunctions and 145 documented accepted points, orbital metric normalization, electron counts, density Hermiticity and negative energy curvatures. All 373 protected scientific payloads retain their original hashes.

The archive contains 45 forward and 112 backward trial JSON records; the historical report uses 111 backward evaluations. Accepted-point counts remain 39/106. This discrepancy is retained explicitly. Forward latest wavefunction matches archived evaluation 45. Backward latest wavefunction matches no archived trial: it cannot be assigned accepted-point provenance. The incomplete backward driver has no serialized optimizer, internal-coordinate, BFGS or IRC state. A new backward attempt must start from the verified TS; ordinary optimization of the last geometry would not complete its IRC. No historical job is currently running.

## Stage B — forward endpoint

Pending displaced optimizations. Existing independent probes at grids 3 and 5 show negative energy curvature; the approximately 31.8i cm^-1 mode must not be discarded. Existing endpoint E=-234.6348399934745 Eh, maximum full-response force 7.797064832e-6 Eh/bohr; stable electronic determinant, nuclear minimum check failed. Raw Hessian uses PySCF default grid-response approximation. No new minimum or grid convergence claimed.

## Stages C–F

Not started. Connectivity unresolved. Electronic fields deferred until connectivity passes. Original laboratory frames and all SN2/carbonyl functionality preserved. No release deployment claimed.

## Reproduction

Run `python research/diels-alder/r3/recover.py` (NumPy required) and `node verify-diels-alder-r2-numerical.cjs` from repository root. Recovery reads r2 artifacts without changing them; its JSON inventory is atomically replaced. R2 computational model and provenance remain in V037_R2_AUDIT.md. New computations must use separate r3 output directories, full-response gradients, and explicitly distinguish endpoint relaxation from IRC integration.
