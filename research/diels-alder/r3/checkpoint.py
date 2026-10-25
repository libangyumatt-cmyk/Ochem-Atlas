"""Atomically snapshot completed endpoint evaluations; exclude in-progress logs."""
from pathlib import Path
import json,zipfile,hashlib,io,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
folder=ROOT/'dist/reaction-lab/diels-alder/r3'/('endpoint-'+sys.argv[1])
rows={p.name:json.loads(p.read_text()) for p in sorted(folder.glob('eval-*.json'))}
assert rows
for r in rows.values():
 assert r['scfConverged'] and abs(r['electronCount']-46)<1e-8
 assert np.isfinite(r['coordinatesBohr']).all() and np.isfinite(r['gradientEhPerBohr']).all()
wave=(folder/'latest-wavefunction.npz').read_bytes();w=np.load(io.BytesIO(wave))
matched=[r['evaluation'] for r in rows.values() if np.max(abs(w['coordinatesBohr']-r['coordinatesBohr']))<1e-10 and abs(float(w['energyHartree'])-r['energyHartree'])<1e-10]
assert matched,'Retry snapshot: newest wavefunction not yet in trial snapshot'
name=f'checkpoint-{max(r["evaluation"] for r in rows.values()):04d}.zip';dest=folder/name;temp=folder/(name+'.pending')
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
 for n in rows:
  z.write(folder/n,n);p=folder/n.replace('.json','.log');z.write(p,p.name)
 for n in ['input.json','options.json','optimizer-status.json','progress.json','verification.json','wavefunction.npz','scf-checkpoint.npz','independent-validation.json','failure.json']:
  p=folder/n
  if p.exists():z.write(p,n)
 state=folder/'optimizer-state.pkl'
 if state.exists():
  data=state.read_bytes();meta=json.loads((folder/'optimizer-state.json').read_text());assert hashlib.sha256(data).hexdigest()==meta['sha256']
  assert meta['evaluations']<=max(r['evaluation'] for r in rows.values())
  z.writestr('optimizer-state.pkl',data);z.writestr('optimizer-state.json',json.dumps(meta,indent=2))
 z.writestr('latest-wavefunction.npz',wave)
with zipfile.ZipFile(temp) as z:assert z.testzip() is None
temp.replace(dest)
r=dict(evaluations=len(rows),wavefunctionMatchesEvaluation=matched,archive=name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='Completed evaluations retained; optimizer completion and minimum verification require separate reports. No serialized optimizer restart is claimed.',latestCompletedTrial=rows[sorted(rows)[-1]])
p=folder/'checkpoint.json';t=p.with_suffix('.pending');t.write_text(json.dumps(r,indent=2)+'\n');t.replace(p)
print(name,len(rows),matched)
