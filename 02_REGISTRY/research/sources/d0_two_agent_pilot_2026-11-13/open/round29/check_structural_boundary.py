#!/usr/bin/env python3
"""Hostile finite controls for norm-error versus exact H.1 structure."""
from pathlib import Path
import json,math,numpy as np
P=Path(__file__).resolve().parent
p=(math.sqrt(5)-1)/2;v=np.array([math.sqrt(p),p]);I=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);Z=np.diag([1.,-1.]);eps=.01;c=.6
M=c*np.eye(4);Mh=M+eps*np.kron(X,Z);J=np.kron(v.reshape(2,1),I);cm=J.T@Mh@J
assert abs(np.linalg.norm(Mh-M,2)-eps)<1e-14
assert np.allclose(cm,c*I+eps*2*math.sqrt(p)*p*Z,atol=1e-14)
assert abs(cm[0,0]-cm[1,1])>1e-3
# Every Hermitian contraction here is a true compressed reflection on a larger
# fixed Hilbert space; square-root dilation does not simulate H.1 preparation.
def reflect(K):
 vals,U=np.linalg.eigh(I4-K@K);R=(U*np.sqrt(vals))@U.T
 return np.block([[K,R],[R,-K]])
I4=np.eye(4);W=reflect(M);Wh=reflect(Mh)
assert np.linalg.norm(W@W-np.eye(8),2)<1e-12 and np.linalg.norm(Wh@Wh-np.eye(8),2)<1e-12
# Similarly close READY effect need not be one exact scalar on every input.
E=.5*I;Eh=E+eps*Z
assert np.linalg.norm(Eh-E,2)<.01000000000001 and np.linalg.eigvalsh(Eh).min()>0 and np.linalg.eigvalsh(Eh).max()<1
out={'status':'PASS_NORM_ONLY_VS_SCALAR_STRUCTURE_HOSTILE','toy_M_norm_error':float(np.linalg.norm(Mh-M,2)),
 'toy_compressed_corner_eigenvalues':[float(x) for x in np.linalg.eigvalsh(cm)],'toy_reflection_norm_error':float(np.linalg.norm(Wh-W,2)),
 'target_ready':0.5,'approx_ready_eigenvalues':[float(x) for x in np.linalg.eigvalsh(Eh)],
 'scope':'finite mathematical counterexamples only; no H1 simulation or statement that A14 violates its required controls',
 'conclusion':'A small norm error alone does not imply exact scalar actual corner or exact scalar READY; preserve T6 structure separately to apply T9-T10.', 'GR_closed':False}
(P/'STRUCTURE_HOSTILE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
