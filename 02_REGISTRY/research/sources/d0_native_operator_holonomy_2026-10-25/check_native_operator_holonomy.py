#!/usr/bin/env python3
"""Bounded native holonomy/paid-clock checks; no root or old suite replay."""
import argparse
from dataclasses import replace
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import mpmath as mp
import sympy as sp
import native_holonomy as nh
from check_native_execution_domain import Quadratic

ne = nh.native
CHECKS = []


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def rejects(name, callback):
    try:
        callback()
    except ne.DomainError:
        check(name, True)
    else:
        raise AssertionError(name)


def native_checks():
    bounds = dict(max_qubits=6, max_expanded_stages=10000)
    layout = ne.Execution(4, (1,), (3,), ())  # third active wire is UNKNOWN, not a free blank
    five = replace(layout, gates=nh.five_cx_identity(0, 1, 2))
    check("odd five-CX identity is exact on all columns including dirty oldRIGHT",
          ne.exact_matrix_equal(ne.word_matrix(five), sp.eye(16)))
    check("both paid identity constructors have literal lengths", len(five.gates) == 5
          and len(nh.two_cx_identity(0, 1)) == 2)
    catalogue = [replace(layout, gates=nh.controlled_holonomy_word(Q, 0, 1)) for Q in (1, 2)]
    catalogue.append(replace(layout, gates=(ne.Gate("G", (1,)),)))
    padded = nh.pad_catalogue_same_clock(catalogue, (0, 1, 2), **bounds)
    for i, (old, new) in enumerate(zip(catalogue, padded)):
        check(f"actual common paid clock preserves all endpoint columns i={i}",
              len(new.gates) == 10 and ne.exact_matrix_equal(ne.word_matrix(new), ne.word_matrix(old)))
    rejects("padding never uses immutable oldRIGHT", lambda: nh.pad_word_same_clock(layout, 5, (0, 1, 3), **bounds))
    rejects("one-stage gap is not a free idle", lambda: nh.pad_word_same_clock(layout, 1, (0, 1, 2), **bounds))
    rejects("three-stage gap is not a free idle", lambda: nh.pad_word_same_clock(layout, 3, (0, 1, 2), **bounds))
    rejects("padding requires three active wires", lambda: nh.pad_word_same_clock(layout, 5, (0, 1), **bounds))
    rejects("zero-length boundary is not a positive clock", lambda: nh.pad_word_same_clock(layout, 0, (0, 1, 2), **bounds))
    rejects("equal N cannot conceal changed input cut", lambda: nh.pad_catalogue_same_clock(
        (layout, replace(layout, blank_wires=())), (0, 1, 2), **bounds))
    for Q in (1, 2):
        observed = ne.word_matrix(catalogue[Q - 1])
        power = ne.G_LOCAL ** (2 * Q)
        expected = sp.kronecker_product(sp.diag(power, power.T), sp.eye(4))
        check(f"native controlled holonomy all-column block identity Q={Q}", ne.exact_matrix_equal(observed, expected))
        check(f"native endpoint is real SO on full active carrier Q={Q}",
              ne.exact_matrix_equal(observed.T * observed, sp.eye(16))
              and ne.GOLDEN_FIELD.from_sympy(sp.expand(observed.det() - 1)) == ne.GOLDEN_FIELD.zero)
    source = ne.Execution(5, (), (), (ne.Gate("G", (1,)),), ne.G_CX_SOURCE_I,
                          source_port=0, source_spin=(3, 4))
    inverse = ne.inverse_word(source, **bounds)
    check("inverse macro restores arbitrary dirty source spin on all 32 columns",
          len(inverse) == 11 and ne.exact_matrix_equal(
              ne.word_matrix(replace(source, gates=inverse)) * ne.word_matrix(source), sp.eye(32)))
    rejects("padding cannot address inaccessible source spin", lambda: nh.pad_word_same_clock(source, 6, (0, 1, 3), **bounds))
    gen = nh.skew_holonomy_generator(sp.diag(1, -1))
    check("symmetric K gives a real skew traceless SO generator", gen.T == -gen and sp.trace(gen) == 0)
    rejects("non-power-two scene cannot acquire unpriced zero modes", lambda: nh.skew_holonomy_generator(sp.eye(3)))
    rejects("nonsymmetric K is not this real holonomy type", lambda: nh.skew_holonomy_generator(sp.Matrix([[0, 1], [0, 0]])))
    return layout, bounds


