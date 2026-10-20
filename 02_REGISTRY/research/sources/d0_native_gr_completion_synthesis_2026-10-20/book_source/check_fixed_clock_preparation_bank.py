#!/usr/bin/env python3
"""Fixed-duration scheduling of the already-owned Golden preparation bank.

Consumes DETERMINANT_PREPARATION_BANK.md, blob
e7b92fae0d6f3dc3e60499f0dd041c18003da872, and its parity instrument.
Does not re-prove that instrument, native gate admission, or a physical clock.

New checks: every retained leaf executes the same schedule; reverse-scan
three-CNOT routing is reversible; seed failure still executes all later
echoes; literal 00/10 records include a paid deterministic zero pad;
the complete all-trial CQ law has the stated source factor.

The rational success probability below is a generic scheduling fixture,
not a replacement for the owned Golden probability 2*p**3.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
from math import isqrt


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def cx_word_swap(x, y):
    """Three literal CNOTs on arbitrary basis values; hence on all vectors."""
    y ^= x
    x ^= y
    y ^= x
    return x, y


for basis in product((0, 1), repeat=2):
    require(cx_word_swap(*basis) == basis[::-1], "three-CNOT word is full SWAP")


def expected_counts(m, K, n_minus):
    return Counter({
        "G": 2*m*K,
        "CX": (6*m + 2*n_minus + 3)*K,
        "parity_reads": m*K,
        "report_symbols": 2*m*K,
        "address_choices": (m+1)*K,
    })


def execute_factory_leaf(bits, m, K, minus_resources):
    """Complete finite control trace; each quantum register is a state token.

    Conditional pure states are supplied by the owned instrument:
    a success gives (+ or -, 1, 1), a failure gives (retained pure work,0,0).
    Both G/G and G/G^T variants have the same success probability.
    Token permutation checks retention without tracing any old register.
    """
    require(len(bits) == m*K, "all scheduled parity values are supplied")
    require(0 not in minus_resources, "first resource is the plus seed")
    require(all(0 < j < m for j in minus_resources), "minus roles are valid")
    before_bits = tuple(bits)
    slots = {"oldRIGHT": ("oldRIGHT", "unknown-protected"),
             "control": ("initial-control", 0),
             "dummy0": ("dummy0", 0), "dummy1": ("dummy1", 0)}
    for j in range(m):
        slots[("target", j)] = (("initial-target", j), 0)
    counts = Counter()
    report = []
    route_history = []
    failed_slots = {}
    seed_control = 0

    def swap(left, right):
        # This is the full three-CNOT identity checked above, not erasure.
        counts["CX"] += 3
        slots[left], slots[right] = slots[right], slots[left]

    for resource in range(m):
        row = bits[resource*K:(resource+1)*K]
        minus_word = resource in minus_resources
        # The two extra CX calls are executed even when their known control0
        # makes their logical action identity. Their prefix clock still ticks.
        sign = "-" if minus_word and seed_control else "+"
        for j, success in enumerate(row):
            counts["G"] += 2
            counts["CX"] += 3 + (2 if minus_word else 0)
            counts["parity_reads"] += 1
            # Original 0/10 report plus a REAL deterministic zero tick on0.
            native = (1, 0) if success else (0,)
            pad = () if success else (0,)
            encoded = native + pad
            require(encoded == (success, 0), "paid equal-length report")
            report.extend(encoded)
            counts["report_symbols"] += len(encoded)
            slots[("A", resource, j)] = (
                ("A", resource, j), sign if success else ("failure", sign))
            slots[("B", resource, j)] = (("B", resource, j), success)
            slots[("C", resource, j)] = (("C", resource, j), success)
            if not success:
                for wire in ("A", "B", "C"):
                    key = (wire, resource, j)
                    failed_slots[key] = slots[key]

        tokens_before = Counter(state[0] for state in slots.values())
        # Reverse scan has exactly K iterations, including the all-failure leaf.
        for j in range(K-1, -1, -1):
            counts["address_choices"] += 1
            pair = (("A", resource, j), ("target", resource)) if row[j] else (
                "dummy0", "dummy1")
            route_history.append((resource, j, "target", pair))
            swap(*pair)
            if resource == 0:
                counts["address_choices"] += 1
                pair = (("B", resource, j), "control") if row[j] else (
                    "dummy0", "dummy1")
                route_history.append((resource, j, "seed", pair))
                swap(*pair)
        require(Counter(state[0] for state in slots.values()) == tokens_before,
                "routing preserves every complete quantum-state token")
        require(slots["dummy0"][1] == slots["dummy1"][1] == 0,
                "dummy SWAP is on known blanks and remains paid")
        successes = [j for j, outcome in enumerate(row) if outcome]
        if successes:
            first = successes[0]
            require(slots[("target", resource)][0] == ("A", resource, first),
                    "reverse scan routes the first successful resource")
            require(slots[("target", resource)][1] == sign,
                    "canonical output has the supplied pure signed state")
        else:
            require(slots[("target", resource)][1] == 0,
                    "failed resource leaves a known blank canonical slot")
        if resource == 0:
            seed_control = slots["control"][1]
            require(seed_control == int(bool(successes)),
                    "canonical seed control is1 on seed success,0 otherwise")

    require(tuple(bits) == before_bits, "all measured parity records retained")
    require(all(slots[key] == state for key, state in failed_slots.items()),
            "all failed quantum registers retained unchanged")
    require(slots["oldRIGHT"] == ("oldRIGHT", "unknown-protected"),
            "no operation acts on oldRIGHT")
    require(tuple(report[::2]) == tuple(bits) and not any(report[1::2]),
            "full fixed-length transcript is lossless and padding deterministic")
    require(counts == expected_counts(m, K, len(minus_resources)),
            "same literal gate/readout/address inventory on every leaf")
    ready = all(any(bits[j*K:(j+1)*K]) for j in range(m))
    if ready:
        require(seed_control == 1, "READY contains a genuine known-one seed")
        require(tuple(slots[("target", j)][1] for j in range(m)) ==
                tuple("-" if j in minus_resources else "+" for j in range(m)),
                "all READY leaves deliver the same canonical quantum tensor")
    return counts, tuple(report), ready, tuple(route_history)


def add_terms(left, right, scale=F(1)):
    result = defaultdict(F, left)
    for key, value in right.items():
        result[key] += scale*value
    return {key: value for key, value in result.items() if value}


def log_terms(value):
    """Exact formal natural logarithm of a positive rational."""
    require(value > 0, "positive log argument")
    result = {}
    for integer, sign in ((value.numerator, 1), (value.denominator, -1)):
        divisor = 2
        while divisor <= isqrt(integer):
            exponent = 0
            while integer % divisor == 0:
                integer //= divisor
                exponent += 1
            if exponent:
                result = add_terms(result, {divisor: sign*exponent})
            divisor += 1
        if integer > 1:
            result = add_terms(result, {integer: sign})
    return result


def entropy_terms(probabilities):
    result = {}
    for probability in probabilities:
        result = add_terms(result, log_terms(probability), -probability)
    return result


def price_derivative(rows):
    """ln(phi) times D(E paid cost - H_phi), including ALL leaves."""
    require(sum(prob for prob, _, _ in rows) == 1, "complete law normalized")
    require(sum(jet for _, jet, _ in rows) == 0, "complete law tangent normalized")
    result = {"ln_phi": sum(jet*cost for _, jet, cost in rows)}
    for probability, jet, _ in rows:
        result = add_terms(result, log_terms(probability), jet)
    return {key: value for key, value in result.items() if value}


# Exhaust all leaves of a small bank, including seed-failure continuations.
m, K, minus_resources = 3, 2, frozenset({1})
alpha, r = F(2, 5), F(3, 5)
leaves = []
inventories = set()
elapsed = set()
old_ready_trial_counts = set()
reports = set()
for bits in product((0, 1), repeat=m*K):
    counts, report, ready, route = execute_factory_leaf(bits, m, K, minus_resources)
    probability = alpha**sum(bits) * r**(m*K-sum(bits))
    # A concrete fixed-duration interface fixture. Address selection and READY
    # handling have declared fixed overhead; these values are NOT native proofs.
    # Parity reads are inventoried separately but not double-charged on top of
    # their two reporting-symbol ticks in this fixture.
    control_ticks = 2*counts["address_choices"] + 5
    cost = counts["G"] + counts["CX"] + counts["report_symbols"] + control_ticks
    leaves.append((probability, ready, cost))
    inventories.add(tuple(sorted(counts.items())))
    elapsed.add(cost)
    reports.add(report)
    if ready:
        old_ready_trial_counts.add(sum(
            next(j+1 for j, b in enumerate(bits[i*K:(i+1)*K]) if b)
            for i in range(m)))
    require(len(route) == (m+1)*K, "fixed reverse-scan iteration count")
require(sum(w for w, _, _ in leaves) == 1, "all factory leaves retained")
require(len(inventories) == len(elapsed) == 1, "fixed duration, not just fixed mean")
require(len(reports) == 2**(m*K), "no measured distinctions lost in equal-length code")
require(len(old_ready_trial_counts) > 1, "old first-success bank has varying ready delay")
sigma = sum(w for w, ready, _ in leaves if ready)
require(sigma == (1-r**K)**m, "unchanged READY probability after all-trial padding")
require(entropy_terms([w for w, _, _ in leaves]) ==
        {prime: m*K*value for prime, value in entropy_terms([alpha, r]).items()},
        "complete all-trial entropy is m*K*h(alpha), not stop-time entropy")

# A finite clock with more labels than the complete scheduled prefix never wraps.
# This implements the supplied clock interface; it does not identify its index with u.
ticks = next(iter(elapsed))
clock_labels = tuple(n % (ticks+1) for n in range(ticks+1))
require(len(set(clock_labels)) == ticks+1 and clock_labels[-1] == ticks,
        "all primitive stages distinct, including identity-on-data dummy calls")

# Verify the symbolic 42N inventory independently by counting the fixed role list.
for N, cap in ((2, 1), (3, 2), (16, 3)):
    roles = tuple("minus" if j % 42 == 1 else "plus" for j in range(42*N))
    require(roles[0] == "plus" and roles.count("minus") == N,
            "actual two-query bank has one minus resource per attempt")
    counts = expected_counts(len(roles), cap, roles.count("minus"))
    require(counts["G"] == 84*N*cap, "fixed bank G inventory")
    require(counts["CX"] == (254*N+3)*cap, "echo, route and seed CX inventory")
    require(counts["report_symbols"] == 84*N*cap, "paid two-symbol parity reports")

# Entire finite monitored detector, with retained terminal unresolved branch.
d, q, horizon, tau = F(3, 7), F(4, 7), 3, 8
detector = []
for n in range(horizon):
    probability = q**n*d
    jet = q**n - (n*q**(n-1)*d if n else 0)  # derivative with respect to d
    detector.append((probability, jet, tau*(n+1)))
detector.append((q**horizon, -horizon*q**(horizon-1), tau*horizon))
complete = []
for weight, ready, factory_cost in leaves:
    if ready:
        complete.extend((weight*prob, weight*jet, factory_cost+cost)
                        for prob, jet, cost in detector)
    else:
        complete.append((weight, F(0), factory_cost))
target = add_terms({}, price_derivative(detector), sigma)
require(price_derivative(complete) == target,
        "whole fixed-clock CQ price source equals actual READY mass times detector source")
require(target != price_derivative(detector),
        "discarding aborted bank histories loses the physical source factor")

print("PASS: every full bank leaf has the same paid primitive inventory and duration")
print("PASS: reverse-scan three-CNOT routing retains failures and selects the first success")
print("PASS: failed seed still executes all minus echoes with a known-zero control")
print("PASS: 00/10 reports include real zero padding; complete entropy is m*K*h(alpha)")
print("PASS: full unconditional Cost-Info source is sigma times the existing detector source")
print("Symbolic native-bank inventory: G=84*N*K, CX=(254*N+3)*K, report ticks=84*N*K")
print("Scope: supplied coherent parity gadget, addressed fixed-time control and primitive clock; no u-clock derivation")
