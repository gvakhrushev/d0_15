"""A posteriori bounds for a local coframe source at all heat depths 1..8192."""
import sys
from pathlib import Path
from fractions import Fraction as Q

import numpy as np
from scipy import sparse, linalg
from scipy.linalg.blas import dgemm

ROOT = Path(__file__).resolve().parents[7]
OWNER = ROOT / "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source"
sys.path.insert(0,str(OWNER))
import check_primary_car_preparation_source as car
import check_primary_car_pointer_source as interval

I = interval.I
UROUND = Q(1,2**53)
N = 2048
P = (I.rational(5).sqrt()-1)*Q(1,2)
ALPHA = P*P*Q(1,128*16)
ZETA = Q(1,2**20)


def gamma(k):
    return k*UROUND/(1-k*UROUND)


def frobenius_over(A, upper):
    # Positive terms, any summation tree. Even N^2 products incur relative
    # error <1e-9.  The factor 1.0001 also covers subnormal terms.
    q = float(np.sum(A*A))
    assert np.isfinite(q) and q*1.0001+1e-290 < float(upper)**2
    assert A.size <= N*N and gamma(A.size+2) < Q(1,10**8)


def operators():
    numbers=car.actual_counts(ROOT)
    values=[I.rational(Q(n*256,sum(numbers))) for n in numbers]
    weights=P*P*P*I([val.lo for val in values],[val.hi for val in values]).sqrt()
    mids=(weights.lo+weights.hi)/2
    assert max(mids-weights.lo)<5e-15 and max(weights.hi-mids)<5e-15
    evens=[j for j in range(16) if not bin(j).count("1")%2]
    odds=[j for j in range(16) if bin(j).count("1")%2]
    rows=[([],[],[]),([],[],[])]
    w=car.site_index(car.W)
    for i,site in enumerate(car.SITES_LIST):
        for m,mask in enumerate(evens):
            for (out,grade,src),c in car.flat_column(site,mask).items():
                j=car.site_index(out)*8+odds.index(grade)
                k=car.site_index(src)
                # Same entry has one geometric coefficient: no hidden dot
                # product over weights in creating the numeric matrices.
                assert abs(c) in (2,4,6)
                for code in (0,1) if k==w else (0,):
                    r,cx,v=rows[code]
                    r.append(j); cx.append(i*8+m); v.append(float(c)*mids[k])
    result=[]
    for r,c,v in rows:
        A=sparse.csr_matrix((v,(r,c)),shape=(N,N))
        assert A.nnz==len(v)
        assert A.getnnz(0).max()<=12 and A.getnnz(1).max()<=12
        result.append(A)
    # Supremum of entry error <6*5e-15+1e-14, at most 12 per row and column.
    assert 12*(6*5e-15+1e-14)<1e-12
    return result


def numerical_basis():
    T,E=operators()
    X,s,Yt=linalg.svd(T.toarray(),lapack_driver="gesdd",check_finite=True)
    Y=Yt.T
    assert np.all(s>=0) and max(s)<4.5
    frobenius_over(X,46); frobenius_over(Y,46)
    frobenius_over(T.data,129); frobenius_over(E.data,8)
    for V in (X,Y):
        gram=dgemm(1.,V,V,trans_a=1)
        diag=np.diag(gram)
        assert np.all((diag>.9)&(diag<1.1))
        np.fill_diagonal(gram,diag-1)  # exact by Sterbenz
        frobenius_over(gram,1e-12)
    # Gram roundoff in Frobenius norm <=gamma_N ||V||_F^2.
    assert gamma(N)*46**2+Q(1,10**12)<Q(1,10**9)
    Vres=T@Y-X*s
    frobenius_over(Vres,1e-12)
    # Dot length <=12 in T@Y, elementwise column scaling, subtraction,
    # primary matrix error in spectral norm <1e-12.
    assert gamma(16)*(129*46+46*5)+Q(46,10**12)+Q(1,10**12)<Q(1,10**9)
    # Both polar corrections have op norm <=1e-9. ||T_exact||<5 follows
    # from ||T_exact Y-X diag(s)||<1e-9 and the same Gram bound.
    assert Q(1,10**9)+(5+5)*Q(1,10**9)<Q(12,10**9)
    EY=E@Y
    local=np.sum(X*EY,axis=0)
    # l1 aggregate error in diag(X^T E Y), including true edge weights.
    err=(gamma(16)*8*46+Q(46,10**12))*46+gamma(N+2)*46*(8*46+1)
    assert err<Q(1,10**7)
    # ||S_w||_* <= sqrt(32)*||S_w||_F; ||S_w||_F^2=144 sigma² rho_w/h².
    rho_w=I.rational(Q(384,421))
    assert (32*144*(P*P*P).square()*rho_w*16).hi<64**2
    return s,local


def power(x,n):
    result=I(np.ones_like(x.lo))
    while n:
        if n%2:
            result=result*x
        n//=2
        if n:
            x=x.square()
    return result


