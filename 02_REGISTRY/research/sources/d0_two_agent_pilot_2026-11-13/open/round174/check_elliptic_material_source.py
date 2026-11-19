"""Check the actual 36-selector on a smooth constant-action CAR family."""

from fractions import Fraction as F
import json
from pathlib import Path
import runpy

import mpmath as mp
import sympy as sp


HERE = Path(__file__).resolve().parent
P_REAL = (sp.sqrt(5)-1)/2
GOLDEN = sp.QQ.algebraic_field(P_REAL)


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def as_interval(x, p):
    coefficients = GOLDEN.from_sympy(x).to_list()
    terms = [mp.iv.mpf(c.numerator)/c.denominator for c in coefficients]
    result = mp.iv.mpf(0)
    for term in terms:
        result = p*result+term
    return result


def sc1_coefficients(p):
    y = sp.symbols("y")
    z = sp.Rational(1,2**20)
    u = P_REAL+P_REAL**2*y
    visible = 4*P_REAL**3
    matter = 4*u**2*(1-u**2)
    gated = visible+(1-visible)*matter
    polynomial = sp.Poly(z*(gated+matter)-z**2*gated*matter, y, extension=P_REAL)
    require(polynomial.degree() == 8, "owned SC1 polynomial")
    coefficients = [as_interval(polynomial.nth(degree),p) for degree in range(9)]
    require(all(abs(c).b < mp.iv.mpf("2e-6") for c in coefficients), "raw report stays near baseline")
    return coefficients


def exact_wave_witnesses():
    z = sp.symbols("z")
    checked = []
    for length in (6,8,12,16,24,32,48,64):
        cyclotomic = sp.Poly(sp.cyclotomic_poly(length,z),z,domain=sp.QQ)

        def power(exponent):
            return z**(exponent % length)

        def reduce(value):
            return sp.rem(sp.Poly(value,z,domain=sp.QQ),cyclotomic).as_expr()

        phase_cosines = [reduce((power(2*n+1)+power(-2*n-1))/2) for n in range(length)]
        denominator = 2-z-power(-1)
        for n,c in enumerate(phase_cosines):
            cos_step = (power(n+1)+power(-n-1)-power(n)-power(-n))/2
            sin_step_times_i = (power(n+1)-power(-n-1)-power(n)+power(-n))/2
            require(reduce(cos_step**2-denominator*(1-c)/2) == 0,
                    "forward cosine difference for the initial physical field")
            require(reduce(-sin_step_times_i**2-denominator*(1+c)/2) == 0,
                    "forward sine difference for the initial physical field")
        require(reduce(sum(phase_cosines)) == 0, "exact mean CAR action invariant")
        require(reduce(sum(c*c for c in phase_cosines)) == F(length,2),
                "exact second moment of the genuine discrete oscillations")
        checked.append(length)
    return checked


def exact_first_digit_coefficients():
    pinned = runpy.run_path(str(HERE.parent/"round173/check_first_selector_digit_source.py"))
    allocations, counts = pinned["split_actual_selector"]()
    signed = lambda j: (-1)**j
    full = [sum(signed(j)*(j+1)**(k+1)*n for j,n in enumerate(allocations))
            for k in range(1,9)]
    partial = [sum(signed(j)*(j+1)**(k+1)*row[0] for j,row in enumerate(counts))
               for k in range(1,9)]
    require(full == [705600]+[0]*7, "complete late interpolation")
    require(partial[1] == 83482704, "strict leading first-digit coefficient")
    for k in range(3,9):
        require(abs(partial[k-1]) <= partial[1]*4**(k-2), "certified partial coefficient envelope")
    return counts, partial


def verify_relative_error(coefficients, partial):
    c1, c2 = coefficients[1:3]
    require(c1.a > 0 and c2.b < 0, "leading two CAR coefficients")
    sign_ratio = -c2/c1
    require(sign_ratio.a > mp.iv.mpf("1.68") and sign_ratio.b < mp.iv.mpf("1.70"),
            "owned normalized ratio")
    for coefficient in coefficients[3:]:
        require(abs(coefficient).b < (-c2).a, "all higher terms have smaller coefficients")
    sigma, max_h, max_t, min_t = F(1,64), F(1,512), F(3,4), F(1,4)
    remainder = sum(
        F(abs(partial[k-1]),partial[1])*(max_h*sigma)**(k-2)
        * k*(1+max_t)**(k-1)/min_t
        for k in range(3,9)
    )
    require(remainder < F(1,200), "uniform strict sign with all eight terms")
    return sign_ratio


def verify_normalized_source(p, counts, partial, coefficient_ratio):
    mp.iv.dps = 60
    r = p**2
    bounds = []
    for bit in (0,1):
        scale = p**(35-bit)
        odd = sum(row[bit] for row in counts[::2])*scale
        even = sum(row[bit] for row in counts[1::2])*scale
        perturb = mp.iv.mpf(".01")*(odd+even)
        sector = []
        for baseline in (r,mp.iv.mpf(1)):
            middle = odd*baseline+even*(1-baseline)
            low, high = middle-perturb, middle+perturb
            require(low.a > mp.iv.mpf(".12") and high.b < mp.iv.mpf(".51"),
                    "conditional output interior after division by actual fixed efficiency")
            sector.append((low,high))
        bounds.append(sector)
    for address_zero,address_one in zip(*bounds):
        require((address_zero[0]-address_one[1]).a > mp.iv.mpf(".08"),
                "strict opposite address slopes yield a nonzero entropy derivative")
    ln_phi = -mp.iv.ln(p)
    low_entropy = mp.iv.ln(1+mp.iv.mpf(".08")/mp.iv.mpf(".51"))/ln_phi
    high_entropy = (mp.iv.ln(mp.iv.mpf(".51")/mp.iv.mpf(".12"))
                    -mp.iv.ln(mp.iv.mpf(".49")))/ln_phi
    source_lo = (mp.iv.mpf("23")*coefficient_ratio*partial[1]/705600
                 / 64**2*mp.iv.mpf(".25")*mp.iv.mpf(".995")*low_entropy)
    source_hi = (mp.iv.mpf("24")*coefficient_ratio*partial[1]/705600
                 / 64**2*mp.iv.mpf(".75")*mp.iv.mpf("1.005")*high_entropy)
    require(source_lo.a > mp.iv.mpf(".08") and source_hi.b < 5,
            "two-sided normalized transverse-source enclosure")


def main():
    mp.iv.dps = 65
    p = (mp.iv.sqrt(5)-1)/2
    layers = exact_wave_witnesses()
    counts, partial = exact_first_digit_coefficients()
    ratio = verify_relative_error(sc1_coefficients(p),partial)
    verify_normalized_source(p,counts,partial,ratio)
    print(json.dumps({
        "status":"PASS",
        "exact_material_car_wave_lattices":layers,
        "material_level":"1/64",
        "ellipse_coordinate_range":["1/4","3/4"],
        "whole_late_scalar_constant_on_entire_family":True,
        "first_digit_cubic_setting_moment":partial[1],
        "max_relative_higher_term":"1/200",
        "informational_source_divided_by_actual_conditional_gain_and_step":["-5","-.08"],
        "physical_native_admission_for_a_smooth_family_proved":False,
        "GR_closed":False,
    },indent=2))


if __name__ == "__main__":
    main()
