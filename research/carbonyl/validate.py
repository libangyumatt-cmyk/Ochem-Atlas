"""Independent reconstruction of energies, normalization, geometry, fields,
fragment references, bond indices, MO assignment and product Hessian.
Run with OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1.
"""
import json,hashlib
import numpy as np
from pyscf import gto,scf,lib,dft
from pyscf.hessian import thermo
from scipy.optimize import linear_sum_assignment
from compute import OUT,BASIS,BOHR
lib.num_threads(1)
try:lib.current_memory()
except FileNotFoundError:lib.current_memory=lambda:(0,0)
def integrate(m,p):
 g=dft.gen_grid.Grids(m);g.level=5;g.build();v=0
 for i in range(0,len(g.coords),10000):
  a=m.eval_gto('GTOval_sph',g.coords[i:i+10000]);v+=np.einsum('pi,ij,pj->p',a,p,a)@g.weights[i:i+10000]
 return float(v)
def main():
 d=json.loads((OUT/'carbonyl.json').read_text());assert d['charge']==-1 and d['multiplicity']==1 and d['electronCount']==18
 reports=[];states={};ref=None;grid=d['grid'];n=np.array(grid['shape']);origin=np.array(grid['originBohr']);step=grid['spacingBohr']
 # Fixed reproducible sampled grid points, plus points nearest each nucleus.
 rng=np.random.default_rng(360);ix=rng.integers(0,n,size=(700,3));idx=np.ravel_multi_index(ix.T,n);points=origin+ix*step
 for f in d['frames']:
  id=f['id'];a=[(x['element'],x['xyzAngstrom']) for x in f['atoms']];m=gto.M(atom=a,basis=BASIS,charge=-1,spin=0,verbose=0)
  wf=np.load(OUT/(id+'-scf.npz'));tr=np.load(OUT/(id+'-tracked.npz'));fields=np.load(OUT/(id+'-fields.npz'));s=m.intor('int1e_ovlp');c=wf['mo_coeff'];p=wf['density_matrix'];tc=tr['mo_coeff'];inds=tr['indices']
  assert f['sourceWavefunctionSha256']==hashlib.sha256((OUT/(id+'-scf.npz')).read_bytes()).hexdigest()
  assert m.nelectron==18 and m.spin==0 and abs(c.T@s@c-np.eye(m.nao)).max()<1e-9
  assert abs(p-(c*wf['mo_occ'])@c.T).max()<1e-9 and abs(np.einsum('ij,ji',p,s)-18)<1e-8
  assert abs(m.atom_coords()*BOHR-wf['coordinates']).max()<1e-9
  mf=scf.RHF(m);mf.mo_coeff=c;mf.mo_occ=wf['mo_occ'];mf.mo_energy=wf['mo_energy'];mf.e_tot=mf.energy_tot(dm=p)
  assert abs(mf.e_tot-f['energyHartree'])<1e-8
  assert np.linalg.norm(mf.get_grad(c,wf['mo_occ'],mf.get_fock(dm=p)))<1e-6
  _,_,si,se=mf.stability(internal=True,external=True,return_status=True);assert si and se
  grad=mf.nuc_grad_method().kernel();assert abs(grad-wf['gradient']).max()<1e-8
  if not f.get('stationaryPointVerified'):
   # Four free Cs internal parameters: O x, Hpair x/y/z.
   g=grad/BOHR;free=np.array([g[1,0],g[2,0]+g[3,0],g[2,1]-g[3,1],g[2,2]+g[3,2]])
   assert abs(free).max()<1e-5
  count=integrate(m,p);assert abs(count-18)<5e-4 and abs(count-f['quadratureElectronCount'])<1e-7
  ao=m.eval_gto('GTOval_sph',points);rho=np.einsum('pi,ij,pj->p',ao,p,ao)
  assert np.allclose(fields['total'].ravel()[idx],rho,rtol=2e-6,atol=2e-7)
  if ref is None:ref=rho
  assert np.allclose(fields['difference'].ravel()[idx],rho-ref,rtol=1e-5,atol=2e-7)
  fragment=[];fragment_checks=[]
  for x in f['fragments']:
   fm=gto.M(atom=[a[j] for j in x['atomIndices']],basis=BASIS,charge=x['charge'],spin=0,verbose=0);fw=np.load(OUT/(id+'-'+x['id']+'-scf.npz'));fd=fw['density_matrix'];fa=fm.eval_gto('GTOval_sph',points)
   assert abs(fm.atom_coords()*BOHR-fw['coordinates']).max()<1e-9
   assert abs(integrate(fm,fd)-fm.nelectron)<5e-4
   ff=scf.RHF(fm);ff.mo_coeff=fw['mo_coeff'];ff.mo_occ=fw['mo_occ'];ff.mo_energy=fw['mo_energy'];ff.e_tot=ff.energy_tot(dm=fd)
   assert abs(ff.e_tot-x['energyHartree'])<1e-8
   _,_,fi,fe=ff.stability(internal=True,external=True,return_status=True)
   assert bool(fi)==x['internalStable'] and bool(fe)==x['externalStable']
   fragment_checks.append(dict(id=x['id'],internalStable=bool(fi),externalStable=bool(fe)))
   fragment.append(np.einsum('pi,ij,pj->p',fa,fd,fa))
  assert np.allclose(fields['deformation'].ravel()[idx],rho-sum(fragment),rtol=1e-5,atol=2e-7)
  for role,j,o in zip(['donor','pi','pistar'],inds,f['orbitals']):
   assert o['index']==j+1 and abs(abs(c[:,j]@s@tc[:,j])-1)<1e-9
   assert np.allclose(fields[role].ravel()[idx],ao@tc[:,j],rtol=3e-6,atol=2e-7)
  if f['tracking']:
   pm,pc,pi=states[f['tracking'][0]['parentFrame']];cross=pc.T@gto.intor_cross('int1e_ovlp',pm,m)@c;assign={}
   for block in [np.where(wf['mo_occ']>0)[0],np.where(wf['mo_occ']==0)[0]]:
    rows,cols=linear_sum_assignment(-abs(cross[np.ix_(block,block)]));assign.update({int(block[x]):int(block[y]) for x,y in zip(rows,cols)})
   for old,j,t in zip(pi,inds,f['tracking']):
    assert assign[int(old)]==j and abs(abs(cross[old,j])-t['alignedOverlap'])<1e-8
    assert pc[:,old]@gto.intor_cross('int1e_ovlp',pm,m)@tc[:,j]>0
  states[id]=(m,tc,inds)
  ps=p@s;ev,u=np.linalg.eigh(s);sq=(u*np.sqrt(ev))@u.T;po=sq@p@sq;sl=m.aoslice_by_atom();xyz=m.atom_coords()*BOHR
  for b in f['bonds']:
   aa,bb=b['atoms'];i,j=sl[aa,2:];k,l=sl[bb,2:]
   assert abs(np.linalg.norm(xyz[aa]-xyz[bb])-b['distanceAngstrom'])<1e-9
   assert abs(np.sum(ps[i:j,k:l]*ps[k:l,i:j].T)-b['mayer'])<1e-8
   assert abs(np.sum(abs(po[i:j,k:l])**2)-b['lowdinWiberg'])<1e-8
  co=xyz[1]-xyz[0];nu=xyz[4]-xyz[0];angle=np.degrees(np.arccos(np.dot(co,nu)/np.linalg.norm(co)/np.linalg.norm(nu)));assert abs(angle-f['angleDegree'])<1e-8
  if f.get('stationaryPointVerified'):
   hw=np.load(OUT/(id+'-hessian.npz'));assert abs(grad).max()<2e-5
   # Recompute analytic Hessian rather than trusting the saved frequencies.
   hh=mf.Hessian().kernel();assert abs(hh-hw['hessian']).max()<1e-7
   fr=thermo.harmonic_analysis(m,hh)['freq_wavenumber'];assert len(fr)==9 and all(x.real>20 and abs(x.imag)<1 for x in fr)
   assert np.max(abs(fr.real-np.array(f['frequenciesCm'])))<.01
  reports.append(dict(id=id,energyHartree=float(mf.e_tot),independentQuadratureElectronCount=count,maximumNuclearGradient=float(abs(grad).max()),complexStability=[bool(si),bool(se)],fragmentStability=fragment_checks,passed=True))
  print('PASS',id,'E',mf.e_tot,'N',count,flush=True)
 (OUT/'validation.json').write_text(json.dumps(dict(program='independent AO reconstruction using PySCF',frames=reports,sampledGridPoints=700,checks='energy, nuclear/SCF gradients, AO metric, quadrature, actual field samples, fragments, Hungarian/sign mapping, two bond indices, distances/angles, recomputed product Hessian',result='pass'),indent=2))
if __name__=='__main__':main()
