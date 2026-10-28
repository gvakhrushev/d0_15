#!/usr/bin/env python3
"""Apply the boundary jet to the actual 7cu QUERY/cut orbit algebra.

The symbolic proof is for all original admitted reflection data 0<c<1.
The six-column numerical fixture is a structural rational realization of
that algebra, not a replay of the original 26-stage compiler or all42 fields.
Heat is not asserted constant merely from a zero first derivative.
"""
from __future__ import annotations
import json
import sympy as sp
import numpy as np
import torch

torch.set_default_dtype(torch.float64)
torch.set_num_threads(1)

def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def symbolic():
    c,u,z,d=sp.symbols('c u z d',positive=True,real=True)
    R=sp.symbols('R',positive=True)
    cc=c*sp.cos(2*u*d)-u*sp.sin(2*u*d)
    j=-R*sp.log(1-z+z*cc**2)
    first=sp.diff(j,d).subs(d,0)
    second=sp.diff(j,d,2).subs(d,0)
    first_target=4*R*z*c*u**2/(1-z*u**2)
    second_target=8*R*z*u**2*(1-(2-z)*u**2)/(1-z*u**2)**2
    for name,expr in [('first',first-first_target),('second',second-second_target)]:
        require(sp.factor(expr.subs(c**2,1-u**2))==0,name+' symbolic jet')
    # Endpoint cut and QUERY are both transported by the same skew K0.
    c0=sp.Rational(3,5);u0=sp.Rational(4,5)
    Q=sp.Matrix([[c0,u0],[u0,-c0]])
    P=sp.diag(1,0);K=Q*P-P*Q
    require(Q*Q==sp.eye(2) and K.T==-K,'exact reflection/skew algebra')
    require(K*K==-u0**2*sp.eye(2),'true generator frequency')
    Rval=2;z0=sp.Rational(1,7)
    f=sp.simplify(first_target.subs({c:c0,u:u0,z:z0,R:Rval}))
    s=sp.simplify(second_target.subs({c:c0,u:u0,z:z0,R:Rval}))
    # Require the nontrivial rank-one Hessian, without any positivity claim.
    HH=sp.Matrix([[s,-s],[-s,s]])
    require(HH.det()==0 and HH.rank()==1,'joint gauge Hessian rank')
    require(HH*sp.Matrix([1,1])==sp.zeros(2,1),'joint transport is null')
    # Two-dimensional generating relation x_-=s,x_+=t gives equal momenta,
    # not vanishing of either momentum (boundary charges are retained).
    a,b,cc2=s,-s,s
    Jac=sp.Matrix([[-a/b,-1/b],[b-cc2*a/b,-cc2/b]])
    Omega=sp.Matrix([[0,1],[-1,0]])
    require(Jac.T*Omega*Jac==Omega,'exact orbit canonical relation')
    require(Jac==sp.Matrix([[1,1/s],[0,1]]),'relative-angle twist map')
    # A point with j''=0 is real for all 0<z<1. Do not assert uniform twist.
    threshold=sp.simplify(second_target.subs(u**2,1/(2-z)))
    require(threshold==0,'mixed-rank-loss threshold')
    return {'first_source_at_rational_fixture':str(f),
            'second_source_at_rational_fixture':str(s),
            'rank_of_two_angle_hessian':1,
            'canonical_shear':str(1/s),
            'rank_loss_condition':'c^2=(1-z)/(2-z)',
            'arbitrary_original_c_symbolic_identity':True}


def numerical(zeta:float):
    c=.6;u=.8;rank=2
    Q0=torch.tensor([[c,u],[u,-c]])
    P0=torch.diag(torch.tensor([1.,0.]))
    K0=Q0@P0-P0@Q0
    support=torch.diag(torch.tensor([1.,1.,0.]))
    I=torch.eye(6)
    def price(w):
        s,t=w
        Rt=torch.matrix_exp(t*K0)
        Rs=torch.matrix_exp(s*K0)
        U=torch.kron(torch.eye(3),Rt@Q0@Rt.T)
        P=torch.kron(support,Rs@P0@Rs.T)
        C=(I-P)@U@P
        F=C.T@C
        return -torch.linalg.slogdet(I-zeta*F)[1]
    def scalar(w):
        s,t=w
        delta=t-s
        contrast=c*torch.cos(2*u*delta)-u*torch.sin(2*u*delta)
        return -rank*torch.log(1-zeta+zeta*contrast**2)
    points=[[0.,0.],[.17,-.23],[-.31,.12],[.24,.24]]
    errors=[]
    for pt in points:
        w=torch.tensor(pt)
        value=abs(float(price(w)-scalar(w)))
        grad=torch.autograd.functional.jacobian(price,w)
        gs=torch.autograd.functional.jacobian(scalar,w)
        hh=torch.autograd.functional.hessian(price,w)
        hs=torch.autograd.functional.hessian(scalar,w)
        ge=float(torch.max(torch.abs(grad-gs)))
        he=float(torch.max(torch.abs(hh-hs)))
        require(value<3e-14 and ge<3e-14 and he<3e-14,'six-column full-operator identity')
        errors.append({'point':pt,'value_error':value,'gradient_error':ge,'Hessian_error':he})
    w=torch.zeros(2)
    H=torch.autograd.functional.hessian(price,w).numpy()
    g=torch.autograd.functional.jacobian(price,w).numpy()
    require(np.linalg.norm(H@np.ones(2))<1e-13,'joint-angle second source')
    require(abs(g.sum())<1e-14,'joint-angle first source')
    require(abs(g[1])>0,'relative source is genuinely nonzero')
    threshold=(1-zeta)/(2-zeta)
    return {'zeta':zeta,'ambient_dimension':6,'active_rank':rank,
            'first_source_s_t':g.tolist(),'Hessian_s_t':H.tolist(),
            'c_squared_twist_threshold':threshold,'checks':errors}


def main():
    out={'status':'PASS_SAME_QUERY_CUT_RELATIVE_ORBIT_JET',
         'consumed_native_source_commit':'172876cdf38bfce6f87fdd4a059d524b60c10eb9',
         'consumed_equations':'7cu:831,835',
         'symbolic':symbolic(),
         'full_matrix_controls':[numerical(1/7),numerical(2**-20)],
         'original_26_stage_replayed':False,
         'physical_temporal_boundary_identified':False,
         'heat_second_variation_set_to_zero':False,
         'original_unpadded42_carrier_identified_with_common_null':False,
         'GR_closed':False}
    print(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()
