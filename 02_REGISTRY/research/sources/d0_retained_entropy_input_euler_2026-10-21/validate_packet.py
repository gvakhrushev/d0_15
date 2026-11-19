#!/usr/bin/env python3
"""Read-only replay of the narrow new checker; --record writes validation explicitly."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, platform, subprocess, sys, tempfile
import numpy as np
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record',action='store_true');args=parser.parse_args()
    here=Path(__file__).resolve().parent; checker=here/'check_retained_input.py'
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    runs=[]
    for flags in [[],['-O']]:
        result=subprocess.run([sys.executable,*flags,str(checker)],capture_output=True,env=env,timeout=150)
        if result.returncode: raise RuntimeError(result.stderr.decode())
        data=json.loads(result.stdout)
        expected=(here/('RESULT_OPTIMIZED.json' if flags else 'RESULT.json')).read_bytes()
        if result.stdout!=expected: raise RuntimeError('frozen checker output mismatch')
        runs.append({'mode':'optimized' if flags else 'normal','status':data['status'],
                     'checks':data['check_count'],'stdout_sha256':hashlib.sha256(result.stdout).hexdigest()})
    raw=checker.read_text(); mutants=[]
    changes=[
      ('omit_paid_initial_boundary',"y = f['Y']-herm(apply(adj(t),f['Y']))", "y = np.zeros_like(f['Y'])"),
      ('wrong_entropy_gradient_sign',"grad = h['Y']+partial_out", "grad = h['Y']-partial_out"),
      ('collapse_retained_horizon',"t, dt = power_jet(f['T'],f['dT'],n)","t, dt = power_jet(f['T'],f['dT'],1)"),
      ('erase_finite_entropy_orbit_source',"jc=h['Y']@c+(back@c.reshape(-1)).reshape(c.shape)/ELL", "jc=h['Y']@c"),
    ]
    def module(path, name):
        spec=importlib.util.spec_from_file_location(name,path)
        obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
    base=module(checker,'base_checker')
    native=base.load_native();f=base.field(native,1/9)
    h2=base.horizon(f,2);h64=base.horizon(f,64)
    yy,u=np.linalg.eigh(f['Y']);c=u@np.diag(np.sqrt([3/32]*8+[1/32]*8))
    rho=c@base.adj(c)
    rng=np.random.default_rng(25);x=base.herm(rng.normal(size=(16,16))+1j*rng.normal(size=(16,16)))
    x-=base.tr(x)*np.eye(16)/16;x/=np.linalg.norm(x)
    step=2e-5
    with tempfile.TemporaryDirectory(prefix='d0-input-mutants-') as td:
        tmp=Path(td)
        for index,(name,old,new) in enumerate(changes):
            if raw.count(old)!=1: raise RuntimeError('mutation anchor not unique: '+name)
            p=tmp/(name+'.py');p.write_text(raw.replace(old,new))
            mutant=module(p,'mutant_'+str(index))
            if index==0:
                mh=mutant.horizon(f,2)
                error=abs(base.tr(rho@mh['Y'])-base.tr(rho@h2['Y']))
                rejected=error>1e-6
                reason='actual two-round paid boundary omitted'
            elif index==1:
                _,grad,_=mutant.free_value_gradient(h64,rho)
                fd=(mutant.free_value_gradient(h64,rho+step*x)[0]-mutant.free_value_gradient(h64,rho-step*x)[0])/(2*step)
                error=abs(fd-base.tr(grad@x));rejected=error>1e-5
                reason='full matrix entropy gradient disagrees with its value differential'
            elif index==2:
                mh=mutant.horizon(f,2)
                error=float(np.linalg.norm(mh['T']-h2['T']));rejected=error>1e-5
                reason='chronological two-round map collapsed to one round'
            else:
                _,a,_=base.orbit_value_gradient(h64,c)
                generator=a/np.linalg.norm(a)
                from scipy.linalg import expm
                plus=expm(step*generator)@c;minus=expm(-step*generator)@c
                fd=(mutant.orbit_value_gradient(h64,plus)[0]-mutant.orbit_value_gradient(h64,minus)[0])/(2*step)
                _,bad,_=mutant.orbit_value_gradient(h64,c)
                error=abs(fd-base.tr(base.adj(bad)@generator));rejected=error>1e-5
                reason='finite retained entropy source is missing on the protected-RIGHT orbit'
            if not rejected:raise RuntimeError('undetected mutation '+name)
            mutants.append({'name':name,'rejected':True,'decisive_error':float(error),'property':reason})
    import numpy, scipy, sympy
    out={'status':'PASS','read_only_expected_outputs':True,'checker_sha256':sha(checker),
         'normal_and_optimized_byte_identical':runs[0]['stdout_sha256']==runs[1]['stdout_sha256'],
         'replays':runs,'mutations':mutants,
         'environment':{'python':platform.python_version(),'numpy':numpy.__version__,
                        'scipy':scipy.__version__,'sympy':sympy.__version__},
         'proof_sha256':sha(here/'PROOF.md'),
         'scope':{'new_checks_only':True,'independent_agent_review':False,
                  'interval_certified_numerical_minima':False,'fresh_Lean':False,'repository_wide_CI':False,
                  'physical_Book03_Info_selected':False,'full_spatial42_root':False,'GR_closed':False}}
    encoded=json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.record:(here/'VALIDATION.json').write_text(encoded)
    sys.stdout.write(encoded)

if __name__=='__main__':main()
