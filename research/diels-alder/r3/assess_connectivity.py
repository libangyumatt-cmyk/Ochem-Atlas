"""Independent endpoint nuclear/electronic checks and chemical-region assessment.
A failed IRC descent check remains a failure even if endpoint minima pass.
"""
from pathlib import Path
import sys,os,json,itertools
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r2'))
from common import *
from compare_endpoints import rmsd
from pyscf.hessian import thermo
folder=Path(os.environ.get('OCHEM_R3_BACKWARD_OUTPUT',str(BASE/'r3/backward-attempt1')))/'endpoints/backward'

def equivalent_rmsd(x,y,pairs):
 values=[]
 for choices in itertools.product([False,True],repeat=len(pairs)):
  ids=list(range(len(x)))
  for swap,(a,b) in zip(choices,pairs):
   if swap:ids[a],ids[b]=ids[b],ids[a]
  values.append(rmsd(x[ids],y))
 return min(values)

def torsion(x):
 a,b,c,d=x;v=b-a;axis=c-b;axis/=np.linalg.norm(axis);u=d-c;n1=np.cross(v,axis);n2=np.cross(axis,u)
 return float(np.degrees(np.arctan2(np.dot(np.cross(n1,n2),axis),np.dot(n1,n2))))

def main():
 v=json.loads((folder/'verification.json').read_text());w=np.load(folder/'wavefunction.npz');x=w['coordinatesAngstrom'];assert np.max(abs(x-v['coordinatesAngstrom']))<1e-12
 assert v['elements']==['C']*6+['H']*10 and v['scfConverged']
 m=gto.M(atom=list(zip(v['elements'],x)),basis='6-31g(d)',verbose=0);s=m.intor('int1e_ovlp');assert np.max(abs(s-w['overlap']))<1e-10
 assert np.max(abs(w['mo_coeff'].T@s@w['mo_coeff']-np.eye(m.nao)))<1e-8 and abs(np.einsum('ij,ji',w['density_matrix'],s)-46)<1e-8
 h=w['hessian'];hs=(h+h.transpose(1,0,3,2))/2;fr=thermo.harmonic_analysis(m,hs)['freq_wavenumber'];freq=np.array([-abs(z.imag) if abs(z.imag)>1e-8 else z.real for z in fr]);assert np.max(abs(freq-v['frequenciesCm']))<1e-5
 assert abs(abs(w['gradient']).max()-v['maxFullResponseGradientEhPerBohr'])<1e-12
 passed=bool(min(freq)>0 and abs(w['gradient']).max()<2e-4 and v['internalStable'] and v['externalStable']);assert passed==v['minimumVerified']
 edges=[(i,j) for i in range(6) for j in range(i+1,6) if np.linalg.norm(x[i]-x[j])<1.85];wanted=[(0,1),(1,2),(2,3),(4,5)]
 parents={6:0,7:0,8:1,9:2,10:3,11:3,12:4,13:4,14:5,15:5};hydrogen=all([i for i in range(6) if np.linalg.norm(x[k]-x[i])<1.3]==[p] for k,p in parents.items())
 fragments=[];referenceEnergy=0.
 for name,ids,pairs,ncarbon in [('reactant-butadiene',[0,1,2,3,6,7,8,9,10,11],[(4,5),(8,9)],4),('reactant-ethylene',[4,5,12,13,14,15],[(2,3),(4,5)],2)]:
  ref=record(name);y=np.array([a['xyzAngstrom'] for a in ref['atoms']]);referenceEnergy+=ref['energyHartree']
  item=dict(reference=name,carbonRmsdAngstrom=rmsd(x[ids][:ncarbon],y[:ncarbon]),fixedMapAllAtomRmsdAngstrom=rmsd(x[ids],y),equivalentHydrogenAllAtomRmsdAngstrom=equivalent_rmsd(x[ids],y,pairs))
  if ncarbon==4:item.update(endpointDieneTorsionDegrees=torsion(x[:4]),referenceDieneTorsionDegrees=torsion(y[:4]))
  fragments.append(item)
 r=dict(minimumVerified=passed,energyHartree=v['energyHartree'],maxFullResponseGradientEhPerBohr=float(abs(w['gradient']).max()),lowestFrequencyCm=float(min(freq)),internalStable=v['internalStable'],externalStable=v['externalStable'],mappedCarbonConnectivityMatchesExpected=edges==wanted,mappedHydrogenParentsMatch=hydrogen,carbonEdgesOneBased=[[a+1,b+1] for a,b in edges],formingDistancesAngstrom=[float(np.linalg.norm(x[a]-x[b])) for a,b in [(0,4),(3,5)]],fragments=fragments,energyRelativeToIndependentIsolatedR1ReactantsHartree=v['energyHartree']-referenceEnergy,finiteDistanceEncounterRegion=True,infinitelySeparatedReactants=False,referenceLimitation='Independent isolated butadiene reference is s-trans; a different diene conformer contributes deformation energy. No universal experimental activation baseline.',strictTwoMinimumIrcConnectivityVerified=False,interpretation='Endpoint checks do not repair the accepted uphill IRC step or convert subsequent forward-ring relaxations into IRC points.')
 write(folder/'independent-validation.json',r);print(json.dumps(r,indent=2))
 path=json.loads((folder.parents[1]/'backward/independent-validation.json').read_text());forward=json.loads((ROOT/'audit/V037_R3_STAGE_B.json').read_text())
 assessment=dict(stage='D',result='IRC validation incomplete',reactantEndpoint=r,forwardEndpointAssessment=forward,backwardDriverConverged=path['driverConverged'],backwardDescentCheckPassed=path['descentCheckPassed'],uphillStepsExceedingTolerance=path['uphillStepsExceedingTolerance'],strictTwoMinimumIrcConnectivityVerified=False,electronicStructureSeriesStage='E deferred in its entirety',remainingWork=['Resolve forced minimum-trust-radius IRC step with a documented new integration attempt.','Establish the forward IRC relation to unstable ring endpoint and relaxed product minima without relabeling ordinary optimization points.','Resolve any failed endpoint vibrational check before claiming a minimum.','Only then select IRC electronic-structure geometries.'])
 write(ROOT/'audit/V037_R3_CONNECTIVITY.json',assessment)
if __name__=='__main__':main()
