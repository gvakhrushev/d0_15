"""Positive Golden prefix calibration and mixed nonseparable cost on both actual NPS2."""
from fractions import Fraction as F
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

direct=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(direct/"round79"/"writer"))
sys.path.insert(0,str(direct/"round80"/"native"))
from check_sharp_history_writer import G, X, a, equal, p, v
from check_return_work import owner_check, simulation


BOUNDARY="11001000011011001011110001011000000011101000010"


def golden_cut():
    x=sp.symbols("x")
    mod=x**2+x-1
    reduce=lambda t:sp.rem(t,mod,x)
    eta=reduce((1-sp.chebyshevt(16,2*x-1))/2)
    assert eta==62725467644416*x-38766470964480
    # Compute all maximal zero siblings before boundary, then the boundary itself.
    # If bit 1 occurs, the subtree rooted at its zero sibling belongs to the event.
    # Powers count genuine token cost 1 for a 0 and 2 for a 1.
    previous=0
    exponents=[]
    for mark in BOUNDARY:
        if mark=='1': exponents.append(previous+1)
        previous+=1+int(mark)
    exponents.append(previous)
    assert len(BOUNDARY)==47 and previous==67
    assert reduce(sum(x**i for i in exponents))==eta
    assert reduce((x+x*x)**18)==1
    assert reduce((x+x*x)**47)==1
    # A fixed 18-bit block suffices even for the first bank. Its other 6 bits are real.
    for n in (12,18):
        same=reduce(x**n*(x+x*x)**(18-n))
        other=reduce(sum(x**i*x**2 for i in range(n)))
        assert same==reduce(x**n) and reduce(same+other)==1
        assert reduce(eta*same+eta*other+1-eta)==1
    print('Golden service class checked exactly: 47 public tosses, maximum boundary cost 67')


def ring_sum(x,y):
    return (x[0]+y[0],x[1]+y[1])


def ring_mul(x,y):
    a,b=x
    c,d=y
    return (a*c+b*d,a*d+b*c-b*d)


def ring_sign(x):
    a,b=x
    c=2*a-b
    sgn=lambda z: (z>0)-(z<0)
    if c*b>=0: return sgn(c+b)
    return sgn(c)*sgn(c*c-5*b*b)


def greedy(x):
    path=[]
    while x not in ((0,0),(1,0)):
        a,b=x
        if ring_sign((a,b-1))<=0:
            path.append(0)
            x=(a+b,a)
        else:
            path.append(1)
            x=(2*a+b-1,a+b-1)
    return path,x==(1,0)


def rotated_ports():
    golden=(0,1)
    one=(1,0)
    delta=(-1,2)
    cheb=[one,delta]
    for _ in range(51):
        twice=ring_mul((2,0),ring_mul(delta,cheb[-1]))
        cheb.append(ring_sum(twice,tuple(-z for z in cheb[-2])))
    get=lambda k:cheb[abs(k+1)]
    def power(n):
        t=one
        for _ in range(n): t=ring_mul(t,golden)
        return t
    for k in range(-50,51):
        for rank in (2,3):
            u=ring_mul(power(6*(rank-1)),ring_mul(get(k),get(k)))
            word,closed=greedy(u)
            weight=(0,0)
            prefix=one
            for digit in word:
                if digit: weight=ring_sum(weight,ring_mul(prefix,golden))
                prefix=ring_mul(prefix,power(1+digit))
            if closed: weight=ring_sum(weight,prefix)
            assert weight==u
    assert ''.join(map(str,greedy((-38766470964480,62725467644416))[0]))==BOUNDARY
    print('exact positive cuts for 202 further true port rotations')


def tagged(q,service,J):
    idle=1-service
    return sum(idle**k*service*q for k in range(J))


def cycles_and_prep():
    for J in range(1,7):
        for u in (F(1,9),F(3,50)):
            for eta in (F(7,8),F(9,10)):
                A=1-(1-eta)**J
                prob=dict(PP=tagged(u,eta,J),BB=tagged(u,eta,J),
                          PB=tagged(1-u,eta,J),BP=tagged(1-u,eta,J))
                assert prob['PP']==prob['BB']==A*u
                assert prob['PB']*prob['BP']==A*A*(1-u)**2
                ready=prob['PB']
                abort=(1-eta)**J
                assert ready+abort+prob['PP']==1
                assert sum((1-eta)**k for k in range(J))/ready==1/(eta*(1-u))
                for M in (1,3,7):
                    assert sum((1-ready)**k*ready for k in range(M))==1-(1-ready)**M
    # Reversal of time-stamped service attempts does not preserve valid stopping words.
    one=('00','10')
    assert one[-1]!='00' and tuple(reversed(one))[-1]=='00'


def finite_cost():
    # The branch-conditional work of actual NC1 on sharp live heads.
    assert equal((v.T*X*v)[0]**2+p**6,1)
    for h in (0,1):
        flip=X if h else sp.eye(2)
        steps=[v,flip*v,G*flip*v,flip*G*flip*v]
        expected=(p**3,p,1) if h else (0,p,0)
        for l,r,d in zip(steps,steps[1:],expected):
            assert equal(1-(l.T*r)[0]**2,d*d)
    iv=mp.iv
    iv.dps=70
    pp=(iv.sqrt(5)-1)/2
    base=iv.ln(1/pp)
    for order,n in (((2,3),12),((3,2),18)):
        owner_check(order)
        u,eta,reflection,detector,lens=simulation(order,iv)
        assert len(reflection[0])==38 and len(detector[0])==400
        assert (u-pp**n).a<=0<=(u-pp**n).b
        def read(q,final):
            first=eta*q
            if final=="P": return iv.sqrt(1-first)
            return iv.sqrt(first)+iv.sqrt((1-eta)/(1-first))
        mix=read(u,"B")+read(1-u,"P")-read(u,"P")-read(1-u,"B")
        switch=2*(1+pp**3)
        movement=mix+switch
        target=-2*iv.ln((1-u)/u)/base
        threshold=-iv.ln(1-eta)/base
        assert .19 < movement.a < movement.b < .27
        assert target.b < -23
        assert 4.61<threshold.a<threshold.b<4.62
        # A finite limit and the exact same candidate receipt laws before all ignored 00.
        for J in (1,3,7):
            K=pp**3*sum(pp**(2*k) for k in range(J))
            Wpp,Wpb,Wbp,Wbb=[K*pp**L for L in (3,3,4,2)]
            assert (Wpp/Wbb-pp).a<=0<=(Wpp/Wbb-pp).b
            assert (Wpb*Wbp/(Wpp*Wbb)-pp**2).a<=0<=(Wpb*Wbp/(Wpp*Wbb)-pp**2).b
        print('NPS2 k=%d mixed physical read %.10f, switch %.10f, mixed work %.10f, required %.10f'%
              (n,float(mix.mid),float(switch.mid),float(movement.mid),float(target.mid)))
    print('critical additional integer service-00 price for self-information: 3')


if __name__=='__main__':
    golden_cut()
    rotated_ports()
    cycles_and_prep()
    finite_cost()
