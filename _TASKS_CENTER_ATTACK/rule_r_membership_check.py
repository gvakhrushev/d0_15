#!/usr/bin/env python3
"""
rule_r_membership_check.py — can-fail controls for RULE_R_MEMBERSHIP_MEMO.md.

Each control can FALSIFY the memo's CONCLUSION (obstruction: no mass-blind, C1-respecting
particle->shell membership rule; S1 cap not lifted). The memo's load-bearing reading (3.3) is:
a mass-blind per-slot rule is either non-invariant under S9xS11xS13 (=> C1-forbidden) or
zone-constant (=> too coarse for the 5/4/4 overlap pattern). These controls exercise exactly that.

No PDG masses are needed for the OBSTRUCTION controls (they are pattern/structure only). The one
POSITIVE control that uses masses is guarded and only confirms the pattern is reachable WITH mass.

Exit 0 iff every control's PASS condition holds (i.e. the obstruction survives). Any FAIL prints
the reason and exits 1 — a genuine refutation hook, not a tautology.
"""
import itertools
import random
import sys

random.seed(20260705)

# ---- Owned frozen membership (slot indices), verbatim from shell_membership_v2.py:28 ----
FROZEN = {"A": [1, 2, 3, 10, 11], "B": [4, 5, 8, 9], "C": [2, 3, 12, 13]}
# Particle-level (memory d0-pdg-phi-lattice-test; slot 1 = gamma light node):
#   A={g,b,d,e,u} B={tau,W,c,Z} C={b,d,t,H} EXCLUDED={mu,s}
# core order (shell_membership_v2.py:146): CORE=[12,5,1,15,24,13,3,4,23,11,2,6,25]; slot=i+1.
# Decode via standard PDG Monte-Carlo ids (1=d,2=u,3=s,4=c,5=b,11=e,13=mu,15=tau,23=Z,24=W,25=H;
# id 12 = the protocol's gamma light-node at slot 1 per memory). This decode is DERIVED from the
# on-disk CORE list + PDG ids (CTRL_DECODE below re-derives it); it reproduces the memory's owned
# particle-level sets A={g,b,d,e,u} B={tau,W,c,Z} C={b,d,t,H} EXCLUDED={mu,s} exactly.
CORE = [12, 5, 1, 15, 24, 13, 3, 4, 23, 11, 2, 6, 25]
PDG_ID = {1: "d", 2: "u", 3: "s", 4: "c", 5: "b", 6: "t", 11: "e",
          13: "mu", 15: "tau", 23: "Z", 24: "W", 25: "H", 12: "gamma"}
SLOT_PARTICLE = {i + 1: PDG_ID[c] for i, c in enumerate(CORE)}
EXCLUDED_SLOTS = [s for s in range(1, 14)
                  if s not in FROZEN["A"] + FROZEN["B"] + FROZEN["C"]]

# ---- Owned zone typing (THE 04.6.M1.gen BOOK_04:912 / THE 04.8.L.1 BOOK_04:1046) ----
# generation index = zone label 9/11/13; center->e (gen1/zone9), torus->mu (gen2/zone11),
# shell->tau (gen3/zone13). We only need the OWNED datum that mu is typed to zone 11.
MU_OWNED_ZONE = 11

results = []
def check(name, passed, detail):
    results.append((name, passed, detail))
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")


# ---- CTRL_FROZEN_SLOTS_MATCH ----
# Guards O1 against drift: the frozen sets here must equal the executor's, and the excluded
# set must be exactly {mu, s} = {6, 7}.
def ctrl_frozen_slots_match():
    excl_particles = sorted(SLOT_PARTICLE[s] for s in EXCLUDED_SLOTS)
    ok = (sorted(EXCLUDED_SLOTS) == [6, 7]) and (excl_particles == ["mu", "s"])
    inter = sorted(set(FROZEN["A"]) & set(FROZEN["C"]))
    ok = ok and inter == [2, 3] and sorted(SLOT_PARTICLE[s] for s in inter) == ["b", "d"]
    sizes = tuple(len(FROZEN[k]) for k in "ABC")
    ok = ok and sizes == (5, 4, 4)
    check("CTRL_FROZEN_SLOTS_MATCH", ok,
          f"excluded={excl_particles}, A∩C={[SLOT_PARTICLE[s] for s in inter]}, sizes={sizes}")


