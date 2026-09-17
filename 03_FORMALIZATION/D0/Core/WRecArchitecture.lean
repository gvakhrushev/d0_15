import D0.Core.WitnessForcing
import D0.Bridge.Assumptions.ClassRecordIsAddressable
import Mathlib.Tactic

/-!
# W-REC — the owned record/archive architecture (F4 Lean lift, leg-classified)

Lean lift of `CLOSE_GAP_W_MEMO.md` §2 (owned architecture) + §7 (obligations
OB-W1..OB-W3), statement structure per `F3_HONEST_BRIDGES_PACKAGE.md` TASK 3 (leg
classification L1–L7). Mirrors `close_gap_w_check.py` checks 1, 3, 4, 6.

**Book contract (citation, not a Lean claim):** `BOOK_01:31-34` — `H_N = H_N^ret ⊕ H_N^tr`,
`P_N + Q_N = I`, `P_N Q_N = 0`; `:37` — "`P_N` is the retained/readout projection, `Q_N`
is the traced/archive projection, `U_N` is the finite tick"; `F_N = P_N U_N† Q_N U_N P_N`
(`:40`, `:183`); retained-is-same-event `:186`/`:8`; archive-is-cross-event `:1995`;
single `Q_N`-writer `:1998`; `Δ` readout-side `:465`.

**Leg classification (the honesty spine of this module):**

* **L1 (PROVED, concrete model):** the record-support partition `P + Q = 1`, `P·Q = 0`
  on the pointed record support `Fin 9` (1 readout slot + 8 archive slots — the same
  `|V₉| = |Ω₈| + 1` shape as `WitnessForcing`). The IDENTIFICATION of `P`/`Q` with
  retained/traced (`:37`) is a book-contract citation in this docstring, not a Lean claim.
* **L2 = OB-W1 (PROVED, decidable, ℤ-scaled):** the `C₈` orbit-average is address-blind —
  `cAvgSum (marker a) = 1` for every address `a` (`cAvgSum = 8·cAvg`, kept over `ℤ` to
  keep the checker off `ℚ`; mirrors check 1).
* **L3 = OB-W2 (PROVED, decidable):** address markers and circulant (trace/content-side)
  matrices are TYPE-DISJOINT: no marker is shift-invariant, every circulant basis element
  is shift-invariant, nonzero, and not a marker (mirrors check 3).
