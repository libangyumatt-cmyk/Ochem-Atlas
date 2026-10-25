"""Cheap analytic H2 stretch tests serialization and interrupted continuation."""
import tempfile
from pathlib import Path
import numpy as np
from geometric.engine import Engine
from geometric.molecule import Molecule
from geometric.optimize import run_optimizer,Optimizer
from optimizer_state import install,resume
class Stretch(Engine):
 def __init__(self,m):super().__init__(m);self.count=0;self.dm=np.eye(1)
 def calc_new(self,coords,dirname):
  self.count+=1;x=coords.reshape(2,3);v=x[1]-x[0];r=np.linalg.norm(v);delta=r-1.4;g=.2*delta*v/r
  return dict(energy=.1*delta**2,gradient=np.array([-g,g]).ravel())
def main():
 with tempfile.TemporaryDirectory() as d:
  folder=Path(d);m=Molecule();m.elem=['H','H'];m.xyzs=[np.array([[0.,0,0],[0,0,1.3]])];m.comms=['Analytic restart check'];m.build_topology();(folder/'input.xyz').write_text('2\nAnalytic restart check\nH 0 0 0\nH 0 0 1.3\n')
  original=Optimizer.evaluateStep;install(folder);saved=Optimizer.evaluateStep
  def interrupt(self):
   saved(self)
   if self.Iteration==2:raise InterruptedError('intentional test interruption')
  Optimizer.evaluateStep=interrupt
  try:run_optimizer(customengine=Stretch(m),input=str(folder/'input.xyz'),prefix=str(folder/'test'),maxiter=40)
  except InterruptedError:pass
  else:raise AssertionError('Interruption not exercised')
  Optimizer.evaluateStep=original;install(folder)
  final=resume(folder);distance=np.linalg.norm(final.xyzs[-1][1]-final.xyzs[-1][0])/.52917721092
  assert abs(distance-1.4)<1e-4,distance
  print('PASS: optimizer pickle round-trip and interrupted analytic continuation',distance)
if __name__=='__main__':main()
