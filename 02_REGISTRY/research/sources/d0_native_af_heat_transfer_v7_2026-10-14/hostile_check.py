#!/usr/bin/env python3
"""Execute modified programs; mathematical rejection must precede hash rejection."""
import argparse,json,os,pathlib,shutil,subprocess,sys,tempfile
HERE=pathlib.Path(__file__).resolve().parent
MUTATIONS=[
 ('lose_right_multiplicity','return ((a+b)*X+a*W)/a, (s.Rational(a+b,b))*Y','return (X+W)/2,Y','full_trace_conservation_0'),
 ('one_Bratteli_pass','M**(2*r)*s.Matrix([A,B])','M**r*s.Matrix([A,B])','two_sided_multiplicity_0_1'),
 ('erase_native_complement','Y=P+q*(Id-P)','Y=P','native_mismatch_full_Gibbs_factor_0'),
 ('wrong_archive_source_sign','(-s.Rational(3,7)+cov)-cov+s.Rational(3,7)','(-s.Rational(3,7)+cov)+cov+s.Rational(3,7)','full_price_restored_by_archive_source'),
 ('wrong_PF_rate','p**(2*n+2*r+3)/D','p**(2*n+r+3)/D','exact_PF_trace_error_0_1'),
]

def run(selected=None):
    original=(HERE/'af_heat_check.py').read_text();rows=[]
    cases=[x for x in MUTATIONS if selected in (None,x[0])]
    for name,old,new,expected in cases:
        if original.count(old)!=1:raise AssertionError(('unique mutation anchor',name))
        with tempfile.TemporaryDirectory(prefix='d0-v7-mutant-') as t:
            root=pathlib.Path(t)
            for f in ('NATIVE_AF_HEAT_TRANSFER_RU.md','af_heat_receipt.json'):shutil.copy2(HERE/f,root/f)
            (root/'af_heat_check.py').write_text(original.replace(old,new))
            result=subprocess.run([sys.executable,'-O',str(root/'af_heat_check.py')],text=True,capture_output=True,timeout=180,env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})
            if result.returncode==0 or expected not in result.stderr:raise AssertionError((name,result.stdout,result.stderr))
            rows.append({'mutation':name,'rejected_by':expected})
    if selected in (None,'false_GR_receipt'):
        with tempfile.TemporaryDirectory(prefix='d0-v7-scope-') as t:
            root=pathlib.Path(t)
            for f in ('af_heat_check.py','NATIVE_AF_HEAT_TRANSFER_RU.md'):shutil.copy2(HERE/f,root/f)
            r=json.loads((HERE/'af_heat_receipt.json').read_text());r['scope']['physical_GR_closed']=True
            (root/'af_heat_receipt.json').write_text(json.dumps(r))
            result=subprocess.run([sys.executable,'-O',str(root/'af_heat_check.py')],text=True,capture_output=True,timeout=180,env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})
            if result.returncode==0 or 'IMMUTABLE_RECEIPT_MISMATCH' not in result.stderr:raise AssertionError('false GR receipt accepted')
            rows.append({'mutation':'false_GR_receipt','rejected_by':'IMMUTABLE_RECEIPT_MISMATCH'})
    return {'status':'PASS_EXECUTED_MUTANTS','results':rows,'physical_GR_closed':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--only');args=p.parse_args()
    data=run(args.only)
    path=HERE/'hostile_receipt.json'
    if args.write:path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    elif not args.only and data!=json.loads(path.read_text()):raise AssertionError('HOSTILE_RECEIPT_MISMATCH')
    print(json.dumps(data,indent=2,sort_keys=True))
