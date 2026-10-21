#!/usr/bin/env python3
"""VALIDATED 42-field interval Newton/Banach root in the original D0 N1 CQ.

Inputs are exact SHA-pinned rational decimals. Original six-face star and
actual sigma-minus Golden N1 nonlinear CQ function, one unrestricted
16+24+2 original field node and fixed two-neighbor rational collar.

CRITICAL: interval matrix exp has an explicit rigorous Taylor tail;
mpmath.iv.expm's tolerance-truncated output MUST NOT replace it.

Numerically generated A is only an arbitrary preconditioner, converted
to EXACT decimal rationals; the published theorem depends exclusively on
OUTWARD interval inequalities for I-A*H and D S. It does not trust rank
or a numerical optimizer. Can take several minutes to run full certificate.
"""
from __future__ import annotations
import argparse, json, sys, hashlib, time
from pathlib import Path
from decimal import Decimal, getcontext
from mpmath import mp,iv

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
from certified_model import CQ, rational_center, COLLAR, CENTER

ORIGINAL={
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py":
"a57f0e3e845290923c2ac88d39ba5c08af4f6fd6",
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/full_n1_euler_analytic.py":
"7ea28c981826c96b01bbdda67a92010dc7221095",
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_full42_n1_single_internal.py":
"da83e40379867f71b598fecd8430444ea027a4da",
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/FULL42_NUMERICAL_REFERENCE.json":
"0d49a7fe811d73c386b0ad644588ff7b1f410e6f"
}
N=42
def check_original_sources():
    for name,sha in ORIGINAL.items():
        b=(REPO/name).read_bytes()
        got=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
        assert got==sha, ("original owner changed",name,got,sha)

def exact_rational_preconditioner():
    """Only GENERATE a candidate A from the original native 42-row source.

    All 1764 entries are then frozen into decimal rationals and verified by
    interval I-A*H below. Thus numpy/scipy are NOT trusted for existence.
    """
    import numpy as np
    from scipy.optimize._numdiff import approx_derivative
    origin=REPO/"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21"
    sys.path.insert(0,str(origin))
    from check_full42_n1_single_internal import problem
    _,_,_,_,_,euler=problem(n=2,weights=[1.,1.])
    witness=json.loads((origin/"FULL42_NUMERICAL_REFERENCE.json").read_text())
    z=np.array(witness["witnesses"]["uniform"]["params42"],dtype=float)
    Jfloat=approx_derivative(euler,z,abs_step=2e-5,method="3-point")
    A=np.linalg.inv(Jfloat)
    rationals=[[format(float(A[i,j]),'.17g') for j in range(N)] for i in range(N)]
    rational_norm=max(sum(abs(Decimal(v)) for v in row) for row in rationals)
    assert rational_norm<Decimal(40)
    return rationals,rational_norm

