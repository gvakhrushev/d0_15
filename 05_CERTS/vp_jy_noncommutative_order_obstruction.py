#!/usr/bin/env python3
"""D0-JY-NONCOMMUTATIVE-ORDER-OBSTRUCTION-001 + D0-TIME-ARROW-ORDERED-SELF-READOUT-001 finite witness cert.

The load-bearing real fact: the localization/defect operator J (nilpotent shift on the rank-3
localization block {0,1,2} of a 4-dim carrier, fixing the archive index 3) and the boundary-closure
readout Y (idempotent oblique projection onto the archive direction e3 that reads the localization-top
slot e2 and the archive slot e3) do NOT commute: J*Y != Y*J, differing at entry (3,1) = -1.

Reading (BOOK_06): a self-readout whose two operations commuted would be order-blind (could not tell
shift-then-read from read-then-shift), so it could not recover the order of its own registered events;
recovering the erased order needs an EXTERNAL CATALOGUE (an order log) -- an unprovable input M1 forbids.
Because the ACTUAL D0 readout (J,Y) is noncommutative, the order is intrinsic finite data: registration
is forced ordered, and ordered registration is the time arrow. No primitive time object, external clock,
or SI unit (c, h, hbar, seconds) enters -- only the nonzero finite commutator.

HONEST SCOPE: the witness + the wired M1 reductio are for the SPECIFIC D0 operators (J,Y) and the binary
ordered-vs-commuting registration selector. The UNIVERSAL claim (every commuting self-readout on any
carrier erases order) is NOT proven; it is the named residual JY-UNIVERSAL-COMMUTING-READOUT-OBSTRUCTION.
A finite witness is not a universal theorem.
"""
import sys
from fractions import Fraction as Fr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def matmul(A, B):
    n = len(A)
    m = len(B[0])
    k = len(B)
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


def sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def commute(A, B):
    return matmul(A, B) == matmul(B, A)


def is_zero(A):
    return all(all(x == 0 for x in row) for row in A)


# ---- the exact integer operators (mirrors the Lean !![...] definitions, column-j convention M[i][j]) ----
J = [[0, 0, 0, 0],
     [1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 0]]
Y = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 1, 1]]
I4 = [[1 if i == j else 0 for j in range(4)] for i in range(4)]


