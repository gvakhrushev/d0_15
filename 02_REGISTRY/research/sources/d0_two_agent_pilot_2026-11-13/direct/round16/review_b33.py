#!/usr/bin/env python3
"""Pin and replay independent operator-compression checks without owner edits."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent;D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round33')
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
receipt=json.loads((B/'RECEIPT.json').read_text())
for name,value in receipt['files'].items():assert h(B/name)==value,name
inputs=json.loads((B/'ACTUAL_COMPRESSION_INPUTS_CHECK.json').read_text())['input_sha256']
for name,value in inputs.items():assert h(D/name)==value,name
assert json.loads((B/'ACTUAL_LEAF_CONSUMER_SPEC_CHECK.json').read_text())['input_sha256']==h(D/'round15/SOURCE_DISPATCH_TABLES.json')
scripts=['check_exact_dag_compression_inputs.py','check_actual_leaf_consumer_contract.py','check_coherent_compression_toy.py','check_dynamic_pair_gates.py']
outputs=['ACTUAL_COMPRESSION_INPUTS_CHECK.json','ACTUAL_LEAF_CONSUMER_SPEC_CHECK.json','COHERENT_TOY_CHECK.json','DYNAMIC_PAIR_SMALL_GATES_CHECK.json']
logs=[]
with tempfile.TemporaryDirectory(prefix='d0-b33-replay-') as tmp:
    temp=Path(tmp)
    for script in scripts:shutil.copyfile(B/script,temp/script)
    for script in scripts:
        result=subprocess.run([sys.executable,'-B','-W','error',str(temp/script)],cwd=tmp,env=dict(os.environ,OPENBLAS_NUM_THREADS='1'),capture_output=True,text=True)
        assert result.returncode==0,(script,result.stdout[-1500:],result.stderr[-2500:])
        logs.append({'script':script,'exit_code':0})
    for output in outputs:assert (temp/output).read_bytes()==(B/output).read_bytes(),output
out={'status':'PASS_B33_OPERATOR_PROOF_AND_ISOLATED_CHECK_REPLAY','B33_commit':'9c89edf90f4c1df44559cff3ed721577d2f3a946',
     'receipt_sha256':h(B/'RECEIPT.json'),'verified_B33_files':receipt['files'],'verified_inputs':inputs,
     'root_replayed_scripts':logs,'byte_identical_outputs':{n:h(B/n) for n in outputs},
     'PF_convention':'rho_x=256*PF_probability(x); inverse_PF_once=1/rho_x from A11',
     'scope':'B33 proves full ideal operator compression conditional on concrete consumer and stated fresh inputs. A16 supplies the ideal consumer with a separately bounded native error; it does not produce the complete H1 instrument.',
     'full_H1_writer_emitted':False,'full_source_alpha_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'ROOT_REVIEW_B33.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'scripts':len(scripts),'byte_identical_outputs':len(outputs)}))