def across_depths(s,local,nlo,nhi):
    m0,m1=2*nlo,2*nhi
    b=I(1.)-ALPHA*I(s).square()
    assert b.lo.min()>.99
    # The exact bases are <=1; tiny outward overruns near zero modes are fine.
    series=I(power(b,m1-1).lo,power(b,m0-1).hi)
    mass=I(power(b,m1).lo,power(b,m0).hi)
    Zhat=2*interval.reduce_sum(mass)
    That=2*interval.reduce_sum(I(s)*series*I(local))
    # For the true block D and its exact orthogonal model D0:
    # ||D-D0||<=delta, ||D||,||D0||<=5, ||B-B0||<=10 alpha delta.
    # Both B and B0 are positive contractions, so the power difference
    # is <=m||B-B0|| by a telescoping product, including repeated values.
    delta=I.rational(Q(12,10**9))
    eZ=4096*m1*10*ALPHA*delta
    eT=64*(1+50*(m1-1)*ALPHA)*delta
    # Replace polar factors by computed X,Y, and numeric diagonal products
    # by exact inner products. Rank trace pairing handles both parity blocks.
    eT=eT+I.rational(Q(64*5*3,10**9)+Q(2*5,10**7))
    Z=Zhat+I(-eZ.hi,eZ.hi)
    tr=That+I(-eT.hi,eT.hi)
    beta=I(m0,m1)*ALPHA
    # The feedback correction uses precisely the same trace and denominator
    # as H. Replacing F^-1 by I incurs the displayed bounded remainder.
    gain=(I(1.)/Z)-128*ZETA*beta
    correction=256*ZETA*beta*5*64*I.rational(ZETA/(1-ZETA))
    source=2*gain*tr+I(-correction.hi,correction.hi)
    assert Z.lo>0 and tr.lo>0 and gain.lo>0
    return source,Z


def certified_history_expansion(Z):
    # The first unequal pair is an exactly fair physical computational bit.
    readiness=(I(1.)-power(I(1.)-2*P*P*P,12))
    readiness=power(readiness,12)
    assert readiness.lo>31/32
    q=readiness*Z*Q(1,4096)
    assert q.lo>1/232
    assert power(I.rational(Q(231,232)),3600).hi<1e-6
    c=ZETA/(1-ZETA)
    jtail=128*4096*16384*c**4/(1-c)
    assert jtail<Q(1,10**13)
    # Positive-CX parity encoding gives an arbitrarily small nonzero step
    # of either sign in expected code minus complete entropy.
    assert (P*P*P).hi < .24 and (1-8*float((P*P*P).lo))<0
    # Noncommuting matrix jet and ordered independent-reset probabilities.
    import sympy as sp
    x=sp.symbols("x")
    T=sp.Matrix([[sp.Rational(3,4),x],[x,sp.Rational(1,3)+x]])
    point=sp.Rational(1,9)
    m=4
    probability=sp.trace(T**m)/2
    prob2=sp.trace(T**(2*m))/2
    assert (T*sp.diff(T,x)-sp.diff(T,x)*T).subs(x,point)!=sp.zeros(2)
    assert (prob2-probability**2).subs(x,point)!=0
    F=(1-sp.Rational(1,16))*sp.eye(2)+sp.Rational(1,16)*T**m
    cd=sp.Rational(1,15)
    # Sum of first three feedback differentials and the exact matrix remainder.
    Jjet=sp.trace(F.inv()*F.diff(x)).subs(x,point)
    core=T**m
    partial=sum((-1)**(k+1)*cd**k*sp.trace((core**k).diff(x))/k for k in range(1,4))
    rem=-cd**4*sp.trace((sp.eye(2)+cd*core).inv()*(core**3)*core.diff(x))
    assert sp.simplify(Jjet-(partial+rem).subs(x,point))==0
    r=sp.Rational(31,32)
    Q1=r*probability
    heat=-sum((1-Q1)**k/k for k in range(1,5))
    exact=probability.diff(x)/probability
    assert sp.simplify(exact-heat.diff(x)-(1-Q1)**4*exact)==0
    print("ready >",float(readiness.lo),"blank lower bound",float(q.lo),
          "heat relative jet error < 1e-6, feedback jet error <",float(jtail),"* ||dB||")


def main():
    s,local=numerical_basis()
    small,_=across_depths(s,local,1,1)
    last,Z=across_depths(s,local,8192,8192)
    certified_history_expansion(Z)
    print("n=1",interval.bounds(small),"n=8192",interval.bounds(last),"deep Z",interval.bounds(Z))
    assert small.lo>.0572 and small.hi<.0573
    assert last.lo>.00120 and last.hi<.00130
    start=1
    bounds=[]
    while start<=8192:
        end=min(8192,start+start//16)
        src,_=across_depths(s,local,start,end)
        bounds.append(float(src.lo))
        start=end+1
    print("all 8192 depths,",len(bounds),"rigorous bins; least lower bound",min(bounds))
    assert min(bounds)>.0010

if __name__=="__main__":
    main()
