"""No new SCF: verify strict reuse and serialized replay-engine invariants."""
from pathlib import Path
import tempfile,pickle,json
import numpy as np
from backward import ReplayEngine
from common import record
from geometric.molecule import Molecule

def main():
 with tempfile.TemporaryDirectory() as directory:
  folder=Path(directory);m=Molecule();m.elem=[a['element'] for a in record()['atoms']];m.xyzs=[np.array([a['xyzAngstrom'] for a in record()['atoms']])];m.comms=['Cache invariant test'];m.build_topology()
  engine=ReplayEngine(m,folder);seed=engine.dm.copy()
  for source in [engine.cache[0],engine.cache[-1]]:
   x=np.array(source['coordinatesBohr']);answer=engine.calc_new(x.ravel(),str(folder))
   assert answer['energy']==source['energyHartree']
   assert np.array_equal(answer['gradient'],np.array(source['gradientEhPerBohr']).ravel())
   row=json.loads((folder/f'eval-{engine.count:04d}.json').read_text());assert row['resultOrigin']=='reused-r2-evaluation' and row['queryMaximumCoordinateDifferenceBohr']==0
  assert engine.reused==2 and engine.fresh==0 and np.array_equal(seed,engine.dm)
  assert not (folder/'latest-wavefunction.npz').exists()
  clone=pickle.loads(pickle.dumps(engine,protocol=5));assert clone.count==2 and len(clone.cache)==112 and np.array_equal(clone.dm,seed)
  print('PASS: two exact geometry-keyed retained SCF/gradient reuses, no new SCF or wavefunction claim, preserved TS guess, importable replay-engine round trip.')
if __name__=='__main__':main()
