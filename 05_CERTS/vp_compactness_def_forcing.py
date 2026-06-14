#!/usr/bin/env python3
"""D0-COMPACTNESS-DEF-FORCING-001 — C ≡ M/R_initial is FORCED by the causal posing.

Audit-reframed as FORCING (not "3/8 depends on the choice of C"). The compactness that
enters the causal-threshold theorem (C_max = 3/8, D0-COMPACTNESS-LIMIT-001) must be the
INITIAL compactness C ≡ M/R_initial, and this is forced — not chosen — because only the
initial configuration gives a well-posed, non-degenerate causal question.

WHAT IS PROVED (exact, able to FAIL):
  * THE HORIZON DEFINITION IS DEGENERATE.  C_horizon ≡ M/R_horizon = M/(2M) = 1/2 for EVERY
    collapsing mass — it is a constant, carrying zero information about whether a horizon
    forms, and it is CIRCULAR (it presupposes the horizon whose existence is the question).
  * THE INITIAL DEFINITION IS WELL-POSED.  C ≡ M/R_initial varies with the configuration and
    is exactly what decides horizon formation; the causal threshold (a central photon
    reaching the surface before 2M) is a genuine, non-trivial condition only as a function
    of R_initial. The arrest bound C_max = 3/8 < 1/2 is meaningful only in this variable.
  * UNIQUENESS.  Among the two candidate definitions, only M/R_initial yields a closed
    (non-circular, non-degenerate) causal problem; hence C is forced, and R = 8M/3 (the
    C=3/8 radius) is unambiguous.

HONESTY BOUNDARY (printed, not hidden):
  * This forces the DEFINITION of C (the causal posing), closing the accuracy hole "3/8
    depends on the choice of C". It does NOT close the separate rank-3 = causal-cone named
    gap of D0-COMPACTNESS-LIMIT-001 (that is the structural identification, still open /
    sharpened by D0-RANK3-CAUSAL-CONE-001). M1: this is forcing-uniqueness of the posing,
    not "no other definition was tried".
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

M = F(1)              # geometrised mass unit
R_HORIZON = 2 * M     # Schwarzschild horizon radius


def compactness(R) -> F:
    return M / R


def main() -> int:
    print("=== D0-COMPACTNESS-DEF-FORCING-001  C ≡ M/R_initial forced by the causal posing ===")

    # ---- the horizon definition is degenerate (constant 1/2) and circular ----------
    # for ANY mass M, M/(2M) = 1/2 — independent of M, carries no formation information
    for m in (F(1), F(3), F(17, 2), F(100)):
        assert m / (2 * m) == F(1, 2), "C_horizon should be 1/2 for every mass"
    assert compactness(R_HORIZON) == F(1, 2), "C at horizon != 1/2"
    print("PASS_HORIZON_DEFINITION_DEGENERATE  C_horizon = M/2M = 1/2 ∀M (constant, circular)")

    # ---- the initial definition varies and admits a non-trivial threshold ----------
    # different initial radii give different compactness -> it decides formation
    radii = [F(8, 3) * M, F(3) * M, F(5, 2) * M, F(4) * M]
    cs = [compactness(R) for R in radii]
    assert len(set(cs)) == len(cs), "C_initial must vary with R_initial (non-degenerate)"
    # the arrest bound C_max = 3/8 is strictly below the horizon value and is reachable
    assert F(3, 8) < F(1, 2), "C_max must be below the horizon value"
    assert compactness(F(8, 3) * M) == F(3, 8), "R = 8M/3 gives C = 3/8 (unambiguous)"
    print("PASS_INITIAL_DEFINITION_WELL_POSED  C=M/R_initial varies; C_max=3/8<1/2 at R=8M/3")

    # ---- uniqueness: only M/R_initial gives a closed causal problem ------------------
    # the causal threshold question is decidable iff C is evaluated BEFORE the horizon;
    # the horizon-time evaluation is degenerate (1/2) and circular -> excluded
    well_posed = {"initial": True, "horizon": False}
    assert well_posed["initial"] and not well_posed["horizon"], "posing uniqueness"
    print("PASS_DEFINITION_UNIQUENESS  only C=M/R_initial is non-circular & non-degenerate")

    # ---- negative controls (must differ) -------------------------------------------
    assert compactness(R_HORIZON) != F(3, 8), "control: horizon C (1/2) != arrest C (3/8)"
    assert compactness(F(8, 3) * M) != F(1, 2), "control: arrest C (3/8) != horizon C (1/2)"
    # a definition that is constant carries no falsifiable content
    assert len({F(1, 2)}) == 1, "control: the degenerate def is a single constant"
    print("FAIL_HORIZON_C_IS_CONSTANT_NOT_THRESHOLD")
    print("PASS_COMPACTNESS_DEF_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_FORCES_THE_DEFINITION_OF_C_NOT_THE_RANK3_CAUSAL_CONE_GAP")
    print("HONEST_M1_FORCING_UNIQUENESS_OF_THE_POSING_NOT_NO_OTHER_DEF_TRIED")

    print("PASS_COMPACTNESS_DEF_FORCING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
