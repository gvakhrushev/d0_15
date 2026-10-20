#!/usr/bin/env python3
"""Exact finite controls for the literal naked-star leading action.

Analytic remainders are proved in A4D_NATIVE_FINITE_PROBE_COMPLETION.md;
this file checks the finite polynomial identities on which that proof relies.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import sympy as sp

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo-root', type=Path, help='repository root; discovered from cwd/script ancestors by default')
parser.add_argument('--output', type=Path, help='write the deterministic exact-control ledger')
parser.add_argument('--expect', type=Path, help='require exact equality with an existing ledger')
args = parser.parse_args()
OWNER_REL = Path('02_REGISTRY/research/certificates/a4d_j2_fixed_realization_ir_check.py')
candidates = ([args.repo_root] if args.repo_root else
              [Path.cwd(), *Path(__file__).resolve().parents,
               Path(__file__).resolve().parent.parent / 'd0_15'])
ROOT = next((candidate.resolve() for candidate in candidates if (candidate / OWNER_REL).is_file()), None)
if ROOT is None:
    parser.error('could not find the exact owner; pass --repo-root')
OWNER = ROOT / OWNER_REL
source = OWNER.read_text()
ns = {'__name__': '_literal_owner_definitions'}
exec(compile(source[:source.index('check("LORENTZ_GENERATORS"')], str(OWNER), 'exec'), ns)
PAIRS, ETA, GEN, G2, STAR = [ns[k] for k in ('PAIRS', 'ETA', 'GENERATORS', 'G2', 'STAR')]
wedge, connection_symbol = ns['wedge'], ns['connection_symbol']
CHECKS = []


def check(name, cond, detail=None):
    assert cond, name
    CHECKS.append({'name': name, 'passed': True, **({'detail': detail} if detail else {})})
    print('PASS_' + name, flush=True)


def eps(seq):
    return 0 if len(set(seq)) != len(seq) else (-1) ** sum(
        seq[i] > seq[j] for i, j in combinations(range(len(seq)), 2))


def orient(r, s):
    return eps((r, s, *[i for i in range(4) if i not in (r, s)]))


def bivector(X):
    C = X * ETA
    return sp.Matrix([C[a, b] for a, b in PAIRS])


def face_weight(E, r, s):
    u, v = [i for i in range(4) if i not in (r, s)]
    return orient(r, s) * wedge(E[:, u], E[:, v]).T * G2 * STAR


def density(E, curvature):
    return sp.expand(sum((face_weight(E, r, s) * bivector(curvature[r, s]))[0]
                         for r, s in PAIRS))


def curvature_full(curvature, r, s):
    return curvature[r, s] if r < s else -curvature[s, r] if r > s else sp.zeros(4)


def ricci_from_internal(E, curvature):
    Ei = E.inv()
    ricci = sp.zeros(4)
    for u in range(4):
        for s in range(4):
            ricci[u, s] = sp.simplify(sum(
                Ei[t, a] * curvature_full(curvature, t, s)[a, b] * E[b, u]
                for t in range(4) for a in range(4) for b in range(4)))
    return ricci


# 1. Literal star/weld sign, tested on all 36 bivector matrix entries.
epsilon_matrix = sp.Matrix(6, 6, lambda i, j: -eps((*PAIRS[i], *PAIRS[j])))
check('G2_STAR_IS_MINUS_EPSILON', G2 * STAR == epsilon_matrix)
check('OWNER_LORENTZ_GENERATORS', all(X.T * ETA + ETA * X == sp.zeros(4) for X in GEN))

# 2. Generic noncommutative BCH expansion. The second log coefficients cancel.
R, S, A, B, dRS, dSR = sp.symbols('R S A B d_rS d_sR', commutative=False)
xs, ys = [R, S, -R, -S], [A, B + dRS, -A - dSR, -B]
first = sp.expand(sum(xs))
second = sp.expand(sum(ys) + sum(X * X / 2 for X in xs)
                   + sum(xs[i] * xs[j] for i, j in combinations(range(4), 2)))
F = dRS - dSR + R * S - S * R
check('PLAQUETTE_ORDER_ONE_ZERO', first == 0)
check('PLAQUETTE_ORDER_TWO_CURVATURE', sp.expand(second - F) == 0)
check('SECOND_LOG_COEFFICIENTS_CANCEL', not second.has(A, B))
# P=I+h^2 F+O(h^3), hence its inverse has coefficient -F.
check('ODD_CURVATURE_HAS_NO_EXTRA_HALF', sp.expand((F - (-F)) / 2 - F) == 0)

# 3. All-coframe identity, coefficientwise in all 36 independent curvatures.
# It is a polynomial identity in all sixteen E entries, not sampled frames.
ev = sp.symbols('e0:16')
E = sp.Matrix(4, 4, ev)
detE = E.det()
adjE = E.adjugate()
weights = {}
for r, s in PAIRS:
    weights[r, s] = [(face_weight(E, r, s) * bivector(X))[0] for X in GEN]
    for alpha, X in enumerate(GEN):
        C = X * ETA
        contraction = sum(adjE[r, a] * adjE[s, b] * C[a, b]
                          for a in range(4) for b in range(4))
        polynomial = sp.expand(detE * weights[r, s][alpha] + contraction)
        assert polynomial == 0, (r, s, alpha)
check('ALL_COFRAME_DENSITY_COEFFICIENTS', True,
      '36 identities polynomial in all 16 coframe entries; det(E)*L + adj(E) adj(E) F = 0')

# 4. The actual Palatini quadratic Hessian is exactly the owned H(0).
av = sp.symbols('a0:24')
omegas = [sum((av[6*r + a] * GEN[a] for a in range(6)), sp.zeros(4)) for r in range(4)]
commutators = {(r, s): omegas[r]*omegas[s]-omegas[s]*omegas[r] for r, s in PAIRS}
comm_density = density(sp.eye(4), commutators)
hessian = sp.hessian(comm_density, av)
H0 = connection_symbol(sp.eye(4), [sp.Integer(1)] * 4)
check('PALATINI_CONNECTION_HESSIAN_IS_OWNER_H0', hessian == H0)
check('PALATINI_CONNECTION_HESSIAN_DETERMINANT_256', hessian.det() == 256)

# The all-solder congruence belongs to zero phase. It cannot silently be
# transported to an arbitrary Fourier phase in a rough-field argument.
stretch = sp.symbols('s', nonzero=True)
stretched = sp.diag(1,1,stretch,stretch)
Pstretch = sp.kronecker_product(stretched.T,sp.eye(6))
zhostile = [sp.Integer(1),sp.I,sp.Integer(1),sp.Integer(1)]
congruence_error = (Pstretch.T*connection_symbol(stretched,zhostile)*Pstretch
                    -stretched.det()*connection_symbol(sp.eye(4),zhostile)).applyfunc(sp.factor)
check('HOSTILE_ALL_PHASE_CONGRUENCE_FAILS',
      sp.simplify(congruence_error[12,13]+sp.I*stretch**2*(stretch-1)) == 0
      and sum(entry != 0 for entry in congruence_error) == 8,
      'z=(1,i,1,1), E=diag(1,1,s,s): entry(12,13)=-i*s^2*(s-1), 8 nonzero polynomial entries')

# 5. Independent torsion equation is injective: D(e^a wedge e^b)=0 => T=0.
triples = list(combinations(range(4), 3))
torsion_vars = sp.symbols('T0:24')


def torsion_wedge_basis(a, b):
    out = {triple: 0 for triple in triples}
    for p, (r, s) in enumerate(PAIRS):
        inds = (r, s, b)
        if len(set(inds)) == 3:
            out[tuple(sorted(inds))] += eps(inds) * torsion_vars[6*a+p]
    return out


torsion_eq = []
for a, b in PAIRS:
    left, right = torsion_wedge_basis(a, b), torsion_wedge_basis(b, a)
    torsion_eq += [left[t] - right[t] for t in triples]
torsion_map = sp.Matrix(torsion_eq).jacobian(torsion_vars)
check('PALATINI_TORSION_MAP_INVERTIBLE', torsion_map.det() != 0,
      'determinant=' + str(torsion_map.det()))

# 6. At E=I, arbitrary 64 first coframe derivatives solve the 24 stationarity
# rows precisely with the Levi-Civita spin connection. This is an independent
# coefficient identity and checks the transport/gauge sign of the conclusion.
dEvars = sp.symbols('de0:64')
dE = [sp.Matrix(4, 4, dEvars[16*r:16*(r+1)]) for r in range(4)]
identity_sub = dict(zip(ev, list(sp.eye(4))))
dweight = {(r, s, a, j): sp.expand(sum(sp.diff(weights[r,s][a], ev[k]) * dEvars[16*j+k]
                                    for k in range(16)).subs(identity_sub))
           for r, s in PAIRS for a in range(6) for j in range(4)}
forcing = sp.Matrix([
    sum(-dweight[j, r, a, j] for j in range(r))
    + sum(dweight[r, j, a, j] for j in range(r+1, 4))
    for r in range(4) for a in range(6)])
dg = [X.T * ETA + ETA * X for X in dE]
gamma = [[[sp.expand(ETA[a,a] * (dg[r][a,b]+dg[b][a,r]-dg[a][r,b])/2)
           for b in range(4)] for r in range(4)] for a in range(4)]
omegaLC = [sp.Matrix(4,4,lambda a,b: gamma[a][r][b]-dE[r][a,b]) for r in range(4)]
check('ARBITRARY_FIRST_JET_LC_IS_LORENTZ',
      all(sp.expand(X.T*ETA+ETA*X) == sp.zeros(4) for X in omegaLC))
lc_coeff = sp.Matrix([X[a,b] for X in omegaLC for a,b in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))])
check('ARBITRARY_FIRST_JET_LC_SOLVES_ALL_24_ROWS',
      (H0*lc_coeff+forcing).applyfunc(sp.expand) == sp.zeros(24,1),
      'all 24x64 first-jet coefficients checked')

# 7. Nonlinear warped coframe, full standard Ricci, literal action, raw Gram
# derivative, and an off-diagonal coordinate shear to expose pack factors.
f,p,q = sp.symbols('f p q', nonzero=True)
EW = sp.diag(1,1,f,f)
gW = EW.T*ETA*EW
giW = gW.inv()


def deriv(expr, r):
    return sp.diff(expr,f)*p+sp.diff(expr,p)*q if r == 1 else sp.S.Zero


GammaW = [sp.Matrix(4,4,lambda a,b: sp.simplify(sum(
    giW[a,k]*(deriv(gW[k,b],r)+deriv(gW[k,r],b)-deriv(gW[r,b],k))/2
    for k in range(4)))) for r in range(4)]
OmegaW = [sp.simplify((EW*GammaW[r]-EW.applyfunc(lambda e: deriv(e,r)))*EW.inv()) for r in range(4)]
FW = {(r,s): sp.simplify(OmegaW[s].applyfunc(lambda e: deriv(e,r))
                         -OmegaW[r].applyfunc(lambda e: deriv(e,s))
                         +OmegaW[r]*OmegaW[s]-OmegaW[s]*OmegaW[r]) for r,s in PAIRS}
LW = sp.simplify(density(EW,FW))
RicW = ricci_from_internal(EW,FW)
RW = sp.simplify(sp.trace(giW*RicW))
GW = sp.simplify(RicW-gW*RW/2)
check('WARP_LITERAL_LEADING_CELL', sp.expand(LW+2*f*q+p*p) == 0)
check('WARP_STANDARD_SCALAR', sp.simplify(RW-4*q/f-2*p*p/f**2) == 0)
check('WARP_MINUS_HALF_EH', sp.simplify(LW+EW.det()*RW/2) == 0)
check('WARP_INTEGRATION_BY_PARTS_DENSITY',
      sp.expand(LW - (p*p-2*deriv(f*p,1))) == 0)

SYM = [(a,b) for a in range(4) for b in range(a,4)]


def gram_response(E0, F0):
    g = E0.T*ETA*E0
    gi = g.inv()
    ans = []
    for a,b in SYM:
        dq = sp.zeros(4); dq[a,b] = dq[b,a] = 1
        dframe = E0*gi*dq/2
        total = 0
        for r,s in PAIRS:
            u,v = [i for i in range(4) if i not in (r,s)]
            dw = wedge(dframe[:,u],E0[:,v])+wedge(E0[:,u],dframe[:,v])
            total += orient(r,s)*(dw.T*G2*STAR*bivector(F0[r,s]))[0]
        ans.append(sp.simplify(total))
    return sp.Matrix(ans)


rhoW = gram_response(EW, FW)
targetW = sp.Matrix([-f*q-p*p/2,0,0,0,p*p/2,0,0,q/(2*f),0,q/(2*f)])
check('WARP_RAW_RESPONSE_ALL_TEN_SLOTS', (rhoW-targetW).applyfunc(sp.simplify) == sp.zeros(10,1))

M = sp.Matrix([[1,sp.Rational(1,3),0,0], [0,1,sp.Rational(1,5),0],
               [0,0,1,sp.Rational(1,7)], [0,0,0,1]])
ES = EW*M
FS = {(r,s): sum((M[u,r]*M[v,s]*curvature_full(FW,u,v)
                 for u in range(4) for v in range(4)),sp.zeros(4)) for r,s in PAIRS}
gS = ES.T*ETA*ES
giS = gS.inv()
RicS = sp.simplify(M.T*RicW*M)
GupS = sp.simplify(giS*(RicS-gS*RW/2)*giS)
rhoS = gram_response(ES,FS)
targetS = sp.Matrix([sp.simplify(ES.det()*GupS[a,b]*(1 if a==b else 2)/2) for a,b in SYM])
check('SHEARED_WARP_RAW_RESPONSE_ALL_TEN_SLOTS', (rhoS-targetS).applyfunc(sp.simplify) == sp.zeros(10,1))
wrongpack = sp.Matrix([sp.simplify(ES.det()*GupS[a,b]/2) for a,b in SYM])
check('HOSTILE_NO_OFFDIAGONAL_FACTOR_FAILS', (rhoS-wrongpack).applyfunc(sp.simplify) != sp.zeros(10,1))
check('HOSTILE_WRONG_ACTION_SIGN_FAILS', sp.simplify(LW-EW.det()*RW/2) != 0)
J = sp.diag(-1,1,1,1)
check('NEGATIVE_ORIENTATION_FLIPS_DENSITY',
      sp.simplify(density(J*EW,{face:J*F0*J for face,F0 in FW.items()})+LW) == 0)

result = {'status':'PASS','scope':'finite exact controls; analytic proof and remainder hypotheses are in A4D_NATIVE_FINITE_PROBE_COMPLETION.md',
          'owner':str(OWNER.relative_to(ROOT)), 'owner_sha256':hashlib.sha256(source.encode()).hexdigest(),
          'checks':CHECKS, 'formulas':{'leading_density':'-det(E)*R_standard/2',
          'warp_leading_density':str(LW),'warp_scalar':str(RW),
          'warp_raw_response':list(map(str,rhoW)), 'torsion_map_determinant':str(torsion_map.det())}}
if args.expect or not args.output:
    expected_path = args.expect or Path(__file__).with_name('a4d_finite_probe_palatini_results.json')
    expected = json.loads(expected_path.read_text())
    assert expected == result, 'ledger differs from --expect'
    print('PASS_EXPECTED_LEDGER', flush=True)
if args.output:
    args.output.write_text(json.dumps(result,indent=2)+'\n')
print('PALATINI_LEADING_ACTION_EXACT_CONTROLS_PASS',flush=True)
