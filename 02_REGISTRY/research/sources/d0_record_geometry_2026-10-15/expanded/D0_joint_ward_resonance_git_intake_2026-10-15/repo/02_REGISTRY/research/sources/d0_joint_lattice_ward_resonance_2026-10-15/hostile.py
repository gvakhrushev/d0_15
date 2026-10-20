#!/usr/bin/env python3
"""Execute actual formula mutants, not only changed manifest checks."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,json,os,argparse
import linear as owned_input
HERE=Path(__file__).resolve().parent
CASES=[
 ('wrong_forward_coframe','d=s.Matrix([1/x - 1 for x in z])','d=s.Matrix([x - 1 for x in z])'),
 ('wrong_compensation_sign','links=[(x-1)*omega for x in z]','links=[-(x-1)*omega for x in z]'),
 ('wrong_offdiagonal_Gram','V[a,b]=V[b,a]=1','V[a,b]=V[b,a]=(1 if a==b else s.Rational(1,2))'),
 ('wrong_dual_symbol','Cd=mixed([1/x for x in z]).T','Cd=mixed(z).T'),
 ('kernel_not_retained_in_inverse','R=simplify((J+P).inv()-P)','R=simplify((J+P).inv()+P)'),
 ('wrong_phase_second_derivative','DD[i,j][aa,bb]-=powers[i]*powers[j]*val','DD[i,j][aa,bb]+=powers[i]*powers[j]*val'),
 ('missing_Schur_term','-U[i].conjugate().T*R*U[j]','+0*U[i].conjugate().T*R*U[j]'),
]
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--write",action="store_true");args=ap.parse_args()
 report=[]
 for name,old,new in CASES:
  with tempfile.TemporaryDirectory(prefix='d0_joint_ward_mutant_') as t:
   root=Path(t);src=root/HERE.name;src.mkdir()
   oldsrc=owned_input.UPSTREAM.parent
   dest=root/oldsrc.name;dest.mkdir();shutil.copy2(oldsrc/'symbol.py',dest/'symbol.py')
   shutil.copy2(HERE/'verify.py',src/'verify.py')
   text=(HERE/'linear.py').read_text()
   if text.count(old)!=1:raise RuntimeError('mutation anchor is not unique: '+name)
   (src/'linear.py').write_text(text.replace(old,new))
   proc=subprocess.run([sys.executable,str(src/'verify.py'),'--mathematics-only'],cwd=src,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
   if proc.returncode==0 or 'AssertionError' not in proc.stdout:raise AssertionError('mutation did not fail on mathematics: '+name+'\n'+proc.stdout[-2000:])
   row={'name':name,'rejected':True,'returncode':proc.returncode,'last_line':proc.stdout.strip().splitlines()[-1]};report.append(row);print(row,flush=True)
 result={'status':'ALL_EXECUTED_MATHEMATICAL_MUTANTS_REJECTED','cases':report}
 if args.write:(HERE/'hostile_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
 elif result!=json.loads((HERE/'hostile_receipt.json').read_text()):raise AssertionError('HOSTILE_RECEIPT_CHANGED')
if __name__=='__main__':main()
