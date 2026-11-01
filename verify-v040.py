"""Structural integrity and preservation; not experimental mechanism validation."""
from pathlib import Path
import json,hashlib,re,xml.etree.ElementTree as ET,unicodedata
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parent;D=json.loads((ROOT/'dist/data.json').read_text());old=json.loads((ROOT/'audit/V040_BASELINE.json').read_text());new=[r for r in D['reactions'] if r.get('releaseAdded')]
assert len({r['id'] for r in D['reactions']})==len(D['reactions'])
inventory=json.loads((ROOT/'content/v040/inventory.json').read_text())
assert {r['id'] for r in new}=={rid for batch in inventory['batches'] for rid in batch}
assert len(D['reactions'])==100 and sum(len(r['steps']) for r in D['reactions'])==338
for r in old['reactions']:assert next(x for x in D['reactions'] if x['id']==r['id'])==r,r['id']
assert old['axes']==D['axes'] and old['codebook']==D['codebook']
for p,h in json.loads((ROOT/'audit/V040_QUANTUM_HASHES.json').read_text()).items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
names={}
def normalize(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).lower())
for r in D['reactions']:
 for name in [r['name'],*r.get('aliases',[])]:
  k=normalize(name)
  assert k not in names or names[k]==r['id'],(name,names.get(k),r['id']);names[k]=r['id']
for r in new:
 for field in ['name','family','equation','conditions','scope','referenceLocators','selectivity','steps','sources','figure']:assert r[field],(r['id'],field)
 assert r['quantumData']['performedCalculations']==[] and r['quantumData']['literatureCases']==[]
 for source in r['sources']:assert source in D['sources'] and D['sources'][source]['url'].startswith('https://')
 for s in r['steps']:
  for field in ['equation','flow','orbital','geometry','assignmentNote','eventKind','eventFigure']:assert s[field]
  if s['code'] is None:assert s['assignmentStatus']=='unassigned-boundary' and len(s['assignmentNote'])>40
  else:assert s['code'] in D['codebook'] and all(v in axis['values'] for v,axis in zip(s['code'],D['axes']))
  p=ROOT/'dist'/s['eventFigure']['src'];assert p.is_file();tree=ET.parse(p);svg=p.read_text();assert '<title>' in svg and '<desc>' in svg
  assert ('Process model:' in svg or 'Condensed structural stage;' in svg) if s['eventFigure']['arrowCount']==0 else 'data-electrons=' in svg
  assert len(re.findall(r'data-electrons=',svg))==s['eventFigure']['arrowCount']
  for endpoint in s['eventFigure']['electronMoves']:
   assert len(endpoint) in [2,3] and (len(endpoint)==2 or endpoint[2] in [1,2])
 ET.parse(ROOT/'dist'/r['figure']['src'])
 assert len(r['representativeSmiles'])==2
 from content.v040.graphs import parse
 for smiles in r['representativeSmiles']:parse(smiles)
 assert not re.search('[\u3400-\u9fff]',json.dumps(r,ensure_ascii=False))
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key not in ['href','src'] or not value:continue
   u=urlsplit(value)
   if u.scheme or u.netloc or not u.path:continue
   if u.path=='sorg-atlas-source.zip':continue # Generated after tests by package_source.py in CI.
   assert (ROOT/'dist'/unquote(u.path)).is_file(),value
Links().feed((ROOT/'dist/index.html').read_text())
print(f'PASS: {len(new)} new entries / {sum(len(r["steps"]) for r in new)} events; unique names/aliases, required fields, unchanged codebook/31 original records, quantum hashes, citations mapped, structural SVG XML/arrows. External HTTP and scientific correctness require separate review.')
