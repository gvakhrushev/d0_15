#!/usr/bin/env python3
import os, subprocess, pathlib, json, sys, time
here=pathlib.Path(__file__).resolve().parent
scripts=['vp_v1129_gauge_isolation.py','vp_v1132_gauge_matter_ward_anomaly.py','vp_v1133_high_gain_full_atlas.py','vp_archive_laplacian_rg_flow.py','vp_archive_seam_curvature_action.py','vp_archive_variational_field_equation.py']
results=[]
env=os.environ.copy()
env.setdefault('PYTHONIOENCODING','utf-8')
env.setdefault('PYTHONUTF8','1')
for s in scripts:
    p=here/s
    if not p.exists(): results.append({'script':s,'status':'MISSING'}); continue
    t=time.time(); proc=subprocess.run([sys.executable,str(p)],cwd=here,text=True,capture_output=True,timeout=90,env=env,encoding='utf-8',errors='replace')
    out=proc.stdout.strip()
    results.append({'script':s,'returncode':proc.returncode,'last_stdout':out.splitlines()[-1:] if out else [],'stderr_tail':proc.stderr.strip().splitlines()[-2:],'seconds':round(time.time()-t,3),'status':'PASS' if proc.returncode==0 and 'PASS' in out else 'FAIL'})
pass_all=all(r.get('status')=='PASS' for r in results)
open('run_all_core_certs_results.json','w',encoding='utf-8').write(json.dumps({'pass':pass_all,'results':results},indent=2,ensure_ascii=False))
print('PASS_RUN_ALL_CORE_CERTS' if pass_all else 'FAIL_RUN_ALL_CORE_CERTS')
