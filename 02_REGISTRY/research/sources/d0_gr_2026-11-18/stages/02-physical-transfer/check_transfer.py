"""Exact checks of the scalar recurrences, finite-horizon test, and carrier field."""
import json
import sympy as sp
import mpmath as mp

s, x, total, baseline, beta, report = sp.symbols("s x A B beta R", positive=True)
u = 1 - s
c0, c1 = 1, 4*s - 3
d0, d1 = 1, 4*s - 1
for m in range(12):
    assert sp.expand(s*c0**2 + u*d0**2 - 1) == 0
    c0, c1 = c1, sp.expand((4*s-2)*c1-c0)
    d0, d1 = d1, sp.expand((4*s-2)*d1-d0)

# Recover the underlying report on one regenerative programme at several caps.
costs = [baseline + total*sum(x**j for j in range(n)) for n in range(5)]
delta = [sp.expand(y-z) for y,z in zip(costs[1:], costs[:-1])]
assert sp.cancel(delta[1]/delta[0] - x) == 0
assert sp.cancel(delta[2]/delta[1] - x) == 0
assert sp.expand(delta[2]**2-delta[1]*delta[3]) == 0
field = sp.symbols("y")
vary = {v:sp.Function(str(v))(field) for v in [baseline, total, beta, report]}
vary[x] = vary[beta]*vary[report]
varying = [v.subs(vary, simultaneous=True) for v in costs]
recovered = (varying[2]-varying[1])/((varying[1]-varying[0])*vary[beta])
assert sp.simplify(recovered.diff(field)-vary[report].diff(field)) == 0

p = (sp.sqrt(5)-1)/2
target = 1/(1+p**2)
t = sp.symbols("t")
assert sp.Poly(sp.minpoly(target,t),t) == sp.Poly(5*t**2-5*t+1,t)
assert sp.simplify((3+p)/5 - target) == 0

mp.mp.dps = 55
pnum = (mp.sqrt(5)-1)/2
snum = pnum**2 + pnum**4
alpha = mp.asin(mp.sqrt(snum))
theta = mp.atan(pnum)
# An explicit lower cost two-word observable uses no approximation.
heat_bound = mp.mpf(528)/1077*9*(mp.mpf(8)/5)**52/mp.factorial(52)
z = mp.mpf(2)**(-20)
j_difference_per_rank = -mp.log(1-z+z*pnum**6)
assert (heat_bound<mp.mpf("2.26e-57") and
        j_difference_per_rank-heat_bound>mp.mpf("9e-7"))
# First actual lengths giving success and the uncut error at the stated levels.
examples = []
m = 0
for exp in [1,2,3,4]:
    while True:
        good = mp.sin((2*m+1)*alpha)
        error = mp.sqrt(2*(1-good))
        if error < mp.mpf(10)**(-exp):
            break
        m += 2
    examples.append({"m":m,"square_calls":92*m+26,"column_error":float(error)})
print(json.dumps({"status":"PASS","exact_recurrences_checked":12,
 "horizon_observation_and_derivative":"exact, including all common varying charges",
 "minimum_polynomial_of_return_probability":"5*t**2-5*t+1",
 "heat_bound_L52":float(heat_bound),"feedback_contrast_per_rank":float(j_difference_per_rank),
 "first_even_amplification_examples":examples,"physical_C_closed":False,"GR_closed":False},
 indent=2))
