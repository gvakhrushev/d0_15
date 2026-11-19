"""Replay EIGHT's actual selector masses and the strict input-curvature test."""

from fractions import Fraction as F
import json
from pathlib import Path
import runpy
import subprocess

import mpmath as mp


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
PRIMARY = "a03c0e1f0"
SELECTOR = (
    "02_REGISTRY/research/sources/d0_gr_2026-11-18/followups/"
    "2026-11-19/metric/selector36_compilation_result.json"
)


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def selector_test():
    source = json.loads(subprocess.check_output(
        ["git", "show", f"{PRIMARY}:{SELECTOR}"], cwd=REPO,
    ))
    owner = runpy.run_path(str(HERE.parent / "round170/check_golden_mask_reference.py"))
    add, sub, mul, powers = (
        owner["add"], owner["subtract"], owner["multiply"], owner["power_table"](38)
    )
    one = owner["ONE"]

    n = source["cut"]
    exact, overshoot = 1, 0
    for _ in range(n):
        exact, overshoot = exact + overshoot, exact
    require((exact, overshoot) == (source["exact_hit_words"], source["overshoot_words"]),
            "pinned EIGHT cost cut is complete")
    active = sum(source["allocations"])
    require(active == source["active_words"] and exact > active > 0, "all eight allocations")
    born = [(k * powers[n][0], k * powers[n][1]) for k in source["allocations"]]
    born_total = mul((active, 0), powers[n])
    remaining = add(mul((exact-active, 0), powers[n]), mul((overshoot, 0), powers[n+1]))
    require(add(born_total, remaining) == one, "positive complete Born address law")

    # Event Info and the original written record first cancel. The new literal
    # 0/10 echo of the already known overshoot flag then gives p or p².
    corrected = [mul((k, 0), powers[1]) for k in source["allocations"]]
    corrected_zero = add(mul((exact-active, 0), powers[1]), mul((overshoot, 0), powers[2]))
    normalizer = add(mul((exact, 0), powers[1]), mul((overshoot, 0), powers[2]))
    require(corrected == [mul(normalizer, weight) for weight in born]
            and corrected_zero == mul(normalizer, remaining), "all nine relative masses restored")
    require(mul((exact+overshoot, 0), born_total) != (active, 0),
            "no echo produces the uniform-leaf rather than the Born macro law")

    # Galois conjugation p -> -1-p sends every positive even power to positive.
    # The originally required exact-to-overshoot factor p has negative conjugate.
    conjugate_p = (-1, -1)
    conjugate_p_sq = mul(conjugate_p, conjugate_p)
    conjugate_zero = (remaining[0]-remaining[1], -remaining[1])
    require(conjugate_p_sq == sub(one, conjugate_p)
            and owner["sign"](conjugate_p) < 0
            and owner["sign"](conjugate_p_sq) > 0, "even-exponent obstruction")
    require(owner["sign"](conjugate_zero) < 0, "real inactive EIGHT mass fails positivity")

    mp.iv.dps = 65
    gp = (mp.iv.sqrt(5)-1)/2
    raw_active = active*gp**n
    count_active = F(active, exact+overshoot)
    require(raw_active.a > mp.iv.mpf(".6085") and raw_active.b < mp.iv.mpf(".6087"),
            "true active selector mass")
    require(F(".5197") < count_active < F(".5200"), "uniform leaf active mass")
    return {
        "exact_and_overshoot_words": [exact, overshoot],
        "existing_setting_counts": source["allocations"],
        "active_uniform_leaf_fraction": str(count_active),
        "active_born_interval": [".6085", ".6087"],
        "matched_sector_priors_with_one_overshoot_echo_nu_1": 9,
        "positive_integer_price_even_power_obstruction": True,
    }


def curvature_test():
    # Exact visible-model fixture: mixed-sign field directions, eight active
    # settings and an inactive old branch. These are hypothetical fixed rates.
    values = [F(6+j, 24+j) for j in range(1, 9)]
    slopes = [F((-1)**j * (j+1), 64) for j in range(1, 9)]
    records = []
    for nu in (1, 2):
        rows = [(F(1), F(0), F(3, 11))]
        for j, (q, slope) in enumerate(zip(values, slopes), start=1):
            rows += [(q, slope, F(j+1, j+4)), (1-q, -slope, F(2*j+1, j+7))]
        mass = [k / probability**nu for probability, _, k in rows]
        curvature = sum(
            k*nu*(nu+1)*slope**2/probability**(nu+2)
            for probability, slope, k in rows
        )
        score_sq = sum(
            value * (slope/probability)**2
            for value, (probability, slope, _) in zip(mass, rows)
        )
        require(curvature == nu*(nu+1)*score_sq and score_sq > 0, "strict affine curvature")
        q, dq = values[0], F(1)
        w1, w0 = F(3, 5)/q**nu, F(2, 3)/(1-q)**nu
        dw1, dw0 = -nu*w1*dq/q, nu*w0*dq/(1-q)
        require(dw1*(w0+w1)-w1*(dw0+dw1) < 0, "economic bit opposes the Born slope")
        # Restore M=P by the field-dependent model K=P^(nu+1).
        # These are the first and second derivatives of k times B=-log K.
        for probability, slope, _ in rows:
            score = slope/probability
            price_slope = -(nu+1)*score
            price_curvature = (nu+1)*score**2
            term = (price_slope+nu*score)**2-price_curvature+nu*score**2
            require(term == 0, "the explicit moving price cancels all curvature terms")
        records.append({"nu": nu, "mixed_affine_slice_strict": True, "visible_bit_derivative_negative": True})
    return records


def check_root_probe():
    # Known sector sums in a normalized finite scalar fixture.
    a0, a1, u0, u1 = F(9, 7), F(4, 7), F(6, 5), F(4, 5)
    m0, m1, m2, m3 = [a0*u0**k + a1*u1**k for k in range(4)]
    discriminant = m0*m2-m1**2
    require(discriminant == a0*a1*(u0-u1)**2 > 0, "two actual groups")
    root_sum = (m0*m3-m1*m2)/discriminant
    root_product = (m1*m3-m2**2)/discriminant
    require(root_sum == u0+u1 and root_product == u0*u1, "four absolute comparisons")
    require((m1-u1*m0)/(u0-u1) == a0 and (u0*m0-m1)/(u0-u1) == a1,
            "absolute prior recovered")
    report_share = (1-m1/(u0*m0))/(1-u1/u0)
    require(report_share == a1/(a0+a1), "two comparisons with calibrated tail")
    p = (mp.iv.sqrt(5)-1)/2
    require((1/(1-9*p**2/4)).b < mp.iv.mpf("7.12"), "certified tail condition")
    return {
        "moment_determinant": str(discriminant),
        "recovered_economic_share": str(report_share),
        "share_error_multiplier_upper_bound": "7.12",
    }


def main():
    print(json.dumps({
        "status": "PASS",
        "primary": PRIMARY,
        "actual_selector": selector_test(),
        "exact_fixed_tariff_model_checks": curvature_test(),
        "field_independent_tail_probe_fixture": check_root_probe(),
        "original_book03_price_derived": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
