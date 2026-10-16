# Reaction laboratory schema 2.0

`dist/reaction-lab/index.json` lists computed systems by stable `id`, catalog
`event` (`reaction-id:zero-based-index`), title and data file. It declares only
currently supplied datasets. Original v0.3.5 SN2 records are retained unchanged;
`build_reaction_systems.py` creates an additive adapter.

Each system supplies charge, multiplicity, electron count, environment, method,
basis, path label, explicit molecular equation/scope, grid, references, energy
reference, source files, evidence/limitations, and arrays described below.
No chemical-specific atom indices or counts belong in the viewer.

| Record | Required contents and meaning |
| --- | --- |
| `series[]` | Stable id, title, frameIds, coordinateLabel. A frame may occur in several series. Ordering is not automatically an IRC. |
| `frames[]` | Stable id; atoms with Cartesian Å and labels/identities; separately calculated Eh energy; geometryKind; SCF diagnostics; mesh/field paths; source files. No interpolated frames. |
| `bonds[]` | Atom index pair, label, Å distance, explicitly defined numeric bond indices. Multiple bonds may be analyzed; drawn connections are separate. Current `mayer`, optional `lowdinWiberg`; future conventions must carry names/definitions. |
| `geometryDescriptors[]` | Named value/unit arrays; no SN2-only assumptions. |
| `connections[]` | Atom index pair and `bond` or `guide` style, for display only. Does not set computed bond order. |
| `orbitalDefinitions[]` | Stable id, title, meshKey, description. Optional spin label for alpha/beta; actual calculated spin orbitals required before publishing. Canonical identities and correspondence are documented separately from interpretation. |
| `orbitals[]` | Role id, canonical 1-based index, occupation, Eh eigenvalue; optional same-spin energy gap/degeneracy warning. |
| `tracking[]` | Parent frame, assigned canonical index, AO-metric overlap, alternative, phase and ambiguity flag. Branches have explicit parents. No universal continuity or degenerate-subspace tracking claim. |
| `fieldDefinitions[]` | Stable id, label, kind, units, signed flag; same-frame field/mesh grids required. Density, density difference, deformation, and future spin-density may be declared. Viewer uses supplied field ids/levels, not fabricated data. |
| `levels` | Three explicit sampled thresholds per field/mesh key, not interpolated grids. |
| `grid` | Shape, bohr origin/spacing, order, alignment, field precision and units. Full coefficients and NPZ grids retained. |
| `references` | Density-difference, deformation and probability conventions; fixed atom mapping and chosen reference frames. |

Amplitude and probability controls select any declared orbital; probability is
rendered as the union of its positive/negative amplitude isosurfaces at sqrt of
the probability threshold. It is not occupation-weighted total electron density.
For future spin density, provide real alpha/beta calculations, spin treatment,
normalization and signed grids. Merely declaring the field does not implement a
radical dataset. Diels–Alder, E2 and radical reaction paths are not supplied.

Relative energies use each system's own frame reference. Never subtract absolute
energies between differently composed systems. Comparison cards retain each
system's last selected calculated geometry and quantity independently.
