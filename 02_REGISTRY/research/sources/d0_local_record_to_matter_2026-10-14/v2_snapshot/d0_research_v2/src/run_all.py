"""Reproduce this offline research stage. No GitHub writes or external requests."""
from __future__ import annotations
import hashlib,json,os,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
(R/'results').mkdir(exist_ok=True);(R/'logs').mkdir(exist_ok=True)
commands=[
 ('input_v1_manifest',[sys.executable,'verify_bundle.py'],R/'input_v1/d0_local_matter_bridge'),
 ('exact_operations',[sys.executable,str(R/'src/derive_operations.py')],R),
 ('exact_operations_optimized',[sys.executable,'-O',str(R/'src/derive_operations.py')],R),
 ('full_curved_words',[sys.executable,str(R/'src/full_curved_word_check.py')],R),
 ('full_curved_words_optimized',[sys.executable,'-O',str(R/'src/full_curved_word_check.py')],R),
 ('rare_history_interval',[sys.executable,str(R/'src/filter_interval.py')],R),
 ('frequency_filter_interval',[sys.executable,str(R/'src/frequency_filter_interval.py')],R),
 ('frequency_filter_interval_optimized',[sys.executable,'-O',str(R/'src/frequency_filter_interval.py')],R),
 ('actual_mutations',[sys.executable,str(R/'src/hostile_mutations.py')],R),
]
records=[]
for name,cmd,cwd in commands:
 t=time.monotonic()
 cp=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=150,
      env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1'})
 text=cp.stdout+'\n'+cp.stderr;(R/'logs'/f'{name}.txt').write_text(text)
 records.append({'name':name,'returncode':cp.returncode,'elapsed_seconds':round(time.monotonic()-t,3)})
 print(name,cp.returncode,flush=True)
 if cp.returncode:raise SystemExit(text)
(R/'results/replay.json').write_text(json.dumps({'status':'PASS','commands':records},indent=2)+'\n')
print('PASS_V2_REPLAY',len(records),'commands')
