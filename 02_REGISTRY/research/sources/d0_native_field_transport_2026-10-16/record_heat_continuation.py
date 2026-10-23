"""Actual v8 record-heat: occupied-shell continuation on full CAR blocks.

The local conformal family differentiates the LITERAL v8 coefficient map,
d(t)=exp(t*phi/2)d0, D(t)=exp(t*phi/2)d0+d0*exp(t*phi/2).  It does not
substitute the separate variable-weight Hodge completion for that program.
Only pinned native creator/basis definitions are consumed, with v8 RESULT
and immutable receipt as documentary inputs.  No old checker is executed.

The exact rational F fixture is NOT the certified stationary root.  Universal
root-window statements below are conditional on the existing v8 root/gap.
All16 grades and all128 occupied-shell/reference components remain.  Matter
second response uses small Fourier blocks; heat/feedback still sum ALL modes.
"""
from __future__ import annotations

import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
JOINT = "02_REGISTRY/research/certificates/a4d_native_joint_adjoint_source.py"
CURVED = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
V8 = "02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/"
PINS = {
    JOINT: "71ba142e284974db57d67c91a77ccd08a7e4f9759e8fc8daef7c5938774c0b28",
    CURVED: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
    V8+"RESULT.md": "f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c",
    V8+"receipt.json": "da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9",
}
ETA = s.diag(1, -1, -1, -1)
SHELL = tuple(tuple(sign if j == r else 0 for j in range(4))
              for r in range(4) for sign in (1, 7))
FOURIER_Q = (3, 3, 0, 0)
SHELL_RANK = 128


def require(condition, name):
    if not bool(condition):
        raise AssertionError(name)


def _definitions(repo):
    for path, digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                "source_pin:"+path)
    # Extract only the actual native creators and the ACDB/ABCD sign bridge.
    tree = ast.parse((repo/CURVED).read_text())
    selected = []
    for node in tree.body:
        if (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name)
                and t.id in {"EXTERIOR_ORDER", "JW_ORDER"} for t in node.targets)):
            selected.append(node)
        if isinstance(node, ast.FunctionDef) and node.name in {"creator", "basis_phase"}:
            selected.append(node)
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=selected, type_ignores=[]), CURVED, "exec"), scope)
    joint_tree = ast.parse((repo/JOINT).read_text())
    creator = [node for node in joint_tree.body
               if isinstance(node, ast.FunctionDef) and node.name == "creator"]
    require(len(creator) == 1, "actual_joint_creator_definition_present")
    joint_scope = {"s": s, "P": SimpleNamespace(creator=scope["creator"])}
    exec(compile(ast.Module(body=creator, type_ignores=[]), JOINT, "exec"), joint_scope)
    return scope, joint_scope["creator"]


def _reduce(value):
    """Exact Q(sqrt(2),i) entries; no numerical tolerance."""
    return s.expand(value)


def _matrix(value):
    return value.applyfunc(_reduce)


def _zero(value):
    if isinstance(value, s.MatrixBase):
        return all(_zero(x) for x in value)
    expanded = _reduce(value)
    return expanded == 0 or s.cancel(expanded) == 0


def add_mode(k, q, sign=1):
    return tuple((a+sign*b) % 8 for a, b in zip(k, q))


def lattice_z8(k):
    """Literal L8 lattice Fourier phase, not an eigenstate catalogue."""
    r = s.sqrt(2)/2
    roots = (1, r*(1+s.I), s.I, r*(-1+s.I), -1,
             r*(-1-s.I), -s.I, r*(1-s.I))
    return s.Matrix([8*(roots[j % 8]-1) for j in k])


def shell_metric_family(a, b):
    """Exact homogeneous positive factor used by the continuation chart.

    a>b>=0 implies F=(a-b)I+b11^T>0; d=a^2+3b^2, o=2ab+2b^2.
    G=F F^T=(d-o)I+o11^T, q=F eta F^T, h_coord=G^-1.
    These are kinematic identities, not a selected physical observer law.
    """
    F = (a-b)*s.eye(4)+b*s.ones(4)
    G = F*F.T
    return F, _matrix(G), _matrix(F*ETA*F.T)


def mode_blocks(creators, G, k):
    z = lattice_z8(k)
    d = _matrix(sum((z[r]*creators[r] for r in range(4)), s.zeros(16)))
    D = _matrix(d+d.H)
    energy = _reduce((z.H*G*z)[0])
    return {"d": d, "D": D, "energy": energy, "z": z}


