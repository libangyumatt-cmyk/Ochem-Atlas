"""Append authored, non-computational reaction batches without changing legacy records."""
from pathlib import Path
from copy import deepcopy
import json,re,hashlib,importlib
from content.v040.model import SOURCES,plain,render
ROOT=Path(__file__).resolve().parent

def apply(payload,batches=3):
 original={r['id']:deepcopy(r) for r in payload['reactions']};payload['sources'].update(deepcopy(SOURCES));new=[]
 for n in range(1,batches+1):
  try:records=importlib.import_module(f'content.v040.batch{n}').A
  except ModuleNotFoundError:
   if n==1:raise
   break
  for authored in records:
   r=deepcopy(authored);rid=r['id'];assert rid not in original and rid not in [x['id'] for x in new];steps=[];images=[]
   for i,e in enumerate(r.pop('events')):
    path,svg,height=render(r,e,i);images.append((svg,height));code=e['code'];note=e.get('scope') or ('No unique existing SORG code: surface/metal-redox/SET or grouped microscopic sequence is outside the defined codebook. Alternatives such as1111 association omit the defining redox/spin process; no new code is introduced.' if code is None else 'Assignment follows the unchanged project convention at teaching-event resolution; it is not a computed descriptor or proof of a unique microscopic mechanism.')
    status='unassigned-boundary' if code is None else ('candidate' if code in ['1113','1133','2222'] or e.get('scope') else 'consistent-with-convention')
    steps.append(dict(title=e['title'],code=code,equation=plain(e['left'])+' → '+plain(e['right']),flow=e['flow'],orbital=e['orbital'],geometry=e['geometry'],diagram={'pt':'proton','sn2':'sn2','add':'carbonyl'}.get(e['kind'],'carbonyl'),eventKind='grouped-stage' if e['kind']=='open' else 'elementary-model',assignmentStatus=status,assignmentNote=note,why=['Electronic-state assumption: '+('not uniquely assigned' if code is None else 'paired-electron model' if code[0]=='1' else 'open-shell model'),e['orbital'],e['flow'],e['geometry']],diagramScope='substrate-matched condensed structural teaching model',eventFigure=dict(src=path,scope='Authored condensed structural notation with explicit intermediate charges; local arrows shown where a defined electron model is used. Process-only arrows mark unassigned grouped stages.',arrowCount=len(e['moves']),reactantStructure=plain(e['left']),productStructure=plain(e['right']),electronMoves=e['moves'],reviewLegend=e['flow'],representation='condensed structural formula; not SMILES or computed geometry')))
   combined='';y=0
   for svg,height in images:combined+=f'<g transform="translate(0,{y})">'+re.sub(r'^.*?<svg[^>]*>|</svg>\s*$','',svg,flags=re.S)+'</g>';y+=height
   overview=f'mechanisms/v040/{rid}.svg';(ROOT/'dist'/overview).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {y}"><title>{r["name"]}: complete teaching sequence</title>'+combined+'</svg>')
   r.update(steps=steps,releaseAdded='0.4.0',batch=n,entryType='scoped synthetic transformation',summary=r['equation']+'. '+r['selectivity'],scope=r['scope']+' Ph=phenyl; Me=methyl; Et=ethyl; Pr=propyl; Ar/R/L denote only the explicitly scoped aryl, spectator substituent or ligand. Counterions not involved in arrows may be omitted consistently.',sources=[r.pop('reference')],referenceLocators=[r.pop('referenceTopic')],facts=[['Selectivity and competition',r['selectivity']],['Evidence level','Textbook/qualitative teaching mechanism; not a new numerical calculation.']],level='Intermediate',note='',mechanismComplete=True,mechanismNote='Complete at the explicitly stated teaching resolution. Named grouped or debated stages may comprise several microscopic events; a concerted event is never split into invented stable intermediates.',figure=dict(src=overview,href=overview,alt='Original condensed structural mechanism: '+r['name'],credit='Ochem Atlas · original authored structural SVG',match='exact',coverage='complete',reviewNote='Authored reaction-specific condensed structures and local electron arrows. Surface/redox models use process arrows where unique electron bookkeeping is not established. No claim of a measured or calculated geometry.',reviewed=True,rightsStatus='original',license='Original Ochem Atlas illustration · CC BY-NC-SA 4.0',licenseUrl='https://creativecommons.org/licenses/by-nc-sa/4.0/',display=True),quantumData=dict(status='not-yet-computed',descriptors=[],note='Qualitative mechanism/orbital interpretation only. No calculation performed or numerical field generated for this new entry.',literatureCases=[],literatureInsights=[],performedCalculations=[],evidenceTypes=['textbook-qualitative-model'],proposedProtocol=dict(model='No new calculation in v0.4.0.',workflow='Existing numerical laboratories remain separate; no protocol was executed for this entry.')),audit=dict(date='2026-11-01',scope='Authored textbook mechanism and structured-graphics editorial checks; not experimental or quantum validation.',researchNeeded='External link reachability and microscopic pathway uniqueness are not assumed; see the mechanism and assignment boundaries.'))
   new.append(r)
 payload['reactions']+=new;payload['version']='0.4.0';payload['updated']='2026-11-01'
 for rid,r in original.items():assert next(x for x in payload['reactions'] if x['id']==rid)==r
 invpath=ROOT/'dist/mechanism-inventory.json';inv=json.loads(invpath.read_text());inv['reactions']=[r for r in inv['reactions'] if r['id'] in original]
 for r in new:inv['reactions'].append(dict(id=r['id'],name=r['name'],beforeStatus='new',beforeFigure=None,afterStatus='teaching-model',afterFigure=r['figure']['src'],afterDisplayed=True,events=[dict(index=i+1,code=s['code'],title=s['title'],equation=s['equation'],focusedImage=s['eventFigure']['src'],afterStatus='teaching-model',coverageBasis='Authored condensed structural teaching event; grouped-stage limitations explicit',limitations=s['assignmentNote']) for i,s in enumerate(r['steps'])]))
 inv['version']='0.4.0';invpath.write_text(json.dumps(inv,ensure_ascii=False,indent=2)+'\n')
 return payload

def main():
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--batches',type=int,default=3);args=parser.parse_args()
 baseline=json.loads((ROOT/'audit/V040_BASELINE.json').read_text());payload=apply(baseline,args.batches)
 (ROOT/'dist/data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n');(ROOT/'dist/data.js').write_text('window.SORG = '+json.dumps(payload,ensure_ascii=False)+';\n')
 print(len(payload['reactions']),'entries;',sum(len(r['steps']) for r in payload['reactions']),'events')
if __name__=='__main__':main()
