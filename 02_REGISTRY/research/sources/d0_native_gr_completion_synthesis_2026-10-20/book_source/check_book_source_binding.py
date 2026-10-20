#!/usr/bin/env python3
"""Exact original Golden port and complete-source translation checks.

No physical Info law is assigned and no historical suite is replayed.
Arithmetic is exact in Q(a), a=sqrt(phi^-1), a^4+a^2-1=0.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


PINNED_INPUTS = {
    "01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md": "668fc904b0585cc7fd5175babead5225c22051422c9c64e197d7b0d42d225342",
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md": "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d",
    "02_REGISTRY/research/A4D_RETAINED_HISTORY_READOUT_AND_NORMALIZER.md": "98b02b22f8678be211f555c2ec0c1d8ac3d2cc43f7dd50b002b8e1424460407b",
    "02_REGISTRY/research/A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md": "6a14686fcaab0b48b78b8ff4f784d989ea3ead1edf0ee28d48b7c20f76c4a7ed",
    "02_REGISTRY/research/A4D_NATIVE_FULL128_PORT_SCORE_SUFFICIENCY_AND_CODE_SOURCE_RECOVERY_2026_10_19.md": "f64e04fa9f3d27a604463561fa3d8c1c997e55d3c55badd91a6b4198ce0f9f4e",
    "02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md": "ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d",
    "02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md": "bd3f1ab51599b0efe17af03e40c59a606200cd1912f801e4bd57e0eb77a6b014",
    "02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md": "c5b2f1021e8da573221f4327bacae67934470a368966456bf328b19fc51555fb",
    "02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md": "8dbca8ff9a4567a2baf216357b5d3ffa2d217281ced4e5d0e535257db2f5e83e",
}


class G:
    """Coefficients in the ordered basis (1,a,a^2,a^3)."""

    def __init__(self, value=0):
        if isinstance(value, G):
            self.c = value.c
        elif isinstance(value, (tuple, list)):
            self.c = tuple(F(x) for x in value)
            if len(self.c) != 4:
                raise ValueError("four coefficients required")
        else:
            self.c = (F(value), F(0), F(0), F(0))

    def __add__(self, other):
        other = G(other)
        return G(tuple(x + y for x, y in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self):
        return G(tuple(-x for x in self.c))

    def __sub__(self, other):
        return self + (-G(other))

    def __rsub__(self, other):
        return G(other) - self

    def __mul__(self, other):
        other = G(other)
        product = [F(0)] * 7
        for i, x in enumerate(self.c):
            for j, y in enumerate(other.c):
                product[i + j] += x * y
        # a^k = a^(k-4) - a^(k-2), k>=4.
        for k in range(6, 3, -1):
            product[k - 4] += product[k]
            product[k - 2] -= product[k]
        return G(product[:4])

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = F(other)
        if other == 0:
            raise ZeroDivisionError
        return G(tuple(x / other for x in self.c))

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("only nonnegative integer powers")
        out = G(1)
        for _ in range(n):
            out = out * self
        return out

    def __eq__(self, other):
        return self.c == G(other).c

    def serial(self):
        return [str(x) for x in self.c]


def mv(matrix, vector):
    return [sum((matrix[i][j] * vector[j] for j in range(2)), G())
            for i in range(2)]


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), G())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parents[5])
    args = parser.parse_args()
    checks = []

    def require(condition, name):
        if not condition:
            raise RuntimeError("FAIL: " + name)
        checks.append(name)

    for relative, expected in PINNED_INPUTS.items():
        found = hashlib.sha256((args.root / relative).read_bytes()).hexdigest()
        require(found == expected, "source SHA256: " + relative)

    one, zero = G(1), G()
    a = G((0, 1, 0, 0))
    p = a * a
    require(p + p**2 == 1, "original Golden p+p^2=1")
    require(p * (1 + p) == 1, "phi=1+p=1/p")
    require(a * (a + a**3) == 1, "inverse of original sqrt(p)")

    # Exact common factor L=-2p N_k^* A from the ORIGINAL nonblank rows.
    common = -2 * p
    require(p * common == -2 * p**2, "original K0=p L coefficient")
    require(a * common == -2 * p * a, "original K1=sqrt(p) L coefficient")
    r0, r1 = p**2, p
    require(r0 + r1 == 1, "all nonblank port mass retained")
    require(p**2 == r0 and a**2 == r1, "absolute amplitude squares")

    cost_gap = F(1)
    log_phi_probability_ratio = F(1)  # q1/q0=1/p=phi.
    require(r1 == r0 * (1 + p), "exact native port probability ratio phi")
    gaps = {
        "absolute_amplitude": cost_gap + log_phi_probability_ratio / 2,
        "absolute_scalar_probability": cost_gap + log_phi_probability_ratio,
        "additional_native_amplitude_marker": cost_gap,
    }
    require(gaps["absolute_amplitude"] == F(3, 2), "amplitude Info gap=3/2")
    require(gaps["absolute_scalar_probability"] == 2, "probability Info gap=2")
    require(gaps["additional_native_amplitude_marker"] == 1,
            "additional-marker Info gap=1")

    # Wrong scalar-probabilities-as-amplitudes binding, with no floating point.
    raw0, raw1 = r0**2, r1**2
    wrong0, wrong1 = (2 - p) / 5, (3 + p) / 5
    require(wrong0 + wrong1 == 1, "wrong squared law still normalized")
    require(wrong0 * (raw0 + raw1) == raw0,
            "wrong law port0=(5-sqrt(5))/10")
    require(wrong1 * (raw0 + raw1) == raw1,
            "wrong law port1=(5+sqrt(5))/10")
    require(wrong0 != r0 and wrong1 != r1,
            "squared-probability binding fails original physical port")

    for x, q0, q1, label in [
        (p, G(F(1, 2)), G(F(1, 2)), "t=log(phi)"),
        (p**2, p, p**2, "t=2log(phi)"),
    ]:
        z = r0 * x + r1 * x**2
        require(q0 * z == r0 * x, label + " true cost-marked port0")
        require(q1 * z == r1 * x**2, label + " true cost-marked port1")
        require(q0 + q1 == 1, label + " retains both ports")

    # Equation (1), on original Golden amplitudes with a coherent Golden
    # reference projector. Test the two formal coefficients 1 and ell
    # separately: ell is NOT replaced by an algebraic approximation.
    v = [[p, zero], [zero, a]]
    dv = [[p / 3, zero], [zero, a / 3]]
    w = [p, p**2]
    ds = [G(1), G(-2)]
    effect = [[p**2, p*a], [p*a, p]]
    deffect = [[zero, one / 7], [one / 7, zero]]
    q = [sum((w[j] * v[j][i] for j in range(2)), G()) for i in range(2)]
    dq0 = [sum((w[j] * dv[j][i] for j in range(2)), G()) for i in range(2)]
    dq1 = [sum((-w[j] * ds[j] * v[j][i] for j in range(2)), G())
           for i in range(2)]
    direct0 = 2 * dot(dq0, mv(effect, q)) + dot(q, mv(deffect, q))
    direct1 = 2 * dot(dq1, mv(effect, q))
    gram0, gram1 = G(), G()
    for i in range(2):
        for j in range(2):
            gram = dot(v[i], mv(effect, v[j]))
            dgram = (dot(dv[i], mv(effect, v[j]))
                     + dot(v[i], mv(deffect, v[j]))
                     + dot(v[i], mv(effect, dv[j])))
            gram0 += w[i] * w[j] * dgram
            gram1 -= w[i] * w[j] * (ds[i] + ds[j]) * gram
    require(gram0 == direct0, "coherent first jet: full moving Gram coefficient")
    require(gram1 == direct1, "coherent first jet: exact log(phi) coefficient")
    require(dot(v[0], mv(effect, v[1])) != 0,
            "coherent control really contains an off-diagonal record term")

    # Native normalization: tangent to an isometry has zero real norm source.
    native = [p, a]
    native_tangent = [-a, p]
    require(dot(native, native) == 1, "native full two-port vector norm")
    require(dot(native, native_tangent) == 0, "native norm derivative cancels")
    common_amplitude, dcommon = p, G(F(3, 7))
    raw = [common_amplitude * z for z in native]
    draw = [dcommon * native[i] + common_amplitude * native_tangent[i]
            for i in range(2)]
    require(2 * dot(raw, draw) == 2 * common_amplitude * dcommon,
            "raw first source retains the common normalization derivative")

    # Every ORIGINAL nonblank label has common probability mass g(y).
    # These rational jets test the product rule, not a new physical source law.
    g, dg = G(F(2, 5)), G(F(3, 11))
    s0, s1, ds0, ds1 = G(1), G(2), G(F(3, 7)), G(F(-2, 9))
    direct_price = ds0 * r0*g + s0*r0*dg + ds1*r1*g + s1*r1*dg
    effect_price = (r0*ds0+r1*ds1)*g + (r0*s0+r1*s1)*dg
    require(direct_price == effect_price, "complete price and common-state product rule")
    require((r0*s0+r1*s1)*dg != 0,
            "dropping moving state/preparation term gives a false zero")
    require(r0*s0+r1*s1 == 1+p, "actual original conditional port mean cost")

    # Original Golden comparison R=R^{-1}. For a supplied full unitary U
    # its port1 block is pa(I-U); full unitary work is not postselected.
    gate = [[p, a], [a, -p]]
    for i in range(2):
        for j in range(2):
            require(sum((gate[i][k]*gate[k][j] for k in range(2)), G())
                    == int(i == j), "original Golden gate involution " + str((i,j)))
    port1_factor = p*a
    require(port1_factor**2 == p**3, "controlled-unitary port1 scale p^3")
    baseline_q1 = 2*p**3
    require(1+baseline_q1 == 1+2*p**3, "literal 0/10 reporter baseline")
    sigma = F(3, 5)  # symbolic coefficient control, NOT a physical selection.
    dt = -G(sigma)/2
    dport1 = -2*p**3*dt
    require(dport1 == sigma*p**3, "real scalar compression t=-sigma*A/2 source")
    require(1*(-dport1)+2*dport1 == sigma*p**3,
            "complete two-port cost source retains complement")
    require(2*(-dport1)+2*dport1 == 0,
            "equal code prices erase the source despite nonzero readout")
    ds_common = G(F(2, 7))
    require((1-baseline_q1)*ds_common+baseline_q1*ds_common == ds_common,
            "moving common net price cannot be dropped by normalization")

    result = {
        "status": "PASS",
        "checks": len(checks),
        "check_names": checks,
        "arithmetic": "exact Q(a), a=sqrt(phi^-1), a^4+a^2-1=0",
        "input_sha256": PINNED_INPUTS,
        "relative_gain_gaps": {k: str(v) for k, v in gaps.items()},
        "native_port_probabilities_in_1_a_a2_a3_basis": [r0.serial(), r1.serial()],
        "wrong_squared_probabilities_in_1_a_a2_a3_basis": [wrong0.serial(), wrong1.serial()],
        "scope": {
            "original_outcomes": 128,
            "checked_carrier": "exact factored original nonblank port; no historical 128-matrix replay",
            "coherent_jet": "formal coefficients of 1 and log(phi), no log approximation",
            "controlled_port": "conditional unitary compression and literal 0/10 reporter only",
            "physical_Info_selected": False,
            "full_programme_price_closed": False,
            "GR_closed": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
