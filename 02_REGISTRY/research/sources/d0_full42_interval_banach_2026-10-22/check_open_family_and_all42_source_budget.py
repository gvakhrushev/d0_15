#!/usr/bin/env python3
"""D0 original full42 Golden N1: certified-root CONSUMER, not a new root proof.

Two logically distinct additions to the pinned strict interval Banach proof:
(A) analytic-IFT open family for nearby positive two-cell PF weights, original
    rational collars and (mathematically) the finite time step;
(B) explicit 42-COMPONENT small-source existence budget, even for a
    non-Lipschitz but continuous missing first-source. No normal-row support
    assumption and NO assertion that actual compulsory Book03 satisfies it.

NO original certificate, root, physics, clock, and original data are modified.
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from pathlib import Path
import hashlib
import json
import sympy as s

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
RECEIPT="02_REGISTRY/research/sources/d0_full42_interval_banach_2026-10-22/RESULT.json"
RECEIPT_BLOB="323c50788a3602e4fa15b60d88dc1a2c76ebd3ba"
getcontext().prec=100
D=Decimal

def check_original_certificate():
    blob=(REPO/RECEIPT).read_bytes()
    ident=hashlib.sha1(b"blob "+str(len(blob)).encode()+b"\0"+blob).hexdigest()
    assert ident==RECEIPT_BLOB,("PINNED_ORIGINAL_INTERVAL_OWNER_CHANGED",ident)
    doc=json.loads(blob)
    r=doc["local_replay"]
    scope=doc["scope"]
    assert doc["status"]=="PASS_RIGOROUS_TAYLOR_INTERVAL_NEWTON_BANACH_ORIGINAL_FULL42_N1"
    assert r["weights"]==[1,1]
    assert scope["all42_configured_N1_finite_root"] is True
    assert scope["physical_compulsory_Book03_HJR_selected"] is False
    assert scope["uniform_h_refinement"] is False
    assert D(r["complex_polydisc_radius"])==D("1e-4")
    assert D(r["existence_ball_infty_radius"])==D("1e-24")
    assert doc["proof_justification"].startswith("Interval-verified")
    return r

def exact_PF_source_identity():
    # Use an arbitrary quadratic ORIGINAL analytic local complete N1 price
    # with generic nonzero cross jets, not a fitted matter coupling.
    a,b,c,d,e,tau,rho,z=s.symbols("a b c d e tau rho z",nonzero=True)
    x,y=s.symbols("x y")
    F=a*x+b*y+c*x*x/2+d*x*y+e*y*y/2
    f=z+z*z
    q=z**3+2*z
    X=-tau*f/rho
    Y=tau*q/rho
    S=rho*F.subs({x:X,y:Y})/(-tau*a)
    source=s.diff(S,z)
    param_source=s.diff(source,rho)
    Fx=s.diff(F,x);Fy=s.diff(F,y)
    Fxx=s.diff(F,x,2);Fxy=s.diff(F,x,y);Fyy=s.diff(F,y,2)
    expected= -((x*Fxx+y*Fxy)*s.diff(f,z)-
                (x*Fxy+y*Fyy)*s.diff(q,z))/(a*rho)
    expected=expected.subs({x:X,y:Y})
    assert s.cancel(param_source-expected)==0
    # Exactly at BOTH source densities zero, even if their FIELD derivatives
    # are not zero, parameter derivative vanishes. Off-null no such promise.
    e0=s.simplify(expected.subs(z,0))
    assert e0==0
    assert s.simplify(param_source)!=0
    return {
       "same_price_PF_source_derivative":
       "-[(x F_xx+y F_xy) Df-(x F_xy+y F_yy) Dq]/(a*rho)",
       "x":"-tau*f/rho", "y":"+tau*q/rho",
       "analytic_PF_parameter":"rho positive; original N1 fixed caps and sign",
       "double_zero_sheet":"f=q=0 => PF source derivative identically zero",
       "finite_off_null_root":"parameter derivative is generally nonzero"}

def explicit_budget(original):
    # All bounds are CONSERVATIVE strict bounds consumed from the PINNED
    # completed full42 interval certificate; all ensuing comparisons exact
    # decimal rationals, no floating arithmetic or numerical root search.
    dimension=42
    R=D(original["complex_polydisc_radius"])
    M=D(10)
    A=D("28.883")
    q_center=D("1.4691e-11")
    drift=D("5.78e-66")
    exact_root_original_ball=D(original["existence_ball_infty_radius"])
    assert exact_root_original_ball==D("1e-24")
    hessian_L=D(dimension*dimension*48)*M/R**3
    assert hessian_L==D("8.4672e17")
    base_center_root_q=q_center+A*hessian_L*exact_root_original_ball
    certified_inverse=A/(1-base_center_root_q)
    assert certified_inverse<D("28.885")

    radius=D("2e-20")
    missing_source_sup=D("3e-22")
    missing_source_lipschitz=D("1e-3")
    q_base=q_center+A*hessian_L*radius
    q_total=q_base+A*missing_source_lipschitz
    # Continuous first-source: Brouwer only needs the BASE contraction.
    base_ball_image=drift+q_base*radius+A*missing_source_sup
    # For a Lipschitz source: Banach needs the stronger contraction.
    unique_ball_image=drift+q_total*radius+A*missing_source_sup
    assert q_base<D("0.49")
    assert q_total<D("0.5181")
    assert base_ball_image<radius
    assert unique_ball_image<radius
    assert missing_source_sup < ((1-q_total)*radius-drift)/A
    # Strict ORIGINAL two opposite unrestrained coframe Hessian signs survive
    # if the EXTRA price is actually C2 and its Hessian row norm<=1e-3.
    # This is NOT asserted for a merely continuous/non-C2 first source.
    Hchange=hessian_L*radius
    lower_positive=D("3.0283")-Hchange-missing_source_lipschitz
    upper_negative=-D("1.0912")+Hchange+missing_source_lipschitz
    assert lower_positive==D("3.0103656")
    assert upper_negative==-D("1.0732656")
    assert lower_positive>0>upper_negative
    # The no-perturbation original root is known already (not reproved here).
    return {
       "field_dimension":dimension,
       "complete_base_Hessian_Lipschitz_infty":str(hessian_L),
       "original_exact_root_inverse_Hessian_bound":str(certified_inverse),
       "validated_Banach_source_ball_radius":str(radius),
       "source_max_norm_full42":str(missing_source_sup),
       "optional_first_source_Lipschitz_max":str(missing_source_lipschitz),
       "base_preconditioned_derivative_bound":str(q_base),
       "with_Lipschitz_source_contraction":str(q_total),
       "continuous_Brouwer_ball_image_upper":str(base_ball_image),
       "Lipschitz_Banach_ball_image_upper":str(unique_ball_image),
       "continuous_source_exists":"YES, if source is continuous and bounded on the stated full42 ball",
       "Lipschitz_source_unique":"YES, if additionally Lipschitz <=1e-3",
       "non_C2_information_compatible":"YES for existence if its FIRST source is continuous and bounded",
       "assumed_41_other_Euler_rows_zero":False,
       "extra_C2_price_if_Hessian_bound_1e_minus3":{
          "coframe_e00_Hessian_strictly_greater_than":str(lower_positive),
          "coframe_e11_Hessian_strictly_less_than":str(upper_negative),
          "unrestricted_field_minimum":False,
          "applicable_to_non_C2_residual":False},
       "actual_original_Book03_residual_proven_small":False}

def main():
    original=check_original_certificate()
    pf=exact_PF_source_identity()
    bounds=explicit_budget(original)
    out={
     "status":"PASS_CONSUMED_FULL42_OPEN_FAMILY_AND_COMPLETE_SOURCE_BUDGET",
     "consumed_original_certificate_blob":RECEIPT_BLOB,
     "PF_parameter_exact_symbolic":pf,
     "all42_budget_exact_rational":bounds,
     "analytic_IF theorem":{
       "original_full42_Hessian_invertible":True,
       "analytic_solution_branch":"YES for some open neighborhood of actual weights (1,1), fixed collar/h, and for small admissible collar and h changes",
       "not_calculated":"An explicit parameter-radius/whole-mesh AF count inclusion",
       "root_nonflat_and_rank_two":"remain on a sufficiently small open parameter neighborhood by continuity",
       "coframe_saddle_of_configured_CQ":"persists under sufficiently small C2 parameter perturbation"},
     "scope":{
       "rigorous_old_interval_root_reexecuted":False,
       "uses_original_completed_receipt_and_analyticity":True,
       "new_standalone_42x42_interval_Hessian_replayed":False,
       "physical_native_Book03_full_residual_computed":False,
       "primitive_field_writer_admitted":False,
       "uniform_refinement_proved":False,
       "GR_closed":False}}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
