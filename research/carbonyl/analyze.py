"""Add explicitly defined Löwdin-orthogonalized Wiberg indices and MO gaps.
Reads full wavefunctions; does not alter wavefunctions or volumetric fields.
"""
import json
import numpy as np
from pyscf import gto
from compute import OUT,BASIS

def main():
 d=json.loads((OUT/'carbonyl.json').read_text())
 d['bondOrderConventions']={'mayer':'sum over AO blocks A/B of (PS)uv(PS)vu, spin-summed RHF P.',
  'lowdinWiberg':'sum over AO blocks A/B of |(S^(1/2) P S^(1/2))uv|^2, symmetric positive overlap square root. Not NBO Wiberg; basis and partition dependent.'}
 for f in d['frames']:
  wf=np.load(OUT/(f['id']+'-scf.npz'));s=wf['overlap'];ev,u=np.linalg.eigh(s);assert ev.min()>1e-7
  sq=(u*np.sqrt(ev))@u.T;p=sq@wf['density_matrix']@sq
  m=gto.M(atom=[(a['element'],a['xyzAngstrom']) for a in f['atoms']],basis=BASIS,charge=-1,spin=0,verbose=0);sl=m.aoslice_by_atom()
  for b in f['bonds']:
   a,c=b['atoms'];i,j=sl[a,2:];k,l=sl[c,2:];b['lowdinWiberg']=float(np.sum(abs(p[i:j,k:l])**2))
  for o in f['orbitals']:
   j=o['index']-1;block=np.where(wf['mo_occ']==o['occupation'])[0];other=[abs(wf['mo_energy'][j]-wf['mo_energy'][k]) for k in block if k!=j]
   o['nearestSameOccupationGapEh']=float(min(other));o['nearDegenerate']=bool(min(other)<1e-5)
 (OUT/'inputs.json').write_text(json.dumps(dict(method=d['method'],basis=d['basis'],charge=d['charge'],multiplicity=d['multiplicity'],environment=d['environment'],scf=d['scfProtocol'],frames=[dict(id=f['id'],atoms=f['atoms'],fixedParameters=None if f.get('stationaryPointVerified') else dict(distanceAngstrom=f['distanceAngstrom'],angleDegree=f['angleDegree']),symmetry='Cs optimization parameterization; full Cartesian gradient/Hessian checked for product') for f in d['frames']]),indent=2))
 (OUT/'carbonyl.json').write_text(json.dumps(d,indent=2))
if __name__=='__main__':main()
