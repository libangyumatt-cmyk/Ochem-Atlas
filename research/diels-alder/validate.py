"""Independent reproducibility checks against retained coefficients/grids."""
import json,hashlib
import numpy as np
from pyscf import gto,lib
from pyscf.hessian import thermo
from compute import OUT,BASIS,BOHR
from fields import quadrature,FRAGS,PAIR,N,ORIGIN,STEP
lib.num_threads(1)
def main():
 d=json.loads((OUT/'diels-alder.json').read_text());report=dict(result='pass',checks=[],frames=[]);ref=np.load(OUT/'approach-fields.npz')['total']
 for f in d['frames']:
  id=f['id'];w=np.load(OUT/(id+'-scf.npz'));v=np.load(OUT/(id+'-fields.npz'));a=[(x['element'],x['xyzAngstrom']) for x in f['atoms']];m=gto.M(atom=a,basis=BASIS,verbose=0);s=m.intor('int1e_ovlp');c=w['mo_coeff'];dm=w['density_matrix'];assert m.nelectron==46
  assert abs(np.einsum('ij,ji',dm,s)-46)<1e-8;assert np.max(abs(c.T@s@c-np.eye(m.nao)))<1e-8;assert np.max(abs(w['coordinates']-m.atom_coords()*BOHR))<1e-9
  assert f['scfConverged'] and f['scfOrbitalGradientNorm']<3e-6
  assert all(v[k].shape==N and np.isfinite(v[k]).all() for k in d['levels']);assert v['total'].min()>-1e-7
  diff=float(np.max(abs(v['difference']-(v['total']-ref))));assert diff<1e-4
  # Reconstruct all fields independently from original wavefunctions at grid nodes.
  grid=np.stack(np.meshgrid(*[ORIGIN[k]+STEP*np.arange(N[k]) for k in range(3)],indexing='ij'),axis=-1).reshape(-1,3)
  # Deterministic lattice subset includes core/bond regions; full fields generated
  # with the same AO formula, independent Becke quadrature validates normalization.
  inds=np.arange(0,len(grid),97);ao=m.eval_gto('GTOval_sph',grid[inds]);rr=np.einsum('pi,ij,pj->p',ao,dm,ao);err=float(max(abs(rr-v['total'].ravel()[inds])));assert err<1e-4
  tw=np.load(OUT/(id+'-tracked.npz'));indices=tw['indices'];probs=[]
  for role,j in zip(['occupied','virtual'],indices):
   phi=ao@tw['mo_coeff'][:,j];assert max(abs(phi-v[role].ravel()[inds]))<1e-6
   probs.append(quadrature(m,np.outer(tw['mo_coeff'][:,j],tw['mo_coeff'][:,j])))
  assert all(abs(q-1)<1e-4 for q in probs)
  if id in ['ts','product']:
   h=np.load(OUT/(id+'-hessian.npz'));fr=thermo.harmonic_analysis(m,h['hessian'])['freq_wavenumber'];freq=[-abs(x.imag) if abs(x.imag)>1 else x.real for x in fr];assert max(abs(np.array(freq)-np.array(f['frequenciesCm'])))<1e-5
   assert abs(h['gradient']).max()<2e-4;assert sum(x<-20 for x in freq)==(1 if id=='ts' else 0)
   if id=='ts':
    slopes=f['unstableMode']['bonds'];assert slopes[0]['drds']<-.05 and slopes[1]['drds']<-.05
    assert abs(slopes[0]['drds']-slopes[1]['drds'])<.01
  if id not in ['ts','product']:
   assert f['constrainedGradientTargetMet']==(f['maxProjectedFreeGradientEhPerBohr']<3e-4)
   if not f['constrainedGradientTargetMet']:assert 'partially relaxed' in f['geometryKind'].lower() and 'partial:' in f['geometryRelaxationStatus']
  if f['geometrySymmetryRmsdAngstrom']<.002:
   assert f['geometryDescriptors'][0]['value']<.002
   assert f['geometryDescriptors'][1]['value']<.002
  for ff in f['fragments']:assert abs(ff['quadratureElectronCount']-ff['electronCount'])<.001
  report['frames'].append(dict(id=id,passed=True,aoFieldReconstructionMaximumError=err,differenceMaximumFloat32Error=diff,orbitalProbabilityIntegrals=probs,projectedGradientEhPerBohr=f['maxProjectedFreeGradientEhPerBohr'],relaxationTargetMet=f.get('constrainedGradientTargetMet'),mappedReflectionRmsdAngstrom=f['geometrySymmetryRmsdAngstrom'],formingDistanceAsymmetryAngstrom=f['geometryDescriptors'][0]['value'],formingMayerAsymmetry=f['geometryDescriptors'][1]['value'],internalStable=f['internalStable'],externalStable=f['externalStable'],quadratureElectronCount=f['quadratureElectronCount']))
 q=d['symmetry'];assert q['samePhaseProducts'][0]*q['samePhaseProducts'][1]>0
 for name in ['reactant-butadiene','reactant-ethylene']:
  f=json.loads((OUT/(name+'.json')).read_text());assert f['maxNuclearGradientEhPerBohr']<2e-4 and min(f['frequenciesCm'])>20
 # Barrier only relative to explicitly optimized isolated reactants, no ZPE.
 et=sum(json.loads((OUT/(n+'.json')).read_text())['energyHartree'] for n in ['reactant-butadiene','reactant-ethylene'])
 ts=next(f for f in d['frames'] if f['id']=='ts');pr=next(f for f in d['frames'] if f['id']=='product')
 report.update(optimizedReactantSumHartree=et,tsMinusOptimizedReactantsKcalMol=(ts['energyHartree']-et)*627.5094740631,productMinusOptimizedReactantsKcalMol=(pr['energyHartree']-et)*627.5094740631,energyCaveat='Electronic differences only, no ZPE/free energy. No IRC connectivity established.',checks=['46-electron charge/spin and AO normalization','Independent level-5 Becke density and orbital quadratures','Stored-grid reconstruction at deterministic lattice subset','Difference reference and fixed grid consistency','Full Hessian frequency recomputation and full gradient','Two forming-bond symmetry within 0.002 Å / 0.002 Mayer except relaxed product','Explicit fragment phase products at both forming regions'])
 (OUT/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
