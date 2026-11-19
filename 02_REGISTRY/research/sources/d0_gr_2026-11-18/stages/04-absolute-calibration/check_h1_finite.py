"""Exact bounds and sampled first variations on the complete H.1 decision tree."""
import json
import math
import sympy as sp

p = (sp.sqrt(5)-1)/2
u = sp.simplify(p**2+p**4)
t = sp.simplify(u**2)
lo, hi = sp.simplify(p**3), sp.simplify(p**2)
assert sp.simplify(lo+p**4-hi) == 0
assert sp.simplify(lo/(1-lo)-p/2) == 0
assert sp.simplify(hi/(1-hi)-p) == 0
assert sp.simplify(t-(25-40*p)) == 0
assert t < p/2 < u < p
assert lo < u/(1+u) < hi
assert sp.simplify(u/(1+u)-(p**3+sp.Rational(3,4)*p**4)) == 0
assert sp.simplify(sum(p**n for n in (4,6,6,8))-t) == 0
p_float, t_float = float(p), float(t)
r, z = 4, 2.0**-20
lower = p_float**4*(1-z)*p_float*(p_float/2-t_float)/(r*z)
samples = []
for s in [0, .25, .5, .75, 1]:
    y = p_float**3+p_float**4*s
    collision = sum(w*w for w in [p_float,p_float**2])
    assert abs(collision**2-t_float) < 1e-12
    completed_event = y+(1-y)*collision**2
    assert abs(completed_event+(1-y)*(1-collision**2)-1) < 1e-12
    two_event = y*y+(1-y)**2*collision**2
    assert abs(two_event+2*y*(1-y)+(1-y)**2*(1-collision**2)-1)<1e-12
    for exponent in [1,1.25,1.5,1.75,2]:
        mass = y**exponent+t_float*(1-y)**exponent
        derivative = exponent*(y**(exponent-1)-t_float*(1-y)**(exponent-1))
        ratio = p_float**4*(1-z+z*s)*derivative/(r*z*mass)
        assert ratio > lower
        samples.append(ratio)
    h_prime = math.log((1-y)/y)
    assert h_prime >= -math.log(p_float)-1e-12
print(json.dumps(dict(status="PASS",proof="symbolic identities, rational-power monotonicity on [0,1] in the accompanying proof",
       leaves=5,two_refinement_mass_exact=str(sp.expand(t)),single_refinement_zero=float(u/(1+u)),
       strict_uniform_lower_at_r4_z2m20=lower,minimum_on_25_diagnostic_points=min(samples),
       microscopic_interface_verified=False,GR_closed=False),indent=2))
