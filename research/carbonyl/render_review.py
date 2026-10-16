"""Render geometry and actual isosurface meshes for internal visual QA only.
Triangle subsets in this review figure reduce rasterization cost; published
meshes and volumetric arrays retain all triangles/data.
"""
from pathlib import Path
import sys,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'dist/reaction-lab/carbonyl'
d=json.loads((OUT/'carbonyl.json').read_text());kinds=['total','difference','deformation','donor','pi','pistar']
fig=plt.figure(figsize=(18,20))
for row,f in enumerate(d['frames']):
 mesh=json.loads((ROOT/'dist'/f['meshFile']).read_text())
 for col,kind in enumerate(kinds):
  ax=fig.add_subplot(len(d['frames']),len(kinds),row*len(kinds)+col+1,projection='3d')
  for sign,s in mesh[kind][1].items():
   if s is None:continue
   v=np.array(s['vertices']).reshape(-1,3);faces=np.array(s['faces']).reshape(-1,3);faces=faces[::max(1,len(faces)//1400)]
   ax.add_collection3d(Poly3DCollection(v[faces],facecolor='#397f79' if sign=='positive' else '#bd8755',alpha=.22,linewidth=0))
  xyz=np.array([a['xyzAngstrom'] for a in f['atoms']])
  for j,a in enumerate(f['atoms']):ax.scatter(*xyz[j],s=20,color={'H':'#8e9896','C':'#243e47','O':'#bd6c62'}[a['element']]);ax.text(*xyz[j],a['label'],fontsize=6)
  for e in f['connections']:
   a,b=e['atoms'];ax.plot(*xyz[[a,b]].T,color='#7b8a86',linewidth=.7,linestyle='--' if e['style']=='guide' else '-')
  ax.set(xlim=(-2.3,2.3),ylim=(-2.3,2.3),zlim=(-2,5.2));ax.view_init(18,-70);ax.set_box_aspect((1,1,1));ax.set_axis_off();ax.set_title(f['id']+' · '+kind,fontsize=9)
fig.tight_layout();target=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'v036-carbonyl-surfaces.png';fig.savefig(target,dpi=125);print(target)
