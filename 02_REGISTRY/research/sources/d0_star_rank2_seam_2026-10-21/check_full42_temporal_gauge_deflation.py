#!/usr/bin/env python3
"""D0 original 42(n-1)-component N1 source: exact residual temporal Lorentz
gauge deflation and numerical 3/4-interval rank-two nonflat roots.

Uses the existing full G2/STAR and full two-real-CAR Golden N1 price.
The six(n-2) omitted time-link rows are NOT assumed zero: the whole
original 42(n-1) Euler covector is independently checked AFTER solving.
Only the configured fixed-price field chart; Book03 selection remains open.
"""
from __future__ import annotations
import argparse,hashlib,json,time
from pathlib import Path
import numpy as np
from scipy.linalg import expm,svdvals
from scipy.optimize import least_squares
from scipy.optimize._numdiff import approx_derivative
from check_full42_n1_single_internal import problem,direct_CQ_value
from check_star_rank2_seam import I,ETA,LORENTZ as L,star_density,matter_query

ROOT=Path(__file__).resolve().parents[4]
PINS={
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_full42_n1_single_internal.py":
"da83e40379867f71b598fecd8430444ea027a4da",
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/full_n1_euler_analytic.py":
"7ea28c981826c96b01bbdda67a92010dc7221095",
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py":
"a57f0e3e845290923c2ac88d39ba5c08af4f6fd6"
}
def gitblob(d):
    return hashlib.sha1(b"blob "+str(len(d)).encode()+b"\0"+d).hexdigest()
def checkpins():
    for path,sha in PINS.items():
        b=(ROOT/path).read_bytes()
        actual=gitblob(b)
        if actual!=sha:raise AssertionError(("changed scientific source",path,actual,sha))

def indices(n):
    assert n>=2
    N=42*(n-1)
    # Fix the ORIGINAL internal temporal outgoing links U0(t_j), j=1..n-2.
    gauge=tuple(42*(j-1)+16+k for j in range(1,n-1) for k in range(6))
    remove=set(gauge)
    active=np.array([k for k in range(N) if k not in remove],dtype=int)
    assert len(gauge)==6*(n-2) and len(active)==36*n-30
    return active,np.array(gauge,dtype=int)

def copied(nodes):
    return [dict(e=c["e"].copy(),U=c["U"].copy(),v=c["v"].copy())
            for c in nodes]

def point_gauge_transform(nodes,j,Z):
    """Exact finite based-fiber change at time site j, with fixed ends.
    g_j=exp(Z); all other g=I. Valid only 2<=j<=n-1, so the original
    first boundary temporal link U0(0) is unmodified.
    """
    n=len(nodes)-1
    assert 2<=j<=n-1
    g=expm(Z);gi=np.linalg.inv(g)
    assert np.linalg.norm(g.T@ETA@g-ETA)<2e-12
    dst=copied(nodes)
    dst[j]["e"]=g@nodes[j]["e"]
    for i in (1,2,3):
        dst[j]["U"][i]=g@nodes[j]["U"][i]@gi
    dst[j-1]["U"][0]=nodes[j-1]["U"][0]@gi
    dst[j]["U"][0]=g@nodes[j]["U"][0]
    return dst

def original_density_invariance(h,nodes,nodes_g,weights):
    old=[];new=[]
    for k in range(len(nodes)-1):
        f=star_density(dict(e=nodes[k]["e"],u=nodes[k]["U"],v=nodes[k]["v"]),
                       dict(e=nodes[k+1]["e"],u=nodes[k+1]["U"],v=nodes[k+1]["v"]),h)
        q=matter_query(dict(e=nodes[k]["e"],u=nodes[k]["U"],v=nodes[k]["v"]))
        fg=star_density(dict(e=nodes_g[k]["e"],u=nodes_g[k]["U"],v=nodes_g[k]["v"]),
                        dict(e=nodes_g[k+1]["e"],u=nodes_g[k+1]["U"],v=nodes_g[k+1]["v"]),h)
        qg=matter_query(dict(e=nodes_g[k]["e"],u=nodes_g[k]["U"],v=nodes_g[k]["v"]))
        old.append([f,q]);new.append([fg,qg])
    err=float(np.max(abs(np.array(new)-np.array(old))))
    price=float(abs(direct_CQ_value(nodes_g,h,weights)-
                    direct_CQ_value(nodes,h,weights)))
    if err>5e-11 or price>5e-11:
        raise AssertionError(("same-price finite gauge covariance",err,price))
    return {"max_original_plaquette_and_CAR_scalar_difference":err,
            "direct_full_CQ_price_difference":price}

def source_problem(n,weights):
    h,base,psi,rhos,fields,euler=problem(n,weights)
    active,dropped=indices(n)
    def expand(y):
        z=np.zeros(42*(n-1))
        z[active]=y
        return z
    def residual(y,detail=False):
        result=euler(expand(y),detail)
        if detail:return result
        return result[active]
    return h,rhos,fields,expand,residual,active,dropped

