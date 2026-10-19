#!/usr/bin/env python3
"""Exact C2 audit of a four-fresh-flag Julia commutator price.

The checker uses the original grade-one Lorentz carrier with the Choi probe
from the pinned full-CAR16 owner.  The other CAR grades are spectators for
this probe; the instrument still retains all four Julia flags and every POVM
outcome.  It tests one specific complete mean-Shannon candidate, not physical
admission or a no-go theorem for other D0 prices.
"""

from collections import defaultdict
from itertools import product

import sympy as sp

I4 = sp.eye(4)
ZERO4 = sp.zeros(4)
SQRT2 = sp.sqrt(2)
SQRT3 = sp.sqrt(3)
P = (sp.sqrt(5) - 1) / 2
GOLDEN_GAIN = 2 - P  # h_2(p)/log(phi), using p+p^2=1
C_SH = GOLDEN_GAIN / (48 * SQRT2)
LOG_PHI = -sp.log(P)


def e(i, j):
    out = sp.zeros(4)
    out[i, j] = 1
    return out


N2 = e(1, 2) + e(2, 0)
N3 = e(1, 3) + e(3, 0)
BAR_N2 = e(0, 2) + e(2, 1)
BAR_N3 = e(0, 3) + e(3, 1)
J = e(2, 3) - e(3, 2)
B = e(1, 1) - e(0, 0)
GENERATORS = (N2, N3, BAR_N2, BAR_N3, J, B)
GENERATOR_NAMES = ("N2", "N3", "barN2", "barN3", "J", "B")


def require(ok, label):
    if not ok:
        raise AssertionError(label)


def zero_jet():
    return (ZERO4, ZERO4, ZERO4, ZERO4)


def jet_product(left, right):
    """Coefficients (00, 10, 01, 11) for a matrix product."""
    l0, la, lb, lab = left
    r0, ra, rb, rab = right
    return (
        l0 * r0,
        la * r0 + l0 * ra,
        lb * r0 + l0 * rb,
        lab * r0 + la * rb + lb * ra + l0 * rab,
    )


def factor_jet(generator, variable=None, sign=1, failure=False):
    """First jet of a success/failure Kraus branch of one fresh Julia gate."""
    base = (SQRT3 / 2 if failure else sp.Rational(1, 2)) * I4
    if generator is None or variable is None:
        return (base, ZERO4, ZERO4, ZERO4)
    signed = sign * generator
    if failure:
        # D(x)=sqrt(I - T(x)^T T(x)), T(x)=exp(xG)/2.
        derivative = -(signed.T + signed) / (4 * SQRT3)
    else:
        derivative = signed / 2
    if variable == "a":
        return (base, derivative, ZERO4, ZERO4)
    if variable == "b":
        return (base, ZERO4, derivative, ZERO4)
    raise ValueError(variable)


def choi_probe():
    omega = sp.zeros(16, 1)
    for i in range(4):
        omega[4 * i + i] = sp.Rational(1, 2)
    signatures = [SQRT2 * sp.kronecker_product(g, I4) * omega
                  for g in GENERATORS]
    gram = sp.Matrix([[sp.simplify(x.dot(y)) for y in signatures]
                      for x in signatures])
    require(gram == sp.eye(6), "original six Lorentz signatures orthonormal")
    require(all(sp.simplify(x.dot(omega)) == 0 for x in signatures),
            "all signatures orthogonal to Choi seed")
    return omega, signatures


OMEGA, SIGNATURES = choi_probe()
POVM_VECTORS = tuple(
    (OMEGA + eps * SIGNATURES[k]) / SQRT2
    for k in range(6) for eps in (1, -1)
)
J_MINUS_INDEX = 2 * 4 + 1


def probability_jet(amplitude):
    x0, xa, xb, xab = amplitude
    return (
        sp.simplify(x0**2 / 12),
        sp.simplify(2 * x0 * xa / 12),
        sp.simplify(2 * x0 * xb / 12),
        sp.simplify(2 * (x0 * xab + xa * xb) / 12),
    )


def dot_jet(left, right):
    x0, xa, xb, xab = left
    y0, ya, yb, yab = right
    return (
        sp.simplify(x0.dot(y0)),
        sp.simplify(xa.dot(y0) + x0.dot(ya)),
        sp.simplify(xb.dot(y0) + x0.dot(yb)),
        sp.simplify(xab.dot(y0) + xa.dot(yb) + xb.dot(ya) + x0.dot(yab)),
    )


