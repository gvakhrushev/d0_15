"""Exact finite catalogue, shift-support and complete comparator column checks."""

from collections import Counter
from fractions import Fraction as F
from itertools import product
import json


SITES = tuple(product(range(4), repeat=4))
DESCRIPTORS = tuple(product((0, 1), repeat=2))
OFFSETS = tuple((2*s0, 0, 2*s2, 0) for s0, s2 in DESCRIPTORS)
PHASE = ((1, 0), (0, 1), (-1, 0), (0, -1))
INPUT_WIDTH = 18
COLUMNS = 2**INPUT_WIDTH
FULL = (1 << COLUMNS)-1


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def next_site(x, direction, distance):
    return tuple((v+distance) % 4 if i == direction else v for i, v in enumerate(x))


def field(descriptor, x):
    u, v = descriptor
    return PHASE[(x[1]+u*x[0]+v*x[2]) % 4]


def original_moment(d, e, x):
    answer = 0
    for j in range(4):
        ahead = next_site(x, j, 1)
        left = [a-b for a, b in zip(field(d, ahead), field(d, x))]
        right = [a-b for a, b in zip(field(e, ahead), field(e, x))]
        sign = 1 if j == 0 else -1
        answer += sign*sum(a*b for a, b in zip(left, right))
    return F(answer, 2)


def check_catalogue():
    representatives = {}
    fields = {}
    for d, e in product(DESCRIPTORS, repeat=2):
        u, v = d
        U, V = e
        scale = -1+u*U-v*V
        k = u-U, v-V
        fields[d, e] = {}
        for x in SITES:
            moment = scale*PHASE[(k[0]*x[0]+k[1]*x[2]) % 4][0]
            require(moment == original_moment(d, e, x), "Literal CAR differences")
            fields[d, e][x] = moment
        mean = F(sum(fields[d, e].values()), 256)
        require(mean == (scale if d == e else 0), "Global catalogue moment")
        for x in SITES:
            shifted = [tuple((a+b) % 4 for a, b in zip(x, tau)) for tau in OFFSETS]
            require(F(sum(fields[d, e][y] for y in shifted), 4) == mean,
                    "Four shifts scalarize the effect at each SITE")
        if scale and k != (0, 0):
            representatives[k] = d, e
    basis = DESCRIPTORS
    for k, l in product(basis, repeat=2):
        diff = k[0]-l[0], k[1]-l[1]
        if k != l:
            require(diff in representatives, "Each off-diagonal Gram frequency occurs")
        row = [PHASE[(diff[0]*tau[0]+diff[1]*tau[2]) % 4] for tau in OFFSETS]
        re, im = (sum(vector[j] for vector in row) for j in range(2))
        require((re, im) == (4 if k == l else 0, 0), "Exact four-character Gram")
    require(len(representatives) == 8, "All eight signed nonzero frequencies")
    moment = fields[(0, 0), (0, 1)]
    fine = [F(1, 8)*(1+F(moment[x], 2)) for x in ((0, 0, 0, 0), (0, 0, 1, 0))]
    require(fine == [F(1, 16), F(1, 8)], "Retained key joint probability still sees SITE")
    return fine


def input_bit(bit):
    if bit < 3:
        data = bytes((0xaa, 0xcc, 0xf0)[bit : bit+1])*(COLUMNS//8)
    else:
        half = 1 << (bit-3)
        data = (b"\0"*half + b"\xff"*half)*(COLUMNS//16//half)
    return int.from_bytes(data, "little")


def comparison_word(direction):
    ops = [("cx", f"x{i}", f"t{i}") for i in range(8)]
    ops += [("cx", "s0", "t1"), ("cx", "s2", "t5")]
    if direction is not None:
        low = 2*direction
        ops += [("cx", f"t{low}", f"t{low+1}"), ("cx", "h", f"t{low}")]
    for i in range(8):
        ops.extend(("cx", name, f"d{i}") for name in (f"t{i}", f"y{i}", "h"))
    ops.append(("ccx", "d0", "d1", "a0"))
    ops.extend(("ccx", f"a{i-2}", f"d{i}", f"a{i-1}") for i in range(2, 8))
    return ops


def apply(word, state):
    for gate, control, *rest in word:
        if gate == "cx":
            state[rest[0]] ^= state[control]
        else:
            state[rest[1]] ^= state[control] & state[rest[0]]


def check_comparators():
    variables = [f"x{i}" for i in range(8)] + ["s0", "s2"] + [f"y{i}" for i in range(8)]
    initial = {name: input_bit(i) for i, name in enumerate(variables)}
    initial["h"] = FULL
    initial.update({f"{prefix}{i}": 0 for prefix, count in (("t", 8), ("d", 8), ("a", 7))
                    for i in range(count)})
    counts = []
    for direction in (None, 0, 1, 2, 3):
        state = initial.copy()
        word = comparison_word(direction)
        apply(word, state)
        expected = FULL
        for j in range(4):
            low, high = [initial[f"x{i}"] for i in (2*j, 2*j+1)]
            if j in (0, 2):
                high ^= initial[f"s{j}"]
            if j == direction:
                low, high = low ^ FULL, high ^ low
            expected &= FULL ^ (low ^ initial[f"y{2*j}"])
            expected &= FULL ^ (high ^ initial[f"y{2*j+1}"])
        require(state["a6"] == expected, "Full X/key/Y column table")
        apply(reversed(word), state)
        require(state == initial, "All protected registers and 23 scratch wires return")
        inventory = Counter(term[0] for term in word)
        counts.append((2*inventory["ccx"], 2*inventory["cx"]+2))
    require(counts == [(14, 70)] + [(14, 74)]*4, "Includes the two NC1 CX")
    total = tuple(8*(2*a+8*b) for a, b in zip(counts[0], counts[1]))
    require(total == (1120, 5856), "Eighty localization calls")
    return counts, total


def main():
    fine = check_catalogue()
    counts, total = check_comparators()
    print(json.dumps({
        "exact_ordered_descriptor_pairs": len(DESCRIPTORS)**2,
        "sites_per_pair": len(SITES),
        "minimal_positive_shift_support": len(OFFSETS),
        "full_comparator_columns_per_offset": COLUMNS,
        "central_and_four_neighbor_Toffoli_CX": counts,
        "eighty_comparator_Toffoli_CX": total,
        "fresh_plus_wires": 16,
        "fine_key_example_probabilities": list(map(str, fine)),
        "full_hq_instrument_and_Book_price_proved": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
