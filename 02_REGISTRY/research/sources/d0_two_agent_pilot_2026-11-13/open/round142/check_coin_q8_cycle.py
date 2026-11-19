"""Check the complementary Golden coin and the local Q8 comparison cycle exactly."""

import json
from itertools import combinations, product

import sympy as sp


LABELS = ("1", "i", "j", "k", "-1", "-i", "-j", "-k")
PRODUCT = (
    (0, 1, 2, 3),
    (1, 4, 3, 6),
    (2, 7, 4, 1),
    (3, 2, 5, 4),
)


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def multiply(left, right):
    basis = PRODUCT[left % 4][right % 4]
    sign = (basis // 4) ^ (left // 4) ^ (right // 4)
    return 4 * sign + basis % 4


def check_coin():
    p = (sp.sqrt(5) - 1) / 2
    a = sp.sqrt(p)
    v = sp.Matrix([a, p])
    actual_cx = sp.diag(sp.eye(2), sp.Matrix([[0, 1], [1, 0]]))
    tagged = actual_cx * sp.kronecker_product(sp.eye(2), v)
    require(tagged == sp.Matrix([[a, 0], [p, 0], [0, p], [0, a]]),
            "The actual coin orientation changed")
    x, y, q, phase = sp.symbols("x y q phase", real=True)
    f0 = q * (1 - q) * (p * x**2 + p**2 * y**2 - 2 * a * p * x * y * phase)
    f1 = q * (1 - q) * (p**2 * x**2 + p * y**2 - 2 * a * p * x * y * phase)
    gap = (f0 - f1) / (q * (1 - q) * p**3)
    normalizer = (1 - q) * x**2 + q * y**2
    require(sp.simplify(gap - (x**2 - y**2)) == 0, "Coin difference depends on phase")
    require(sp.simplify(normalizer + q * gap - x**2) == 0, "Wrong first weight")
    require(sp.simplify(normalizer - (1 - q) * gap - y**2) == 0, "Wrong second weight")
    for variable, expected in ((x, 2*x), (y, -2*x), (q, 0), (phase, 0)):
        derivative = sp.diff(f0 - f1, variable).subs(y, x)
        require(sp.simplify(derivative - q*(1-q)*p**3*expected) == 0,
                "Wrong source at saturation")

    delta = sp.Symbol("delta", real=True)
    defect = q*(1-q)*(x**2 + y**2 - 2*x*y*sp.cos(delta))
    for variable in (x, y, q, delta):
        require(sp.diff(defect, variable).subs({y: x, delta: 0}) == 0,
                "The squared reference defect must be stationary at phase saturation")
    require(sp.simplify(sp.diff(defect, delta).subs({y: x, delta: sp.pi/2})
                        - 2*q*(1-q)*x**2) == 0,
            "Equal magnitudes alone must not force the defect source to vanish")

    isometry = sp.Matrix([[a, 0], [0, a], [p, 0], [0, p]])
    require(sp.simplify(isometry.T * isometry - sp.eye(2)) == sp.zeros(2),
            "The two-sector example must be an isometry on its input")
    born_range = isometry * isometry.T
    weights = sp.diag(x, y, y, phase)
    commutator = weights * born_range - born_range * weights
    leakage = (sp.eye(4) - born_range) * weights * isometry
    require(sp.simplify(sp.trace(commutator.T * commutator)
                        - 2 * sp.trace(leakage.T * leakage)) == 0,
            "Wrong factor in the graph energy identity")
    return {"amplitude_order_by_coin": [["sqrt(p)", "p"], ["p", "sqrt(p)"]],
            "phase_cancels_from_weight_jet": True, "saturation_graph_energy": True}


def edges_for(translations):
    return [
        ((0, g), (1, multiply(h, g)))
        for h, g in product(translations, range(8))
    ]


def components(edges):
    neighbors = {(b, g): set() for b, g in product(range(2), range(8))}
    for left, right in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    unseen = set(neighbors)
    sizes = []
    while unseen:
        start = unseen.pop()
        pending = [start]
        size = 1
        while pending:
            fresh = neighbors[pending.pop()] & unseen
            unseen -= fresh
            pending.extend(fresh)
            size += len(fresh)
        sizes.append(size)
    return sorted(sizes), neighbors


def check_translators():
    for control, sign, i_bit, j_bit in product(range(2), repeat=4):
        encoded = 4 * sign + i_bit + 2 * j_bit
        i_output = 4 * (sign ^ (control & i_bit)) + (i_bit ^ control) + 2 * j_bit
        j_sign = sign ^ (control & i_bit) ^ (control & j_bit)
        j_output = 4 * j_sign + i_bit + 2 * (j_bit ^ control)
        require(i_output == multiply(control, encoded), "Wrong controlled i address")
        require(j_output == multiply(2 * control, encoded), "Wrong controlled j address")


def check_regular_algebra():
    def translation(h, right=False):
        matrix = sp.zeros(8)
        for g in range(8):
            row = multiply(g, h) if right else multiply(h, g)
            matrix[row, g] = 1
        return matrix

    c4 = (0, 1, 4, 5)
    basis = [translation(h) for h in c4]
    rj = translation(2, right=True)
    require(rj*rj == translation(4), "Right j squared must be the common central minus")
    for a in basis:
        require(rj*a == a*rj, "Left and right regular actions must commute")
    for parity, a, b in product((0, 1), basis, basis):
        left, right = a*rj**parity, b*rj**parity
        require(left*right.T == a*b.T and a*b.T in basis,
                "Same-parity block products must lie in the C4 group algebra")
    # The identity column of every even block has no support on j C4;
    # every odd block has the opposite support. A controlled j needs both.
    for g in c4:
        require(multiply(g, 2) not in c4, "The other coset must stay distinct")


def check_cycle():
    check_translators()
    check_regular_algebra()
    edges = edges_for((0, 1, 2))
    sizes, neighbors = components(edges)
    require(sizes == [16] and len(set(edges)) == 24, "Wrong full graph")
    require(components(edges_for((4,)))[0] == [2] * 8, "Wrong one-translation graph")
    require(components(edges_for((0, 1, 4, 5)))[0] == [8, 8], "Wrong C4 components")
    for first, second in combinations(((0, g) for g in range(8)), 2):
        require(len(neighbors[first] & neighbors[second]) <= 1, "Found a four-cycle")

    cycle = [(0, 0), (1, 0), (0, 5), (1, 5), (0, 7), (1, 2), (0, 0)]
    require(all(second in neighbors[first] for first, second in zip(cycle, cycle[1:])),
            "The six-cycle uses an unavailable edge")

    def length(vertex):
        bit, group = vertex
        return 4 + bit + bin(group).count("1")

    changes = [(-1)**index * (length(second) - length(first))
               for index, (first, second) in enumerate(zip(cycle, cycle[1:]))]
    require(changes == [1, -1, 1, 0, -1, 2], "Wrong Golden edge exponents")
    require(sum((-1)**index * value for index, value in enumerate(changes)) == 0,
            "The literal code prices do not telescope")
    return {"vertices": 16, "edges": 24, "relative_rank": 15, "cycle_rank": 9,
            "C4_components": [8, 8], "girth": 6,
            "example_cycle": [(b, LABELS[g]) for b, g in cycle],
            "unoriented_leaf_length_differences": changes}


def main():
    print(json.dumps({"status": "PASS", "coin": check_coin(), "Q8": check_cycle(),
                      "full_Book_price_selected": False, "GR_closed": False}, indent=2))


if __name__ == "__main__":
    main()
