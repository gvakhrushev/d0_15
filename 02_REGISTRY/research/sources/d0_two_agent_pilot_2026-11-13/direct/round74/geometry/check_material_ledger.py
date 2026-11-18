"""Exact all-column two-port instrument on the material resource (880)."""
import json
from itertools import combinations
from math import log, sqrt

import sympy as s


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


a, A, B = s.symbols("a A B", real=True)
p = a**2
r = 2*a*p
c = p-p**2
mod = a**4+a**2-1


def zero(expr):
    n, d = s.fraction(s.cancel(expr))
    return s.rem(n, mod, a) == 0 and s.rem(d, mod, a) != 0


def equal(left, right, label):
    require(left.shape == right.shape and all(zero(t) for t in left-right), label)


I = s.eye(2)
G = s.Matrix([[a,-p],[p,a]])
Z = s.diag(1,-1)
CX = s.eye(4)
CX.row_swap(2,3)
v = G[:,0]
X = s.Matrix([[0,1],[1,0]])


def staged_instrument(switched):
    # All inputs include the initialized witness as an actual two-dimensional factor.
    mixer = s.kronecker_product(G.T,I)
    read_witness = s.kronecker_product(I,G.T)
    operation = (CX*mixer*CX) if switched else (mixer*CX*CX)
    equal(operation.T*operation,s.eye(4),"two-port unitarity")
    return read_witness*operation*s.kronecker_product(s.Matrix([A,B]),v)


def verify_actual_inverse():
    qi = s.diag(X,X)
    qi[0,1] = -1
    qi[2,3] = -1
    source = s.diag(s.eye(4),qi)
    z_spin = s.kronecker_product(Z,s.eye(4))
    equal(source**2,z_spin,"two native SourceI stages implement the phase on all Spin columns")
    equal(z_spin*s.kronecker_product(G,s.eye(4))*z_spin,
          s.kronecker_product(G.T,s.eye(4)),"paid native inverse on an arbitrary Spin state")


def probabilities(branch):
    return [s.expand(vv**2) for vv in branch]


def jet(probs, u, v0, du, dv):
    return [s.expand((s.diff(q,A)*du+s.diff(q,B)*dv).subs({A:u,B:v0})) for q in probs]


def check_instruments():
    verify_actual_inverse()
    equal(G.T*G,I,"canonical orthogonal gate")
    require(zero(1-r**2-c**2) and zero(c-p**3), "exact kept and rejected witness amplitudes")
    marked = staged_instrument(True)
    plain = staged_instrument(False)
    formulas = s.Matrix([a*A+p*r*B,p*c*B,a*B-p*r*A,-p*c*A])
    equal(marked,formulas,"all four signed terminal amplitudes")
    equal(plain,s.Matrix([a*A+p*B,0,a*B-p*A,0]),"same-inventory comparator")
    physical = probabilities(marked)
    comparison = probabilities(plain)
    require(zero(sum(physical)-A**2-B**2) and zero(sum(comparison)-A**2-B**2),
            "all four output masses retained")

    u, t, d = s.symbols("u t d", real=True)
    low = [xx.subs({A:u,B:a}) for xx in physical]
    high = [xx.subs({A:d,B:t}) for xx in physical]
    require(zero(low[1]-p**9), "absolute calibration leaf from the fixed material anchor")
    require(zero(low[2]-p**2*(1-r*u)**2), "signed scalar packet")
    require(zero(high[1]-p**2*c**2*t**2) and zero(high[3]-p**2*c**2*d**2),
            "top amplitude and material slack retain their own branches")
    require(zero(high[0]-p*d**2-p**2*r**2*t**2-2*a*p*r*d*t),
            "signed top amplitude from the same outcomes")

    lower = jet(physical,0,a,1,0)
    upper = jet(physical,p,0,0,1)
    for jrow, h in ((lower,2*p**2*r),(upper,2*a*p**2*r)):
        require(all(zero(x-y) for x,y in zip(jrow,(h,0,-h,0))), "only bright rows contribute at first order")
    logs1 = s.diff(low[2],u).subs(u,0)/low[2].subs(u,0)
    logs14 = s.diff(high[0],t).subs({t:0,d:p})/high[0].subs({t:0,d:p})
    require(zero(logs1+2*r) and zero(logs14-2*r/a), "both material coordinates on the actual vacuum")
    for probs, rel in ((physical,r),(comparison,1)):
        flat_low = [xx.subs({A:0,B:a}) for xx in probs]
        flat_high = [xx.subs({A:p,B:0}) for xx in probs]
        require(zero(flat_low[0]-p*rel**2*flat_low[2]) and
                zero(flat_high[2]-p*rel**2*flat_high[0]),
                "two ratios for the complete entropy tangent")
    require(zero(4*p**4-(8-12*p)),"exact lower bound input for p*r^2")
    require((s.Rational(5,8))**2+s.Rational(5,8)>1,
            "p<5/8 proves 4p^4>1/2")


def check_choi_reader():
    # Every two computational labels become an addressed two-row minor
    # without mixing other input labels into that minor.
    for width in range(1,6):
        for left, right in combinations(range(2**width), 2):
            diff = left ^ right
            control = diff & -diff
            targets = diff ^ control
            def mapped(x):
                return x ^ targets if x & control else x
            pair = (mapped(left),mapped(right))
            require(pair[0]^pair[1] == control, "CX network makes exactly one bit differ")
            require({x for x in range(2**width)
                     if (mapped(x)^pair[0]) in (0,control)} == {left,right},
                    "selected portion contains no other Choi entry")
    choices = [0,0,0,0]
    for word in range(256):
        ones = bin(word).count("1")
        weight = p**(8+ones)
        conditions = (word == 0, not (word & 1),
                      bin(word & 15).count("1") == 1, bool(word & 63))
        for n, condition in enumerate(conditions):
            if condition:
                choices[n] += weight
    require(all(zero(value-target) for value,target in zip(choices,(p**8,p,4*p**5,4*p**3))),
            "all 256 paid eight-bit histories yield the four exact event factors")
    x, anchor, weight = s.symbols("x anchor w", real=True)
    probs = probabilities(staged_instrument(True))
    numerator = choices[0]*probs[0]-choices[1]*probs[3]-choices[2]*probs[1]
    for first in (True, False):
        scale = choices[3]*probs[3 if first else 1]
        pair = (anchor,anchor*x) if first else (anchor*x,anchor)
        require(zero(weight*(numerator-x*scale).subs(dict(zip((A,B),pair)))),
                "signed frequency minus moving anchor times the original matrix entry")


if __name__ == "__main__":
    check_instruments()
    check_choi_reader()
    pg = (sqrt(5)-1)/2
    rg = 2*pg**1.5
    gain = 2*pg**2*(rg*log(1/(pg*rg**2))-log(1/pg))
    print(json.dumps({"passed":True, "vacuum_anchor":"p^9", "signed_material_rows":
                      ["-2r","2r/a"], "conditional_entropy_contrast":gain,
                      "choi_coordinate":"(P_plus-P_minus)/P_anchor",
                      "golden_histories_checked":256,"GR_closed":False},sort_keys=True))
