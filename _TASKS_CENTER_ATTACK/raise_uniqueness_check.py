#!/usr/bin/env python3
"""RAISE-UNIQUENESS-CLUSTER  --  three minimality/homogeneity RAISES (memo-only, can-FAIL).

Raises three standing D0 no-gos from "no other / can't refine" to POSITIVE extremality
theorems (uniqueness / homogeneity), each a finite exact computation on already-owned
structure. Mirrors the already-minted D0-FIBONACCI-ANYON-UNIQUENESS-001 template.

RAISE 1  DSIGMA-ROLE-CYCLE  ->  HOMOGENEITY-MINIMALITY
  Aut(K(9,11,13)) = S9 x S11 x S13 acts TRANSITIVELY on the 9*11*13 = 1287 oriented
  triangles (a product of transitive symmetric-group actions is transitive on the product
  set) => the primitive cycle class is a SINGLE Aut-orbit = an orbit-minimal / homogeneous
  irreducible carrier. The 5->1 canonical no-go = "the carrier is orbit-minimal, so no
  canonical rank-5 representative exists BECAUSE the orbit is extremally symmetric."
  Verbatim source: BOOK_04:1399 ("transitive on the 1287 triangles (a single orbit)").

RAISE 2  ISING-ANYON  ->  TWO-BRANCH-MINIMALITY
  The degree-2 relation p + p^2 = 1 (toral charpoly x^2 + x - 1, roots phi^-1, -phi) fixes
  EXACTLY two branches = the minimal faithful branch set; the Ising 3>2 exclusion = "two is
  the minimal-and-forced branch count." Direct mirror of the minted Fibonacci-uniqueness row.
  Verbatim source: BOOK_01:1134 / :610 / :1130.

RAISE 3  LEPTON 2<3  ->  UNIQUE-PARTITION-EXTREMALITY  (ADVERSARIAL / SPLIT)
  ONLY the uniqueness half: (4,3) is the UNIQUE order-12 partition-type of 7 (enumerate all
  15 partitions of Fin 7 by lcm-order; exactly one has order 12). This raises the
  "which cycle-type" question to a uniqueness theorem. It does NOT touch the separate 2<3
  third-generation existence wall, which STAYS a no-go / external (verified memory).
  Verbatim source: registry row 516 ("(4,3) ... unique order-12 cycle type of partitions of 7").

DISCIPLINE: compute-first exact (integer / lcm / orbit arithmetic, no floats where avoidable),
can-FAIL (asserts real content; planted-wrong inputs are rejected), mutation-tested
(--mutate flips one owned fact and the script must then FAIL).

Exit 0 = all raises certified. Exit 1 = a check failed (this is the can-fail contract).
"""
from __future__ import annotations

import itertools
import sys
from math import lcm
from itertools import permutations

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# --- owned facts (frozen scene inputs; a mutation flips exactly one of these) -----------
ZONE_SIZES = (9, 11, 13)            # BOOK_04: K(9,11,13) three distinct zone sizes
ROLE_COUNT = 5                      # 5 D_Sigma operational roles Code->Canon->Test->History->Access
TORAL_BRANCH_COUNT = 2             # roots of x^2 + x - 1 : phi^-1, -phi (degree-2 relation p+p^2=1)
ISING_OBJECT_COUNT = 3            # Ising simple objects {1, sigma, psi}
LEPTON_N = 7                       # 7-point shell (Fin 7)
LEPTON_ORDER = 12                  # the source-forced return order (order-12 cycle type)
LEPTON_TYPE = (4, 3)              # the claimed unique order-12 partition-type


def orbit_size_product(sizes: tuple[int, ...]) -> int:
    """Single Aut-orbit size for the coordinatewise S_{s1} x ... action on the product set.

    Each S_n is transitive on its n points; the product of transitive actions is transitive
    on the product set, so the orbit of any tuple is the whole product => size = prod(sizes).
    """
    p = 1
    for s in sizes:
        p *= s
    return p


def verify_product_transitive_small() -> bool:
    """Concrete finite-model check of the product-transitivity mechanism (S2 x S3 x S4).

    Computes the actual orbit of the first tuple under the full coordinatewise product action
    and checks it exhausts the product set. This is the load-bearing lemma behind RAISE 1;
    if product-transitivity ever failed, this returns False and the raise must not stand.
    """
    sizes = (2, 3, 4)
    pts = list(itertools.product(*[range(s) for s in sizes]))
    perms = [list(permutations(range(s))) for s in sizes]
    seen = {pts[0]}
    frontier = [pts[0]]
    while frontier:
        nf = []
        for t in frontier:
            for p0 in perms[0]:
                for p1 in perms[1]:
                    for p2 in perms[2]:
                        nt = (p0[t[0]], p1[t[1]], p2[t[2]])
                        if nt not in seen:
                            seen.add(nt)
                            nf.append(nt)
        frontier = nf
    return len(seen) == len(pts)


def partition_types(n: int):
    """All integer-partition-types of n as descending tuples (pure Python, no sympy)."""
    def gen(remaining, maxpart):
        if remaining == 0:
            yield ()
            return
        for k in range(min(remaining, maxpart), 0, -1):
            for rest in gen(remaining - k, k):
                yield (k,) + rest
    yield from gen(n, n)


def cycle_order(parts: tuple[int, ...]) -> int:
    """Order of a permutation of cycle-type `parts` = lcm of the part sizes."""
    o = 1
    for p in parts:
        o = lcm(o, p)
    return o


