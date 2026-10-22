"""Independent full-response endpoint relaxation and full analytic Hessian checks.
These are ordinary optimizations; they are not IRC continuation points.
"""
from common import *
from irc import FreshEngine
from geometric.molecule import Molecule
from geometric.optimize import run_optimizer
from pyscf.hessian import thermo

def verify(folder,x):
 m,f=solve(x/BOHR,folder/'verification.log');p=f.make_rdm1();s=m.intor('int1e_ovlp')
 grad=f.nuc_grad_method();grad.grid_response=True;g=grad.kernel()
 save_npz(folder/'scf-checkpoint.npz',coordinatesAngstrom=x,gradient=g,mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,density_matrix=p,overlap=s)
 write(folder/'progress.json',dict(stage='SCF/gradient complete; Hessian and determinant stability pending'))
 h=f.Hessian().kernel();vib=thermo.harmonic_analysis(m,h);freq=np.array([-abs(z.imag) if abs(z.imag)>1e-8 else z.real for z in vib['freq_wavenumber']])
 save_npz(folder/'wavefunction.npz',coordinatesAngstrom=x,gradient=g,hessian=h,frequenciesCm=freq,normal_modes=vib['norm_mode'],mo_coeff=f.mo_coeff,mo_occ=f.mo_occ,mo_energy=f.mo_energy,density_matrix=p,overlap=s)
 write(folder/'progress.json',dict(stage='Full analytic Hessian complete; determinant stability pending',lowestFrequencyCm=float(min(freq))))
 _,_,si,se=f.stability(internal=True,external=True,return_status=True)
 r=dict(energyHartree=float(f.e_tot),coordinatesAngstrom=x.tolist(),elements=[m.atom_symbol(i) for i in range(m.natm)],electronCount=float(np.einsum('ij,ji',p,s)),maxFullResponseGradientEhPerBohr=float(abs(g).max()),frequenciesCm=freq.tolist(),internalStable=bool(si),externalStable=bool(se),scfConverged=bool(f.converged),minimumVerified=bool(abs(g).max()<2e-4 and min(freq)>0 and si and se),hessianConvention='Full all-nuclear-coordinate analytic PySCF Hessian with default grid-response approximation. Not a full moving-grid-response Hessian; full-response gradients used for optimization and final forces.')
 write(folder/'verification.json',r);return r

def main():
 direction=sys.argv[1];assert direction in ['forward','backward']
 source=OUT/direction/'status.json';status=json.loads(source.read_text());assert status['complete'] and status['driverConverged']
 name=direction;displacement=0.
 if '--displace-mode' in sys.argv:
  displacement=float(sys.argv[sys.argv.index('--displace-mode')+1]);name+='-mode-'+str(displacement)
 folder=OUT/'endpoints'/name;folder.mkdir(parents=True,exist_ok=True)
 assert not (folder/'verification.json').exists(),'Existing endpoint retained.'
 x=np.array(status['finalCoordinatesAngstrom'])
 if displacement:
  w=np.load(OUT/'endpoints'/direction/'wavefunction.npz');x=w['coordinatesAngstrom'].copy();mode=w['normal_modes'][0];mode=mode/np.linalg.norm(mode);x+=displacement*mode
 write(folder/'input.json',dict(source=str(source.relative_to(ROOT)),sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),coordinatesAngstrom=x.tolist(),softModeDisplacementNormAngstrom=displacement,note='Separate endpoint relaxation, not IRC continuation; soft-mode displacement when stated is an initial guess, not an independently calculated IRC geometry.'))
 molecule=Molecule();molecule.elem=[a['element'] for a in record()['atoms']];molecule.xyzs=[x];molecule.comms=['Independent unconstrained endpoint relaxation'];molecule.build_topology()
 engine=FreshEngine(molecule,folder)
 options=dict(coordsys='dlc',trust=.05,tmax=.1,maxiter=80,convergence_energy=1e-8,convergence_grms=1e-5,convergence_gmax=3e-5,convergence_drms=.0003,convergence_dmax=.0005)
 write(folder/'options.json',options)
 try:
  final=run_optimizer(customengine=engine,input=str(BASE/'ts.xyz'),prefix=str(folder/'optimization'),**options)
  write(folder/'optimizer-status.json',dict(converged=True,finalCoordinatesAngstrom=final.xyzs[-1].tolist(),evaluations=engine.count))
  result=verify(folder,np.array(final.xyzs[-1]));print('ENDPOINT',name,result['minimumVerified'],min(result['frequenciesCm']),flush=True)
 except Exception as exc:
  write(folder/'failure.json',dict(error=type(exc).__name__+': '+str(exc),evaluations=engine.count));raise
 finally:archive(folder,'eval-*.*','evaluations.zip')

if __name__=='__main__':main()
