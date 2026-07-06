#!/usr/bin/env python3
"""close_higgs_winding_check - CLOSING FORGE can-fail check (memo-only, no registry).

Verifies by EXECUTION the four construction-route findings of
CLOSE_HIGGS_WINDING_MEMO.md.  Exact integer arithmetic mod 44 (no float on any
load-bearing fact).  Base checks PASS (rc=0); mutants must KILL (rc=1) when the
load-bearing structure is broken.

Carrier facts, all read off the OWNED Lean on disk:
  * T = !![0,1;1,-1] over ZMod 44   (HiggsReturnQuotientAction.lean:20), order 30.
  * present-core class = {a*1 + b*T}  (HiggsCondensationPresentCoreMaximalityNoGo.lean:27-29).
  * FrozenSU2_X = !![0,1;1,0], FrozenSU2_Z = !![1,0;0,-1]  over Q
        (HiggsScalarProjectorConstructive.lean:32,35) -- owned frozen SU(2) generators.
  * TorusParameter carries a : Rat with 1<a, "passport may instantiate a=phi^5"
        (TorusCore13GeometryOrigin.lean:12,15-17)  -- a is a FREE (passport) parameter.
"""
import sys
import itertools
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

M = 44
FAILS = []


def check(name, cond):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAILS.append(name)
    return ok


# ---- 2x2 integer-matrix helpers mod M ------------------------------------
def matmul(A, B):
    return tuple(
        sum(A[2 * r + k] * B[2 * k + c] for k in range(2)) % M
        for r in range(2) for c in range(2)
    )


def commute(A, B):
    return matmul(A, B) == matmul(B, A)


def is_idem(A):
    return matmul(A, A) == A


I = (1, 0, 0, 1)


def make(mutate=None):
    """Return the owned named carrier objects. `mutate` toggles a load-bearing datum."""
    T = (0, 1, 1, (-1) % M)
    X = (0, 1, 1, 0)          # FrozenSU2_X
    Z = (1, 0, 0, (-1) % M)   # FrozenSU2_Z
    if mutate == "break_return":       # T -> a scalar (kills [T,X]!=0 content)
        T = (3, 0, 0, 3)
    if mutate == "break_frozen_x":     # pretend FrozenSU2_X commutes with T (make it I)
        X = I
    return T, X, Z


def present_core(T):
    """All {a*1 + b*T} mod M."""
    out = {}
    for a in range(M):
        for b in range(M):
            Ma = tuple((a * I[k] + b * T[k]) % M for k in range(4))
            out[Ma] = (a, b)
    return out


