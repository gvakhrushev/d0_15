#!/usr/bin/env python3
"""Exact finite TWO real CAR scalar-source elimination and flux Routh map.

Consumes ORIGINAL GoldenMaster N=1 (caps9/20, sigma-minus included, real
original F) and actual 3/4/5-interval FULL42 configured CQ root receipts.
No replacement matter action, no postselected output, no new detector.

The exact mathematical result holds for spatially homogeneous original
coframe/independent links (not necessarily diagonal/pureboost), two REAL
scalar gradients psi_A(j,x)=theta_A(j)+s_Ai*x_i, and arbitrary POSITIVE
PF weights rho_j which are constant on each spatial slice (may JUMP in time).
It eliminates scalar stationarity EXACTLY for sufficiently small faithful
N1 fields, even when f_star and q are nonzero. It does not select Book03
or solve geometric Euler, actual nonhomogeneous spatial AF/PF, or GR.
"""
from __future__ import annotations
from pathlib import Path
from itertools import product
import hashlib,sys,json
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq,root

ROOT=Path(__file__).resolve().parents[4]
ORIGINAL={
"02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py":
"525b257ec671500bd02c4791f9579dbde2439f21",
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/RESULT_TEMPORAL_GAUGE_MULTISLAB_2026_10_22.json":
"6f7afdada3f590c8f5a136388c322201059f291e",
}
def checkpins():
    for path,sha in ORIGINAL.items():
        blob=(ROOT/path).read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(blob)).encode()+b"\0"+blob).hexdigest()
        assert actual==sha,(path,actual,sha)
sys.path.insert(0,str(ROOT/"02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21"))
from native_master import GoldenMaster

NATIVE=GoldenMaster(65)
TAU=.05
NATIVE_B=float(NATIVE.b)

def symbolic():
    g,J1,J2,w,wy,tau,rho=sp.symbols("g J1 J2 w wy tau rho",positive=True)
    S1,S2,Qperp=sp.symbols("S1 S2 Qperp")
    v1=(J1/w-S1)/g;v2=(J2/w-S2)/g
    q=sp.expand(g*(v1*v1+v2*v2)+2*S1*v1+2*S2*v2+
                Qperp+(S1*S1+S2*S2)/g)
    assert sp.simplify(q-(J1*J1+J2*J2)/(g*w*w)-Qperp)==0
    Gy=1+2*tau*(J1*J1+J2*J2)*wy/(rho*g*w**3)
    mat=(sp.eye(2)-2*tau*wy/(rho*g*w**3*Gy)*
                  sp.Matrix([J1,J2])*sp.Matrix([[J1,J2]]))/(g*w)
    assert sp.simplify(mat*sp.Matrix([J1,J2])
              -sp.Matrix([J1,J2])/(g*w*Gy))==sp.zeros(2,1)
    assert sp.simplify(mat*sp.Matrix([J2,-J1])
              -sp.Matrix([J2,-J1])/(g*w))==sp.zeros(2,1)
    # On a FREE independent coframe site, the true native radial equation
    # xF_x-yF_y=0 gives the same exact analytic off-null curvature law;
    # the mixed F_xy cancels in the second-order implicit coefficient.
    x,y,a,b,c,d,e=sp.symbols("x y a b c d e",nonzero=True)
    F=a*x+b*y+c*x*x/2+d*x*y+e*y*y/2
    c1=b/a;c2=(e-c*c1*c1)/a
    trace=sp.expand((x*sp.diff(F,x)-y*sp.diff(F,y))
                    .subs(x,c1*y+c2*y*y))
    assert sp.simplify(trace.coeff(y,1))==0
    assert sp.simplify(trace.coeff(y,2))==0
    return {
     "exact_full_Lorentz_schur":
       "q=|J|²/(g^{00} F_y(x,y)²)+sum_A (g^{ij}-g^{0i}g^{0j}/g^{00}) s_Ai s_Aj",
     "local_nonzero_q_equation":
       "y=tau/rho[|J|²/(g^{00}F_y(x,y)²)+Qperp]",
     "implicit_Gy":
       "1+2*tau*|J|²*F_yy/(rho*g^{00} F_y³)",
     "two_flux_jacobian_eigenvalues":
       ["1/(g^{00}F_y) (perp J)",
        "1/(g^{00}F_y G_y) (parallel J)"],
     "finite_time_Euler":
       "D^-_0 J_A=0 for A=1,2; ALL original spatial terms vanish by homogeneous data",
     "trace_first_jet":"chi'(0)=F_y(0)/F_x(0)",
     "trace_second_jet":
       "chi[y²]=[F_yy(0)-F_xx(0)*(F_y/F_x)^2]/F_x(0)",
     "mixed_Fxy_cancels_in_second_trace_coefficient":True,
     "Dirichlet_matter_hessian":"strict SPD if g^{00},F_y,G_y>0 (time difference Laplacian)"
    }

