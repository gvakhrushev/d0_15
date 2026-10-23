#!/usr/bin/env python3
"""Exact full16 readout of Lorentz transport from the actual raising word.

Only the pinned AST _creators helper executes; no historical run()/replay.
The null completion is tested across, rather than just along, the null cone.
This is operator reconstruction, not a physical gate or a price-selection law.
Default execution is read-only; --output explicitly writes a JSON receipt.
"""
from __future__ import annotations

import argparse
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform

import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
HELPER = ("02_REGISTRY/research/sources/"
          "d0_complete_record_channel_2026-10-17/check_flat_relaxation.py")
CURVED = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
PINS = {
    HELPER: "0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9",
    CURVED: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
}
CHECKS: list[str] = []
I4, I16, O16 = s.eye(4), s.eye(16), s.zeros(16)
ETA = s.diag(1, -1, -1, -1)


def clean(value):
    return s.cancel(s.expand(value))


def matrix_clean(matrix):
    return matrix.applyfunc(clean)


def require(name, condition):
    if condition is not True and condition != s.true:
        raise ArithmeticError(f"FAILED {name}: {condition}")
    CHECKS.append(name)


def equal(name, actual, expected):
    difference = actual-expected
    entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
    require(name, all(clean(entry) == 0 for entry in entries))


def literal_creators():
    for relative, digest in PINS.items():
        require("literal_pin:"+relative,
                hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() == digest)
    tree = ast.parse((ROOT/HELPER).read_text())
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "_creators"]
    require("only_literal_creator_helper_loaded", len(nodes) == 1)
    scope = {"s": s, "ast": ast, "lru_cache": lru_cache, "CURVED": CURVED}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), HELPER, "exec"), scope)
    creators, order = scope["_creators"](ROOT)
    require("actual_ACDB_exterior_order", order == (0, 2, 3, 1))
    return creators, order


def exterior(M, order):
    """All grades0..4 in the literal exterior basis, without a carrier cut."""
    indices = [[i for i in order if mask & (1 << i)] for mask in range(16)]
    U = s.zeros(16)
    for i, rows in enumerate(indices):
        for j, cols in enumerate(indices):
            if len(rows) == len(cols):
                U[i, j] = clean(M.extract(rows, cols).det()) if rows else 1
    return U


def creator(C, vector):
    return sum((vector[i]*C[i] for i in range(4)), O16)


def contraction(C, covector):
    # Complex-linear covector contraction; no conjugation of its coefficients.
    return sum((covector[i]*C[i].H for i in range(4)), O16)


def clocks_and_car(C, order):
    Ox = s.Matrix([[s.Rational(3, 5), -s.Rational(4, 5), 0, 0],
                   [s.Rational(4, 5), s.Rational(3, 5), 0, 0],
                   [0, 0, 1, 0], [0, 0, 0, 1]])
    Oy = s.Matrix([[s.Rational(5, 13), -s.Rational(12, 13), 0, 0],
                   [s.Rational(12, 13), s.Rational(5, 13), 0, 0],
                   [0, 0, 1, 0], [0, 0, 0, 1]])
    nu_x, nu_y = Ox[:, 0], Oy[:, 0]
    Jx, Jy = Ox*ETA*Ox.T, Oy*ETA*Oy.T
    equal("clock_x_involution", Jx*Jx, I4)
    equal("clock_y_involution", Jy*Jy, I4)
    require("unequal_endpoint_clocks", nu_x != nu_y and Jx != Jy)
    numbers = [c*c.H for c in C]
    parity = s.diag(*[(-1)**bin(mask).count("1") for mask in range(16)])
    Hx, Hy = exterior(Jx, order), exterior(Jy, order)
    for name, nu, H in [("x", nu_x, Hx), ("y", nu_y, Hy)]:
        cnu = creator(C, nu)
        equal("CAR_clock_fundamental_symmetry_"+name,
              H, parity*(I16-2*cnu*cnu.H))
        equal("positive_frame_clock_norm_"+name, (nu.T*nu)[0], 1)
    P1 = sum((numbers[i]*s.prod([I16-numbers[j] for j in range(4) if j != i])
              for i in range(4)), O16)
    equal("P1_is_actual_CAR_polynomial", P1,
          s.diag(*[int(bin(mask).count("1") == 1) for mask in range(16)]))
    equal("P1_is_projector", P1*P1, P1)
    gamma = [C[i]+ETA[i, i]*C[i].H for i in range(4)]
    chi = gamma[0]*gamma[1]*gamma[2]*gamma[3]
    Wx, Wy = exterior(Ox, order), exterior(Oy, order)
    chix, chiy = Wx*chi*Wx.H, Wy*chi*Wy.H
    equal("chi_x_square_minus_one", chix*chix, -I16)
    equal("chi_y_square_minus_one", chiy*chiy, -I16)
    return Ox, Oy, nu_x, Jx, Jy, Hx, Hy, P1, chix, chiy