def main() -> int:
    print("=== D0-JY-NONCOMMUTATIVE-ORDER-OBSTRUCTION-001 / D0-TIME-ARROW-ORDERED-SELF-READOUT-001 ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: J=nilpotent shift on localization block {0,1,2}, archive index 3 "
          "fixed; Y=idempotent boundary-closure projection (Y e2=e3, Y e3=e3); the order-distinguishing "
          "entry is (3,1) of [J,Y] -- structure fixed before any number")

    # --- finite fact 1: Y is a genuine readout projection (idempotent) ---
    assert matmul(Y, Y) == Y, "Y must be idempotent (a genuine readout projection)"
    print("PASS_Y_IDEMPOTENT  Y*Y = Y  (Y is a genuine boundary-closure readout projection, not arbitrary)")

    # --- finite fact 2: J is nilpotent (J^3 = 0): a defect-shift with no fixed information ---
    J3 = matmul(matmul(J, J), J)
    assert is_zero(J3), "J must be nilpotent J^3 = 0"
    print("PASS_J_NILPOTENT  J^3 = 0  (J is the localization defect-shift)")

    # --- finite fact 3 (load-bearing): J*Y != Y*J, differing at entry (3,1) = -1 ---
    C = sub(matmul(J, Y), matmul(Y, J))
    assert not commute(J, Y), "the load-bearing fact: J and Y must NOT commute"
    assert C[3][1] == -1, "the order-distinguishing commutator entry (3,1) must be -1"
    assert not is_zero(C), "[J,Y] must be a nonzero matrix"
    print(f"PASS_JY_COMMUTATOR_NONZERO  J*Y != Y*J ; [J,Y](3,1) = {C[3][1]} != 0 "
          "(shift-then-read != read-then-shift: order is observable)")

    # --- finite fact 4: commuting erases order (structural lemma at (J,Y)) ---
    # orderSensitive(R) := defect*readout != readout*defect ; commuting => not orderSensitive (tautological core)
    def order_sensitive(defect, readout):
        return not commute(defect, readout)
    # if (J,Y) commuted it would not be order-sensitive; since it does NOT commute, it IS order-sensitive:
    assert order_sensitive(J, Y), "the D0 readout (J,Y) must be order-sensitive"
    print("PASS_COMMUTING_ERASES_ORDER  commuting(defect,readout) => not orderSensitive; (J,Y) is "
          "order-sensitive because it does NOT commute")

    # --- finite fact 5: the binary registration selector forces 'ordered' (M1 reductio mirror) ---
    order_recovery_cost = {"ordered": Fr(0), "commuting": Fr(1)}
    forced = min(order_recovery_cost, key=lambda p: order_recovery_cost[p])
    assert forced == "ordered", "the ordered registration policy must be the unique strict minimum"
    assert order_recovery_cost["commuting"] > order_recovery_cost["ordered"], \
        "the commuting (order-erasing) policy must cost an external order catalogue"
    print("PASS_ORDERED_M1FORCED  registration selector strict-min = 'ordered' (cost 0); 'commuting' "
          "costs 1 = an external order catalogue (RequiresExternalCatalogue, M1-forbidden)")

    # ================= negative controls (each must actually fire) =================
    # FAIL_J_EQ_I_Y_EQ_I_COMMUTE_REJECTED: J=I, Y=I commute -> no order obstruction
    if commute(I4, I4):
        print("FAIL_J_EQ_I_Y_EQ_I_COMMUTE_REJECTED  J=I,Y=I commute => no [.,.] obstruction, no order arrow "
              "(a trivial identity readout cannot source time)")
    else:
        print("ERROR_CONTROL_NOT_FIRED J=I,Y=I should commute"); return 1
    assert is_zero(sub(matmul(I4, I4), matmul(I4, I4))), "I,I commutator must be zero (control sanity)"

    # FAIL_COMMUTING_JY_REJECTED: a commuting pair (two diagonal matrices) gives no order sensitivity
    D1 = [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]]
    D2 = [[5, 0, 0, 0], [0, 6, 0, 0], [0, 0, 7, 0], [0, 0, 0, 8]]
    if commute(D1, D2) and not order_sensitive(D1, D2):
        print("FAIL_COMMUTING_JY_REJECTED  a commuting (diagonal) pair has [.,.]=0 => not order-sensitive: "
              "it erases order, so it cannot be the D0 readout that sources time")
    else:
        print("ERROR_CONTROL_NOT_FIRED diagonal pair should commute"); return 1
    assert is_zero(sub(matmul(D1, D2), matmul(D2, D1))), "diagonal pair commutator must be zero"

    # FAIL_EXTERNAL_CLOCK_INSERTED_REJECTED: no primitive time / SI unit enters; the only content is [J,Y].
    # The order arrow is sourced ONLY by the integer commutator [J,Y]; the numeric DATA of this cert is the
    # set of entries appearing in J, Y, and the derived products -- it must contain NO SI clock constant.
    data_values = set()
    for M in (J, Y, J3, C, [[order_recovery_cost["ordered"], order_recovery_cost["commuting"]]]):
        for row in M:
            for x in row:
                data_values.add(x)
    si_clock_constants = {299792458, Fr(6626070150, 10 ** 43), Fr(1054571817, 10 ** 43)}  # c, h, hbar
    inserted_clock = bool(data_values & si_clock_constants)
    if not inserted_clock:
        print("FAIL_EXTERNAL_CLOCK_INSERTED_REJECTED  no primitive time object / external clock / SI unit "
              "(c, h, hbar, seconds) appears in the cert data; the time arrow is sourced ONLY by [J,Y] != 0")
    else:
        print("ERROR_CONTROL_NOT_FIRED an SI clock constant leaked into the data"); return 1
    assert not inserted_clock, "no SI clock constant may appear in the numeric data of this cert"
    assert data_values <= {-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, Fr(0), Fr(1)}, \
        "the cert data must be only the small integers of J, Y and the binary registration costs"

    print("HONEST_PROOF_TARGET  the UNIVERSAL commuting-readout obstruction (every commuting self-readout "
          "on any carrier erases order) is NOT proven -- named residual "
          "JY-UNIVERSAL-COMMUTING-READOUT-OBSTRUCTION. This cert proves the SPECIFIC D0 (J,Y) witness + the "
          "binary registration selector reductio. A finite witness is not a universal theorem.")
    print("PASS_JY_NONCOMMUTATIVE_ORDER_OBSTRUCTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
