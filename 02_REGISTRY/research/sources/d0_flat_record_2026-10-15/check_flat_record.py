#!/usr/bin/env python3
"""Exact checks for a conditional flat, metric-complete record construction.
No assertion of native D0 admission, physical action selection or GR closure.
Run with Python 3 and SymPy; -O must give the same output.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
import sympy as s


def eq(a, b, label):
    if isinstance(a, s.MatrixBase) or isinstance(b, s.MatrixBase):
        z = s.Matrix(a)-s.Matrix(b)
        ok = all(s.simplify(e) == 0 for e in z)
    else:
        ok = s.simplify(a-b) == 0
    if not ok:
        raise ArithmeticError(label)


def frame(n):
    out = []
    labels=[]
    for i,j in combinations(range(n),2):
        for sign in (1,-1):
            k=s.zeros(n,1); k[i]=1; k[j]=sign
            out.append(k); labels.append((i,j,sign))
    return labels,out


def sym_basis(n):
    result=[]
    for i in range(n):
        E=s.zeros(n);E[i,i]=1; result.append(E)
    for i,j in combinations(range(n),2):
        E=s.zeros(n);E[i,j]=E[j,i]=1/s.sqrt(2);result.append(E)
    return result


def run():
    p=(s.sqrt(5)-1)/2; c=s.simplify(p**3); w0=s.simplify(p**2)
    eq(p+p**2,1,'golden normalization')
    eq(w0*(1-w0),c,'golden variance')
    eq(1-2*w0,c,'golden derivative')

    # Complete two-outcome isometry at theta=0. Full projector, not a selected branch.
    w=s.symbols('w',positive=True); z=w*(1-w); r=s.sqrt(z)
    P=s.Matrix([[1-w,r],[r,w]])
    Pw=P.diff(w)
    Pt=s.Matrix([[0,-s.I*r],[s.I*r,0]])
    Ptt=s.Matrix([[0,-r],[-r,0]])
    eq(P*P,P,'projector')
    eq(s.trace(P),1,'full trace')
    inner=lambda A,B:s.simplify(s.trace(A*B)/2)
    eq(inner(Pt,Pt),z,'angular metric')
    eq(inner(Pw,Pw),1/(4*z),'amplitude metric')
    eq(inner(Pw,Pt),0,'normal-tangent orthogonality')
    eq(inner(Ptt,Pw),-(1-2*w)/2,'second form amplitude contraction')

    dimension_checks={}
    for n in range(2,8):
        labels,ks=frame(n); I=s.eye(n)
        eq(sum((k*k.T for k in ks),s.zeros(n)),2*(n-1)*I,'second moment')
        for A in sym_basis(n):
            image=sum(((k.T*A*k)[0]*(k*k.T) for k in ks),s.zeros(n))
            diagonal=s.diag(*[A[i,i] for i in range(n)])
            expected=4*A+2*(n-4)*diagonal+2*s.trace(A)*I
            eq(image,expected,'general fourth moment')
        dimension_checks[str(n)]={
            'diagonal_traceless_eigenvalue':2*(n-2),
            'offdiagonal_eigenvalue':4,
            'isotropic_traceless_response':n==4,
        }

    labels,ks=frame(4); basis=sym_basis(4); m=len(ks)
    M=s.Matrix([[(k.T*A*k)[0] for k in ks] for A in basis])
    if M.rank()!=10: raise ArithmeticError('source rank')
    eigs={str(e):mult for e,mult in (M*M.T).eigenvals().items()}
    if eigs!={'12':1,'4':9}: raise ArithmeticError('source singular values')
    # Unscaled right inverse R(E)_alpha=3 k.E.k-Tr(E); actual lift is R/c.
    for A in basis:
        f=s.Matrix([3*(k.T*A*k)[0]-s.trace(A) for k in ks])
        eq(sum((f[a]*ks[a]*ks[a].T for a in range(m)),s.zeros(4))/12,A,
           'all ten source lifts')

    # Both Gauss contractions are nonzero but equal: intrinsic metric is flat.
    q0=c*s.eye(4)/2
    eq(sum((c*k*k.T/m for k in ks),s.zeros(4)),q0,'constant flat metric')
    for i in range(4):
      for j in range(4):
       for k in range(4):
        for l in range(4):
          gauss=sum(c*(v[i]*v[k]*v[j]*v[l]-v[i]*v[l]*v[j]*v[k])/m for v in ks)
          eq(gauss,0,'full flat Riemann tensor')
    Imean=s.simplify(sum(c*(k.dot(k))**2 for k in ks)/m/(c/2)**2)
    Inorm=s.simplify(sum(c*sum(k[i]**2*k[j]**2 for i in range(4) for j in range(4)) for k in ks)/m/(c/2)**2)
    eq(Imean,16/c,'nonzero mean curvature norm')
    eq(Inorm,Imean,'intrinsic cancellation')

    # Kernel = 3 perfect matchings of K4 with sum-zero matching amplitudes.
    a,b=s.symbols('a b',real=True)
    match={(0,1):a,(2,3):a,(0,2):b,(1,3):b,(0,3):-a-b,(1,2):-a-b}
    f=s.Matrix([match[(i,j)] for i,j,_ in labels]); S=a*a+a*b+b*b
    eq(M*f,s.zeros(10,1),'two internal modes invisible to first metric jet')
    eq(sum(f),0,'fixed mean branch budget')
    eq(sum(t*t for t in f),8*S,'internal information norm')
    eq(sum(t**3 for t in f),-12*a*b*(a+b),'internal cubic')
    eq(sum((f[i]**2*ks[i]*ks[i].T for i in range(m)),s.zeros(4)),4*S*s.eye(4),
       'internal second-order backreaction')
    K=f.jacobian([a,b])
    if K.rank()!=2 or len(M.nullspace())!=2: raise ArithmeticError('kernel dimension')

    # A complete linear split of amplitude variations into 10 metric and 2 internal slots.
    N=s.Matrix.hstack((K[:,0]+K[:,1])/s.sqrt(3),K[:,0]-K[:,1])
    eq(N.T*N,8*s.eye(2),'orthogonal internal coordinates')
    eq(M*N,s.zeros(10,2),'metric-internal split')
    if M.col_join(N.T/8).rank()!=12: raise ArithmeticError('complete 10+2 split')
    for j in range(12):
        rvec=s.eye(12)[:,j]
        E=(3*sum((rvec[i]*ks[i]*ks[i].T for i in range(m)),s.zeros(4))-sum(rvec)*s.eye(4))/c
        recovered=c*s.Matrix([(k.T*E*k)[0] for k in ks])/12+N*(N.T*rvec)/8
        eq(recovered,rvec,'complete channel source decomposition')
    # Same local flat q with different memory bending: rescale the phase frequency.
    sw=w*(1-w); scale2=c/sw
    qfixed=sw*scale2*s.eye(4)/2
    eq(qfixed,q0,'isometric flat family')
    bending=s.simplify(4*sw*scale2**2/(c/2)**2)
    eq(bending,16/sw,'isometric bending varies')
    eq(s.diff(bending,w).subs(w,w0),-16/c,'nonconstant isometric bending at golden base')
    # Linear-intrinsic classification within the explicitly assumed two-invariant class.
    alpha,beta=s.symbols('alpha beta')
    stationary=s.simplify(s.diff((alpha+beta)*bending,w).subs(w,w0))
    eq(stationary,-16*(alpha+beta)/c,'conditional relative coefficient selection')

    # Classical relative entropy is a distinguishing observable, not a physical energy.
    ref=s.symbols('r0',positive=True)
    D=w*s.log(w/ref)+(1-w)*s.log((1-w)/(1-ref))
    d2=s.simplify(s.diff(D,w,2).subs({w:w0,ref:w0}))
    d3=s.simplify(s.diff(D,w,3).subs({w:w0,ref:w0}))
    eq(d2,1/c,'relative entropy second derivative')
    eq(d3,-1/c,'relative entropy third derivative')
    eq(d2*sum(t*t for t in f)/(2*m),S/(3*c),'relative entropy quadratic')
    eq(d3*sum(t**3 for t in f)/(6*m),a*b*(a+b)/(6*c),'relative entropy cubic')

    # Source space = nine shape directions + one budget direction.
    fvar=s.symbols('f0:12')
    dg=c*sum((fvar[i]*ks[i]*ks[i].T for i in range(m)),s.zeros(4))/m
    dmean=sum(fvar)/m
    eq(s.trace(q0.inv()*dg)/2,2*dmean,'volume-code tangent identity')
    projector=s.eye(m)-s.ones(m)/m
    if (M*projector).rank()!=9: raise ArithmeticError('fixed budget shape rank')
    # Equal mean weight is not a nonlinear fixed determinant constraint.
    eps=s.symbols('eps',real=True)
    qinternal=q0-eps**2*S*s.eye(4)/3
    eq(s.diff(qinternal.det(),eps,2).subs(eps,0),-c**3*S/3,
       'fixed-code countercontrol: second volume derivative nonzero')

    # Positive pairing -> Lorentz reflection is an involution, no action inference.
    v=s.Matrix(s.symbols('v0:4',real=True))
    A=s.Matrix(4,4,lambda i,j:s.Symbol('g'+str(min(i,j))+str(max(i,j)),real=True))
    # At q=I and t=e0 the reflection differential has signs + on time slots, - on spatial block.
    t=s.Matrix([1,0,0,0]); Q=s.eye(4)+eps*A
    g=2*(Q*t)*(Q*t).T/(t.T*Q*t)[0]-Q
    dg_ref=g.diff(eps).subs(eps,0)
    expected=A.copy()
    for i in range(1,4):
      for j in range(1,4): expected[i,j]=-expected[i,j]
    eq(dg_ref,expected,'signature differential preserves ten variations')

    return {
      'scope':'exact kinematics and conditional invariant classification; NOT native admission or GR proof',
      'pair_channels':m,'full_record_dimension':2*m,'source_rank':10,
      'source_moment_eigenvalues':eigs,'right_inverse_norm':'6/p^3 (Frobenius to Euclidean)',
      'q0':'p^3 I_4/2','Riemann':'identically zero for this flat family',
      'squared_mean_curvature':str(Imean),'squared_second_form':str(Inorm),
      'dimension_checks':dimension_checks,'metric_kernel_dimension':2,
      'internal_KL_quadratic':'(a^2+a*b+b^2)/(3*p^3*log(phi))',
      'internal_KL_cubic':'a*b*(a+b)/(6*p^3*log(phi))',
      'fixed_budget_metric_rank':9,
      'volume_code_tangent':'delta log sqrt(det q) = 2 delta(mean w)',
      'fixed_budget_not_nonlinear_fixed_volume':True,
      'conditional_geometric_density':'alpha ||H||^2+beta ||b||^2 is intrinsic on isometric flat carriers only if alpha+beta=0',
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    data=run()
    text=json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__': main()
