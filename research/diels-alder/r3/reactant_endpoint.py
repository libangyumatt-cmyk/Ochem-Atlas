"""Independent reactant endpoint check after actual backward-driver convergence."""
from pathlib import Path
import os,sys
root=Path(__file__).resolve().parents[3]
os.environ['OCHEM_R2_OUTPUT']=os.environ.get('OCHEM_R3_BACKWARD_OUTPUT',str(root/'dist/reaction-lab/diels-alder/r3/backward-attempt1'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r2'))
from common import OUT
from optimizer_state import install
from endpoints import main
if __name__=='__main__':
 install(OUT/'endpoints/backward');sys.argv=[sys.argv[0],'backward'];main()
