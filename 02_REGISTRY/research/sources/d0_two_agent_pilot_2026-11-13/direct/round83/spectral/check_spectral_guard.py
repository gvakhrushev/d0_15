"""Reproduce the guarded detector's passive, Born, root and terminal estimates."""
from fractions import Fraction
from itertools import product
from math import comb, factorial
from pathlib import Path
import sys

from mpmath import iv
import sympy as sp

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "round82" / "device"))
import check_prepaid_report as device

iv.dps = 65
p = (iv.sqrt(5)-1)/2
eta = 16*p**9
sigma = 4*p**3
beta = 2*p**2
ell = -iv.log(p)


def certify(ok, msg):
    if not ok:
        raise ArithmeticError(msg)


def between(x, lower, upper):
    certify(x.a > iv.mpf(lower) and x.b < iv.mpf(upper), str(x))


def tail(n, q):
    return sum(comb(n, j)*q**j*(1-q)**(n-j) for j in range((2*n+2)//3, n+1))


def odds_eps(depth):
    x = beta/11
    error = 2*x**depth / factorial(depth) / (1-x/(depth+1))
    m = iv.exp(-2*beta)
    return iv.log((m+error)/(m-error))/ell


def native_flags():
    coeff = lambda n: device.Golden.cast(n)
    def power(x,n):
        v = coeff(1)
        for _ in range(n):
            v = v*x
        return v
    # Full positive native G on a paid birth v. Replay its matrix from owner.
    v = sp.Matrix([device.ne.A,device.ne.P])
    u = device.ne.G_LOCAL*v
    equal = lambda e: device.ne.GOLDEN_FIELD.from_sympy(e) == device.ne.GOLDEN_FIELD.zero
    certify(equal(u[1]**2-4*device.ne.P**3), "true Gv flag")
    certify(equal(v[1]**2-device.ne.P**2), "passive birth")
    certify(equal((u[0])**2-device.ne.P**6), "true failure")
    cos2 = 2*device.p - device.one
    cos4 = 2*cos2*cos2-device.one
    certify(device.one-cos4*cos4==16*power(device.p,9), "raw detector efficiency")
    # Explicit native square on a separate vv for the common warm terminal.
    gate = device.ne.Gate("CX",(0,1))
    execution = device.ne.Execution(2,(0,1),(),(gate,gate))
    m = device.ne.gate_matrix(execution,gate)
    certify(m*m == sp.eye(4), "four-column final pair")
    for n in range(1,8):
        for q, analytic in ((p**2,tail(n,p**2)),(sigma,tail(n,sigma))):
            paths = sum(q**sum(bits)*(1-q)**(n-sum(bits)) for bits in product(range(2),repeat=n)
                        if 3*sum(bits) >= 2*n)
            certify(0 in paths-analytic, "all guard words")
    # The underlying odds are not a golden unit, independent of numerical logs.
    norm = lambda a,b: a*a-a*b-b*b
    certify(norm(9,-16) == -31 and Fraction(-16**2,31**2) != -1, "odds norm")


def geometry():
    ha,h0,scale,z = sp.symbols("ha h0 scale z",real=True)
    G0 = 1-z+z*(h0+ha)
    Gs = 1-z+z*(h0+scale*ha)
    ratio = scale*G0/Gs
    certify(sp.cancel(1-ratio-(1-scale)*(1-z+z*h0)/Gs)==0,"relative upper gain")
    certify(sp.cancel(ratio-scale-scale*z*(1-scale)*ha/Gs)==0,"relative lower gain")
    for t in (17,33,65):
        n=t
        s,c=tail(t,p**2),tail(t,sigma)
        gain=1-s*(1-p**(4*n))
        A=n*eta*p**2-(1+p**2)*(1-(1-eta)**n)
        if t==17:
            between(s,".00691683832280",".00691683832283")
            between(c,".9997829857990",".9997829857992")
            between(gain,".9930831616771",".9930831616773")
            between(c*A,".0096959587085",".0096959587088")
        if t==65:
            between(1-c,".0000000000029",".0000000000031")
            between(1-gain,".0000014029721",".0000014029723")
        print("guard",t,"passive",float(s.mid),"Born",float(c.mid),
              "DJ factor at least",float(gain.mid),"cash gain",float((c*A).mid))
    two_thirds=iv.mpf(2)/3
    certify(((1+p**2)/2**two_thirds).b < 1 and
            (2**two_thirds*(1-sigma/2)).b < 1, "exponential separation")


def root_and_terminals():
    # Test exact expected price and retained entropy on all masks, via AD polynomial
    # coefficients in q (old field probability), independently of closed formula.
    for n in range(1,8):
        weighted = []
        for y in (0,1):
            L = iv.mpf(0)
            H = iv.mpf(0)
            for mask in product(range(2),repeat=n):
                hits=sum(mask)
                mask_mass=eta**hits*(1-eta)**(n-hits)
                sectors=((0,p),(1,p**2)) if y and hits else ((0,iv.mpf(1)),)
                for b,pb in sectors:
                    mass=mask_mass*pb
                    L+=mass*(3*n+(1+b)*hits)
                    H-=mass*iv.log(mass)/ell
            weighted.append((L,H))
        dL=weighted[1][0]-weighted[0][0]
        dH=weighted[1][1]-weighted[0][1]
        for nu in (1,2):
            test=dL-(1+iv.mpf(1)/nu)*dH
            expect=n*eta*p**2-(1+iv.mpf(1)/nu)*(1+p**2)*(1-(1-eta)**n)
            certify(0 in test-expect and (test-expect).delta.b<iv.mpf("1e-57"),
                    "full conditional root slope")
    u=-iv.log(eta/(1-eta))/ell
    between(u,"2.7471791161328","2.7471791161329")
    x=beta/11
    heat34=iv.mpf(66)/359 * x**34/factorial(33)/(1-x/34)
    between(heat34,"8.77e-78","8.78e-78")
    e4=odds_eps(4)
    between(e4,".00003765112",".00003765114")
    certify((3-u-e4).a > iv.mpf(".25278"),"golden lattice, spectral odds")
    certify((2*u-5-e4).a > iv.mpf(".49431"),"surprisal cost, nu=1")
    certify((iv.mpf(3)/2*u-4-e4/2).a > iv.mpf(".12074"),"surprisal cost, nu=2")
    print("terminal logarithmic odds bound",float(e4.mid),"true cost in gold",float(u.mid))
    print("PASS")


if __name__ == "__main__":
    native_flags()
    geometry()
    root_and_terminals()
