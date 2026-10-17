#!/usr/bin/env python3
"""Full local-snapshot replay in temporary copies; no release-tree mutations."""
# D0_CI_TIMEOUT_SECONDS=1200
from __future__ import annotations
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');a=ap.parse_args()
 env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'}
 subprocess.run([sys.executable,str(BASE/'verify_intake.py')],env=env,check=True)
 if a.verify_only:return
 records=[]
 with tempfile.TemporaryDirectory(prefix='d0_complete_intake_') as td:
  d=Path(td);v2=d/'v2_snapshot/d0_research_v2';v1=d/'independent_v1';v3=d/'continuation_v3'
  shutil.copytree(BASE/'v2_snapshot/d0_research_v2',v2)
  shutil.copytree(v2/'input_v1/d0_local_matter_bridge',v1)
  shutil.copytree(BASE/'continuation_v3',v3)
  commands=[('v1_full_replay',[sys.executable,str(v1/'src/run_all.py')]),
            ('v2_full_replay',[sys.executable,str(v2/'src/run_all.py')]),
            ('v3_exact',[sys.executable,str(v3/'src/moving_preparation_exact.py')]),
            ('v3_exact_optimized',[sys.executable,'-O',str(v3/'src/moving_preparation_exact.py')]),
            ('v3_interval',[sys.executable,str(v3/'src/moving_preparation_interval.py')]),
            ('v3_interval_optimized',[sys.executable,'-O',str(v3/'src/moving_preparation_interval.py')]),
            ('v3_actual_mutations',[sys.executable,str(v3/'src/hostile_mutations.py')])]
  for name,cmd in commands:
   start=time.monotonic();r=subprocess.run(cmd,cwd=d,text=True,capture_output=True,timeout=300,env=env)
   output=(r.stdout or '')+'\n'+(r.stderr or '')
   records.append({'name':name,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'output':output})
   print(name,'PASS' if r.returncode==0 else 'FAIL',flush=True)
   if r.returncode:
    print(output);raise AssertionError(('REPLAY_FAILED',name))
 subprocess.run([sys.executable,str(BASE/'verify_intake.py')],env=env,check=True)
 destination=ROOT/'.build';destination.mkdir(exist_ok=True)
 report={'status':'PASS','commands':records,'release_tree_preserved':True,
         'physical_forcing_or_GR_closed':False,'new_Lean_compilation':False,
         'manifest_sha256':hashlib.sha256((BASE/'MANIFEST.json').read_bytes()).hexdigest()}
 (destination/'d0_local_record_to_matter_intake_replay.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS_LOCAL_INTAKE_ALL_THREE_STAGES',len(records),'complete command groups')
if __name__=='__main__':main()
