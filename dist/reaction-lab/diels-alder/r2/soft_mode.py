"""Ten actual tight-SCF finite-displacement energies on the unresolved mode.
This is one directional curvature study, not a full numerical Hessian or IRC.
"""
from common import *
import time

def main():
 source=OUT/'endpoints/forward/verification.json'
 while not source.exists():
  failure=source.parent/'failure.json'
  if failure.exists():raise RuntimeError('Endpoint verification failed before mode study: '+failure.read_text())
  time.sleep(5)
 endpoint=json.loads(source.read_text())
 if endpoint['minimumVerified']:print('Endpoint minimum passed; no unresolved-mode study needed.',flush=True);return
 w=np.load(source.parent/'wavefunction.npz');x=w['coordinatesAngstrom'];mode=np.real_if_close(w['normal_modes'][np.argmin(w['frequenciesCm'])]);assert np.isrealobj(mode);mode=mode/np.linalg.norm(mode)
 folder=OUT/'soft-mode';folder.mkdir(exist_ok=True)
 definition=dict(sourceWavefunctionSha256=hashlib.sha256((source.parent/'wavefunction.npz').read_bytes()).hexdigest(),sourceLowestFrequencyCm=float(min(endpoint['frequenciesCm'])),coordinatesAngstrom=x.tolist(),cartesianUnitMode=mode.tolist(),coordinateConvention='R(s)=R0+s*v; sum|v|^2=1; s is total Cartesian norm in angstrom. Not a mass-weighted IRC displacement; direction sign inherited from retained eigenvector.',method='Restricted B3LYP (VWN-RPA)/6-31G(d), gas phase, neutral singlet, 46 electrons',scfEnergyToleranceHartree=1e-12,scfOrbitalGradientThreshold=1e-7,stability='Determinant stability not recomputed for these probes. SCF convergence/root continuity and the independently checked center endpoint are separate from a full stability analysis.')
 write(folder/'definition.json',definition);results=[]
 for grid in [3,5]:
  for step in [0.,-.01,.01,-.03,.03]:
   name=f'grid{grid}-step{step}';target=folder/(name+'.json')
   if target.exists():results.append(json.loads(target.read_text()));continue
   coords=x+step*mode
   m=gto.M(atom=list(zip(endpoint['elements'],coords)),basis='6-31g(d)',charge=0,spin=0,max_memory=1200,verbose=4,output=str(folder/(name+'.log')))
   f=dft.RKS(m);f.xc='b3lyp';f.grids.level=grid;f.conv_tol=1e-12;f.conv_tol_grad=1e-7;f.max_cycle=120;f.kernel(dm0=w['density_matrix']);assert f.converged
   p=f.make_rdm1();s=m.intor('int1e_ovlp');save_npz(folder/(name+'.npz'),coordinatesAngstrom=coords,energyHartree=f.e_tot,mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,density_matrix=p,overlap=s)
   r=dict(id=name,gridLevel=grid,displacementNormAngstrom=step,energyHartree=float(f.e_tot),electronCount=float(np.einsum('ij,ji',p,s)),scfConverged=bool(f.converged),scfOrbitalGradientNorm=float(np.linalg.norm(f.get_grad(f.mo_coeff,f.mo_occ,f.get_fock()))))
   write(target,r);results.append(r);print('MODE ENERGY',name,r['energyHartree'],flush=True)
 checks=[]
 for grid in [3,5]:
  points={r['displacementNormAngstrom']:r['energyHartree'] for r in results if r['gridLevel']==grid}
  for size in [.01,.03]:checks.append(dict(gridLevel=grid,displacementNormAngstrom=size,energyCurvatureEhPerBohr2=(points[size]+points[-size]-2*points[0.])/(size/BOHR)**2))
 write(folder/'results.json',dict(points=results,directionalChecks=checks,interpretation='Central finite energy curvature along one retained Cartesian mode only. Not a complete numerical Hessian, converged frequency spectrum or independently validated IRC.'))
 print('Directional energy study complete.',flush=True)

if __name__=='__main__':main()
