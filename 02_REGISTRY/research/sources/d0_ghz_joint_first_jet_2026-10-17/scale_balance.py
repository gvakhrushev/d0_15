"""Full16 continuum leading scale equation, at the unchanged v8 parameters.

New interval calculation only: no lattice spectrum/root suite is imported.
Gaussian tails and the feedback cycle tail are explicitly enclosed.
"""
import json
from fractions import Fraction
import mpmath as mp


mp.iv.dps = 55
iv = mp.iv
ONE = iv.mpf(1)
BETA = 3-iv.sqrt(5)
ZCOIN = ONE/(2**20)
MULTIPLICITY = 128
RATIO = ZCOIN/(1-ZCOIN)
GAUSSIAN_CUT = 32
CYCLE_CUT = 3


def enclose_fraction(value):
    f = Fraction(value)
    return iv.mpf(f.numerator)/f.denominator


def scale_interval(lo, hi):
    return iv.mpf([enclose_fraction(lo).a, enclose_fraction(hi).b])


def gaussian_moments(t):
    """Enclose sum k^(2r) exp(-t k^2), r=0,1,2, on Z."""
    result = []
    for degree in (0, 2, 4):
        finite = ONE if degree == 0 else iv.mpf(0)
        for k in range(1, GAUSSIAN_CUT+1):
            finite += 2*k**degree*iv.exp(-t*k*k)
        first = GAUSSIAN_CUT+1
        ratio = (iv.mpf(first+1)/first)**degree*iv.exp(-t*(2*first+1))
        if not bool(ratio.b < 1):
            raise ArithmeticError("Gaussian tail ratio is not contractive")
        tail = 2*first**degree*iv.exp(-t*first*first)/(1-ratio)
        result.append(finite+iv.mpf([0, tail.b]))
    return result


def traces(scale, cycle):
    theta, second, fourth = gaussian_moments(cycle*BETA/scale**2)
    Z = 16*theta**4
    T = 64*second*theta**3/scale**2
    U = (64*fourth*theta**3+192*second**2*theta**2)/scale**4
    Tp = (-2*T+2*cycle*BETA*U)/scale
    return Z, T, U, Tp


def equation(lo, hi=None):
    scale = scale_interval(lo, lo if hi is None else hi)
    Z, T, U, Tp = traces(scale, 1)
    Zp = 2*BETA*T/scale
    series = iv.mpf(0)
    derivative_series = iv.mpf(0)
    for r in range(CYCLE_CUT+1):
        _, Tj, _, Tjp = traces(scale, r+1)
        series += (-RATIO)**r*Tj
        derivative_series += (-RATIO)**r*Tjp
    # Absolute cycle tails: T_j<=T_1, U_j<=U_1. Derivative uses
    # |T_j'| <= (2/s)(T_1+j beta U_1), summed geometrically.
    first = CYCLE_CUT+1
    power_tail = RATIO**first/(1-RATIO)
    j_tail = RATIO**first*((first+1)-first*RATIO)/(1-RATIO)**2
    value_tail = (power_tail*T).b
    derivative_tail = ((2/scale)*(power_tail*T+BETA*j_tail*U)).b
    series += iv.mpf([-value_tail, value_tail])
    derivative_series += iv.mpf([-derivative_tail, derivative_tail])
    coefficient = MULTIPLICITY*BETA*ZCOIN/(1-ZCOIN)
    value = scale**-2-T/Z+coefficient*series
    derivative = -2/scale**3-Tp/Z+T*Zp/Z**2+coefficient*derivative_series
    return value, derivative, MULTIPLICITY*ZCOIN*BETA*Z


def endpoints(x):
    return [str(x.a), str(x.b)]


def run():
    lo, hi = Fraction(12, 5), Fraction(5, 2)
    left, _, _ = equation(lo)
    right, _, _ = equation(hi)
    if not (bool(left.b < 0) and bool(right.a > 0)):
        raise ArithmeticError("Actual leading radial equation not bracketed")
    coarse_lo, coarse_hi = lo, hi
    derivative_boxes = []
    for j in range(16):
        lower = coarse_lo+(coarse_hi-coarse_lo)*j/16
        upper = coarse_lo+(coarse_hi-coarse_lo)*(j+1)/16
        _, derivative_box, _ = equation(lower, upper)
        if not bool(derivative_box.a > 0):
            raise ArithmeticError("Coarse bracket derivative not positive")
        derivative_boxes.append(derivative_box)
    for _ in range(25):
        middle = (lo+hi)/2
        value, _, _ = equation(middle)
        if bool(value.b < 0):
            lo = middle
        elif bool(value.a > 0):
            hi = middle
        else:
            raise ArithmeticError("Bisection sign enclosure undecided")
    _, derivative, budget = equation(lo, hi)
    if not bool(derivative.a > 0):
        raise ArithmeticError("Local scale root not unique")
    if not bool(budget.b < 1):
        raise ArithmeticError("Full scale-source necessary bound violated")
    return {
        "schema": "d0-ghz-actual-leading-scale/1",
        "status": "PASS",
        "scale_interval_rational": [str(lo), str(hi)],
        "scale_interval_decimal": [float(lo), float(hi)],
        "left_initial_balance": endpoints(left),
        "right_initial_balance": endpoints(right),
        "root_bracket_derivative": endpoints(derivative),
        "initial_bracket_uniqueness_derivative_boxes": [endpoints(x) for x in derivative_boxes],
        "root_bracket_M_z_beta_Z": endpoints(budget),
        "beta": "3-sqrt(5)", "z": "2^-20", "M": 128,
        "full_Fock_trace_multiplicity": 16,
        "period": "2*pi", "gaussian_cut": GAUSSIAN_CUT,
        "feedback_cycle_cut": CYCLE_CUT,
        "interval_decimal_precision": iv.dps,
        "old_spectrum_or_root_replayed": False,
        "scale_is_solved_not_calibration_fitted": True,
        "leading_joint_source_scale_only": True,
        "finite_stationary_sequence_proved": False,
        "physical_preparation_admission_proved": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
