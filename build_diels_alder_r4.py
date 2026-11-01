"""Publish checked r4 diagnostic status; never promote a partial integration."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'dist/reaction-lab/diels-alder/r4'
def extend(d):
 checks=json.loads((ROOT/'audit/V037_R4_VALIDATION.json').read_text());assert not checks['completeIndependentIrcVerified']
 d['validationR4']=dict(overallStatus='IRC validation incomplete',strictIrcConnectivityVerified=False,validatedIRCSeriesExposed=False,report='reaction-lab/diels-alder/r4/V037_R4_AUDIT.md',summary='Fresh grid3/grid5 probes reproduce the uphill step and support integration overshoot rather than SCF noise. Smaller-step trials and six independent TS-started descending steps are diagnostic tests only; full independent endpoint connectivity remains unresolved.')
 shutil.copy2(ROOT/'V037_R4_AUDIT.md',OUT/'V037_R4_AUDIT.md');shutil.copy2(ROOT/'audit/V037_R4_VALIDATION.json',OUT/'validation-summary.json')
 d['sourceFiles'].extend([dict(label='r4 path-repair audit and limitations',path=d['validationR4']['report']),dict(label='r4 complete calculation records and checkpoints',path='reaction-lab/diels-alder/r4/calculations.zip')]);return d
