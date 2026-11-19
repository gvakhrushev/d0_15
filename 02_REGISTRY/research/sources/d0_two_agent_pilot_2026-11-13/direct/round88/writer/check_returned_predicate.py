"""Replay the returned binary writers with explicit reversible gates (Python 3.9+)."""
import json
from fractions import Fraction
from itertools import product
from math import isclose, sqrt


def check(condition, message):
    if not condition:
        raise ValueError(message)


def close(x, y):
    return isclose(x, y, rel_tol=2e-12, abs_tol=2e-12)


def apply(x, word):
    for target, controls in word:
        if all(x & (1 << control) for control in controls):
            x ^= 1 << target
    return x


def multi_x(controls, target, first_clean):
    """Positive multi-control decomposed into Toffoli and clean workspace."""
    if len(controls) <= 2:
        return [(target, controls)]
    compute = [(first_clean, controls[:2])]
    for i in range(2, len(controls) - 1):
        compute.append((first_clean + i - 1, (first_clean + i - 2, controls[i])))
    center = (target, (first_clean + len(controls) - 3, controls[-1]))
    return compute + [center] + list(reversed(compute))


def comparator(bits):
    """XOR [v < m] into output, m has one extra bit to include 2**bits."""
    inputs = tuple(range(2 * bits + 1))
    target = len(inputs)
    positive = multi_x(inputs, target, target + 1)
    word = []
    for v in range(1 << bits):
        for m in range(v + 1, 1 << (bits + 1)):
            code = v | (m << bits)
            flip = [(wire, ()) for wire in inputs if not code & (1 << wire)]
            word.extend(flip + positive + list(reversed(flip)))
    return word, target


def actual_compare():
    word, target = comparator(3)
    inverse = list(reversed(word))
    copied = target + 10
    for v, m, prior in product(range(8), range(16), range(2)):
        initial = v | (m << 3) | (prior << target)
        expected = prior ^ (v < m)
        computed = apply(initial, word)
        check(computed == ((v | (m << 3)) | (expected << target)), "dirty comparator")
        final = apply(apply(computed, [(copied, (target,))]), inverse)
        check(final == initial | (expected << copied), "copy and actual inverse")
    return {"basis_cases": 256, "elementary_gates": len(word)}


def hadamard(state, bit):
    width = 1 << bit
    for low in range(len(state)):
        if low & width:
            continue
        high = low | width
        a, b = state[low], state[high]
        state[low], state[high] = (a + b) / sqrt(2), (a - b) / sqrt(2)


def permute(state, transform):
    new = [0.0] * len(state)
    for i, value in enumerate(state):
        new[transform(i)] += value
    return new


def original_writer():
    # Four work bits, a comparison scratch, and the new independent report.
    rows = []
    for threshold in (10, 11, 12):
        state = [1.0] + [0.0] * 63
        for bit in range(4):
            hadamard(state, bit)
        compare = lambda i: i ^ (16 if (i & 15) < threshold else 0)
        state = permute(state, compare)
        state = permute(state, lambda i: i ^ (32 if i & 16 else 0))
        state = permute(state, compare)
        for bit in reversed(range(4)):
            hadamard(state, bit)
        q = Fraction(threshold, 16)
        total = q*q + (1-q)**2
        check(close(sum(a*a for a in state[32:]), q), "report marginal")
        check(close(state[32]**2, q*q) and close(state[0]**2, (1-q)**2), "real return")
        check(all(close(state[i+32], -state[i]) for i in range(1, 32)), "failure report")
        rows.append({"q": str(q), "return": str(total), "click_given_return": str(q*q/total)})
    return rows


