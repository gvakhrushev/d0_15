#!/usr/bin/env python3
"""Bounded exact algebra for the central complete-pointer source theorem.

Only Python's standard library is used.  Rational probabilities are exact;
logarithms of positive rationals are represented by rational coefficients of
log(prime).  No numerical entropy, floating-point approximation, old checker,
golden derivative-bound replay, Lean invocation or native gate admission occurs.

Consumer: A4D_BACKWARD_EINSTEIN_SOURCE_COMPLETION.md, sections 3--4.
Owned input: A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md at
3f368179627acc9f2c3e9616df729ac2280a77a0, sections 1--4 and 8--9.

The fixtures have two old blocks of dimension two and two complete flag
outcomes per block.  They test the dimension-independent algebra proved in the
memo, and are not substitutions for the full AF, full16/reference128, original
golden instrument or its independently required total-cost/source contract.
All displayed entropies are in natural units; division by the fixed log(phi)
and addition of the owned constant programme price preserve these identities.
"""

from fractions import Fraction as F


class LogForm:
    """Exact affine form c + sum_p a_p log(p), with rational coefficients."""

    def __init__(self, terms=None):
        self.terms = {key: F(value) for key, value in (terms or {}).items()
                      if value}

    @classmethod
    def constant(cls, value):
        return cls({0: F(value)})

    @classmethod
    def logarithm(cls, value):
        value = F(value)
        if value <= 0:
            raise ValueError("logarithm requires a positive rational")
        result = {}
        for number, sign in ((value.numerator, 1), (value.denominator, -1)):
            divisor = 2
            while divisor * divisor <= number:
                multiplicity = 0
                while number % divisor == 0:
                    number //= divisor
                    multiplicity += 1
                if multiplicity:
                    result[divisor] = result.get(divisor, F(0)) + sign * multiplicity
                divisor += 1
            if number > 1:
                result[number] = result.get(number, F(0)) + sign
        return cls(result)

    def __add__(self, other):
        if not isinstance(other, LogForm):
            other = LogForm.constant(other)
        result = dict(self.terms)
        for key, value in other.terms.items():
            result[key] = result.get(key, F(0)) + value
        return LogForm(result)

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return LogForm({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, LogForm) else -F(other))

    def __mul__(self, scalar):
        scalar = F(scalar)
        return LogForm({key: scalar * value for key, value in self.terms.items()})

    def __rmul__(self, scalar):
        return self * scalar

    def __truediv__(self, scalar):
        return self * (1 / F(scalar))

    def __eq__(self, other):
        if not isinstance(other, LogForm):
            other = LogForm.constant(other)
        return self.terms == other.terms

    def __repr__(self):
        if not self.terms:
            return "0"
        pieces = []
        for key in sorted(self.terms):
            value = self.terms[key]
            pieces.append(str(value) if key == 0 else f"({value})*log({key})")
        return " + ".join(pieces)


def require(condition, label):
    if not condition:
        raise ArithmeticError("central_pointer: " + label)


def equal(actual, expected, label):
    require(actual == expected, f"{label}: actual={actual!r}, expected={expected!r}")


def probability(values, label):
    require(all(value >= 0 for value in values), label + " nonnegative")
    equal(sum(values), F(1), label + " normalized")


def kl(q, r):
    require(len(q) == len(r), "KL dimensions")
    require(all(value > 0 for value in r), "faithful reference")
    return sum((mass * LogForm.logarithm(mass / prior)
                for mass, prior in zip(q, r) if mass), LogForm())


def kl_source(q, r, dq, dr=None):
    """Full derivative at positive q,r, including normalized-reference source."""
    require(all(mass > 0 for mass in q), "source has positive outcome masses")
    require(all(prior > 0 for prior in r), "source has positive reference masses")
    if dr is None:
        dr = [F(0)] * len(r)
    return (sum((tangent * (LogForm.logarithm(mass / prior) + 1)
                 for mass, prior, tangent in zip(q, r, dq)), LogForm())
            - sum((mass * tangent / prior
                   for mass, prior, tangent in zip(q, r, dr)), F(0)))