def read_B(C, P1, X, u, nu):
    alpha = nu.T/(nu.dot(u))
    one_particle = P1*contraction(C, alpha)*X*P1
    indices = [1 << i for i in range(4)]
    return matrix_clean(one_particle.extract(indices, indices)), alpha


def read_u(X):
    # Lambda(M)|vac>=|vac>; all four coefficients are already in actual X.
    return matrix_clean(X.extract([1 << i for i in range(4)], [0]))


def null_data(B, u, Jx, Jy):
    q = clean((u.T*Jx*u)[0])
    b = matrix_clean(B.T*Jx*u)
    S = matrix_clean(Jy-B.T*Jx*B)
    bb = clean(b.dot(b))
    z = matrix_clean(b/bb)
    scalar = clean((z.T*S*z)[0])
    return q, b, S, bb, z, scalar


def fixture(C, order, clock, name, u, M):
    _, _, nu, Jx, Jy, Hx, Hy, P1, chix, chiy = clock
    equal(name+":Lorentz", M.T*Jx*M, Jy)
    equal(name+":proper", M.det(), 1)
    U, Ui = exterior(M, order), exterior(matrix_clean(Jy*M.T*Jx), order)
    equal(name+":all16_inverse", U*Ui, I16)
    equal(name+":vacuum_retained", U[0, 0], 1)
    equal(name+":top_grade_retained", U[15, 15], 1)
    X = creator(C, u)*U
    equal(name+":actual_vacuum_to_grade1_recovers_u", read_u(X), u)
    u = read_u(X)
    require(name+":strict_native_contraction_window", s.trace(X.H*X) < 1)
    B, alpha = read_B(C, P1, X, u, nu)
    equal(name+":actual_grade1_to2_readout", B, (I4-u*alpha)*M)
    q, b, S, bb, z, scalar = null_data(B, u, Jx, Jy)
    a = (alpha*M).T
    equal(name+":Lorentz_completion_equation", S, b*a.T+a*b.T+q*a*a.T)
    require(name+":nonzero_b", bb > 0)
    r = clean(a.dot(z))
    require(name+":positive_local_branch", 1+q*r > 0)
    d = s.sqrt(clean(1+q*scalar))
    t = clean(scalar/(1+d))
    a_read = matrix_clean((S*z-b*t)/d)
    M_read = matrix_clean(B+u*a_read.T)
    equal(name+":null_completion_readout", M_read, M)
    U_read = exterior(M_read, order)
    equal(name+":full16_reconstruction", U_read, U)
    equal(name+":positive_adjoint_inverse_with_clocks", Hy*U_read.H*Hx, Ui)
    require(name+":bare_positive_adjoint_is_wrong", U.H != Ui)
    equal(name+":moving_chirality_intertwines", chix*U, U*chiy)
    equal(name+":moving_chirality_creation_sign",
          chix*creator(C, u)*(-chix), -contraction(C, Jx*u))
    if q != 0:
        gamma_u = creator(C, u)+contraction(C, Jx*u)
        chi_read = gamma_u*(X-chix*X*(-chiy))/q
        equal(name+":nonnull_chi_full16_readout", chi_read, U)
    else:
        equal(name+":null_formula_without_q_inverse",
              a_read, S*z-scalar*b/2)
    return {"name": name, "q": str(q), "b_norm_squared": str(bb),
            "d": str(d), "trace_X_adjoint_X": str(s.trace(X.H*X)),
            "full16_reconstructed": True, "bare_adjoint_rejected": True}


