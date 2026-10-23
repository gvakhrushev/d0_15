#!/usr/bin/env python3
"""Exact controls for the actual archive seam action / Palatini gate boundary.

Uses D=L_f J-J L_c with the repository's cyclic phase lift. It does not
replace D by a freely encoded detector. Frozen-fine stationarity, local
conductance variations, two genuine Born contrasts, and the literal
Palatini Hessian are checked. Default replay never rewrites its ledger.
"""
from __future__ import annotations
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys
import sympy as sp

INPUTS = [
    '03_FORMALIZATION/D0/Geometry/ArchiveSeamCurvature.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCurvatureDensity.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveVariation.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveLocalLaplacianVariation.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCanonicalLaplacian.lean',
    '02_REGISTRY/research/certificates/a4d_j2_fixed_realization_ir_check.py',
    '02_REGISTRY/research/certificates/a4d_identity_quarter_nonlinear_response_check.py',
]


def cycle(m):
    assert m >= 3
    out = sp.zeros(m)
    for i in range(m):
        for j in ((i-1) % m, (i+1) % m):
            out[i, j] = -1
        out[i, i] = 2
    return out


def lift(m):
    out = sp.zeros(m+1, m)
    for i in range(m+1):
        out[i, i % m] = 1
    return out


def edge_basis(m, local):
    pairs = [(i, (i+1) % m) for i in range(m)] if local else list(combinations(range(m), 2))
    out = []
    for i, j in pairs:
        b = sp.zeros(m, 1)
        b[i], b[j] = 1, -1
        out.append(b*b.T)
    return pairs, out


def inner(a, b):
    return sum(x*y for x, y in zip(a, b))