* **L4 = OB-W3 (PROVED, decidable, ℤ-scaled):** averaging is idempotent on the matrix-unit
  basis — `cAvgSum (cAvgSum E) = 8 • cAvgSum E` — the escape-closure leg (a "separate
  downstream registration" reached through the trace inherits blindness; mirrors check 6).
* **L5 (EXPLICIT HYPOTHESIS, never a theorem):** the single-`Q_N`-writer SWEEP — a
  corpus-exhaustiveness fact (`CLOSE_GAP_W_MEMO.md` §2.1 disk sweep); Lean cannot decide
  what BOOK_01 does not contain. Carried as the `SingleQNWriterSweep` structure. No
  decidable shadow is built here (the F3 option is declined to avoid the shadow
  masquerading as the sweep).
* **L6 (EXPLICIT HYPOTHESIS):** `:988` — physicality ⇒ alters/constrains an addressable
  registration (the CORE contradiction theorem is cited, not formalized this wave).
* **L7 (EXPLICIT HYPOTHESIS):** R-A — the class-record IS an addressable registration:
  the registered ledger id `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE`
  (`D0.Bridge.ClassRecordIsAddressableAssumption`), un-owned and un-discharged.

**Honesty guard (F3 TASK 3, verbatim obligation):** `h_halt` is NOT promoted to a proved
term. The derivation chain G1 & G2 & G3 & W-REC ⇒ W-ELEM is certified propositionally by
`close_gap_w_check.py` check 5; its Lean form needs the un-owned R-A discharge and stays
hypothesis-shaped (memo `:406`). The capstone below is a thin re-export of the built
`card_base_forced_conditional` (`WitnessForcing.lean`) with the h_halt support
RE-ATTRIBUTED to "W-REC (L1–L4, proved here) + `:988` (L6) + R-A (L7) + single-writer
sweep (L5)" per `CLOSE_GAP_W_MEMO.md:402-406` — so `D0.All` sees ONE forcing statement,
not two competing ones.
-/

namespace D0.Core.WRecArchitecture

open Matrix

/-! ## L1 — the record-support partition on the concrete model -/

/-- Concrete record support: `Fin 9` = 1 retained/readout slot (`0`) + 8 traced/archive
slots (`1..8`) — the pointed-shell shape `|Ω₈| + 1`. Model choice, cited to `:33-34`. -/
abbrev RecordSupport := Fin 9

/-- Retained/readout projection (0/1 diagonal on slot `0`). -/
def Pret : Matrix RecordSupport RecordSupport ℤ :=
  Matrix.of fun i j => if i = j ∧ (i : ℕ) = 0 then 1 else 0

/-- Traced/archive projection (0/1 diagonal on slots `1..8`). -/
def Qtr : Matrix RecordSupport RecordSupport ℤ :=
  Matrix.of fun i j => if i = j ∧ (i : ℕ) ≠ 0 then 1 else 0

/-- **L1 (partition algebra, `BOOK_01:33-34` on the concrete model):**
`P + Q = 1` and `P·Q = 0` — the retained/traced split is an exact resolution of the
identity with orthogonal legs. -/
theorem retained_traced_partition :
    Pret + Qtr = (1 : Matrix RecordSupport RecordSupport ℤ) ∧ Pret * Qtr = 0 := by
  constructor
  · ext i j; revert i j; native_decide
  · ext i j; revert i j; native_decide

/-! ## L2/L3/L4 — the decidable obligations over the circulated sector `Fin 8` -/

/-- Address marker at `a`: the diagonal matrix unit `E_{aa}` over the 8 signed roles. -/
def marker (a : Fin 8) : Matrix (Fin 8) (Fin 8) ℤ :=
  Matrix.of fun i j => if i = a ∧ j = a then 1 else 0

/-- ℤ-scaled `C₈` orbit average: `cAvgSum M = Σ_k S^k M S^{-k}` entrywise
(`= 8 · cAvg M`; kept over `ℤ` so every leg is checker-friendly without `ℚ`). -/
def cAvgSum (M : Matrix (Fin 8) (Fin 8) ℤ) : Matrix (Fin 8) (Fin 8) ℤ :=
  Matrix.of fun i j => ∑ k : Fin 8, M (i - k) (j - k)

/-- **L2 = OB-W1 (marker-averaging is address-blind, mirrors check 1):** the full-cycle
average of EVERY address marker is the (scaled) uniform matrix — `cAvgSum (marker a) = 1`
for all `a`. Circulation erases WHICH address carried the mark. -/
theorem marker_average_address_blind :
    ∀ a : Fin 8, cAvgSum (marker a) = (1 : Matrix (Fin 8) (Fin 8) ℤ) := by
  native_decide

/-- Shift invariance (circulant property): constant along the `C₈` translation action. -/
def ShiftInvariant (M : Matrix (Fin 8) (Fin 8) ℤ) : Prop :=
  ∀ k i j : Fin 8, M (i - k) (j - k) = M i j

instance : DecidablePred ShiftInvariant := fun M => by
  unfold ShiftInvariant; infer_instance

/-- Circulant basis element `d`: ones exactly on the stripe `j - i = d`. -/
def circ (d : Fin 8) : Matrix (Fin 8) (Fin 8) ℤ :=
  Matrix.of fun i j => if j - i = d then 1 else 0

/-- "Is an address marker" (decidable finite existential). -/
def IsMarker (M : Matrix (Fin 8) (Fin 8) ℤ) : Prop := ∃ a : Fin 8, M = marker a

instance : DecidablePred IsMarker := fun M => by
  unfold IsMarker; infer_instance

/-- **L3 = OB-W2 (address-vs-trace type disjointness, mirrors check 3):** no address
marker is shift-invariant; every circulant basis element IS shift-invariant, is nonzero,
and is NOT a marker. Address position and circulated trace content are disjoint types. -/
theorem addr_disjoint_from_trace :
    (∀ a : Fin 8, ¬ ShiftInvariant (marker a)) ∧
    (∀ d : Fin 8, ShiftInvariant (circ d) ∧ circ d ≠ 0 ∧ ¬ IsMarker (circ d)) := by
  native_decide

/-- Matrix unit `E_e` at position `e = (r, c)` (the full basis, not only diagonals). -/
def stdB (e : Fin 8 × Fin 8) : Matrix (Fin 8) (Fin 8) ℤ :=
  Matrix.of fun i j => if i = e.1 ∧ j = e.2 then 1 else 0

/-- **L4 = OB-W3 (averaging idempotent, ℤ-scaled, mirrors check 6):**
`cAvgSum (cAvgSum E) = 8 • cAvgSum E` on the whole matrix-unit basis — the escape-closure
leg: routing a registration through the traced sector and averaging again adds nothing;
downstream registrations inherit address-blindness. -/
theorem avg_idempotent :
    ∀ e : Fin 8 × Fin 8, cAvgSum (cAvgSum (stdB e)) = (8 : ℤ) • cAvgSum (stdB e) := by
  native_decide

/-! ## L5/L6 — the explicit hypothesis carriers (never theorems) -/

/-- **L5 carrier (corpus sweep, `CLOSE_GAP_W_MEMO.md` §2.1):** "the ONLY cross-event
write into `Q_N` from the circulated sector is the `:1998` emission." A
corpus-EXHAUSTIVENESS fact — Lean cannot decide what BOOK_01 does not contain — so it is
carried as an explicit hypothesis structure, never proved. (The F3 optional decidable
shadow over a frozen operator list is deliberately NOT built: list-completeness would
itself remain the hypothesis, and the shadow must not masquerade as the sweep.) -/
structure SingleQNWriterSweep where
  statement : Prop
  cited : statement

/-- **L6 carrier (`BOOK_01:988`, CORE contradiction theorem — cited, not formalized):**
physicality ⇒ alters/constrains an addressable registration (INTERACT-WITH only; the
IS-typing is L7's separate assumption). -/
structure PhysicalityRequiresAddressable where
  statement : Prop
  cited : statement

/-! ## The re-attributed capstone -/

set_option linter.unusedVariables false in
/-- **GAP-W capstone, W-REC re-attribution (thin re-export, F3 TASK 3).** GIVEN the three
named hypothesis legs — L5 single-writer sweep, L6 `:988`, L7 R-A
(`ASSUMP-CLASS-RECORD-IS-ADDRESSABLE`) — and the joint hypotheses on the number `m` of
adjoined stationary marks (`h_halt : 1 ≤ m`, now documented as backed by
L5 + L6 + L7 **+ the L1–L4 legs proved above**, per `CLOSE_GAP_W_MEMO.md:402-406`;
`h_nocopy : m < 2` = W-T1 + W-BIT unchanged), the base cardinal is forced:
`|Ω₈| + m = 9`. The statement and proof are EXACTLY `card_base_forced_conditional`
(`WitnessForcing.lean`) — one forcing statement in `D0.All`, re-attributed not re-proved;
`h_halt` is NOT promoted to a proved term (honesty guard, memo `:406`). -/
theorem card_base_forced_wrec (m : ℕ)
    (h_wrec : SingleQNWriterSweep)                             -- L5, sweep
    (h_g2 : PhysicalityRequiresAddressable)                    -- L6, :988 cited
    (h_ra : D0.Bridge.ClassRecordIsAddressableAssumption)      -- L7, registered ASSUMP
    (h_halt : 1 ≤ m)      -- backed by L1–L4 + h_wrec + h_g2 + h_ra (attribution, not proof)
    (h_nocopy : m < 2) :  -- W-T1 + W-BIT, unchanged
    Fintype.card D0.Omega8 + m = 9 :=
  D0.Core.WitnessForcing.card_base_forced_conditional m h_halt h_nocopy

end D0.Core.WRecArchitecture
