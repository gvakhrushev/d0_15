#!/usr/bin/env python3
"""Conditional ADM closure test, NOT a D0 native generator reconstruction.

Exact symbolic contractions plus numerical Poisson brackets computed by AD
from the unreduced canonical Hamiltonian on a periodic Fourier regulator.
The numerical controls keep all six spatial metric/momentum components but
use fields depending on one spatial coordinate. They do not prove a lattice
constraint algebra or any D0->GR claim; the continuum proof is in PROOF_RU.md.
"""
from __future__ import annotations
import json
import math
import sys
import numpy as np
import sympy as sp
import torch

torch.set_default_dtype(torch.float64)
torch.set_num_threads(1)

def check(ok: bool, text: str) -> None:
    if not ok:
        raise AssertionError(text)


def exact_controls() -> dict:
    lam=sp.symbols('lambda', real=True)
    p00,p11,p22,p01,p02,p12=sp.symbols('p00 p11 p22 p01 p02 p12')
    n00,n11,n22,n01,n02,n12=sp.symbols('n00 n11 n22 n01 n02 n12')
    P=sp.Matrix([[p00,p01,p02],[p01,p11,p12],[p02,p12,p22]])
    N=sp.Matrix([[n00,n01,n02],[n01,n11,n12],[n02,n12,n22]])
    I=sp.eye(3)
    # Pointwise tensor identity in an orthonormal spatial frame. It is tensorial.
    lhs=sp.trace((P-lam*sp.trace(P)*I)*(sp.trace(N)*I-N))
    rhs=(1-2*lam)*sp.trace(P)*sp.trace(N)-sp.trace(P*N)
    check(sp.expand(lhs-rhs)==0,'gravitational trace-anomaly contraction')
    C=sp.Matrix([[sp.Rational(13,10),sp.Rational(1,5)],
                 [sp.Rational(1,5),sp.Rational(9,10)]])
    D=C.inv()
    check(C*D==sp.eye(2),'common matter cone inverse matrices')
    K=sp.Matrix([[sp.Rational(3,5),sp.Rational(2,7),0],
                 [sp.Rational(2,7),-sp.Rational(1,3),sp.Rational(1,8)],
                 [0,sp.Rational(1,8),sp.Rational(4,9)]])
    pi=K-sp.trace(K)*I
    check(pi-sp.Rational(1,2)*sp.trace(pi)*I==K,'Legendre trace inversion')
    check(sp.expand(sp.trace(pi*pi)-sp.trace(pi)**2/2
                    -(sp.trace(K*K)-sp.trace(K)**2))==0,'Legendre ADM kinetic form')
    # Curvature of the prior moving-cut connection is internal, not HDA.
    Pcut=sp.diag(1,1,0,0)
    W1=sp.Matrix([[1,2],[3,4]])
    W2=sp.Matrix([[0,1],[-1,2]])
    def tang(w):
        return sp.zeros(2).row_join(w.T).col_join(w.row_join(sp.zeros(2)))
    S1,S2=tang(W1),tang(W2)
    comm=lambda a,b:a*b-b*a
    K1,K2=comm(S1,Pcut),comm(S2,Pcut)
    check(comm(K1,Pcut)==S1 and comm(K2,Pcut)==S2,'moving-cut transport identity')
    check(comm(K1,K2)==-comm(S1,S2),'cut curvature algebra')
    # d1K2-d2K1=-2[S1,S2], hence curvature Omega=-[S1,S2].
    Omega=-2*comm(S1,S2)-comm(K1,K2)
    check(Omega==-comm(S1,S2) and comm(Omega,Pcut)==sp.zeros(4),
          'Kato curvature is block diagonal')
    check(Omega!=sp.zeros(4),'nonzero internal curvature control')
    # Anomaly witnesses on a periodic unit spatial metric: N=1, M=cos(x).
    x=sp.symbols('x', real=True)
    v=-sp.sin(x)
    # Divergence-free momentum: pi_22=cos(x), all others zero, hence Dg=0.
    anomaly=sp.integrate(v*sp.diff(sp.cos(x),x),(x,0,2*sp.pi))
    check(anomaly==sp.pi,'isolated lambda anomaly witness')
    # pi_11=cos(x), pi_22=-cos(x) is trace-free and has Dg != 0.
    dg=sp.integrate(v*(-2*sp.diff(sp.cos(x),x)),(x,0,2*sp.pi))
    check(dg==-2*sp.pi,'isolated AB anomaly witness')
    # p=1, phi=cos(x) detects any chosen field-space CD entry.
    matter=sp.integrate(v*sp.diff(sp.cos(x),x),(x,0,2*sp.pi))
    check(matter==sp.pi,'matter speed-matrix anomaly witness')
    return {'symbolic_tests':10,'cut_curvature_nonzero':True,
            'lambda_witness_integral':'pi','gravity_witness_integral':'-2*pi',
            'matter_witness_integral':'pi'}


