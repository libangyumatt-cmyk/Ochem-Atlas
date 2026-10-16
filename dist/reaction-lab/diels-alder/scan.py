"""Three relaxed double-distance constrained points, independent of TS verification.
Starting seed is explicitly not assumed stationary. Not an IRC.
"""
from compute import *
from study import single

def main():
 s=json.loads((OUT/'ts-seed.json').read_text());seed_a=[(x['element'],x['xyzAngstrom']) for x in s['atoms']];a=seed_a
 for id,r in [('pre-ts',2.5),('approach',3.0),('post-ts',1.9)]:
  if (OUT/('raw-'+id+'.json')).exists():continue
  con=OUT/(id+'-constraints.txt');con.write_text(f'$set\ndistance 1 5 {r}\ndistance 4 6 {r}\n$end\n');m,f=solve(seed_a if id=='post-ts' else a,OUT/(id+'-optimization.log'))
  opt=optimize(f,constraints=str(con),enforce=.1,convergence_cmax=1e-5,maxsteps=70,convergence_grms=8e-5,convergence_gmax=2e-4,verbose=0);single('raw-'+id,opt);a=[(opt.atom_symbol(i),v*BOHR) for i,v in enumerate(opt.atom_coords())]
if __name__=='__main__':main()
