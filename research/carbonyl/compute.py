"""Gas-phase H- + H2CO: RHF/6-31++G(d,p), charge -1, singlet, 18e.
Four Cs-relaxed distance/angle constrained points; one separately optimized
methoxide minimum; two alternative angles at the shared 1.9 A distance.
No IRC or transition state is claimed. Run with OMP_NUM_THREADS=1.
"""
from pathlib import Path
import json, platform, sys
import numpy as np
import scipy, pyscf
from scipy.optimize import minimize
from pyscf import gto,scf,lib
from pyscf.hessian import thermo
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'dist/reaction-lab/carbonyl';OUT.mkdir(parents=True,exist_ok=True)
BOHR=.529177210903;BASIS='6-31++g(d,p)'
lib.num_threads(1)
try:lib.current_memory()
except FileNotFoundError:lib.current_memory=lambda:(0,0)
def coords(p):
    co,hx,hy,hz,r,t=p
    return [('C',(0,0,0)),('O',(co,0,0)),('H',(hx,hy,hz)),('H',(hx,-hy,hz)),('H',(r*np.cos(t),0,r*np.sin(t)))]
def solve(a,log=None,charge=-1):
    m=gto.M(atom=a,basis=BASIS,unit='Angstrom',charge=charge,spin=0,verbose=4 if log else 0,output=str(log) if log else None)
    f=scf.RHF(m);f.conv_tol=1e-11;f.conv_tol_grad=1e-7;f.max_cycle=150;f.kernel()
    if not f.converged:f=f.newton();f.kernel()
    assert f.converged
    return m,f
def opt(start,r=None,t=None):
    fixed=r is not None
    def fun(x):
        p=np.r_[x,r,t] if fixed else x
        m,f=solve(coords(p));g=f.nuc_grad_method().kernel()/BOHR
        co,hx,hy,hz,rr,tt=p
        j=np.array([g[1,0],g[2,0]+g[3,0],g[2,1]-g[3,1],g[2,2]+g[3,2],
          g[4,0]*np.cos(tt)+g[4,2]*np.sin(tt),rr*(-g[4,0]*np.sin(tt)+g[4,2]*np.cos(tt))])
        return f.e_tot,j[:4] if fixed else j
    z=minimize(fun,np.array(start[:4] if fixed else start),jac=True,method='BFGS',options={'gtol':3e-7,'maxiter':100})
    assert max(abs(z.jac))<1e-5,(z.message,z.jac)
    return np.r_[z.x,r,t] if fixed else z.x,float(max(abs(z.jac)))
