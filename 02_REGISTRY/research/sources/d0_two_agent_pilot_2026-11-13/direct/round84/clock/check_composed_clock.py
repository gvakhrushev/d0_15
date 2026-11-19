"""Retained branching clock, real suffix gates and field comparison for A84."""
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path
import sys

from mpmath import iv
import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "d0_native_execution_domain_2026-10-24"))
import native_execution as ne

iv.dps=60
p=(iv.sqrt(5)-1)/2
a=iv.sqrt(p)
x=2*p**2/11
v=np.array([float(a.mid),float(p.mid)])
G=np.array(ne.G_LOCAL,dtype=float)
bit=np.array([[0,1],[1,0]])
cx=np.eye(4)[[0,1,3,2]]
def need(value, message):
    if not value:
        raise ArithmeticError(message)

def enclose(value,low,high):
    need(value.a>iv.mpf(low) and value.b<iv.mpf(high), str(value))

def exact(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(ne.GOLDEN_FIELD).to_dense()

def corrector():
    gate=ne.Gate
    spec=dict(profile=ne.G_CX_SOURCE_I,source_port=2,source_spin=(3,4))
    one=ne.Execution(5,(),(),(gate("G",(1,)),),**spec)
    inv=ne.inverse_word(one,max_qubits=5,max_expanded_stages=32)
    call=inv+(gate("CX",(0,1)),gate("G",(1,)),gate("CX",(0,1)))
    actual=ne.Execution(5,(),(),call,**spec)
    target=sp.kronecker_product(sp.diag(sp.eye(2),ne.G_LOCAL.T**2),sp.eye(8))
    need(len(inv)==11 and len(call)==14,"paid routing and equalization")
    need(exact(ne.word_matrix(actual,max_qubits=5))==exact(target),"all 32 port/Spin columns")
    # Two genuine mid-graph preparations with all the same routed addresses.
    swap=(gate("CX",(1,2)),gate("CX",(2,1)),gate("CX",(1,2)))
    phase=swap+(gate("SourceI",(2,3,4)),)*2+swap
    g=(gate("G",(1,)),)*2
    for w,k in ((phase+phase+g,2),(phase+g+phase,-2)):
        E=ne.Execution(5,(),(),w,**spec)
        want=sp.kronecker_product(sp.eye(2),ne.G_LOCAL**k,sp.eye(8))
        need(len(w)==18 and exact(ne.word_matrix(E,max_qubits=5))==exact(want),"signed true words")

def indicator_reader():
    totals=[]
    probs=[]
    for t in (0,1):
        control=np.eye(2)[t]
        initial=np.kron(control,v)
        moved=cx@initial
        # On each already registered sector, the old field bit stays sharp.
        state=np.kron(moved.reshape(2,2)[t],v)
        def dist(a,b):
            return np.sqrt(max(0.,1.-min(1.,np.dot(a,b)**2)))
        cost=0. if t==0 else dist(initial,moved)
        for op in (cx,np.kron(np.eye(2),G),cx):
            emitted=op@state
            cost+=dist(state,emitted)
            state=emitted
        probs.append([sum(state[:2]**2),state[2]**2,state[3]**2])
        totals.append(cost)
    np.testing.assert_allclose(probs,[[float(p.mid),float((p**2).mid),0.],
                                       [float((p**2).mid),float(p.mid),0.]],atol=2e-15)
    f=lambda u:iv.sqrt(1-(1-(1-2*a*p)*u)**2)
    j=lambda u:iv.sqrt(2*u-u*u)
    delta=p**3+f(p)-f(p**2)+j(p)-j(p**2)
    enclose(delta,".4136426329563",".4136426329565")
    need(abs(totals[1]-totals[0]-float(delta.mid))<3e-14,"paid reader distance")
    return delta

def enumerate_rc3(n,geometry_bits,paired):
    # Every branch range below has the same old rank; entries are passive,
    # without a second Born factor. Test cold masses from actual final vectors.
    nc0=(G@v); nc1=(G.T@v)
    prob=lambda b: (float(p.mid),float((p*p).mid))[b]
    overlap=lambda z: float(np.dot(v,z)**2)
    total=0.
    leaves=0
    for y,old in geometry_bits:
        total+=old*prob(0)*overlap(nc0)
        leaves+=1
        for N in (0,1):
            after=nc1 if N else G.T@G.T@nc0
            np.testing.assert_allclose(after,[1.,0.],atol=1e-15)
            head=prob(1)*overlap(nc1)*prob(N)*overlap(after)*prob(1-N)
            count=4 if paired else 2+n
            for outcomes in product((0,1),repeat=count):
                weight=head
                for b in outcomes:
                    weight*=prob(b)*overlap((nc0,nc1)[b])
                total+=old*weight
                leaves+=1
    expected=(p**2+2*p**(11 if paired else (9+n)))*sum(z for _,z in geometry_bits)
    need(abs(total-float(expected.mid))<1e-13,"complete cold range sum")
    need(leaves==len(geometry_bits)*(33 if paired else (1+2**(3+n))),"occupied rank")
    return leaves,total

def dimension(n,padding):
    # Count the full pre-action workspace at every raw stage, including each
    # of the three full child carriers of NC1. A death leaf still closes.
    @lru_cache(None)
    def program(stage,d,remaining=0):
        def raw(sequence):
            dim=d; out=0
            for letter in sequence:
                out+=dim
                if letter=="B":
                    dim*=2
            return out,dim
        def step(seq,next_stage,k=0):
            count,child=raw(seq)
            return count+program(next_stage,child,k)
        def nc(seq,zero,one):
            count,dim=raw(seq+"BGGGM") # birth of tail, CX G CX, router
            next_cost=sum(program(k,dim,j) for k,j in (zero,one,("pad",0)))
            return count+next_cost
        if stage=="pad":
            return raw("BB"+"G"*padding)[0]
        if stage=="H":
            return nc("B",("field",0),("N",0))
        if stage=="N":
            return nc("B",("NB",0),("NB",0))
        if stage=="NB":
            return step("B"+"G"*(11+2+14),"early",2)
        if stage=="early":
            onward=("early",remaining-1) if remaining>1 else ("field",n)
            return nc("BG",onward,onward)
        if stage=="field":
            # Four-qubit transported Z twice, two G, measure new field head.
            onward=("late",remaining) if remaining else ("pad",0)
            return nc("B"+"G"*18,onward,onward)
        if stage=="late":
            onward=("late",remaining-1) if remaining>1 else ("pad",0)
            return nc("BG",onward,onward)
        raise ValueError(stage)
    return program("H",8)

def main():
    corrector()
    delta=indicator_reader()
    field_bits=[(0,float((p**2).mid)),(1,float((p**3).mid))]
    for n in range(1,7):
        enumerate_rc3(n,field_bits,False)
    enumerate_rc3(1,field_bits,True)
    qdiff=(3*p-4*p**3)**2-p**2
    enclose(qdiff,".4458247200",".4458247201")
    enclose(p**5*qdiff,".04019998992",".04019998994")
    depth=16
    e=2*x**depth/factorial(depth)/(1-x/(depth+1))
    heat=132*e/359
    enclose(heat,"1.0333e-32","1.0334e-32")
    D=dimension(1,depth)
    need(D==228237624 and 425*D==97000990200,"all addressed clock-stage dimensions")
    k=p**2+2*p**10
    z=iv.mpf(1)/2**20
    root_rank=8; leaf_rank=16*17
    J=-(leaf_rank-root_rank)*iv.log(1-z)-root_rank*iv.log(1-z+z*p*k)
    enclose(J,".00025752180505111",".00025752180505113")
    print("actual occupied terminal rank",leaf_rank,"full clock D",D,"Hodge modes",425*D)
    print("cold scalar",float((p*k).mid),"J",float(J.mid),"abs log-heat secant <",float(heat.b))
    binary_h=lambda q:-(q*iv.log(q)+(1-q)*iv.log(1-q))/(-iv.log(p))
    entropy_change=binary_h(p**2+qdiff)-binary_h(p**2)
    length_change=(1+p**5)*qdiff
    enclose(length_change-entropy_change,".9133756654972",".9133756654974")
    root_changes=[length_change-(1+iv.mpf(1)/nu)*entropy_change for nu in (1,2)]
    enclose(root_changes[0],"1.3407266210","1.3407266212")
    enclose(root_changes[1],"1.1270511432","1.1270511434")
    print("whole letter-minus-CQ secant",float((length_change-entropy_change).mid),
          "root ledger main terms",[float(y.mid) for y in root_changes])
    print("physical field secant",float(qdiff.mid),"paid CQ cash difference",float((p**5*qdiff).mid),
          "gate contrast",float(delta.mid))
    print("PASS")

if __name__=="__main__":
    main()
