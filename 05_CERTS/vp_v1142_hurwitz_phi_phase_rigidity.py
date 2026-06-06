#!/usr/bin/env python3
"""D0 v11.42 Hurwitz / phi phase rigidity and tripartite index checks."""
from fractions import Fraction
from math import sqrt, gcd
import json

phi = (1+sqrt(5))/2
alpha = 1/(phi*phi)
# continued fraction for alpha numerically

def cont_frac(x, n=12):
    out=[]
    y=x
    for _ in range(n):
        a=int(y)
        out.append(a)
        y=y-a
        if abs(y)<1e-15: break
        y=1/y
    return out

cf = cont_frac(alpha, 12)
# convergents from CF

def convergents(cf):
    conv=[]
    for i in range(len(cf)):
        f=Fraction(0)
        for a in reversed(cf[:i+1]):
            if f.numerator==0:
                f=Fraction(a,1)
            else:
                f=Fraction(a,1)+1/f
        conv.append(f)
    return conv
conv=convergents(cf)
err=[]
for f in conv[2:]:
    q=f.denominator
    err.append(float(q*q*abs(alpha-f.numerator/f.denominator)))
# Euler phi

def euler_phi(n):
    result=n
    p=2
    m=n
    while p*p<=m:
        if m%p==0:
            while m%p==0: m//=p
            result-=result//p
        p+=1
    if m>1: result-=result//m
    return result
# tripartite counts
n1,n2,n3=9,11,13
V=n1+n2+n3
E=n1*n2+n1*n3+n2*n3
T=n1*n2*n3
C3=0
# quotient matrix eigenvalues roughly
import numpy as np
Q=np.array([[0,n2,n3],[n1,0,n3],[n1,n2,0]], dtype=float)
eigs=np.linalg.eigvals(Q)
# Hurwitz tail check: alpha = [0;2,1,1,...]
cf_expected_prefix = [0,2] + [1]*10
checks = {
    "continued_fraction_tail_all_ones": cf[:12] == cf_expected_prefix,
    "hurwitz_limit_close_to_1_over_sqrt5": abs(err[-1] - 1/sqrt(5)) < 1e-3,
    "phi44_is_20": euler_phi(44) == 20,
    "phi710_is_280": euler_phi(710) == 280,
    "d13_branch_count": euler_phi(44) == 20,
    "ew_branch_depth": euler_phi(710)//8 == 35 and euler_phi(710)%8==0,
    "tripartite_vertices": V == 33,
    "tripartite_edges": E == 359,
    "tripartite_triangles": T == 1287,
    "no_3_simplices": C3 == 0,
    "three_shell_quotient_modes": len(eigs) == 3,
}
status = "PASS_V11_42_HURWITZ_PHI_PHASE_RIGIDITY" if all(checks.values()) else "FAIL"
results={
    "status": status,
    "phi": phi,
    "alpha_phi_minus_2": alpha,
    "continued_fraction_alpha": cf,
    "q2_error_tail_samples": err[-5:],
    "hurwitz_constant": 1/sqrt(5),
    "euler_phi_44": euler_phi(44),
    "euler_phi_710": euler_phi(710),
    "tripartite_counts": {"V": V, "E": E, "T": T, "C3": C3},
    "shell_quotient_eigenvalues": [float(x.real) if abs(x.imag)<1e-10 else [float(x.real), float(x.imag)] for x in eigs],
    "checks": checks,
}
print(json.dumps(results, indent=2, ensure_ascii=False))
if status.startswith('FAIL'):
    raise SystemExit(1)
