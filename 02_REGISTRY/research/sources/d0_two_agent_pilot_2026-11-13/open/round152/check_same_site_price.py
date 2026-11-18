"""Check the channel, tariff bounds and actual A76 directional SITE scores."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "direct/round76/record"))
import check_noisy_site_price as source

I, O = source.I, source.O

PINS = {
    "direct/round76/record/check_noisy_site_price.py":
        "170f1b51e3f3cb1625c062b658e95782380a1a054328a921549df337b1838123",
    "direct/round76/record/NOISY_SITE_PRICE_RU.md":
        "6fc67bf3838f13be24dc7e34b99dabaac8c3d5da2ccf00fac9e72f5256be1bda",
    "direct/round76/record/DATA_GEOMETRY_RU.md":
        "e446ef984b0a99406319ad9bdd9f0b9ba2c44ecec9eea93c345ac25fb2121cfb",
    "direct/round75/history/TWO_SITE_SOURCE_RU.md":
        "b22c08ca55b1c6996fa58066b01b178f175c6db2ee1ddbceb0ae8ed945bdd29c",
    "open/round149/RESULT.json":
        "2be40017b14c0416317ca3ffeb0e82ee1bc85aee451e32c7b1eb08893459d13e",
    "open/round151/RESULT.json":
        "e913ee80002fee725b805d329a55b275680e0c2ff50fcb741d8e3537a8f72ca3",
}
GAMMA_LOW, GAMMA_HIGH = Q(44, 100), Q(54, 100)
SPLUS_MAX, SMINUS_MAX = Q(8386, 10**6), Q(8903, 10**6)


def check_tariffs(p, logphi):
    r0 = p.square()
    s = I((p * r0).sqrt().lo, .5)
    c = I(3.).sqrt() - 1
    w = (1 + 2*s).sqrt()
    fs = (1 + c*s)/w + c*w
    fss = (2*c - 1 + 3*c*s)/(w*w*w)
    for ratio in (4*logphi*s.square(), logphi*(fs/s - (I(1.) - 4*s.square())*fss)/4):
        O.require(ratio.lo > I.rational(GAMMA_LOW).hi
                  and ratio.hi < I.rational(GAMMA_HIGH).lo, "uniform curvature ratio")
    calibration = I(22.).sqrt()
    O.require(calibration.lo > I.rational(Q(469, 100)).hi
              and calibration.hi < I.rational(Q(47, 10)).lo, "spectral calibration")
    O.require((p + r0).contains(1) and (p - r0 - p*r0).contains(0),
              "Golden normalization and channel contrast")


def positive_part(v):
    return I(np.maximum(0., v.lo), np.maximum(0., v.hi))


def site_scores(p, base, w, dw, fw, bw, u, du, logphi):
    site_ids = np.arange(256)
    masks = np.array([[bin(x & a).count("1") % 2 for x in site_ids]
                      for a in range(256)])
    parity = I(masks)
    mass, slope, py_entropy, splus, sminus, variation = (I(0.) for _ in range(6))
    parity_slopes = I(np.zeros(256))
    for cf in range(2):
        vals, ders = source.owner.actions(cf, w, dw, fw, bw, u, du)
        for j, (value, tangent) in enumerate(zip(vals, ders)):
            blank = j == cf == 0
            for port in ((0, 1) if blank else (1,)):
                scale = -2 * (p.square() if port == 0 else p*p.sqrt())
                z = value*scale + base if blank and port == 0 else value*scale
                dz = tangent*scale
                q = source.sum_at_site(z.square())
                dq = 2*source.sum_at_site(z*dz)
                O.require(np.all(q.lo > 0), "positive sharp SITE masses in every active mark")
                qy = O.reduce_sum(q)
                surprisal = source.ln(qy/q) / logphi
                multiple = I(1.) if blank else 1 + p
                mass = mass + multiple*qy
                dqy = O.reduce_sum(dq)
                slope = slope + multiple*dqy
                for factor in ((I(1.),) if blank else (I(1.), p)):
                    py_entropy = py_entropy - factor*dqy*O.logarithm(factor*qy)/logphi
                splus = splus + multiple*O.reduce_sum(positive_part(dq)*surprisal)
                sminus = sminus + multiple*O.reduce_sum(positive_part(-dq)*surprisal)
                variation = variation + multiple*O.reduce_sum(source.absolute(dq))/2
                terms = parity*dq
                while terms.lo.shape[1] > 1:
                    terms = terms[:, ::2] + terms[:, 1::2]
                parity_slopes = parity_slopes + multiple*terms[:, 0]
    O.require(mass.contains(1) and slope.contains(0), "normalized actual sharp SITE law")
    O.require(splus.hi < I.rational(SPLUS_MAX).lo, "positive surprisal-weighted score")
    O.require(sminus.hi < I.rational(SMINUS_MAX).lo, "negative surprisal-weighted score")
    O.require(py_entropy.hi < I.rational(Q(245225, 10**9)).lo, "old entropy slope")
    bit_slopes = parity_slopes[[1 << j for j in range(8)]]
    contrast = p*p.square()
    bit_round = contrast*O.reduce_sum(bit_slopes)
    negative = contrast*parity_slopes[208]
    O.require(bit_round.lo > 0, "an equal round's printing slope")
    O.require(negative.hi < I.rational(Q(-749, 10**8)).lo, "negative parity printing slope")
    O.require(parity_slopes[208].hi < np.min(np.delete(parity_slopes.lo, 208)),
              "most negative fixed positive-control parity, including constant zero")
    return {
        "D_H_old": O.bounds(py_entropy),
        "D_old_and_sharp_site_TV": O.bounds(variation),
        "S_plus": O.bounds(splus),
        "S_minus": O.bounds(sminus),
        "D_site_bits": [O.bounds(bit_slopes[j]) for j in range(8)],
        "D_native_print_one_full_bit_round": O.bounds(bit_round),
        "D_site_parity_208": O.bounds(parity_slopes[208]),
        "D_native_print_one_parity_208": O.bounds(negative),
    }


def price_bounds():
    rows = {}
    threshold = {(1, "unit"): Q(127, 10000), (1, "spectral"): Q(37, 10000),
                 (2, "unit"): Q(41, 10000), (2, "spectral"): Q(124, 10000)}
    for nu in (1, 2):
        base = Q(2204, 100000)-Q(4344153, 10**9)-nu*Q(245225, 10**9)
        for label, lo, hi in (("unit", Q(1), Q(1)), ("spectral", Q(469, 100), Q(47, 10))):
            a = max(Q(0), nu - lo*GAMMA_LOW)
            b = max(Q(0), hi*GAMMA_HIGH - nu)
            lower = base-a*SPLUS_MAX-b*SMINUS_MAX
            upper_correction = b*SPLUS_MAX+a*SMINUS_MAX
            O.require(lower > threshold[nu, label], "uniform strict lower price")
            rows[f"nu_{nu}_{label}"] = {
                "lower_for_every_equal_round_schedule": str(lower),
                "lower_decimal": float(lower),
                "upper_work_minus_info_slope": str(upper_correction),
            }
    return rows


def main():
    for name, digest in PINS.items():
        O.require(hashlib.sha256((PILOT/name).read_bytes()).hexdigest() == digest,
                  f"pinned source {name}")
    p, z, w, dw, fw, bw, u, du, _ = source.owner.site_vector()
    logphi = -O.logarithm(p)
    check_tariffs(p, logphi)
    print(json.dumps({
        "round": "B152",
        "source_hashes": PINS,
        "actual_outward_scores": site_scores(p, z, w, dw, fw, bw, u, du, logphi),
        "pointwise_curvature_ratio": ["44/100", "54/100"],
        "scalar_tariff_tests": price_bounds(),
        "absolute_Book03_cost_info_proven": False,
        "GR_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
