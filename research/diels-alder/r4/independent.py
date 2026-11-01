"""Independent Cartesian mass-weighted Euler descent with Armijo backtracking.
A deliberately bounded integrator test, not a certified complete IRC.
"""
from pathlib import Path
import sys,json,zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r2'))
from common import *
NEW=BASE/'r4'
def main():
 kind=sys.argv[1];assert kind in ['ts','local'];folder=NEW/('independent-'+kind);folder.mkdir(parents=True,exist_ok=True);assert not (folder/'input.json').exists() or '--recover-start' in sys.argv
 convention=json.loads((BASE/'r2/restart-20261022/path-validation.json').read_text())['coordinateConvention'];mass=np.array(convention['massesAmu'])[:,None];root=np.sqrt(mass)
 if kind=='ts':
  x=np.array([a['xyzAngstrom'] for a in record()['atoms']])/BOHR
  with zipfile.ZipFile(BASE/'r3/backward-attempt1/backward/evaluations.zip') as z:r=json.loads(z.read('eval-0001.json'))
  assert np.max(abs(x-r['coordinatesBohr']))<1e-8;x=np.array(r['coordinatesBohr']);energy=r['energyHartree'];g=np.array(r['gradientEhPerBohr']);dm=np.load(BASE/'ts-scf.npz')['density_matrix']
  h=np.load(BASE/'ts-hessian.npz')['hessian'].transpose(0,2,1,3).reshape(48,48);weights=np.repeat(root[:,0],3);hm=(h+h.T)/2/weights[:,None]/weights[None,:];eig,vec=np.linalg.eigh(hm);direction=vec[:,0].reshape(16,3);assert eig[0]<0
  def distance(x):return sum(np.linalg.norm(x[a]-x[b]) for a,b in [(0,4),(3,5)])
  if distance(x+.02*direction/root)<distance(x):direction=-direction
  first=.02*direction
 else:
  w=np.load(NEW/'backward-diagnostic/grid3-135.npz');x=w['coordinatesBohr'];energy=float(w['energyHartree']);g=w['gradientEhPerBohr'];dm=w['density_matrix'];first=None
 write(folder/'input.json',dict(method='Normalized Cartesian mass-weighted Euler steepest descent, Armijo backtracking; independent of DLC/BFGS/geomeTRIC stepping',coordinate='q_i=sqrt(m_i/amu)*R_i/bohr; g_q=g_R/sqrt(m_i/amu)',massesAmu=mass[:,0].tolist(),kind=kind,maxAcceptedNewPoints=6,maxFreshEvaluations=16,initialStepBohrSqrtAmu=.02,armijoCoefficient=1e-4,minimumStepBohrSqrtAmu=1e-6,scope='Bounded numerical-method test, not complete endpoint connectivity; no interpolation.'))
 accepted=[];trials=[];step=.02
 for count in range(1,17):
  gq=g/root;direction=first if first is not None else -step*gq/np.linalg.norm(gq);candidate=x+direction/root
  existing=folder/f'eval-{count:03d}.npz'
  if existing.exists():
   w=np.load(existing);assert np.max(abs(w['coordinatesBohr']-candidate))<1e-12;assert 'converged SCF energy' in (folder/f'eval-{count:03d}.log').read_text();newEnergy=float(w['energyHartree']);ng=w['gradientEhPerBohr'];npdm=w['density_matrix'];s=w['overlap'];converged=True
  else:
   m,f=solve(candidate,folder/f'eval-{count:03d}.log',dm);grad=f.nuc_grad_method();grad.grid_response=True;ng=grad.kernel();npdm=f.make_rdm1();s=m.intor('int1e_ovlp');newEnergy=float(f.e_tot);converged=bool(f.converged)
   save_npz(existing,coordinatesBohr=candidate,energyHartree=newEnergy,gradientEhPerBohr=ng,mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,density_matrix=npdm,overlap=s)
  limit=energy if first is not None else energy-1e-4*step*np.linalg.norm(gq);ok=bool(newEnergy<limit)
  row=dict(evaluation=count,energyHartree=newEnergy,coordinatesBohr=candidate.tolist(),accepted=ok,energyChangeHartree=newEnergy-energy,stepMassWeighted=float(np.linalg.norm(direction)),scfConverged=converged,electronCount=float(np.einsum('ij,ji',npdm,s)),formingDistancesAngstrom=[float(np.linalg.norm(candidate[a]-candidate[b])*BOHR) for a,b in [(0,4),(3,5)]])
  trials.append(row)
  if ok:x=candidate;energy=newEnergy;g=ng;dm=npdm;accepted.append(row);first=None
  else:
   step/=2
   if first is not None:first/=2
  write(folder/'progress.json',dict(trials=trials,accepted=accepted,status='bounded integration in progress',completePathVerified=False));archive(folder,'eval-*.*','evaluations.zip')
  if len(accepted)>=6 or step<1e-6:break
 write(folder/'result.json',dict(trials=trials,accepted=accepted,scope='Initial segment or local repair test only; not complete independently verified IRC',completePathVerified=False,terminatedBy='six accepted points' if len(accepted)>=6 else 'evaluation/step budget'))
 print(kind,'accepted',len(accepted),'evaluations',len(trials),flush=True)
if __name__=='__main__':main()
