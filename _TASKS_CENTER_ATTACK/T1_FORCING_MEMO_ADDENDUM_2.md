# T1 ADDENDUM 2 — ledger question resolved into presentation covariance (candidate X″)

**Author:** chief researcher. Status: DRAFT; no registry row edited. Supersedes the "single-ledger vs
two-ledger" framing of Addendum 1 after corpus-evidence collection.

## 1. What the corpus actually says about weight bookkeeping (quotes)

- **BOOK_01 §01.6.1a (Route A):** "Memory of depth 1 admits exactly two channels: direct registration
  of weight `p`, and the first self-return of weight `p²`." — the return channel's `p²` is the square
  of the step weight: compositional, not a separate stamp.
- **BOOK_03 §03.3.0:** the history weight is forced `w(γ) = φ^{−S(γ)}` by multiplicativity +
  additivity of cost + unique sum-to-product map; **§03.3 line 29 defines the admissible histories
  `Γ_D(k)` WITH their weights** — histories are weighted objects in the owned construction.
- **BOOK_03 §03.3.0a:** `S(γ) = Σ_e Cost(e) − Σ_v Info(v)`; "at each branch the history commits a
  choice (a bit)" — Info is booked per committed choice (per visit), and both advance and return
  commit a choice.
- **BOOK_06 §06.8 Block III:** "each archive-delay tick multiplies the active amplitude by φ⁻¹" —
  in the Feshbach expansion each extra circulation is one extra `U`-factor: again one factor per act.

Conclusion: **the owned bookkeeping is uniformly compositional** — weight = product over acts, typing
of channels is positional (which act-sequence), never an extra weight stamp on the return act. In
Bartholdi coordinates this is the t = 1 bookkeeping. (The golden point t = p of Addendum 1 revives
only under a first-visit reading of Info — see §4.)

## 2. New verified fact: the three vNext2 families are one object

At t = 1 the Bartholdi identity degenerates to `det(I − u(B+R)) = det(I − uA)`. Verified directly on
K(9,11,13) (float, 3 rational u, plus full spectrum): **the nonzero spectrum of the full directed-edge
transfer B+R (the E family, dim 718) is exactly the nonzero spectrum of the adjacency A (the W
family, dim 33)** — {21.837, −9.758, −12.079}, the vacuum-cubic roots — plus zeros. Together with
W1's exact Ihara–Bass verification (t = 0), the map of presentations is:

```
one weighted history ledger (owned, §03.3)
 ├─ vertex presentation   (W):  det(I − uA)                      dim 33
 ├─ edge presentation     (E):  det(I − u(B+R)) = det(I − uA)     dim 718, same nonzero spectrum
 └─ factored presentation (NB): det(I − uB) = Bass factor × det(I − uA + u²(D−I))   dim 718
```

The vNext2 inequivalences ("depth-2 carriers 15708 ≠ 14990; transfer dims 33 ≠ 718") are
carrier-bookkeeping differences between presentations of this single object, and the identity family
supplies the intertwining determinants.

## 3. The forcing sketch (DEF-0.2.2, replaces the original memo's case analysis)

Assume ¬X″: the refinement rule must *select one* presentation as physical. The selection label
("which presentation") changes no distinguishable outcome — the determinant/spectral identities above
are proved equalities. A mandatory-but-outcome-neutral structure is, by the dichotomy blade
(BOOK_00 §00.9, branch B), exactly a hidden external catalogue: ⊥M1. Hence no selection is
admissible; the forced object is the presentation-covariant class, and the canonical comparison map
`Ξ` is the identity family itself. **Outcome D is thereby re-read, not contradicted: vNext2 correctly
proved that no presentation is selected — because selection itself is M1-inadmissible.**

Candidate consequences (each needs the closure protocol before any status motion):
- `PRIM-SCENE-HISTORY-REFINEMENT-RULE` dissolves (the "missing rule" was a which-presentation label);
- `PRIM-COMPARISON-MAP-XI-N` acquires a single candidate owner: the Ihara–Bass/Bartholdi identity family;
- `PRIM-DIRAC-SCALE-SELECTION` to be re-examined as presentation gauge.

## 4. Honest residuals (named)

1. **Level of the intertwining.** The identities are det/spectral-level; the vNext2 hierarchy typing
   (compression < spectral < heat < Feshbach) demands more for the strong claims. Bass's block-matrix
   proof supplies explicit start/end maps between the edge and vertex carriers — these are the
   candidate conditional-expectation intertwiners; upgrading det-level to Ξ_N-level via those maps is
   the main remaining calculation (fed to TASK W7 step 1b).
2. **The Info-revisit fork.** §03.3.0a's per-choice reading gives t = 1 (this addendum). A first-visit
   reading ("a revisit distinguishes nothing new") gives bump suppression φ^{−Info(v)} — the golden
   point of Addendum 1. The fork needs its own owner; note the Ξ-claim of §3 is fork-independent
   (the identity family covers all t), so the presentation-covariance resolution is robust to it.
3. **Depth-2 carrier counts.** 15708 vs 14990 remain genuinely different STATE-SPACE sizes for tower
   construction; the claim here is that M1 forbids promoting either count to physical content without
   the intertwiner — not that the counts are equal.
