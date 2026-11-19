#!/usr/bin/env python3
"""Exact bounded application of the endpoint-isometric field-writing map.

This is a fixed COORDINATE positive-pairing obstruction under the declared
contravariant solder dictionary. Moving the solder also moves that pairing;
an explicit hostile control prevents a universal field-writing exclusion.
No engine orbit, geometric Euler calculation, physical force or price is
replayed or selected. Standard library; checks remain active under -O.
"""

from fractions import Fraction as R
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


SOURCE_PINS = {
    "02_REGISTRY/research/A4D_NATIVE_MATTER_OBSERVER_PAIRING.md":
        "badfe4177ddcd90f9b138419b84afa8f828574c7b7d191df5fec8f266f1130f9",
    "02_REGISTRY/research/A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md":
        "f54810cf9cc16f2282eb602fa606381cdd9622c7f877fef5211e978c55e4956c",
    "02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md":
        "601e5bb9203789a66ad2a945aad30da92b6233ac40417d54c6b47c95dc43536b",
    "02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md":
        "8dbca8ff9a4567a2baf216357b5d3ffa2d217281ced4e5d0e535257db2f5e83e",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/RESULT.md":
        "290772fb869cfa73ed0cc419d3182048d80ea9b02312be0b9d56ad558f5c47be",
    "02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md":
        "36eaeb8617630acaeace297fa64e7b8c33b92fc4824133a2b8e3515c4c79520a",
    "02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py":
        "7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_CAR_ACTUATED_METRIC.md":
        "b9dd63f0888a062941c1744d800120e47d20777f429f892f5a98c504a3c0a4be",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rejection(test, message):
    try:
        test()
    except RuntimeError:
        return message
    raise RuntimeError("negative control unexpectedly accepted: " + message)


class Poly:
    """Small exact sparse Laurent ring; only monomials may be inverted."""

    def __init__(self, value=0):
        if isinstance(value, dict):
            self.terms = {m: R(c) for m, c in value.items() if c}
        elif isinstance(value, Poly):
            self.terms = value.terms.copy()
        else:
            self.terms = {(): R(value)} if value else {}

    @classmethod
    def variable(cls, name):
        return cls({((name, 1),): R(1)})

    def __add__(self, other):
        result = self.terms.copy()
        for monomial, coefficient in Poly(other).terms.items():
            result[monomial] = result.get(monomial, R(0)) + coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        result = {}
        for left, a in self.terms.items():
            for right, b in Poly(other).terms.items():
                powers = dict(left)
                for name, exponent in right:
                    powers[name] = powers.get(name, 0) + exponent
                monomial = tuple(sorted((n, e) for n, e in powers.items() if e))
                result[monomial] = result.get(monomial, R(0)) + a * b
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int), "integer Laurent exponent")
        if exponent < 0:
            require(len(self.terms) == 1, "only a nonzero monomial is invertible")
            monomial, coefficient = next(iter(self.terms.items()))
            return Poly({tuple((n, e * exponent) for n, e in monomial):
                         coefficient ** exponent})
        result = Poly(1)
        for _ in range(exponent):
            result *= self
        return result

    def __eq__(self, other):
        return self.terms == Poly(other).terms

    def __bool__(self):
        return bool(self.terms)


def eye(n=4):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def transpose(a):
    return tuple(zip(*a))


def madd(a, b):
    return tuple(tuple(x + y for x, y in zip(row, other))
                 for row, other in zip(a, b))


def mscale(a, scalar):
    return tuple(tuple(scalar * x for x in row) for row in a)


def mmul(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(row, column))
                       for column in transpose(b)) for row in a)


def outer(v):
    return tuple(tuple(x * y for y in v) for x in v)


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def determinant(a):
    total = 0
    for permutation in permutations(range(len(a))):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(len(a)) for j in range(i + 1, len(a)))
        term = (-1) ** inversions
        for i, j in enumerate(permutation):
            term *= a[i][j]
        total += term
    return total


