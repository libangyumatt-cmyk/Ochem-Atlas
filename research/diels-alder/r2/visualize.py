"""Actual accepted geometries/energies only; report validation status on plots."""
from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def molecule(ax,x,title):
 x=np.array(x);elements=[a['element'] for a in record()['atoms']]
 ax.scatter(*x[:6].T,s=65,c='#345c68');ax.scatter(*x[6:].T,s=20,c='#c2ccd0')
 for i in range(16):
  if i<6:ax.text(*x[i],str(i+1),fontsize=9)
  for j in range(i+1,16):
   limit=1.85 if i<6 and j<6 else 1.30
   if (i<6 or j<6) and np.linalg.norm(x[i]-x[j])<limit:ax.plot(*x[[i,j]].T,color='#617a84',lw=2)
 for i,j in [(0,4),(3,5)]:
  if np.linalg.norm(x[i]-x[j])>=1.85:ax.plot(*x[[i,j]].T,color='#bf812d',ls='--',lw=1)
 span=np.ptp(x,axis=0).max()/2+.4;center=x.mean(0)
 ax.set_xlim(center[0]-span,center[0]+span);ax.set_ylim(center[1]-span,center[1]+span);ax.set_zlim(center[2]-span,center[2]+span);ax.set_box_aspect([1,1,1]);ax.set_axis_off();ax.view_init(20,-65);ax.set_title(title,fontsize=10)

def main():
 r=json.loads((OUT/'path-validation.json').read_text());fig=plt.figure(figsize=(12,8));views=[('Retained r1 saddle',np.array([a['xyzAngstrom'] for a in record()['atoms']]))]
 for d,b in r['branches'].items():
  if b['acceptedIRCPoints']:
   p=b['acceptedIRCPoints'][-1];views.append((d+' latest accepted point\nnot an endpoint/minimum claim',p['coordinatesAngstrom']))
 views.append(('Independent r1 product minimum',np.array([a['xyzAngstrom'] for a in record('product')['atoms']])))
 for i,(title,x) in enumerate(views):molecule(fig.add_subplot(2,2,i+1,projection='3d'),x,title)
 fig.suptitle('Diels–Alder: actual calculated structures; path verification '+r['result']);fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(OUT/'geometry-validation.png',dpi=140);plt.close(fig)
 fig,axs=plt.subplots(1,2,figsize=(12,4));ts=record()['energyHartree']
 for d,b in r['branches'].items():
  pts=b['acceptedIRCPoints'];q=[p['cumulativeChordLengthBohrSqrtAmu'] for p in pts];axs[0].scatter(q,[(p['energyHartree']-ts)*627.5094740631 for p in pts],s=12,label=d)
  for k,label in [(0,'C1–C5'),(1,'C4–C6')]:axs[1].scatter(q,[p['formingDistancesAngstrom'][k] for p in pts],s=12,marker='o' if k==0 else 'x',label=d+' '+label)
 for ax in axs:ax.set_xlabel('Cumulative accepted chord length / bohr sqrt(amu)');ax.legend(fontsize=8)
 axs[0].set_ylabel('Electronic energy relative to retained TS / kcal mol⁻¹');axs[1].set_ylabel('Forming bond distances / Å');fig.suptitle('Actual accepted IRC evaluations; verification '+r['result']);fig.tight_layout();fig.savefig(OUT/'path-validation.png',dpi=140);plt.close(fig)

if __name__=='__main__':main()
