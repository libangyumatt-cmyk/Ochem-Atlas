"""Dependency-free release archive/provenance check, also run in CI."""
from pathlib import Path
import json,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[3];R=ROOT/'dist/reaction-lab/diels-alder/r4'
with zipfile.ZipFile(R/'calculations.zip') as z:
 assert z.testzip() is None
 manifest=json.loads(z.read('MANIFEST.json'))
 for name,sha in manifest.items():
  assert '..' not in Path(name).parts and not Path(name).is_absolute()
  assert hashlib.sha256(z.read(name)).hexdigest()==sha,name
  if name.endswith('.npz'):
   import io
   with zipfile.ZipFile(io.BytesIO(z.read(name))) as inner:assert inner.testzip() is None,name
 independent=json.loads(z.read('independent-ts/result.json'));assert not independent['completePathVerified'] and len(independent['accepted'])==6 and len(independent['trials'])==8
 assert all(p['energyChangeHartree']<0 for p in independent['accepted'])
 for size in ['0.001','0.0005']:assert not json.loads(z.read(f'trust-{size}/result.json'))['accepted']
 diagnostics=json.loads(z.read('diagnostic-validation.json'))
 for check in diagnostics['gridChecks'].values():assert check['uphillEnergyDifferenceEh']>3e-6 and abs(check['gradientDifferenceEhPerBohr'])<1e-6
for name,sha in json.loads((ROOT/'audit/V037_R4_PRESERVED_DATA.json').read_text()).items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
assert not json.loads((ROOT/'audit/V037_R4_VALIDATION.json').read_text())['completeIndependentIrcVerified']
print('PASS: r4 archive CRC/SHA, NPZ CRCs, bounded independent descent, rejected trust trials, numerical-gradient checks and 364 unchanged prior files; no full IRC claim.')
