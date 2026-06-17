#!/usr/bin/env python3
"""EMPIRICAL STRESS REFERENCE — NOT A FORCING CERTIFICATE.  (§00.9 anti-numerology firewall)

WHAT THIS IS. A ported-legacy stress script that confronts a *frozen, fitted* charged-lepton
row with the PDG muon/tau masses and FAILs loudly if the frozen row no longer reproduces them.
It is a backward consistency check, NOT a forward derivation.

WHY IT IS NOT A FORCING CERT.
  - The selector ratio r_mu = 3.8814328681047283 (see `r=[...]` below) is a FITTED free knob:
    backing it out of the PDG mass, mu_ref/me / (A_depth**0.25 * B_mu) ≈ 3.881401, reproduces
    the hardcoded 3.881433 to ~5 sig figs. The 17-digit decimal is a HYP realization, not a
    forced invariant. The `assert abs(mu_rel)<1e-4 and abs(tau_rel)<1e-4` below is therefore a
    9+ digit match of a fitted row to data — and per §00.9 a 9-digit data match is NEVER "THE".

IT FEEDS NO THE/CERT-CLOSED STATUS.
  - It is NOT the registered cert for D0-LEPTON-002. The canonical `python_cert` for that claim
    is `05_CERTS/vp_charged_lepton_transfer_certificate.py` (09_LEAN_FORMALIZATION/docs/
    CLAIM_TO_LEAN_MAP.csv) — a different file.
  - `.github/workflows/guards.yml` runs `run_registered_certs.py` (no --orphans) and
    `check_cert_can_fail.py`; both read only the registry `python_cert` column, so neither ever
    executes this file. It runs only under a manual `run_registered_certs.py --orphans` audit,
    where its `claims` list is empty — it gates nothing.
  - The `*_RESULTS.json/.md` it writes are consumed by nothing (and are skipped by
    tools/sync_canonical_file_map.py).

WHERE THE REAL CONTENT LIVES. The forcing part that D0 actually owns is the integer-additive
Lucas ladder m_mu/m_e ⊇ L11+L4 = 206 (THE, BOOK_04 §04.8.L.1); the decimal VALUE is HYP. See the
§00.9 caveat on D0-LEPTON-002 in CLAIM_TO_LEAN_MAP.csv / 03_THEORY_MAP/theory_semantic_index.md.

DO NOT promote, cite, or run this as a forcing certificate. Keep it as an empirical stress probe.
"""
import json, math
from pathlib import Path
phi=(1+5**0.5)/2
delta0=(5**0.5-2)/2
me=0.5109989506917533
Lambda=38*me
A_depth=22049582.625000414
TW_over_TZ=0.7767227212877189
# FITTED FREE KNOBS (§00.9): r_mu/r_tau are backed out of the PDG masses, not forced invariants.
r=[1.0,3.8814328681047283,10.318348325399374]
B_e=1.0
B_mu=TW_over_TZ*(1+delta0**3/(2-delta0))
B_tau=1+delta0+delta0/phi+delta0**2-(2-delta0)*delta0**3
p=[0.0,0.25,1/3]
R_e=r[0]*(A_depth**p[0])*B_e
R_mu=r[1]*(A_depth**p[1])*B_mu
R_tau=r[2]*(A_depth**p[2])*B_tau
m_e=me; m_mu=R_mu*me; m_tau=R_tau*me
mu_ref=105.6583755; tau_ref=1776.86
mu_rel=m_mu/mu_ref-1; tau_rel=m_tau/tau_ref-1
assert abs(phi**2-phi-1)<1e-15
assert abs(delta0-(1/(2*phi**3)))<1e-15
assert abs(R_e-1)<1e-15
assert 206.7<R_mu<206.9
assert 3477.0<R_tau<3477.6
# BACKWARD consistency stress gate on a FITTED row (§00.9) — not a forward forcing/derivation.
assert abs(mu_rel)<1e-4 and abs(tau_rel)<1e-4
res={
 'status':'STRESS_REFERENCE_PASS_CHARGED_LEPTON_GENERATION_ACTION',
 'firewall_status':'EMPIRICAL_STRESS_REFERENCE_NOT_A_FORCING_CERT (see module docstring; §00.9)',
 'registered_cert_for_D0_LEPTON_002':'05_CERTS/vp_charged_lepton_transfer_certificate.py',
 'feeds_THE_or_CERT_CLOSED_status':False,
 'phi':phi,'delta0':delta0,'Lambda_act_MeV':Lambda,
 'A_depth_EW':A_depth,'TW_over_TZ':TW_over_TZ,
 'selector_ratios_r':r,
 'generation_lift_exponents':{'electron':p[0],'muon':p[1],'tau':p[2]},
 'boundary_factors':{'B_e':B_e,'B_mu':B_mu,'B_tau':B_tau},
 'charged_lepton_mass_ratios_D0':{'e':R_e,'mu':R_mu,'tau':R_tau},
 'charged_lepton_masses_MeV_single_section':{'e':m_e,'mu':m_mu,'tau':m_tau},
 'external_stress_reference_MeV':{'mu':mu_ref,'tau':tau_ref},
 'external_stress_relative_errors':{'mu':mu_rel,'tau':tau_rel},
 'muon_formula':'r_mu * A_EW^(1/4) * (T_W/T_Z) * (1 + delta0^3/(2-delta0))',
 'tau_formula':'r_tau * A_EW^(1/3) * (1 + delta0 + delta0/phi + delta0^2 - (2-delta0) delta0^3)',
 'guardrail':'No Lucas-number charged-lepton fit is used. The generation action uses registered selector ratios, EW radial depth, weak projection, PNO quarter lift and rank-cubic lift only.'
}
base=Path(__file__).resolve().parents[1]
(base/'04_CERTS'/'D0_CHARGED_LEPTON_GENERATION_ACTION_RESULTS.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
(base/'04_CERTS'/'D0_CHARGED_LEPTON_GENERATION_ACTION_RESULTS.md').write_text('# D0 charged-lepton generation action results\n\n```json\n'+json.dumps(res,indent=2)+'\n```\n',encoding='utf-8')
print(res['status'])