def inverse(a):
    n = len(a)
    rows = [[R(x) for x in row] + [R(i == j) for j in range(n)]
            for i, row in enumerate(a)]
    for column in range(n):
        pivot = next((i for i in range(column, n) if rows[i][column]), None)
        require(pivot is not None, "invertible rational matrix")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [x / scale for x in rows[column]]
        for i in range(n):
            if i != column:
                scale = rows[i][column]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[column])]
    return tuple(tuple(row[n:]) for row in rows)


def quadratic(a, v):
    return sum(v[i] * a[i][j] * v[j] for i in range(4) for j in range(4))


def frobenius_squared(a):
    return sum(x * x for row in a for x in row)


def pairing_norm_squared(a, g):
    # Exactly ||Q^(-1/2) A Q^(-1/2)||_F^2 for symmetric A and G=Q^-1.
    return trace(mmul(mmul(g, a), mmul(g, a)))


def endpoint(q_positive, w):
    g = inverse(q_positive)
    norm = quadratic(g, w)
    require(norm > 0, "nonzero first grade in positive pairing")
    return madd(mscale(q_positive, -1), mscale(outer(w), 2 / norm))


def positive(a):
    return a == transpose(a) and all(
        determinant(tuple(tuple(a[i][j] for j in range(k)) for i in range(k))) > 0
        for k in range(1, 5))


def check_universal_algebra():
    # For arbitrary SPD Q=L L^T write w=L u.  Then
    # q=L[-I+2uu^T/(u^Tu)]L^T.  Clearing the positive denominator
    # checks the universal matrix polynomial, rather than sampling Q.
    u = tuple(Poly.variable("u" + str(i)) for i in range(4))
    d = sum(x * x for x in u)
    numerator = madd(mscale(eye(), -d), mscale(outer(u), 2))
    require(trace(numerator) == -2 * d, "universal trace in dimension four")
    require(mmul(numerator, numerator) == mscale(eye(), d * d),
            "universal involution after clearing the positive denominator")

    b = tuple(tuple(Poly.variable("b%d%d" % (min(i, j), max(i, j)))
                    for j in range(4)) for i in range(4))
    remainder = sum((b[i][i] - b[j][j]) ** 2
                    for i in range(4) for j in range(i + 1, 4))
    remainder += 8 * sum(b[i][j] ** 2 for i in range(4) for j in range(i + 1, 4))
    require(4 * frobenius_squared(b) - trace(b) ** 2 == remainder,
            "exact sum-of-squares Frobenius trace bound")
    return {
        "generic_positive_Q": "arbitrary invertible congruence of exact 4-variable polynomial identity",
        "invariants": ["Tr(Q^-1 q)=-2", "q Q^-1 q=Q"],
        "closed_set": "continuous image of the unit sphere; analytical compactness argument",
        "weighted_Frobenius_bound": "||q_target-r||_Q >= |Tr(Q^-1 q_target)+2|/2",
        "trace_bound_certificate": "sum of 6 diagonal-difference squares and 6 off-diagonal squares",
    }


ETA_NULL = ((0, 1, 0, 0), (1, 0, 0, 0),
            (0, 0, -1, 0), (0, 0, 0, -1))
ETA_REST = ((1, 0, 0, 0), (0, -1, 0, 0),
            (0, 0, -1, 0), (0, 0, 0, -1))
T = ((1, R(1, 2), 0, 0), (1, R(-1, 2), 0, 0),
     (0, 0, 1, 0), (0, 0, 0, 1))
VV = outer((0, 1, 0, 0))


def coframe(h):
    return ((1, 0, 0, 0), (R(1, 2) * h, 1, 0, 0),
            (0, 0, 1, 0), (0, 0, 0, 1))


def primary_pair(h, kappa, q_internal):
    e = coframe(h)
    f = coframe(-h)
    q = mscale(mmul(mmul(f, ETA_NULL), transpose(f)), kappa)
    pairing = mscale(mmul(mmul(f, q_internal), transpose(f)), kappa)
    return e, f, q, pairing


