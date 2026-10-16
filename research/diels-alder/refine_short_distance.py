"""Independent fresh-grid constrained relaxation of the 1.9 Å input.
SLSQP, all Cartesian coordinates, two exact distances and six rigid-frame gauges.
Full moving-grid analytic RKS gradient drives optimization. A fresh final SCF at
aligned geometry must also pass the original default-gradient projected target.
This is a constrained geometry, never a stationary point or an IRC.
"""
from compute import *
from study import aligned,single
from scipy.optimize import minimize
from types import SimpleNamespace
import ast,sys

def jac_dist(x):
 x=x.reshape(-1,3);j=np.zeros((2,x.size))
 for k,(a,b) in enumerate([(0,4),(3,5)]):
  u=(x[a]-x[b])/np.linalg.norm(x[a]-x[b]);j[k,3*a:3*a+3]=u;j[k,3*b:3*b+3]=-u
 return j

def projected(g,x):
 j=jac_dist(x);g=g.ravel();return float(max(abs(g-j.T@np.linalg.solve(j@j.T,j@g))))

def main():
 lib.num_threads(4)
 lines=(OUT/'short-distance-seed.xyz').read_text().splitlines()[2:];els=[line.split()[0] for line in lines];x0=np.array([list(map(float,line.split()[1:4])) for line in lines]);ref=x0-x0.mean(0);rot=[]
 for axis in np.eye(3):rot.append(np.cross(axis[None,:],ref).ravel())
 gauges=np.vstack([np.tile(v,(len(x0),1)).ravel() for v in np.eye(3)]+rot);gauges/=np.linalg.norm(gauges,axis=1)[:,None]
 guess=np.load(OUT/'short-distance-seed-scf.npz')['density_matrix'];cache={};history=[]
 def evaluate(x):
  nonlocal guess
  if cache and np.array_equal(x,cache['x']):return cache['energy'],cache['gradient']
  m=gto.M(atom=list(zip(els,x.reshape(-1,3))),basis=BASIS,charge=0,spin=0,verbose=0)
  f=dft.RKS(m);f.xc=XC;f.grids.level=3;f.conv_tol=1e-11;f.conv_tol_grad=3e-7;f.max_cycle=120;f.kernel(dm0=guess);assert f.converged
  guess=f.make_rdm1();gr=f.nuc_grad_method();gr.grid_response=True;g=gr.kernel()
  row=dict(evaluation=len(history),energyHartree=float(f.e_tot),maxMovingGridProjectedGradientEhPerBohr=projected(g,x),distancesAngstrom=[float(np.linalg.norm(x.reshape(-1,3)[a]-x.reshape(-1,3)[b])) for a,b in [(0,4),(3,5)]])
  history.append(row);print(row,flush=True);cache.update(x=x.copy(),energy=float(f.e_tot),gradient=g.ravel()/BOHR)
  return cache['energy'],cache['gradient']
 def constraint(x):
  xx=x.reshape(-1,3);return np.r_[[np.linalg.norm(xx[a]-xx[b])-1.9 for a,b in [(0,4),(3,5)]],gauges@(x-x0.ravel())]
 def constraint_jac(x):return np.vstack([jac_dist(x),gauges])
 class ForceTargetReached(Exception):pass
 def accepted(x):
  evaluate(x)
  if history[-1]['maxMovingGridProjectedGradientEhPerBohr']<1e-5 and max(abs(constraint(x)))<1e-7:raise ForceTargetReached
 try:
  z=minimize(evaluate,x0.ravel(),jac=True,method='SLSQP',constraints=[dict(type='eq',fun=constraint,jac=constraint_jac)],callback=None if '--original-options' in sys.argv else accepted,options=dict(ftol=1e-12 if '--original-options' in sys.argv else 1e-10,maxiter=80 if '--original-options' in sys.argv else 60,disp=True))
 except ForceTargetReached:
  z=SimpleNamespace(x=cache['x'],success=False,message='Stopped by declared projected-force criterion, not a SciPy convergence status')
 (OUT/'short-distance-refinement.json').write_text(json.dumps(dict(method='SLSQP with fresh RKS SCF and rebuilt level-3 grids at every trial',gradient='analytic RKS including full moving-grid response',distanceAngstrom=1.9,rigidGauge='centroid translation and linear Eckart rotation constraints referenced to initial published geometry',scfEnergyToleranceEh=1e-11,scfOrbitalGradientTolerance=3e-7,success=bool(z.success),message=str(z.message),maxConstraintResidual=float(max(abs(constraint(z.x)))),history=history,initialCoordinatesAngstrom=x0.tolist(),initialGuess='short-distance-seed-scf.npz',coordinatesAngstrom=z.x.reshape(-1,3).tolist()),indent=2))
 finish(z.x,els)

