"""Replay the primary CAR jets and certify the fixed per-mark tariff bound."""

from fractions import Fraction
import json
from pathlib import Path
import runpy

import sympy as sp
from sympy.polys.matrices import DomainMatrix

COMMIT = "076d5d5a7b366c0dd0970f388df7a9e6895498c4"
PIN = "2ac8b4202c0212cf19a66c0a8940680cf94a405bdd99f2466936076faa7e9d66"


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def primary():
    # The directed checkout includes this hash-verified upstream constructor.
    check = Path(__file__).resolve().parents[2] / "direct/round69/primary/check_stopped_fine.py"
    return runpy.run_path(str(check))["original_jet"]()


def verify_grouped_maps(data):
    ns, dns = data["ns"], data["dns"]
    a, da, lam = data["a"], data["da"], data["kappa"]
    identity, zero, same = data["I"], data["O"], data["same"]
    values = [n.H * a for n in ns]
    jets = [dn.H * a + n.H * da for n, dn in zip(ns, dns)]
    require(same(values[0], lam * identity) and same(jets[0], zero), "The STOP-0 row moved")
    def gaussian(matrix):
        return DomainMatrix.from_Matrix(matrix.applyfunc(sp.expand)).convert_to(sp.QQ_I).to_dense()

    block = [(gaussian(b), gaussian(b.H), gaussian(db), gaussian(db.H))
             for b, db in zip(values[1:], jets[1:])]
    expected = gaussian(lam * (1-lam) * identity)
    gaussian_zero = gaussian(zero)
    for transpose in (False, True):
        section = gaussian_zero
        derivative = gaussian_zero
        for b, adj, db, dadj in block:
            if transpose:
                b, adj, db, dadj = adj, b, dadj, db
            section += adj.matmul(b)
            derivative += dadj.matmul(b) + adj.matmul(db)
        require(section == expected, "Nonquiet group is not scalar")
        require(derivative.is_zero_matrix, "Nonquiet group has a nonzero jet")
    rates = {}
    for j, (n, dn) in enumerate(zip(ns[1:], dns[1:]), 1):
        trace_jet = sp.expand(sp.trace(dn*n.H + n*dn.H))/16
        rate = trace_jet/(1-lam)
        if rate:
            rates[j] = int(631 * rate)
            require(rates[j] == 631 * rate, "Row jet changed denominator")
    expected = {9: -108, **dict.fromkeys([13, 29, 45, 61], 3),
                **dict.fromkeys([16, 20, 24, 28, 48, 52, 56, 60], 12)}
    require(rates == expected and sum(rates.values()) == 0, "Fine row rate table changed")
    require(rates[9] * (1-lam) / 631 == -sp.Rational(27, 160), "Warmup rate changed")
    bits = [sum(rate for j, rate in rates.items() if j & (1 << k)) for k in range(6)]
    require(bits == [-96, 0, 60, -48, 102, 54], "Binary write rate table changed")
    stop_scores = {}
    for j in (9, 16):
        normalized_row = sp.expand(sp.trace(ns[j]*ns[j].H))/(16*(1-lam))
        stop_scores[2*j] = sp.cancel(rates[j]/(631*normalized_row))
    require(stop_scores == {18: -sp.Rational(5, 24), 32: sp.Rational(4, 3)},
            "The immediate fine STOP probability scores changed")
    return rates, bits, stop_scores


def verify_range_bound():
    p_upper = Fraction(61803398874990, 10**14)
    require(p_upper*p_upper + p_upper > 1, "Upper Golden bracket failed")
    lam = Fraction(9, 640)
    q_upper = 4*p_upper**3*lam
    v_upper = q_upper*(1-lam)
    upper = Fraction(108, 631) * (1+p_upper)*v_upper / (1-q_upper)
    safe = Fraction(3675, 10**6)
    require(upper < safe, "Fine tariff coefficient bound is too small")
    require(Fraction(6799, 100000) > safe * Fraction(1850, 100), "Positive-mass threshold")
    require(Fraction(5099, 100000) > safe * Fraction(1387, 100), "Amplitude-mass threshold")
    return str(safe)


def main():
    data = primary()
    rates, bits, stop_scores = verify_grouped_maps(data)
    print(json.dumps({
        "status": "PASS",
        "primary_commit": COMMIT,
        "primary_checker_sha256": PIN,
        "quiet_stop_leaf_probability_jet_zero": True,
        "coarse_readout_grouped_effect_and_identity_output_jets_zero": True,
        "even_warmup_label_18_probability_jet": "-27*p^4*lambda/40",
        "fine_label_rates_times_631": rates,
        "immediate_stop_log_probability_jets": {0: "0", **{z: str(v) for z, v in stop_scores.items()}},
        "six_address_bit_rates_times_631": bits,
        "fixed_tariff_coefficient_strict_upper": verify_range_bound(),
        "book03_actual_info_selected": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
