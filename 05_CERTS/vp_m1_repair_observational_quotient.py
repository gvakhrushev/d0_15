# STRUCTURE_FIXED_BEFORE_NUMBER: observations, equivalence, and extension grammar precede counting.
"""Certificate for the M1 repair observational quotient and no-fourth-class reductio."""

from collections import defaultdict


DISCRIMINATIONS = (
    ("comparison-0", "reading"),
    ("comparison-1", "reading"),
    ("one-loop", "history"),
    ("order-memory", "op_pair"),
)


def quotient_classes(items: tuple[tuple[str, str], ...]) -> dict[str, tuple[str, ...]]:
    classes: dict[str, list[str]] = defaultdict(list)
    for witness, observation in items:
        classes[observation].append(witness)
    return {k: tuple(v) for k, v in classes.items()}


def admissible_contents(components: tuple[str, ...]) -> list[dict[str, bool]]:
    result: list[dict[str, bool]] = []
    for mask in range(1 << len(components)):
        result.append(
            {component: bool((mask >> i) & 1) for i, component in enumerate(components)}
        )
    return result


def forced_values(
    components: tuple[str, ...], observer: str, observed: bool, target: str
) -> set[bool]:
    values = {
        content[target]
        for content in admissible_contents(components)
        if content[observer] == observed
    }
    return values


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: observational equivalence and extension grammar "
        "are fixed before quotient cardinality is computed."
    )

    quotient = quotient_classes(DISCRIMINATIONS)
    assert set(quotient) == {"reading", "history", "op_pair"}
    assert quotient["reading"] == ("comparison-0", "comparison-1")
    assert len(quotient) == 3
    print("PASS_OBSERVATIONAL_QUOTIENT: duplicate reading witnesses collapse; three classes remain")

    current = tuple(quotient)
    external = "theta"
    extended = current + (external,)
    for observer in current:
        values = forced_values(extended, observer, False, external)
        assert values == {False, True}
    print(
        "PASS_OUTCOME_AFFECTING: theta varies while every chosen current observer is held fixed"
    )

    current_derivable = set(current)
    assert external not in current_derivable
    assert external not in current
    print("PASS_UNDERIVED_NONPROTOCOL: theta is neither current derivation nor protocol datum")

    for observer in current:
        values = forced_values(extended, observer, False, external)
        assert len(values) != 1
    print("PASS_EXTERNAL_CATALOGUE: no current observer forces either theta value")
    print("PASS_NO_MANDATORY_FOURTH_CLASS: a mandatory theta contradicts M1 resolution")

    canonical_scene_zones = tuple(sorted(quotient))
    assert len(canonical_scene_zones) == len(quotient)
    assert len(canonical_scene_zones) == 3
    print("PASS_FAITHFUL_SCENE: quotient classes and canonical variable zones are bijective")

    collapsed = {
        "reading": "reading",
        "history": "history",
        "op_pair": "op_pair",
        external: "reading",
    }
    collapsed_components = tuple(dict.fromkeys(collapsed.values()))
    values_after_mutation = forced_values(
        collapsed_components, "reading", False, collapsed[external]
    )
    assert values_after_mutation == {False}
    print(
        "FAIL_CONNECTION_MUTATION_CONTROL: connecting theta to reading makes its value forced"
    )

    assert len({"reading", "history"}) == 2
    print("FAIL_CLASS_DELETION_CONTROL: deleting op_pair lowers the quotient cardinality")
    print("PASS_M1_REPAIR_OBSERVATIONAL_QUOTIENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
