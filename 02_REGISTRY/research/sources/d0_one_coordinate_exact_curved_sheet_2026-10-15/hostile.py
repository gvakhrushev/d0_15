#!/usr/bin/env python3
"""Execute actual operator mutations; do not reject them merely by file hash."""
import argparse,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).parent
MUTATIONS=[
 ('flip_native_star_sign','(0,1):((2,3),-1)','(0,1):((2,3),1)'),
 ('remove_inverse_edge_sign','direct=[1,z[r],-z[ss],-1]','direct=[1,z[r],z[ss],-1]'),
 ('wrong_shared_link_polarization','role[roles[j],roles[i]]-=inverse[i]*direct[j]/2','role[roles[j],roles[i]]+=inverse[i]*direct[j]/2'),
 ('invert_wrong_transpose','s.Integer(1)]).T','s.Integer(1)])'),
 ('wrong_scalar_resolvent','Q=14+z*z+z**-2','Q=12+z*z+z**-2'),
]
def main():
 pa=argparse.ArgumentParser();pa.add_argument('--write',type=Path);args=pa.parse_args();out=[]
 for name,old,new in MUTATIONS:
  with tempfile.TemporaryDirectory(prefix='d0-onecoord-hostile-') as d:
   d=Path(d)
   for f in ['algebra.py','verify.py','root_center.json']:shutil.copy(ROOT/f,d/f)
   text=(d/'algebra.py').read_text()
   if text.count(old)!=1:raise AssertionError('MUTATION_TARGET_NOT_UNIQUE: '+name)
   (d/'algebra.py').write_text(text.replace(old,new))
   p=subprocess.run([sys.executable,'-O',str(d/'verify.py'),'--algebra'],cwd=d,capture_output=True,text=True,timeout=50,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
   if p.returncode==0:raise AssertionError('MUTANT_SURVIVED: '+name)
   if 'AssertionError' not in p.stderr:raise AssertionError('NONMATHEMATICAL_MUTANT_FAILURE: '+name+'\n'+p.stderr)
   line=next(z for z in p.stderr.splitlines()[::-1] if 'AssertionError:' in z)
   out.append({'mutation':name,'rejected_by':line.split('AssertionError:',1)[1].strip()})
 result={'status':'PASS_EXECUTED_OPERATOR_MUTATIONS','results':out,'scope':'No interval-existence or full physical claim is obtained merely from rejecting mutants.'}
 print(json.dumps(result,indent=2))
 if args.write:args.write.write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
