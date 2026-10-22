"""Independent raw-trial path/provenance and endpoint numerical checks."""
from common import *
from geometric.molecule import PeriodicTable
from pyscf.hessian import thermo
lib.num_threads(1)

def evaluations(folder):
 paths=sorted(folder.glob('eval-*.json'))
 if paths:return [json.loads(p.read_text()) for p in paths]
 with zipfile.ZipFile(folder/'evaluations.zip') as z:return [json.loads(z.read(n)) for n in sorted(z.namelist()) if n.endswith('.json')]

def main():
 report=dict(result='incomplete',branches={},endpoints={},limitations=[])
 elems=[a['element'] for a in record()['atoms']];mass=np.array([PeriodicTable[e] for e in elems]);start=np.array([a['xyzAngstrom'] for a in record()['atoms']])/BOHR
 report['coordinateConvention']=dict(massesAmu=mass.tolist(),units='bohr sqrt(amu)',metric='Sum of sqrt(sum_i mass_i * |delta Cartesian r_i|^2) over accepted points. Discrete chord length, not exact analytic arc length. No step interpolation. Fixed r1 atom mapping; native laboratory coordinates with no independent per-point rotation.')
 for direction in ['forward','backward']:
  folder=OUT/direction;state=json.loads((folder/'status.json').read_text());ev=evaluations(folder)
  assert ev and np.max(abs(np.array(ev[0]['coordinatesBohr'])-start))<1e-8
  for name,sha in state['initialSources'].items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==sha
  for e in ev:
   assert e['scfConverged'] and abs(e['electronCount']-46)<1e-8 and e['orbitalGradientNorm']<3e-6
   assert np.array(e['coordinatesBohr']).shape==(16,3) and np.isfinite(e['coordinatesBohr']).all() and np.isfinite(e['gradientEhPerBohr']).all()
  rows=json.loads((folder/'step-provenance.json').read_text());accepted=[r for r in rows if r['accepted'] and not r['endpointOptimization']];points=[];previous=start;cumulative=0.;previous_energy=record()['energyHartree'];uphill=[]
  for r in accepted:
   x=np.array(r['coordinatesBohr']);e=min(ev,key=lambda e:np.max(abs(np.array(e['coordinatesBohr'])-x)));assert np.max(abs(np.array(e['coordinatesBohr'])-x))<1e-8
   cumulative+=float(np.sqrt(np.sum(mass[:,None]*(x-previous)**2)));uphill.append(e['energyHartree']-previous_energy)
   points.append(dict(evaluation=e['evaluation'],energyHartree=e['energyHartree'],coordinatesAngstrom=(x*BOHR).tolist(),formingDistancesAngstrom=[float(np.linalg.norm(x[i]-x[j])*BOHR) for i,j in [(0,4),(3,5)]],cumulativeChordLengthBohrSqrtAmu=cumulative));previous=x;previous_energy=e['energyHartree']
  largest=max(uphill) if uphill else None
  report['branches'][direction]=dict(driverComplete=state['complete'],driverConverged=state['driverConverged'],rawEvaluations=len(ev),acceptedIRCPoints=points,maximumAcceptedEnergyIncreaseHartree=largest)
  if not state['complete'] or not state['driverConverged']:report['limitations'].append(direction+' driver convergence incomplete')
  if not points or largest>3e-6:report['limitations'].append(direction+' failed 3e-6 Eh accepted-step descent tolerance')
  folder=OUT/'endpoints'/direction;p=folder/'verification.json'
  if not p.exists():report['limitations'].append(direction+' independent endpoint verification missing');continue
  v=json.loads(p.read_text());w=np.load(folder/'wavefunction.npz');assert v['elements']==elems
  m=gto.M(atom=list(zip(elems,v['coordinatesAngstrom'])),basis='6-31g(d)',verbose=0);s=m.intor('int1e_ovlp');assert np.max(abs(w['mo_coeff'].T@s@w['mo_coeff']-np.eye(m.nao)))<1e-8
  assert abs(np.einsum('ij,ji',w['density_matrix'],s)-46)<1e-8
  fr=thermo.harmonic_analysis(m,w['hessian'])['freq_wavenumber'];freq=np.array([-abs(z.imag) if abs(z.imag)>1e-8 else z.real for z in fr]);assert max(abs(freq-v['frequenciesCm']))<1e-5
  assert abs(float(abs(w['gradient']).max())-v['maxFullResponseGradientEhPerBohr'])<1e-12
  passed=bool(min(freq)>0 and abs(w['gradient']).max()<2e-4 and v['scfConverged'] and v['internalStable'] and v['externalStable']);report['endpoints'][direction]=dict(minimumVerified=passed,lowestFrequencyCm=float(min(freq)),energyHartree=v['energyHartree'])
  if not passed:report['limitations'].append(direction+' endpoint failed minimum verification')
 for name,sha in json.loads((ROOT/'audit/V037_R2_PRESERVED_DATA.json').read_text()).items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
 report['preservation']='All protected scientific files match their baseline hashes.'
 if not report['limitations']:report['result']='path-and-minima-pass-pending-connectivity-comparison'
 write(OUT/'path-validation.json',report)
 print(report['result'],report['limitations'],flush=True)

if __name__=='__main__':main()
