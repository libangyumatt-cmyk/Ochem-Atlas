"""Independent validation of distributed SN2 wavefunctions and scalar fields."""
import json
import numpy as np
from pyscf import gto,scf,lib
from scipy.optimize import linear_sum_assignment
from compute_sn2 import ROOT, OUT, BASIS, BOHR
lib.num_threads(1)
try:lib.current_memory()
except FileNotFoundError:lib.current_memory=lambda:(0,0)
D=json.loads((OUT/'sn2.json').read_text());ref=None;previous=None
h=np.load(OUT/'symmetric-hessian.npz')
assert np.max(abs(h['gradient']))<2e-5
assert sum(v.imag>20 for v in h['frequencies'])==1
assert sum(v.real>20 for v in h['frequencies'])==11
# Verify that the unstable mode changes the two C-Cl distances oppositely.
mode=h['normal_modes'][int(np.argmax(h['frequencies'].imag))]
a=mode[0,0]-mode[1,0];b=mode[2,0]-mode[0,0]
assert a*b<0
for f in D['frames']:
    coords=[(a['element'],a['xyzAngstrom']) for a in f['atoms']]
    m=gto.M(atom=coords,basis=BASIS,unit='Angstrom',charge=-1,spin=0,verbose=0)
    w=np.load(OUT/(f['id']+'-scf.npz'));t=np.load(OUT/(f['id']+'-tracked.npz'));g=np.load(OUT/(f['id']+'-fields.npz'))
    C,S,P=w['mo_coeff'],w['overlap'],w['density_matrix'];occ=w['mo_occ']
    assert m.nelectron==44 and sum(occ)==44
    assert np.max(abs(m.intor('int1e_ovlp')-S))<1e-10
    assert np.max(abs(C.T@S@C-np.eye(m.nao)))<1e-9
    assert abs(np.einsum('ij,ji',P,S)-44)<1e-9
    assert np.max(abs(P-(C*occ)@C.T))<1e-10
    mf=scf.RHF(m)
    assert abs(mf.energy_tot(dm=P)-f['energyHartree'])<1e-8
    assert np.linalg.norm(mf.get_grad(C,occ,mf.get_fock(dm=P)))<1e-6
    assert abs(f['quadratureElectronCount']-44)<5e-4
    for atom,key in [(1,'rinAngstrom'),(2,'routAngstrom')]:
        assert abs(np.linalg.norm(w['coordinates'][atom]-w['coordinates'][0])-f[key])<1e-9
    assert np.max(abs(w['coordinates']-m.atom_coords()*BOHR))<1e-9
    shape=tuple(D['grid']['shape']);origin=np.array(D['grid']['originBohr']);step=D['grid']['spacingBohr']
    for kind in ['total','difference','deformation','occupied','virtual']:assert g[kind].shape==shape and np.isfinite(g[kind]).all()
    assert g['total'].min()>=0
    if ref is None:ref=g['total'].copy()
    assert np.allclose(g['difference'],g['total']-ref,atol=3e-4,rtol=3e-6)
    # Re-evaluate a reproducible set of field grid points from the AO coefficients.
    flat=np.unique(np.r_[np.arange(0,np.prod(shape),997),np.ravel_multi_index((40,24,24),shape)])
    ijk=np.array(np.unravel_index(flat,shape)).T;xyz=origin+step*ijk;ao=m.eval_gto('GTOval_sph',xyz)
    density=np.einsum('pi,ij,pj->p',ao,P,ao)
    assert np.allclose(g['total'].ravel()[flat],density,atol=3e-5,rtol=2e-6)
    for name,j in zip(['occupied','virtual'],t['indices']):
        assert np.allclose(g[name].ravel()[flat],ao@t['mo_coeff'][:,j],atol=1e-7,rtol=3e-6)
    fragment_sum=np.zeros(len(xyz))
    for fragment in f['fragments']:
        name=fragment['id'];inds=fragment['atomIndices'];fw=np.load(OUT/(f['id']+'-'+name+'-scf.npz'))
        fm=gto.M(atom=[coords[i] for i in inds],basis=BASIS,charge=fragment['charge'],spin=0,verbose=0)
        aof=fm.eval_gto('GTOval_sph',xyz);fragment_sum+=np.einsum('pi,ij,pj->p',aof,fw['density_matrix'],aof)
        assert fragment['scfConverged'] and abs(fragment['quadratureElectronCount']-fm.nelectron)<5e-4
        assert abs(np.einsum('ij,ji',fw['density_matrix'],fm.intor('int1e_ovlp'))-fm.nelectron)<1e-8
    assert np.allclose(g['deformation'].ravel()[flat],density-fragment_sum,atol=3e-5,rtol=3e-6)
    if previous:
        pm,pc,pi=previous;overlap=pc.T@gto.intor_cross('int1e_ovlp',pm,m)@t['mo_coeff']
        for i,j,record in zip(pi,t['indices'],f['tracking']):
            assert abs(overlap[i,j]-record['alignedOverlap'])<1e-8
            block=np.where(occ==occ[j])[0]
            if occ[j]>0:block=np.where(occ>0)[0]
            rows,cols=linear_sum_assignment(-abs(overlap[np.ix_(block,block)]))
            assert dict(zip(block[rows],block[cols]))[i]==j
    previous=m,t['mo_coeff'],t['indices']
    print('PASS',f['id'],'coefficients, density/reference fields, normalization records, energy, distances and MO matching')
print('PASS Hessian: one imaginary vibrational mode with opposite C-Cl distance changes; no IRC asserted.')
