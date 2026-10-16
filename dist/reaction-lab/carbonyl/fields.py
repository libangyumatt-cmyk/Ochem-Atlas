"""Actual AO-evaluated densities/amplitudes on one fixed Cartesian grid.
Difference reference: addition-0. Deformation reference: same-geometry
Hnu- + neutral H2CO, own fragment bases, no ghosts. Never renormalized.
"""
from pathlib import Path
import json,hashlib,shutil,sys
import numpy as np
from scipy.optimize import linear_sum_assignment
from pyscf import gto,dft,lib
from skimage.measure import marching_cubes
from compute import ROOT,OUT,BASIS,BOHR,solve
lib.num_threads(1)
N=(91,71,101);ORIGIN=np.array([-9.,-7.,-7.]);STEP=.2
LEVELS={'total':[.02,.05,.1],'difference':[.001,.003,.008],'deformation':[.001,.003,.008],
        'donor':[.025,.04,.06],'pi':[.025,.04,.06],'pistar':[.025,.04,.06]}
def quadrature(mol,dm):
    grid=dft.gen_grid.Grids(mol);grid.level=5;grid.build();count=0.
    for i in range(0,len(grid.coords),10000):
        a=mol.eval_gto('GTOval_sph',grid.coords[i:i+10000]);count+=np.einsum('pi,ij,pj->p',a,dm,a)@grid.weights[i:i+10000]
    return float(count)
def surfaces(field,level):
    out={}
    for name,sign in [('positive',1),('negative',-1)]:
        if np.max(sign*field)<=level:out[name]=None;continue
        v,f,_,_=marching_cubes(np.asarray(field*sign,dtype=np.float32),level,allow_degenerate=False)
        out[name]=dict(vertices=np.round((v*STEP+ORIGIN)*BOHR,3).ravel().tolist(),faces=f.ravel().tolist(),triangleCount=len(f))
    return out
