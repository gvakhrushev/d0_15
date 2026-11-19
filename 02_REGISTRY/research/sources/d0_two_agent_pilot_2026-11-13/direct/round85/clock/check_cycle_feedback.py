"""Fixed-port two-slot query, normalized marked ranges and the measured dilation."""
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path
import sys
import numpy as np
from mpmath import iv

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'round84'/'assembly'))
from check_retained_replicas import Golden, a, p, one, ne, action, rotation, phase_word

iv.dps=75
P=(iv.sqrt(5)-1)/2
A=iv.sqrt(P)
theta=iv.atan2(P,A)
z=iv.mpf(1)/2**20
modes=((2,2),(2,3))

def need(b,msg):
    if not b: raise ArithmeticError(msg)

def inside(x,lo,hi):
    need(x.a>iv.mpf(lo) and x.b<iv.mpf(hi),str(x))

@lru_cache(None)
def native_word():
    spec=ne.Execution(6,(5,),(),(),ne.G_CX_SOURCE_I,2,(0,1))
    word=tuple(g for k,j in product(range(2),repeat=2) for g in
               phase_word(spec,(3,4),(k,j),5,modes[k][j],max_qubits=6,max_expanded_stages=500))
    need(2*(len(word)+3)==422,"true raw chronology")
    for g in word:
        if 4 in g.wires:
            need(g.op=="CX" and g.wires[0]==4,"slot address used only as control")
    for col in range(64):
        k,j,b=(col>>2)&1,(col>>1)&1,col&1
        c,s=rotation(modes[k][j])
        psi={col:one}
        for g in word:
            psi=action(psi,g,6)
        need(psi=={col:c,col^1:(-s if b else s)},"all pointer/dirty source columns")
    return word

def trigonometric(k):
    return ([iv.cos(4*theta*n) for n in modes[k]],
            [iv.sin(4*theta*n) for n in modes[k]])

def lane(k,e):
    c,s=trigonometric(k)
    mean=lambda row: P*row[0]+e*P**2*row[1]
    q=P*s[0]**2+P**2*s[1]**2
    C,S=mean(c),mean(s)
    return q,C,S

def feedback(k,e1,e2):
    q,C,S=lane(k,e1)
    _,c,s=lane(1-k,e2)
    b=A*c+P*s
    marked=P*b**2*(P*C**2/(1-q)+P**2*S**2/q)
    eig=[(A*b*(A*P*C+sign*P**3*S))**2 for sign in (1,-1)]
    return q,marked,eig

def direct_complete_instrument(k,signs):
    # Direct normalized full quantum vectors, not scalar thermal weights.
    pp=float(P.mid); aa=float(A.mid); v=np.array([aa,pp]); g=np.array([[aa,-pp],[pp,aa]])
    def real_slot(i,e):
        C,S=trigonometric(i)
        columns=[np.array([float(c.mid),float(s.mid)]) for c,s in zip(C,S)]
        return np.vstack((aa*columns[0],e*pp*columns[1]))
    psi=real_slot(k,signs[0])
    other=real_slot(1-k,signs[1])
    # Store coordinates in order J1, pointer1, J2, pointer2, NC1-tail.
    eta=np.kron(np.kron(v,v),np.kron(np.kron(v,v),v))
    tagged=[]
    amplitudes=[]
    for b in (0,1):
        reduced=np.kron(np.outer(psi[:,b],np.eye(2)[b]).ravel(),other.ravel())
        after=np.kron(reduced,(g@v,g.T@v)[b])
        norm=np.linalg.norm(after)
        tagged.append(after)
        amplitudes.append(np.dot(eta,after/norm))
    q,sharp,eigs=feedback(k,*signs)
    need(abs(np.vdot(tagged[1],tagged[1])-float(q.mid))<1e-14,"actual one-read probability")
    need(abs(sum(x*x for x in amplitudes)-float(sharp.mid))<2e-14,"both normalized occupied ranges")
    # Serial dilation: E is the canonical incoming v on every born line.
    # The two flags e,f are independent true zeros before copying. See native
    # inverse compiler below. At the end they both store b and tail is zero.
    I=np.eye(2); X=I[::-1]
    old=np.eye(16)
    kernels=[]
    for b in (0,1):
        pointer=np.kron(np.outer(psi[:,b],I[b]).ravel(),other.ravel())
        env=np.kron(np.array([1.,0.]),np.kron(I[b],I[b]))
        unit=old if b==0 else np.kron(X,np.eye(8))
        kernels.append(np.einsum('x,ab->xab',np.kron(pointer,env),unit))
    serial=kernels[0]+kernels[1]
    cold_inputs=np.kron(np.kron(np.kron(v,v),np.kron(v,v)),np.kron(v,np.kron(v,v)))
    cold=np.einsum('x,xij->ij',cold_inputs,serial)
    need(np.max(np.abs(np.einsum('xab,xac->bc',serial,serial)-old))<2e-14,"old target with full spin")
    actual=np.linalg.eigvalsh(np.einsum("ki,kj->ij",cold,cold))
    np.testing.assert_allclose(actual,np.sort(np.repeat([float(ev.mid) for ev in eigs],8)),atol=2e-15)
    for b in (0,1):
        left=kernels[b].copy()
        chosen=np.arange(serial.shape[0])%2==b  # e is lowest new coordinate
        np.testing.assert_allclose(serial*chosen[:,None,None],left,atol=1e-15)

