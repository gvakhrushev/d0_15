#!/usr/bin/env python3
"""A rigorous downstream Decimal/Brouwer/Banach SOURCE tolerance for the
already-certified ORIGINAL UNPADDED 0/10 two-site 42-Euler root.

Consumes the frozen outward interval receipt. Does NOT replay 1764 Hessian
enclosures or derive/estimate the actual Book03 H+J+R remaining source.
"""
from __future__ import annotations
import hashlib
import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 85
ROOT = Path(__file__).resolve().parents[4]
ORIGINAL = "02_REGISTRY/research/sources/d0_original_unpadded42_2026-10-22/"
PINS = {
    ORIGINAL+"RESULT.json": "0ac76b58522d84f5bcc787fb6b6da0c99e1211cd",
    ORIGINAL+"center_new.json": "6b520fbd6218444601d90d7e30b738f8c828bd22",
    ORIGINAL+"check_unpadded42.py": "2d441ee3bc656a6872c8865f5846ef90c4d58038",
}
def pinned_bytes(path, expected):
    data = (ROOT/path).read_bytes()
    blob = hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    if blob != expected:
        raise AssertionError(("original frozen scientific owner changed", path, blob, expected))
    return data

def less(record, key):
    value = record[key]
    if not (isinstance(value,str) and value.startswith("<")):
        raise AssertionError(("not a rigorous strict upper bound", key,value))
    return Decimal(value[1:].split()[0])

def greater(record, key):
    value = record[key]
    if not (isinstance(value,str) and value.startswith(">")):
        raise AssertionError(("not a rigorous strict lower bound", key,value))
    return Decimal(value[1:].split()[0])

def compute():
    originals = {k:pinned_bytes(k,v) for k,v in PINS.items()}
    certificate = json.loads(originals[ORIGINAL+"RESULT.json"])
    center = json.loads(originals[ORIGINAL+"center_new.json"])
    assert certificate["status"] == "PASS_LOCAL_OUTWARD_INTERVAL_BANACH_ORIGINAL_UNPADDED_42_ROOT"
    assert "0/10" in certificate["result"]
    assert "1+click" in certificate["actual_changed_payment"]
    assert "sigma-minus" in certificate["original_model"]
    assert len(center["z42"]) == 42
    cc = certificate["certificate"]
    assert cc["original_full_Hessian_entries"] == 42**2
    preconditioner = less(cc,"original_old_root_rational_preconditioner_infinity_upper")
    defect = less(cc,"certified_new_near_inverse_infinity")
    drift = less(cc,"center_drift_infinity")
    assert less(cc,"center_full_gradient_infinity_upper") < Decimal("1e-50")
    center_radius = Decimal(cc["real_exact_root_ball_radius_infinity"])
    R = Decimal(certificate["analytic_domain"]["complex_polydisc_radius"])
    assert R == Decimal("1e-4")
    scalar_M = Decimal("20")
    assert less(certificate["analytic_domain"],"full_scalar_abs_upper") < scalar_M
    # Same holomorphic polydisc/Cauchy derivative estimate as the owned
    # unpadded proof, now applied to a LARGER real source-robustness ball.
    C = Decimal(42)**2 * Decimal(48) * scalar_M / R**3
    source_ball = Decimal("1e-20")
    permitted_source = Decimal("1e-22")
    permitted_source_lip = Decimal("0.01")
    qbase = defect + preconditioner*C*source_ball
    total_image = drift + qbase*source_ball + preconditioner*permitted_source
    contraction = qbase + preconditioner*permitted_source_lip
    assert source_ball + center_radius < R/2
    assert Decimal("0") < qbase < Decimal("1")
    assert total_image < source_ball
    assert contraction < 1
    # Every continuous full 42-source obeying the norm budget has an EXACT
    # zero by Brouwer. Lipschitz source adds exact uniqueness by Banach.
    # No 'all other 41 rows vanish' hypothesis is needed.
    displacement_bound = preconditioner*permitted_source/(1-qbase)
    assert displacement_bound < source_ball
    # Largest perturbation allowable by THIS conservative Cauchy majorant:
    # optimize ((1-d)-A*C*r)*r/A over r>0. This is a SUFFICIENT
    # certificate envelope, NOT an obstruction for larger physical source.
    optimal_ball = (1-defect)/(2*preconditioner*C)
    optimal_residual = (1-defect)**2/(4*preconditioner**2*C)
    assert optimal_ball > 0
    assert optimal_residual > permitted_source
    # Only when the actual residual is the gradient of a genuine C2 PRICE
    # with ||Hessian||_inf <= .01 does the original saddle's inertia persist.
    original_positive = greater(cc,"strict_positive_coframe_e00_Hessian")
    original_negative = less(cc,"strict_negative_coframe_e11_Hessian")
    variation = C*(source_ball+center_radius)
    positive_after = original_positive - variation - permitted_source_lip
    negative_after = original_negative + variation + permitted_source_lip
    assert positive_after > Decimal("2.89")
    assert negative_after < Decimal("-1.02")
    # A hostile high source violates THIS small sufficient ball, but
    # this is NOT a global physical no-go.
    hostile_source = Decimal("2e-22")
    assert drift + qbase*source_ball + preconditioner*hostile_source > source_ball
    return {
       "status": "PASS_RIGOROUS_DOWNSTREAM_UNPADDED_0_10_FULL42_SOURCE_ROBUSTNESS",
       "consumed_original_result_blob":PINS[ORIGINAL+"RESULT.json"],
       "old_certificate_preserved": True,
       "actual_original_code":"0 cost 1; 10 cost 2; same native N1 Golden/CAR/six faces",
       "dimensions":42,
       "complex_polydisc_radius":str(R),
       "holomorphic_scalar_M":str(scalar_M),
       "preconditioner_upper":str(preconditioner),
       "center_I_minus_AH_upper":str(defect),
       "center_drift_upper":str(drift),
       "third_derivative_Cauchy_Lipschitz_upper":str(C),
       "continuous_all42_source": {
          "real_cube_radius":str(source_ball),
          "full_first_source_supremum_allowed":str(permitted_source),
          "base_preconditioned_Jacobian_defect_upper":str(qbase),
          "map_image_radius_upper":str(total_image),
          "strict_Brouwer_inclusion":True,
          "exact_real_root_exists":True,
          "full42_other_rows_must_vanish":False,
          "root_displacement_from_old_unpadded_root_upper":str(displacement_bound)
       },
       "Lipschitz_source": {
          "Lipschitz_constant_allowed":str(permitted_source_lip),
          "Banach_contraction_upper":str(contraction),
          "exact_root_unique_in_cube":True
       },
       "best_source_budget_of_this_particular_majorant": {
          "optimized_real_cube_radius":str(optimal_ball),
          "strict_supremum_must_be_below":str(optimal_residual),
          "not_a_global_impossibility_when_exceeded":True
       },
       "C2_extra_price_only": {
          "Hessian_operator_norm_upper":str(permitted_source_lip),
          "unrestricted_positive_coframe_Hessian_lower":str(positive_after),
          "unrestricted_negative_coframe_Hessian_upper":str(negative_after),
          "uncorrected_saddle_cannot_become_full_open_field_minimum":True
       },
       "scope": {
          "actual_remaining_Book03_HJR_source_evaluated":False,
          "physical_0_10_execution_compulsorily_selected":False,
          "42_field_writer_reachable":False,
          "upstream_input_clock_preparation_Euler_solved":False,
          "arbitrary_original_AF_PF_weights_or_uniform_refinement":False,
          "GR_closed":False
       }
    }

if __name__ == "__main__":
    print(json.dumps(compute(),indent=2))