def source_trace_receipts():
    assert NATIVE.a<0<NATIVE.b and NATIVE.hyy>0
    c2=(NATIVE.hyy-NATIVE.hxx*NATIVE.ratio**2)/NATIVE.a
    file=ROOT/"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/RESULT_TEMPORAL_GAUGE_MULTISLAB_2026_10_22.json"
    report=json.loads(file.read_text())
    checked=[]
    for trial in report["numerical_runs"]:
        if "source_f" not in trial or "source_q" not in trial:
            continue  # the nonuniform-PF n3 receipt omits per-cell f,q
        f=trial["source_f"];q=trial["source_q"]
        rho=trial["pf"]
        assert len(f)==len(q)==len(rho)==trial["n"]
        for j in range(1,len(f)): # actual FREE coframe anchors only
            x=-mp.mpf(str(TAU))*mp.mpf(str(f[j]))/mp.mpf(str(rho[j]))
            y=mp.mpf(str(TAU))*mp.mpf(str(q[j]))/mp.mpf(str(rho[j]))
            err=(x*NATIVE.fx(x,y)-y*NATIVE.fy(x,y))/NATIVE.a
            chi=mp.findroot(
             lambda X:X*NATIVE.fx(X,y)-y*NATIVE.fy(X,y),NATIVE.ratio*y)
            f_exact=-mp.mpf(str(rho[j]))*chi/mp.mpf(str(TAU))
            f_quad=float(NATIVE.kappa)*q[j]-float(c2)*TAU*q[j]**2/rho[j]
            assert abs(float(err))<1e-10,(trial["n"],j,err)
            assert abs(float(f_exact)-f[j])<2e-9
            assert abs(f_quad-f[j])<3e-9
            checked.append({
             "n":trial["n"],"interior_anchor":j,
             "rho":rho[j],"f":f[j],"q":q[j],
             "f_div_q":f[j]/q[j],
             "full_native_radial_div_a":float(err),
             "native_implicit_star_error":float(f_exact)-f[j],
             "quadratic_constitutive_error":f_quad-f[j]})
    assert len(checked)==9,len(checked)
    return {
      "original_native_a":mp.nstr(NATIVE.a,25),
      "original_native_b":mp.nstr(NATIVE.b,25),
      "kappa_original":mp.nstr(NATIVE.kappa,25),
      "native_Fyy_strict_positive_at_flat":NATIVE.hyy>0,
      "nonlinear_trace_second_coefficient":mp.nstr(c2,25),
      "actual_full42_n3_n4_n5_interior_receipt_count":len(checked),
      "max_normalized_radial_error":max(abs(x["full_native_radial_div_a"]) for x in checked),
      "data":checked}

# Native off-null diagnostic: arbitrary original time-varying positive PF,
# original signed Lorentz metric inverse with NONZERO g^{0x}.
# The x values here are legitimate small scalar geometric OPERANDS, not
# claimed to be the f of a separately executed lattice root.
PF=np.array([1.,2.,1.,3.,1.])
G00=np.array([1.12,1.17,1.25,1.34,1.40])
G0X=np.array([.10,-.06,.02,.08,-.03])
GXX=np.array([-1.17,-1.25,-1.14,-1.05,-1.11])
S=np.array([0.,.018]) # two REAL original scalar spatial x-gradients
GX=np.array([.00013,-.00011,.00008,-.00005,.00017])
H=.06

