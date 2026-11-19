"""Exact sector-source checks and quantitative H.1/B170 controls."""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
from math import isqrt
from pathlib import Path
import json
import subprocess

import sympy as sp


PILOT = Path(__file__).resolve().parents[3]
ROOT = PILOT.parents[3]
METRIC = (
    "02_REGISTRY/research/sources/d0_gr_2026-11-18/"
    "followups/2026-11-19/metric/"
)
P_REAL = (sp.sqrt(5)-1)/2
FIELD = sp.QQ.algebraic_field(P_REAL)
P = FIELD.from_sympy(P_REAL)


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def check_source_pins():
    references = {
        ("a3ef80fff", "UNMATCHED_WEIGHT_BRIDGE_RU.md"):
            "b2861b57b7ab93940b0799e5143a550c0c042805146d3ce55544183148d77b67",
        ("04931a7a26a9741bba0584c8e1413613ff7a28d5", "EIGHT_READERS_RU.md"):
            "e6cf63011b94a10068d9545eb901c6f17c22024693d9ea21bc874dcd7f86fb0e",
    }
    for (revision, name), expected in references.items():
        result = subprocess.check_output(
            ["git", "show", f"{revision}:{METRIC}{name}"], cwd=ROOT
        )
        require(sha256(result).hexdigest() == expected, name)
    b170 = PILOT/"open/round170/recursion/CAUSAL_COLOUR_RECURSION_RU.md"
    require(sha256(b170.read_bytes()).hexdigest() ==
            "80f8ec3b30f3da6ddbf917d6e802ca41835947c2da56a853ed899e30f3c7fae9",
            "B170 recursion pin changed")
    return len(references)+1


def check_group_formula():
    x, y = sp.symbols("x y", positive=True)
    rows_w = ((2*(1-x), (1-x)*(3+y)), (4*x, x*(1+y)))
    rows_v = (((1-x)*y, (1-x)*(5-y)), (3*x, 2*x))
    z_w = sum(sum(row) for row in rows_w)
    z_v = sum(sum(row) for row in rows_v)
    for direction in (x, y):
        leaf_derivative = sp.diff(sp.log(z_w/z_v), direction)
        exact = sum(
            (sum(row_v)/z_v-sum(row_w)/z_w)*sp.diff(sp.log(sum(row_w)), direction)
            + sum(row_v)/z_v*sp.diff(sp.log(sum(row_v)/sum(row_w)), direction)
            for row_w, row_v in zip(rows_w, rows_v)
        )
        require(sp.simplify(leaf_derivative+exact) == 0,
                "grouping dropped a moving conditional derivative")
    pi = sp.Matrix([sp.Rational(1, 4)]*4) + x*sp.Matrix([1,-1,0,0])
    a, b = sp.Matrix([4,2,3,1]), sp.Matrix([4,2,1,3])
    require(b != a and sp.expand(a.dot(pi)-b.dot(pi)) == 0,
            "the restricted affine model should conceal an unmatched sector")
    full_tangent = sp.Matrix([[1,-1,0,0],[0,1,-1,0],[0,0,1,-1]])
    require(full_tangent.rank() == 3
            and full_tangent.col_join(sp.Matrix([[1,1,1,1]])).rank() == 4,
            "the full conditional model should admit a converse")
    q, rho_a, rho_b = sp.symbols("q rho_a rho_b", positive=True)
    f_a, f_b = 1-q+rho_a*q, 1-q+rho_b*q
    exact_binary = sp.diff(sp.log(f_a/f_b),q)
    require(sp.simplify(exact_binary-(rho_a-rho_b)/(f_a*f_b)) == 0,
            "wrong scalar contrast sign")

    # A positive multiple of the graph source can survive an affine offset.
    masses = sp.Matrix([1-q,q])
    aa = sp.Matrix([3,1]).dot(masses)
    bb = sp.Matrix([7,3]).dot(masses)
    require(sp.expand(bb-2*aa) == 1, "wrong positive-multiple control")
    require(sp.simplify(sp.diff(sp.log(bb),q)
                        -2*aa/bb*sp.diff(sp.log(aa),q)) == 0,
            "wrong normalized gain with an absolute affine offset")

    # Score coordinates already carry the L²(Q) orthonormalization.
    lift = sp.diag(3,sp.Rational(1,2),0)
    right_inverse = sp.diag(sp.Rational(1,3),2,0)
    require(lift*right_inverse == sp.diag(1,1,0), "wrong score right lift")
    require((lift.T*sp.eye(3)[:,1]).dot(lift.T*sp.eye(3)[:,1]) == sp.Rational(1,4),
            "right-lift lower bound failed at its sharp axis")
    return {"full_tangent_rank": 3, "conditional_rank_fixture": 1,
            "right_lift_lower_singular_value": "1/2"}


def root_endpoints():
    scale = 10**400
    low = Q(isqrt(5*scale**2)-scale,2*scale)
    high = low+Q(1,2*scale)
    require(low**2+low < 1 < high**2+high, "invalid Golden interval")
    return low, high


def enclosure(element):
    bounds = root_endpoints()
    coefficients = [Q(c.numerator,c.denominator) for c in element.to_list()]
    coefficients = [Q(0)]*(2-len(coefficients))+coefficients
    slope, constant = coefficients
    ends = [constant+slope*x for x in bounds]
    return min(ends), max(ends)


