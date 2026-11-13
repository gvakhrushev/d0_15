#!/usr/bin/env python3
"""Pin B31 provenance and replay its exact checks in a rootlike temporary copy."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
A=P.parents[5]
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
R=Path('02_REGISTRY/research/sources')
pilot=R/'d0_two_agent_pilot_2026-11-13'
b=B/pilot/'open/round31'
h=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
receipt=json.loads((b/'RECEIPT.json').read_text())
candidates=[B/R/'d0_paid_moment_field_writer_2026-10-21/code/PAID_CODE_AND_MOMENT_WRITER.md',B/R/'d0_native_execution_domain_2026-10-24/native_execution.py']
for root in [B/pilot/'open/round27',B/pilot/'open/round30',A/pilot/'direct/round12',A/pilot/'direct/round14']:
    candidates += [f for f in root.iterdir() if f.is_file()]
byhash={h(f):f for f in candidates}
verified={}
for label,value in receipt['input_sha256'].items():
    assert value in byhash,(label,'missing input')
    verified[label]={'path':str(byhash[value]),'sha256':value}
for name,value in receipt['output_sha256'].items():assert h(b/name)==value,name
outputs=['ROUTER_CHECK.json','LOGICAL_FAIR_ROUTER.json','NATIVE_FAIR_BANK.json','NATIVE_FAIR_BANK_CHECK.json','NATIVE_STRUCTURE_CHECK.json','FAIR_READINESS_CERT.json']
commands=['check_fair_router.py','build_native_fair_bank.py','check_native_bank_structure.py','certify_fair_readiness.py']
with tempfile.TemporaryDirectory(prefix='d0-b31-root-replay-') as temp:
    root=Path(temp)/'root';target=root/pilot/'open/round31'
    shutil.copytree(b,target)
    owner=R/'d0_native_execution_domain_2026-10-24/native_execution.py'
    (root/owner).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(B/owner,root/owner)
    for name in outputs:(target/name).unlink()
    logs=[]
    for script in commands:
        run=subprocess.run([sys.executable,'-B','-W','error',str(target/script)],cwd=str(root),env=dict(os.environ,OPENBLAS_NUM_THREADS='1'),capture_output=True,text=True)
        assert run.returncode==0,(script,run.stdout[-2000:],run.stderr[-3000:])
        logs.append({'script':script,'exit_code':run.returncode})
    for name in outputs:assert (target/name).read_bytes()==(b/name).read_bytes(),name
result={'status':'PASS_B31_PROOF_RECEIPT_AND_ISOLATED_EXACT_REPLAY',
    'B31_commit':'b648521b916006d72b87654340043d2a815ab801',
    'B31_receipt_sha256':h(b/'RECEIPT.json'),'verified_inputs':verified,'verified_outputs':receipt['output_sha256'],
    'root_replayed_scripts':logs,'byte_identical_regenerated_outputs':{n:h(b/n) for n in outputs},
    'small_float_native_check_repeated':False,
    'scope':'Exact parity state, coherent first-success SWAP, native prefix/inverse/structure and component readiness; not complete birth ledger or full alpha.',
    'full_native_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'ROOT_REVIEW_B31.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'scripts':len(logs),'byte_identical_outputs':len(outputs)}))
