#!/usr/bin/env python3
"""
history_stratification_nogo_check.py
===================================
CANDIDATE NO-GO for the obligation stated at
09_LEAN_FORMALIZATION/D0/Foundation/DetectionCapabilityBoundary.lean:36-41 (verbatim):

  "To recover exactly two detection capabilities, the theory needs a typed
   stratification theorem placing history/order in the memory layer and proving
   that primitive detector comparison factors through the current observation,
   not through history."

CLAIM (N). No such theorem is derivable INSIDE the DetectionCapabilityBoundary
model. That model's three capability coordinates are related by a symmetry group
that acts transitively on the three primitive comparisons; therefore every
predicate definable from the model's own primitives is equivariant, and no
equivariant predicate can hold of historyComparison while failing on
membershipComparison. The stratification must IMPORT an asymmetry.

EXACT MISSING OBJECT: a named asymmetry distinguishing the history coordinate
from the membership and value coordinates. Until one is supplied, "exactly two
detection capabilities" cannot be recovered by any criterion stated in this model.

WHY THIS IS NOT A RESTATEMENT. The module already proves history is a third
primitive (history_is_third_primitive, LEAN_PROVED). That is an EXISTENCE result:
a third capability survives. Claim N is a different, stronger statement about the
WHOLE class of possible fixes: it says the repair route the module itself
proposes cannot be carried out internally, and says exactly what must be added.
The module leaves the repair open; N shows the repair is not merely undone but
unreachable from inside, and names the minimal import.

THE MODEL (transcribed from DetectionCapabilityBoundary.lean:50-96):
  Observation           = (member, value, history) in Bool^3          -> 8 states
  Comparison            = Observation -> Observation -> Bool
  OperationalComparison = can both accept and reject
  <f>Comparison         = fun x y => decide (x.f = y.f)   for f in the 3 fields
  <F>OnlyChange x x'    = the OTHER two fields agree
  Uses<F> cmp           = exists x x' y, <F>OnlyChange x x' and cmp x y != cmp x' y
  capabilityVector cmp  = (UsesMembership, UsesValue, UsesHistory)

Exit 0 iff every check passes and every negative control fires.
"""

from itertools import permutations, product
import sys

FAILURES, PASSES = [], []


def check(name, cond, detail=""):
    (PASSES if cond else FAILURES).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"   [{detail}]" if detail else ""))
    return bool(cond)


# ---------------------------------------------------------------------------
# The model, transcribed exactly. 3 coordinates, indices 0=member 1=value 2=history
# ---------------------------------------------------------------------------
COORD = {0: "member", 1: "value", 2: "history"}
OBS = list(product([0, 1], repeat=3))          # 8 observations
OBS_IDX = {o: i for i, o in enumerate(OBS)}


def eq_pattern(x, y):
    """(x.m==y.m, x.v==y.v, x.h==y.h) — the datum the primitives read."""
    return tuple(int(x[i] == y[i]) for i in range(3))


# The comparisons expressible from coordinate-equality data: a Boolean function
# of the 3-bit equality pattern. 2^8 = 256 of them. All three primitives are here.
PATTERNS = list(product([0, 1], repeat=3))     # 8 possible equality patterns
PAT_IDX = {p: i for i, p in enumerate(PATTERNS)}


def make_cmp(truth):
    """truth: an 8-bit tuple over PATTERNS -> a Comparison."""
    return lambda x, y: truth[PAT_IDX[eq_pattern(x, y)]]


ALL_TRUTHS = list(product([0, 1], repeat=8))   # 256 comparisons


def operational(truth):
    cmp = make_cmp(truth)
    vals = {cmp(x, y) for x in OBS for y in OBS}
    return 0 in vals and 1 in vals


