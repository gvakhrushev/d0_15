#!/usr/bin/env python3
"""Exact controls for intrinsic restriction and fixed-golden two-step stationarity.
No native metric operator map or analytic Jacobi theorem is supplied by this checker.
"""
import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_constrained_price_source'
HEAD = '0545eaf95ac3857b30c43f266311c80c1d751d01'
PROOF = '02_REGISTRY/research/A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md'
SCOPE = {
    'intrinsic_joint_source_normal_form': 'GENERIC_LEAN_IDENTITY_AND_ANALYTIC_COMPLETE_TANGENT_CHART',
    'golden_full_archive_two_tick_jacobi_contraction': 'GENERIC_LEAN_ZERO_AT_SYMMETRIC_INVOLUTIONS',
    'actual_recorded_fullStep_block_binding': 'COMPILED_LEAN',
    'analytic_logdet_derivative': 'ANALYTIC_FINITE_DIMENSIONAL_JACOBI_PROOF_IN_MEMO',
    'generic_logdet_HasDerivAt_compiled': False,
    'fixed_golden_compression_class_exhaustive_for_all_core_variations': False,
    'zero_feedback_first_jet_means_zero_feedback_operator_jet': False,
    'zero_feedback_first_jet_means_zero_whole_bootstrap_source': False,
    'all_archive_delays_metric_response_zero': False,
    'native_Gamma_or_its_first_jet_constructed': False,
    'own_heat_metric_link_matter_source_or_Ward_constructed': False,
    'metric_lift_independence_without_link_equations': False,
    'source_equals_rho0': False,
    'G0_or_T0_T1_T2_T3_fully_closed': False,
    'curved_roots_soundness_recovery_positive_GR_or_global_closure': False,
    'new_action_selector_temperature_or_postulate': False,
    'parent_terminals_changed': False,
}


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def controls():
    checks = {}

    def check(name, condition):
        assert bool(condition), name
        checks[name] = checks.get(name, 0)+1

    receipt = json.loads((ROOT/(BASE+'_results.json')).read_text())
    output = (ROOT/receipt['output']).read_text()
    names = re.findall(r'^theorem ([A-Za-z0-9_]+)', (ROOT/(BASE+'.lean')).read_text(), re.M)
    check('kernel_exit_and_declared_input', receipt['status'] == 'PASS'
          and receipt['compiler_exit_code'] == 0 and receipt['input_head'] == HEAD)
    check('actual_propositions_and_axioms', names == receipt['declarations']
          and len(names) == receipt['printed_propositions'] == receipt['printed_axiom_dependencies'] == 33)
    for name in names:
        qualified = 'D0.Research.NativeConstrainedPriceSource.'+name
        check('resolved_proposition_and_transitive_axioms', re.search(r'^'+re.escape(qualified)+r'(?:\.\{|[ :])', output, re.M)
              and ("'"+qualified+"' depends on axioms:" in output
                   or "'"+qualified+"' does not depend on any axioms" in output))
    check('no_nonstandard_axioms_or_compiler_diagnostics',
          set(receipt['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
          and not any(word in output for word in ['error:', 'warning:', 'sorryAx']))
    for path, digest in {**receipt['transitive_d0_source_sha256'],
                         **receipt['toolchain_input_sha256'],
                         **receipt['prior_packet_input_sha256'],
                         receipt['capsule']: receipt['capsule_sha256'],
                         receipt['output']: receipt['output_sha256']}.items():
        check('all_pinned_inputs', sha(path) == digest)

    a, p = s.symbols('a p')
    ideal = s.groebner([a*a-p, p*p+p-1], a, p)
    z = s.Rational(1, 7)

    def zero(expr):
        if isinstance(expr, s.MatrixBase):
            return all(zero(v) for v in expr)
        num, den = s.cancel(expr).as_numer_denom()
        assert ideal.reduce(den)[1] != 0, 'ZERO_QUOTIENT_DENOMINATOR'
        return ideal.reduce(num)[1] == 0

    def unit(n, i, j):
        A = s.zeros(n); A[i, j] = 1
        return A

    def skews(n):
        return [unit(n, i, j)-unit(n, j, i) for i, j in itertools.combinations(range(n), 2)]

    def block(A, B, C, D):
        return A.row_join(B).col_join(C.row_join(D))

    cases = [(2, 2, s.eye(2)), (2, 4, s.Matrix([[0, 1], [1, 0]])),
             (4, 5, s.diag(1, -1, 1, -1))]
    rows = []
    for n, m, H in cases:
        R = s.eye(m)[:, :n]; S = R*H
        V = s.diag(*([0]*n+[1]*(m-n)))
        U = block(a*s.eye(n), -p*R.T, p*S, a*S*R.T+V)
        A2 = (U*U)[:n, :n]
        F2 = (U*U)[n:, :n].T*(U*U)[n:, :n]
        c = 2*z*p**3
        Res = ((1-c)*s.eye(n)+c*H)/(1-2*c)
        check('full_archive_owned_orthogonal_operator', zero(U.T*U-s.eye(n+m)))
        check('full_two_step_active_block', zero(A2-(a*a*s.eye(n)-p*p*H)))
        check('all_archive_feedback_rows_retained', zero(F2-(s.eye(n)-A2.T*A2)))
        check('golden_involution_feedback', zero(F2-2*p**3*(s.eye(n)+H)))
        check('genuine_resolvent_domain', zero((s.eye(n)-z*F2)*Res-s.eye(n)))
        count = 0
        for side in ['R', 'S']:
            for X in skews(m):
                XR = X if side == 'R' else s.zeros(m)
                XS = X if side == 'S' else s.zeros(m)
                dR, dS = XR*R, XS*S
                dV = XS*V-V*XR
                dU = block(s.zeros(n), -p*dR.T, p*dS,
                           a*(dS*R.T+S*dR.T)+dV)
                dA2 = (dU*U+U*dU)[:n, :n]
                B2 = (U*U)[n:, :n]
                dB2 = (dU*U+U*dU)[n:, :n]
                dF2 = dB2.T*B2+B2.T*dB2
                dH = dR.T*S+R.T*dS
                check('complete_isometry_tangent_equations', zero(dR.T*R+R.T*dR)
                      and zero(dS.T*S+S.T*dS))
                check('actual_full_U_jet_orthogonal', zero(dU.T*U+U.T*dU))
                check('relative_first_jet_orthogonal', zero(dH.T*H+H.T*dH))
                check('actual_retained_jet', zero(dA2+p*p*dH))
                check('actual_full_feedback_jet', zero(dF2-p**3*(dH+dH.T)))
                check('full_archive_jacobi_source_zero', zero(z*s.trace(Res*dF2)))
                count += 1
        rows.append({'active': n, 'archive': m, 'independent_frame_generator_tests': count})

    H = s.Matrix([[0, 1], [1, 0]])
    dH = H*skews(2)[0]
    check('operator_jet_can_be_nonzero_while_price_jet_zero', dH+dH.T != s.zeros(2))
    ambient = s.eye(2)
    check('ambient_non_tangent_is_detected', ambient.T+ambient != s.zeros(2)
          and not zero(z*s.trace((s.eye(2)/(1-4*z*p**3))*p**3*(ambient+ambient.T))))
    t = s.symbols('t', real=True)
    cayley = s.Matrix([[1-t*t, -2*t], [2*t, 1-t*t]])/(1+t*t)
    A = p*s.eye(2)-p*p*cayley
    F = s.eye(2)-A.T*A
    check('noninvolutive_exception_is_admitted_orthogonal_curve', cayley.T*cayley == s.eye(2)
          or s.simplify(cayley.T*cayley-s.eye(2)) == s.zeros(2))
    cjet = F.diff(t).subs(t, 1)
    jvalue = z*s.trace(cjet)/(1-2*z*p**3)
    check('noninvolutive_exception_preserved', zero(jvalue+4*z*p**3/(1-2*z*p**3)) and not zero(jvalue))
    check('nonconstant_parameter_gap_sensitivity_retained', s.diff(-s.log(1-4*z*p**3), p) != 0)

    # Independent exact joint carrier; no feedback-to-metric map is assigned.
    n = 4; eta = s.diag(1, -1, -1, -1)
    factors = [s.eye(n)+s.Rational(k+1, 7)*unit(n, 0, 1)
               +s.Rational(k+2, 9)*unit(n, 2, 3) for k in range(5)]
    q = [f*eta*f.T for f in factors]
    rot = s.eye(n); rot[1, 1] = rot[2, 2] = s.Rational(3, 5)
    rot[1, 2] = -s.Rational(4, 5); rot[2, 1] = s.Rational(4, 5)
    boost = s.eye(n); boost[0, 0] = boost[1, 1] = s.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = s.Rational(4, 3)
    D = [factors[0]*L*factors[e+1].inv() for e, L in enumerate([s.eye(n), rot, boost, boost*rot])]
    A = [s.Matrix(n, n, lambda i, j: (k+1)*(i+1)+j*j) for k in range(5)]
    B = [s.Matrix(n, n, lambda i, j: (k+2)*(i+1)**2-j) for k in range(4)]
    R = [q[0].inv()*d for d in D]
    M = [b*r.T for b, r in zip(B, R)]
    sym = [unit(n, i, j) if i == j else unit(n, i, j)+unit(n, j, i)
           for i in range(n) for j in range(i, n)]
    fp = lambda x, y: s.trace(x.T*y)
    Lambdas = [s.Matrix(n, n, lambda i, j: (e+1)*(i+j+1)) for e in range(4)]
    Ac = [a.copy() for a in A]; Bc = [b.copy() for b in B]
    for e in range(4):
        Ac[0] -= Lambdas[e]; Ac[e+1] += D[e].T*Lambdas[e]*D[e]
        Bc[e] += 2*Lambdas[e]*D[e]*q[e+1]
    Mc = [b*r.T for b, r in zip(Bc, R)]
    As = A[0]+sum(M, s.zeros(n))/2
    Asc = Ac[0]+sum(Mc, s.zeros(n))/2
    check('conormal_center_cotangent_unchanged', Asc == As)
    for e in range(4):
        check('conormal_target_cotangent_unchanged', Ac[e+1]-D[e].T*Mc[e]*D[e]/2 == A[e+1]-D[e].T*M[e]*D[e]/2)
        check('conormal_link_skew_cotangent_unchanged', Mc[e]-Mc[e].T == M[e]-M[e].T)
    probes = []
    for site in range(5):
        for v in sym:
            Vs = [s.zeros(n) for _ in range(5)]; Vs[site] = v
            probes.append((Vs, [s.zeros(n) for _ in range(4)]))
    for e in range(4):
        for k in skews(n):
            Ks = [s.zeros(n) for _ in range(4)]; Ks[e] = k
            probes.append(([s.zeros(n) for _ in range(5)], Ks))
    for Vs, Ks in probes:
        W = [((Vs[0]-d*Vs[e+1]*d.T)/2+Ks[e])*R[e] for e, d in enumerate(D)]
        check('full_joint_tangent_all_50_plus_24', all(d*Vs[e+1]*d.T+w*q[e+1]*d.T+d*q[e+1]*w.T == Vs[0]
              for e, (d, w) in enumerate(zip(D, W))))
        lhs = sum(fp(a, v) for a, v in zip(A, Vs))+sum(fp(b, w) for b, w in zip(B, W))
        rhs = fp(As, Vs[0])+sum(fp(A[e+1]-D[e].T*M[e]*D[e]/2, Vs[e+1])+fp(M[e], Ks[e]) for e in range(4))
        check('intrinsic_source_normal_form_all_74', lhs == rhs)
        conormal = sum(fp(ac-a, v) for a, ac, v in zip(A, Ac, Vs))+sum(fp(bc-b, w) for b, bc, w in zip(B, Bc, W))
        check('full_conormal_restriction_all_74', conormal == 0)
    check('off_shell_link_lift_ambiguity_retained', any(fp(m, k) != 0 for m in M for k in skews(n)))
    for v in sym:
        symA = (As+As.T)/2
        check('all_ten_packed_metric_weights', fp(As, v) == sum((1 if i == j else 2)*symA[i, j]*v[i, j]
              for i in range(n) for j in range(i, n)))
    return {'checks': checks, 'check_count': sum(checks.values()), 'golden_archive_fixtures': rows,
            'joint_metric_probes': 50, 'joint_connection_probes': 24,
            'compiled_propositions': len(names),
            'transitive_d0_source_pins': len(receipt['transitive_d0_source_sha256'])}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    result = {'schema': 'd0-constrained-price-source/1', 'input_head': HEAD, 'scope': SCOPE,
              'proof_sha256': sha(PROOF), 'checker_sha256': sha(BASE+'_check.py'),
              'lean_receipt_sha256': sha(BASE+'_results.json'), **controls()}
    if args.output:
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    else:
        expected = json.loads((args.expect or ROOT/(BASE+'_certificate.json')).read_text())
        assert expected.get('scope') == SCOPE, 'SOURCE_SCOPE_MISMATCH'
        assert result == expected, 'EXACT_CERTIFICATE_MISMATCH'
    print('PASS_NATIVE_CONSTRAINED_PRICE_SOURCE', result['check_count'], 'controls')


if __name__ == '__main__':
    main()
