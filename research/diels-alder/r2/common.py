"""Fresh r2 calculations; all published r1 scientific files are read-only."""
from pathlib import Path
import os,sys,json,hashlib,zipfile
import numpy as np
from pyscf import gto,dft,lib

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'dist/reaction-lab/diels-alder'
OUT=Path(os.environ.get('OCHEM_R2_OUTPUT',str(BASE/'r2/restart-20261022')))
OUT.mkdir(parents=True,exist_ok=True)
BOHR=lib.param.BOHR
lib.num_threads(int(os.environ.get('OCHEM_THREADS','3')))
try:lib.current_memory()
except FileNotFoundError:lib.current_memory=lambda:(0,0)

def write(path,data):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 temp=path.with_name(path.name+'.pending');temp.write_text(json.dumps(data,indent=2)+'\n');temp.replace(path)

def save_npz(path,**data):
 path=Path(path);temp=path.with_name(path.name+'.pending')
 with temp.open('wb') as h:np.savez_compressed(h,**data)
 temp.replace(path)

def record(name='ts'):return json.loads((BASE/(name+'.json')).read_text())

def solve(x_bohr,log,dm=None,grid=3,basis='6-31g(d)',elements=None):
 elements=elements or [a['element'] for a in record()['atoms']]
 m=gto.M(atom=list(zip(elements,x_bohr)),unit='Bohr',basis=basis,charge=0,spin=0,max_memory=1200,verbose=4,output=str(log))
 f=dft.RKS(m);f.xc='b3lyp';f.grids.level=grid;f.conv_tol=1e-10;f.conv_tol_grad=1e-6;f.max_cycle=120
 f.kernel(dm0=dm)
 if not f.converged:raise RuntimeError('SCF did not converge')
 return m,f

def archive(folder,pattern,name):
 files=sorted(p for p in folder.glob(pattern) if p.suffix in ['.json','.log','.npz'])
 temp=folder/(name+'.'+str(os.getpid())+'.pending')
 with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
  for p in files:z.write(p,p.name)
 with zipfile.ZipFile(temp) as z:assert z.testzip() is None and len(z.namelist())==len(files)
 temp.replace(folder/name)
