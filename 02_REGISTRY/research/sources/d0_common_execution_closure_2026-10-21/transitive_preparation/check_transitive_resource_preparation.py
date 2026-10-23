#!/usr/bin/env python3
"""Narrow controls for the measured transitive-bank source theorem.

No original geometric/root/rank suite is executed. Source contracts and
the all-carrier statements are the analytic proof, not fitted fixtures.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_quadratic_field(repo, relpath):
    path = repo / relpath
    spec = importlib.util.spec_from_file_location("pinned_native_probe_arithmetic", path)
    require(spec is not None and spec.loader is not None, "pinned arithmetic loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.Q, module.P


def controlled_shift_control():
    sizes = (1, 2, 4, 8)
    counts = {}
    for n in sizes:
        k = (n - 1).bit_length()
        for label in range(n):
            slots = list(range(n))
            paid_transpositions = 0
            for bit in range(k):
                step = 1 << bit
                # Each shift-by-step permutation has gcd(n, step)=step cycles.
                for residue in range(step):
                    cycle = list(range(residue, n, step))
                    # Swap the pivot successively; execute the same circuit
                    # even when its controlling measured bit is zero.
                    for other in cycle[1:]:
                        paid_transpositions += 1
                        if label & step:
                            slots[cycle[0]], slots[other] = slots[other], slots[cycle[0]]
            require(slots == [((i - label) % n) for i in range(n)],
                    "fixed controlled transposition network is a cyclic shift")
            require(paid_transpositions == ((k - 1) * n + 1 if n > 1 else 0),
                    "paid permutation schedule independent of measured shift")
        counts[str(n)] = (k - 1) * n + 1 if n > 1 else 0
    # Purifiers retain their original labels; only LEFT factors are permuted.
    # Each input factor appears once in each output slot across all shifts.
    for slot in range(8):
        require(sorted((slot - j) % 8 for j in range(8)) == list(range(8)),
                "transitivity with retained, unpermuted purifier labels")
    return {"sizes": list(sizes), "fixed_register_transpositions": counts,
            "only_LEFT_permuted": True, "shift_label_retained": True}


def actual_weight_source_control(Q, p):
    # The pinned cost20 owner proves these actual count values occur, and
    # total=10946 on S=256. This is a two-density algebra fixture, not a
    # re-execution or replacement of the original geometric root theorem.
    total, sites = 10946, 256
    count_plus, count_minus = 29, 78
    rho_plus = F(sites * count_plus, total)
    rho_minus = F(sites * count_minus, total)
    require(F(count_plus, 1) / rho_plus == F(count_minus, 1) / rho_minus,
            "literal unequal-count inverse-PF cancellation")
    t = F(1, 17)
    slots = 4 * (count_plus + count_minus)
    n = 1 << (slots - 1).bit_length()
    dx, dy = [F(0)] * n, [F(0)] * n
    cursor = 0
    # Distinct local implementations use disjoint four-copy slots. On the
    # diagonal x=y=t, q_plus=x_a*x_b-y_c*y_d and q_minus has opposite roles.
    for count, rho, orientation in ((count_plus, rho_plus, 1),
                                    (count_minus, rho_minus, -1)):
        for _ in range(count):
            a, b, c, d = range(cursor, cursor + 4)
            if orientation == 1:
                dx[a] = dx[b] = t / rho
                dy[c] = dy[d] = -t / rho
            else:
                dy[a] = dy[b] = t / rho
                dx[c] = dx[d] = -t / rho
            cursor += 4
    require(cursor == slots and any(dx) and any(dy),
            "independent unsymmetrized slots have nonzero sources")
    require(sum(dx) == sum(dy) == 0, "collective material source cancels exactly")
    # Explicitly average all 512 cyclic shifts for every physical/padded slot.
    sym_x = [sum(dx[(i + j) % n] for j in range(n)) / n for i in range(n)]
    sym_y = [sum(dy[(i + j) % n] for j in range(n)) / n for i in range(n)]
    require(not any(sym_x) and not any(sym_y),
            "every independent material-copy source vanishes after the paid twirl")
    require(2 * t / rho_plus != 0,
            "a separate twirl inside one local report would not close its source")
    require(2 * t * (count_plus - count_minus) != 0,
            "omitting the original inverse-PF weight fails the cancellation")

    z, tau = Q(F(1, 2**20)), p**2 / 4096
    ell, band_a = 4 * p**3, 4 * p**3 * (1 + p**6)
    qq, rr = 1 - z * ell, 1 - z * band_a
    r0 = 1 - qq * rr
    cq = -8 * z * tau * p**6 * (rr + qq * p**6)
    require(r0.sign() > 0 and (Q(F(1, 2)) - r0).sign() > 0,
            "original primary report is interior below one half")
    require(cq.sign() < 0, "both original material report channels retained")
    require(all(cq * v == 0 for v in sym_x + sym_y),
            "exact original report coefficient multiplies all zero slot sources")
    return {"actual_count_values": [count_plus, count_minus],
            "actual_count_total": total, "site_count": sites,
            "rho": [str(rho_plus), str(rho_minus)],
            "independent_used_copies": slots, "padded_copies": n,
            "report_r0_Qp": r0.text(), "native_material_coefficient_Qp": cq.text(),
            "all_independent_sources_zero": True,
            "local_only_and_missing_weight_countercontrols": True,
            "scope": "two-density algebra fixture; no new primary root claim"}


def matrix(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def bilinear(h, x, y):
    return sum(x[i] * h[i][j] * y[j]
               for i in range(len(x)) for j in range(len(y)))


def multigroup_hessian_control():
    n, m = 4, 2
    size = n + m
    gradient = [F((-1)**i * (i + 2), 13) for i in range(size)]
    h = [[F((i + 1) * (j + 1) + (i - j)**2 + (-1)**(i + j), 19)
          for j in range(size)] for i in range(size)]
    avg_g = [F(0)] * size
    avg_h = matrix(size)
    for shift_n, shift_m in itertools.product(range(n), range(m)):
        permutation = [(i + shift_n) % n for i in range(n)]
        permutation += [n + (j + shift_m) % m for j in range(m)]
        for i in range(size):
            avg_g[i] += gradient[permutation[i]] / (n * m)
            for j in range(size):
                avg_h[i][j] += h[permutation[i]][permutation[j]] / (n * m)
    require(all(v == sum(gradient[:n]) / n for v in avg_g[:n]),
            "first group independent derivative is its diagonal derivative/N")
    require(all(v == sum(gradient[n:]) / m for v in avg_g[n:]),
            "second group independent derivative is its diagonal derivative/N")
    require(all(avg_h[i][j] == avg_h[0][(j - i) % n]
                for i in range(n) for j in range(n)), "cyclic Hessian blocks")
    require(all(avg_h[i][n+j] == avg_h[0][n]
                for i in range(n) for j in range(m)), "cross-group blocks constant")
    require(sum(avg_h[0][:n]) == sum(h[i][j] for i in range(n) for j in range(n)) / n,
            "uniform-mode Hessian equals diagonal Hessian/N")
    relative = [F(1), F(-1), F(0), F(0), F(0), F(0)]
    other = [F(0)] * n + [F(2), F(3)]
    uniform = [F(1)] * n + [F(0)] * m
    require(bilinear(avg_h, relative, other) == 0,
            "relative mode decouples from every other resource group")
    require(bilinear(avg_h, relative, uniform) == 0,
            "relative mode decouples from its uniform mode")
    require(bilinear(avg_h, relative, relative) != 0,
            "relative Hessian is not erased by source symmetrization")
    return {"group_sizes": [n, m], "arbitrary_nonzero_gradient_formula": True,
            "block_circulant": True, "cross_group_uniform_modes_only": True,
            "relative_Hessian_not_zero": True}


def entropy_and_abort_control():
    # Analytic cancellation coefficients; logarithms need not be approximated
    # to show the first-order identities at a uniform alphabet.
    derivatives = [F(1, 5), F(-2, 5), F(3, 5), F(-2, 5)]
    report_jets = [F(2, 7), F(0), F(-5, 11), F(0)]
    require(sum(derivatives) == 0, "normalized complete flag variation")
    flag_entropy_log_coefficient = -sum(derivatives)
    readiness_entropy_coefficient = sum(derivatives)
    report_coefficient = sum(report_jets) / 4
    require(flag_entropy_log_coefficient == readiness_entropy_coefficient == 0,
            "uniform flags and matched ready/abort reports cancel all weight sources")
    require(derivatives[0] + derivatives[2] != 0,
            "success readiness genuinely varies in the hostile normal direction")
    require(report_coefficient != 0,
            "matching abort does not erase the genuine report derivative")

    with localcontext() as ctx:
        ctx.prec = 70
        phi = (Decimal(1) + Decimal(5).sqrt()) / 2
        def entropy(q):
            return -(q*q.ln() + (1-q)*(1-q).ln()) / phi.ln()
        a, b = Decimal(3)/16, Decimal(5)/16
        conditional = (entropy(a) + entropy(b)) / 2
        averaged = entropy((a+b)/2)
        require(averaged > conditional,
                "entropy of averaged report differs from retained-label conditional entropy")
        gap = str(averaged - conditional)
        # The signs are analytic: h'(r0)>0 and h''(r0)<0 for r0<1/2.
        r0, epsilon = F(1, 4), F(1, 32)
        require(0 < r0 - 2*epsilon < r0 + 2*epsilon < 1,
                "linear-difference two-qubit effect strictly positive")
        require(0 < r0 < r0 + epsilon < F(1, 2),
                "antisymmetric-projector effect strictly positive")
    return {"uniform_flag_source_zero": True,
            "matched_abort_weight_source_zero": True,
            "nonzero_readiness_derivative": str(derivatives[0] + derivatives[2]),
            "remaining_true_report_coefficient": str(report_coefficient),
            "entropy_average_gap_decimal_diagnostic": gap,
            "relative_binary_CQ_curvature_both_signs": True,
            "entropy_gap_scope": "strict sign also follows analytically from entropy concavity"}


def own_price_control(Q, p):
    sites = 256
    # m(t)=sqrt(1-t²)(sqrt(p)|1>+p|14>)+t|2> is normalized.
    require(p + p*p == 1, "original clock/slack normalization")
    # Neither |0> nor |15> occurs, so both exact LEFT clock moments vanish
    # for all t, while <A>=(p sqrt(1-t²)+t)^2/(2S).
    derivative = p / sites
    require(derivative.sign() > 0, "positive own-price off-code source survives")
    # An identical additive own charge is already invariant under every shift.
    n = 4
    diagonal_derivative = n * derivative
    require(diagonal_derivative / n == derivative,
            "transitivity equalizes but cannot erase identical input prices")
    return {"clock_moments_identically_zero": True,
            "complete_RIGHT_Gram_preserved_by_local_normalization": True,
            "actual_positive_observable_price_derivative_Qp": derivative.text(),
            "independent_input_price_residual_not_erased": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    pins_path = here / "SOURCE_PINS.json"
    pins = json.loads(pins_path.read_text())
    for item in pins["sources"]:
        data = subprocess.check_output(
            ["git", "-C", str(args.repo), "show", pins["source_ref"] + ":" + item["path"]]
        )
        require(hashlib.sha256(data).hexdigest() == item["sha256"],
                "historical source pin: " + item["path"])
    arithmetic_pin = next(item for item in pins["sources"]
                          if item["path"] == pins["native_arithmetic"])
    require(hashlib.sha256((args.repo / pins["native_arithmetic"]).read_bytes()).hexdigest()
            == arithmetic_pin["sha256"],
            "current imported arithmetic equals the pinned historical source")
    Q, p = load_quadratic_field(args.repo, pins["native_arithmetic"])
    result = {
        "status": "PASS",
        "source_ref": pins["source_ref"],
        "source_count": len(pins["sources"]),
        "source_verification_mode": "git show source_ref:path; imported arithmetic additionally current-hash checked",
        "proof_sha256": hashlib.sha256((here / "TRANSITIVE_RESOURCE_PREPARATION.md").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_pins_sha256": hashlib.sha256(pins_path.read_bytes()).hexdigest(),
        "controlled_shift": controlled_shift_control(),
        "material_source": actual_weight_source_control(Q, p),
        "multigroup_hessian": multigroup_hessian_control(),
        "entropy_and_abort": entropy_and_abort_control(),
        "own_input_price": own_price_control(Q, p),
        "scope": {
            "all_independent_downstream_prep_rows": "analytic theorem on product inputs",
            "fixed_collar_moments": "required; optional paid boundary routing stated",
            "programme_group": "requires companion full-normal diagonal source lemma",
            "arbitrary_entangling_bank_tangents": False,
            "own_input_price_source_eliminated": False,
            "native_resource_supply_or_task_selected": False,
            "GR_closed": False,
        },
    }
    destination = args.output or here / "CHECK_RESULT.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
