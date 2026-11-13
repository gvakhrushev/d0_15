#!/usr/bin/env python3
"""Return explicit signed SO3 DAGs for private phases and actual archive tail.

Numerical search proposes words; independent dyadic certification is separate.
The target fixture is the actual60-call NPS, not a fitted geometric source.
"""
import importlib.util,json,sys,hashlib,time
from pathlib import Path
import mpmath as mp

HERE=Path(__file__).resolve().parent
source=HERE/'inputs/d0_so3_sk_compiler_20261026.py'
spec=importlib.util.spec_from_file_location('owned_private_sk',source)
sk=importlib.util.module_from_spec(spec);sys.modules[spec.name]=sk;spec.loader.exec_module(sk)
mp.mp.dps=100
started=time.monotonic()
compiler=sk.SKCompiler(dps=100,net_depth=10,pivots=128)
sk.meaningful_convention_checks(compiler)
p=(mp.sqrt(5)-1)/2
q=p*p+16*p**12
t=mp.exp(1j*624*mp.atan2(p,mp.sqrt(p)))
a=2*(1-mp.re(t));b=2*mp.re(t)-1
targets=[]
rounds=12
for branch,prob in enumerate((1-q,q)):
    eps=1-prob;z=mp.sqrt(prob)
    for _ in range(rounds):
        z=z*t*(t+a*eps);eps=eps*(b+a*eps)**2
    targets.append((f'phase_{branch}',mp.arg(z)))
targets.append(('archive_tail',mp.atan(p*p)))
reports=[]
for name,angle in targets:
    target=compiler.target_plane01(angle)
    for depth in range(8):
        word=compiler.compile(target,depth)
        report=compiler.numerical_report(name,target,word,depth)
        print(json.dumps({k:report[k] for k in ('name','depth','abstract_letter_length','SO3_operator_error_numerical')}),flush=True)
        if mp.mpf(report['SO3_operator_error_numerical'])<mp.mpf('1e-25'):break
    else:raise ArithmeticError('finite search did not reach target; no precision claim')
    reports.append(report)
bundle=compiler.bundle(reports)
bundle['fixture']={'nps_query':'Af=Ab=G_source^3, full original E0+36-call echo retained',
                   'q':'p^2+16*p^12','recovery_rounds':rounds,'stable_phase_multiplier':624}
bundle['search_seconds']=time.monotonic()-started
bundle['owning_compiler_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
(HERE/'CORRECTION_WORDS.json').write_text(json.dumps(bundle,indent=2)+'\n')
print(json.dumps({'status':'NUMERICAL_PROPOSALS_SAVED','nodes':len(bundle['nodes']),
                  'elapsed_seconds':bundle['search_seconds'],'certified':False}),flush=True)
