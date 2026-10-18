#!/usr/bin/env python3
"""Bounded consumers: measured adaptive histories, true clock and full source.

Loads only two pinned old definition owners, not their suites. Exact finite
identities and analytic-limit prerequisites remain separate. Default is read-only.
"""
import argparse
import ast
import hashlib
import json
import itertools
from pathlib import Path
import sympy as s


def quantile_and_price_case():
    checks = []

    def require(name, test):
        if not test:
            raise ArithmeticError(name)
        checks.append(name)

    x, y, eps = s.symbols('x y epsilon', real=True)
    rho = (1 + eps*x*y)/(1 + eps/4)
    R0 = (x + eps*x*x/4)/(1 + eps/4)
    R1 = (y + eps*x*y*y/2)/(1 + eps*x/2)
    jac = s.Matrix([R0, R1]).jacobian([x, y])
    require('nonseparable four-role triangular Jacobian',
            s.cancel(jac.det()-rho) == 0)
    velocity = s.Matrix([s.diff(R0,eps), s.diff(R1,eps)]).subs(eps,0)
    require('true moving-density first source',
            s.simplify(s.diff(velocity[0],x)+s.diff(velocity[1],y)
                       -s.diff(s.log(rho),eps).subs(eps,0)) == 0)
    require('conditional CDF keeps both endpoints',
            R0.subs(x,0) == 0 and s.cancel(R0.subs(x,1)-1) == 0
            and R1.subs(y,0) == 0 and s.cancel(R1.subs(y,1)-1) == 0)
    # Complete adaptive law and the actual full Book cocycle.
    r, u, v, ell = s.symbols('r u v ell', positive=True)
    q = [(1-r)*(1-u), (1-r)*u, r*(1-v), r*v]
    require('complete adaptive two-level law', s.expand(sum(q)-1) == 0)
    mu = s.symbols('mu0:4', positive=True)
    cost = [-s.log(m)/ell for m in mu]
    info = [s.log(a/m)/ell for a,m in zip(q,mu)]
    full = sum(a*(c-i) for a,c,i in zip(q,cost,info))
    entropy = -sum(a*s.log(a) for a in q)/ell
    require('whole-code Cost-Info cancellation before variation',
            s.expand_log(full-entropy,force=True).expand() == 0)
    h = lambda z: -z*s.log(z)-(1-z)*s.log(1-z)
    require('conditional entropy retains branch-weight derivative',
            s.expand_log(entropy-(h(r)+(1-r)*h(u)+r*h(v))/ell,
                         force=True).expand() == 0)
    extra = sum(qi*ai for qi,ai in zip(q,[0,0,1,1]))
    require('deterministic metadata alone does not cancel unpaid cost',
            s.simplify(s.diff(extra,r)-1) == 0)
    return dict(status='PASS', checks=checks,
        scope='Exact conditional quantile/source identities and full-code cocycle; '
              'no physical actuation, full-price binding or independent matter selection inferred.')


def two_tick_scene_source_case():
    checks = []

    def require(name, test):
        if not test:
            raise ArithmeticError(name)
        checks.append(name)

    raw = s.symbols('b', positive=True)
    G = s.Matrix([[s.sqrt(1-raw),-s.sqrt(raw)],
                  [s.sqrt(raw),s.sqrt(1-raw)]])
    B = s.expand((G*G)[1,0]**2)
    require('literal two-tick scene effect', s.expand(B-4*raw*(1-raw)) == 0)
    p = (s.sqrt(5)-1)/2
    z, t2, f, q, sigma = s.symbols('z t2 f q sigma', real=True)
    e = p*p*(1+t2*f)
    b = (p+sigma*p*p*t2*q)**2
    bb = 4*b*(1-b)
    lam = 4*e*(1-e)
    # Full ONE feedback includes BOTH scene-normalizer and AF-return terms.
    price = -s.log(1-z*bb)-s.log(1-z*(lam+(1-lam)*bb))
    L = 4*p**3
    Q = 1-z*L
    R = 1-z*(L+p**6*L)
    bg = {f:0,q:0}
    Cstar = s.simplify(s.diff(price,f).subs(bg))
    Cmat = s.simplify(s.diff(price,q).subs(bg))
    require('two-tick background is L not p squared', s.simplify(bb.subs(q,0)-L) == 0)
    require('actual two-tick material first jet',
            s.simplify(s.diff(bb,q).subs(q,0)-8*sigma*p**6*t2) == 0)
    require('full geometric coefficient',
            s.simplify(Cstar-4*z*p**11*t2/R) == 0)
    require('full material coefficient including normalizer',
            s.simplify(Cmat-8*sigma*z*p**6*t2*(1/Q+p**6/R)) == 0)
    ratio = 2*sigma/p**5*(R/Q+p**6)
    require('ratio of actual full sources', s.simplify(Cmat-Cstar*ratio) == 0)
    require('exact golden zero-fugacity ratio',
            s.simplify(ratio.subs(z,0)-sigma*(10+6*s.sqrt(5))) == 0)
    return dict(status='PASS',checks=checks,
        Lambda_plus_fixed_z=str(s.N(ratio.subs({z:s.Rational(1,2**20),sigma:1}),40)),
        scope='One repeated scene word and its full source; supports conditional '
              'local null-scalar construction, not compulsory native scene choice.')


