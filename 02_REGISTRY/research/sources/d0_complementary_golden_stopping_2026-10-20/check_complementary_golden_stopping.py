#!/usr/bin/env python3
"""Exact original-Golden complementary-sign stopping instrument.

Standard library only. Exact matrix checks use Q[a]/(a^4+a^2-1), p=a^2.
This is a conditional execution theorem, not a G0 admission/GR claim.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform
import random

@dataclass(frozen=True)
class Q4:
    c: tuple[F, F, F, F]

    @staticmethod
    def scalar(x=0):
        return Q4((F(x), F(0), F(0), F(0)))

    def __add__(self, other):
        other = other if isinstance(other, Q4) else Q4.scalar(other)
        return Q4(tuple(x+y for x,y in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self):
        return Q4(tuple(-x for x in self.c))

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q4) else -Q4.scalar(other))

    def __rsub__(self, other):
        return Q4.scalar(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Q4) else Q4.scalar(other)
        t = [F(0)] * 7
        for i, x in enumerate(self.c):
            for j, y in enumerate(other.c):
                t[i+j] += x*y
        # a^k = a^(k-4) - a^(k-2), k >= 4.
        for k in range(6, 3, -1):
            t[k-4] += t[k]
            t[k-2] -= t[k]
        return Q4(tuple(t[:4]))

    __rmul__ = __mul__

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError('Nonnegative integer exponent required')
        out, base = Q4.scalar(1), self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n >>= 1
        return out

    def value(self):
        aa = math.sqrt((math.sqrt(5)-1)/2)
        return sum(float(c)*aa**k for k,c in enumerate(self.c))

ZERO, ONE = Q4.scalar(), Q4.scalar(1)
a = Q4((F(0),F(1),F(0),F(0)))
p = a*a

def eye(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]

def diag(xs):
    n = len(xs)
    return [[(xs[i] if isinstance(xs[i],Q4) else Q4.scalar(xs[i]))
             if i == j else ZERO for j in range(n)] for i in range(n)]

def scale(c, X):
    return [[c*x for x in row] for row in X]

def add(X,Y):
    return [[x+y for x,y in zip(rx,ry)] for rx,ry in zip(X,Y)]

def transpose(X):
    return [list(r) for r in zip(*X)]

def mul(X,Y):
    Yt = transpose(Y)
    return [[sum((x*y for x,y in zip(row,col)), ZERO) for col in Yt] for row in X]

def kron(X,Y):
    return [[X[i][j]*Y[k][l] for j in range(len(X[0])) for l in range(len(Y[0]))]
            for i in range(len(X)) for k in range(len(Y))]

def same(X,Y,msg):
    if X != Y:
        raise AssertionError(msg)

def near(x,y,tol,msg):
    if abs(x-y) > tol:
        raise AssertionError(f'{msg}: {x} versus {y}')

def exact_native_instrument():
    # Literal gate from GoldenOrderInterferometer.gate, not a balanced substitute.
    G = [[a,-p],[p,a]]
    I2 = eye(2)
    Z = diag([1,-1])
    pp, pm = diag([1,0]), diag([0,1])
    same(mul(transpose(G),G),I2,'native Golden orthogonality')
    assert p+p**2 == ONE and p-p**2 == p**3
    q, r = 4*p**3, p**6
    assert q+r == ONE
    # A symbolic two-sector control: it is NOT an asserted new physical register.
    D0 = add(scale(p,I2),scale(p**2,Z))
    B0 = scale(a*p,add(Z,scale(-1,I2)))
    D1 = add(scale(p,I2),scale(-(p**2),Z))
    B1 = scale(-a*p,add(Z,I2))
    Kminus, Kplus, Kfail = B0, mul(B1,D0), mul(D1,D0)
    same(Kminus,scale(-2*a*p,pm),'minus conclusive Kraus')
    same(Kplus,scale(-2*a*p,pp),'plus conclusive Kraus')
    same(Kfail,scale(p**3,I2),'entire inconclusive cycle is scalar identity')
    complete = add(add(mul(transpose(Kminus),Kminus),mul(transpose(Kplus),Kplus)),
                   mul(transpose(Kfail),Kfail))
    same(complete,I2,'complete three-outcome instrument')
    same(mul(Kminus,pp),scale(0,I2),'never report minus on plus')
    same(mul(Kplus,pm),scale(0,I2),'never report plus on minus')
    for N in range(9):
        total = sum((q*r**k for k in range(N)),ZERO)+r**N
        assert total == ONE
    # Hostile control: two copies of the SAME reference are NOT state-preserving.
    assert mul(D0,D0)[0][0] != mul(D0,D0)[1][1]
    # Every one-query dark matrix has unequal positive singular values.
    assert D0[0][0]**2 != D0[1][1]**2
    assert D1[0][0]**2 != D1[1][1]**2

    # Literal original quaternion i: two signal-arm applications yield relative sign.
    Li = [[Q4.scalar(x) for x in row] for row in
          [[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]]
    I4 = eye(4)
    Ii = [[ZERO for _ in range(8)] for _ in range(8)]
    for i in range(4):
        for j in range(4):
            Ii[i][j] = I4[i][j]
            Ii[4+i][4+j] = Li[i][j]
    R8 = diag([1]*4+[-1]*4)
    same(mul(Ii,Ii),R8,'existing local i squared gives native reference flip')
    G8 = kron(G,I4)
    same(mul(mul(R8,G8),R8),transpose(G8),'reverse mixer uses forward controls')
    # Every entry of the whole original 8-axis two-arm/quaternion operation.
    for s in [1,-1]:
        C8 = diag([1]*4+[s]*4)
        U8 = mul(mul(transpose(G8),C8),G8)
        dark = [row[:4] for row in U8[:4]]
        bright = [row[:4] for row in U8[4:]]
        same(dark,scale(p+s*p**2,I4),'full quaternion dark amplitude')
        same(bright,scale((s-1)*a*p,I4),'full quaternion bright amplitude')
    return q,r

def full_reference_and_source(qf,rf):
    # Actual 128-column fixed Gram fixture, not a claim of G0 preparation.
    n = 128
    cp = [math.cos(.1 + .9*j/(n-1)) / math.sqrt(n) for j in range(n)]
    cm = [math.sin(.1 + .9*j/(n-1)) / math.sqrt(n) for j in range(n)]
    for j in range(n):
        near(cp[j]**2+cm[j]**2,1/n,2e-17,'original full RIGHT Gram diagonal')
    pf = math.sqrt(rf)
    failure_error = max(abs((pf*x)/math.sqrt(rf)-x) for x in cp+cm)
    assert failure_error < 1e-14
    wplus = sum(x*x for x in cp)
    wminus = sum(x*x for x in cm)
    near(wplus+wminus,1,1e-14,'full128 source normalization')
    # Every failure preserves the full joint state. Success need not preserve
    # the right marginal conditionally; the complete nonselective channel does.
    unconditional_right = [qf*(cp[j]**2+cm[j]**2)+rf/n for j in range(n)]
    assert max(abs(x-1/n) for x in unconditional_right) < 2e-17
    selected_right_error = max(abs(cp[j]**2/wplus-1/n) for j in range(n))
    assert selected_right_error > 1e-3  # retained hostile control

    # On a definite original central-sheet sector, conclusive readout also
    # preserves arbitrary full RIGHT preparation (only a global amplitude acts).
    original = 1 / math.sqrt(n)
    conclusive_normalized = (-math.sqrt(qf)*original) / math.sqrt(qf)
    near(conclusive_normalized,-original,1e-15,'definite-sheet successful RIGHT lift')

    # Moving sign projector Z(theta): complete clock score must not erase sign source.
    theta=.7
    w=[math.cos(theta/2)**2,math.sin(theta/2)**2]
    dw=[-math.sin(theta)/2,math.sin(theta)/2]
    fisher=sum(d*d/x for x,d in zip(w,dw))
    near(fisher,1,1e-14,'exact ideal sign Fisher')
    for N in [1,2,4,7]:
        Fi=sum(qf*rf**k*d*d/x for k in range(N) for x,d in zip(w,dw))
        near(Fi,(1-rf**N)*fisher,1e-14,'all stopped labels retain exact source')
    ell=math.log((1+math.sqrt(5))/2)
    Hsign=-sum(x*math.log(x)/ell for x in w)
    Hclock=(-math.log(qf)-(rf/qf)*math.log(rf))/ell
    Hwhole=0.0; dHwhole=0.0
    for k in range(1,30):
        alpha=qf*rf**(k-1)
        for x,d in zip(w,dw):
            v=alpha*x
            Hwhole -= v*math.log(v)/ell
            dHwhole -= alpha*d*math.log(v)/ell
    dHsign=-sum(d*math.log(x)/ell for x,d in zip(w,dw))
    near(Hwhole,Hclock+Hsign,2e-13,'complete clock plus sign entropy, no lost leaf')
    near(dHwhole,dHsign,2e-13,'real sign source survives all retained retry records')

    # Actual invocation clock: minus stops on query 2k-1; plus on query 2k.
    calls_minus=sum((2*k-1)*qf*rf**(k-1) for k in range(1,30))
    calls_plus=sum(2*k*qf*rf**(k-1) for k in range(1,30))
    near(calls_minus,2/qf-1,1e-13,'minus actual attempt clock')
    near(calls_plus,2/qf,1e-13,'plus actual attempt clock')
    c0,c1=3.25,5.5
    cminus=sum(((k-1)*(c0+c1)+c0)*qf*rf**(k-1) for k in range(1,30))
    cplus=sum((k*(c0+c1))*qf*rf**(k-1) for k in range(1,30))
    near(cminus,(c0+rf*c1)/qf,1e-12,'complete minus paid-cost recurrence')
    near(cplus,(c0+c1)/qf,1e-12,'complete plus paid-cost recurrence')
    return {'failure_joint_state_error':failure_error,
            'selected_success_RIGHT_change_control':selected_right_error,
            'sign_Fisher':fisher,'clock_entropy_phi':Hclock,'retained_entropy_source':dHwhole,
            'mean_queries_minus':calls_minus,'mean_queries_plus':calls_plus}

def original_triangle_consumer():
    # Consume the original 143+104+80 triangle basis, NOT another rank census.
    A,B,C=range(9),range(9,20),range(20,33)
    edge=lambda u,v: tuple(sorted((u,v)))
    E=[edge(u,v) for left,right in [(A,B),(A,C),(B,C)] for u in left for v in right]
    assert len(E)==359
    rng=random.Random(33420261020)
    bits={e:rng.randrange(2) for e in E}
    tau=lambda a,b,c:bits[edge(a,b)]^bits[edge(b,c)]^bits[edge(a,c)]
    basis=[(0,b,c) for b in B for c in C]
    basis += [(a,9,c) for a in A if a!=0 for c in C]
    basis += [(a,b,20) for a in A if a!=0 for b in B if b!=9]
    assert len(basis)==327 and len(set(basis))==327
    y={edge(0,b):0 for b in B}
    y.update({edge(0,c):0 for c in C})
    y.update({edge(a,9):0 for a in A if a!=0})
    for b in B:
        for c in C: y[edge(b,c)]=tau(0,b,c)
    for a in A:
        if a==0: continue
        for c in C: y[edge(a,c)]=tau(a,9,c)^y[edge(9,c)]
    for a in A:
        if a==0: continue
        for b in B:
            if b!=9: y[edge(a,b)]=tau(a,b,20)^y[edge(b,20)]^y[edge(a,20)]
    assert set(y)==set(E)
    for a in A:
        for b in B:
            for c in C:
                assert y[edge(a,b)]^y[edge(b,c)]^y[edge(a,c)] == tau(a,b,c)
    return {'native_edges':359,'basis_bits':327,'readout_consistency_checks':1287,
            'negative_basis_bits_in_fixture':sum(tau(*t) for t in basis)}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,help='Write NEW JSON receipt only when explicitly requested')
    args=ap.parse_args()
    q,r=exact_native_instrument()
    with localcontext() as ctx:
        ctx.prec=80
        pd=(Decimal(5).sqrt()-1)/2
        qd,rd=4*pd**3,pd**6
        assert abs(qd+rd-1)<Decimal('1e-75')
        all327=1-(1-rd**7)**327
        assert all327 < Decimal('0.000001')
        numbers={'p':str(pd),'success_per_cycle':str(qd),'failure_per_cycle':str(rd),
                 'mean_cycles_one':str(1/qd),'mean_cycles_327':str(327/qd),
                 'unresolved_327_with_cap7':str(all327),
                 'mean_queries_minus':str(2/qd-1),'mean_queries_plus':str(2/qd)}
    qf,rf=float(qd),float(rd)
    details=full_reference_and_source(qf,rf)
    graph=original_triangle_consumer()
    result={'status':'PASS','python':platform.python_version(),
            'input_ref':'6b5fdc323b2109e7955d55dcc6f209b76835f0f4',
            'golden_gate_owner_blob':'7b59090312c610e1e19f426d7ed8f4a982ebf296',
            'control_owner_blob':'b7e7fb4bda7ad2d6d67ce911b042c6ac7b493cc4',
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'exact_checks':['native Golden quartic arithmetic','all-eight-axis Q8 probe',
                            'local-i-squared reference flip','complete paired Kraus identity',
                            'zero-error both signs','all-dark identity','finite all-leaf normalization',
                            'same-reference negative control'],
            'numerical_controls':details,'native_triangle_consumer':graph,'numbers':numbers,
            'scope':{'native_physical_admission':False,'global_Dmin_optimality':False,
                     'full_Book_price_selected':False,'GR_closed':False,
                     'finite_uniform_maximum_halting_time':False}}
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    print(text,end='')
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding='utf-8')

if __name__=='__main__':
    main()
