#!/usr/bin/env python3
"""Run mathematical mutants in disposable directories, not just hash failures."""
import json, os, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
original=(HERE/'verify.py').read_text()
mutations={
 'lost_pending_branch':('return B0*X*adj(B0)+Y, B1*X*adj(B1)','return B0*X*adj(B0), B1*X*adj(B1)'),
 'wrong_source_for_return':('return B0*X*adj(B0)+Y, B1*X*adj(B1)','return B0*X*adj(B0)+Y, B1*Y*adj(B1)'),
 'resplit_pending_in_numeric':('return B0@X@B0.conj().T+Y, B1@X@B1.conj().T','return B0@X@B0.conj().T+B0@Y@B0.conj().T, B1@X@B1.conj().T'),
 'frozen_instrument_jet':('dXX=dB0@X@B0.conj().T+B0@dX@B0.conj().T+B0@X@dB0.conj().T+dY','dXX=B0@dX@B0.conj().T+dY'),
 'frozen_prepared_density':('dL=1j*HL@L','dL=np.zeros_like(L)'),
 'entropy_as_gain':('cost=-sp.log(mu)/g;gain=sp.log(q/mu)/g','cost=-sp.log(mu)/g;gain=-sp.log(q)/g'),
 'erase_coherent_offdiagonal':('p**2*sp.Matrix([[1,c],[c,1]])','p**2*sp.eye(2)'),
 'wrong_net_source_sign':('netjet=4*p*p*iv.log(4)/(5*ell)','netjet=-4*p*p*iv.log(4)/(5*ell)'),
}
stages={'resplit_pending_in_numeric':'numeric','frozen_instrument_jet':'numeric','frozen_prepared_density':'numeric','wrong_net_source_sign':'interval'}
out=[]
for name,(old,new) in mutations.items():
    if original.count(old)!=1:raise RuntimeError('MUTATION_ANCHOR: '+name)
    with tempfile.TemporaryDirectory(prefix='d0-gain-mutant-') as td:
        p=Path(td)/'verify.py';p.write_text(original.replace(old,new))
        run=subprocess.run([sys.executable,'-O',str(p),'--math-only','--stage',stages.get(name,'exact')],capture_output=True,text=True,timeout=120,
            env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
        text=run.stdout+run.stderr
        if run.returncode==0 or 'MATHEMATICAL_GATE:' not in text:
            raise RuntimeError('MUTATION_NOT_MATHEMATICALLY_REJECTED: '+name+'\n'+text[-1000:])
        gate=text.split('MATHEMATICAL_GATE:')[-1].splitlines()[0].strip()
        out.append({'mutation':name,'rejected':True,'gate':gate})
        print('REJECTED',name,gate,flush=True)
with tempfile.TemporaryDirectory(prefix='d0-gain-false-scope-') as td:
    root=Path(td)
    for f in ('verify.py','RESULT.md','receipt.json'):(root/f).write_bytes((HERE/f).read_bytes())
    receipt=json.loads((root/'receipt.json').read_text());receipt['scope']['original_fixed_source_terminal_or_GR_closed']=True
    (root/'receipt.json').write_text(json.dumps(receipt))
    run=subprocess.run([sys.executable,'-O',str(root/'verify.py')],capture_output=True,text=True,timeout=120,
        env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
    if run.returncode==0 or 'IMMUTABLE_RECEIPT_MISMATCH' not in run.stderr:
        raise RuntimeError('FALSE_SCOPE_NOT_REJECTED')
print(json.dumps({'status':'PASS','mathematical_mutants':out,'false_physical_receipt_rejected':True},sort_keys=True))
