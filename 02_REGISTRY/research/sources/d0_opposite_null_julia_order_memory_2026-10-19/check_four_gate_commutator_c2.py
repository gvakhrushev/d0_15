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
B_MINUS_INDEX = 2 * 5 + 1


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


def split_pointer(probabilities, pointer_index):
    """Refine one pointer in every history; retain both Golden labels."""
    split = []
    coarse_pointer_jets = [sp.S.Zero] * 4
    for _, branch in probabilities:
        q = branch[pointer_index]
        coarse_pointer_jets = [coarse_pointer_jets[i] + q[i] for i in range(4)]
        split.extend(branch[:pointer_index])
        split.extend((tuple(P * x for x in q),
                      tuple(P**2 * x for x in q)))
        split.extend(branch[pointer_index + 1:])
    require(len(split) == 224, "one retained Golden split per flag history")
    require(all(q[0] > 0 for q in split), "strictly positive fine outcomes")
    total = tuple(sp.simplify(sum(q[i] for q in split)) for i in range(4))
    require(total == (sp.S.One, sp.S.Zero, sp.S.Zero, sp.S.Zero),
            "all-history refinement preserves complete probability jets")
    return split, tuple(sp.simplify(x) for x in coarse_pointer_jets)


def split_pointer_on_history(probabilities, pointer_index,
                              target=(False, False, False, False)):
    """Refine one pointer in one flag history; leave every sibling intact."""
    split = []
    selected = None
    for history, branch in probabilities:
        if history == target:
            q = branch[pointer_index]
            selected = tuple(sp.simplify(x) for x in q)
            split.extend(branch[:pointer_index])
            split.extend((tuple(P * x for x in q),
                          tuple(P**2 * x for x in q)))
            split.extend(branch[pointer_index + 1:])
        else:
            split.extend(branch)
    require(selected is not None, "target flag history exists")
    require(len(split) == len(probabilities) * 13 + 1,
            "one branch-local Golden refinement")
    require(all(q[0] > 0 for q in split), "positive branch-local fine outcomes")
    total = tuple(sp.simplify(sum(q[i] for q in split)) for i in range(4))
    require(total == (sp.S.One, sp.S.Zero, sp.S.Zero, sp.S.Zero),
            "branch-local refinement preserves complete probability jets")
    return split, selected


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


def entropy_first_jet(probabilities, axis):
    """Exact first Shannon jet; axis=1 selects a, axis=2 selects b."""
    grouped_logs = defaultdict(lambda: sp.S.Zero)
    total_derivative = sp.S.Zero
    for q0, qa, qb, _ in probabilities:
        derivative = qa if axis == 1 else qb
        total_derivative += derivative
        grouped_logs[q0] += derivative
    raw = total_derivative + sum(coef * sp.log(base)
                                 for base, coef in grouped_logs.items())
    raw = sp.expand_log(sp.expand(raw), force=True)
    return sp.simplify(-raw / LOG_PHI)


def add_matrix_jets(left, right, right_sign=1):
    return tuple(left[i] + right_sign * right[i] for i in range(4))


def transpose_matrix_jet(jet):
    return tuple(matrix.T for matrix in jet)


def group_factor_jet(generator, variable, sign=1):
    jet = [I4, ZERO4, ZERO4, ZERO4]
    jet[1 if variable == "a" else 2] = sign * generator
    return tuple(jet)


def direct_julia_instrument(group_word_jet):
    """First/mixed jet of the direct Julia instrument T=U/2, D=sqrt(I-T^T T)."""
    success = tuple(matrix / 2 for matrix in group_word_jet)
    t_transpose_t = jet_product(transpose_matrix_jet(success), success)
    slack = add_matrix_jets((I4, ZERO4, ZERO4, ZERO4), t_transpose_t, -1)
    require(slack[0] == sp.Rational(3, 4) * I4,
            "direct Julia slack has positive 3/4 identity base")

    # Solve D^2=slack order by order around D_0=(sqrt(3)/2)I.
    failure = (
        SQRT3 * I4 / 2,
        slack[1] / SQRT3,
        slack[2] / SQRT3,
        slack[3] / SQRT3
        - (slack[1] * slack[2] + slack[2] * slack[1]) / (3 * SQRT3),
    )
    return success, failure


def assert_complete_kraus_jets(branches, label):
    total = zero_jet()
    for _, kraus_jet in branches:
        total = add_matrix_jets(
            total, jet_product(transpose_matrix_jet(kraus_jet), kraus_jet)
        )
    require(total == (I4, ZERO4, ZERO4, ZERO4),
            f"{label} is complete through mixed order")