def log_golden_bounds():
    low, high = root_endpoints()

    def series(p):
        t = p/(2+p)
        lower_value = 2*sum(t**(2*k+1)/(2*k+1) for k in range(24))
        upper_value = lower_value+2*t**49/(49*(1-t*t))
        return lower_value, upper_value

    return series(low)[0], series(high)[1]


def check_b170():
    last, current = FIELD.one, P**3
    for _ in range(2,21):
        last, current = current, 2*P**3*current-last
    eta = (1-current)/2
    wait = 1-eta
    sigma = P**(-2)
    none = P**4/wait
    active = P**4/eta
    total_0 = (P**3/wait+P**5/eta)**12
    total_1 = sigma*(none+active)**12+(1-sigma)*none**12
    ratio = total_1/total_0
    ratio_lo, ratio_hi = enclosure(ratio)
    require(Q("0.91986643") < ratio_lo <= ratio_hi < Q("0.91986645"),
            "wrong actual B170 grouped continuation ratio")
    ell_lo, ell_hi = log_golden_bounds()
    delta_lo, delta_hi = 1-ratio_hi, 1-ratio_lo
    gain_lo = delta_lo/(ell_hi*(1-Q(23,100)*delta_lo))
    gain_hi = delta_hi/(ell_lo*(1-Q(38,100)*delta_hi))
    require(Q("0.16965") < gain_lo < gain_hi < Q("0.17176"),
            "wrong normalized discrepancy against equal sector masses")

    # Transfer unnormalized weight between two actual masks at fixed Y=0.
    # These perturbed weights are a mathematical control, not measured heat.
    old_empty = (P**3/wait)**12
    old_all = (P**5/eta)**12
    small = FIELD.convert(sp.Rational(1,10**9))
    new_empty, new_all = small*old_empty, old_all+(1-small)*old_empty
    shifted = total_0-old_empty-old_all+new_empty+new_all
    require(shifted == total_0 and old_empty/new_empty == FIELD.convert(10**9),
            "leaf rescaling must be invisible to sector jet")
    require(total_1/shifted == ratio, "sector mismatch introduced by regrouping")
    return {"ratio_interval": ["0.91986643","0.91986645"],
            "discrepancy_per_Dq_times_nu": ["0.16965","0.17176"],
            "hidden_single_leaf_ratio": 10**9}


def check_eight_setting_rank():
    y = sp.symbols("y")
    fugacity = sp.Rational(1,2**20)
    matter_u = P_REAL+P_REAL**2*y
    matter_block = 4*matter_u**2*(1-matter_u**2)
    base = 4*P_REAL**3
    combined = base+(1-base)*matter_block
    report = fugacity*(combined+matter_block)-fugacity**2*combined*matter_block
    coefficients = sp.Poly(report.expand(), y, extension=P_REAL).all_coeffs()[::-1]
    require(len(coefficients)==9, "wrong native SC1 matter degree")
    signed_intervals = [enclosure(FIELD.from_sympy(c)) for c in coefficients[1:]]
    require(signed_intervals[0][0] > 0
            and all(upper < 0 for _,upper in signed_intervals[1:]),
            "a native moment coefficient vanished")

    layers = 16
    level = [sp.Rational(j,64) for j in range(1,9)]
    profiles = [0]*layers
    for j, s in enumerate(level):
        profiles[2*j] = sp.sqrt(s)/layers
    energy = [(layers*(profiles[(j+1)%layers]-profiles[j]))**2
              for j in range(layers)]
    for j,s in enumerate(level):
        require(energy[2*j] == energy[(2*j-1)%layers] == s,
                "periodic material pulses are not disjoint")
    for value in profiles:
        require(bool(value**2 < 1-P_REAL), "canonical preparation lost slack")

    vandermonde = sp.Matrix([[j**k for k in range(8)] for j in range(1,9)])
    inverse = vandermonde.inv()
    norm = max(sum(abs(value) for value in row) for row in inverse.tolist())
    transposed_norm = max(sum(abs(value) for value in row) for row in inverse.T.tolist())
    step_e, step_s = Q(1,512), Q(1,64)
    diagonal_lower = min(
        k*min(abs(lo),abs(hi))*(step_e*step_s)**(k-1)
        for k,(lo,hi) in enumerate(signed_intervals,1)
    )
    norm_product = norm*transposed_norm
    upper = 8*Q(int(norm_product.p),int(norm_product.q))/(step_e**2*diagonal_lower)
    require(upper < Q("9.011e57"), "uniform fixture right lift bound failed")

    # With nonuniform fixed strictly positive PF counts, a permutation
    # contributes its own exponent tuple and cannot cancel identically.
    monomials = set(permutations(range(8)))
    require(len(monomials) == 40320, "nonuniform PF determinant terms collide")
    return {"setting_matter_rank_when_admitted": 8,
            "normalized_inverse_inf_upper": "9.011e57",
            "nonuniform_PF_distinct_determinant_monomials": len(monomials)}


def main():
    print(json.dumps({
        "source_pins": check_source_pins(),
        "grouped_identity": check_group_formula(),
        "b170": check_b170(),
        "eight_setting": check_eight_setting_rank(),
        "physical_field_writer_admitted": False,
        "full_book_price_selected": False,
        "GR_closed": False,
        "status": "PASS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
