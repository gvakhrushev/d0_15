#!/usr/bin/env python3
"""EXACT original full128 Jones two-clock coframe/observer quotient.
One L4 k=(i,i,-1,-i); ALL 128 Kraus/round, native Walsh/Golden/Julia roots;
two exact finite-field minors: relative rank16 and same-geometry SO3 rank13.
Research-only: native physical preparation/Book03 action/GR unproved.
"""
import numpy as np
PRIMES={1009:(226,469),4001:(842,899),101:(27,10)}
REL=[0,19,65,91,123,2523,105,4251,4347,9371,2491,49,6363,8443,1211,2235]
JOINT=[0,2432,8320,91,27,7552,4224,15674,4251,9371,49,11771,2536]
ORDER=(0,2,3,1)

def rankmod(A,q):
    B=A.copy();rank=0;det=1
    for col in range(B.shape[1]):
        pivot=next((i for i in range(rank,B.shape[0]) if B[i,col]%q),None)
        if pivot is None:continue
        if pivot!=rank:
            B[[rank,pivot]]=B[[pivot,rank]];det=-det
        d=int(B[rank,col]);det=det*d%q
        scale=pow(d,-1,q)
        for j in range(rank+1,B.shape[0]):
            fac=int(B[j,col])*scale%q
            B[j,col:]=(B[j,col:]-fac*B[rank,col:])%q
        rank+=1
    return rank,det%q

