#!/usr/bin/env python3
"""T3 archive leg: the hull sum spectrum generates the biquadratic K = Q(sqrt2,sqrt5) and
Gal(K/Q) = V4 acts simply transitively on it, factor-wise: golden conjugation (fixes Q(sqrt10)),
window swap c<->r (fixes Q(sqrt5)), double swap (fixes Q(sqrt2)). Exit 1 on failure."""
import sympy as sp, sys
s5, s10 = sp.sqrt(5), sp.sqrt(10)
g = [(-1+s5)/2, (-1-s5)/2]                       # toral time pair {phi^-1, -phi}, Q(sqrt5)
w = [sp.Rational(3,2)-s10/40, sp.Rational(3,2)+s10/40]   # archive window pair, Q(sqrt10)
S = [[sp.simplify(gi+wj) for wj in w] for gi in g]
s11 = S[0][0]
ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name); ok = ok and bool(cond)
def conj(e, f5, f10):
    if f5: e = e.subs(s5, -s5)
    if f10: e = e.subs(s10, -s10)
    return sp.simplify(e)
def find(e):
    for i in range(2):
        for j in range(2):
            if sp.simplify(e - S[i][j]) == 0: return (i,j)
check("joint spectrum generates K (min poly degree 4)", sp.degree(sp.minimal_polynomial(s11, sp.Symbol('x'))) == 4)
check("sigma fixing Q(sqrt10) = golden conjugation only", find(conj(s11, True, False)) == (1,0))
check("sigma fixing Q(sqrt5)  = window swap only",        find(conj(s11, False, True)) == (0,1))
check("sigma fixing Q(sqrt2)  = double swap",             find(conj(s11, True, True)) == (1,1))
check("V4 simply transitive on the quadruple", {find(conj(s11,a,b)) for a in (0,1) for b in (0,1)} == {(0,0),(0,1),(1,0),(1,1)})
# negative control: a NON-Galois substitution (sqrt10 -> 2*sqrt10) does not permute the spectrum
check("negative control: non-Galois map leaves the spectrum", find(sp.simplify(s11.subs(s10, 2*s10))) is None)
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