def heat_kernel(angle, N, delta, beta):
    beta_clock = 2 * N ** 2 * beta / delta ** 2
    # EVERY one of the N clock roots is summed; neither a prepared block
    # nor the lowest Fourier root replaces this full finite heat trace.
    return mp.fsum(mp.exp(-beta_clock * (1 - mp.cos((angle + 2 * mp.pi * k) / N))) for k in range(N))


def spectral_checks(layout, bounds):
    mp.mp.dps = 90
    p = (mp.sqrt(5) - 1) / 2
    theta = mp.atan2(p, mp.sqrt(p))
    delta, beta, z, rank, dimension = mp.mpf(1) / 16, mp.mpf(1), mp.mpf(1) / 4, 8, 16
    words = [replace(layout, gates=nh.controlled_holonomy_word(Q, 0, 1)) for Q in (33, 580)]
    common = nh.pad_catalogue_same_clock(words, (0, 1, 2), **bounds)
    check("native finite catalogue has common ACTUAL clock 1166", {len(e.gates) for e in common} == {1166})
    qp, u0 = Quadratic(0, 1), Quadratic(-1, 2)
    tt, uu = [Quadratic(1), u0], [Quadratic(1), 2 * u0]
    for _ in range(2, 581):
        tt.append(2 * u0 * tt[-1] - tt[-2]); uu.append(2 * u0 * uu[-1] - uu[-2])
    rows = []
    for Q, expected_sign, word, paid in zip((33, 580), (-1, 1), words, common):
        check(f"exact native principal-angle return certificate Q={Q}",
              (tt[Q] - Fraction(9999, 10000)).sign() > 0 and uu[Q - 1].sign() == expected_sign)
        phi = mp.atan2(mp.sin(2 * Q * theta), mp.cos(2 * Q * theta))
        kappa, eta = abs(phi) / delta, delta * mp.mpf("1e-7")
        inv = ne.inventory(paid, **bounds)
        check(f"all padding and native rotations really counted Q={Q}",
              inv.g_count == 2 * Q and inv.cx_count == 1166 - 2 * Q
              and inv.full_dimension == dimension and inv.input_dimension == rank)
        feedback = -rank * mp.log(1 - z * mp.sin(phi) ** 2)
        values = []
        for N in (len(word.gates), len(paid.gates)):
            Z = dimension * (heat_kernel(phi, N, delta, beta) + heat_kernel(-phi, N, delta, beta))
            shifted = dimension * (heat_kernel(phi + eta, N, delta, beta) + heat_kernel(-phi - eta, N, delta, beta))
            recovered_error = abs(mp.log(shifted / Z)) / beta
            K = kappa + eta / delta
            tail = mp.exp(-9 * beta / delta ** 2)
            bound = 2 * mp.exp(beta * K ** 2) / delta ** 2 * (delta * K + 5 * mp.pi * tail / (1 - tail) ** 2) * eta
            check(f"full heat endpoint error has N-independent recovered bound Q={Q} N={N}", recovered_error <= bound)
            check(f"native full heat retains rebit pair Hodge and all scene/oldRIGHT modes Q={Q} N={N}",
                  Z > 0 and abs(Z / (4 * rank * mp.exp(-beta * kappa ** 2)) - 1) < mp.mpf("1e-7"))
            normalized_feedback = 2 * N ** 2 * feedback / delta ** 2
            values.append(normalized_feedback)
        check(f"fixed-z feedback retains exact normalized N-squared growth Q={Q}",
              abs(values[1] / values[0] - (mp.mpf(len(paid.gates)) / len(word.gates)) ** 2) < mp.mpf("1e-65"))
        e_error = abs(mp.sin(phi + eta) ** 2 - mp.sin(phi) ** 2)
        e_bound = 2 * abs(phi) * eta + eta ** 2
        j_error = rank * abs(mp.log((1 - z * mp.sin(phi + eta) ** 2) / (1 - z * mp.sin(phi) ** 2)))
        j_bound = rank * z * e_bound / (1 - z * min(1, (abs(phi) + eta) ** 2))
        check(f"near-identity compressed feedback error keeps delta-eta and eta-squared Q={Q}", e_error <= e_bound and j_error <= j_bound)
        alpha, m = mp.mpf(1) / 8, 8
        d_squared = (1 - mp.exp(-alpha * kappa ** 2)) / alpha
        check(f"finite-alpha scalar heat identity for K_alpha holds Q={Q}",
              abs((1 - alpha * d_squared) ** m - mp.exp(-beta * kappa ** 2)) < mp.mpf("1e-80"))
        rows.append({"Q": Q, "native_stages": len(word.gates), "paid_common_N": len(paid.gates),
                     "principal_angle": mp.nstr(phi, 20), "K_eigenvalue_magnitude": mp.nstr(kappa, 20),
                     "normalized_feedback_at_common_N": mp.nstr(values[1], 20), "input_rank": rank,
                     "full_fibre_dimension": dimension, "paired_clock_modes": 2 * len(paid.gates) * dimension})
    return {"delta": "1/16", "beta_sp": "1", "fixed_z": "1/4", "rows": rows,
            "wire_order": "data,rebit,spare_active,oldRIGHT; helper generator is rebit-first",
            "thermal_scalar_arithmetic": "mpmath 90 digits; bounded checks, not an interval certificate",
            "original_heat_dictionary": "K_alpha=D*sqrt(-log(I-alpha*D^2)/(alpha*D^2)); beta_sp=m*alpha",
            "K_dot_identified_with_D_dot": False, "feedback_counted_once": True,
            "endpoint_feedback": "sin^2(delta*K)", "recovered_heat_error": "O(eta/delta), uniform in N",
            "raw_heat_error": "delta^2/(2*N^2) times recovered heat error",
            "feedback_error": "r*z*(2*delta*||K||*eta+eta^2)/(1-z*min(1,(delta*||K||+eta)^2))",
            "whole_normalized_feedback_error": "O(N^2*eta/delta+N^2*eta^2/delta^2)",
            "fixed_z_target_feedback_source_removed": False}


