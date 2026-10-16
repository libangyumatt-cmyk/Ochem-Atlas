"""Static QA renderings of actual retained coordinates and isosurface triangles."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from compute import OUT,ROOT
QA=ROOT/'research/diels-alder';COL={'C':'#344d55','H':'#d3d6cb'}
def molecule(ax,f):
 x=np.array([a['xyzAngstrom'] for a in f['atoms']])
 for c in f['connections']:
  p=x[c['atoms']];ax.plot(*p.T,color='#63736d',lw=1.5,ls=':' if c['style']=='guide' else '-')
 for e in ['C','H']:
  p=np.array([a['xyzAngstrom'] for a in f['atoms'] if a['element']==e]);ax.scatter(*p.T,s=45 if e=='C' else 20,c=COL[e],edgecolors='#777777')
 center=x.mean(0);r=3.3
 ax.set(xlim=(center[0]-r,center[0]+r),ylim=(center[1]-r,center[1]+r),zlim=(center[2]-r,center[2]+r));ax.set_box_aspect([1,1,1]);ax.view_init(25,-65);ax.set_axis_off()
def field(ax,surf):
 for sign,col in [('positive','#239b90'),('negative','#cc8a3a')]:
  if not surf[sign]:continue
  v=np.array(surf[sign]['vertices']).reshape(-1,3);t=np.array(surf[sign]['faces']).reshape(-1,3);ax.add_collection3d(Poly3DCollection(v[t],facecolor=col,alpha=.45,edgecolor='none'))
def main():
 d=json.loads((OUT/'diels-alder.json').read_text());fig=plt.figure(figsize=(16,4))
 for i,f in enumerate(d['frames']):
  ax=fig.add_subplot(1,5,i+1,projection='3d');molecule(ax,f);ax.set_title(f"{f['id']}{(' · partial' if f.get('constrainedGradientTargetMet') is False else '')}\nC1–C5 {f['bonds'][0]['distanceAngstrom']:.3f} Å\nC4–C6 {f['bonds'][1]['distanceAngstrom']:.3f} Å",fontsize=10)
 fig.suptitle('Calculated geometries: constrained study + verified saddle/minimum; NOT IRC');fig.tight_layout(rect=[0,0,1,.85]);fig.savefig(QA/'validation-structures.png',dpi=140);plt.close(fig)
 f=next(f for f in d['frames'] if f['id']=='ts');m=json.loads((OUT/'ts-meshes.json').read_text());sm=json.loads((OUT/'symmetry-meshes.json').read_text());fig=plt.figure(figsize=(16,5))
 for i,key in enumerate(['total','deformation','occupied','fragment']):
  ax=fig.add_subplot(1,4,i+1,projection='3d');molecule(ax,f)
  if key=='fragment':
   field(ax,sm['diene'][1]);field(ax,sm['dienophile'][1]);label='Separate frozen-fragment MOs\n0.045 bohr⁻³ᐟ²'
  else:field(ax,m[key][1]);label=key+'\n'+str(d['levels'][key][1])+(' bohr⁻³ᐟ²' if key=='occupied' else ' e bohr⁻³')
  ax.set_title(label,fontsize=11)
 fig.suptitle('Actual TS meshes; signed colors denote field sign, never electrical charge');fig.tight_layout(rect=[0,0,1,.85]);fig.savefig(QA/'validation-surfaces.png',dpi=150);plt.close(fig)
 # Independently inspect the regenerated short-distance surfaces, not only TS.
 f=next(f for f in d['frames'] if f['id']=='post-ts');m=json.loads((OUT/'post-ts-meshes.json').read_text());fig=plt.figure(figsize=(16,5))
 for i,key in enumerate(['total','difference','deformation','occupied']):
  ax=fig.add_subplot(1,4,i+1,projection='3d');molecule(ax,f);field(ax,m[key][1]);ax.set_title(key+'\n'+str(d['levels'][key][1])+(' bohr⁻³ᐟ²' if key=='occupied' else ' e bohr⁻³'),fontsize=11)
 fig.suptitle('Regenerated calculated 1.9 Å fields; constrained geometry, NOT IRC');fig.tight_layout(rect=[0,0,1,.85]);fig.savefig(QA/'validation-short-distance-surfaces.png',dpi=150);plt.close(fig)
if __name__=='__main__':main()
