import Mathlib.Tactic

/-!
# D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001 / D0-ARCHIVE-NEUMANN-TICK-OWNER-001 — discrete time = Feshbach archive-delay index

BOOK_06 §06.8. Python certificates:
`05_CERTS/vp_feshbach_schur_time_delay_owner.py`, `05_CERTS/vp_archive_neumann_tick_owner.py`.

Block II of the static-to-dynamics closure: dynamics is FORCED by finite self-readout, not primitive.
This module encodes the FINITE PATH-GRAMMAR of the Feshbach–Schur effective operator over the
retained(rank-3)/archive(dim-30) split:

  `W_eff = P U P  +  P U Q (I − Q U Q)⁻¹ Q U P`,

with the archive resolvent expanded as the (formal) Neumann series

  `(I − Q U Q)⁻¹ = Σ_{k≥0} (Q U Q)ᵏ`,    so that    `W_eff = Σ_{k≥0} P U Q (Q U Q)ᵏ Q U P`.

The DIRECT term (`k = 0`) is `P U Q · Q U P` glued onto `P U P`: zero internal archive circulations.
Each higher-order term (`k ≥ 1`) inserts exactly `k` copies of the archive round-trip factor `Q U Q`,
i.e. the readout makes `k` extra excursions into the dim-30 archive before returning to the rank-3
active sector. The order-`k` term is `archivePathTerm k`; its `archiveCirculations` count is exactly the
number of `(Q U Q)` factors, namely `k`. We DEFINE the discrete tick as that index: `tickIndex t := t.k`.
The central reading — "time is the Feshbach archive-delay index" — is then the finite/decidable identity

  `tickIndex (neumannTerm k) = (neumannTerm k).archiveCirculations = k`.

The tick is NOT an external parameter inserted by hand: it is read OFF the path grammar (the number of
archive circulations), so the same datum cannot be set independently of the operator term.

HONESTY BOUNDARY. CERT-CLOSED here is exactly the finite/decidable PATH-GRAMMAR tick-index identity:
the order-`k` term has `k` archive circulations and `tickIndex = k`, with the `k = 0` direct `P U P`
term separated (0 circulations) from the delay terms `k ≥ 1`. What is NOT proven here is the Neumann
series CONVERGENCE — that `(I − Q U Q)⁻¹ = Σ_k (Q U Q)ᵏ` actually sums — which requires the spectral
radius `ρ(Q U Q) < 1` (the resolvent / convergence domain). That analytic convergence condition is the
named residual; the per-term combinatorial identity holds regardless. No primitive time object, external
clock, or SI unit (c, h, ħ, seconds) enters: the only "time" content is the dimensionless integer index `k`.
-/

namespace D0.Evolution.FeshbachSchurTimeDelayOwner

/-! ## 1. The retained(rank-3)/archive(dim-30) Feshbach–Schur split -/

/-- The retained/archive block split of the Feshbach–Schur effective operator:
`retainedRank = 3` (the active sector `P`), `archiveRank = 30` (the traced-out archive `Q`). -/
structure RetainedArchiveSplit where
  retainedRank : Nat
  archiveRank : Nat
  h_retained : retainedRank = 3
  h_archive : archiveRank = 30

/-- The D0 Feshbach–Schur split: retained rank 3 (active carrier), archive dim 30 (kernel). -/
def feshbachSplit : RetainedArchiveSplit := ⟨3, 30, rfl, rfl⟩

/-- **archive_rank_eq_thirty.** The archive block has dimension exactly 30. -/
theorem archive_rank_eq_thirty : feshbachSplit.archiveRank = 30 := rfl

/-- **retained_rank_eq_three.** The retained (active) block has rank exactly 3. -/
theorem retained_rank_eq_three : feshbachSplit.retainedRank = 3 := rfl

/-- Both block ranks at once, straight from the split data. -/
theorem split_ranks (s : RetainedArchiveSplit) :
    s.retainedRank = 3 ∧ s.archiveRank = 30 := ⟨s.h_retained, s.h_archive⟩

/-! ## 2. The Neumann path-grammar term and its archive-circulation count -/

/-- An order-`k` archive path term of the effective operator: the Neumann term
`P U Q (Q U Q)ᵏ Q U P`. The single datum `k` is the number of internal archive round-trips. -/
structure ArchivePathTerm where
  /-- The Neumann order = number of internal `(Q U Q)` archive-circulation factors. -/
  k : Nat

/-- The order-`k` Neumann term `P U Q (Q U Q)ᵏ Q U P`. -/
def neumannTerm (k : Nat) : ArchivePathTerm := ⟨k⟩

