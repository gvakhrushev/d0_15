"""A paid native read on either precomputed head; test movement on a purification."""
from itertools import product
from math import log, sqrt
import json
import numpy as np
from mpmath import iv

p=(sqrt(5)-1)/2
a=sqrt(p)
ell=-log(p)
v=np.array([a,p])
X=np.array([[0.,1.],[1.,0.]])
G=np.array([[a,-p],[p,a]])
I=np.eye(2)
CX=np.block([[I,np.zeros((2,2))],[np.zeros((2,2)),X]])
tail_G=np.kron(I,G)


def motion(x,y):
    return sqrt(max(0.,1-float(np.vdot(x,y).real)**2))


def first_reader(s):
    # rows are orthogonal old-reference sectors; final two factors are head,tail
    pair=np.array([sqrt(1-s),0.,0.,sqrt(s)])
    state=np.kron(pair,v)
    moves=[]
    for small in (CX,tail_G,CX):
        target=np.kron(I,small)@state
        moves.append(motion(state,target))
        state=target
    assert abs(sum(np.abs(state.reshape(2,2,2)[:,1,:].ravel())**2)-s)<2e-15
    return np.array(moves)


def formulas(s):
    d=1-2*a*p
    return np.array([sqrt(1-(1-d*s)**2),p,sqrt(1-(1-s)**2)])


def echo_and_measurement(s):
    # Three times two inverse CX would already cover either single reading
    # convention; five pairs cover both nonselective and selective charges together.
    head=np.array([sqrt(1-s),0.,0.,sqrt(s)])
    start=np.kron(head,[1.,0.])
    copy=np.kron(I,CX)@start
    assert np.allclose(np.kron(I,CX)@copy,start)
    echo=motion(start,copy)
    assert abs(echo-sqrt(1-(1-s)**2))<1e-14
    blocks=np.diag([1.,0.,1.,0.])
    b0=blocks@head/sqrt(1-s)
    b1=(head-blocks@head)/sqrt(s)
    rho=np.outer(head,head)
    dephased=(1-s)*np.outer(b0,b0)+s*np.outer(b1,b1)
    assert abs(np.linalg.norm(rho-dephased,ord="nuc")/2-sqrt(s*(1-s)))<1e-14
    assert abs(motion(head,b0)-sqrt(s))<1e-14
    assert abs(motion(head,b1)-sqrt(1-s))<1e-14
    return 10*echo+sqrt(s*(1-s)),(sqrt(s),sqrt(1-s))


def run():
    for s in (0,.601,.64,.71,.77,.799,1):
        assert np.max(np.abs(first_reader(s)-formulas(s)))<3e-8
    # One extra zero produces exactly the three sharp-zero charges, including G.
    assert np.max(np.abs(formulas(0)-np.array([0,p,0])))<1e-14
    # Jumps chosen via a paid native selector with every comparison slot
    # prepared beforehand. Demonstrate two high-probability heads by actual G powers.
    theta=np.arcsin(p)
    examples=[float(np.sin(m*theta)**2) for m in (8,11)]
    assert all(.6<s<.8 for s in examples) and abs(examples[0]-examples[1])>.015
    ip=(iv.sqrt(5)-1)/2
    assert (1-16*ip**6)/((-iv.log(ip))*(1+4*ip**6))>iv.mpf(".18")
    pairs=[(0.,0.,0.),(8.,.2,20.),(.07,50.,.001)]
    def price(s,alpha,rates,extra):
        t=1-alpha
        H=-((1-s)*log(1-s)+s*log(s))/ell
        common=np.dot(rates,formulas(s))
        # m=8 extra writes on 0; weighted gate charges of these and the
        # branch-independent address/header offset may be arbitrary positive.
        c0=9+extra
        c1=2
        S=[common+c0-alpha*H+t*log(1-s)/ell,
           common+c1-alpha*H+t*log(s)/ell]
        m=min(S)
        assert m==S[1]
        return m-log(sum(np.exp(-ell*(x-m)) for x in S))/ell,m
    # Uniform on 0.6<s<0.8: g'(s)=(1-s)/sqrt(1-(1-s)^2)>1/5.
    # Nonselective reading derivative >=-3/4, selective cheap leaf >=-sqrt(5)/2.
    assert 2-iv.mpf(3)/4-iv.sqrt(5)/2>0
    for s in (.601,.65,.73,.799):
        h=1e-6
        left,right=(echo_and_measurement(s+eps) for eps in (-h,h))
        for bit in (0,1):
            assert (right[0]+right[1][bit]-left[0]-left[1][bit])/(2*h)>.13
        assert right[1][0]>=right[1][1]
    n=0
    for s,alpha,rates,extra in product((.605,.65,.74,.795),(0,.2,.7,1),pairs,(0,50,200)):
        dx=1e-6
        lo,hi=price(s-dx,alpha,rates,extra),price(s+dx,alpha,rates,extra)
        assert min((y-x)/(2*dx) for x,y in zip(lo,hi))>.18
        n+=1
    print(json.dumps(dict(source="NC1 on a fully purified live head",
                          native_high_probability_heads=examples,
                          extra_zero_prints=8,base_gap=7,echo_CX_pairs=5,
                          selective_and_nonselective_reading_covered_at_common_rate=True,
                          own_positive_logsum_slope_lower=".18",finite_checks=n,
                          complete_address_tariff_derived=False,GR_closed=False),indent=2))


if __name__=="__main__":
    run()
