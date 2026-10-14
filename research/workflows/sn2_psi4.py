"""Optional first-step reproduction seed. NOT run in the Atlas release.

Requires an independently installed, licensed-for-your-use Psi4 distribution.
This is B3LYP/aug-cc-pVDZ, NOT the published ZORA-OLYP/TZ2P/ADF study.
It optimizes isolated CH3Cl and checks its frequencies. It does not find a
reaction complex, TS, IRC, activation strain, or bond-order trajectory.
"""
import json
from pathlib import Path

import psi4

psi4.set_memory("2 GB")
psi4.set_num_threads(2)
psi4.core.set_output_file("sn2_seed_psi4.out", False)
psi4.set_options({"scf_type": "df", "reference": "rhf", "d_convergence": 1e-8,
                  "e_convergence": 1e-8, "basis": "aug-cc-pvdz"})

substrate = psi4.geometry("""
0 1
C
Cl 1 1.79
H 1 1.09 2 109.5
H 1 1.09 2 109.5 3 120.0
H 1 1.09 2 109.5 3 240.0
symmetry c1
""")
energy, wavefunction = psi4.optimize("b3lyp", molecule=substrate, return_wfn=True)
psi4.frequency("b3lyp", molecule=substrate)
geom = substrate.geometry().to_array() * psi4.constants.bohr2angstroms
distance = float(((geom[0] - geom[1]) ** 2).sum() ** 0.5)
result = {
    "model": "isolated neutral singlet CH3Cl (not SN2)",
    "method": "Psi4 B3LYP/aug-cc-pVDZ, density-fitted SCF; no solvent",
    "energy_hartree": float(energy),
    "C_Cl_angstrom": distance,
    "coordinates_angstrom": geom.tolist(),
    "frequencies": "Inspect sn2_seed_psi4.out; no imaginary mode required for a minimum",
    "status": "user-executed only after running; not an Atlas-generated result"
}
Path("sn2_seed_psi4.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print("Wrote sn2_seed_psi4.out and sn2_seed_psi4.json. Verify frequencies before use.")
