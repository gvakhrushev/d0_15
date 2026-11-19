#!/usr/bin/env python3
"""Small coherent-compression and full matrix-source controls only."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import mpmath as mp
import sympy as sp
import matrix_collective as mc

CHECKS = []
SOURCES = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOURCES/"d0_native_bilinear_return_echo_2026-10-25"))
import native_echo as en


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def trace(a):
    return mp.fsum(a[i, i] for i in range(a.rows))


def vector_signs(N, coordinate):
    return mp.matrix([mc.sign(z, coordinate, N) for z in range(4**N)])


def normalized(v):
    return v/mc.norm(v)


def exact_selector(N):
    pairs, h, _ = mc.label_preparer(N)
    m, size = len(pairs), h.rows
    eta = sp.Matrix([sp.sqrt(sp.Rational(1, m)) if j < m else 0 for j in range(size)])
    v = sp.eye(size)[:, 0]-eta
    exact_h = sp.eye(size)-2*v*v.T/(v.T*v)[0]
    assert (exact_h.T*exact_h).applyfunc(sp.simplify) == sp.eye(size)
    weights = [sp.simplify(exact_h[0, j]*exact_h[j, 0]) for j in range(size)]
    assert weights == [sp.Rational(1, m) if j < m else 0 for j in range(size)]
    actual, expected = {}, {}
    for bank in range(4**N):
        mean_b = sum(Fraction(mc.sign(bank, 2*j+1, N), N) for j in range(N))
        mean_eb = sum(Fraction(mc.sign(bank, 2*i, N)*mc.sign(bank, 2*j+1, N), m) for i, j in pairs)
        for data in (0, 1):
            expected[2*bank+data, 2*bank+data] = (mean_b+mean_eb)/2
            expected[2*bank+(data ^ 1), 2*bank+data] = (mean_eb-mean_b)/2
            for label, weight in enumerate(weights):
                pair = pairs[label] if label < m else None
                b1, ports = mc.route(bank, 0, pair, N)
                e, b = ports >> 1, ports & 1
                b2, p2 = mc.route(b1, ports, pair, N)
                assert p2 == 0
                index = (2*b2+(data ^ e), 2*bank+data)
                actual[index] = actual.get(index, Fraction())+Fraction(weight.p, weight.q)*(-1)**(e+b)
    return {k: v for k, v in actual.items() if v} == {k: v for k, v in expected.items() if v}


def run():
    mp.mp.dps = 70
    tol, zeta = mp.mpf("1e-48"), mp.mpf(2)**-20
    p = (mp.sqrt(5)-1)/2
    u = v = p**3
    packet = mc.packet(p*p, p*p)
    correlated = mp.matrix([mp.sqrt(p), 0, 0, p])
    x = mp.matrix([[0, 1], [1, 0]])
    expected = (1-2*p*p)*((1-p*p)*mp.eye(2)-p*p*x)
    rows = []
    for N in (2, 3):
        pairs, h, eta = mc.label_preparer(N)
        check(f"exact rational signed-permutation amplitude compression gives EVERY U-statistic column N{N}", exact_selector(N))
        check(f"full power-of-two label Householder is orthogonal and prepares every ordered injection N{N}",
              mc.norm(h.T*h-mp.eye(h.rows)) < tol and mc.norm(h[:, 0]-eta) < tol
              and len(pairs) == N*(N-1))
        routed = set()
        permutation = []
        for label in range(h.rows):
            pair = pairs[label] if label < len(pairs) else None
            for bank in range(4**N):
                for ports in range(4):
                    b1, p1 = mc.route(bank, ports, pair, N)
                    check_inverse = mc.route(b1, p1, pair, N) == (bank, ports)
                    if not check_inverse:
                        raise AssertionError("routing inverse failed")
                    routed.add((label, b1, p1))
                    permutation.append((label*4**N+b1)*4+p1)
        check(f"coherent routing is a bijection on ALL dirty-port and unused-label columns N{N}",
              len(routed) == h.rows*4**N*4)
        visited, cycles = set(), 0
        for start in range(len(permutation)):
            if start not in visited:
                cycles += 1
                current = start
                while current not in visited:
                    visited.add(current)
                    current = permutation[current]
        check(f"fixed work-only encoder has determinant plus one without using DATA as compiler workspace N{N}",
              (len(permutation)-cycles) % 2 == 0 and (4**N*4) % 2 == 0)
        kernel = mc.coherent_corner(N)
        explicit = sum((mc.pair_kernel(N, pair) for pair in pairs), mp.zeros(kernel.rows))/len(pairs)
        check(f"literal label prepare-route-V-unroute-unprepare gives the operator-valued U statistic N{N}",
              mc.norm(kernel-explicit) < tol and mc.norm(kernel) <= 1+tol)
        psi = mc.product(packet, N)
        psi_corr = mc.product(correlated, N)
        check(f"rank8 corner retains BOTH bands and removes same-packet correlation on the IID section N{N}",
              mc.norm(mc.return_matrix(kernel, psi)-expected) < tol
              and mc.norm(mc.return_matrix(kernel, psi_corr)-expected) < tol)
        qminus = 1-zeta+zeta*v*v
        qplus = 1-zeta+zeta*u*u*v*v
        dminus, dplus = -8*zeta*v/qminus, -8*zeta*u*v/qplus
        gu, gv = v*dplus, dminus+u*dplus
        for label, base, cov in (("product", packet, 0), ("correlated-packet", correlated, 1-u*v)):
            state = mc.product(base, N)
            variance1 = (1-u*u)*gu*gu+2*cov*gu*gv+(1-v*v)*gv*gv
            remainder = dplus*dplus*((1-u*u)*(1-v*v)+cov*cov)/(N*(N-1))
            g = mc.gradient(kernel, state, zeta)
            check(f"full matrix logdet gradient matches exact first plus second Hoeffding norms {label} N{N}",
                  abs(mc.norm(g)**2/4-variance1/N-remainder) < tol)
        if N == 2:
            score = mc.score(kernel, psi, zeta)
            conditional = mc.one_conditional(score, packet)
            mean = (psi.T*score*psi)[0]
            ze, zb = mp.diag([1, 1, -1, -1]), mp.diag([1, -1, 1, -1])
            first = (gu*(ze-u*mp.eye(4))+gv*(zb-v*mp.eye(4)))/2
            check("full two-band cotangent has the required one-slot conditional and NONZERO direct-bias first component",
                  mc.norm(conditional-mean*mp.eye(4)-first) < tol and mc.norm(first*packet) > mp.mpf("1e-8"))
            # Antisymmetric cross-packet excitation: genuinely correlated
            # direction, orthogonal to all one-coordinate marginal tangents.
            raw = mp.matrix([((mc.sign(z, 0, N)-u)*(mc.sign(z, 3, N)-v)
                            -(mc.sign(z, 2, N)-u)*(mc.sign(z, 1, N)-v))*psi[z]
                             for z in range(4**N)])
            tangent = normalized(raw)
            eps = mp.mpf("1e-17")
            fd = (mc.price(kernel, normalized(psi+eps*tangent), zeta)
                  -mc.price(kernel, normalized(psi-eps*tangent), zeta))/(2*eps)
            check("arbitrary correlated pure tangent uses the actual matrix-logdet cotangent",
                  abs(fd-mp.re((tangent.H*mc.gradient(kernel, psi, zeta))[0])) < mp.mpf("1e-32")
                  and abs((psi.H*tangent)[0]) < tol)
            symmetric = mp.matrix([((mc.sign(z, 0, N)-u)*(mc.sign(z, 3, N)-v)
                                    +(mc.sign(z, 2, N)-u)*(mc.sign(z, 1, N)-v))*psi[z]
                                   for z in range(4**N)])
            symmetric = normalized(symmetric)
            symmetric_fd = (mc.price(kernel, normalized(psi+eps*symmetric), zeta)
                            -mc.price(kernel, normalized(psi-eps*symmetric), zeta))/(2*eps)
            symmetric_source = mp.re((symmetric.H*mc.gradient(kernel, psi, zeta))[0])
            marginal_sources = [2*mp.fsum(symmetric[z]*mc.sign(z, coordinate, N)*psi[z]
                                          for z in range(4**N)) for coordinate in range(2*N)]
            check("symmetric two-excitation tangent preserves all marginal first sources but has NONZERO correlation remainder",
                  max(abs(t) for t in marginal_sources) < tol
                  and abs(symmetric_source) > mp.mpf("1e-8")
                  and abs(symmetric_fd-symmetric_source) < mp.mpf("1e-32"))
            moved = normalized(psi+mp.mpf(".2")*tangent)
            cs = [mc.return_matrix(mc.pair_kernel(N, pair), moved) for pair in pairs]
            c = mc.return_matrix(kernel, moved)
            actual_F = mp.eye(2)-c*c
            averaged_F = sum((mp.eye(2)-ci*ci for ci in cs), mp.zeros(2))/len(cs)
            wrong_price = -4*mp.log(mp.det(mp.eye(2)-zeta*averaged_F))
            check("hostile averaged defects lose programme leakage and differ from the actual amplitude return",
                  mc.norm(actual_F-averaged_F) > mp.mpf(".001")
                  and min(mp.eigsy(actual_F-averaged_F, eigvals_only=True)) > -tol
                  and abs(mc.price(kernel, moved, zeta)-wrong_price) > mp.mpf("1e-8"))
            test_kernel, test_psi = kernel, psi
        rows.append({"N": N, "ordered_labels": len(pairs), "full_label_dimension": h.rows,
                     "compressed_bank_DATA_columns": kernel.rows,
                     "full_ideal_fibre_with_spin": h.rows*4**N*4*2*4,
                     "protected_input_rank": 8, "J_product": mp.nstr(mc.price(kernel, psi, zeta), 30),
                     "sqrtN_gradient_over2": mp.nstr(mp.sqrt(N)*mc.norm(mc.gradient(kernel, psi, zeta))/2, 30)})
    # Global synthetic two-band matrix diagnostic: an honest zero first
    # conditional with a nonzero second component, NOT a native GR root.
    toy_rows = []
    for N in (2, 3):
        toy, c0, direction = mc.toy_kernel(N)
        state = mc.product(mp.matrix([1/mp.sqrt(2), 1/mp.sqrt(2)]), N)
        alpha = -8*zeta*trace(((1-zeta)*mp.eye(2)+zeta*c0*c0)**-1*c0*direction)
        norm_exact = 2*abs(alpha)*mp.sqrt(mp.mpf(2)/(N*(N-1)))
        check(f"global matrix toy has scalar first conditional and the true second-component source N{N}",
              mc.norm(mc.return_matrix(toy, state)-c0) < tol
              and abs(mc.norm(mc.gradient(toy, state, zeta))-norm_exact) < tol)
        if N == 2:
            t = mc.score(toy, state, zeta)
            t1 = mc.one_conditional(t, mp.matrix([1/mp.sqrt(2), 1/mp.sqrt(2)]))
            check("global toy cancellation is an operator identity rather than restriction of preparation tangents",
                  mc.norm(t1-trace(t1)*mp.eye(2)/2) < tol and norm_exact > 0)
        toy_rows.append({"N": N, "gradient_norm": mp.nstr(norm_exact, 30)})
    # Encoder error may destroy every read-only block. This right Givens
    # perturbation is an actual orthogonal encoder perturbation in the ideal
    # finite model; it is NOT claimed to be a compiled native word.
    angle = mp.mpf(".003")
    r_bank = mp.eye(test_psi.rows)
    r_bank[0, 0] = r_bank[3, 3] = mp.cos(angle)
    r_bank[0, 3], r_bank[3, 0] = -mp.sin(angle), mp.sin(angle)
    r = mc.kron(r_bank, mp.eye(2))
    changed = r.T*test_kernel*r
    delta = 2*mp.sin(angle/2)
    epsilon = mc.norm(changed-test_kernel)
    td = mc.norm(mc.score(changed, test_psi, zeta)-mc.score(test_kernel, test_psi, zeta))
    gd = mc.norm(mc.gradient(changed, test_psi, zeta)-mc.gradient(test_kernel, test_psi, zeta))
    check("full encoder perturbation bounds the Hermitian matrix kernel even after read-only structure is lost",
          epsilon <= 2*delta+tol and epsilon > 0)
    check("true matrix score error obeys32 zeta epsilon over the squared logdet gap",
          td <= 32*zeta*epsilon/(1-zeta)**2)
    check("projected pure-gradient error obeys128 zeta delta over the squared logdet gap",
          gd <= 128*zeta*delta/(1-zeta)**2)
    # Separate WHOLE-bank state error; not one-copy error silently reused N times.
    moved = normalized(test_psi+mp.mpf(".002")*normalized(mp.matrix([1]+[0]*(test_psi.rows-1))))
    eta_error = mc.norm(moved-test_psi)
    state_debt = mc.norm(mc.gradient(test_kernel, moved, zeta)-mc.gradient(test_kernel, test_psi, zeta))
    check("whole-bank preparation error has its own256 zeta eta gradient budget",
          state_debt <= 256*zeta*eta_error/(1-zeta)**2)
    # Actual small native count fixture; this is not the new compiled selector.
    ne = en.native
    forward = (ne.Gate("G", (0,)), ne.Gate("G", (1,)), ne.Gate("CX", (0, 1)),
               ne.Gate("G", (0,)), ne.Gate("CX", (1, 0)), ne.Gate("G", (1,)), ne.Gate("CX", (0, 1)))
    whole = en.layout(forward+en.middle_word()+ne.inverse_word(en.layout(forward), **en.BOUNDS))
    inventory = ne.inventory(whole, **en.BOUNDS)
    check("literal native forward-middle-raw-inverse inventory is6g_port plus12g_off plus2c plus11",
          len(whole.gates) == 6*2+12*2+2*3+11 == 53
          and inventory.g_count == 8 and inventory.source_i_count == 20 and inventory.cx_count == 25)
    return {"checks": CHECKS, "checks_passed": len(CHECKS), "rows": rows, "global_matrix_toy": toy_rows,
            "processor_error": {"delta": mp.nstr(delta, 30), "kernel_epsilon": mp.nstr(epsilon, 30),
                                "score_error": mp.nstr(td, 30), "gradient_error": mp.nstr(gd, 30)},
            "matrix_scope": "ideal coherent full compressed32/128 columns; routing all dirty ports/labels; no global native word or clock matrix",
            "numeric_arithmetic": "70-digit mpmath non-interval; label/rational compression, permutation parity and native counts exact",
            "primitive_count_fixture": {"g_port": 2, "g_off": 2, "c": 3, "actual_N": 53},
            "same_protected_input_rank": 8, "source_spin_multiplier": 4,
            "global_source_interface": "ONE aggregate X=tau*sum(c_i*f_i), Y=tau*sum(c_i*q_i); on Sigma only; Gamma=4*a0*tau, W=1",
            "new_global_native_word_emitted": False, "efficient_compiler_claimed": False,
            "uniform_label_native_primitive_claimed": False, "readiness_or_gamma_dropped": False,
            "canonical42_root_replayed": False, "toy_is_physical42_example": False,
            "direct_Eb_first_Hoeffding_component_vanishes": False,
            "whole_pure_bank_preparation_from_unknown_RIGHT_claimed": False,
            "continuous_native_word_selector_proved": False, "full_native_joint_stationarity_proved": False,
            "physical_admission_proved": False, "GR_closed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result.update(schema="d0.native-matrix-collective-return-check/1", status="PASS")
    repo = SOURCES.parents[2]
    primary = repo/"02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
    paths = [Path(__file__).resolve(), Path(mc.__file__).resolve(), Path(__file__).with_name("PROOF.md"),
             SOURCES/"d0_native_bilinear_return_echo_2026-10-25"/"PROOF.md",
             SOURCES/"d0_native_bilinear_return_echo_2026-10-25"/"native_echo.py",
             en.DOMAIN/"native_execution.py",
             SOURCES/"d0_native_operator_holonomy_2026-10-25"/"PROOF.md",
             repo/"02_REGISTRY/research/A4D_NONVACUUM_COLLECTIVE_PREPARATION_SOURCE_EQUIVALENCE_2026_10_22.md"]
    result["inputs_sha256"] = {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    text_primary = primary.read_text(encoding="utf-8")
    result["consumed_sections_sha256"] = {}
    for section in ("7h", "7s", "7ac"):
        start = text_primary.index("## "+section+".")
        end = text_primary.find("\n## ", start+4)
        body = text_primary[start:end if end >= 0 else len(text_primary)]
        result["consumed_sections_sha256"][section] = hashlib.sha256(body.encode()).hexdigest()
    result["runtime"] = {"python": sys.version.split()[0], "mpmath": mp.__version__}
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