def null_volume_proper_clock_case():
    eta = s.diag(1,-1,-1,-1)
    k = s.Matrix([1,1,0,0])
    ell = eta*k
    z = s.symbols('deformation', real=True)
    N = k*ell.T
    e = s.eye(4)+z*N/2
    metric = e.T*eta*e
    F = e.inv()
    q = F*eta*F.T
    b = F*s.eye(4)[:,0]
    alpha = s.simplify(q.inv()*b)
    checks = {
        'null rank-one endomorphism is nilpotent': N*N == s.zeros(4),
        'exact same-volume coframe path': s.expand(e.det()-1) == 0,
        'all-order Kerr-Schild metric identity':
            metric.applyfunc(s.expand) == eta+z*ell*ell.T,
        'proper clock remains unit': s.simplify((alpha.T*q*alpha)[0]-1) == 0,
        'proper clock actually moves despite fixed volume':
            s.diff(alpha,z) == ell/2,
    }
    for name, condition in checks.items():
        if not condition:
            raise ArithmeticError(name)
    return dict(status='PASS',checks=list(checks),
        scope='Volume/quantile placement source vanishes on this exact null path; '
              'the actual CAR clock one-form still varies. Its full-price '
              'source requires the real observer/clock/controller equations.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    for rel, expected in PINS.items():
        actual = hashlib.sha256((root/rel).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError('changed pinned definition owner: '+rel)
    result = dict(status='PASS', source_pins=PINS,
        adaptive=adaptive_record_history_case(root),
        clock=clock_consumer(),
        complete_price_and_quantile=quantile_and_price_case(),
        retained_factory=retained_clock_factory(root),
        actual_two_tick_scene=two_tick_scene_source_case(),
        null_volume_and_clock=null_volume_proper_clock_case(),
        GR_closed=False, native_clock_forced=False, exact_compiled_roots=False)
    # The family of repetitions changes free-leaf preparation equations.
    result['retained_factory']['preparation_boundary'] = (
        'Use the actual fixed-RIGHT/PF fibre or solve all repeated preparation rows. '
        'For free old weights, H(r)+M sum r_i g_i has stationary r_i proportional '
        'to exp(M g_i), so the old single-shot capacity profile is not preserved.')
    text = json.dumps(result, indent=2, ensure_ascii=False)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


PINS = {'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': '42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078', '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': '16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527'}

def adaptive_record_history_case(root):
    root = Path(root)
    (a, p, r) = s.symbols('a p r', real=True)
    gb = s.groebner([a * a - p, p * p + p - 1], a, p, domain=s.QQ.frac_field(r))

    def red(v):
        (n, d) = s.cancel(v).as_numer_denom()
        return s.cancel(gb.reduce(s.expand(n))[1] / gb.reduce(s.expand(d))[1])

    def mat(M):
        return M.applyfunc(red)
    I = s.eye(16)
    I4 = s.eye(4)
    subs = [tuple((i for i in range(4) if mask & 1 << i)) for mask in range(16)]
    ns = dict(s=s, a=a, p=p, I=I, DEG=s.diag(*map(len, subs)), SUBS=subs, mat=mat)
    pins = {}
    for (rel, names) in {'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': ['creator', 'ext', 'record_basis'], '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': ['record']}.items():
        tree = ast.parse((root / rel).read_text())
        pins[rel] = {}
        for name in names:
            node = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name))
            pins[rel][name] = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
            exec(compile(ast.Module(body=[node], type_ignores=[]), rel, 'exec'), ns)
    checks = []

    def check(name, test):
        if not test:
            raise ArithmeticError(name)
        checks.append(name)
    m = s.zeros(16, 1)
    m[1] = m[15] = 1
    m[3] = m[13] = r
    norm = 2 * (1 + r * r)
    (U0, P0) = ns['record'](I4, I4[:, 0])
    (Um, Pm) = ns['record'](I4, -I4[:, 1])
    first = [mat(P0 * U0 * m), mat((I - P0) * U0 * m)]
    grades = [s.Matrix([v[1 << i] for i in range(4)]) for v in first]
    check('branch0_actual_first_grade', mat(grades[0] - s.Matrix([0, -p * r, 0, 0])) == s.zeros(4, 1))
    check('branch1_actual_first_grade', mat(grades[1] - s.Matrix([a, 0, 0, 0])) == s.zeros(4, 1))
    check('complete_first_probabilities', red((first[0].T * first[0])[0] / norm - p * p) == 0 and red((first[1].T * first[1])[0] / norm - p) == 0)
    check('positive_mass_singular_branch_at_r0', grades[0].subs(r, 0) == s.zeros(4, 1) and red((first[0].T * first[0])[0].subs(r, 0) / 2 - p * p) == 0)
    Bbasis = ns['record_basis']()
    T = s.Matrix([[1, 0, 1, 0], [1, 0, -1, 0], [0, 1, 0, 1], [0, 1, 0, -1]]) / s.sqrt(2)
    blank = Bbasis * s.kronecker_product(T.T * s.diag(1, 0, 1, 0) * T, I4) * Bbasis.T
    check('actual_whole_blank_input', mat(blank * m - m) == s.zeros(16, 1))
    original_record0 = Bbasis * s.kronecker_product(T.T * s.diag(1, 0, 1, 0) * T, I4) * Bbasis.T
    check('first_readout_is_actual_record_outcome', mat((original_record0 - P0) * U0 * m) == s.zeros(16, 1))
    S = s.Matrix([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    ES = ns['ext'](S)
    check('axis_rotation_is_signed_basis_permutation', all((sum((v != 0 for v in ES.row(i))) == 1 for i in range(16))) and all((v in (-1, 0, 1) for v in ES)))
    check('axis_gate_exact_literal_intertwining', mat(ES * U0 * ES.T - Um) == s.zeros(16))
    check('axis_cut_exact_literal_intertwining', ES * P0 * ES.T == Pm)

    def permutation(bit_map, nbits=4):
        out = s.zeros(1 << nbits)
        for old in range(1 << nbits):
            out[bit_map(old), old] = 1
        return out

    def X(j, nbits=4):
        return permutation(lambda b: b ^ 1 << j, nbits)

    def CX(c, t, nbits=4):
        return permutation(lambda b: b ^ (b >> c & 1) << t, nbits)

    def SW(j, k, nbits=4):
        return CX(j, k, nbits) * CX(k, j, nbits) * CX(j, k, nbits)
    G = s.Matrix([[a, -p], [p, a]])
    G0 = s.kronecker_product(s.eye(8), G)
    check('native_G_transpose_echo', mat(X(0) * G0 * X(0) - G0.T) == s.zeros(16))
    D = mat(U0 * G0.T)
    expectedD = s.diag(*[(-1) ** ((b & 1) * int(sum((b >> j & 1 for j in (1, 2, 3))) >= 2)) for b in range(16)])
    check('native_U0_majority_phase_exact', D == expectedD)
    A = D * X(2) * D * X(2)
    CZ01 = CX(3, 1) * A * CX(3, 1)
    Z0 = A * X(3) * A * X(3)
    check('derived_CZ01_without_assumed_CZ', CZ01 == s.diag(*[(-1) ** ((b & 1) * (b >> 1 & 1)) for b in range(16)]))
    check('derived_Z0_without_assumed_reflection', Z0 == s.diag(*[(-1) ** (b & 1) for b in range(16)]))
    axis_word = SW(0, 1) * Z0 * CZ01
    check('exact_all16_axis_word', axis_word == ES)
    check('recording_by_old_P0_cut_then_restore', mat(axis_word * P0 * U0 * axis_word.T - Pm * Um) == s.zeros(16))
    input32 = s.Matrix.vstack(m, s.zeros(16, 1))
    seed_copy = CX(0, 4, 5)
    check('family_specific_retained_one_from_initial_copy', seed_copy * input32 == s.Matrix.vstack(s.zeros(16, 1), m))
    U032 = s.diag(U0, U0)
    G032 = s.diag(G0, G0)

    def Xbuf(j):
        return CX(4, j, 5)
    D32 = mat(U032 * Xbuf(0) * G032 * Xbuf(0))
    A32 = mat(D32 * Xbuf(2) * D32 * Xbuf(2))
    CZ32 = mat(CX(3, 1, 5) * A32 * CX(3, 1, 5))
    Z32 = mat(A32 * Xbuf(3) * A32 * Xbuf(3))
    ES32 = mat(SW(0, 1, 5) * Z32 * CZ32)
    check('retained_one_exact_all16_clean_code_axis_word', ES32[16:, 16:] == ES and ES32[:16, 16:] == s.zeros(16) and (ES32[16:, :16] == s.zeros(16)))
    check('all_offcode_buffer_complement_retained_unitarily', mat(ES32.T * ES32 - s.eye(32)) == s.zeros(32))
    ESback32 = mat(CZ32 * Z32 * SW(0, 1, 5))
    check('axis_inverse_without_U0_adjoint_primitive', ESback32[16:, 16:] == ES.T and ESback32[:16, 16:] == s.zeros(16))
    check('inverse_word_offcode_complement_unitary', mat(ESback32.T * ESback32 - s.eye(32)) == s.zeros(32))
    check('entire_second_axis_word_on_retained_buffer', mat((ES32 * U032 * ESback32)[16:, 16:] - Um) == s.zeros(16))
    K = {'00': mat(Pm * Um * P0 * U0), '01': mat((I - Pm) * Um * P0 * U0), '10': mat(P0 * U0 * (I - P0) * U0), '11': mat((I - P0) * U0 * (I - P0) * U0)}
    check('all16_Kraus_completeness', mat(sum((k.T * k for k in K.values()), s.zeros(16)) - I) == s.zeros(16))
    prob = {h: red(((k * m).T * (k * m))[0] / norm) for (h, k) in K.items()}
    z = s.Rational(1, 2) + 2 * a * p * r / (1 + r * r)
    expected = {'00': p * p * z, '01': p * p * (1 - z), '10': p ** 3, '11': p * p}
    check('all_four_actual_history_probabilities', all((red(prob[h] - v) == 0 for (h, v) in expected.items())))
    check('all_history_probabilities_sum_one', red(sum(prob.values()) - 1) == 0)
    check('strict_branch_probability_gap', red(s.Rational(1, 2) - a * p - (a - p) ** 2 / 2) == 0)
    dz = s.diff(z, r)
    ddz = s.diff(z, r, 2)
    check('entropy_first_source_zero_at_r1', red(dz.subs(r, 1)) == 0)
    check('entropy_second_source_coefficient', red(ddz.subs(r, 1) + a * p) == 0)
    N0 = I - P0
    E = {h: mat(k.T * k) for (h, k) in K.items()}
    Aproj = mat(N0 * E['00'] * N0 / (p * p))
    W = [1, 3, 13, 15]
    P2 = s.Matrix([[p, a * p], [a * p, p * p]])
    check('all_N0_first_leaf_normalized_effect_is_projector', mat(Aproj * Aproj - Aproj) == s.zeros(16))
    check('four_coefficient_projector_block', mat(Aproj.extract(W, W) - s.diag(P2, P2)) == s.zeros(4))
    check('all_N0_other_leaf_effects', mat(N0 * E['01'] * N0 - p * p * (N0 - Aproj)) == s.zeros(16) and mat(N0 * E['10'] * N0 - p ** 3 * N0) == s.zeros(16) and (mat(N0 * E['11'] * N0 - p * p * N0) == s.zeros(16)))
    m1 = m.subs(r, 1)
    s1 = s.Rational(1, 2) + a * p
    c = p - s.Rational(1, 2)
    delta = mat((Aproj - s1 * N0) * m1)
    expected_delta = s.zeros(16, 1)
    for (mask, sign) in zip(W, (1, -1, 1, -1)):
        expected_delta[mask] = c * sign
    check('exact_nonzero_all_amplitude_normal', mat(delta - expected_delta) == s.zeros(16, 1) and delta != s.zeros(16, 1))
    check('amplitude_normal_is_sphere_tangent', red((m1.T * delta)[0]) == 0 and N0 * delta == delta)
    check('full_amplitude_expectation_derivative', red((delta.T * Aproj * m1)[0] / 2 - 2 * c * c) == 0)
    check('whole_blank_and_buffer_sector_commute', mat(blank * N0 - N0 * blank) == s.zeros(16))
    check('whole_blank_projection_kills_normal', mat(blank * delta) == s.zeros(16, 1))
    dbranch0 = mat(P0 * U0 * delta)
    dbranch1 = mat(N0 * U0 * delta)
    check('normal_keeps_branch_observer_axes_locally', all((dbranch0[1 << i] == 0 for i in (0, 2, 3))) and all((dbranch1[1 << i] == 0 for i in (1, 2, 3))))
    check('normal_is_outside_original_blank_readout_identification', mat((original_record0 - P0) * U0 * delta) != s.zeros(16, 1))
    PBm = ES * blank * ES.T
    check('intrinsic_and_occupation_second_cuts_commute', mat(PBm * Pm - Pm * PBm) == s.zeros(16) and mat(blank * P0 - P0 * blank) == s.zeros(16))
    intrinsic = {}
    joint = {}
    joint_prob = {}
    intrinsic_prob = {}
    for (i, (V, PB, PA)) in enumerate(((Um, PBm, Pm), (U0, blank, P0))):
        firstcut = blank if i == 0 else I - blank
        for j in range(2):
            oldcut = PB if j == 0 else I - PB
            ki = mat(oldcut * V * firstcut * U0)
            intrinsic[str(i) + str(j)] = ki
            intrinsic_prob[str(i) + str(j)] = red(((ki * m).T * (ki * m))[0] / norm)
            for k in range(2):
                activecut = PA if k == 0 else I - PA
                kj = mat(activecut * ki)
                joint[str(i) + str(j) + str(k)] = kj
                joint_prob[str(i) + str(j) + str(k)] = red(((kj * m).T * (kj * m))[0] / norm)
    iq = {'00': p * p / 2, '01': p * p / 2, '10': p * p, '11': p ** 3}
    jq = {'000': p * p * z / 2, '001': p * p * (1 - z) / 2, '010': p * p * z / 2, '011': p * p * (1 - z) / 2, '100': 0, '101': p * p, '110': p ** 3, '111': 0}
    check('literal_intrinsic_four_history_law', all((red(intrinsic_prob[h] - v) == 0 for (h, v) in iq.items())))
    check('literal_intrinsic_history_has_zero_r_source', all((s.diff(v, r) == 0 for v in intrinsic_prob.values())))
    check('complete_intrinsic_plus_occupation_eight_history_law', all((red(joint_prob[h] - v) == 0 for (h, v) in jq.items())))
    check('joint_instrument_all16_completeness', mat(sum((k.T * k for k in joint.values()), s.zeros(16)) - I) == s.zeros(16))
    check('joint_marginals_recover_both_retained_laws', all((red(sum((joint_prob[i + j + k] for j in '01')) - prob[i + k]) == 0 for i in '01' for k in '01')) and all((red(sum((joint_prob[i + j + k] for k in '01')) - intrinsic_prob[i + j]) == 0 for i in '01' for j in '01')))
    active_copy = CX(0, 4, 5)
    check('new_occupation_readout_is_literal_CNOT', active_copy[:16, :16] == P0 and active_copy[16:, :16] == N0)
    check('second_intrinsic_readout_differs_in_both_branches', any((red(intrinsic_prob['0' + j] - prob['0' + j]) != 0 for j in '01')) and any((red(intrinsic_prob['1' + j] - prob['1' + j]) != 0 for j in '01')))
    intrinsic_cost = red(sum(((2 + int(h[0]) + int(h[1])) * v for (h, v) in intrinsic_prob.items())))
    joint_code_cost = red(sum(((3 + sum(map(int, h))) * v for (h, v) in joint_prob.items())))
    check('original_intrinsic_code_cost_constant', red(intrinsic_cost - (3 + 5 * p) / 2) == 0)
    check('explicit_extra_readout_code_cost', red(joint_code_cost - ((9 + p) / 2 - p * p * z)) == 0)
    check('literal_U0_inverse_word', mat(G0.T * U0 * G0.T - U0.T) == s.zeros(16))
    Ginv32 = mat(Xbuf(0) * G032 * Xbuf(0))
    Uinv32 = mat(Ginv32 * U032 * Ginv32)
    check('retained_buffer_realizes_full16_U0_inverse', Uinv32[16:, 16:] == mat(U0.T) and Uinv32[:16, 16:] == s.zeros(16))
    check('inverse_realization_retains_offcode_complement', mat(Uinv32.T * Uinv32 - s.eye(32)) == s.zeros(32))
    costs = {'00': 2, '01': 3, '10': 3, '11': 4}
    cost = red(sum((costs[h] * prob[h] for h in costs)))
    check('selected_occupation_view_binary_code_cost', red(cost - (4 - p - p * p * z)) == 0)
    check('port_cost_second_source_at_r1', red(s.diff(cost, r, 2).subs(r, 1) - a * p ** 3) == 0)
    halt = {'0H': p * p, '10': p * p, '11': p ** 3}
    check('singular_halt_complete_prefix_cut', red(sum(halt.values()) - 1) == 0)
    check('singular_halt_matches_native_intrinsic_labels', red(halt['10']-intrinsic_prob['10'].subs(r,0)) == 0 and red(halt['11']-intrinsic_prob['11'].subs(r,0)) == 0)
    return dict(status='PASS', checks=checks, source_definition_pins=pins, domain='r>0; known initial whole-blank ray m_r/sqrt(2(1+r^2)); read first native pointer before selecting the second axis gate', branch_observers={'0': '-e1', '1': 'e0'}, probabilities={'00': 'p^2*s(r)', '01': 'p^2*(1-s(r))', '10': 'p^3', '11': 'p^2'}, s='1/2+2*a*p*r/(1+r^2)', entropy={'H': '(1+p)*h(p^2)+p^2*h(s)', 'Hprime': 'p^2*log((1-s)/s)*sprime', 'Hsecond': 'p^2*(log((1-s)/s)*ssecond-sprime^2/(s*(1-s)))', 'at_r1_first': '0', 'at_r1_second': '-a*p^3*log((1/2-a*p)/(1/2+a*p)) >0'}, preparation_scope={'N0_effect': 'E00|N0=p^2*A, A^2=A; E01=p^2*(I-A), E10=p^3*I, E11=p^2*I', 'ordered_four_subspace': '(e0,e01,e023,Omega): A=diag(P2,P2), P2=[[p,a*p],[a*p,p^2]]', 'r1_normal': 'raw m1=(1,1,1,1), delta_m=(A-s1)*m1=(p-1/2)*(1,-1,1,-1), s1=1/2+a*p', 'normalized_source': 'For psi=m1/2 and delta_psi=delta_m/2, D s=2*(p-1/2)^2 and D H=2*p^2*(p-1/2)^2*log((1/2-a*p)/(1/2+a*p))<0', 'blank_constraint': 'The actual whole-blank projector annihilates delta_m exactly and commutes with N0. Therefore this is a preparation-normal row outside the whole-blank code, not an admissible whole-blank tangent. The fixed-policy entropy gradient projects to zero on the whole-blank sphere at m1.', 'scope': 'This preparation-normal calculation concerns the extended fixed P0 occupation-cut protocol, not the intrinsic-plus-copy instrument off its blank input code. Hsecond(r1)>0 is not full native preparation Euler. On larger preparation changes the branch-dependent tuple can also change its axis, requiring the actual controller and field derivatives. The original first-record/active-cut equality is not extended off the blank code.'}, intrinsic_record={'probabilities': ['p^2/2', 'p^2/2', 'p^2', 'p^3'], 'H': '(1+p)*h(p^2)+p^2*log(2)', 'r_source': '0', 'original_two_port_code_mean': '(3+5*p)/2'}, complete_joint_record={'order': 'first intrinsic, second intrinsic, added occupation copy', 'probabilities': {'000': 'p^2*s/2', '001': 'p^2*(1-s)/2', '010': 'p^2*s/2', '011': 'p^2*(1-s)/2', '100': '0', '101': 'p^2', '110': 'p^3', '111': '0'}, 'H': '(1+p)*h(p^2)+p^2*h(s)+p^2*log(2)', 'r_source': 'Same as selected occupation marginal, because the additional conditional intrinsic entropy is the constant p^2*log(2).', 'all_three_binary_lengths_1_2_mean': '(9+p)/2-p^2*s', 'resource': 'Added active-occupation output is explicitly copied by CNOT mode0 to a distinct fresh-zero readout bit. It does not replace either intrinsic record. The additional code/reading and its physical selection must be declared.'}, exact_inverse_resource={'identity': 'U0^T=G0^T U0 G0^T; G0^T=X0 G0 X0', 'cost': 'One initial CNOT supplies the retained-one buffer on the specified input family. Each inverse G uses one forward G and two CNOTs; each inverse U0 uses one forward U0, two G and four CNOTs. CNOT is its own inverse.', 'scope': 'Closes the inverse-supply premise of the already owned fixed-width addressed compiler class on this prepared subspace, not all-state basis preparation, density, derivative compilation or full-price admission by itself.'}, selected_occupation_code={'expected_cost': '4-p-p^2*s', 'first_source': '-p^2*sprime', 'second_source_r1': 'a*p^3', 'scope': 'Selected occupation-view binary lengths1,2 only; these are not the original intrinsic two-port law. No assertion that this pays controller, labels, normalization computation or archive storage.'}, singular_cut={'native_intrinsic_r0': {'0H': 'p^2', '10': 'p^2', '11': 'p^3'}, 'occupation_marginal_r0': {'0H': 'p^2', '10': 'p^3', '11': 'p^2'}, 'complete_joint_r0': {'0H': 'p^2', '101': 'p^2', '110': 'p^3'}, 'entropy': '(1+p)*h(p^2)', 'warning': 'No silently chosen U at zero first grade. Continuation from r>0 is a different instrument; its full joint entropy has an extra 2*p^2*log(2), while either separate marginal adds p^2*log(2).'}, reference='The four all16 Kraus maps tensor I_reference128. Completeness preserves the full RIGHT marginal after summing histories; individual conditioned RIGHT marginals need not equal the initial one. A product initial known m preserves its spectator reference in each branch.', history_carrier='Complete joint law: eight retained histories times CAR16 times the explicit retained control buffer =256 dimensions before tensoring reference128. The selected four-history marginal alone has logical dimension64. The extra occupation readout and control buffer are separate declared record resources; old intrinsic outputs, all complements and costs are retained.', execution='Exact axis word: D=U0 G0^T, A=D X2 D X2, CZ01=CX(3,1) A CX(3,1), Z0=A X3 A X3, Lambda(S)=SWAP01 Z0 CZ01. All16 and the full32 retained-buffer completion are verified. One fresh-zero bit is copied from initial occupation bit0, which equals one on the specified seed family; it remains a constant control and implements X with CNOT. The branch0 second round is Lambda(S)^T, U0, old P0 readout, Lambda(S). This is a classical history-address policy, not arbitrary coherent controlled-word generation. The input-family premise, extra retained bit, all offcode unitary action and controller cost remain explicit.', whole_price='If and only if the actual complete raw Book weight is the normalized Born history law and its full code/reference is supplied, expected Cost-Info=H/log(phi). Deterministic controller metadata is a function of history and adds no Shannon entropy, but this does not set its physical cost to zero or prove that binding.', distinction='This is not the unmeasured chronology U_(a,-pr)/sqrt(p+p^2*r^2) U_e0. Measuring the first record changes both its conditional state and its next metric/query.')

def clock_consumer():
    (t, u, eps) = s.symbols('t u epsilon', real=True)
    c = s.symbols('c', positive=True)
    J = 1 + eps * s.cos(2 * s.pi * t)
    q = s.diag(c * c / J ** 2, -c * c, -c * c, -c * c)
    b = s.Matrix([c / J, 0, 0, 0])
    g = q.inv()
    alpha = s.simplify(g * b)
    if not alpha == s.Matrix([J / c, 0, 0, 0]):
        raise ArithmeticError('alpha == s.Matrix([J / c, 0, 0, 0])')
    if not s.simplify((alpha.T * q * alpha)[0] - 1) == 0:
        raise ArithmeticError('s.simplify((alpha.T * q * alpha)[0] - 1) == 0')
    integral = s.integrate(alpha[0], (t, 0, t))
    total = s.integrate(alpha[0], (t, 0, 1))
    tau = s.simplify(integral / total)
    if not s.simplify(tau - t - eps * s.sin(2 * s.pi * t) / (2 * s.pi)) == 0:
        raise ArithmeticError('s.simplify(tau - t - eps * s.sin(2 * s.pi * t) / (2 * s.pi)) == 0')
    if not s.simplify(s.diff(tau, t) - J) == 0:
        raise ArithmeticError('s.simplify(s.diff(tau, t) - J) == 0')
    X1 = -s.sin(2 * s.pi * u) / (2 * s.pi)
    X2 = s.sin(4 * s.pi * u) / (2 * s.pi)
    X = u + eps * X1 + eps ** 2 * X2 / 2
    residual = s.series(tau.subs(t, X) - u, eps, 0, 3).removeO().expand()
    if not s.simplify(residual) == 0:
        raise ArithmeticError('s.simplify(residual) == 0')
    r_star = s.symbols('r_star', positive=True)
    M = s.symbols('M', integer=True, positive=True)
    ell = s.symbols('ell', positive=True)
    r = r_star / J ** 2
    r1 = s.diff(r, eps).subs(eps, 0)
    r2 = s.diff(r, eps, 2).subs(eps, 0)
    if not s.simplify(r1 + 2 * r_star * s.cos(2 * s.pi * t)) == 0:
        raise ArithmeticError('s.simplify(r1 + 2 * r_star * s.cos(2 * s.pi * t)) == 0')
    if not s.simplify(r2 - 6 * r_star * s.cos(2 * s.pi * t) ** 2) == 0:
        raise ArithmeticError('s.simplify(r2 - 6 * r_star * s.cos(2 * s.pi * t) ** 2) == 0')
    hprime = s.log((1 - r_star) / r_star)
    hsecond = -1 / (r_star * (1 - r_star))
    H1 = s.simplify(M / ell * hprime * r1)
    H2 = s.simplify(M / ell * (hsecond * r1 ** 2 + hprime * r2))
    expected = M * r_star / ell * (6 * s.log((1 - r_star) / r_star) - 4 / (1 - r_star)) * s.cos(2 * s.pi * t) ** 2
    if not s.simplify(H2 - expected) == 0:
        raise ArithmeticError('s.simplify(H2 - expected) == 0')
    nodes = [s.S(0), s.Rational(1, 4), s.Rational(1, 2), s.Rational(3, 4)]
    if not sum((s.cos(2 * s.pi * x) for x in nodes)) == 0:
        raise ArithmeticError('sum((s.cos(2 * s.pi * x) for x in nodes)) == 0')
    if not sum((s.cos(2 * s.pi * x) ** 2 for x in nodes)) == 2:
        raise ArithmeticError('sum((s.cos(2 * s.pi * x) ** 2 for x in nodes)) == 2')
    first = s.simplify(sum((H1.subs(t, x) for x in nodes)))
    second = s.simplify(sum((H2.subs(t, x) for x in nodes)))
    if not first == 0:
        raise ArithmeticError('first == 0')
    if not s.simplify(second - 2 * M * r_star / ell * (6 * s.log((1 - r_star) / r_star) - 4 / (1 - r_star))) == 0:
        raise ArithmeticError('s.simplify(second - 2 * M * r_star / ell * (6 * s.log((1 - r_star) / r_star) - 4 / (1 - r_star))) == 0')
    return {'status': 'PASS', 'owned_clock_identity': 'b=Fn,q=FetaF^T,g=q^-1;alpha=gb=F^-Teta n;alpha^Tqalpha1', 'clock_source': 'Dalpha=-g(Dq)alpha+gDb;actualq,bjetsincludeclockandcoframevariations', 'direction_vs_scale': 'beta_n/nu constantalonglapse n=e0;scalecomesfromactualCARcoefficientu0andclockcalibration,notpointeralone', 'lapse_b': 'b0=c/J;J=1+epsilon cos2pi t;alpha0=J/c', 'normalized_proper_time': str(tau), 'inverse_first_jet': str(X1), 'inverse_second_jet': str(X2), 'general_inverse_jet': 'Xa=-tau_a/tau_t;Xab=-(tau_ab+tau_ta Xb+tau_tb Xa+tau_tt XaXb)/tau_t', 'C2_bound_scope': 'positiveclockgap tau_t>=kappa andboundedC3time/C2fieldjetsgiveC2stableinverse;quadratureandpolynomialqueryerrorsmustcontrolthesejets', 'conditional_coherent_availability': 'alphaandinverseareanalyticfunctionsalreadyownedCAR/clockqueryinvariantsoncompactgapchart;existingall-outputC3compilerappliesifthoseaddressedqueriesareactuallysupplied', 'actual_metrology_flag_law': 'r=delta^2 b0^2=r_star/J^2;scalar rI16 effectmakesfreshflaglawsBernoulliproductevenwithsameunknownmatter/fulloldhistory/reference128', 'probe_count': 'fourquarter-periodsettings,Meach:4Mretainedcoframeflags;clocknormalizationflagsmayberetainedtooandarefieldindependenthere', 'full_same_history_price': 'meanCostInfo=H(fullflags)/ell=M sum_j h(rj)/ell forcompletecutN1;fixedcodeanditsgaincancelasowned,notasassumedzerohardwarecost', 'at_background_first_source': str(first), 'at_background_second_source': str(second), 'strict_positive_scope': '0<r_star<=1/16;6log((1-r_star)/r_star)-4/(1-r_star)>=6log15-64/15>116/15;log15>2sincee<3', 'price_consequence': 'finitefrequencyclockcanapproximateplacementbutthisretainedmeasurementpricehasnonvanishingO(M)lapseHessian;mustnotdropflagsorpriceitonlybyfixedgatecount', 'old_RIGHT': 'operationsonactivequery/freshworkcommutewithfixedoldRIGHTandreference;newrecordretained,noresetorunknownstatecloning', 'minimal_native_primitive_consumer': 'bindactualelapsedtime/addressactuationtointegralofalphaandX=tau^-1(wordseed),includingallwork/outcomecontrollerprice;currentgatepointeridentitydoesnotstateit', 'scope': 'measuredmetrologyrouteonly;coherentqueryrouteisnotexcluded;computabilityisnotnativeexecutionselectionorfullsourcepreservation', 'native_clock_law_claimed': False, 'full_physical_price_preservation_claimed': False}


def retained_clock_factory(root):
    root = Path(root)
    checks = []

    def require(name, value):
        if value is not True:
            raise AssertionError(name)
        checks.append(name)
    p = (s.sqrt(5) - 1) / 2
    a = s.simplify(p ** 2)
    require('golden normalization', s.simplify(p + a - 1) == 0)
    for k in range(1, 6):
        words = list(itertools.product((0, 1), repeat=k))
        probs = [s.prod((a if bit else p for bit in word)) for word in words]
        costs = [sum((2 if bit else 1 for bit in word)) for word in words]
        require(f'complete unconditional coin bank k={k}', s.simplify(sum(probs) - 1) == 0)
        require(f'coin bank success k={k}', s.simplify(probs[-1] - a ** k) == 0)
        expected = s.simplify(sum((q * c for (q, c) in zip(probs, costs))))
        require(f'coin bank entropy and actual mean golden cost k={k}', s.simplify(expected - k * (p + 2 * a)) == 0)
    for k in range(1, 6):
        eps = s.simplify(a ** k)
        probs = [s.simplify(p * a ** j) for j in range(k)] + [eps]
        costs = [2 * j + 1 for j in range(k)] + [2 * k]
        require(f'complete retained prefix k={k}', s.simplify(sum(probs) - 1) == 0)
        expected = s.simplify(sum((q * c for (q, c) in zip(probs, costs))))
        require(f'prefix entropy divided by ell equals actual golden mean cost k={k}', s.simplify(expected - s.sqrt(5) * (1 - eps)) == 0)
    (r, u, theta) = s.symbols('r u theta', real=True)
    f = u ** 4 + theta * u ** 3 + theta ** 2 * u ** 2
    for l in (2, 3, 4):
        B = sum((s.binomial(l, j) * r ** j * (1 - r) ** (l - j) * f.subs(u, s.Rational(j, l)) for j in range(l + 1)))
        for order in (0, 1, 2):
            delta = f
            for _ in range(order):
                delta = s.expand(delta.subs(u, u + s.Rational(1, l)) - delta)
            rhs = s.ff(l, order) * sum((s.binomial(l - order, j) * r ** j * (1 - r) ** (l - order - j) * delta.subs(u, s.Rational(j, l)) for j in range(l - order + 1)))
            require(f'exact Bernstein law derivative l={l}, order={order}', s.expand(s.diff(B, r, order) - rhs) == 0)
        rr = s.Rational(1, 3) + theta / 20
        composed = B.subs(r, rr)
        chain2 = (s.diff(B, theta, 2) + s.diff(B, theta, r) / 10 + s.diff(B, r, 2) / 400).subs(r, rr)
        require(f'full second field derivative includes likelihood derivative l={l}', s.expand(s.diff(composed, theta, 2) - chain2) == 0)
    eps = s.symbols('epsilon', positive=True)
    for M in range(1, 7):
        reciprocal = sum((s.binomial(M, l) * eps ** l * (1 - eps) ** (M - l) / s.Integer(l + 1) for l in range(M + 1)))
        formula = (1 - (1 - eps) ** (M + 1)) / ((M + 1) * eps)
        require(f'exact rare-success reciprocal moment M={M}', s.cancel(reciprocal - formula) == 0)
    clock = [(p, 0, 0), (a * (1 - r), 1, 0), (a * r, 1, 1)]
    geom = {s.S(0): s.Rational(1, 4), s.Rational(1, 2): s.Rational(5, 16), s.S(1): s.Rational(3, 8)}
    records = []
    for pair in itertools.product(clock, repeat=2):
        prob = s.prod((row[0] for row in pair))
        L = sum((row[1] for row in pair))
        K = sum((row[2] for row in pair))
        estimate = s.Rational(K, L) if L else s.Rational(1, 2)
        e = geom[estimate]
        records.append((prob, e, L, K))
    require('all nine complete clock histories retained', len(records) == 9)
    require('complete clock normalizer', s.simplify(sum((row[0] for row in records)) - 1) == 0)
    full = []
    for (prob, e, _, _) in records:
        for bits in itertools.product((0, 1), repeat=2):
            gp = s.prod((e if bit else 1 - e for bit in bits))
            full.append(s.expand(prob * gp))
    require('two actual geometry calls and all thirty-six full histories', len(full) == 36)
    require('full factory normalizer', s.simplify(sum(full) - 1) == 0)
    for e in geom.values():
        h = -e * s.log(e) - (1 - e) * s.log(1 - e)
        hg = -sum((s.expand_log(s.log(s.prod((e if bit else 1 - e for bit in bits))), force=True) * s.prod((e if bit else 1 - e for bit in bits)) for bits in itertools.product((0, 1), repeat=2)))
        require(f'two-call geometry entropy at e={e}', s.simplify(hg - 2 * h) == 0)
    (sig, mm, ee) = s.symbols('sigma M epsilon', positive=True)
    P = theta ** 2 + theta ** 3
    C = theta + theta ** 3
    Y = theta ** 4
    whole = (mm * sig * P + mm * ee * C + Y) / (mm * sig)
    for order in (1, 2):
        require(f'whole-price signal-normalized field derivative order={order}', s.simplify(s.diff(whole, theta, order) - s.diff(P, theta, order) - ee / sig * s.diff(C, theta, order) - s.diff(Y, theta, order) / (mm * sig)) == 0)
    source_paths = ['02_REGISTRY/research/sources/d0_operational_car_clock_readout_2026-10-17/RESULT_RU.md', '02_REGISTRY/research/A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md', '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md']
    pins = {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in source_paths}
    return {'status': 'PASS', 'checks': len(checks), 'checked_identities': checks, 'source_sha256': pins, 'actual_prefix': 'MAIN: execute all k independent fresh golden coins. A word with j R bits has probability p^(k+j); all 2^k words are retained. Success R^k has probability epsilon=p^(2k).', 'actual_prefix_cost': 'MAIN: E Cost = H(coin bank)/ell = k*(p+2*p^2), field-independent. OPTIONAL stopped causal prefix has E Cost = H(prefix)/ell = sqrt(5)*(1-epsilon), only if that stopping policy is supplied.', 'complete_factory': 'Old measured Y once, M full k-coin banks, d clock probes on each R^k success, deterministic retained record-to-address policy, then M actual scalar geometry calls.', 'exact_normalized_price': 'H(Y)/(M*ell) + k*h(p^2)/ell + epsilon*sum_j h(r_j)/ell + E[g_geom(theta, Phi_clip(K/L))]. With L=0 use one fixed fallback address. This normalizes the WHOLE action by M.', 'scalar_scope': 'Clock and geometry effects must be scalar conditionally on retained Y, or a separately priced fresh factory must prove the same product law. No arbitrary repeated non-scalar POVM is replaced by iid outcomes.', 'likelihood_binding': 'This is the existing SAME-history w=q binding on the complete finite trace-preserving tree, N identically 1. No physical Book binding is inferred from Born normalization alone.', 'bernstein_derivative': 'D_r^alpha B_l F = product_j[(l)_(alpha_j)/l^(alpha_j)] * E[D_u^alpha F(Z)]; Z_j=[Bin(l-alpha_j,r_j)+sum_(s<=alpha_j) Uniform_s]/l; total |alpha|<=2.', 'bernstein_C2': 'For F in C^4 with norm K and r in C^2, on the compact chart, ||B_l F(theta,r(theta))-F(theta,r(theta))||_C2 <= C/l. All source derivatives through the outcome law are included.', 'explicit_C2_constant': 'Using max-component derivative norms, one safe C is (3+d+d^2)*K*(1+2*d*R1+d*R2+d^2*R1^2), for R1=max |D r_j| and R2=max |D^2 r_j|.', 'rare_success_bound': 'Error <= 2*C/((M+1)*epsilon) + C_fallback*exp(-M*epsilon), because E[1/(L+1)] = [1-(1-epsilon)^(M+1)]/[(M+1)*epsilon].', 'full_source_bound': 'Let A_n=||sum h(r_nj)/ell||_C2, B_n=actual Bernstein C2 constant, D_n=fallback bound, Y_n=||H(Y_n)/ell||_C2 and sigma_n>0 be the actual field-independent geometric signal. After retaining the exact field-independent coin-bank constant, the signal-normalized C2 error is <= [epsilon*A_n + 2*B_n/((M+1)*epsilon) + D_n*exp(-M*epsilon) + Y_n/M]/sigma_n. Every constant is allowed to depend on h_n,t_n and actual query derivatives.', 'arbitrary_signal_conditions': 'Require epsilon*A_n/sigma_n -> 0, B_n/(M*epsilon*sigma_n) -> 0, D_n*exp(-M*epsilon)/sigma_n -> 0 and Y_n/(M*sigma_n) -> 0. Unit-level weak-clock convergence alone is insufficient.', 'only_C2_variant': 'No uniform C4 hypothesis is needed for qualitative convergence. With joint C2 F_n, let K_n bound all mixed derivatives through order 2 and omega_n be their uniform spatial modulus. For l>=2 and eta>0, the Bernstein error before the r-chain factor is <= K_n/l + omega_n(eta) + 2*K_n*(d/4+1)/(l*eta^2). Choose eta_n,L0_n so this is o(sigma_n). If M*epsilon>=2*L0_n, the remaining low-L tail is <=2*C_r*K_n*exp(-M*epsilon/8), with C_r=1+2*d*R1+d*R2+d^2*R1^2.', 'regularity_scope': 'The actual clock-to-address-to-query profile F_n must be joint C2 on its chart; a bare nearest-cell map pi_h(X) is a step function. Existing C2 Palatini estimates do not supply an arbitrary uniform C4 address bound.', 'existing_AF_signal': 'The existing AF Palatini owner defines f_h=h^(-4)*P_star and normalizes the actual price by t^2, so sigma=t^2 on that supplied normalized query family. If execution instead uses raw P_star without that gain, sigma=t^2*h^4. The gain and its h-dependent query cost must be actually supplied.', 'conservative_signal_schedule': 'If actual derivative bounds A_n,B_n,D_n,Y_n grow at most polynomially and h_n=ceil(phi^(n/16))^(-1), t_n^2=h_n, even the smaller raw signal sigma_n=h_n^5 works with k_n=ceil(n/4), epsilon_n=p^(2*k_n), M_n=ceil(phi^n): epsilon_n/sigma_n<=32*p^(3*n/16), 1/(M_n*epsilon_n*sigma_n)<=32*p^(3*n/16-2), 1/(M_n*sigma_n)<=32*p^(11*n/16). Thus all source errors vanish under those stated derivative bounds. Relabel total resource budget N=2n: polynomial(n)*phi^n fits phi^N eventually for bounded/polynomial per-query cost.', 'fixed_dimension_schedule': 'M_k=ceil(phi^(3k)), epsilon_k=p^(2k). Then M_k*epsilon_k >= phi^k, source error O(p^k), retained clock source O(p^(2k)), and old-history source O(p^(3k)).', 'resource_count': 'MAIN uses exactly M*k fresh coin flags, at most d*M clock flags, and M actual geometry calls; expected clock calls are d*M*epsilon. All old RIGHT/reference128 and all raw CAR16 retained; no matter reset is used for the scalar product law.', 'golden_budget': 'For bounded per-query cost and polynomial(k) arithmetic, total resource poly(k)*phi^(3k) fits phi^(4k) eventually. Without a quantitative actual address/compiler cost bound, only a computable diagonal schedule N_k >= ceil(log_phi(actual_total_cost_k)) is justified; no universal phi-rate is asserted.', 'remaining_execution_scope': 'The actual finite causal record-to-address query policy and all its work must be supplied/compiled. Logical computability of Phi is not a native proper-time actuation law or forcing theorem. Approximate compilation needs its own complete-price C2 error control; C3 unitary approximation alone does not imply it at new zero-probability pointer branches.', 'root_scope': 'C2 convergence of the whole normalized price/source on a smooth positive chart; no exact finite roots, free factory-preparation Euler, physical admission, Einstein dynamics, or source forcing are claimed.'}


if __name__ == '__main__':
    main()
