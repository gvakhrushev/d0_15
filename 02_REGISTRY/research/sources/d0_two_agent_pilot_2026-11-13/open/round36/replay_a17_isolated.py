#!/usr/bin/env python3
"""Rebuild A17 in isolated clone and compare semantics under path rebasing."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess,tempfile
P=Path(__file__).resolve().parent;ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13');base=Path('02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
rels=['round12/compile_source_selectors.py','round12/TEN_SIGN_REPORT_PALETTE.json','round13/reversible_selectors.py','round13/compile_native_cz.py','round13/TOP_SOURCE_SELECTOR_CIRCUIT.json','round13/INTERNAL_SELECTOR_CIRCUIT.json','round13/FIRST_SUCCESS_CIRCUITS.json','round13/TEN_SIGN_REPORT_CIRCUIT.json','round13/CIRCUIT_COMPILATION.json','round14/native_boolean.py','round14/NATIVE_BOOLEAN_ANGLE.json','round15/source_dispatcher.py','round15/SOURCE_DISPATCH_TABLES.json','round15/SOURCE_DISPATCH_COMPILATION.json','round16/source_select.py','round16/SOURCE_SELECT_COMPILATION.json','round17/report_assembly.py','round17/check_report_assembly.py']
files=[base/x for x in rels]+[Path('02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py')]
outs=['GLOBAL_REPORT_PLAN.json','GLOBAL_REPORT_COMPILATION.json','GLOBAL_REPORT_CHECK.json'];target=ROOT/base/'round17';sha=lambda x:sha256(x.read_bytes()).hexdigest();inputs={str(x):sha(ROOT/x) for x in files};original={x:sha(target/x) for x in outs};logs=[]
def normcomp(c):
 c=dict(c); h=c['input_sha256'];new={}
 for k,v in h.items():
  if '/direct/' in k:key='direct/'+k.rsplit('/direct/',1)[1]
  elif '/open/round31/' in k:key='open/round31/'+k.rsplit('/open/round31/',1)[1]
  else:raise ValueError(k)
  assert key not in new;new[key]=v
 c['input_sha256']=new;return c
def normcheck(c):
 c=dict(c);h=dict(c['input_sha256']);h['GLOBAL_REPORT_COMPILATION.json']='<path-rebased-compilation-hash>';c['input_sha256']=h;return c
with tempfile.TemporaryDirectory(prefix='a17-replay-',dir=P) as td:
 tmp=Path(td)
 for rel in files:(tmp/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,tmp/rel)
 work=tmp/base/'round17'
 for script in ('report_assembly.py','check_report_assembly.py'):
  r=subprocess.run(['python3','-B','-W','error',script],cwd=work,capture_output=True,text=True,check=True);logs.append({'script':script,'stdout':r.stdout.strip(),'stderr':r.stderr})
 output={x:sha(work/x) for x in outs};assert output['GLOBAL_REPORT_PLAN.json']==original['GLOBAL_REPORT_PLAN.json']
 assert normcomp(json.loads((work/outs[1]).read_text()))==normcomp(json.loads((target/outs[1]).read_text()))
 assert normcheck(json.loads((work/outs[2]).read_text()))==normcheck(json.loads((target/outs[2]).read_text()))
 assert {str(x):sha(ROOT/x) for x in files}==inputs and {x:sha(target/x) for x in outs}==original
out={'status':'PASS_ISOLATED_A17_BUILDER_AND_CHECKER','input_sha256':inputs,'original_outputs_sha256':original,'clone_outputs_sha256':output,'plan_byte_identical':True,'compilation_equal_after_rebasing_input_path_keys':True,'checker_equal_after_rebasing_compilation_hash':True,'root_B31_bank_read_only_at_absolute_path':True,'commands':logs,'original_files_modified':False,'full_native_walk_executed':False,'GR_closed':False}
(P/'A17_ISOLATED_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'plan_byte_identical':True,'other_two_semantically_equal_after_path_rebasing':True,'commands':logs},indent=2))
