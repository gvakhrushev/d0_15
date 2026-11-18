#!/usr/bin/env python3
"""Bounded numerical control for nodewise entropy, not a native instrument."""
import itertools,json,math
import numpy as np

def need(x,msg):
 if not bool(x):raise AssertionError(msg)
checks=[]
def ck(x,name):need(x,name);checks.append(name)
I=np.eye(2); X=np.array([[0.,1.],[1.,0.]]);Z=np.diag([1.,-1.])
q=np.array([.23,.72,.47]);delta=np.array([.08,.06,.09])
axes=[Z,(X+Z)/math.sqrt(2),X]
E=[q[j]*I+delta[j]*axes[j] for j in range(3)]
ck(all(np.linalg.norm(E[i]@E[j]-E[j]@E[i])>1e-4 for i,j in ((0,1),(1,2),(0,2))), 'three actual effects are pairwise noncommuting')
def sqrt_psd(M):
 w,v=np.linalg.eigh((M+M.conj().T)/2)
 need(np.min(w)>-1e-12,'positive operator')
 return (v*np.sqrt(np.maximum(w,0)))@v.conj().T
def entropy(M):
 w=np.linalg.eigvalsh((M+M.conj().T)/2)
 need(np.min(w)>-1e-12,'positive state')
 w=w[w>1e-14]
 return float(-np.sum(w*np.log(w)))
def h(x):return -x*math.log(x)-(1-x)*math.log(1-x)
K=[(sqrt_psd(I-e),sqrt_psd(e)) for e in E]
for j in range(3):
 ck(np.linalg.norm(K[j][0].conj().T@K[j][0]+K[j][1].conj().T@K[j][1]-I)<1e-13,f'block {j} is trace preserving')
bell=np.array([1.,0.,0.,1.])/math.sqrt(2);psi=np.outer(bell,bell)
states=[psi,.63*psi+.37*np.eye(4)/4,np.eye(4)/4,np.diag([1.,0.,0.,0.])]
L=np.array([max(abs(math.log((1-(q[j]-delta[j]))/(q[j]-delta[j]))),
                     abs(math.log((1-(q[j]+delta[j]))/(q[j]+delta[j])))) for j in range(3)])
bound=float(np.sum(L*delta));target=sum(h(x) for x in q)
largest=0.
for si,rho in enumerate(states):
 weights=[];branches=[]
 for bits in itertools.product((0,1),repeat=3):
  U=np.eye(4)
  for j,b in enumerate(bits):U=np.kron(K[j][b],I)@U
  block=U@rho@U.conj().T;branches.append(block);weights.append(float(np.trace(block).real))
 weights=np.array(weights);need(abs(np.sum(weights)-1)<1e-12,'joint probability normalization')
 iq=sum(entropy(block) for block in branches)-entropy(rho)
 hc=float(-sum(v*math.log(v) for v in weights if v>0))
 for value,name in ((iq,'retained CQ'),(hc,'full classical')):
  err=abs(value-target);largest=max(largest,err)
  ck(err<=bound+1e-12,f'{name} nodewise bound for state {si}')
for bq,bc in ((0.,0.),(.3,.7),(10.,2.)):
 qbound=float(np.sum((1+(bq+bc)*L/math.log((1+math.sqrt(5))/2))*delta))
 for si,rho in enumerate(states):
  probs=[];branches=[]
  for bits in itertools.product((0,1),repeat=3):
   U=np.eye(4)
   for j,b in enumerate(bits):U=np.kron(K[j][b],I)@U
   block=U@rho@U.conj().T;branches.append(block);probs.append(float(np.trace(block).real))
  probs=np.array(probs)
  actual_cost=sum(probs[k]*sum(1+b for b in bits) for k,bits in enumerate(itertools.product((0,1),repeat=3)))
  iq=sum(entropy(block) for block in branches)-entropy(rho)
  hc=float(-sum(v*math.log(v) for v in probs if v>0))
  ref_cost=3+sum(q);ell=math.log((1+math.sqrt(5))/2)
  error=abs((actual_cost-(bq*iq+bc*hc)/ell)-(ref_cost-(bq+bc)*target/ell))
  ck(error<=qbound+1e-12,f'price error bound state {si} weights {bq},{bc}')
print(json.dumps({'status':'PASS_NUMERIC_DIAGNOSTIC','check_count':len(checks),'checks':checks,
 'entropy_bound':bound,'largest_entropy_error':largest,'effect_centres':q.tolist(),
 'effect_radii':delta.tolist(),'scope':'noncommuting abstract effects and retained qubit/reference outcomes; not a native compiler or physical task admission'},indent=2))