def instrument_probability_jets(gates):
    """Return all 16*13 coarse pointer jets for four chronological gates.

    Each gate is (generator, variable, sign).  A None generator denotes a
    flat identity operation with its own complete Julia flag.  Multiplication
    is chronological left action, so the returned Lorentz product is the
    reverse of the tuple order.
    """
    require(len(gates) == 4, "four separate fresh Julia flags")
    output = []
    for failures in product((False, True), repeat=4):
        factors = [factor_jet(g, v, s, fail)
                   for (g, v, s), fail in zip(gates, failures)]
        total = (I4, ZERO4, ZERO4, ZERO4)
        for factor in factors:
            total = jet_product(factor, total)
        states = tuple(sp.kronecker_product(k, I4) * OMEGA for k in total)
        probs = []
        for vec in POVM_VECTORS:
            amps = tuple(sp.simplify(vec.dot(state)) for state in states)
            probs.append(probability_jet(amps))
        norm = dot_jet(states, states)
        rest = tuple(sp.simplify(norm[i] - sum(q[i] for q in probs))
                     for i in range(4))
        branch = probs + [rest]
        require(all(sp.simplify(q[0]) > 0 for q in branch),
                "strictly positive branch/outcome baseline")
        output.append((failures, branch))
    require(len(output) == 16 and sum(len(branch) for _, branch in output) == 208,
            "all 16 retained flags times all 13 coarse outcomes")
    total_jet = tuple(sp.simplify(sum(q[i] for _, branch in output
                                      for q in branch)) for i in range(4))
    require(total_jet == (sp.S.One, sp.S.Zero, sp.S.Zero, sp.S.Zero),
            "whole complete record normalized through mixed order")
    return output


def split_j_minus(probabilities):
    """Refine the J- pointer in every history; retain both Golden labels."""
    split = []
    coarse_jminus = [sp.S.Zero] * 4
    for _, branch in probabilities:
        q = branch[J_MINUS_INDEX]
        coarse_jminus = [coarse_jminus[i] + q[i] for i in range(4)]
        split.extend(branch[:J_MINUS_INDEX])
        split.extend((tuple(P * x for x in q),
                      tuple(P**2 * x for x in q)))
        split.extend(branch[J_MINUS_INDEX + 1:])
    require(len(split) == 224, "one retained Golden split per flag history")
    require(all(q[0] > 0 for q in split), "strictly positive fine outcomes")
    return split, tuple(sp.simplify(x) for x in coarse_jminus)


def entropy_mixed_jet(probabilities):
    """Exact entropy ab jet, grouping equal rational baseline probabilities."""
    grouped_logs = defaultdict(lambda: sp.S.Zero)
    rational_part = sp.S.Zero
    for q0, qa, qb, qab in probabilities:
        rational_part += qab + qa * qb / q0
        grouped_logs[q0] += qab
    log_part = sum(coef * sp.log(base)
                   for base, coef in grouped_logs.items())
    raw = sp.expand(rational_part + log_part)
    # All baselines are positive rationals. Expand their prime factors before
    # simplifying the exact logarithmic cancellation.
    raw = sp.expand_log(raw, force=True)
    return sp.simplify(-raw / LOG_PHI)


def face_geometry_check():
    commutator = N2 * BAR_N3 - BAR_N3 * N2
    require(commutator == J, "[N2,barN3]=J exactly")

    # Differentiate the actual four factors in the original based-face
    # convention; the opposite product is its inverse at the required jet.
    def link_jet(g, variable, sign):
        out = [I4, ZERO4, ZERO4, ZERO4]
        out[1 if variable == "a" else 2] = sign * g
        return tuple(out)

    product_jet = (I4, ZERO4, ZERO4, ZERO4)
    for factor in (link_jet(N2, "a", 1), link_jet(BAR_N3, "b", 1),
                   link_jet(N2, "a", -1), link_jet(BAR_N3, "b", -1)):
        product_jet = jet_product(product_jet, factor)
    inverse_jet = (I4, ZERO4, ZERO4, ZERO4)
    for factor in (link_jet(BAR_N3, "b", 1), link_jet(N2, "a", 1),
                   link_jet(BAR_N3, "b", -1), link_jet(N2, "a", -1)):
        inverse_jet = jet_product(inverse_jet, factor)
    mixed_product = product_jet[3]
    require(mixed_product == commutator == J,
            "actual crossed-null plaquette mixed derivative")
    mixed_inverse = inverse_jet[3]
    require(mixed_inverse == -J, "inverse plaquette mixed derivative")
    mixed_curvature = (mixed_product - mixed_inverse) / 2
    require(mixed_curvature == J, "original R(P) mixed curvature derivative")

    h = sp.symbols("h", positive=True)
    coframe = h * I4
    eta = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                     [0, 0, -1, 0], [0, 0, 0, -1]])
    epsilon = sp.LeviCivita
    # This is the original accepted G_2(e_u wedge e_v, star b(R)) convention:
    # the bivector pair a<b is summed once and the complementary c<d once.
    face = (2, 3)
    u, v = (i for i in range(4) if i not in face)
    curvature_dual = mixed_curvature * eta
    palatini_pair = sp.S.Zero
    for a in range(4):
        for b in range(a + 1, 4):
            c, d = (i for i in range(4) if i not in (a, b))
            bivector = coframe[a, u] * coframe[b, v] - coframe[b, u] * coframe[a, v]
            palatini_pair += epsilon(a, b, c, d) * bivector * curvature_dual[c, d]
    face_mixed = sp.expand(epsilon(*face, u, v) * palatini_pair)
    require(sp.simplify(face_mixed + h**2) == 0,
            "original (2,3) star-face mixed coefficient")
    return h, face_mixed


