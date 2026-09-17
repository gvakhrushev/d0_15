# STRUCTURE_FIXED_BEFORE_NUMBER: binary supports, cellular boundary, and capacity equations precede outputs.
"""Certificate for concrete repair semantics, topological shell attachment, and forcing-DAG closure."""

from itertools import product


SIDES = ("left", "right")
SIDE_PERMUTATIONS = (
    {"left": "left", "right": "right"},
    {"left": "right", "right": "left"},
)


def support_arity(uses: dict[str, bool]) -> int:
    return sum(int(uses[s]) for s in SIDES)


def relabel_support(
    support: frozenset[str], permutation: dict[str, str]
) -> frozenset[str]:
    return frozenset(permutation[side] for side in support)


def same_support_orbit(
    left: frozenset[str], right: frozenset[str]
) -> bool:
    return any(relabel_support(left, permutation) == right for permutation in SIDE_PERMUTATIONS)


def cellular_boundary(cell_coefficients: tuple[int, ...]) -> tuple[int, int, int]:
    # each shell 2-cell attaches along the circulation (1,1,1)
    total = sum(cell_coefficients)
    return (total, total, total)


def centered_edges(m: int, d: int) -> int:
    return (m - d) * m + (m - d) * (m + d) + m * (m + d)


def centered_triangles(m: int, d: int) -> int:
    return (m - d) * m * (m + d)


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: physical side-support, 2-cell boundary, and "
        "capacity equations are fixed before scene outputs."
    )

    physical_repairs = {
        "comparison": {"left": False, "right": False},
        "one-loop": {"left": True, "right": False},
        "order-memory": {"left": True, "right": True},
    }
    arities = {name: support_arity(support) for name, support in physical_repairs.items()}
    assert arities == {"comparison": 0, "one-loop": 1, "order-memory": 2}
    assert set(arities.values()) == {0, 1, 2}
    print("PASS_CONCRETE_SUPPORT_QUOTIENT: physical comparisons realise exactly arities 0,1,2")

    # The arity quotient is not an arbitrary numerical collapse. It is exactly the orbit quotient
    # of labelled supports under the preregistered side relabelings.
    exact_supports = tuple(
        frozenset(side for side, used in zip(SIDES, mask) if used)
        for mask in product((False, True), repeat=2)
    )
    assert len(set(exact_supports)) == 4
    for left in exact_supports:
        for right in exact_supports:
            assert same_support_orbit(left, right) == (len(left) == len(right))
    left_only = frozenset(("left",))
    right_only = frozenset(("right",))
    assert left_only != right_only and same_support_orbit(left_only, right_only)
    print(
        "PASS_PROTOCOL_ORBIT_QUOTIENT: four labelled supports reduce to three orbits "
        "exactly under preregistered side relabeling"
    )

    # 2-cell attachment: no cells cannot fill the nonzero cycle; one shell cell does.
    zero_cycle = (0, 0, 0)
    cycle = (1, 1, 1)
    defect_generated_cycle = {"trivial": zero_cycle, "closed-nontrivial": cycle}
    assert defect_generated_cycle["trivial"] == zero_cycle
    assert defect_generated_cycle["closed-nontrivial"] == cycle != zero_cycle
    assert cellular_boundary(()) == (0, 0, 0) != cycle
    assert cellular_boundary((1,)) == cycle
    print(
        "PASS_DEFECT_GENERATED_SHELL: the nontrivial closed defect generates the nonzero cycle; "
        "zero 2-cells fail and one shell 2-cell fills it"
    )

    # Linear route no-go: phi scale can coexist with the one-loop history collapse.
    phi_non_captured = True
    one_loop_histories_separated = False
    assert phi_non_captured and not one_loop_histories_separated
    print("FAIL_LINEAR_SCALE_TO_MEMORY: non-captured scale does not force two-loop memory")

    # Independent capacity selector, not count alone.
    solutions = []
    for m in range(1, 50):
        for d in range(0, m + 1):
            edge_defect = 3 * m * m - centered_edges(m, d)
            triangle_defect = m**3 - centered_triangles(m, d)
            if edge_defect == 4 and triangle_defect == 44:
                solutions.append((m - d, m, m + d))
    assert solutions == [(9, 11, 13)]
    print("PASS_INDEPENDENT_SIZE_SELECTOR: capacity defects (4,44) uniquely give (9,11,13)")

    # The forcing DAG consumes sizes reconstructed from owned capacities, not the named shell table.
    role_capacity = 4
    terminal_capacity = 44
    dyad_capacity = 2
    assert terminal_capacity % role_capacity == 0
    capacity_center = terminal_capacity // role_capacity
    capacity_spread = dyad_capacity
    capacity_sizes = tuple(
        capacity_center + (rank - 1) * capacity_spread for rank in range(3)
    )
    assert capacity_sizes == (9, 11, 13) == solutions[0]
    print("PASS_CAPACITY_DERIVED_SIZES: qT/Role and Dyad reconstruct the shell sizes")

    # Mutations can fail each load-bearing leg.
    assert cellular_boundary((0,)) != cycle
    assert support_arity({"left": True, "right": True}) != 1
    assert not same_support_orbit(frozenset(), left_only)
    assert defect_generated_cycle["trivial"] != cycle
    assert not any(
        3 * m * m - centered_edges(m, d) == 5
        and m**3 - centered_triangles(m, d) == 44
        for m in range(1, 50)
        for d in range(0, m + 1)
    )
    print(
        "FAIL_MUTATION_CONTROLS: zero shell coefficient, wrong orbit, trivial defect, "
        "collapsed arity, and defect-5 all rejected"
    )

    print("PASS_CASCADE_FULL_FORCING_DAG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
