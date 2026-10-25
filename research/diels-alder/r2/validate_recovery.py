"""Validate recovered interrupted trials; never promote them to a complete IRC."""
from common import *
lib.num_threads(1)

def main():
 folder=BASE/'r2/recovery-20261024';branch=folder/'backward'
 manifest=json.loads((folder/'manifest.json').read_text())
 for name,digest in manifest['files'].items():
  assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest,name
 with zipfile.ZipFile(branch/'evaluations.zip') as z:
  assert z.testzip() is None
  ev=[json.loads(z.read(n)) for n in sorted(z.namelist()) if n.endswith('.json')]
 assert len(ev)==148
 state=json.loads((branch/'status.json').read_text())
 assert not state['complete'] and not state['driverConverged']
 for name,digest in state['initialSources'].items():
  assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest
 start=np.array([a['xyzAngstrom'] for a in record()['atoms']])/BOHR
 assert np.max(abs(start-np.array(ev[0]['coordinatesBohr'])))<1e-8
 for e in ev:
  assert e['scfConverged'] and abs(e['electronCount']-46)<1e-8
  assert e['orbitalGradientNorm']<3e-6
  assert np.array(e['coordinatesBohr']).shape==(16,3)
  assert np.isfinite(e['coordinatesBohr']).all() and np.isfinite(e['gradientEhPerBohr']).all()
 rows=json.loads((branch/'step-provenance.json').read_text())
 selected=[r for r in rows if r['accepted'] and not r['endpointOptimization']]
 points=[];previous=record()['energyHartree']
 for r in selected:
  x=np.array(r['coordinatesBohr'])
  e=min(ev,key=lambda e:np.max(abs(np.array(e['coordinatesBohr'])-x)))
  assert np.max(abs(np.array(e['coordinatesBohr'])-x))<1e-8
  step=e['energyHartree']-previous;assert step<3e-6
  points.append(dict(evaluation=e['evaluation'],energyHartree=e['energyHartree'],energyIncrementHartree=step,formingDistancesAngstrom=[float(np.linalg.norm(x[i]-x[j])*BOHR) for i,j in [(0,4),(3,5)]]))
  previous=e['energyHartree']
 report=dict(numericalConsistency='pass',rawEvaluations=len(ev),acceptedIRCPoints=len(points),maximumAcceptedEnergyIncreaseHartree=max(p['energyIncrementHartree'] for p in points),lastAcceptedPoint=points[-1],driverComplete=False,driverConverged=False,scope='Recovered interrupted branch only. No endpoint verification, infinite separation or completed IRC connection is claimed.')
 write(folder/'validation.json',report);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
