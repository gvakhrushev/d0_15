#!/usr/bin/env python3
"""Exact full128 support-safe Hellinger native mixed-rank certification.

Exact original 34/37 Jones Kraus owner below with derivative-capture-only
hooks; independently classify all chronological 128² Kraus amplitudes over
Z[a,i]/(a^4+a²-1,i²+1), then certify Hellinger 10x10/3x3 minors in 3 fields.
No native selected Book03 action or Palatini coefficient match is claimed.

Original owner:
Keeps both Golden ports, all Walsh labels, true fixed negative words and
Julia Sylvester root jets. Exact 34×34 and 37×37 minors in three algebraic
number-field reductions. Research: selected physical Book price GR OPEN.
"""
import numpy as np

ORDER=(0,2,3,1)
PIN34=[0,2432,9344,13440,4224,91,7296,17,59,15488,123,10368,41,9,
       89,49,8320,25,3456,2459,2451,2555,65,12416,5248,97,14464,
       7571,11667,5339,4315,3323,11675,7387]
PIN37=[0,2432,9344,4224,13440,17,89,91,59,7296,123,15488,9,41,
       10368,49,8320,25,27,2459,2451,2523,12416,65,5248,97,14464,
       2489,7571,15763,2555,5339,4315,3323,7579,11707,7387]
