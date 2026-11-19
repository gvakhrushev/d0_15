"""Exact first-digit partition of the original selector and its source direction."""

from fractions import Fraction as F
import json
from pathlib import Path
import subprocess

import mpmath as mp


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
PRIMARY = "a03c0e1f0"
RECEIPT = (
    "02_REGISTRY/research/sources/d0_gr_2026-11-18/followups/"
    "2026-11-19/metric/selector36_compilation_result.json"
)


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def split_actual_selector():
    receipt = json.loads(subprocess.check_output(
        ["git", "show", f"{PRIMARY}:{RECEIPT}"], cwd=REPO,
    ))
    allocations = receipt["allocations"]
    # A leading zero spends one cost unit; its exact-hit suffix has cost 35.
    older, current = 0,1
    for _ in range(36):
        older,current = current,older+current
    running = older
    require(running == receipt["overshoot_words"], "first-zero prefix rank boundary")
    rows = []
    for count in allocations:
        low = min(running,count)
        rows.append([low,count-low])
        running -= low
    expected = [[5644800,0],[4939200,0],[4346352,44048],[0,3087000],
                [0,1580544],[0,548800],[0,115200],[0,11025]]
    require(rows == expected and running == 0, "all eight executed address buckets")
    return allocations, rows


def bound_gap_and_source(rows):
    mp.iv.dps = 55
    p = (mp.iv.sqrt(5)-1)/2
    r = p**2
    scales = p**35,p**34
    odd = [sum(row[x] for row in rows[::2])*scales[x] for x in (0,1)]
    even = [sum(row[x] for row in rows[1::2])*scales[x] for x in (0,1)]
    baseline = [odd[x]*r+even[x]*(1-r) for x in (0,1)]
    baseline_slope = (odd[0]-even[0])-(odd[1]-even[1])
    require(baseline_slope.a > 0, "minimum of the common raw baseline at p^2")
    worst_gap = baseline[0]-baseline[1]-mp.iv.mpf(".01")*sum(odd+even)
    require(worst_gap.a > mp.iv.mpf(".08"), "strict first-digit conditional gap")
    ln_phi = -mp.iv.ln(p)
    minimum = mp.iv.mpf(".32") * rows[0][0] * p**36/ln_phi
    require(minimum.a > mp.iv.mpf(".112"), "visible source lower bound")
    return ".08", ".112"


def main():
    allocations, rows = split_actual_selector()
    dx = [F(0)]*8
    dx[0],dx[3] = F(1),-F(allocations[0],allocations[3])
    require(sum(F(n)*v for n,v in zip(allocations,dx)) == 0, "same late marginal")
    expected = set((sum(n[x]*v for n,v in zip(rows,dx)) for x in (0,1)))
    require(expected == {F(allocations[0]),-F(allocations[0])}, "strict earlier conditional drift")
    min_gap, min_score = bound_gap_and_source(rows)
    print(json.dumps({
        "status":"PASS",
        "first_digit_split_of_the_actual_selector36":rows,
        "slope_of_setting_4_when_setting_1_has_unit_slope":str(dx[3]),
        "late_marginal_derivative":"0",
        "conditional_gap_lower_bound_times_actual_eta":min_gap,
        "extra_record_source_lower_bound_times_actual_eta_squared":min_score,
        "visible_direction_has_native_admission_proved":False,
        "GR_closed":False,
    },indent=2))


if __name__ == "__main__":
    main()
