"""Compare independently relaxed IRC endpoint candidates to retained r1 minima.
Connectivity uses explicit 1.85 Å carbon and 1.30 Å C–H diagnostic cutoffs,
not a bond-order definition. Different conformers are reported, not relabeled.
"""
from common import *

def rmsd(x,y):
 x=np.array(x);y=np.array(y);a=x-x.mean(0);b=y-y.mean(0);u,_,vh=np.linalg.svd(a.T@b);rot=u@np.diag([1,1,np.linalg.det(u@vh)])@vh
 return float(np.sqrt(np.mean(np.sum((a@rot-b)**2,axis=1))))

def main():
 path=json.loads((OUT/'path-validation.json').read_text());report=dict(result='incomplete',pathValidationResult=path['result'],endpoints={},limitations=list(path['limitations']))
 graph_product={(0,1),(1,2),(2,3),(3,5),(4,5),(0,4)};graph_reactant={(0,1),(1,2),(2,3),(4,5)}
 refs={name:record(name) for name in ['product','reactant-butadiene','reactant-ethylene']}
 hydrogen_parents={6:0,7:0,8:1,9:2,10:3,11:3,12:4,13:4,14:5,15:5}
 for direction in ['forward','backward']:
  file=OUT/'endpoints'/direction/'verification.json'
  if not file.exists():continue
  v=json.loads(file.read_text());x=np.array(v['coordinatesAngstrom']);actual={(i,j) for i in range(6) for j in range(i+1,6) if np.linalg.norm(x[i]-x[j])<1.85};wanted=graph_product if direction=='forward' else graph_reactant
  hydrogen_ok=all([i for i in range(6) if np.linalg.norm(x[h]-x[i])<1.3]==[parent] for h,parent in hydrogen_parents.items())
  row=dict(minimumVerified=path['endpoints'][direction]['minimumVerified'],mappedCarbonConnectivityMatchesExpected=actual==wanted,mappedHydrogenParentsMatch=hydrogen_ok,carbonEdges=sorted(map(list,actual)),formingDistancesAngstrom=[float(np.linalg.norm(x[i]-x[j])) for i,j in [(0,4),(3,5)]])
  if direction=='forward':
   old=refs['product'];y=np.array([a['xyzAngstrom'] for a in old['atoms']]);row.update(carbonRmsdToIndependentR1Angstrom=rmsd(x[:6],y[:6]),fixedLabelAllAtomRmsdToIndependentR1Angstrom=rmsd(x,y),energyDifferenceFromIndependentR1Hartree=v['energyHartree']-old['energyHartree'])
  else:
   row['finiteDistanceEncounterRegion']=True;row['notInfinitelySeparatedReactants']=True;row['energyRelativeToIndependentIsolatedR1ReactantsHartree']=v['energyHartree']-refs['reactant-butadiene']['energyHartree']-refs['reactant-ethylene']['energyHartree'];row['fragments']=[]
   for name,ids in [('reactant-butadiene',[0,1,2,3,6,7,8,9,10,11]),('reactant-ethylene',[4,5,12,13,14,15])]:
    y=np.array([a['xyzAngstrom'] for a in refs[name]['atoms']]);n=4 if name=='reactant-butadiene' else 2
    row['fragments'].append(dict(reference=name,carbonRmsdAngstrom=rmsd(x[ids][:n],y[:n]),fixedLabelAllAtomRmsdAngstrom=rmsd(x[ids],y),interpretation='Fixed mapping comparison; conformer changes and equivalent-H labels can increase RMSD. No new isolated reactant optimization.'))
  report['endpoints'][direction]=row
  if actual!=wanted or not hydrogen_ok:report['limitations'].append(direction+' mapped connectivity check failed')
 if not report['limitations'] and len(report['endpoints'])==2:report['result']='pass'
 report['scope']='Verified connection toward stated bonding regions only when all checks pass. Endpoint minimizations are separate from IRC. No infinite separation, conformer global-minimum guarantee, competing-pathway exclusion or universal synchronicity is claimed.'
 write(OUT/'connectivity-validation.json',report);print(report['result'],report['limitations'],flush=True)

if __name__=='__main__':main()
