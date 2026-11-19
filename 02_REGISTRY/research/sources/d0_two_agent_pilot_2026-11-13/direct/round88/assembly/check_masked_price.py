"""One paid random phase, local work marginals, and a retained source for the full record."""
from fractions import Fraction as F
from itertools import product
import json
import math

import numpy as np
from mpmath import iv

iv.dps=65
p=(math.sqrt(5)-1)/2
v=np.array([math.sqrt(p),p])
G=np.array([[v[0],-v[1]],[v[1],v[0]]])
X=np.eye(2)[[1,0]]
Z=np.diag([1.,-1.])
phi=(1+math.sqrt(5))/2


def need(test,name):
    if not test:
        raise ArithmeticError(name)


def close(x,y,name):
    need(np.max(np.abs(x-y))<3e-13,name)


def gate(state,op,*targets):
    other=[k for k in range(state.ndim) if k not in targets]
    axes=list(targets)+other
    flat=state.transpose(axes).reshape(len(op),-1)
    result=np.einsum("ij,jk->ik",op,flat)
    return result.reshape(state.shape).transpose(np.argsort(axes))


def marginal(state,*targets):
    other=[k for k in range(state.ndim) if k not in targets]
    flat=state.transpose(list(targets)+other).reshape(2**len(targets),-1)
    return np.einsum("ij,kj->ik",flat,flat.conj())


CX=np.eye(4)[[0,1,3,2]]
def rotation(t):
    return np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])


def entropy(x):
    return -sum(t*math.log(t)/math.log(phi) for t in (x,1-x) if t)


def prepare_pair():
    # Zero for the marker is obtained using the paid inverse of G.
    old=np.einsum("a,r,b->arb",v,v,np.einsum("ij,j->i",G.T,v))
    for lines in [(0,2),(1,2)]:
        old=gate(old,CX,*lines)
    split=old[:,:,1]
    eta=np.sum(split**2)
    close(eta,2*p**3,"physical odd herald")
    # The odd flag is a physically known 1, used as a control for X on the reference.
    plus=gate(split/math.sqrt(eta),X,1)
    close(plus,np.eye(2)/math.sqrt(2),"heralded Phi+")
    return plus


def experiment(pair,delta,j):
    # Target A, reference R, and true NC1 tail in v. Old spectators factor.
    psi=np.einsum("ar,f->arf",pair,v)
    if j:
        psi=gate(psi,Z,0)
        psi=gate(psi,X,0)
    psi=gate(psi,rotation(delta),0)
    check=[marginal(psi,0,1)]
    psi=gate(psi,CX,1,0)
    check.append(marginal(psi,1,0))
    psi=gate(psi,CX,0,2)
    check.append(marginal(psi,0,2))
    psi=gate(psi,G,2)
    check.append(marginal(psi,2))
    psi=gate(psi,CX,0,2)
    check.append(marginal(psi,0,2))
    prob=np.sum(psi[1]**2)
    leaves=[]
    for t in range(2):
        leaf=psi.copy()
        leaf[1-t]=0
        mass=np.sum(leaf**2)
        leaves.append(marginal(leaf/math.sqrt(mass),0,1,2))
    return prob,check,leaves


def audit():
    pair=prepare_pair()
    ref=None
    samples=[]
    conditional=[]
    for d in (.30,.35,.40,.45):
        out=[experiment(pair,d,j) for j in (0,1)]
        probs=[s[0] for s in out]
        avg=[(x+y)/2 for x,y in zip(out[0][1],out[1][1])]
        close(np.array(probs),np.array([math.sin(d)**2,math.cos(d)**2]),"signed phase probability")
        if ref is None:
            ref=(avg,out[0][2])
        for i,mat in enumerate(avg):
            close(mat,ref[0][i],"field-dependent CW1 decoder marginal")
        for _,_,leaves in out:
            for i,mat in enumerate(leaves):
                close(mat,ref[1][i],"normalized FULL terminal range")
        q=probs[0]
        conditional.append(sum(entropy(qj) for qj in probs)/2)
        samples.append([d,q,conditional[-1]])
    need(np.all(np.diff(conditional)>0),"field entropy")
    # If a physical postgate charge can read the secret phase j, a local projector detects q/2.
    need(abs((samples[-1][1]-samples[0][1])/2)>0.04,"local charge with archive access")
    return samples, len(ref[0])


def address_mask():
    # For each slot and for either single-bit name, preserve the distribution over physical addresses.
    for y in (0,1):
        first=[y^b for b in (0,1)]
        second=[b for b in (0,1)]
        need(sorted(first)==sorted(second)==[0,1],"one-event address trace")
        need(all((f^s)==y for f,s in zip(first,second)),"full query/retained name")
    for y,r,k0,k1,t in product(range(2),repeat=5):
        key=[k0,k1]
        key[y^r] ^= 1
        new_t = t ^ key[1^r]
        key[y^r] ^= 1
        new_t ^= key[1^r]
        need(key==[k0,k1] and new_t==t^y,"single masked query on dirty rails")
    # A paid pair of address events can read their joint correlation.
    need([(sum((y^b)==b for b in (0,1))) for y in (0,1)]==[2,0],"address pair")


def clock_bound():
    # Strict lower bound for h_phi'(sin^2 d) sin(2d) on the whole arc. Choose a
    # terminal service length using the actual joint positive admission mass.
    d=iv.mpf(["0.30","0.45"]); q=iv.sin(d)**2
    slope=iv.log((1-q)/q)/iv.log((1+iv.sqrt(5))/2)*iv.sin(2*d)
    need(slope.a>1,"honest entropy slope")
    # Example: four mixed physical rails, one registered mask and one registered phase.
    eta=2*((iv.sqrt(5)-1)/2)**3
    alpha=eta**6
    x=F(1,11)
    L=2
    while float(F(132,359)*x**L/F(math.factorial(L-1))/(1-x/L)) >= float(alpha.a)/2:
        L+=2
    return L


if __name__=="__main__":
    samples,n=audit()
    address_mask()
    print(json.dumps(dict(paid_input_pair_success="2*p^3",mixed_core_and_reference=True,
          phase_outcomes=2,quantum_decoder_marginals_per_phase=n,uniform_record_probability=.5,
          conditional_entropy_in_phi_units=samples,all_normalized_leaf_ranges_fixed=True,
          example_sufficient_even_final_service=clock_bound(),
          full_fine_record_needed=True,per_history_nonlinear_weight_selected=False,
          GR_closed=False),indent=2))
