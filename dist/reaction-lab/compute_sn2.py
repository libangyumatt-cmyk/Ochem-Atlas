"""RHF/6-31+G(d) chloride identity SN2. Five independently computed geometries.
No IRC: fixed Cl distances, C3v-constrained relaxation of the three hydrogens.
The symmetric center is separately optimized and Hessian-tested.
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/reaction-lab/compute_sn2.py
"""
from pathlib import Path
import json, platform
import numpy as np
import scipy, pyscf
from scipy.optimize import minimize
from pyscf import gto, scf, lib
from pyscf.hessian import thermo

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'dist/reaction-lab';OUT.mkdir(exist_ok=True)
lib.num_threads(1)
try:lib.current_memory()
except FileNotFoundError:lib.current_memory=lambda:(0,0)
BOHR=.529177210903
BASIS='6-31+g(d)'

def atoms(rin,rout,rho,h):
    return [('C',(0,0,0)),('Cl',(-rin,0,0)),('Cl',(rout,0,0))]+[
        ('H',(h,rho*np.cos(a),rho*np.sin(a))) for a in np.arange(3)*2*np.pi/3]

def solve(coords,log=None,charge=-1):
    mol=gto.M(atom=coords,unit='Angstrom',basis=BASIS,charge=charge,spin=0,
              verbose=4 if log else 0,output=str(log) if log else None)
    mf=scf.RHF(mol);mf.conv_tol=1e-11;mf.conv_tol_grad=1e-7;mf.max_cycle=150
    mf.kernel()
    if not mf.converged:
        mf=mf.newton();mf.kernel()
    assert mf.converged
    return mol,mf

def optimize_center():
    def fun(x):
        mol,mf=solve(atoms(x[0],x[0],x[1],0))
        grad=mf.nuc_grad_method().kernel()/BOHR
        gr=-grad[1,0]+grad[2,0]
        gh=sum(grad[3+j,1]*np.cos(a)+grad[3+j,2]*np.sin(a)
               for j,a in enumerate(np.arange(3)*2*np.pi/3))
        return mf.e_tot,np.array([gr,gh])
    result=minimize(fun,[2.3,1.06],jac=True,method='BFGS',options={'gtol':2e-7,'maxiter':60})
    print('Symmetric optimization',result.x,result.fun,result.jac,result.message,flush=True)
    assert np.max(abs(result.jac))<2e-5
    return result.x

def main():
    import sys
    if '--reuse-center' in sys.argv:
        meta=json.loads((OUT/'calculation.json').read_text())
        rt=meta['centerClDistanceAngstrom'];rhot=meta['centerCHDistanceAngstrom']
        verified=meta['centerVerifiedTransitionState'];meta['frames']=[]
    else:
        rt,rhot=optimize_center()
        mol,mf=solve(atoms(rt,rt,rhot,0),OUT/'symmetric-hessian.log')
        gradient=mf.nuc_grad_method().kernel()
        hessian=mf.Hessian().kernel()
        vibration=thermo.harmonic_analysis(mol,hessian)
        freq=vibration['freq_wavenumber']
        frequency=[{'realCm':float(v.real),'imaginaryCm':float(v.imag)} for v in freq]
        imag=sum(v.imag>20 for v in freq)
        stationary=float(np.max(abs(gradient)))<2e-5
        verified=stationary and imag==1
        np.savez_compressed(OUT/'symmetric-hessian.npz',gradient=gradient,hessian=hessian,
                            frequencies=freq,normal_modes=vibration['norm_mode'])
        meta={'method':'RHF','basis':'6-31+G(d)','program':'PySCF '+pyscf.__version__,
              'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
              'charge':-1,'multiplicity':1,'electronCount':44,'environment':'isolated gas phase',
              'pathKind':'Five-point constrained distance scan; not an IRC. Fixed C and both Cl nuclei; C3v-constrained H relaxation.',
              'centerClDistanceAngstrom':float(rt),'centerCHDistanceAngstrom':float(rhot),
              'centerVerifiedTransitionState':bool(verified),'centerMaxGradientEhPerBohr':float(np.max(abs(gradient))),
              'centerImaginaryModeCountAbove20Cm':int(imag),'centerFrequencies':frequency,'frames':[]}
        print('Center Hessian',verified,frequency,flush=True)
    for k,q in enumerate([-.6,-.3,0,.3,.6]):
        rin,rout=rt-q,rt+q
        if q:
            def fun(x):
                mol,mf=solve(atoms(rin,rout,x[0],x[1]))
                g=mf.nuc_grad_method().kernel()/BOHR
                gr=sum(g[3+j,1]*np.cos(a)+g[3+j,2]*np.sin(a)
                       for j,a in enumerate(np.arange(3)*2*np.pi/3))
                return mf.e_tot,np.array([gr,sum(g[3:,0])])
            result=minimize(fun,[rhot,-q*.35],jac=True,method='BFGS',options={'gtol':3e-7,'maxiter':60})
            assert np.max(abs(result.jac))<2e-5,(k,result)
            rho,h=result.x
        else:rho,h=rhot,0
        coords=atoms(rin,rout,rho,h)
        mol,mf=solve(coords,OUT/f'frame-{k}.log')
        S=mol.intor('int1e_ovlp');C=np.array(mf.mo_coeff);occ=mf.mo_occ;dm=mf.make_rdm1()
        assert np.max(abs(C.T@S@C-np.eye(mol.nao)))<1e-9
        assert abs(np.einsum('ij,ji',dm,S)-44)<1e-9
        # Mayer bond index for a closed-shell AO density matrix P: sum (PS)uv(PS)vu.
        PS=dm@S;slices=mol.aoslice_by_atom()
        def mayer(a,b):
            i,j=slices[a,2:];l,m=slices[b,2:]
            return float(np.sum(PS[i:j,l:m]*PS[l:m,i:j].T))
        f={'id':f'frame-{k}','qAngstrom':q,'energyHartree':float(mf.e_tot),
           'rinAngstrom':float(rin),'routAngstrom':float(rout),
           'atoms':[{'element':s,'xyzAngstrom':list(map(float,v)),'label':('C','Cl in','Cl out','H1','H2','H3')[i]} for i,(s,v) in enumerate(coords)],
           'geometryKind':'Hessian-verified first-order saddle' if q==0 and verified else 'constrained scan frame; not a stationary point',
           'scfConverged':bool(mf.converged),'orthonormalError':float(np.max(abs(C.T@S@C-np.eye(mol.nao)))),
           'electronCountAOMetric':float(np.einsum('ij,ji',dm,S)),
           'scfOrbitalGradientNorm':float(np.linalg.norm(mf.get_grad(C,occ,mf.get_fock()))),
           'mayerCClIn':mayer(0,1),'mayerCClOut':mayer(0,2)}
        np.savez_compressed(OUT/f'frame-{k}-scf.npz',mo_coeff=C,mo_energy=mf.mo_energy,mo_occ=occ,
                            overlap=S,density_matrix=dm,coordinates=mol.atom_coords()*BOHR)
        (OUT/f'frame-{k}.xyz').write_text('6\n'+f['geometryKind']+'\n'+''.join(f'{s} {v[0]:.12f} {v[1]:.12f} {v[2]:.12f}\n' for s,v in coords))
        mol.stdout.close();meta['frames'].append(f)
        print(k,q,mf.e_tot,rin,rout,'Mayer',f['mayerCClIn'],f['mayerCClOut'],flush=True)
        (OUT/'calculation.json').write_text(json.dumps(meta,indent=2))
    (OUT/'calculation.json').write_text(json.dumps(meta,indent=2))

if __name__=='__main__':main()