def run():
    h, face_mixed = face_geometry_check()

    # Four gates in chronological order B^-1,A^-1,B,A yield the actual
    # matrix product A B A^-1 B^-1.  Each has its own retained Julia flag.
    loop_gates = ((BAR_N3, "b", -1), (N2, "a", -1),
                  (BAR_N3, "b", 1), (N2, "a", 1))
    loop = instrument_probability_jets(loop_gates)
    fine, q_jminus = split_j_minus(loop)

    one_edge = instrument_probability_jets(
        ((None, None, 1), (J, "a", 1), (None, None, 1), (None, None, 1))
    )
    _, one_q_jminus = split_j_minus(one_edge)
    require(one_q_jminus[1] == -1 / (48 * SQRT2),
            "four-gate one-link J- pointer first derivative")
    one_source = sp.simplify(GOLDEN_GAIN * one_q_jminus[1])
    require(sp.simplify(one_source + C_SH) == 0,
            "one-link complete Golden mean-Shannon source")

    loop_q_source = q_jminus[3]
    require(sp.simplify(loop_q_source + 1 / (384 * SQRT2)) == 0,
            "crossed-loop retained J- pointer mixed derivative")
    raw_mixed = entropy_mixed_jet([q for _, branch in loop for q in branch])
    require(raw_mixed == 0,
            "unmarked all-outcome complete Shannon mixed source is zero")
    fine_mixed = sp.simplify(raw_mixed + GOLDEN_GAIN * loop_q_source)
    require(sp.simplify(fine_mixed + C_SH / 8) == 0,
            "complete Golden-refined price has exact factor-eight C2 mismatch")
    direct_fine_mixed = entropy_mixed_jet(fine)
    require(sp.simplify(direct_fine_mixed - fine_mixed) == 0,
            "direct 224-outcome Golden-refined entropy jet")

    # Per-face scale is already fixed by the first jet; it cannot repair C2.
    kappa = h**2 / C_SH
    matched_first = sp.simplify(kappa * (-C_SH) - face_mixed)
    require(matched_first == 0, "flat first-jet normalization matches")
    mismatch = sp.simplify(kappa * fine_mixed - face_mixed / 8)
    require(mismatch == 0, "scaled mixed source is exactly one eighth")

    print("PASS [N2,barN3]=J and original crossed-null plaquette coefficient=-h^2")
    print("PASS 16 fresh-flag histories x 13 complete POVM outcomes = 208 coarse outcomes")
    print("PASS one retained J- Golden split in every history = 224 fine outcomes")
    print("PASS all baseline probabilities are strictly positive; full probability jets normalize")
    print(f"PASS one-link source = -c_Sh = {sp.sstr(-C_SH)}")
    print(f"PASS unmarked Shannon mixed source = {sp.sstr(raw_mixed)}")
    print(f"PASS crossed-loop J- probability mixed derivative = {sp.sstr(loop_q_source)}")
    print(f"PASS Golden-refined Shannon mixed source = -c_Sh/8 = {sp.sstr(-C_SH/8)}")
    print("PASS first-jet-fixed scale leaves exact 1/8 crossed-null face source")
    print("SCOPE: rejects this complete mean-Shannon candidate at C2 only; no native-D0 no-go")


if __name__ == "__main__":
    run()