def enc(value):
    if isinstance(value, sp.MatrixBase):
        return [[str(value[i, j]) for j in range(value.cols)] for i in range(value.rows)]
    return str(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    checks = []
    def check(name, ok):
        assert ok, name
        checks.append(name)
        print('PASS_' + name, flush=True)

    # The old full variation has only symmetry and row-sum equations;
    # the newer local owner gives the genuine off-diagonal support rule.
    old = (repo / INPUTS[2]).read_text()
    local = (repo / INPUTS[3]).read_text()
    check('ACTUAL_FROZEN_FINE_VARIATION_SOURCE',
          '- rectangularMatrixMul (archiveLiftOperator n) δ.dL' in old)
    check('OLD_SUPPORT_PROP_AND_NEW_GENUINE_LOCAL_PREDICATE',
          'local_support : Prop' in old and '¬ rolePhaseAdjacent n x y → dL x y = 0' in local)

    rows = []
    for m in (3, 4, 5, 6):
        J, Lc, Lf = lift(m), cycle(m), cycle(m+1)
        D = Lf*J-J*Lc
        check(f'ACTUAL_CANONICAL_SEAM_{m}',
              inner(D, D) == 4 and D.rank() == 2 and
              J.T*J == sp.diag(2, *([1]*(m-1))))
        for locality in (False, True):
            pairs, es = edge_basis(m, locality)
            K = sp.Matrix.hstack(*[sp.Matrix(list(J*e)) for e in es])
            H = 2*K.T*K
            gradient = sp.Matrix([-2*inner(D, J*e) for e in es])
            check(f'VARIATION_RANK_{m}_{locality}',
                  K.rank() == len(es) and H.rank() == len(es) and
                  all(e == e.T and e*sp.ones(m, 1) == sp.zeros(m, 1) for e in es))
            if locality:
                check(f'CANONICAL_LOCAL_GATE_FAIL_{m}',
                      gradient == sp.Matrix([6]+[0]*(m-2)+[6]))
            rows.append({'coarse_size': m, 'local': locality,
                         'variation_dimension': len(es), 'variation_rank': K.rank(),
                         'hessian_rank': H.rank(), 'canonical_gradient': enc(gradient)})

    stationary = []
    # m=3 is complete, hence this first case solves ALL old full variations.
    # m=4 solves the genuine nearest-neighbor variation owner only.
    for m, response_side in ((3, 'fine'), (4, 'coarse')):
        J, Lc, Lf = lift(m), cycle(m), cycle(m+1)
        pairs, es = edge_basis(m, True)
        D = Lf*J-J*Lc
        K = sp.Matrix.hstack(*[sp.Matrix(list(J*e)) for e in es])
        H = 2*K.T*K
        gradient = sp.Matrix([-2*inner(D, J*e) for e in es])
        shift = -H.inv()*gradient
        weights = sp.ones(m, 1)+shift
        Lstar = sum((weights[i]*es[i] for i in range(m)), sp.zeros(m))
        Ds = Lf*J-J*Lstar
        native_gradient = sp.Matrix([-2*inner(Ds, J*e) for e in es])
        check(f'POSITIVE_LOCAL_STATIONARY_MINIMUM_{m}',
              native_gradient == sp.zeros(m, 1) and all(w > 0 for w in weights))
        if response_side == 'fine':
            R = Ds*Ds.T
            Z = sp.diag(1, -1, 0, 0)
            signed_gradient = sp.Matrix([-2*inner(Z*Ds, J*e) for e in es])
            expected = sp.Matrix([sp.Rational(4, 5), 0, sp.Rational(8, 5)])
            check('FULL_OLD_VARIATION_COVERED_AT_M3', len(es) == m*(m-1)//2)
        else:
            R = Ds.T*Ds
            Z = sp.diag(1, -1, 0, 0)
            signed_gradient = sp.Matrix([-2*inner(Ds*Z, J*e) for e in es])
            expected = sp.Matrix([sp.Rational(4,13), sp.Rational(6,13), 0, sp.Rational(2,13)])
        # R is positive by an exact Gram factorization; the two coordinate
        # effects are genuine disjoint positive Born effects.
        signed_value = sp.trace(Z*R)
        native_value = inner(Ds, Ds)
        born_gradient = signed_gradient/native_value
        check(f'GENUINE_BORN_CONTRAST_DOES_NOT_INHERIT_GATE_{m}',
              sp.trace(R) == native_value and native_value > 0 and
              signed_gradient == expected and any(x != 0 for x in born_gradient))
        eps = sp.symbols('eps', real=True)
        v = -J*es[0]
        secant = sp.expand((inner(Ds+eps*v, Ds+eps*v)-inner(Ds-eps*v, Ds-eps*v))/(2*eps))
        check(f'ACTUAL_NATIVE_CENTERED_SECANT_AT_STATIONARITY_{m}', secant == 0)
        check(f'NONZERO_ENDPOINTS_ARE_NOT_STATIONARY_{m}', (H*sp.Matrix([1]+[0]*(m-1)))[0] > 0)
        stationary.append({'coarse_size': m, 'scope': 'affine extension: all old full variation equations' if m == 3 else 'affine extension: all genuine local variation equations',
                           'fine_L': enc(Lf), 'lift_J': enc(J), 'coarse_Lstar': enc(Lstar),
                           'positive_conductances': enc(weights), 'seam_Dstar': enc(Ds),
                           'native_action': enc(native_value), 'native_gradient': enc(native_gradient),
                           'positive_response_side': response_side, 'signed_output': enc(signed_value),
                           'signed_gradient': enc(signed_gradient), 'normalized_Born_gradient': enc(born_gradient)})

    owner = repo / INPUTS[5]
    namespace = {'__name__': '_a4d_literal_definitions'}
    source = owner.read_text()
    exec(compile(source.split('check("LORENTZ_GENERATORS"')[0], str(owner), 'exec'), namespace)
    gens, eta = namespace['GENERATORS'], namespace['ETA']
    H0 = namespace['connection_symbol'](sp.eye(4), [sp.Integer(1)]*4)
    check('FULL_PALATINI_ZERO_PHASE_INERTIA_12_12',
          H0.rank() == 24 and H0.eigenvals() == {sp.Integer(-2):4, sp.Integer(-1):8,
                                               sp.Integer(1):8, sp.Integer(2):4})
    pos, neg = sp.zeros(24, 1), sp.zeros(24, 1)
    pos[1], pos[9], neg[1], neg[9] = 1, -1, 1, 1
    check('PALATINI_BOTH_SIGN_TANGENTS', (pos.T*H0*pos)[0] == 2 and (neg.T*H0*neg)[0] == -2)
    sys.path.insert(0, str(repo/'02_REGISTRY/research/certificates'))
    import numpy as np
    import a4d_identity_quarter_nonlinear_response_check as N
    identity_links = np.array([[N.jconst(N.I, 0) for _ in range(4)] for _ in range(4)])
    ek, eq = N.euler_links(identity_links)
    check('FLAT_BASE_IS_FULL_PHYSICAL_STATIONARY', not np.any(ek) and not np.any(eq))

    t = sp.symbols('t', real=True)
    def cayley(X):
        return (sp.eye(4)-t*X/2).inv()*(sp.eye(4)+t*X/2)
    wedge = namespace['wedge']
    W = wedge(sp.eye(4)[:, 2], sp.eye(4)[:, 3]).T*namespace['G2']*namespace['STAR']
    exact_paths = []
    for sign in (1, -1):
        U, V = cayley(gens[1]), cayley(sign*gens[3])
        P = U*V*U.inv()*V.inv()
        C = (P-P.inv())/2
        bv = sp.Matrix([(C*eta)[a,b] for a,b in namespace['PAIRS']])
        density = sp.factor((W*bv)[0])
        expected = -sign*16*t**2*(t**4+16)/((t-2)**2*(t+2)**2*(t**2+4)**2)
        check(f'EXACT_LITERAL_PALATINI_SIGNED_PATH_{sign}',
              sp.factor(density-expected) == 0 and
              sp.simplify(U.T*eta*U-eta) == sp.zeros(4) and
              sp.simplify(V.T*eta*V-eta) == sp.zeros(4) and
              sp.limit(density/t**2, t, 0) == -sign)
        exact_paths.append({'role0': 'Cayley(t G02)', 'role1': f'Cayley({sign} t G12)',
                            'density': str(density), 'value_at_t_one_tenth': str(density.subs(t, sp.Rational(1,10)))})

    # Do not overclaim a no-go for independent doubling: both gradients
    # vanish separately for either sign of an independently varied action.
    x, y = sp.symbols('x y', real=True)
    sum_action, difference_action = x*x+y*y, x*x-y*y
    check('INDEPENDENT_DOUBLING_GATE_EXCEPTION_RETAINED',
          sp.solve([sp.diff(sum_action,x), sp.diff(sum_action,y)], (x,y)) ==
          sp.solve([sp.diff(difference_action,x), sp.diff(difference_action,y)], (x,y)) == {x:0,y:0})

    payload = {'status': 'PASS',
               'input_sha256': {p: hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in INPUTS},
               'checks': checks, 'variation_controls': rows, 'stationary_Born_counterexamples': stationary,
               'Palatini_H0_inertia': {'positive':12,'negative':12,'zero':0},
               'literal_Palatini_paths': exact_paths,
               'scope': 'Fixed fine Laplacian and lift, actual coarse Laplacian variations. Independent doubled-sector signed readout is not globally excluded.'}
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True)+'\n')
    expected_path = args.expect or (Path(__file__).with_name('a4d_native_seam_action_gate_results.json') if not args.output else None)
    if expected_path is not None:
        if not expected_path.is_file():
            parser.error('missing pinned ledger; use --output only for explicit regeneration')
        assert json.loads(expected_path.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
        print('PASS_IMMUTABLE_PINNED_LEDGER', flush=True)
    print('PASS_ACTUAL_SEAM_ACTION_GATE_BOUNDARY', flush=True)

if __name__ == '__main__':
    main()
