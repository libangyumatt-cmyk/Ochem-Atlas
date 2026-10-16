"""Improve TS guess by relaxing both forming distances at 2.25 Å first.
That constrained seed is not called a transition state. A subsequent unconstrained
full-gradient search and independent full Hessian decide TS status.
"""
from compute import *
from study import single

def main():
 (OUT/'inputs.json').write_text(json.dumps(dict(method='B3LYP (PySCF default VWN-RPA)',basis=BASIS,charge=0,multiplicity=1,electronCount=46,environment='isolated gas phase',gridLevel=3,seed=[(e,v.tolist()) for e,v in seed()],seedConstraintAngstrom=2.25,scanConstraintsAngstrom=[3.,2.5,1.9],optimizerGradientRmsTarget=8e-5,optimizerGradientMaximumTarget=2e-4,finalCartesianGradientTolerance=2e-4,gradientUnits='Eh/bohr',scfEnergyToleranceEh=1e-10,scfOrbitalGradientTolerance=1e-6,software='PySCF '+__import__('pyscf').__version__,path='constrained seed -> unconstrained saddle; constrained study, no IRC'),indent=2))
 con=OUT/'ts-seed-constraints.txt';con.write_text('$set\ndistance 1 5 2.25\ndistance 4 6 2.25\n$end\n')
 if (OUT/'ts-seed.xyz').exists():
  lines=(OUT/'ts-seed.xyz').read_text().splitlines()[2:];ms=gto.M(atom=[(x.split()[0],list(map(float,x.split()[1:4]))) for x in lines],basis=BASIS,verbose=0)
 else:
  m,f=solve(seed(),OUT/'ts-seed-optimization.log');ms=optimize(f,constraints=str(con),maxsteps=40,convergence_energy=1e-5,convergence_grms=5e-4,convergence_gmax=1e-3,convergence_drms=.01,convergence_dmax=.02,verbose=0)
 single('ts-seed',ms)
 m,f=solve([(ms.atom_symbol(i),v*BOHR) for i,v in enumerate(ms.atom_coords())],OUT/'ts-refinement.log')
 opt=optimize(f,transition=True,hessian=True,trust=.03,tmax=.1,maxsteps=50,convergence_grms=8e-5,convergence_gmax=2e-4,verbose=0)
 _,_,r=save('ts',opt,'Full-dimensional transition-state candidate; status from full gradient and Hessian')
 assert r['maxNuclearGradientEhPerBohr']<2e-4 and sum(v<-20 for v in r['frequenciesCm'])==1
 r.update(geometryKind='Full-gradient and Hessian verified first-order saddle; IRC not performed',stationaryPointVerified=True);(OUT/'ts.json').write_text(json.dumps(r,indent=2))
if __name__=='__main__':main()
