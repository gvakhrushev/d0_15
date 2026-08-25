import D0.Tower.DetectionQuadratic

/-!
# D0-GAP-E-PORT-EXHAUSTION-001 — port-power exhaustion of the extension ladder (Lean lift, DRAFT)

Forge memo: `_TASKS_CENTER_ATTACK/CLOSE_GAP_E_DIMENSIONAL_MEMO.md` (12th pass, §7.1 proposed this
module). Python certificate: `close_gap_e_dimensional_check.py`.

The GAP-E completeness quantifier: an admissible zone-extension alphabet is a port-power `D₂^k`
of the binary terminal dyad with `k ≤ 2`, where the cap is the OWNED two-comparison-kind count
(`D0.Tower.DetectionQuadratic.two_comparison_kinds`) and the ladder `{D₂¹, D₂²}` is the owned
capacity tower (B01:1548/:1816). Hence the admissible size-set is EXACTLY `{2, 4}`: the surviving
even rivals `|X| ∈ {6, 8}` (towers `(9,11,15)`, `(9,11,17)`) die — `6` is not a dyad power at all
(cap-independent), and `8 = D₂³` demands a third port, excluded by the cap. Therefore `z₃ ≤ 13`.

This module is deliberately thin, on the `DetectionQuadratic` pattern: the decidable ARITHMETIC of
the exhaustion (powers, the size-set, the rival kills, the zone bound) is machine-checked here;
the cap is REUSED from the CORE two-kind count, not re-proved. The categorical identification
"port ⟺ comparison kind" and the reading "two ports exhaust the ladder" remain the forcing
READING (DEF-0.2.2 style), exactly parallel to `DetectionQuadratic`'s own categorical leg —
narrated, not a separate machine-checked categorical theorem.

Negative control (machine-checked): at cap 3 the size `8 = 2³` is RE-ADMITTED
(`eight_readmitted_at_cap_three`) — the cap is load-bearing, the exclusion can fail.
-/

namespace D0.Tower

/-- The port-count cap: the number of comparison kinds of the detection act. OWNED by
`two_comparison_kinds`; reused, never assumed. -/
def portCap : ℕ := Fintype.card ComparisonKind

theorem portCap_eq_two : portCap = 2 := two_comparison_kinds

/-- **The port-power size-set is exactly `{2, 4}`.** Under the owned cap, a port-power
`D₂^k` (`1 ≤ k ≤ portCap`) has size `2` or `4`, and both occur (the owned ladder
`V₁₁ = V₉ ⊔ D₂`, `V₁₃ = V₉ ⊔ ABCD`, `|ABCD| = |D₂|²`). -/
theorem port_power_sizes (k : ℕ) (hk1 : 1 ≤ k) (hk2 : k ≤ portCap) :
    2 ^ k = 2 ∨ 2 ^ k = 4 := by
  rw [portCap_eq_two] at hk2
  interval_cases k <;> simp

/-- Both owned ladder sizes are realized: `D₂¹` and `D₂² = ABCD`. -/
theorem ladder_sizes_realized :
    (∃ k, 1 ≤ k ∧ k ≤ portCap ∧ 2 ^ k = 2) ∧ (∃ k, 1 ≤ k ∧ k ≤ portCap ∧ 2 ^ k = 4) :=
  ⟨⟨1, by simp [portCap_eq_two]⟩, ⟨2, by simp [portCap_eq_two]⟩⟩

/-- **L-D3a (cap-independent kill of `|X| = 6`).** Six is not a dyad power at any exponent:
`2² < 6 < 2³` and dyad powers are strictly monotone. The rival tower `(9,11,15)` has no
port-power realization at all. -/
theorem six_not_port_power (k : ℕ) : 2 ^ k ≠ 6 := by
  intro h
  have h4 : (2 : ℕ) ^ 2 < 2 ^ k := by omega
  have h8 : (2 : ℕ) ^ k < 2 ^ 3 := by omega
  have hk2 : 2 < k := (Nat.pow_lt_pow_iff_right (by norm_num)).mp h4
  have hk3 : k < 3 := (Nat.pow_lt_pow_iff_right (by norm_num)).mp h8
  omega

