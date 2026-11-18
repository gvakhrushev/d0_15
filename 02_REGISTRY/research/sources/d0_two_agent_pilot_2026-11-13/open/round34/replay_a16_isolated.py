#!/usr/bin/env python3
"""Replay A16 builder/checker in a temporary copy, byte-compare outputs."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess,tempfile
P=Path(__file__).resolve().parent
ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13')
base=Path('02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
files=['round11/PERIODIC_SOURCE_BINDING.json','round13/reversible_selectors.py','round13/compile_native_cz.py','round14/native_boolean.py','round14/NATIVE_BOOLEAN_ANGLE.json','round15/source_dispatcher.py','round15/SOURCE_DISPATCH_TABLES.json','round15/SOURCE_DISPATCH_COMPILATION.json','round15/PREPROCESSOR_READY_COMPOSITION.json','round16/source_select.py','round16/check_source_select.py']
files=[base/x for x in files]+[Path('02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py')]
outs=['DYNAMIC_PAIR_LIBRARY.json','SOURCE_SELECT_COMPILATION.json','SOURCE_SELECT_CHECK.json'];target=ROOT/base/'round16'
def digest(p):return sha256(p.read_bytes()).hexdigest()
inputs={str(x):digest(ROOT/x) for x in files};orig={x:digest(target/x) for x in outs};logs=[]
with tempfile.TemporaryDirectory(prefix='a16-replay-',dir=P) as tmp:
 tmp=Path(tmp)
 for f in files:(tmp/f).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/f,tmp/f)
 work=tmp/base/'round16'
 for script in ('source_select.py','check_source_select.py'):
  r=subprocess.run(['python3','-B','-W','error',script],cwd=work,text=True,capture_output=True,check=True);logs.append({'script':script,'stdout':r.stdout.strip(),'stderr':r.stderr})
 actual={x:digest(work/x) for x in outs};assert actual==orig,(actual,orig)
 assert {str(x):digest(ROOT/x) for x in files}==inputs and {x:digest(target/x) for x in outs}==orig
out={'status':'PASS_ISOLATED_A16_BUILDER_AND_CHECKER','input_sha256':inputs,'all_three_outputs_byte_identical':actual,'commands':logs,'source_owner_files_modified':False,'all_astronomical_native_gates_executed':False,'physical_C_closed':False,'GR_closed':False}
(P/'A16_ISOLATED_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'outputs_byte_identical':list(actual),'commands':logs},indent=2))
