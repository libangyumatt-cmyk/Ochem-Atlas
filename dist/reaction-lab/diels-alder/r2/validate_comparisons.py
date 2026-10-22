"""Independent reconstruction of new method diagnostics from retained arrays."""
from common import *
lib.num_threads(1)

def main():
 folder=OUT/'comparisons';rows=[]
 for file in sorted(folder.glob('*.json')):
  if file.name.endswith('-progress.json') or file.name=='validation.json':continue
  r=json.loads(file.read_text());name=file.stem;source=record(r['case'])
  assert r['geometrySha256']==hashlib.sha256((BASE/(r['case']+'.json')).read_bytes()).hexdigest()
  x=np.array([a['xyzAngstrom'] for a in source['atoms']]);elements=[a['element'] for a in source['atoms']]
  w=np.load(folder/(name+'-analysis.npz'));m=gto.M(atom=list(zip(elements,x)),basis=r['basis'],verbose=0);s=m.intor('int1e_ovlp');p=w['density_matrix']
  assert np.max(abs(x-w['coordinatesAngstrom']))<1e-10
  assert r['scfConverged'] and r['scfOrbitalGradientNorm']<3e-6
  assert np.max(abs(w['mo_coeff'].T@s@w['mo_coeff']-np.eye(m.nao)))<1e-8
  assert abs(np.einsum('ij,ji',p,s)-m.nelectron)<1e-8 and abs(r['electronCount']-m.nelectron)<1e-8
  assert np.max(abs(p-p.T))<1e-10
  if 'correlationEnergyHartree' in r:assert abs(r['energyHartree']-r['referenceEnergyHartree']-r['correlationEnergyHartree'])<1e-10
  ev,u=np.linalg.eigh(s);root=(u*np.sqrt(ev))@u.T;q=root@p@root;ps=p@s;sl=m.aoslice_by_atom()
  for bond in r['bonds']:
   i,j=bond['atoms'];a,b=sl[i,2:];c,d=sl[j,2:]
   assert abs(bond['distanceAngstrom']-np.linalg.norm(x[i]-x[j]))<1e-10
   assert abs(bond['mayer']-np.sum(ps[a:b,c:d]*ps[c:d,a:b].T))<1e-10
   assert abs(bond['lowdinWiberg']-np.sum(q[a:b,c:d]**2))<1e-10
  if 'sampleCoordinatesBohr' in w:
   points=w['sampleCoordinatesBohr'][::137];om=gto.M(atom=list(zip(elements,x)),basis='6-31g(d)',verbose=0);old=np.load(BASE/(r['case']+'-scf.npz'))
   a=m.eval_gto('GTOval_sph',points);b=om.eval_gto('GTOval_sph',points);delta=np.einsum('pi,ij,pj->p',a,p,a)-np.einsum('pi,ij,pj->p',b,old['density_matrix'],b)
   assert max(abs(delta-w['sameGeometryDensityDifference'][::137]))<1e-10
   tracked=np.load(BASE/(r['case']+'-tracked.npz'));cross=gto.intor_cross('int1e_ovlp',om,m)
   for match in r['orbitalMatches']:
    j,k=match['r1Index']-1,match['comparisonIndex']-1;proj=tracked['mo_coeff'][:,j]@cross@w['mo_coeff'];block=np.where(w['mo_occ']>0 if match['role']=='occupied' else w['mo_occ']==0)[0]
    assert k in block and abs(abs(proj[k])-match['absoluteSpatialOverlap'])<1e-10 and abs(proj[k])>=max(abs(proj[block]))-1e-10
    assert proj[k]*match['phaseToMatchR1']>=0
  rows.append(dict(case=name,numericalConsistencyPassed=True,referenceInternalStable=r['referenceInternalStable'],referenceExternalStable=r['referenceExternalStable']))
 write(folder/'validation.json',dict(result='pass' if len(rows)==12 else 'partial',completedCases=len(rows),cases=rows,interpretation='Consistency of retained calculations. A pass does not validate an unstable reference or establish method convergence.'))
 print('Independently checked',len(rows),'comparison cases',flush=True)

if __name__=='__main__':main()
