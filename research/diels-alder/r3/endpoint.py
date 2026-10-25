"""Separate +/- soft-mode endpoint relaxations; never IRC points. Atomic milestones."""
from pathlib import Path
import sys,os
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r2'))
from common import *
from endpoints import verify
from irc import FreshEngine
from geometric.molecule import Molecule
from geometric.optimize import run_optimizer
OLD=BASE/'r2/restart-20261022'
NEW=Path(os.environ.get('OCHEM_R3_OUTPUT',str(BASE/'r3')))
def main():
 sign=sys.argv[1];assert sign in ['plus','minus']
 retry='--from-checkpoint' in sys.argv
 folder=NEW/('endpoint-'+sign+('-retry1' if retry else ''));folder.mkdir(parents=True,exist_ok=True)
 assert not (folder/'input.json').exists(),'Retain attempt; do not overwrite.'
 source=OLD/'endpoints/forward/wavefunction.npz';w=np.load(source)
 mode=np.real_if_close(w['normal_modes'][np.argmin(w['frequenciesCm'])]);assert np.isrealobj(mode)
 mode/=np.linalg.norm(mode);step=.15 if sign=='plus' else -.15
 x=w['coordinatesAngstrom']+step*mode
 seed=w['density_matrix'];restartSource=None
 if retry:
  previous=NEW/('endpoint-'+sign)/'latest-wavefunction.npz';restartSource=str(previous.resolve());old=np.load(previous);x=old['coordinatesBohr']*BOHR;seed=old['density_matrix']
 write(folder/'input.json',dict(sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),coordinatesAngstrom=x.tolist(),cartesianUnitMode=mode.tolist(),displacementNormAngstrom=step,restartGeometrySource=restartSource,restartConvention='New ordinary optimization from saved geometry, not faithful optimizer continuation' if retry else None,interpretation='Unconstrained endpoint optimization from retained negative mode; not an IRC extension.',software=dict(pyscf=__import__('pyscf').__version__,geometric=__import__('geometric').__version__,numpy=np.__version__)))
 molecule=Molecule();molecule.elem=[a['element'] for a in record()['atoms']];molecule.xyzs=[x];molecule.comms=['r3 displaced endpoint'];molecule.build_topology()
 from optimizer_state import install
 install(folder)
 engine=FreshEngine(molecule,folder);engine.dm=seed
 options=dict(coordsys='dlc',trust=.05,tmax=.1,maxiter=100,convergence_energy=1e-9,convergence_grms=3e-6,convergence_gmax=1e-5,convergence_drms=.0001,convergence_dmax=.0003)
 write(folder/'options.json',options)
 try:
  final=run_optimizer(customengine=engine,input=str(BASE/'ts.xyz'),prefix=str(folder/'optimization'),**options)
  write(folder/'optimizer-status.json',dict(converged=True,finalCoordinatesAngstrom=final.xyzs[-1].tolist(),evaluations=engine.count))
  r=verify(folder,np.array(final.xyzs[-1]));print('VERIFICATION',r['minimumVerified'],min(r['frequenciesCm']),flush=True)
 except BaseException as exc:
  write(folder/'failure.json',dict(error=type(exc).__name__+': '+str(exc),evaluations=engine.count));raise
 finally:archive(folder,'eval-*.*','evaluations.zip')
if __name__=='__main__':main()
