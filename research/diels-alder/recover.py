"""Recover metadata from retained completed SCF/Hessian without repeating Hessian."""
from compute import *
def recover(id,kind):
 w=np.load(OUT/(id+'-scf.npz'));xyz=w['coordinates'];elements=['C']*6+['H']*10 if len(xyz)==16 else (['C']*4+['H']*6 if len(xyz)==10 else ['C']*2+['H']*4)
 m=gto.M(atom=list(zip(elements,xyz)),basis=BASIS,verbose=0);return save(id,m,kind,reuse_hessian=True)
if __name__=='__main__':recover(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'Full Hessian computed; see validation')