def record_probability_jets(branches, label):
    """Evaluate all 13 positive tester outcomes on supplied Kraus histories."""
    output = []
    for history, kraus_jet in branches:
        states = tuple(sp.kronecker_product(k, I4) * OMEGA for k in kraus_jet)
        probs = []
        for vec in POVM_VECTORS:
            amps = tuple(sp.simplify(vec.dot(state)) for state in states)
            probs.append(probability_jet(amps))
        norm = dot_jet(states, states)
        rest = tuple(sp.simplify(norm[i] - sum(q[i] for q in probs))
                     for i in range(4))
        branch = probs + [rest]
        require(all(sp.simplify(q[0]) > 0 for q in branch),
                f"{label} has positive complete tester baselines")
        output.append((history, branch))
    total = tuple(sp.simplify(sum(q[i] for _, branch in output for q in branch))
                  for i in range(4))
    require(total == (sp.S.One, sp.S.Zero, sp.S.Zero, sp.S.Zero),
            f"{label} complete tester normalizes through mixed order")
    return output


def branch_outcomes(records, history):
    return next(branch for candidate, branch in records if candidate == history)


def branch_mass(records, history):
    branch = branch_outcomes(records, history)
    return tuple(sp.simplify(sum(q[i] for q in branch)) for i in range(4))


def composition_defect_check():
    """Compare one dilation of a product with two sequential fresh dilations."""
    summary = []
    for pair, g1, g2 in (("J", N2, BAR_N3), ("B", N2, BAR_N2)):
        for order in ("AB", "BA"):
            if order == "AB":
                first, second = (g1, "a"), (g2, "b")
            else:
                first, second = (g2, "b"), (g1, "a")
            group_word = jet_product(
                group_factor_jet(second[0], second[1]),
                group_factor_jet(first[0], first[1]),
            )
            direct_success, direct_failure = direct_julia_instrument(group_word)
            direct_branches = (("success", direct_success),
                               ("failure", direct_failure))
            assert_complete_kraus_jets(direct_branches, f"direct {pair} {order}")
            direct_records = record_probability_jets(
                direct_branches, f"direct {pair} {order}"
            )

            sequential_branches = []
            for failures in product((False, True), repeat=2):
                first_kraus = factor_jet(first[0], first[1], 1, failures[0])
                second_kraus = factor_jet(second[0], second[1], 1, failures[1])
                sequential_branches.append(
                    (failures, jet_product(second_kraus, first_kraus))
                )
            assert_complete_kraus_jets(
                sequential_branches, f"sequential {pair} {order}"
            )
            sequential_records = record_probability_jets(
                sequential_branches, f"sequential {pair} {order}"
            )

            direct_all_success = branch_mass(direct_records, "success")
            sequential_all_success = branch_mass(
                sequential_records, (False, False)
            )
            require(direct_all_success == tuple(4 * q for q in sequential_all_success),
                    f"{pair} {order} all-success record has exact factor-four composition defect")
            direct_events = branch_outcomes(direct_records, "success")
            sequential_events = branch_outcomes(sequential_records, (False, False))
            require(len(direct_events) == len(sequential_events) == 13,
                    f"{pair} {order} compares all 13 common tester effects")
            require(all(tuple(sp.simplify(qd[i] - 4 * qs[i]) for i in range(4))
                        == (sp.S.Zero,) * 4
                        for qd, qs in zip(direct_events, sequential_events)),
                    f"{pair} {order} every positive effect resolves the composition defect")
            direct_defect = tuple(
                sp.simplify(direct_all_success[i] - sequential_all_success[i])
                for i in range(4)
            )
            expected = ((sp.Rational(3, 16), 0, 0, 0) if pair == "J"
                        else (sp.Rational(3, 16), 0, 0, sp.Rational(3, 16)))
            require(direct_defect == expected,
                    f"{pair} {order} measurable all-success composition defect jet")

            sequential_success = next(k for history, k in sequential_branches
                                      if history == (False, False))
            operator_defect = tuple(
                sp.simplify(direct_success[i] - sequential_success[i])
                for i in range(4)
            )
            require(operator_defect == tuple(matrix / 4 for matrix in group_word),
                    f"{pair} {order} success-operator defect is the composed word divided by four")
            summary.append((pair, order, direct_defect))
    return summary


