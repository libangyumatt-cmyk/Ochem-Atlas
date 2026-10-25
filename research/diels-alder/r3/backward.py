"""Fresh TS driver with strict geometry-keyed reuse of actual r2 SCF/gradients.
Not continuation from a fabricated r2 optimizer state. A cache miss runs a new
B3LYP calculation. Reused results retain their original geometry and provenance.
"""
from pathlib import Path
import sys,os,json,zipfile,hashlib
os.environ['OCHEM_R2_OUTPUT']=str(Path(__file__).resolve().parents[3]/'dist/reaction-lab/diels-alder/r3/backward-attempt1')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r2'))
import common,irc
from common import np,write,save_npz,archive,BASE,OUT
from optimizer_state import install
OLD=BASE/'r2/restart-20261022/backward'
OriginalEngine=irc.FreshEngine
class ReplayEngine(OriginalEngine):
 def __init__(self,molecule,folder):
  super().__init__(molecule,folder);self.reused=0;self.fresh=0
  state=json.loads((OLD/'status.json').read_text())
  for name,sha in state['initialSources'].items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==sha
  with zipfile.ZipFile(OLD/'evaluations.zip') as z:
   assert z.testzip() is None
   self.cache=[json.loads(z.read(n)) for n in sorted(z.namelist()) if n.endswith('.json')]
  for r in self.cache:
   assert r['scfConverged'] and abs(r['electronCount']-46)<1e-8 and r['orbitalGradientNorm']<3e-6
   assert np.isfinite(r['coordinatesBohr']).all() and np.isfinite(r['gradientEhPerBohr']).all()
  write(folder/'reuse-definition.json',dict(source=str(OLD.relative_to(common.ROOT)),sourceArchiveSha256=hashlib.sha256((OLD/'evaluations.zip').read_bytes()).hexdigest(),maximumCoordinateDifferenceBohr=1e-12,convention='Fresh TS-started driver; reuse only geometry-identical retained evaluations to numerical precision. No interpolation. Original source geometry and actual query residual retained. Cache miss invokes new full-response grid3 SCF/gradient. Cached points have no new wavefunction claim. Density guess starts from retained TS; reused trials do not update it. Full optimizer states are saved after evaluated steps.'))
 def calc_new(self,coords,dirname):
  x=coords.reshape(-1,3);dist=[float(np.max(abs(x-np.array(r['coordinatesBohr'])))) for r in self.cache];idx=int(np.argmin(dist))
  if dist[idx]<=1e-12:
   source=self.cache[idx];self.count+=1;self.reused+=1;r=dict(source);r.update(evaluation=self.count,resultOrigin='reused-r2-evaluation',sourceEvaluation=source['evaluation'],queryMaximumCoordinateDifferenceBohr=dist[idx])
   write(self.folder/f'eval-{self.count:04d}.json',r)
   if self.count%5==0:archive(self.folder,'eval-*.*','evaluations.zip')
   result=dict(energy=r['energyHartree'],gradient=np.array(r['gradientEhPerBohr']).ravel())
  else:
   result=super().calc_new(coords,dirname);self.fresh+=1
   path=self.folder/f'eval-{self.count:04d}.json';r=json.loads(path.read_text());r['resultOrigin']='new-r3-SCF-gradient';write(path,r)
   # Keep a complete wavefunction for every new expensive evaluation.
   wave=(self.folder/'latest-wavefunction.npz').read_bytes();target=self.folder/f'wavefunction-{self.count:04d}.npz';temp=target.with_suffix('.pending');temp.write_bytes(wave);temp.replace(target)
  write(self.folder/'reuse-progress.json',dict(evaluations=self.count,reusedR2=self.reused,newSCFGradients=self.fresh,scientificStatus='Pending independent descent, convergence and endpoint checks; counts do not claim completed IRC.'))
  return result

def main():
 folder=OUT/'backward';folder.mkdir(parents=True,exist_ok=True)
 assert not (folder/'status.json').exists(),'Existing attempt retained.'
 install(folder);irc.FreshEngine=ReplayEngine;sys.argv=[sys.argv[0],'backward'];irc.main()
ReplayEngine.__module__='backward'
if __name__=='__main__':
 sys.modules['backward']=sys.modules[__name__]
 main()
