#!/usr/bin/env python3
"""shell_rule_r_attempt4.py — SHELL-RULE-R ATTEMPT 4 archived scoring script (2026-07-04).

Root-asymmetry rebuild after skeptic #1 killed attempt-3/S2-as-derivation (K1 bijection joint
fitted; K2 weight-space rhyme; K3 untestable nu-falsifier; mu-seat trilemma wound; missing
archived ablation = discipline gap this file repairs).

BINDING CONSTRAINTS (ledger "Attempt 4 — direction"):
(a) bijection joint first: zone<->circle either = the owned radial object m_rad
    (TorusShellAttachment.lean:84-95 strictMono inner9<core11<outer13 -> 9->B,11->A,13->C)
    or dropped. PRIMARY REFRAME under test: circles = even-ladder rung strata,
    r_B:r_A:r_C = phi^2:phi^4:phi^6 = Q(6):Q(8):Q(10), Q(D)=2*delta0*phi^(D-1)=phi^(D-4).
(b) connectives ONLY from the root asymmetry: branch split (p+,p-)=(phi^-1,phi^-2)
    [BOOK_01:522-526], full branch gap 2*delta0=phi^-3 [BOOK_01:669], round-trip factor 2
    (4pi double-cycle holonomy, [Q8,Q8]=Z(Q8)={+-1}) [BOOK_01:830, BOOK_04:872-876],
    delta-cascade delta_{-n}=delta0^(n+1) [BOOK_01:1122, vp_dim_ladder_compact.py],
    Galois conjugation on Q(phi) VALUES only (never graph symmetry — Iter25 wall BOOK_04:1383),
    +2 evenness via holonomy parity [BOOK_01:1885-1899].
(c) MANDATORY uniform-application audit per connective; two equally-natural readings giving a
    slot two seats = connective DEAD (no bespoke clauses).
(d) falsifiers computable under the frozen protocol (shell_membership_v2.py machinery).

OWNED-MATERIAL SWEEP RESULT (grep-verified, this session):
- Q(D) ladder cert-backed for D=1..8 ONLY (vp_dim_ladder_compact.py:30-36); owned semantic
  anchors: D=1 (binary cut, Q=phi^-3=2*delta0) and D=4 (role budget, Q=1) [BOOK_01:1122].
  NO owned semantics exist for D=6, D=8, D=10; Q(10) is outside the cert range. |Omega_8|=8
  is a GROUP ORDER (Omega_8={A,B,C,D}x{+,-}~=Q_8, BOOK_01:763-802), never linked to ladder D=8.
- The even ladder {phi^0,phi^2,phi^4,phi^6} is owned as the AF Dirac^2 eigenvalue ladder with
  eigenspace multiplicities {F2,F4,F6,F8}={1,3,8,21} summing to 33
  [BOOK_02:1295, D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001]; scene<->AF SPECTRAL transport is
  NO-GO (bunching 20*phi>13; the scene cannot host phi^2:phi^4:phi^6) [BOOK_02:1291].
- NO owned text assigns particles/slots/zones to rungs. No "rung" vocabulary in BOOK_01/02/04.
- Owned mass-blind per-slot data: generation (=zone label, THE 04.6.M1.gen BOOK_04:912);
  charge/T3/Y (anomaly row Y=(1/6,-2/3,1/3,-1/2,1,0), T3=+-1/2, BOOK_04:1377,1397); lepton
  sheet keying (e unramified 0 / mu 4-cycle / tau 3-cycle, BOOK_04:1113,1135,1939); e forced
  base register (BOOK_04:964-996); mu zone-11 localization (BOOK_04:1046); terminal triad
  (BOOK_04:643-665); W,Z vacuum-cell edges + H diagonal (BOOK_04:926); H V13 condensation
  (BOOK_04:1615). ALL of these per-slot values are RATIONAL — Galois conjugation (R5) has
  nothing mass-blind to act on (named missing piece M2).

SELECTOR MOTIVATIONS — STATED HERE, BEFORE ANY SCORE (discipline rule 1):
R4-S1a "cascade-generation direct": generation g = delta-cascade level; even-shell registration
  requires the round-trip doubling (R3), so rung(fermion)=2g; bosons carry no generation -> no
  rung. UNIFORM-AUDIT: DEAD BEFORE SCORING — the cascade<->generation offset is unowned; three
  equally natural readings (cascade exponent -3g; -3(g+1); zone address 9/11/13) give parity
  patterns (odd,even,odd)/(even,odd,even)/(odd,odd,odd) and the orientation rung=2g vs 2(4-g)
  is equally free. Scored anyway as a control (both orientations).
R4-S1b: same principle, reversed orientation rung=2(4-g).
R4-S2 "charge-branch": the owned A2 axis projection writes charge in thirds (BOOK_04:910);
  branch multiplicity n=|3Q|; round-trip doubling -> rung=2n, seat iff rung in {2,4,6}.
  UNIFORM-AUDIT: CLEAN (|3Q| is single-valued per slot; the Y-reading is audit-dead because
  each quark carries two Weyl hypercharges; the T3-reading leaves bosons ill-typed). The one
  audit-clean root-connected uniform selector found.
R4-S3a "sheet-cycle order": rung = the slot's owned winding order; even order -> direct seat
  (R6), odd order -> round-trip doubled (R3); no owned order -> no seat. e:0->phi^0->no shell;
  mu:4->rung4; tau:3->doubled->rung6. This MECHANIZES skeptic #1's mu-seat wound: the owned
  sheet keying uniformly applied SEATS mu at rung 4 (=A) — the flagship {mu} exclusion is
  anti-derived. R4-S3b variant: odd order -> excluded (tau out).
R4-S4 "K1-compliant zone control": obey the ONLY owned radial object m_rad
  (9->B, 11->A, 13->C); fermions at zone(gen); H->13->C (REM 04.6.M1.Lambda); gamma,W,Z have
  no owned zone -> no seat. Shows what obeying the owned object buys.
R4-L1 pair-placement audit (lemma, not a selector): the root asymmetry's ONLY two-valued
  structure is the branch pair; doubled branch-degree pairs give rung-sets {2,4} (direct+return),
  {4,6} (return+gap), {2,6} (direct+gap). Nothing owned selects among the three; the target
  needs {4,6}. The down-pair placement is a 1-of-3 fitted joint — same shape as the killed
  bijection joint.
CEILING "affine class": every uniform map rung=2*(a*g+b*n+c) over the owned integer fields
  (g=generation, n=|3Q|), a,b in {-2..2}, c in {-4..8}, bosons under both conventions
  (excluded / n-only), seat iff value in {1,2,3}. Charged as a CLASS (max k reported, nothing
  selected from it). Single-valuedness lemma: no function slot->one rung can match the target's
  b,d double-membership, so every class member has k_exact <= 11.
REFRAME VALUE-ECHO TESTS (computable under the frozen protocol, per (d)):
  E1: fitted circle-size exponents log_phi(r) vs (2,4,6);
  E2: LOO stability of the exponent triple (13 folds, prereg Q2b machinery);
  E3: mass-scramble null for the even-exponent echo (200 seeded draws): fraction of scrambles
      whose sorted exponent triple is as close to (2,4,6) as the real one.

Scoring metric FROZEN = attempt-1/3 metric: per-slot seat-SET equality (exact), nonempty proper
subset = partial; k* = exact count; null p = P(family member agrees with the TARGET on >= k*
slots), computed over BOTH exact families: fixed-excluded 69,300 and free-excluded 5,405,400
(skeptic #1's family; cross-checks asserted: hist 13->1, 12->0, 11->66).
"""
import itertools
import math
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, "/Users/grigorijvahrusev/Downloads/d0_15/_TASKS_CENTER_ATTACK")
from shell_membership_v2 import (FROZEN, PHI, all_assignments, build_nodes,
                                 load_masses)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

