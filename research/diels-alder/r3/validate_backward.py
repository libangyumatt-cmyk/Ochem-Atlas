"""Independent descent, provenance, atom mapping and wavefunction checks.
Run on a completed attempt, or explicitly record an incomplete checkpoint.
"""
from pathlib import Path
import sys,json,zipfile,hashlib,os,io
import numpy as np
ROOT=Path(__file__).resolve().parents[3];BASE=ROOT/'dist/reaction-lab/diels-alder';FOLDER=Path(os.environ.get('OCHEM_R3_BACKWARD_OUTPUT',str(BASE/'r3/backward-attempt1')))/'backward';BOHR=.52917721092

def main():
 state=json.loads((FOLDER/'status.json').read_text());trace=json.loads((FOLDER/'step-provenance.json').read_text())
 with zipfile.ZipFile(FOLDER/'evaluations.zip') as z:
  assert z.testzip() is None;ev={json.loads(z.read(n))['evaluation']:json.loads(z.read(n)) for n in z.namelist() if n.endswith('.json')}
 # A live archive may lag completed rows; include only closed, atomic JSON files.
 for p in FOLDER.glob('eval-*.json'):
  row=json.loads(p.read_text());ev[row['evaluation']]=row
 with zipfile.ZipFile(BASE/'r2/restart-20261022/backward/evaluations.zip') as z:old={json.loads(z.read(n))['evaluation']:json.loads(z.read(n)) for n in z.namelist() if n.endswith('.json')}
 for n,sha in state['initialSources'].items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==sha
 archives={}
 for archivePath in FOLDER.glob('wavefunctions-*.zip'):
  with zipfile.ZipFile(archivePath) as z:
   assert z.testzip() is None
   for name in z.namelist():archives[name]=archivePath
 manifest=json.loads((FOLDER/'wavefunction-manifest.json').read_text()) if (FOLDER/'wavefunction-manifest.json').exists() else None
 reused=fresh=0
 for row in ev.values():
  x=np.array(row['coordinatesBohr']);g=np.array(row['gradientEhPerBohr']);assert x.shape==g.shape==(16,3) and np.isfinite(x).all() and np.isfinite(g).all() and np.isfinite(row['energyHartree'])
  assert row['scfConverged'] and abs(row['electronCount']-46)<1e-8 and row['orbitalGradientNorm']<3e-6
  if row['resultOrigin']=='reused-r2-evaluation':
   r=old[row['sourceEvaluation']];assert np.array_equal(x,r['coordinatesBohr']) and np.array_equal(g,r['gradientEhPerBohr']) and row['energyHartree']==r['energyHartree'] and row['queryMaximumCoordinateDifferenceBohr']<=1e-12;reused+=1
  else:
   assert row['resultOrigin']=='new-r3-SCF-gradient';fresh+=1
   p=FOLDER/f'wavefunction-{row["evaluation"]:04d}.npz'
   if p.exists() and not os.environ.get('OCHEM_R3_ARCHIVES_ONLY'):payload=p.read_bytes()
   else:
    with zipfile.ZipFile(archives[p.name]) as z:payload=z.read(p.name)
   if manifest is not None:assert hashlib.sha256(payload).hexdigest()==manifest[p.name]['sha256']
   with zipfile.ZipFile(io.BytesIO(payload)) as z:assert z.testzip() is None
   w=np.load(io.BytesIO(payload));c=w['mo_coeff'];s=w['overlap'];dm=w['density_matrix'];assert np.max(abs(c.T@s@c-np.eye(c.shape[1])))<1e-8
   assert abs(np.einsum('ij,ji',dm,s)-46)<1e-8 and np.max(abs(dm-dm.T))<1e-10
   assert np.max(abs(w['coordinatesBohr']-x))<1e-12 and abs(float(w['energyHartree'])-row['energyHartree'])<1e-12 and np.max(abs(w['gradientEhPerBohr']-g))<1e-12
 ts=json.loads((BASE/'ts.json').read_text());assert [a['element'] for a in ts['atoms']]==['C']*6+['H']*10
 convention=json.loads((BASE/'r2/restart-20261022/path-validation.json').read_text())['coordinateConvention'];mass=np.array(convention['massesAmu']);prev=np.array([a['xyzAngstrom'] for a in ts['atoms']])/BOHR;energy=ts['energyHartree'];chord=0.;points=[];increments=[]
 for row in trace:
  if not row['accepted'] or row['endpointOptimization']:continue
  x=np.array(row['coordinatesBohr']);r=min(ev.values(),key=lambda e:np.max(abs(x-np.array(e['coordinatesBohr']))));assert np.max(abs(x-r['coordinatesBohr']))<1e-8
  chord+=float(np.sqrt(np.sum(mass[:,None]*(x-prev)**2)));increments.append(r['energyHartree']-energy)
  points.append(dict(evaluation=r['evaluation'],origin=r['resultOrigin'],energyHartree=r['energyHartree'],coordinatesAngstrom=(np.array(r['coordinatesBohr'])*BOHR).tolist(),formingDistancesAngstrom=[float(np.linalg.norm(x[i]-x[j])*BOHR) for i,j in [(0,4),(3,5)]],cumulativeChordLengthBohrSqrtAmu=chord))
  prev=x;energy=r['energyHartree']
 maxup=max(increments) if increments else None;descent=bool(points and maxup<3e-6)
 uphill=[dict(previousEvaluation=points[i-1]['evaluation'],evaluation=points[i]['evaluation'],energyIncreaseHartree=points[i]['energyHartree']-points[i-1]['energyHartree']) for i in range(1,len(points)) if points[i]['energyHartree']>points[i-1]['energyHartree']+3e-6]
 forced='Forcing it to take a step' in (FOLDER/'path.log').read_text()
 report=dict(stage='C',uphillStepsExceedingTolerance=uphill,driverForcedMinimumStepObserved=forced,driverComplete=state['complete'],driverConverged=state['driverConverged'],driverError=state.get('error'),evaluations=len(ev),reusedEvaluations=reused,newScfGradientEvaluations=fresh,acceptedIRCPoints=points,maximumAcceptedEnergyIncreaseHartree=maxup,descentToleranceHartree=3e-6,descentCheckPassed=descent,atomMapping='C1-C4 butadiene, C5-C6 ethylene, H7-H16; neutral singlet C6H10, 46 electrons',coordinateConvention=convention,endpointMinimumVerification='Separate endpoint optimization/Hessian/stability required; convergence alone is insufficient.',strictTwoMinimumIrcConnectivityVerified=False)
 temp=FOLDER/'independent-validation.json.pending';temp.write_text(json.dumps(report,indent=2)+'\n');temp.replace(FOLDER/'independent-validation.json')
 print(json.dumps({k:v for k,v in report.items() if k not in ['acceptedIRCPoints','coordinateConvention']},indent=2))
if __name__=='__main__':main()
