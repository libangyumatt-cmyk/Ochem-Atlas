"""Targeted transported ring-puckering energy curvature at an actual forward IRC point.
Not a Hessian spectrum or a valley-ridge bifurcation search.
"""
from pathlib import Path
import sys,json,zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r2'))
from common import *
def main():
 old=BASE/'r2/restart-20261022';folder=BASE/'r4/forward-curvature';folder.mkdir(parents=True,exist_ok=True)
 rows=json.loads((old/'path-validation.json').read_text())['branches']['forward']['acceptedIRCPoints'];point=rows[5];x=np.array(point['coordinatesAngstrom']);w=np.load(old/'endpoints/forward/wavefunction.npz');y=w['coordinatesAngstrom'];mode=np.real_if_close(w['normal_modes'][0]);assert np.isrealobj(mode)
 a=y-y.mean(0);b=x-x.mean(0);u,_,vh=np.linalg.svd(a.T@b);rot=u@np.diag([1,1,np.linalg.det(u@vh)])@vh;v=mode@rot;v/=np.linalg.norm(v)
 write(folder/'definition.json',dict(sourceForwardEvaluation=point['evaluation'],sourceCoordinatesAngstrom=x.tolist(),sourceEnergyHartree=point['energyHartree'],formingDistancesAngstrom=point['formingDistancesAngstrom'],transportedCartesianUnitMode=v.tolist(),convention='Proper-rotation Kabsch transport of retained endpoint ring mode to fixed mapped IRC geometry; total Cartesian displacement norm in angstrom. Directional energy diagnostic, not IRC samples, a normal-mode spectrum or a VRI proof.'))
 for t in [0.,-.01,.01]:
  name=f'step{t}';target=folder/(name+'.json')
  if target.exists():continue
  m=gto.M(atom=list(zip(['C']*6+['H']*10,x+t*v)),basis='6-31g(d)',charge=0,spin=0,max_memory=1200,output=str(folder/(name+'.log')),verbose=4);f=dft.RKS(m);f.xc='b3lyp';f.grids.level=3;f.conv_tol=1e-12;f.conv_tol_grad=1e-7;f.max_cycle=120;f.kernel(dm0=w['density_matrix']);assert f.converged;p=f.make_rdm1();s=m.intor('int1e_ovlp')
  save_npz(folder/(name+'.npz'),coordinatesAngstrom=x+t*v,energyHartree=f.e_tot,mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,density_matrix=p,overlap=s)
  write(target,dict(displacementAngstrom=t,energyHartree=float(f.e_tot),scfConverged=True,electronCount=float(np.einsum('ij,ji',p,s))));archive(folder,'step*.*','completed-probes.zip')
 points={t:json.loads((folder/f'step{t}.json').read_text())['energyHartree'] for t in [0.,-.01,.01]};curvature=(points[-.01]+points[.01]-2*points[0.])/(.01/BOHR)**2
 write(folder/'result.json',dict(energyCurvatureEhPerBohr2=curvature,sourceEvaluation=point['evaluation'],sourceEnergyAgreementHartree=points[0.]-point['energyHartree'],interpretation='One transported-coordinate curvature only; no complete Hessian or valley-ridge bifurcation claim. Existing endpoint/grid5 diagnostics and product minima retained without repetition.'))
if __name__=='__main__':main()
