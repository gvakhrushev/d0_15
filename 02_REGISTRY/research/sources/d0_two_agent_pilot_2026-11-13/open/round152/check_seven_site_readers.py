"""Certify the 128 source rows with a quotient of SITE read by seven Golden taps."""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

OWNER = Path(__file__).resolve().parents[2] / "direct/round76/record"
sys.path.insert(0, str(OWNER))
import check_data_geometry as source


def main():
    pin = "a1ecfdae207938aa36e6ef3f9fb314d833f48383d7ff345880c39491d475c830"
    source.require(hashlib.sha256((OWNER/"check_data_geometry.py").read_bytes()).hexdigest() == pin,
                   "original derivative and residual enclosure")
    # One representative per quotient ID, with bit 6 set to zero.
    representatives = np.array([(x & 63) | ((x & 64) << 1) for x in range(128)])
    distances = np.array([[bin(x ^ r).count("1") for x in range(128)] for r in range(128)])
    geo = source.geo
    terms, _, cols, _ = geo.assemble()
    p = geo.heat.P
    prefactors = (-2*p*p, -2*p*p.sqrt())
    a = geo.matrix_ball(terms, [1]*16)
    c = cols, np.full(cols.shape, 5e-17)
    ac = geo.ball_apply(a, c)
    u = geo.ball_apply(a, ac, transpose=True)
    states = [source.sum_ball(c, source.scalar_ball(u, prefactors[0])),
              source.scalar_ball(u, prefactors[1])]
    slopes = np.zeros((2, 256, 128))
    errors = np.zeros_like(slopes)
    for col, idx in enumerate(geo.ACTIVE):
        da = source.derivative_matrix(terms, idx)
        dac = geo.ball_apply(da, c)
        du = source.sum_ball(geo.ball_apply(a, dac, transpose=True),
                             geo.ball_apply(da, ac, transpose=True))
        for branch in range(2):
            mid, rad = source.dot_by_site(states[branch], source.scalar_ball(du, prefactors[branch]))
            slopes[branch, :, col], errors[branch, :, col] = 2*mid, 2*rad

    powers = [p]
    for _ in range(13):
        powers.append(powers[-1]*p)
    values = np.array([float(v.lo+(v.hi-v.lo)/2) for v in powers])
    widths = np.array([1.000001*max(m-float(v.lo), float(v.hi)-m)+1e-290
                       for m, v in zip(values, powers)])
    channel = values[6+distances]
    channel_error = widths[6+distances]

    def multiply(left, right):
        return np.einsum("ik,kj->ij", left, right, optimize=False)

    result = {}
    for branch, (j, e) in enumerate(zip(slopes, errors)):
        partner = representatives ^ 69
        quotient, error = source.sum_ball((j[representatives], e[representatives]),
                                          (j[partner], e[partner]))
        recorded = multiply(channel, quotient)
        uncertainty = (multiply(channel, error)
                       + multiply(channel_error, np.abs(quotient)+error)
                       + 8e-14*multiply(channel, np.abs(quotient)))
        sharp_check = source.selected_minor(quotient, error)
        noisy_check = source.selected_minor(recorded, 1.000001*uncertainty+1e-290)
        result[str(branch)] = {
            "sharp_inverse_defect_under": 1e-8,
            "noisy_inverse_defect_under": .006,
        }
        source.require(sharp_check["certified_inverse_defect"] < 1e-8
                       and noisy_check["certified_inverse_defect"] < .006, "replay bounds")
    print(json.dumps({
        "A76_pinned_rank_source": pin,
        "kernel_mask": 69,
        "golden_targets": 7,
        "positive_CX_letters": 9,
        "joint_probability_rank": 128,
        "old_blank_Fourier_marks_by_port": result,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
