"""Equal-forming-distance relaxed scan, optimized product/reactants.
Constraints are saved verbatim. This is explicitly not an IRC.
"""
import json
import numpy as np
from pyscf import gto
from pyscf.geomopt.geometric_solver import optimize
from compute import *
def aligned(m,ref):
 x=m.atom_coords()*BOHR;y=np.array([a['xyzAngstrom'] for a in ref['atoms']]);cx=x[:6].mean(0);cy=y[:6].mean(0);u,_,v=np.linalg.svd((x[:6]-cx).T@(y[:6]-cy));r=u@np.diag([1,1,np.linalg.det(u@v)])@v;x=(x-cx)@r+cy
 return gto.M(atom=[(m.atom_symbol(i),v) for i,v in enumerate(x)],basis=BASIS,verbose=0)
def single(id,m):
 a=[(m.atom_symbol(i),v*BOHR) for i,v in enumerate(m.atom_coords())];m,f=solve(a,OUT/(id+'.log'));g=f.nuc_grad_method().kernel();s=m.intor('int1e_ovlp');dm=f.make_rdm1()
 np.savez_compressed(OUT/(id+'-scf.npz'),mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,overlap=s,density_matrix=dm,coordinates=m.atom_coords()*BOHR,gradient=g)
 rec=dict(id=id,geometryKind='Two equal C–C distances constrained; all other coordinates relaxed. Not a stationary point or IRC.',atoms=[dict(element=e,xyzAngstrom=list(map(float,v)),label=f'{e}{i+1}',atomId=str(i)) for i,(e,v) in enumerate(a)],energyHartree=float(f.e_tot),maxNuclearGradientEhPerBohr=float(abs(g).max()),scfConverged=bool(f.converged),electronCountAOMetric=float(np.einsum('ij,ji',dm,s)),orthonormalError=float(abs(f.mo_coeff.T@s@f.mo_coeff-np.eye(m.nao)).max()),scfOrbitalGradientNorm=float(np.linalg.norm(f.get_grad(f.mo_coeff,f.mo_occ,f.get_fock()))))
 (OUT/(id+'.json')).write_text(json.dumps(rec,indent=2));(OUT/(id+'.xyz')).write_text(str(len(a))+'\n'+rec['geometryKind']+'\n'+''.join(f'{e} {v[0]:.12f} {v[1]:.12f} {v[2]:.12f}\n' for e,v in a));print('SAVED',id,f.e_tot,flush=True)
 return rec

def main():
 lib.num_threads(4)
 ts=json.loads((OUT/'ts.json').read_text());a=[(x['element'],x['xyzAngstrom']) for x in ts['atoms']]
 for id in ['approach','pre-ts','post-ts']:
  if (OUT/(id+'.json')).exists() or not (OUT/('raw-'+id+'.json')).exists():continue
  raw=json.loads((OUT/('raw-'+id+'.json')).read_text());rm=gto.M(atom=[(x['element'],x['xyzAngstrom']) for x in raw['atoms']],basis=BASIS,verbose=0);single(id,aligned(rm,ts))
 if (OUT/'product-scf.npz').exists():return
 # Independent product minimum, rigidly aligned before a final SCF/Hessian.
 raw=json.loads((OUT/'product-raw.json').read_text());rm=gto.M(atom=[(x['element'],x['xyzAngstrom']) for x in raw['atoms']],basis=BASIS,verbose=0)
 mm,ff,rec=save('product',aligned(rm,ts),'Unconstrained cyclohexene minimum candidate')
 assert rec['maxNuclearGradientEhPerBohr']<2e-4 and min(rec['frequenciesCm'])>20
 rec.update(geometryKind='Full-gradient and Hessian verified cyclohexene minimum',stationaryPointVerified=True);(OUT/'product.json').write_text(json.dumps(rec,indent=2))
if __name__=='__main__':main()