def noncommuting_gradient():
    mp.mp.dps = 90
    D = mp.matrix([[mp.mpf(".2"), mp.mpf(".1")], [mp.mpf(".1"), mp.mpf("-.35")]])
    H = mp.matrix([[mp.mpf(".1"), mp.mpf(".3")], [mp.mpf(".3"), mp.mpf(".2")]])
    alpha, m, beta = mp.mpf(1) / 8, 8, mp.mpf(1)
    eigenvalues, U = mp.eigsy(D)
    f = lambda x: mp.sign(x) * mp.sqrt(-mp.log1p(-alpha * x ** 2) / alpha)
    values = [f(x) for x in eigenvalues]
    K = U * mp.diag(values) * U.T
    h = U.T * H * U
    dk = mp.matrix(2)
    for i in range(2):
        for j in range(2):
            slope = (eigenvalues[i] / ((1 - alpha * eigenvalues[i] ** 2) * values[i])
                     if i == j else (values[i] - values[j]) / (eigenvalues[i] - eigenvalues[j]))
            dk[i, j] = slope * h[i, j]
    DK = U * dk * U.T
    B = mp.eye(2) - alpha * D * D
    E = U * mp.diag([mp.exp(-beta * x ** 2) for x in values]) * U.T
    trace = lambda a: mp.fsum(a[i, i] for i in range(2))
    Z = trace(B ** m)
    old = -2 * trace(D * B ** (m - 1) * H) / Z
    new = -2 * trace(E * K * DK) / trace(E)
    check("finite-alpha test genuinely retains a noncommuting direction", mp.norm(D * H - H * D) > mp.mpf(".01") and abs(h[0, 1]) > mp.mpf(".01"))
    check("finite-alpha full matrix heat identity survives noncommutation", mp.norm(E - B ** m) < mp.mpf("1e-80"))
    check("noncommutative Frechet DK is not silently replaced by H", mp.norm(DK - H) > mp.mpf("1e-5"))
    check("original finite55 gradient equals the K_alpha chain-rule gradient", abs(old - new) < mp.mpf("1e-80"))
    return {"alpha": "1/8", "m": m, "beta_sp": "1", "arithmetic": "mpmath 90 digits; non-interval bounded check",
            "DK_method": "eigenbasis divided differences including off-diagonal H",
            "old_gradient": mp.nstr(old, 30), "K_chain_rule_gradient": mp.nstr(new, 30),
            "DK_minus_H_norm": mp.nstr(mp.norm(DK - H), 20)}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    layout, bounds = native_checks(); spectrum = spectral_checks(layout, bounds)
    gradient = noncommuting_gradient()
    paths = (Path(__file__), Path(nh.__file__), nh.DOMAIN / "native_execution.py",
             nh.DOMAIN / "check_native_execution_domain.py")
    result = {"schema": "d0.native-operator-holonomy-check/1", "status": "PASS",
              "checks_passed": len(CHECKS), "checks": CHECKS, "spectrum": spectrum,
              "noncommuting_finite55_gradient": gradient,
              "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              "scope": {"general_SK_compiler_implemented": False, "external_SK_theorem_required": True,
                        "SK_FPTEAS_target_hypothesis_retained": True, "old_suites_or_GR_roots_replayed": False,
                        "physical_beta_z_or_cut_selected": False, "full_GR_closed": False}}
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output: args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__": main()
