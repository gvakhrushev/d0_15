#!/usr/bin/env python3
"""Exact short replay of the submitted Hodge reduction and its scope.

No four-variable determinant or factorization is recomputed. We verify
matrix identities, one small univariate chiral determinant, and local
kernel/cokernel derivative ranks. The rank-23 conclusion follows from
simple, disjoint polynomial roots, not from numerical root fitting.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
SOURCE = HERE/'A_and_mixed_symbol_entries.json'
LEDGER = HERE/'a4d_resonance_divisor_chiral_numerator.json'
data = json.loads(SOURCE.read_text())
z = sp.symbols('z0:4', nonzero=True)
A = sp.zeros(24)
for row,col,expr in data['A_entries']:
    A[row,col] = sp.sympify(expr, locals=dict(zip(data['coordinates'],z)))

star = sp.zeros(6)
for col,(row,sign) in enumerate([(5,-1),(4,1),(3,-1),(2,1),(1,-1),(0,1)]):
    star[row,col] = sign
omega = sp.diag(star,star,star,star)
columns = []
for chirality in (1,-1):
    for role in range(4):
        for j,k,sign in [(0,5,1),(1,4,-1),(2,3,1)]:
            v = sp.zeros(24,1)
            v[6*role+j] = 1
            v[6*role+k] = chirality*sign*sp.I
            columns.append(v)
T = sp.Matrix.hstack(*columns)
C = (T.inv()*A*T).applyfunc(sp.cancel)
M = C[:12,12:]
N = C[12:,:12]
congruence = (T.T*A*T).applyfunc(sp.cancel)

def zero(matrix):
    return all(sp.cancel(entry)==0 for entry in matrix)

checks = {}
def check(name, assertion):
    checks[name] = bool(assertion)
    if not assertion:
        raise AssertionError(name)

check('OMEGA_SQUARED_MINUS_ID',omega*omega==-sp.eye(24))
check('OMEGA_SKEW',omega.T==-omega)
check('ANTICOMMUTATOR_ZERO',zero(A*omega+omega*A))
check('SIMILARITY_OFF_DIAGONAL',zero(C[:12,:12]) and zero(C[12:,12:]))
check('CONGRUENCE_DIAGONAL',zero(congruence[:12,12:]) and zero(congruence[12:,:12]))
check('CONSTANT_T_DETERMINANT_4096',T.det()==4096)
check('COEFFICIENT_CONJUGATE_BLOCKS',zero(N-M.xreplace({sp.I:-sp.I})))
check('A_TRANSPOSE_RECIPROCITY',zero(A.xreplace({x:1/x for x in z})-A.T))
check('M_TRANSPOSE_RECIPROCITY',zero(M.xreplace({x:1/x for x in z})-M.T))
check('ALL_3_BY_3_ROLE_BLOCKS_SKEW',all(zero(M[3*r:3*r+3,3*s:3*s+3].T+M[3*r:3*r+3,3*s:3*s+3]) for r in range(4) for s in range(4)))

cleared = [sp.Poly(sp.expand(2*sp.prod(z)*entry),*z,extension=sp.I) for entry in M if entry!=0]
coefficients = [c for poly in cleared for c in poly.coeffs()]
check('CLEARED_M_GAUSSIAN_INTEGER_COEFFICIENTS',all(sp.re(c).is_Integer and sp.im(c).is_Integer for c in coefficients))
check('CLEARED_M_NOT_OVER_REAL_INTEGERS',any(sp.im(c)!=0 for c in coefficients))

# Explicit all-complex-character counterexample to universal even rank.
u = z[0]
f = ((151-48*sp.I)*u**6-396*u**5+(-178+252*sp.I)*u**4
     -2216*u**3+(-97-252*sp.I)*u**2-876*u+124+48*sp.I)
M_slice = M.subs(dict(zip(z[1:],(1,-1,2))))
det_M_slice = sp.cancel(M_slice.det(method='domain-ge'))
check('EXPLICIT_SEXTIC_DETERMINANT',sp.cancel(det_M_slice-f/(128*u**3))==0)
poly = sp.Poly(f,u,extension=sp.I)
conjugate_poly = sp.Poly(f.xreplace({sp.I:-sp.I}),u,extension=sp.I)
check('SEXTIC_ALL_ROOTS_SIMPLE',sp.gcd(poly,poly.diff()).degree()==0)
check('SEXTIC_CONJUGATE_ROOTS_DISJOINT',sp.gcd(poly,conjugate_poly).degree()==0)
check('SEXTIC_NO_ZERO_ROOT',poly.TC()!=0)
# Each root alpha is nonzero and a simple determinant zero: rank M=11.
# The other block has nonzero determinant there: rank N=12. Hence rank A=23.

at_i = dict.fromkeys(z,sp.I)
M_i = M.subs(at_i)
M_derivative = sum((M.diff(x).subs(at_i) for x in z),sp.zeros(12))
right = sp.Matrix.hstack(*M_i.nullspace())
left = sp.Matrix.vstack(*[v.T for v in M_i.T.nullspace()])
check('M_QUARTER_WAVE_RANK_8',M_i.rank()==8)
check('M_QUARTER_WAVE_FIRST_DERIVATIVE_RANK_2',(left*M_derivative*right).applyfunc(sp.expand).rank()==2)

ledger = json.loads(LEDGER.read_text())
terms = {tuple(row[:4]):sp.sympify(row[4]) for row in ledger['terms']}
check('P_PLUS_NUMERATOR_RECIPROCITY',all(terms.get(tuple(6-e for e in powers),0)==coefficient for powers,coefficient in terms.items()))
result = {
    'schema':1,
    'baseline_main':'e80a3b1ccf615fb4f70bf5900181592604928497',
    'live_PR317_head':'bfe9e28d4f424851085260d8ca7ec0f1403961d8',
    'A_source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'P_plus_ledger_sha256':hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
    'checks':checks,
    'cleared_M_nonzero_entries':len(cleared),
    'cleared_M_distinct_monomials':len(set(powers for poly in cleared for powers,c in poly.terms())),
    'cleared_M_total_terms':sum(len(poly.terms()) for poly in cleared),
    'rank_23_counterexample':{
        'characters':['alpha','1','-1','2'],
        'alpha_definition':'any complex root of f; all are nonzero and simple',
        'f':str(sp.expand(f)),
        'det_M':str(f/(128*u**3)),
        'rank_M':11,'rank_coefficient_conjugate_M':12,'rank_A':23,
        'reason':'simple determinant root and coprime conjugate determinant',
    },
    'theorem_on_physical_torus':{
        'N_equals_M_adjoint':True,
        'rank_A_equals_2_rank_M':True,
        'det_A_equals_abs_det_M_squared_nonnegative':True,
        'physical_resonance_in_both_conjugate_factor_zero_loci':True,
        'derivation':'coefficient conjugation plus simultaneous-inversion transpose reciprocity',
    },
    'scope':'Exact Hodge structural identities and one algebraic rank-23 counterexample; not complete complex rank strata, absolute irreducibility or a stationary metric-response theorem.',
    'terminal':'A4D_HODGE_REDUCTION_SCOPE_AND_ODD_COMPLEX_RANK_VERIFIED',
}
out=HERE/'a4d_hodge_structural_review_results.json'
out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('PASS',len(checks),'exact checks')
print('RANK23_COUNTEREXAMPLE',result['rank_23_counterexample']['f'])
print('PHYSICAL_RANK_DOUBLING_ONLY',True)
print('RESULT',out)