def transverse_family(C, order, clock, N):
    """Exact rational one-parameter identity implies every transverse jet."""
    Ox, Oy, nu, Jx, Jy, _, _, P1, _, _ = clock
    eps = s.Symbol("eps", real=True)
    k = s.Rational(1, 5)+eps
    M = matrix_clean(Ox*(I4+k*N+k*k*N*N/2)*Oy.T)
    u = Ox*s.Matrix([1+eps, 1, 0, 0])/16
    U = exterior(M, order)
    X = creator(C, u)*U
    equal("transverse_family:actual_X_recovers_moving_u", read_u(X), u)
    u = read_u(X)
    B, alpha = read_B(C, P1, X, u, nu)
    equal("transverse_family:actual_full16_X_readout", B, (I4-u*alpha)*M)
    q, b, S, bb, z, scalar = null_data(B, u, Jx, Jy)
    equal("transverse_family:q_crosses_null", q, eps*(2+eps)/256)
    require("transverse_family:transverse_not_null_tangent", s.diff(q, eps).subs(eps, 0) != 0)
    a = matrix_clean((alpha*M).T)
    r = clean(a.dot(z))
    # A certified positive square root on a full open neighborhood of eps=0.
    # This branch certificate avoids replacing sqrt(d^2) by d globally.
    d = clean(1+q*r)
    equal("transverse_family:completion_equation", S, b*a.T+a*b.T+q*a*a.T)
    equal("transverse_family:square_root_identity", d*d, 1+q*scalar)
    equal("transverse_family:positive_branch_at_null", d.subs(eps, 0), 1)
    require("transverse_family:b_nonzero_at_null", bb.subs(eps, 0) > 0)
    require("transverse_family:alpha_regular_at_null", nu.dot(u).subs(eps, 0) != 0)
    a_read = matrix_clean((S*z-b*scalar/(1+d))/d)
    M_read = matrix_clean(B+u*a_read.T)
    equal("transverse_family:exact_one_parameter_identity", M_read, M)
    U_read = exterior(M_read, order)
    equal("transverse_family:exact_full16_identity", U_read, U)
    for jet in (1, 2):
        equal(f"transverse_family:full16_jet{jet}",
              U_read.diff(eps, jet).subs(eps, 0), U.diff(eps, jet).subs(eps, 0))

    # Wrong shortcut: extending only the q=0 formula off the null cone.
    a_bad = matrix_clean(S*z-scalar*b/2)
    M_bad = matrix_clean(B+u*a_bad.T)
    equal("null_only_shortcut:agrees_at_null", M_bad.subs(eps, 0), M.subs(eps, 0))
    bad_jets = []
    difference = M_bad-M
    for jet in (1, 2):
        error = matrix_clean(difference.diff(eps, jet).subs(eps, 0))
        witnesses = [(i, j, error[i, j]) for i in range(4) for j in range(4) if error[i, j] != 0]
        require(f"null_only_shortcut:wrong_transverse_jet{jet}", bool(witnesses))
        i, j, value = witnesses[0]
        bad_jets.append({"derivative_order": jet, "matrix_entry": [i, j],
                         "incorrect_minus_actual": str(value)})
    return {"parameter": "eps", "u": "Ox*(1+eps,1,0,0)/16",
            "M": "Ox*exp((1/5+eps)*N)*Oy^T; N^3=0",
            "q": str(q), "full16_exact_one_parameter_identity": True,
            "transverse_derivative_orders_checked": [1, 2],
            "domain": "open neighborhood of eps=0 with nu.u!=0, b^T b>0, 1+q*r>0",
            "null_only_extension_counterexamples": bad_jets}


