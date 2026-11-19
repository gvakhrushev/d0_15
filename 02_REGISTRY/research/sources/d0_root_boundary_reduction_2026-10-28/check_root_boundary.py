#!/usr/bin/env python3
"""Full Book03-type spectral Hessian and conditional boundary reduction.

All numerical families below are STRUCTURAL finite-matrix controls, not an
assertion of a physically admitted D0 field or local lapse generator.
The action is evaluated as given, including its full thermal normalizer.
The boundary chart is fixed before root solving. No archived code is run.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
import scipy.linalg as la
from scipy.optimize import brentq, root
import torch

torch.set_default_dtype(torch.float64)
torch.set_num_threads(1)
DT=torch.complex128
P=(math.sqrt(5)-1)/2
BETA=2*P*P


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise AssertionError(msg)


def t(a): return torch.tensor(a,dtype=DT)

I=torch.eye(4,dtype=DT)
P0=t(np.diag([1,1,0,0]))
G=t(np.kron([[math.sqrt(P),-P],[P,math.sqrt(P)]],np.eye(2)))
SX=t(la.block_diag(np.eye(2),1j*np.diag([1,-1])))
U0=SX@G
rng=np.random.default_rng(281026)
HH=[]
for k in range(6):
    R=rng.integers(-3,4,(4,4))+1j*rng.integers(-3,4,(4,4))
    HH.append(t((R+R.conj().T)/20))
K1,K2,K3=[1j*h for h in HH[:3]]
D0=t(np.diag([.3,.7,1.2,1.8]))+.13*HH[4]


def operators(v):
    x,z,y=v
    U=torch.matrix_exp(x*K1)@U0@torch.matrix_exp(z*K2)@torch.matrix_exp(y*K3)
    W=torch.matrix_exp(.4*x*K2+.3*y*K3+.1*torch.sin(z)*K1)
    cut=W@P0@W.mH
    M=D0+.12*x*HH[0]+.1*y*HH[1]+.08*torch.sin(z)*HH[2]+.03*torch.cos(z)*HH[3]
    delta=M.mH@M
    C=(I-cut)@U@cut
    F=C.mH@C
    return U,cut,delta,F


def price(v, fugacity=2**-20):
    _,_,delta,F=operators(v)
    Z=torch.trace(torch.matrix_exp(-BETA*delta)).real
    K=I-fugacity*F
    return torch.log(Z)/BETA-torch.linalg.slogdet(K)[1]


def real_matrices(v):
    _,_,delta,F=operators(v)
    return torch.stack([delta.real,delta.imag,F.real,F.imag])


def all_derivatives(point, fugacity):
    v=torch.tensor(point,dtype=torch.float64,requires_grad=True)
    mats=real_matrices(v).detach().numpy()
    jac=torch.func.jacfwd(real_matrices)(v).detach().numpy()
    second=torch.func.jacfwd(torch.func.jacfwd(real_matrices))(v).detach().numpy()
    Hd=torch.autograd.functional.hessian(lambda w:price(w,fugacity),v).detach().numpy()
    grad=torch.autograd.functional.jacobian(lambda w:price(w,fugacity),v).detach().numpy()
    delta=mats[0]+1j*mats[1];F=mats[2]+1j*mats[3]
    dD=jac[0]+1j*jac[1];dF=jac[2]+1j*jac[3]
    ddD=second[0]+1j*second[1];ddF=second[2]+1j*second[3]
    return delta,F,dD,dF,ddD,ddF,grad,Hd


def spectral_hessian(point,fugacity):
    delta,F,dD,dF,ddD,ddF,g,Hd=all_derivatives(point,fugacity)
    lam,V=la.eigh(delta)
    logw=-BETA*lam
    p=np.exp(logw-logw.max());p=p/p.sum()
    rho=(V*p)@V.conj().T
    LM=np.empty((4,4))
    for i in range(4):
        for j in range(4):
            diff=math.log(p[i])-math.log(p[j])
            LM[i,j]=p[i] if abs(diff)<1e-12 else (p[i]-p[j])/diff
    R=la.inv(np.eye(4)-fugacity*F)
    analytic=np.empty((3,3));ga=np.empty(3)
    naive=np.empty((3,3))
    for a in range(3):
        Da=dD[:,:,a];Fa=dF[:,:,a]
        ga[a]=(-np.trace(rho@Da)+fugacity*np.trace(R@Fa)).real
        for b in range(3):
            Db=dD[:,:,b];Fb=dF[:,:,b]
            Ae=V.conj().T@Da@V;Be=V.conj().T@Db@V
            means=np.trace(rho@Da)*np.trace(rho@Db)
            cov=(np.sum(LM*Ae*Be.T)-means).real
            covariance_naive=(np.trace(rho@Da@Db)-means).real
            rest=(-np.trace(rho@ddD[:,:,a,b])+fugacity*np.trace(R@ddF[:,:,a,b])
                  +fugacity**2*np.trace(R@Fb@R@Fa)).real
            analytic[a,b]=BETA*cov+rest
            naive[a,b]=BETA*covariance_naive+rest
    err=float(np.max(np.abs(analytic-Hd)))
    ge=float(np.max(np.abs(ga-g)))
    require(err<3e-10,'full noncommuting Hessian mismatch')
    require(ge<3e-11,'full first source mismatch')
    naive_err=float(np.max(np.abs(naive-Hd)))
    require(naive_err>1e-6,'noncommuting covariance negative control was not detected')
    # Central finite differences of the full gradient, independent of formula.
    def gradient(x):
        return torch.autograd.functional.jacobian(lambda w:price(w,fugacity),
                       torch.tensor(x,dtype=torch.float64)).numpy()
    eps=2e-5;Hfd=np.empty((3,3))
    for b in range(3):
        step=np.eye(3)[b]*eps
        Hfd[:,b]=(gradient(np.asarray(point)+step)-gradient(np.asarray(point)-step))/(2*eps)
    fd_err=float(np.max(np.abs(Hfd-Hd)))
    require(fd_err<5e-7,'full-gradient finite-difference Hessian mismatch')
    return {'fugacity':fugacity,'analytic_vs_AD':err,'first_source_error':ge,
            'finite_difference_error':fd_err,'incorrect_commuting_covariance_error':naive_err}


def boundary_control():
    # Fixed structural chart: boundary (x,y), retained internal variable z.
    x0,y0=.17,-.21
    def grad(x,z,y):
        v=torch.tensor([x,z,y],dtype=torch.float64)
        return torch.autograd.functional.jacobian(price,v).numpy()
    grid=np.linspace(-math.pi,math.pi,41)
    zz=[]
    for l,r in zip(grid[:-1],grid[1:]):
        if grad(x0,l,y0)[1]*grad(x0,r,y0)[1]<0:
            zz.append(brentq(lambda z:grad(x0,z,y0)[1],l,r,xtol=1e-13))
    require(bool(zz),'no structural stationary interior branch found')
    chosen=None
    for z0 in sorted(zz,key=abs):
        v=torch.tensor([x0,z0,y0])
        H=torch.autograd.functional.hessian(price,v).numpy()
        ii=[0,2]
        He=H[np.ix_(ii,ii)]-np.outer(H[ii,1],H[1,ii])/H[1,1]
        if abs(H[1,1])>1e-4 and abs(He[0,1])>1e-4:
            chosen=(z0,H,He);break
    require(chosen is not None,'structural branch is not regular/twisted')
    z0,H,He=chosen
    def zstar(x,y):
        sol=root(lambda w:[grad(x,w[0],y)[1]],[z0],tol=1e-11)
        residual=abs(grad(x,sol.x[0],y)[1])
        require(residual<2e-11,'interior solve residual too large')
        return float(sol.x[0])
    def reduced_gradient(x,y):
        z=zstar(x,y)
        g=grad(x,z,y)
        return g[[0,2]]
    step=2e-5
    He_fd=np.column_stack([(reduced_gradient(x0+step,y0)-reduced_gradient(x0-step,y0))/(2*step),
                           (reduced_gradient(x0,y0+step)-reduced_gradient(x0,y0-step))/(2*step)])
    schur_err=float(np.max(np.abs(He-He_fd)))
    require(schur_err<3e-8,'stationary Schur response mismatch')
    a,b,c=He[0,0],He[0,1],He[1,1]
    map_jac=np.array([[-a/b,-1/b],[b-c*a/b,-c/b]])
    Omega=np.array([[0.,1.],[-1.,0.]])
    sympl_err=float(np.max(np.abs(map_jac.T@Omega@map_jac-Omega)))
    require(sympl_err<1e-10,'generating-relation symplectic identity failed')
    g0=reduced_gradient(x0,y0);pin=-g0[0]
    def canonical_map(x,pin_new):
        def equations(w):
            z,y=w
            gg=grad(x,z,y)
            return [gg[1],gg[0]+pin_new]
        sol=root(equations,[z0,y0],tol=1e-11)
        require(np.max(np.abs(equations(sol.x)))<3e-11,'canonical solve residual')
        z,y=sol.x
        return np.array([y,grad(x,z,y)[2]])
    h=1e-6
    def fd5(fun,a):
        return (-fun(a+2*h)+8*fun(a+h)-8*fun(a-h)+fun(a-2*h))/(12*h)
    Jfd=np.column_stack([fd5(lambda xx:canonical_map(xx,pin),x0),
                         fd5(lambda pp:canonical_map(x0,pp),pin)])
    map_err=float(np.max(np.abs(Jfd-map_jac)))
    map_relative_err=map_err/max(1.,float(np.max(np.abs(map_jac))))
    require(map_relative_err<2e-7,'canonical implicit map relative finite-difference mismatch')
    freeze_err=float(np.max(np.abs(H[np.ix_([0,2],[0,2])]-He)))
    require(freeze_err>1e-6,'frozen internal variable negative control absent')
    # Canonical structure exists here only as a boundary relation of this
    # structural price/chart. No actual D0 ADM or lapse map is asserted.
    return {'stationary_internal_coordinate':z0,'internal_residual':abs(grad(x0,z0,y0)[1]),
            'internal_Hessian':float(H[1,1]),'boundary_mixed_Hessian':float(b),
            'reduced_Hessian':He.tolist(),'Schur_vs_reduced_derivative_error':schur_err,
            'symplectic_error':sympl_err,'implicit_map_Jacobian_error':map_err,
            'implicit_map_Jacobian_relative_error':map_relative_err,
            'incorrect_frozen_interior_Hessian_error':freeze_err}


def determinant_sewing():
    # Fixed 2+2 block split of the ORIGINAL full resolvent matrix in this
    # structural control. This is Gaussian block elimination, NOT an
    # identification with physical stationary-field elimination.
    def pieces(v,zeta=.19):
        _,_,delta,F=operators(v)
        K=I-zeta*F
        Ki=K[:2,:2];B=K[:2,2:];D=K[2:,2:]
        Schur=D-B.mH@torch.linalg.solve(Ki,B)
        ji=-torch.linalg.slogdet(Ki)[1]
        jb=-torch.linalg.slogdet(Schur)[1]
        direct=-torch.linalg.slogdet(K)[1]
        return direct,ji+jb,jb
    v=torch.tensor([.31,-.43,.27])
    a,b,c=pieces(v)
    grads=[torch.autograd.functional.jacobian(lambda w:pieces(w)[j],v).numpy() for j in range(3)]
    value_err=abs(float((a-b).detach()))
    source_err=float(np.max(np.abs(grads[0]-grads[1])))
    erased_error=float(np.max(np.abs(grads[0]-grads[2])))
    require(value_err<1e-12 and source_err<1e-12,'exact full determinant sewing mismatch')
    require(erased_error>1e-3,'erasing internal determinant negative control absent')
    return {'value_error':value_err,'full_source_error':source_err,
            'source_error_if_internal_determinant_erased':erased_error}


def exact_seam():
    # No actual extra physical price added: elementary comparison that
    # exposes why the logs of separate slabs cannot replace the whole price.
    import sympy as s
    a,d,c,x=s.symbols('a d c x', positive=True)
    # K=[[a,xc],[xc,d]]; full J=-ln(a*d-x²c²).
    J=-s.log(a*d-x*x*c*c)
    Jsewn=-s.log(a)-s.log(d-x*x*c*c/a)
    require(s.simplify(s.diff(J-Jsewn,x))==0,'symbolic Schur source')
    naive=-s.log(a)-s.log(d)
    require(s.simplify(s.diff(J-naive,x)-2*x*c*c/(a*d-x*x*c*c))==0,
            'exact nonadditive seam response')
    # A mixed Hessian may be zero even though the full function exists:
    # f(x,y)=f0(x)+f1(y) defines a Lagrangian relation but not a twist map.
    y=s.symbols('y',real=True)
    require(s.diff(x*x+y*y,x,y)==0,'degenerate boundary negative control')
    return {'symbolic_sewing':True,'naive_seam_derivative':'2*x*c^2/(a*d-x^2*c^2)',
            'canonical_map_requires_mixed_rank':True}


def main():
    out={
      'status':'PASS_ROOT_HESSIAN_AND_CONDITIONAL_BOUNDARY_REDUCTION',
      'source_commit':'c4a92cb0f2326bf7ae2a8127c49f5b65ea71ce5a',
      'hessian_controls':[spectral_hessian([.21,-.37,.29],2**-20),
                          spectral_hessian([-.14,.61,.43],.19)],
      'boundary':boundary_control(),
      'sewing':determinant_sewing(),
      'exact':exact_seam(),
      'scope':'full spectral formula; structural matrix charts, not original D0 causal boundary',
      'D0_native_causal_boundary_identified':False,
      'D0_native_lapse_generators_constructed':False,
      'original_all42_replayed':False,'Lean_or_CI_run':False,'GR_closed':False}
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
