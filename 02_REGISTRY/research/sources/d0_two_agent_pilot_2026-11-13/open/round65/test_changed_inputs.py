#!/usr/bin/env python3
"""Check which changed input values are actually enforced; temporary files only."""
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
from hashlib import sha256
import json, sys
P=Path(__file__).resolve().parent
O=P.parent
script=(P/'certify_scalar_hessian_envelope.py').read_text()
env=json.loads((O/'round21/CHART_ENVELOPE_RESULT.json').read_text())
target=(O/'round25/TARGETS_RU.md').read_text()
with TemporaryDirectory(dir=P) as t:
    T=Path(t)
    envpath=T/'env.json'; targetpath=T/'target.md'
    envpath.write_text(json.dumps(env)); targetpath.write_text(target)
    src=script.replace("envfile=O/'round21/CHART_ENVELOPE_RESULT.json'",f'envfile=Path({str(envpath)!r})')
    src=src.replace("O/'round25/TARGETS_RU.md'",f'Path({str(targetpath)!r})')
    src=src.replace("P=Path(__file__).resolve().parent;O=P.parent;",f'P=Path({str(T)!r});O=Path({str(O)!r});')
    tmp=T/'check.py';tmp.write_text(src)
    def invoke():
        result=run([sys.executable,str(tmp)],capture_output=True,text=True)
        return result.returncode
    assert invoke()==0
    first=json.loads((T/'SCALAR_HESSIAN_ENVELOPE.json').read_text())
    bad=dict(env);bad['coframe_creator_norm_strict_upper']='1'
    envpath.write_text(json.dumps(bad))
    assert invoke()!=0
    envpath.write_text(json.dumps(env))
    assert 'epsilon_h=2^-1531' in target
    targetpath.write_text(target.replace('epsilon_h=2^-1531','epsilon_h=2^-1',1))
    assert invoke()==0
    second=json.loads((T/'SCALAR_HESSIAN_ENVELOPE.json').read_text())
    assert first['source_sha256'][str(targetpath)]!=second['source_sha256'][str(targetpath)]
print(json.dumps({'baseline':'PASS','invalid_coframe_bound':'REJECTED','changed_documented_epsilon':'PASS_WITH_CHANGED_HASH_ONLY','meaning':'source digest records drift but checker does not parse or reject changed TARGETS constants; owner equivalence remains an external premise'}))
