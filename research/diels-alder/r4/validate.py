"""Reconstruct diagnostic derivatives and AO-metric checks from saved arrays."""
from pathlib import Path
import sys,json,zipfile
import numpy as np
ROOT=Path(__file__).resolve().parents[3];BASE=ROOT/'dist/reaction-lab/diels-alder/r4';folder=BASE/'backward-diagnostic'
def main():
 definition=json.loads((folder/'definition.json').read_text());v=np.array(definition['directionCartesianUnit']);assert abs(np.linalg.norm(v)-1)<1e-12;report={'gridChecks':{},'interpretation':'pending'}
 for grid in [3,5]:
  rows={}
  for n in ['135','138','138-minus','138-plus']:
   name=f'grid{grid}-{n}';r=json.loads((folder/(name+'.json')).read_text());w=np.load(folder/(name+'.npz'));c=w['mo_coeff'];s=w['overlap'];p=w['density_matrix'];assert np.max(abs(c.T@s@c-np.eye(c.shape[1])))<1e-8 and abs(np.einsum('ij,ji',p,s)-46)<1e-8
   assert r['scfConverged'] and r['orbitalGradientNorm']<3e-7
   assert abs(float(w['energyHartree'])-r['energyHartree'])<1e-12 and abs(np.sum(w['gradientEhPerBohr']*v)-r['directionalGradientEhPerBohr'])<1e-12
   rows[n]=r
  fd=(rows['138-plus']['energyHartree']-rows['138-minus']['energyHartree'])/.002;analytic=rows['138']['directionalGradientEhPerBohr'];report['gridChecks'][str(grid)]=dict(uphillEnergyDifferenceEh=rows['138']['energyHartree']-rows['135']['energyHartree'],centralFiniteDifferenceEhPerBohr=fd,analyticDirectionalGradientEhPerBohr=analytic,gradientDifferenceEhPerBohr=fd-analytic,gradientConsistencyPassed=abs(fd-analytic)<1e-6)
 report['interpretation']='Positive step energy change reproduced at both grids; finite-difference gradient agrees with full-response analytic gradient within the explicitly stated 1e-6 Eh/bohr diagnostic tolerance. Evidence favors an integration overshoot/forced acceptance, not random SCF energy noise; this does not isolate coordinate-representation effects or establish grid convergence.' if all(r['gradientConsistencyPassed'] and r['uphillEnergyDifferenceEh']>3e-6 for r in report['gridChecks'].values()) else 'Diagnostic consistency requirements not all passed; uncertainty retained.'
 p=BASE/'diagnostic-validation.json';t=p.with_suffix('.pending');t.write_text(json.dumps(report,indent=2)+'\n');t.replace(p);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
