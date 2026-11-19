#!/usr/bin/env python3
"""Whole spectral action: exact scalar elimination, regular nonlinear sectors,
source/second-source transport, literal scene heat, and negative controls.

Run: OPENBLAS_NUM_THREADS=1 python check_spectral_closure.py
All requires remain active under python -O. No file is modified by this checker.
Analytic theorems, interval certificates, and floating diagnostics are separately
reported. No native full-execution/GR claim follows from passing this script.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import itertools
import json
import importlib.util
import numpy as np
import sympy as sp
from mpmath import mp, iv
from scipy.linalg import expm, expm_frechet
from native_spectral import jets, complete

mp.dps = 80
iv.dps = 100
CHECKS: list[str] = []
ROOT = Path(__file__).resolve().parent


def require(label: str, yes: bool) -> None:
    if not bool(yes):
        raise ArithmeticError(label)
    CHECKS.append(label)


def near(label, a, b, tol=mp.mpf('1e-60')):
    require(label, abs(a-b) < tol)


def interval_ends(a):
    # Decimal display only. All certified predicates use the iv endpoints.
    return [mp.nstr(mp.mpf(a.a), 27), mp.nstr(mp.mpf(a.b), 27)]


def upper_abs(a):
    return max(abs(a.a), abs(a.b))



def independent_scalar_jets():
    """Check the handwritten interval jets against independent mp differentiation
    of a scalar expression, without using any jet formula in the reference."""
    def scalar(x, y, theta):
        p=(mp.sqrt(5)-1)/2; z=mp.mpf(2)**-20; beta=2*p*p
        E=p*p*(1+x); l=4*E*(1-E)
        b=p-p*p*y; bb=4*b*b*(1-b*b)
        aa=1-(1-l)*(1-bb)
        return -mp.log1p(-z*aa)-mp.log1p(-z*bb)+theta*(mp.exp(-beta*aa)+mp.exp(-beta*bb))/beta
    points=[('0','0','0'),('.008','-.00015','4e-7'),
            ('-.007','.00012','2e-7'),('.001','-.00003','1e-8')]
    errors=[]
    for xs,ys,ths in points:
        x,y,theta=map(mp.mpf,(xs,ys,ths)); v=jets(mp,x,y,theta)
        fun=lambda xx,yy:scalar(xx,yy,theta)
        for key,order in [('F',(0,0)),('Fx',(1,0)),('Fy',(0,1)),
                          ('Fxx',(2,0)),('Fxy',(1,1)),('Fyy',(0,2))]:
            reference=mp.diff(fun,(x,y),order)
            errors.append(abs(reference-v[key]))
            near('independent scalar versus interval jet '+key,reference,v[key])
        def thfun(xx,yy):
            base=jets(mp,xx,yy)
            return 2/(mp.mpf(17)+2*mp.mpf(2162688)*base['t'])
        def G(xx,yy):
            th=thfun(xx,yy)
            fx=mp.diff(lambda zz:scalar(zz,yy,th),xx)
            fy=mp.diff(lambda zz:scalar(xx,zz,th),yy)
            return xx*fx-yy*fy
        c=complete(mp,x,y,mp.mpf(2162688),mp.mpf(17))
        near('independent self-consistent thermal trace x source',mp.diff(G,(x,y),(1,0)),c['Gx'])
        near('independent self-consistent thermal trace y source',mp.diff(G,(x,y),(0,1)),c['Gy'])
    return dict(points=len(points),derivative_checks=8*len(points),
                max_scalar_jet_error=mp.nstr(max(errors),16),
                scope='Independent high-precision diagnostics of the algebraic formulas used by the outward interval proof; not an interval oracle replacement.')


def interval_certificate():
    Wmin = 528*8**4
    p=(iv.sqrt(5)-1)/2; beta=2*p*p
    theta_max=iv.exp(beta)/(2*Wmin)
    theta=iv.mpf([0,theta_max.b])
    x=iv.mpf(['-.01','.01']); y=iv.mpf(['-.0002','.0002'])
    v=jets(iv,x,y,theta)
    # Use the equivalent positive factorization to certify the physical range.
    E=p*p*(1+x); L=4*E*(1-E)
    b=p-p*p*y; B=4*b*b*(1-b*b)
    A=1-(1-L)*(1-B)
    require('entire operand rectangle has 0<L<1', L.a>0 and L.b<1)
    require('entire operand rectangle has 0<B<A<1', B.a>0 and A.b<1 and (A-B).a>0)
    require('uniform positive geometric slope', v['Fx'].a>iv.mpf('1.38e-8'))
    require('uniform negative matter slope', v['Fy'].b<-iv.mpf('3.30e-7'))
    require('whole nonlinear Ward map has negative nonzero determinant',
            v['ward_det'].b<-iv.mpf('4.04e-15'))
    require('fixed-thermal trace equation is monotone in x', v['Tx'].a>iv.mpf('1.318e-8'))
    Ttheta=-x*iv.exp(-beta*v['A'])*v['Ax']+y*(iv.exp(-beta*v['A'])*v['Ay']+iv.exp(-beta*v['B'])*v['By'])
    # For all W>=Wmin and Z0>=0, W theta <= 1/t. Avoid dependency explosion
    # from feeding an unbounded W interval into W*theta^2.
    correction=upper_abs(Ttheta)*theta_max*beta*iv.exp(-beta*v['A'])*upper_abs(v['Ax'])/v['t']
    Gx_lower=v['Tx'].a-correction.b
    require('self-consistent (not frozen theta) trace derivative positive',
            Gx_lower>iv.mpf('1.318e-8'))
    minus=jets(iv,iv.mpf('-.01'),y,theta)['T']
    plus=jets(iv,iv.mpf('.01'),y,theta)['T']
    require('left endpoint strictly negative for all sectors', minus.b<-iv.mpf('5.8e-11'))
    require('right endpoint strictly positive for all sectors', plus.a>iv.mpf('4.9e-11'))
    return dict(precision='100-digit outward mpmath.iv arithmetic',
                W_min=Wmin, W_range='W >= W_min', Z0_range='Z0 >= 0; fixed',
                x_range=['-0.01','0.01'], y_range=['-0.0002','0.0002'],
                theta_upper=interval_ends(theta_max), Fx=interval_ends(v['Fx']),
                Fy=interval_ends(v['Fy']), Ward_determinant=interval_ends(v['ward_det']),
                self_consistent_Gx_lower=interval_ends(Gx_lower),
                left_trace=interval_ends(minus),right_trace=interval_ends(plus),
                implication='For every stated W,Z0 and every y in the interval, exactly one x in (-.01,.01) solves the self-consistent trace equation.')


def exact_native_and_roots():
    x,y=sp.symbols('x y',real=True)
    p=(sp.sqrt(5)-1)/2
    E=p*p*(1+x); L=4*E*(1-E); b=p-p*p*y
    B=4*b*b*(1-b*b); A=L+(1-L)*B
    require('positive A factorization is the same original polynomial',
            sp.expand(A-(1-(1-L)*(1-B)))==0)
    require('original geometric/matter signs at origin',
            sp.simplify(sp.diff(A,y).subs({x:0,y:0})/sp.diff(A,x).subs({x:0,y:0})+2*p)==0)
    require('original B slope ratio',
            sp.simplify(sp.diff(B,y).subs({x:0,y:0})/sp.diff(A,x).subs({x:0,y:0})+2*p**-5)==0)
    v=jets(mp,mp.mpf(0),mp.mpf(0))
    lam=v['Fy']/v['Fx']
    near('unchanged original finite-fugacity ratio', lam,
         mp.mpf('-23.416406751884074972895582'),mp.mpf('1e-23'))
    rows=[]
    for LL in (8,16,32,64):
        W=528*LL**4
        for yy in ('-0.0001','0','0.0001'):
            yy=mp.mpf(yy)
            xx=mp.findroot(lambda xx:complete(mp,xx,yy,W)['T'],
                           (-24*yy-mp.mpf('.001'),-24*yy+mp.mpf('.001')))
            r=complete(mp,xx,yy,W)
            near('full self-consistent trace root diagnostic', r['T'],0)
            require('root lies inside certified rectangle', abs(xx)<mp.mpf('.01'))
            near('thermal stationarity', 1/r['theta'],r['Z']/2)
            near('original trace ratio at the root', xx,yy*r['Fy']/r['Fx'])
            rows.append(dict(L=LL,y=mp.nstr(yy,12),x=mp.nstr(xx,27),
                             lambda_sector=mp.nstr(r['Fy']/r['Fx'],27),
                             theta=mp.nstr(r['theta'],22)))
    return dict(j_x_origin=mp.nstr(v['Fx'],32),lambda_feedback=mp.nstr(lam,32),
                roots=rows,root_precision='80-digit numerical locations; existence and uniqueness are supplied by the separate interval monotonicity certificate, not by findroot')


def auxiliary_schur():
    beta=jets(mp,0,0)['beta']
    mult=[528*1000,528*2000,528*3000]
    Z0=mp.mpf(7*sum(mult))
    v0=list(map(mp.mpf,['.001','-.00002','-.002','.00003','.003','-.00001']))
    def data(v):
        js=[jets(mp,v[2*k],v[2*k+1]) for k in range(3)]
        Z=Z0+2*sum(m*d['t'] for m,d in zip(mult,js))
        J=sum(m*d['j'] for m,d in zip(mult,js))
        return Z,J
    def price(*v):
        Z,J=data(v)
        return mp.log(Z)/beta+J
    Z,J=data(v0); theta=2/Z
    def lag(v,th):
        ZZ,JJ=data(v)
        return JJ+(th*ZZ/2-mp.log(th/2)-1)/beta
    near('complete nonlocal scalar value equals exact scalar envelope',lag(v0,theta),price(*v0))
    near('one scalar auxiliary equation solved',mp.diff(lambda th:lag(v0,th),theta),0)
    require('scalar auxiliary is a strict minimum at fixed fields',
            mp.diff(lambda th:lag(v0,th),theta,2)>0)
    dZ=[]; graderr=[]; hesserr=[]; neglected=[]
    for k in range(6):
        orders=[0]*6;orders[k]=1
        dZ.append(mp.diff(lambda *v:data(v)[0],tuple(v0),tuple(orders)))
        graderr.append(abs(mp.diff(price,tuple(v0),tuple(orders))-
                           mp.diff(lambda *v:lag(v,theta),tuple(v0),tuple(orders))))
    for k in range(6):
        for l in range(6):
            orders=[0]*6;orders[k]+=1;orders[l]+=1
            raw=mp.diff(lambda *v:lag(v,theta),tuple(v0),tuple(orders))
            corr=dZ[k]*dZ[l]/(beta*Z*Z)
            actual=mp.diff(price,tuple(v0),tuple(orders))
            hesserr.append(abs(actual-(raw-corr)))
            neglected.append(abs(actual-raw))
    require('whole six-operand source survives scalar elimination',max(graderr)<mp.mpf('1e-60'))
    require('all 36 Hessian entries obey the full Schur formula',max(hesserr)<mp.mpf('1e-60'))
    require('negative control: freezing theta loses a genuine second source',max(neglected)>mp.mpf('1e-9'))
    return dict(max_gradient_error=mp.nstr(max(graderr),12),max_hessian_error=mp.nstr(max(hesserr),12),
                omitted_Schur_max=mp.nstr(max(neglected),16),
                scope='Six independent original scalar operands at three sites, not a fabricated all42 lattice checker; the identity pulls back through any specified smooth field map.')


def pinned_geometry_normalization():
    path=ROOT/'inputs/check_all40_arbitrary_brinkmann.py'
    raw=path.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require('unaltered upstream all40 original checker blob',blob=='e502807955321465903d7ab1a248e0456ac69f60')
    spec=importlib.util.spec_from_file_location('original_all40',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    eta=mod.eta
    frames=[sp.eye(4),sp.Matrix([[1,sp.Rational(1,5),0,0],[sp.Rational(1,7),1,0,0],
                              [0,sp.Rational(1,9),sp.Rational(3,2),0],[sp.Rational(1,11),0,0,sp.Rational(4,3)]])]
    total=0
    for E in frames:
        require('orientation-positive actual normalization fixture',E.det()>0)
        Ei=E.inv()
        for r,t in mod.pairs:
            u,v=[i for i in range(4) if i not in (r,t)]
            for a,b in mod.pairs:
                X=sp.zeros(4);X[a,b]=1;X[b,a]=-1;X=X*eta
                native=sp.LeviCivita(r,t,u,v)*mod.pair(E,u,v,X)
                C=X*eta
                scalar=sum((Ei[r,i]*Ei[t,j]-Ei[t,i]*Ei[r,j])*C[i,j]
                           for i in range(4) for j in range(4))
                require('literal finite EPS_PLUS pair fixes +one-half EH density',
                        sp.simplify(native-E.det()*scalar/2)==0)
                total+=1
    return dict(upstream_blob=blob,exact_rational_contraction_cases=total,
                continuum_normalization='f_B = (1/2) vol_g R / mu0; fixed EPS_PLUS orientation, not canonical negative G2STAR')


def true_scene_heat():
    sizes=[9,11,13]; degrees=[24,22,20]
    rw=sp.eye(3)
    for i in range(3):
        for j in range(3):
            if i!=j:rw[i,j]=-sp.Rational(sizes[j],degrees[i])
    l=sp.Symbol('l')
    expected=l*(160*l*l-480*l+359)/160
    require('exact literal K913 part-constant spectrum',sp.expand(rw.charpoly(l).as_expr()-expected)==0)
    groups=np.repeat(np.arange(3),sizes)
    A=(groups[:,None]!=groups[None,:]).astype(float)
    D=A.sum(axis=1); R=np.diag(D**-.5)
    L=np.eye(33)-R@A@R
    beta=float(jets(mp,0,0)['beta'])
    ev=np.linalg.eigvalsh(L)
    spectrum=np.array([0]+[1]*30+[1.5-np.sqrt(10)/40,1.5+np.sqrt(10)/40])
    require('all 33 scene modes retained',np.max(np.abs(np.sort(ev)-np.sort(spectrum)))<3e-15)
    exactZ=1+30*np.exp(-beta)+2*np.exp(-1.5*beta)*np.cosh(beta*np.sqrt(10)/40)
    heat=np.log(exactZ)/beta
    require('complete scene heat including zero mode',abs(np.trace(expm(-beta*L))-exactZ)<2e-13)
    # Genuine single existing graph edge perturbation: no replacement Hodge.
    P=np.zeros_like(A);P[0,9]=P[9,0]=1
    dD=P.sum(axis=1); Rp=np.diag(-.5*D**-1.5*dD)
    Rpp=np.diag(.75*D**-2.5*dD*dD)
    Lp=-(Rp@A@R+R@P@R+R@A@Rp)
    Lpp=-(Rpp@A@R+R@A@Rpp+2*Rp@P@R+2*R@P@Rp+2*Rp@A@Rp)
    EE=expm(-beta*L);Z=np.trace(EE)
    dEE=expm_frechet(-beta*L,-beta*Lp,compute_expm=False)
    Zp=np.trace(dEE)
    first=-np.trace(EE@Lp)/Z
    second=-np.trace(dEE@Lp+EE@Lpp)/Z+np.trace(EE@Lp)*Zp/Z**2
    def H(t):
        AA=A+t*P; DD=AA.sum(axis=1)
        RR=np.diag(DD**-.5);LL=np.eye(33)-RR@AA@RR
        return np.log(np.trace(expm(-beta*LL)))/beta
    eps=1e-3
    fd=(H(eps)-H(-eps))/(2*eps)
    fd2=(H(eps)-2*H(0)+H(-eps))/eps**2
    require('moving scene heat is not silently frozen',abs(first)>1e-9)
    require('native normalized scene source vs independent difference',abs(fd-first)<1e-10)
    require('native normalized scene Hessian vs independent difference',abs(fd2-second)<1e-8)
    require('dimension-free first source bound for actual scene',abs(first)<=np.linalg.norm(Lp,2)+1e-14)
    require('dimension-free second source bound for actual scene',
            abs(second)<=np.linalg.norm(Lpp,2)+2*beta*np.linalg.norm(Lp,2)**2+1e-14)
    # A moving orthogonal frame is a coordinate change, not an edge change.
    X=np.zeros_like(L);X[0,12]=1;X[12,0]=-1
    comm=X@L-L@X
    require('actual pure-frame heat source vanishes by trace commutator',abs(np.trace(EE@comm)/Z)<1e-14)
    return dict(exact_spectrum='0 (1), 1 (30), 3/2-sqrt(10)/40 (1), 3/2+sqrt(10)/40 (1)',
                Z=repr(float(Z)),heat=repr(float(heat)),
                existing_edge_first_source=repr(float(first)),existing_edge_second_source=repr(float(second)),
                edge_source_fd_error=repr(float(abs(fd-first))),edge_second_fd_error=repr(float(abs(fd2-second))),
                first_operator_bound=repr(float(np.linalg.norm(Lp,2))),second_operator_bound=repr(float(np.linalg.norm(Lpp,2)+2*beta*np.linalg.norm(Lp,2)**2)),
                qualification='Fixed scene and coordinate-conjugate scene have zero field source. An independently varying real edge is a different admitted-domain question and the source is explicitly nonzero.')


def noncommuting_heat():
    beta=mp.mpf('0.7')
    DD=mp.diag([mp.mpf('.2'),mp.mpf('.8'),mp.mpf('1.4')])
    A=mp.matrix([[mp.mpf('.1'),mp.mpf('.2'),0],[mp.mpf('.2'),mp.mpf('-.1'),mp.mpf('.15')],[0,mp.mpf('.15'),mp.mpf('.05')]])
    B=mp.matrix([[mp.mpf('.2'),0,mp.mpf('.11')],[0,mp.mpf('.1'),mp.mpf('-.08')],[mp.mpf('.11'),mp.mpf('-.08'),mp.mpf('-.07')]])
    C=mp.matrix([[mp.mpf('.03'),mp.mpf('.04'),0],[mp.mpf('.04'),0,0],[0,0,mp.mpf('-.02')]])
    tr=lambda M:sum(M[k,k] for k in range(3))
    def H(t,s):return mp.log(tr(mp.expm(-beta*(DD+t*A+s*B+t*s*C))))/beta
    weights=[mp.exp(-beta*DD[i,i]) for i in range(3)];Z=sum(weights)
    meanA=sum(weights[i]*A[i,i] for i in range(3))/Z
    meanB=sum(weights[i]*B[i,i] for i in range(3))/Z
    bkm=mp.mpf(0)
    for i in range(3):
        for j in range(3):
            logmean=weights[i] if i==j else (weights[i]-weights[j])/(mp.log(weights[i])-mp.log(weights[j]))
            bkm+=logmean*A[i,j]*B[j,i]/Z
    analytic=-sum(weights[i]*C[i,i] for i in range(3))/Z+beta*(bkm-meanA*meanB)
    actual=mp.diff(H,(0,0),(1,1))
    near('noncommuting heat first source',mp.diff(lambda t:H(t,0),0),-meanA)
    near('noncommuting heat mixed Hessian via BKM',actual,analytic)
    diag_only=-sum(weights[i]*C[i,i] for i in range(3))/Z+beta*(sum(weights[i]*A[i,i]*B[i,i] for i in range(3))/Z-meanA*meanB)
    require('negative control: a commuting-only Hessian is false',abs(actual-diag_only)>mp.mpf('1e-5'))
    # Direct sum and tensor-sum inventories are different, no free padding.
    near('direct-sum repeats do not multiply heat field source',mp.diff(lambda t:mp.log(5*tr(mp.expm(-beta*(DD+t*A))))/beta,0),-meanA)
    near('tensor-sum heat repeats multiply the source',mp.diff(lambda t:5*H(t,0),0),-5*meanA)
    return dict(noncommuting_hessian_error=mp.nstr(abs(actual-analytic),12),
                erroneous_commuting_hessian_difference=mp.nstr(actual-diag_only,20),
                first_source=mp.nstr(-meanA,20))


def weak_signal_test():
    # Original operands remain independent, off the null sheet and with PF jumps.
    # This is a source convergence diagnostic, not a lattice-root existence test.
    rho=list(map(mp.mpf,['.5','1','1.5']))
    f=list(map(mp.mpf,['.10','-.06','.03']))
    q=list(map(mp.mpf,['-.02','.01','.015']))
    v=jets(mp,0,0);a=v['Fx']; lam=v['Fy']/a
    rows=[]
    for L in [8,16,32,64]:
        tau=mp.mpf(1)/(L*L)
        js=[jets(mp,tau*ff/rr,tau*qq/rr) for ff,qq,rr in zip(f,q,rho)]
        value=sum(rr*(jj['j']-v['j']) for rr,jj in zip(rho,js))/(3*tau*a)
        target=sum(ff+lam*qq for ff,qq in zip(f,q))/3
        errgrad=max(abs(jj[k]/a-t) for jj in js for k,t in [('Fx',1),('Fy',lam)])
        errhess=max(abs(tau*jj[k]/(rr*a)) for jj,rr in zip(js,rho) for k in ['Fxx','Fxy','Fyy'])
        rows.append(dict(L=L,value_error=mp.nstr(abs(value-target),14),
                         normalized_gradient_error=mp.nstr(errgrad,14),
                         normalized_second_source=mp.nstr(errhess,14)))
    require('off-null weak-signal source error decreases at expected order',
            mp.mpf(rows[0]['normalized_gradient_error'])/mp.mpf(rows[1]['normalized_gradient_error'])>3.9)
    require('off-null second-source correction decreases at expected order',
            mp.mpf(rows[0]['normalized_second_source'])/mp.mpf(rows[1]['normalized_second_source'])>3.9)
    return dict(rows=rows,qualification='Illustrates the analytic C2 Taylor bound with fixed positive PF jumps; no generic strong all-grid Euler convergence or arbitrary-root compactness inferred.')


def main():
    result=dict(status='PASS_SCOPED_GLOBAL_SPECTRAL_EQUATION_COMPOSITION',
                source_commit_read='a82df288e4832d53fd52fc88a78ef2dc123bcc88')
    result['independent_scalar_jets']=independent_scalar_jets()
    result['interval_certificate']=interval_certificate()
    result['original_source_and_sectors']=exact_native_and_roots()
    result['global_thermal_auxiliary']=auxiliary_schur()
    result['exact_geometric_normalization']=pinned_geometry_normalization()
    result['literal_scene_heat']=true_scene_heat()
    result['noncommuting_heat']=noncommuting_heat()
    result['off_null_C2_diagnostic']=weak_signal_test()
    result['checks']=len(CHECKS)
    result['physical_scope']=dict(actual_scene_equals_paired_Hodge=False,
                                  forced_full_native_execution=False,independent_apparatus_Euler_solved=False,
                                  universal_finite_root_recovery=False,GR_closed=False)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