def independent_price_gradient(nodes,h,weights):
    """Independent full nonlinear N1 ENTROPY VALUE, not the source routine.
    Left-generator link jets and original two-scalar chronological increments
    are actual allowed original 42-field tangents at each free time site.
    """
    step=1e-20
    n=len(nodes)-1
    grad=[]
    for j in range(1,n):
        for k in range(42):
            trial=[dict(e=c["e"].astype(complex).copy(),
                        U=c["U"].astype(complex).copy(),
                        v=c["v"].astype(complex).copy()) for c in nodes]
            if k<16:
                trial[j]["e"][k//4,k%4]+=1j*step
            elif k<40:
                axis,gen=divmod(k-16,6)
                trial[j]["U"][axis]=expm(1j*h*step*L[gen])@trial[j]["U"][axis]
            else:
                a=k-40
                trial[j-1]["v"][a,0]+=1j*step/h
                trial[j]["v"][a,0]-=1j*step/h
            grad.append(np.imag(direct_CQ_value(trial,h,weights))/step)
    return np.asarray(grad,float)

def run(n,weights,max_nfev=120):
    t0=time.monotonic()
    h,rhos,fields,expand,residual,active,dropped=source_problem(n,weights)
    y0=np.zeros(len(active))
    # Real first-value solver, no gauge-penalty/counterterm or scalar source fit.
    fit=least_squares(residual,y0,method="trf",x_scale="jac",
                      max_nfev=max_nfev,xtol=1e-12,gtol=1e-12,ftol=1e-12)
    full,src,nodes=residual(fit.x,True)
    err=float(np.max(abs(full)))
    err_omitted=float(max(abs(full[dropped]))) if len(dropped) else 0.
    if err>5e-10 or err_omitted>5e-10:
        raise AssertionError(("full original Euler regression",n,err,err_omitted))
    jets=independent_price_gradient(nodes,h,rhos)
    err_price=float(np.max(abs(jets-full)))
    if err_price>2e-9 or np.max(abs(jets))>2e-9:
        raise AssertionError(("independent full CQ first source",n,err_price))
    H=approx_derivative(residual,fit.x,method="3-point",abs_step=5e-6)
    spec=svdvals(H)
    if float(spec[-1])<1e-4:raise AssertionError(("unresolved gauge kernel",n,spec[-1]))
    gauge=point_gauge_transform(nodes,2,.13*L[0]-.09*L[4])
    cov=original_density_invariance(h,nodes,gauge,rhos)
    full_original_source_count=42*(n-1)
    # Check the actual 4x4 proper-Lorentz fields and two independent CAR stresses.
    geometry=[]
    for j,c in enumerate(nodes[:-1]):
        metric=c["e"].T@ETA@c["e"]
        ev=np.linalg.eigvalsh(metric)
        if np.count_nonzero(ev>0)!=1 or np.count_nonzero(ev<0)!=3:
            raise AssertionError(("wrong metric signature",j,ev))
        stress=sum(np.outer(v,v) for v in c["v"])
        if np.linalg.matrix_rank(stress)!=2:
            raise AssertionError(("one CAR stream lost",j))
        spatial=c["U"][1]@c["U"][2]@np.linalg.inv(c["U"][1])@np.linalg.inv(c["U"][2])
        geometry.append({"node":j,
          "spatial_based_holonomy_nonidentity_norm":float(np.linalg.norm(spatial-I)),
          "two_real_CAR_source_rank":2})
    # Only distinguish the commutator from floating-point identity here; the
    # nonflat amplitude is reported separately and scales with the finite h.
    if max(x["spatial_based_holonomy_nonidentity_norm"] for x in geometry)<1e-8:
        raise AssertionError("lost nonflat original based holonomy")
    return {
      "status":"PASS_ORIGINAL_CONFIGURED_N1_GAUGE_FIXED_MULTISLAB_NUMERICAL",
      "n_intervals":n,"h":h,"PF_time_weights":list(rhos),
      "all_42_times_free_nodes":full_original_source_count,
      "residual_gauge_dimension_exact":6*(n-2),
      "gauge_fixed_original_source_dimension":len(active),
      "max_all_original_Euler":err,
      "max_omitted_temporal_link_Euler":err_omitted,
      "max_independent_full_N1_price_derivative":float(max(abs(jets))),
      "analytic_vs_independent_price_source_error":err_price,
      "min_numerical_singular_after_gauge":float(spec[-1]),
      "max_numerical_singular_after_gauge":float(spec[0]),
      "finite_exact_gauge_action_test":cov,
      "nonflat_rank_two_material_checks":geometry,
      "max_field_coordinate_change":float(max(abs(fit.x))),
      "nfev":int(fit.nfev),"wall_seconds":time.monotonic()-t0,
      "scope":{
       "same_complete_N1_CQ_ledger":True,
       "actual_full_Book03_physical_selection":False,
       "actual_AFPF_descendant_weights":False,
       "arbitrary_4D_inhomogeneous_geometry":False,
       "validated_interval_root_existence":False,
       "uniform_h_to_zero_refinement":False,
       "GR_closed":False}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--intervals",type=int,choices=(3,4,5),default=3)
    ap.add_argument("--pf",default="")
    ap.add_argument("--max-nfev",type=int,default=120)
    ap.add_argument("--json",type=Path)
    args=ap.parse_args()
    checkpins()
    weights=([1.]*args.intervals if not args.pf else
             [float(x) for x in args.pf.split(",")])
    if len(weights)!=args.intervals or min(weights)<=0:
        raise ValueError("positive PF time weights per complete interval required")
    result=run(args.intervals,weights,args.max_nfev)
    out=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
    print(out,end="")
    if args.json:args.json.write_text(out,encoding="utf-8")
if __name__=="__main__":main()