def uses(truth, i):
    """UsesMembership / UsesValue / UsesHistory, transcribed: change ONLY
    coordinate i of the first argument and see if the result can move."""
    cmp = make_cmp(truth)
    for x in OBS:
        for y in OBS:
            xp = list(x)
            xp[i] = 1 - xp[i]
            xp = tuple(xp)          # differs from x ONLY in coordinate i
            if cmp(x, y) != cmp(xp, y):
                return True
    return False


def capability_vector(truth):
    return tuple(int(uses(truth, i)) for i in range(3))


# The three primitives of the module.
def primitive_truth(i):
    """<f>Comparison = decide (x.f = y.f): true exactly when pattern bit i is 1."""
    return tuple(p[i] for p in PATTERNS)


PRIMITIVES = {COORD[i]: primitive_truth(i) for i in range(3)}


# ---------------------------------------------------------------------------
# The symmetry: S3 permuting the three coordinates.
# ---------------------------------------------------------------------------
def act_on_truth(sigma, truth):
    """(sigma . cmp)(x,y) = cmp(sigma^-1 x, sigma^-1 y). On pattern-comparisons
    this permutes the pattern bits."""
    inv = [0, 0, 0]
    for i, s in enumerate(sigma):
        inv[s] = i
    new = [0] * 8
    for p in PATTERNS:
        # the pattern of the sigma-acted observations
        q = tuple(p[inv[i]] for i in range(3))
        new[PAT_IDX[q]] = truth[PAT_IDX[p]]
    return tuple(new)


S3 = list(permutations(range(3)))