def certified_bound(opts):
    getcontext().prec=160
    iv.dps=115
    start=time.monotonic()
    model=CQ(iv)
    z=rational_center(iv)
    R=Decimal("1e-4")
    M=Decimal(10)
    scale=lambda t:iv.mpf(str(t))
    box=[]
    for value in CENTER["z42"]:
        t=Decimal(value)
        box.append(iv.mpc([str(t-R),str(t+R)],[str(-R),str(R)]))
    boxprice=model.price(box)
    assert abs(boxprice).b<scale(10),"original whole price complex analytic bound"
    assert len(model.last_clicks)==2
    for click in model.last_clicks:
        assert click.real.a>scale("1e-6")
        assert click.real.b<scale("1e-5")
        assert (1-click).real.a>scale(".9999")
    assert len(CENTER["z42"])==42 and len(COLLAR["psi1"])==3
    if opts.verbose:
        print("PASS original N1 analytic complete complex polydisc, certified exp tail",
              round(time.monotonic()-start,2),flush=True)
    # Source F=grad S via true complex-step. Use Cauchy bound for the
    # imaginary-step truncation error (not a claim that any finite step is
    # itself the exact derivative).
    S0=model.price(z).real
    def shift(k,step,l=None,sign=1):
        out=z.copy()
        out[k]=iv.mpc(out[k],iv.mpf(step))
        if l is not None:
            out[l]=iv.mpc(out[l],iv.mpf(str(Decimal(step)*sign)))
        return out
    df=Decimal("1e-40")
    marginF=Decimal(2)*M*df*df/R**3
    F=[]
    for k in range(N):
        d=model.price(shift(k,str(df))).imag/scale(df)
        F.append(d)
        if opts.verbose and (k+1)%10==0:
            print("source entries",k+1,flush=True)
    fmax=max(abs(v).b for v in F)+scale(marginF)
    assert fmax<scale("1e-62"),fmax
    if opts.smoke:
        return {"status":"PASS_CERTIFIED_FULL42_SMOKE_NOT_EXISTENCE",
                "full_complex_price_abs_upper":"<10",
                "center_first_source_upper":str(fmax),
                "rigorous_matrix_expm":"Taylor 30 / 2^11; exact bound 1e-120",
                "full_interval_Hessian_computed":False,
                "GR_closed":False}
    # Entire Hessian, 1764 entries, independently by interval differences
    # of the SCALAR PRICE rather than reusing the native 42-row Euler code.
    dj=Decimal("1e-19")
    d=scale(dj)
    marginJ=scale(4*M*dj*dj/R**4)
    J=[[None]*N for _ in range(N)]
    for i in range(N):
        s_i=model.price(shift(i,str(dj))).real
        J[i][i]=-2*(s_i-S0)/(d*d)+iv.mpf([-1,1])*marginJ
        for j in range(i+1,N):
            p=model.price(shift(i,str(dj),j,+1)).real
            q=model.price(shift(i,str(dj),j,-1)).real
            v=-(p-q)/(2*d*d)+iv.mpf([-1,1])*marginJ
            J[i][j]=v
            J[j][i]=v
        if opts.verbose and (i+1)%4==0:
            print("Hessian certified rows",i+1,"sec",round(time.monotonic()-start,1),flush=True)
    # Two strict real signed directions, as the original physical coframe
    # is varied UNRESTRICTED inside the declared finite 42-input collar.
    assert J[0][0].a>scale(2),"original e00 positive second derivative"
    assert J[5][5].b<scale("-.7"),"original e11 negative second derivative"
    # A from original double root is EXACTLY rationalized here; the ONLY
    # validity test of A is the rigorous interval near-inverse inequality.
    A,rational_norm=exact_rational_preconditioner()
    Ai=[[iv.mpf(v) for v in row] for row in A]
    normA=scale(rational_norm)
    defect=iv.mpf(0)
    for i in range(N):
        rowsum=iv.mpf(0)
        for j in range(N):
            x=sum(Ai[i][k]*J[k][j] for k in range(N))
            v=(iv.mpf(1) if i==j else iv.mpf(0))-x
            rowsum+=abs(v).b
        defect=max(defect,rowsum.b)
    # Holomorphic Cauchy bound on complete polydisc D_R for all
    # third partials in D_{R/2}: 3!*2^3*M/R^3=48*M/R^3.
    # Summing over 42 field coordinates and 42 Hessian rows:
    # ||J(x)-J(center)||inf <=42^2*48*M*||x-center||inf/R^3.
    ball=Decimal("1e-24")
    shiftbound=Decimal(N*N*48)*M*ball/R**3
    contraction=defect+normA*scale(shiftbound)
    drift=normA*fmax
    assert contraction<scale(".01"),contraction
    assert drift<scale((Decimal(1)-Decimal(".01"))*ball),drift
    # Actual oriented nondegenerate coframe, nonidentity original spatial
    # 4x4 holonomy and TWO independent real material directions survive
    # throughout the (much smaller) validated REAL root ball.
    rball=[]
    for v in CENTER["z42"]:
        mid=Decimal(v)
        rball.append(iv.mpf([str(mid-ball),str(mid+ball)]))
    e,U,ps=model.nodes(rball)
    det=iv.det(e)
    assert det.a>scale(1),"oriented nondegenerate original coframe"
    P=U[1]*U[2]*(model.eta*U[1].T*model.eta)*(model.eta*U[2].T*model.eta)
    assert P[1,2].real.a>scale(".001"),"nonidentity original based spatial holonomy"
    p1t=(ps[1][0]-ps[0][0])/model.h
    assert p1t.a>scale(".08"),"first real scalar gradient active"
    assert model.amp.a>scale(".1"),"second real scalar gradient active"
    # Any root has Hessian deviation <= 42*48*M*ball/R^3 in a given
    # matrix entry. So the positive and negative directions persist.
    entryshift=scale(Decimal(N*48)*M*ball/R**3)
    assert J[0][0].a-entryshift>scale(2)
    assert J[5][5].b+entryshift<scale("-.7")
    report={
      "status":"PASS_RIGOROUS_INTERVAL_BANACH_FULL42_N1",
      "interpretation":"EXACT real stationary root of ALL 42 configured finite CQ Euler equations, unique in the stated small ball",
      "original":"six canonical G2STAR based plaquettes; same sigma-minus complete N1 Golden price; 2 original real CAR scalar fields",
      "rational_input":{"h":COLLAR["h"],"PF":[1,1],
             "collar_sha256":"b86d94a59f5b0ecfec55af3a6c0db80eec257d41b09f3a03c59e367f56093fa1",
             "center_sha256":"0258a6bc84446dd8a506479acc59f4dbf503f3417c508444c516cce9c314f2f5"},
      "verified_matrix_exponential":{"scale":2048,"taylor_degree":30,
            "elementwise_tail_upper":"1e-120",
            "input_generator_norm":"strictly < 1 over whole complex polydisc"},
      "complex_analytic_price":{"polydisc_radius":"1e-4",
            "uniform_absolute_price_upper":10,"click_real_lower":"1e-6",
            "click_real_upper":"1e-5"},
      "bounded_center_source_inf":str(fmax),
      "rational_preconditioner_norm_inf":str(rational_norm),
      "interval_near_inverse_defect_inf":str(defect),
      "Hessian_Lipschitz_times_ball":str(shiftbound),
      "contraction_inf":str(contraction),
      "center_drift_inf":str(drift),
      "root_ball_radius_inf":str(ball),
      "saddle":{"e00_second_source_lower":str(J[0][0].a),
                "e11_second_source_upper":str(J[5][5].b),
                "positive_and_negative_original_free_coframe_directions":True},
      "nontrivial_witness":{"det_coframe_lower":str(det.a),
          "spatial_holonomy_12_lower":str(P[1,2].real.a),
          "two_independent_real_CAR_field_gradients":True},
      "proof":"Banach on x -> x - A*grad(S), real complete 42 field source, strict contraction",
      "scope":{"full42_real_root_one_fixed_rational_collar":True,
               "PF_true_spatially_variable_AF_masses":False,
               "second_PF_[1,2]_exact_proved":False,
               "n3_or_h_to_zero_refinement":False,
               "unconstrained_minimum":False,
               "physical_Book03_HJR_price_selected":False,
               "native_primitive_field_writer_admitted":False,
               "GR_closed":False}}
    return report

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--smoke",action="store_true",
                    help="only complete analytic box/center source; NOT an existence proof")
    ap.add_argument("--verbose",action="store_true")
    ap.add_argument("--json",type=Path)
    opts=ap.parse_args()
    check_original_sources()
    result=certified_bound(opts)
    data=json.dumps(result,indent=2)+"\n"
    print(data,end="")
    if opts.json:
        opts.json.write_text(data,encoding="utf-8")

if __name__=="__main__":
    main()
