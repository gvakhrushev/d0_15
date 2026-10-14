#!/usr/bin/env python3
"""Execute altered mathematics in fresh directories before receipt checking."""
from pathlib import Path
import os,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
original=(HERE/'verify.py').read_text()
changes=[
 ('wrong_loop_sign','V=-(2*P-I)*(2*R-I)','V=(2*P-I)*(2*R-I)','complete_loop_defect'),
 ('difference_not_sum_square','K=(P+R-I)**2','K=(P-R)**2','complete_loop_defect'),
 ('wrong_golden_average','B=p*I+(p*p/2)*(V+V.T)','B=p*I+(p*p/3)*(V+V.T)','same_golden_survival_full_space'),
 ('freeze_archive_frame_jet','Qd=Qd+T*Q-Q*T','Qd=Qd','REJECT_frozen_archive_frame_jet'),
 ('zero_cutoff_weight','extra=126976*gamma','extra=0*gamma','interval_cutoff_mass_strictly_positive'),
 ('drop_reference_multiplicity','def eqs(x,mult=2048):','def eqs(x,mult=16):','strict_contraction'),
 ('freeze_coefficient_jet','Cd=s.diag(0,s.Rational(3,5),0)','Cd=s.zeros(3)','full_Q_jet_is_tangent'),
]
results=[]
for name,before,after,expected in changes:
    if original.count(before)!=1:raise AssertionError(('MUTATION_ANCHOR',name))
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td);(dst/'verify.py').write_text(original.replace(before,after))
        (dst/'RESULT.md').write_bytes((HERE/'RESULT.md').read_bytes())
        proc=subprocess.run([sys.executable,'-O',str(dst/'verify.py'),'--write'],capture_output=True,text=True,
                            env={**os.environ,'OPENBLAS_NUM_THREADS':'1'},timeout=40)
        if proc.returncode==0 or expected not in proc.stderr:
            raise AssertionError((name,proc.returncode,proc.stdout,proc.stderr[-1600:]))
        results.append({'mutation':name,'rejected_at':expected})
with tempfile.TemporaryDirectory() as td:
    dst=Path(td);(dst/'verify.py').write_bytes((HERE/'verify.py').read_bytes())
    (dst/'RESULT.md').write_bytes((HERE/'RESULT.md').read_bytes())
    r=json.loads((HERE/'receipt.json').read_text());r['GR_closed']=True
    (dst/'receipt.json').write_text(json.dumps(r))
    proc=subprocess.run([sys.executable,'-O',str(dst/'verify.py')],capture_output=True,text=True,timeout=40)
    if proc.returncode==0 or 'IMMUTABLE_RECEIPT_MISMATCH' not in proc.stderr:raise AssertionError('FALSE_GR_RECEIPT')
    results.append({'mutation':'false_GR_receipt','rejected_at':'IMMUTABLE_RECEIPT_MISMATCH'})
print(json.dumps({'status':'PASS','executed_math_mutations':len(changes),'rejections':results},indent=2))
