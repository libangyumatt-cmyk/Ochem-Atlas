"""Targeted fixed-r1-geometry method/basis/grid diagnostics; no reoptimization.
Run one case/tag at a time, or use --all for separately checkpointed processes.
An unstable reference is retained and flagged, never treated as validation.
"""
from common import *
import subprocess,fcntl
from pyscf import scf
from pyscf.mp.dfmp2_native import DFRMP2
from pyscf.df.addons import make_auxbasis

def main():
 folder=OUT/'comparisons';folder.mkdir(exist_ok=True)
 cases=['reactant-ethylene','reactant-butadiene','ts','product'];tags=['grid5','def2tzvp','ri-mp2-def2tzvp']
 if '--all' in sys.argv:
  for case in cases:
   for tag in tags:subprocess.run([sys.executable,'-u',__file__,case,tag],check=True)
  return
 case,tag=sys.argv[1:3];assert case in cases and tag in tags;name=case+'-'+tag;target=folder/(name+'.json')
 case_lock=(folder/(name+'.run.lock')).open('a');fcntl.flock(case_lock,fcntl.LOCK_EX)
 if target.exists():print('Retained completed',name,flush=True);return
 source=record(case);elements=[a['element'] for a in source['atoms']];x=np.array([a['xyzAngstrom'] for a in source['atoms']])/BOHR
 basis='6-31g(d)' if tag=='grid5' else 'def2-tzvp';grid=5 if tag=='grid5' else 3
 if tag=='ri-mp2-def2tzvp':
  m=gto.M(atom=list(zip(elements,x)),unit='Bohr',basis=basis,charge=0,spin=0,max_memory=1200,verbose=4,output=str(folder/(name+'.log')))
  f=scf.RHF(m).density_fit();f.conv_tol=1e-10;f.conv_tol_grad=1e-6;f.max_cycle=120;f.kernel();assert f.converged
 else:m,f=solve(x,folder/(name+'.log'),grid=grid,basis=basis,elements=elements)
 s=m.intor('int1e_ovlp');p=f.make_rdm1()
 save_npz(folder/(name+'-scf.npz'),coordinatesAngstrom=x*BOHR,mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,density_matrix=p,overlap=s)
 write(folder/(name+'-progress.json'),dict(stage='SCF converged; stability and analysis pending',energyHartree=float(f.e_tot)))
 _,_,si,se=f.stability(internal=True,external=True,return_status=True)
 write(folder/(name+'-progress.json'),dict(stage='Reference stability completed; final analysis pending',internalStable=bool(si),externalStable=bool(se)))
 result=dict(case=case,tag=tag,geometrySource=case+'.json (unchanged r1 optimized geometry)',geometrySha256=hashlib.sha256((BASE/(case+'.json')).read_bytes()).hexdigest(),method='RI-RMP2' if tag=='ri-mp2-def2tzvp' else 'B3LYP (VWN-RPA)',basis=basis,gridLevel=None if tag=='ri-mp2-def2tzvp' else grid,charge=0,multiplicity=1,scfConverged=bool(f.converged),scfOrbitalGradientNorm=float(np.linalg.norm(f.get_grad(f.mo_coeff,f.mo_occ,f.get_fock()))),referenceInternalStable=bool(si),referenceExternalStable=bool(se),referenceEnergyHartree=float(f.e_tot),referenceLimitation='Unstable reference: diagnostic only, not accepted as a validated correlated benchmark.' if not(si and se) else 'Determinant stability does not establish correlation/basis convergence or exclude multireference effects.')
 energy=float(f.e_tot);arrays={}
 if tag=='ri-mp2-def2tzvp':
  mp=DFRMP2(f,auxbasis=make_auxbasis(m,mp2fit=True));mp.kernel();p=mp.make_rdm1(ao_repr=True);energy=float(mp.e_tot)
  result.update(correlationEnergyHartree=float(mp.e_corr),densityConvention='Unrelaxed MP2 one-particle density; HF canonical orbitals, not correlated natural orbitals.',hfAuxiliaryBasis=f.with_df.auxbasis,correlationAuxiliaryBasis=mp.auxmol.basis,frozenElectrons=0)
 elif case=='ts' or '--gradient' in sys.argv:
  grad=f.nuc_grad_method();grad.grid_response=True;g=grad.kernel();arrays['fullResponseGradient']=g;result.update(maxFullResponseGradientEhPerBohr=float(abs(g).max()),densityConvention='Restricted Kohn–Sham occupation-weighted one-particle density.')
 else:
  result.update(gradientStatus='Not calculated in this fixed-geometry diagnostic; no alternative-level stationary point is claimed.',densityConvention='Restricted Kohn–Sham occupation-weighted one-particle density.')
 result['bonds']=[]
 if len(elements)==16:
  ev,u=np.linalg.eigh(s);root=(u*np.sqrt(ev))@u.T;q=root@p@root;ps=p@s;slices=m.aoslice_by_atom()
  for i,j in [(0,4),(3,5),(0,1),(2,3),(4,5),(1,2)]:
   a,b=slices[i,2:];c,d=slices[j,2:];result['bonds'].append(dict(atoms=[i,j],distanceAngstrom=float(np.linalg.norm(x[i]-x[j])*BOHR),mayer=float(np.sum(ps[a:b,c:d]*ps[c:d,a:b].T)),lowdinWiberg=float(np.sum(q[a:b,c:d]**2))))
  old=np.load(BASE/(case+'-scf.npz'));om=gto.M(atom=list(zip(elements,x)),unit='Bohr',basis='6-31g(d)',verbose=0)
  tracked=np.load(BASE/(case+'-tracked.npz'));cross=gto.intor_cross('int1e_ovlp',om,m);matches=[]
  for role,j in zip(['occupied','virtual'],tracked['indices']):
   projection=tracked['mo_coeff'][:,j]@cross@f.mo_coeff;block=np.where(f.mo_occ>0 if role=='occupied' else f.mo_occ==0)[0];k=int(block[np.argmax(abs(projection[block]))]);matches.append(dict(role=role,r1Index=int(j)+1,comparisonIndex=k+1,absoluteSpatialOverlap=float(abs(projection[k])),phaseToMatchR1=1 if projection[k]>=0 else -1,interpretation='Same-geometry canonical spatial match; overlap is not an interaction energy.'))
  result['orbitalMatches']=matches
  nodes=np.stack(np.meshgrid(np.arange(-10,12,.56),np.arange(-9,11,.56),np.arange(-7,13,.56),indexing='ij'),axis=-1).reshape(-1,3);deltas=[]
  for start in range(0,len(nodes),2000):
   points=nodes[start:start+2000];a=m.eval_gto('GTOval_sph',points);b=om.eval_gto('GTOval_sph',points);deltas.append(np.einsum('pi,ij,pj->p',a,p,a)-np.einsum('pi,ij,pj->p',b,old['density_matrix'],b))
  delta=np.concatenate(deltas);arrays.update(sampleCoordinatesBohr=nodes,sameGeometryDensityDifference=delta);result['densityComparison']=dict(reference='Unchanged r1 B3LYP/6-31G(d), grid3, at identical nuclei and laboratory coordinates; current minus reference.',units='electron bohr^-3',sampling='x[-10,12), y[-9,11), z[-7,13) bohr, spacing0.56bohr; z fastest. Coarse samples, not a quantitative core integral or unique transferred charge.',sampleRms=float(np.sqrt(np.mean(delta**2))))
 save_npz(folder/(name+'-analysis.npz'),coordinatesAngstrom=x*BOHR,mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,density_matrix=p,overlap=s,**arrays)
 result.update(energyHartree=energy,electronCount=float(np.einsum('ij,ji',p,s)))
 write(target,result);print('COMPLETED',name,energy,si,se,flush=True)

if __name__=='__main__':main()
