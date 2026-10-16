#!/usr/bin/env python3
"""Run real mathematical mutations; bypass hash checks for those mutations."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
ENV={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
MUTATIONS=[
 ('omit_return_child','[K1*x for x in A]','[K0*x for x in A]','full_AF_restriction_A_0'),
 ('wrong_AF_restriction','return X[:a,:a] + W, X[a:,a:]','return X[:a,:a] - W, X[a:,a:]','full_AF_restriction_A_0'),
 ('forget_moving_preparation','+ amps[i]*drho*amps[j].H','+ 0*amps[i]*drho*amps[j].H','joint_data_basis_Ward_A_1'),
 ('incorrect_PF_weight','hFN,hWN=FN/(p*t),WN/(p*p*t)','hFN,hWN=FN/t,WN/(p*p*t)','native_PF_martingale_A_0'),
 ('erase_return_cost','else 2 for b in word','else 1 for b in word','cost_depth_pending_0'),
 ('flip_information_source','source=-iv.mpf(4)/5','source=iv.mpf(4)/5','strict_information_source'),
 ('erase_information_hessian','hessian=iv.mpf(16)/15','hessian=iv.mpf(0)/15','strict_information_hessian'),
]
def main():
    text=(HERE/'verify.py').read_text();reports=[]
    for name,old,new,gate in MUTATIONS:
        if text.count(old)!=1:raise RuntimeError('mutation anchor '+name)
        with TemporaryDirectory(prefix='d0-cost-info-') as td:
            path=Path(td)/'verify.py';path.write_text(text.replace(old,new))
            r=subprocess.run([sys.executable,'-O',str(path),'--math-only'],env=ENV,capture_output=True,text=True,timeout=120)
            if r.returncode==0 or gate not in r.stderr:
                raise AssertionError((name,'expected mathematical gate '+gate,r.returncode,r.stderr[-1200:]))
            reports.append({'name':name,'rejected_at':gate})
    with TemporaryDirectory(prefix='d0-cost-info-scope-') as td:
        dest=Path(td)
        for name in ('verify.py','RESULT.md','receipt.json'):(dest/name).write_bytes((HERE/name).read_bytes())
        obj=json.loads((dest/'receipt.json').read_text());obj['scope']['M1_forcing_of_complete_physical_action']=True
        (dest/'receipt.json').write_text(json.dumps(obj))
        r=subprocess.run([sys.executable,'-O',str(dest/'verify.py')],env=ENV,capture_output=True,text=True,timeout=120)
        if r.returncode==0 or 'IMMUTABLE_RECEIPT_MISMATCH' not in r.stderr:raise AssertionError('false physical-action receipt accepted')
    print(json.dumps({'status':'PASS','executed_mathematical_mutations':reports,'false_physical_action_receipt_rejected':True},sort_keys=True))
if __name__=='__main__':main()
