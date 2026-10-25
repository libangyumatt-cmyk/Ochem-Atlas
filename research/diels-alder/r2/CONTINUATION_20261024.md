# Scientific-validation continuation, 2026-10-24

Base: published commit d2abc2355505c4b30dc9d91917c80aad8ee34d0e.
The original published validation failure and interruption record are retained.

## Recovered evidence

The restored original workspace contained 148 backward SCF/gradient evaluations
and 142 accepted non-endpoint-optimization IRC points. Independent reconstruction
checks their initial TS hashes, atom mapping, SCF convergence, orbital gradient,
electron count, finite arrays, accepted-point provenance and downhill energies.
The largest accepted energy increment is -5.719829232475604e-8 Eh.
Last accepted forming distances: 4.0126709290 and 4.2502730206 Angstrom.
The native driver never recorded convergence. These are interrupted IRC points,
not a newly verified complete branch or infinitely separated reactants.
Their independent snapshot is `dist/reaction-lab/diels-alder/r2/recovery-20261024/`;
`validate_recovery.py` checks its manifest and raw compressed evaluations.

A recovered complete product/grid5 fixed-geometry comparison passed the existing
independent matrix, electron-count, bond-index, orbital-match and density-sampling
reconstruction, bringing the retained complete comparison count from seven to
eight at the first continuation checkpoint. It is not a new optimized geometry.

## New attempts

1. Independent ordinary product-endpoint relaxation initialized by a +0.15
   Angstrom total Cartesian-norm displacement along the stored original imaginary
   mode. This displacement is an initial guess, not an IRC point. Full-response
   gradients, a fresh final SCF, Hessian and stability checks remain required.
2. Fresh backward IRC from the original TS with unchanged electronic model and
   convergence thresholds, initial/maximum trust radius 0.10 Angstrom and a
   maximum 240 iterations. Its directory is `retry-20261024`; it is a separate
   attempt, not a stitched continuation of the lost driver state. The original
   0.05 Angstrom/160-iteration attempt is retained without relabeling.
3. Remaining fixed-geometry method comparisons are recomputed using the existing
   documented script. Incomplete previous SCF-only checkpoints do not count as
   complete analyses.

Run commands (from repository root; use an absolute output path for endpoint
scripts that record source paths relative to the repository):

```sh
OCHEM_THREADS=3 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/endpoints.py forward --displace-mode 0.15
OCHEM_R2_OUTPUT="$PWD/dist/reaction-lab/diels-alder/r2/retry-20261024" OCHEM_THREADS=3 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/irc.py backward --trust 0.1 --maxiter 240
OCHEM_THREADS=2 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/compare.py --all
OCHEM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/diels-alder/r2/validate_recovery.py
```

No new minimum, complete IRC, synchronized IRC electronic fields, or alternative
method stationary point is claimed by this checkpoint. No viewer changes or
new reaction entries are introduced.