NAME = {1: "gam", 2: "b", 3: "d", 4: "tau", 5: "W", 6: "mu", 7: "s", 8: "c",
        9: "Z", 10: "e", 11: "u", 12: "t", 13: "H"}
# seat masks: A=1, B=2, C=4, excluded=0
TARGET = {1: 1, 2: 5, 3: 5, 4: 2, 5: 2, 6: 0, 7: 0, 8: 2, 9: 2, 10: 1, 11: 1,
          12: 4, 13: 4}
GEN = {2: 3, 3: 1, 4: 3, 6: 2, 7: 2, 8: 2, 10: 1, 11: 1, 12: 3}  # fermions only
N3Q = {1: 0, 2: 1, 3: 1, 4: 3, 5: 3, 6: 3, 7: 1, 8: 2, 9: 0, 10: 3, 11: 2,
       12: 2, 13: 0}  # |3Q| per slot
RUNG2MASK = {2: 2, 4: 1, 6: 4}  # reframe identification: rung phi^2=B, phi^4=A, phi^6=C
                                 # (fixed by the radius VALUES r_B<r_A<r_C = phi^2<phi^4<phi^6,
                                 #  the passport's own convention — not fitted per selector)


def agree(pred):
    """exact / partial / miss counts vs TARGET under the frozen metric."""
    k = p = 0
    for s in range(1, 14):
        pm, tm = pred[s], TARGET[s]
        if pm == tm:
            k += 1
        elif pm != 0 and (pm & tm) == pm:
            p += 1
    return k, p