def four_gate_composition_defect_check():
    """Tie the C2 face source scale to one vs four sequential Julia successes."""
    summary = []
    cases = (("J", BAR_N3, J_MINUS_INDEX),
             ("B", BAR_N2, B_MINUS_INDEX))
    for label, opposite_null, pointer_index in cases:
        gates = ((opposite_null, "b", -1), (N2, "a", -1),
                 (opposite_null, "b", 1), (N2, "a", 1))
        group_word = (I4, ZERO4, ZERO4, ZERO4)
        for generator, variable, sign in gates:
            group_word = jet_product(
                group_factor_jet(generator, variable, sign), group_word
            )

        direct_success, direct_failure = direct_julia_instrument(group_word)
        direct_branches = (("success", direct_success),
                           ("failure", direct_failure))
        assert_complete_kraus_jets(direct_branches, f"direct four-edge {label}")
        direct_records = record_probability_jets(
            direct_branches, f"direct four-edge {label}"
        )
        sequential_branches = []
        for failures in product((False, True), repeat=4):
            word = (I4, ZERO4, ZERO4, ZERO4)
            for (generator, variable, sign), failed in zip(gates, failures):
                word = jet_product(
                    factor_jet(generator, variable, sign, failed), word
                )
            sequential_branches.append((failures, word))
        assert_complete_kraus_jets(
            sequential_branches, f"sequential four-edge {label}"
        )
        sequential_records = record_probability_jets(
            sequential_branches, f"sequential four-edge {label}"
        )
        direct_mass = branch_mass(direct_records, "success")
        sequential_mass = branch_mass(
            sequential_records, (False, False, False, False)
        )
        require(direct_mass == tuple(64 * q for q in sequential_mass),
                f"four-edge {label} direct/sequential all-success mass ratio is 64")
        defect = tuple(sp.simplify(direct_mass[i] - sequential_mass[i])
                       for i in range(4))
        require(defect == (sp.Rational(63, 256), 0, 0, 0),
                f"four-edge {label} measurable composition defect")

        direct_events = branch_outcomes(direct_records, "success")
        sequential_events = branch_outcomes(
            sequential_records, (False, False, False, False)
        )
        require(all(tuple(sp.simplify(qd[i] - 64 * qs[i]) for i in range(4))
                    == (sp.S.Zero,) * 4
                    for qd, qs in zip(direct_events, sequential_events)),
                f"all 13 four-edge {label} effects resolve the factor-64 defect")
        direct_pointer = direct_events[pointer_index]
        sequential_pointer = sequential_events[pointer_index]
        require(direct_pointer[3] == -SQRT2 / 96
                and sequential_pointer[3] == -SQRT2 / 6144,
                f"four-edge {label} pointer mixed jets exhibit the factor 64")

        direct_fine, _ = split_pointer_on_history(
            direct_records, pointer_index, "success"
        )
        sequential_fine, _ = split_pointer_on_history(
            sequential_records, pointer_index
        )
        direct_raw = entropy_mixed_jet(
            [q for _, branch in direct_records for q in branch]
        )
        sequential_raw = entropy_mixed_jet(
            [q for _, branch in sequential_records for q in branch]
        )
        require(direct_raw == sequential_raw == 0,
                f"unmarked four-edge {label} complete mixed sources vanish")
        direct_increment = sp.simplify(
            entropy_mixed_jet(direct_fine) - direct_raw
        )
        sequential_increment = sp.simplify(
            entropy_mixed_jet(sequential_fine) - sequential_raw
        )
        require(sp.simplify(direct_increment + C_SH) == 0
                and sp.simplify(sequential_increment + C_SH / 64) == 0,
                f"four-edge {label} Golden source increments differ exactly by 64")
        require(sp.simplify(direct_increment - 64 * sequential_increment) == 0,
                f"four-edge {label} Golden source scale is exactly the composition factor")
        summary.append((label, defect, -C_SH, -C_SH / 64))
    return summary