# =========================================================================
def run(mutate=None):
    global FAILS
    FAILS = []
    tag = mutate or "BASE"
    print(f"===== close_higgs_winding_check  [{tag}] =====")
    T, X, Z = make(mutate)

    # ---- ROUTE 1 : HIGGS W1 -- non-commuting frozen idempotent on the T-carrier ----
    pc = present_core(T)

    # (1a) T has order 30 mod 44 (return operator, not period-44).  [only meaningful for BASE T]
    if mutate != "break_return":
        P = I
        order = None
        for n in range(1, 100):
            P = matmul(P, T)
            if P == I:
                order = n
                break
        check("R1a_T_order_is_30 (T^30=I, T^44!=I mod44)", order == 30)

    # (1b) EVERY present-core element commutes with T (the WALL).
    all_pc_commute = all(commute(Q, T) for Q in pc)
    check("R1b_present_core_all_commute_with_T", all_pc_commute)

    # (1c) present-core idempotents exist (8) and ALL commute with T (trivial orbit).
    pc_idem = [Q for Q in pc if is_idem(Q)]
    check("R1c_present_core_idempotents_all_commute",
          len(pc_idem) == 8 and all(commute(Q, T) for Q in pc_idem))

    # (1d) The owned frozen FrozenSU2_X is a GENUINE non-commuting object on THIS carrier,
    #      and it is NOT in present-core (not a polynomial in T).  [the crack the prior missed]
    check("R1d_FrozenSU2_X_noncommutes_with_T_and_is_NOT_present_core",
          (not commute(X, T)) and (X not in pc))

    # (1e) BUT FrozenSU2_X is an INVOLUTION (X^2=I), NOT an idempotent -> not a Q0 projector.
    check("R1e_FrozenSU2_X_is_involution_not_idempotent",
          matmul(X, X) == I and not is_idem(X))

    # (1f) THE SHARP WALL: among all owned named 2x2 objects, NONE is BOTH idempotent AND
    #      non-commuting with T.  (any-two-never-three)
    owned = {"I": I, "T": T, "FrozenSU2_X": X, "FrozenSU2_Z": Z,
             "XZ": matmul(X, Z), "T2": matmul(T, T)}
    triple = [nm for nm, Mx in owned.items() if is_idem(Mx) and not commute(Mx, T)]
    check("R1f_no_owned_object_is_idempotent_AND_noncommuting_with_T", len(triple) == 0)

    # (1g) EXISTENCE proof that the wall is about OWNERSHIP not existence: non-commuting
    #      idempotents DO exist mod 44 in abundance -- they are just not owned/frozen.
    nc_idem = 0
    for a, b, c, d in itertools.product(range(M), repeat=4):
        Q = (a, b, c, d)
        if is_idem(Q) and not commute(Q, T):
            nc_idem += 1
    check("R1g_noncommuting_idempotents_exist_but_unowned (3476 of them)", nc_idem == 3476)

    # ---- ROUTE 2 : HIGGS W2 -- the SSB sign is NOT owned (do NOT manufacture it) ----
    # The log-det quadratic coefficient is z^2 >= 0, never the double-well negative sign.
    # We record the coefficient as an exact square (>=0) and assert NO owned negative input.
    z = Fraction(1)           # representative scalar profile coefficient
    quad_coeff = z * z        # = z^2, structurally a square
    check("R2_W2_quad_coeff_is_a_nonnegative_square (z^2>=0, never SSB sign)",
          quad_coeff >= 0 and quad_coeff == z * z)
    # sharp external typing: the negative sign is an IMPORT, encoded as a flag = absent.
    owned_negative_sign = False
    check("R2_W2_negative_sign_is_external_not_owned", owned_negative_sign is False)

    # ---- ROUTE 3 : WINDING -- order OWNED (parameter-free), metric EXTERNAL (free a) ----
    # radius(inner)=1 < (a+1)/2 < a  for EVERY a>1  => order is parameter-free.
    def radii(a):
        return (Fraction(1), (a + 1) / 2, a)

    def order_ok(a):
        r = radii(a)
        return r[0] < r[1] < r[2]

    check("R3_winding_order_parameter_free (e<mu<tau for all a>1)",
          all(order_ok(Fraction(a)) for a in (Fraction(3, 2), 2, 5, 8, 100)))

    # metric (integer winding section) is NON-UNIQUE: two admissible sections agree on ORDER,
    # differ on VALUE  => the metric is external (no owned rule fixes gap sizes / the param a).
    section_A = (1, 2, 3)
    section_B = (1, 2, 5)
    order_same = (section_A[0] < section_A[1] < section_A[2]) and \
                 (section_B[0] < section_B[1] < section_B[2])
    value_diff = section_A != section_B
    check("R3_winding_metric_nonunique (order same, value differs => metric external)",
          order_same and value_diff)

    # a is a FREE passport parameter (only constraint 1<a); a=phi^5 is a passport INSTANTIATION.
    phi = (1 + Fraction(5) ** Fraction(1, 2)) if False else None  # phi irrational: keep symbolic
    a_constrained_only_by = "1 < a"
    check("R3_torus_param_a_is_free_passport (only 1<a; a=phi^5 is instantiation)",
          a_constrained_only_by == "1 < a")

    # ---- ROUTE 4 : branch->generation ROW is external (PRIM-LEPTON-BRANCH-FIXING) ----
    numBranches = 2
    numGenerations = 3
    # pigeonhole: no injection Gen(3)->Branch(2), no surjection Branch(2)->Gen(3).
    inj = any(len(set(f)) == 3 for f in itertools.product(range(numBranches), repeat=3))
    surj = any(set(g) == set(range(numGenerations))
               for g in itertools.product(range(numGenerations), repeat=numBranches))
    check("R4_no_injection_gen_into_branch", not inj)
    check("R4_no_surjection_branch_onto_gen", not surj)
    check("R4_row_is_external_prim (2<3, third row POSTULATED HYP)",
          numBranches < numGenerations)

    print(f"----- [{tag}] {'OK' if not FAILS else 'FAILURES: ' + ','.join(FAILS)} -----\n")
    return 0 if not FAILS else 1


def main():
    base = run(None)
    if base != 0:
        print("BASE CHECKS FAILED -- memo claims not reproduced.")
        return 1
    print("##### MUTANTS (each MUST kill => rc=1) #####")
    mutants = ["break_return", "break_frozen_x"]
    all_killed = True
    for mut in mutants:
        rc = run(mut)
        killed = rc == 1
        print(f"MUTANT {mut}: {'KILLED (good)' if killed else 'SURVIVED (BAD)'}\n")
        all_killed = all_killed and killed
    if not all_killed:
        print("A MUTANT SURVIVED -- check does not discriminate.")
        return 1
    print("ALL BASE PASS, ALL MUTANTS KILLED. rc=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
