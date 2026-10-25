"""Cofinal reflected-source budgets and a literal read-only request adapter.

Rational models below are comparison arithmetic, not new gate primitives.
Native fixtures consume the old reflected-word identities without replaying
their matrix proofs.  The request adapter does emit literal G/CX/SourceI.
Neither finite endpoints nor their catalogues assert a physical C1 selector.
"""
from dataclasses import dataclass, replace
from fractions import Fraction
from math import isqrt
from pathlib import Path
import sys

SOURCES = Path(__file__).resolve().parent.parent
REFLECTED = SOURCES / "d0_exact_report_reflected_cohorts_2026-10-25"
sys.path.insert(0, str(REFLECTED))
import reflected_report as rr

native = rr.native
if Path(rr.__file__).resolve() != (REFLECTED / "reflected_report.py").resolve():
    raise ImportError("the owned reflected-report sibling is required")


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("an exact integer or Fraction is required")
    return Fraction(value)


def ceil_fraction(value):
    value = rational(value)
    return -(-value.numerator // value.denominator)


def ceil_fourth_root(value):
    if type(value) is not int or value < 0:
        raise ValueError("a nonnegative integer is required")
    lower = isqrt(isqrt(value))
    return lower + (lower**4 != value)


def parity(value):
    return bin(value).count("1") % 2


@dataclass(frozen=True)
class MeshBudget:
    k: int
    ell_sq: Fraction
    g: Fraction
    c_quad: Fraction
    other: tuple[Fraction, ...] = ()

    @property
    def gbar(self):
        return rational(self.g) * rational(self.c_quad)


def integer_envelopes(budgets):
    """C_m is a declared certified finite envelope; m is one-based."""
    envelopes, previous = [], 1
    for level, budget in enumerate(budgets, 1):
        if type(budget.k) is not int or budget.k < 1:
            raise ValueError("the finite report order is a positive integer")
        ell_sq, gbar = rational(budget.ell_sq), budget.gbar
        if ell_sq <= 0 or gbar <= 0:
            raise ValueError("positive physical lift and gain are required")
        values = (Fraction(previous), Fraction(level), Fraction(budget.k**2),
                  ell_sq, 1/gbar, *map(rational, budget.other))
        if any(value <= 0 for value in values):
            raise ValueError("certified auxiliary envelopes must be positive")
        previous = max(map(ceil_fraction, values))
        envelopes.append(previous)
    if not envelopes:
        raise ValueError("at least one mesh budget is required")
    return tuple(envelopes)


def mesh_level(index, envelopes):
    """Finite-catalogue prefix of m(j); the first finite exception stays level1."""
    if type(index) is not int or index < 1:
        raise ValueError("the cohort index is a positive integer")
    if not envelopes or any(type(v) is not int or v < i
            for i, v in enumerate(envelopes, 1)):
        raise ValueError("positive integer envelopes must dominate their level")
    if tuple(sorted(envelopes)) != tuple(envelopes):
        raise ValueError("envelopes must be nondecreasing")
    return max((level for level, value in enumerate(envelopes, 1)
                if value**64 <= index), default=1)


def cohort_size(index, order):
    if type(index) is not int or index < 1 or type(order) is not int or order < 1:
        raise ValueError("positive integer cohort index and report order required")
    return max(2, ceil_fourth_root(order**8 * index**3))


def physical_lift_sq(counts, ell_squares):
    if len(counts) != len(ell_squares) or not counts:
        raise ValueError("matching nonempty count/lift lists required")
    if any(type(n) is not int or n < 1 for n in counts):
        raise ValueError("packet counts are positive integers")
    values = tuple(map(rational, ell_squares))
    if any(value <= 0 for value in values):
        raise ValueError("physical lift squares must be positive")
    return sum((n*value for n, value in zip(counts, values)), Fraction())


def prefix_quantities(rows, zeta=Fraction(1, 2**20), *, protected_rank=4):
    """Actual one-closing determinant and its physical common-source gain.

Each row has alpha,gamma,q,g,c_quad, with Dq=g*c_quad*E+error.
The input values are exact arithmetic models, not supplied native angles.
"""
    zeta = rational(zeta)
    if not 0 < zeta < 1 or type(protected_rank) is not int or protected_rank < 1:
        raise ValueError("positive rank and zeta in (0,1) required")
    product, coefficients = Fraction(1), []
    for row in rows:
        alpha, gamma, q, g, c_quad = (rational(row[name]) for name in
            ("alpha", "gamma", "q", "g", "c_quad"))
        if not (1 <= alpha <= 2 and Fraction(1, 2) <= gamma <= 1
                and 0 < q < Fraction(1, 2) and g > 0 and c_quad > 0):
            raise ValueError("the actual positive compact report/gain collar is required")
        x = gamma*q
        t = 1-alpha*x*(1-x)
        a = alpha*gamma*(1-2*x)/t
        product *= t
        coefficients.append((a, g*c_quad, t))
    if not coefficients:
        raise ValueError("a finite nonempty prefix is required")
    rank = protected_rank * (1 << len(coefficients))
    denominator = 1-zeta+zeta*product
    weight = rank*zeta*product/denominator
    A = sum((a*gbar for a, gbar, _ in coefficients), Fraction())
    return {"product": product, "rank": rank, "denominator": denominator,
            "weight": weight, "A": A, "gain": weight*A,
            "coefficients": tuple(coefficients)}


def normalized_source(rows, report_derivatives, zeta=Fraction(1, 2**20)):
    data = prefix_quantities(rows, zeta)
    if len(report_derivatives) != len(data["coefficients"]):
        raise ValueError("every actual report derivative is retained")
    numerator = sum((a*rational(dq) for (a, _, _), dq in
                     zip(data["coefficients"], report_derivatives)), Fraction())
    return numerator/data["A"]


def physical_certificate_sq(rows, variances, lift_sq):
    """Square of K||D_Psi J||/Gamma, with the true physical factor4."""
    data = prefix_quantities(rows)
    if len(variances) != len(rows) or rational(lift_sq) <= 0:
        raise ValueError("matching variance rows and positive lift square required")
    product = Fraction(1)
    for variance in variances:
        variance = rational(variance)
        if variance < 0:
            raise ValueError("variance cannot be negative")
        product *= 1+variance
    return 16*rational(lift_sq)*(product-1)/(data["A"]**2)


def native_prefix(cohorts, *, old_right_count=1):
    """Small literal inventory/protection fixture, not the full canonical bank.

The old K1 reflected echo is copied onto disjoint private controls/meters.
Its previously proved all-column helper/spin identity is consumed here.
"""
    if type(cohorts) is not int or cohorts < 1:
        raise ValueError("positive finite prefix length required")
    if type(old_right_count) is not int or old_right_count < 0:
        raise ValueError("the oldRIGHT count is an explicit nonnegative integer")
    old = tuple(range(3, 3+old_right_count))
    start = 3+old_right_count
    gates, private = [], []
    for index in range(cohorts):
        control, meter = start+2*index, start+2*index+1
        source, _, _, _ = rr.echo_execution(1)
        mapping = {0: 0, 1: control, 2: meter, 3: 1, 4: 2}
        gates.extend(native.Gate(g.op, tuple(mapping[q] for q in g.wires))
                     for g in source.gates)
        private.append((control, meter))
    execution = native.Execution(start+2*cohorts,
        (0, *(pair[0] for pair in private)), old, tuple(gates),
        native.G_CX_SOURCE_I, 0, (1, 2))
    native.validate_execution(execution, **rr.bounds(execution))
    return execution, tuple(private)


def _linear_word(work, a):
    """An exact CNOT map taking local e0 to the nonzero binary vector a."""
    pivot = (a & -a).bit_length()-1
    word = []
    if pivot:
        p, q = work[0], work[pivot]
        word.extend((native.Gate("CX", (p, q)), native.Gate("CX", (q, p)),
                     native.Gate("CX", (p, q))))
    for bit in range(len(work)):
        if bit != pivot and a & (1 << bit):
            word.append(native.Gate("CX", (work[pivot], work[bit])))
    return tuple(word)


def keyed_star_word(execution, work, keys, a, exponent=1, request=0):
    """Exact read-only Walsh-localized native star-plane rotation.

On the chosen request it is exp(2**(n-1+d)*exponent*theta*J_(0,a));
on every other request it is EXACT identity, on all work/helper/spin
columns.  No ideal Boolean, continuous angle or supplied known-one is used.
"""
    work, keys = tuple(work), tuple(keys)
    if not work or len(set(work+keys)) != len(work+keys):
        raise native.DomainError("nonempty distinct work/key wires are required")
    if (type(a) is not int or not 0 < a < (1 << len(work))
            or type(exponent) is not int or exponent < 1
            or type(request) is not int or not 0 <= request < (1 << len(keys))):
        raise native.DomainError("invalid finite star-plane/request parameters")
    forbidden = set(execution.old_right) | set(execution.source_spin or ())
    if forbidden & set(work+keys):
        raise native.DomainError("the star compiler cannot address spin or oldRIGHT")
    if execution.profile != native.G_CX_SOURCE_I or execution.source_port in work+keys:
        raise native.DomainError("the adapter reserves a distinct source-I helper port")
    linear = _linear_word(work, a)
    wire_to_local = {wire: bit for bit, wire in enumerate(work)}
    images = []
    for bit in range(len(work)):
        image = 1 << bit
        for gate in linear:
            control, target = map(wire_to_local.__getitem__, gate.wires)
            if image & (1 << control):
                image ^= 1 << target
        images.append(image)
    positive = (native.Gate("G", (work[0],)),)*exponent
    negative = native.inverse_word(replace(execution, gates=positive),
                                   **rr.bounds(execution))
    result = []
    for subset in range(1 << len(keys)):
        flips = tuple(native.Gate("CX", (key, work[0]))
                       for bit, key in enumerate(keys) if subset & (1 << bit))
        power = negative if parity(subset & request) else positive
        for b in range(1 << len(work)):
            if parity(b & a) != 1:
                continue
            v = sum((parity(b & image) << bit)
                    for bit, image in enumerate(images)) ^ 1
            ladder = tuple(native.Gate("CX", (work[bit], work[0]))
                           for bit in range(1, len(work)) if v & (1 << bit))
            Q = ladder+linear
            result.extend(tuple(reversed(Q))+flips+power+tuple(reversed(flips))+Q)
    word = tuple(result)
    native.validate_execution(replace(execution, gates=word), **rr.bounds(execution))
    return word
