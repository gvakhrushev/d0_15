import Mathlib.Tactic

/-!
# D0-PHASON-WZ-TRANSFER-OWNER-001 — phason equation-of-state `w_D0 = p/ρ` (scaffold + kernel-only no-go)

The dark-energy reading of the 30-dimensional archive kernel (`30 = 8 ⊕ 10 ⊕ 12`, the nullity of
K(9,11,13)) requires a finite **pressure-energy** pair, not the kernel dimension alone. This module:

* defines the internal equation of state `w_D0 = pressure / ρ` on the nonzero-energy domain
  (`D0-PHASON-PRESSURE-EOS-SCAFFOLD-001`, the EOS *form* — the D0 phason pressure is the log-det
  loop-pressure response `LOGDET-PRESSURE-COUPLING-CERT-CLOSED` and the energy is the archive
  relative-acceleration `RELATIVE-ARCHIVE-ACCELERATION-CERT-CLOSED`; those instantiate the pair);
* proves the **no-go** `D0-PHASON-WZ-KERNEL-ONLY-NOGO-001`: two pressure-energy pairs over the SAME
  30-dim kernel give different `w_D0`, so the kernel dimension alone does NOT determine `w` — a finite
  pressure-energy operator is required.

The explicit internal `w_D0(u)` / finite `w_N` formula (the actual phason `ρ(u), p(u)` functions) and
the redshift `u → z` map remain open / passport (`D0-PHASON-WZ-TRANSFER-OWNER-001` = PROOF-TARGET;
the CPL reading is passport-only). No survey datum (DESI/H0/Ωm/r_d) enters here.
Cert: `05_CERTS/vp_phason_wz_transfer_owner.py`, `vp_phason_pressure_eos.py`.
-/

namespace D0.Cosmology

/-- The archive/dark kernel: the nullity-30 sector `30 = 8 ⊕ 10 ⊕ 12` of K(9,11,13). -/
structure ArchiveKernel where
  dim : Nat
  h_dim : dim = 30

/-- A finite phason pressure-energy pair (internal quantities; no external survey datum). -/
structure PhasonPressureEnergy where
  rho : ℚ
  pressure : ℚ
  h_rho : rho ≠ 0

/-- Internal equation of state `w_D0 = p/ρ`, defined on the nonzero-energy domain. -/
def w_D0 (pe : PhasonPressureEnergy) : ℚ := pe.pressure / pe.rho

/-- **Scaffold.** `w_D0` is well-defined as `p/ρ` on the nonzero-energy domain. -/
theorem phason_w_defined_on_nonzero_energy (pe : PhasonPressureEnergy) :
    w_D0 pe = pe.pressure / pe.rho := rfl

/-- **D0-PHASON-WZ-KERNEL-ONLY-NOGO-001.** The 30-dimensional kernel ALONE does not determine `w`:
two phason pressure-energy pairs over the same kernel yield different `w_D0`. Hence a finite
pressure-energy operator (not the kernel dimension) is required to fix the equation of state. -/
theorem kernel_dim_alone_does_not_determine_w (_K : ArchiveKernel) :
    ∃ pe1 pe2 : PhasonPressureEnergy, w_D0 pe1 ≠ w_D0 pe2 := by
  refine ⟨⟨1, -1, by norm_num⟩, ⟨1, -1/2, by norm_num⟩, ?_⟩
  unfold w_D0
  norm_num

/-- The 30-dim kernel exists, yet (by the no-go) does not by itself pin `w` — the EOS needs the pair. -/
theorem kernel_present_but_insufficient (K : ArchiveKernel) :
    K.dim = 30 ∧ (∃ pe1 pe2 : PhasonPressureEnergy, w_D0 pe1 ≠ w_D0 pe2) :=
  ⟨K.h_dim, kernel_dim_alone_does_not_determine_w K⟩

end D0.Cosmology
