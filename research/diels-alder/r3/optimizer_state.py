"""Version-specific trusted-local geomeTRIC state snapshots after evaluated steps.
Pickles are executable inputs: never load an untrusted checkpoint. Each saved
state is immediately round-tripped and its nuclear/electronic state compared.
"""
import pickle,hashlib,json,os
from pathlib import Path
import numpy as np
from geometric.optimize import Optimizer

def install(folder):
 original=Optimizer.evaluateStep
 def evaluate(self):
  original(self)
  target=Path(folder)/'optimizer-state.pkl';temp=target.with_suffix('.pending')
  data=pickle.dumps(self,protocol=5);clone=pickle.loads(data)
  for k in ['X','G','H']:assert np.array_equal(getattr(self,k),getattr(clone,k)),k
  assert self.Iteration==clone.Iteration and self.state==clone.state
  assert self.engine.count==clone.engine.count
  assert np.array_equal(self.engine.dm,clone.engine.dm)
  with temp.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  temp.replace(target)
  meta=dict(phase='after evaluateStep; recalcHess pending if set',iteration=self.Iteration,state=int(self.state),evaluations=self.engine.count,sha256=hashlib.sha256(data).hexdigest(),recalcHess=bool(self.recalcHess),format='Python pickle5, trusted local input only; geomeTRIC1.1.1/PySCF2.14.0',roundTripValidation='X,G,H,state,iteration,engine count and density matrix exact')
  t=Path(folder)/'optimizer-state.json.pending';t.write_text(json.dumps(meta,indent=2)+'\n');t.replace(Path(folder)/'optimizer-state.json')
 Optimizer.evaluateStep=evaluate

def resume(folder):
 folder=Path(folder);data=(folder/'optimizer-state.pkl').read_bytes();meta=json.loads((folder/'optimizer-state.json').read_text());assert hashlib.sha256(data).hexdigest()==meta['sha256']
 opt=pickle.loads(data)
 # Finish the original loop tail before its next iteration. Never reinitialize
 # the IRC, internal coordinates, BFGS matrix, trust radius or engine cache.
 if opt.recalcHess:opt.calcEnergyForce()
 calc=opt.calcEnergyForce;prepare=opt.prepareFirstStep
 opt.calcEnergyForce=lambda:None;opt.prepareFirstStep=lambda:None
 # Avoid lambda persistence: restore both methods before entering the loop.
 def skip_initial():
  opt.calcEnergyForce=calc
 def skip_prepare():
  opt.prepareFirstStep=prepare
 opt.calcEnergyForce=skip_initial;opt.prepareFirstStep=skip_prepare
 return opt.optimizeGeometry()