def check_symbolic_primary():
    h, s, kappa = (Poly.variable(name) for name in ("H", "s", "kappa"))
    tinv = inverse(T)
    require(mmul(mmul(transpose(T), ETA_REST), T) == ETA_NULL,
            "owned rational null-to-rest dictionary")
    internal = mmul(tinv, transpose(tinv))
    require(internal == ((R(1, 2), 0, 0, 0), (0, 2, 0, 0),
                         (0, 0, 1, 0), (0, 0, 0, 1)),
            "actual primary rest-clock observer positive pairing in null coordinates")
    e, f, q, pairing = primary_pair(h, kappa, internal)
    g = mmul(mmul(transpose(e), ETA_NULL), e)
    require(mmul(e, f) == eye(), "symbolic inverse coframe")
    require(g == ((h, 1, 0, 0), (1, 0, 0, 0),
                  (0, 0, -1, 0), (0, 0, 0, -1)), "full primary covariant metric")
    require(mmul(g, q) == mscale(eye(), kappa),
            "quotient metric is contravariant kappa times inverse g")
    require(determinant(e) == 1 and determinant(g) == -1,
            "profile changes preserve determinant and fixed calibration density")
    frest = mmul(f, tinv)
    require(q == mscale(mmul(mmul(frest, ETA_REST), transpose(frest)), kappa),
            "actual rest coframe T E has the same Lorentz quotient")
    require(pairing == mscale(mmul(frest, transpose(frest)), kappa),
            "actual coordinate pairing carries the rest solder")
    g_positive = mscale(mmul(mmul(transpose(e), mmul(transpose(T), T)), e), kappa ** -1)
    require(mmul(g_positive, pairing) == eye(), "symbolic inverse positive pairing")
    # This also checks the actual unit rest observer, without adjoining sqrt(kappa).
    observer = tuple(frest[i][0] for i in range(4))
    require(quadratic(mscale(g, kappa ** -1), observer) == kappa ** -1,
            "actual transported rest observer has the retained timelike normalization")
    require(madd(mscale(q, -1), mscale(outer(observer), 2 * kappa)) == pairing,
            "moving-solder pair is generated by the owned observer formula")
    for size in range(1, 5):
        minor = tuple(tuple(pairing[i][j] for j in range(size)) for i in range(size))
        expected = kappa * R(1, 2) if size == 1 else kappa ** size
        require(determinant(minor) == expected, "positive leading principal minor for kappa>0")

    _, _, target, moved_pairing = primary_pair(h + s, kappa, internal)
    difference = madd(target, mscale(q, -1))
    require(difference == mscale(VV, -kappa * s),
            "exact primary profile perturbation is contravariant vv rank one")
    trace_gap = trace(mmul(g_positive, target)) + 2
    require(trace(mmul(g_positive, q)) == -2, "initial primary point lies on its leaf")
    require(g_positive[1][1] == R(1, 2) * kappa ** -1,
            "actual rational-null primary G_vv")
    require(trace_gap == -kappa * s * g_positive[1][1] == -s * R(1, 2),
            "nonzero fixed-coordinate-pairing trace gap")
    require(trace_gap ** 2 * R(1, 4) == s ** 2 * R(1, 16),
            "actual primary weighted separation squared is s^2/16")
    require(mmul(mmul(q, g_positive), q) == pairing,
            "symbolic primary involution")
    moved_g = mscale(mmul(mmul(transpose(coframe(h + s)), mmul(transpose(T), T)),
                          coframe(h + s)), kappa ** -1)
    require(trace(mmul(moved_g, target)) == -2,
            "each moving-solder endpoint obeys its own trace invariant")
    require(mmul(mmul(target, moved_g), target) == moved_pairing,
            "each moving-solder endpoint obeys its own involution")
    pairing_change = madd(moved_pairing, mscale(pairing, -1))
    expected_change = ((0, -kappa * s * R(1, 4), 0, 0),
                       (-kappa * s * R(1, 4), kappa * (h * s * R(1, 4) + s ** 2 * R(1, 8)), 0, 0),
                       (0, 0, 0, 0), (0, 0, 0, 0))
    require(pairing_change == expected_change and pairing_change != mscale(eye(), 0),
            "actual moving solder changes coordinate Q even with internal data fixed")

    # A valid different observer/convention has positive internal Q=I.
    # It is deliberately not substituted for the owned primary rest-clock input.
    _, _, alternate_q, alternate_pairing = primary_pair(h, kappa, eye())
    alternate_g = mscale(mmul(transpose(e), e), kappa ** -1)
    require(alternate_q == q and mmul(alternate_g, alternate_pairing) == eye(),
            "Q_internal=I alternative leaves Lorentz q unchanged")
    require(trace(mmul(alternate_g, target)) + 2 == -s,
            "alternate observer has the separately typed trace gap")
    controls = [
        rejection(lambda: require(q == mscale(g, kappa), "covariant metric conflation"),
                  "covariant g is not quotient q"),
        rejection(lambda: require(internal == eye(), "rational null Gram omitted"),
                  "owned rational rest-to-null map is not Euclidean orthogonal"),
        rejection(lambda: require(trace(mmul(g_positive, target)) == -2,
                                  "rank-one target on fixed leaf"),
                  "nonzero profile target fails fixed-Q invariant"),
        rejection(lambda: require(moved_pairing == pairing, "moving solder freezes Q"),
                  "fixed internal Q does not mean fixed coordinate Q"),
    ]
    return {
        "symbolic_variables": "arbitrary real H,s; fixed positive kappa",
        "full_matrix_dimension": 4,
        "actual_null_positive_internal": "diag(1/2,2,1,1)",
        "quotient_dictionary": "q_H=kappa*(E_H^T eta_null E_H)^-1",
        "profile_change": "delta q=-kappa*s*e_v e_v^T",
        "general_initial_observer_trace_gap": "-kappa*s*(Q_0^-1)_vv",
        "actual_primary_observer_trace_gap": "-s/2",
        "actual_primary_weighted_Frobenius_lower_bound": "abs(s)/4",
        "alternate_Qinternal_I_trace_gap": "-s",
        "moving_solder_control": "q and coordinate Q both change; internal eta and Q fixed",
    }, controls