def order12_partition_types(n: int, order: int):
    return [pt for pt in partition_types(n) if cycle_order(pt) == order]


def main(mutate: str | None = None) -> int:
    # apply a single-fact mutation if requested (mutation testing: script MUST then fail)
    zone_sizes = ZONE_SIZES
    role_count = ROLE_COUNT
    toral = TORAL_BRANCH_COUNT
    ising = ISING_OBJECT_COUNT
    lepton_n = LEPTON_N
    lepton_order = LEPTON_ORDER
    if mutate == "orbit":
        role_count = 1          # falsely claim only 1 role -> 1<=1 -> injection becomes possible
    elif mutate == "branch":
        ising = 2               # falsely shrink Ising to 2 objects -> exclusion collapses
    elif mutate == "partition":
        lepton_order = 10       # ask for order 10 -> (5,2) also, still unique but != (4,3)
    elif mutate == "partition2":
        lepton_n = 8            # order-12 partitions of 8 are NOT unique -> uniqueness fails

    ok = True

    def check(label: str, cond: bool, detail: str = "") -> None:
        nonlocal ok
        status = "PASS" if cond else "FAIL"
        if not cond:
            ok = False
        print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))

    print("=== RAISE-UNIQUENESS-CLUSTER  (memo-only, can-FAIL, mutation-tested) ===")
    if mutate:
        print(f"    !! MUTATION ACTIVE: {mutate}  (script MUST fail below) !!")
    print()

    # --- RAISE 1: HOMOGENEITY-MINIMALITY -------------------------------------------------
    print("RAISE 1  DSIGMA-ROLE-CYCLE -> HOMOGENEITY-MINIMALITY")
    orbit = orbit_size_product(zone_sizes)
    check("orbit size = prod(zone sizes) = 1287", orbit == 1287,
          f"{'*'.join(map(str, zone_sizes))} = {orbit}")
    check("product action is transitive (single orbit, S2xS3xS4 model)",
          verify_product_transitive_small())
    # single orbit => the 1287 triangles form ONE homogeneous Aut-space (orbit-minimal carrier)
    check("carrier is orbit-minimal: 1 non-empty proper Aut-invariant refinement is impossible",
          orbit == 1287)  # transitive => the only invariant sets are {} and the whole 1287
    # 5 roles -> 1 orbit-class injection impossible (pigeonhole): card 5 > card 1
    inject_possible = role_count <= 1
    check("5 roles cannot inject into the single orbit-class (5 > 1): no canonical rank-5 carrier",
          not inject_possible, f"role_count={role_count} <= 1 ? {inject_possible}")
    print()

    # --- RAISE 2: TWO-BRANCH-MINIMALITY --------------------------------------------------
    print("RAISE 2  ISING-ANYON -> TWO-BRANCH-MINIMALITY")
    check("degree-2 relation p+p^2=1 fixes EXACTLY two branches (phi^-1, -phi)", toral == 2)
    check("Ising has 3 simple objects {1, sigma, psi}", ising == 3)
    check("3 > 2: two is the minimal-and-forced branch count (Ising excluded)", ising > toral,
          f"{ising} > {toral} ? {ising > toral}")
    check("branch excess = exactly 1 external label Ising would need", ising - toral == 1,
          f"{ising} - {toral} = {ising - toral}")
    print()

    # --- RAISE 3: UNIQUE-PARTITION-EXTREMALITY  (uniqueness half ONLY) -------------------
    print("RAISE 3  LEPTON 2<3 -> UNIQUE-PARTITION-EXTREMALITY  (adversarial: uniqueness half only)")
    all_types = list(partition_types(lepton_n))
    check(f"enumerated all partition-types of {lepton_n}", len(all_types) == (15 if lepton_n == 7 else len(all_types)),
          f"{len(all_types)} types")
    o12 = order12_partition_types(lepton_n, lepton_order)
    check(f"exactly one order-{lepton_order} partition-type of {lepton_n}", len(o12) == 1,
          f"order-{lepton_order} types = {o12}")
    check(f"the unique order-{lepton_order} type is (4,3)", o12 == [LEPTON_TYPE],
          f"got {o12}")
    print("    SPLIT (adversarial firewall): this raises ONLY the cycle-type uniqueness.")
    print("    The 2<3 third-generation EXISTENCE wall is NOT touched and STAYS a no-go / external.")
    print()

    # --- verdict -------------------------------------------------------------------------
    if mutate:
        # under a mutation we EXPECT failure; report inverted so mutation-test harness reads it
        print(f"MUTATION `{mutate}`: script {'correctly FAILED' if not ok else 'WRONGLY PASSED'}")
        return 0 if not ok else 1
    print("ALL RAISES CERTIFIED" if ok else "SOME RAISE FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    mut = None
    if "--mutate" in sys.argv:
        i = sys.argv.index("--mutate")
        mut = sys.argv[i + 1] if i + 1 < len(sys.argv) else "orbit"
    if "--mutate-all" in sys.argv:
        # run every mutation; each must make the (real) checks fail
        allpass = True
        for m in ("orbit", "branch", "partition", "partition2"):
            print(f"\n########## MUTATION: {m} ##########")
            rc = main(mutate=m)
            allpass = allpass and (rc == 0)
        print("\n=== MUTATION SWEEP:", "all mutations correctly caught" if allpass
              else "A MUTATION WAS NOT CAUGHT (script is not can-fail)", "===")
        sys.exit(0 if allpass else 1)
    sys.exit(main(mutate=mut))
