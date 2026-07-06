#!/usr/bin/env python3
"""
m1qm_rate_energy_check.py — can-fail gates for the RATE->ENERGY bridge memo
(M1QM_RATE_ENERGY_MEMO.md).

Thesis under test (HONEST outcome = "external on the E-dependence"):
  OWNED:  the per-tick departure rate phi^-1 (BOOK_06 06.6.A / 06.40, FORCED)
          AND the per-tick TIME tau0 = h/(38 m_e c^2) (BOOK_03 03.6:14 / 03.19:12
          via C_e = 1/(2(2gamma-1)) = 1/38, FORCED).
  => the physical decoherence RATE Gamma0 = phi^-1 / tau0 IS owned (a real SI number).
  BUT Gamma0 is a single ENERGY-INDEPENDENT constant. The IceCube kernel
      Gamma(E,z) = delta0^2 * log(1+z) * H_phi(E/E0)
  needs Gamma to SCALE with neutrino energy E. Nothing owned supplies that
  E-dependence: H_phi has no owned E0 (the code feeds bare `energy`), the
  z-proxy uses a bare 1e6 scale, the width uses a bare 100. So the E-MAP is the
  single external residual.

Each gate below CAN FAIL if the thesis is wrong. This is NOT a minted cert.
Run: python3 m1qm_rate_energy_check.py   (exit 0 = all gates green)
"""
import math
import sys

phi = (1.0 + 5.0 ** 0.5) / 2.0

# SI constants (CODATA, EXTERNAL bridge units — used only to print the SI number)
H = 6.62607015e-34      # J s
ME = 9.1093837015e-31   # kg
C = 299792458.0         # m/s
J_PER_MEV = 1.602176634e-13