def local_solve(j,hatJ):
    metric00=G00[j]
    Qperp=(GXX[j]-G0X[j]**2/metric00)*(S@S)
    xm=mp.mpf(str(GX[j]))
    def wjet(y):
        v=mp.mpf(str(y))
        w=float(NATIVE.fy(xm,v)/NATIVE.b)
        wy=float(mp.diff(lambda vv:NATIVE.fy(xm,vv),v)/NATIVE.b)
        return w,wy
    def residual(y):
        w,_=wjet(y)
        return y-TAU/PF[j]*((hatJ@hatJ)/(metric00*w*w)+Qperp)
    y=brentq(residual,-2e-4,2e-4,xtol=5e-18)
    w,wy=wjet(y)
    Gy=1+2*TAU/PF[j]*(hatJ@hatJ)*wy/(metric00*w**3)
    assert w>0 and Gy>0
    v=(hatJ/w-G0X[j]*S)/metric00
    dvdJ=(np.eye(2)-2*TAU/PF[j]*wy/(metric00*w**3*Gy)*
                       np.outer(hatJ,hatJ))/(metric00*w)
    assert abs(residual(y))<2e-14
    return y,w,v,Gy,dvdJ

def boundary(hatJ):
    data=[local_solve(j,hatJ) for j in range(len(PF))]
    return H*sum(s[2] for s in data),data

def price_from_actual_scalar_history(psi):
    val=mp.mpf(0)
    for j in range(len(PF)):
        v=(psi[j+1]-psi[j])/H
        q=G00[j]*(v@v)+2*G0X[j]*(v@S)+GXX[j]*(S@S)
        val+=mp.mpf(str(PF[j]))*NATIVE.F(
         mp.mpf(str(GX[j])),mp.mpf(str(TAU*q/PF[j])))
    return val

