"""Rotate the independent product minimum into the common lab frame,
then compute a fresh SCF, all nuclear gradients and the full Hessian.
The alignment target coordinates do not themselves imply TS verification.
"""
from compute import *
from study import aligned

def main():
 lib.num_threads(2)
 w=np.load(OUT/'ts-scf.npz');ref={'atoms':[dict(xyzAngstrom=x.tolist()) for x in w['coordinates']]}
 raw=json.loads((OUT/'product-raw.json').read_text());m=gto.M(atom=[(x['element'],x['xyzAngstrom']) for x in raw['atoms']],basis=BASIS,verbose=0)
 _,_,r=save('product',aligned(m,ref),'Aligned independent product minimum candidate')
 assert r['maxNuclearGradientEhPerBohr']<2e-4 and min(r['frequenciesCm'])>20
 r.update(geometryKind='Full-gradient and Hessian verified cyclohexene minimum',stationaryPointVerified=True);(OUT/'product.json').write_text(json.dumps(r,indent=2))
if __name__=='__main__':main()
