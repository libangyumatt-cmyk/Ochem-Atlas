"""Expose actual r2 validation status; never promote incomplete IRC fields."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist/reaction-lab/diels-alder/r2'

def extend(d):
 run=OUT/'restart-20261022';path=run/'path-validation.json'
 if not path.exists():return d
 p=json.loads(path.read_text());c=json.loads((run/'connectivity-validation.json').read_text()) if (run/'connectivity-validation.json').exists() else None
 # New validated electronic-field frames require a separate implementation
 # and independent gate. A passing path report alone cannot expose a series.
 result='path-checks-pass-fields-pending' if c and c['result']=='pass' else 'incomplete'
 d['validationR2']=dict(result=result,pathResult=p['result'],connectivityResult=c['result'] if c else 'pending',validatedIRCSeriesExposed=False,report='reaction-lab/diels-alder/r2/V037_R2_AUDIT.md')
 d['pathKind']='Original constrained study: Not an IRC. Separate r2 bidirectional IRC calculations and endpoint checks are documented; a validated synchronized IRC series is not yet available.'
 complete=all(r['driverComplete'] for r in p['branches'].values())
 label='INCOMPLETE' if complete else 'IN PROGRESS'
 d['warnings'].append('IRC VALIDATION '+label+': '+('; '.join(c['limitations'] if c else p['limitations']) or 'Path checks passed; selected-point electronic fields and independent field validation remain pending.')+' Displayed geometries and electronic fields remain the original r1 constrained study, saddle and minimum.')
 comparisons=[]
 for f in (run/'comparisons').glob('*.json'):
  if f.name.endswith('-progress.json') or f.name=='validation.json':continue
  r=json.loads(f.read_text())
  if 'energyHartree' in r:comparisons.append((f.stem,r))
 d['limitations'][0]=f'r2 retains {len(comparisons)}/12 targeted fixed-r1-geometry grid/basis/RI-MP2 comparisons. These do not establish alternative-level stationary points or basis/correlation convergence. Displayed fields retain the original B3LYP/6-31G(d), grid3 model.'
 d['limitations'][1]='r2 IRC-driver convergence and independently verified endpoint connectivity are separate tests. Until all path and selected-electronic-field checks pass, the original five displayed geometries remain separately calculated constrained/saddle/minimum structures. Consult the r2 audit for actual completed and missing calculations.'
 unstable=[name for name,r in comparisons if not r['referenceInternalStable'] or not r['referenceExternalStable']]
 if unstable:d['warnings'].append('METHOD DIAGNOSTIC LIMITATION: unstable reference determinants in '+', '.join(unstable)+'. These values are retained as diagnostics, not validated correlated benchmarks; they do not replace the displayed B3LYP fields.')
 for source in (ROOT/'research/diels-alder/r2').glob('*'):
  if source.is_file() and source.suffix in ['.py','.txt']:shutil.copy2(source,OUT/source.name)
 links=[('r2 scientific validation and limitations','V037_R2_AUDIT.md'),('r2 exact software versions','software-versions.json'),('r2 reproduction dependencies','requirements.txt'),('r2 accepted-point/provenance checks','restart-20261022/path-validation.json'),('r2 independent endpoint comparisons','restart-20261022/connectivity-validation.json'),('r2 method diagnostic checks','restart-20261022/comparisons/validation.json'),('Actual calculated geometries (validation status labeled)','restart-20261022/geometry-validation.png'),('Actual calculated path energies/distances','restart-20261022/path-validation.png')]
 for direction in ['forward','backward']:
  for label,file in [('IRC driver state and parameters','status.json'),('Accepted/rejected-step provenance','step-provenance.json'),('Raw SCF/gradient trial archive','evaluations.zip')]:links.append((direction+' '+label,'restart-20261022/'+direction+'/'+file))
 for label,file in links:
  if (OUT/file).exists():d['sourceFiles'].append(dict(label=label,path='reaction-lab/diels-alder/r2/'+file))
 return d