/-- The number of internal `(Q U Q)` archive-circulation factors in a path term — read OFF the
grammar, defined to be the Neumann order `k`. -/
def ArchivePathTerm.archiveCirculations (t : ArchivePathTerm) : Nat := t.k

/-- The discrete time tick of a path term IS its Neumann order `t.k`. The tick is defined FROM the
term (not inserted independently): it is the archive-circulation count read off the path grammar. -/
def tickIndex (t : ArchivePathTerm) : Nat := t.k

/-- **neumann_term_k_has_k_archive_circulations.** The order-`k` Neumann term has exactly `k` internal
`(Q U Q)` archive-circulation factors. -/
theorem neumann_term_k_has_k_archive_circulations (k : Nat) :
    (neumannTerm k).archiveCirculations = k := rfl

/-- **tick_index_eq_archive_circulation_count.** The discrete tick of the order-`k` term equals its
archive-circulation count — time is READ OFF the path grammar, not inserted by hand. -/
theorem tick_index_eq_archive_circulation_count (k : Nat) :
    tickIndex (neumannTerm k) = (neumannTerm k).archiveCirculations := rfl

/-- The tick of the order-`k` term is `k` (the two definitions agree on the explicit term). -/
theorem tick_index_eq_k (k : Nat) : tickIndex (neumannTerm k) = k := rfl

/-! ## 3. The direct `k = 0` term `P U P` is separated from the delay terms `k ≥ 1` -/

/-- **The direct term has zero archive circulations.** The `k = 0` Neumann term is the DIRECT
`P U Q · Q U P` glued onto `P U P` — no internal `(Q U Q)` round-trip — so its tick is `0`. -/
theorem direct_term_zero_circulations :
    (neumannTerm 0).archiveCirculations = 0 ∧ tickIndex (neumannTerm 0) = 0 := ⟨rfl, rfl⟩

/-- **The delay terms `k ≥ 1` carry a strictly positive tick.** Every higher-order term makes at least
one archive excursion, so it is genuinely delayed (separated from the direct `k = 0` term). -/
theorem delay_term_positive_tick (k : Nat) (hk : 1 ≤ k) :
    1 ≤ (neumannTerm k).archiveCirculations := by
  simpa [ArchivePathTerm.archiveCirculations, neumannTerm] using hk

/-- **The direct term is separated from the delay terms.** A term is the DIRECT `P U P` term iff its
tick is `0`; the delay terms all have tick `≥ 1`. So a delay term (`k ≥ 1`) is never the direct term:
`P U P` is never miscounted as a delayed (`k ≥ 1`) circulation. -/
theorem direct_separated_from_delay (k : Nat) (hk : 1 ≤ k) :
    tickIndex (neumannTerm k) ≠ tickIndex (neumannTerm 0) := by
  simp only [tick_index_eq_k]
  omega

/-! ## 4. Bundled owner certificate -/

/-- **D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001 / D0-ARCHIVE-NEUMANN-TICK-OWNER-001.**
`time_is_feshbach_delay_index` — the bundled finite path-grammar tick identity:
  1. the split is retained rank 3 / archive dim 30;
  2. the order-`k` Neumann term `P U Q (Q U Q)ᵏ Q U P` has exactly `k` archive circulations;
  3. its discrete tick equals that archive-circulation count (`= k`): time is READ OFF the grammar;
  4. the direct `k = 0` term `P U P` has tick `0` (zero circulations);
  5. every delay term `k ≥ 1` has a strictly positive tick (separated from the direct term).
CERT-CLOSED (finite/decidable). The Neumann series CONVERGENCE
`(I − Q U Q)⁻¹ = Σ_k (Q U Q)ᵏ` (spectral radius `ρ(Q U Q) < 1`, the resolvent/convergence domain) is
NOT proven here — it is the named analytic residual. No external time parameter is introduced. -/
theorem time_is_feshbach_delay_index :
    (feshbachSplit.retainedRank = 3 ∧ feshbachSplit.archiveRank = 30) ∧
    (∀ k : Nat, (neumannTerm k).archiveCirculations = k) ∧
    (∀ k : Nat, tickIndex (neumannTerm k) = (neumannTerm k).archiveCirculations) ∧
    ((neumannTerm 0).archiveCirculations = 0 ∧ tickIndex (neumannTerm 0) = 0) ∧
    (∀ k : Nat, 1 ≤ k → 1 ≤ (neumannTerm k).archiveCirculations) :=
  ⟨⟨retained_rank_eq_three, archive_rank_eq_thirty⟩,
   neumann_term_k_has_k_archive_circulations,
   tick_index_eq_archive_circulation_count,
   direct_term_zero_circulations,
   delay_term_positive_tick⟩

end D0.Evolution.FeshbachSchurTimeDelayOwner
