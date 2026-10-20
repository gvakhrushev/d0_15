#!/usr/bin/env python3
"""Exact original full128 two-fresh-tick Jones+ metric10+Lorentz24 tomography.
Keeps both Golden ports, all Walsh labels, true fixed negative words and
Julia Sylvester root jets. Exact 34×34 and 37×37 minors in three algebraic
number-field reductions. Research: selected physical Book price GR OPEN.
"""
import numpy as np

ORDER=(0,2,3,1)
PIN34=[0,27,91,123,1211,49,15674,65,19,2235,89,72,105,25,251,
       185,1049,1184,17,2523,248,2491,2057,1241,2120,2145,6267,
       2280,2448,2536,2544,7419,3096,3387]
PIN37=[0,27,91,123,1211,49,15674,65,19,2235,89,105,11771,185,
       1049,25,251,1184,17,1241,2057,2120,2523,248,2491,2145,
       73,2280,2448,6267,2536,2544,3096,3355,7419,3387,3513]
PRIMES=[(1009,226,469,746,250),(4001,842,899,2021,794),
        (101,27,10,52,33)]

def rankdet(A,q):
    B=A.copy()%q
    rank=0;det=1
    for col in range(B.shape[1]):
        pivot=next((i for i in range(rank,B.shape[0]) if B[i,col]%q),None)
        if pivot is None:continue
        if pivot!=rank:
            B[[pivot,rank]]=B[[rank,pivot]];det=-det
        value=int(B[rank,col]);det=det*value%q
        invvalue=pow(value,-1,q)
        for j in range(rank+1,B.shape[0]):
            coeff=int(B[j,col])*invvalue%q
            B[j,col:]=(B[j,col:]-coeff*B[rank,col:])%q
        rank+=1
    return rank,det%q

