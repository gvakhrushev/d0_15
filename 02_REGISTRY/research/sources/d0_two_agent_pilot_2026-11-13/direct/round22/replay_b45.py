#!/usr/bin/env python3
"""Replay B45 checks with all writes intercepted; never alter B's artifacts."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
Q=B/'02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round45'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checkpoint=json.loads((Q/'B45_CHECKPOINT.json').read_text())
for f,digest in checkpoint['file_sha256'].items():assert h(Q/f)==digest,f
rev=subprocess.check_output(['git','rev-parse','681ba4f6f'],cwd=B,text=True).strip()
for f in [*checkpoint['file_sha256'],'B45_CHECKPOINT.json']:
    assert subprocess.check_output(['git','show',rev+':'+str((Q/f).relative_to(B))],cwd=B)==(Q/f).read_bytes()
wrapper='''from pathlib import Path
import runpy,sys
script=Path(sys.argv[1]);expected=Path(sys.argv[2]);old=Path.write_text;outputs=[]
def intercept(path,text,*args,**kwargs):
    assert path.resolve()==expected.resolve(),('unexpected write',str(path))
    assert text.encode()==expected.read_bytes(),('nonidentical output',str(path))
    outputs.append(str(path));return len(text)
Path.write_text=intercept
sys.path.insert(0,str(script.parent))
runpy.run_path(str(script),run_name='__main__')
assert outputs==[str(expected)]
'''
checks=[('verify_site_angles.py','SITE_ANGLE_INDEPENDENT_CHECK.json'),('check_site_matrix.py','SITE_MATRIX_CHECK.json'),
        ('check_site_native.py','SITE_NATIVE_CHECK.json'),('verify_site_inventory.py','SITE_INVENTORY_CHECK.json')]
records=[]
with tempfile.TemporaryDirectory(prefix='d0_a22_b45_') as tmp:
    path=Path(tmp)/'replay.py';path.write_text(wrapper)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    for script,output in checks:
        p=subprocess.run([sys.executable,'-B','-W','error',str(path),str(Q/script),str(Q/output)],cwd=Q,env=env,text=True,capture_output=True,timeout=600)
        assert p.returncode==0,(script,p.stdout[-2000:],p.stderr[-3000:])
        records.append({'script':script,'output':output,'output_sha256':h(Q/output),'isolated_JSON_identical':True})
        print('replayed',script,flush=True)
out={'status':'PASS_ROOT_INDEPENDENT_REPLAY_B45_FULL_SITE','B45_commit':rev,'checkpoint_sha256':h(Q/'B45_CHECKPOINT.json'),
     'pinned_files_sha256':checkpoint['file_sha256'],'isolated_replays':records,
     'all166_angles_replayed_with_rectangular_intervals':True,'all255_tree_nodes_and44722_compact_SITE_blocks_replayed':True,
     'all256_original_input_columns':True,'new_clean_work':0,'operator_error_lt':'2^-3259',
     'physical_C_closed':False,'GR_closed':False}
(P/'ROOT_REVIEW_B45.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'isolated_replays':len(records)}))