def save(p,id,group,free_gradient,minimum=False):
    a=coords(p);m,f=solve(a,OUT/(id+'.log'));c=f.mo_coeff;s=m.intor('int1e_ovlp');dm=f.make_rdm1();g=f.nuc_grad_method().kernel()
    _,_,stable_i,stable_e=f.stability(internal=True,external=True,return_status=True)
    assert stable_i and stable_e,(id,stable_i,stable_e)
    np.savez_compressed(OUT/(id+'-scf.npz'),mo_coeff=c,mo_occ=f.mo_occ,mo_energy=f.mo_energy,overlap=s,density_matrix=dm,coordinates=m.atom_coords()*BOHR,gradient=g,parameters=p)
    ps=dm@s;sl=m.aoslice_by_atom()
    def bond(a,b):
        i,j=sl[a,2:];k,l=sl[b,2:];return float(np.sum(ps[i:j,k:l]*ps[k:l,i:j].T))
    xyz=np.array([v for _,v in a]);v=xyz[1:4]-xyz[0]
    normal=np.cross(xyz[2]-xyz[1],xyz[3]-xyz[1]);height=abs(np.dot(xyz[0]-xyz[1],normal))/np.linalg.norm(normal)
    angle_sum=sum(np.degrees(np.arccos(np.clip(np.dot(v[i],v[j])/np.linalg.norm(v[i])/np.linalg.norm(v[j]),-1,1))) for i,j in [(0,1),(1,2),(2,0)])
    frame={'id':id,'group':group,'geometryKind':'constrained Cs-relaxed frame; not a stationary point',
      'atoms':[dict(element=e,xyzAngstrom=list(map(float,v)),label=['C','O','H1','H2','H nu'][i],atomId=['C','O','H1','H2','Hnu'][i]) for i,(e,v) in enumerate(a)],
      'energyHartree':float(f.e_tot),'scfConverged':bool(f.converged),'internalStable':bool(stable_i),'externalStable':bool(stable_e),
      'orthonormalError':float(abs(c.T@s@c-np.eye(m.nao)).max()),'electronCountAOMetric':float(np.einsum('ij,ji',dm,s)),
      'scfOrbitalGradientNorm':float(np.linalg.norm(f.get_grad(c,f.mo_occ,f.get_fock()))),'maxNuclearGradientEhPerBohr':float(abs(g).max()),
      'maxFreeParameterGradientEhPerAngstromOrRadian':free_gradient,
      'distanceAngstrom':float(p[4]),'angleDegree':float(np.degrees(p[5])),
      'bonds':[dict(atoms=[0,1],label='C–O',distanceAngstrom=float(p[0]),mayer=bond(0,1)),dict(atoms=[0,4],label='C–H(nu)',distanceAngstrom=float(p[4]),mayer=bond(0,4))],
      'geometryDescriptors':[dict(label='O–C–H(nu) approach angle',value=float(np.degrees(p[5])),unit='°'),dict(label='C displacement from O/H1/H2 plane',value=float(height),unit='Å'),dict(label='360° minus O–C–H1 / H1–C–H2 / H2–C–O sum',value=float(360-angle_sum),unit='°')],
      'connections':[dict(atoms=[0,j],style='guide' if j==4 else 'bond') for j in range(1,5)]}
    if minimum:
        h=f.Hessian().kernel();ha=thermo.harmonic_analysis(m,h);fr=ha['freq_wavenumber']
        np.savez_compressed(OUT/(id+'-hessian.npz'),hessian=h,gradient=g,frequencies=fr,normal_modes=ha['norm_mode'])
        assert abs(g).max()<2e-5 and all(x.real>20 and abs(x.imag)<1 for x in fr),(g,fr)
        frame.update(geometryKind='Hessian-verified methoxide minimum',frequenciesCm=[float(x.real) for x in fr],stationaryPointVerified=True)
    (OUT/(id+'.xyz')).write_text('5\n'+frame['geometryKind']+'\n'+''.join(f'{e} {v[0]:.12f} {v[1]:.12f} {v[2]:.12f}\n' for e,v in a))
    m.stdout.close();print(id,frame['energyHartree'],frame['distanceAngstrom'],frame['angleDegree'],height,flush=True)
    return frame

def main():
    meta=dict(method='RHF',basis='6-31++G(d,p)',program='PySCF '+pyscf.__version__,python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,charge=-1,multiplicity=1,electronCount=18,
      environment='isolated gas phase; bare hydride, no counterion or solvent',
      scfProtocol=dict(energyToleranceEh=1e-11,orbitalGradientTolerance=1e-7,maxCycles=150,newtonFallback=True,stability='internal and external RHF stability checked for every complex frame'),
      pathKind='Four fixed C–H(nu) distance / 110° angle Cs-relaxed frames plus a separately optimized minimum; two matched-distance angle comparisons. Not an IRC. No transition state claimed.',
      atomMapping='C, O, H1, H2, Hnu fixed identities. C at origin, O on +x, Hnu in xz with z>0; H1/H2 reflected across xz. No post-hoc fit.',
      competingPathways='Bare gas-phase hydride is an idealized donor, not LiAlH4 or NaBH4. H abstraction (H2 + HCO−), detachment/other electronic states and solvent/counterion chemistry were not compared; the constrained addition branch does not establish global selectivity or kinetics.',frames=[])
    start=[1.2,-.58,.94,0,3,np.radians(110)]
    for i,r in enumerate([3.,2.4,1.9,1.5]):
        p,err=opt(start,r,np.radians(110));meta['frames'].append(save(p,f'addition-{i}','addition',err));start=p
        if r==1.9:middle=p.copy()
    p,err=opt(start);meta['frames'].append(save(p,'product','addition',err,True))
    for angle in [90,130]:
        p,err=opt(middle,1.9,np.radians(angle));meta['frames'].append(save(p,f'angle-{angle}','angles',err))
    (OUT/'calculation.json').write_text(json.dumps(meta,indent=2))
if __name__=='__main__':main()
