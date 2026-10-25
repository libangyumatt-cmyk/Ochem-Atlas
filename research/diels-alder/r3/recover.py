"""Read-only r2 recovery; no new electronic calculations or r2 mutation."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'dist/reaction-lab/diels-alder'
OLD=BASE/'r2/restart-20261022'
OUT=ROOT/'audit/V037_R3_RECOVERY.json'
def main():
 report={'scientificStatus':'IRC validation incomplete','files':{},'branches':{}}
 for p in sorted(OLD.rglob('*')):
  if not p.is_file():continue
  report['files'][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
  if p.suffix in ('.zip','.npz'):
   with zipfile.ZipFile(p) as z:assert z.testzip() is None,p
  if p.suffix=='.npz':
   with np.load(p) as w:
    for k in w.files:
     if np.issubdtype(w[k].dtype,np.number):assert np.isfinite(w[k]).all(),(p,k)
 protected=json.loads((ROOT/'audit/V037_R2_PRESERVED_DATA.json').read_text())
 for name,sha in protected.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
 ts=json.loads((BASE/'ts.json').read_text());assert [a['element'] for a in ts['atoms']]==['C']*6+['H']*10
 provenance=json.loads((OLD/'path-validation.json').read_text())
 for direction in ['forward','backward']:
  folder=OLD/direction;state=json.loads((folder/'status.json').read_text())
  for name,sha in state['initialSources'].items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==sha
  with zipfile.ZipFile(folder/'evaluations.zip') as z:ev=[json.loads(z.read(n)) for n in sorted(z.namelist()) if n.endswith('.json')]
  for e in ev:
   assert e['scfConverged'] and abs(e['electronCount']-46)<1e-8 and e['orbitalGradientNorm']<3e-6
   for k in ['coordinatesBohr','gradientEhPerBohr']:assert np.array(e[k]).shape==(16,3) and np.isfinite(e[k]).all()
   assert np.isfinite(e['energyHartree'])
  with np.load(folder/'latest-wavefunction.npz') as w:
   matches=[e for e in ev if np.max(abs(w['coordinatesBohr']-e['coordinatesBohr']))<1e-10 and abs(float(w['energyHartree'])-e['energyHartree'])<1e-10]
   checkpointMatch=[e['evaluation'] for e in matches]
  points=provenance['branches'][direction]['acceptedIRCPoints']
  report['branches'][direction]={'driverComplete':state['complete'],'driverConverged':state['driverConverged'],'evaluations':len(ev),'acceptedPoints':len(points),'latestWavefunctionMatchingEvaluations':checkpointMatch,'latestWavefunctionUsableForFaithfulRestart':False,'lastAcceptedEvaluation':points[-1]['evaluation'],'lastFormingDistancesAngstrom':points[-1]['formingDistancesAngstrom'],'restartDecision':'No serialized Optimizer/internal-coordinate/BFGS/IRC state retained. Wavefunction and coordinates support a new SCF guess, not faithful IRC continuation. Restart backward from TS in a new attempt; retain completed forward branch.'}
 report['protectedPayloads']=len(protected)
 report['comparisons']='Seven complete analyses retained; do not repeat for connectivity recovery.'
 report['endpoint']='Forward stationary geometry has negative curvature at grids 3 and 5; minimum verification failed. Both displaced optimizations required.'
 report['archiveIntegrity']='All retained ZIP/NPZ CRCs passed; all numerical NPZ arrays finite.'
 temp=OUT.with_suffix('.pending');temp.write_text(json.dumps(report,indent=2)+'\n');temp.replace(OUT)
 print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
if __name__=='__main__':main()
