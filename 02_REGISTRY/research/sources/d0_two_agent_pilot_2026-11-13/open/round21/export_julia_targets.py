#!/usr/bin/env python3
"""Numerical all-column Julia32 targets of the selected ORIGINAL L=4 centre.

This streams local centre targets, not the compiled H.1 Choi-bank writer,
its exponential SAM palette, source signs, or all marked prefix maps.
"""
from pathlib import Path
import hashlib,json
import numpy as np

HERE=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (HERE/'BRINKMANN_L4_CENTRE.jsonl').read_text().splitlines()]
order=(0,2,3,1)
creators=[]
for r in range(4):
    cr=np.zeros((16,16));before=order[:order.index(r)]
    for bits in range(16):
        if not ((bits>>r)&1):cr[bits|(1<<r),bits]=(-1)**sum((bits>>j)&1 for j in before)
    creators.append(cr)
Id=np.eye(16); eye=np.eye(32)
mm=lambda x,y:np.einsum('ij,jk->ik',x,y,optimize=False)

def exterior(U):
    out=np.zeros((16,16))
    for a in range(16):
      ar=[j for j in order if (a>>j)&1]
      for b in range(16):
        br=[j for j in order if (b>>j)&1]
        if len(ar)==len(br):out[a,b]=1 if not ar else np.linalg.det(U[np.ix_(ar,br)])
    return out

def root(M):
    val,vec=np.linalg.eigh((M+M.T)/2)
    assert val.min()>0
    return mm(vec*np.sqrt(val),vec.T)

def julia(C):
    left=root(Id-mm(C,C.T));right=root(Id-mm(C.T,C))
    return np.block([[C,left],[right,-C.T]])

unitary_error=0.;min_defect=1.
coframe=np.empty((256,2,4,32,32));links=np.empty((256,4,32,32))
identical_link=julia(Id/2)
for i,row in enumerate(rows):
    V=np.array(row['native_coframe_columns_approx']);U=np.array(row['U_u_approx'])
    rho=row['rho_num']/row['rho_den']
    for mode,scale in enumerate((1.,np.sqrt(rho))):
        for r in range(4):
            C=sum(scale*V[j,r]*creators[j] for j in range(4))
            min_defect=min(min_defect,float(np.linalg.eigvalsh(Id-mm(C,C.T)).min()))
            J=julia(C);unitary_error=max(unitary_error,float(np.max(np.abs(mm(J.T,J)-eye))))
            coframe[i,mode,r]=J
    Lu=exterior(U);C=Lu/2
    min_defect=min(min_defect,float(np.linalg.eigvalsh(Id-mm(C,C.T)).min()))
    links[i,0]=julia(C);links[i,1:]=identical_link
    unitary_error=max(unitary_error,float(np.max(np.abs(mm(links[i,0].T,links[i,0])-eye))))
assert min_defect>0 and unitary_error<1e-12
out=HERE/'CENTRE_JULIA32_TARGETS_NUMERIC.npz'
np.savez_compressed(out,coframe_raw_and_pf=coframe,proper_links=links,
                    sites=np.array([r['site'] for r in rows],dtype=np.int16))
result={'status':'CENTRE_NUMERIC_JULIA32_TARGETS_NOT_GATE_WORD',
        'sites':len(rows),'coframe_matrices':256*2*4,'link_matrices':256*4,
        'dimensions':'32x32, all columns','creator_order':order,
        'coframe_modes':['native_raw','source_compatible_sqrt_rho_dressed'],
        'min_left_defect_eigenvalue_float':min_defect,'max_orthogonality_error_float':unitary_error,
        'float_not_interval_certified':True,'whole_choi_programme_banks_constructed':False,
        'all_sample_vertices_constructed':False,'compiled_native_words_emitted':False,
        'geometry_input_sha256':hashlib.sha256((HERE/'BRINKMANN_L4_CENTRE.jsonl').read_bytes()).hexdigest(),
        'npz_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'GR_closed':False}
(HERE/'JULIA_TARGET_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
