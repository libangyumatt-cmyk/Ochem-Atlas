"""Strict cached replay from the retained state23, never inventing missing SCFs."""
from pathlib import Path
import sys,pickle,zipfile,json,hashlib
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'r3'),str(Path(__file__).resolve().parents[1]/'r2')]
import optimizer_state,backward,irc
from geometric.optimize import OPT_STATE
from common import *
OLD=BASE/'r3/backward-attempt1/backward';NEW=BASE/'r4/reconstruction'
class ReachedMilestone(Exception):pass
def main():
 NEW.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(OLD/'evaluations.zip') as z:rows={json.loads(z.read(n))['evaluation']:json.loads(z.read(n)) for n in z.namelist() if n.endswith('.json')}
 with zipfile.ZipFile(OLD/'checkpoint-0023.zip') as z:
  assert z.testzip() is None;data=z.read('optimizer-state.pkl');meta=json.loads(z.read('optimizer-state.json'));assert hashlib.sha256(data).hexdigest()==meta['sha256'];opt=pickle.loads(data)
 opt.engine.__class__=irc.FreshEngine;opt.engine.folder=NEW;opt.dirname=str(NEW/'driver.tmp');opt.params.xyzout=str(NEW/'replay.xyz');opt.params.qdata=None;matches=[]
 def replay(self,coords,dirname):
  n=self.count+1;r=rows[n];delta=float(np.max(abs(coords.reshape(-1,3)-r['coordinatesBohr'])))
  if delta>1e-12:raise RuntimeError(f'Exact reconstruction failed at source evaluation {n}: residual {delta} bohr; no fresh SCF attempted.')
  self.count=n;matches.append(dict(evaluation=n,coordinateResidualBohr=delta));return dict(energy=r['energyHartree'],gradient=np.array(r['gradientEhPerBohr']).ravel())
 irc.FreshEngine.calc_new=replay;original=irc.Optimizer.evaluateStep
 def evaluate(self):
  original(self)
  if self.engine.count in [135,138]:
   assert abs(float(self.E)-rows[self.engine.count]['energyHartree'])<1e-12
   p=NEW/f'state-{self.engine.count}.pkl';tmp=p.with_suffix('.pending');tmp.write_bytes(pickle.dumps(self,protocol=5));tmp.replace(p)
   write(NEW/f'state-{self.engine.count}.json',dict(evaluation=self.engine.count,iteration=self.Iteration,energyHartree=float(self.E),trustAngstrom=float(self.trust),minimumTrustAngstrom=float(self.params.tmin),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),origin='Reconstructed by strict source-coordinate cached replay, not a directly retained r3 snapshot.'))
  if self.engine.count>=138:raise ReachedMilestone()
 irc.Optimizer.evaluateStep=evaluate
 try:
  if opt.recalcHess:opt.calcEnergyForce()
  while opt.state not in [OPT_STATE.CONVERGED,OPT_STATE.FAILED]:
   opt.step()
   if opt.state==OPT_STATE.NEEDS_EVALUATION:opt.calcEnergyForce();opt.evaluateStep()
   if opt.recalcHess:opt.calcEnergyForce()
 except ReachedMilestone:write(NEW/'result.json',dict(result='135 and 138 reconstructed',replayed=matches,newSCFCalculations=0))
 except Exception as e:write(NEW/'result.json',dict(result='exact reconstruction unavailable',error=type(e).__name__+': '+str(e),replayed=matches,newSCFCalculations=0));raise
if __name__=='__main__':main()
