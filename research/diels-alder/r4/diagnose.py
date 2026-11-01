"""Fresh, tightly converged energy/gradient probes; no r3 files modified."""
from pathlib import Path
import sys,os,json,zipfile,io,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r2'))
from common import *
OLD=BASE/'r3/backward-attempt1/backward';NEW=BASE/'r4';FOLDER=NEW/'backward-diagnostic'
def source(i):
 with zipfile.ZipFile(OLD/'evaluations.zip') as z:assert z.testzip() is None;return json.loads(z.read(f'eval-{i:04d}.json'))
def main():
 FOLDER.mkdir(parents=True,exist_ok=True);a,b=source(135),source(138);x0=np.array(a['coordinatesBohr']);x1=np.array(b['coordinatesBohr']);v=x1-x0;v/=np.linalg.norm(v)
 spec=dict(model='B3LYP(VWN-RPA)/6-31G(d), neutral singlet C6H10, 46 electrons',sourceArchiveSha256=hashlib.sha256((OLD/'evaluations.zip').read_bytes()).hexdigest(),directionCartesianUnit=v.tolist(),finiteDifferenceStepBohr=.001,scfEnergyToleranceEh=1e-12,scfGradientTolerance=1e-7,gradientConvention='full moving-grid response',points='135 and 138 independent recalculations; +/- probes at 138 are diagnostics, not IRC points')
 write(FOLDER/'definition.json',spec);manifest=json.loads((OLD/'wavefunction-manifest.json').read_text())
 for grid in [3,5]:
  for name,i,t in [('135',135,0),('138',138,0),('138-minus',138,-.001),('138-plus',138,.001)]:
   ident=f'grid{grid}-{name}';target=FOLDER/(ident+'.json')
   if target.exists():continue
   r=source(i);x=np.array(r['coordinatesBohr'])+t*v;n=f'wavefunction-{i:04d}.npz';entry=manifest[n]
   with zipfile.ZipFile(OLD/entry['archive']) as z:data=z.read(n)
   assert hashlib.sha256(data).hexdigest()==entry['sha256'];seed=np.load(io.BytesIO(data))['density_matrix']
   write(FOLDER/'progress.json',dict(current=ident,status='calculation started; no result claimed'))
   m=gto.M(atom=list(zip(['C']*6+['H']*10,x)),unit='Bohr',basis='6-31g(d)',charge=0,spin=0,max_memory=1200,verbose=4,output=str(FOLDER/(ident+'.log')))
   f=dft.RKS(m);f.xc='b3lyp';f.grids.level=grid;f.conv_tol=1e-12;f.conv_tol_grad=1e-7;f.max_cycle=120;f.kernel(dm0=seed);assert f.converged
   grad=f.nuc_grad_method();grad.grid_response=True;g=grad.kernel();p=f.make_rdm1();s=m.intor('int1e_ovlp')
   save_npz(FOLDER/(ident+'.npz'),coordinatesBohr=x,energyHartree=f.e_tot,gradientEhPerBohr=g,mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,density_matrix=p,overlap=s)
   write(target,dict(id=ident,sourceEvaluation=i,displacementBohr=t,grid=grid,energyHartree=float(f.e_tot),scfConverged=True,electronCount=float(np.einsum('ij,ji',p,s)),orbitalGradientNorm=float(np.linalg.norm(f.get_grad(f.mo_coeff,f.mo_occ,f.get_fock()))),directionalGradientEhPerBohr=float(np.sum(g*v)),maxGradientEhPerBohr=float(abs(g).max())))
   archive(FOLDER,'grid*.*','completed-probes.zip');print('COMPLETE',ident,float(f.e_tot),flush=True)
 write(FOLDER/'progress.json',dict(status='eight probe calculations completed; independent validation required'))
if __name__=='__main__':main()