def check(q,a,i,want34,want37):
    assert (a**4+a*a-1)%q==0 and (i*i+1)%q==0
    p=a*a%q;nu=3*pow(5,-1,q)%q;b=4*pow(5,-1,q)%q
    assert (p*p+p-1)%q==0
    assert (nu*nu+b*b-1)%q==0
    inv=lambda n:pow(int(n)%q,-1,q)
    eye=np.eye(16,dtype=np.int64)
    zero=np.zeros((16,16),dtype=np.int64)
    mm=lambda x,y:(x@y)%q
    C=[]
    for role in range(4):
        m=zero.copy()
        prior=ORDER[:ORDER.index(role)]
        for bits in range(16):
            if not (bits>>role)&1:
                m[bits+(1<<role),bits]=(-1)**sum(bool(bits&(1<<j)) for j in prior)%q
        C.append(m)
    left=[mm(c,c.T) for c in C]
    right=[mm(c.T,c) for c in C]
    had=np.array([[(-1)**((lab&j).bit_count()) for j in range(32)]
                   for lab in range(32)],dtype=np.int64)
    weight=[(-2*p*p)%q,(-2*a*p)%q]
    psi=np.zeros(16,dtype=np.int64)
    # Literal Jones+ |psi>=(-a(|vac>+|123>)+p(|e0>+|top>))/sqrt(2);
    # drop common 1/sqrt2 ONLY for rank and nonzero determinant checks.
    psi[0]=psi[14]=-a%q
    psi[1]=psi[15]=p
    zlist=[i,i,q-1,(-i)%q]  # legal original L=4 Fourier character

    def root_derivative(projector,delta):
        blocks=[(eye-projector)%q,projector]
        eigen=[1,b]
        out=zero.copy()
        for j in range(2):
            for k in range(2):
                out=(out-inv(eigen[j]+eigen[k])*
                     mm(mm(blocks[j],delta),blocks[k]))%q
        return out

    def e4(j,k):
        X=np.zeros((4,4),dtype=np.int64);X[j,k]=1;return X

    lor=[e4(0,j)+e4(j,0) for j in (1,2,3)]+[
        e4(2,3)-e4(3,2),e4(3,1)-e4(1,3),e4(1,2)-e4(2,1)]
    gens=[]
    for X in lor:
        G=zero.copy()
        for j in range(4):
            for k in range(4):
                if X[j,k]:
                    G=(G+int(X[j,k])*mm(C[j],C[k].T))%q
        gens.append(G)

    def qarray(direction=None):
        words=[[],[]];adjs=[[],[]]
        for role in range(4):
            z=zlist[role]
            v=nu*C[role]%q
            P=nu*z*C[role]%q
            Pd=nu*inv(z)*C[role].T%q
            L=(eye+(b-1)*left[role])%q
            R=(eye+(b-1)*right[role])%q
            if direction is None or direction[1]!=role:
                dP=dPd=dL=dR=dv=zero
            elif len(direction)==2:
                # Actual coframe creator/Dirac leg variation:
                j=direction[0]
                dP=nu*z*C[j]%q
                dPd=nu*inv(z)*C[j].T%q
                dv=nu*C[j]%q
                dL=root_derivative(left[role],nu*nu*
                    (mm(C[j],C[role].T)+mm(C[role],C[j].T))%q)
                dR=root_derivative(right[role],nu*nu*
                    (mm(C[j].T,C[role])+mm(C[role].T,C[j]))%q)
            else:
                # Actual proper link acts on transported P, not the
                # UNTRANSPORTED negative-word creators or their fixed roots.
                G=gens[direction[0]]
                dP=nu*z*mm(C[role],G)%q
                dPd=nu*inv(z)*mm(G.T,C[role].T)%q
                dv=zero
                dL=root_derivative(left[role],
                    (mm(dP,Pd)+mm(P,dPd))%q)
                dR=root_derivative(right[role],
                    (mm(dPd,P)+mm(Pd,dP))%q)
            fixed_dL=dL if (direction is not None and len(direction)==2) else zero
            fixed_dR=dR if (direction is not None and len(direction)==2) else zero
            rows=[
                (P,L,Pd,L,dP,dL,dPd,dL),
                (Pd,R,P,R,dPd,dR,dP,dR),
                ((-v)%q,(-L)%q,(-v.T)%q,(-L)%q,
                 (-dv)%q,(-fixed_dL)%q,(-dv.T)%q,(-fixed_dL)%q),
                ((-v.T)%q,(-R)%q,(-v)%q,(-R)%q,
                 (-dv.T)%q,(-fixed_dR)%q,(-dv)%q,(-fixed_dR)%q)]
            for x,y,xa,ya,dx,dy,dxa,dya in rows:
                for _ in range(2):
                    if direction is None:
                        words[0].append(x);words[1].append(y)
                        adjs[0].append(xa);adjs[1].append(ya)
                    else:
                        words[0].append(dx);words[1].append(dy)
                        adjs[0].append(dxa);adjs[1].append(dya)
        def walsh(xs):
            return ((had@np.stack(xs).reshape(32,256))%q*inv(32)%q).reshape(32,16,16)
        Q=np.empty((64,16,16),dtype=np.int64)
        Qa=np.empty_like(Q)
        for comp in (0,1):
            Q[comp::2]=walsh(words[comp])
            Qa[comp::2]=walsh(adjs[comp])
        return Q,Qa

    def kraus(Q,Qa,A,d=None):
        K=np.empty((128,16,16),dtype=np.int64)
        Ka=np.empty_like(K)
        for j in range(64):
            if d is None:
                value=mm(Qa[j],A); adjoint=mm(A,Q[j])
            else:
                dQ,dQa,dA=d
                value=(mm(dQa[j],A)+mm(Qa[j],dA))%q
                adjoint=(mm(dA,Q[j])+mm(A,dQ[j]))%q
            for port in (0,1):
                K[2*j+port]=weight[port]*value%q
                Ka[2*j+port]=weight[port]*adjoint%q
        if d is None:
            K[0]=(K[0]+eye)%q
            Ka[0]=(Ka[0]+eye)%q
        return K,Ka

    Q,Qa=qarray()
    A=Q[0]
    assert np.array_equal(A,Qa[0])
    K,Ka=kraus(Q,Qa,A)
    total=zero.copy()
    for j in range(128):
        total=(total+mm(Ka[j],K[j]))%q
    assert np.array_equal(total,eye),'Literal full128 baseline completeness'

    records=sorted(set(PIN34+PIN37))
    first=sorted({item//128 for item in records})
    second=sorted({item%128 for item in records})
    states={j:K[j]@psi%q for j in first}
    bras={j:psi@Ka[j]%q for j in first}
    effects={j:mm(Ka[j],K[j]) for j in second}
    J=np.zeros((len(records),40),dtype=np.int64)

    for column in range(40):
        direction=(divmod(column,4) if column<16 else
                   ((column-16)%6,(column-16)//6,1))
        dQ,dQa=qarray(direction)
        dK,dKa=kraus(Q,Qa,A,d=(dQ,dQa,dQ[0]))
        ward=zero.copy()
        for j in range(128):
            ward=(ward+mm(dKa[j],K[j])+mm(Ka[j],dK[j]))%q
        assert np.array_equal(ward,zero),('all40 full128 Ward',q,column)
        deff={j:(mm(dKa[j],K[j])+mm(Ka[j],dK[j]))%q for j in second}
        ds={j:dK[j]@psi%q for j in first}
        db={j:psi@dKa[j]%q for j in first}
        for row,item in enumerate(records):
            j,k=divmod(item,128)
            value=bras[j]@(deff[k]@states[j])
            value+=db[j]@(effects[k]@states[j])
            value+=bras[j]@(effects[k]@ds[j])
            J[row,column]=int(value*inv(2)%q)  # actual normalized Jones pure-state density

    H=np.diag([1,-1,-1,-1]).astype(np.int64)
    def unit(i,j):
        B=np.zeros((4,4),dtype=np.int64);B[i,j]=1;return B
    metric=[]
    for i in range(4):
        for j in range(i,4):
            symmetric=unit(i,j)+(unit(j,i) if i!=j
                                 else np.zeros((4,4),dtype=np.int64))
            metric.append((H@symmetric).reshape(16)%q)
    boosts=[(unit(0,j)+unit(j,0)).reshape(16)%q for j in (1,2,3)]
    rotations=[(unit(i,j)-unit(j,i)).reshape(16)%q
               for i,j in ((1,2),(1,3),(2,3))]
    T=np.stack(metric+boosts+rotations,axis=1)%q
    assert rankdet(T,q)[0]==16
    assert not np.any(J[:,:16]@T[:,13:]%q),'Jones SO3 stabilizer Ward'
    F34=np.c_[J[:,:16]@T[:,:10]%q,J[:,16:]]%q
    F37=np.c_[J[:,:16]@T[:,:13]%q,J[:,16:]]%q
    A34=F34[[records.index(i) for i in PIN34],:]
    A37=F37[[records.index(i) for i in PIN37],:]
    r34,d34=rankdet(A34,q);r37,d37=rankdet(A37,q)
    assert (r34,d34)==(34,want34),(q,r34,d34,want34)
    assert (r37,d37)==(37,want37),(q,r37,d37,want37)
    assert rankdet(J,q)[0]==37
    print('PASS field',q,'metric10+link24 det',d34,
          'coframe16+link24 rank37, 3 SO3 gauge, 37-minor det',d37)
    return d34,d37

if __name__=='__main__':
    for args in PRIMES:
        check(*args)
    print('PASS native full128 SAME Jones preparation & SAME field in BOTH ticks,')
    print('      all40 first-order Kraus completeness, exact metric10+link24 rank34.')
    print('NO CLAIM: compulsory native Jones controller, selected Book03 Cost−Info,')
    print('          Einstein 40-Euler source, matter Ward, uniform GR refinement.')
