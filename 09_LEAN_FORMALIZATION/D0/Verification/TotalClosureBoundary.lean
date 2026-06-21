import Mathlib.Data.List.Basic
import Mathlib.Tactic

/-!
# D0-TOTAL-CLOSURE-BOUNDARY-001 — every lane has exactly one admissible terminal state

The ten parallel lanes (A–J) each terminate in one of the eight admissible terminal states. Encoding the
assignment as a `List (lane × Terminal)` makes "every lane is in a terminal state" a type-level guarantee
(every entry is a `Terminal` constructor) plus a decidable length check. No lane is an unowned future task.
This mirrors `TOTAL_CLOSURE_BOARD.csv`.
-/

namespace D0.Verification.TotalClosureBoundary

/-- The eight admissible terminal states (no synonyms allowed). -/
inductive Terminal
  | certClosed
  | noGo
  | noGoClosed
  | passportClosed
  | empiricalPassport
  | operatorScaffoldCertified
  | proofTargetOnePrimitive
  | inactiveBridge
  deriving DecidableEq, Repr

open Terminal

/-- Terminal state of each lane (A–J). Lanes A/B/C/D/E/G are present-core maximality NO-GOs (open physics
reduced to one named primitive each); F is a formalism passport; H carries CERT + empirical passport; I, J
are certificate/ledger CERTs. -/
def laneTerminal : List (String × Terminal) :=
  [ ("A", noGo),                 -- scene-native refinement underdetermined
    ("B", noGo),                 -- phason physical magnitude underdetermined
    ("C", noGo),                 -- CMB smoothing underdetermined
    ("D", noGo),                 -- lepton branch-fixing underdetermined
    ("E", noGo),                 -- alpha residue realization underdetermined
    ("F", passportClosed),       -- finite→continuum formalism passport
    ("G", noGo),                 -- Higgs/hypercharge/baryon present-core no-gos
    ("H", empiricalPassport),    -- echo + horizon-hum falsifier passports
    ("I", certClosed),           -- corpus integrity + certificate board
    ("J", certClosed) ]          -- research method ledger

/-- All ten lanes are assigned a terminal state. -/
theorem all_lanes_terminal : laneTerminal.length = 10 := by decide

/-- No lane is left in a non-terminal (unowned) state: every entry is one of the eight constructors
(guaranteed by typing) and the lane labels are distinct. -/
theorem lane_labels_distinct : (laneTerminal.map (·.1)).Nodup := by decide

/-- At least one lane reaches each of the load-bearing terminal kinds used in this program. -/
theorem terminal_kinds_present :
    (laneTerminal.map (·.2)).contains noGo = true ∧
    (laneTerminal.map (·.2)).contains passportClosed = true ∧
    (laneTerminal.map (·.2)).contains empiricalPassport = true ∧
    (laneTerminal.map (·.2)).contains certClosed = true := by decide

/-- **D0-TOTAL-CLOSURE-BOUNDARY-001.** Ten lanes, each in exactly one admissible terminal state, with
distinct labels and the program's terminal kinds all represented. -/
theorem total_closure_boundary :
    laneTerminal.length = 10 ∧ (laneTerminal.map (·.1)).Nodup :=
  ⟨all_lanes_terminal, lane_labels_distinct⟩

end D0.Verification.TotalClosureBoundary
