"""Exact bounds for diagonal trace-work concavity and the two physical dials."""

from fractions import Fraction as F
from itertools import product
import json

import mpmath as mp
import sympy as sp


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def check_derivatives():
    t, c, q, b = sp.symbols("t c q b", real=True)
    a = q+b*t
    radicand = 2*c*a-c**2*a**2
    work = 2*sp.sqrt(radicand)
    expected = -2*c**2*b**2/radicand**sp.Rational(3,2)
    require(sp.simplify(sp.diff(work,t,2)-expected) == 0, "literal CNOT work curvature")
    v = sp.symbols("v", real=True)
    slope_squared = (1-v)**2*v/(2-v)
    derivative_sign_numerator = sp.diff(slope_squared,v)*(2-v)**2/(2*(1-v))
    require(sp.simplify(derivative_sign_numerator-(v**2-3*v+1)) == 0,
            "monotonic native tuning from c=0")
    k, w = sp.symbols("k w", positive=True)
    a0, a1, a2, b0, b1, b2 = sp.symbols("a0 a1 a2 b0 b1 b2", real=True)
    x = sp.exp(-k*(a0+a1*t+a2*t*t/2))
    y = w*sp.exp(-k*(b0+b1*t+b2*t*t/2))
    curvature = sp.diff(-sp.log(x+y)/k,t,2).subs(t,0)
    x0,y0 = x.subs(t,0),y.subs(t,0)
    expected = (x0*a2+y0*b2)/(x0+y0)-k*x0*y0*(a1-b1)**2/(x0+y0)**2
    require(sp.simplify(curvature-expected) == 0, "absolute two-history covariance identity")


def check_conditional_round():
    # Two old labels, two ancilla basis states. DD AA and A DD A
    # are named only by their native chronological permutation.
    for old,x,y in product((0,1),repeat=3):
        for word in ("DDAA","ADDA"):
            record = [old,x,y]
            for letter in word:
                control = 0 if letter == "A" else 1
                record[control+1] ^= record[control]
            require(record == [old,x,y], "unchanged endpoint on every input column")


def golden_power(c, s, exponent):
    real, imaginary = mp.iv.mpf(1), mp.iv.mpf(0)
    while exponent:
        if exponent % 2:
            real, imaginary = real*c-imaginary*s, real*s+imaginary*c
        c, s = c*c-s*s, 2*c*s
        exponent //= 2
    return real, imaginary


def certify_constants():
    mp.iv.dps = 65
    p = (mp.iv.sqrt(5)-1)/2
    r = p**2
    a_min, a_max = F(1,2560),F(1,1024)
    gap = a_min**2/64  # Jensen midpoint gap on t in [1/4,3/4], before the native error.
    require(gap > F("2.38e-9"), "uniform finite curvature signal")
    require(mp.iv.sqrt(p).a > (4/(3*mp.iv.sqrt(3)) + mp.iv.mpf(".01")).b,
            "room for the second positive work dial")
    c,s = golden_power(mp.iv.sqrt(p),p,16)
    require((-c).a > mp.iv.mpf(".32") and (-c).b < mp.iv.mpf(".34")
            and (-s).a > mp.iv.mpf(".92") and (-s).b < mp.iv.mpf(".96"),
            "exact Golden interference rotation")
    t_over_root = 1/mp.iv.sqrt(3)
    root_cubed = mp.iv.mpf(".75")*mp.iv.sqrt(mp.iv.mpf(".75"))
    v_min = mp.iv.mpf(".16") + mp.iv.mpf(".23")*t_over_root
    v_max = mp.iv.mpf(".17") + mp.iv.mpf(".32")*t_over_root
    u_min = mp.iv.mpf(".23")/root_cubed
    require(v_min.a > mp.iv.mpf(".28") and v_max.b < mp.iv.mpf(".36")
            and u_min.a > mp.iv.mpf(".34"), "interference slope and curvature")
    require((r-mp.iv.mpf(".82")/1024).a > mp.iv.mpf(".38")
            and r.b < mp.iv.mpf(".383"), "nondegenerate bases")
    q_floor,q_ceil = F(".38"),F(".383")
    require(1/(q_floor*(2-q_ceil)*(1-q_ceil)) < 4, "log curvature loss")
    require(F(".34")/F(".36")-4*F(".36")*a_max > F(".9"), "strictly positive interference curvature")
    require(2*(1-q_ceil)*F(".28") > F(".01"), "adequate curvature dial range")
    d_minus = mp.iv.mpf(".5")/(mp.iv.mpf(".6")**mp.iv.mpf("1.5"))
    d_plus = mp.iv.mpf(8)/9/(mp.iv.mpf(".75")**mp.iv.mpf("1.5"))
    require((d_minus+d_plus).b < 3, "sum of both diagonal curvature magnitudes")
    require(F(".009") > 3*a_max, "opposite sign reached before diagonal tuning exhausts")
    return {
        "uniform_a_interval":["1/2560","1/1024"],
        "jensen_gap_lower_per_unit_rate":"2.38e-9",
        "positive_extra_slope_range_in_units_of_a":["0",".01"],
        "positive_interference_curvature_per_interference_slope_lower":".9",
        "two_continuous_target_dials_cancel_first_and_second_conditional_work_jets": True,
        "native_dials_only_approximate_the_calibrated_values": True,
    }


def finite_native_angle_example():
    p = (mp.iv.sqrt(5)-1)/2
    r = p**2
    cos_frame, sin_frame = golden_power(mp.iv.sqrt(p),p,16)
    a = 1/(4096*(2-mp.iv.sqrt(2)))
    t = mp.iv.mpf(".5")
    half = mp.iv.mpf(".5")
    d = -sin_frame/4
    square_root = mp.iv.sqrt(1-t*t)
    q = (
        (r-a*(1+t)/2, -a/2, 0),
        (half+a*t/2, a/2, 0),
        (r-a/2-a*cos_frame*t/2-a*d*square_root,
         a*(-cos_frame/2+d*t/square_root), a*d/square_root**3),
    )
    angles = (72434,85468)
    targets = [
        1-golden_power(mp.iv.sqrt(p),p,2*power)[1] for power in angles
    ]
    require(all(c.a > 0 and c.b < 1 for c in targets), "physical target range")
    first, second = mp.iv.mpf(0), mp.iv.mpf(0)
    for c, (probability,slope,curve) in zip((targets[0],1,targets[1]),q):
        factor = probability*(2-c*probability)
        first_gate = 2*mp.iv.sqrt(c)*(1-c*probability)/mp.iv.sqrt(factor)
        second_gate = -2*mp.iv.sqrt(c)/(factor*mp.iv.sqrt(factor))
        first += first_gate*slope
        second += first_gate*curve+second_gate*slope**2
    require(abs(first).b < mp.iv.mpf("3e-9") and abs(second).b < mp.iv.mpf("3e-9"),
            "strict native angle residual on the ideal B174 field")
    return {
        "material_lattice":8,
        "fixed_native_target_powers":list(angles),
        "conditional_first_and_second_remainders_each_below":"3e-9",
        "normalized_geometric_gain_precision_attained":False,
    }


def main():
    check_derivatives()
    check_conditional_round()
    print(json.dumps({
        "status":"PASS",
        "diagonal_trace_curvature_certified":True,
        "fixed_absolute_log_sum_covariance_identity":True,
        "center_compensation":certify_constants(),
        "native_target_example_on_ideal_field":finite_native_angle_example(),
        "complete_microscopic_price_derived":False,
        "GR_closed":False,
    },indent=2))


if __name__ == "__main__":
    main()