def joint(q, flags):
    return [mass * probability for index, mass in enumerate(q)
            for probability in flags[index // 2]]


def pointer_price(q, reference, conditional):
    return kl(q, reference) + sum(
        (mass * conditional[index // 2] for index, mass in enumerate(q)), LogForm())


def pointer_source(q, reference, conditional, dq):
    return kl_source(q, reference, dq) + sum(
        (mass * conditional[index // 2] for index, mass in enumerate(dq)), LogForm())


def block_psd(matrix):
    """Exact real symmetric 2x2 PSD criterion; used only for the two witnesses."""
    return (matrix[0][1] == matrix[1][0] and matrix[0][0] >= 0
            and matrix[1][1] >= 0
            and matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2 >= 0)


def diagonal(blocks):
    return [block[index][index] for block in blocks for index in range(2)]


def run():
    log = LogForm.logarithm
    reference = [F(1, 6), F(1, 6), F(1, 3), F(1, 3)]
    q = [F(1, 10), F(1, 5), F(3, 10), F(2, 5)]
    flags = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
    flag_reference = [[F(1, 5), F(4, 5)], [F(1, 10), F(9, 10)]]
    for values, label in ((reference, "old reference"), (q, "old state")):
        probability(values, label)
    for index in range(2):
        probability(flags[index], f"flag {index}")
        probability(flag_reference[index], f"flag reference {index}")

    conditional = [kl(p, nu) for p, nu in zip(flags, flag_reference)]
    equal(conditional[0], log(F(5, 4)), "exact first flag price")
    equal(conditional[1], log(F(5, 3)), "exact second flag price")
    qout, rout = joint(q, flags), joint(reference, flag_reference)
    probability(qout, "complete output")
    probability(rout, "complete output reference")
    equal(kl(qout, rout), pointer_price(q, reference, conditional),
          "complete flag relative-entropy chain rule")

    # Both tilt weights are the exact exponentials of the computed flag prices.
    tilt = [F(4, 5), F(3, 5)]
    for index in range(2):
        equal(log(tilt[index]), -conditional[index], "tilt is exp(-conditional price)")
    normalizer = sum(mass * tilt[index // 2] for index, mass in enumerate(reference))
    equal(normalizer, F(2, 3), "Gibbs normalizer")
    qstar = [mass * tilt[index // 2] / normalizer
             for index, mass in enumerate(reference)]
    equal(qstar, [F(1, 5), F(1, 5), F(3, 10), F(3, 10)], "tilted pointer masses")
    probability(qstar, "tilted state")
    reduced = -log(normalizer)
    equal(pointer_price(q, reference, conditional), reduced + kl(q, qstar),
          "full Gibbs remainder identity")
    equal(pointer_price(qstar, reference, conditional), reduced,
          "exact reduced minimum value")

    # Every normalized density tangent has a trace-zero pointer tangent.
    # The three basis tangents span the whole four-outcome normalization plane.
    for index in range(3):
        tangent = [F(0)] * 4
        tangent[index], tangent[3] = F(1), F(-1)
        equal(pointer_source(qstar, reference, conditional, tangent), LogForm(),
              "stationarity on every normalized pointer tangent")
    scales = [F(1, 7), F(2, 9), F(-1, 8), F(3, 11)]
    mean_scale = sum(mass * value for mass, value in zip(qstar, scales))
    amplitude_tangent = [2 * mass * (value - mean_scale)
                         for mass, value in zip(qstar, scales)]
    equal(sum(amplitude_tangent), F(0), "actual normalized amplitude tangent")
    equal(pointer_source(qstar, reference, conditional, amplitude_tangent), LogForm(),
          "full preparation source with its normalizer")
    unnormalized_tangent = [2 * mass * value for mass, value in zip(qstar, scales)]
    require(pointer_source(qstar, reference, conditional, unnormalized_tangent) != LogForm(),
            "negative control rejects a frozen preparation normalizer")

    # Two full PSD block states, total ranks four and two, have the same pointer.
    diagonal_state = [[[F(1, 5), F(0)], [F(0), F(1, 5)]],
                      [[F(3, 10), F(0)], [F(0), F(3, 10)]]]
    coherent_state = [[[F(1, 5), F(1, 5)], [F(1, 5), F(1, 5)]],
                      [[F(3, 10), F(3, 10)], [F(3, 10), F(3, 10)]]]
    require(diagonal_state != coherent_state, "distinct states on one pointer fibre")
    for state in (diagonal_state, coherent_state):
        require(all(block_psd(block) for block in state), "fibre witness is PSD")
        equal(diagonal(state), qstar, "same complete pointer on different-rank states")
        equal(pointer_price(diagonal(state), reference, conditional), reduced,
              "same exact price on different-rank states")
    midpoint = [[[((diagonal_state[j][a][b] + coherent_state[j][a][b]) / 2)
                  for b in range(2)] for a in range(2)] for j in range(2)]
    require(all(block_psd(block) for block in midpoint), "convex midpoint is PSD")
    equal(diagonal(midpoint), qstar, "convex midpoint stays on the fibre")
    equal(pointer_source(qstar, reference, conditional, [F(0)] * 4), LogForm(),
          "off-diagonal normalized density tangents are pointer-invisible")

    # Coarsening only the old pointer to its actually supplied type is a separate
    # complete readout.  Its reduced normalizer is unchanged; it is not free cut
    # equivalence for every preparation away from the respective minimizing fibre.
    type_reference = [sum(reference[:2]), sum(reference[2:])]
    type_optimum = [sum(qstar[:2]), sum(qstar[2:])]
    type_normalizer = sum(prior * weight for prior, weight in zip(type_reference, tilt))
    equal(type_normalizer, normalizer, "type-only reduced normalizer")
    equal(kl(type_optimum, type_reference)
          + sum((mass * value for mass, value in zip(type_optimum, conditional)), LogForm()),
          reduced, "type-only exact minimum")

    # Genuine flag probability derivatives, rather than differentiation of a
    # previously computed value remainder.  Old preparation/reference are fixed.
    dflags = [[F(1, 7), F(-1, 7)], [F(1, 3), F(-1, 3)]]
    dconditional = [kl_source(p, nu, dp)
                    for p, nu, dp in zip(flags, flag_reference, dflags)]
    equal(dconditional[0], F(2, 7) * log(2), "first actual conditional source")
    equal(dconditional[1], F(2, 3) * log(3), "second actual conditional source")
    for preparation in (q, qstar):
        actual = kl_source(joint(preparation, flags), rout, joint(preparation, dflags))
        expected = sum((mass * dconditional[index // 2]
                        for index, mass in enumerate(preparation)), LogForm())
        equal(actual, expected, "central geometric source factorization")
    envelope_source = sum((mass * dconditional[index // 2]
                           for index, mass in enumerate(qstar)), LogForm())
    dnormalizer = -sum((mass * tilt[index // 2] * dconditional[index // 2]
                       for index, mass in enumerate(reference)), LogForm())
    equal(-dnormalizer / normalizer, envelope_source,
          "actual reduced source differentiates the same normalizer")

    # A normalized moving central reference has a real, nonzero extra source.
    dreference = [F(1, 60), F(1, 60), F(-1, 60), F(-1, 60)]
    equal(sum(dreference), F(0), "moving central reference stays normalized")
    reference_source = kl_source(qstar, reference, [F(0)] * 4, dreference)
    equal(reference_source, LogForm.constant(F(-1, 100)),
          "moving reference contributes its actual source")
    reference_dnormalizer = sum(mass * tilt[index // 2]
                               for index, mass in enumerate(dreference))
    equal(-reference_dnormalizer / normalizer, F(-1, 100),
          "reference source agrees with full envelope derivative")
    require(reference_source != LogForm(),
            "negative control rejects omission of the moving-reference source")

    # Forgetting the new flag leaves a different observable with a different
    # conditional price and, in general, a different preparation source.
    omitted_flag_price = kl(qout, rout) - kl(q, reference)
    equal(omitted_flag_price, F(3, 10) * log(F(5, 4)) + F(7, 10) * log(F(5, 3)),
          "omitted full flag has a nonzero exact conditional price")
    require(omitted_flag_price != LogForm(), "negative control rejects dropping the flag")
    transfer = [F(1, 10), F(0), F(-1, 10), F(0)]
    equal(pointer_source(qstar, reference, conditional, transfer), LogForm(),
          "complete price has zero preparation source at the tilted optimum")
    equal(kl_source(qstar, reference, transfer), F(1, 10) * log(F(4, 3)),
          "old-only price has a different preparation source")

    # One proper boundary support illustrates the exact restricted tilt.  This
    # checks finite support algebra, not differentiability of density entropy at
    # missing outcomes; the amplitude t^2 log(t^2) argument is in the memo.
    support = [0, 2, 3]
    support_z = sum(reference[index] * tilt[index // 2] for index in support)
    support_q = [reference[index] * tilt[index // 2] / support_z if index in support else F(0)
                 for index in range(4)]
    probability(support_q, "proper-support tilt")
    equal(pointer_price(support_q, reference, conditional), -log(support_z),
          "proper-support stationary value")
    equal(pointer_price(support_q, reference, conditional) - reduced, log(normalizer / support_z),
          "proper-support value gap")
    require(support_z < normalizer, "proper support is not the global minimizing distribution")

    return "\n".join([
        "Central complete-pointer algebra: exact rational/log-prime verification.",
        "Complete outputs: KL(old,flag)=KL(old)+sum(type_mass * KL(flag|type)).",
        "One common fixture has conditional prices log(5/4), log(5/3), Z=2/3,",
        "and q*=(1/5,1/5,3/10,3/10); price=-log(Z)+KL(q||q*) exactly.",
        "Every normalized pointer tangent has zero preparation source at q*;",
        "the actual amplitude normalizer is retained.  Freezing it fails.",
        "Distinct PSD states of ranks four and two, and their convex midpoint,",
        "share the exact pointer minimum.  No unique state/Hessian inverse is used.",
        "Type-only and full-pointer reduced minima agree in their declared cuts.",
        "Direct flag probability jets give the central source and the exact",
        "derivative of the same Gibbs normalizer; no derivative of a remainder is used.",
        "Moving central reference adds -1/100 in the exact normalized fixture;",
        "omitting that source is rejected.  Forgetting the flag also changes the price",
        "and changes one preparation source by (1/10)*log(4/3).",
        "A proper-support tilt has the exact gap log(Z/Z_support)>0; amplitude",
        "rank-birth/stationarity and all-size convexity are analytic memo statements.",
        "Scope: bounded algebra fixtures only, not actual golden-program values,",
        "native reachability, physical Cost-minus-Info selection or an Einstein closure.",
        "No old suites, golden sign bounds, original sources, flags or grades were changed.",
    ])


if __name__ == "__main__":
    print(run())
