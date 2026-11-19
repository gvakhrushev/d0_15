"""Native matched-clock single-cohort forks and actual price-cofield helpers.

The small source words below are literal native contrasts, not a new GR
root or a continuous angle primitive.  Rational gain models are diagnostics.
"""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import sys

SOURCES = Path(__file__).resolve().parent.parent
REFLECTED = SOURCES / "d0_exact_report_reflected_cohorts_2026-10-25"
sys.path.insert(0, str(REFLECTED))
import reflected_report as rr

native = rr.native
if Path(rr.__file__).resolve() != (REFLECTED / "reflected_report.py").resolve():
    raise ImportError("the owned reflected source helper is required")


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("an exact integer or Fraction is required")
    return Fraction(value)


def source_echo(power, *, stages=153):
    """Actual G_control**power;M_ref;inverse, with real2CX padding.

    K1 middle has33 stages.  Inverse of every off-port G has11 stages.
    The default catalogue is r4,r5,r10 and its common clock153.
    """
    if type(power) is not int or power < 1 or type(stages) is not int:
        raise native.DomainError("positive integer source power and clock required")
    middle, controls, meter, m = rr.middle_execution(1)
    forward = (native.Gate("G", (controls[0],)),)*power
    backward = native.inverse_word(replace(middle, gates=forward), **rr.bounds(middle))
    body = forward+middle.gates+backward
    gap = stages-len(body)
    if gap < 0 or gap % 2:
        raise native.DomainError("this fixed-middle catalogue requires an even nonnegative gap")
    idle_pair = (native.Gate("CX", (controls[0], meter)),)*2
    execution = replace(middle, gates=body+idle_pair*(gap//2))
    native.validate_execution(execution, **rr.bounds(execution))
    return execution, controls[0], meter, m


def prefix_execution(cohorts, *, fork=None, base_power=5, stages=153,
                     old_right_count=1):
    """One baseline or one fixed fork(j,power); future blocks stay baseline.

    j is one-based.  Every finite prefix uses the predeclared common clock.
    Larger prefixes literally append blocks to the SAME fixed fork.
    """
    if type(cohorts) is not int or cohorts < 1:
        raise native.DomainError("a positive finite cohort count is required")
    if type(old_right_count) is not int or old_right_count < 0:
        raise native.DomainError("oldRIGHT multiplicity is an explicit nonnegative integer")
    if fork is not None and (not isinstance(fork, tuple) or len(fork) != 2
            or type(fork[0]) is not int or fork[0] < 1 or fork[0] > cohorts):
        raise native.DomainError("the fixed fork must already occur in this prefix")
    old = tuple(range(3, 3+old_right_count))
    start = 3+old_right_count
    gates, private = [], []
    for j in range(1, cohorts+1):
        power = fork[1] if fork is not None and j == fork[0] else base_power
        local, _, _, _ = source_echo(power, stages=stages)
        control, meter = start+2*(j-1), start+2*(j-1)+1
        mapping = {0: 0, 1: control, 2: meter, 3: 1, 4: 2}
        gates.extend(native.Gate(g.op, tuple(mapping[q] for q in g.wires))
                     for g in local.gates)
        private.append((control, meter))
    execution = native.Execution(start+2*cohorts,
        (0, *(pair[0] for pair in private)), old, tuple(gates),
        native.G_CX_SOURCE_I, 0, (1, 2))
    native.validate_execution(execution, **rr.bounds(execution))
    return execution, tuple(private)


def scalar_data(reports, alpha=Fraction(3, 2), gamma=Fraction(3, 4),
                zeta=Fraction(1, 2**20), *, protected_rank=4):
    alpha, gamma, zeta = map(rational, (alpha, gamma, zeta))
    if not 1 <= alpha <= 2 or not Fraction(1, 2) <= gamma <= 1 or not 0 < zeta < 1:
        raise ValueError("actual compact native gain conditions required")
    if type(protected_rank) is not int or protected_rank < 1:
        raise ValueError("the protected input rank is a positive integer")
    reports = tuple(map(rational, reports))
    if not reports or any(not 0 < q < Fraction(1, 2) for q in reports):
        raise ValueError("a nonempty positive report collar is required")
    grams = tuple(1-alpha*gamma*q*(1-gamma*q) for q in reports)
    slopes = tuple(alpha*gamma*(1-2*gamma*q)/t for q, t in zip(reports, grams))
    product = Fraction(1)
    for t in grams:
        product *= t
    rank = protected_rank*(1 << len(reports))
    denominator = 1-zeta+zeta*product
    weight = rank*zeta*product/denominator
    return dict(reports=reports, grams=grams, slopes=slopes, product=product,
                rank=rank, denominator=denominator, weight=weight)


def probe_relative_ratio(old_product, q0, qminus, qplus, *, alpha=Fraction(3, 2),
                         gamma=Fraction(3, 4), zeta=Fraction(1, 2**20), mp=None):
    """One-edge divided full-price gain / TRUE BASE chain gain.

    The old product can be arbitrarily small; no nominal standalone gain
    replaces the actual base.  mp supplies the requested numerical precision.
    """
    if mp is None:
        import mpmath as mp
    values = tuple(map(rational, (old_product, q0, qminus, qplus, alpha, gamma, zeta)))
    old_product, q0, qminus, qplus, alpha, gamma, zeta = values
    if not 0 < old_product <= 1:
        raise ValueError("the actual old scalar Gram product must be positive")
    data = scalar_data((q0, qminus, qplus), alpha, gamma, zeta)
    t0, tm, tp = data["grams"]
    a0 = data["slopes"][0]
    def num(x):
        return mp.mpf(x.numerator)/x.denominator
    old, zz = num(old_product), num(zeta)
    base_weight_per_rank = zz*old*num(t0)/(1-zz+zz*old*num(t0))
    if qplus == qminus:
        edge_weight_per_rank = zz*old*num(tm)/(1-zz+zz*old*num(tm))
        return edge_weight_per_rank*num(data["slopes"][1])/(base_weight_per_rank*num(a0))
    # log1p avoids catastrophic subtraction for a tiny old product.
    price_difference_per_rank = -mp.log1p(
        zz*old*(num(tp)-num(tm))/(1-zz+zz*old*num(tm)))
    beta_per_rank = price_difference_per_rank/num(qplus-qminus)
    return beta_per_rank/(base_weight_per_rank*num(a0))


def price_edge(reports, index, qminus, qplus, *, alpha=Fraction(3, 2),
               gamma=Fraction(3, 4), zeta=Fraction(1, 2**20), mp=None):
    if mp is None:
        import mpmath as mp
    if type(index) is not int or not 0 <= index < len(reports):
        raise ValueError("a valid cohort coordinate is required")
    data = scalar_data(reports, alpha, gamma, zeta)
    old = data["product"]/data["grams"][index]
    ratio = probe_relative_ratio(old, reports[index], qminus, qplus,
                                 alpha=alpha, gamma=gamma, zeta=zeta, mp=mp)
    def num(x):
        x = rational(x)
        return mp.mpf(x.numerator)/x.denominator
    beta = ratio*num(data["weight"]*data["slopes"][index])
    return beta*num(rational(qplus)-rational(qminus))


def cofield_error_budget(L, M3, gbar, delta, eta):
    L, M3, gbar, delta, eta = map(rational, (L, M3, gbar, delta, eta))
    if min(L, M3, gbar, delta) <= 0 or eta < 0:
        raise ValueError("positive finite norms/gain/spacing and nonnegative state error required")
    return (L/gbar)*(M3*delta**2/6+2*eta/delta)


def coordinate_chord_error(readout_norm, eta, delta):
    R, eta, delta = map(rational, (readout_norm, eta, delta))
    if R <= 0 or delta <= 0 or eta < 0:
        raise ValueError("positive readout norm/spacing and nonnegative error required")
    return 2*R*eta/delta
