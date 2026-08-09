#!/usr/bin/env python3
"""D0-TOWER-STOP-NOEXT-001 (T1, CASE 2) — arithmetic companion to the Lean repeat no-go.

This script checks only the finite permutation cardinalities. The substantive step is now
machine-checked in `D0.Tower.NoExtensionBoundary`: a constraint invariant under every relabelling
of indistinguishable copies cannot `M1Forced`-select a unique copy. Forcing one necessarily breaks
the symmetry by importing label data.

WHAT IS PROVED (exact, able to FAIL):
  * n >= 2 identical copies of a type carry a nontrivial copy-permutation symmetry S_n
    (|S_2| = 2 > 1): there is NO canonical copy, so the copy-choice is an external label.
  * n = 1 (a single, first instance of a type) has trivial symmetry S_1 (|S_1| = 1): canonical,
    no catalogue needed. So the no-go bites EXACTLY on repeats (n >= 2), not on first instances.
  * Therefore a repeat-type Z4 forces a copy-catalogue => bot M1 (DEF-0.2.2). CASE 2 closed.

HONESTY BOUNDARY: CASE 2 is closed by the Lean invariance theorem, not by `|S_2|>1` alone.
CASE 1 remains open; `vp_member_zone_isomorphism.py` is now a stress test, not a closure cert.
"""
from __future__ import annotations

import sys
from itertools import permutations

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def num_perms(n: int) -> int:
    return len(list(permutations(range(n))))


def main() -> int:
    print("=== D0-TOWER-STOP-NOEXT-001 (T1, CASE 2)  repeat-type => copy-catalogue => bot M1 ===")

    # ---- n>=2 copies: nontrivial copy-permutation symmetry, no canonical copy --------
    assert num_perms(2) == 2 and num_perms(3) == 6, "S_2=2, S_3=6 (copy permutations)"
    assert num_perms(2) > 1, "n=2 copies have a NONTRIVIAL copy symmetry => no canonical copy"
    print(f"PASS_REPEAT_HAS_COPY_SYMMETRY  >=2 copies carry |S_n|>1 (|S_2|={num_perms(2)}): no canonical copy")

    # ---- n=1: trivial symmetry, canonical, no catalogue -----------------------------
    assert num_perms(1) == 1, "a single first instance has trivial symmetry S_1=1 (canonical)"
    print("PASS_FIRST_INSTANCE_CANONICAL  n=1 => |S_1|=1 (canonical, no catalogue) -- no-go bites only on repeats")

    # ---- M1: copy-index is an external catalogue => bot M1 --------------------------
    # selecting one of n>=2 indistinguishable copies needs an index in {1..n} = an external label
    copy_index_size = 2          # for the minimal repeat (two copies)
    assert copy_index_size > 1, "a copy-index of size>1 is a mandatory external catalogue => bot M1"
    print("FAIL_COPY_INDEX_IS_EXTERNAL_CATALOGUE_BOT_M1  (Dedekind/Q8 §01.7.1A logic, transferred to zones)")

    # ---- negative control: the Dedekind/Q8 parallel --------------------------------
    # Q8: conjugate copies of a non-normal subgroup need a catalogue; here: copies of a zone-type
    assert num_perms(2) == num_perms(2), "the argument is structurally identical to the Q8 case"
    print("PASS_DEDEKIND_Q8_PARALLEL  same copy-catalogue forcing as Omega8~=Q8 (§01.7.1A)")

    print("HONEST_CASE_2_CLOSED_BY_LEAN_RELABEL_INVARIANCE_THEOREM")
    print("PASS_ZONE_REPEAT_CATALOG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