def coherent_controls(C):
    """Decisive finite premises; no SWAP simulation or convergence suite."""
    # Principal whitening: its positive square root is itself Lorentz.
    n = s.Matrix([s.Rational(5, 4), s.Rational(3, 4), 0, 0])
    h = -ETA+2*ETA*n*n.T*ETA
    L = s.Matrix([[s.Rational(5, 4), -s.Rational(3, 4), 0, 0],
                  [-s.Rational(3, 4), s.Rational(5, 4), 0, 0],
                  [0, 0, 1, 0], [0, 0, 0, 1]])
    equal("principal_whitening:unit_future_n", (n.T*ETA*n)[0], 1)
    equal("principal_whitening:positive_symmetric_L", L.T, L)
    require("principal_whitening:Sylvester_positive",
            all(L[:j, :j].det() > 0 for j in range(1, 5)))
    equal("principal_whitening:L_is_actual_positive_root", L*L, h)
    equal("principal_whitening:h_Lorentz", h*ETA*h, ETA)
    equal("principal_whitening:L_Lorentz", L*ETA*L, ETA)
    equal("principal_whitening:Ln_is_e0", L*n, I4[:, 0])
    equal("principal_whitening:J_is_eta", L.inv().T*ETA*L.inv(), ETA)

    # A genuine full-CAR raising word. Its Julia roots are exact occupation
    # polynomials, so this test neither guesses a square root nor cuts grades.
    X = s.Rational(3, 5)*C[0]
    number = C[0]*C[0].H
    equal("Julia_fixed_state:actual_occupation_selfadjoint", number.H, number)
    equal("Julia_fixed_state:actual_occupation_projector", number*number, number)
    left = I16-number/5
    right = (4*I16+number)/5
    equal("Julia_fixed_state:positive_left_root_squared", left*left, I16-X*X.H)
    equal("Julia_fixed_state:positive_right_root_squared", right*right, I16-X.H*X)
    julia = X.row_join(left).col_join(right.row_join(-X.H))
    equal("Julia_fixed_state:full32_unitary", julia.H*julia, s.eye(32))
    swap_port = s.kronecker_product(s.Matrix([[0, 1], [1, 0]]), I16)
    O = swap_port*julia
    blank = s.zeros(32, 1)
    blank[15, 0] = 1  # coefficient port0, actual Fock-top mask15.
    equal("Julia_fixed_state:raising_annihilates_Fock_top", X*I16[:, 15], s.zeros(16, 1))
    equal("Julia_fixed_state:O_unitary", O.H*O, s.eye(32))
    equal("Julia_fixed_state:O_fixes_known_blank_exactly", O*blank, blank)

    # P U P specifies a compression, not an invariant subspace for sym(U).
    P, Z = s.diag(1, 0), s.diag(1, -1)
    V = s.Matrix([[s.Rational(3, 5), s.Rational(4, 5)],
                  [s.Rational(4, 5), -s.Rational(3, 5)]])
    equal("double_P:reflection_orthogonal", V.T*V, s.eye(2))
    equal("double_P:compression_only_correct_entry", P*V*P, s.Rational(3, 5)*P)
    require("double_P:compression_only_crossblock_nonzero", (s.eye(2)-P)*V*P != s.zeros(2))
    A = P*V*P*V*P
    equal("double_P:actual_entry_polynomial", A, s.Rational(9, 25)*P)
    equal("double_P:actual_polynomial_crossblocks_zero", (s.eye(2)-P)*A*P, s.zeros(2))
    reflection_words = [R0*V*R1*V*R2
                        for R0 in (s.eye(2), Z) for R1 in (s.eye(2), Z)
                        for R2 in (s.eye(2), Z)]
    equal("double_P:finite_eight_word_LCU", sum(reflection_words, s.zeros(2))/8, A)
    require("double_P:missing_intermediate_P_changes_polynomial", P*V*V*P != A)

    W = s.Matrix([[s.Rational(3, 5), -s.Rational(4, 5)],
                  [s.Rational(4, 5), s.Rational(3, 5)]])
    J = s.Matrix([[0, -1], [1, 0]])
    def skew(U):
        return s.zeros(2).row_join(-U).col_join(U.T.row_join(s.zeros(2)))
    K = skew(W)
    equal("skew_word:orthogonal_W", W.T*W, s.eye(2))
    equal("skew_word:K_is_skew", K.T, -K)
    equal("skew_word:K_square_minus_one", K*K, -s.eye(4))
    t = s.Symbol("t", real=True)
    D = s.diag(W, s.eye(2))
    rotation = s.kronecker_product(s.cos(t)*s.eye(2)+s.sin(t)*J, s.eye(2))
    equal("skew_word:exact_exponential_conjugation", D*rotation*D.T,
          s.cos(t)*s.eye(4)+s.sin(t)*K)
    equal("skew_word:paired_symmetric_generator", K+skew(W.T),
          2*s.kronecker_product(J, (W+W.T)/2))
    initial = s.Matrix([1, 0, 0, 0])
    outside = s.kronecker_product(s.eye(2), s.eye(2)-P)
    equal("double_P:sandwiched_generator_keeps_work", outside*s.kronecker_product(J, A)*initial,
          s.zeros(4, 1))
    equal("double_P:compression_only_generator_leaks_at_first_order",
          outside*s.kronecker_product(J, V)*initial,
          s.Matrix([0, 0, 0, s.Rational(4, 5)]))
    return {"principal_positive_root_has_fixed_J_eta": True,
            "Julia_test": "X=(3/5)C0; O=sigma_x(port) J(X)",
            "known_fixed_state": "port0 tensor Fock-top; all16 data grades retained",
            "double_P_LCU_word_count": 8,
            "compression_only_work_leakage_first_jet": "4/5",
            "scope": "Exact finite compiler premises, not finite-product cleanwork or physical admission",
            "product_formula_convergence_tested": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Explicit opt-in JSON receipt; default read-only")
    args = parser.parse_args()
    C, order = literal_creators()
    clock = clocks_and_car(C, order)
    Ox, Oy = clock[:2]
    null = s.Matrix([1, 1, 0, 0])
    w = s.Matrix([0, 0, 1, 0])
    N = null*(w.T*ETA)-w*(null.T*ETA)
    equal("null_unipotent_generator_Lorentz", N.T*ETA+ETA*N, s.zeros(4))
    equal("null_unipotent_generator_cube_zero", N**3, s.zeros(4))
    require("null_unipotent_generator_square_nonzero", N*N != s.zeros(4))
    fixtures = []
    for eps, name in [(s.S.Zero, "null_unipotent"),
                      (s.Rational(1, 20), "timelike_perturbation"),
                      (-s.Rational(1, 20), "spacelike_perturbation")]:
        k = s.Rational(1, 5)+eps
        M = Ox*(I4+k*N+k*k*N*N/2)*Oy.T
        u = Ox*s.Matrix([1+eps, 1, 0, 0])/16
        fixtures.append(fixture(C, order, clock, name, u, M))
    boost = s.Matrix([[s.Rational(5, 4), s.Rational(3, 4), 0, 0],
                      [s.Rational(3, 4), s.Rational(5, 4), 0, 0],
                      [0, 0, 1, 0], [0, 0, 0, 1]])
    fixtures.append(fixture(C, order, clock, "finite_boost",
                            Ox*s.Matrix([1, s.Rational(19, 20), 0, 0])/16, Ox*boost*Oy.T))
    # The null completion is local, not a global formula for every nonnull u.
    # For u parallel to the clock, b=0; the q!=0 chirality formula still works.
    _, _, nu, Jx, Jy, _, _, P1, chix, chiy = clock
    u_time = Ox[:, 0]/16
    U_time = exterior(Ox*boost*Oy.T, order)
    X_time = creator(C, u_time)*U_time
    B_time, _ = read_B(C, P1, X_time, u_time, nu)
    equal("pure_time_domain_control:b_zero", B_time.T*Jx*u_time, s.zeros(4, 1))
    q_time = (u_time.T*Jx*u_time)[0]
    require("pure_time_domain_control:nonnull", q_time > 0)
    gamma_time = creator(C, u_time)+contraction(C, Jx*u_time)
    equal("pure_time_domain_control:chi_formula_still_exact",
          gamma_time*(X_time-chix*X_time*(-chiy))/q_time, U_time)
    eps = s.Symbol("eps", real=True)
    X_scale = (1+eps)*X_time
    equal("moving_u_countercontrol:actual_X_recovers_scaled_u",
          read_u(X_scale), (1+eps)*u_time)
    frozen_read = gamma_time*(X_scale-chix*X_scale*(-chiy))/q_time
    equal("moving_u_countercontrol:frozen_u_spurious_first_jet",
          frozen_read.diff(eps).subs(eps, 0), U_time)
    require("moving_u_countercontrol:actual_transport_first_jet_zero",
            U_time.diff(eps) == O16)
    family = transverse_family(C, order, clock, N)
    coherent = coherent_controls(C)
    result = {
        "status": "PASS", "input_commit": "3447a1842d676a1b7c7f2ebe7e1c7b583ad9ba63",
        "python": platform.python_version(), "sympy": s.__version__,
        "source_sha256": PINS, "carrier_dimension": 16, "all_exterior_grades_retained": True,
        "checks": CHECKS, "check_count": len(CHECKS), "fixtures": fixtures,
        "transverse_family": family, "coherent_controls": coherent,
        "scope": "Smooth local algebraic reconstruction of full Lorentz transport from X=C(u)Lambda(M)",
        "u_recovered_from_actual_X": True,
        "physical_gate_compilation": False, "native_price_selection": False, "gr_closure": False,
        "remaining_obligation": "An algebraic readout does not establish coherent physical execution or its full price",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
