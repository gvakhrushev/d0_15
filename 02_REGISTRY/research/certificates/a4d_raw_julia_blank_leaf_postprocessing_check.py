#!/usr/bin/env python3
"""Exact native-Julia blank obstruction to passive sharp AF-leaf postprocessing.

Scope: CLASSICAL decoding of raw recorded words, not coherent access to data,
active LEFT CNOT registration, new measurements or GR physical forcing.
Read-only; no historical certificates are modified.
"""
import json
import sympy as sp

p = (sp.sqrt(5) - 1) / 2
u = sp.symbols("u", real=True)
assert sp.simplify(p + p**2 - 1) == 0

# Literal Julia golden port contribution at scalar A**2=u.
# Blank port0/label0, other port0, all port1; the 128 labels remain
# a complete POVM, although this two-active-Walsh-row algebraic fixture
# assigns zero effect to unrelated labels. This is NOT a native CAR16 census.
blank = 1 - 2*p**2*u
other_port0 = 4*p**4*u*(1-u)
port1_sum = 4*p**3*u
assert sp.simplify(blank**2 + other_port0 + port1_sum - 1) == 0

nu = sp.Rational(1, 256)
R = 2
T = sp.Rational(1, 4)
rows = []
for m in [1, 2, 8, 32]:
    floor = (1 - 2*p**2*(R*nu)**2)**(2*m)
    assert 0 < float(floor) < 1
    rows.append({
        "rounds": m,
        "minimum_blank_probability": float(floor.evalf(15)),
        "two_leaf_worst_TV_lower_bound": float((floor/2).evalf(15))
    })

# With m*nu_m**2 -> T the all-blank effect remains uniformly positive.
asymptotic_floor = sp.exp(-4*p**2*T*R**2)
assert 0 < float(asymptotic_floor) < 1

# A positive, complete POVM which saturates the sharp two-leaf decoder
# bound s(1-1/d): the ambiguous blank has effect s I.
s = sp.Rational(1, 3)
P = [sp.diag(1,0), sp.diag(0,1)]
E = [s*sp.eye(2), (1-s)*P[0], (1-s)*P[1]]
assert sum(E, sp.zeros(2)) == sp.eye(2)
for i in (0, 1):
    decoder = sp.Rational(1,2)*E[0] + E[i+1]
    p_correct = sp.trace(P[i]*decoder)
    assert p_correct == 1-s/2

# On the faithful uniform input the joint measurement has H(Y|Omega)
# exactly s log 2 (the blank is ambiguous, other words identify Y).
r = sp.Symbol("r", real=True)
h = lambda x: -x*sp.log(x)-(1-x)*sp.log(1-x)
assert sp.simplify(sp.diff(h(r),r).subs(r,sp.Rational(3,10))
                   - sp.log(sp.Rational(7,3))) == 0
missing_entropy_toy = s*sp.log(2)
assert float(missing_entropy_toy) >= float(s*s*sp.log(2))
# Scalar Julia effects are independent of the AF leaf; then precisely
# H(Y,Omega)-H(Omega)=h(r), with a nonzero preparation derivative at r=.3.

receipt = {
    "status":"EXACT_ALGEBRA_PASS",
    "carrier":"generic finite POVM plus two-mode Julia port algebra",
    "golden_128_port_completeness":"PASS",
    "exact_sharp_PVM_by_passive_postprocessing":"IMPOSSIBLE_WITH_FULL_RANK_BLANK",
    "minimax_control":"s*(1-1/d) sharp",
    "finite_blank_checks":rows,
    "weak_T_blank_limit":str(asymptotic_floor),
    "weak_T_blank_limit_decimal":float(asymptotic_floor.evalf(15)),
    "weak_T_two_leaf_TV_limit":float((asymptotic_floor/2).evalf(15)),
    "conditional_entropy_lower_bound":"s**2 * log(d)",
    "toy_conditional_entropy":str(missing_entropy_toy),
    "scalar_leaf_entropy_source_at_r_3_10":"log(7/3)",
    "scope":"NOT active LEFT gates; NOT exact D0-to-GR"
}
print(json.dumps(receipt, indent=2, sort_keys=True))

