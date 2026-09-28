#!/usr/bin/env python3
"""Exact finite operational-cut protocol pair.

This checker is deliberately finite and typed.  It compares two protocols over
the same joint carrier, actions, owner-facing verification record, archive
projection, witness lines, catalogue values, and comparator.  The only changed
primitive is the allowed transition relation.

Terminal:
    D0-OPERATIONAL-CUT-PROTOCOL-PAIR-EXACT
"""

from collections import deque
from dataclasses import dataclass
from enum import Enum


class Archive(str, Enum):
    NONE = "none"
    SAFE = "safe"
    EXPOSED = "exposed"


@dataclass(frozen=True)
class State:
    name: str
    has_enclosure: bool
    inside_enclosure: bool
    hazard_isolated: bool
    archive: Archive


@dataclass(frozen=True)
class Protocol:
    name: str
    transitions: frozenset[tuple[str, str, str]]


STATES = (
    State("exposed_none", False, False, False, Archive.NONE),
    State("carrying_none", True, False, False, Archive.NONE),
    State("safe_none", True, True, True, Archive.NONE),
    State("safe_recorded", True, True, True, Archive.SAFE),
    State("exposed_recorded", False, False, False, Archive.EXPOSED),
)
BY_NAME = {state.name: state for state in STATES}

ACTIONS = (
    "noop",
    "acquire_enclosure",
    "enter_and_isolate",
    "record_safe",
    "record_exposed",
)
ACTION_KIND = {
    "noop": "identity",
    "acquire_enclosure": "physical-cross-cut",
    "enter_and_isolate": "physical-cross-cut",
    "record_safe": "archive-write",
    "record_exposed": "archive-write",
}

LINES = ("line0", "line1")
CATALOGUES = ("catalogue0", "catalogue1")
CUTS = ("subject|apparatus", "subject+enclosure|hazard")

INITIAL = "exposed_none"
SAFE_TARGET = "safe_none"


def safe_state(state: State) -> bool:
    return state.inside_enclosure and state.hazard_isolated


def verification_record(state: State) -> tuple:
    """Owner-facing P.record analogue.

    It is injective on the declared State carrier, as required by the accepted
    verification contract.  The scenario's archive flag is only one component.
    """

    return (
        state.name,
        state.has_enclosure,
        state.inside_enclosure,
        state.hazard_isolated,
        state.archive.value,
    )


def archive_record(state: State) -> str:
    """Scenario-level archive projection, intentionally coarser than P.record."""

    return state.archive.value


def compare(_line: str, _catalogue: str, left: tuple, right: tuple) -> bool:
    """Catalogue-invariant exact comparison on owner-facing records."""

    return left != right


COMMON = {
    (state.name, "noop", state.name)
    for state in STATES
}
COMMON.add(("exposed_none", "record_exposed", "exposed_recorded"))

ALLOW_RELATION = frozenset(
    COMMON
    | {
        ("exposed_none", "acquire_enclosure", "carrying_none"),
        ("carrying_none", "enter_and_isolate", "safe_none"),
        ("safe_none", "record_safe", "safe_recorded"),
    }
)

BLOCK_RELATION = frozenset(COMMON)

ALLOW = Protocol("allow_transfer", ALLOW_RELATION)
BLOCK = Protocol("block_transfer", BLOCK_RELATION)


def reachable(protocol: Protocol, start: str) -> set[str]:
    seen = {start}
    queue = deque([start])
    while queue:
        source = queue.popleft()
        for src, _action, dst in protocol.transitions:
            if src == source and dst not in seen:
                seen.add(dst)
                queue.append(dst)
    return seen


def step(protocol: Protocol, source: str, action: str) -> str:
    destinations = sorted(
        dst
        for src, act, dst in protocol.transitions
        if src == source and act == action
    )
    assert len(destinations) == 1, (protocol.name, source, action, destinations)
    return destinations[0]


def verification_contract(protocol: Protocol) -> dict[str, bool]:
    records = [verification_record(state) for state in STATES]
    state_nontrivial = len(STATES) >= 2
    line_nontrivial = len(LINES) >= 2 and LINES[0] != LINES[1]
    catalogue_nonempty = len(CATALOGUES) >= 1
    record_injective = len(set(records)) == len(records)

    correct = True
    for line in LINES:
        for catalogue in CATALOGUES:
            for x in STATES:
                for y in STATES:
                    got = compare(
                        line,
                        catalogue,
                        verification_record(x),
                        verification_record(y),
                    )
                    if got != (x != y):
                        correct = False

    return {
        "state_nontrivial": state_nontrivial,
        "line_nontrivial": line_nontrivial,
        "catalogue_nonempty": catalogue_nonempty,
        "record_injective": record_injective,
        "correct": correct,
    }


def redescribe(state_name: str, cut: str) -> str:
    assert state_name in BY_NAME
    assert cut in CUTS
    return state_name


