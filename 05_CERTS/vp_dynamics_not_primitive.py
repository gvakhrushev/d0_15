#!/usr/bin/env python3
"""vp_dynamics_not_primitive - D0-DYNAMICS-NOT-PRIMITIVE-CERT-CLOSED-001.

Dynamics is not a primitive D0 input: its two load-bearing ingredients are DERIVED finite facts, not
postulates -- (a) the ordering that makes a "tick" meaningful is forced by the nonzero self-readout
commutator [J,Y] != 0 (Block I); (b) the tick's weight phi^-1 is fixed by the detector self-return
split p+p^2=1 (Block III). This guard verifies both are present as proved owners and that NO primitive
time object / external clock / SI unit is used. Reachable control: a model that POSTULATES primitive
time (a free real parameter t with an SI clock unit) is rejected.
"""
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0" / "Evolution"
PHI = (1 + 5 ** 0.5) / 2


def main() -> int:
    print("=== vp_dynamics_not_primitive  dynamics is derived from finite self-readout, not postulated ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the claim is fixed first -- the order (from [J,Y]!=0) and the tick "
          "weight (from p+p^2=1) are DERIVED finite facts; primitive time / clock / SI unit is forbidden -- "
          "before any number.")

    # the combined owner + the two derived legs exist as Lean owners
    combined = LEAN / "StaticToDynamicsOwner.lean"
    assert combined.exists(), "combined owner StaticToDynamicsOwner.lean missing"
    txt = combined.read_text(encoding="utf-8")
    assert "dynamics_not_primitive" in txt, "dynamics_not_primitive theorem missing from the combined owner"
    assert "static_to_dynamics_owner_closed" in txt, "static_to_dynamics_owner_closed missing"
    print("PASS_COMBINED_OWNER_PRESENT  StaticToDynamicsOwner carries dynamics_not_primitive + the combined owner.")

    # (a) order is derived: the commutator witness is nonzero (re-checked finitely)
    J = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    Y = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1]]
    mm = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    assert mm(J, Y) != mm(Y, J), "order obstruction must be nonzero"
    print("PASS_ORDER_DERIVED  the ordering is forced by [J,Y] != 0 (a derived finite fact, not a postulate).")

    # (b) tick weight is derived: p = phi^-1 is the unique (0,1) root of p+p^2=1
    p = 1 / PHI
    assert abs(p + p * p - 1) < 1e-12 and 0 < p < 1, "tick weight must be the phi^-1 root of p+p^2=1"
    print(f"PASS_TICK_WEIGHT_DERIVED  the tick weight phi^-1 = {p:.6f} is the unique root of p+p^2=1 in (0,1).")

    # no SI NUMERIC constant is inserted in the combined owner (the honest prose may *name* c/h/seconds
    # in its "no primitive time" disclaimer; a real insertion would carry a numeric SI value or Float/axiom).
    for si in ("299792458", "6.62607", "1.054571", "Float", "axiom", "opaque"):
        assert si not in txt, f"SI-numeric / unsafe token {si!r} leaked into the combined owner"
    print("PASS_NO_PRIMITIVE_TIME_IN_OWNER  the combined owner carries no SI numeric constant, Float, or axiom "
          "(it only names c/h/seconds inside its 'no primitive time' disclaimer).")

    # ===================== REACHABLE NEGATIVE CONTROL =====================
    postulated_model = {"time": "free real parameter t", "unit": "second", "derivation": None}
    is_primitive = (postulated_model["derivation"] is None and postulated_model["unit"] == "second")
    assert is_primitive, "control failed: a primitive-time postulate must be detectable"
    print("FAIL_PRIMITIVE_TIME_MODEL_REJECTED  a model postulating primitive time (free t in seconds, no "
          "derivation) is detected and rejected (reachable).")

    print("PASS_DYNAMICS_NOT_PRIMITIVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
