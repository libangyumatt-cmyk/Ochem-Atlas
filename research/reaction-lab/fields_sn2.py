"""Evaluate actual SCF densities/orbitals and defined references on a common grid.
Requires compute_sn2.py outputs. No interpolation of electronic fields.
"""
from pathlib import Path
import json, gzip, shutil, hashlib
import numpy as np
from scipy.optimize import linear_sum_assignment
from pyscf import gto, scf, dft, lib
from skimage.measure import marching_cubes
from compute_sn2 import ROOT, OUT, BASIS, BOHR, solve
lib.num_threads(1)
N=(81,49,49);ORIGIN=np.array([-10.,-6.,-6.]);STEP=.25
LEVELS={'total':[.02,.05,.1],'difference':[.001,.003,.008],'deformation':[.001,.003,.008],
        'occupied':[.025,.04,.06],'virtual':[.025,.04,.06]}

def surfaces(field,level):
    result={}
    for name,sign in [('positive',1),('negative',-1)]:
        if (field*sign).max()<=level:result[name]=None;continue
        v,f,_,_=marching_cubes((field*sign).astype(np.float32),level,allow_degenerate=False)
        result[name]={'vertices':np.round((v*STEP+ORIGIN)*BOHR,3).ravel().tolist(),'faces':f.ravel().tolist(),'triangleCount':len(f)}
    return result

def quadrature(mol,dm):
    grid=dft.gen_grid.Grids(mol);grid.level=5;grid.build()
    count=0.
    for i in range(0,len(grid.coords),12000):
        ao=mol.eval_gto('GTOval_sph',grid.coords[i:i+12000]);rho=np.einsum('pi,ij,pj->p',ao,dm,ao)
        count+=rho@grid.weights[i:i+12000]
    return float(count)