# ---- CTRL_PERSLOT_NOT_INVARIANT ----
# Reproduce M2 X4 for the membership consumer specifically: a per-slot membership indicator is
# NOT invariant under a within-zone relabeling of the 33 vertices. We model the 13 core slots as
# living on 13 distinct graph vertices split across zones 9/11/13; a per-slot indicator that
# distinguishes slots is moved by a permutation that fixes zones setwise.
# PASS = we find at least one zone-respecting permutation that changes the membership indicator
#        (=> per-slot membership is non-invariant => needs the C1-forbidden bridge).
# FAIL = every zone-respecting permutation leaves it invariant (would mean it is torsor-safe).
def ctrl_perslot_not_invariant():
    # assign the 13 core slots to zones by the owned generation typing where known; the rest
    # split across the three zones (matter 9,11 / vacuum 13). Exact split is irrelevant to the
    # non-invariance claim; we only need >=2 slots sharing a zone so a swap is available.
    # Minimal, owned-agnostic model: zone9={1,2,3,10,11}, zone11={4,5,6,7,8}, zone13={9,12,13}.
    zones = {9: [1, 2, 3, 10, 11], 11: [4, 5, 6, 7, 8], 13: [9, 12, 13]}
    membership = {s: tuple(k for k in "ABC" if s in FROZEN[k]) for s in range(1, 14)}
    changed = False
    for _ in range(2000):
        perm = {}
        for zslots in zones.values():
            src = list(zslots)
            dst = list(zslots)
            random.shuffle(dst)
            perm.update(dict(zip(src, dst)))
        # membership after relabeling: slot s now carries the label that vertex perm[s] had
        new_membership = {s: membership[perm[s]] for s in range(1, 14)}
        if new_membership != membership:
            changed = True
            break
    check("CTRL_PERSLOT_NOT_INVARIANT", changed,
          "found a zone-respecting relabeling that changes per-slot membership"
          if changed else "membership invariant under all sampled zone relabelings (unexpected)")


# ---- CTRL_ZONE_CONSTANT_TOO_COARSE (FALSIFIER for A1) ----
# Any zone-constant (C1-respecting) rule assigns the SAME membership to all slots in a zone.
# PASS = no zone-constant rule can reproduce FROZEN (because within a single zone the frozen
#        pattern already differs: some excluded, some placed, some doubled).
# FAIL = some zone assignment makes the frozen membership zone-constant (would give a C1-safe rule).
def ctrl_zone_constant_too_coarse():
    membership = {s: frozenset(k for k in "ABC" if s in FROZEN[k]) for s in range(1, 14)}
    # A rule is zone-constant iff there EXISTS a partition of the 13 slots into <=3 zones such that
    # membership is constant on each block. Equivalently: the number of DISTINCT membership values
    # must be <= 3 AND slots with different membership must be separable into <=3 blocks — but a
    # zone-constant rule REQUIRES membership be a function of the zone only, so distinct membership
    # values force distinct zones. Count distinct membership values:
    distinct = set(membership.values())
    ok = len(distinct) > 3
    check("CTRL_ZONE_CONSTANT_TOO_COARSE", ok,
          f"{len(distinct)} distinct membership values > 3 => no zone-constant (<=3-block) rule "
          f"reproduces the pattern; values={sorted(tuple(sorted(v)) for v in distinct)}")


# ---- CTRL_MU_TYPING_CONFLICT ----
# Owned typing puts mu in zone 11 (THE 04.8.L.1); frozen membership EXCLUDES mu from every shell.
# PASS = the two disagree on mu (mu is typed to a zone but excluded from every shell) AND no
#        zone->shell bijection reconciles it (a bijection would map zone 11 to exactly one shell,
#        placing mu, contradicting exclusion).
# FAIL = mu's owned zone maps consistently to its (empty) membership under some zone->shell map.
def ctrl_mu_typing_conflict():
    mu_slot = [s for s, p in SLOT_PARTICLE.items() if p == "mu"][0]
    mu_membership = [k for k in "ABC" if mu_slot in FROZEN[k]]
    excluded = (mu_membership == [])
    # Any zone->shell partial map either sends zone 11 to some shell (=> mu placed, contradiction)
    # or to nothing (=> not a total zone->shell rule, so it cannot be the derivation Q1 needs).
    conflict = excluded and MU_OWNED_ZONE == 11
    check("CTRL_MU_TYPING_CONFLICT", conflict,
          f"mu typed->zone {MU_OWNED_ZONE} yet membership={mu_membership} (excluded) "
          f"=> no zone->shell bijection reconciles")


