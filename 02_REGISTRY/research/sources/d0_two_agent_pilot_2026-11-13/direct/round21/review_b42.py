#!/usr/bin/env python3
"""Pinned B42 consuming review, with isolated final native/resource replays."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
R=B/'02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round42'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checkpoint=json.loads((R/'B42_CHECKPOINT.json').read_text())
for name,digest in checkpoint['file_sha256'].items():assert h(R/name)==digest,name
assert checkpoint['angles']==5018 and checkpoint['literal_inverse_depth3_checked']
jobs=[('check_native_proper_link.py','NATIVE_PROPER_LINK_CHECK.json'),
      ('check_full_julia_schedule.py','FULL_JULIA_SCHEDULE_CHECK.json'),
      ('build_resource_receipt.py','PROPER_LINK_NATIVE_RESOURCES.json')]
replays=[]
with tempfile.TemporaryDirectory(prefix='d0-a21-b42-final-') as tmp:
    dst=Path(tmp)/'round42';dst.mkdir()
    for name in checkpoint['file_sha256']:shutil.copy2(R/name,dst/name)
    env=dict(os.environ);env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1'
    for script,output in jobs:
        result=subprocess.run([sys.executable,'-B','-W','error',script],cwd=dst,env=env,text=True,capture_output=True)
        assert result.returncode==0,(script,result.stdout[-2000:],result.stderr[-2000:])
        assert json.loads((dst/output).read_text())==json.loads((R/output).read_text()),(script,'JSON differs')
        replays.append({'script':script,'output':output,'output_sha256':h(R/output),'isolated_JSON_identical':True})
        print('B42 final isolated replay passed',script,flush=True)
for name,digest in checkpoint['file_sha256'].items():assert h(R/name)==digest
for name in ['INDEPENDENT_PROPER_LINK_ANGLES.json','RECTANGULAR_SAMPLE_CHECK.json','SOURCE_NAME_CHECK.json','PYTHON_FALLBACK_CHECK.json']:
    assert json.loads((R/name).read_text())['status'].startswith('PASS_')
out={'status':'PASS_CONSUMED_FINAL_B42_PROPER_LINK_COMPILER',
     'B42_commit':subprocess.check_output(['git','rev-parse','f4deec43d'],cwd=B,text=True).strip(),
     'checkpoint_sha256':h(R/'B42_CHECKPOINT.json'),'pinned_files_sha256':checkpoint['file_sha256'],
     'isolated_final_replays':replays,'internal_depth2_and_outer_depth3_price_bug_fixed_and_replayed':True,
     'source_scope':'B25 original proper-link Julia,336 exact formula families,23296 address/localSAM sectors,all32 input columns',
     'all5018_angle_bounds_replayed_by_B_at_8448_bits':True,'alternative_rectangular_power_samples_by_B':336,
     'all_angle_replay_reexecuted_by_root':False,
     'source_analytic_review':'Original exact Golden/Machin fields and finite matrix-exponential tail; positive boost certified or symbolically zero by source type; interval pivots; CAR covariance and full LDR Julia formula consumed from B41.',
     'proper_link_operator_error_lt':'2^-3257','strict_offsector_identity':True,'private_clean_work':0,
     'full_Omega_loader_compiled_by_this_review':False,'physical_C_closed':False,'GR_closed':False}
(P/'ROOT_REVIEW_B42.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'isolated_final_replays':len(replays)}))