def main():
    meta=json.loads((OUT/'calculation.json').read_text())
    grid=np.stack(np.meshgrid(*[ORIGIN[k]+STEP*np.arange(N[k]) for k in range(3)],indexing='ij'),axis=-1).reshape(-1,3)
    result={**meta,'schemaVersion':'1.0','event':'sn2:0','modelId':'chloride-identity-sn2',
        'grid':{'shape':N,'originBohr':ORIGIN.tolist(),'spacingBohr':STEP,'order':'C order, z fastest',
                'alignment':'C fixed at origin; incoming Cl on negative x, outgoing Cl on positive x; H1 in +y half-plane. No fit, rotation or relabeling.',
                'densityUnits':'electron bohr^-3','orbitalUnits':'bohr^-3/2','meshCoordinates':'angstrom','fieldPrecision':'float32 in NPZ; full float64 coefficients retained'},
        'references':{'difference':'rho(frame) minus rho(frame 0), at identical Cartesian grid coordinates. Includes nuclear displacement; not a unique electron-transfer density.',
        'deformation':'rho(complex) minus rho(Cl_in−) minus rho(CH3Cl_out), separately SCF-solved at each frame geometry in each fragment own 6-31+G(d) basis (no ghost functions). Fixed fragment membership across the scan; not counterpoise-corrected EDA.',
        'probability':'Absolute square of selected occupied canonical spatial orbital; integrates to 1, not occupation-weighted electron density.',
        'signs':'Teal positive / amber negative electron-number difference. Colors do not mean positive/negative electrical charge.'},
        'levels':LEVELS,'frames':[]}
    previous=None;reference=None
    cached={f['id']:f for f in json.loads((OUT/'sn2.json').read_text())['frames']} if (OUT/'sn2.json').exists() else {}
    for f in meta['frames']:
        k=int(f['id'].split('-')[-1]);wf=np.load(OUT/f'{f["id"]}-scf.npz')
        coords=[(a['element'],a['xyzAngstrom']) for a in f['atoms']]
        mol=gto.M(atom=coords,basis=BASIS,charge=-1,spin=0,verbose=0)
        C=wf['mo_coeff'].copy();occ=wf['mo_occ'];S=wf['overlap'];dm=wf['density_matrix']
        source_hash=hashlib.sha256((OUT/f'{f["id"]}-scf.npz').read_bytes()).hexdigest()
        if f['id'] in cached and cached[f['id']].get('sourceWavefunctionSha256')==source_hash and cached[f['id']].get('trackingProtocol')==2 and (OUT/f'{f["id"]}-fields.npz').exists():
            saved=cached[f['id']];tracked=np.load(OUT/f'{f["id"]}-tracked.npz')
            previous=mol,tracked['mo_coeff'],tracked['indices'].tolist()
            if reference is None:reference=np.load(OUT/f'{f["id"]}-fields.npz')['total'].astype(float).ravel()
            result['frames'].append(saved)
            if k==0:result['initialSelection']=json.loads((OUT/'sn2.json').read_text())['initialSelection']
            print(f['id'],'reusing validated fields for identical coefficients/geometry',flush=True)
            continue
        # Same-geometry fragment references, fixed membership (Cl incoming / rest).
        fragment_fields=[];fragment_meta=[];fragments=[]
        for name,inds,charge in [('incoming',[1],-1),('substrate',[0,2,3,4,5],0)]:
            fragment_path=OUT/f'{f['id']}-{name}-scf.npz'
            if fragment_path.exists():
                fw=np.load(fragment_path)
                fm=gto.M(atom=[coords[i] for i in inds],basis=BASIS,charge=charge,spin=0,verbose=0)
                assert np.max(abs(fm.atom_coords()*BOHR-fw['coordinates']))<1e-9
                assert 'converged SCF energy' in (OUT/f'{f['id']}-{name}.log').read_text()
                ff=scf.RHF(fm);ff.mo_coeff=fw['mo_coeff'];ff.mo_occ=fw['mo_occ'];ff.mo_energy=fw['mo_energy']
                ff.e_tot=ff.energy_tot(dm=fw['density_matrix']);ff.converged=True
            else:
                fm,ff=solve([coords[i] for i in inds],OUT/f'{f['id']}-{name}.log',charge=charge)
            fd=ff.make_rdm1();F=np.zeros(len(grid))
            for i in range(0,len(grid),10000):
                a=fm.eval_gto('GTOval_sph',grid[i:i+10000]);F[i:i+len(a)]=np.einsum('pi,ij,pj->p',a,fd,a)
            count=quadrature(fm,fd)
            assert abs(count-fm.nelectron)<5e-4,(name,count)
            fragment_fields.append(F);fragments.append((fm,ff))
            np.savez_compressed(OUT/f'{f["id"]}-{name}-scf.npz',mo_coeff=ff.mo_coeff,mo_occ=ff.mo_occ,mo_energy=ff.mo_energy,
                                overlap=fm.intor('int1e_ovlp'),density_matrix=fd,coordinates=fm.atom_coords()*BOHR)
            fragment_meta.append({'id':name,'atomIndices':inds,'charge':charge,'multiplicity':1,'scfConverged':bool(ff.converged),
                                  'electronCount':fm.nelectron,'quadratureElectronCount':count,'energyHartree':float(ff.e_tot)})
            if fm.stdout is not __import__('sys').stdout:fm.stdout.close()
        tracking=[]
        if previous is None:
            # Initial occupied canonical orbital chosen by overlap with the incoming
            # chloride occupied 3px-like orbital, not by canonical index alone.
            fm,ff=fragments[0]
            px=[i for i,s in enumerate(fm.ao_labels()) if '3px' in s]
            assert len(px)==1
            donor=int(max(np.where(ff.mo_occ>0)[0],key=lambda j:abs(ff.mo_coeff[px[0],j])))
            overlap=ff.mo_coeff[:,donor]@gto.intor_cross('int1e_ovlp',fm,mol)@C
            occupied=int(max(np.where(occ>0)[0],key=lambda j:abs(overlap[j])))
            fm,ff=fragments[1]
            # Same-sign Cartesian px coefficients have opposite signs in the
            # C--Cl internuclear region: a stated sigma-antibonding AO trial.
            labels=fm.ao_labels();trial=np.zeros(fm.nao)
            for i,label in enumerate(labels):
                if '0 C 2px' in label or '1 Cl 3px' in label:trial[i]=1.
            trial/=np.sqrt(trial@fm.intor('int1e_ovlp')@trial)
            weights=trial@fm.intor('int1e_ovlp')@ff.mo_coeff
            lumo=int(max(np.where(ff.mo_occ==0)[0],key=lambda j:abs(weights[j])))
            overlapv=ff.mo_coeff[:,lumo]@gto.intor_cross('int1e_ovlp',fm,mol)@C
            virtual=int(max(np.where(occ==0)[0],key=lambda j:abs(overlapv[j])))
            indices=[occupied,virtual]
            for j in indices:
                pos=np.argmax(abs(C[:,j]));C[:,j]*=1 if C[pos,j]>=0 else -1
            result['initialSelection']={'occupiedIndex':occupied+1,'incomingFragmentOrbitalIndex':donor+1,
                'incomingProjection':float(abs(overlap[occupied])),'virtualIndex':virtual+1,'substrateVirtualIndex':lumo+1,'substrateTrialProjection':float(abs(weights[lumo])),
                'virtualSelection':'Fragment virtual with maximal normalized (C 2px + Cl_out 3px) AO-trial projection, then projected onto full-complex virtual MOs. Not assumed to be the LUMO.',
                'substrateProjection':float(abs(overlapv[virtual])),
                'identity':'Projected selection of full-complex canonical MOs. These are NOT fragment-localized donor/acceptor surfaces.'}
        else:
            pm,pc,pi=previous;cross=pc.T@gto.intor_cross('int1e_ovlp',pm,mol)@C;assignment={}
            for block in [np.where(occ>0)[0],np.where(occ==0)[0]]:
                rows,cols=linear_sum_assignment(-abs(cross[np.ix_(block,block)]))
                assignment.update({int(block[a]):int(block[b]) for a,b in zip(rows,cols)})
            indices=[assignment[j] for j in pi]
            for old,new in zip(pi,indices):
                raw=float(cross[old,new]);C[:,new]*=1 if raw>=0 else -1
                best=float(np.max(np.delete(abs(cross[old]),new)))
                tracking.append({'previousIndex':old+1,'index':new+1,'signedOverlapBeforeAlignment':raw,
                                 'alignedOverlap':abs(raw),'nextCandidate':best,'ambiguous':abs(raw)<.7 or abs(raw)<=best})
        previous=mol,C.copy(),indices
        rho=np.zeros(len(grid));mo=[np.zeros(len(grid)),np.zeros(len(grid))]
        for i in range(0,len(grid),10000):
            ao=mol.eval_gto('GTOval_sph',grid[i:i+10000]);rho[i:i+len(ao)]=np.einsum('pi,ij,pj->p',ao,dm,ao)
            for j,index in enumerate(indices):mo[j][i:i+len(ao)]=ao@C[:,index]
        count=quadrature(mol,dm);assert abs(count-44)<5e-4,(f['id'],count)
        assert rho.min()>-1e-10
        if reference is None:reference=rho.copy()
        fields={'total':rho.reshape(N),'difference':(rho-reference).reshape(N),
                'deformation':(rho-fragment_fields[0]-fragment_fields[1]).reshape(N),
                'occupied':mo[0].reshape(N),'virtual':mo[1].reshape(N)}
        np.savez_compressed(OUT/f'{f["id"]}-fields.npz',**{key:v.astype('float32') for key,v in fields.items()},origin_bohr=ORIGIN,spacing_bohr=STEP)
        np.savez_compressed(OUT/f'{f["id"]}-tracked.npz',mo_coeff=C,indices=indices)
        local={**f,'trackingProtocol':2,'sourceWavefunctionSha256':source_hash,'quadratureElectronCount':count,'uniformGridElectronEstimate':float(rho.sum()*STEP**3),
               'normalizationNote':'AO-metric count and independent level-5 Becke quadrature are normalization checks. Uniform display grid under-resolves nuclear cores; its integral is reported, never rescaled.',
               'fragments':fragment_meta,'tracking':tracking,'orbitals':[{'index':j+1,'energyHartree':float(wf['mo_energy'][j]),'occupation':int(occ[j])} for j in indices],
               'fieldFile':f'reaction-lab/{f["id"]}-fields.npz','meshFile':f'reaction-lab/{f["id"]}-meshes.json'}
        meshes={key:[surfaces(field,level) for level in LEVELS[key]] for key,field in fields.items()}
        (OUT/f'{f["id"]}-meshes.json').write_text(json.dumps(meshes,separators=(',',':')))
        result['frames'].append(local)
        (OUT/'sn2.json').write_text(json.dumps(result,indent=2))
        print(f['id'],'density',count,'uniform',local['uniformGridElectronEstimate'],'MOs',indices,'tracking',tracking,flush=True)
    (OUT/'sn2.json').write_text(json.dumps(result,indent=2))
    for name in ['compute_sn2.py','fields_sn2.py']:
        shutil.copy2(Path(__file__).parent/name,OUT/name)

if __name__=='__main__':main()
