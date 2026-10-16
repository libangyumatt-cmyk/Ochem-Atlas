"""Method diagnostic only, not an implemented radical reaction dataset.
Compare isolated RHF H− with neutral doublet ROHF H in the same basis.
"""
import json
import numpy as np
from pyscf import gto,scf
from compute import OUT,BASIS

def main():
 m=gto.M(atom=[('H',(0,0,0))],basis=BASIS,charge=0,spin=1,verbose=4,output=str(OUT/'neutral-hydrogen.log'))
 f=scf.ROHF(m);f.conv_tol=1e-11;f.conv_tol_grad=1e-7;f.kernel();assert f.converged
 np.savez_compressed(OUT/'neutral-hydrogen-scf.npz',mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,overlap=m.intor('int1e_ovlp'),density_matrix=f.make_rdm1(),coordinates=m.atom_coords(),coordinateUnit='bohr')
 d=json.loads((OUT/'carbonyl.json').read_text());ehm=d['frames'][0]['fragments'][0]['energyHartree']
 x=dict(method='ROHF',basis=d['basis'],charge=0,multiplicity=2,electronCount=1,neutralHydrogenEnergyHartree=float(f.e_tot),hydrideRHFenergyHartree=ehm,detachmentEnergyHartree=float(f.e_tot-ehm),meaning='E(H doublet) + E(free electron at rest=0) minus E(H− RHF). Negative means this RHF finite-basis hydride reference is not energetically bound against detachment. This is a diagnostic of model inadequacy, not a computed complex detachment pathway or prediction of experimental hydride stability.')
 (OUT/'detachment-check.json').write_text(json.dumps(x,indent=2));print(x);m.stdout.close()
if __name__=='__main__':main()
