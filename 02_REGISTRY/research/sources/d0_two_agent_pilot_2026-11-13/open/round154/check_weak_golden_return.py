"""Verify one finite weak Golden word and its centered site-price source."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "open/round153"))
import check_positive_gain_site_bound as strong

I, O = strong.I, strong.O
PINS = {
    "open/round153/check_positive_gain_site_bound.py":
        "5c5f1257327de26ae0022e683441596858aa90ff77deef45db9583b57ae48d0c",
    "open/round153/RESULT.json":
        "ea8e6e355a32b5c9d8676c6a56e00a88d78e4159630317dceded9d7ef4706e21",
    "direct/round77/equations/ADDRESS_PREPARATION_RU.md":
        "caeb32e605fa4f78ac41e608e04e0f4a87c99d2ad88193f90c5eacb37fa32745",
}
G_COUNT_INCLUDING_BIRTH = 130_967
PROBE_COUNT = 108_000_000
MASK = 208


def complex_product(left, right):
    a, b = left
    c, d = right
    return a*c-b*d, a*d+b*c


def golden_power(p, exponent):
    acc = I(1.), I(0.)
    square = p.sqrt(), p
    while exponent:
        if exponent % 2:
            acc = complex_product(acc, square)
        exponent //= 2
        if exponent:
            square = complex_product(square, square)
    return acc


def actual_score(a, da, b, db, multiplicity):
    score = multiplicity[:, None]*(a*db-b*da)/(a+b)
    by_mask = sum((score[tag] for tag in range(score.lo.shape[0])), I(0.))
    by_mask_abs = sum((strong.source.absolute(score[tag]) for tag in range(score.lo.shape[0])), I(0.))
    O.require(by_mask[MASK-1].hi < np.min(np.delete(by_mask.lo,MASK-1)),
              "strongest negative centered SITE parity")
    O.require(by_mask[MASK-1].hi < -.00003180870, "negative centered SITE score")
    return by_mask[MASK-1], by_mask_abs[MASK-1]


def main():
    for name, digest in PINS.items():
        O.require(hashlib.sha256((PILOT/name).read_bytes()).hexdigest() == digest,"pinned source")
    p, q, dq, multiplicity, _, _ = strong.physical_site()
    logphi = -O.logarithm(p)
    cosine, sine = golden_power(p,G_COUNT_INCLUDING_BIRTH)
    delta = cosine.square()-sine.square()
    O.require(cosine.lo > 0 and sine.lo > 0 and delta.lo > 0 and delta.hi < .02,
              "first-quadrant weak pointer and positive contrast")
    f = I(np.array([[bin(mask & x).count("1") % 2 for x in range(256)]
                    for mask in range(1,256)]))
    not_f = I(1.)-f
    a, b = strong.parity_sum(q[:, None, :],not_f),strong.parity_sum(q[:, None, :],f)
    da, db = strong.parity_sum(dq[:, None, :],not_f),strong.parity_sum(dq[:, None, :],f)
    score, abs_score = actual_score(a,da,b,db,multiplicity)
    loading = PROBE_COUNT*delta
    quadratic = PROBE_COUNT*delta.square()
    r = I.rational(Q(49,100))
    other = I(1.)-r
    h = -(r*O.logarithm(r)+other*O.logarithm(other))/logphi
    margin = O.logarithm(r)/logphi-other+2*h
    O.require(margin.lo > .88 and logphi.lo > .48, "strict one-step gain margin")
    gain_lower = margin-4*quadratic
    dephase_bound = quadratic/2
    mi_error = 10*quadratic*abs_score
    free = loading*score+I(-mi_error.hi,mi_error.hi)
    O.require(gain_lower.lo > .85, "all weak-reading raw gains")
    O.require(dephase_bound.hi < .0031, "averaged trace/diamond memory error")
    O.require(free.hi < -.025 and free.lo > -.026, "centered finite negative source")
    print(json.dumps({
        "round": "B154",
        "pinned_source_hashes": PINS,
        "mask": MASK,
        "fresh_pointers": PROBE_COUNT,
        "G_per_pointer_including_birth": G_COUNT_INCLUDING_BIRTH,
        "CX_per_pointer": 3,
        "positive_G_and_CX_letters_including_birth": PROBE_COUNT*(G_COUNT_INCLUDING_BIRTH+3),
        "delta": O.bounds(delta),
        "linear_loading": O.bounds(loading),
        "quadratic_loading": O.bounds(quadratic),
        "conditional_site_source": O.bounds(score),
        "abs_conditional_site_source": O.bounds(abs_score),
        "raw_Info_on_weak_reads_lower": float(gain_lower.lo),
        "averaged_memory_diamond_error_upper": float(dephase_bound.hi),
        "C1_price_source_at_reference_after_old_scalar_centering": O.bounds(free),
        "literal_fixed_pointer_letter_counts_only": True,
        "native_tariff_and_clock_selection_proven": False,
        "GR_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