/-- **L-D3b (capped kill of `|X| = 8`).** Eight IS a dyad power — but only at exponent 3,
which demands a third port: excluded by the owned cap. The rival tower `(9,11,17)` dies at
the cap, not by arithmetic accident. -/
theorem eight_needs_third_port (k : ℕ) (hk : k ≤ portCap) : 2 ^ k ≠ 8 := by
  rw [portCap_eq_two] at hk
  interval_cases k <;> simp

/-- **Negative control (can-fail).** At cap 3 the size 8 is re-admitted: the exclusion of the
`(9,11,17)` rival is carried by the OWNED cap `portCap = 2` and would fail if a third
comparison kind existed. -/
theorem eight_readmitted_at_cap_three : ∃ k, k ≤ 3 ∧ 2 ^ k = 8 := ⟨3, by simp⟩

/-- **The rival kill (L-D4).** Neither surviving even rival size `{6, 8}` is an admissible
port-power under the owned cap. -/
theorem rivals_killed (n : ℕ) (hn : n = 6 ∨ n = 8) :
    ¬∃ k, 1 ≤ k ∧ k ≤ portCap ∧ 2 ^ k = n := by
  rintro ⟨k, _, hk2, hpow⟩
  rcases hn with rfl | rfl
  · exact six_not_port_power k hpow
  · exact eight_needs_third_port k hk2 hpow

/-- **The zone bound.** A zone extension by a port-power alphabet lands at `z = 9 + 2^k ∈ {11, 13}`;
hence the third zone satisfies `z₃ ≤ 13` at the arithmetic layer. This bound is conditional on the
FULL conditioning of the 12th-pass forge, not on one reading alone: (i) the forcing reading
port ⟺ comparison kind (Channel A), (ii) the `:860` falsifier read as falsifier (Channel B — the
memo's reopening hook requires severing BOTH channels), (iii) the owned ladder generation
`{D₂¹, D₂²}` (B01:1548/:1816 — cap and ladder are orthogonal load-bearing legs, memo mutation
`--mut-grant-cap-without-ladder`), and (iv) the base-V₉ reading `z₃ = 9 + |X|`. The hypothesis
`1 ≤ k` is owned ground: the size-1 extension (`V₁₀`, an extra hidden marker) is excluded at
B01:1556 (GAP_E_DYAD_POWER_MEMO OWN-5). -/
theorem zone_bound (k : ℕ) (hk1 : 1 ≤ k) (hk2 : k ≤ portCap) : 9 + 2 ^ k ≤ 13 := by
  rcases port_power_sizes k hk1 hk2 with h | h <;> omega

/-- **D0-GAP-E-PORT-EXHAUSTION-001 (arithmetic leg).** Bundle: the owned cap is 2, the port-power
size-set is `{2, 4}` with both realized, the rivals `{6, 8}` are killed, and every admissible
extension keeps `z₃ ≤ 13`. The categorical leg (two kinds exhaust the ladder) is the forcing
reading, parallel to `detection_quadratic`. -/
theorem port_power_exhaustion :
    portCap = 2 ∧
    (∀ k, 1 ≤ k → k ≤ portCap → 2 ^ k = 2 ∨ 2 ^ k = 4) ∧
    (∀ n, (n = 6 ∨ n = 8) → ¬∃ k, 1 ≤ k ∧ k ≤ portCap ∧ 2 ^ k = n) ∧
    (∀ k, 1 ≤ k → k ≤ portCap → 9 + 2 ^ k ≤ 13) :=
  ⟨portCap_eq_two, port_power_sizes, rivals_killed, zone_bound⟩

end D0.Tower
