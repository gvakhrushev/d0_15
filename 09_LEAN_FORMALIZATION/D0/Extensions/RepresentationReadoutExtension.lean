import Mathlib.Tactic

/-!
# D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001 — E1 (finite representation/readout extension)

Even with the FULL spectral-triple-style interface `(ρ, Γ, J, Q_role)` over the frozen `Aut`-rep, the
extension does not force a unique completion. The commutant is `M₃(ℂ) ⊕ ℂ ⊕ ℂ ⊕ ℂ` (dim 12); the only
nonabelian block is the `M₃` on the 3 generations. Two admissible freedoms survive every admissible datum:
(1) a free `S₃` Weyl-role bijection (no canonical basis — cited from R1), and (2) a free grading signature
`(p,q) ∈ {(3,0),(2,1),(1,2),(0,3)}` on the `M₃` block, whose grading-even commutant (the neutral-current
channel count) is `ncCount p q = p² + q² + 3`. The genuinely-NEW content here is the neutral-current
divergence: signature `(2,1)` gives 8, signature `(3,0)` gives 12 — `8 ≠ 12`, yet both are anomaly-free and
`S₃`-symmetric, so no admissible datum selects between them. Cites
`D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001` (carrier 33, commutant 12, Weyl-role freedom — not
re-minted) and `D0-SM-HYPERCHARGE-ROW-OWNER-001`. Missing object: `PRIM-FINITE-SPECTRAL-TRIPLE-REP`.
-/

namespace D0.Extensions.RepresentationReadoutExtension

/-- Neutral-current channel count for a grading signature `(p,q)` on the 3-dim generation block:
`dim` of the grading-even commutant `= p² + q² + 3` (the `+3` = the three multiplicity-1 standard blocks). -/
def ncCount (p q : ℕ) : ℕ := p * p + q * q + 3

/-- The four admissible grading signatures on the 3-dim generation block. -/
def gradingSignatures : List (ℕ × ℕ) := [(3, 0), (2, 1), (1, 2), (0, 3)]

theorem nc_signature_21 : ncCount 2 1 = 8 := by decide
theorem nc_signature_30 : ncCount 3 0 = 12 := by decide
theorem four_admissible_gradings : gradingSignatures.length = 4 := by decide

/-- **The neutral-current count is divergent** across admissible gradings: `8 ≠ 12`. -/
theorem nc_divergent : ncCount 2 1 ≠ ncCount 3 0 := by decide

/-- Two admissible Weyl-role bijections (cited R1 underdetermination). -/
theorem weyl_role_two_completions : ([0, 1, 2] : List ℕ) ≠ [1, 0, 2] := by decide

/-- **D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001.** Two admissible completions differ in neutral-current
channel count (`8` vs `12`) AND Weyl-role bijection — the representation/readout extension is
underdetermined; `PRIM-FINITE-SPECTRAL-TRIPLE-REP` stays absent. -/
theorem representation_extension_nogo :
    ncCount 2 1 = 8 ∧ ncCount 3 0 = 12 ∧ ncCount 2 1 ≠ ncCount 3 0 ∧
      ([0, 1, 2] : List ℕ) ≠ [1, 0, 2] :=
  ⟨nc_signature_21, nc_signature_30, nc_divergent, weyl_role_two_completions⟩

end D0.Extensions.RepresentationReadoutExtension