def deriv(t: torch.Tensor) -> torch.Tensor:
    n=t.shape[0]
    freqs=torch.fft.fftfreq(n,d=1.0/n).reshape((n,)+(1,)*(t.ndim-1))
    return torch.fft.ifft(1j*freqs*torch.fft.fft(t,dim=0),dim=0).real


def connection(q: torch.Tensor):
    inv=torch.linalg.inv(q)
    dq=deriv(q)
    zero=torch.zeros_like(dq)
    partial=torch.stack([dq,zero,zero],dim=1) # site, derivative, row, column
    gamma=[]
    for k in range(3):
        rows=[]
        for i in range(3):
            vals=[]
            for j in range(3):
                s=sum(inv[:,k,l]*(partial[:,i,l,j]+partial[:,j,l,i]-partial[:,l,i,j])
                      for l in range(3))/2
                vals.append(s)
            rows.append(torch.stack(vals,dim=1))
        gamma.append(torch.stack(rows,dim=1))
    gam=torch.stack(gamma,dim=1) # site, upper, lower, lower
    dgam=deriv(gam)
    ric=[]
    for i in range(3):
        cols=[]
        for j in range(3):
            val=dgam[:,0,i,j]
            if j==0:
                val=val-sum(dgam[:,k,i,k] for k in range(3))
            val=val+sum(gam[:,k,k,l]*gam[:,l,i,j]-gam[:,k,j,l]*gam[:,l,i,k]
                        for k in range(3) for l in range(3))
            cols.append(val)
        ric.append(torch.stack(cols,dim=1))
    Ric=torch.stack(ric,dim=1)
    scalar=torch.einsum('nij,nij->n',inv,Ric)
    return inv,gam,scalar


def hamiltonian(fields, lapse, A,B,lam,C,D,Lambda=0.23,quartic=0.0):
    q,pi,phi,p=fields
    q=(q+q.transpose(1,2))/2
    pi=(pi+pi.transpose(1,2))/2
    inv,gam,R=connection(q)
    sqrtq=torch.sqrt(torch.linalg.det(q))
    trpi=torch.einsum('nij,nij->n',q,pi)
    pi_lo=q@pi@q
    pisq=torch.einsum('nij,nij->n',pi_lo,pi)
    grav=(A*(pisq-lam*trpi**2)/sqrtq-B*sqrtq*R+2*B*Lambda*sqrtq
          +quartic*sqrtq*(pisq/sqrtq**2)**2)
    dp=deriv(phi)
    matter=(torch.einsum('na,ab,nb->n',p,C,p)/(2*sqrtq)
            +sqrtq*inv[:,0,0]*torch.einsum('na,ab,nb->n',dp,D,dp)/2)
    potential=sqrtq*(.17*phi[:,0]**2+.11*phi[:,1]**2+.03*phi[:,0]**2*phi[:,1]**2)
    return (2*math.pi/q.shape[0])*torch.sum(lapse*(grav+matter+potential))


def fields_for(n:int,curved=True):
    x=torch.arange(n)*(2*math.pi/n)
    c,s=torch.cos,torch.sin
    L=torch.zeros(n,3,3)
    L[:,0,0]=torch.exp(.13*s(x)) if curved else 1.
    L[:,1,1]=torch.exp(.08*c(2*x)) if curved else 1.1
    L[:,2,2]=torch.exp(-.09*c(x)) if curved else .9
    if curved:
        L[:,1,0]=.07*c(x);L[:,2,0]=.06*s(2*x);L[:,2,1]=.05*c(3*x)
    q=L@L.transpose(1,2)
    pi=torch.zeros_like(q)
    pi[:,0,0]=.3*c(x)+.1*s(2*x)
    pi[:,1,1]=.2*s(x)-.1*c(2*x)
    pi[:,2,2]=.12*c(3*x)+.07
    pi[:,0,1]=pi[:,1,0]=.08*s(2*x)
    pi[:,0,2]=pi[:,2,0]=.09*c(2*x)
    pi[:,1,2]=pi[:,2,1]=.05*s(x)
    phi=torch.stack([s(x)+.2*c(2*x),.3*c(x)-.1*s(3*x)],dim=1)
    p=torch.stack([.4*c(2*x)+.15,.3*s(x)+.1],dim=1)
    N=1+.2*s(x)+.15*c(2*x)
    M=.7+.3*c(x)-.1*s(2*x)
    return [v.detach().requires_grad_(True) for v in [q,pi,phi,p]],N,M