def true_record_word():
    # Verify the rest of the physical flag/target/dump scheme separately on
    # all dirty target/port/spin columns, for both normalized NC1 sectors.
    # 0,1 Spin; 2 PORT; 3 already cut pointer; 4 old target;
    # 5 live NC1 tail, 6 first copied flag, 7 sealed record.
    gate=ne.Gate
    context=ne.Execution(8,(5,6,7),(),(),ne.G_CX_SOURCE_I,2,(0,1))
    def inverse(q):
        word=ne.Execution(8,(5,6,7),(),(gate("G",(q,)),),ne.G_CX_SOURCE_I,2,(0,1))
        return tuple(ne.inverse_word(word,max_qubits=8,max_expanded_stages=100))
    nc=(gate('CX',(3,5)),gate('G',(5,)),gate('CX',(3,5)))
    stages=(('B',5),)+nc+(('B',6),)+inverse(6)+(gate('CX',(3,6)),('B',7))+inverse(7)+(
        gate('CX',(6,7)),gate('CX',(6,4)))+inverse(5)+(gate('CX',(6,5)),)+inverse(5)+(gate('CX',(6,5)),)
    def birth(state,q):
        bit=1<<(7-q); ans={}
        for i,v in state.items():
            need(not (i&bit),"canonical birth must use new wire")
            ans[i]=a*v; ans[i|bit]=p*v
        return ans
    for col in range(32):
        b=(col>>1)&1
        psi={col<<3:one}
        for gate in stages:
            psi=birth(psi,gate[1]) if isinstance(gate,tuple) else action(psi,gate,8)
        # All three final ancilla values are (0,b,b).
        expected=(col<<3)^(b<<3)^(b<<1)^b
        need(psi=={expected:one},"real compiled conditional target and retained f,e")

def matched_full_range():
    # Inverse the native one-slot compiler, including every routed SourceI,
    # then check both signs on all six-wire input columns.
    word=native_word()
    spec=ne.Execution(6,(5,),(),word,ne.G_CX_SOURCE_I,2,(0,1))
    inverse=ne.inverse_word(spec,max_qubits=6,max_expanded_stages=7000)
    for col in range(64):
        k,j,b=(col>>2)&1,(col>>1)&1,col&1
        C,S=rotation(modes[k][j])
        psi={col:C,col^1:(-S if b else S)}
        for gate in inverse:
            psi=action(psi,gate,6)
        need(psi=={col:one},"native inverse on full true query columns")
    # Build each actual four-wire block, after passive birth, including the
    # native inverse bringing the pointers' canonical v to real zeros.
    v=np.array([float(A.mid),float(P.mid)])
    e0=np.array([1.,0.]); G=np.array([[v[0],-v[1]],[v[1],v[0]]])
    blank=np.kron(np.kron(v,v),np.kron(v,v))
    mask=(np.arange(16)&4)!=0
    gs=[]
    for k in (0,1):
        slot=[]
        for c,s in zip(*trigonometric(k)):
            R=np.array([[float(c.mid),-float(s.mid)],[float(s.mid),float(c.mid)]])
            slot.append(np.einsum('ij,jk->ik',R,G.T))
        M=np.zeros((4,4))
        M[:2,:2]=slot[0];M[2:,2:]=slot[1];gs.append(M)
    report=[]
    for k in range(2):
        matrix=np.kron(gs[k],gs[1-k])
        actual=np.einsum('ij,j->i',matrix,blank)
        c=[]
        for b in (0,1):
            back=np.einsum('ij,i->j',matrix,actual*(mask==b))
            c.append(np.dot(blank,back))
        q=feedback(k,1,1)[0]
        np.testing.assert_allclose(c,[1-float(q.mid),float(q.mid)],atol=1e-14,rtol=0.)
        returned=A*(P*c[0]+P**2*c[1])
        need(abs(returned**2-P*(P-P**3*q)**2).b<2e-15,"serial matched amplitude")
        marked=P*(P**2*c[0]+P**4*c[1])
        need(abs(marked-P*(P**2*(1-q)+P**4*q)).b<2e-15,"single external register")
        report.append(-8*iv.log(1-z+z*P*(P-P**3*q)**2))
    inside(report[1]-report[0],"1.19908937e-7","1.19908939e-7")
    # The retained environment flag distinguishes outputs even after restoring
    # all query wires; an external read only on e commutes with query inverse.

