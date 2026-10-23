#!/usr/bin/env python3
"""Complete original six-face Palatini plus two-scalar finite Ward pullback.

No discrete diffeomorphism symmetry is assumed. The exact finite failure is
computed, with every independent 16 coframe/24 proper-link/2 scalar source.
The smooth-grid tests are NOT roots or physical Book/field-writer admission.
"""
from __future__ import annotations
import argparse
from itertools import combinations
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
import check_discrete_material_ward as matter

PAIR=list(combinations(range(4),2)); PI={v:i for i,v in enumerate(PAIR)}
ETA=matter.ETA
G2=np.diag([ETA[a,a]*ETA[b,b] for a,b in PAIR])
STAR=np.zeros((6,6))
for x,(y,sign) in {(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
                   (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}.items():
    STAR[PI[y],PI[x]]=sign
H=G2@STAR
GEN=[]
for i in (1,2,3):
    X=np.zeros((4,4));X[0,i]=X[i,0]=1;GEN.append(X)
for i,j in ((1,2),(1,3),(2,3)):
    X=np.zeros((4,4));X[i,j]=1;X[j,i]=-1;GEN.append(X)
GEN=np.array(GEN)
checks=[]


def need(cond,label):
    if not bool(cond):raise ArithmeticError(label)
    checks.append(label)


def tr(A):return np.swapaxes(A,-1,-2)


def shift(A,axis,steps=1):return np.roll(A,-steps,axis=axis)


def inv_lorentz(A):return ETA@tr(A)@ETA


def orient(r,s):
    seq=[r,s]+[j for j in range(4) if j not in (r,s)]
    return (-1)**sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))


def wedge(u,v):
    return np.stack([u[...,a]*v[...,b]-u[...,b]*v[...,a] for a,b in PAIR],axis=-1)


def biv(C):return np.stack([C[...,a,b]*ETA[b,b] for a,b in PAIR],axis=-1)


def star_density_and_source(e,U,h,grad=True):
    """Literal original P=Lr(x)Ls(x+r)Lr(x+s)^-1 Ls(x)^-1,
    R=(P-P^-1)/2, and h^-4 star(h e,U). Source is per site; h^4
    quadrature belongs to the caller and cancels in the Ward identities.
    """
    f=np.zeros(e.shape[:-2]);ee=np.zeros_like(e);gU=np.zeros_like(U)
    for r,s in PAIR:
        u,v=[j for j in range(4) if j not in (r,s)]
        Ar=U[...,r,:,:];Bs=shift(U[...,s,:,:],r)
        Cr=shift(U[...,r,:,:],s);Ds=U[...,s,:,:]
        Ci=inv_lorentz(Cr);Di=inv_lorentz(Ds)
        P=Ar@Bs@Ci@Di;Piv=inv_lorentz(P);C=(P-Piv)/2
        B=wedge(e[..., :,u],e[..., :,v]); cb=biv(C)
        fac=orient(r,s)/(h*h)
        f+=fac*np.einsum('...i,ij,...j->...',B,H,cb)
        if not grad:continue
        # Unconstrained matrix differential of inverse; contraction with the
        # actual eta-skew link variations gives the genuine Lorentz source.
        dB=fac*np.einsum('ij,...j->...i',H,cb)
        Tw=np.zeros_like(e)
        for k,(a,b) in enumerate(PAIR):
            Tw[...,a,b]=dB[...,k];Tw[...,b,a]=-dB[...,k]
        ee[..., :,u]+=np.einsum('...ij,...j->...i',Tw,e[..., :,v])
        ee[..., :,v]-=np.einsum('...ij,...j->...i',Tw,e[..., :,u])
        dc=fac*np.einsum('...i,ij->...j',B,H)
        W=np.zeros_like(e)
        for k,(a,b) in enumerate(PAIR):W[...,a,b]=dc[...,k]*ETA[b,b]
        GP=(W+tr(Piv)@W@tr(Piv))/2
        gA=GP@tr(Bs@Ci@Di)
        gB=tr(Ar)@GP@tr(Ci@Di)
        gCi=tr(Ar@Bs)@GP@tr(Di)
        gDi=tr(Ar@Bs@Ci)@GP
        gC=-tr(Ci)@gCi@tr(Ci)
        gD=-tr(Di)@gDi@tr(Di)
        gU[...,r,:,:]+=gA+shift(gC,s,-1)
        gU[...,s,:,:]+=gD+shift(gB,r,-1)
    if not grad:return f
    # Actual left proper-link tangent delta U_r=h sum_k v_rk G_k U_r.
    ew=np.empty(U.shape[:-2]+(6,))
    for r in range(4):
        for k in range(6):
            ew[...,r,k]=h*np.einsum('...ij,...ij->...',gU[...,r,:,:],GEN[k]@U[...,r,:,:])
    return f,ee,ew


