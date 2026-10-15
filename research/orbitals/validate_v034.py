"""Independent checks of distributed coefficients, grids, and scan correspondence.
Run with the pinned research/orbitals/requirements.txt environment.
Does not regenerate or modify scientific datasets.
"""
import gzip
import json
from pathlib import Path
import numpy as np
from pyscf import gto, scf, lib
from pyscf.tools import cubegen
from scipy.optimize import linear_sum_assignment

lib.num_threads(1)
try:
    lib.current_memory()
except FileNotFoundError:
    lib.current_memory = lambda: (0, 0)
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'dist/orbital-files/v034'
data = json.loads((ROOT / 'dist/orbital-diversity.json').read_text())
previous = None
for s in data['systems'] + data['scan']:
    mol = gto.M(atom=[(a['element'], a['xyzAngstrom']) for a in s['atoms']],
                charge=s['charge'], spin=s['multiplicity']-1, basis='sto-3g',
                unit='Angstrom', symmetry=True, verbose=0)
    wf = np.load(OUT / (s['id']+'-scf.npz'))
    C, occ = wf['mo_coeff'], wf['mo_occ']
    S = mol.intor('int1e_ovlp')
    assert np.max(abs(S-wf['overlap'])) < 1e-10
    assert np.max(abs(C.T@S@C-np.eye(mol.nao))) < 1e-10
    assert sum(occ) == mol.nelectron == s['electronCount']
    assert np.max(abs(mol.atom_coords()*0.529177210903-wf['atom_coords_angstrom'])) < 1e-9
    mf = scf.ROHF(mol) if s['multiplicity'] == 2 else scf.RHF(mol)
    dm = mf.make_rdm1(C, occ)
    assert abs(mf.energy_tot(dm=dm)-s['totalEnergyHartree']) < 1e-9
    fock = mf.get_fock(dm=dm)
    grad = float(np.linalg.norm(mf.get_grad(C, occ, fock)))
    assert grad < 1e-6, (s['id'], grad)
    coords = mol.atom_coords(unit='Angstrom')
    distances = np.linalg.norm(coords[:, None]-coords[None, :], axis=2)
    assert np.min(distances+np.eye(mol.natm)*100) > .7
    if s['multiplicity'] == 2:
        assert s['method'] == 'ROHF' and mol.nelec == (12, 11)
        # Check the determinant rather than trusting a reported scalar S².
        Ca, Cb = C[:, occ>0], C[:, occ==2]
        s2 = .5*(.5+1)+mol.nelec[1]-np.sum(abs(Ca.T@S@Cb)**2)
        assert abs(s2-.75) < 1e-10
        assert abs(np.einsum('ij,ji', dm[0]-dm[1], S)-1) < 1e-10
    cc = cubegen.Cube(mol, 44, 44, 44, margin=3)
    ao = mol.eval_gto('GTOval_sph', cc.get_coords())
    for o in s['orbitals']:
        path = ROOT / 'dist/orbital-files' / (o['fileStem']+'.cube.gz')
        lines = gzip.decompress(path.read_bytes()).decode().splitlines()
        n = abs(int(lines[2].split()[0]))
        field = np.fromstring(' '.join(lines[6+n:]), sep=' ')
        expected = (np.einsum('pi,ij,pj->p', ao, dm[0]-dm[1], ao)
                    if o['kind']=='spin-density' else ao@C[:, o['index']-1])
        # Cube writer retains five decimal places in scientific notation.
        assert np.max(abs(field-expected)) < 5.1e-6
        if o['kind']=='spin-density':
            somo = s['orbitals'][0]['index']-1
            assert np.max(abs(expected-(ao@C[:, somo])**2)) < 1e-12
            assert np.min(field) >= -1e-10 and o['mesh']['negative'] is None
        elif s['id'] in ('allyl', 'benzene', 'butadiene'):
            grid = field.reshape(44, 44, 44)
            assert np.max(abs(grid+grid[:, :, ::-1])) < 1e-5
            assert abs(o['occupation']-occ[o['index']-1]) < 1e-12
    if s['id'] == 'benzene':
        eps = [wf['mo_energy'][o['index']-1] for o in s['orbitals']]
        assert abs(eps[1]-eps[2]) < 1e-8 and abs(eps[3]-eps[4]) < 1e-8
        assert sum(o['occupation'] for o in s['orbitals']) == 6
    if 'torsionDegrees' in s:
        angle = np.degrees(np.arctan2(coords[5, 2], coords[5, 1]))
        assert abs(angle-s['torsionDegrees']) < 1e-8
        labels = mol.ao_labels()
        a = np.zeros(mol.nao); b = a.copy(); a[labels.index('0 C 2pz   ')] = 1
        t = np.radians(s['torsionDegrees'])
        b[labels.index('1 C 2pz   ')] = np.cos(t)
        b[labels.index('1 C 2py   ')] = -np.sin(t)
        local = a@S@b/np.sqrt((a@S@a)*(b@S@b))
        assert abs(local-s['localPAOOverlap']) < 1e-10
        if previous:
            pm, pc, old = previous
            cross = pc.T@gto.intor_cross('int1e_ovlp', pm, mol)@C
            assignment = {}
            for block in (np.where(occ>0)[0], np.where(occ==0)[0]):
                rows, cols = linear_sum_assignment(-abs(cross[np.ix_(block, block)]))
                assignment.update({int(block[r]): int(block[c]) for r, c in zip(rows, cols)})
            for oldo, newo, report in zip(old['orbitals'], s['orbitals'], s['tracking']):
                i, j = oldo['index']-1, newo['index']-1
                assert assignment[i] == j
                assert cross[i, j] > .95
                assert abs(cross[i, j]-report['alignedOverlap']) < 1e-9
                assert abs(np.max(np.delete(abs(cross[i]), j))-report['nextBestOverlap']) < 1e-9
            assert abs(np.linalg.norm(coords[1]-coords[0])-1.334) < 1e-9
        previous = mol, C, s
    print(f"PASS {s['id']}: electron count, AO metric, energy, gradient {grad:.2e}, grids, identity")