def main():
    meta=json.loads((OUT/'calculation.json').read_text());meta.update(grid=dict(shape=N,originBohr=ORIGIN.tolist(),spacingBohr=STEP,order='C order, z fastest',alignment=meta['atomMapping'],densityUnits='electron bohr^-3',orbitalUnits='bohr^-3/2',meshCoordinates='angstrom',fieldPrecision='float32, full float64 SCF coefficients retained'),levels=LEVELS,
      references=dict(difference='rho(current) minus rho(addition-0), on identical Cartesian points. Includes nuclear displacement; not a unique charge-transfer measure.',deformation='rho(complex) minus same-geometry Hnu− and neutral H2CO, each in its own RHF/6-31++G(d,p) basis, no ghosts. Fixed atom membership; not counterpoise-corrected EDA.',probability='Absolute square of one selected canonical spatial orbital, normalized to 1, without occupation factor.',signs='Teal positive / amber negative electron-number difference or orbital amplitude; never positive/negative electrical charge.'))
    grid=np.stack(np.meshgrid(*[ORIGIN[k]+STEP*np.arange(N[k]) for k in range(3)],indexing='ij'),axis=-1).reshape(-1,3)
    reference=None;states={};previous=None
    for f in meta['frames']:
        id=f['id'];a=[(x['element'],x['xyzAngstrom']) for x in f['atoms']];m=gto.M(atom=a,basis=BASIS,charge=-1,spin=0,verbose=0)
        wf=np.load(OUT/(id+'-scf.npz'));c=wf['mo_coeff'].copy();occ=wf['mo_occ'];dm=wf['density_matrix'];s=wf['overlap']
        fragments=[];fragment_density=[];fragment_meta=[]
        for name,inds,charge in [('hydride',[4],-1),('formaldehyde',[0,1,2,3],0)]:
            fm,ff=solve([a[i] for i in inds],OUT/(id+'-'+name+'.log'),charge=charge);fd=ff.make_rdm1();rho=np.zeros(len(grid))
            for i in range(0,len(grid),10000):
                ao=fm.eval_gto('GTOval_sph',grid[i:i+10000]);rho[i:i+len(ao)]=np.einsum('pi,ij,pj->p',ao,fd,ao)
            q=quadrature(fm,fd);assert abs(q-fm.nelectron)<5e-4
            _,_,si,se=ff.stability(internal=True,external=True,return_status=True)
            np.savez_compressed(OUT/(id+'-'+name+'-scf.npz'),mo_coeff=ff.mo_coeff,mo_occ=ff.mo_occ,mo_energy=ff.mo_energy,overlap=fm.intor('int1e_ovlp'),density_matrix=fd,coordinates=fm.atom_coords()*BOHR)
            fragment_meta.append(dict(id=name,atomIndices=inds,charge=charge,multiplicity=1,electronCount=fm.nelectron,scfConverged=bool(ff.converged),internalStable=bool(si),externalStable=bool(se),quadratureElectronCount=q,energyHartree=float(ff.e_tot)))
            fragments.append((fm,ff));fragment_density.append(rho);fm.stdout.close()
        tracking=[]
        if previous is None:
            fm,ff=fragments[0];ov=ff.mo_coeff[:,0]@gto.intor_cross('int1e_ovlp',fm,m)@c
            donor=int(max(np.where(occ>0)[0],key=lambda j:abs(ov[j])))
            fm,ff=fragments[1];labels=fm.ao_labels();pz=[i for i,label in enumerate(labels) if '2pz' in label and label.split()[1] in ['C','O']];assert len(pz)==2
            # Substrate lies essentially in xy at initial frame. Declared valence
            # pz trial: same-sign pi, opposite-sign pi*. Fragment MOs remain canonical.
            picks=[];initial=[]
            for role,sign,block in [('pi',1,ff.mo_occ>0),('pistar',-1,ff.mo_occ==0)]:
                trial=np.zeros(fm.nao);trial[pz[0]]=1;trial[pz[1]]=sign;ss=fm.intor('int1e_ovlp');trial/=np.sqrt(trial@ss@trial)
                w=trial@ss@ff.mo_coeff;j=int(max(np.where(block)[0],key=lambda j:abs(w[j])))
                ovf=ff.mo_coeff[:,j]@gto.intor_cross('int1e_ovlp',fm,m)@c
                target=int(max(np.where(occ>0 if role=='pi' else occ==0)[0],key=lambda j:abs(ovf[j])))
                picks.append(target);initial.append(dict(role=role,fragmentIndex=j+1,trialProjection=float(abs(w[j])),complexIndex=target+1,complexProjection=float(abs(ovf[target]))))
            indices=[donor,*picks];assert len(set(indices))==3
            for j in indices:c[:,j]*=1 if c[np.argmax(abs(c[:,j])),j]>=0 else -1
            meta['initialSelection']=dict(donorComplexIndex=donor+1,hydride1sProjection=float(abs(ov[donor])),carbonylSelections=initial,protocol='Project hydride occupied 1s and neutral formaldehyde occupied pi / virtual pi* canonical MOs onto full-complex occupied / virtual spaces. Fragment pi references maximize normalized C2pz + O2pz (occupied) or C2pz - O2pz (virtual) AO-trial overlap. These full-complex canonical orbitals are not localized donor/acceptor orbitals.')
        else:
            parent='addition-2' if f['group']=='angles' else previous
            pm,pc,pi=states[parent];cross=pc.T@gto.intor_cross('int1e_ovlp',pm,m)@c;assign={}
            for block in [np.where(occ>0)[0],np.where(occ==0)[0]]:
                rows,cols=linear_sum_assignment(-abs(cross[np.ix_(block,block)]));assign.update({int(block[x]):int(block[y]) for x,y in zip(rows,cols)})
            indices=[assign[j] for j in pi]
            for role,old,new in zip(['donor','pi','pistar'],pi,indices):
                raw=float(cross[old,new]);c[:,new]*=1 if raw>=0 else -1;block=np.where(occ>0 if occ[new]>0 else occ==0)[0]
                nextbest=max([abs(cross[old,j]) for j in block if j!=new],default=0)
                tracking.append(dict(role=role,parentFrame=parent,previousIndex=old+1,index=new+1,signedOverlapBeforeAlignment=raw,alignedOverlap=abs(raw),nextCandidate=float(nextbest),ambiguous=bool(abs(raw)<.7 or abs(raw)<=nextbest)))
        states[id]=(m,c.copy(),indices);previous=id
        rho=np.zeros(len(grid));amplitude=np.zeros((len(grid),3))
        for i in range(0,len(grid),10000):
            ao=m.eval_gto('GTOval_sph',grid[i:i+10000]);rho[i:i+len(ao)]=np.einsum('pi,ij,pj->p',ao,dm,ao);amplitude[i:i+len(ao)]=ao@c[:,indices]
        q=quadrature(m,dm);assert abs(q-18)<5e-4 and rho.min()>-1e-10
        if reference is None:reference=rho.copy()
        fields=dict(total=rho.reshape(N),difference=(rho-reference).reshape(N),deformation=(rho-sum(fragment_density)).reshape(N))
        fields.update({key:amplitude[:,i].reshape(N) for i,key in enumerate(['donor','pi','pistar'])})
        np.savez_compressed(OUT/(id+'-fields.npz'),**{k:v.astype('float32') for k,v in fields.items()},origin_bohr=ORIGIN,spacing_bohr=STEP)
        np.savez_compressed(OUT/(id+'-tracked.npz'),mo_coeff=c,indices=indices)
        boundary={k:float(max(abs(v[0]).max(),abs(v[-1]).max(),abs(v[:,0]).max(),abs(v[:,-1]).max(),abs(v[:,:,0]).max(),abs(v[:,:,-1]).max())) for k,v in fields.items()}
        assert all(boundary[k]<min(LEVELS[k]) for k in fields),boundary
        f['maximumAbsoluteBoundaryField']=boundary
        mesh={k:[surfaces(v,level) for level in LEVELS[k]] for k,v in fields.items()};(OUT/(id+'-meshes.json')).write_text(json.dumps(mesh,separators=(',',':')))
        f.update(quadratureElectronCount=q,uniformGridElectronEstimate=float(rho.sum()*STEP**3),fragments=fragment_meta,tracking=tracking,
          sourceWavefunctionSha256=hashlib.sha256((OUT/(id+'-scf.npz')).read_bytes()).hexdigest(),orbitals=[dict(id=role,index=j+1,occupation=int(occ[j]),energyHartree=float(wf['mo_energy'][j])) for role,j in zip(['donor','pi','pistar'],indices)],meshFile=f'reaction-lab/carbonyl/{id}-meshes.json',fieldFile=f'reaction-lab/carbonyl/{id}-fields.npz')
        print(id,'integral',q,'uniform',f['uniformGridElectronEstimate'],'MOs',indices,'tracking',tracking,flush=True)
    (OUT/'carbonyl.json').write_text(json.dumps(meta,indent=2))
    for name in ['compute.py','fields.py']:shutil.copy2(Path(__file__).parent/name,OUT/name)
if __name__=='__main__':main()
