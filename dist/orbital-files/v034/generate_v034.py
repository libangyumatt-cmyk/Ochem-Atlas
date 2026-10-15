"""Reproduce v0.3.4 independently; never overwrites v0.3.3 datasets.
Fixed model geometries, RHF/STO-3G or spin-adapted open-shell ROHF/STO-3G.
Run OMP_NUM_THREADS=1 python research/orbitals/generate_v034.py.
"""
import gzip, json, shutil, platform
from pathlib import Path
import numpy as np
import pyscf, skimage
from pyscf import gto, scf, lib, symm
from pyscf.tools import cubegen
from skimage.measure import marching_cubes
from scipy.optimize import linear_sum_assignment
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'dist/orbital-files/v034'; OUT.mkdir(exist_ok=True)
N=44; ISO=.035; BOHR=.529177210903
lib.num_threads(1)
try: lib.current_memory()
except FileNotFoundError: lib.current_memory=lambda:(0,0)
def mesh(field,cc,level):
 result={}
 for name,sign in [('positive',1),('negative',-1)]:
  if (field*sign).max()<=level: result[name]=None; continue
  v,f,_,_=marching_cubes((field*sign).astype('float32'),level,allow_degenerate=False)
  xyz=(v*(np.diag(cc.box)/(N-1))+cc.boxorig)*BOHR
  result[name]={'vertices':np.round(xyz,3).ravel().tolist(),'faces':f.ravel().tolist(),'triangleCount':len(f)}
 return result