def bounds():
    for k in range(2):
        for signs in ((1,1),(1,-1),(-1,1)):
            direct_complete_instrument(k,signs)
    for j,expected in enumerate((".0161131194792",".00040159097546")):
        v=feedback(j,1,1)[1]
        need(abs(v-iv.mpf(expected)).b<iv.mpf("2e-14"),"original marked cold")
    h0,h1=[feedback(j,1,1)[1] for j in (0,1)]
    dif=P**6*(h1-h0)
    inside(dif,"-.0008755734746","-.0008755734744")
    # H=0 also does the same neutral readout at the end; it contributes p^2.
    positive=-8*iv.log((1-z+z*(P**2+P**6*h1))/(1-z+z*(P**2+P**6*h0)))
    inside(positive,"6.68008e-9","6.68012e-9")
    # Dual numbers through algebraic polynomial factors. At t=0 the two
    # passive projections have respective derivatives -sin(alpha), +sin(alpha).
    e=iv.cos(2*theta); speed=iv.sin(2*theta)
    q,C,S=lane(0,e); _,c,s=lane(1,e)
    cs,ss=trigonometric(0); cu,su=trigonometric(1)
    dc=-P**2*speed*cs[1]; ds=-P**2*speed*ss[1]
    b=A*c+P*s; db=P**2*speed*(A*cu[1]+P*su[1])
    v=P*C*C/(1-q)+P**2*S*S/q
    dv=2*P*C*dc/(1-q)+2*P**2*S*ds/q
    marked=P*b*b*v; dm=P*(2*b*db*v+b*b*dv)
    dj=-8*z*dm/(1-z+z*marked)
    inside(dm,".0016713584931",".0016713584934")
    inside(dj,"-1.275147e-8","-1.275146e-8")
    ser=iv.mpf(0)
    for sg in (1,-1):
        h=A*b*(A*P*C+sg*P**3*S)
        dh=A*db*(A*P*C+sg*P**3*S)+A*b*(A*P*dc+sg*P**3*ds)
        ser-=8*z*2*h*dh/(1-z+z*h*h)
    inside(ser,"-2.963177e-9","-2.963175e-9")
    # One actual native small angular secant (two-control words capped separately).
    m=93997; eps=2*m*theta
    eps-=2*iv.pi*round(float((eps/(2*iv.pi)).mid))
    inside(abs(eps),"0.0000412","0.0000415")
    jvals=[]; svals=[]
    for sign in (1,-1):
        _,h,ss=feedback(0,iv.cos(2*theta+sign*eps),iv.cos(2*theta-sign*eps))
        jvals.append(-8*iv.log(1-z+z*h))
        svals.append(-8*sum(iv.log(1-z+z*y) for y in ss))
    inside((jvals[0]-jvals[1])/(2*eps),"-1.275147e-8","-1.275146e-8")
    inside((svals[0]-svals[1])/(2*eps),"-2.963177e-9","-2.963175e-9")
    x=2*P**2/11
    err=iv.mpf(264)/359*x**16/factorial(16)/(1-x/17)
    inside(err,"1.0333e-32","1.0334e-32")
    print("two marked cold scalars",*[float(v.mid) for v in (h0,h1)])
    print("one common root, opened source",float(positive.mid))
    print("fixed signal; marked and serial full J slopes",float(dj.mid),float(ser.mid))
    print("PASS")

if __name__=="__main__":
    native_word()
    true_record_word()
    matched_full_range()
    bounds()
