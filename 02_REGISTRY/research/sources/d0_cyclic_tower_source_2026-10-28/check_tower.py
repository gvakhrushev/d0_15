#!/usr/bin/env python3
"""Canonical AF tower source: exact identities and full defining-block checks.

The seven-stage binary word is the pinned native word. The two-level dense
AF test is a structural smaller profile; no emitted large AF device, physical
variation domain, GR root, or full-clock diagonalization is asserted.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import scipy.linalg as la
import sympy as sp
from sympy.polys.matrices import DomainMatrix

COUNT = 0
P = (math.sqrt(5)-1)/2
M = np.array([[1,1],[1,0]], dtype=np.int64)

def require(ok, label):
    global COUNT
    COUNT += 1
    if not bool(ok):
        raise ArithmeticError(label)

def near(a,b,label,tol=4e-12):
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    require(err<tol, f'{label}: {err}')
    return err

def kernel(r,c):
    mult=np.linalg.matrix_power(M,r)
    gamma=P**r
    loss=4*(1-c*c)
    C=1-gamma*loss
    T=np.array([[P**(r+b-a)*(mult[b,a]-loss*int(a==b)) for b in range(2)] for a in range(2)])
    return C,T,T/C

def exact_kernel():
    p=(sp.sqrt(5)-1)/2
    f=sp.QQ.algebraic_field(p)
    def eq(x,y): require(f.from_sympy(x-y)==f.zero,'exact Golden transition identity')
    rows=[]
    for r in (4,6,8,10,16):
        F=sp.Matrix([[1,1],[1,0]])**r
        for c in (sp.Rational(1,5),sp.Rational(3,5),p):
            loss=4*(1-c*c);C=1-p**r*loss
            T=sp.Matrix(2,2,lambda a,b:p**(r+b-a)*(F[b,a]-loss*int(a==b)))
            eq(sum(T[0,j] for j in range(2)),C)
            eq(sum(T[1,j] for j in range(2)),C)
            # Contractivity only for a genuine positive profile.
            valid=all(float(sp.N(F[a,a]-loss))>=0 for a in range(2)) and float(C)>0
            if valid:
                for a in range(2):
                    for b in range(2): require(float(sp.N(T[a,b]/C))>=0,'positive exact transition')
                v=sp.Matrix([[1/(1+p*p),p*p/(1+p*p)]])
                eq((v*T)[0,0],C*v[0,0]);eq((v*T)[0,1],C*v[0,1])
            rows.append({'increment':r,'c':str(c),'positive_profile':valid})
    # A shallow unmatched profile can produce a signed map: not silently CP.
    C,T,K=kernel(4,.2)
    require(float(K.min())<0,'shallow-profile negative control')
    C,T,K=kernel(8,P)
    require(float(K.min())>0,'actual k4 profile strictly positive')
    return {'native_k4_C':C,'native_k4_transition':K.tolist(),
            'native_stationary_weights':[1/(1+P*P),P*P/(1+P*P)],
            'tested_exact_profiles':rows,'shallow_profile_not_promoted':True}

def native_word_rows():
    a=sp.sqrt((sp.sqrt(5)-1)/2)
    field=sp.QQ.algebraic_field(a)
    def dm(x): return DomainMatrix.from_Matrix(sp.Matrix(x)).convert_to(field)
    p=a*a
    gg=sp.Matrix([[a,-p],[p,a]])
    G=dm(sp.kronecker_product(gg,sp.eye(8)))
    CX=dm(sp.kronecker_product(sp.diag(sp.eye(2),sp.Matrix([[0,1],[1,0]])),sp.eye(4)))
    Li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    SI=dm(sp.diag(sp.eye(8),sp.kronecker_product(sp.eye(2),Li)))
    ident=dm(sp.eye(16));R=dm(sp.kronecker_product(sp.diag(-1,1,1,1),sp.eye(4)))
    gates=[G,CX,SI,SI,G,SI,SI]
    wires=[(0,),(0,1),(0,2,3),(0,2,3),(0,),(0,2,3),(0,2,3)]
    W=ident
    for g in gates:
        require((g.transpose().matmul(g)-ident).is_zero_matrix,'native full16 gate')
        W=g.matmul(W)
    require((W-W.transpose()).is_zero_matrix,'actual reflected native word')
    require((W.matmul(W)-ident).is_zero_matrix,'actual involution')
    def extract(A,rr,cc): return A.extract(rr,cc)
    def ptr(A):
        out=dm(sp.zeros(4))
        for w in range(4):out=out+extract(A,list(range(4*w,4*w+4)),list(range(4*w,4*w+4)))
        return out
    spin=dm(sp.eye(4))
    require((extract(W,list(range(4)),list(range(4)))-spin.scalarmul(field.from_sympy(p))).is_zero_matrix,'native cold p')
    Wm=W.to_Matrix()
    Wwork=Wm.extract([0,4,8,12],[0,4,8,12])
    require((W-dm(sp.kronecker_product(Wwork,sp.eye(4)))).is_zero_matrix,'complete protected-factor restoration')
    L=W.matmul(R).matmul(W).matmul(R)
    require((ptr(L)-spin.scalarmul(field.from_sympy(4*p*p))).is_zero_matrix,'native complete loop trace')
    suffix=[None]*8;suffix[7]=ident
    for j in reversed(range(7)):suffix[j]=suffix[j+1].matmul(gates[j])
    raw=0;nonzero=0;skew_nonzero=0
    for j,ww in enumerate(wires):
        q=2**len(ww)
        for u in range(q):
            for v in range(u+1,q):
                h=sp.zeros(16)
                for col in range(16):
                    bits=[(col>>(3-t))&1 for t in range(4)]
                    local=sum(bits[w]<<(len(ww)-1-t) for t,w in enumerate(ww))
                    if local not in (u,v):continue
                    dest=v if local==u else u
                    out=bits[:]
                    for t,w in enumerate(ww):out[w]=(dest>>(len(ww)-1-t))&1
                    row=sum(out[t]<<(3-t) for t in range(4))
                    h[row,col]=1 if local==u else -1
                H=suffix[j+1].matmul(dm(h)).matmul(suffix[j+1].transpose())
                dW=H.matmul(W)
                X=extract(dW,list(range(4)),list(range(4)))
                for dL in (W.matmul(R).matmul(dW).matmul(R),dW.matmul(R).matmul(W).matmul(R)):
                    Y=ptr(dL)
                    expected=(X+X.transpose()).scalarmul(field.from_sympy(4*p))
                    require((Y+Y.transpose()-expected).is_zero_matrix,'each independent original raw loop source')
                    raw+=1
                    nonzero+=not (Y+Y.transpose()).is_zero_matrix
                    skew_nonzero+=not (Y-Y.transpose()).is_zero_matrix
    require(raw==240,'all240 old native rows')
    return {'native_word_calls':7,'original_raw_loop_rows':raw,
            'nonzero_Hermitian_rows':nonzero,'nonzero_skew_rows':skew_nonzero,
            'all16_native_columns_checked_exactly':True,
            'large_88_call_AF_profile_replayed':False}

def embed(old,r,spin):
    mult=np.linalg.matrix_power(M,r)
    return [la.block_diag(*[old[a] for a in range(2) for _ in range(int(mult[b,a]))]) for b in range(2)]

def placement(old_dims,r,spin,b,a,work_count):
    mult=np.linalg.matrix_power(M,r)
    off=sum(int(mult[b,t])*old_dims[t]*spin for t in range(a))
    return [[off+(w*old_dims[a]+row)*spin+k for w in range(work_count) for k in range(spin)]
            for row in range(old_dims[a])]

def fresh(logicals,old_dims,r,spin,identity=True):
    mult=np.linalg.matrix_power(M,r)
    ds=mult@np.asarray(old_dims)
    out=[np.eye(int(d)*spin,dtype=complex) if identity else np.zeros((int(d)*spin,)*2,complex) for d in ds]
    for a in range(2):
        local=logicals[a];q=local.shape[0]//spin
        require(int(mult[a,a])>=q,'actual profile has enough diagonal copies')
        for inds in placement(old_dims,r,spin,a,a,q):out[a][np.ix_(inds,inds)]=local
    return out

def expectation(new,old_dims,r,spin):
    mult=np.linalg.matrix_power(M,r)
    out=[np.zeros((d*spin,d*spin),complex) for d in old_dims]
    for b in range(2):
        off=0
        for a in range(2):
            size=old_dims[a]*spin
            for _ in range(int(mult[b,a])):
                out[a]+=P**(r+b-a)*new[b][off:off+size,off:off+size]
                off+=size
    return out

def partial(local,spin):
    return sum((local[k:k+spin,k:k+spin] for k in range(0,len(local),spin)),np.zeros((spin,spin),complex))

def loop(c,spin):
    u=math.sqrt(1-c*c)
    U=np.kron([[c,u],[u,-c]],np.eye(spin))
    R=np.kron(np.diag([-1,1]),np.eye(spin))
    return U@R@U@R,U,R

def dense_tower():
    # True Fibonacci inclusion and GNS conditional trace; smaller STRUCTURAL
    # work2/Spin2 controls, not a replacement for the emitted work4/Spin4 word.
    spin=2;r=4;dims0=[1,1];dims1=list(np.linalg.matrix_power(M,r)@dims0)
    dims2=list(np.linalg.matrix_power(M,r)@dims1)
    cs=[.8,.85];base=[loop(c,spin) for c in cs]
    first=fresh([base[0][0]]*2,dims0,r,spin)
    second=fresh([base[1][0]]*2,dims1,r,spin)
    history=[L@A for L,A in zip(second,embed(first,r,spin))]
    C1,T1,K1=kernel(r,cs[0]);C2,T2,K2=kernel(r,cs[1])
    def cold(blocks):return expectation(expectation(blocks,dims1,r,spin),dims0,r,spin)
    C=la.block_diag(*cold(history));s=C1*C2
    near(C,s*np.eye(4),'whole two-level canonical cold value')
    for L in first+second:near(L.conj().T@L,np.eye(len(L)),'all defining-block columns unitary')
    # GNS all old-input columns are checked by trace inner products. No
    # enormous regular left-multiplication matrix is formed or discarded.
    old_tau=[P,P*P];new_tau=[P**9,P**10]
    for a in range(2):
        for row in range(spin):
            for col in range(spin):
                E=[np.zeros((spin,spin),complex) for _ in range(2)];E[a][row,col]=1
                image=embed(embed(E,r,spin),r,spin)
                inner=sum(new_tau[b]*np.trace(image[b].conj().T@history[b]) for b in range(2))
                near(inner,old_tau[a]*cold(history)[a][row,col],'literal GNS compression matrix entry')
    rng=np.random.default_rng(281026)
    maxerr=0.;maxsource=0.;negdiff=0.;maxfd=0.;maxgns=0
    z=.19;D=(1-z)*np.eye(4)+z*C.conj().T@C
    for stage in (0,1):
        for typ in (0,1):
            for trial in range(4):
                A=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));H=(A-A.conj().T)/2
                L=base[stage][0];dL=H@L
                logs=[np.zeros((4,4),complex)]*2;logs[typ]=dL
                if stage==0:
                    dfirst=fresh(logs,dims0,r,spin,False)
                    dwhole=[b@a for b,a in zip(second,embed(dfirst,r,spin))]
                else:
                    dsecond=fresh(logs,dims1,r,spin,False)
                    dwhole=[b@a for b,a in zip(dsecond,embed(first,r,spin))]
                x=np.zeros((2,spin,spin),complex);x[typ]=P**r*partial(dL,spin)
                predicted=C2*x if stage==0 else np.einsum('ab,bij->aij',T1,x)
                actual=np.array(cold(dwhole))
                maxerr=max(maxerr,near(actual,predicted,'complete independent source through the earlier cut'))
                dC=la.block_diag(*actual)
                g=-2*z*np.trace(la.solve(D,C.conj().T@dC)).real
                dP=la.block_diag(*predicted)
                gp=-2*z*np.trace(la.solve(D,C.conj().T@dP)).real
                maxsource=max(maxsource,near(g,gp,'full determinant first source'))
                if trial==0:
                    for aa in range(2):
                        for rr in range(spin):
                            for cc in range(spin):
                                E=[np.zeros((spin,spin),complex) for _ in range(2)]
                                E[aa][rr,cc]=1
                                img=embed(embed(E,r,spin),r,spin)
                                ip=sum(new_tau[b]*np.trace(img[b].conj().T@dwhole[b]) for b in range(2))
                                maxgns=max(maxgns,near(ip/old_tau[aa],actual[aa,rr,cc],'derivative literal full GNS input matrix entry'))
                    def full_price(t):
                        logs=[base[stage][0].copy(),base[stage][0].copy()]
                        logs[typ]=la.expm(t*H)@logs[typ]
                        if stage==0:
                            aa=fresh(logs,dims0,r,spin)
                            vv=[b@a for b,a in zip(second,embed(aa,r,spin))]
                        else:
                            bb=fresh(logs,dims1,r,spin)
                            vv=[b@a for b,a in zip(bb,embed(first,r,spin))]
                        cc=la.block_diag(*cold(vv))
                        pencil=(1-z)*np.eye(4)+z*cc.conj().T@cc
                        return -float(np.linalg.slogdet(pencil)[1])
                    h=2e-4
                    fd=(-full_price(2*h)+8*full_price(h)-8*full_price(-h)+full_price(-2*h))/(12*h)
                    maxfd=max(maxfd,near(fd,g,'independent full price derivative',3e-10))
                if stage==1:
                    negdiff=max(negdiff,float(la.norm(actual-C1*x)))
    require(negdiff>1e-3,'ignoring type transport gives the wrong source')
    # A locally skew insertion remains skew after every earlier channel.
    B=np.array([[1j,.3],[-.3,-.5j]])
    xs=np.array([B,-2*B])
    actual=np.einsum('ab,bij->aij',T1,xs)
    near(actual+actual.conj().transpose(0,2,1),0,'skew apparatus source cannot become Hermitian under this tower map')
    return {'levels':2,'increment_per_level':r,'old_block_sizes':dims0,
      'intermediate_block_sizes':[int(x) for x in dims1],
      'final_block_sizes':[int(x) for x in dims2],
      'full_regular_dimension':int(sum(x*x for x in dims2)*spin),
      'canonical_input_rank':4,'ordinary_input_trace_not_AF_trace':True,
      'all_defining_columns_retained':True,'max_source_operator_error':maxerr,
      'max_price_source_error':maxsource,'max_full_price_FD_error':maxfd,
      'max_literal_GNS_source_error':maxgns,'wrong_untransported_source_difference':negdiff,
      'emitted_native_AF_hardware_claimed':False}

def long_history():
    # No random reassignment of primitive c: actual c=p of the seven-call word.
    C,T,K=kernel(8,P)
    A=np.array([[[.2,.13j],[-.13j,-.1]],[[.31,.08],[.08,.2]]])
    start=max(la.norm(x,2) for x in A)
    records=[]
    for n in (1,2,8,64,512):
        Kn=np.linalg.matrix_power(K,n)
        B=np.einsum('ab,bij->aij',Kn,A)
        out=max(la.norm(x,2) for x in B)
        require(out<=start+1e-12,'no accumulated apparatus amplification')
        near(Kn@np.ones(2),np.ones(2),'same-sign free source not erased')
        records.append({'past_loops':n,'operator_norm_ratio':float(out/start),'row_sum_error':float(np.max(abs(Kn.sum(1)-1)))})
    # Noncentral old-record coupling is explicitly NOT covered by the profile.
    # Scalar partial trace alone is insufficient to preserve a past source.
    Z=np.diag([1.,-1.])
    X=1j*Z;V=np.diag([1j,-1j])
    require(abs(np.trace(X))<1e-14 and abs(np.trace(X@V))>1,'centred insertion can be detected by a non-profile past')
    return {'controls':records,'unrestricted_old_record_couplings_not_erased':True}

def main():
    out={'input_commit':'d53ef61c8c578c5a6cf16b88d17f8576ced0f64d',
      'exact_transfer':exact_kernel(),'native_local_source':native_word_rows(),
      'direct_full_blocks':dense_tower(),'many_cuts':long_history()}
    out.update({'checks':COUNT,'status':'PASS_CANONICAL_TOWER_SOURCE_TRANSPORT',
      'GR_closed':False,'physical_AF_actuation_proved':False,
      'physical_comparison_domain_proved':False,'large_clock_replayed':False,
      'new_all42_root':False,'Lean_or_CI_run':False,
      'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False))

if __name__=='__main__':main()
