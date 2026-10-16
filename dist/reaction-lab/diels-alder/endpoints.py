"""Independent unconstrained reactant and cyclohexene optimizations."""
from compute import *
from rdkit import Chem
from rdkit.Chem import AllChem

def optimize_rd(rd,name):
 rd=Chem.AddHs(rd);AllChem.EmbedMolecule(rd,randomSeed=37);AllChem.MMFFOptimizeMolecule(rd);xyz=rd.GetConformer();a=[(at.GetSymbol(),tuple(xyz.GetAtomPosition(i))) for i,at in enumerate(rd.GetAtoms())]
 m,f=solve(a,OUT/(name+'-optimization.log'));opt=optimize(f,maxsteps=80,convergence_grms=8e-5,convergence_gmax=2e-4,verbose=0);return save(name,opt,'Unconstrained independently optimized endpoint; full Hessian checked')
def main():
 for name,smiles in [('reactant-ethylene','C=C'),('reactant-butadiene','C=CC=C')]:
  if (OUT/(name+'.json')).exists():continue
  _,_,r=optimize_rd(Chem.MolFromSmiles(smiles),name);assert r['maxNuclearGradientEhPerBohr']<2e-4 and min(r['frequenciesCm'])>20
 # Mapping agrees with TS carbons and RDKit AddHs hydrogen ordering.
 rw=Chem.RWMol()
 for _ in range(6):rw.AddAtom(Chem.Atom('C'))
 for i,j,order in [(0,1,1),(1,2,2),(2,3,1),(3,5,1),(5,4,1),(4,0,1)]:rw.AddBond(i,j,Chem.BondType.DOUBLE if order==2 else Chem.BondType.SINGLE)
 rd=rw.GetMol();Chem.SanitizeMol(rd)
 optimize_rd(rd,'product-raw')
if __name__=='__main__':main()