# ---------------------------------------------------------------- selectors
def sel_S1a():
    pred = {s: 0 for s in range(1, 14)}
    for s, g in GEN.items():
        pred[s] = RUNG2MASK.get(2 * g, 0)
    return pred


def sel_S1b():
    pred = {s: 0 for s in range(1, 14)}
    for s, g in GEN.items():
        pred[s] = RUNG2MASK.get(2 * (4 - g), 0)
    return pred


def sel_S2():
    pred = {}
    for s in range(1, 14):
        pred[s] = RUNG2MASK.get(2 * N3Q[s], 0)
    return pred


def sel_S3(double_odd=True):
    pred = {s: 0 for s in range(1, 14)}
    pred[6] = RUNG2MASK[4]                      # mu: 4-cycle -> rung 4
    pred[4] = RUNG2MASK[6] if double_odd else 0  # tau: 3-cycle -> doubled 6 | excluded
    pred[10] = 0                                 # e: unramified 0 -> phi^0 -> no shell
    return pred


def sel_S4():
    m_rad = {1: 2, 2: 1, 3: 4}  # zone(gen): g1->9->B, g2->11->A, g3->13->C (owned strictMono)
    pred = {s: 0 for s in range(1, 14)}
    for s, g in GEN.items():
        pred[s] = m_rad[g]
    pred[13] = 4  # H -> zone 13 -> C (REM 04.6.M1.Lambda)
    return pred


SELECTORS = [
    ("R4-S1a cascade-gen direct (AUDIT-DEAD: offset trilemma; control)", sel_S1a()),
    ("R4-S1b cascade-gen reversed (AUDIT-DEAD: same; control)", sel_S1b()),
    ("R4-S2 charge-branch 2|3Q| (AUDIT-CLEAN)", sel_S2()),
    ("R4-S3a sheet-order, odd doubled (mechanized mu-wound)", sel_S3(True)),
    ("R4-S3b sheet-order, odd excluded", sel_S3(False)),
    ("R4-S4 K1-compliant zone control (m_rad)", sel_S4()),
]


# ---------------------------------------------------------- exact null families
def family_hist_fixed():
    assigns = all_assignments()
    assert len(assigns) == 69300, len(assigns)
    frozen = (tuple(sorted(FROZEN["A"])), tuple(FROZEN["B"]), tuple(sorted(FROZEN["C"])))
    assert frozen in assigns
    hist = Counter()
    for A, B, C in assigns:
        pred = {s: 0 for s in range(1, 14)}
        for s in A:
            pred[s] |= 1
        for s in B:
            pred[s] |= 2
        for s in C:
            pred[s] |= 4
        hist[sum(pred[s] == TARGET[s] for s in range(1, 14))] += 1
    return hist


def family_hist_free():
    """free-excluded family: excluded pair over C(13,2); sizes 5/4/4, |A^C|=2. 5,405,400 total."""
    slots = list(range(1, 14))
    t = TARGET
    hist = Counter()
    for E in itertools.combinations(slots, 2):
        base = sum(t[x] == 0 for x in E)
        pool = [s for s in slots if s not in E]
        t5 = {s: int(t[s] == 5) for s in pool}
        t1 = {s: int(t[s] == 1) for s in pool}
        t4 = {s: int(t[s] == 4) for s in pool}
        t2 = {s: int(t[s] == 2) for s in pool}
        for S in itertools.combinations(pool, 2):
            aS = base + t5[S[0]] + t5[S[1]]
            rest = [s for s in pool if s not in S]
            for Aex in itertools.combinations(rest, 3):
                aA = aS + sum(t1[s] for s in Aex)
                rem = [s for s in rest if s not in Aex]
                T2rem = sum(t2[s] for s in rem)
                for Cex in itertools.combinations(rem, 2):
                    a = aA + t4[Cex[0]] + t4[Cex[1]] + T2rem - t2[Cex[0]] - t2[Cex[1]]
                    hist[a] += 1
    total = sum(hist.values())
    assert total == 5405400, total
    assert hist[13] == 1 and hist[12] == 0 and hist[11] == 66, dict(hist)  # skeptic #1 x-checks
    return hist


