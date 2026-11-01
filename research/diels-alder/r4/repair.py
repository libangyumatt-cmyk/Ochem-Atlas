"""Targeted integration trials from the strictly reconstructed accepted state135."""
from pathlib import Path
import sys,pickle,hashlib,json,zipfile,io
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'r3'),str(Path(__file__).resolve().parents[1]/'r2')]
import optimizer_state,irc
from geometric.optimize import OPT_STATE
from common import *
OLD=BASE/'r3/backward-attempt1/backward';NEW=BASE/'r4'
def main():
 size=float(sys.argv[1]);folder=NEW/f'trust-{size}';folder.mkdir(parents=True,exist_ok=True);assert not (folder/'input.json').exists()
 source=NEW/'reconstruction/state-135.pkl';meta=json.loads(source.with_suffix('.json').read_text());data=source.read_bytes();assert hashlib.sha256(data).hexdigest()==meta['sha256'];opt=pickle.loads(data)
 opt.engine.folder=folder;opt.dirname=str(folder/'driver.tmp');opt.params.xyzout=str(folder/'path.xyz');opt.params.qdata=None;opt.params.tmin=size/10;opt.params.tmax=size;opt.trust=size;opt.params.maxiter=200
 manifest=json.loads((OLD/'wavefunction-manifest.json').read_text());n='wavefunction-0135.npz';item=manifest[n]
 with zipfile.ZipFile(OLD/item['archive']) as z:opt.engine.dm=np.load(io.BytesIO(z.read(n)))['density_matrix']
 write(folder/'input.json',dict(sourceSha256=meta['sha256'],sourceEvaluation=135,initialTrustAngstrom=size,maximumTrustAngstrom=size,minimumTrustAngstrom=size/10,scope='Independent single integration-step diagnostic from reconstructed state135; not a complete repaired IRC.'))
 before=opt.X.copy();previous=float(opt.E);opt.step()
 if opt.state==OPT_STATE.NEEDS_EVALUATION:opt.calcEnergyForce();candidate=opt.X.copy();candidateEnergy=float(opt.E);opt.evaluateStep()
 else:raise RuntimeError('Trial did not request evaluation')
 result=dict(sourceEnergyHartree=previous,trialEnergyHartree=candidateEnergy,energyChangeHartree=candidateEnergy-previous,accepted=bool(np.max(abs(opt.X-candidate))<1e-10),queryCoordinatesBohr=candidate.reshape(-1,3).tolist(),formingDistancesAngstrom=[float(np.linalg.norm(candidate.reshape(-1,3)[a]-candidate.reshape(-1,3)[b])*BOHR) for a,b in [(0,4),(3,5)]],descentToleranceHartree=3e-6,descentCheckPassed=candidateEnergy-previous<=3e-6,scientificStatus='single step only; no global IRC connectivity claim')
 save_npz(folder/'optimizer-cartesian-state.npz',X=opt.X,G=opt.G,H=opt.H);temp=folder/'optimizer-state.pending';temp.write_bytes(pickle.dumps(opt,protocol=5));temp.replace(folder/'optimizer-state.pkl');write(folder/'result.json',result);archive(folder,'eval-*.*','evaluations.zip');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