def check(q,a,i):
    assert (a**4+a*a-1)%q==0 and (i*i+1)%q==0
    p=a*a%q;nu=3*pow(5,-1,q)%q;b=4*pow(5,-1,q)%q
    assert (p*p+p-1)%q==0 and (nu*nu+b*b-1)%q==0
    inv=lambda n:pow(int(n)%q,-1,q)
    eye=np.eye(16,dtype=np.int64);zero=np.zeros((16,16),dtype=np.int64)
    mm=lambda x,y:(x@y)%q
    C=[]
    for role in range(4):
        m=zero.copy();prior=ORDER[:ORDER.index(role)]
        for bits in range(16):
            if (bits>>role)&1==0:
                m[bits+(1<<role),bits]=(-1)**sum(bool(bits&(1<<j)) for j in prior)%q
        C.append(m)
    left=[mm(c,c.T) for c in C];right=[mm(c.T,c) for c in C]
    had=np.array([[(-1)**((row&j).bit_count()) for j in range(32)]
                  for row in range(32)],dtype=np.int64)
    weight=[(-2*p*p)%q,(-2*a*p)%q]
    psi=np.zeros(16,dtype=np.int64)
    psi[0]=psi[14]=-a%q;psi[1]=psi[15]=p # original Jones+, sqrt2 irrelevant to rank
    phases=[i,i,q-1,(-i)%q]
    def root_derivative(proj,delta):
        qs=[(eye-proj)%q,proj];eig=[1,b];out=zero.copy()
        for ix in range(2):
            for jx in range(2):
                out=(out-inv(eig[ix]+eig[jx])*
                     mm(mm(qs[ix],delta),qs[jx]))%q
        return out
    def qarray(pos=None):
        words=[[],[]];adj=[[],[]]
        for role in range(4):
            z=phases[role];v=nu*C[role]%q
            P=nu*z*C[role]%q;Pdag=nu*inv(z)*C[role].T%q
            L=(eye+(b-1)*left[role])%q
            R=(eye+(b-1)*right[role])%q
            if pos is None or pos[1]!=role:
                dP=dPd=dL=dR=dv=zero
            else:
                j=pos[0]
                dP=nu*z*C[j]%q;dPd=nu*inv(z)*C[j].T%q;dv=nu*C[j]%q
                dL=root_derivative(left[role],nu*nu*
                    (mm(C[j],C[role].T)+mm(C[role],C[j].T))%q)
                dR=root_derivative(right[role],nu*nu*
                    (mm(C[j].T,C[role])+mm(C[role].T,C[j]))%q)
            arr=[(P,L,Pdag,L,dP,dL,dPd,dL),
                 (Pdag,R,P,R,dPd,dR,dP,dR),
                 ((-v)%q,(-L)%q,(-v.T)%q,(-L)%q,
                  (-dv)%q,(-dL)%q,(-dv.T)%q,(-dL)%q),
                 ((-v.T)%q,(-R)%q,(-v)%q,(-R)%q,
                  (-dv.T)%q,(-dR)%q,(-dv)%q,(-dR)%q)]
            for x,y,xa,ya,dx,dy,dxa,dya in arr:
                for _ in range(2):
                    if pos is None:
                        words[0].append(x);words[1].append(y)
                        adj[0].append(xa);adj[1].append(ya)
                    else:
                        words[0].append(dx);words[1].append(dy)
                        adj[0].append(dxa);adj[1].append(dya)
        def transform(xs):
            return ((had@np.stack(xs).reshape(32,256))%q*
                    inv(32)%q).reshape(32,16,16)
        Q=np.empty((64,16,16),dtype=np.int64);Qa=np.empty_like(Q)
        for side in (0,1):
            Q[side::2]=transform(words[side])
            Qa[side::2]=transform(adj[side])
        return Q,Qa
    def makeK(Q,Qa,A,d=None):
        K=np.empty((128,16,16),dtype=np.int64);Ka=np.empty_like(K)
        for j in range(64):
            if d is None:
                v=mm(Qa[j],A);w=mm(A,Q[j])
            else:
                dQ,dQa,dA=d
                v=(mm(dQa[j],A)+mm(Qa[j],dA))%q
                w=(mm(dA,Q[j])+mm(A,dQ[j]))%q
            for port in (0,1):
                K[2*j+port]=weight[port]*v%q
                Ka[2*j+port]=weight[port]*w%q
        if d is None:
            K[0]=(K[0]+eye)%q;Ka[0]=(Ka[0]+eye)%q
        return K,Ka
    Q,Qa=qarray();A=Q[0]
    assert np.array_equal(A,Qa[0])
    K,Ka=makeK(Q,Qa,A)
    normalization=zero.copy()
    for j in range(128):
        normalization=(normalization+mm(Ka[j],K[j]))%q
    assert np.array_equal(normalization,eye)
    selected=set(REL+JOINT)
    first=sorted({j//128 for j in selected})
    second=sorted({j%128 for j in selected})
    states={j:K[j]@psi%q for j in first}
    bras={j:psi@Ka[j]%q for j in first}
    effects={j:mm(Ka[j],K[j]) for j in second}
    relative=np.empty((16,16),dtype=np.int64)
    joint=np.empty((13,16),dtype=np.int64)
    for ci in range(16):
        dQ,dQa=qarray(divmod(ci,4))
        dK,dKa=makeK(Q,Qa,A,d=(dQ,dQa,dQ[0]))
        dEffect={j:(mm(dKa[j],K[j])+mm(Ka[j],dK[j]))%q
                 for j in second}
        dstate={j:dK[j]@psi%q for j in first}
        dbra={j:psi@dKa[j]%q for j in first}
        for mat,rows,both in ((relative,REL,False),(joint,JOINT,True)):
            for ri,record in enumerate(rows):
                x,y=divmod(record,128)
                v=bras[x]@(dEffect[y]@states[x])
                if both:
                    v+=dbra[x]@(effects[y]@states[x])+bras[x]@(effects[y]@dstate[x])
                mat[ri,ci]=int(v%q)
    for a1,b1 in ((6,9),(7,13),(11,14)):
        assert np.array_equal(joint[:,a1],joint[:,b1])
    r16,det16=rankmod(relative,q)
    r13,det13=rankmod(joint,q)
    assert r16==16 and det16!=0,(q,r16,det16)
    assert r13==13 and det13!=0,(q,r13,det13)
    print('q',q,'relative16 det',det16,'sameSO3 rank13 det',det13)

if __name__=='__main__':
    for q,(a,i) in PRIMES.items():check(q,a,i)
    print('PASS native full128 two-tick Jones: relative16 + common-SO3 quotient13')
    print('GR_closed=false; fundamental Book price/physical preparation unproved')