def conformal_first_block(left, right, q=FOURIER_Q):
    """D'(0) from exp(t*cos(q.x)/2), with the literal coefficient order."""
    if left["mode"] not in (add_mode(right["mode"], q), add_mode(right["mode"], q, -1)):
        return s.zeros(16)
    return _matrix((right["d"]+left["d"].H)/4)


def conformal_second_block(left, right, q=FOURIER_Q):
    """D''(0): Fourier(phi^2)/4 times (d_right+d_left^*)."""
    lk, rk = left["mode"], right["mode"]
    if lk == rk:
        factor = s.Rational(1, 8)
    elif lk in (add_mode(rk, q, 2), add_mode(rk, q, -2)):
        factor = s.Rational(1, 16)
    else:
        factor = s.S.Zero
    return _matrix(factor*(right["d"]+left["d"].H))


def actual_shell_response(creators, G, q=FOURIER_Q):
    """All full16 blocks for the occupied-shell first/second response.

    R=(Delta-epsilon)^-1 on the off-shell subspace.  Each denominator is
    supplied by the ACTUAL homogeneous symbol.  No preparation weights are
    chosen: the initial P/128 purification is exactly the v8 preparation.
    Its shell/reference kernel tangents remain free, not projected away.
    """
    modes = set(SHELL)
    for k in SHELL:
        modes.update((add_mode(k, q), add_mode(k, q, -1)))
    data = {}
    for k in sorted(modes):
        data[k] = dict(mode_blocks(creators, G, k), mode=k)
    epsilon = data[SHELL[0]]["energy"]
    D1, X, eta, Y, E2 = {}, {}, {}, {}, {}
    schur_trace = s.S.Zero
    eta_norm_squared = s.S.Zero
    for k in SHELL:
        products = s.zeros(16)
        schur = s.zeros(16)
        for sign in (1, -1):
            l = add_mode(k, q, sign)
            A = conformal_first_block(data[l], data[k], q)
            D1[l, k], D1[k, l] = A, A.H
            B = _matrix(data[l]["D"]*A+A*data[k]["D"])
            X[l, k], X[k, l] = B, B.H
            gap = _reduce(data[l]["energy"]-epsilon)
            eta[l, k] = -B/(s.sqrt(SHELL_RANK)*gap)
            products += A.H*A
            gram = _matrix(B.H*B)
            schur += gram/gap
            schur_trace += s.trace(gram)/gap
            eta_norm_squared += s.trace(gram)/(SHELL_RANK*gap**2)
        D2 = conformal_second_block(data[k], data[k], q)
        Y[k] = _matrix(data[k]["D"]*D2+D2*data[k]["D"]+2*products)
        E2[k] = _matrix(Y[k]-2*schur)
    return {"modes": data, "epsilon": epsilon, "D1": D1, "X": X,
            "eta": eta, "Y_shell": Y, "E2_shell": E2,
            "schur_trace": schur_trace, "eta_norm_squared": eta_norm_squared,
            "matter_relaxation_second_source": -2*schur_trace/SHELL_RANK,
            "matter_second_source": sum(s.trace(M) for M in E2.values())/SHELL_RANK}


def trace_off_shell_square(epsilon, energy, inner_product):
    """Full16 CAR trace Tr(X_lk^* X_lk), with the ACTUAL 1/4 D1 coefficient."""
    return (epsilon**2+energy**2)/2+2*epsilon*energy+inner_product*s.conjugate(inner_product)


def occupied_second_trace(G, k, q=FOURIER_Q):
    """Exact full16 trace of the effective occupied second operator E2_k.

    Uses CAR trace identities, not an averaged replacement of the matrix
    matter equation.  Different traces already obstruct a common scalar E2.
    """
    zk = lattice_z8(k)
    epsilon = _reduce((zk.H*G*zk)[0])
    result = 6*epsilon
    for sign in (1, -1):
        zl = lattice_z8(add_mode(k, q, sign))
        energy = _reduce((zl.H*G*zl)[0])
        inner = _reduce((zl.H*G*zk)[0])
        result += energy-2*trace_off_shell_square(epsilon, energy, inner)/(energy-epsilon)
    return result


def occupied_trace_contrast(d, o):
    """Exact e0 minus e2 E2 trace contrast, strictly NEGATIVE for d>o>0."""
    rt2 = s.sqrt(2)
    polynomial = (14+rt2)*d**2+(2+2*rt2)*d*o-(8+7*rt2)*o**2
    return -64*(d+3*o)*polynomial/((d+o)*((7+5*rt2)*d+(11+8*rt2)*o))


