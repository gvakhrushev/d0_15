"""Exact controls for the terminal coherent-work criterion. No physical tariff is assigned."""
import json
import sympy as sp


def check_zero(expr):
    if isinstance(expr, sp.MatrixBase):
        for item in expr:
            check_zero(item)
    elif sp.simplify(expr) != 0:
        raise ValueError(str(expr))


q = sp.symbols("q", positive=True)
u, v = sp.sqrt(1-q), sp.sqrt(q)
vector = sp.Matrix([u, v, 0])
projector = sp.diag(0, 1, 0)
a, b, c, t = sp.symbols("a b c t", real=True)
work = sp.Matrix([[a, c, 0], [c, b, 0], [0, 0, t]])
mean = (vector.T * work * vector)[0]
slope = b-a+c*(1-2*q)/(u*v)
base = a+c*v/u
check_zero(sp.diff(mean, q)-slope)
check_zero((work-slope*projector-base*sp.eye(3))*vector)

# A false positive at one central probability is removed by the second.
bad = sp.Matrix([[0, 0, 1], [0, 0, -1], [1, -1, 0]])
check_zero(bad * vector.subs(q,sp.Rational(1,2)))
check_zero((bad * vector.subs(q,sp.Rational(1,5)))[2] - 1/sp.sqrt(5))

# An optimum genuinely requiring a complex relative phase on a two-mode slice.
# With fixed q, the only real phase choices yield the two endpoints.
x, y = sp.symbols("x y", positive=True)
k = sp.Matrix([x,y])
return_operator = k*k.T
for sign in (-1,1):
    w = sp.Matrix([u,sign*v])
    check_zero((w.T*return_operator*w)[0]-(x*u+sign*y*v)**2)
complex_state = sp.Matrix([u,sp.I*v])
midpoint = x*x*(1-q)+y*y*q
check_zero((sp.Matrix([[u,-sp.I*v]])*return_operator*complex_state)[0] - midpoint)
d, z, rank, moment, target = sp.symbols("d z rank moment target",positive=True)
h = -rank*sp.log(d+z*moment)
price = rank*z*moment/(d+z*target)+h
check_zero(sp.diff(price,moment).subs(moment,target))
check_zero(sp.diff(price,moment,2)-rank*z*z/(d+z*moment)**2)
print(json.dumps({"status":"PASS", "same_section_slope":"symbolic",
                  "one_probability_false_positive":True, "complex_midpoint_attains_optimum":True,
                  "full_physical_price_identified":False},indent=2))