def face_geometry_check():
    def commutator_curvature(g1, g2):
        require(g1 * g2 - g2 * g1 != ZERO4, "noncommuting gate pair")

        # Differentiate the actual four factors in the based-face convention;
        # the opposite product is its inverse at the required jet.
        def link_jet(g, variable, sign):
            out = [I4, ZERO4, ZERO4, ZERO4]
            out[1 if variable == "a" else 2] = sign * g
            return tuple(out)

        product_jet = (I4, ZERO4, ZERO4, ZERO4)
        for factor in (link_jet(g1, "a", 1), link_jet(g2, "b", 1),
                       link_jet(g1, "a", -1), link_jet(g2, "b", -1)):
            product_jet = jet_product(product_jet, factor)
        inverse_jet = (I4, ZERO4, ZERO4, ZERO4)
        for factor in (link_jet(g2, "b", 1), link_jet(g1, "a", 1),
                       link_jet(g2, "b", -1), link_jet(g1, "a", -1)):
            inverse_jet = jet_product(inverse_jet, factor)
        commutator = g1 * g2 - g2 * g1
        require(product_jet[3] == commutator,
                "actual based plaquette mixed derivative")
        require(inverse_jet[3] == -commutator,
                "inverse plaquette mixed derivative")
        curvature = (product_jet[3] - inverse_jet[3]) / 2
        require(curvature == commutator,
                "original R(P) mixed curvature derivative")
        return curvature

    curvature_j = commutator_curvature(N2, BAR_N3)
    curvature_b = commutator_curvature(N2, BAR_N2)
    require(curvature_j == J, "[N2,barN3]=J exactly")
    require(curvature_b == B, "[N2,barN2]=B exactly")

    h = sp.symbols("h", positive=True)
    coframe = h * I4
    eta = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                     [0, 0, -1, 0], [0, 0, 0, -1]])
    epsilon = sp.LeviCivita

    def palatini_face_mixed(face, curvature):
        u, v = (i for i in range(4) if i not in face)
        curvature_dual = curvature * eta
        palatini_pair = sp.S.Zero
        # Original accepted G_2 convention: sum a<b and complementary c<d once.
        for a in range(4):
            for b in range(a + 1, 4):
                c, d = (i for i in range(4) if i not in (a, b))
                bivector = (coframe[a, u] * coframe[b, v]
                            - coframe[b, u] * coframe[a, v])
                palatini_pair += epsilon(a, b, c, d) * bivector * curvature_dual[c, d]
        return sp.expand(epsilon(*face, u, v) * palatini_pair)

    face_j = palatini_face_mixed((2, 3), curvature_j)
    face_b = palatini_face_mixed((0, 1), curvature_b)
    require(sp.simplify(face_j + h**2) == 0,
            "original (2,3) star-face J mixed coefficient")
    require(sp.simplify(face_b + h**2) == 0,
            "original (0,1) star-face B mixed coefficient")
    return h, face_j, face_b


def branch_resolved_readout(g1, g2, pointer_index, h, face_mixed, label):
    """Check one complete all-success record against a Lorentz face's two jets."""
    curvature = g1 * g2 - g2 * g1
    loop_gates = ((g2, "b", -1), (g1, "a", -1),
                  (g2, "b", 1), (g1, "a", 1))
    allgood_word = (I4, ZERO4, ZERO4, ZERO4)
    for generator, variable, sign in loop_gates:
        allgood_word = jet_product(
            factor_jet(generator, variable, sign, failure=False), allgood_word
        )
    require(allgood_word[0] == I4 / 16 and allgood_word[3] == curvature / 16,
            f"all-success {label} word is 1/16 times its plaquette jet")

    loop = instrument_probability_jets(loop_gates)
    unmarked_mixed = entropy_mixed_jet(
        [q for _, branch in loop for q in branch]
    )
    require(unmarked_mixed == 0, f"unmarked {label} complete Shannon mixed source vanishes")
    allgood_fine, allgood_q = split_pointer_on_history(loop, pointer_index)
    require(allgood_q[3] == -SQRT2 / 6144,
            f"all-success {label}-minus crossed-loop probability mixed derivative")
    mixed_source = entropy_mixed_jet(allgood_fine)
    require(sp.simplify(mixed_source + C_SH / 64) == 0,
            f"all-success {label} Shannon mixed source")

    one_edge = instrument_probability_jets(
        ((None, None, 1), (curvature, "a", 1),
         (None, None, 1), (None, None, 1))
    )
    one_unmarked = entropy_first_jet(
        [q for _, branch in one_edge for q in branch], axis=1
    )
    require(one_unmarked == 0, f"unmarked {label} one-link source vanishes")
    one_fine, one_q = split_pointer_on_history(one_edge, pointer_index)
    require(one_q[1] == -SQRT2 / 6144,
            f"all-success {label}-minus one-link probability first derivative")
    first_source = entropy_first_jet(one_fine, axis=1)
    require(sp.simplify(first_source + C_SH / 64) == 0,
            f"all-success {label} Shannon first source")
    require(sp.simplify(first_source - mixed_source) == 0,
            f"all-success {label} first and mixed sources agree")

    kappa = 64 * h**2 / C_SH
    require(sp.simplify(kappa * first_source - face_mixed) == 0,
            f"branch-local {label} scale matches original face first jet")
    require(sp.simplify(kappa * mixed_source - face_mixed) == 0,
            f"same branch-local {label} scale matches original face C2 jet")
    return first_source, mixed_source


