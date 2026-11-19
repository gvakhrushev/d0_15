"""Exact algebra for the two programmes of the D0 15-transition interferometer."""
import json
import sympy as s

A, B, C, D = s.symbols("A B C D", positive=True)
p = (s.sqrt(5) - 1) / 2
a = s.sqrt(p)
simplify = s.simplify
q = 4 * p**3
assert simplify(1 - q - p**6) == 0

def responses(a0, a1, b0, b1):
    return ((a0 + a1)**2, (b0 - b1)**2, (a0 - a1)**2, (b0 + b1)**2)

plus_zero, plus_one, minus_zero, minus_one = responses(A, B, C, D)
assert s.expand((minus_zero + minus_one - plus_zero - plus_one).subs(D,C) + 4*(A*B-C**2)) == 0
x = s.symbols("x")
assert simplify(-x**2+x-p**3 + (x-p)*(x-p**2)) == 0
for u,v in ((p,p**2),(p**2,p)):
    raw = tuple(map(simplify, responses(u,v,p*a,p*a)))
    assert all(simplify(x-y)==0 for x,y in zip(raw,(1,0,p**6,4*p**3)))

m = simplify(1-(1-p**2)*q)
assert simplify(m-(1-4*p**4))==0
tilted = simplify(p**2*q / m)
assert 0 < tilted < q < 1
# The inversion is exact at nonzero leakage too, up to the signs of the two dark amplitudes.
A0,B0,C0,D0 = map(s.Rational,(7,2,5,3))
u,v,w,t = responses(A0,B0,C0,D0)
delta = v/(u+v)
eta = t/(w+t)
lam = (w+t)/(u+v)
h = s.sqrt(delta/(1-delta))
z = s.sqrt((1-eta)*lam*(1+h**2))
j = s.sqrt(eta*lam*(1+h**2))
inverse = [(1+z)/2,(1-z)/2,(j+h)/2,(j-h)/2]
assert inverse == [c/(A0+B0) for c in (A0,B0,C0,D0)]

print(json.dumps({
    "status":"PASS",
    "original_record_p_one_identity":"0",
    "original_record_p_one_order":"4*p**3",
    "positive_path_ratios":["p:p**2:p*sqrt(p):p*sqrt(p)","p**2:p:p*sqrt(p):p*sqrt(p)"],
    "local_flip_toll": {"cost_unit":1,"mean_contrast":"4*p**3","absolute_order_mass":"1-4*p**4","tilted_p":float(tilted)},
    "nonzero_leakage_inverse": [str(c) for c in inverse],
    "physical_C_established":False
},ensure_ascii=False,indent=2))
