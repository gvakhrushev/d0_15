#!/usr/bin/env python3
"""New algebraic consequences of the two supplied D0 syntheses.

Does NOT re-run either original audit, prove global GR, or select native physics.
General analytic proofs and scope conditions are in SYNTHESIS_RU.md.
All equalities below are exact SymPy identities; no floating-point fitting.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

RESULTS: list[dict] = []

def equal(name: str, lhs, rhs=0) -> None:
    d = lhs-rhs
    if isinstance(d, s.MatrixBase):
        ok = all(s.simplify(x)==0 for x in d)
    else:
        ok = s.simplify(d)==0
    if not ok:
        raise RuntimeError(f'FAILED {name}: {d}')
    RESULTS.append({'identity':name, 'result':'exact'})

def condition(name: str, ok: bool) -> None:
    if not bool(ok):
        raise RuntimeError('FAILED '+name)
    RESULTS.append({'identity':name, 'result':'exact'})


def run() -> dict:
    q,y,z,h,a,b,c,eps = s.symbols('q y z h a b c eps', real=True)
    # Smooth connected critical fibres: microscopic z is unconstrained, source unique.
    S=(y-q*q)**2/2+q**3/3
    equal('regular connected critical fibre',s.diff(S,y).subs(y,q*q))
    equal('regular fibre source',s.diff(S,q).subs(y,q*q),q*q)
    equal('regular fibre reduced Hessian',
          (s.diff(S,q,2)-s.diff(S,q,y)**2/s.diff(S,y,2)).subs(y,q*q),2*q)
    # The audit's qc control fails the critical-projection submersion hypothesis.
    singular=q*z
    equal('singular projection control',s.diff(singular,z),q)
    equal('singular horizontal ambiguity',s.diff(singular,q),z)
    # Nonzero vertical Hessian on separate branches does not identify their response.
    Sd=(y*y-1)**2/4+q*y
    equal('disconnected branch stationarity +',s.diff(Sd,y).subs({q:0,y:1}))
    equal('disconnected branch stationarity -',s.diff(Sd,y).subs({q:0,y:-1}))
    condition('disconnected source mismatch',s.diff(Sd,q).subs(y,1)!=s.diff(Sd,q).subs(y,-1))
    # Exact singular Schur reduction: coupled kernel must remain as a variable.
    Ss=a*q*q/2+b*q*y+c*q*z+h*y*y/2
    Sr=s.factor(Ss.subs(y,-b*q/h))
    equal('singular Schur retained-variable reduction',Sr,(a-b*b/h)*q*q/2+c*q*z)
    equal('kernel compatibility is not optional',s.diff(Sr,z),c*q)
    H=s.diag(2,0,0);B=s.Matrix([[3,5],[1,2],[2,4]])
    Hplus=s.diag(s.Rational(1,2),0,0);P=s.eye(3)-H*Hplus
    condition('minimal coupled-kernel rank identity',P*B != s.zeros(3,2))
    condition('coupled-kernel exact rank', (P*B).rank()==H.row_join(B).rank()-H.rank()==1)
    # Large hidden inverse need not create large Schur response.
    He=s.diag(1,eps**2)
    Bbounded=s.Matrix([1,eps**2]); Bdivergent=s.Matrix([1,eps])
    equal('bounded stationary lift despite singular limit',He.inv()*Bbounded,s.Matrix([1,1]))
    equal('bounded response with bounded lift',(Bbounded.T*He.inv()*Bbounded)[0],1+eps**2)
    equal('bounded response alone need not bound lift',(Bdivergent.T*He.inv()*Bdivergent)[0],2)
    equal('divergent lift control',(He.inv()*Bdivergent)[1],1/eps)
    # Exact quadratic resonance form and its rank-one factorization.
    x1,y1,x2,y2,theta=s.symbols('x1 y1 x2 y2 theta', real=True)
    chi1=x1+s.I*y1;chi2=x2+s.I*y2
    Q=x1*x1-y1*y1-x2*x2+y2*y2
    A=s.Matrix([[x1+x2,y1+y2],[y1-y2,x1-x2]])
    equal('resonance equals real determinant',A.det(),Q)
    r,aa,bb=s.symbols('r aa bb', real=True)
    param={x1:r*s.cos(aa),y2:r*s.sin(aa),y1:r*s.cos(bb),x2:r*s.sin(bb)}
    equal('null-cone parametrization',s.trigsimp(Q.subs(param)))
    phase_re=(x1*x1-y1*y1-x2*x2+y2*y2)*s.cos(2*theta)-2*(x1*y1-x2*y2)*s.sin(2*theta)
    rot={x1:x1*s.cos(theta)-y1*s.sin(theta),y1:x1*s.sin(theta)+y1*s.cos(theta),
         x2:x2*s.cos(theta)-y2*s.sin(theta),y2:x2*s.sin(theta)+y2*s.cos(theta)}
    equal('phase rotation of compatibility',s.trigsimp(Q.subs(rot,simultaneous=True)-phase_re))
    equal('phase robust complex factorization',chi1**2-chi2**2,(chi1-chi2)*(chi1+chi2))
    condition('fixed-phase cone not phase robust',phase_re.subs({x1:1,y1:1,x2:0,y2:0,theta:s.pi/4}) == -2)
    for sign in (-1,1):
        equal('robust polarization '+str(sign),(chi1**2-chi2**2).subs({x2:sign*x1,y2:sign*y1}))
    # Complete two-history Gram datum from calibrated positive comparison costs.
    Nm,Np,u,v,ca,si=s.symbols('Nm Np u v ca si', real=True)
    Kplus=Nm+Np-2*(ca*u+si*v)
    Kminus=Nm+Np-2*(ca*u-si*v)
    equal('Gram imaginary quadrature',(Kminus-Kplus)/(4*si),v)
    equal('Gram real quadrature',(2*(Nm+Np)-Kminus-Kplus)/(4*ca),u)
    p=(s.sqrt(5)-1)/2
    equal('golden comparer has unit phase modulus',p+p*p,1)
    # Magnitude/phase first jet: z(t)=exp(t*u/2+i*t*f) for real u,f.
    t,f=s.symbols('t f',real=True)
    psi=s.exp(t*u/2+s.I*t*f)
    equal('raw amplitude first jet',s.diff(psi,t).subs(t,0),u/2+s.I*f)
    N=s.symbols('N',positive=True);N0=s.symbols('N0',positive=True)
    prob=N/(N+N0)
    equal('flag recovers relative normalizer',s.factor(prob/(1-prob)),N/N0)
    equal('flag derivative is log normalizer derivative',s.diff(s.log(prob/(1-prob)),N),1/N)
    # Normalized probabilities / Berry one-form are not automatically a scalar action.
    tt,ff=s.symbols('tt ff',real=True)
    vpsi=s.Matrix([s.cos(tt),s.exp(s.I*ff)*s.sin(tt)])
    A_t=s.im((s.conjugate(vpsi).T*vpsi.diff(tt))[0]).simplify()
    A_f=s.im((s.conjugate(vpsi).T*vpsi.diff(ff))[0]).simplify()
    equal('normalized phase connection theta',A_t)
    equal('normalized phase connection phi',A_f,s.sin(tt)**2)
    equal('nonintegrable phase connection control',s.diff(A_f,tt)-s.diff(A_t,ff),s.sin(2*tt))
    # Induced connection and curvature of the SAME golden instrument from the audit.
    # J(U) = [sqrt(p) I; p U], U=exp(i*x*sigma_x)exp(i*y*sigma_y).
    # Values and two derivatives at zero are exact. No old D0 cubic is recomputed.
    sx=s.Matrix([[0,1],[1,0]]);sy=s.Matrix([[0,-s.I],[s.I,0]]);sz=s.diag(1,-1)
    eye2=s.eye(2);zero2=s.zeros(2)
    JJ=(s.sqrt(p)*eye2).col_join(p*eye2)
    Jx=zero2.col_join(p*s.I*sx);Jy=zero2.col_join(p*s.I*sy)
    Jxy=zero2.col_join(-p*sx*sy)
    Proj=JJ*JJ.H
    equal('golden moving inclusion isometry',JJ.H*JJ,eye2)
    equal('golden record branch zero effect',JJ[:2,:].H*JJ[:2,:],p*eye2)
    equal('golden record branch one effect',JJ[2:,:].H*JJ[2:,:],p*p*eye2)
    ax=JJ.H*Jx;ay=JJ.H*Jy
    equal('golden induced connection x',ax,p*p*s.I*sx)
    equal('golden induced connection y',ay,p*p*s.I*sy)
    dax_y=Jx.H*Jy+JJ.H*Jxy
    day_x=Jy.H*Jx+JJ.H*Jxy
    Fxy=s.simplify(dax_y-day_x+ax*ay-ay*ax)
    Second=Jx.H*(s.eye(4)-Proj)*Jy-Jy.H*(s.eye(4)-Proj)*Jx
    equal('archive-complement curvature identity',Fxy,Second)
    equal('nonzero golden curvature',Fxy,2*s.I*p**3*sz)
    equal('golden branch variance coefficient',p*p*(1-p*p),p**3)
    Qxx=Jx.H*(s.eye(4)-Proj)*Jx
    Qxy=Jx.H*(s.eye(4)-Proj)*Jy
    equal('golden distinguishability quadratic form',Qxx,p**3*eye2)
    equal('golden offdiagonal operator-valued quadratic form',Qxy,s.I*p**3*sz)
    equal('ordinary trace is not Palatini contraction',s.trace(Fxy),0)
    # Field-dependent fine inclusion changes off-diagonal source even with J.H*J=I.
    psi0=s.Matrix([1,0])
    phase_factor=JJ.H*Jy
    condition('moving inclusion first jet is not automatically zero',phase_factor!=zero2)
    # Moving observer Hilbert fibres: no finite-dimensional Poincare representation is claimed.
    eta=s.diag(1,-1,-1,-1);e0=s.Matrix([1,0,0,0])
    def boost(axis:int):
        L=s.eye(4);L[0,0]=L[axis,axis]=s.Rational(5,3)
        L[0,axis]=L[axis,0]=s.Rational(4,3)
        return L
    def canon(u):
        gam=u[0];vec=u[1:4,0]
        C=s.eye(4);C[0,0]=gam
        C[0,1:4]=vec.T;C[1:4,0]=vec
        C[1:4,1:4]=s.eye(3)+vec*vec.T/(gam+1)
        return s.simplify(C)
    def pos(u):return 2*eta*u*u.T*eta-eta
    def W(L,u):return s.simplify(canon(L*u).inv()*L*canon(u))
    Lx,Ly=boost(1),boost(2)
    for label,L,u0 in [('first',Lx,e0),('second',Ly,Lx*e0),('composed',Ly*Lx,e0)]:
        equal(label+' Lorentz identity',L.T*eta*L,eta)
        equal(label+' moving positive norm',L.T*pos(L*u0)*L,pos(u0))
        equal(label+' canonical boost factor',canon(u0).inv().T*canon(u0).inv(),pos(u0))
        equal(label+' positive fibre isometry',W(L,u0).T*W(L,u0),s.eye(4))
        equal(label+' time-axis fixed in trivialization',W(L,u0)*e0,e0)
    equal('observer-fibre composition',W(Ly,Lx*e0)*W(Lx,e0),W(Ly*Lx,e0))
    equal('pure-boost Hilbert rotation is identity',W(Lx,e0),s.eye(4))
    condition('pure boost not physically erased',Lx*e0!=e0)
    Wxy=W(Ly*Lx,e0)
    equal('non-collinear boost rotation cosine',Wxy[1,1],s.Rational(15,17))
    equal('non-collinear boost rotation sine magnitude',Wxy[1,2]**2,s.Rational(8,17)**2)
    # Stationary normal elimination uses the known Schur quartic coefficient.
    HH,BB,CC=s.symbols('HH BB CC',nonzero=True)
    yy=-BB*t*t/(2*HH)
    equal('quartic coefficient',s.expand(HH*yy*yy/2+BB*yy*t*t/2+CC*t**4/24),t**4*(CC/24-BB*BB/(8*HH)))
    # A constant coupled background has source from a g-dependent quartic coefficient.
    g,chi,lam,gl=s.symbols('g chi lam gl',real=True)
    potential=(lam+gl*g)*chi**4
    equal('interaction can source a constant envelope',s.diff(potential,g).subs(g,0),gl*chi**4)
    return {'status':'NEW_EXACT_ALGEBRA_AND_GENERAL_ANALYTIC_DEDUCTIONS',
            'exact_identities':RESULTS,
            'wigner_rotation':str(Wxy),
            'source_audits_replayed':False,
            'original_resonance_cubic_recomputed':False,
            'general_descent_theorem':'analytic proof in SYNTHESIS_RU.md, not certified by finite examples',
            'native_physical_admission_proved':False,
            'nonlinear_resonant_roots_proved':False,
            'GR_closed':False,
            'Lean_compilation':False,
            'sympy':s.__version__}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    out=run()
    text=json.dumps(out,ensure_ascii=False,indent=2)+'\n'
    if args.output: args.output.write_text(text,encoding='utf8')
    print(text)
