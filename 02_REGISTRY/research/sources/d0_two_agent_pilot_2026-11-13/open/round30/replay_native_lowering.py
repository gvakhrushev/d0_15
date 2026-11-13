#!/usr/bin/env python3
"""Isolated A14 supplementary lowering checker; source inputs are read-only."""
from pathlib import Path
import tempfile,shutil,subprocess,hashlib,json,os
P=Path(__file__).resolve().parent
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
f13=['reversible_selectors.py','INTERNAL_SELECTOR_CIRCUIT.json','TOP_SOURCE_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json','FIRST_SUCCESS_CIRCUITS.json','CIRCUIT_COMPILATION.json']
f14=['native_boolean.py','lower_native_selectors.py','check_native_lowering.py','NATIVE_BOOLEAN_ANGLE.json','NATIVE_BOOLEAN_LIBRARY.json','NATIVE_SELECTOR_LOWERING.json','NATIVE_LOWERING_CHECK.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();original={f'round13/{n}':sha(root/'round13'/n) for n in f13}|{f'round14/{n}':sha(root/'round14'/n) for n in f14}
with tempfile.TemporaryDirectory(prefix='lower_review_',dir=P) as tmp:
 d=Path(tmp);(d/'round13').mkdir();(d/'round14').mkdir()
 for n in f13:shutil.copy2(root/'round13'/n,d/'round13'/n)
 for n in f14:shutil.copy2(root/'round14'/n,d/'round14'/n)
 x=subprocess.run(['python3','-B','-W','error','check_native_lowering.py'],cwd=d/'round14',capture_output=True,text=True,check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 result=json.loads(x.stdout);assert sha(d/'round14/NATIVE_LOWERING_CHECK.json')==original['round14/NATIVE_LOWERING_CHECK.json'] and result['actual_logical_macro_wirings_checked']==350
out={'status':'PASS_ISOLATED_A14_SUPPLEMENTARY_LOWERING','input_sha256':original,'checker_output':result,'byte_equal_to_owner':True,'owner_modified':False,'GR_closed':False}
(P/'ISOLATED_LOWERING_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'macro_bindings':350}))
