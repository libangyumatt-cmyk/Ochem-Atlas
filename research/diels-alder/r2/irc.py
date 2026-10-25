"""geomeTRIC bidirectional IRC with full moving-grid-response gradients.
Run each direction separately. Driver convergence is NOT endpoint validation.
"""
from common import *
import geometric
from geometric.engine import Engine
from geometric.molecule import Molecule
from geometric.optimize import run_optimizer,Optimizer

class FreshEngine(Engine):
 def __init__(self,molecule,folder):
  super().__init__(molecule);self.folder=folder;self.count=0
  self.dm=np.load(BASE/'ts-scf.npz')['density_matrix']
 def calc_new(self,coords,dirname):
  self.count+=1;x=coords.reshape(-1,3)
  m,f=solve(x,self.folder/f'eval-{self.count:04d}.log',self.dm);self.dm=f.make_rdm1()
  grad=f.nuc_grad_method();grad.grid_response=True;g=grad.kernel()
  data=dict(evaluation=self.count,coordinatesBohr=x.tolist(),energyHartree=float(f.e_tot),gradientEhPerBohr=g.tolist(),scfConverged=bool(f.converged),orbitalGradientNorm=float(np.linalg.norm(f.get_grad(f.mo_coeff,f.mo_occ,f.get_fock()))),electronCount=float(np.einsum('ij,ji',self.dm,m.intor('int1e_ovlp'))))
  write(self.folder/f'eval-{self.count:04d}.json',data)
  save_npz(self.folder/'latest-wavefunction.npz',coordinatesBohr=x,mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,density_matrix=self.dm,overlap=m.intor('int1e_ovlp'),gradientEhPerBohr=g,energyHartree=f.e_tot)
  print('EVALUATION',self.folder.name,self.count,data['energyHartree'],flush=True)
  if self.count%5==0:archive(self.folder,'eval-*.*','evaluations.zip')
  return dict(energy=f.e_tot,gradient=g.ravel())

def main():
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('direction',choices=['forward','backward'])
 parser.add_argument('--trust',type=float,default=.05,help='Initial/maximum trust radius in Angstrom; retained in options.json/status.json.')
 parser.add_argument('--maxiter',type=int,default=160)
 args=parser.parse_args();direction=args.direction
 assert 0.005<=args.trust<=.2 and args.maxiter>0
 folder=OUT/direction;folder.mkdir(exist_ok=True)
 assert not (folder/'status.json').exists(),'Retain previous attempt; choose a new OCHEM_R2_OUTPUT directory.'
 ts=record();x=np.array([a['xyzAngstrom'] for a in ts['atoms']]);h=np.load(BASE/'ts-hessian.npz')['hessian'].transpose(0,2,1,3).reshape(48,48)
 np.savetxt(folder/'initial-hessian.txt',h)
 molecule=Molecule();molecule.elem=[a['element'] for a in ts['atoms']];molecule.xyzs=[x];molecule.comms=['Retained verified r1 TS; no forming-distance constraints'];molecule.build_topology()
 engine=FreshEngine(molecule,folder);trace=[];original=Optimizer.evaluateStep
 def evaluate(self):
  before=self.X.copy();iteration=self.Iteration;ordinary=bool(self.IRC_info['opt']);original(self)
  trace.append(dict(iteration=iteration,accepted=bool(np.max(abs(self.X-before))<1e-10),endpointOptimization=ordinary,optimizationAfterStep=bool(self.IRC_info['opt']),coordinatesBohr=before.reshape(-1,3).tolist(),state=str(self.state)))
  write(folder/'step-provenance.json',trace)
 Optimizer.evaluateStep=evaluate
 options=dict(irc=True,irc_direction=direction,coordsys='dlc',hessian='file:'+str(folder/'initial-hessian.txt'),trust=args.trust,tmin=.005,tmax=args.trust,maxiter=args.maxiter,convergence_energy=1e-7,convergence_grms=3e-5,convergence_gmax=8e-5,convergence_drms=.0006,convergence_dmax=.001,subfrctor=2)
 status=dict(complete=False,driverConverged=False,scientificValidation='pending: independent descent and endpoint checks required',options=options,gradientConvention='Full moving-grid-response analytic B3LYP gradients; fresh level-3 grid each trial. Initial Hessian is unchanged r1 default-response analytic Hessian; subsequent BFGS updates. Not a full-response Hessian calculation.',model=dict(charge=0,multiplicity=1,electrons=46,method='B3LYP (VWN-RPA)',basis='6-31G(d)',environment='isolated gas phase'),software=dict(pyscf=__import__('pyscf').__version__,geometric=geometric.__version__),initialSources={p:hashlib.sha256((BASE/p).read_bytes()).hexdigest() for p in ['ts.json','ts-scf.npz','ts-hessian.npz']})
 write(folder/'status.json',status)
 try:
  path=run_optimizer(customengine=engine,input=str(BASE/'ts.xyz'),prefix=str(folder/'path'),**options)
  status.update(driverConverged=True,finalCoordinatesAngstrom=path.xyzs[-1].tolist())
 except Exception as exc:
  status['error']=type(exc).__name__+': '+str(exc)
  raise
 finally:
  status.update(complete=True,evaluations=engine.count);write(folder/'status.json',status);archive(folder,'eval-*.*','evaluations.zip')

if __name__=='__main__':main()
