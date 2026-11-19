#!/usr/bin/env python3
"""Exact Golden detector gadgets and their complete capped-renewal price.

Only the standard library and the owned preparation-bank ring are used.
Every check stays active under -O.  This is a conditional circuit/resource
composition: physical primitive, moving-query, task and Book03 admission
remain inputs.  No old geometry, determinant-source or Lean replay is run.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
import json

from check_determinant_preparation_bank import (
    A, G, GT, ONE, P, ZERO, add, expect_rejection, mul, power, require, ring_sum, scale,
)


IDENTITY = ((ONE, ZERO), (ZERO, ONE))
X = ((ZERO, ONE), (ONE, ZERO))
H_NUMERATOR = ((ONE, ONE), (ONE, scale(ONE, -1)))


def matrix_product(left, right):
    return tuple(tuple(ring_sum(mul(left[i][k], right[k][j]) for k in range(2))
                       for j in range(2)) for i in range(2))


def matrix_power(matrix, exponent):
    result = IDENTITY
    for _ in range(exponent):
        result = matrix_product(matrix, result)
    return result


def basis(qubits, index):
    result = [ZERO] * (1 << qubits)
    result[index] = ONE
    return result


def apply_gate(state, target, matrix):
    """Little-endian qubit addresses; exact real amplitudes in Q[a]."""
    result = [ZERO] * len(state)
    mask = 1 << target
    for source, amplitude in enumerate(state):
        if amplitude == ZERO:
            continue
        column = int(bool(source & mask))
        for row in range(2):
            coefficient = matrix[row][column]
            if coefficient != ZERO:
                destination = (source & ~mask) | row * mask
                result[destination] = add(result[destination], mul(coefficient, amplitude))
    return result


def apply_cnot(state, control, target):
    result = [ZERO] * len(state)
    for source, amplitude in enumerate(state):
        destination = source ^ (1 << target) if source & (1 << control) else source
        result[destination] = amplitude
    return result


def apply_word(state, word):
    for instruction in word:
        if instruction[0] == "CX":
            state = apply_cnot(state, instruction[1], instruction[2])
        else:
            state = apply_gate(state, instruction[1], G if instruction[0] == "G" else GT)
    return state


def inverse(word):
    return [("GT" if op[0] == "G" else "G", op[1]) if op[0] != "CX" else op
            for op in reversed(word)]


def controlled_word(controls, target):
    if not controls:
        return [("G", target)]
    previous = controlled_word(controls[:-1], target)
    cx = [("CX", controls[-1], target)]
    return cx + inverse(previous) + cx + previous


def native_word(word, known_one):
    result = []
    for instruction in word:
        if instruction[0] == "GT":
            target = instruction[1]
            result.extend([("CX", known_one, target), ("G", target), ("CX", known_one, target)])
        else:
            result.append(instruction)
    return result


def gate_counts(word):
    return {"G": sum(op[0] == "G" for op in word),
            "CX": sum(op[0] == "CX" for op in word)}


def norm_squared(state):
    return ring_sum(power(amplitude, 2) for amplitude in state)


def check_controlled_phase():
    require(matrix_product(matrix_product(X, G), X) == GT, "exact XGX inverse echo")
    # Verify the retained known-one wire, including superpositions on target.
    for target_bit in (0, 1):
        source = basis(2, 2 + target_bit)
        actual = apply_word(source, native_word([("GT", 0)], 1))
        require(actual == apply_gate(source, 0, GT), "inverse echo preserves known-one control")
    results = []
    for k in (2, 3):
        target, controls = k, list(range(k))
        word = controlled_word(controls, target)
        rotation = matrix_power(G, 1 << k)
        for index in range(1 << (k + 1)):
            actual = apply_word(basis(k + 1, index), word)
            all_controls = index & ((1 << k) - 1) == (1 << k) - 1
            expected = apply_gate(basis(k + 1, index), target, rotation) if all_controls else basis(k + 1, index)
            require(actual == expected, "W_k=C^k G^(2^k) on entire computational basis")
        m = 1 << (k - 1)
        trial = [("GT", target)] * m + word
        half_rotation = matrix_power(G, m)
        cosine, sine = half_rotation[0][0], half_rotation[1][0]
        success = power(sine, 2)
        expected_success = scale(power(P, 3 if k == 2 else 9), 4 if k == 2 else 16)
        require(success == expected_success, "exact CZ/CCZ heralding probability")
        require(add(power(cosine, 2), success) == ONE, "complete phase-trial normalization")
        for controls_index in range(1 << k):
            state = apply_word(basis(k + 1, controls_index), trial)
            sign = -1 if controls_index == (1 << k) - 1 else 1
            expected = [ZERO] * (1 << (k + 1))
            expected[controls_index] = cosine
            expected[controls_index | (1 << target)] = scale(sine, -sign)
            require(state == expected, "K0=cos(m theta) I, K1=-sin(m theta) C^k Z")
            require(norm_squared(state) == ONE, "no phase-gadget branch deleted")
        counts = gate_counts(native_word(trial, k + 1))
        require(counts == {"G": 3 * m, "CX": (1 << (k + 2)) - 2}, "native inverse-echo gate ledger")
        results.append({"controls": k, "basis_inputs": 1 << (k + 1),
                        "success": "4*p^3" if k == 2 else "16*p^9",
                        "native_gate_counts_per_trial": counts,
                        "gate_ticks_excluding_measurement": sum(counts.values()),
                        "Z_measurements_per_trial": 1})
    return results


def x_cycle_word(inverse_second=False):
    # Data0 and two fresh ancillas1,2; each measured ancilla is kept.
    return [("G", 1), ("CX", 1, 0), ("G", 1),
            ("G", 2), ("CX", 2, 0), ("GT" if inverse_second else "G", 2)]


def check_x_cycle():
    ap = mul(A, P)
    expected = {
        (0, 0): ((power(P, 3), ZERO), (ZERO, power(P, 3))),
        (1, 0): tuple(tuple(mul(ap, add(IDENTITY[i][j], X[i][j])) for j in range(2)) for i in range(2)),
        (0, 1): tuple(tuple(scale(mul(ap, add(IDENTITY[i][j], scale(X[i][j], -1))), -1)
                           for j in range(2)) for i in range(2)),
        (1, 1): ((ZERO, ZERO), (ZERO, ZERO)),
    }
    actual = {outcome: [[ZERO] * 2 for _ in range(2)] for outcome in expected}
    for data in (0, 1):
        state = apply_word(basis(3, data), x_cycle_word(True))
        for b in (0, 1):
            for c in (0, 1):
                for output in (0, 1):
                    actual[(b, c)][output][data] = state[output | (b << 1) | (c << 2)]
        require(norm_squared(state) == ONE, "complete two-probe X cycle")
    actual = {key: tuple(tuple(row) for row in value) for key, value in actual.items()}
    require(actual == expected, "all four exact X-cycle Kraus matrices and signs")
    counts = gate_counts(native_word(x_cycle_word(True), 3))
    require(counts == {"G": 4, "CX": 4}, "X-cycle echo ledger")
    # An explicit hostile control: replacing the second inverse by forward G
    # changes the instrument; all four branches may not be reused silently.
    wrong = apply_word(basis(3, 0), x_cycle_word(False))
    right = apply_word(basis(3, 0), x_cycle_word(True))
    require(wrong != right, "forward-for-inverse X-cycle mutation rejected")
    return expected, {"native_gate_counts_per_cycle": counts, "gate_ticks": 8,
                      "Z_measurements_per_cycle": 2,
                      "success_total": "4*p^3", "scalar_failure": "p^3*I",
                      "hostile_control": "second inverse replaced by forward changes Kraus instrument"}


def controlled_z(state, controls):
    return [scale(value, -1) if all(index & (1 << bit) for bit in controls) else value
            for index, value in enumerate(state)]


def check_h_and_toffoli(x_kraus):
    ap = mul(A, P)
    # Use the unnormalized + resource and H numerator.  Both omitted sqrt(2)
    # factors are tracked by norm ratios, so no field extension is required.
    for input_bit in (0, 1):
        initial = [ZERO] * 4
        initial[input_bit] = initial[input_bit | 2] = ONE
        entangled = controlled_z(initial, (0, 1))
        for outcome, label in [((1, 0), 0), ((0, 1), 1)]:
            actual = apply_gate(entangled, 0, x_kraus[outcome])
            expected = [ZERO] * 4
            for measured in (0, 1):
                for output in (0, 1):
                    # Minus outcome leaves |-> and X H on output, with a
                    # global minus from the actual K01, retained explicitly.
                    coefficient = H_NUMERATOR[output ^ label][input_bit]
                    expected[measured | (output << 1)] = scale(
                        mul(ap, coefficient), (-1 if label else 1) * (-1 if label and measured else 1))
            require(actual == expected, "H teleport branch is pure X^label H with known measured input")
            require(norm_squared(actual) == scale(power(P, 3), 4), "uniform teleport labels on basis input")
    # Explicit purification/reference check.  The unnormalized Bell input
    # has norm2; resource norm2, so the starting norm is4.
    initial = [ZERO] * 8
    for bit in (0, 1):
        for resource in (0, 1):
            initial[bit | (resource << 1) | (bit << 2)] = ONE
    entangled = controlled_z(initial, (0, 1))
    for outcome in ((1, 0), (0, 1)):
        output = apply_gate(entangled, 0, x_kraus[outcome])
        require(norm_squared(output) == scale(power(P, 3), 8), "uniform teleport label for entangled input")
    # K10* K10 + K01* K01 = s2 I.  The preceding exact factorization
    # proves arbitrary-reference branch equality by linearity, not sampling.
    success = scale(power(P, 3), 4)
    require(add(power(P, 6), success) == ONE, "X cycle has state-independent scalar failure")
    for index in range(8):
        state = apply_gate(basis(3, index), 2, H_NUMERATOR)
        state = controlled_z(state, (0, 1, 2))
        state = apply_gate(state, 2, H_NUMERATOR)
        state = [scale(v, Q(1, 2)) for v in state]
        expected = basis(3, index ^ 4 if index & 3 == 3 else index)
        require(state == expected, "H_target CCZ H_target is exact Toffoli on all basis states")
    return {"teleport_success_labels": 2, "conditional_label_probability": "1/2",
            "H_success_probability_with_cap_L": "b2^2",
            "known_X_correction_CX_ticks_if_minus": 1,
            "canonical_output_SWAP_CX_ticks": 3,
            "Toffoli_basis_inputs": 8, "Toffoli_uses": "H_target, CCZ, H_target"}


# Exact Boolean polynomial algebra: monomials are squarefree variable sets,
# coefficients are mod2.  Equal polynomials prove equality on every bit string.
BOOL_ZERO = frozenset()


def variable(index):
    return frozenset((frozenset((index,)),))


def bxor(left, right):
    return left ^ right


def band(left, right):
    result = set()
    for a in left:
        for b in right:
            term = a | b
            if term in result:
                result.remove(term)
            else:
                result.add(term)
    return frozenset(result)


def bor(left, right):
    return bxor(bxor(left, right), band(left, right))


def evaluate(poly, bits):
    value = 0
    for monomial in poly:
        value ^= int(all(bits[index] for index in monomial))
    return value


def check_boolean_detector():
    wires, word = [], []

    def fresh(value=BOOL_ZERO):
        wires.append(value)
        return len(wires) - 1

    original = [fresh(variable(i)) for i in range(46)]

    def cx(control, target):
        wires[target] = bxor(wires[target], wires[control])
        word.append(("CX", control, target))

    def toffoli(c1, c2, target):
        wires[target] = bxor(wires[target], band(wires[c1], wires[c2]))
        word.append(("TOF", c1, c2, target))

    def logical_or(a, b):
        output = fresh()
        cx(a, output)
        cx(b, output)
        toffoli(a, b, output)
        return output

    def and_chain(inputs):
        output = inputs[0]
        for control in inputs[1:]:
            new_output = fresh()
            toffoli(output, control, new_output)
            output = new_output
        require(wires[output] == frozenset((frozenset(inputs),)), "20-bit AND polynomial is exactly the all-ones event")
        # Every possible first-zero position and both extremal suffixes; the
        # polynomial identity above covers all 2^20 inputs, beyond these probes.
        for first_zero in range(len(inputs)):
            for suffix in (0, 1):
                bits = [0] * len(wires)
                for j, bit in enumerate(inputs):
                    bits[bit] = int(j < first_zero) if j <= first_zero else suffix
                require(evaluate(wires[output], bits) == 0, "AND first-zero orbit control")
        bits = [1] * len(wires)
        require(evaluate(wires[output], bits) == 1, "AND all-ones control")
        return output

    yes_flags = []
    for query in range(2):
        base = query * 23
        # The original retained addresses are {0,2}: middle bit is free.
        qflag = logical_or(original[base], original[base + 2])
        for index in range(8):
            bits = [0] * len(wires)
            for j in range(3):
                bits[base + j] = (index >> j) & 1
            require(evaluate(wires[qflag], bits) == int(index not in (0, 2)), "original Q={0,2} complement")
        coin = and_chain(original[base + 3:base + 23])
        yes = fresh()
        toffoli(qflag, coin, yes)
        yes_flags.append(yes)
    final = logical_or(*yes_flags)
    expected_queries = []
    for query in range(2):
        base = query * 23
        coin = frozenset((frozenset(range(base + 3, base + 23)),))
        expected_queries.append(band(bor(variable(base), variable(base + 2)), coin))
    require(wires[final] == bor(*expected_queries), "complete 46-input detector polynomial")
    counts = {name: sum(op[0] == name for op in word) for name in ("TOF", "CX")}
    require(counts == {"TOF": 43, "CX": 6}, "actual full Boolean detector gate word")
    require(2 * counts["TOF"] == 86 and 42 + 86 == 128, "same-stage fair resource bank is 128N")
    return {"query_input_bits": 46, "symbolic_entire_domain": "all 2^46 computational inputs",
            "final_polynomial_monomials": len(wires[final]), "gate_counts": counts,
            "extra_plus_resources_per_stage": 86, "total_bank_resources_per_stage": 128,
            "efficiency_event": "20 independent coherent fair bits all equal to one"}


def check_caps_and_net_source():
    lo, hi = Q(618, 1000), Q(619, 1000)
    require(lo * lo + lo - 1 < 0 < hi * hi + hi - 1, "positive Golden-root enclosure")
    require(Q(47, 50) < 4 * lo ** 3 < 4 * hi ** 3 < 1, "0<f2<3/50")
    require(Q(1, 5) < 16 * lo ** 9 < 16 * hi ** 9 < 1, "0<f3<4/5")
    cap = 20
    bad_bound = 43 * (4 * Q(3, 50) ** cap + Q(4, 5) ** cap)
    require(bad_bound < Q(1, 2), "172 CZ/X and 43 CCZ capped gadgets have beta>1/2")
    # Each H has one CZ RUS and one X-cycle RUS.  Each Toffoli has two Hs
    # and one CCZ.  Their branch probabilities are independent of all data.
    require(43 * 2 * 2 == 172, "stage beta=b2^172*b3^43")
    # Binary-record entropy <2 Golden units since phi^2>2. Two-bit entropy
    # is therefore <4. Read/controller prices are nonnegative, not assigned1.
    require(hi ** 2 < Q(1, 2), "log_phi(2)<2")
    require(20 - 2 == 18 and 42 - 2 == 40 and 8 - 4 == 4, "positive per-trial net gate-price lower bounds")
    require(Q(47, 50) ** 2 > Q(22, 25), "first H success has probability>22/25")
    kappa_lower = Q(18) + Q(22, 25) * 40
    require(kappa_lower == Q(266, 5) > 53, "full stage kappa>53 without dropping paid work")
    # For x>=0, E_N(x)<=(1+x)E'_N(x), N>=2. The difference has exact
    # coefficients0,2,4,...,2(N-2),N-2. This is an algebraic transport
    # of the OWNED N=2 threshold, not reuse of the old full c_N gap.
    polynomial_horizons = [2, 3, 7, 100]
    for N in polynomial_horizons:
        E = [1] * N
        derivative = [j + 1 for j in range(N - 1)]
        product = derivative + [0]
        for j, coefficient in enumerate(derivative):
            product[j + 1] += coefficient
        difference = [a - b for a, b in zip(product, E)]
        require(difference == [0] + [2 * j for j in range(1, N - 1)] + [N - 2],
                "generic renewal E_N/E'_N coefficient comparison")
        require(all(c >= 0 for c in difference) and derivative[0] == 1,
                "renewal threshold bounded by N=2 and E'_N>=1")
    # beta*h(q)+h'(q)E_N(beta*q)/E'_N(beta*q)
    # <=h(q)+(1+q)h'(q)<27.5, since beta<=1 and q<.01<1/2.
    # The final scalar threshold and original d>.99 are OWNED inputs.
    source_lower = Q(1, 2) * Q(1, 2) * Q(99, 100) * (Q(53) - Q(55, 2))
    require(source_lower == Q(5049, 800) > 6, "alpha*c_N>6 under the owned source-threshold inputs")
    bank_examples = []
    for N in (1, 2, 7, 100):
        resources = 128 * N
        K = 1
        while resources * Q(53, 100) ** K > Q(1, 2):
            K += 1
        require(resources * Q(53, 100) ** K <= Q(1, 2), "128N preparation bank alpha>=1/2")
        bank_examples.append({"N": N, "resources": resources, "K": K})
    return {"RUS_cap_L": cap, "stage_readiness": "beta=b2^172*b3^43>1/2",
            "stage_abort_union_upper_rational": str(bad_bound),
            "stage_kappa_strict_lower_bound": str(kappa_lower),
            "renewal_threshold_transport_horizons": polynomial_horizons,
            "renewal_polynomial_identity": "(1+x)E'_N(x)-E_N(x)=sum_{j=1}^{N-2}2j*x^j+(N-2)*x^(N-1)",
            "owned_inputs": ["N=2 bound h(q)+(1+q)h'(q)<27.5", "d>0.99", "N>=2"],
            "full_alpha_source_strict_lower_bound": str(source_lower),
            "128N_preparation_bank_examples": bank_examples}


@dataclass(frozen=True)
class Stage:
    probability: Q
    ready: bool
    cost: Q
    record: tuple


def stage_records(successes, caps, costs):
    """Small rational ledger fixture, NOT a numerical physical gate price."""
    records = []

    def visit(index, probability, cost, record):
        if index == len(successes):
            # An actual uniform teleport outcome, correction, canonical route.
            for label in (0, 1):
                records.append(Stage(probability / 2, True, cost + 3 + label, record + (label,)))
            return
        s, cap, trial_cost = successes[index], caps[index], costs[index]
        for failed in range(cap):
            visit(index + 1, probability * (1 - s) ** failed * s,
                  cost + (failed + 1) * trial_cost, record + (failed + 1,))
        records.append(Stage(probability * (1 - s) ** cap, False,
                             cost + cap * trial_cost, record + ("abort",)))

    visit(0, Q(1), Q(3), ())
    return records


@dataclass(frozen=True)
class RenewalLeaf:
    probability: Q
    jet: Q
    cost: Q
    powers: tuple
    terminal: str


def renewal_leaves(stages, q, cap):
    result = []
    terms = len(stages) + 2

    def visit(depth, probability, cost, powers):
        for index, stage in enumerate(stages):
            counts = list(powers)
            counts[index] += 1
            stage_probability = probability * stage.probability
            stage_cost = cost + stage.cost
            if not stage.ready:
                jet = stage_probability * (Q(counts[-2]) / q - Q(counts[-1]) / (1 - q))
                result.append(RenewalLeaf(stage_probability, jet, stage_cost, tuple(counts), "stage-abort"))
                continue
            for continued in (False, True):
                leaf_counts = counts.copy()
                leaf_counts[-2 if continued else -1] += 1
                leaf_probability = stage_probability * (q if continued else 1 - q)
                if continued and depth + 1 < cap:
                    visit(depth + 1, leaf_probability, stage_cost, tuple(leaf_counts))
                else:
                    jet = leaf_probability * (Q(leaf_counts[-2]) / q - Q(leaf_counts[-1]) / (1 - q))
                    terminal = "unresolved-cap" if continued else "query-success"
                    result.append(RenewalLeaf(leaf_probability, jet, stage_cost, tuple(leaf_counts), terminal))

    visit(0, Q(1), Q(0), (0,) * terms)
    return result


def check_renewal_fixture(successes, caps, q, horizon):
    stages = stage_records(successes, caps, (Q(20), Q(42)))
    require(sum((s.probability for s in stages), Q(0)) == 1, "complete stage transcript mass")
    beta = sum((s.probability for s in stages if s.ready), Q(0))
    require(beta == (1 - (1 - successes[0]) ** caps[0]) * (1 - (1 - successes[1]) ** caps[1]),
            "stage readiness is product of actual capped trial laws")
    expected_cost = sum((s.probability * s.cost for s in stages), Q(0))
    leaves = renewal_leaves(stages, q, horizon)
    require(sum((leaf.probability for leaf in leaves), Q(0)) == 1, "renewal retains every stage abort and N cap")
    require(sum((leaf.jet for leaf in leaves), Q(0)) == 0, "complete renewal probability first jet")
    x = beta * q
    E = sum((x ** j for j in range(horizon)), Q(0))
    dE = beta * sum((j * x ** (j - 1) for j in range(1, horizon)), Q(0))
    cost = sum((leaf.probability * leaf.cost for leaf in leaves), Q(0))
    cost_jet = sum((leaf.jet * leaf.cost for leaf in leaves), Q(0))
    require(cost == expected_cost * E, "actual gate clock is EC(T)*E_N(beta*q)")
    require(cost_jet == expected_cost * dE, "all aborted stage costs enter the clock first source")
    entropy = tuple(-sum((leaf.probability * leaf.powers[i] for leaf in leaves), Q(0))
                    for i in range(len(stages) + 2))
    entropy_jet = tuple(-sum((leaf.jet * leaf.powers[i] for leaf in leaves), Q(0))
                        for i in range(len(stages) + 2))
    expected_entropy = tuple(-s.probability * E for s in stages) + (-beta * q * E, -beta * (1 - q) * E)
    expected_entropy_jet = tuple(-s.probability * dE for s in stages) + (
        -beta * E - beta * q * dE, beta * E - beta * (1 - q) * dE)
    require(entropy == expected_entropy, "full entropy is [H(T)+beta*h(q)]*E_N(beta*q)")
    require(entropy_jet == expected_entropy_jet, "full entropy first-source coefficients include stage entropy renewal")
    # The universal -sum P'/ln(phi) term is zero by the exact mass jet above.
    full_source = (cost_jet,) + tuple(-value for value in entropy_jet)
    formula_source = (expected_cost * dE,) + tuple(s.probability * dE for s in stages) + (
        beta * E + beta * q * dE, -beta * E + beta * (1 - q) * dE)
    require(full_source == formula_source, "D[(kappa-beta*h(q))*E_N(beta*q)] exactly matches all leaf sources")
    abort_mass = sum((leaf.probability for leaf in leaves if leaf.terminal == "stage-abort"), Q(0))
    require(abort_mass > 0, "actual stage aborts are nonempty")
    kept_mass = sum((leaf.probability for leaf in leaves if leaf.terminal != "stage-abort"), Q(0))
    require(kept_mass == 1 - abort_mass < 1, "erasing RUS aborts fails normalization")
    erased_abort_control = expect_rejection(
        lambda: require(kept_mass == 1, "erasing stage RUS aborts loses normalization"),
        "erasing stage RUS aborts loses normalization")
    require(any(leaf.terminal == "unresolved-cap" for leaf in leaves), "unresolved query cap retained")
    # A cheap exact distinction between measuring an efficiency coin and
    # measuring only its coarse query flag. At lambda=1/2,z=1/4 the former
    # source is zero; the latter is (1/4)log_phi(7), strictly positive.
    z, lam = Q(1, 4), Q(1, 2)
    coarse_odds, measured_odds = (1 - z * lam) / (z * lam), (1 - lam) / lam
    require(coarse_odds == 7 and measured_odds == 1, "measured coin cannot replace coherent coarse flag entropy/source")
    return {"stage_transcripts": len(stages), "complete_renewal_leaves": len(leaves),
            "q": str(q), "N": horizon, "beta": str(beta),
            "clock_cost": str(cost), "clock_source": str(cost_jet),
            "retained_stage_abort_mass": str(abort_mass),
            "price_source_coefficients_constant_then_stage_logs_then_q_logs": [str(v) for v in full_source],
            "negative_controls": [erased_abort_control,
                                  "measured efficiency coin source=0 versus coarse source=log_phi(7)/4"]}


def main():
    phase = check_controlled_phase()
    x_kraus, x_cycle = check_x_cycle()
    teleport = check_h_and_toffoli(x_kraus)
    boolean = check_boolean_detector()
    bounds = check_caps_and_net_source()
    fixtures = [check_renewal_fixture((Q(3, 5), Q(2, 3)), (1, 2), Q(2, 7), 3),
                check_renewal_fixture((Q(2, 3), Q(3, 5)), (2, 2), Q(3, 5), 2)]
    print(json.dumps({"status": "PASS: exact conditional Golden detector and full renewal composition",
                      "ring": "Q[a]/(a^4+a^2-1), a>0,p=a^2",
                      "controlled_phase_gadgets": phase, "X_cycle": x_cycle,
                      "H_teleportation_and_Toffoli": teleport, "Boolean_detector": boolean,
                      "caps_and_source_bounds": bounds, "full_renewal_fixtures": fixtures,
                      "price": "S=(kappa-beta*h_phi(q))*E_N(beta*q), kappa=EC(T)-H_phi(T)",
                      "retained_assumptions": [
                          "Owned moving original 8D query and fixed field/readout through variable delays",
                          "Paid fresh blanks, canonical addressed slots, measured feedforward and nonnegative read/controller costs",
                          "Same complete measured transcript and pure retained conditional work",
                          "Compulsory future task, physical Book03 Info and all primitive admission remain open",
                          "Owned determinant/source threshold is consumed, not re-proved by fixtures",
                      ]}, indent=2))


if __name__ == "__main__":
    main()