PRIMES=[(1009,226,469,360,541),(4001,842,899,1510,3401),
        (101,27,10,91,13)]

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
    dKstore=[];dKastore=[]

    for column in range(40):
        direction=(divmod(column,4) if column<16 else
                   ((column-16)%6,(column-16)//6,1))
        dQ,dQa=qarray(direction)
        dK,dKa=kraus(Q,Qa,A,d=(dQ,dQa,dQ[0]))
        dKstore.append(dK);dKastore.append(dKa)
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
    certify_hellinger(q,a,i,K,Ka,psi,dKstore,dKastore)
    return d34,d37


# TRUE char-0 support: K_even=I_(j=0)-(1-a²) M_j/12800,
# K_odd=-a³ M_j/12800, M_j=Qnum_j†Qnum_0, Qnum=160 Q.
# Coefficients are Gaussian integers; no rounding/float thresholds.
_EXACT_SUPPORT=None
def exact_support():
    global _EXACT_SUPPORT
    if _EXACT_SUPPORT is not None:return _EXACT_SUPPORT
    C=[]
    for role in range(4):
        c=np.zeros((16,16),dtype=np.int64);prior=ORDER[:ORDER.index(role)]
        for bits in range(16):
            if not bits&(1<<role):
                c[bits|(1<<role),bits]=(-1)**sum(bool(bits&(1<<j)) for j in prior)
        C.append(c)
    eye=np.eye(16,dtype=np.int64);words=[[],[]]
    for role,z in enumerate((1j,1j,-1,-1j)):
        c=C[role];P=3*z*c;Pd=P.conj().T
        L=5*eye-c@c.T;R=5*eye-c.T@c
        for x,y in ((P,L),(Pd,R),(-3*c,-L),(-3*c.T,-R)):
            for _ in range(2):words[0].append(x);words[1].append(y)
    had=np.array([[(-1)**((j&k).bit_count()) for k in range(32)]
                  for j in range(32)],dtype=np.int64)
    qn=np.empty((64,16,16),dtype=complex)
    for comp in (0,1):
        qn[comp::2]=np.einsum('ab,bij->aij',had,np.array(words[comp]))
    M=np.einsum('aij,jk->aik',qn.conj().transpose(0,2,1),qn[0])
    mr=np.rint(M.real).astype(np.int64);mi=np.rint(M.imag).astype(np.int64)
    assert np.array_equal(M,mr+1j*mi)
    psi=np.zeros((9,16),dtype=np.int64)
    psi[1,0]=psi[1,14]=-1;psi[2,1]=psi[2,15]=1
    sr=np.zeros((9,128,16),dtype=np.int64);si=np.zeros_like(sr)
    for j in range(128):
        if j==0:sr[:,j,:]+=12800*psi
        re=(mr[j//2]@psi.T).T;im=(mi[j//2]@psi.T).T
        if j%2==0:
            sr[:,j,:]-=re;si[:,j,:]-=im
            sr[2:,j,:]+=re[:-2];si[2:,j,:]+=im[:-2]
        else:
            sr[3:,j,:]-=re[:-3];si[3:,j,:]-=im[:-3]
    wr=np.zeros((9,128,128,16),dtype=np.int64);wi=np.zeros_like(wr)
    for k in range(128):
        if k==0:wr[:,:,k,:]+=12800*sr;wi[:,:,k,:]+=12800*si
        x,y=mr[k//2],mi[k//2]
        re=(np.einsum('ij,daj->dai',x,sr,optimize=True)
            -np.einsum('ij,daj->dai',y,si,optimize=True))
        im=(np.einsum('ij,daj->dai',x,si,optimize=True)
            +np.einsum('ij,daj->dai',y,sr,optimize=True))
        if k%2==0:
            wr[:,:,k,:]-=re;wi[:,:,k,:]-=im
            wr[2:,:,k,:]+=re[:-2];wi[2:,:,k,:]+=im[:-2]
        else:
            wr[3:,:,k,:]-=re[:-3];wi[3:,:,k,:]-=im[:-3]
    assert max(np.max(abs(wr)),np.max(abs(wi)))<2**48
    for d in range(8,3,-1):
        wr[d-2]-=wr[d];wr[d-4]+=wr[d]
        wi[d-2]-=wi[d];wi[d-4]+=wi[d]
        wr[d].fill(0);wi[d].fill(0)
    assert not np.any(wr[4:]) and not np.any(wi[4:])
    support=np.any((wr[:4]!=0)|(wi[:4]!=0),axis=(0,3))
    assert support.sum()==1764 and (~support).sum()==14620
    _EXACT_SUPPORT=(support,wr[:4],wi[:4])
    print("PASS EXACT Q(a,i) original support: 1764 bright, 14620 dark")
    return _EXACT_SUPPORT

def certify_hellinger(q,a,i,K,Ka,psi,dKs,dKas):
    support,pr,pi=exact_support()
    inv=lambda n:pow(int(n)%q,-1,q)
    state=(K@psi)%q;bras=(psi@Ka)%q
    w=np.einsum('kij,aj->aki',K,state,optimize=True)%q
    bw=np.einsum('aj,kji->aki',bras,Ka,optimize=True)%q
    # Independent exact Gaussian-integer amplitudes == original number-field Kraus.
    reduced=sum((pr[d]+i*pi[d])*pow(a,d,q) for d in range(4))%q
    assert np.array_equal(w,reduced*pow(12800,-2,q)%q)
    pb=np.einsum('aki,aki->ak',bw,w,optimize=True)%q*inv(2)%q
    assert int(np.sum(pb)%q)==1
    bright=support.reshape(-1)
    assert np.array_equal(bright,pb.reshape(-1)!=0)
    DW=[];DB=[];DQ=[]
    for dK,dKa in zip(dKs,dKas):
        ds=(dK@psi)%q;db=(psi@dKa)%q
        dw=(np.einsum('kij,aj->aki',dK,state,optimize=True)
            +np.einsum('kij,aj->aki',K,ds,optimize=True))%q
        dwb=(np.einsum('aj,kji->aki',db,Ka,optimize=True)
             +np.einsum('aj,kji->aki',bras,dKa,optimize=True))%q
        dq=(np.einsum('aki,aki->ak',dwb,w,optimize=True)
            +np.einsum('aki,aki->ak',bw,dw,optimize=True))%q*inv(2)%q
        assert int(np.sum(dq)%q)==0
        DW.append(dw.reshape(128*128,16))
        DB.append(dwb.reshape(128*128,16))
        DQ.append(dq.reshape(-1))
    DW=np.array(DW);DB=np.array(DB);DQ=np.array(DQ)
    def e4(j,k):
        Z=np.zeros((4,4),dtype=np.int64);Z[j,k]=1;return Z
    eta=np.diag([1,-1,-1,-1]).astype(np.int64)
    metric=[]
    for j in range(4):
        for k in range(j,4):
            X=e4(j,k)+(e4(k,j) if j!=k else np.zeros((4,4),dtype=np.int64))
            metric.append((eta@X).reshape(16))
    T=np.column_stack(metric)
    J=np.concatenate((T.T@DQ[:16],DQ[16:]),axis=0)%q
    U=np.concatenate((np.tensordot(T.T,DW[:16],axes=1),DW[16:]),axis=0)%q
    UB=np.concatenate((np.tensordot(T.T,DB[:16],axes=1),DB[16:]),axis=0)%q
    qb=pb.reshape(-1)[bright]
    js=J[:,bright]
    weighted=js*np.array([inv(int(x)) for x in qb],dtype=np.int64)[None,:]%q
    light=(weighted[:10]@js[10:].T)%q*inv(2)%q
    dark=~bright
    du=U[:,dark,:].reshape(34,-1)
    dub=UB[:,dark,:].reshape(34,-1)
    birth=(dub[:10]@du[10:].T+du[:10]@dub[10:].T)%q*inv(2)%q
    full=(light+birth)%q
    det10=rankdet(full[:,:10],q)
    det3=rankdet(birth[[0,4,7],:][:,[0,6,12]],q)
    assert det10==(10,{1009:259,4001:2109,101:13}[q]),(q,det10)
    assert det3==(3,{1009:306,4001:822,101:17}[q]),(q,det3)
    assert rankdet(full,q)[0]==10 and rankdet(birth,q)[0]==3
    print("PASS EXACT Hellinger q=",q,"full metric10xlink24 det10=",det10[1],
          "dark rank>=3 det3=",det3[1])

if __name__=='__main__':
    for args in PRIMES:
        check(*args)
    print('PASS native full128 SAME Jones preparation & SAME field in BOTH ticks,')
    print('      all40 first-order Kraus completeness, exact metric10+link24 rank34.')
    print('NO CLAIM: compulsory native Jones controller, selected Book03 Cost−Info,')
    print('          Einstein 40-Euler source, matter Ward, uniform GR refinement.')