def finish(x,els):
 m=gto.M(atom=list(zip(els,x.reshape(-1,3))),basis=BASIS,verbose=0);ts=json.loads((OUT/'ts.json').read_text());m=aligned(m,ts)
 # Validate independently before replacing the published point.
 mm,ff=solve([(m.atom_symbol(i),v*BOHR) for i,v in enumerate(m.atom_coords())],OUT/'post-ts-refinement-verification.log');fixed=ff.nuc_grad_method().kernel();gr=ff.nuc_grad_method();gr.grid_response=True;moving=gr.kernel();xx=mm.atom_coords()*BOHR
 checks=dict(defaultProjectedGradientEhPerBohr=projected(fixed,xx.ravel()),movingGridProjectedGradientEhPerBohr=projected(moving,xx.ravel()),maxConstraintDeviationAngstrom=float(max(abs(np.linalg.norm(xx[a]-xx[b])-1.9) for a,b in [(0,4),(3,5)])))
 print('INDEPENDENT FINAL CHECKS',checks,flush=True)
 p=OUT/'short-distance-refinement.json';report=json.loads(p.read_text());report['independentFinalChecks']=checks;p.write_text(json.dumps(report,indent=2))
 assert checks['defaultProjectedGradientEhPerBohr']<3e-4 and checks['movingGridProjectedGradientEhPerBohr']<3e-4 and checks['maxConstraintDeviationAngstrom']<1e-5
 rec=single('post-ts',mm);rec['geometryKind']='Two equal 1.9 Å forming distances constrained; independently fresh-grid relaxed Cartesian geometry. Not a stationary point or IRC.';rec['refinementChecks']=checks;(OUT/'post-ts.json').write_text(json.dumps(rec,indent=2))
 w=np.load(OUT/'post-ts-scf.npz');data={k:w[k] for k in w.files};data['gradient_full_grid_response']=moving;np.savez_compressed(OUT/'post-ts-scf.npz',**data)

def checkpoint_main():
 candidate=json.loads((OUT/'short-distance-candidate.json').read_text());seed=(OUT/'short-distance-seed.xyz').read_text().splitlines()[2:];history=[]
 for line in (OUT/'short-distance-optimization.log').read_text().splitlines():
  if line.startswith("{'evaluation':"):history.append(ast.literal_eval(line))
 report=dict(method='SLSQP with fresh RKS SCF and rebuilt level-3 grids at every trial',gradient='analytic RKS including full moving-grid response',distanceAngstrom=1.9,rigidGauge='centroid translation and linear Eckart rotation constraints referenced to initial published geometry',scfEnergyToleranceEh=1e-11,scfOrbitalGradientTolerance=3e-7,optimizerReportedSuccess=False,stoppingReason='Stopped after completed evaluations reached moving-grid projected gradient below 1e-5 Eh/bohr; the latest genuine SCF checkpoint was retained and independently rechecked. Acceptance is based on final force checks, not optimizer status.',history=history,initialCoordinatesAngstrom=[list(map(float,line.split()[1:4])) for line in seed],initialGuess='short-distance-seed-scf.npz',coordinatesAngstrom=candidate['coordinatesAngstrom'])
 (OUT/'short-distance-refinement.json').write_text(json.dumps(report,indent=2));finish(np.array(candidate['coordinatesAngstrom']).ravel(),candidate['elements'])
if __name__=='__main__':
 if '--checkpoint' in sys.argv:checkpoint_main()
 else:main()
