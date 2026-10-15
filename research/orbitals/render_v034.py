"""Render static projections from the same computed meshes used by the viewer."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

root=Path(__file__).resolve().parents[2]
data=json.loads((root/'dist/orbital-diversity.json').read_text())
data['systems'] += data['scan']
out=root/'dist/orbital-files'
colors={'positive':'#397f79','negative':'#bd8755'}
for system in data['systems']:
 for orbital in system['orbitals']:
  fig=plt.figure(figsize=(6.4,4.2),facecolor='#f2f4ec')
  ax=fig.add_subplot(111,projection='3d',computed_zorder=False)
  ax.set_facecolor('#f2f4ec')
  all_xyz=[]
  for sign in ('negative','positive'):
   mesh=orbital['mesh'][sign]
   if mesh is None:continue
   vertices=np.array(mesh['vertices']).reshape(-1,3)
   triangles=np.array(mesh['faces']).reshape(-1,3)
   poly=Poly3DCollection(vertices[triangles],facecolors=colors[sign],edgecolor='none',alpha=.57,zorder=1)
   ax.add_collection3d(poly)
   all_xyz.append(vertices)
  coords=np.array([a['xyzAngstrom'] for a in system['atoms']])
  all_xyz.append(coords)
  for a in system['atoms']:
   x,y,z=a['xyzAngstrom']
   ax.scatter([x],[y],[z],s=100 if a['element']!='H' else 45,
              c={'H':'#d9dedb','C':'#344b53','O':'#c97961'}[a['element']],depthshade=False,zorder=5)
   ax.text(x,y,z+.16,a['label'],fontsize=8,color='#203c43',zorder=6)
  bounds=np.concatenate(all_xyz)
  mid=(bounds.max(axis=0)+bounds.min(axis=0))/2
  span=max(np.ptp(bounds,axis=0))*.65
  ax.set_xlim(mid[0]-span,mid[0]+span)
  ax.set_ylim(mid[1]-span,mid[1]+span)
  ax.set_zlim(mid[2]-span,mid[2]+span)
  ax.view_init(elev=22,azim=-58)
  ax.set_axis_off()
  ax.set_title(f"{system['name']} · {orbital['name']} · {system['method']}/{system['basis']}",fontsize=11,color='#203c43')
  caption=('Alpha excess / beta excess · spin density ±0.003 e bohr⁻³' if orbital['kind']=='spin-density' else 'Teal + phase · amber − phase · |ψ| = 0.035 bohr⁻³ᐟ²')
  fig.text(.5,.04,caption,ha='center',fontsize=8,color='#576f6b')
  path=out/f"{orbital['fileStem']}.png"
  fig.savefig(path,dpi=110,bbox_inches='tight',pad_inches=.1)
  plt.close(fig)
  print(path.name)
