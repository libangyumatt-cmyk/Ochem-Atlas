"""Expose independently checked r3 findings without promoting an IRC series."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'dist/reaction-lab/diels-alder/r3'
def extend(d):
 assessment=json.loads((ROOT/'audit/V037_R3_CONNECTIVITY.json').read_text());back=json.loads((OUT/'backward-attempt1/backward/independent-validation.json').read_text())
 assert assessment['result']=='IRC validation incomplete' and not assessment['strictTwoMinimumIrcConnectivityVerified']
 assert assessment['reactantEndpoint']['minimumVerified']
 assert back['driverConverged'] and not back['descentCheckPassed']
 assert all(x['minimumVerified'] for x in assessment['forwardEndpointAssessment']['endpoints'].values())
 d['validationR3']=dict(overallStatus='IRC validation incomplete',strictIrcConnectivityVerified=False,validatedIRCSeriesExposed=False,backwardDriverConverged=True,backwardDescentCheckPassed=False,acceptedBackwardPoints=len(back['acceptedIRCPoints']),maximumAcceptedEnergyIncreaseHartree=back['maximumAcceptedEnergyIncreaseHartree'],descentToleranceHartree=back['descentToleranceHartree'],reactantEndpointMinimumVerified=assessment['reactantEndpoint']['minimumVerified'],report='reaction-lab/diels-alder/r3/V037_R3_AUDIT.md',summary='Two independently relaxed cyclohexene minima and a finite butadiene–ethylene encounter minimum passed checks. The backward driver forced one uphill step beyond the fixed descent tolerance; the original forward endpoint is a ring conformational saddle. Strict two-minimum IRC connectivity remains unverified.')
 d['pathKind']='Original constrained study: Not an IRC. Separate r3 recovery verified relaxed product/encounter minima but failed an independent IRC descent check; no validated electronic-field series is exposed.'
 d['limitations'][1]=d['validationR3']['summary']+' Displayed fields remain the original constrained/saddle/minimum calculations.'
 d['warnings'].append('IRC VALIDATION INCOMPLETE (r3): '+d['validationR3']['summary'])
 shutil.copy2(ROOT/'V037_R3_AUDIT.md',OUT/'V037_R3_AUDIT.md');shutil.copy2(ROOT/'audit/V037_R3_CONNECTIVITY.json',OUT/'connectivity-assessment.json')
 d['sourceFiles'].extend([dict(label='r3 recovery, numerical results and limitations',path=d['validationR3']['report']),dict(label='r3 independent connectivity assessment',path='reaction-lab/diels-alder/r3/connectivity-assessment.json')])
 return d