def check_rational_transitions():
    cholesky = ((2, 0, 0, 0), (R(1, 3), 1, 0, 0),
                (R(-1, 2), R(2, 5), R(3, 2), 0), (1, R(-1, 4), R(1, 7), R(4, 3)))
    candidates = (eye(), ((4, 0, 0, 0), (0, R(1, 4), 0, 0),
                         (0, 0, 2, 0), (0, 0, 0, R(1, 2))),
                  mmul(cholesky, transpose(cholesky)))
    vectors = ((1, 0, 0, 0), (1, R(2, 3), R(-1, 4), R(1, 5)),
               (R(-3, 7), 1, 2, R(1, 2)))
    controls = []
    count = 0
    for pairing in candidates:
        require(positive(pairing), "exact Sylvester positivity of rational Q")
        g = inverse(pairing)
        outputs = []
        for w in vectors:
            q = endpoint(pairing, w)
            outputs.append(q)
            require(trace(mmul(g, q)) == -2, "rational trace invariant")
            require(mmul(mmul(q, g), q) == pairing, "rational full involution")
            require(determinant(q) == -determinant(pairing), "Lorentz determinant")
            q_inverse = inverse(q)
            norm = quadratic(q_inverse, w)
            require(norm == quadratic(g, w) > 0, "new first grade is genuinely timelike")
            require(madd(mscale(q, -1), mscale(outer(w), 2 / norm)) == pairing,
                    "observer construction recovers preserved Q")
            require(endpoint(pairing, tuple(-3 * x for x in w)) == q,
                    "observer-line scaling and sign do not change endpoint")
            count += 1
        require(all(outputs[i] != outputs[j] for i in range(3) for j in range(i + 1, 3)),
                "nonparallel endpoint transitions actually change the metric")
        target = madd(outputs[0], mscale(VV, R(-2, 7)))
        gap = trace(mmul(g, target)) + 2
        require(gap == R(-2, 7) * g[1][1] and gap != 0,
                "arbitrary SPD-Q rank-one target trace defect")
        for reachable in outputs:
            delta = madd(target, mscale(reachable, -1))
            require(4 * pairing_norm_squared(delta, g) >= gap * gap,
                    "weighted Frobenius separation for every tested endpoint")
            require(frobenius_squared(delta) * frobenius_squared(g) >= gap * gap,
                    "ordinary Frobenius separation retains the full G norm")
        controls.append(rejection(lambda: require(outputs[1] == outputs[0], "frozen q"),
                                  "fixed Q permits nonparallel q motion"))
    return {"positive_Q_fixtures": len(candidates), "exact_endpoints": count,
            "checks": "full trace, involution, timelike inverse, determinant, line scaling and both norm bounds"}, controls


