"""Reproducible B3LYP/6-31G(d) gas-phase singlet C6H10 study.
Run OMP_NUM_THREADS=1 python research/diels-alder/compute.py.
All optimizations use full Cartesian analytic nuclear gradients.
"""
from pathlib import Path
import json,sys
import numpy as np
from pyscf import gto,dft,lib
from pyscf.geomopt.geometric_solver import optimize
from pyscf.geomopt import geometric_solver
# PySCF normally recomputes even a file: Hessian. Reuse this retained analytic
# seed Hessian only for the identical documented seed; final Hessian is fresh.
_make_hessian=geometric_solver._make_hessian
def retained_seed_hessian(scanner,option,tmpdir):
 if isinstance(option,str) and option.startswith("file:") and Path(option[5:]).exists():return option
 return _make_hessian(scanner,option,tmpdir)
geometric_solver._make_hessian=retained_seed_hessian
from pyscf.hessian import thermo
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'dist/reaction-lab/diels-alder';OUT.mkdir(parents=True,exist_ok=True)
BOHR=.529177210903;BASIS='6-31g(d)';XC='b3lyp'
lib.num_threads(4)
try:lib.current_memory()
except FileNotFoundError:lib.current_memory=lambda:(0,0)
def solve(atoms,log=None):
 m=gto.M(atom=atoms,basis=BASIS,charge=0,spin=0,unit='Angstrom',verbose=4 if log else 0,output=str(log) if log else None)
 f=dft.RKS(m);f.xc=XC;f.grids.level=3;f.conv_tol=1e-10;f.conv_tol_grad=1e-6;f.max_cycle=120;f.kernel()
 assert f.converged
 return m,f
def seed():
 c=np.array([[-1.4,.6,0],[-.73,-.55,0],[.73,-.55,0],[1.4,.6,0],[-.67,.6,2.1],[.67,.6,2.1]])
 a=[('C',x) for x in c]
 for i,neighbors in [(0,[1]),(1,[0,2]),(2,[1,3]),(3,[2]),(4,[5]),(5,[4])]:
  vs=[(c[j]-c[i])/np.linalg.norm(c[j]-c[i]) for j in neighbors]
  if len(vs)==2: dirs=[-sum(vs)/np.linalg.norm(sum(vs))]
  else:
   v=vs[0];p=np.array([-v[1],v[0],0]);dirs=[-.5*v+np.sqrt(.75)*p,-.5*v-np.sqrt(.75)*p]
  a.extend(('H',c[i]+1.085*v) for v in dirs)
 return a

def save(id,m,kind,reuse_hessian=False):
 a=[(m.atom_symbol(i),v*BOHR) for i,v in enumerate(m.atom_coords())];m,f=solve(a,OUT/(id+'.log'));g=f.nuc_grad_method().kernel();s=m.intor('int1e_ovlp');dm=f.make_rdm1()
 np.savez_compressed(OUT/(id+'-scf.npz'),mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,overlap=s,density_matrix=dm,coordinates=m.atom_coords()*BOHR,gradient=g)
 h=np.load(OUT/(id+'-hessian.npz'))['hessian'] if reuse_hessian else f.Hessian().kernel();ha=thermo.harmonic_analysis(m,h);freq=ha['freq_wavenumber'];fs=[float(-abs(v.imag) if abs(v.imag)>1 else v.real) for v in freq]
 np.savez_compressed(OUT/(id+'-hessian.npz'),hessian=h,frequencies=np.array(fs),normal_modes=ha['norm_mode'],gradient=g)
 rec=dict(id=id,geometryKind=kind,atoms=[dict(element=e,xyzAngstrom=list(map(float,v)),label=f'{e}{i+1}',atomId=str(i)) for i,(e,v) in enumerate(a)],energyHartree=float(f.e_tot),frequenciesCm=fs,maxNuclearGradientEhPerBohr=float(abs(g).max()),scfConverged=bool(f.converged),electronCountAOMetric=float(np.einsum('ij,ji',dm,s)),orthonormalError=float(abs(f.mo_coeff.T@s@f.mo_coeff-np.eye(m.nao)).max()),scfOrbitalGradientNorm=float(np.linalg.norm(f.get_grad(f.mo_coeff,f.mo_occ,f.get_fock()))))
 (OUT/(id+'.json')).write_text(json.dumps(rec,indent=2));(OUT/(id+'.xyz')).write_text(str(len(a))+'\n'+kind+'\n'+''.join(f'{e} {v[0]:.12f} {v[1]:.12f} {v[2]:.12f}\n' for e,v in a));print('SAVED',id,rec['maxNuclearGradientEhPerBohr'],fs,flush=True)
 return m,f,rec

def main():
 a=seed();(OUT/'inputs.json').write_text(json.dumps(dict(method='B3LYP (PySCF default VWN-RPA convention)',basis=BASIS,charge=0,multiplicity=1,electronCount=46,gridLevel=3,seed=[(e,v.tolist()) for e,v in a],optimization='geomeTRIC full Cartesian gradients; TS initial analytic Hessian',software='PySCF '+__import__('pyscf').__version__),indent=2))
 m,f=solve(a,OUT/'ts-optimization.log')
 ts=optimize(f,transition=True,hessian=("file:"+str(OUT/"seed-hessian.txt")) if (OUT/"seed-hessian.txt").exists() else True,trust=.05,tmax=.15,maxsteps=60,convergence_grms=8e-5,convergence_gmax=2e-4,verbose=0)
 tm,tf,tr=save('ts',ts,'Transition-state candidate: status determined from full gradient and Hessian')
 assert tr['maxNuclearGradientEhPerBohr']<2e-4 and sum(x<-20 for x in tr['frequenciesCm'])==1,tr
 tr['geometryKind']='Full-gradient and Hessian verified first-order saddle; IRC not performed';tr['stationaryPointVerified']=True;(OUT/'ts.json').write_text(json.dumps(tr,indent=2))

if __name__=='__main__':main()
