#!/usr/bin/env python3
"""Run D0 v16 publication guardrails."""
import subprocess, sys, pathlib, json, time
here = pathlib.Path(__file__).resolve().parent
scripts = ['vp_publication_claim_register_guardrail.py']
results=[]
for s in scripts:
    t=time.time()
    proc=subprocess.run([sys.executable, str(here/s)], cwd=here, text=True, capture_output=True, timeout=120)
    out=proc.stdout.strip()
    results.append({
        'script': s,
        'returncode': proc.returncode,
        'status': 'PASS' if proc.returncode == 0 and 'PASS' in out else 'FAIL',
        'stdout_tail': out.splitlines()[-10:],
        'stderr_tail': proc.stderr.strip().splitlines()[-10:],
        'seconds': round(time.time()-t,3),
    })
pass_all=all(r['status']=='PASS' for r in results)
(here/'run_all_publication_guardrails_results.json').write_text(json.dumps({'pass': pass_all, 'results': results}, indent=2), encoding='utf-8')
print('PASS_RUN_ALL_PUBLICATION_GUARDRAILS' if pass_all else 'FAIL_RUN_ALL_PUBLICATION_GUARDRAILS')
if not pass_all:
    print(json.dumps(results, indent=2))
    sys.exit(1)
