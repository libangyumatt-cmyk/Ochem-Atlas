"""Active-run pipeline: wait for one actual branch, then verify its endpoint."""
from common import *
import time,subprocess

def main():
 direction=sys.argv[1];assert direction in ['forward','backward']
 while True:
  status=json.loads((OUT/direction/'status.json').read_text())
  if status['complete']:break
  time.sleep(5)
 if not status['driverConverged']:raise RuntimeError(direction+' driver did not converge; original data retained')
 folder=OUT/'endpoints'/direction;folder.mkdir(parents=True,exist_ok=True)
 if (folder/'verification.json').exists():return
 with (folder/'driver-stdout.log').open('w') as log:
  result=subprocess.run([sys.executable,'-u',str(Path(__file__).with_name('endpoints.py')),direction],stdout=log,stderr=subprocess.STDOUT)
 if result.returncode:raise RuntimeError('Independent endpoint check failed; see retained stdout')

if __name__=='__main__':main()
