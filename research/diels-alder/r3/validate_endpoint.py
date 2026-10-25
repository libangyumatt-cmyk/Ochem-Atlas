"""Independent saved-array validation; no SCF. Does not certify an IRC."""
from pathlib import Path
import sys,itertools
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r2'))
from common import *
from compare_endpoints import rmsd
from pyscf.hessian import thermo
folder=BASE/'r3'/('endpoint-'+sys.argv[1]);v=json.loads((folder/'verification.json').read_text());w=np.load(folder/'wavefunction.npz');x=w['coordinatesAngstrom']
assert v['scfConverged'] and np.max(abs(x-v['coordinatesAngstrom']))<1e-12
m=gto.M(atom=list(zip(v['elements'],x)),basis='6-31g(d)',verbose=0);s=m.intor('int1e_ovlp')
assert np.max(abs(s-w['overlap']))<1e-10
assert np.max(abs(w['mo_coeff'].T@s@w['mo_coeff']-np.eye(m.nao)))<1e-8
assert abs(np.einsum('ij,ji',w['density_matrix'],s)-46)<1e-8
h=w['hessian'];hs=(h+h.transpose(1,0,3,2))/2
fr=thermo.harmonic_analysis(m,hs)['freq_wavenumber'];freq=np.array([-abs(z.imag) if abs(z.imag)>1e-8 else z.real for z in fr]);assert max(abs(freq-v['frequenciesCm']))<1e-5
assert abs(abs(w['gradient']).max()-v['maxFullResponseGradientEhPerBohr'])<1e-12
ref=record('product');y=np.array([a['xyzAngstrom'] for a in ref['atoms']])
edges=[(i,j) for i in range(6) for j in range(i+1,6) if np.linalg.norm(x[i]-x[j])<1.85]
expected=[(0,1),(0,4),(1,2),(2,3),(3,5),(4,5)]
parents={6:0,7:0,8:1,9:2,10:3,11:3,12:4,13:4,14:5,15:5}
hydrogen=all([i for i in range(6) if np.linalg.norm(x[k]-x[i])<1.3]==[p] for k,p in parents.items())
best=rmsd(x,y)
for choices in itertools.product([False,True],repeat=4):
 ids=list(range(16))
 for swap,(a,b) in zip(choices,[(6,7),(10,11),(12,13),(14,15)]):
  if swap:ids[a],ids[b]=ids[b],ids[a]
 best=min(best,rmsd(x[ids],y))
passed=bool(min(freq)>0 and abs(w['gradient']).max()<2e-4 and v['internalStable'] and v['externalStable'])
assert passed==v['minimumVerified']
r=dict(minimumVerified=passed,lowestFrequencyCm=float(min(freq)),energyHartree=v['energyHartree'],maxGradientEhPerBohr=float(abs(w['gradient']).max()),mappedCarbonConnectivityMatches=edges==expected,mappedHydrogenConnectivityMatches=hydrogen,carbonRmsdAngstrom=rmsd(x[:6],y[:6]),fixedMapAllAtomRmsdAngstrom=rmsd(x,y),equivalentHydrogenAllAtomRmsdAngstrom=best,energyDifferenceFromIndependentProductHartree=v['energyHartree']-ref['energyHartree'],formingDistancesAngstrom=[float(np.linalg.norm(x[a]-x[b])) for a,b in [(0,4),(3,5)]],scope='Proper rotations and translations removed; four same-carbon H pairs enumerated. Distinct conformers are not identified as identical. Saved stability flags retained, not recomputed by this algebraic validator. This endpoint optimization alone does not verify IRC connectivity.')
write(folder/'independent-validation.json',r);print(json.dumps(r,indent=2))