def p_tail(hist, k):
    tot = sum(hist.values())
    return sum(v for a, v in hist.items() if a >= k) / tot, tot


# ------------------------------------------------------------- affine ceiling
def affine_ceiling():
    best = (-1, None)
    seen = set()
    n_scored = 0
    for a in range(-2, 3):
        for b in range(-2, 3):
            for c in range(-4, 9):
                for bos in ("excluded", "n-only"):
                    pred = {}
                    for s in range(1, 14):
                        if s in GEN:
                            v = a * GEN[s] + b * N3Q[s] + c
                        elif bos == "n-only":
                            v = b * N3Q[s] + c
                        else:
                            pred[s] = 0
                            continue
                        pred[s] = RUNG2MASK.get(2 * v, 0)
                    key = tuple(pred[s] for s in range(1, 14))
                    if key in seen:
                        continue
                    seen.add(key)
                    n_scored += 1
                    k, part = agree(pred)
                    assert k <= 11, "single-valued map matched a doubled slot exactly?!"
                    if k > best[0]:
                        best = (k, (a, b, c, bos, part))
    return best, n_scored


# ------------------------------------------------------------- reframe echoes
def fit_circle(pts):
    x, y = pts[:, 0], pts[:, 1]
    M = np.column_stack([2 * x, 2 * y, np.ones_like(x)])
    cx, cy, c = np.linalg.lstsq(M, x * x + y * y, rcond=None)[0]
    return cx, cy, math.sqrt(max(0.0, cx * cx + cy * cy + c))


def exponents(nodes, drop=None):
    out = []
    for lab in ("B", "A", "C"):
        pts = np.array([nodes[s] for s in FROZEN[lab] if s != drop])
        if len(pts) < 3:
            return None
        r = fit_circle(pts)[2]
        out.append(math.log(r) / math.log(PHI) if r > 1e-12 else float("-inf"))
    return out


