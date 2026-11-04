#!/usr/bin/env python3
"""Verify §7fk evidence bytes and optional Git sources; no owner code execution."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess

P = Path(__file__).resolve().parent
M = json.loads((P/'MANIFEST.json').read_text())

def need(ok, why):
    if not ok:
        raise ValueError(why)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def git(*args):
    return subprocess.check_output(['git','-C',str(P),*args])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify-source-objects',action='store_true')
    args=parser.parse_args()
    patch=lzma.decompress((P/'complete_delta.patch.xz').read_bytes())
    need(sha(patch)==M['patch_sha256'],'patch mismatch')
    for path,pins in M['changed_blobs'].items():
        raw=lzma.decompress((P/pins['snapshot']).read_bytes())
        need(blob(raw)==pins['head_blob'] and sha(raw)==pins['head_sha256'],'snapshot mismatch: '+path)
    memo_path=next(x for x in M['changed_blobs'] if x.startswith('02_REGISTRY/'))
    memo=lzma.decompress((P/M['changed_blobs'][memo_path]['snapshot']).read_bytes())
    checker=(P/'check_retention_collar.py').read_bytes()
    receipt=(P/'owner_compact_receipt.json').read_bytes()
    proof=(P/'proof_section.md').read_bytes()
    a,b=M['owner_checker_range']; x,y=M['owner_proof_range']
    need(memo[a:b]==checker and sha(checker)==M['checker_sha256'],'checker mismatch')
    need(memo[x:y]==proof and sha(proof)==M['owner_proof_sha256'],'proof mismatch')
    need(sha(receipt)==M['owner_compact_receipt_sha256'],'compact receipt mismatch')
    section=memo.decode().split('## 7fk. ',1)[1].split('\n## 7',1)[0]
    fences=re.findall(r'(?m)^```(\w+)\n(.*?)^```[ \t]*$',section,re.S)
    need([b.encode() for a,b in fences if a=='json']==[receipt],'receipt differs from embedded source')
    meta=json.loads(receipt)
    need(meta['checker_sha256']==M['checker_sha256'] and meta['proof_sha256']==M['owner_proof_sha256'], 'owner code/proof pin differs')
    need(meta['normal_result_sha256']==M['owner_expected_stdout_sha256'] and meta['check_count']==M['owner_reported_check_count'] and meta['classifications']==M['owner_reported_check_counts'],'owner compact receipt differs')
    need(len(M['inherited_prior_input_pins_at_base'])==17,'prior input set mismatch')
    if args.verify_source_objects:
        need(git('rev-parse',M['head']+'^').decode().strip()==M['base'],'parent mismatch')
        need(git('diff','--no-ext-diff','--binary','--full-index',M['base'],M['head'],'--')==patch,'full diff mismatch')
        for path,pins in M['changed_blobs'].items():
            for rev,prefix in ((M['base'],'base'),(M['head'],'head')):
                raw=git('show',rev+':'+path)
                need(blob(raw)==pins[prefix+'_blob'] and sha(raw)==pins[prefix+'_sha256'],'source blob mismatch: '+path)
        for path,pins in M['inherited_prior_input_pins_at_base'].items():
            raw=git('show',M['base']+':'+path)
            need(blob(raw)==pins['blob'] and sha(raw)==pins['sha256'],'prior input mismatch: '+path)
    print('PASS: full diff/snapshots, checker, embedded proof and compact receipt'+(' and source Git objects' if args.verify_source_objects else ' (Git inputs not checked)'))

if __name__=='__main__':
    main()
