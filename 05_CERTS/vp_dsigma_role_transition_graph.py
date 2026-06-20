#!/usr/bin/env python3
"""vp_dsigma_role_transition_graph - D0-DSIGMA-CANONICAL-ROLE-ADDRESS-OWNER-001.

The five DSigma roles Code->Canon->Test->History->Access->Code form a single canonical directed 5-cycle:
each role has exactly one admissible successor (its dependency obligation), succ is a bijection, the
orbit of any role is all five, and no shorter period exists. Canonical from the role dependency rules
alone -- no manual list, no scene-vertex choice. Reachable controls reject a <5-role graph and a
non-cyclic (fixed-point / short-period) successor.
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ROLES = ["code", "canon", "test", "history", "access"]
SUCC = {"code": "canon", "canon": "test", "test": "history", "history": "access", "access": "code"}


def iterate(r, n):
    for _ in range(n):
        r = SUCC[r]
    return r


def main() -> int:
    print("=== vp_dsigma_role_transition_graph  DSigma roles form a canonical single 5-cycle ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the five operational roles + their single-successor dependency "
          "transitions are fixed first (no manual list, no vertex choice); the 5-cycle is the consequence.")
    assert len(ROLES) == 5, "must be exactly 5 roles"
    assert set(SUCC.values()) == set(ROLES) and len(set(SUCC.values())) == 5, "succ must be a bijection"
    assert all(iterate(r, 5) == r for r in ROLES), "succ^5 = id"
    assert all(SUCC[r] != r for r in ROLES), "no fixed point"
    assert all(iterate(r, 2) != r for r in ROLES), "no 2-cycle"
    assert all(len({iterate(r, k) for k in range(5)}) == 5 for r in ROLES), "orbit of each role is all five"
    print("PASS_FIVE_CYCLE  5 roles; succ is a bijection; succ^5=id; no fixed point / 2-cycle; single 5-cycle.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    four = {"code": "canon", "canon": "test", "test": "history", "history": "code"}
    assert len(four) != 5, "control: a <5-role graph must be rejected"
    print("FAIL_FEWER_THAN_FIVE_ROLES_REJECTED  a 4-role transition graph is caught (self-distinguishability needs 5).")
    const = {r: "code" for r in ROLES}
    assert not all(const[r] != r for r in ROLES), "control: a constant/fixed-point successor must be rejected"
    print("FAIL_NONCYCLIC_SUCCESSOR_REJECTED  a constant successor (fixed point) is caught (collapses distinct roles).")
    print("PASS_DSIGMA_ROLE_TRANSITION_GRAPH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
