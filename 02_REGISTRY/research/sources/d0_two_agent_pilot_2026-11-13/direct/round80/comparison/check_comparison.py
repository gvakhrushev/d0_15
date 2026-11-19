"""Two capped physical measurements: scalar identities and the old channel on original NPS2."""
from fractions import Fraction as F
from math import atan2, cos, pi, sin, sqrt
from pathlib import Path
import sys

import numpy as np
import sympy as sp

DIRECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(DIRECT/"round79"/"memory"))
from check_cold_compensation import raw_bank, product

p=(sqrt(5)-1)/2
a=sqrt(p)
theta=atan2(p,a)
eta=sin(16*theta)**2


def masses(u,retry,cap,limit):
    d=(1-retry)**limit
    b=1-d
    result=[("A",0,d)]
    weight=1
    for k in range(cap+1):
        hit=u if k==0 else 1-u
        result.append(("P",k,weight*b*hit))
        weight*=b*(1-hit)
        if k!=cap:
            result.append(("D",k+1,weight*d))
    result.append(("B",cap+1,weight))
    return result


def sector(u,eta,cap,limit):
    d=(1-eta)**limit
    b=1-d
    f=b*(1-u)*(b*u)**cap
    gap=d*(d+f)/(1-b*u)
    t=(d+f)*(1-u)/(1-b*u)
    x=sqrt(u*(1-u))*gap
    return f,d,d-gap,t,x


def algebra():
    u,b,f=sp.symbols("u b f")
    d=1-b
    e1=d*(b*(1-u)-f)/(1-b*u)
    assert sp.factor(d-e1-d*(d+f)/(1-b*u))==0
    assert sp.factor(f+d*(1-u)+u*e1-(d+f)*(1-u)/(1-b*u))==0
    for v in (F(2,9),F(3,11)):
        for rate in (F(3,4),F(8,9)):
            for m in (0,1,3,7):
                for j in (1,2,4):
                    rows=masses(v,rate,m,j)
                    f,d,de,t,x=sector(v,rate,m,j)
                    assert sum(w for _,_,w in rows)==1
                    assert sum(w for tag,_,w in rows if tag=="D")==de
                    assert sum(w for tag,_,w in rows if tag=="B")==f
                    assert d*(1-v)+de*v+f==t
    # Enumerate actual raw strings, not just the number of accepted sectors.
    def visit(u,rate,cap,limit):
        leaves=[]
        def advance(k,left,weight,raw):
            hit=u if k==0 else 1-u
            for mark,prob in (("00",1-rate),("10",rate*hit),("01",rate*(1-hit))):
                w=weight*prob
                if mark=="10": tag="P"
                elif mark=="01" and k==cap: tag="B"
                elif mark=="00" and left==1: tag="A" if k==0 else "D"
                else:
                    if mark=="00": advance(k,left-1,w,raw+(mark,))
                    else: advance(k+1,limit,w,raw+(mark,))
                    continue
                leaves.append((raw+(mark,),tag,w))
        advance(0,limit,F(1),())
        return leaves
    u0,e0,m,j=F(2,11),F(6,7),2,2
    raw=visit(u0,e0,m,j)
    model=masses(u0,e0,m,j)
    for tag in ("P","B","A","D"):
        assert sum(w for _,t,w in raw if t==tag)==sum(w for t,_,w in model if t==tag)


def dyad(x,y=None):
    return np.outer(x,x if y is None else y)


def basis(x,kind):
    z=np.diag([1.,-1.])
    axis=[z if i in ({0,2} if kind==2 else {0,1,2}) else np.eye(2) for i in range(4)]
    o=np.array([[cos(x),-sin(x)],[sin(x),cos(x)]])
    axis[0]=product(product(o.T,z),o)
    word=np.array([[1.]])
    for matrix in axis: word=np.kron(word,matrix)
    return word


def channel(x,kind,cap,limit):
    seed=np.array([1.])
    for i in range(4): seed=np.kron(seed,[a,p])
    r=basis(x,kind)
    ri=product(r,seed)
    c=product(ri,seed)
    u=c*c
    B=(ri-c*seed)/sqrt(1-u)
    RB=product(r,B)
    states={"P":seed, "B":B,"A":ri,"D":RB}
    rows=masses(u,eta,cap,limit)
    blocks=[w*(dyad(states[tag])-dyad(seed)) for tag,_,w in rows]
    all_branch=sum(blocks)
    tn=lambda mat: sum(abs(np.linalg.eigvalsh(mat)))
    forgotten=tn(all_branch)/2
    kept=sum(map(tn,blocks))/2
    f,d,de,t,off=sector(u,eta,cap,limit)
    off=off if c>=0 else -off
    np.testing.assert_allclose(all_branch,t*(dyad(B)-dyad(seed))+off*(dyad(seed,B)+dyad(B,seed)),atol=2e-14)
    assert abs(forgotten-sqrt(t*t+off*off))<2e-14
    assert abs(kept-(f+d*sqrt(1-u)+de*sqrt(u)))<4e-14
    return forgotten,kept,all_branch,blocks,u


