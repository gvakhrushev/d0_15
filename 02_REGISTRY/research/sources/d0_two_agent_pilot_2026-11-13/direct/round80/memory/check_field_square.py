"""Eight-setting bounds and matched phase-square arithmetic on literal NPS2 banks."""
from fractions import Fraction
from math import comb, log
from pathlib import Path
import sys

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "round79" / "memory"))
from check_cold_compensation import A as a, P as p, V as v, raw_bank, product, close


def selector_margin():
    d = 705600
    weights = [Fraction((-1)**(j-1)*comb(8,j), j*j) for j in range(1,9)]
    counts = [d*abs(w) for w in weights]
    assert all(x.denominator == 1 for x in counts) and sum(counts) == 20316969
    plo, phi = Fraction(61803398,10**8), Fraction(618034,10**6)
    assert plo*(plo+1) < 1 < phi*(phi+1)
    lo = sum(counts)*plo**38
    hi = sum(counts)*phi**37
    assert lo > Fraction(232,1000) and hi < Fraction(377,1000)
    # Numerical display, with the rational bounds above certifying the margin.
    active = int(sum(counts))*p**36
    print("eight-setting Q in [%.10f, %.10f]; 1-2Q >= %.10f" %
          (active*p*p,active*p,1-2*active*p))


def overlap_writers():
    field = sp.QQ.algebraic_field(sp.sqrt((sp.sqrt(5)-1)/2))
    pf = field.from_sympy((sp.sqrt(5)-1)/2)
    af = field.from_sympy(sp.sqrt((sp.sqrt(5)-1)/2))
    # Fresh sharp zero copies have Born overlaps a,p. The two padding rails
    # have conditional overlaps (a,p), (p^3,1) respectively.
    for n in range(2,19):
        k = (n+5)//6
        pad = 6*k-n
        left = af**(n+pad) * pf**(3*k)
        right = pf**(n+pad)
        assert left==right==pf**(6*k)
    # Independently contract the raw one-wire gates of both padding types.
    g = np.array([[a,-p],[p,a]])
    for bit in range(2):
        x = np.eye(2) if bit==0 else np.flipud(np.eye(2))
        t = product(g,product(x,v))
        u = product(x,product(g,product(x,product(g,v))))
        close(product(v,t),(a,p)[bit])
        close(product(v,u),(p**3,1)[bit])


def bank_square(order, q):
    word, j = raw_bank(order)
    image = product(word,j)
    # Test the first NC1 output bit. Its 11 sector is exactly dark here.
    e = np.diag([int(i%4 >= 2) for i in range(64)])
    prob = p**2+p**3*q
    close(product(image.T, product(e,image)),prob*np.eye(4))
    branch = [product(e_,image) for e_ in (np.eye(64)-e,e)]
    r = np.eye(4)
    for left, right in ((1.,1.),(a**4,p**4),(p**6,p**6)):
        for s in (1,-1):
            controlled = left*branch[0]+s*right*branch[1]
            cold = product(j.T,product(word.T,controlled))
            close(cold,(left*(1-prob)+s*right*prob)*r)
    # Appending a legal Z to the accessible report leaves its Born law unchanged
    # and exchanges the two bare corners on the same unknown Spin columns.
    phase = np.eye(64)-2*e
    zimage = product(phase,image)
    close(product(zimage.T,product(e,zimage)),prob*r)
    bare_plus = product(j.T,image)
    bare_minus = product(j.T,zimage)
    assert abs(bare_plus[0,0]**2-bare_minus[0,0]**2) > .001
    close(product(j.T,product(phase,zimage)),bare_plus)
    close(product(zimage.T,product(phase,zimage)),product(image.T,product(phase,image)))


def feedback_and_cq():
    q, l, b, d, t = sp.symbols('q l b d t', positive=True)
    plus, minus = l*(1-q)+b*q, l*(1-q)-b*q
    numerator, denominator = d+t*plus**2, d+t*minus**2
    g = (sp.diff(numerator,q)*denominator-sp.diff(denominator,q)*numerator)
    assert sp.expand(g-4*t*l*b*(d*(1-2*q)+t*plus*minus))==0
    z = 2**-20
    eigs = (0.,.2,.5,1.)
    l,r = a**3,p**3
    q0 = 0.31
    # Use log1p in the numerical slope because the physical z is small.
    def rect(at):
        c1,c0 = l*(1-at)+r*at, l*(1-at)-r*at
        return -2*sum(np.log1p(z*u*(c1*c1-c0*c0)/(1-z+z*u*c0*c0)) for u in eigs)
    step=1e-5
    finite=(rect(q0+step)-rect(q0-step))/(2*step)
    c1,c0 = l*(1-q0)+r*q0,l*(1-q0)-r*q0
    exact=-8*sum(z*u*l*r*((1-z)*(1-2*q0)+z*u*c1*c0) /
                 ((1-z+z*u*c1*c1)*(1-z+z*u*c0*c0)) for u in eigs)
    close(finite,exact)
    # Classical experiment: arbitrary old quantum impurity cancels at each
    # previous classical atom, including nonconstant fine distributions at T=1.
    plus_q = p**2+4*p**6
    gain = (plus_q*log(plus_q/p**2)+(1-plus_q)*log((1-plus_q)/p))/log(1/p)
    def h(q):
        return -sum(x*log(x)/log(1/p) for x in (q,1-q) if x)
    for true_q in (.24,.31,.37):
        old = ((0,0.4*(1-true_q),.23),(0,0.6*(1-true_q),.5),
               (1,0.3*true_q,.1),(1,0.7*true_q,.76))
        def new_price(sign):
            new_entropy = 0.
            length = 0.
            for tick, weight, impurity in old:
                previous=-log(weight)/log(1/p)+h(impurity)
                if tick:
                    qread = plus_q if sign==1 else p**2
                    length += weight*(1+qread)
                    new_entropy += weight*((previous+h(qread))-previous)
            return length-new_entropy
        close(2*(new_price(1)-new_price(-1)),2*true_q*gain)
    print("CQ rectangle slope %.12f times b; conditional old-Gram slope %.12g" % (2*gain,exact))


if __name__ == "__main__":
    selector_margin()
    overlap_writers()
    bank_square((2,3),p**2)
    bank_square((3,2),2*p**3)
    feedback_and_cq()