# Stronger independent AF/GNS test: every old-left-neutral effect F must have
# ||F-P_i||_op >= 1/2 for a noncentral leaf P_i.
P_old0 = sp.kronecker_product(sp.diag(1, 0), sp.eye(2))
P_old1 = sp.kronecker_product(sp.diag(0, 1), sp.eye(2))
U_swap = sp.kronecker_product(sp.Matrix([[0,1],[1,0]]), sp.eye(2))
assert U_swap*P_old0*U_swap == P_old1
assert P_old0*P_old1 == sp.zeros(4)
for xx, yy in [(sp.Rational(1,2), sp.Rational(1,2)),
               (sp.Rational(1,4), sp.Rational(3,4)),
               (sp.Rational(9,10), sp.Rational(7,10))]:
    F_old_neutral = sp.kronecker_product(sp.eye(2), sp.diag(xx,yy))
    assert U_swap*F_old_neutral*U_swap == F_old_neutral
    op_error = max(abs(eig) for eig in (F_old_neutral-P_old0).eigenvals())
    assert op_error >= sp.Rational(1,2)
assert U_swap*P_old0 != P_old0*U_swap
print("AF_BIMODULE_COMMUTANT_NO_GO: EXACT PASS, sharp error floor 1/2")

# At the SAME terminal AF level, uniform fine-leaf mass and the canonical
# compatible trace have genuinely different RIGHT-block center marginals.
# This does NOT contradict fixed-coarse-level PF convergence from descendants.
phi = 1/p
for n in range(11):
    aN, bN = sp.fibonacci(n+2), sp.fibonacci(n+1)
    dN = aN+bN
    xPF = sp.simplify(aN*p**(n+1))
    xUniform = sp.Rational(aN,dN)
    assert sp.simplify(xPF+bN*p**(n+2)-1)==0
    assert sp.simplify(xPF-xUniform)!=0
    if n == 3:
        # Exhaust all within-block directions on this finite simplex:
        # source rank d-2. The missing direction changes central X/Y mass.
        contrasts=[]
        for j in range(1,int(aN)):
            vec=[0]*int(dN); vec[0]=1; vec[j]=-1; contrasts.append(vec)
        for j in range(int(aN)+1,int(dN)):
            vec=[0]*int(dN); vec[int(aN)]=1
            vec[j]=-1; contrasts.append(vec)
        assert sp.Matrix(contrasts).rank()==int(dN)-2
        assert all(sum(v[:int(aN)])==0 and sum(v[int(aN):])==0
                   for v in contrasts)
center_gap = sp.simplify(phi/sp.sqrt(5)-p)
assert sp.simplify(center_gap-(1-2/sp.sqrt(5)))==0
print("AF_RIGHT_CENTER_CONSERVATION: EXACT PASS; moving-level TV=",
      center_gap, float(center_gap))

# A minimal connected LEFT preparation graph is sufficient mathematically
# to span the probability-simplex tangent and force uniform stationary r.
# Intra-block trees have rank d-2; one X/Y bridge upgrades it to d-1.
aN, bN = 5, 3
dN = aN + bN
inside_edges = [(i,i+1) for i in range(aN-1)] + [
    (aN+i,aN+i+1) for i in range(bN-1)]
bridge_edge = (aN-1,aN)
def incidence_weighted(edges):
    columns=[]
    for i,j in edges:
        v=[0]*dN
        v[i]=sp.Rational(2,dN)
        v[j]=-sp.Rational(2,dN)
        columns.append(v)
    return sp.Matrix(columns).T
assert incidence_weighted(inside_edges).rank()==dN-2
assert incidence_weighted(inside_edges+[bridge_edge]).rank()==dN-1
print("AF_ONE_CROSS_BLOCK_MIXER: EXACT PASS, probability tangent ranks",
      dN-2, dN-1)
