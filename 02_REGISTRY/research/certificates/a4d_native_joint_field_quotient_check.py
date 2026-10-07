#!/usr/bin/env python3
"""Exact complete-star joint quotient and source-variation controls."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

HEAD = '00aa52091ae004fac6c1dc11964be3fa191b75b8'
BASE = '02_REGISTRY/research/certificates/a4d_native_joint_field_quotient'
PROOF = '02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md'
I = s.eye(4)
ETA = s.diag(1, -1, -1, -1)
BLADES = [p for k in range(5) for p in itertools.combinations(range(4), k)]
PAIRS = list(itertools.combinations_with_replacement(range(4), 2))


def exterior(F):
    return s.Matrix(16, 16, lambda i, j: 0 if len(BLADES[i]) != len(BLADES[j])
                    else F.extract(BLADES[i], BLADES[j]).det())


def exterior_jet(H):
    result = s.zeros(16)
    for j, blade in enumerate(BLADES):
        for p, old in enumerate(blade):
            for new in range(4):
                word = list(blade)
                word[p] = new
                if len(set(word)) != len(word):
                    continue
                sign = (-1)**sum(a > b for k, a in enumerate(word) for b in word[k+1:])
                result[BLADES.index(tuple(sorted(word))), j] += sign*H[new, old]
    return result


def flat(M):
    return list(M)


def packed(M):
    return [M[i, j] for i, j in PAIRS]


def emat(i, j):
    M = s.zeros(4)
    M[i, j] = 1
    return M


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path)
    p.add_argument('--expect', type=Path)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    checks = []

    def check(name, value):
        assert bool(value), name
        checks.append(name)

    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    check('COMPILED_15_DECLARATIONS', receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0
          and receipt['owner_input_head'] == HEAD and receipt['printed_axiom_dependencies'] == 15 and not receipt['sorryAx'])
    pins = {**receipt['transitive_d0_source_sha256'], **receipt['toolchain_input_sha256'],
            receipt['capsule']: receipt['capsule_sha256'], receipt['output']: receipt['output_sha256']}
    check('ALL_NATIVE_AND_TOOLCHAIN_PINS', all(sha(p) == h for p, h in pins.items()))
    out = (root/receipt['output']).read_text()
    check('STANDARD_AXIOMS_CLEAN_COMPILER_OUTPUT', set(receipt['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
          and all(x not in out for x in ['error:', 'warning:', 'sorryAx']))
    for name in ['same_gram_relative_frame', 'exterior_matter_complete', 'transported_center_factorization',
                 'transported_gram_factorization', 'ambient_source_derivative', 'constrained_source_derivative_zero']:
        check('BOUND_'+name, "'D0.Research.NativeJointFieldQuotient."+name+"' depends on axioms:" in out)

    B = s.Matrix([[s.Rational(5, 4), s.Rational(3, 4), 0, 0], [s.Rational(3, 4), s.Rational(5, 4), 0, 0],
                  [0, 0, 1, 0], [0, 0, 0, 1]])
    R = s.Matrix([[1, 0, 0, 0], [0, s.Rational(3, 5), s.Rational(-4, 5), 0],
                  [0, s.Rational(4, 5), s.Rational(3, 5), 0], [0, 0, 0, 1]])
    # Four incoming links have sources 1..4 and common target 0.
    F = [s.diag(1+s.Rational(i, 7), 1+s.Rational(i, 9), 1, 1)*(I+s.Rational(i, 5)*emat(0, 2)) for i in range(5)]
    U = [B, R, B*R, R*B]
    a = [s.Matrix([i+1, 2-i, 3, -1]) for i in range(4)]
    psi = [s.Matrix([s.Rational((i+1)*(j+1), 3) for j in range(16)]) for i in range(5)]
    Fi = [f.inv() for f in F]
    rho = [exterior(f) for f in F]
    q = [f*ETA*f.T for f in F]
    D = [F[e+1]*U[e]*Fi[0] for e in range(4)]
    b = [F[e+1]*a[e] for e in range(4)]
    m = [rho[i]*psi[i] for i in range(5)]
    check('INHABITED_NONDEGENERATE_FULL_JOINT_CARRIER', all(f.det() != 0 for f in F)
          and all(u*ETA*u.T == ETA and u.det() == 1 and u[0, 0] > 0 for u in U)
          and all(v != 0 for ps in psi for v in ps) and all(av != s.zeros(4, 1) for av in a))
    check('ALL_FOUR_METRIC_ISOMETRY_CONSTRAINTS', all(D[e]*q[0]*D[e].T == q[e+1] for e in range(4)))
    check('ALL_LINK_SHIFT_MATTER_RECONSTRUCTIONS',
          all(Fi[e+1]*D[e]*F[0] == U[e] and Fi[e+1]*b[e] == a[e] for e in range(4))
          and all(rho[i].inv()*m[i] == psi[i] for i in range(5)))
    check('EXTERIOR_ALL_GRADES_AND_FUNCTOR', [sum(len(p) == k for p in BLADES) for k in range(5)] == [1, 4, 6, 4, 1]
          and exterior(F[2]*B) == rho[2]*exterior(B)
          and exterior(B)*exterior(B.inv()) == s.eye(16))
    t = s.Symbol('t')
    HH = s.Matrix(4, 4, lambda i, j: i+2*j-2)
    check('FULL_EXTERIOR_FIRST_JET_FROM_MINORS', exterior(I+t*HH).diff(t).subs(t, 0) == exterior_jet(HH))

    Lam = [B, R, B*R, R*B, B*B*R]
    Fp = [F[i]*Lam[i] for i in range(5)]
    Up = [Lam[e+1].inv()*U[e]*Lam[0] for e in range(4)]
    ap = [Lam[e+1].inv()*a[e] for e in range(4)]
    psip = [exterior(Lam[i].inv())*psi[i] for i in range(5)]
    check('FINITE_SITEWISE_JOINT_GAUGE_INVARIANTS',
          all(Fp[i]*ETA*Fp[i].T == q[i] and exterior(Fp[i])*psip[i] == m[i] for i in range(5))
          and all(Fp[e+1]*Up[e]*Fp[0].inv() == D[e] and Fp[e+1]*ap[e] == b[e] for e in range(4)))
    check('UNIQUE_GAUGE_RECONSTRUCTED_FROM_RAW_SOLDERS', all(Fi[i]*Fp[i] == Lam[i] for i in range(5)))
    check('AFFINE_SHIFT_DATA_NOT_DISCARDED', F[1]*(a[0]+s.Matrix([1, 0, 0, 0])) != b[0])
    check('ALL_MATTER_DATA_NOT_DISCARDED', rho[0].rank() == 16)

    gens = []
    ij = list(itertools.combinations(range(4), 2))
    for i, j in ij:
        G = emat(i, j)-ETA[i, i]/ETA[j, j]*emat(j, i)
        gens.append(G)
    check('ALL_SIX_LORENTZ_GENERATORS', all(G*ETA+ETA*G.T == s.zeros(4) for G in gens))

    def inputs_zero():
        return [s.zeros(4) for _ in range(5)], [s.zeros(4) for _ in range(4)], [s.zeros(4, 1) for _ in range(4)], [s.zeros(16, 1) for _ in range(5)]

    def variation(df, du, da, dp):
        dq = [df[i]*ETA*F[i].T+F[i]*ETA*df[i].T for i in range(5)]
        dd = [df[e+1]*U[e]*Fi[0]+F[e+1]*du[e]*Fi[0]-D[e]*df[0]*Fi[0] for e in range(4)]
        db = [df[e+1]*a[e]+F[e+1]*da[e] for e in range(4)]
        dm = [rho[i]*(exterior_jet(Fi[i]*df[i])*psi[i]+dp[i]) for i in range(5)]
        return s.Matrix([z for v in dq for z in packed(v)]+[z for v in dd for z in flat(v)]
                        +[z for v in db for z in flat(v)]+[z for v in dm for z in flat(v)])

    labels = [('F', i, j, k) for i in range(5) for j in range(4) for k in range(4)]
    labels += [('U', e, g, 0) for e in range(4) for g in range(6)]
    labels += [('a', e, i, 0) for e in range(4) for i in range(4)]
    labels += [('psi', i, j, 0) for i in range(5) for j in range(16)]
    columns = []
    for typ, n, j, k in labels:
        df, du, da, dp = inputs_zero()
        if typ == 'F': df[n][j, k] = 1
        if typ == 'U': du[n] = gens[j]*U[n]
        if typ == 'a': da[n][j] = 1
        if typ == 'psi': dp[n][j] = 1
        columns.append(variation(df, du, da, dp))
    Jac = s.Matrix.hstack(*columns)
    check('FULL_JACOBIAN_210_BY_200_ALL24_LINK_ROWS', Jac.shape == (210, 200)
          and sum(z[0] == 'U' for z in labels) == 24 and sum(z[0] == 'psi' for z in labels) == 80)

    gauge_columns = []
    for vertex in range(5):
        for H in gens:
            hs = [s.zeros(4) for _ in range(5)]
            hs[vertex] = H
            df = [F[i]*hs[i] for i in range(5)]
            du = [-hs[e+1]*U[e]+U[e]*hs[0] for e in range(4)]
            da = [-hs[e+1]*a[e] for e in range(4)]
            dp = [-exterior_jet(hs[i])*psi[i] for i in range(5)]
            coords = [z for v in df for z in flat(v)]
            for e in range(4):
                X = du[e]*U[e].inv()
                coefficients = [X[i, j] for i, j in ij]
                assert sum((c*G for c, G in zip(coefficients, gens)), s.zeros(4)) == X
                coords.extend(coefficients)
            coords += [z for v in da for z in flat(v)]+[z for v in dp for z in flat(v)]
            gauge_columns.append(s.Matrix(coords))
    Gauge = s.Matrix.hstack(*gauge_columns)
    check('GAUGE_IS_FULL_JACOBIAN_KERNEL_INCLUSION', Jac*Gauge == s.zeros(210, 30))
    rank_j, rank_g = Jac.to_DM().rank(), Gauge.to_DM().rank()
    check('EXACT_JOINT_RANK_170_KERNEL_30', rank_j == 170 and rank_g == 30 and 200-rank_j == rank_g)

    constraint_cols = []
    for k in range(210):
        dq = [s.zeros(4) for _ in range(5)]
        dd = [s.zeros(4) for _ in range(4)]
        if k < 50:
            vertex, packed_i = divmod(k, 10)
            i, j = PAIRS[packed_i]
            dq[vertex][i, j] = dq[vertex][j, i] = 1
        elif k < 114:
            edge, pos = divmod(k-50, 16)
            i, j = divmod(pos, 4)
            dd[edge][i, j] = 1
        dc = [dd[e]*q[0]*D[e].T+D[e]*dq[0]*D[e].T+D[e]*q[0]*dd[e].T-dq[e+1] for e in range(4)]
        constraint_cols.append(s.Matrix([v for M in dc for v in packed(M)]))
    Constraint = s.Matrix.hstack(*constraint_cols)
    check('ACTUAL_CONSTRAINT_DIFFERENTIAL_ANNIHILATES_ALL_VARIATIONS', Constraint*Jac == s.zeros(40, 200))
    rank_c = Constraint.to_DM().rank()
    check('COMPLETE_CONSTRAINED_IMAGE_IN_CONTROL', rank_c == 40 and 210-rank_c == rank_j)

    ambient = s.Matrix([i+1 for i in range(210)])
    euler = Jac.T*ambient
    v = Gauge[:, 6]  # source site 1, first boost
    ward_terms = [(euler[a:b, :].T*v[a:b, :])[0] for a, b in [(0, 80), (80, 104), (104, 120), (120, 200)]]
    check('JOINT_WARD_ALL_FOUR_SECTORS_REQUIRED', all(w != 0 for w in ward_terms) and sum(ward_terms) == 0)
    check('DROPPING_A_SOURCE_LINK_OR_MATTER_TERM_FAILS', all(sum(ward_terms)-w != 0 for w in ward_terms))
    extension = Constraint.row(0)
    check('CONSTRAINT_EXTENSION_NATIVE_ACTION_DERIVATIVE_ZERO', extension*Jac == s.zeros(1, 200))
    check('AMBIENT_METRIC_SOURCE_CAN_BE_FALSE', extension[:, :50] != s.zeros(1, 50)
          and extension[:, :50]*Jac[:50, :] != s.zeros(1, 200))
    V = s.Matrix(4, 4, lambda i, j: i+j+1)
    P = s.Matrix(4, 4, lambda i, j: i*j+1)
    weights = [1 if i == j else 2 for i, j in PAIRS]
    check('TEN_METRIC_COMPONENTS_PACKED_DUAL_WEIGHTS', s.trace(P.T*V) == sum(w*P[i, j]*V[i, j] for w, (i, j) in zip(weights, PAIRS)))

    BF = s.Matrix(4, 4, lambda r, c: (int(r == c)+D[r][r, c])/2)
    center = s.Matrix(4, 4, lambda r, c: (F[0][r, c]+(F[r+1]*U[r])[r, c])/2)
    check('EXACT_NATIVE_INCOMING_CENTER_FACTOR', center == BF*F[0])
    check('TRANSPORTED_GRAM_IN_COMPLETE_QUOTIENT', center*ETA*center.T == BF*q[0]*BF.T and BF.det() != 0)
    check('RAW_GRAM_RECOVERED_FROM_CENTERED_GRAM_AND_RAW_DRESSED_LINKS', BF.inv()*(center*ETA*center.T)*BF.inv().T == q[0])
    flip = s.diag(1, -1, -1, 1)
    badB = (I+flip)/2
    check('RAW_NONDEGENERACY_DOES_NOT_ENSURE_CENTER_NONDEGENERACY', flip*ETA*flip.T == ETA
          and flip.det() == 1 and I.det() != 0 and badB.det() == 0)

    nyquist = []
    tau = s.Rational(1, 3)
    for L in [2, 4, 8]:
        for x in range(L):
            sign = (-1)**x
            fx = s.diag(1+tau*sign, -1, -1, -1)
            fy = s.diag(1-tau*sign, -1, -1, -1)
            incoming = fy*fx.inv()
            outgoing = fx*fy.inv()
            Bx = s.diag(1/(1+tau*sign), 1, 1, 1)
            By = s.diag(1/(1-tau*sign), 1, 1, 1)
            nyquist.append((fx.det() != 0 and fx[0, 0] > 0 and Bx.det() != 0
                            and (incoming[0, 0]+1)/2 == Bx[0, 0] and Bx*fx == ETA
                            and Bx*outgoing*By.inv() == I and fx*ETA*fx.T != ETA))
    check('ALL_EVEN_CONTROL_NYQUIST_STATES_INHABITED_NONDEGENERATE', all(nyquist))
    check('CENTERED_DATA_DO_NOT_SEPARATE_NATIVE_LORENTZ_ORBITS', all(nyquist) and len(nyquist) == 14)
    improper = s.diag(1, -1, 1, 1)
    timeflip = s.diag(-1, -1, 1, 1)
    check('PROPER_COMPONENT_LABEL_CANNOT_BE_DROPPED', improper*ETA*improper.T == ETA and improper.det() == -1)
    check('TIME_CONE_LABEL_CANNOT_BE_DROPPED', timeflip*ETA*timeflip.T == ETA and timeflip.det() == 1 and timeflip[0, 0] < 0)

    D1, D2 = F[0]*B*Fi[1], F[1]*R*Fi[2]
    av, bv = a[:2]
    check('DRESSED_LINK_BLOCK_COMPOSITION_EXACT', D1*D2 == F[0]*(B*R)*Fi[2])
    check('DRESSED_AFFINE_SHIFT_BLOCK_COMPOSITION_EXACT', F[0]*(av+B*bv) == F[0]*av+D1*(F[1]*bv))
    check('METRIC_COMPATIBILITY_PRESERVED_BY_BLOCKING', (D1*D2)*q[2]*(D1*D2).T == q[0])
    check('FULL_EXTERIOR_MATTER_BLOCK_COMPOSITION', exterior(D1*D2) == exterior(D1)*exterior(D2))

    scope = {
        'joint_orbit_and_tangent_completeness': 'ANALYTIC_EXPLICIT_RECONSTRUCTION',
        'actual_exterior_and_center_bindings': 'COMPILED_LEAN',
        'source_extension_derivatives': 'COMPILED_LEAN_WITH_GENUINE_HAS_DERIV_AT',
        'finite_star_rank_certificate': 'EXACT_170_PLUS_30_AND_40_CONSTRAINTS',
        'full_orbit_assembly_compiled': False,
        'finite_rank_implies_all_meshes': False,
        'affine_translations_quotiented': False,
        'physical_diffeomorphisms_derived': False,
        'proper_orbits_ignore_component_labels': False,
        'centered_only_readout_is_complete': False,
        'raw_nondegeneracy_implies_center_nondegeneracy': False,
        'response_null_is_gauge': False,
        'metric_and_dressed_links_independent': False,
        'ambient_partial_is_native_source': False,
        'Lorentz_Ward_is_stress_divergence': False,
        'native_joint_action_selected': False,
        'all_native_admission_constraints_classified': False,
        'native_refinement_selected': False,
        'physical_matter_source_constructed': False,
        'G0_closed': False,
        'positive_GR': False,
        'whole_core_no_go': False,
        'original_parent_terminals_changed': False,
    }
    payload = {
        'status': 'PASS_NATIVE_JOINT_FIELD_QUOTIENT', 'input_head': HEAD,
        'inputs_sha256': {p: sha(p) for p in [PROOF,
            '02_REGISTRY/research/MEMO_A4D_STAR_DENSITY_LORENTZ_NONLINEAR_QUOTIENT.md',
            '02_REGISTRY/research/A4D_NATIVE_AFFINE_HISTORY_SCALAR_BOUNDARY.md']},
        'checker_sha256': sha(BASE+'_check.py'), 'lean_receipt_sha256': sha(BASE+'_results.json'),
        'compiled_declarations': 15, 'transitive_native_pins': len(receipt['transitive_d0_source_sha256']),
        'ranks': {'native_variables': 200, 'quotient_ambient_variables': 210,
                  'jacobian': rank_j, 'gauge': rank_g, 'constraint': rank_c},
        'ward_terms': [str(v) for v in ward_terms], 'checks': checks, 'scope': scope,
    }
    encoded = json.dumps(payload, sort_keys=True, indent=2)+'\n'
    if args.output: args.output.write_text(encoded)
    else:
        expect = args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expect.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_JOINT_FIELD_QUOTIENT', len(checks), 'controls', payload['transitive_native_pins'], 'D0 pins', flush=True)


if __name__ == '__main__':
    main()
