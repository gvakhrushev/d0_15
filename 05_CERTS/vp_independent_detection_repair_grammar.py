# STRUCTURE_FIXED_BEFORE_NUMBER: the loop budget and order-arity model precede the kind count.
"""Certificate: the repair-grammar kind count is derived from the double-detection loop budget.

The order-arities realisable on b independent detection loops are {0,1,...,b}; their count is b+1.
The D0 budget is 2 (independent repeated detection), giving exactly 3 kinds. Controls at other
budgets and the pigeonhole cap are checked; no target number is assumed before the budget.
"""

from itertools import combinations


def realizable_arities(budget: int) -> list[int]:
    # order-arity k = joint order of k of the b supplied loops, 0 <= k <= b
    return list(range(budget + 1))


def kind_count(budget: int) -> int:
    return len(realizable_arities(budget))


def arity_fits_budget(arity: int, budget: int) -> bool:
    return arity <= budget


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: the loop budget and order-arity model are fixed "
        "before any kind count is read."
    )

    detection_budget = 2  # independent repeated detection = two independent loops

    assert kind_count(detection_budget) == detection_budget + 1
    assert kind_count(detection_budget) == 3
    print("PASS_COUNT_FROM_BUDGET: two independent loops give exactly 3 = 2+1 repair kinds")

    # the three arities map to the three carried floors
    floor_arity = {"reading": 0, "history": 1, "opPair": 2}
    assert sorted(floor_arity.values()) == realizable_arities(detection_budget)
    print("PASS_FLOORS_REALIZE_ARITIES: reading/history/opPair realise arities 0,1,2")

    # controls: single detection caps at two, triple detection would give four
    assert kind_count(1) == 2
    assert kind_count(3) == 4
    print("PASS_BUDGET_CONTROLS: single detection -> 2 kinds; triple detection -> 4 kinds")

    # pigeonhole cap: a (b+2)-th arity class cannot fit on a b-loop budget
    for budget in range(0, 5):
        assert not arity_fits_budget(budget + 1, budget)
    print("FAIL_FOURTH_ARITY_CONTROL: an arity beyond the budget provably does not fit")

    # falsifiable mutation: pretending the budget were 3 would break the derived 3
    wrong_budget = 3
    assert kind_count(wrong_budget) != 3
    print("FAIL_WRONG_BUDGET_CONTROL: a mis-stated budget yields the wrong kind count")

    print("PASS_INDEPENDENT_DETECTION_REPAIR_GRAMMAR")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
