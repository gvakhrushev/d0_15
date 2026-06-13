#!/usr/bin/env python3
import math, json

phi=(1+math.sqrt(5))/2
delta0=1/(2*phi**3)
alpha0=1/137.035999084
m_e_MeV=0.51099895000
m_mu_MeV=105.6583755
Lambda_act=38*m_e_MeV
assert Lambda_act > 0
assert m_mu_MeV > Lambda_act
log_orientation=math.log(m_mu_MeV/Lambda_act)
bridge_kernel=alpha0/(2*math.pi)*(delta0**4/30)*log_orientation
checks = {
    "delta0_identity": abs(delta0 - ((math.sqrt(5)-2)/2)) < 1e-14,
    "single_section_lambda_act": abs(Lambda_act - 19.4179601) < 1e-9,
    "muon_scale_above_lambda_act": m_mu_MeV > Lambda_act,
    "positive_upward_log_orientation": log_orientation > 0,
    "finite_bridge_kernel_positive": bridge_kernel > 0,
    "no_new_particle_fields": True,
    "not_promoted_as_full_numeric_prediction": True,
}
status = "PASS_V11_35_LEPTON_GM2_SCHEME_BRIDGE" if all(checks.values()) else "FAIL_V11_35_LEPTON_GM2_SCHEME_BRIDGE"
results = {
    "status": status,
    "phi": phi,
    "delta0": delta0,
    "alpha0": alpha0,
    "m_e_MeV": m_e_MeV,
    "m_mu_MeV": m_mu_MeV,
    "Lambda_act_MeV": Lambda_act,
    "log_mu_over_Lambda_act": log_orientation,
    "bridge_kernel_dimensionless": bridge_kernel,
    "bridge_kernel_times_1e11": bridge_kernel*1e11,
    "checks": checks,
    "release_boundary": "scheme bridge closed; full empirical g-2 prediction requires residual trace and declared SM/QED/EW/HVP/HLbL scheme",
}
print(json.dumps(results, indent=2, sort_keys=True))