def check_inheritance():
    # The pinned executor uses modes(n)=(n+2)^4 and pi(child)=child%modes(n).
    # Only this explicit adapter is tested; no engine transitions are run.
    diagnostics = []
    for stage in (0, 1, 2):
        parents, children = (stage + 2) ** 4, (stage + 3) ** 4
        projection = tuple(y % parents for y in range(children))
        multiplicities = tuple(projection.count(x) for x in range(parents))
        require(min(multiplicities) > 0, "actual archive projection is surjective")
        weights = tuple(R(2 * x + 1, parents ** 2) for x in range(parents))
        # Symmetric parent matrices, including off-diagonal coordinates twice.
        fields = tuple(((R(x + 1, 5), R(1, 3), 0, 0),
                        (R(1, 3), R(-x, 7), 0, 0),
                        (0, 0, R(2, 5), 0), (0, 0, 0, R(-1, 2)))
                       for x in range(parents))
        pairings = tuple(primary_pair(R(x, parents), R(3, 2), eye())[3]
                         for x in range(parents))
        norms = tuple(pairing_norm_squared(a, inverse(q)) for a, q in zip(fields, pairings))
        parent_norm = sum(mu * norm for mu, norm in zip(weights, norms))
        child_norm = sum(weights[x] * norms[x] / multiplicities[x] for x in projection)
        require(sum(weights) == 1 and child_norm == parent_norm,
                "actual hereditary weighted squared-norm identity")
        diagnostics.append({"stage": stage, "parents": parents, "children": children,
                            "multiplicity_min": min(multiplicities),
                            "multiplicity_max": max(multiplicities)})
    omitted_weights_mass = sum(weights[x] for x in projection)
    controls = [rejection(lambda: require(omitted_weights_mass == 1, "omit child multiplicity"),
                          "unweighted copying is not the inherited isometry"),
                rejection(lambda: require(frobenius_squared(outer((1, 1, 0, 0))) == 3,
                                          "count symmetric off diagonal once"),
                          "Frobenius norm retains both off-diagonal entries")]
    return {"projection": "child % (stage+2)^4", "levels": diagnostics,
            "norm_identity": "sum_child mu_parent/d_parent * ||A_parent||_Q^2 = sum_parent mu_parent*||A_parent||_Q^2",
            "scope": "ordinary inheritance with stated conditional weights; no physical refinement trigger"}, controls


def main():
    root = Path(__file__).resolve().parents[5]
    for relative, expected in SOURCE_PINS.items():
        require(sha256((root / relative).read_bytes()).hexdigest() == expected,
                "pinned source changed: " + relative)
    generic = check_universal_algebra()
    primary, primary_controls = check_symbolic_primary()
    rational, rational_controls = check_rational_transitions()
    inheritance, inheritance_controls = check_inheritance()
    print(json.dumps({
        "status": "PASS",
        "scope": "fixed coordinate pairing and fixed contravariant dictionary only",
        "generic": generic,
        "primary": primary,
        "rational_controls": rational,
        "inheritance": inheritance,
        "negative_controls": primary_controls + rational_controls + inheritance_controls,
        "source_sha256": SOURCE_PINS,
        "physical_joint_step_derived": False,
        "full_paid_graph_or_GR_selection_derived": False,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
