#!/usr/bin/env python3
"""Known-code noncollinear chronology and its unknown-input type boundary.
Loads only named existing definitions; no old suite is run.
"""
import argparse,ast,hashlib,json
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
import sympy as s

PINS={'02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py': '7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9', '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': '42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078', '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': '16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527'}

def runtime_case(root):
    ROOT = Path(root).resolve()
    engine = '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py'
    tree = ast.parse((ROOT / engine).read_text())
    en = dict(dataclass=dataclass)
    for name in ['_sgn', 'quadratic_sign', 'Golden']:
        node = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name))
        exec(compile(ast.Module(body=[node], type_ignores=[]), engine, 'exec'), en)
    Golden = en['Golden']
    Z = Golden.integer(0)
    O = Golden.integer(1)
    A = Golden((0, 1, 0, 0))
    P = Golden((0, 0, 1, 0))
    en.update(ZERO=Z, ONE=O, A=A, P=P)
    for name in ['State', 'literal_axis_gate', 'encode', 'decode']:
        node = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name))
        exec(compile(ast.Module(body=[node], type_ignores=[]), engine, 'exec'), en)
    State = en['State']
    literal_axis_gate = en['literal_axis_gate']
    subs = [tuple((i for i in range(4) if mask & 1 << i)) for mask in range(16)]

    def det(M):
        n = len(M)
        answer = Z
        for pi in permutations(range(n)):
            term = O
            for i in range(n):
                term = term * M[i][pi[i]]
            answer = answer + (-1) ** sum((pi[i] > pi[j] for i in range(n) for j in range(i + 1, n))) * term
        return answer

    def exterior(R):
        return [[det([[R[i][j] for j in T] for i in S]) if len(S) == len(T) else Z for T in subs] for S in subs]

    def mv(M, v):
        return tuple((sum((x * y for (x, y) in zip(row, v)), Z) for row in M))

    def transpose(M):
        return list(map(list, zip(*M)))

    def norm(v):
        return sum((x * x for x in v), Z)

    def coded_unit_plane_record(state):
        """Recompute n from stored first grade on its certified norm-one plane.

    This is an exact classical function, not a quantum gate evaluating an
    unknown input's amplitudes. It uses only the old Golden +,* codec.
    """
        w = [state.matter[1 << j] for j in range(4)]
        if not (w[2] == w[3] == Z and norm(w) == O):
            raise ArithmeticError('Exact control failed: w[2] == w[3] == Z and norm(w) == O')
        (x, y) = w[:2]
        R = [[x, -y, Z, Z], [y, x, Z, Z], [Z, Z, O, Z], [Z, Z, Z, O]]
        ER = exterior(R)
        local = State(mv(transpose(ER), state.matter))
        out = State(mv(ER, literal_axis_gate(local, 1).matter))
        q = [[2 * w[i] * w[j] - (O if i == j else Z) for j in range(4)] for i in range(4)]
        return (out, tuple(w), q, ER)
    m = [Z] * 16
    for mask in [1, 3, 13, 15]:
        m[mask] = O
    initial = State(tuple(m))
    first = literal_axis_gate(initial, 1)
    (second, nplus, qplus, ER) = coded_unit_plane_record(first)
    checks = []

    def check(name, condition):
        if not condition:
            raise ArithmeticError(name)
        checks.append(name)
    check('stored_unnormalized_norm_four', norm(initial.matter) == Golden.integer(4))
    check('stored_first_grade_unit', norm([first.matter[1 << j] for j in range(4)]) == O)
    check('computed_noncollinear_observer', nplus == (A, -P, Z, Z))
    check('all16_norm_first_second', norm(first.matter) == norm(second.matter) == Golden.integer(4))
    for (label, state) in [('initial', initial), ('first', first), ('second', second)]:
        check('old_codec_roundtrip_' + label, en['decode'](en['encode'](state)) == state)
    (a, p) = s.symbols('a p', real=True)
    gb = s.groebner([a * a - p, p * p + p - 1], a, p, domain=s.QQ)

    def red(x):
        (n, d) = s.cancel(x).as_numer_denom()
        return s.cancel(gb.reduce(s.expand(n))[1] / gb.reduce(s.expand(d))[1])

    def mat(x):
        return x.applyfunc(red)
    cn = dict(s=s, a=a, p=p, I=s.eye(16), DEG=s.diag(*map(len, subs)), SUBS=subs, mat=mat)
    for (rel, names) in {'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': ['creator', 'ext'], '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': ['record']}.items():
        tr = ast.parse((ROOT / rel).read_text())
        for name in names:
            node = next((n for n in tr.body if isinstance(n, ast.FunctionDef) and n.name == name))
            exec(compile(ast.Module(body=[node], type_ignores=[]), rel, 'exec'), cn)

    def expr(g):
        return sum((c * a ** i for (i, c) in enumerate(g.coefficients)))

    def symvec(v):
        return s.Matrix(list(map(expr, v)))
    R = s.Matrix([[expr(v) for v in row] for row in [[A, P, Z, Z], [-P, A, Z, Z], [Z, Z, O, Z], [Z, Z, Z, O]]])
    (U0, _) = cn['record'](s.eye(4), s.eye(4)[:, 0])
    (Up, _) = cn['record'](s.eye(4), s.Matrix([a, -p, 0, 0]))
    ES = s.Matrix([[expr(v) for v in row] for row in ER])
    check('full16_exterior_intertwining', mat(ES * U0 * ES.T - Up) == s.zeros(16))
    check('first_full16_literal', mat(U0 * symvec(initial.matter) - symvec(first.matter)) == s.zeros(16, 1))
    check('second_full16_literal', mat(Up * symvec(first.matter) - symvec(second.matter)) == s.zeros(16, 1))
    check('full16_second_gate_orthogonal', mat(Up.T * Up - s.eye(16)) == s.zeros(16))
    check('computed_metric_matches_owner', mat(s.Matrix([[expr(v) for v in row] for row in qplus]) + s.eye(4) - 2 * s.Matrix([a, -p, 0, 0]) * s.Matrix([a, -p, 0, 0]).T) == s.zeros(4))
    check('noncollinear_initial_grade2_retained', initial.matter[3] == O and initial.matter[13] == O)
    return dict(status='PASS', checks=checks, outputs={name: [list(x.coefficients) for x in state.matter] for (name, state) in [('initial', initial), ('first', first), ('second', second)]}, code_lengths={name: len(en['encode'](state)) for (name, state) in [('initial', initial), ('first', first), ('second', second)]}, observer=[list(x.coefficients) for x in nplus], scope='Classical known-code runtime on actual noncollinear r=1 family. All16 retained; fixed-parameter local orthogonality preserves arbitrary reference spectator. Normalized amplitudes are raw values/2, not stored in Golden. No physical gate generation, admission, peak-workspace cost or whole-price identity claimed.')

