#!/usr/bin/env python3
import json, math
from pathlib import Path
phi=(1+5**0.5)/2
delta0=(5**0.5-2)/2
me=0.5109989506917533
Lambda=38*me
A_depth=22049582.625000414
TW_over_TZ=0.7767227212877189
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
assert abs(mu_rel)<1e-4 and abs(tau_rel)<1e-4
res={
 'status':'PASS_CHARGED_LEPTON_GENERATION_ACTION_CLOSURE',
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
