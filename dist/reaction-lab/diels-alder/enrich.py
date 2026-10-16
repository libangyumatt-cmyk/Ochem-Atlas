"""Idempotent metadata analysis from retained nuclear gradients/coordinates.
Does not regenerate or alter quantum-chemical fields or energies.
"""
from compute import OUT
import json
import numpy as np

def main():
 path=OUT/'diels-alder.json';d=json.loads(path.read_text())
 for f in d['frames']:
  names={'approach':'3.0 Å constrained','pre-ts':'2.5 Å constrained','ts':'Verified saddle','post-ts':'1.9 Å constrained','product':'Verified cyclohexene minimum'}
  f['label']=names[f['id']]+f" · C1–C5 {f['bonds'][0]['distanceAngstrom']:.3f} Å"
  f['plotLabel']={'approach':'r=3.0','pre-ts':'r=2.5','ts':'TS','post-ts':'r=1.9','product':'product'}[f['id']]
  if f['id']=='product':
   for edge in f['connections']:
    if sorted(edge['atoms']) in [[0,4],[3,5]]:edge['style']='bond'
  w=np.load(OUT/(f['id']+'-scf.npz'));x=w['coordinates'];g=w['gradient'].ravel();j=np.zeros((2,len(g)))
  for row,(a,b) in enumerate([(0,4),(3,5)]):
   u=(x[a]-x[b])/np.linalg.norm(x[a]-x[b]);j[row,3*a:3*a+3]=u;j[row,3*b:3*b+3]=-u
  f['maxProjectedFreeGradientEhPerBohr']=float(max(abs(g-j.T@np.linalg.solve(j@j.T,j@g))))
  if f['id'] not in ['ts','product']:
   f['constrainedGradientTargetEhPerBohr']=3e-4;f['constrainedGradientTargetMet']=f['maxProjectedFreeGradientEhPerBohr']<3e-4
   f['geometryRelaxationStatus']='independent projected-gradient target met' if f['constrainedGradientTargetMet'] else 'partial: independent projected-gradient target NOT met'
   if not f['constrainedGradientTargetMet']:
    f['label']=f['label'].replace('constrained','constrained, PARTIALLY RELAXED')
    f['geometryKind']='Fixed forming distances, partially relaxed geometry; independent projected gradient exceeds 3e-4 Eh/bohr target. Not a stationary point or IRC.'
  label='Max distance-constraint projected nuclear gradient';f['geometryDescriptors']=[q for q in f['geometryDescriptors'] if q['label']!=label]+[dict(label=label,value=f['maxProjectedFreeGradientEhPerBohr'],unit='Eh/bohr')]
  if 'refinementChecks' in f:
   label='Moving-grid response projected nuclear gradient';f['geometryDescriptors']=[q for q in f['geometryDescriptors'] if q['label']!=label]+[dict(label=label,value=f['refinementChecks']['movingGridProjectedGradientEhPerBohr'],unit='Eh/bohr')]
 partial=[f['id'] for f in d['frames'] if f.get('constrainedGradientTargetMet') is False]
 d['pathKind']='Two relaxed equal-distance constrained points, one partially relaxed short-distance input, a full-Hessian verified saddle and an independent product minimum. Not an IRC; no full endpoint connectivity established.' if partial else 'Three independently checked equal-distance constrained points, a full-Hessian verified saddle and an independent product minimum. Not an IRC; no full endpoint connectivity established.'
 warning='PARTIAL GEOMETRY RELAXATION: '+', '.join(partial)+' exceeds the independent projected-gradient target (3e-4 Eh/bohr); its electronic fields are calculated at the stated input, not a fully relaxed constrained point.'
 d['warnings']=[w for w in d.get('warnings',[]) if not w.startswith('PARTIAL GEOMETRY RELAXATION:')]
 if partial:d['warnings'].append(warning)
 path.write_text(json.dumps(d,indent=2))
if __name__=='__main__':main()
