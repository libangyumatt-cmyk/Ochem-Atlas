# v0.3.3 orbital laboratory: reproducibility and scope

These are **Atlas-generated calculations**, separate from the published Cl⁻ + CH₃Cl SN2 evidence in `research/evidence.json`. The three neutral, singlet, isolated molecules were calculated at **fixed, manually specified input geometries**, with restricted Hartree–Fock (RHF) and the STO-3G Gaussian basis in PySCF **2.14.0**. The coordinates are in each `.xyz` file and in `generate.py`. No experimental geometry, geometry optimization, frequency analysis, solvation model, transition state, or reaction path is claimed.

## Reproduce

Python 3.12.14, PySCF 2.14.0, NumPy 2.3.5, SciPy 1.17.0, h5py 3.15.1, scikit-image 0.25.2 and Matplotlib 3.10.8 were used. In a normal Python environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r research/orbitals/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python research/orbitals/generate.py
.venv/bin/python research/orbitals/render_fallback.py
npm test
```

The hosted executor did not expose `/proc/<pid>/statm`, a memory-estimation path used by PySCF. `generate.py` catches that specific `FileNotFoundError` and sets PySCF's memory-estimate callback to zero for these tiny in-core systems; no electronic integrals or SCF equations were changed. In an ordinary environment this workaround is not used. Runtime BLAS thread limits were used for reproducible resource consumption, not chemistry.

The script saves full SCF output logs, a compressed NumPy archive (`mo_coeff`, `mo_energy`, `mo_occ`, AO overlap and input coordinates), and seven Gaussian cube wavefunction grids, gzip compressed for the site. The fixed 44³ sampling grid has a 3-bohr margin around each molecule. The browser loads `dist/orbital-data.json`, a derived triangle mesh from scikit-image's marching-cubes algorithm at ψ = ±0.035 bohr⁻³ᐟ². Vertex coordinates are rounded to 0.001 Å **for the display mesh only**; the cube grid is retained. Static PNG projections are rendered from those same meshes for browsers without WebGL. The `outputs/summary.json` excludes mesh vertices to allow quick inspection.

| System | Input Cartesian coordinates in Å | Electrons | Selected canonical orbitals (1-based index) | RHF total energy (hartree) |
|---|---|---:|---|---:|
| H₂ | H (0,0,−0.370), H (0,0,+0.370) | 2 | 1σg (1), 1σu* (2) | −1.11675930740 |
| C₂H₄ | C (±0.667,0,0), H (±1.232,±0.923,0) with each H on its adjacent carbon side | 16 | π HOMO (8), π* LUMO (9) | −77.07268171166 |
| CH₂O | C (0,0,0), O (1.210,0,0), H (−0.570,±0.935,0) | 16 | π(C=O) (7), n(O) HOMO (8), π*(C=O) LUMO (9) | −112.35385994749 |

All reported values are **model outputs**, not experimental energies. The electron count and `CᵀSC=I` orthonormality were checked to better than 3.1×10⁻¹⁵ for these runs. Each selected occupied MO has occupation 2, each selected virtual MO occupation 0. The π/π* orbitals are odd under reflection through the molecular plane (z=0); formaldehyde's in-plane n(O) is even. Ethylene's π and π* also differ by phase across C=C. H₂'s bonding 1σg is nonnegative in this real STO-3G representation at this isovalue, so **no artificial negative lobe** was drawn. The arbitrary global sign of any real MO can be reversed with no change in |ψ|².

Canonical MO identities were checked using the AO coefficient pattern and spatial symmetry, not inferred from orbital index alone. RHF orbital energies, particular canonical orbital shapes and virtual orbitals depend on method and basis. An isosurface shows signed amplitude rather than electron charge, density or a trajectory. The static carbonyl π* picture can help discuss acceptor symmetry, but it does not calculate nucleophile attack, activation energy, selectivity or Bürgi–Dunitz geometry. Ethylene alone does not compute the Diels–Alder interacting pair.

Scientific/software references: [PySCF SCF user guide](https://pyscf.org/user/scf.html), [PySCF cube generation API](https://pyscf.org/pyscf_api_docs/pyscf.tools.html), Sun *et al.*, [*WIREs Comput. Mol. Sci.* **8**, e1340 (2018)](https://doi.org/10.1002/wcms.1340); Roothaan, [*Rev. Mod. Phys.* **23**, 69 (1951)](https://doi.org/10.1103/RevModPhys.23.69); Kohn and Sham, [*Phys. Rev.* **140**, A1133 (1965)](https://doi.org/10.1103/PhysRev.140.A1133). Three.js 0.186.1 is locally bundled under its MIT license. These references explain methods; **the numerical results above were calculated in this repository**, not taken from those papers.

## v0.3.4 orbital diversity and rigid torsion scan

See [V034_AUDIT.md](../../V034_AUDIT.md) for full provenance, tables, validation, correspondence and limitations. Run `generate_v034.py`, `render_v034.py`, then `validate_v034.py` with the pinned requirements above. New outputs reside in `dist/orbital-files/v034/` and `dist/orbital-diversity.json`. They preserve all v0.3.3 results. Allyl uses a spin-pure open-shell ROHF doublet; benzene and s-trans-butadiene use RHF. The five ethylene torsion frames are separate constrained RHF calculations from 0° to 60°, matched using cross-geometry AO-metric overlaps and sign alignment. They are not an IRC or a verified correlated ground-state torsional profile.