def occupied_vacuum_second_defect(G, k=(1, 0, 0, 0), q=FOURIER_Q):
    """Vacuum entry minus full16 mean of E2, from exact CAR traces.

    At the actual d/o root and k=e0 it is 8sqrt(2)(d-o)>0.  This is
    nonscalar within one occupied Fock block, not merely between momenta.
    """
    zk = lattice_z8(k)
    epsilon = _reduce((zk.H*G*zk)[0])
    defect = s.S.Zero
    for sign in (1, -1):
        zl = lattice_z8(add_mode(k, q, sign))
        energy = _reduce((zl.H*G*zl)[0])
        inner = _reduce((zl.H*G*zk)[0])
        defect += (epsilon*energy-inner*s.conjugate(inner))/(4*(energy-epsilon))
    return defect


def program_gradient(eigenvalue, alpha, rounds, reference, fugacity, full_Z):
    """Actual H+J_program coefficient; Z contains ALL data/Fock modes."""
    b = 1-alpha*eigenvalue
    return (-b**(2*rounds-1)/full_Z
            +reference*(2*rounds*alpha)*fugacity*b**(2*rounds-1)
            /(1-fugacity+fugacity*b**(2*rounds)))


def full_second_source(eigenvalues, X, Y_diagonal, shell_schur_trace,
                       alpha, rounds, reference, fugacity, full_Z):
    """Exact complete S'' on this nonzero Fourier jet (delta Z=0).

    Caller MUST supply every 8^4 momentum and every diagonal Y block.  This
    routine intentionally does not accept just the occupied-shell data as a
    full thermal carrier. X contains all directed nonzero Fourier blocks.
    No old4096-mode calculation is run by the focused consumer.
    """
    if len(eigenvalues) != 8**4 or set(Y_diagonal) != set(eigenvalues):
        raise ValueError("complete_4096_mode_heat_and_feedback_carrier_required")
    if any(k == l and not _zero(M) for (k, l), M in X.items()):
        raise ValueError("this_formula_requires_zero_diagonal_first_Fourier_jet")
    variable = s.Symbol("actual_Delta_eigenvalue", real=True)
    kappa = program_gradient(variable, alpha, rounds, reference, fugacity, full_Z)
    response = s.S.Zero
    for k, energy in eigenvalues.items():
        coefficient = kappa.subs(variable, energy)+(s.Rational(1, SHELL_RANK) if k in SHELL else 0)
        response += coefficient*s.trace(Y_diagonal[k])
    for (k, l), block in X.items():
        if (l, k) not in X:
            raise ValueError("both_Hermitian_Fourier_directions_required")
        gap = _reduce(eigenvalues[k]-eigenvalues[l])
        divided = (s.diff(kappa, variable).subs(variable, eigenvalues[k]) if gap == 0
                   else (kappa.subs(variable, eigenvalues[k])-kappa.subs(variable, eigenvalues[l]))/gap)
        response += divided*s.trace(block*X[l, k])
    return response-2*shell_schur_trace/SHELL_RANK