def native_experiment():
    Jhat=np.array([.047,-.013])
    dtheta,cells=boundary(Jhat)
    hessian=H*sum(x[4] for x in cells)
    vals=np.linalg.eigvalsh(hessian)
    assert vals[0]>.2
    fd_error=0.
    for k in range(2):
        delta=1e-5
        pp=Jhat.copy();mm=Jhat.copy();pp[k]+=delta;mm[k]-=delta
        numerical=(boundary(pp)[0]-boundary(mm)[0])/(2*delta)
        fd_error=max(fd_error,float(np.max(abs(numerical-hessian[:,k]))))
    assert fd_error<5e-10
    sol=root(lambda x:boundary(x)[0]-dtheta,np.array([.02,-.008]),
              tol=1e-12)
    assert sol.success and max(abs(sol.x-Jhat))<1e-11
    psi=np.zeros((len(PF)+1,2))
    for j,v in enumerate(cells):psi[j+1]=psi[j]+H*v[2]
    assert max(abs(psi[-1]-dtheta))<1e-14
    currents=[]
    for j in range(len(PF)):
        v=(psi[j+1]-psi[j])/H
        q=G00[j]*(v@v)+2*G0X[j]*(v@S)+GXX[j]*(S@S)
        w=float(NATIVE.fy(mp.mpf(str(GX[j])),
                   mp.mpf(str(TAU*q/PF[j])))/NATIVE.b)
        currents.append(w*(G00[j]*v+G0X[j]*S))
    Epsi=max(float(np.max(abs(x-Jhat))) for x in currents)
    assert Epsi<2e-12
    # Independent differentiation of actual TOTAL native N1 price at the
    # exact scalar solution and at separately perturbed OFFSHELL scalars.
    on_shell=0.
    for j,k in product(range(1,len(PF)),range(2)):
        step=3e-5
        temp=psi.copy();temp[j,k]+=step
        pp=price_from_actual_scalar_history(temp)
        temp[j,k]-=2*step
        mm=price_from_actual_scalar_history(temp)
        on_shell=max(on_shell,abs(float((pp-mm)/(2*step))))
    assert on_shell<4e-12
    off=psi.copy();off[2,0]+=.00025;off[3,1]-=.00018
    offJ=[]
    for j in range(len(PF)):
        v=(off[j+1]-off[j])/H
        q=G00[j]*(v@v)+2*G0X[j]*(v@S)+GXX[j]*(S@S)
        w=float(NATIVE.fy(mp.mpf(str(GX[j])),
                   mp.mpf(str(TAU*q/PF[j])))/NATIVE.b)
        offJ.append(w*(G00[j]*v+G0X[j]*S))
    error_off=0.
    for j,k in product(range(1,len(PF)),range(2)):
        analytic=2*TAU*NATIVE_B*(offJ[j-1][k]-offJ[j][k])/H
        dx=1e-6
        trial=off.copy();trial[j,k]+=dx
        pp=price_from_actual_scalar_history(trial)
        trial[j,k]-=2*dx
        mm=price_from_actual_scalar_history(trial)
        direct=float((pp-mm)/(2*dx))
        error_off=max(error_off,abs(analytic-direct))
    assert error_off<5e-13
    # DIRICHLET matter block: exactly a weighted TWO-component graph
    # Laplacian. Site weights are positive even for the irregular PF.
    n=len(PF)
    native_h=H
    Hess=np.zeros((2*(n-1),2*(n-1)))
    for j in range(n):
        A=np.linalg.inv(cells[j][4]) # dJhat/d(time gradients), positive
        for node,sgn in ((j,-1),(j+1,1)):
            if 1<=node<n:
                inds=slice(2*(node-1),2*node)
                Hess[inds,inds]+=A
        if 1<=j<n and 1<=j+1<n:
            aa=slice(2*(j-1),2*j)
            bb=slice(2*j,2*(j+1))
            Hess[aa,bb]-=A;Hess[bb,aa]-=A
    Hess*=2*TAU*NATIVE_B/H**2
    mateigs=np.linalg.eigvalsh(Hess)
    assert mateigs[0]>0
    # The native matter-only Hessian is (2*tau*b/h^2) times a true
    # two-component positive Dirichlet time-edge Laplacian. Its EXACT
    # discrete spectral gap is >= 4*sin(pi/(2n))^2 times min local block.
    native_gmin=min(float(v[1]*G00[j]) for j,v in enumerate(cells))
    actual_sine_bound=8*TAU*NATIVE_B/native_h**2 * native_gmin * (
        np.sin(np.pi/(2*n))**2)
    coarse_uniform_bound=8*TAU*NATIVE_B*native_gmin/(n*n*native_h*native_h)
    assert mateigs[0]+1e-14>=actual_sine_bound
    assert actual_sine_bound+1e-14>=coarse_uniform_bound
    return {"true_original_F":"N1 cap Kpre9 Lgate20; sigma-minus included",
      "time_jagged_PF":PF.tolist(),
      "metric_time_inverses":G00.tolist(),
      "g_time_spatial_shift":G0X.tolist(),
      "original_curvature_operands_x":GX.tolist(),
      "matter_spatial_gradients":S.tolist(),
      "two_flux_normalized_J_div_b":Jhat.tolist(),
      "flux_recovered_from_two_end_dirichlet":sol.x.tolist(),
      "cell_y_values":[v[0] for v in cells],
      "cell_Fy_over_b":[v[1] for v in cells],
      "cell_Gy":[v[3] for v in cells],
      "min_local_flux_jacobian_eigen":min(float(np.linalg.eigvalsh(v[4])[0])
                                          for v in cells),
      "global_end_boundary_2x2_eigen":vals.tolist(),
      "end_boundary_jacobian_independent_FD_error":fd_error,
      "both_true_original_material_current_error":Epsi,
      "independent_FULL_N1_price_on_shell_scalar_source_max":on_shell,
      "independent_FULL_N1_price_OFFSHELL_source_error":error_off,
      "Dirichlet_exact_matter_Hessian_min_eigen":float(mateigs[0]),
      "native_Dirichlet_analytic_sine_lower_bound":float(actual_sine_bound),
      "native_Dirichlet_uniform_coarse_lower_bound":float(coarse_uniform_bound),
      "native_Fy_over_b_g00_min":native_gmin}

def main():
    checkpins()
    result={"status":"PASS_EXACT_TWO_CAR_FINITE_FLUX_ROUTH_SCHUR",
      "reused_owner_blobs":ORIGINAL,
      "exact":symbolic(),"full42_receipts":source_trace_receipts(),
      "original_N1_numeric":native_experiment(),
      "scope":{
        "all_N_free_time_slab_cells_supported_in_analytic_chart":True,
        "two_scalar_stationarity_eliminated_exactly":True,
        "full_metric_may_have_g0i_nonzero":True,
        "PF_may_jump_in_TIME":True,
        "PF_may_jump_in_SPACE":False,
        "original_connected_4D_gravity_source_newly_solved":False,
        "real_AF_descendant_weight_sequence_instantiated":False,
        "original_primitive_field_writer_or_Book03_selected":False,
        "exact_full_geometry_root_from_numeric_receipts":False,
        "GR_closed":False}}
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
