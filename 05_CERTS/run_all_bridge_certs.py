#!/usr/bin/env python3
import subprocess, pathlib, json, sys, time
here=pathlib.Path(__file__).resolve().parent
scripts=['vp_v1133_qft_rg_scheme_passports.py', 'vp_dusty_plasma_d0_mapping.py', 'vp_ligo_discovery_negative_control.py']
results=[]
for s in scripts:
    p=here/s
    if not p.exists():
        results.append({'script':s,'status':'MISSING'}); continue
    t=time.time(); proc=subprocess.run([sys.executable,str(p)],cwd=here,text=True,capture_output=True,timeout=90)
    out=proc.stdout.strip()
    results.append({'script':s,'returncode':proc.returncode,'last_stdout':out.splitlines()[-1:] if out else [],'stderr_tail':proc.stderr.strip().splitlines()[-2:],'seconds':round(time.time()-t,3),'status':'PASS' if proc.returncode==0 and 'PASS' in out else 'FAIL'})
pass_all=all(r.get('status')=='PASS' for r in results)
open(here/'run_all_bridge_certs_results.json','w').write(json.dumps({'pass':pass_all,'results':results},indent=2))
print('PASS_RUN_ALL_BRIDGE_CERTS' if pass_all else 'FAIL_RUN_ALL_BRIDGE_CERTS')
