from pathlib import Path
import json,hashlib,zipfile
root=Path(__file__).resolve().parents[3];folder=root/'dist/reaction-lab/diels-alder/r4';target=folder/'calculations.zip';temp=target.with_suffix('.pending');manifest={}
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(folder.rglob('*')):
  if not p.is_file() or p.suffix in ['.zip','.pending'] or any(s.endswith('.tmp') for s in p.parts):continue
  name=str(p.relative_to(folder));data=p.read_bytes();manifest[name]=hashlib.sha256(data).hexdigest();z.writestr(name,data)
 z.writestr('MANIFEST.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(temp) as z:assert z.testzip() is None
temp.replace(target);print(len(manifest),'files',target.stat().st_size,'bytes')
