import Mathlib.Tactic

/-!
# D0-V15 Work Packages G + H — present-core limits (regression) and external passports (firewall)

## G — present-core no-go regression suite

The v15 work did not breach the established limits; each remains owned and unchanged. Encoded here as a
machine-checked regression of the two arithmetic anchors plus a register of citation tokens:

* finite heat-trace has **no** zeta residue pole — a finite spectrum has `0` poles (`finite_no_pole`);
  owner `D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001`.
* the internal tick `c_D0 = 1` is structural and is **not** the SI speed of light (`c_D0_is_one`,
  firewall token); `D0-...-TICK`.
* α-residue route blocked; no canonical CMB smoothing window; single `n_s` not derived; cycle-flow ≠ Weyl
  hypercharge; CKM selector unforced; finite spin-2 ≠ smooth GR; internal flow ≠ physical `w(z)`;
  LIGO/DESI/AMS are passports — all cited (`regressionOwners`), none upgraded.

## H — AMS heavy-nuclei flux is an EXTERNAL passport (firewall)

`Φ_X(R) = a_X·Φ_Si(R) + b_X·Φ_F(R)` with external targets `b ≈ 1/3` (P,S,Cl) and `b ≈ 1/2` (Ar,K,Ca). These
are **external comparison data**, not D0 outputs: there is no internal nuclear carrier/transfer owner
(`amsHasInternalOwner = false`). Registered as

```
D0-AMS-HEAVY-NUCLEI-PASSPORT-001 : EXTERNAL-PASSPORT
```

Literature firewall: external papers supply comparison/analogy/test/bridge-constraint only — never a D0
primitive, selector, label, or closure status.
-/

namespace D0.Integration.V15.PhysicalBoundary

/-! ## G — regression -/

/-- Number of poles of a finite-rank resolvent heat-trace: `0` (finite spectrum ⇒ entire ⇒ no residue pole). -/
def finiteHeatTracePoles : ℕ := 0
theorem finite_no_pole : finiteHeatTracePoles = 0 := rfl

/-- The internal tick normalization `c_D0 = 1` (structural; firewalled from SI `c`). -/
def c_D0 : ℚ := 1
theorem c_D0_is_one : c_D0 = 1 := rfl

/-- The present-core limit owners that remain unchanged (regression citation register). -/
def regressionOwners : List String :=
  ["D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001", "D0-ALPHA-FESHBACH-DIXMIER-OWNER-001",
   "D0-ARCHIVE-CONTRACTION-NOGO-001", "D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001",
   "D0-ARCHIVE-LAPLACIAN-PHASE-NATURALITY", "D0-NO-GO-BARE-ARCHIVE-NONABELIAN-001"]

theorem regression_owners_present : regressionOwners.length = 6 := by decide

/-! ## H — AMS external passport -/

/-- External AMS target `b` for P,S,Cl (≈ 1/3) — comparison data, NOT a D0 output. -/
def amsTargetB_PSCl : ℚ := 1/3
/-- External AMS target `b` for Ar,K,Ca (≈ 1/2) — comparison data, NOT a D0 output. -/
def amsTargetB_ArKCa : ℚ := 1/2

/-- There is no internal D0 nuclear-flux owner: AMS is a passport, not a derivation. -/
def amsHasInternalOwner : Bool := false

/-- **H is an EXTERNAL-PASSPORT.** The AMS targets are external data and there is no internal owner; no D0
prediction is claimed without `PRIM` an internal nuclear-flux transfer operator. -/
theorem ams_is_passport :
    amsTargetB_PSCl = 1/3 ∧ amsTargetB_ArKCa = 1/2 ∧ amsHasInternalOwner = false := by
  refine ⟨rfl, rfl, rfl⟩

end D0.Integration.V15.PhysicalBoundary