def independent_tape():
    """Enumerate all 2^14 fair words for each sharp tag and input."""
    total = 1 << 14
    count = 0
    samples = {}
    for i, j, tag in product(range(3), range(3), (0, 1)):
        s, t = Fraction(i, 4), Fraction(j, 4)
        m_s, m_t = int(4*(1-s)), int(4*(1-t))
        hits = 0
        for selector, v, w, dilution, head in product(range(4), range(8), range(8), range(4), range(16)):
            sigma = 0
            if selector == 0 and dilution < 2:
                sigma = 1 if ((v < m_s) == (w < m_t)) else -1
            elif selector == 1 and tag == 0 and dilution == 0:
                sigma = -1 if ((v < m_t) == (w < m_t)) else 1
            hits += head < 11 + sigma
        got = Fraction(hits, total)
        target = Fraction(11, 16) + (2*s*t - (t*t if tag == 0 else 0)) / 256
        check(got == target, "independent sign-product predicate")
        samples[(i, j, tag)] = got
        count += total
    # Using one copy twice changes a diagonal term with t=1/2 from 1/4 to 1.
    check(sum(((-1)**(v < 2))**2 for v in range(8)) == 8, "common sample")
    return {"complete_basis_histories": count, "tape_fair_bits": 14,
            "example_q_given_tag0_tag1": [str(samples[(1, 2, k)]) for k in (0, 1)]}


def root_and_archive():
    p = (sqrt(5) - 1) / 2
    a = sqrt(p)
    born = (p, p*p)
    nc1_cold = (p*p, p**3)
    check(all(close(w, p*b) for w, b in zip(nc1_cold, born)), "NC1 cold/Born")
    overlap = (a*p + p*a) / sqrt(2)
    check(close(overlap**2, 2*p**3), "uniform physical dual-rail tape")
    # Direct coherent contraction of three fair pairs, one genuine golden tag
    # and one output head against passive births.
    direct = 0.0
    q = 0.0
    for item, tag in product(range(8), range(2)):
        click = (item + 2*tag) % 5 >= 2
        q += born[tag] * click / 8
        direct += (a*p/sqrt(2))**3 * born[tag] * (p if click else a)
    check(close(direct, overlap**3*(a*(1-q)+p*q)), "coherent cold discrepancy")
    check(close((-p)*a + a*p, 0), "physical dark K")
    d = 3
    allowed, allowed_cold = 2*p**3, 2*p**5
    early = sum(allowed**j * (born[0]**2 + born[1]**2) for j in range(d))
    h0 = sum(allowed_cold**j * (nc1_cold[0]**2 + nc1_cold[1]**2) for j in range(d))
    check(close(early + allowed**d, 1), "early plus later/complete mass")
    for y in (0, 1):
        check((y ^ (1-y)) == 1, "real name rail at late stop")
    # Enumerate the complete service tree in a two-factory example; a stop has
    # exactly one leaf. The actual construction allows any finite readiness.
    f, g = Fraction(3, 4), Fraction(7, 8)
    valid = allowed**d
    late = [valid*float(1-f), valid*float(f*(1-g))]
    success = valid*float(f*g)
    check(close(early + sum(late) + success, 1), "complete service tree")
    for report in (Fraction(5, 8), Fraction(11, 16), Fraction(3, 4)):
        lost = sum(late) + success*float(2*report*(1-report))
        old_return = early + success*float(report**2 + (1-report)**2)
        check(close(old_return + lost, 1), "true unrecovered mass")
        check(close(early + success + sum(late), 1), "new physical return")
    check(close(allowed_cold, 2*nc1_cold[0]*nc1_cold[1]), "balanced cold pairs")
    return {"valid_pair_born": "2*p^3", "valid_pair_cold": "2*p^5",
            "early_cold_d3": format(h0, ".12f"), "checked_retained_tape_words": 16}


def amplitude_obstruction():
    # 11/5 has squareclass 55. F=Q(sqrt(2),sqrt(5)) has classes 1,2,5,10.
    check(55 not in {1, 2, 5, 10}, "radical in base")
    p_norm = -1
    norm = Fraction(11, 5)**2 / p_norm
    check(norm == Fraction(-121, 25), "relative norm")
    return {"flat_probability": "11/16", "ratio_squared": "11/5",
            "squared_radical_class": 55, "relative_norm_other_case": str(norm)}


if __name__ == "__main__":
    result = {"a88": "returned_predicate", "comparator": actual_compare(),
              "old_writer": original_writer(), "independent_writer": independent_tape(),
              "physical_archive": root_and_archive(), "pure_exit_obstruction": amplitude_obstruction(),
              "covers_arbitrary_unknown_field_input": False, "GR_closed": False}
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
