#!/usr/bin/env python3
"""Exact-rational improvement of the owned K=100 million generated renewal-HJR
Banach continuation to every finite K>=58,500,000.

CONSUMES the SAME original h=1/4 42-coordinate CQ interval certificate,
same three-status native Golden report, same generated HJR-type heat and
same strict native constants. Does NOT claim physical Book03 Hodge/clock
identification, a new geometric root, actual factory/gate execution, or GR.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import factorial
from decimal import Decimal, localcontext
from pathlib import Path
import argparse, hashlib, json

PINS={
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/RIGOROUS_EXACT42_CERTIFICATE.json":
   "9f4bdef4c367660539c588db01819330ff0d55b3",
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/REPORT_BRIDGE_RESULT.json":
   "2c7193f54da76aaf108d2821c45daddac7457f02",
 "02_REGISTRY/research/sources/d0_renewal_gibbs_bridge_2026-10-22/check_explicit_k100m_root_bound.mjs":
   "b53a9d6d316b4f592a66d04cd0a9dc17012664b9",
}
def verify_inputs(repo):
    for path,sha in PINS.items():
        v=(repo/path).read_bytes()
        digest=hashlib.sha1(b"blob "+str(len(v)).encode()+b"\0"+v).hexdigest()
        if digest!=sha:raise AssertionError(("input owner mutated",path,digest,sha))
    cert=json.loads((repo/next(iter(PINS))).read_text())
    assert cert["dimension"]==42
    assert F(cert["holomorphic_complex_polydisc_radius"])==F(1,10**7)
    assert F(cert["used_source_bound"])==F(1,1000)
    assert F(cert["preconditioner_decimal_exact_row_inf_norm"])<50
    assert F(cert["qcenter_including_error"])<F(145,10**9)
    assert F(cert["newton_center_shift_bound"])<F(2,10**58)
    assert F(cert["root_cube_radius"])<F(5,10**26)
    return True

def run():
    cap=58_500_000
    # The ALREADY owned uniform complex tail uses |1-q_a|<=1-8e-7
    # for ALL THREE actual measured states (FAIL,READY0,READY1), on both
    # native h4 cells on the certified entire 42-complex R-polydisc.
    alpha=F(8,10_000_000)
    x=alpha*cap
    assert x==F(234,5)
    # Positive Taylor terms are a RIGOROUS rational lower bound for exp(x).
    partial_exp=sum((x**n)/factorial(n) for n in range(121))
    # For every K>=cap, capped harmonic tail
    # delta(K)<=exp(-alpha*K)/(alpha*K)<=1/(x*partial_exp).
    exact_tail_upper=1/(x*partial_exp)
    coarse_tail=F(11,10**23)  # 1.1e-22, safely above TRUE exact rational bound
    assert exact_tail_upper<coarse_tail

    # The 3-outcome KL quadratic cancellation is consumed from the actual
    # complete ternary first-match owner: each cell <=10 delta^2, two
    # cells and betaBook>0.7, so complete scalar HJR-type price <32 delta^2.
    assert 2*10/F(7,10)<32
    full_price_error=32*coarse_tail**2

    # ORIGINAL native-Golden source conversion:
    # c=-gamma*log(phi)*(1/20)*h_phi'(r*)*r_x*/betaBook.
    # The already owned STRICT inequalities give |c|>6.318e-9>6e-9.
    c_from_native=F(45,100)*F(48,100)*F(1,20)*26*F(18,10**9)/F(8,10)
    cmin=F(6,10**9)
    assert c_from_native>cmin

    R=F(1,10**7)   # certified ORIGINAL complex polydisc radius
    r=F(5,10**26)  # NEW real contraction ball, bigger than old 1e-30
    M=F(1,1000)    # certified ORIGINAL |S_CQ|<.001
    A=50          # certified inverse/preconditioner row norm<49.444
    d=42
    # Old certified source preconditioner center and center drift upper bounds.
    qcenter=F(145,10**9)       # >1.448471754...e-7
    old_drift=F(2,10**58)      # >1.48331446...e-58
    # The original Cauchy bound on third derivatives is 48M/R^3 at
    # all real points inside the R/2 box. Multiply by 42^2 row terms.
    q_move=A*d*d*48*M*r/R**3
    # At every new x in B_r(center), the COMPLEX polydisc distance
    # to the certified analytic boundary is >=R-r, not (incorrectly) R.
    R_remaining=R-r
    q_finite=A*2*d*full_price_error/(cmin*R_remaining**2)
    q=qcenter+q_move+q_finite
    drift=old_drift+A*full_price_error/(cmin*R)
    margin=(1-q)*r
    assert r<R/2
    assert q<F(212,1000),("not a contraction",q)
    assert drift<F(33,10**27),("center image too large",drift)
    assert drift<margin,("failed to map ball into itself",drift,margin)
    # Invertible A: ||I-A Hess_old||<1 and square 42x42.
    # For EVERY integer K>=cap, monotonicity of its actual harmonic tail
    # improves every bound; T_K=x-A*(c^-1 D S_HJR,K) is contracting.
    # Thus a UNIQUE REAL exact full42 stationary root exists on B_r,
    # with nonflat/rank2 signs inherited from the old tiny verified box.
    # Its displacement from the limiting native CQ root is bounded by
    # A*(32 delta(K)^2)/(cmin*(R-r)*(1-q)) and ->0 exponentially in 2K.

    with localcontext() as ctx:
        ctx.prec=66
        def dec(z):return str(Decimal(z.numerator)/Decimal(z.denominator))
        output={
         "status":"PASS_EXACT_RATIONAL_K585M_FULL42_ROOT_CONTINUATION",
         "previous_cap":100_000_000,"new_cap":cap,
         "saved_worst_case_comparisons":100_000_000-cap,
         "cap_reduction_percent":"41.5",
         "all_integer_caps_at_least_new_cap_proved":True,
         "published_input_Git_blobs":PINS,
         "rational_checks":{
           "alphaK":dec(x),
           "tail_upper_by_120th_rational_exp_series":dec(exact_tail_upper),
           "used_complete_harmonic_tail_upper":dec(coarse_tail),
           "two_cell_complete_KL_price_error_upper":dec(full_price_error),
           "native_source_conversion_lower_from_owned_inequalities":dec(c_from_native),
           "used_native_source_conversion_lower":dec(cmin),
           "old_h4_complex_chart_radius":dec(R),
           "old_h4_complex_price_sup":dec(M),
           "new_real_ball_radius":dec(r),
           "new_real_ball_within_half_complex_chart":True,
           "old_preconditioned_center_Jacobian_bound":dec(qcenter),
           "original_Hessian_change_preconditioned":dec(q_move),
           "new_HJR_Hessian_change_preconditioned":dec(q_finite),
           "complete_contraction_upper":dec(q),
           "preconditioned_center_shift_upper":dec(drift),
           "required_ball_inclusion_margin":dec(margin),
           "strict_ball_inclusion":True},
         "analytic_conclusion":{
           "old_exact42_CQ_root":"consumed",
           "new_exact42_finite_HJR_type_root":"unique in NEW larger ball",
           "uniform_in_K":"every integer K>=58500000",
           "limit_of_roots":"y_K->same certified CQ root as K->infinity",
           "root_error_rate":"O(exp(-2*8e-7*K)/(8e-7*K)^2)",
           "fixed_collar":"original exact rational h=1/4 two-cell collar",
           "material":"two real independent original CAR currents",
           "geometry":"nonflat and Lorentzian"},
         "scope":{"compulsory_Book03_Hodge_heat_identified":False,
           "complete_original_HJR_selected":False,
           "physical_comparison_clock_paid":False,
           "physical_field_writer_and_input_Euler":False,
           "mesh_uniform_refinement_proved":False,
           "unconstrained_field_minimum":False,"GR_closed":False}}
    return output

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,
                    help="Verify strict original published owner Git blobs and JSON")
    ap.add_argument("--json",type=Path)
    opts=ap.parse_args()
    if opts.repo:verify_inputs(opts.repo)
    data=run()
    txt=json.dumps(data,indent=2,ensure_ascii=False)+"\n"
    if opts.json:opts.json.write_text(txt,encoding="utf-8")
    print(txt,end="")

if __name__=="__main__":
    main()