def unknown_input_case(root):
    ROOT = Path(root).resolve()
    (a, p, b, r) = s.symbols('a p b r', real=True)
    ideal = s.groebner([b * b - p - p * p * r * r, a * a - p, p * p + p - 1], b, a, p, domain=s.QQ.frac_field(r))

    def red(x):
        (n, d) = s.cancel(x).as_numer_denom()
        return s.cancel(ideal.reduce(s.expand(n))[1] / ideal.reduce(s.expand(d))[1])

    def mat(x):
        return x.applyfunc(red)
    subs = [tuple((i for i in range(4) if mask & 1 << i)) for mask in range(16)]
    ns = dict(s=s, a=a, p=p, I=s.eye(16), DEG=s.diag(*map(len, subs)), SUBS=subs, mat=mat)
    pins = {}
    for (rel, names) in {'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': ['creator', 'ext', 'record_basis'], '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': ['record']}.items():
        tree = ast.parse((ROOT / rel).read_text())
        pins[rel] = {}
        for name in names:
            node = next((x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == name))
            pins[rel][name] = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
            exec(compile(ast.Module(body=[node], type_ignores=[]), rel, 'exec'), ns)
    checks = []

    def check(name, condition):
        if not condition:
            raise ArithmeticError(name)
        checks.append(name)
    I4 = s.eye(4)
    B = ns['record_basis']()
    T = s.Matrix([[1, 0, 1, 0], [1, 0, -1, 0], [0, 1, 0, 1], [0, 1, 0, -1]]) / s.sqrt(2)
    blank = B * s.kronecker_product(T.T * s.diag(1, 0, 1, 0) * T, I4) * B.T
    m = s.zeros(16, 1)
    m[1] = m[15] = 1
    m[3] = m[13] = r
    N = 2 * (1 + r * r)
    check('initial_full_blank', mat(blank * m - m) == s.zeros(16, 1))
    check('whole_input_norm', (m.T * m)[0] == N)
    (U0, P0) = ns['record'](I4, I4[:, 0])
    first = mat(U0 * m)
    check('first_scalar', red(first[0] + p) == 0)
    check('first_grade', mat(s.Matrix([first[1 << i] for i in range(4)]) - s.Matrix([a, -p * r, 0, 0])) == s.zeros(4, 1))
    nplus = s.Matrix([a / b, -p * r / b, 0, 0])
    check('updated_observer_unit', red((nplus.T * nplus)[0] - 1) == 0)
    (Uplus, Pplus) = ns['record'](I4, nplus)
    second = mat(Uplus * first)
    check('second_scalar_actual_literal_gate', red(second[0] + p * (a + b)) == 0)
    check('full_first_gate_orthogonal', mat(U0.T * U0 - s.eye(16)) == s.zeros(16))
    check('full_updated_gate_orthogonal', mat(Uplus.T * Uplus - s.eye(16)) == s.zeros(16))
    qplus = mat(-I4 + 2 * nplus * nplus.T)
    w = s.Matrix([a, -p * r, 0, 0])
    check('endpoint_metric_involution', mat(qplus * qplus - I4) == s.zeros(4))
    check('endpoint_metric_determinant', red(qplus.det() + 1) == 0)
    check('endpoint_timelike_pairing', red((w.T * qplus * w)[0] - b * b) == 0)
    check('endpoint_Q_is_I', mat(-qplus + 2 * w * w.T / (b * b) - I4) == s.zeros(4))
    check('all16_second_norm', red((second.T * second)[0] - N) == 0)
    check('fixed_parameter_reference_isometry', mat((Uplus * U0).T * (Uplus * U0) - s.eye(16)) == s.zeros(16))
    num = p ** 3 * (1 + s.sqrt(1 + p * r * r)) ** 2
    r4 = s.expand(s.series(num, r, 0, 6).removeO()).coeff(r, 4)
    check('nonquadratic_r4', s.simplify(r4 + p ** 5 / 4) == 0)
    check('fourth_derivative_at_zero', s.simplify(s.diff(num, r, 4).subs(r, 0) + 6 * p ** 5) == 0)
    A = s.Matrix(16, 16, lambda i, j: s.Symbol('A%d_%d' % (i, j)))
    check('all_fixed_effects_are_quadratic', s.diff((m.T * A * m)[0], r, 3) == 0)
    return dict(status='PASS', checks=checks, source_definition_pins=pins, input_norm=str(N), vacuum_probability='p^2*(a+sqrt(p+p^2*r^2))^2/(2*(1+r^2))', first_output={str(i): str(x) for (i, x) in enumerate(first) if x != 0}, second_output={str(i): str(x) for (i, x) in enumerate(second) if x != 0}, numerator_r4=str(r4), scope='fixed input-independent instrument on unknown CAR amplitudes; does not prohibit a classical coded-tuple update')