def signed_survival_checks(repo):
    """Four exact algebraic LEFT-fixture groups, not a physical native gate.

    The algebraic unitary fixture is not a test of the separate v8 positive
    survival lower bound. No CAR grade cut, admission rule, old checker or receipt is
    introduced.  The only repository definition consumed is the SHA-pinned
    actual AF counts/segments inclusion.  All four gate copies and all
    M2+M1 -> M3+M2 complements/multiplicities remain in the calculation.
    """
    import ast
    import hashlib
    from pathlib import Path
    import sympy as s

    repo = Path(repo).resolve()
    checks = []

    def zero(value):
        values = list(value) if isinstance(value, s.MatrixBase) else [value]
        return all(s.simplify(item) == 0 for item in values)

    def require(condition, label):
        if not bool(condition):
            raise ArithmeticError("signed_survival:"+label)

    def gate(R, S):
        Z = s.zeros(R.rows)
        return s.BlockMatrix([[R, Z, -S, Z], [Z, R, Z, -S],
                              [Z, S, Z, R], [S, Z, R, Z]]).as_explicit()

    alpha = s.Rational(1, 4)
    root_alpha = s.Rational(1, 2)
    I = s.eye(2)

    # Signed S, including a NEGATIVE spectral branch.  Full four-copy gate;
    # no terminal success sector or complement is dropped.
    D = s.diag(-1, 2)
    C = s.diag(s.sqrt(7)/2, 1)
    R = I-alpha*D**2
    S = root_alpha*D*C
    U = gate(R, S)
    preparation = s.Matrix.vstack(I, s.zeros(6, 2))
    P = s.diag(1, 1, 1, 1, 0, 0, 0, 0)
    retained, leaked = P*U*preparation, (s.eye(8)-P)*U*preparation
    require(all((zero(C*C-(2*I-alpha*D**2)), zero(S*S-(I-R*R)),
                 zero(U.H*U-s.eye(8)), zero(U*U.H-s.eye(8)),
                 zero(preparation.H*U*preparation-R),
                 zero(retained.H*retained-R*R), zero(leaked.H*leaked-S*S),
                 S[0, 0] < 0)),
            "full4copy_unitarity_signed_survival_and_complete_complement")
    checks.append("signed_survival:full4copy_unitarity_signed_survival_and_complete_complement")

    # Around D=0, signed S(t) is analytic with nonzero first derivative.
    # The positive sqrt(E(t)) has the |t| cusp and is not the same germ.
    t = s.Symbol("signed_D_crossing", real=True)
    signed = root_alpha*t*s.sqrt(2-alpha*t*t)
    unsigned = root_alpha*s.Abs(t)*s.sqrt(2-alpha*t*t)
    right = s.limit(unsigned/t, t, 0, dir="+")
    left = s.limit(unsigned/t, t, 0, dir="-")
    require(all((zero(s.diff(signed, t).subs(t, 0)-s.sqrt(2)/2),
                 zero(right-s.sqrt(2)/2), zero(left+s.sqrt(2)/2),
                 right != left, zero(signed**2-unsigned**2),
                 zero(signed.subs(t, -1)+s.sqrt(7)/4))),
            "zero_D_signed_analytic_jet_not_unsigned_absolute_value_cusp")
    checks.append("signed_survival:zero_D_signed_analytic_jet_not_unsigned_absolute_value_cusp")

    # Actual noncommuting Hermitian jet at diag(0,d), d=2.  The positive
    # root derivative is the Sylvester solution, not one-sided division.
    D0, dD = s.diag(0, 2), s.Matrix([[0, 1], [1, 0]])
    C0 = s.diag(s.sqrt(2), 1)
    dQ = -alpha*(D0*dD+dD*D0)
    dC = s.Matrix(2, 2, lambda i, j: dQ[i, j]/(C0[i, i]+C0[j, j]))
    R0, S0 = I-alpha*D0**2, root_alpha*D0*C0
    dR, dS = dQ, root_alpha*(dD*C0+D0*dC)
    naive = C0.inv()*dQ/2
    require(all((not zero(D0*dD-dD*D0), zero(C0*dC+dC*C0-dQ),
                 zero(dC-dC.H), not zero(C0*naive+naive*C0-dQ),
                 zero(dS-dD/2), zero(dS-dS.H),
                 zero(R0*dR+dR*R0+S0*dS+dS*S0))),
            "noncommuting_Sylvester_root_and_signed_gate_tangent")
    checks.append("signed_survival:noncommuting_Sylvester_root_and_signed_gate_tangent")

    # Import ONLY two pure definitions of the ACTUAL AF inclusion, not its
    # module/certificate entrypoint.  alphaD^2<2 gives all positive roots.
    relative = "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py"
    source = (repo/relative).read_bytes()
    require(hashlib.sha256(source).hexdigest() ==
            "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
            "actual_AF_inclusion_definition_pin")
    tree = ast.parse(source)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in {"counts", "segments"}]
    require(len(nodes) == 2, "actual_AF_inclusion_definitions_present")
    scope = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), relative, "exec"), scope)
    counts, segments = scope["counts"], scope["segments"]
    paths = segments(2, 1, 1)

    def inclusion(blocks):
        result = []
        for size, rows in zip(counts(2), paths):
            block = s.zeros(size)
            for kind, _path, offset in rows:
                original = blocks[kind]
                block[offset:offset+original.rows, offset:offset+original.cols] = original
            result.append(block)
        return tuple(result)

    O = s.Matrix([[3, -4], [4, 3]])/5
    DA, DB = O*D*O.T, s.Matrix([[s.Rational(1, 2)]])
    CA, CB = O*C*O.T, s.Matrix([[s.sqrt(31)/4]])
    oldD, oldC = (DA, DB), (CA, CB)
    oldR = tuple(s.eye(M.rows)-alpha*M**2 for M in oldD)
    oldS = tuple(root_alpha*M*N for M, N in zip(oldD, oldC))
    fineD, fineC = inclusion(oldD), inclusion(oldC)
    fineR = tuple(s.eye(M.rows)-alpha*M**2 for M in fineD)
    fineS = tuple(root_alpha*M*N for M, N in zip(fineD, fineC))

    # Independently construct the fine positive root in its exact rational
    # spectral fixture; this includes the M1 complement in M3 and repeated M2.
    O3 = s.diag(O, 1)
    directC = (O3*s.diag(s.sqrt(7)/2, 1, s.sqrt(31)/4)*O3.T, CA)
    old_gates = tuple(gate(A, B) for A, B in zip(oldR, oldS))
    amplified = [s.zeros(12), s.zeros(8)]
    for i in range(4):
        for j in range(4):
            old_entries = (old_gates[0][2*i:2*i+2, 2*j:2*j+2],
                           old_gates[1][i:i+1, j:j+1])
            for target, entry in enumerate(inclusion(old_entries)):
                size = entry.rows
                amplified[target][size*i:size*(i+1), size*j:size*(j+1)] = entry
    require(all((counts(1) == (2, 1), counts(2) == (3, 2),
                 paths == [[(0, (0,), 0), (1, (0,), 2)], [(0, (1,), 0)]],
                 all(zero(A-B) for A, B in zip(directC, fineC)),
                 all(zero(A-B) for A, B in zip(inclusion(oldR), fineR)),
                 all(zero(A-B) for A, B in zip(inclusion(oldS), fineS)),
                 all(zero(N*N-(2*s.eye(M.rows)-alpha*M*M))
                     for M, N in zip(fineD, directC)),
                 all(zero(A-gate(B, Cc))
                     for A, B, Cc in zip(amplified, fineR, fineS)),
                 all(zero(A.H*A-s.eye(A.rows)) for A in amplified))),
            "actual_AF_star_inclusion_functional_naturality_all_complements")
    checks.append("signed_survival:actual_AF_star_inclusion_functional_naturality_all_complements")
    return checks


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    basis, native_creator = _definitions(repo)
    checks = ["source_pin:"+path for path in PINS]

    def eq(actual, expected, name):
        require(_zero(actual-expected), name)
        checks.append(name)

    def yes(condition, name):
        require(condition, name)
        checks.append(name)

    receipt = json.loads((repo/(V8+"receipt.json")).read_text())
    yes(receipt["interval"]["Fock_dimension"] == 16
        and receipt["interval"]["purifying_reference_dimension"] == 128
        and receipt["interval"]["rounds"] == 8192,
        "documentary_v8_full_Fock_reference_and_round_count")
    phase = basis["basis_phase"]()
    eq(phase*phase, s.eye(16), "actual_native_ACDB_to_ABCD_sign_bridge")
    creators = []
    for r in range(4):
        actual = phase*native_creator(s.eye(4)[:, r])*phase
        expected = basis["creator"](r, basis["JW_ORDER"])
        eq(actual, expected, "native_creator_sign_transport_"+str(r))
        creators.append(actual)
    for r in range(4):
        for t in range(4):
            eq(creators[r]*creators[t]+creators[t]*creators[r], s.zeros(16),
               "all_grade_creation_anticommutator_"+str((r, t)))
            eq(creators[r].H*creators[t]+creators[t]*creators[r].H,
               int(r == t)*s.eye(16), "all_grade_CAR_"+str((r, t)))

    # Generic homogeneous bridge; no preferred physical frame is selected.
    a, b = s.symbols("positive_diagonal_factor positive_offdiagonal_factor", real=True)
    F, G, qnative = shell_metric_family(a, b)
    Finv = s.eye(4)/(a-b)-b*s.ones(4)/((a-b)*(a+3*b))
    require(all(s.cancel(x) == 0 for x in F*Finv-s.eye(4)), "generic_exact_inverse_frame")
    checks.append("generic_exact_inverse_frame")
    eq(G, (a*a+3*b*b-(2*a*b+2*b*b))*s.eye(4)+(2*a*b+2*b*b)*s.ones(4),
       "generic_FFtranspose_is_actual_d_o_metric")
    J = F*s.eye(4)[:, 0]
    g = Finv.T*ETA*Finv
    h = Finv.T*Finv
    require(all(s.cancel(x) == 0 for x in qnative*g-s.eye(4)), "native_q_inverse_retained")
    checks.append("native_q_inverse_retained")
    require(all(s.cancel(x) == 0 for x in h*G-s.eye(4)), "positive_coordinate_pairing_is_G_inverse")
    checks.append("positive_coordinate_pairing_is_G_inverse")
    require(all(s.cancel(x) == 0 for x in -g+2*(g*J)*(g*J).T-h), "same_frame_observer_reflection")
    checks.append("same_frame_observer_reflection")

    # Explicit rational near-root control, never labelled a stationary root.
    F0, G0, _q0 = shell_metric_family(s.Rational(1, 4), s.Rational(1, 125))
    d0, o0 = G0[0, 0], G0[0, 1]
    yes(0 < o0 < d0 and d0+3*o0 < 1, "rational_control_positive_and_inside_v8_coefficient_domain")
    eq(d0, s.Rational(15673, 250000), "rational_control_diagonal_NOT_v8_root")
    eq(o0, s.Rational(129, 31250), "rational_control_offdiagonal_NOT_v8_root")
    # Stored native legs are eta*F_r^T.  The full exterior eta conjugation,
    # together with the OWNED basis phase, sends these to the literal v8
    # positive creators with Gram F F^T.  No Fock grades are removed.
    eta_exterior = s.diag(*[(-1)**bin(mask & 14).count("1") for mask in range(16)])
    full_bridge = phase*eta_exterior
    eq(full_bridge*full_bridge.H, s.eye(16), "full_native_eta_leg_and_basis_bridge_is_unitary")
    c = tuple(_matrix(full_bridge*native_creator(ETA*F0.row(r).T)*full_bridge.H)
              for r in range(4))
    for r in range(4):
        eq(c[r], sum((F0[r, j]*creators[j] for j in range(4)), s.zeros(16)),
           "actual_stored_native_leg_to_v8_coefficient_"+str(r))
    for r in range(4):
        for t in range(4):
            eq(c[r].H*c[t]+c[t]*c[r].H, G0[r, t]*s.eye(16),
               "literal_positive_coefficient_CAR_"+str((r, t)))
    # Every symmetric metric direction has a raw homogeneous frame lift.
    for r in range(4):
        for t in range(r, 4):
            V = s.zeros(4)
            V[r, t] = V[t, r] = 1
            dF = V*F0.inv().T/2
            eq(dF*F0.T+F0*dF.T, V, "all_ten_metric_slot_frame_lifts_"+str((r, t)))

    difference_set = {tuple((a-b) % 8 for a, b in zip(k, l)) for k in SHELL for l in SHELL}
    yes(FOURIER_Q not in difference_set and add_mode((0,)*4, FOURIER_Q, 2) not in difference_set,
        "actual_nonresonant_first_and_second_Fourier_frequency")
    response = actual_shell_response(c, G0)
    data, epsilon = response["modes"], response["epsilon"]
    yes(len(SHELL) == 8 and SHELL_RANK == 8*16, "entire_first_shell_and_full_reference_rank128")
    yes(len({data[k]["energy"] for k in SHELL}) == 1, "all128_occupied_states_share_same_base_eigenvalue")
    for k, mode in data.items():
        eq(mode["D"]**2, mode["energy"]*s.eye(16), "literal_Dirac_square_full16_"+str(k))
    for k in SHELL:
        for sign in (1, -1):
            l = add_mode(k, FOURIER_Q, sign)
            yes(l not in SHELL, "first_metric_jet_has_no_occupied_shell_block_"+str((k, sign)))
            gap = _reduce(data[l]["energy"]-epsilon)
            # Q(sqrt2) sign: a rational lower estimate follows from sqrt2 in(1,3/2).
            lower = min(s.expand(gap).subs(s.sqrt(2), 1), s.expand(gap).subs(s.sqrt(2), s.Rational(3, 2)))
            yes(lower > s.Rational(1, 2), "actual_connected_off_shell_gap_"+str((k, sign)))
            eta = response["eta"][l, k]
            eq(gap*eta+response["X"][l, k]/s.sqrt(SHELL_RANK), s.zeros(16),
               "full128_reference_off_shell_matter_equation_"+str((k, sign)))
            eq(conformal_first_block(data[k], data[l]), response["D1"][l, k].H,
               "literal_first_coefficient_jet_Hermitian_"+str((k, sign)))
        eq(response["Y_shell"][k], epsilon*s.eye(16)/4+2*sum(
            (response["D1"][l, k].H*response["D1"][l, k]
             for l in (add_mode(k, FOURIER_Q), add_mode(k, FOURIER_Q, -1))), s.zeros(16)),
           "actual_second_operator_jet_retains_Dsecond_and_Dfirst_squared_"+str(k))
        for sign in (1, -1):
            l = add_mode(k, FOURIER_Q, sign)
            inner = _reduce((data[l]["z"].H*G0*data[k]["z"])[0])
            eq(s.trace(response["X"][l, k].H*response["X"][l, k]),
               trace_off_shell_square(epsilon, data[l]["energy"], inner),
               "independent_full16_CAR_trace_off_shell_square_"+str((k, sign)))
        eq(s.trace(response["E2_shell"][k]), occupied_second_trace(G0, k),
           "independent_full16_effective_second_trace_"+str(k))

    # A root-window theorem, not an extrapolation from the rational control:
    # the exact homogeneous expression has a strictly negative contrast
    # throughout d>o>0, so this PRESCRIBED curve fails second compatibility.
    d, o = s.symbols("root_metric_diagonal root_metric_offdiagonal", real=True)
    generic_G = (d-o)*s.eye(4)+o*s.ones(4)
    eq(occupied_second_trace(generic_G, (1, 0, 0, 0))
       -occupied_second_trace(generic_G, (0, 0, 1, 0)), occupied_trace_contrast(d, o),
       "actual_root_uniform_occupied_trace_contrast_closed_formula")
    rt2 = s.sqrt(2)
    Pcontrast = (14+rt2)*d**2+(2+2*rt2)*d*o-(8+7*rt2)*o**2
    eq(Pcontrast, (d-o)*((14+rt2)*d+(16+3*rt2)*o)+(8-4*rt2)*o**2,
       "root_uniform_trace_contrast_polynomial_positive_decomposition")
    yes(8-4*rt2 > 0, "root_uniform_trace_contrast_strict_sign_coefficient")
    e0_response = response["E2_shell"][(1, 0, 0, 0)]
    eq(e0_response[0, 0]-s.trace(e0_response)/16,
       occupied_vacuum_second_defect(G0),
       "independent_full16_CAR_vacuum_second_defect")
    eq(occupied_vacuum_second_defect(generic_G), 8*s.sqrt(2)*(d-o),
       "actual_root_uniform_nonscalar_defect_8sqrt2_times_d_minus_o")
    rational_contrast = occupied_trace_contrast(d0, o0)
    yes(s.simplify(rational_contrast) < 0,
        "rational_nonroot_control_also_has_distinct_occupied_second_traces")
    e0_effective = response["E2_shell"][(1, 0, 0, 0)]
    scalar_defect = e0_effective-s.trace(e0_effective)*s.eye(16)/16
    nonscalar_entry = next(((i, j) for i in range(16) for j in range(16)
                            if not _zero(scalar_defect[i, j])), None)

    # Independent literal exponential coefficient derivatives, no frozen jets.
    t, phi = s.symbols("actual_conformal_parameter actual_site_cosine", real=True)
    coefficient = s.exp(t*phi/2)
    eq(s.diff(coefficient, t).subs(t, 0), phi/2, "literal_local_coefficient_first_derivative")
    eq(s.diff(coefficient, t, 2).subs(t, 0), phi**2/4, "literal_local_coefficient_second_derivative")
    eq(s.Rational(1, 4)*s.Rational(1, 2), s.Rational(1, 8), "actual_Dsecond_zero_frequency_coefficient")
    yes(all(not _zero(M) for M in response["X"].values()), "actual_nonempty_metric_Fourier_source_blocks")
    k, l = (1, 0, 0, 0), (4, 3, 0, 0)
    vacuum = s.eye(16)[:, 0]
    inner = _reduce((data[l]["z"].H*G0*data[k]["z"])[0])
    eq((vacuum.H*response["X"][l, k]*vacuum)[0], inner/2,
       "actual_Fourier_jet_vacuum_matrix_element_strictly_nonzero")
    yes(inner != 0, "actual_connected_metric_jet_not_a_gauge_zero")
    # Every summand has a positive denominator and a positive Gram.  The
    # explicit nonzero element makes the relaxation source strictly negative.
    yes(response["matter_relaxation_second_source"] != 0,
        "actual_nonzero_matter_Schur_correction_not_fitted")
    yes(response["eta_norm_squared"] != 0, "actual_matter_preparation_moves_off_shell")
    yes(all(k not in SHELL for k, _old in response["eta"]),
        "matter_first_normalization_orthogonality_and_all_kernel_directions_retained")
    eq(s.Rational(128, SHELL_RANK), 1, "canonical_maximal_purification_norm_without_new_weights")
    eq(sum(s.trace(M) for M in response["E2_shell"].values())/SHELL_RANK,
       response["matter_second_source"], "actual_second_response_is_occupied_operator_average")

    # The exact same return determines heat and feedback; no independent
    # generator or Delta->Lambda substitution in quadratic matter is made.
    lam, alpha, fug, Z = s.symbols("actual_lambda alpha fugacity full_trace_Z", positive=True)
    rounds = s.Symbol("actual_round_count", integer=True, positive=True)
    bret = 1-alpha*lam
    Lambda = -s.log(bret)/alpha
    beta = 2*rounds*alpha
    eq(s.diff(Lambda, lam), 1/bret, "unique_positive_return_generator_source")
    positive_B = s.Symbol("actual_positive_return_eigenvalue", positive=True)
    yes(s.simplify(s.exp(-beta*(-s.log(positive_B)/alpha))-positive_B**(2*rounds)) == 0,
        "same_actual_positive_return_heat_factor")
    pencil = 1-fug+fug*bret**(2*rounds)
    positive_pencil = 1-fug+fug*positive_B**(2*rounds)
    eq(s.simplify(-alpha*s.diff(-128*s.log(positive_pencil), positive_B)
                  -128*beta*fug*positive_B**(2*rounds-1)/positive_pencil), 0,
       "same_actual_feedback_derivative_retains_reference128")
    eq(program_gradient(lam, alpha, rounds, 128, fug, Z),
       -bret**(2*rounds-1)/Z+128*beta*fug*bret**(2*rounds-1)/pencil,
       "full_heat_feedback_kappa_retains_complete_Z_and_multiplicity")
    try:
        full_second_source({k: data[k]["energy"] for k in SHELL}, {}, response["Y_shell"],
                           response["schur_trace"], alpha, rounds, 128, fug, Z)
    except ValueError:
        checks.append("occupied_shell_cannot_replace_full4096_mode_thermal_Hessian")
    else:
        raise AssertionError("incomplete_thermal_carrier_was_accepted")
    checks.extend(signed_survival_checks(repo))
    return {"exact_checks": len(checks), "checks": checks,
            "native_creator_basis": "Actual eta*F_r native legs: full exterior eta and owned ACDB/ABCD phase conjugation, all16 retained",
            "rational_control": {"F_diagonal": "1/4", "F_offdiagonal": "1/125",
                "G_diagonal": str(d0), "G_offdiagonal": str(o0), "stationary_root": False},
            "occupied_shell_rank": 128, "Fock_dimension": 16,
            "Fourier_metric_jet": [3, 3, 0, 0], "matter_small_block_count": len(response["eta"]),
            "actual_root_scope": "Conditional on pinned v8 root and gap: PXP=0, Qeta=-R X Psi, ||R||<=2, second compatibility P(Y-2XRX)P=epsilon_second P",
            "operator_second_source": "E2_k=Y_kk-2 sum_l X_kl X_lk/(lambda_l-epsilon), full16 matrix at each of8 momenta",
            "prescribed_conformal_curve_second_compatibility": "FAILS at actual root: Tr(E2_e0)-Tr(E2_e2)<0 for every d>o>0",
            "actual_root_e0_vacuum_minus_full16_mean": "8*sqrt(2)*(d-o)>0",
            "coefficient_only_second_acceleration_can_repair_first_jet": False,
            "signed_survival_scope": "Algebraic full4copy and AF inclusion fixtures; actual survival bound and physical selection are separate",
            "rational_e0_nonscalar_witness_entry": list(nonscalar_entry) if nonscalar_entry is not None else None,
            "root_trace_contrast": "-64*(d+3o)*[(d-o)*((14+sqrt2)*d+(16+3sqrt2)*o)+(8-4sqrt2)*o^2]/[(d+o)*((7+5sqrt2)*d+(11+8sqrt2)*o)]",
            "complete_price_second_source": "Tr[(P/128+kappa)Y]+sum_ALL_k,l kappa^[1](lambda_k,lambda_l)Tr16(X_kl X_lk)-2Tr(PXRX)/128; deltaZ=0",
            "all_4096_thermal_modes_retained_in_formula": True,
            "workspace": "128^8192, retained spectator identity as in v8; no active-bath claim",
            "curved_joint_critical_family_claimed": False,
            "physical_action_AF_identification_or_affine_shift_law_selected": False}
