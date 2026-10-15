"""Internal visual review, not a source of scientific scalar fields."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from compute_sn2 import OUT
D=json.loads((OUT/'sn2.json').read_text());frames=D['frames'];fig=plt.figure(figsize=(18,3.3*len(frames)),facecolor='#fffefa')
for i,f in enumerate(frames):
 meshes=json.loads((OUT/(f['id']+'-meshes.json')).read_text())
 for j,kind in enumerate(['total','difference','deformation','occupied','virtual']):
  ax=fig.add_subplot(len(frames),5,i*5+j+1,projection='3d',computed_zorder=False);ax.set_facecolor('#f2f4ec')
  for sign,s in meshes[kind][1].items():
   if not s:continue
   v=np.array(s['vertices']).reshape(-1,3);tri=np.array(s['faces']).reshape(-1,3)
   ax.add_collection3d(Poly3DCollection(v[tri],facecolors='#397f79' if sign=='positive' else '#bd8755',edgecolors='none',alpha=.4,zorder=1))
  for a in f['atoms']:
   x,y,z=a['xyzAngstrom'];ax.scatter(x,y,z,s=30,c={'Cl':'#6e9673','C':'#344b53','H':'#d9dedb'}[a['element']],zorder=5);ax.text(x,y,z+.2,a['label'],fontsize=7,zorder=6)
  ax.set_xlim(-4,4);ax.set_ylim(-2.2,2.2);ax.set_zlim(-2.2,2.2);ax.set_box_aspect((8,4.4,4.4));ax.view_init(20,-63);ax.set_axis_off();ax.set_title(f"{f['id']} · {kind}\nq {f['qAngstrom']:.2f} Å · iso {D['levels'][kind][1]}",fontsize=9)
fig.tight_layout();fig.savefig('/workspace/scratch/69db76a371c7/v035-surfaces-review.png',dpi=115);plt.close(fig)