def native_test():
    m,j=3,2
    delta=p**3
    for kind,order in ((2,(2,3)),(3,(3,2))):
        v,i=raw_bank(order)
        z4=np.diag([(-1)**((n>>1)&1) for n in range(64)])
        literal=product(v.T,product(z4,v))
        np.testing.assert_allclose(literal,np.kron(np.eye(4),basis(0,kind)),atol=3e-13)
        ref=channel(0,kind,m,j)
        du=-8*a*p*delta**(2*kind-1)
        # Consecutive native G^k rotations straddling 0; G^(-k) has a positive full-column compiler.
        # First find an actual k with a small nonzero angle to re-use on both sides.
        ks=np.arange(1,200001)
        angles=(ks*theta+pi)%(2*pi)-pi
        k=int(ks[np.argmin(abs(angles))])
        eps=abs(k*theta-round(k*theta/(2*pi))*2*pi)
        assert 5e-7<eps<1e-4
        plus=channel(eps,kind,m,j)
        minus=channel(-eps,kind,m,j)
        assert abs((plus[4]-minus[4])/(2*eps)-du)<1e-8
        bounds=[(plus[h]-minus[h])/(2*eps) for h in range(2)]
        M=(plus[2]-minus[2])/(2*eps)
        tr=lambda m: np.abs(np.linalg.eigvalsh(m)).sum()/2
        deriv=tr(M)
        cq=sum(tr((h-g)/(2*eps)) for h,g in zip(plus[3],minus[3]))
        # Analytic derivatives at epsilon=0; B itself moves in the actual WORK.
        u=sp.symbols('u', positive=True)
        fail=sp.Float((1-eta)**j,20)
        b=1-fail
        f=b*(1-u)*(b*u)**m
        gap=fail*(fail+f)/(1-b*u)
        t=(fail+f)*(1-u)/(1-b*u)
        x=sp.sqrt(u*(1-u))*gap
        kept=f+fail*sp.sqrt(1-u)+(fail-gap)*sp.sqrt(u)
        g0=sp.sqrt(t*t+x*x)
        analytic=[float(expr.diff(u).subs(u,ref[4]))*du for expr in (g0,kept)]
        np.testing.assert_allclose(analytic,bounds,rtol=3e-5,atol=4e-9)
        seed=i[:,0][:16]
        dr=-2*np.array([[0,1],[1,0]])
        dword=np.kron(dr,basis(0,kind)[:8,:8])
        ri=product(basis(0,kind),seed)
        dri=product(dword,seed)
        c=delta**kind
        slope=du/(2*c)
        s=sqrt(1-c*c)
        B=(ri-c*seed)/s
        db=(dri-slope*seed)/s+B*du/(2*s*s)
        assert abs(product(B,db))<4e-14
        t0,x0=[float(y.subs(u,ref[4])) for y in (t,x)]
        dt,dx=[float(y.diff(u).subs(u,ref[4]))*du for y in (t,x)]
        exact_matrix=dt*(dyad(B)-dyad(seed))+dx*(dyad(seed,B)+dyad(B,seed))
        exact_matrix+=t0*(dyad(db,B)+dyad(B,db))+x0*(dyad(db,seed)+dyad(seed,db))
        np.testing.assert_allclose(exact_matrix,M,atol=2e-9)
        # Derivative of each record block, then sum trace norms (the labels stay separate).
        current={"P":seed,"B":B,"A":ri,"D":product(basis(0,kind),B)}
        jets={"P":0*seed,"B":db,"A":dri,
              "D":product(dword,B)+product(basis(0,kind),db)}
        exact_cq=0.
        for tag,_,weight in masses(u,sp.Float(eta,22),m,j):
            w=sp.sympify(weight)
            v0,s0=current[tag],jets[tag]
            mat=float(w.diff(u).subs(u,ref[4]))*du*(dyad(v0)-dyad(seed))
            mat+=float(w.subs(u,ref[4]))*(dyad(v0,s0)+dyad(s0,v0))
            exact_cq+=tr(mat)
        assert abs(exact_cq-cq)<1e-8
        # Four true pairwise SWAPs restore the old Work addresses; old Spin/RIGHT are spectators.
        for state in current.values():
            after=np.outer(state,seed).T
            np.testing.assert_allclose(product(after,after.T),dyad(seed),atol=3e-13)
        print(f'NPS2 s={kind} du={du:.9g} forgotten={ref[0]:.9g} recorded={ref[1]:.9g}')
        print('  norm slopes %.9g, %.9g; half derivative channel norms %.9g, %.9g; k=%d eps=%.9g'%
              (*analytic,tr(exact_matrix),exact_cq,k,eps))
        assert cq+2e-9>=deriv


if __name__=='__main__':
    algebra()
    native_test()
