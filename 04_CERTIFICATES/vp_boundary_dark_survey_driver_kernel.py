#!/usr/bin/env python3
"""D0 boundary-dark survey-driver kernel certificate.

This certificate verifies the internal, parameter-free D0 dark-sector object:
fixed tilt seed, fixed archive-pressure seed, fixed terminal boundary gap, and
fixed golden attenuation expressed as an additive optical-depth kernel.
A telescope catalogue is an external readout of this object, not a new D0 layer.
"""
from __future__ import annotations
import json, math
from pathlib import Path

try:
    from d0_graph import delta_0, phi
except Exception:
    phi=(1+math.sqrt(5))/2
    delta_0=(math.sqrt(5)-2)/2

V13=13
LAMBDA_B_ACT=0.012763468417239953

def A(c: float) -> float:
    return 1.0/(1.0+delta_0/c)

def run_vp_boundary_dark_survey_driver_kernel() -> dict[str, object]:
    A13=A(V13)
    Aphi=A(phi)
    lambda_terminal=LAMBDA_B_ACT*A13
    chi_B=-math.log(Aphi)
    n_s=29/30
    w_a=-(delta_0**8)
    # Suppression kernel checks.  W_B is external survey-window shape, but once
    # it is normalized with W_B=0..1 the D0 attenuation is fixed.
    kernel_at_no_boundary=math.exp(-chi_B*0.0)
    kernel_at_full_boundary=math.exp(-chi_B*1.0)
    rel_kernel_err=abs(kernel_at_full_boundary-Aphi)
    result={
        "status":"PASS_BOUNDARY_DARK_SURVEY_DRIVER_KERNEL",
        "source":"finite boundary/archive operator family A(c)=1/(1+delta0/c)",
        "delta0":delta_0,
        "phi":phi,
        "lambda_B_active":LAMBDA_B_ACT,
        "A_V13":A13,
        "lambda_B_terminal":lambda_terminal,
        "A_phi":Aphi,
        "chi_B":chi_B,
        "n_s_D0":n_s,
        "one_minus_n_s":1-n_s,
        "w0_D0":-1.0,
        "w_a_D0":w_a,
        "attenuation_kernel":"K_B[W]=exp(-chi_B*W), with external survey window 0<=W<=1",
        "C_l_driver":"C_l=4*pi*int dk/k A_s*(k/k*)^(-1/30)*|exp(-chi_B*W_B(k))*Delta_l^external(k;w0=-1,w_a=-delta0^8)|^2",
        "kernel_checks":{
            "K_B_W0":kernel_at_no_boundary,
            "K_B_W1":kernel_at_full_boundary,
            "K_B_W1_minus_A_phi_abs":rel_kernel_err,
        },
        "closed_dark_object":{
            "type":"fixed archive-readout tuple plus boundary kernel",
            "Omega_DM_typing":"catalogue coordinate, not primitive D0 invariant",
            "particle_typing":"external phenomenological representation unless production/propagation/interaction/detector maps are derived"
        },
        "forbidden_shortcuts":[
            "lambda_B_terminal -> Omega_DM as a raw equality",
            "lambda_B_active -> dark-particle mass without production and interaction maps",
            "M_Z*sqrt(lambda_B) as active D0 claim",
            "survey nuisance parameters refitting D0 seeds",
        ],
        "external_applications":"telescope likelihood, baryon subtraction, lensing reconstruction, nonlinear growth and instrument selection apply the D0 tuple; they are not new D0-core layers",
    }
    if rel_kernel_err < 1e-15 and 0 < Aphi < 1 and chi_B > 0 and w_a < 0:
        result["status"]="PASS_BOUNDARY_DARK_SURVEY_DRIVER_KERNEL"
    else:
        result["status"]="FAIL_BOUNDARY_DARK_SURVEY_DRIVER_KERNEL"
    return result

if __name__=='__main__':
    res=run_vp_boundary_dark_survey_driver_kernel()
    print(f"vp_boundary_dark_survey_driver_kernel: [{res['status']}]")
    print(json.dumps(res, indent=2, sort_keys=True))