def print_tables() -> None:
    print("STATE_TABLE")
    print("name|has_enclosure|inside|hazard_isolated|archive|safe|verification_record")
    for state in STATES:
        print(
            f"{state.name}|{int(state.has_enclosure)}|{int(state.inside_enclosure)}|"
            f"{int(state.hazard_isolated)}|{state.archive.value}|{int(safe_state(state))}|"
            f"{verification_record(state)}"
        )

    print("ACTION_TABLE")
    print("action|kind")
    for action in ACTIONS:
        print(f"{action}|{ACTION_KIND[action]}")

    print("CUT_TABLE")
    print("state|cut|joint_state_after_redescription")
    for state in STATES:
        for cut in CUTS:
            print(f"{state.name}|{cut}|{redescribe(state.name, cut)}")

    for protocol in (ALLOW, BLOCK):
        print(f"TRANSITION_TABLE {protocol.name}")
        print("source|action|target")
        for src, action, dst in sorted(protocol.transitions):
            print(f"{src}|{action}|{dst}")

    print("ARCHIVE_TABLE")
    print("state|archive_record|safe")
    for state in STATES:
        print(f"{state.name}|{archive_record(state)}|{int(safe_state(state))}")


def main() -> None:
    # Same carrier, action type, record maps, witness lines and comparator.
    assert ALLOW.name != BLOCK.name
    assert set(ALLOW.transitions) != set(BLOCK.transitions)
    assert tuple(BY_NAME) == tuple(state.name for state in STATES)
    assert len(set(ACTIONS)) == len(ACTIONS)
    assert len(set(verification_record(state) for state in STATES)) == len(STATES)

    allow_contract = verification_contract(ALLOW)
    block_contract = verification_contract(BLOCK)
    assert allow_contract == block_contract
    assert all(allow_contract.values())

    print("PASS_SAME_VERIFICATION_CONTRACT", allow_contract)
    print("PASS_SAME_CARRIER_ACTION_RECORD_AND_COMPARATOR")

    # Exact allowed-transition witness.
    s1 = step(ALLOW, INITIAL, "acquire_enclosure")
    s2 = step(ALLOW, s1, "enter_and_isolate")
    assert s1 == "carrying_none"
    assert s2 == SAFE_TARGET
    assert safe_state(BY_NAME[s2])
    print("PASS_ALLOW_SAFE_PATH", (INITIAL, s1, s2))

    # Same safe state exists in the carrier but is unreachable without the two
    # physical transition edges.
    allow_reach = reachable(ALLOW, INITIAL)
    block_reach = reachable(BLOCK, INITIAL)
    assert SAFE_TARGET in allow_reach
    assert SAFE_TARGET not in block_reach
    assert BY_NAME[SAFE_TARGET] in STATES
    print("PASS_DIFFERENT_REACHABILITY")
    print("ALLOW_REACHABLE", sorted(allow_reach))
    print("BLOCK_REACHABLE", sorted(block_reach))

    # Changing only the cut label is a re-description of one joint state.
    for state in STATES:
        a = redescribe(state.name, CUTS[0])
        b = redescribe(state.name, CUTS[1])
        assert a == b == state.name
    assert step(ALLOW, INITIAL, "acquire_enclosure") != INITIAL
    print("PASS_CUT_REDESCRIPTION_IS_NOT_STATE_TRANSITION")

    # Absence of a scenario archive record does not determine safety.
    safe_none = BY_NAME["safe_none"]
    exposed_none = BY_NAME["exposed_none"]
    assert archive_record(safe_none) == archive_record(exposed_none) == Archive.NONE.value
    assert safe_state(safe_none)
    assert not safe_state(exposed_none)
    print("PASS_NO_ARCHIVE_RECORD_DOES_NOT_IMPLY_SAFE_OR_DANGER")

    # Hostile label mutation: relabeling one state as "safe" changes no
    # operational map.  The label therefore cannot manufacture an
    # identification.
    hostile_safe_label = {state.name: safe_state(state) for state in STATES}
    hostile_safe_label["exposed_none"] = True
    assert hostile_safe_label["exposed_none"] != safe_state(exposed_none)
    assert verification_record(exposed_none) == verification_record(BY_NAME["exposed_none"])
    assert archive_record(exposed_none) == Archive.NONE.value
    print("PASS_HOSTILE_SAFE_LABEL_HAS_NO_OPERATIONAL_EFFECT")

    # The exact Popperian owner constrains nontriviality, two lines, a runnable
    # catalogue and comparator correctness.  Both protocols satisfy those same
    # predicates while their transition relations differ.
    assert all(verification_contract(protocol).values() for protocol in (ALLOW, BLOCK))
    assert ALLOW.transitions != BLOCK.transitions
    print("PASS_VERIFICATION_CONTRACT_DOES_NOT_FIX_TRANSITION_RELATION")

    print_tables()

    print("D0-OPERATIONAL-CUT-PROTOCOL-PAIR-EXACT")
    print(
        "STATE_REACHABILITY: safe_none is reachable only in allow_transfer; "
        "block_transfer lacks the required physical edges."
    )
    print(
        "RECORDED_KNOWLEDGE: archive='none' occurs on both safe and exposed states; "
        "absence of that archive record implies neither safety nor danger."
    )
    print(
        "ORTHOGONALITY_SCOPE: no density operators or measurement effects are "
        "defined here; D0-VERIFIABLE-REGISTRATION-ORTHOGONALITY-001 is therefore "
        "only a typed boundary, not an extra transition constraint."
    )


if __name__ == "__main__":
    main()
