"""Continue a targeted state135 repair, preserving every accepted/rejected trial.
Abort before any forced uphill step can become a validated path point.
"""
from pathlib import Path
import sys,pickle,json,hashlib
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'r3'),str(Path(__file__).resolve().parents[1]/'r2')]
import optimizer_state,irc
from geometric.optimize import OPT_STATE
from common import *
NEW=BASE/'r4';folder=NEW/'continued-repair'
def main():
 folder.mkdir(parents=True,exist_ok=True);assert not (folder/'input.json').exists();source=NEW/'trust-0.0005/optimizer-state.pkl';opt=pickle.loads(source.read_bytes())
 opt.engine.folder=folder;opt.dirname=str(folder/'driver.tmp');opt.params.xyzout=str(folder/'path.xyz');opt.params.qdata=None;opt.params.maxiter=160
 write(folder/'input.json',dict(sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),minimumTrustAngstrom=opt.params.tmin,maximumTrustAngstrom=opt.params.tmax,scope='Continuation from reconstructed state135 after rejected smaller-step trial; previous r3 forced point preserved separately.',maximumNewEvaluations=30))
 trace=[];lastAcceptedEnergy=float(opt.E);startCount=opt.engine.count
 try:
  while opt.state not in [OPT_STATE.CONVERGED,OPT_STATE.FAILED] and opt.engine.count-startCount<30:
   opt.step()
   if opt.state==OPT_STATE.NEEDS_EVALUATION:
    opt.calcEnergyForce();query=opt.X.copy();energy=float(opt.E);opt.evaluateStep();accepted=bool(np.max(abs(query-opt.X))<1e-10);delta=energy-lastAcceptedEnergy
    row=dict(evaluation=opt.engine.count,energyHartree=energy,accepted=accepted,energyChangeFromLastAcceptedHartree=delta,trustAngstrom=float(opt.trust),endpointOptimization=bool(opt.IRC_info['opt']),coordinatesBohr=query.reshape(-1,3).tolist());trace.append(row)
    write(folder/'trace.json',trace);temp=folder/'optimizer-state.pending';temp.write_bytes(pickle.dumps(opt,protocol=5));temp.replace(folder/'optimizer-state.pkl')
    if accepted:
     if delta>3e-6:raise RuntimeError('Accepted uphill step exceeded fixed 3e-6 Eh threshold; path remains invalid.')
     lastAcceptedEnergy=energy
   if opt.recalcHess:opt.calcEnergyForce()
  write(folder/'result.json',dict(driverConverged=opt.state==OPT_STATE.CONVERGED,trialCount=len(trace),acceptedTrials=sum(r['accepted'] for r in trace),allAcceptedStepsPassedDescent=all(r['energyChangeFromLastAcceptedHartree']<=3e-6 for r in trace if r['accepted']),fullIndependentIrcVerified=False,termination='driver state or 30-evaluation diagnostic budget'))
 except BaseException as e:write(folder/'failure.json',dict(error=type(e).__name__+': '+str(e),trialCount=len(trace)));raise
 finally:archive(folder,'eval-*.*','evaluations.zip')
if __name__=='__main__':main()
