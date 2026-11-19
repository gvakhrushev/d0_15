#!/usr/bin/env python3
"""Logical Golden seed and structural factory-cut tests, not a Book03 test."""
from itertools import product
from pathlib import Path
import ast
import json
import numpy as np

owner=Path(__file__).with_name('check_native_golden_descriptor_secants.py')
tree=ast.parse(owner.read_text())
program_def=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='program')
scope={}
exec(compile(ast.Module(body=[program_def],type_ignores=[]),str(owner),'exec'),scope)
p=(5**0.5-1)/2
r=p*p
rows=[]
for n in range(2,9):
    word=scope['program'](n)
    # Every k occurrence is a control. No logical stage writes the program.
    for op in word:
        assert op[-1]!='k'
    prob=np.zeros((2,2))
    overlap=np.zeros(2)
    for h,*z in product((0,1),repeat=n+1):
        w=(r if h else p)*np.prod([r if bit else p for bit in z])
        t0=h
        t1=int(h or not any(z))
        prob[0,t0]+=w
        prob[1,t1]+=w
        if t0==t1:overlap[t0]+=w
    delta=p**(n+1)
    assert np.allclose(prob[:,1],[r,r+delta],atol=1e-13)
    assert np.allclose(overlap,[p-delta,r],atol=1e-13)
    assert abs(sum(overlap)-(1-delta))<1e-13
    # The two programmed environmental output vectors form a PSD Gram matrix.
    gram=np.array([[1,sum(overlap)],[sum(overlap),1]])
    eig=np.linalg.eigvalsh(gram)
    assert min(eig)>-1e-13
    eigen_small=delta/2
    entropy=-(eigen_small*np.log2(eigen_small)+(1-eigen_small)*np.log2(1-eigen_small))
    rows.append({'N':n,'logical_operations_with_k_as_target':0,
                 'program_0_t1':prob[0,1],'program_1_t1':prob[1,1],
                 'output_trace_program_coherence_factor':float(sum(overlap)),
                 'program_output_entanglement_bits_for_plus_input':float(entropy),
                 'gram_min_eigenvalue':float(min(eig))})

# Structural failure cuts: k, second control, target, local resource. The
# exact owner gives each fine measurement record a scalar norm; test only
# the program commutators of the corresponding normalized cut unitaries here.
I=np.eye(16,dtype=complex)
Pk=np.diag([1 if (j>>3)==0 else 0 for j in range(16)])
H=np.array([[1,1],[1,-1]],complex)/2**0.5
Ht=np.kron(np.kron(np.eye(4),H),np.eye(2))
CZtr=np.diag([-1 if (j&2 and j&1) else 1 for j in range(16)])
CCZ=np.diag([-1 if (j&8 and j&4 and j&2) else 1 for j in range(16)])
def mm(a,b): return np.einsum('ij,jk->ik',a,b,optimize=False)
cuts={'resource_1_failure':I,'resource_2_failure':I,'h1_cz_failure':I,
      'h1_x_failure':CZtr,'ccz_failure':Ht,'h2_cz_failure':mm(CCZ,Ht),
      'h2_x_failure':mm(CZtr,mm(CCZ,Ht)),'success':mm(Ht,mm(CCZ,Ht))}
for name,V in cuts.items():
    assert np.isfinite(V).all(),name
    assert np.linalg.norm(mm(V,Pk)-mm(Pk,V))<1e-13,name
    assert np.linalg.norm(mm(V.conj().T,V)-I)<1e-13,name
out={'status':'conditional logical seed and representative normalized cuts; not microscopic factory simulation',
     'seed_tests':rows,'tested_normalized_factory_cuts':list(cuts),
     'source_scalar_effect_required_for_every_thin_record':True,
     'complete_seed_plus_factory_expansion_or_Book03_verified':False,
     'GR_closed':False}
Path(__file__).with_name('seed_program_centrality_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
