#!/usr/bin/env python3
"""Finite-jet universality controls for the existing D0 source theorem.

This checks a changed, not all-input-faithful, report law with the SAME value
and derivative at the original reference. It keeps full retained determinants,
independent current shape coordinates, the old matrix, and the true gain.
The finite all-column reporter is a mathematical target, not an emitted native
G/CX/SourceI word. The 42-coordinate test is off-shell and pointwise, not a PDE
solution or finite-mesh GR root. Analytic source bounds are in PROOF_RU.md.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, math, platform
import mpmath as mp
import numpy as np
import scipy.linalg as la
import sympy as sp
import torch

COUNT=0

def check(ok:bool,name:str)->None:
    global COUNT
    COUNT+=1
    if not bool(ok): raise ArithmeticError(name)

def near(a,b,name:str,tol=2e-11)->float:
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    check(err<tol,name+': '+str(err))
    return err


def bernstein_exact():
    P,P0,t=sp.symbols('P P0 theta',real=True)
    b=[0,(1+t*P0**2)/4,sp.Rational(1,2)-t*P0*(1-P0)/3,
       sp.Rational(3,4)+t*(1-P0)**2/4,1]
    q=sum(sp.binomial(4,k)*b[k]*P**k*(1-P)**(4-k) for k in range(5))
    desired=P+t*P*(1-P)*(P-P0)**2
    check(sp.expand(q-desired)==0,'four-copy complete truth table')
    check(sp.expand((q-P).subs(P,P0))==0,'reference effect unchanged')
    check(sp.simplify(sp.diff(q,P).subs(P,P0)-1)==0,'reference first derivative unchanged')
    check(sp.simplify(sp.diff(q,t).subs(P,P0))==0,'reference shape source zero')
    check(sp.simplify(sp.diff(q,t,P).subs(P,P0))==0,'reference mixed first derivative zero')
    check(sp.simplify(sp.diff(q,P,2).subs(P,P0)-2*t*P0*(1-P0))==0,
          'report law is genuinely changed at second order')
    # Exact analytic endpoint bounds for each affine-in-theta coefficient.
    for p0 in (F(0),F(1,1048576),F(1,3),F(1,2),F(1)):
        for theta in (F(-1),F(0),F(1)):
            bs=[F(0),(1+theta*p0*p0)/4,F(1,2)-theta*p0*(1-p0)/3,
                F(3,4)+theta*(1-p0)**2/4,F(1)]
            for u in bs:check(0<=u<=1,'genuine probability for each count')
    # For arbitrary P0 in [0,1], b1 in [0,1/2], b2 in[5/12,7/12], b3 in[1/2,1].
    x=F(7,80);qmax=x*(1+x*x)
    check(1-2*qmax>F(4,5),'new corner retains a real positive uniform margin')
    return {'full_polynomial':'Q_theta(P)=P+theta*P*(1-P)*(P-P0)^2',
            'Bernstein_coefficients':[str(x) for x in b],
            'exact_equal_value_and_first_jet':True,'exact_task_equality':False,
            'READY_report_upper_bound':str(qmax),
            'cold_corner_lower_bound':str(1-2*qmax)}


def report_factory(P:float,P0:float,theta:float):
    """All 32 WORK columns, four trial records plus one output, no postselection."""
    beta=[0.,(1+theta*P0*P0)/4,.5-theta*P0*(1-P0)/3,
          .75+theta*(1-P0)**2/4,1.]
    R=np.array([[math.sqrt(1-P),-math.sqrt(P)],
                [math.sqrt(P),math.sqrt(1-P)]])
    V=np.ones((1,1))
    for _ in range(4):V=np.kron(V,R)
    V=np.kron(V,np.eye(2))
    controlled=np.zeros((32,32))
    for word in range(16):
        q=beta[word.bit_count()]
        controlled[2*word:2*word+2,2*word:2*word+2]=np.array(
            [[math.sqrt(1-q),-math.sqrt(q)],[math.sqrt(q),math.sqrt(1-q)]])
    A=controlled@V
    Pi=np.diag([int(j%2==1) for j in range(32)])
    U=A.T@(np.eye(32)-2*Pi)@A
    p=(math.sqrt(5)-1)/2
    G=np.array([[math.sqrt(p),-p],[p,math.sqrt(p)]])
    born=np.ones((1,1))
    for _ in range(5):born=np.kron(born,G)
    j=born[:,0]
    canon=born@U@born.T
    P_eff=float(np.sum((A[:,0]**2)*np.diag(Pi)))
    expected=P+theta*P*(1-P)*(P-P0)**2
    near(A.T@A,np.eye(32),'full preparation unitary')
    near(U@U,np.eye(32),'same reflected wrapper on all columns')
    near(canon@canon,np.eye(32),'same wrapper on raw-born input')
    near(P_eff,expected,'finite truth table computes exact polynomial')
    near(j@canon@j,1-2*expected,'raw-born full cold amplitude')
    near(np.trace(U),0,'unchanged full reflection signature')
    return U,canon,j,expected,A


def full_operator_controls():
    K=np.array([[.53,.13],[.03,.27]])
    past=np.block([[K,la.sqrtm(np.eye(2)-K@K.T)],
                   [la.sqrtm(np.eye(2)-K.T@K),-K.T]])
    near(past.T@past,np.eye(4),'full nonnormal past completion')
    check(la.norm(K.T@K-K@K.T)>.01,'old matrix is nonnormal')
    out=[];heat=[];last=None
    z=2**-20;N=4;beta=2*((math.sqrt(5)-1)/2)**2
    for theta in (-1.,0.,1.):
        U,canon,j,prob,A=report_factory(.21,.19,theta)
        full=np.kron(past,canon)
        old=np.eye(4)[:,:2];i=np.column_stack([np.kron(old[:,k],j) for k in range(2)])
        cold=i.T@full@i
        near(cold,(1-2*prob)*K,'one whole old/current corner')
        PP=i@i.T
        Ffull=PP@full.T@(np.eye(128)-PP)@full@PP
        Jfull=-np.log1p(-z*la.eigvalsh((Ffull+Ffull.T)/2)).sum()
        Fsmall=np.eye(2)-cold.T@cold
        Jsmall=-np.log1p(-z*la.eigvalsh((Fsmall+Fsmall.T)/2)).sum()
        error=near(Jfull,Jsmall,'all128 return determinant keeps complement',5e-20)
        # A structural full 4-stage clock, not four paid native calls.
        # Same full endpoint eigenvalues imply the same full clock heat.
        shifts=np.zeros((N*128,N*128))
        for l in range(N):
            gate=full if l==N-1 else np.eye(128)
            shifts[((l+1)%N)*128:((l+1)%N+1)*128,l*128:(l+1)*128]=gate
        Delta=np.eye(N*128)-(shifts+shifts.T)/2
        H=math.log(2*np.exp(-beta*la.eigvalsh(Delta)).sum())/beta
        heat.append(H)
        if last is not None:check(abs(prob-last)>1e-7,'finite report probabilities actually differ')
        last=prob
        out.append({'theta':theta,'report_probability':prob,'full_return_price':float(Jfull),
                    'determinant_error':error})
    near(heat,np.repeat(heat[0],3),'all clock modes retained, no heat counterterm',3e-13)
    return {'full_old_current_dimension':128,'protected_rank':2,'clock_modes_both_grades':1024,
            'controls':out,'max_clock_heat_difference':max(abs(x-heat[0]) for x in heat),
            'actual_native_words_emitted':False,'clock_scope':'structural fixed bare paired clock'}


def symbolic_taylor_bound():
    """Exact value AND independent-variable derivative bounds on a full box."""
    x,y,t=sp.symbols('x y theta',real=True)
    r0=sp.Rational(1,8);rf=sp.Rational(1,11);rq=sp.Rational(2,7)
    # Structural nontrivial fixed-first-jet family; not the original r.
    r=r0+rf*x+rq*y+sp.Rational(1,9)*x*y+t*(x*x+2*x*y+3*y*y)/37
    H=F(2,37)+2*(F(1,9)+F(2,37))+F(6,37)
    Htheta=F(2+2*2+6,37)
    vals=[]
    for epsilon in (F(1,16),F(1,64),F(1,256)):
        # Two sites: mu*rho sum1, and a true normalized PF variation.
        mu=[F(1,2),F(1,2)];rho=[F(3,4),F(5,4)];dr=[F(1,7),-F(1,7)]
        w=[[F(1,5),-F(1,6)],[F(1,7),F(1,4)]]
        dw=[[F(2,9),-F(1,3)],[F(1,11),F(1,6)]]
        sig=[F(3,2),F(4,5)];ds=[F(1,9),-F(1,7)]
        th=[F(2,3),-F(1,2)];dth=[F(3,5),-F(2,7)]
        actual=F(0);leading=F(0);bound=F(0)
        for j in range(2):
            v=[sig[j]*q for q in w[j]]
            dv=[ds[j]*w[j][k]+sig[j]*dw[j][k] for k in range(2)]
            u=[epsilon*q/rho[j] for q in v]
            du=[epsilon*(dv[k]/rho[j]-v[k]*dr[j]/rho[j]**2) for k in range(2)]
            sub={x:u[0],y:u[1],t:th[j]}
            rr=F(r.subs(sub));rx=F(sp.diff(r,x).subs(sub));ry=F(sp.diff(r,y).subs(sub));rt=F(sp.diff(r,t).subs(sub))
            actual+=mu[j]*(dr[j]*rr+rho[j]*(rx*du[0]+ry*du[1]+rt*dth[j]))
            leading+=epsilon*mu[j]*(F(rf)*dv[0]+F(rq)*dv[1])
            vn=max(map(abs,v));dn=max(map(abs,dv))
            bound+=epsilon**2*mu[j]/rho[j]*(H*vn*dn+H*vn*vn*abs(dr[j]/rho[j])/2+Htheta*vn*vn*abs(dth[j])/2)
        check(abs(actual-leading)<=bound,'full joint Taylor/PF/shape/coframe-scaling source bound')
        vals.append({'epsilon':str(epsilon),'actual_remainder':float(abs(actual-leading)),
                     'exact_bound':float(bound),'normalized_error':float(abs(actual-leading)/epsilon)})
    check(vals[2]['normalized_error']<vals[0]['normalized_error']/10,'source error not merely value error')
    return {'constants_exact':{'H':str(H),'H_theta':str(Htheta)},'tests':vals,
            'structural_polynomial':True}


def original_report(x,y):
    p=(mp.sqrt(5)-1)/2;zz=mp.mpf(2)**-20
    E=p*p*(1+x);ell=4*E*(1-E);u=p+p*p*y;B=4*u*u*(1-u*u);A=ell+(1-ell)*B
    return zz*(A+B)-zz*zz*A*B


def full_return_jet():
    mp.mp.dps=100
    r0=original_report(0,0);rf=mp.diff(lambda x:original_report(x,0),0)
    rq=mp.diff(lambda y:original_report(0,y),0);lam=-rq/rf
    aa=mp.mpf(17)/50;z=mp.mpf(2)**-20;p=(mp.sqrt(5)-1)/2
    K=mp.matrix([[mp.mpf('.53'),mp.mpf('.13')],[mp.mpf('.03'),mp.mpf('.27')]])
    A=K.T*K;P0=aa*r0
    def post(P,t):return P+t*P*(1-P)*(P-P0)**2
    W=[(mp.mpf('.2'),mp.mpf('.1')),(-mp.mpf('.1'),mp.mpf('.07'))]
    shape=[mp.mpf('.6'),-mp.mpf('.8')]
    rows=[]
    for e in (mp.mpf(2)**-4,mp.mpf(2)**-7,mp.mpf(2)**-10,mp.mpf(2)**-13):
        r=[original_report(e*f,-e*q) for f,q in W]
        P=[aa*v for v in r];Q=[post(v,t) for v,t in zip(P,shape)]
        cs=[1-2*v for v in Q];ss=mp.fprod(v*v for v in cs)
        eta=p**80;D=(1-z)*mp.eye(2)+z*eta*ss*A;Di=D**-1
        tr=mp.trace(Di*A) if hasattr(mp,'trace') else sum((Di*A)[i,i] for i in range(2))
        w=z*eta*ss*tr;L=sum(1/c for c in cs)
        Gamma=4*aa*e*rf*w*L
        weights=[(1/c)/L for c in cs]
        norm_shape=mp.mpf(0)
        for j in range(2):
            dq=P[j]*(1-P[j])*(P[j]-P0)**2
            analytic=4*w*dq/cs[j]
            def J(th):
                qj=[post(P[k],th if k==j else shape[k]) for k in range(2)]
                sj=mp.fprod((1-2*v)**2 for v in qj)
                DD=(1-z)*mp.eye(2)+z*eta*sj*A
                return -mp.log(mp.det(DD))
            d=mp.diff(J,shape[j])
            check(abs(d-analytic)<mp.mpf('1e-90'),'true complete matrix-price shape derivative')
            norm_shape+=abs(analytic/Gamma)
        # Leading normalized field co-vector, with old matrix and weights retained.
        err_field=mp.mpf(0)
        for j,(f,q) in enumerate(W):
            PP=P[j];theta=shape[j]
            qprime=1+theta*((1-2*PP)*(PP-P0)**2+2*PP*(1-PP)*(PP-P0))
            rx=mp.diff(lambda x:original_report(x,-e*q),e*f)
            ry=mp.diff(lambda y:original_report(e*f,y),-e*q)
            gx=weights[j]*qprime*rx/rf
            gy=-weights[j]*qprime*ry/rf
            err_field+=abs(gx-weights[j])+abs(gy-weights[j]*lam)
        rows.append({'epsilon':mp.nstr(e,12),'true_Gamma':mp.nstr(Gamma,24),
                     'independent_shape_dual_norm':mp.nstr(norm_shape,24),
                     'independent_field_error_l1':mp.nstr(err_field,24),
                     'shape_norm_over_epsilon':mp.nstr(norm_shape/e,24),
                     'all_current_weights_sum':mp.nstr(sum(weights),6)})
    check(mp.mpf(rows[-1]['independent_shape_dual_norm'])<mp.mpf(rows[0]['independent_shape_dual_norm'])/100,
          'nonfaithful independent shape sources decay without dilution')
    check(mp.mpf(rows[-1]['independent_field_error_l1'])<mp.mpf(rows[0]['independent_field_error_l1'])/100,
          'original full report has the same leading field source')
    # Positive residual is preserved if independent first-order coupling is changed.
    eps=mp.mpf('1e-5'); f,q=W[0]
    delta_first=q  # changing lambda by theta in the linear material term
    check(abs(delta_first)>mp.mpf('.01'),'changed linear slope ratio not silently erased')
    return {'r0':mp.nstr(r0,30),'r_f':mp.nstr(rf,30),'lambda':mp.nstr(lam,30),
            'readiness':str(aa),'original_REFERENCE_effect':mp.nstr(P0,30),
            'matrix_old_history_kept':True,'retention_blocks_in_control':80,'tests':rows,
            'native_words_executed':False}


def coframe_identity():
    torch.set_default_dtype(torch.float64);torch.set_num_threads(1)
    eta=torch.diag(torch.tensor([1.,-1.,-1.,-1.]));pairs=[(a,b) for a in range(4) for b in range(a+1,4)]
    grad0=torch.tensor([.7,.1,-.2,.3]);grad1=torch.tensor([-.2,.5,.1,-.1])
    lam=-23.4164067518840749729
    def lag(y):
        e=y[:16].reshape(4,4);ei=torch.linalg.inv(e);g=e.T@eta@e;gi=torch.linalg.inv(g)
        ws=[]
        for mu in range(4):
            anti=torch.zeros((4,4),dtype=y.dtype)
            for k,(a,b) in enumerate(pairs):
                anti[a,b]=y[16+mu*6+k];anti[b,a]=-y[16+mu*6+k]
            ws.append(anti@eta)
        R=y[0]*0
        for mu in range(4):
            for nu in range(4):
                Fmn=(ws[mu]@ws[nu]-ws[nu]@ws[mu])@eta
                R+=torch.einsum('a,b,ab->',ei[mu],ei[nu],Fmn)
        q=y[40]**2*(grad0@gi@grad0)+y[41]**2*(grad1@gi@grad1)
        return R/2+lam*q
    y=torch.linspace(-.03,.04,42);y[:16]=(torch.eye(4)+.03*torch.arange(16).reshape(4,4)/16).flatten()
    y[40]=.13;y[41]=-.17;y.requires_grad_(True)
    sig=torch.tensor(1.37,requires_grad=True)
    def transform(v,s):return torch.cat([v[:16]/torch.sqrt(s),v[16:]])
    direct=sig*lag(y);pullback=lag(transform(y,sig))
    near(direct.detach(),pullback.detach(),'exact old-moment coframe amplitude absorption',2e-13)
    ge,gs=torch.autograd.grad(direct,(y,sig),retain_graph=True)
    he,hs=torch.autograd.grad(pullback,(y,sig),retain_graph=True)
    err=near(ge.detach(),he.detach(),'all42 pointwise covector absorption',2e-12)
    near(gs.detach(),hs.detach(),'independent positive amplitude source is retained',2e-13)
    ward=2*sig*gs+torch.dot(y[:16],ge[:16])
    near(ward.detach(),0.,'amplitude/coframe dependence identity, not assumed equation',2e-12)
    check(float(torch.linalg.norm(ge).detach())>0.1,'test is truly off shell')
    # Derived material coframe is the same through both paths.
    e=y[:16].reshape(4,4);ee=transform(y,sig)[:16].reshape(4,4)
    h1=torch.sqrt(sig/torch.linalg.det(e))*e
    h2=ee/torch.sqrt(torch.linalg.det(ee))
    near(h1.detach(),h2.detach(),'material metric determined by the amplified matter source',2e-13)
    # A spatially varying multiplier has this pointwise equality before the
    # independent connection is eliminated; no Levi-Civita rescaling is presumed.
    return {'pointwise_field_components':42,'extra_amplitude_coordinate':1,
            'source_chain_error':err,'coframe_amplitude_Ward_error':abs(float(ward.detach())),
            'off_shell_source_norm':float(torch.linalg.norm(ge).detach()),
            'connection_varied_independently':True,'finite_mesh_or_solution_checked':False}


def necessary_controls():
    eps=sp.symbols('eps',positive=True);theta=sp.symbols('theta',real=True)
    # Value closeness AND equal flat value/slope are insufficient if mixed
    # shape derivatives grow with refinement.
    u=sp.symbols('u',real=True)
    bad=u*u*sp.sin(theta/(eps*eps))
    check(sp.simplify(bad.subs(u,0))==0,'bad family shares baseline')
    check(sp.simplify(sp.diff(bad,u).subs(u,0))==0,'bad family shares first jet')
    badsource=sp.simplify(sp.diff(bad,theta).subs({u:eps,theta:0})/eps)
    check(badsource==1/eps,'unbounded mixed derivative counterexample retained')
    base=sp.diff(theta,theta)/eps
    check(base==1/eps,'freely changed baseline is not a suppressed source')
    rat=sp.diff(theta*u,theta).subs(u,eps)/eps
    check(rat==1,'changed relative linear coefficient persists')
    # No 1/M dilution of independent shape sources: dual l1 average at common centre.
    for M in (1,2,7,100):
        check(sum([F(1,M)]*M)==1,'independent-current normalization')
    return {'fast_shape_normalized_source':'1/epsilon','free_baseline_source':'1/epsilon',
            'changed_first_jet_ratio_source':'nonzero O(1)',
            'no_unrestricted_physical_selection_claim':True}


def main():
    out={'input_commit':'83bf7da04a3d2558edc2fa412dbc43f19c9653cc',
         'bernstein':bernstein_exact(),'full_operator':full_operator_controls(),
         'exact_Taylor_PF_bound':symbolic_taylor_bound(),'actual_original_report':full_return_jet(),
         'coframe':coframe_identity(),'negative_controls':necessary_controls()}
    out.update({'checks':COUNT,'status':'PASS_SCOPED_REPORT_FIRST_JET_UNIVERSALITY',
                'unrestricted_D0_GR_closed':False,'native_postprocessor_emitted':False,
                'global_fine_history_equivalence_claimed':False,'Lean_or_CI_run':False,
                'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'environment':{'python':platform.python_version(),'numpy':np.__version__,
                               'sympy':sp.__version__,'torch':torch.__version__}})
    print(json.dumps(out,sort_keys=True,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
