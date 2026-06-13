#!/usr/bin/env python3
"""Run the v15/v16 integration certificates that were explicitly discussed."""
import subprocess, pathlib, json, sys, time

here = pathlib.Path(__file__).resolve().parent
scripts = [
    # Book 04 / matter operator boundary layer
    'vp_higgs_scalar_projector_constructive.py',
    'vp_higgs_scalar_projector_positive.py',
    'vp_higgs_yukawa_section_transfer.py',
    'vp_meson_defect_transfer_algebra.py',
    'vp_meson_positive_defect_transfer.py',
    'vp_cvft_baryon_40_56_decomposition.py',
    'vp_cvft_baryon_spin_flavour_40_56.py',
    'vp_baryon_40_56_anonymous_poles.py',
    # Fractal tick / self substrate / continuum
    'vp_self_substrate_trace_principle.py',
    'vp_fractal_tick_informational_mechanics.py',
    'vp_continuum_from_fractal_tick.py',
    # Edge / ramification / horizon bridges
    'vp_edge_alpha_trace.py',
    'vp_edge_alpha_trace_constructive.py',
    'vp_ramification_edge_ueff_companion.py',
    # v16 external bridge / negative controls
    'vp_dusty_plasma_d0_mapping.py',
    'vp_ligo_discovery_negative_control.py',
    # publication claim guardrail
    'vp_publication_claim_register_guardrail.py',
]

results=[]
for s in scripts:
    p=here/s
    if not p.exists():
        results.append({'script':s,'status':'MISSING'})
        continue
    t=time.time()
    proc=subprocess.run([sys.executable,str(p)],cwd=here,text=True,capture_output=True,timeout=120)
    out=proc.stdout.strip()
    status='PASS' if proc.returncode==0 and 'PASS' in out else 'FAIL'
    results.append({
        'script':s,
        'returncode':proc.returncode,
        'last_stdout':out.splitlines()[-5:] if out else [],
        'stderr_tail':proc.stderr.strip().splitlines()[-5:],
        'seconds':round(time.time()-t,3),
        'status':status,
    })

pass_all=all(r.get('status')=='PASS' for r in results)
(here/'run_all_v16_integrated_certs_results.json').write_text(json.dumps({'pass':pass_all,'results':results},indent=2), encoding='utf-8')
print('PASS_RUN_ALL_V16_INTEGRATED_CERTS' if pass_all else 'FAIL_RUN_ALL_V16_INTEGRATED_CERTS')
if not pass_all:
    print(json.dumps([r for r in results if r.get('status')!='PASS'], indent=2))
