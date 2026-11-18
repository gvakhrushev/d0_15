"""Same local coframe ray for the original H+J+R and the A74 port component."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import json
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "curvature"))
import check_local_coframe_source as heat
import check_work_memory as work

I = heat.I


def require(ok, label):
    if not ok:
        raise ValueError(label)


def material_ray():
    car = heat.car
    p = heat.P
    rows = np.array(car.fourier_numerators())
    counts = car.actual_counts(heat.ROOT)
    weights = {x: p*p*p*I.rational(Fraction(256*n, sum(counts))).sqrt()
               for x, n in zip(car.SITES_LIST, counts)}
    amplitude = defaultdict(lambda: I(np.zeros(128)))
    local = defaultdict(lambda: I(np.zeros(128)))
    vacuum = ((1, p.sqrt()), (14, p))
    for i, x in enumerate(car.SITES_LIST):
        row = I(rows[i].astype(float))
        for mask, coefficient in vacuum:
            for (out, grade, site), val in car.flat_column(x, mask).items():
                entry = (coefficient*weights[site]*Fraction(val, 128))*row
                key = (out, grade)
                amplitude[key] = amplitude[key] + entry
                if site == car.W:
                    local[key] = local[key] + entry
    energy = sum((heat.interval.reduce_sum(v.square()) for v in amplitude.values()), I(0.))
    scale_derivative = -2*sum((heat.interval.reduce_sum(amplitude[k]*v)
                               for k,v in local.items()), I(0.))
    require(6.8565877248 < energy.lo < energy.hi < 6.8565877249, "absolute R")
    require(-0.048597675741 < scale_derivative.lo < scale_derivative.hi < -0.048597675740,
            "fixed-preparation Weyl source of R")
    return energy, scale_derivative


def certified_windows(s, local, thresholds):
    # Reuse each enclosure of the full trace for every candidate payment.
    regions = {label: [] for label in thresholds}
    lower_bounds = {label: 1e9 for label in thresholds}
    def visit(left, right):
        heat_row, _ = heat.across_depths(s, local, left, right)
        differences = {k: heat_row-v for k,v in thresholds.items()}
        if any(float(v.lo) <= 0 <= float(v.hi) for v in differences.values()):
            require(left < right, f"unresolved integer depth {left}")
            midpoint = (left + right)//2
            visit(left, midpoint)
            visit(midpoint+1, right)
            return
        for key, diff in differences.items():
            sign = 1 if diff.lo > 0 else -1
            gap = min(abs(float(diff.lo)), abs(float(diff.hi)))
            lower_bounds[key] = min(lower_bounds[key], gap)
            window = regions[key]
            if window and window[-1][2] == sign and window[-1][1]+1 == left:
                window[-1][1] = right
            else:
                window.append([left,right,sign])
    for n in range(1,8193,32):
        visit(n, min(n+31,8192))
    return regions, lower_bounds


def exact_enclosure(reported):
    lo, hi = (I.rational(Fraction(str(x))) for x in reported)
    return I(lo.lo, hi.hi)


def main():
    energy, derivative = material_ray()
    verified = work.bounds()
    alpha = heat.P*heat.P*heat.P*Fraction(1,1024)
    port = alpha*energy
    # The direct interval accumulation is wider than the independent fine-port
    # certificate; their distinct enclosures must intersect.
    independent = exact_enclosure(verified["physical_port_range"])
    require(max(port.lo, independent.lo) < min(port.hi, independent.hi), "same physical flat port")
    seq = exact_enclosure(verified["sequential_gain"])
    snap = exact_enclosure(verified["one_current_bit_gain"])
    spectral = I.rational(22).sqrt()
    thresholds = {"original_HJR":-derivative, "post_full":I(0.),
                  "post_sequential_unit":-seq*derivative,
                  "post_sequential_spectral":-spectral*seq*derivative,
                  "post_current_unit":-snap*derivative,
                  "post_current_spectral":-spectral*snap*derivative}
    s, local = heat.numerical_basis()
    first, _ = heat.across_depths(s, local, 1, 1)
    last, _ = heat.across_depths(s, local, 8192, 8192)
    required_shift = first-last
    require(0.05598 < required_shift.lo <= required_shift.hi < 0.05602, "two-depth source")
    require(required_shift.lo/2 > 0.02799, "minimax residual for one endpoint correction")
    windows, lower = certified_windows(s, local, thresholds)
    require(windows["original_HJR"] == [[1,424,1],[425,8192,-1]], "all original depths")
    require(windows["post_current_unit"] == [[1,1615,1],[1616,8192,-1]], "unit readout")
    require(windows["post_current_spectral"] == [[1,8192,-1]], "spectral readout")
    for label in ("post_full", "post_sequential_unit", "post_sequential_spectral"):
        require(windows[label] == [[1,8192,1]], label)
    require(lower["original_HJR"] > 6.4e-7 and lower["post_current_unit"] > 3e-6,
            "quantitative gap at the two depth transitions")
    result = {"R":heat.interval.bounds(energy), "dR":heat.interval.bounds(derivative),
              "required_late_minus_early_source":heat.interval.bounds(required_shift),
              "all_integer_depths":windows, "certified_lower_abs_source":lower}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