def oneform_lie(A,xi,h):
    # Last axes are (one-form index r, internal component k).
    out=sum(xi[...,a,None,None]*matter.fp(A,a,h) for a in range(4))
    for r in range(4):
        out[...,r,:]+=sum(A[...,a,:]*matter.fp(xi[...,a],r,h)[...,None] for a in range(4))
    return out


def oneform_adjoint(A,E,h):
    W=np.empty(A.shape[:-2]+(4,))
    for a in range(4):
        W[...,a]=np.einsum('...rk,...rk->...',E,matter.fp(A,a,h))
        for r in range(4):
            W[...,a]-=matter.bm(np.einsum('...k,...k->...',E[...,r,:],A[...,a,:]),r,h)
    return W


def matter_source(e,psi,k,h):
    G,w,q=matter.material_data(e,psi,h)
    T=np.einsum('...Ai,...Aj->...ij',w,w)
    d_g=-k[...,None,None]*(G@T@G)
    Ee=2*ETA@e@d_g
    Epsi=np.zeros_like(psi)
    for mu in range(4):
        cur=2*k[...,None]*np.einsum('...j,...Aj->...A',G[...,mu,:],w)
        Epsi-=matter.bm(cur,mu,h)
    return Ee,Epsi


def connection_fields(n):
    shape=(n,)*4;t=np.meshgrid(*([2*np.pi*np.arange(n)/n]*4),indexing='ij')
    omega=np.empty(shape+(4,6))
    # U_r=exp(h Omega_r) on the actual strict principal-log chart.
    # All six algebra directions are active; different links do not commute.
    for r in range(4):
        for k in range(6):
            omega[...,r,k]=(.025*np.sin(t[(r+k)%4]+.2*(k+1))
                            +.01*np.cos(t[(r+1)%4]+t[(k+2)%4]))
    U=expm(np.einsum('...rk,kij->...rij',omega,GEN)/n)
    return omega,U