def bracket_test(n, A,B,lam,C,D,curved=True,quartic=0.0):
    fields,N,M=fields_for(n,curved)
    HN=hamiltonian(fields,N,A,B,lam,C,D,quartic=quartic)
    HM=hamiltonian(fields,M,A,B,lam,C,D,quartic=quartic)
    gn=torch.autograd.grad(HN,fields,retain_graph=False)
    gm=torch.autograd.grad(HM,fields,retain_graph=False)
    w=2*math.pi/n
    bracket=(sum(torch.sum(gn[a]*gm[b]-gn[b]*gm[a]) for a,b in [(0,1),(2,3)])/w).item()
    with torch.no_grad():
        q,pi,phi,p=fields
        inv,gam,R=connection(q)
        vlower=N*deriv(M)-M*deriv(N)
        v=inv[:,:,0]*vlower[:,None]
        div=deriv(pi)[:,:,0]+torch.einsum('njkl,nkl->nj',gam,pi)
        Dg=-2*torch.einsum('nij,nj->ni',q,div)
        trpi=torch.einsum('nij,nij->n',q,pi)
        gamma_trace=torch.stack([sum(gam[:,k,k,i] for k in range(3)) for i in range(3)],dim=1)
        gradtrace=torch.zeros(n,3);gradtrace[:,0]=deriv(trpi)
        gradtrace=gradtrace-gamma_trace*trpi[:,None]
        grav=w*torch.sum(v*Dg).item()
        anomaly=w*torch.sum(v*gradtrace).item()
        CDeff=C@D
        matter=w*torch.sum(v[:,0]*torch.einsum('na,ab,nb->n',p,CDeff,deriv(phi))).item()
        matter_standard=w*torch.sum(v[:,0]*torch.sum(p*deriv(phi),dim=1)).item()
        pisq=torch.einsum('nij,nij->n',q@pi@q,pi)
        X=pisq/torch.linalg.det(q)
        current=4*B*quartic*X[:,None,None]*(pi-trpi[:,None,None]*inv)
        current_div=deriv(current)[:,:,0]+torch.einsum('njkl,nkl->nj',gam,current)
        quartic_bracket=-w*torch.sum(vlower*current_div[:,0]).item()
        prediction=A*B*grav+matter+2*A*B*(1-2*lam)*anomaly+quartic_bracket
        desired=grav+matter_standard
    return {'n':n,'poisson_bracket':bracket,'predicted_bracket':prediction,
            'discretization_error':abs(bracket-prediction),'geometric_closure_defect':bracket-desired,
            'predicted_closure_defect':prediction-desired,
            'D_gravity':grav,'D_matter':matter_standard,'trace_witness':anomaly}


def main():
    out={'scope':'conditional continuum Hamiltonian class; numerical controls are NOT native D0',
         'exact':exact_controls()}
    C=torch.tensor([[1.3,.2],[.2,.9]])
    D=torch.linalg.inv(C)
    good=[bracket_test(n,1.7,1/1.7,.5,C,D) for n in (17,33,65)]
    wrong_quartic=bracket_test(65,1.7,1/1.7,.5,C,D,quartic=.35)
    wrong_lambda=bracket_test(65,1.7,1/1.7,.41,C,D)
    wrong_gravity=bracket_test(65,1.7,.7,.5,C,D)
    wrong_matter=bracket_test(65,1.7,1/1.7,.5,C,D+torch.tensor([[.2,.1],[.1,-.05]]))
    for row in good[-2:]+[wrong_lambda,wrong_gravity,wrong_matter,wrong_quartic]:
        check(row['discretization_error']<1e-8,'continuum bracket against unreduced AD control')
    check(abs(good[-1]['geometric_closure_defect'])<1e-9,'good coefficient closure')
    for row in [wrong_lambda,wrong_gravity,wrong_matter,wrong_quartic]:
        check(abs(row['geometric_closure_defect'])>1e-4,'wrong coefficient detected')
    out.update({'correct_family':good,'negative_controls':{'trace_coefficient':wrong_lambda,
                'gravity_speed':wrong_gravity,'matter_matrix':wrong_matter,'quartic_kinetic':wrong_quartic},
                'D0_native_lapse_generators_constructed':False,
                'D0_native_symplectic_form_constructed':False,
                'D0_root_closure_proved':False,
                'GR_closed':False,'status':'PASS_CONDITIONAL_REFOLIATION_CLOSURE'})
    print(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()