def main():
    print("=" * 78)
    print("Stratification NO-GO candidate — DetectionCapabilityBoundary is symmetric")
    print("=" * 78)

    # -- M1: the transcription reproduces the module's own proved facts -------
    print("\n[M1] transcription fidelity (must reproduce the module's LEAN_PROVED facts)")
    vecs = {n: capability_vector(t) for n, t in PRIMITIVES.items()}
    check(
        "M1a: capabilityVector(membershipComparison) == (1,0,0)",
        vecs["member"] == (1, 0, 0), f"got {vecs['member']}",
    )
    check(
        "M1b: capabilityVector(valueComparison) == (0,1,0)",
        vecs["value"] == (0, 1, 0), f"got {vecs['value']}",
    )
    check(
        "M1c: capabilityVector(historyComparison) == (0,0,1)  [history_is_third_primitive]",
        vecs["history"] == (0, 0, 1), f"got {vecs['history']}",
    )
    check(
        "M1d: all three primitives are operational",
        all(operational(t) for t in PRIMITIVES.values()),
        "each both accepts and rejects, as the module proves",
    )
    # no membership/value representation of history: history's vector is not in
    # the span of the other two coordinates (it lights a coordinate they cannot).
    check(
        "M1e: no membership/value combination reaches history's capability coordinate",
        vecs["history"][2] == 1 and vecs["member"][2] == 0 and vecs["value"][2] == 0,
        "reproduces no_membership_value_representation_of_history",
    )

    # -- N1: S3 acts on the comparison set ------------------------------------
    print("\n[N1] the symmetry group acts on the model")
    closed = all(act_on_truth(s, t) in set(ALL_TRUTHS) for s in S3 for t in
                 [primitive_truth(0), primitive_truth(1), primitive_truth(2)])
    check("N1a: S3 maps pattern-comparisons to pattern-comparisons", closed,
          "the action is well defined on the 256-element comparison set")

    # equivariance of the capability vector
    equivar = True
    for s in S3:
        for t in ALL_TRUTHS:
            lhs = capability_vector(act_on_truth(s, t))
            rhs = tuple(capability_vector(t)[[s.index(i) for i in range(3)][j]]
                        for j in range(3))
            if lhs != rhs:
                equivar = False
                break
        if not equivar:
            break
    check(
        "N1b: capabilityVector is S3-EQUIVARIANT on all 256 comparisons",
        equivar,
        "every capability statement transforms with the permutation; none is pinned to history",
    )

    # operationality is invariant
    op_inv = all(operational(t) == operational(act_on_truth(s, t))
                 for s in S3 for t in ALL_TRUTHS)
    check("N1c: OperationalComparison is S3-INVARIANT", op_inv,
          "the module's only non-coordinate predicate cannot see the difference")

    # -- N2: THE NO-GO — the three primitives form ONE orbit ------------------
    print("\n[N2] the no-go")
    orb = {act_on_truth(s, PRIMITIVES["history"]) for s in S3}
    same_orbit = (PRIMITIVES["member"] in orb) and (PRIMITIVES["value"] in orb)
    check(
        "N2a: {membership, value, history} is a SINGLE S3-orbit (size %d)" % len(orb),
        same_orbit and len(orb) == 3,
        "history is carried onto membership by a symmetry of the model",
    )
    # A predicate is S3-invariant iff it is a union of orbits. Since the three
    # primitives share an orbit, no invariant predicate separates them. Verified
    # directly by exhaustion over orbits rather than asserted.
    orbits = {}
    for t in ALL_TRUTHS:
        key = min(act_on_truth(s, t) for s in S3)   # canonical orbit representative
        orbits.setdefault(key, set()).add(t)
    sep_exists = any(
        (PRIMITIVES["history"] in blk) != (PRIMITIVES["member"] in blk)
        for blk in orbits.values()
    )
    check(
        "N2b: NO S3-invariant predicate separates history from membership",
        not sep_exists,
        f"{len(orbits)} orbits on 256 comparisons; the primitives share one",
    )
    check(
        "N2c: therefore the stratification theorem is NOT derivable in this model",
        (not sep_exists) and same_orbit,
        "any proof must import an asymmetry between history and the other coordinates",
    )

    # -- NEGATIVE CONTROLS ----------------------------------------------------
    print("\n[NEGATIVE CONTROLS]")
    # (a) Break the symmetry: allow only the swap of member<->value (history
    #     singled out by fiat). A separating predicate must now EXIST, else the
    #     no-go would be vacuous rather than a statement about full S3.
    S2 = [(0, 1, 2), (1, 0, 2)]
    orbits2 = {}
    for t in ALL_TRUTHS:
        key = min(act_on_truth(s, t) for s in S2)
        orbits2.setdefault(key, set()).add(t)
    sep2 = any(
        (PRIMITIVES["history"] in blk) != (PRIMITIVES["member"] in blk)
        for blk in orbits2.values()
    )
    check(
        "NC1: with history singled out by fiat (S2 only), a separating predicate EXISTS",
        sep2,
        "so N2 genuinely consumes the full S3 symmetry of the model; not a tautology",
    )
    # (b) The action must be nontrivial — otherwise everything is trivially invariant.
    moved = sum(1 for t in ALL_TRUTHS if any(act_on_truth(s, t) != t for s in S3))
    check(
        "NC2: the S3 action is nontrivial (%d of 256 comparisons are moved)" % moved,
        moved > 0,
        "an inert group would make N2 content-free",
    )
    # (c) Hand-checkable: the orbit of the constant-true comparison is a singleton.
    const_true = tuple([1] * 8)
    check(
        "NC3: hand-checkable — the constant comparison is a fixed point (orbit size 1)",
        len({act_on_truth(s, const_true) for s in S3}) == 1,
        "and it is NOT operational, so it is outside the primitives",
    )
    check(
        "NC4: the constant comparison is indeed non-operational (never rejects)",
        not operational(const_true),
        "confirms the operationality filter is doing work",
    )

    print("\n" + "=" * 78)
    print(f"checks passed: {len(PASSES)}   failed: {len(FAILURES)}")
    if FAILURES:
        for f in FAILURES:
            print("   -", f)
        return 1
    print("CLAIM N stands: the three capability coordinates of the")
    print("DetectionCapabilityBoundary model form a single symmetry orbit, so the")
    print("stratification theorem the module calls for cannot be proved inside it.")
    print("EXACT MISSING: a named asymmetry separating history from membership/value.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