def calc(key,name,atoms,spin=0,previous=None,angle=None):
 basis='sto-3g'
 mol=gto.M(atom=atoms,basis=basis,unit='Angstrom',charge=0,spin=spin,symmetry=True,verbose=4,output=str(OUT/f'{key}.log'))
 mf=scf.ROHF(mol) if spin else scf.RHF(mol)
 mf.conv_tol=1e-11; mf.conv_tol_grad=1e-7; mf.max_cycle=200
 energy=mf.kernel(); assert mf.converged,key
 S=mol.intor('int1e_ovlp'); C=np.array(mf.mo_coeff); occ=np.array(mf.mo_occ)
 err=max(np.max(abs(c.T@S@c-np.eye(mol.nao))) for c in [C])
 dm=mf.make_rdm1(); counts=[float(np.einsum('ij,ji',d,S)) for d in (dm if spin else [dm])]
 assert err<1e-8 and abs(sum(counts)-mol.nelectron)<1e-8
 s2,mult=mf.spin_square() if spin else (0.,1.)
 assert not spin or abs(s2-.75)<1e-8,(key,s2)
 coeff=C
 syms=symm.label_orb_symm(mol,mol.irrep_name,mol.symm_orb,coeff)
 pz=[i for i,s in enumerate(mol.ao_labels()) if '2pz' in s]
 weights=np.einsum('ui,uv,vi->i',coeff[pz],S[np.ix_(pz,pz)],coeff[pz])
 pi=list(np.where(weights>.95)[0])
 tracking=[]
 if previous:
  pm,pc,tracked=previous
  cross=gto.intor_cross('int1e_ovlp',pm,mol)
  overlap=pc.T@cross@coeff
  assignment={}
  for indices in [np.where(occ>0)[0],np.where(occ==0)[0]]:
   r,c=linear_sum_assignment(-abs(overlap[np.ix_(indices,indices)]))
   assignment.update({int(indices[i]):int(indices[j]) for i,j in zip(r,c)})
  pi=[assignment[i] for i in tracked]
  for old,new in zip(tracked,pi):
   raw=float(overlap[old,new]); coeff[:,new]*=1 if raw>=0 else -1
   row=abs(overlap[old]); other=np.delete(row,new)
   tracking.append({'previousIndex':int(old+1),'currentIndex':int(new+1),'signedOverlapBeforeAlignment':raw,'alignedOverlap':abs(raw),'nextBestOverlap':float(max(other))})
   assert abs(raw)>.70 and abs(raw)>max(other), (key,tracking)
 else:
  for j in range(coeff.shape[1]):
   k=np.argmax(abs(coeff[:,j])); coeff[:,j]*=1 if coeff[k,j]>=0 else -1
 if spin:
  pi=[int(np.where(occ==1)[0][0])]
 method='ROHF' if spin else 'RHF'
 item={'id':key,'name':name,'charge':0,'multiplicity':spin+1,'electronCount':mol.nelectron,'method':method,'basis':basis.upper(),'program':f'PySCF {pyscf.__version__}',
  'totalEnergyHartree':float(energy),'orthonormalError':float(err),'electronCounts':counts,'s2':float(s2),'spinContamination':float(s2-.75) if spin else 0,'scfConverged':bool(mf.converged),
  'geometryKind':'constrained rigid torsion scan; no relaxation, optimization or IRC' if angle is not None else 'fixed manually specified model geometry; not optimized or measured',
  'pointGroup':mol.topgroup,'atoms':[{'element':s,'xyzAngstrom':list(map(float,v)),'label':f'{s}{i+1}'} for i,(s,v) in enumerate(atoms)],'orbitals':[],'tracking':tracking}
 if angle is not None:
  item['torsionDegrees']=angle
  # Actual normalized overlap of left pz and the rotated right perpendicular 2p AO.
  labels=mol.ao_labels(); iz=labels.index('0 C 2pz   '); rz=labels.index('1 C 2pz   '); ry=labels.index('1 C 2py   ')
  a=np.zeros(mol.nao);b=a.copy();a[iz]=1;b[rz]=np.cos(np.radians(angle));b[ry]=-np.sin(np.radians(angle))
  item['localPAOOverlap']=float(a@S@b/np.sqrt((a@S@a)*(b@S@b)))
 (OUT/f'{key}.xyz').write_text(f'{len(atoms)}\n{item["geometryKind"]}; {method}/{basis.upper()} charge 0 multiplicity {spin+1}\n'+''.join(f'{s} {v[0]:.10f} {v[1]:.10f} {v[2]:.10f}\n' for s,v in atoms))
 np.savez_compressed(OUT/f'{key}-scf.npz',mo_coeff=C,mo_energy=mf.mo_energy,mo_occ=occ,overlap=S,atom_coords_angstrom=mol.atom_coords()*BOHR)
 cc=cubegen.Cube(mol,N,N,N,margin=3); ao=mol.eval_gto('GTOval_sph',cc.get_coords())
 def field_entry(index,title,description,field,level=ISO,kind='orbital'):
  token='spin' if kind=='spin-density' else f'mo{index+1}'
  path=OUT/f'{key}-{token}.cube';cc.write(field,str(path),f'{method}/{basis.upper()} {title}; {kind}')
  Path(str(path)+'.gz').write_bytes(gzip.compress(path.read_bytes(),compresslevel=9,mtime=0))
  assert gzip.decompress(Path(str(path)+'.gz').read_bytes()) == path.read_bytes()
  path.unlink()
  o={'index':int(index+1),'name':title,'character':kind,'description':description,'kind':kind,'fileStem':f'v034/{key}-{token}',
   'isovalue':level,'isovalueUnit':'e bohr⁻³' if kind=='spin-density' else 'bohr⁻³ᐟ²','mesh':mesh(field,cc,level),'gridMin':float(field.min()),'gridMax':float(field.max())}
  if kind=='orbital':o.update(occupation=int(occ[index]),energyHartree=float(mf.mo_energy[index]),symmetry=str(syms[index]),spinChannel='singly occupied alpha' if spin else 'restricted')
  item['orbitals'].append(o)
 for j,i in enumerate(pi):
  if spin:
   title='SOMO (open-shell ROHF)';desc='A spin-adapted open-shell doublet with a singly occupied molecular orbital. The central carbon is near a SOMO node. ROHF constrains doubly occupied alpha/beta spatial orbitals to coincide; it omits UHF spin polarization.'
  else:
   title=f'π{j+1}' if angle is None else ['Tracked π-derived occupied','Tracked π*-derived virtual'][j]
   desc=f'Canonical {method} π orbital, MO {i+1}, {syms[i]} symmetry in the computational subgroup. '
   if key=='benzene':desc+='The six-carbon π system is delocalized. Degenerate pairs allow arbitrary orthogonal combinations; an individual partner is not a unique observable. Orbitals alone do not measure aromatic stabilization or establish a reaction pathway.'
   elif key=='butadiene':desc+=f'The four π orbitals have progressively increasing nodal structure (π{j+1}: {j} longitudinal nodes in the ideal conjugated-chain interpretation, plus the molecular plane). This s-trans geometry must reorganize to s-cis for Diels–Alder; no transition state is computed.'
   else:desc+='An independently solved Fock problem at this geometry; identity follows maximum cross-geometry AO-metric overlap, with sign alignment, rather than MO index. Only the constrained RHF branch is shown.'
  field=(ao@coeff[:,i]).reshape(cc.get_ngrids() and (N,N,N))
  field_entry(i,title,desc,field)
 if spin:
  field=np.einsum('pi,ij,pj->p',ao,dm[0]-dm[1],ao).reshape(N,N,N)
  field_entry(-1,'Spin density ρα − ρβ','Signed ROHF spin density from alpha minus beta occupied densities. It equals the SOMO density in this one-unpaired-electron model; beta-excess polarization is absent by construction. Teal is alpha excess; amber would be beta excess. This is a density, not orbital phase; it cannot be phase reversed.',field,.003,'spin-density')
 mol.stdout.close()
 print(key,'E',energy,'pi',pi,'S2',s2,'orth',err,flush=True)
 return item,(mol,coeff.copy(),pi)