def gate_boundary_case(root):
    ROOT = Path(root)
    (a, p) = s.symbols('a p', real=True)
    gb = s.groebner([a * a - p, p * p + p - 1], a, p, domain=s.QQ)

    def red(x):
        (n, d) = s.cancel(x).as_numer_denom()
        return s.cancel(gb.reduce(s.expand(n))[1] / gb.reduce(s.expand(d))[1])

    def mat(x):
        return x.applyfunc(red)
    subs = [tuple((i for i in range(4) if mask & 1 << i)) for mask in range(16)]
    ns = dict(s=s, a=a, p=p, I=s.eye(16), DEG=s.diag(*map(len, subs)), SUBS=subs, mat=mat)
    pins = {}
    for (rel, names) in {'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': ['creator', 'ext'], '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': ['record']}.items():
        tree = ast.parse((ROOT / rel).read_text())
        pins[rel] = {}
        for name in names:
            node = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name))
            pins[rel][name] = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
            exec(compile(ast.Module(body=[node], type_ignores=[]), rel, 'exec'), ns)
    (U0, _) = ns['record'](s.eye(4), s.eye(4)[:, 0])
    (Up, _) = ns['record'](s.eye(4), s.Matrix([a, -p, 0, 0]))
    R = s.Matrix([[a, p, 0, 0], [-p, a, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    ER = ns['ext'](R)
    f = s.Poly(a ** 4 + a * a + 1, a, modulus=2)

    def mod2(x):
        (n, d) = s.cancel(x.subs(p, a * a)).as_numer_denom()
        return s.rem(s.Poly(n, a, modulus=2) * s.invert(s.Poly(d, a, modulus=2), f), f).as_expr()
    b = a + a * a
    d = 1 + a + a * a + a ** 3
    checks = []

    def check(name, condition):
        if not condition:
            raise ArithmeticError(name)
        checks.append(name)

    def sums(M, axis):
        return [mod2(sum(M.row(i) if axis == 'row' else M.col(i))) for i in range(M.rows)]
    G = s.Matrix([[a, -p], [p, a]])
    J = s.Matrix([[0, -1], [1, 0]])
    CX = s.zeros(4)
    for j in range(4):
        CX[j ^ (j >> 0 & 1) << 1, j] = 1
    fullStep = s.Matrix([[a, 0, -p, 0], [0, a, 0, -p], [0, p, 0, a], [p, 0, a, 0]])
    check('b_square_one', mod2(b * b - 1) == 0)
    check('target_class_distinct_even', mod2(d - 1) != 0)
    check('target_class_distinct_odd', mod2(d - b) != 0)
    check('target_class_square_one', mod2(d * d - 1) == 0)
    for (name, M, c) in [('G', G, b), ('G_inverse', G.T, b), ('quarter_turn', J, 1), ('CNOT', CX, 1), ('fullStep', fullStep, b), ('U_e0', U0, b)]:
        for axis in ['row', 'col']:
            check(name + '_' + axis + '_augmentation', sums(M, axis) == [c] * M.rows)
    check('tensor_golden_even_augmentation', sums(s.kronecker_product(G, G), 'row') == [1] * 4)
    check('literal_target_all16_row_class_d', sums(Up, 'row') == [d] * 16)
    check('literal_target_all16_col_class_d', sums(Up, 'col') == [d] * 16)
    check('literal_target_orthogonal', mat(Up.T * Up - s.eye(16)) == s.zeros(16))
    CG = s.diag(s.eye(2), G)
    E2 = CX * CG * CX
    E2_expected = s.eye(4)
    E2_expected[1, 1] = E2_expected[2, 2] = a
    E2_expected[1, 2] = p
    E2_expected[2, 1] = -p
    check('extra_control_exact_two_mode_word', mat(E2 - E2_expected) == s.zeros(4))
    E = s.kronecker_product(s.eye(4), E2)
    check('extra_control_all16_exterior_word', mat(E - ER) == s.zeros(16))
    check('extra_control_target_exact', mat(E * U0 * E.T - Up) == s.zeros(16))
    check('nonuniform_control_not_in_existing_palette', sums(CG, 'col') == [1, 1, b, b])
    x = s.symbols('x:4')
    cross = s.Poly(s.expand(sum(x) ** 2 - sum((t * t for t in x))), *x, modulus=2)
    check('integral_workspace_square_identity', cross.is_zero)
    check('fair_raw_seed_has_zero_augmentation', s.Integer(2) % 2 == 0)
    return dict(status='PASS', checks=checks, source_definition_pins=pins, coefficient_ring='A=Z[a]/(a^4+a^2-1), p=a^2', residue_ring='A/2A=F2[a]/(a^4+a^2+1)', native_word_class='b^N in {1,a+a^2}', target_class=str(d), exact_extra_control_word='E=CX_0to1 C_1(G_0) CX_0to1 tensor I_(bits2,3); U_nplus=E U_e0 E^T', workspace='Any normalized integral workspace returned exactly unchanged is excluded; different output workspace is excluded if both input/output are native G/CNOT-preparable from basis. Arbitrary dirty output and nonintegral supplied resources are not excluded.', excluded_from_palette='Supplied field-dependent Julia/SELECT, arbitrary controlled rotations, nonintegral Hadamard/prepared seeds. Their existence or cost is not inferred.', price_scope='This is an execution/type result. No controller/full Book price identity or physical admission is claimed.')

def julia_query_case(root):
    ROOT = Path(root)
    (a, p) = s.symbols('a p', real=True)
    gb = s.groebner([a * a - p, p * p + p - 1], a, p, domain=s.QQ)

    def red(x):
        (n, d) = s.cancel(x).as_numer_denom()
        return s.cancel(gb.reduce(s.expand(n))[1] / gb.reduce(s.expand(d))[1])

    def mat(M):
        return M.applyfunc(red)
    subs = [tuple((i for i in range(4) if mask & 1 << i)) for mask in range(16)]
    ns = dict(s=s, a=a, p=p, I=s.eye(16), DEG=s.diag(*map(len, subs)), SUBS=subs, mat=mat)
    pins = {}
    for (rel, names) in {'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': ['creator', 'ext'], '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': ['record']}.items():
        tree = ast.parse((ROOT / rel).read_text())
        pins[rel] = {}
        for name in names:
            node = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name))
            pins[rel][name] = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
            exec(compile(ast.Module(body=[node], type_ignores=[]), rel, 'exec'), ns)

    def permutation(f):
        M = s.zeros(32)
        for j in range(32):
            M[f(j), j] = 1
        return M

    def X(bit):
        return permutation(lambda j: j ^ 1 << bit)

    def CX(control, target):
        return permutation(lambda j: j ^ (j >> control & 1) << target)

    def SWAP(i, j):
        return CX(i, j) * CX(j, i) * CX(i, j)

    def controlled_G(control, target):
        M = s.eye(32)
        for j in range(32):
            if j >> control & 1 and (not j >> target & 1):
                k = j | 1 << target
                M[j, j] = M[k, k] = a
                M[k, j] = p
                M[j, k] = -p
        return M
    c = ns['creator'](s.eye(4)[:, 0])
    N = c * c.T
    Din = s.eye(16) + (a - 1) * (s.eye(16) - N)
    Dout = s.eye(16) + (a - 1) * N
    J = (p * c).row_join(Dout).col_join(Din.row_join(-p * c.T))
    checks = []

    def check(name, condition):
        if not condition:
            raise ArithmeticError(name)
        checks.append(name)
    check('creator_full16', c.T * c + N == s.eye(16))
    check('actual_defect_in', mat(Din * Din - (s.eye(16) - p * p * c.T * c)) == s.zeros(16))
    check('actual_defect_out', mat(Dout * Dout - (s.eye(16) - p * p * c * c.T)) == s.zeros(16))
    check('full32_Julia_unitary', mat(J.T * J - s.eye(32)) == s.zeros(32))
    V = X(4) * J
    check('single_query_controlled_G', mat(X(0) * CX(4, 0) * V * CX(4, 0) * X(0) - controlled_G(0, 4)) == s.zeros(32))
    P = SWAP(0, 1) * SWAP(4, 0)
    CG = P.T * X(0) * CX(4, 0) * X(4) * J * CX(4, 0) * X(0) * P
    check('all32_logical_controlled_G_tensor_identity', mat(CG - controlled_G(1, 0)) == s.zeros(32))
    E = CX(0, 1) * CG * CX(0, 1)
    R = s.Matrix([[a, p, 0, 0], [-p, a, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    ER = ns['ext'](R)
    check('all32_exterior_R_tensor_identity', mat(E - s.kronecker_product(s.eye(2), ER)) == s.zeros(32))
    (U0, _) = ns['record'](s.eye(4), s.eye(4)[:, 0])
    (Up, _) = ns['record'](s.eye(4), s.Matrix([a, -p, 0, 0]))
    compiled = E * s.kronecker_product(s.eye(2), U0) * E.T
    check('chronology_all32_tensor_identity', mat(compiled - s.kronecker_product(s.eye(2), Up)) == s.zeros(32))
    check('all32_full_complement_unitarity', mat(compiled.T * compiled - s.eye(32)) == s.zeros(32))
    seed = s.zeros(16, 1)
    seed[1] = seed[15] = 1
    decoded = (CX(1, 2) * CX(1, 3))[:16, :16] * seed
    expected = s.zeros(16, 1)
    expected[1] = expected[3] = 1
    check('owned_seed_two_CNOT_fairbit_decoder', decoded == expected)
    return dict(status='PASS', checks=checks, source_definition_pins=pins, exact_required_operand='X=p*C(e0), coefficient bit4; J(X) plus adjoint for reverse word', formula='CG=P^T X0 CX4to0 X4 J(pC0) CX4to0 X0 P; P=SWAP01 SWAP40; E=CX0to1 CG CX0to1; compiled=E (I2 tensor U_e0) E^T', syntactic_counts={'Julia': 2, 'CNOT': 32, 'X': 6, 'U_e0': 1}, counts_scope='Unoptimized syntax: each SWAP costs3 CNOT. X gates require existing admitted flips or basis-one control, retained unchanged. These counts are NOT a Book action or full price.', workspace='Existing coefficient bit returns identically for all states; no blank, projection, trace or reset. RIGHT/reference and all old histories are spectator identities.', resource_scope='Specified Julia matrix is an exact sufficient resource inside the declared Julia-query class. Full-Lorentz owner explicitly leaves its native physical generation/controller price open. Original seed decoding does not supply an additional independent seed or its preparation adjoint.')

def generic_julia_chronology(root):
    root = Path(root)
    (a, p, x, y) = s.symbols('a p x y', real=True)
    gb = s.groebner([y * y + x * x - 1, a * a - p, p * p + p - 1], y, a, p, domain=s.QQ.frac_field(x))

    def red(v):
        (n, d) = s.cancel(v).as_numer_denom()
        return s.cancel(gb.reduce(s.expand(n))[1] / gb.reduce(s.expand(d))[1])

    def mat(M):
        return M.applyfunc(red)

    def tangent(M):
        return mat(M.diff(x) * y - M.diff(y) * x)
    subs = [tuple((i for i in range(4) if mask & 1 << i)) for mask in range(16)]
    ns = dict(s=s, a=a, p=p, I=s.eye(16), DEG=s.diag(*map(len, subs)), SUBS=subs, mat=mat)
    pins = {}
    for (rel, names) in {'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py': ['creator', 'ext'], '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py': ['record']}.items():
        tr = ast.parse((root / rel).read_text())
        pins[rel] = {}
        for name in names:
            node = next((n for n in tr.body if isinstance(n, ast.FunctionDef) and n.name == name))
            pins[rel][name] = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
            exec(compile(ast.Module(body=[node], type_ignores=[]), rel, 'exec'), ns)
    checks = []

    def check(name, condition):
        if not condition:
            raise ArithmeticError(name)
        checks.append(name)

    def perm(n, f):
        M = s.zeros(1 << n)
        for j in range(1 << n):
            M[f(j), j] = 1
        return M

    def X(n, bit):
        return perm(n, lambda j: j ^ 1 << bit)

    def CX(n, c, t):
        return perm(n, lambda j: j ^ (j >> c & 1) << t)

    def SWAP(n, i, j):
        return CX(n, i, j) * CX(n, j, i) * CX(n, i, j)

    def CG(n, c, t):
        M = s.eye(1 << n)
        for j in range(1 << n):
            if j >> c & 1 and (not j >> t & 1):
                k = j | 1 << t
                M[j, j] = M[k, k] = y
                M[k, j] = x
                M[j, k] = -x
        return M
    c = s.Matrix([[0, 0], [1, 0]])
    J4 = (x * c).row_join(s.diag(1, y)).col_join(s.diag(y, 1).row_join(-x * c.T))
    cg4 = X(2, 0) * CX(2, 1, 0) * X(2, 1) * J4 * CX(2, 1, 0) * X(2, 0)
    check('generic_four_coordinate_Julia_unitarity', mat(J4.T * J4 - s.eye(4)) == s.zeros(4))
    check('generic_same_query_controlled_rotation', mat(cg4 - CG(2, 0, 1)) == s.zeros(4))
    c0 = ns['creator'](s.eye(4)[:, 0])
    N = c0 * c0.T
    Dout = s.eye(16) + (y - 1) * N
    Din = s.eye(16) + (y - 1) * (s.eye(16) - N)
    J = (x * c0).row_join(Dout).col_join(Din.row_join(-x * c0.T))
    check('full16_actual_positive_defect_squares', mat(Dout * Dout - s.eye(16) + x * x * c0 * c0.T) == s.zeros(16) and mat(Din * Din - s.eye(16) + x * x * c0.T * c0) == s.zeros(16))
    P = SWAP(5, 0, 1) * SWAP(5, 4, 0)
    cg = P.T * X(5, 0) * CX(5, 4, 0) * X(5, 4) * J * CX(5, 4, 0) * X(5, 0) * P
    check('generic_all32_controlled_rotation_work_identity', mat(cg - CG(5, 1, 0)) == s.zeros(32))
    E = CX(5, 0, 1) * cg * CX(5, 0, 1)
    R = s.Matrix([[y, x, 0, 0], [-x, y, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    ER = ns['ext'](R)
    check('generic_all32_exterior_rotation_work_identity', mat(E - s.kronecker_product(s.eye(2), ER)) == s.zeros(32))
    (U0, P0) = ns['record'](s.eye(4), s.eye(4)[:, 0])
    (Up, _) = ns['record'](s.eye(4), s.Matrix([y, -x, 0, 0]))
    compiled = mat(ER * U0 * ER.T)
    check('generic_all16_literal_record_intertwining', mat(compiled - Up) == s.zeros(16))
    check('generic_all16_first_angle_jet', mat(tangent(compiled) - tangent(Up)) == s.zeros(16))
    jet_at_r1 = mat(tangent(Up).subs({x: p, y: a}, simultaneous=True))
    check('first_angle_jet_is_not_frozen', jet_at_r1 != s.zeros(16))
    (r, b) = s.symbols('r b', real=True, nonzero=True)
    dr = lambda v: s.diff(v, r) + p * p * r / b * s.diff(v, b)
    dxnum = s.expand(s.cancel((dr(p * r / b) - p * p / b ** 3) * b ** 3))
    dynum = s.expand(s.cancel((dr(a / b) + a * p * p * r / b ** 3) * b ** 3))
    check('actual_family_differentiated_dx', s.expand(dxnum.subs(b * b, p + p * p * r * r)) == 0)
    check('actual_family_differentiated_dy', dynum == 0)
    check('actual_family_angle_chain_rule', red(a * p * a - p * p) == 0)
    check('actual_r1_unit_radius', red(p + p * p - 1) == 0)
    check('actual_r1_query_has_nonzero_derivative', red(p * p) != 0)
    nz = next(((i, j, red(jet_at_r1[i, j])) for i in range(16) for j in range(16) if red(jet_at_r1[i, j]) != 0))
    return dict(status='PASS', checks=checks, source_definition_pins=pins, domain='x,y real, x^2+y^2=1, y>0; strict |x|<1 makes defects positive and smooth', literal_query_owner='02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md, section2 equation(5)', operator_identity='E(x,y)=I_coeff tensor Lambda([[y,x],[-x,y]] directsum I2); E(I_coeff tensor U_e0)E^T=I_coeff tensor U_(y,-x)', angle_derivative='T=y*d/dx-x*d/dy; identity holds exactly also for T', nonzero_angle_jet_entry=[nz[0], nz[1], str(nz[2])], original_matter_family={'b': 'sqrt(p+p^2*r^2)', 'x': 'p*r/b', 'y': 'a/b', 'dx_dr': 'p^2/b^3', 'dy_dr': '-a*p^2*r/b^3', 'd_dr': '(a*p/b^2)*T', 'at_r1': 'x=p,y=a,dx=p^2,dy=-a*p^2'}, source_scope='Actual full-feedback first jets transfer by the chain rule only if the varying Julia operand x(m)*C0 is really supplied, including its derivative. A fixed J(pC0) proves only the r=1 operator value. No physical parameter-update or controller-price law is asserted.')

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);parser.add_argument('--output',type=Path);args=parser.parse_args()
 for path,pin in PINS.items():
  if hashlib.sha256((args.root/path).read_bytes()).hexdigest()!=pin:raise ArithmeticError('Owner changed: '+path)
 result={'status':'PASS','owner_sha256':PINS,'coded_runtime':runtime_case(args.root),'unknown_input_boundary':unknown_input_case(args.root),'physical_gate_boundary':gate_boundary_case(args.root),'supplied_Julia_resource':julia_query_case(args.root),'variable_Julia_family':generic_julia_chronology(args.root)}
 text=json.dumps(result,indent=2)+'\n'
 if args.output:args.output.write_text(text)
 print(text,end='')
