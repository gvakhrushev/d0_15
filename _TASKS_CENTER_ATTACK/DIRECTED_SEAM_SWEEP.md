# DIRECTED SEAM SWEEP — rounds 1–2 + the compression-washout theorem (record)

**Status:** sweep record (nulls are results); one new mini-theorem; no registry edit.
Scripts: `directed_seam_sweep.py` (round 1, exact), round-2 inline (float, reproducible).

## The compression-washout mini-theorem (new; provable from the Ξ-identities)

The canonical compressions of the ENTIRE Bartholdi family land inside the symmetric vertex
algebra: from the owned identities SB = AS − T, TB = (D−I)S, SJ = T, TJ = S, STᵀ = A, SSᵀ = TTᵀ = D:

```
T B Sᵀ = (D−I)·D,   S B Sᵀ = A·D − A,   T J Sᵀ = D,   S J Sᵀ = A,  …
```

— every word in {B, J} compressed through any of S,T on both sides is a word in ⟨A, D⟩, where the
seam vanishes identically (SEAM_LOCATION_THEOREM). **Directedness is washed out by the canonical
maps.** Verified round 1: seams of T·X·Sᵀ for X ∈ {B, B−J, B∘J} are identically zero. Consequence:
the α-seam is invisible to the whole canonical raw-graph layer — vertex algebra, edge family, AND
their Φ-compressions. Any realization must use within-zone-structured (Q₈-labeled) objects, which
are exactly the non-canonical (contact/terminal) layer.

## Round 2 (edge carrier, Q₈-contact split, directed Hashimoto archive): NULL

Seam nonzero (within-zone structure does reach it) but moments at degree scale:
(μ₁, μ₂, μ₃) ≈ (−133.4, 5884.9, −35205) [8-mode split] and (−90.4, 4280.4, −16211) [branch-only];
ratios ≈ −15 vs required 2457.6; μ₃ badly nonzero (no truncation). The natural directed owned
candidates fail all three constraints simultaneously.

## Honest state of the α-realization after the sweep

The three-way constraint set {directed + N-truncating, moment pair (1/3, 12288/5), through owned
carriers} has now survived: the symmetric class (impossible — theorem), the canonical raw layer
(seam-free — washout theorem), and the natural directed edge candidates (wrong scale, no
truncation — this sweep). **One named unswept corner remains:** directed archive blocks built from
the Q₈/holomorph structure inside the kernel's zone-9 block (the 8-dim difference space of V₉
contains the witness direction ⊕ E₄⊕E₃ — the holomorph module lives inside the owned dim-30
archive), with N-truncation from the owned SeamTransportLinear mechanism. If that corner also
nulls, the honest closing is the NO-GO: "no owned seam realizes the pair — ASSUMP-DIXMIER-TRACE is
irreducible," now backed by a swept candidate space rather than absence of attempts.
