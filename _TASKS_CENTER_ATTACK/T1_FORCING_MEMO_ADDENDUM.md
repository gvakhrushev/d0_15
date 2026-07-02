# T1 MEMO ADDENDUM — self-adversarial review result: a named hole and a revised candidate

**Author:** chief researcher, reviewing own memo per §05.8.R (a critique must name a second object or
a named gap — both are done below). Status: DRAFT; no registry row edited.

## The hole in the original memo (named second object)

Original case (B) argued: a return-containing family needs a *new* weight parameter ⇒ exogenous ⇒ ⊥M1.
This fails for one specific value: a return weight **derivable from the grammar itself**. The named
second object is the **Bartholdi zeta** ζ(u,t) — the two-parameter extension of the Ihara zeta in
which the parameter t weights exactly the backtrack (bump) occurrences (Bartholdi 1999; Mizuno–Sato).
Its determinant identity, **verified numerically on K(9,11,13)** at 5 points including both
degenerations (scratchpad `bartholdi_check.py`):

```
det(I − u(B + tR)) = (1 − (1−t)²u²)^(|E|−|V|) · det(I − uA + (1−t)(D − (1−t)I)u²)
```

where R is the backtrack involution on directed edges. At t = 0 this is Ihara–Bass (NB); at t = 1 it
is the all-walks side. So W, NB, E are not three rival families — they are **specializations of one
two-parameter object**, and the real question is: which t is M1-admissible?

## The revised candidate (golden Bartholdi point)

The D0 closure equation p + p² = 1 says: the unique t ∈ (0,1) with **1 − t = t²** is t = φ⁻¹ = p.
Weight bookkeeping: if an ordinary step carries the direct-channel weight and a return step carries
one extra factor p (making the return pair weigh p·p² relative bookkeeping), the Bartholdi bump
parameter is exactly t = p. At the golden point the identity specializes to

```
det(I − u(B + pR)) = (1 − p⁴u²)^326 · det(I − uA + p²(D − p²I)u²)
```

— the vertex-side backtrack correction carries **precisely the typed channel weight p²**, and the
trivial-cycle factor carries p⁴ = (p²)² (the double return). Nothing is imported: every constant is
a power of φ⁻¹ forced upstream.

**Revised claim X′ (candidate, replaces X of the original memo):** the scene-native refinement rule
is the directed-edge carrier with the **typed Bartholdi transfer B_p = B + pR**; the typing t is
forced to p by the closure equation (1−t = t² *is* p+p²=1); the untyped specializations are both
inadmissible — t = 1 (W/E) assigns the return act the untyped weight 1 (not its grammar weight,
outcome-affecting, underivable ⇒ exogenous), and t = 0 (pure NB) erases a channel the grammar owns
(single-ledger undercount) *unless* the corpus reads the history layer and the channel layer as
separate ledgers.

## The decision point the corpus must answer (named gap)

Between X (NB, t=0) and X′ (golden, t=p) the discriminating question is **single-ledger vs
two-ledger**: is the refinement family required to *contain* the return channel with its grammar
weight (single ledger ⇒ t = p forced), or does it *compose* with a separately-carried p²-channel
(two ledgers ⇒ t = 0 forced, and the Bass factor is the composition seam)? This is a corpus-level
typing question (BOOK_00 §00.3 channel grammar vs vNext2 history-tower construction), not a
computation. Until it is answered, T1 stands as: **the admissible set is exactly {t=0, t=p} — a
two-completion situation in the sense of D0-COMPLETION-ADMISSIBILITY-001 — with all other t
(including t=1, i.e. W and E) excluded by the exogenous-weight blade.** That is already strictly
stronger than the recorded Outcome D (which held W, NB, E all admissible), and is honest about what
remains.

Note the structural bonus in either resolution: the Bartholdi identity itself is the comparison map
Ξ (718 ↔ 33) for *every* t, so `PRIM-COMPARISON-MAP-XI-N` has a single candidate owner regardless of
which completion wins.

## Verification obligations created (fed to TASK W7)

1. Exact (ℚ(φ)) verification of the Bartholdi identity and its golden specialization on the scene.
2. Exact statement sourcing (Bartholdi 1999; Mizuno–Sato) — hypotheses, conventions (bump counting,
   cyclic vs path), md≥2 applicability.
3. Spectral fingerprint of B_p and of the golden vertex-side polynomial; comparison against owned
   invariants (report-only; no promotion). Numeric preview: Perron(B_p) ≈ 21.4540 vs Perron(B) ≈
   20.8335, Perron(A) ≈ 21.8374.
