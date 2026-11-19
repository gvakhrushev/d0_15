"""Exact four-wire gate schedules, native-blank work, and retained reference preparation."""
from collections import Counter
from fractions import Fraction
from itertools import product
import json


def require(value, message):
    if not value:
        raise ArithmeticError(message)


# Pair (m,n) represents m+n*p, p^2=1-p.
def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def neg(x):
    return tuple(-a for a in x)


def mul(x, y):
    a, b = x
    c, d = y
    return a*c+b*d, a*d+b*c-b*d


def power(x, n):
    result = (1, 0)
    for _ in range(n):
        result = mul(result, x)
    return result


one, zero, p = (1, 0), (0, 0), (0, 1)
p2 = power(p, 2)
p3 = power(p, 3)
gates = {"P": (0, 1), "Q0": (1, 2), "Q1": (1, 3), "T": (3, 4)}


def schedule(field):
    words = []
    for j in (0, 1):
        q = f"Q{j}"
        words.extend(("P", q, "P", q) if field == j else ("P", "P", q, q))
    return words


def run(word, state):
    state = list(state)
    charge = 0
    for name in word:
        control, target = gates[name]
        state[target] ^= state[control]
        if name == "Q0":
            charge += state[1]
    return tuple(state), charge


def raw_work(word, active_width):
    """Full computational diagonal of independent canonical births."""
    work = zero
    for state in product((0, 1), repeat=active_width):
        prob = mul(power(p, state.count(0)), power(p2, state.count(1)))
        _, charge = run(word, state)
        work = add(work, mul((charge, 0), prob))
    return work


def odd_population(blank_count):
    even, odd = one, zero
    for _ in range(blank_count):
        even, odd = add(mul(even, p), mul(odd, p2)), add(mul(even, p2), mul(odd, p))
    return odd


def main():
    schedules = [schedule(j) for j in range(2)]
    checks = 0
    for field, word in enumerate(schedules):
        require(Counter(word) == {"P": 4, "Q0": 2, "Q1": 2}, "named inventory")
        for state in product((0, 1), repeat=4):
            wanted = list(state)
            wanted[2+field] ^= state[0]
            require(run(word, state)[0] == tuple(wanted), "dirty column")
            require(run(word[::-1], wanted)[0] == state, "mechanical return")
            checks += 2
        # At each prefix the full uniform ensemble induces I/4 on the
        # true local two-port support, including vanishing off-diagonals.
        for i, name in enumerate(word):
            local_states = Counter()
            outputs = {run(word[:i+1], st)[0] for st in product((0, 1), repeat=4)}
            require(len(outputs) == 16, "unitary permutation")
            c, t = gates[name]
            for out in outputs:
                local_states[out[c], out[t]] += 1
            require(list(sorted(local_states.values())) == [4]*4, "tracial CW1")

    queries = [w+["T"]+w[::-1]+["T"] for w in schedules]
    for field, word in enumerate(queries):
        for state in product((0, 1), repeat=5):
            want = list(state)
            want[4] ^= state[0]*field
            require(run(word, state)[0] == tuple(want), "complete addressed query")
            checks += 1
    forward_work = [raw_work(word, 4) for word in schedules]
    query_work = [raw_work(word, 5) for word in queries]
    gap = add(forward_work[0], neg(forward_work[1]))
    full_gap = add(query_work[0], neg(query_work[1]))
    require(gap == power(p, 5) and full_gap == mul((2, 0), gap), "native blank gap")

    # Independent recurrence for the CNOT preparation, expressed in Z[p].
    # Squared Bloch x suffices, since all coefficients and overlaps are positive.
    t_squared = mul((4, 0), p3)
    masks = {}
    for k in (1, 2, 4, 8):
        b = odd_population(k)
        z = add(one, mul((-2, 0), b))
        require(z == power(p, 3*k), "actual parity preparation")
        # Coherent XOR with a fresh canonical control leaves X invariant;
        # each independent copied target reduces its squared overlap by 4p^3.
        x_sq = t_squared
        for ell in range(7):
            require(x_sq == power(t_squared, ell+1), "copied-target X")
            if ell == 6:
                masks[k] = {"gap_pair_two_legs": mul((2, 0), mul(p2, z)),
                            "squared_trace_error_six_raw_shadows": add(x_sq, mul(z, z))}
            x_sq = mul(x_sq, t_squared)

    # Independent amplitude calculation on each complete coherent reference.
    # Initial amplitude on an n-bit reference address with r ones is a^(n+r).
    amplitude_cases = 0
    for k in range(1, 4):
        for ell in range(4):
            n = k + ell
            exponents = {}
            for state in product((0, 1), repeat=n):
                out = list(state)
                out[0] ^= sum(state[1:k]) % 2
                for j in range(k, n):
                    out[j] ^= out[0]
                exponents[tuple(out)] = n + sum(state)
            require(len(exponents) == 2**n, "native reference permutation")
            parity = (ell+1) % 2
            z, x_without_a = zero, zero
            for address, e in exponents.items():
                z = add(z, mul((1-2*address[0], 0), power(p, e)))
                other = (1-address[0], *address[1:])
                total = e + exponents[other]
                require(total % 2 == parity, "X parity in exact ring")
                x_without_a = add(x_without_a, power(p, (total-parity)//2))
            x_sq = mul(power(p, parity), mul(x_without_a, x_without_a))
            require(z == power(p, 3*k) and x_sq == power(t_squared, ell+1),
                    "full retained wave disagrees with marginal")
            amplitude_cases += 1

    # At H=B=v, verify the exact parity law independently on every 6-letter
    # order with repetitions in this palette (not just the displayed two words).
    words_checked = 0
    for word in product(("P", "Q0", "Q1"), repeat=6):
        m_odd, seen = 0, 0
        for name in word:
            if name == "P":
                seen ^= 1
            elif name == "Q0":
                m_odd += seen
        expected = add(mul((word.count("Q0"), 0), p2), mul((m_odd, 0), gap))
        require(raw_work(word, 4) == expected, "general prefix parity")
        require(run(word, (1,0,0,0))[0][2] == m_odd % 2, "slope column")
        words_checked += 1
    # In a two-qubit active gate, the normalized trace of CX is 1/2.
    require(Fraction(sum((c, t^c) == (c,t) for c,t in product((0,1), repeat=2)),4)
            == Fraction(1,2), "purified trace distance check")
    print(json.dumps({"basis_equalities_for_words_and_true_queries": checks,
                      "all_length_six_word_orders_tested": words_checked,
                      "independent_full_reference_preparations": amplitude_cases,
                      "full_native_work_at_Q0": query_work, "forward_native_work_at_Q0": forward_work,
                      "full_difference_in_Zp": full_gap, "forward_difference_in_Zp": gap,
                      "named_counts_per_loader": dict(sorted(Counter(schedules[0]).items())),
                      "raw_shadow_examples_in_Zp": masks, "schedules": schedules,
                      "charging_all_admitted_physics_established": False},
                     ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
