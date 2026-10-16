"""Execute altered programs and require a mathematical AssertionError (not syntax errors)."""
from __future__ import annotations
import json,os,subprocess,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
CASES=[
('wrong_golden_gain','derive_operations.py','    gamma=p**3','    gamma=p**2'),
('missing_echo_inverse','derive_operations.py','s.kronecker_product(G.T,I)*s.diag(V,U)','s.kronecker_product(G,I)*s.diag(V,U)'),
('omit_first_distinguishing_event','derive_operations.py','    actual=fail(tau)','    actual=tau'),
('drop_count_multiplicity','derive_operations.py','s.binomial(T,k)*E**k','E**k'),
('drop_curvature_in_D_square','full_curved_word_check.py','Delta=D@D','Delta=d.T@d+d@d.T'),
('wrong_adjoint_word_sign','full_curved_word_check.py','coef.extend([1,1,1,-1,-2])','coef.extend([1,1,1,1,-2])'),
('freeze_actual_link_derivative','full_curved_word_check.py','dD=dd+dd.T','dD=np.zeros_like(dd)'),
('reverse_quadratic_reconstruction_sign','full_curved_word_check.py','rec-=coef[j]*coef[k]*K','rec+=coef[j]*coef[k]*K'),
]
records=[]
for name,fn,old,new in CASES:
 original=(R/'src'/fn).read_text()
 if old not in original:raise AssertionError(('MUTATION_ANCHOR_MISSING',name))
 with tempfile.TemporaryDirectory(prefix='d0_v2_mutant_')as td:
  root=Path(td);(root/'src').mkdir();(root/'results').mkdir()
  dest=root/'src'/fn;dest.write_text(original.replace(old,new,1))
  result=subprocess.run([sys.executable,'-O',str(dest)],capture_output=True,text=True,
       env={**os.environ,'OPENBLAS_NUM_THREADS':'1'},timeout=35)
  if result.returncode==0 or 'AssertionError'not in result.stderr:
   raise AssertionError(('MUTANT_DID_NOT_FAIL_MATHEMATICALLY',name,result.stdout,result.stderr))
  tail=result.stderr.splitlines()[-1]
  records.append({'name':name,'status':'REJECTED_AS_EXPECTED','returncode':result.returncode,'last_error':tail})
  print('REJECTED',name,tail)
(R/'results/actual_code_mutations.json').write_text(json.dumps({'status':'PASS','executed_mutants':records},indent=2)+'\n')
