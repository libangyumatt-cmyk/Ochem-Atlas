"""Recompute r4 invariants, segment descent, mode direction and prior-data hashes."""
from pathlib import Path
import hashlib,json,zipfile,numpy as np
ROOT=Path(__file__).resolve().parents[3];BASE=ROOT/'dist/reaction-lab/diels-alder';R=BASE/'r4'
def main():
 prior=json.loads((ROOT/'audit/V037_R4_PRESERVED_DATA.json').read_text())
 for p,h in prior.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 matrices=0
 for p in R.rglob('*'):
  if p.suffix in ['.npz','.zip']:
   with zipfile.ZipFile(p) as z:assert z.testzip() is None,p
  if p.suffix!='.npz':continue
  with np.load(p) as w:
   for k in w.files:assert np.isfinite(w[k]).all(),(p,k)
   if all(k in w for k in ['mo_coeff','overlap','density_matrix']):
    c=w['mo_coeff'];s=w['overlap'];dm=w['density_matrix'];assert np.max(abs(c.T@s@c-np.eye(c.shape[1])))<1e-8 and abs(np.einsum('ij,ji',dm,s)-46)<1e-8;matrices+=1
 independent=json.loads((R/'independent-ts/result.json').read_text());definition=json.loads((R/'independent-ts/input.json').read_text());mass=np.array(definition['massesAmu']);root=np.sqrt(mass)[:,None]
 with zipfile.ZipFile(BASE/'r3/backward-attempt1/backward/evaluations.zip') as z:ts=json.loads(z.read('eval-0001.json'))
 h=np.load(BASE/'ts-hessian.npz')['hessian'].transpose(0,2,1,3).reshape(48,48);weights=np.repeat(np.sqrt(mass),3);_,v=np.linalg.eigh((h+h.T)/2/weights[:,None]/weights[None,:]);first=independent['trials'][0];dq=((np.array(first['coordinatesBohr'])-ts['coordinatesBohr'])*root).ravel();overlap=abs(float(np.dot(dq/np.linalg.norm(dq),v[:,0])));assert overlap>1-1e-8
 previous=ts['energyHartree']
 for row in independent['trials']:
  w=np.load(R/f'independent-ts/eval-{row["evaluation"]:03d}.npz');assert np.max(abs(w['coordinatesBohr']-row['coordinatesBohr']))<1e-12 and abs(float(w['energyHartree'])-row['energyHartree'])<1e-12
  if row['accepted']:assert row['energyHartree']<previous;previous=row['energyHartree']
 forward=json.loads((R/'forward-curvature/result.json').read_text());energies={t:json.loads((R/f'forward-curvature/step{t}.json').read_text())['energyHartree'] for t in [0.,-.01,.01]};curvature=(energies[-.01]+energies[.01]-2*energies[0.])/(.01/.52917721092)**2;assert abs(curvature-forward['energyCurvatureEhPerBohr2'])<1e-10
 summary=dict(priorFilesUnchanged=len(prior),wavefunctionsChecked=matrices,independentAcceptedSteps=len(independent['accepted']),independentFreshEvaluations=len(independent['trials']),imaginaryModeMassWeightedOverlap=overlap,initialStepMassWeightedBohrSqrtAmu=float(np.linalg.norm(dq)),forwardTransportedCurvatureEhPerBohr2=curvature,scientificClassification='2: connectivity supported but numerical integration remains unresolved',completeIndependentIrcVerified=False,limitations=['Independent integration covers only six accepted initial steps, not endpoints.','Smaller geomeTRIC continuation terminates after one accepted step; endpoint verification is not complete.','Directional ring curvature is not a full Hessian spectrum or VRI demonstration.'])
 p=ROOT/'audit/V037_R4_VALIDATION.json';t=p.with_suffix('.pending');t.write_text(json.dumps(summary,indent=2)+'\n');t.replace(p);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
