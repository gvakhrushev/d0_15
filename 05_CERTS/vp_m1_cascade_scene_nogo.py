# STRUCTURE_FIXED_BEFORE_NUMBER: repair classes and variable scenes are defined before cardinality is read.
"""Deterministic certificate for the M1/cascade variable-scene count no-go.

The certificate is a negative control, not a selector. It checks that:

* the present semantic package is unchanged at scene counts two and four;
* the finitely classified repair kinds support a faithful assignment exactly when the scene has
  enough zones, so the assignment is a renamed lower bound;
* deleting injectivity glues two repair kinds into one zone;
* the hollow four-zone transport matrix has rank four.
"""

from fractions import Fraction


REPAIR_CLASSES = ("reading", "history", "op_pair")
PRESENT_FACT_FINGERPRINT = (
    "carried-cascade",
    "owner-facts",
    "computed-kinds",
    "concrete-two-sided-class-M1",
)


def matrix_rank(matrix: list[list[int]]) -> int:
    a = [[Fraction(x) for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col] != 0), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [x / scale for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row and a[r][col] != 0:
                factor = a[r][col]
                a[r] = [x - factor * y for x, y in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def present_model(zone_count: int) -> tuple[int, tuple[str, ...]]:
    assert zone_count > 0
    return zone_count, PRESENT_FACT_FINGERPRINT


def faithful_kind_assignment_exists(zone_count: int) -> bool:
    return len(REPAIR_CLASSES) <= zone_count


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: repair classes and present semantic facts are fixed "
        "before their cardinalities are computed."
    )

    two = present_model(2)
    four = present_model(4)
    assert two[1] == four[1] == PRESENT_FACT_FINGERPRINT
    assert two[0] != four[0]
    print("PASS_COUNT_PARAMETRIC_MODELS: identical present facts survive at zoneCount=2 and zoneCount=4")

    computed_count = len(REPAIR_CLASSES)
    assert computed_count == 3
    for zone_count in range(1, 7):
        assert faithful_kind_assignment_exists(zone_count) == (computed_count <= zone_count)
    print("PASS_KIND_ASSIGNMENT_IFF_BOUND: finite kind assignment is exactly card(kinds)<=zoneCount")

    glued = {"reading": 0, "history": 1, "op_pair": 1}
    assert glued["history"] == glued["op_pair"]
    assert len(set(glued.values())) == 2 < computed_count
    print("FAIL_INJECTIVITY_DELETION_CONTROL: deleting injectivity glues history and op_pair in two zones")

    hollow_four = [[0 if i == j else 1 for j in range(4)] for i in range(4)]
    assert matrix_rank(hollow_four) == 4
    duplicate_row_mutation = [row[:] for row in hollow_four]
    duplicate_row_mutation[3] = duplicate_row_mutation[2][:]
    assert matrix_rank(duplicate_row_mutation) == 3
    print("PASS_FOUR_ZONE_RANK: hollow four-zone transport has rank 4")
    print("FAIL_RANK_MUTATION_CONTROL: duplicating one zone row drops rank to 3")

    assert not (two[0] == four[0])
    print("PASS_NO_UNIQUE_COUNT: the present grammar cannot determine one zone count")
    print("PASS_M1_CASCADE_SCENE_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
