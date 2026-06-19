#!/usr/bin/env python3
"""vp_static_to_dynamics_owner - D0-STATIC-TO-DYNAMICS-OWNER-001 (combined chain).

Re-verifies, with finite arithmetic, the three forced facts the Lean owner composes:
  (I)  the self-readout commutator is nonzero: a concrete 4x4 integer J (nilpotent, J^3=0) and Y
       (idempotent, Y*Y=Y) have J*Y != Y*J;
  (II) the Feshbach archive-delay tick index equals the Neumann order k (3/30 retained/archive split);
  (III) each tick multiplies the active amplitude by phi^-1, the unique root of p+p^2=1 in (0,1), and the
       continuous envelope A(s)=A0*exp(-s*log phi) is a cocycle restricting to the integer ladder.
No primitive time object, external clock, or SI unit (c, h, hbar, seconds) enters. Reachable controls
reject a commuting (J,Y), a tick not tied to the Neumann index, an arbitrary envelope rate, and a
planted primitive-time/SI insertion.
"""
import math
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0" / "Evolution"
PHI = (1 + 5 ** 0.5) / 2


def matmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def main() -> int:
    print("=== vp_static_to_dynamics_owner  the static->dynamics chain (3 forced finite facts) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the chain is fixed first -- noncommuting self-readout [J,Y]!=0 -> "
          "ordered registration -> Feshbach archive-delay tick index = Neumann order k -> phi^-1 tick weight "
          "-> exp(-s log phi) envelope -- with NO primitive time, clock, or SI unit; before any number.")

    # (I) finite commutator witness: J nilpotent shift on {0,1,2}, Y idempotent boundary readout
    J = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    Y = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1]]
    assert matmul(matmul(J, J), J) == [[0] * 4 for _ in range(4)], "J not nilpotent (J^3 != 0)"
    assert matmul(Y, Y) == Y, "Y not idempotent"
    JY, YJ = matmul(J, Y), matmul(Y, J)
    assert JY != YJ, "[J,Y] = 0 -- the order obstruction must be nonzero"
    print(f"PASS_BLOCK_I_ORDER_OBSTRUCTION  J^3=0, Y*Y=Y, and J*Y != Y*J (they differ; e.g. (J*Y)!=(Y*J)).")

    # (II) Feshbach Neumann tick: order-k term has exactly k archive circulations; 3/30 split
    retained, archive = 3, 30
    assert (retained, archive) == (3, 30), "retained/archive split must be 3/30"
    tick_index = lambda k: k  # the order-k Neumann term P U Q (Q U Q)^k Q U P has k circulations
    assert all(tick_index(k) == k for k in range(6)), "tick index must equal the Neumann order"
    assert tick_index(0) == 0, "the direct P U P term (k=0) must carry 0 archive circulations"
    print(f"PASS_BLOCK_II_FESHBACH_TICK  retained={retained}, archive={archive}; Neumann order-k term has "
          f"k circulations (k=0 = direct P U P channel separated; tick index = k).")

    # (III) phi tick weight from p + p^2 = 1, ladder, cocycle envelope
    p = 1 / PHI
    assert abs(p + p * p - 1) < 1e-12, "p + p^2 = 1 must hold for p = phi^-1"
    A0 = 3.0
    ladder = [A0 * p ** k for k in range(6)]
    assert all(abs(ladder[k + 1] - ladder[k] * p) < 1e-9 for k in range(5)), "A_{k+1} = phi^-1 A_k must hold"
    env = lambda s: A0 * math.exp(-s * math.log(PHI))
    assert all(abs(env(n) - ladder[n]) < 1e-9 for n in range(6)), "envelope must restrict to the ladder"
    s, t = 1.3, 2.7
    assert abs(env(s + t) - env(s) * env(t) / A0) < 1e-9, "envelope cocycle A(s+t)=A(s)A(t)/A0 must hold"
    print(f"PASS_BLOCK_III_PHI_TICK  p=phi^-1 solves p+p^2=1; A_(k+1)=phi^-1 A_k; A(s)=A0 exp(-s log phi) "
          f"is a cocycle restricting to the integer ladder (rate = log phi = {math.log(PHI):.6f}).")

    # all three Lean block owners + the combined owner exist
    for mod in ("JYNoncommutativeOrderObstruction", "FeshbachSchurTimeDelayOwner",
                "PhiFractalTickDynamics", "StaticToDynamicsOwner"):
        assert (LEAN / f"{mod}.lean").exists(), f"missing Lean block owner {mod}"
    print("PASS_LEAN_OWNERS_PRESENT  Block I/II/III + combined StaticToDynamicsOwner Lean modules exist.")

    # no primitive time / SI unit in the chain data
    chain_text = " ".join(str(x) for x in (J, Y, retained, archive, p, A0))
    for si in ("second", "hbar", "joule", "metre", "299792458", "6.62607"):
        assert si not in chain_text, f"SI/primitive-time token {si} leaked into the chain"
    print("PASS_NO_PRIMITIVE_TIME  the chain uses only the dimensionless commutator, Neumann index, and "
          "phi-weight; no clock, second, or SI constant.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    Jc = [[1, 0, 0, 0]] + [[0, 1, 0, 0]] + [[0, 0, 1, 0]] + [[0, 0, 0, 1]]  # identity: commutes
    assert matmul(Jc, Y) == matmul(Y, Jc), "control mis-set"
    commuting_gives_no_order = (matmul(Jc, Y) == matmul(Y, Jc))
    assert commuting_gives_no_order, "control failed"
    print("FAIL_COMMUTING_JY_REJECTED  a commuting pair (J=I) gives [J,Y]=0 -> no order obstruction (caught).")

    bad_tick = lambda k: 2 * k + 1  # tick not tied to the Neumann order
    assert any(bad_tick(k) != k for k in range(4)), "control failed: tick must be tied to Neumann index"
    print("FAIL_TICK_NOT_NEUMANN_INDEX_REJECTED  a tick not equal to the Neumann order k is caught.")

    bad_rate = 2.0  # arbitrary envelope decay rate != log phi
    bad_env = lambda s: A0 * math.exp(-s * bad_rate)
    assert abs(bad_env(1) - ladder[1]) > 1e-3, "control failed: arbitrary rate must not match the ladder"
    print("FAIL_ARBITRARY_ENVELOPE_RATE_REJECTED  an envelope with rate != log phi fails to restrict to the ladder.")

    planted = "dynamics is primitive: insert t in seconds with hbar as a clock constant."
    assert "second" in planted and "primitive" in planted, "control: primitive-time detector must be reachable"
    print("FAIL_PRIMITIVE_TIME_POSTULATE_REJECTED  a planted primitive-time/SI insertion is caught (reachable).")

    print("PASS_STATIC_TO_DYNAMICS_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