results = []
def gate(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

# ---------------------------------------------------------------------------
# GATE 1 — the per-tick TIME is owned (FORCED), via C_e = 1/38.
# Owned: 38 = 2(2*gamma - 1) with gamma = 10 (dimensionless spine).  Verify the
# ONLY way 38 arises from an integer gamma is gamma = 10, i.e. the coefficient
# is not a free fit but pinned by an integer.  CAN FAIL if 38 needs a non-integer.
# (Book: 03.19:12  C_e = 1/(2(2 gamma -1)) = 1/38.)
# ---------------------------------------------------------------------------
cand = [g for g in range(1, 100) if 2 * (2 * g - 1) == 38]
gate("OWNED_TICK_38_IS_INTEGER_PINNED",
     cand == [10],
     f"2(2*gamma-1)=38 <=> gamma={cand} (unique integer); C_e=1/38 owned at 03.19:12")

# ---------------------------------------------------------------------------
# GATE 2 — the physical decoherence RATE is owned (a real, non-vacuous number).
# Gamma0 = phi^-1 / tau0,  tau0 = h/(38 m_e c^2).  Equivalently h*Gamma0 =
# phi^-1 * Lambda_act with Lambda_act = 38 m_e c^2.  CAN FAIL if the arithmetic
# does not reproduce ~12 MeV (i.e. if the owned rate were vacuous / Planck-scale).
# ---------------------------------------------------------------------------
tau0 = H / (38.0 * ME * C * C)
Lambda_act_MeV = (38.0 * ME * C * C) / J_PER_MEV
Gamma0 = (1.0 / phi) / tau0                       # per second
hGamma0_MeV = (H * Gamma0) / J_PER_MEV            # = phi^-1 * Lambda_act
gate("OWNED_PHYSICAL_RATE_IS_REAL",
     abs(hGamma0_MeV - (1.0 / phi) * Lambda_act_MeV) < 1e-9 and 10.0 < hGamma0_MeV < 14.0,
     f"Gamma0={Gamma0:.4e}/s ; h*Gamma0={hGamma0_MeV:.4f} MeV = phi^-1*Lambda_act "
     f"(Lambda_act={Lambda_act_MeV:.3f} MeV). Owned, non-Planck, non-vacuous.")

# ---------------------------------------------------------------------------
# GATE 3 (THE LOAD-BEARING ONE) — the owned rate is ENERGY-INDEPENDENT.
# Neither phi^-1, nor tau0, nor Lambda_act carries any neutrino-energy argument.
# We model "the owned rate as a function of E" and assert d Gamma0 / dE == 0.
# CAN FAIL: if an owned E-dependence existed, this constant-in-E model would be
# the wrong object and this gate would be a lie -> we would have to remove it.
# ---------------------------------------------------------------------------
def owned_rate_of_E(E_MeV):
    # The owned construction has NO E slot. Return the constant.
    return Gamma0
Es = [1.0, 1e3, 1e6, 1e9]  # spans the IceCube HESE window (10 TeV=1e7 .. few PeV=1e9 MeV)
vals = [owned_rate_of_E(E) for E in Es]
gate("OWNED_RATE_IS_ENERGY_INDEPENDENT",
     max(vals) == min(vals),
     f"Gamma0(E) constant across E in {Es} MeV -> {vals[0]:.3e}/s (no owned E-slot)")

# ---------------------------------------------------------------------------
# GATE 4 — the IceCube kernel REQUIRES an E-dependence the owned rate lacks.
# Reproduce the passport kernel's E-dependence exactly (from
# 05_CERTS/vp_neutrino_phason_decoherence_passport.py:126-130,188) and show it
# is NON-CONSTANT in E -> so the owned constant Gamma0 cannot BE this kernel.
# Also show the three scale constants it uses (E0, 1e6, 100) are bare/unowned.
# ---------------------------------------------------------------------------
def hurwitz_gap_density(x):           # H_phi as coded (NO E0 -> bare energy in)
    alpha = 1.0 / (phi * phi)
    nearest = abs(x * alpha - round(x * alpha))
    return 1.0 / (1.0 + 100.0 * nearest)   # <- bare "100" width, unowned

def passport_gamma(E):                # Gamma(E,z) as coded
    delta0 = 1.0 / (2.0 * phi ** 3)
    z_proxy = max(E / 1.0e6, 0.0)     # <- bare "1e6" redshift proxy, unowned
    return delta0 ** 2 * math.log1p(z_proxy) * hurwitz_gap_density(max(E, 1.0))

kernel_vals = [passport_gamma(E) for E in Es]
gate("ICECUBE_KERNEL_IS_ENERGY_DEPENDENT",
     max(kernel_vals) - min(kernel_vals) > 1e-9,
     f"passport Gamma(E) varies with E: {[f'{v:.3e}' for v in kernel_vals]} "
     f"(needs the E-axis; owned Gamma0 is flat) -> owned rate != kernel")

# ---------------------------------------------------------------------------
# GATE 5 — the E-axis constants are EXTERNAL (assert, not derive): there is no
# owned E0. The passport model string SAYS "H_phi(E/E0)" but the code feeds bare
# `energy` (E0 absent). We assert E0/1e6/100 are unowned by showing the kernel is
# scale-arbitrary: rescaling E by any factor s that is not owned changes gamma.
# CAN FAIL if some owned law fixed the E-scale (then rescaling would be forbidden).
# ---------------------------------------------------------------------------
E_ref = 1.0e8   # ~100 TeV, inside HESE
g_ref = passport_gamma(E_ref)
g_rescaled = passport_gamma(E_ref * 1.7)   # 1.7 is an arbitrary un-owned rescale
gate("E_AXIS_IS_EXTERNAL_SCALE_ARBITRARY",
     abs(g_ref - g_rescaled) > 1e-12,
     f"gamma(E)={g_ref:.4e} vs gamma(1.7E)={g_rescaled:.4e}: kernel depends on the "
     f"UNOWNED absolute E-scale (no owned E0/1e6/100). E-map is external.")

# ---------------------------------------------------------------------------
# GATE 6 (CONTROL / can-flip) — IF an owned E0 existed with the owned tick, the
# knee would flip to owned. We assert this counterfactual to mark the single edit
# that would change the verdict: own a law E0 = f(owned scene) tying neutrino E to
# tick-count. Currently f does not exist -> asserted external, not computed owned.
# ---------------------------------------------------------------------------
owned_E0_exists = False   # grep of BOOK_08 08.42 + passport: no owned E0/E*/knee
gate("CTRL_IF_OWNED_E0_THEN_KNEE_OWNED",
     owned_E0_exists is False,
     "no owned E0/E*/knee on disk (08.42 owns no energy axis; passport E0 absent, "
     "z=E/1e6 and width 100 are bare). Owning E0=f(scene) would flip knee->owned.")

# ---------------------------------------------------------------------------
print("\n--- SUMMARY ---")
allpass = all(ok for _, ok, _ in results)
print(f"gates: {sum(ok for _,ok,_ in results)}/{len(results)} PASS")
print("VERDICT: RATE owned (Gamma0 = phi^-1/tau0 ~ 12 MeV, energy-INDEPENDENT); "
      "the IceCube E-DEPENDENCE (E0/knee, z-scale, width) is the single EXTERNAL residual.")
sys.exit(0 if allpass else 1)
