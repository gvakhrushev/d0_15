#!/usr/bin/env python3
"""Isolated replay of B27 logical words and actual native zero/phase macros."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib,json,os,shutil,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
REL=Path('02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
B=ROOT/REL/'round27'
NATIVE=Path('02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((B/'RECEIPT.json').read_text())
assert sha(ROOT/REL/'round25/SOURCE_LEAF_BINDING.json')==receipt['input_sha256']['SOURCE_LEAF_BINDING.json']
assert sha(ROOT/NATIVE)==receipt['input_sha256']['native_execution.py']
for name,value in receipt['output_sha256'].items():assert sha(B/name)==value,name
scripts=[('build_leaf_inventory.py',['ACTUAL_PAIR_INVENTORY.jsonl','CHOI_EXAMPLE_GATE_LIST.json','CAR_EXAMPLE_GATE_LIST.json','PAIR_INVENTORY_SUMMARY.json']),
         ('check_controlled_involution.py',['LOGICAL_CHECK.json']),('check_native_Z.py',['NATIVE_Z_CHECK.json'])]
outputs={}
with TemporaryDirectory(prefix='d0_a13_review_b27_') as temp:
    root=Path(temp);dest=root/REL/'round27'
    shutil.copytree(B,dest,ignore=shutil.ignore_patterns('__pycache__'))
    for rel in [NATIVE,REL/'round25/SOURCE_LEAF_BINDING.json']:
        (root/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,root/rel)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1')
    for script,names in scripts:
        process=subprocess.run([sys.executable,'-B','-W','error',str(dest/script)],text=True,capture_output=True,env=env)
        assert process.returncode==0,(script,process.stdout,process.stderr)
        assert not process.stderr,(script,process.stderr)
        for name in names:
            assert sha(dest/name)==sha(B/name),name
            outputs[name]=sha(dest/name)
        print(script,'PASS',len(names),'byte-identical files',flush=True)
result={'status':'PASS_B27_ISOLATED_LOGICAL_AND_NATIVE_REPLAY','input_sha256':receipt['input_sha256'],
        'B27_output_sha256':receipt['output_sha256'],'B27_receipt_sha256':sha(B/'RECEIPT.json'),
        'byte_identical_regenerated_outputs':outputs,
        'native_scope':'Exact routed Z and G inverse, with accessible declared port and untouched unknown Spin/port at boundaries; whole logical X/CCX/CZ words not native compiled.',
        'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'ROOT_REVIEW_B27.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],flush=True)