def main():
    print("=== SHELL-RULE-R ATTEMPT 4 — root-asymmetry selectors vs frozen target ===")
    print("target masks:", {NAME[s]: TARGET[s] for s in range(1, 14)})

    print("\n[audit] R4-S1 cascade<->generation offset trilemma (parity of the cascade phi-"
          "exponent per generation):")
    print("  reading 1: exponent -3g       -> parities (odd,even,odd)   for g=1,2,3")
    print("  reading 2: exponent -3(g+1)   -> parities (even,odd,even)")
    print("  reading 3: zone address 9/11/13 -> parities (odd,odd,odd)")
    print("  three equally-natural readings, three parity patterns -> connective DEAD (c).")

    print("\n[audit] R4-L1 pair placement from the root two-valuedness (doubled degree pairs):")
    for pair, rungs in [("direct+return", (2, 4)), ("return+gap", (4, 6)),
                        ("direct+gap", (2, 6))]:
        m = RUNG2MASK[rungs[0]] | RUNG2MASK[rungs[1]]
        hits = sum(m == TARGET[s] for s in (2, 3))
        print(f"  {pair:14s} -> rungs {rungs} mask {m}: matches b,d on {hits}/2 slots")
    print("  nothing owned selects among the three -> down-pair seat = 1-of-3 fitted joint.")

    print("\n[null] enumerating exact families...")
    hf = family_hist_fixed()
    hF = family_hist_free()
    print(f"  fixed-excluded family: 69300; agreement-with-target hist "
          f"{dict(sorted(hf.items()))}")
    print(f"  free-excluded family: 5405400; top of hist "
          f"{{13:{hF[13]}, 12:{hF[12]}, 11:{hF[11]}, 10:{hF[10]}}} (skeptic x-checks PASS)")
    mean_fixed = sum(a * v for a, v in hf.items()) / 69300
    mean_free = sum(a * v for a, v in hF.items()) / 5405400
    print(f"  chance level: mean agreement fixed={mean_fixed:.3f}, free={mean_free:.3f}; "
          f"fixed-family FLOOR = {min(hf)} (excluded {{mu,s}} always agrees)")

    print("\n[scores] selector | exact | partial | p_fixed(>=k) | p_free(>=k)")
    for name, pred in SELECTORS:
        k, part = agree(pred)
        pf, _ = p_tail(hf, k)
        pF, _ = p_tail(hF, k)
        tab = " ".join(f"{NAME[s]}:{pred[s]}" for s in range(1, 14))
        print(f"  {name}")
        print(f"    table [{tab}]")
        print(f"    k={k}/13 partial={part}  p_fixed={pf:.4f}  p_free={pF:.4f}")

    (bk, meta), n_cls = affine_ceiling()
    pf, _ = p_tail(hf, bk)
    pF, _ = p_tail(hF, bk)
    print(f"\n[ceiling] affine class over (g,|3Q|): {n_cls} distinct assignments scored; "
          f"max k_exact = {bk}/13 at (a,b,c,bosons,partials)={meta}")
    print(f"  class-max tail: p_fixed={pf:.4f}, p_free={pF:.4f}; single-valued bound k<=11 "
          f"verified over the whole class (b,d doubling unreachable)")

    print("\n[reframe] E1 — circle-size exponents log_phi(r), frozen fit:")
    masses = load_masses()
    core = [12, 5, 1, 15, 24, 13, 3, 4, 23, 11, 2, 6, 25]
    slot_mass = {i + 1: masses[p] for i, p in enumerate(core) if p in masses}
    slot_mass.pop(1, None)
    nodes = build_nodes(slot_mass)
    e_obs = exponents(nodes)
    dev = [e_obs[i] - t for i, t in enumerate((2, 4, 6))]
    T_obs = max(abs(d) for d in dev)
    print(f"  (e_B,e_A,e_C) = ({e_obs[0]:.3f},{e_obs[1]:.3f},{e_obs[2]:.3f}) vs (2,4,6); "
          f"devs=({dev[0]:+.3f},{dev[1]:+.3f},{dev[2]:+.3f}); T_obs={T_obs:.3f}")
    cs = {lab: fit_circle(np.array([nodes[s] for s in FROZEN[lab]])) for lab in "ABC"}
    seps = {p: math.dist(cs[p[0]][:2], cs[p[1]][:2]) for p in ("AB", "AC", "BC")}
    print(f"  centers NOT concentric: |cA-cB|={seps['AB']:.2f} |cA-cC|={seps['AC']:.2f} "
          f"|cB-cC|={seps['BC']:.2f} vs r_B={cs['B'][2]:.2f} — strata reading is size-ratio only")

    print("\n[reframe] E2 — LOO exponent stability (13 folds; nearest-integer rounding):")
    stable = 0
    for drop in range(1, 14):
        e = exponents(nodes, drop=drop)
        rnd = tuple(round(x) for x in e)
        ok = rnd == (2, 4, 6)
        stable += ok
        print(f"  drop {NAME[drop]:>3s}: ({e[0]:6.3f},{e[1]:6.3f},{e[2]:6.3f}) -> {rnd} "
              f"{'OK' if ok else 'BREAK'}")
    print(f"  rounding stable (2,4,6) in {stable}/13 folds")

    print("\n[reframe] E3 — mass-scramble null for the even-exponent echo (200 draws, "
          "seed 20260704):")
    rng = np.random.default_rng(20260704)
    slots = sorted(slot_mass)
    vals = [slot_mass[s] for s in slots]
    hit_246 = hit_even = 0
    for _ in range(200):
        nod = build_nodes(dict(zip(slots, rng.permutation(vals))))
        e = exponents(nod)
        if e is None or any(math.isinf(x) for x in e):
            continue
        es = sorted(e)
        T = max(abs(es[i] - t) for i, t in enumerate((2, 4, 6)))
        Te = max(abs(x - 2 * round(x / 2)) for x in es)
        hit_246 += T <= T_obs
        hit_even += Te <= T_obs
    print(f"  P(scramble sorted-exponents within T_obs of (2,4,6)) = {hit_246}/200 = "
          f"{hit_246/200:.3f}")
    print(f"  P(scramble exponents all within T_obs of SOME even ints) = {hit_even}/200 = "
          f"{hit_even/200:.3f}")

    print("\n[verdict] see SHELL_RULE_R_LEDGER.md Attempt 4 record.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
