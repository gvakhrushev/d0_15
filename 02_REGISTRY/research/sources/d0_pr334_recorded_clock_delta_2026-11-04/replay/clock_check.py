#!/usr/bin/env python3
"""Exact application of the owned state collar; no PDE/root/native search."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import sympy as s

checks = {}


def need(value, label):
    if value is not True:
        raise RuntimeError(label)
    checks[label] = True


delta = F(1, 1000)
inverse_gap = F(1, 249)
glo, ghi = 1 - inverse_gap, 1 + inverse_gap
bmax = F(1, 248)
hmax = 3 * bmax**2 + ghi / glo
vmin, vmax = F(249, 1000), F(261, 1000)
xlo = glo * (vmin**2 - 2 * 3 * delta**2)
xhi = ghi * vmax**2
p0lo = vmin - 3 * bmax * delta
q0hi = 20 * ghi * vmax

need(4 * delta / (1 - 4 * delta) == inverse_gap,
     "Neumann inverse difference is one over 249")
need(F(3, 48) == F(1, 16), "kappa below 24 gives initial pi above one quarter")
need(F(3, 46) < F(13, 50)**2, "kappa above 23 gives initial pi below 13 over 50")
need(hmax < 2, "spatial hyperbolic matrix upper bound below two")
need(xlo > F(1, 20), "clock gradient norm lower bound above one twentieth")
need(xhi < F(1, 10), "clock gradient norm upper bound below one tenth")
need(glo * vmin == F(31, 125), "future gradient time component lower bound")
need(p0lo > F(6, 25), "coordinate scalar derivative positive with margin")
need(q0hi < 6, "scalar-clock flow time speed below six")
need(10 * F(31, 125) == F(62, 25), "scalar-clock flow time speed lower bound")
need(6 * F(1, 12) == F(1, 2), "Tstar over twelve stays in half the slab")

# Exact completion of the square for arbitrary shift and symmetric h.
g00, vv = s.symbols("g00 vv", real=True)
bb = s.Matrix(s.symbols("b0:3", real=True))
ww = s.Matrix(s.symbols("w0:3", real=True))
h00, h01, h02, h11, h12, h22 = s.symbols(
    "h00 h01 h02 h11 h12 h22", real=True
)
hh = s.Matrix([[h00, h01, h02], [h01, h11, h12], [h02, h12, h22]])
ginv = s.zeros(4)
ginv[0, 0] = g00
ginv[0, 1:4] = g00 * bb.T
ginv[1:4, 0] = g00 * bb
ginv[1:4, 1:4] = g00 * (bb * bb.T - hh)
pp = s.Matrix([vv - (bb.T * ww)[0], *ww])
need(s.expand((pp.T * ginv * pp)[0]
              - g00 * (vv**2 - (ww.T * hh * ww)[0])) == 0,
     "physical gradient norm uses the actual convective derivative")

# A wave clock can have a non-exact proper-duration one-form.
t, x = s.symbols("t x", real=True)
eps = s.symbols("eps", positive=True)
psi = t * (1 + eps * x)
pt, px = s.diff(psi, t), s.diff(psi, x)
X = s.expand(pt**2 - px**2)
need(s.diff(psi, t, 2) - s.diff(psi, x, 2) == 0,
     "hostile scalar is an exact flat wave")
need(X.subs({t: 0, x: 0}) == 1, "hostile clock has a timelike neighbourhood")
qt, qx = pt / X, -px / X
need(s.simplify(qt * pt + qx * px - 1) == 0,
     "clock flow evaluates scalar at unit rate")
need(s.simplify(qt**2 - qx**2 - 1 / X) == 0,
     "clock flow metric norm is inverse X")
alpha_t, alpha_x = pt / s.sqrt(X), px / s.sqrt(X)
curl = s.simplify((s.diff(alpha_x, t) - s.diff(alpha_t, x))
                  .subs({t: 0, x: 0}))
need(curl == eps, "proper-duration one-form has nonzero exterior derivative")
need(F(3, 4)**2 - F(1, 4)**2 == F(1, 2),
     "hostile X is at least one half on the stated small patch")

path = Path(__file__)
result = {
    "status": "PASS",
    "input_head": "057ae65246d234f168348a0c14d863cdcd112b56",
    "number_of_checks": len(checks),
    "checks": checks,
    "exact_bounds": {
        "h_upper": str(hmax),
        "X_lower": str(xlo),
        "X_upper": str(xhi),
        "coordinate_derivative_lower": str(p0lo),
        "clock_flow_time_speed_upper": str(q0hi),
    },
    "hostile_wave_clock": {
        "psi": str(psi),
        "X": str(X),
        "exterior_derivative_dt_wedge_dx_at_origin": str(curl),
        "patch": "abs(eps*x)<1/4 and abs(eps*t)<1/4",
        "not_a_claim": "not asserted to solve the coupled Einstein equations",
    },
    "not_claimed": [
        "new initial-data or PDE-energy theorem",
        "PDE integration or emitted native history",
        "native primitive ticks equal scalar time or proper duration",
        "global exact proper-time one-form",
    ],
    "checker_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
}
print(json.dumps(result, sort_keys=True))