def run_grid(n):
    h=1/n;e,psi,xi,k,rho=matter.smooth_fields(n);om,U=connection_fields(n)
    lor=float(np.max(abs(tr(U)@ETA@U-ETA)))
    need(lor<1e-12,'original proper-link Lorentz condition n='+str(n))
    f,Ee,Ew=star_density_and_source(e,U,h)
    Jg=oneform_adjoint(tr(e),tr(Ee),h)+oneform_adjoint(om,Ew,h)
    de,dpsi=matter.lie_variation(e,psi,xi,h)
    dom=oneform_lie(om,xi,h)
    direct=float(np.mean(np.einsum('...ai,...ai->...',Ee,de)+np.einsum('...rk,...rk->...',Ew,dom)))
    adjoint=float(np.mean(np.einsum('...a,...a->...',Jg,xi)))
    need(abs(direct-adjoint)<1e-10,'exact geometric source pullback n='+str(n))
    q0=matter.material_data(e,psi,h)[2]
    k,an,native_price,master_error=matter.native_master_grid(q0,rho)
    q,C,R,Jm,chain=matter.material_ward(e,psi,k,h)
    Eem,Epsim=matter_source(e,psi,k,h)
    # an=a/b is the actual Golden coefficient ratio from the same N=1 price.
    total=oneform_adjoint(tr(e),tr(an*Ee+Eem),h)+oneform_adjoint(om,an*Ew,h)
    for a in range(4):total[...,a]+=np.einsum('...A,...A->...',Epsim,matter.fp(psi,a,h))
    expected=an*Jg+Jm+np.stack([k*matter.fp(q,a,h) for a in range(4)],axis=-1)
    closure=float(abs(total-expected).max())
    need(closure<2e-10,'all42 exact finite source Ward balance n='+str(n))
    fd=None; full_fd=None
    if n==4:
        step=1e-6
        V=h*np.einsum('...rk,kij->...rij',dom,GEN)
        Up=expm(step*V)@U;Um=expm(-step*V)@U
        plus=float(np.mean(star_density_and_source(e+step*de,Up,h,grad=False)))
        minus=float(np.mean(star_density_and_source(e-step*de,Um,h,grad=False)))
        fd=abs((plus-minus)/(2*step)-direct)
        need(fd<1e-7,'independent full plaquette and coframe finite difference')
        # Genuine local Lorentz gauge control on all 40 original slots.
        coeff=np.stack([.07*np.sin(2*np.pi*np.indices((n,)*4)[j%4]/n+.1*j)
                        for j in range(6)],axis=-1)
        Lam=np.einsum('...k,kij->...ij',coeff,GEN)
        gauge_e=Lam@e
        gauge_dot=float(np.sum(Ee*gauge_e))
        for r in range(4):
            V=(Lam-U[...,r,:,:]@shift(Lam,r)@inv_lorentz(U[...,r,:,:]))/h
            c=np.stack([V[...,0,1],V[...,0,2],V[...,0,3],
                        V[...,1,2],V[...,1,3],V[...,2,3]],axis=-1)
            gauge_dot+=float(np.sum(Ew[...,r,:]*c))
        need(abs(gauge_dot)<1e-10,'all40 exact local Lorentz source Ward')
        qg=matter.q_first_jet(e,psi,gauge_e,np.zeros_like(psi),h)
        need(float(abs(qg).max())<1e-13,'scalar/coframe dictionary exact Lorentz gauge source')

        qplus=matter.material_data(e+step*de,psi+step*dpsi,h)[2]
        qminus=matter.material_data(e-step*de,psi-step*dpsi,h)[2]
        matplus=matter.native_master_grid(qplus,rho)[2]
        matminus=matter.native_master_grid(qminus,rho)[2]
        actual_secant=an*(plus-minus)/(2*step)+float(np.mean(matplus-matminus))/(2*step)
        full_source=float(np.mean(np.einsum('...a,...a->...',total,xi)))
        full_fd=abs(actual_secant-full_source)
        need(full_fd<2e-6,'full nonlinear Golden K price independently differentiated')
        # Exact flat identity-link control: Palatini density and full discrete
        # Lie contraction vanish, despite no imposed continuum equations.
        flat_e=np.broadcast_to(np.eye(4),e.shape).copy()
        flat_U=np.broadcast_to(np.eye(4),U.shape).copy()
        zf,ze,zw=star_density_and_source(flat_e,flat_U,h)
        need(np.max(abs(zf))+np.max(abs(ze))+np.max(abs(zw))<1e-12,
             'literal flat Palatini all40 source control')
    return {'n':n,'sites':n**4,'lorentz_error':lor,
            'geometry_pullback_error':abs(direct-adjoint),
            'full42_ward_balance_error':closure,'geometry_finite_difference_error':fd,
            'full_nonlinear_price_finite_difference_error':full_fd,
            'native_master_residual':master_error,'native_a_over_b':an,
            'geometric_defect_inf':float(abs(Jg).max()),
            'geometric_defect_over_h':float(abs(Jg).max()/h),
            'material_defect_inf':float(abs(Jm).max()),
            'whole_residual_status':'SAMPLED_DIAGNOSTIC_NOT_A_ROOT'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    need(np.all(STAR@STAR==-np.eye(6)),'original Lorentz middle-degree star')
    need(all(np.max(abs(X.T@ETA+ETA@X))==0 for X in GEN),'all six actual proper-link generators')
    grids=[run_grid(n) for n in (4,8,12,16)]
    result={'status':'PASS_ORIGINAL_ALL42_FINITE_WARD_PULLBACK',
            'input_ref':matter.INPUT_REF,'grids':grids,'checks':checks,
            'scope':{'literal_original_six_face_star':True,
                     'all16_plus24_plus2_source_contract':True,
                     'discrete_diffeomorphism_invariance_assumed':False,
                     'computed_geometric_and_material_defects':True,
                     'actual_N1_master_slope_and_a_over_b':True,
                     'diagnostics_are_stationary_solutions':False,
                     'actual_PF_refinement_regularity_proved':False,
                     'physical_field_writer_or_Book_selected':False,'GR_closed':False}}
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n';print(text,end='')
    if args.json:args.json.write_text(text,encoding='utf-8')

if __name__=='__main__':main()
