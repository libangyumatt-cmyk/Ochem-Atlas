"""Package each completed new-SCF wavefunction exactly, in small atomic ZIPs."""
from pathlib import Path
import os,zipfile,hashlib,json
ROOT=Path(__file__).resolve().parents[3]
folder=Path(os.environ.get('OCHEM_R3_BACKWARD_OUTPUT',str(ROOT/'dist/reaction-lab/diels-alder/r3/backward-attempt1')))/'backward'
files=sorted(folder.glob('wavefunction-*.npz'));assert files
manifest={}
for offset in range(0,len(files),10):
 group=files[offset:offset+10];name='wavefunctions-'+group[0].stem.split('-')[1]+'-'+group[-1].stem.split('-')[1]+'.zip';target=folder/name;temp=folder/(name+'.pending')
 with zipfile.ZipFile(temp,'w',zipfile.ZIP_STORED) as z:
  for p in group:
   with zipfile.ZipFile(p) as inner:assert inner.testzip() is None
   z.write(p,p.name);manifest[p.name]=dict(archive=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 with zipfile.ZipFile(temp) as z:assert z.testzip() is None
 temp.replace(target)
p=folder/'wavefunction-manifest.json';t=p.with_suffix('.pending');t.write_text(json.dumps(manifest,indent=2)+'\n');t.replace(p)
print('Archived',len(files),'actual wavefunctions in',(len(files)+9)//10,'CRC-checked atomic ZIPs; original bytes retained.')