def main():
 systems=[]
 allyl=[('C',(-1.212,.0,0)),('C',(0,.7,0)),('C',(1.212,0,0)),('H',(-2.15,.54,0)),('H',(-1.212,-1.08,0)),('H',(0,1.78,0)),('H',(2.15,.54,0)),('H',(1.212,-1.08,0))]
 systems.append(calc('allyl','Allyl radical · C₃H₅',allyl,spin=1)[0])
 benz=[]
 for element,r in [('C',1.397),('H',2.477)]:
  benz += [(element,(r*np.cos(t),r*np.sin(t),0)) for t in np.arange(6)*np.pi/3]
 systems.append(calc('benzene','Benzene · C₆H₆',benz)[0])
 but=[('C',(-1.855,.58,0)),('C',(-.735,-.15,0)),('C',(.735,.15,0)),('C',(1.855,-.58,0)),('H',(-2.82,.095,0)),('H',(-1.80,1.66,0)),('H',(-.81,-1.23,0)),('H',(.81,1.23,0)),('H',(2.82,-.095,0)),('H',(1.80,-1.66,0))]
 systems.append(calc('butadiene','1,3-Butadiene · C₄H₆ (s-trans)',but)[0])
 scan=[];prev=None
 for angle in [0,15,30,45,60]:
  theta=np.radians(angle)
  atoms=[('C',(-.667,0,0)),('C',(.667,0,0)),('H',(-1.232,-.923,0)),('H',(-1.232,.923,0)),('H',(1.232,-.923*np.cos(theta),-.923*np.sin(theta))),('H',(1.232,.923*np.cos(theta),.923*np.sin(theta)))]
  item,prev=calc(f'torsion-{angle:02d}',f'Ethylene · {angle}° torsion',atoms,previous=prev,angle=angle)
  scan.append(item)
 data={'schemaVersion':'1.0','provenance':{'program':f'PySCF {pyscf.__version__}','python':platform.python_version(),'numpy':np.__version__,'skimage':skimage.__version__,'grid':N,'orbitalIsovalue':ISO,'spinDensityIsovalue':.003,'phaseConvention':'First geometry: largest AO coefficient positive. Scan: maximum one-to-one cross-AO overlap within occupied/virtual blocks, positive matched overlap. No interpolation.'},'systems':systems,'scan':scan}
 (ROOT/'dist/orbital-diversity.json').write_text(json.dumps(data,separators=(',',':'),ensure_ascii=False))
 summary={**data,'systems':[{**s,'orbitals':[{k:v for k,v in o.items() if k!='mesh'} for o in s['orbitals']]} for s in systems], 'scan':[{**s,'orbitals':[{k:v for k,v in o.items() if k!='mesh'} for o in s['orbitals']]} for s in scan]}
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
 shutil.copy2(__file__,OUT/'generate_v034.py')
if __name__=='__main__':main()
