#!/usr/bin/env python3
"""Strict interval Banach 42-root for the ORIGINAL UNPADDED Golden F/R 0/10.

No new action/operator/report probability, free fit, dropped abort or arbitrary
42-row assumption. Use ORIGINAL certified_model.CQ, original SHA-pinned h0
three-node collar and its original 16 coframe+24 Lorentz+2 CAR model.
Add only real declared terminal expected code cost E[C_0/10]=1+click.
This checker reconstructs the PREVIOUS original rational preconditioner
at its old CQ center, then rigorously checks it on the new native scalar source.
The numerical original A is merely a proposal: complete interval I-AH<1
is the proof. The new 42-vector center is an exact rational-decimal string.
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from pathlib import Path
import argparse, json, time
from mpmath import iv
from certified_unpadded import NativeUnpaddedCQ, CENTER, COLLAR, rational_center
from check_interval42 import exact_rational_preconditioner, check_original_sources

N=42

def proof(smoke=False, verbose=False):
    check_original_sources()
    getcontext().prec=160
    iv.dps=115
    start=time.monotonic()
    model=NativeUnpaddedCQ(iv)
    z=rational_center(iv)
    R=Decimal("1e-4")
    M=Decimal(20)
    scale=lambda x:iv.mpf(str(x))
    box=[]
    for value in CENTER["z42"]:
        t=Decimal(value)
        box.append(iv.mpc([str(t-R),str(t+R)],[str(-R),str(R)]))
    whole=model.price(box)
    absbox=abs(whole).b
    assert absbox<scale(M), ("entire N1 code price complex box",absbox)
    assert len(model.last_clicks)==2
    for q in model.last_clicks:
        assert q.real.a>scale("1e-6")
        assert q.real.b<scale("1e-5")
        assert (1-q).real.a>scale(".9999")
    S0=model.price(z).real
    def shift(i,step,j=None,sign=+1):
        out=z.copy()
        out[i]=iv.mpc(out[i],scale(step))
        if j is not None:
            out[j]=iv.mpc(out[j],scale(str(Decimal(step)*sign)))
        return out
    df=Decimal("1e-40")
    marginF=scale(Decimal(2)*M*df*df/R**3)
    F=[]
    for k in range(N):
        value=model.price(shift(k,str(df))).imag/scale(df)
        F.append(value)
        if verbose and (k+1)%10==0:
            print("original native 0/10 gradient rows",k+1,flush=True)
    fmax=max(abs(v).b for v in F)+marginF
    assert fmax<scale("1e-50"), ("center source too large",fmax)
    if smoke:
        return {"status":"PASS_UNPADDED42_ANALYTIC_SMOKE_NOT_EXISTENCE",
            "complex_box_price_lt_20":str(absbox),
            "first_source_interval_bound":str(fmax),
            "GR_closed":False}

    # Explicitly enclose all 42*42 Hessian values of the SAME full scalar
    # price with outward iv and a Cauchy-verified complex-step truncation.
    dj=Decimal("1e-19")
    d=scale(dj)
    marginJ=scale(Decimal(4)*M*dj*dj/R**4)
    H=[[None]*N for _ in range(N)]
    for i in range(N):
        si=model.price(shift(i,str(dj))).real
        H[i][i]=-2*(si-S0)/(d*d)+iv.mpf([-1,1])*marginJ
        for j in range(i+1,N):
            p=model.price(shift(i,str(dj),j,+1)).real
            q=model.price(shift(i,str(dj),j,-1)).real
            v=-(p-q)/(2*d*d)+iv.mpf([-1,1])*marginJ
            H[i][j]=v
            H[j][i]=v
        if (i+1)%4==0 and verbose:
            print("new complete 0/10 Hessian rows",i+1,
                "seconds",round(time.monotonic()-start,1),flush=True)
    assert H[0][0].a>scale(2)
    assert H[5][5].b<scale("-.7")

    # Crucial SYNTHESIS: reuse the PREVIOUS certified mathematical inverse
    # candidate for the original padded root WITHOUT redefining it, or any
    # fitted source. The entire new near-inverse remains independently
    # outward-verified despite the physically different actual code cost.
    Arational,Anorm=exact_rational_preconditioner()
    Ai=[[iv.mpf(v) for v in row] for row in Arational]
    Ainf=scale(Anorm)
    defect=iv.mpf(0)
    for i in range(N):
        rowsum=iv.mpf(0)
        for j in range(N):
            x=sum(Ai[i][k]*H[k][j] for k in range(N))
            v=(iv.mpf(1) if i==j else iv.mpf(0))-x
            rowsum+=abs(v).b
        defect=max(defect,rowsum.b)
    # Uniform exact holomorphic Cauchy third-derivative bound on the half box.
    # ||D2S(z)-D2S(zcenter)||inf <= 42^2*48*M ||z-zcenter||inf/R^3
    ball=Decimal("1e-24")
    shiftbound=Decimal(N*N*48)*M*ball/R**3
    contraction=defect+Ainf*scale(shiftbound)
    drift=Ainf*fmax
    assert defect<scale(".04"), ("new native-code source J fails previous inverse",defect)
    assert contraction<scale(".04"), ("Banach strict contraction",contraction)
    assert drift<scale(Decimal(".96")*ball), ("Banach image condition",drift)

    # Finite ORIGINAL geometry and two independent real material gradients:
    # full original 42 field variables FREE, nonflat and nonvacuum on ball.
    realball=[]
    for v in CENTER["z42"]:
        t=Decimal(v)
        realball.append(iv.mpf([str(t-ball),str(t+ball)]))
    e,U,ps=model.nodes(realball)
    det=iv.det(e)
    assert det.a>scale(1)
    Pxy=U[1]*U[2]*(model.eta*U[1].T*model.eta)*(model.eta*U[2].T*model.eta)
    assert Pxy[1,2].real.a>scale(".001")
    assert ((ps[1][0]-ps[0][0])/model.h).a>scale(".08")
    assert model.amp.a>scale(".1")
    entryshift=scale(Decimal(N*48)*M*ball/R**3)
    assert H[0][0].a-entryshift>scale(2)
    assert H[5][5].b+entryshift<scale("-.7")

    return {
      "status":"PASS_RIGOROUS_BANACH_LITERAL_NATIVE_0_10_ALL42_N1_NONFLAT_RANK2",
      "reused_original_operators":"unchanged six G2STAR based plaquettes, original N1 p=phi^-1 z=2^-20 sigma-minus two CAR currents; real original h0 collar and all 42 free field rows",
      "actual_terminal_code":"original F cost1/ R cost2 => real E[C_report]=1+click; no equal-width padding",
      "rational_center_dimension":42,
      "rigorous_matrix_exponential":"original Taylor30 / 2^11 and 1e-120 elementwise remainder",
      "whole_complex_polydisc_radius":"1e-4",
      "whole_scalar_price_complex_upper":str(absbox),
      "original_old_CQ_preconditioner_reused":True,
      "all_Hessian_entries_outward_interval":1764,
      "center_full42_source_inf_upper":str(fmax),
      "rational_preconditioner_inf_upper":str(Anorm),
      "verified_new_inverse_defect_inf":str(defect),
      "Hessian_Lipschitz_times_ball":str(shiftbound),
      "Banach_contraction_inf":str(contraction),
      "center_drift_inf":str(drift),
      "exact_root_existence_and_uniqueness_ball_inf":"1e-24",
      "nonflat_based_spatial_holonomy_12_lower":str(Pxy[1,2].real.a),
      "positive_oriented_coframe_det_lower":str(det.a),
      "two_independent_real_CAR_gradients":True,
      "original_coframe_Hessian_positive_lower":str(H[0][0].a-entryshift),
      "original_coframe_Hessian_negative_upper":str(H[5][5].b+entryshift),
      "actual_unpadded_price_is_compulsory_full_Book03_HJR":False,
      "all_independent_preparation_clock_oldRIGHT_Euler":False,
      "native_G0_input_writer_admitted":False,
      "original_raw216_uniform_refinement":False,
      "GR_closed":False
    }

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--smoke",action="store_true",
                   help="analytic chart and 42 source but NOT existence")
    a.add_argument("--verbose",action="store_true")
    a.add_argument("--json",type=Path)
    args=a.parse_args()
    result=proof(args.smoke,args.verbose)
    txt=json.dumps(result,indent=2)+"\n"
    print(txt,end="")
    if args.json: args.json.write_text(txt,encoding="utf-8")

if __name__=="__main__":main()