def run():
    h, face_j, face_b = face_geometry_check()

    # Four gates in chronological order B^-1,A^-1,B,A yield the actual
    # matrix product A B A^-1 B^-1.  Each has its own retained Julia flag.
    loop_gates = ((BAR_N3, "b", -1), (N2, "a", -1),
                  (BAR_N3, "b", 1), (N2, "a", 1))
    loop = instrument_probability_jets(loop_gates)
    fine, q_jminus = split_pointer(loop, J_MINUS_INDEX)

    one_edge = instrument_probability_jets(
        ((None, None, 1), (J, "a", 1), (None, None, 1), (None, None, 1))
    )
    one_unmarked_first = entropy_first_jet(
        [q for _, branch in one_edge for q in branch], axis=1
    )
    require(one_unmarked_first == 0,
            "unmarked complete one-link Shannon first source vanishes")
    allhistory_one_fine, allhistory_one_q = split_pointer(one_edge, J_MINUS_INDEX)
    allhistory_one_source = sp.simplify(GOLDEN_GAIN * allhistory_one_q[1])
    require(allhistory_one_q[1] == -SQRT2 / 96,
            "all-history one-link J- probability derivative")
    require(sp.simplify(allhistory_one_source + C_SH) == 0,
            "all-history one-link Golden mean-Shannon source")
    one_allgood_fine, one_allgood_q = split_pointer_on_history(one_edge, J_MINUS_INDEX)
    one_allgood_source = entropy_first_jet(one_allgood_fine, axis=1)
    require(one_allgood_q[1] == -SQRT2 / 6144,
            "all-success J- one-link probability derivative")
    require(sp.simplify(one_allgood_source + C_SH / 64) == 0,
            "all-success complete Golden mean-Shannon first source")

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
    matched_first = sp.simplify(kappa * (-C_SH) - face_j)
    require(matched_first == 0, "flat first-jet normalization matches")
    mismatch = sp.simplify(kappa * fine_mixed - face_j / 8)
    require(mismatch == 0, "scaled mixed source is exactly one eighth")

    j_first, j_mixed = branch_resolved_readout(
        N2, BAR_N3, J_MINUS_INDEX, h, face_j, "J"
    )
    b_first, b_mixed = branch_resolved_readout(
        N2, BAR_N2, B_MINUS_INDEX, h, face_b, "B"
    )
    composition = composition_defect_check()
    four_edge_composition = four_gate_composition_defect_check()

    print("PASS [N2,barN3]=J and original crossed-null plaquette coefficient=-h^2")
    print("PASS 16 fresh-flag histories x 13 complete POVM outcomes = 208 coarse outcomes")
    print("PASS one retained J- Golden split in every history = 224 fine outcomes")
    print("PASS all baseline probabilities are strictly positive; full probability jets normalize")
    print(f"PASS one-link source = -c_Sh = {sp.sstr(-C_SH)}")
    print(f"PASS unmarked Shannon mixed source = {sp.sstr(raw_mixed)}")
    print(f"PASS crossed-loop J- probability mixed derivative = {sp.sstr(loop_q_source)}")
    print(f"PASS Golden-refined Shannon mixed source = -c_Sh/8 = {sp.sstr(-C_SH/8)}")
    print("PASS first-jet-fixed scale leaves exact 1/8 crossed-null face source")
    print("PASS one all-success J- or B- Golden refinement gives 209 positive outcomes")
    print(f"PASS both branch-resolved first/mixed sources agree = -c_Sh/64 = {sp.sstr(-C_SH/64)}")
    print("PASS one branch-local scale 64*h^2/c_Sh matches both J and B face jets")
    print("SCOPE: the uniform-history refinement fails C2; the all-good refinement matches two Lorentz face jets only")
    print("SCOPE: neither readout is thereby selected by physical native D0")
    print("PASS direct and sequential Julia instruments are each complete on the full positive 13-effect record")
    print("PASS AB/BA composition defect is measured in both retained flags and the full POVM")
    print("PASS each of the 13 all-success effects has the exact factor-four probability defect")
    for pair, order, defect in composition:
        print(f"COMPOSITION {pair} {order}: all-success probability defect jet = {sp.sstr(defect)}")
    for pair, defect, direct_source, sequential_source in four_edge_composition:
        print(f"FOUR-EDGE {pair}: all-success defect={sp.sstr(defect)}; Golden source increment direct/sequential={sp.sstr(direct_source)} / {sp.sstr(sequential_source)}")
    print("SCOPE: the common factor 64 in the two-face match exactly compensates this four-success attenuation, but native D0 has not selected it")
    print("SCOPE: defect concerns this T(U)=U/2 Julia candidate; it is not a no-go for other native D0 actuation")


if __name__ == "__main__":
    run()
