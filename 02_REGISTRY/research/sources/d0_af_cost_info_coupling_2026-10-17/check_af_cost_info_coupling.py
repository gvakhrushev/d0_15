"""Literal AF-record price versus the Einstein-Hilbert interior source.

The owned second-record price is a function of golden constants and of
external probe coordinates.  This module differentiates that price on a
lapse, on a shift, and on a matter amplitude, and differentiates the
Einstein-Hilbert bulk density on the same three directions.  It does not
set one derivative equal to the other.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp
from mpmath import mp


CHECKS: list[str] = []


def require(condition: object, name: str) -> None:
    CHECKS.append(name)
    if condition is True:
        return
    if condition is False or condition is None:
        raise AssertionError(name)
    if isinstance(condition, sp.Basic):
        raise AssertionError(name)
    if not condition:
        raise AssertionError(name)


def is_zero(expr) -> bool:
    return sp.simplify(expr) == 0


def _curvature(metric, coords):
    n = len(coords)
    g = sp.Matrix(metric)
    ginv = sp.simplify(g.inv())
    gamma = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for rho in range(n):
        for mu in range(n):
            for nu in range(mu, n):
                acc = 0
                for sig in range(n):
                    acc += ginv[rho, sig] * (
                        sp.diff(g[nu, sig], coords[mu])
                        + sp.diff(g[mu, sig], coords[nu])
                        - sp.diff(g[mu, nu], coords[sig])
                    )
                value = sp.simplify(acc / 2)
                gamma[rho][mu][nu] = value
                gamma[rho][nu][mu] = value
    ricci = sp.zeros(n)
    for nu in range(n):
        for rho in range(nu, n):
            value = 0
            for lam in range(n):
                value += sp.diff(gamma[lam][nu][rho], coords[lam])
                value -= sp.diff(gamma[lam][nu][lam], coords[rho])
                for sig in range(n):
                    value += gamma[lam][lam][sig] * gamma[sig][nu][rho]
                    value -= gamma[lam][rho][sig] * gamma[sig][nu][lam]
            ricci[nu, rho] = sp.simplify(value)
            ricci[rho, nu] = ricci[nu, rho]
    scalar = sp.simplify(sum(ginv[i, j] * ricci[i, j] for i in range(n) for j in range(n)))
    einstein = sp.simplify(ricci - sp.Rational(1, 2) * scalar * g)
    return g, ginv, scalar, einstein


def _raised_contraction(ginv, einstein, dg):
    raised = sp.simplify(ginv * einstein * ginv)
    return sp.simplify(sum(raised[i, j] * dg[i, j] for i in range(4) for j in range(4)))


def _words(cost: int) -> list[tuple[int, ...]]:
    found: list[tuple[int, ...]] = []

    def walk(used: int, acc: list[int]) -> None:
        if used == cost:
            found.append(tuple(acc))
            return
        if used + 1 <= cost:
            acc.append(0)
            walk(used + 1, acc)
            acc.pop()
        if used + 2 <= cost:
            acc.append(1)
            walk(used + 2, acc)
            acc.pop()

    walk(0, [])
    return found


def _center(word: tuple[int, ...], p) -> tuple:
    lo = [mp.mpf(0)] * 4
    hi = [mp.mpf(1)] * 4
    for index, bit in enumerate(word):
        slot = index % 4
        width = hi[slot] - lo[slot]
        cut = lo[slot] + p * width
        if bit == 0:
            hi[slot] = cut
        else:
            lo[slot] = cut
    return tuple((lo[i] + hi[i]) / 2 for i in range(4))


def _fibonacci(n: int) -> int:
    a, b = 1, 1
    if n <= 2:
        return 1
    for _ in range(n - 2):
        a, b = b, a + b
    return b


def run() -> dict:
    CHECKS.clear()
    mp.dps = 40
    p = (mp.sqrt(5) - 1) / 2
    phi = 1 / p
    log_phi = mp.log(phi)
    require(abs((p + p ** 2) - 1) < mp.mpf("1e-30"), "golden_partition")

    def probabilities(effect):
        weight = mp.sqrt(p) * p
        root = mp.sqrt(1 - effect)
        branch = mp.sqrt(effect)
        fine = [
            (weight * root + branch / mp.sqrt(2)) ** 2,
            (weight * root - branch / mp.sqrt(2)) ** 2,
            weight * weight * (1 - effect),
            p ** 4 * (1 - effect),
            p ** 4 * (1 - effect),
        ]
        return fine

    def f0(effect):
        fine = probabilities(effect)
        return 3 + fine[3] + fine[4] + sum(q * mp.log(q) for q in fine) / log_phi

    def shannon_over_log_phi(effect):
        fine = probabilities(effect)
        return -sum(q * mp.log(q) for q in fine) / log_phi

    probe = p ** 2
    fine_at_gate = probabilities(probe)
    require(abs(sum(fine_at_gate) - 1) < mp.mpf("1e-30"), "type0_probabilities_sum_to_one")
    f0_prime = mp.diff(f0, probe)
    kappa = 2 * p ** 5 * f0_prime
    a_inf = phi / mp.sqrt(5)
    product = kappa * a_inf
    require(mp.mpf("0.58484") < f0_prime < mp.mpf("0.58485"), "f0_prime_in_owner_interval")
    require(
        abs(product - mp.mpf("0.0763194856457334")) < mp.mpf("1e-16"),
        "probe_coefficient_reproduced",
    )
    rel = f0(probe)
    shan = shannon_over_log_phi(probe)
    require(abs(rel - shan) > mp.mpf("1e-6"), "relative_entropy_is_not_von_neumann")
    central_cost = -6 * p ** 10
    require(abs(central_cost - f0_prime) > mp.mpf("1e-3"), "central_cost_is_not_f0_prime")

    printed = {
        8: ("0.4967219", "0.3206100", "0.2351376"),
        12: ("0.4908399", "0.3212103", "0.2417979"),
        16: ("0.4962472", "0.3292365", "0.2471890"),
        20: ("0.4983187", "0.3313064", "0.2474902"),
        24: ("0.4985168", "0.3317396", "0.2481661"),
    }
    expected_counts = {8: 34, 12: 233, 16: 1597, 20: 10946, 24: 75025}
    for n, (e0, e2, e01) in printed.items():
        words = _words(n)
        require(len(words) == expected_counts[n] == _fibonacci(n + 1), f"count_{n}")
        mass = mp.mpf(0)
        m0 = m1 = m01 = mp.mpf(0)
        for word in words:
            center = _center(word, p)
            weight = p ** n
            mass += weight
            m0 += weight * center[0]
            m1 += weight * center[0] ** 2
            m01 += weight * center[0] * center[1]
        require(abs(m0 / mass - mp.mpf(e0)) < mp.mpf("5e-8"), f"mean_x0_{n}")
        require(abs(m1 / mass - mp.mpf(e2)) < mp.mpf("5e-8"), f"mean_x0sq_{n}")
        require(abs(m01 / mass - mp.mpf(e01)) < mp.mpf("5e-8"), f"mean_x0x1_{n}")

    z = mp.power(2, -20)
    q = z / (1 - z)
    ratio = -mp.polylog(3, -q) / -mp.polylog(2, -q)
    beta_lambda = 6 * ratio
    require(abs(beta_lambda - mp.mpf("6.000000715256187")) < mp.mpf("1e-14"), "ir_polylog_ratio")

    # Owned price arguments.  N, shift and psi are not among them.
    u0, t_probe, n_cell = sp.symbols("u0 t N_cell", real=True)
    blank = sp.Integer(6)
    # Linearised owned probe response: one address, coefficient kept symbolic
    # and then specialised.  The metric parameters never enter.
    af_price = blank + t_probe * u0
    lapse, shift, matter, radius = sp.symbols("N epsilon psi a", positive=True)
    require(is_zero(sp.diff(af_price, lapse)), "af_price_lapse_partial_is_zero")
    require(is_zero(sp.diff(af_price, shift)), "af_price_shift_partial_is_zero")
    require(is_zero(sp.diff(af_price, matter)), "af_price_matter_partial_is_zero")
    require(sp.diff(af_price, u0) == t_probe, "af_price_responds_to_its_own_probe")
    # Multiplying the blank price by a cell count is a different functional.
    repeated = blank * n_cell + t_probe * u0
    require(sp.diff(repeated, n_cell) == blank, "repeated_baseline_sees_cell_count")
    require(is_zero(sp.diff(af_price, n_cell)), "owned_baseline_ignores_cell_count")

    t, x, theta, phi = sp.symbols("t x theta phi", real=True)
    metric = sp.diag(-(lapse ** 2), 1, radius ** 2, radius ** 2 * sp.sin(theta) ** 2)
    g, ginv, scalar, einstein = _curvature(metric, (t, x, theta, phi))
    require(is_zero(scalar - 2 / radius ** 2), "sphere_product_scalar")
    dg_lapse = sp.zeros(4)
    dg_lapse[0, 0] = sp.diff(-(lapse ** 2), lapse)
    lapse_contraction = _raised_contraction(ginv, einstein, dg_lapse)
    require(is_zero(lapse_contraction + 2 / (lapse * radius ** 2)), "lapse_einstein_contraction")
    require(not is_zero(lapse_contraction), "lapse_einstein_contraction_not_identically_zero")
    sqrt_g = sp.simplify(sp.sqrt(-g.det()))
    bulk = sp.simplify(scalar * sqrt_g)
    angle = sp.integrate(sp.integrate(bulk, (theta, 0, sp.pi)), (phi, 0, 2 * sp.pi))
    require(is_zero(angle - 8 * sp.pi * lapse), "lapse_bulk_integral")
    require(not is_zero(sp.diff(angle, lapse)), "lapse_bulk_derivative_nonzero")

    metric_shift = sp.zeros(4)
    metric_shift[0, 0] = -(lapse ** 2)
    metric_shift[0, 1] = metric_shift[1, 0] = shift
    metric_shift[1, 1] = 1
    metric_shift[2, 2] = radius ** 2
    metric_shift[3, 3] = radius ** 2 * sp.sin(theta) ** 2
    gs, ginvs, scalars, einsteins = _curvature(metric_shift, (t, x, theta, phi))
    dg_shift = sp.zeros(4)
    dg_shift[0, 1] = dg_shift[1, 0] = 1
    shift_contraction = _raised_contraction(ginvs, einsteins, dg_shift)
    expected_shift = -2 * shift / (radius ** 2 * (lapse ** 2 + shift ** 2))
    require(is_zero(shift_contraction - expected_shift), "shift_einstein_contraction")
    require(not is_zero(shift_contraction.subs(shift, 1)), "shift_source_nonzero_off_the_zero_section")
    # At zero shift this particular contraction vanishes.  That one point is
    # not an identification: the two functions of the shift still differ.
    require(is_zero(shift_contraction.subs(shift, 0)), "shift_source_vanishes_at_zero")
    require(not is_zero(shift_contraction - sp.diff(af_price, shift)), "shift_functions_are_not_the_same")

    matter_action = matter ** 2 / 2
    require(not is_zero(sp.diff(matter_action, matter) - sp.diff(af_price, matter)), "matter_sources_differ")
    require(not is_zero(sp.diff(af_price, lapse) - lapse_contraction), "lapse_sources_differ")

    volume_density = blank * sqrt_g
    volume_lapse = sp.diff(volume_density, lapse)
    require(not is_zero(volume_lapse), "blank_times_volume_restores_lapse_source")

    # The forbidden identification would copy the Einstein contraction into
    # the AF derivative.  The receipt records that this copy was not made.
    require(not is_zero(lapse_contraction - sp.diff(af_price, lapse)), "einstein_value_was_not_copied_into_af")
    u_of_lapse = sp.Function("u")
    composed = t_probe * u_of_lapse(lapse)
    require(
        sp.diff(composed, lapse) == t_probe * sp.diff(u_of_lapse(lapse), lapse),
        "chain_rule_splits_probe_from_lapse",
    )
    require(is_zero(sp.diff(t_probe * sp.Integer(0), lapse)), "owned_gate_does_not_define_u_of_lapse")

    receipt = {
        "schema": "d0-af-cost-info-coupling/1",
        "status": "PASS",
        "candidate": True,
        "gr_derived": False,
        "equation_20_closed": False,
        "equation_28_closed": False,
        "coupling_holds": False,
        "sources_coincide": False,
        "literal_metric_partial_of_af_price": "0",
        "lapse_einstein_contraction": str(lapse_contraction),
        "shift_einstein_contraction": str(shift_contraction),
        "matter_partial_of_half_psi_squared": str(sp.diff(matter_action, matter)),
        "af_matter_partial": "0",
        "probe_coefficient": mp.nstr(product, 20),
        "f0_prime": mp.nstr(f0_prime, 20),
        "relative_entropy_at_golden_gate": mp.nstr(rel, 20),
        "von_neumann_over_log_phi_at_golden_gate": mp.nstr(shan, 20),
        "central_cost_probe_derivative": mp.nstr(central_cost, 20),
        "beta_abs_lambda_eff": mp.nstr(beta_lambda, 20),
        "mixed_length_operator_identity_checked": False,
        "observer_argument_present": False,
        "matter_argument_present": False,
        "constant_chosen_to_match_einstein": False,
        "blank_volume_law_cancels": False,
        "route_scope": "owned AF probe price (Jacobian (3),(6) and AF memo (7)); not every future primitive",
        "reopening_hook": "an admitted operation whose Cost-Info arguments include the lapse and a shift, with interior derivatives equal to the Einstein-Hilbert covector plus an independent matter covector",
        "check_count": len(CHECKS),
    }
    require(receipt["coupling_holds"] is False, "coupling_flag_false")
    require(receipt["gr_derived"] is False, "gr_not_derived")
    require(receipt["sources_coincide"] is False, "sources_coincide_false")
    receipt["check_count"] = len(CHECKS)
    return receipt


def main() -> None:
    receipt = run()
    text = json.dumps(receipt, indent=2, ensure_ascii=True)
    out = Path(__file__).with_name("receipt.json")
    out.write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"PASS {receipt['check_count']} {receipt['coupling_holds']}")


if __name__ == "__main__":
    main()
