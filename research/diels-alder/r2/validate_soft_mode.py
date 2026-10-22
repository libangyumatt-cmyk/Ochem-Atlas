"""Independently reconstruct probe positions, metric identities and curvatures."""
from common import *
lib.num_threads(1)

def main():
 folder=OUT/'soft-mode';definition=json.loads((folder/'definition.json').read_text());data=json.loads((folder/'results.json').read_text());x=np.array(definition['coordinatesAngstrom']);v=np.array(definition['cartesianUnitMode']);assert abs(np.linalg.norm(v)-1)<1e-12
 assert definition['sourceWavefunctionSha256']==hashlib.sha256((OUT/'endpoints/forward/wavefunction.npz').read_bytes()).hexdigest()
 elems=[a['element'] for a in record()['atoms']];energies={};assert len(data['points'])==10
 for r in data['points']:
  w=np.load(folder/(r['id']+'.npz'));expected=x+r['displacementNormAngstrom']*v;assert np.max(abs(w['coordinatesAngstrom']-expected))<1e-12
  assert r['scfConverged'] and r['scfOrbitalGradientNorm']<3e-7
  m=gto.M(atom=list(zip(elems,expected)),basis='6-31g(d)',verbose=0);s=m.intor('int1e_ovlp')
  assert np.max(abs(w['mo_coeff'].T@s@w['mo_coeff']-np.eye(m.nao)))<1e-8
  assert abs(np.einsum('ij,ji',w['density_matrix'],s)-46)<1e-8 and abs(float(w['energyHartree'])-r['energyHartree'])<1e-12
  energies[r['gridLevel'],r['displacementNormAngstrom']]=r['energyHartree']
 for r in data['directionalChecks']:
  g,h=r['gridLevel'],r['displacementNormAngstrom'];curvature=(energies[g,h]+energies[g,-h]-2*energies[g,0.])/(h/BOHR)**2
  assert abs(curvature-r['energyCurvatureEhPerBohr2'])<1e-12
 write(folder/'validation.json',dict(result='pass',pointCount=10,curvatureRows=4,scope='Reconstruction/normalization of actual directional energy probes; not full Hessian or IRC validation.'))
 print('PASS: ten actual energy probes and four directional curvatures',flush=True)

if __name__=='__main__':main()
