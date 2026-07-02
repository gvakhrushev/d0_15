# R1 λ-CLOSURE — the coprimality forcing of λ = 1 (DRAFT, submitted to skeptic with the full R1 package)

**Author:** chief researcher. Status: DRAFT candidate theorem; no registry row edited. Builds on
`R1_SCOUT_MEMO.md` and `R1_SUBFORCINGS_AND_LAMBDA.md`; the fork named there (common-λ vs zone
lattices) is resolved here into a conjunction with an exact consequence.

## Claim Λ1

The holonomy of the unified chain is forced: **λ = 1**. The chain's CONDITIONAL-EXTENSION marker,
on its holonomy leg, is dischargeable; the λ=1 slice (`TerminalReturn.lean`, the bare Umu/Utau —
exactly the slice where the holomorph weld `Umu = L_i|⟨i⟩-span` lives) is not a convenience but the
forced point.

## The three legs

**Leg 1 — single λ (single holonomy section).** DEF-0.2.2: assume two independent holonomies
λ_μ ≠ λ_τ. Each is outcome-affecting (dressed factors, spectra). Two independent underivable
phases = two exogenous parameters where at most one section is admissible — the same blade that
bans a second action/mass anchor (§03.16.B single-section discipline; a second independent
holonomy is a second calibration section). One λ survives. [Risk: §03.16.B's owned scope is
*dimensional* anchors; the extension to phase sections must be argued, not cited — named gap G1.]

**Leg 2 — per-zone registrability (the N=D extension, the load-bearing step).** §01.22 owns
(CORE-FORCING) the phase-circle discretization for the base zone: N < D glues addresses (⊥M1),
N > D needs a significance catalog (⊥M1), so N = D. Extension claimed: a return-cycle holonomy is
a phase **registered by the zone its circuit saturates** — the corpus's own q_T derivation reads
zone 11 as the phase register of the first moving shell (q_T = lcm(|ABCD|, V₁₁): the window
multiplies the cycle period by the zone's address count). A phase off the zone's D_Z-lattice is
either indistinguishable from its lattice representative (then M1+ canonicalizes TO the lattice
point — no content) or claims a sub-address distinction requiring an external resolution catalog
(⊥M1). Hence a holonomy registered at zone Z lies in μ_{D_Z}. The μ-circuit saturates zone 11 and
the τ-circuit zone 13, and the single λ of Leg 1 is registered at BOTH: λ ∈ μ₁₁ ∩ μ₁₃.
[Risks, named: G2 — the §01.22 blades are stated for the addressor cycle γ*, not for branch
holonomies; the extension sentence above is new forcing text, the skeptic's primary target.
G3 — the μ-circuit passes through V₉ too; if the register is the joint one (V₉×V₁₁), the lattice
is μ₉₉ etc.; then Leg 3 still closes via gcd(99, 117) = 9... NOT 1 — the joint-register reading
does NOT trivially close and must be excluded or handled; recorded honestly.]

**Leg 3 — coprimality (arithmetic).** gcd(11,13) = 1 ⇒ μ₁₁ ∩ μ₁₃ = {1} ⇒ **λ = 1**. (All three
zone counts are pairwise coprime — 9/11/13 — so any two-zone registration closes the same way;
the +2-ladder's coprimality is doing physical work here.) [No risk; integer arithmetic.]

## What closes if Λ1 survives review

1. The holonomy leg of `D0-EDGE-COVER-FAMILY-001`'s conditionality is discharged: the family
   collapses to its λ=1 member — which is the corpus's own already-written bare slice.
2. The holomorph module's λ=1-slice caveat (carried since `TASK_W8_REPORT.md`) dissolves: the
   weld `Umu = L_i|⟨i⟩-span` sits at the forced point.
3. With sub-forcing A (½-port) the R_* leg is also candidate-discharged; the unified chain's
   CONDITIONAL marker would then rest on the **contact leg alone** — the same single bit as
   `T2_PRIME_FINAL_STATE.md` R1-core. The programme's entire residual would then be: one contact
   bit (+ R2's mechanical Lean attachment).
4. A falsification hook exists: if any owned window or passport REQUIRES λ ≠ 1 (a nontrivial
   dressed-phase effect), Λ1 dies — reviewers should search for such a requirement; none is known
   to the author (the books introduce TerminalReturn at λ=1 as the bare case).

## Interaction with the lattice finding's 44-weld (honest accounting)

The μ₁₁-weld of `R1_SUBFORCINGS_AND_LAMBDA.md` (zeros on the 2π/44 lattice = q_T) was evidence for
the lattice READING; at the forced point λ=1 the factor zeros sit on the 4-lattice and the owned
44-window arises from the §01.22 capacity route independently. No circularity: the lattice reading
constrains WHERE λ may sit; coprimality selects the point; the 44-window never enters the forcing.
The 39-flag of the previous memo becomes moot at λ=1 (no prediction is owed); it stays recorded
only as a consequence the zone-lattice reading WOULD have had at a nontrivial point.

## Named gaps for the skeptic (complete list)

G1 (Leg 1 scope extension: dimensional → phase sections), G2 (N=D extension to branch holonomies —
the load-bearing new text), G3 (joint-register alternative: μ₉₉-type lattices, where coprimality
FAILS — gcd(99, 117) = 9; this alternative must be killed by a named argument or Λ1 is a
two-completion, {λ=1} vs {λ ∈ μ₉ at the joint register}), G4 (any owned λ≠1 requirement anywhere
in the corpus — the falsification sweep).