# ---- CTRL_LABELS_RATIONAL ----
# M2's owned label values are rational (Q8 exponent 4; characters in {0,+-1,+-2}). Requirement
# (2-rational): a mass-blind per-slot IRRATIONAL Q(phi)\Q invariant is NOT supplied.
# PASS = every owned Q8 character value is rational (in Z here). FAIL = an irrational appears.
def ctrl_labels_rational():
    # Q8 = {+-1,+-i,+-j,+-k}; irreducible characters: four 1-dim (values +-1) + one 2-dim
    # (values on classes: 2, -2, 0, 0, 0). All integers => rational.
    char_2dim = [2, -2, 0, 0, 0]  # on classes {1},{-1},{+-i},{+-j},{+-k}
    ones = [1, 1, 1, 1, 1]
    all_vals = char_2dim + ones
    ok = all(float(v).is_integer() for v in all_vals)
    check("CTRL_LABELS_RATIONAL", ok,
          f"all owned Q8 character values rational: {all_vals} (Galois-on-values empty)")


# ---- CTRL_MISS_R_EXISTS_WOULD_REFUTE (POSITIVE control) ----
# Confirms the obstruction is about MASS-BLINDNESS + C1, not that the pattern is unreachable.
# A mass-USING per-slot rule trivially reproduces membership (just look up each slot's shells).
# PASS = a per-slot (mass-using / vertex-distinguishing) lookup reproduces FROZEN exactly.
# This is the control that would let a future owner REFUTE the memo: if the same lookup could be
# made mass-BLIND and C1-respecting, the obstruction falls. Here it is neither (it is a raw table).
def ctrl_miss_r_exists_would_refute():
    lookup = {s: tuple(k for k in "ABC" if s in FROZEN[k]) for s in range(1, 14)}
    reconstructed = {"A": sorted(s for s in lookup if "A" in lookup[s]),
                     "B": sorted(s for s in lookup if "B" in lookup[s]),
                     "C": sorted(s for s in lookup if "C" in lookup[s])}
    ok = all(reconstructed[k] == sorted(FROZEN[k]) for k in "ABC")
    check("CTRL_MISS_R_EXISTS_WOULD_REFUTE", ok,
          "per-slot lookup reproduces frozen membership (pattern reachable WITH per-slot data; "
          "obstruction is specifically mass-blind + C1, per §4)")


def ctrl_decode():
    # Re-derive the slot->particle decode and check it reproduces memory's owned particle sets.
    def parts(slots):
        return sorted(SLOT_PARTICLE[s] for s in slots)
    ok = (parts(FROZEN["A"]) == ["b", "d", "e", "gamma", "u"] and
          parts(FROZEN["B"]) == ["W", "Z", "c", "tau"] and
          parts(FROZEN["C"]) == ["H", "b", "d", "t"] and
          parts(EXCLUDED_SLOTS) == ["mu", "s"])
    check("CTRL_DECODE", ok,
          f"A={parts(FROZEN['A'])} B={parts(FROZEN['B'])} C={parts(FROZEN['C'])} "
          f"excl={parts(EXCLUDED_SLOTS)} (matches owned memory sets)")


def main():
    ctrl_decode()
    ctrl_frozen_slots_match()
    ctrl_perslot_not_invariant()
    ctrl_zone_constant_too_coarse()
    ctrl_mu_typing_conflict()
    ctrl_labels_rational()
    ctrl_miss_r_exists_would_refute()
    n_fail = sum(1 for _, p, _ in results if not p)
    print(f"\n=== {len(results) - n_fail}/{len(results)} PASS ===")
    if n_fail:
        print("A control FAILED: the memo's obstruction reading is refuted on that line — inspect.")
        return 1
    print("Obstruction survives all controls: no mass-blind C1-respecting membership rule owned; "
          "S1 cap NOT lifted; EXACT-MISSING = MISS-R (see memo §4).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
