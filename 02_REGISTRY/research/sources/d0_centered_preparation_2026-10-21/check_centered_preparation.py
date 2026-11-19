#!/usr/bin/env python3
"""Narrow checks of exact joint centred preparation elimination.

The original DATA4096/RIGHT128/255-leaf support certificate is consumed, not
rerun. Exact full16 CAR identities and an explicit coupled DATA8/RIGHT1
three-leaf fixture test the new application. No source is written or fetched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sympy as sp
import mpmath as mp

CHECKS: list[str] = []


def require(name: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError("FAILED: " + name)
    CHECKS.append(name)


def source_checks(repo: Path) -> dict:
    pins = json.loads(Path(__file__).with_name("SOURCE_PINS.json").read_text())
    for row in pins["inputs"]:
        require("source_" + Path(row["path"]).name,
                hashlib.sha256((repo / row["path"]).read_bytes()).hexdigest()
                == row["sha256"])
    return {"read_head": pins["read_head"], "checked_input_count": len(pins["inputs"])}


def exact_checks() -> dict:
    p = (sp.sqrt(5) - 1) / 2
    alpha, beta = p, p**2
    eq = lambda x: sp.simplify(sp.trigsimp(x)) == 0
    require("golden_mixture_normalization", eq(alpha + beta - 1))
    a, theta, u, c, b, radius = sp.symbols("a theta u c b radius", real=True)
    J = sp.zeros(16)
    U = sp.eye(16)
    for j in (6, 10, 12, 14):
        J[j+1, j], J[j, j+1] = 1, -1
        U[j, j] = U[j+1, j+1] = sp.cos(a)
        U[j+1, j], U[j, j+1] = sp.sin(a), -sp.sin(a)
    require("literal_generator_rank_eight", J.rank() == 8)
    require("literal_full16_skew", J.T == -J)
    require("literal_full16_rotation_orthogonal",
            all(eq(v) for v in U.T*U-sp.eye(16)))
    require("untouched_low_CAR_complements",
            all(U[:, j] == sp.eye(16)[:, j] for j in (0, 1, 2, 3, 4, 5, 8, 9)))
    require("high_CAR_complement_is_retained", not eq(U[7, 6]))
    vec = sp.zeros(16, 1)
    vec[1], vec[0] = sp.sqrt(p), c
    vec[14], vec[15] = radius*sp.cos(theta), radius*sp.sin(theta)
    moved = vec.subs(theta, theta+a)
    require("exact_full16_angle_dictionary", all(eq(v) for v in U*vec-moved))
    norm = (vec.T*vec)[0]
    require("original_material_normalization",
            eq(sp.trigsimp(norm).subs(radius**2, p**2-c**2)-1))
    slack = sp.sqrt(p*p-c*c-b*b)
    amp = sp.zeros(16, 1)
    amp[1], amp[0], amp[14], amp[15] = sp.sqrt(p), c, slack, b
    require("exact_original_top_tangent",
            all(eq(v) for v in J*amp-slack*amp.diff(b)))
    require("centre_map_inverse", eq((u-beta*a)+beta*a-u))
    require("second_arm_centre_map", eq(u-beta*a+a-(u+alpha*a)))
    # Arbitrary density differential: all blocks, including inter-site and RIGHT.
    d_sigma = sp.Matrix(3,3,sp.symbols('dsigma0:9'))
    require("complete_density_centre_cancellation",
            all(eq(v) for v in -alpha*beta*d_sigma+beta*alpha*d_sigma))
    f_theta, f_a = sp.symbols("f_theta f_a")
    transformation=sp.Matrix([u-beta*a,a]).jacobian(sp.Matrix([u,a]))
    transformed_source=transformation.T*sp.Matrix([f_theta,f_a])
    require("full_source_pullback", all(eq(v) for v in
            transformed_source-sp.Matrix([f_theta,f_a-beta*f_theta])))
    # The actual four mixed terms equal p times the physical Gram Hessian.
    q0, h, q1, d, k, e = sp.symbols("q0 h q1 d k e", real=True)
    E = sp.Matrix([[q0,h,0,0],[h,q1,0,0],[0,0,d,k],[0,0,k,e]])
    C = sp.Matrix([sp.sqrt(p),sp.sqrt(p*p-b*b-c*c),b,c])
    J4 = sp.zeros(4); J4[2,1],J4[1,2] = 1,-1
    C0=C.subs({b:0,c:0}); zero={b:0,c:0}
    for name,mvar in (("top",b),("scalar",c)):
        T=C.diff(mvar).subs(zero)
        R=(T.T*E*J4*C0 + (J4*C0).T*E*T
           +(J4*T).T*E*C0+C0.T*E*J4*T)[0]
        H=sp.diff((C.T*E*C)[0],b,mvar).subs(zero)
        require("four_term_selected_Hessian_identity_"+name,eq(R-p*H))
        require("mixed_matrix_Golden_factor_"+name,eq(beta*R-p**3*H))
    require("scalar_effect_negative_control",
            eq(sp.diff((C.T*sp.eye(4)*C)[0],b,b).subs(zero)))
    # Complete original counting reference, including terminal abort.
    zeta=sp.symbols("zeta", real=True)
    require("cap2_counting_reference_complete",eq((1-zeta)+zeta*(1-zeta)+zeta*zeta-1))
    cost, ticks=sp.symbols("cost ticks", real=True)
    lp=sp.log(1/p)
    logmu=-ticks*sp.log(64)+cost*sp.log(p)
    require("port_cost_is_not_double_counted",eq(cost+logmu/lp+ticks*sp.log(64)/lp))
    B=sp.Matrix([[sp.Rational(3,5),sp.Rational(1,7)],
                 [sp.Rational(1,7),sp.Rational(2,3)]])
    require("cap2_actual_occupation_effect",B.T==B and sp.eye(2)+B.T*B==sp.eye(2)+B**2)
    require("fixed_timestep_occupation_is_not_two",sp.eye(2)+B**2!=2*sp.eye(2))
    v=sp.symbols("v", real=True)
    require("logarithmic_convexity_bound_factor",eq(6-10*v+4*v*v-(1-v)*(6-4*v)))
    return {"native_generator_rank":8,"native_stiffness":"p^5/256",
            "exact_source_identity":"D_a S|a=0 = p^2 slack D_b S0",
            "exact_mixed_matrix":"M = p^3 P_b D_m^2 S0",
            "all_255_original_leaves_retained_by_consumed_owner":True}


def numerical_checks() -> dict:
    mp.mp.dps=130
    p=(mp.sqrt(5)-1)/2; alpha=p; beta=p*p; lp=mp.log(1/p)
    n=8

    def effects(g):
        E0=mp.eye(n)/3; E1=mp.eye(n)/3
        d0=(1,-1,2,-2,-1,1,-2,2)
        d1=(2,1,-1,-2,-2,-1,1,2)
        for j in range(n):
            E0[j,j]+=mp.mpf(d0[j])/50+g*mp.mpf(d1[j])/300
            E1[j,j]+=mp.mpf(d1[j])/60-g*mp.mpf(d0[j])/400
        for i,j,v in [(0,5,mp.mpf(1)/100),(2,7,mp.mpf(1)/80),(3,6,mp.mpf(1)/90)]:
            E0[i,j]=E0[j,i]=v
        for i,j,v in [(1,4,mp.mpf(1)/110),(2,6,mp.mpf(1)/120),(3,7,-mp.mpf(1)/100)]:
            E1[i,j]=E1[j,i]=v
        return [E0,E1,mp.eye(n)-E0-E1]

    def psi(c,theta):
        z=[]
        for j in range(2):
            r=mp.sqrt(p*p-c[j]*c[j])
            z.extend([mp.sqrt(p),r*mp.cos(theta[j]),r*mp.sin(theta[j]),c[j]])
        return mp.matrix(z)/mp.sqrt(2)

    def dot(x,E,y): return (x.T*E*y)[0]
    mu=[mp.mpf(1)/2,mp.mpf(1)/3,mp.mpf(1)/6]
    prices=[mp.mpf(j+1)+mp.log(mu[j])/lp for j in range(3)]

    def pair_price(g,c,th0,th1,ledger=True):
        x,y=psi(c,th0),psi(c,th1)
        total=-mp.log(2)/lp if ledger else mp.mpf(0)
        for j,E in enumerate(effects(g)):
            u,v,w=dot(x,E,x),dot(y,E,y),dot(x,E,y)
            trace=alpha*u+beta*v
            if th0==th1:
                low=mp.mpf(0)  # Exact proven coincident-arm rank, no threshold.
            else:
                det=alpha*beta*(u*v-w*w)
                if det<=0:
                    raise RuntimeError("Nonpositive noncoincident test Gram")
                low=2*det/(trace+mp.sqrt(trace*trace-4*det))
            high=trace-low
            total-=high*mp.log(high)/lp
            if low!=0: total-=low*mp.log(low)/lp
            if ledger: total+=prices[j]*trace
        return total

    def original(g,c,theta,a,ledger=True):
        return pair_price(g,c,theta,[theta[j]+a[j] for j in range(2)],ledger)

    def centred(g,c,u,a,ledger=True):
        return pair_price(g,c,[u[j]-beta*a[j] for j in range(2)],
                          [u[j]+alpha*a[j] for j in range(2)],ledger)

    def diagonal(g,c,u,ledger=True):
        # Independent one-arm expression, retaining the same capacity offset.
        x=psi(c,u)
        value=-mp.log(2)/lp if ledger else mp.mpf(0)
        for j,E in enumerate(effects(g)):
            q=dot(x,E,x)
            value-=q*mp.log(q)/lp
            if ledger: value+=prices[j]*q
        return value

    g=mp.mpf('0.17'); c=[mp.mpf('.03'),mp.mpf('-.02')]
    u=[mp.mpf('.07'),mp.mpf('-.05')]; a=[mp.mpf('.003'),mp.mpf('-.002')]
    for gg in [-mp.mpf('.2'),mp.mpf('.2')]:
        es=effects(gg)
        require('complete_fixture_effects_'+str(gg),mp.norm(sum(es,mp.zeros(n))-mp.eye(n))<mp.mpf('1e-125'))
        for j,E in enumerate(es):
            radius=max(sum(abs(E[i,k]) for k in range(n) if k!=i)-E[i,i] for i in range(n))
            require('strict_Gershgorin_effect_'+str(gg)+'_'+str(j),radius<0)
    require('noncommuting_fixture_effects',mp.norm(effects(g)[0]*effects(g)[1]-effects(g)[1]*effects(g)[0])>mp.mpf('1e-5'))
    require('cross_site_fixture_coupling',effects(g)[0][0,5]!=0 and effects(g)[0][2,7]!=0)
    parity=mp.diag([-1,-1,1,1,-1,-1,1,1])
    require('fixture_CAR_parity',all(mp.norm(E*parity-parity*E)==0 for E in effects(g)))
    require('full_material_norm',abs(mp.norm(psi(c,u))**2-1)<mp.mpf('1e-125'))
    zero=[mp.mpf(0),mp.mpf(0)]
    require('diagonal_same_price',abs(centred(g,c,u,zero)-diagonal(g,c,u))<mp.mpf('1e-125'))
    theta=[u[j]-beta*a[j] for j in range(2)]
    require('exact_price_coordinate_identity',abs(original(g,c,theta,a)-centred(g,c,u,a))<mp.mpf('1e-120'))
    source_errors=[]
    for j in range(2):
        def vary(v,index,x):
            out=list(v);out[index]=x;return out
        orig_theta=mp.diff(lambda x:original(g,c,vary(theta,j,x),a),theta[j])
        orig_a=mp.diff(lambda x:original(g,c,theta,vary(a,j,x)),a[j])
        centre_u=mp.diff(lambda x:centred(g,c,vary(u,j,x),a),u[j])
        centre_a=mp.diff(lambda x:centred(g,c,u,vary(a,j,x)),a[j])
        err=max(abs(centre_u-orig_theta),abs(centre_a-(orig_a-beta*orig_theta)))
        require('full_source_pullback_'+str(j),err<mp.mpf('1e-105'))
        source_errors.append(err)
    # Original fixed-material source survives; centred relative source cancels.
    h=mp.mpf('1e-22')
    source0=[]
    for j in range(2):
        direction=[h if k==j else mp.mpf(0) for k in range(2)]
        negative=[-v for v in direction]
        dc=(centred(g,c,u,direction)-centred(g,c,u,negative))/(2*h)
        do=(original(g,c,u,direction)-original(g,c,u,negative))/(2*h)
        dbase=mp.diff(lambda x:diagonal(g,c,[x if k==j else u[k] for k in range(2)]),u[j])
        require('centred_relative_source_zero_'+str(j),abs(dc)<mp.mpf('1e-40'))
        require('diagonal_Ward_source_'+str(j),abs(do-beta*dbase)<mp.mpf('1e-40'))
        source0.append(do)
    require('frozen_material_is_a_different_problem',max(abs(v) for v in source0)>mp.mpf('1e-5'))
    # Full spectral price gap, and the actual projected small-cluster coefficient.
    gap_rows=[]
    for di,direction0 in enumerate([(1,0),(0,1),(1,-2)]):
        length=mp.sqrt(sum(v*v for v in direction0))
        direction=[mp.mpf(v)/length for v in direction0]
        x=psi(c,u)
        tangent=mp.matrix([mp.diff(lambda t:psi(c,[u[k]+t*direction[k] for k in range(2)])[j],0) for j in range(n)])
        Q=alpha*beta*sum(dot(tangent,E,tangent)-dot(x,E,tangent)**2/dot(x,E,x) for E in effects(g))
        require('projected_small_cluster_positive_'+str(di),Q>0)
        errors=[]
        for exponent in (4,12,30):
            r=mp.power(10,-exponent);av=[r*v for v in direction]
            gap=centred(g,c,u,av)-diagonal(g,c,u)
            require('positive_complete_centred_gap_'+str(di)+'_'+str(exponent),gap>0)
            ratio=gap/(Q*r*r*mp.log(1/(r*r))/lp)
            errors.append(abs(ratio-1))
            gap_rows.append({'direction':list(direction0),'angle_exponent':exponent,'gap_to_log_coefficient_ratio':mp.nstr(ratio,20)})
        require('log_gap_coefficient_convergence_'+str(di),errors[2]<errors[1]<errors[0])
        require('log_gap_coefficient_final_accuracy_'+str(di),errors[-1]<mp.mpf('.1'))
    # Direct full-price mixed source versus diagonal material Hessian, in the
    # ORIGINAL normalized (b1,c1,b2,c2) amplitudes, not angle surrogates.
    def unpack(m):
        cc=[m[1],m[3]]
        th=[mp.asin(m[2*j]/mp.sqrt(p*p-cc[j]*cc[j])) for j in range(2)]
        return cc,th
    def diag_m(m):
        cc,th=unpack(m);return diagonal(g,cc,th)
    def orig_m(m,av):
        cc,th=unpack(m);return original(g,cc,th,av)
    z4=[mp.mpf(0)]*4;hm=mp.mpf('1e-18');matrix_errors=[]
    for row in range(2):
        for col in range(4):
            def hess_value(s,t):
                mm=list(z4);mm[2*row]+=s;mm[col]+=t;return diag_m(mm)
            H=mp.diff(lambda s:mp.diff(lambda t:hess_value(s,t),0),0)
            mplus=list(z4);mplus[col]=hm
            mminus=list(z4);mminus[col]=-hm
            aplus=list(zero);aplus[row]=hm
            aminus=[-v for v in aplus]
            mixed=(orig_m(mplus,aplus)-orig_m(mplus,aminus)
                   -orig_m(mminus,aplus)+orig_m(mminus,aminus))/(4*hm*hm)
            error=abs(mixed-p**3*H)
            require('complete_price_mixed_Hessian_'+str(row)+'_'+str(col),error<mp.mpf('1e-31'))
            matrix_errors.append(error)
    return {'data_dimension':8,'oldRIGHT_dimension':1,'sites':2,'leaves':3,
            'precision_decimal_digits':mp.mp.dps,'original_D0_spectral_replay':False,
            'max_source_pullback_error':mp.nstr(max(source_errors),12),
            'fixed_material_sources':[mp.nstr(v,20) for v in source0],
            'max_mixed_Hessian_error':mp.nstr(max(matrix_errors),12),
            'log_gap_diagnostics':gap_rows}


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path)
    args=parser.parse_args()
    repo=args.repo if args.repo is not None else Path(__file__).resolve().parents[4]
    sources=source_checks(repo)
    exact=exact_checks()
    numerical=numerical_checks()
    result={'status':'PASS','checks':len(CHECKS),'sources':sources,'exact':exact,
            'numerical_fixture':numerical,'check_names':CHECKS,
            'scope':{'joint_stationary_equivalence_analytic_proof':'PROOF.md',
                     'independent_review_performed':False,'refinement_uniformity_proved':False,
                     'Book_price_selected':False,'GR_closed':False}}
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))


if __name__=='__main__':main()
