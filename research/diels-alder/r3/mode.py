"""Reconstruct the old endpoint mode and its internal-coordinate character."""
from pathlib import Path
import sys,itertools
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r2'))
from common import *
from pyscf.hessian import thermo
old=BASE/'r2/restart-20261022';w=np.load(old/'endpoints/forward/wavefunction.npz');x=w['coordinatesAngstrom'];h=w['hessian'];hs=(h+h.transpose(1,0,3,2))/2
m=gto.M(atom=list(zip(['C']*6+['H']*10,x)),basis='6-31g(d)',verbose=0)
vib=thermo.harmonic_analysis(m,hs);freq=vib['freq_wavenumber'];idx=int(np.argmax(abs(freq.imag)));mode=np.real_if_close(vib['norm_mode'][idx]);mode/=np.linalg.norm(mode)
saved=np.real_if_close(w['normal_modes'][0]);saved/=np.linalg.norm(saved)
s=m.intor('int1e_ovlp');assert np.max(abs(w['mo_coeff'].T@s@w['mo_coeff']-np.eye(m.nao)))<1e-8
assert abs(np.einsum('ij,ji',w['density_matrix'],s)-46)<1e-8
assert abs(np.sum(mode*saved))>.999
ring=[0,1,2,3,5,4]
def torsion(q):
 a,b,c,d=q;v=b-a;axis=c-b;axis/=np.linalg.norm(axis);u=d-c
 n1=np.cross(v,axis);n2=np.cross(axis,u)
 return np.degrees(np.arctan2(np.dot(np.cross(n1,n2),axis),np.dot(n1,n2)))
rows=[]
for j in range(6):
 ids=[ring[(j+k)%6] for k in range(4)]
 angles=[torsion((x+t*mode)[ids]) for t in [-.01,0,.01]]
 delta=(angles[2]-angles[0]+180)%360-180
 rows.append(dict(atomsOneBased=[i+1 for i in ids],torsionDegrees=angles[1],derivativeDegreesPerAngstrom=delta/.02))
report=dict(sourceSha256=hashlib.sha256((old/'endpoints/forward/wavefunction.npz').read_bytes()).hexdigest(),symmetrizedImaginaryFrequencyCm=float(abs(freq[idx].imag)),modeMetric='Cartesian unit norm, displacement in angstrom; arbitrary sign',carbonSquaredAmplitudeFraction=float(np.sum(mode[:6]**2)),ringTorsions=rows,interpretation='Ring torsional/puckering direction based on internal torsion derivatives. Genuine negative directional energy curvature retained at both grids in r2; displaced minimizations needed to distinguish conformational instability from numerical/optimization effects. No harmless-mode assumption.')
write(ROOT/'audit/V037_R3_MODE.json',report);print(json.dumps(report,indent=2))
