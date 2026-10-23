#!/usr/bin/env python3
"""Literal normalized K(9,11,13) heat/feedback and conditional source descent.

Every original edge and all 718 oriented histories are retained. This is
an independent reconstruction from the published scene formulas, NOT an
import/replay of the native full128 or original all42 field constructor.
No claim of a common physical writer, internal stationary section, or GR.
Requires numpy, scipy, mpmath. Writes nothing: JSON goes to stdout.
"""
from __future__ import annotations
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.linalg import expm_frechet
from mpmath import mp

P = (np.sqrt(5.0)-1.0)/2.0
BETA = 2*P*P
ZETA = 2.0**-20
ZONES = np.repeat(np.arange(3), [9,11,13])
EDGES = [(i,j) for i in range(33) for j in range(i+1,33)
         if ZONES[i] != ZONES[j]]
CHECKS: list[str] = []

def require(label: str, condition: bool) -> None:
    if not bool(condition):
        raise ArithmeticError(label)
    CHECKS.append(label)

def close(label: str, x, y, tol: float) -> None:
    error = float(np.max(np.abs(np.asarray(x)-np.asarray(y))))
    require(label + f' (error={error:.3g})', error < tol)

def adjacency(w: np.ndarray) -> np.ndarray:
    out = np.zeros((33,33))
    for k,(i,j) in enumerate(EDGES):
        out[i,j] = out[j,i] = w[k]
    return out

def scene(w: np.ndarray, alpha=None, gamma=None):
    """Analytic log-weight 0/1/2 jet: w(t)=w exp(t alpha+t^2 gamma/2)."""
    if np.any(w <= 0) or w.shape != (359,):
        raise ValueError('359 strictly positive scene conductances required')
    A = adjacency(w)
    d = A.sum(axis=1)
    root = 1/np.sqrt(d)
    norm = root[:,None]*root[None,:]
    T = norm*A
    L = np.eye(33)-T
    if alpha is None:
        return T,L
    if gamma is None:
        gamma = np.zeros(359)
    A1 = adjacency(w*alpha)
    A2 = adjacency(w*(alpha*alpha+gamma))
    R = A1.sum(axis=1)/d
    Q = A2.sum(axis=1)/d
    S1 = norm*A1
    G1 = -R/2
    G2 = 3*R*R/4-Q/2
    T1 = S1+(G1[:,None]+G1[None,:])*T
    T2 = norm*A2 + 2*(G1[:,None]+G1[None,:])*S1
    T2 += (G2[:,None]+G2[None,:]+2*G1[:,None]*G1[None,:])*T
    return T,L,T1,-T1,T2,-T2

def price(T):
    eig = np.linalg.eigvalsh(T)
    heat_weights = np.exp(-BETA*(1-eig))
    Z = float(heat_weights.sum())
    H = np.log(Z)/BETA
    J = -float(np.log1p(-ZETA*(1-eig*eig)).sum())
    return H,J,Z

def source(T,L1,L2=None):
    L = np.eye(33)-T
    ev,U = np.linalg.eigh(L)
    ew = np.exp(-BETA*ev)
    Z = float(ew.sum())
    rho = (U*(ew/Z))@U.T
    dh = -float(np.trace(rho@L1))
    Q = (1-ZETA)*np.eye(33)+ZETA*T@T
    dj = 2*ZETA*float(np.trace(T@np.linalg.solve(Q,L1)))
    if L2 is None:
        return dh,dj,rho
    e1 = expm_frechet(-BETA*L,-BETA*L1,compute_expm=False)
    rho1 = e1/Z-rho*np.trace(e1)/Z
    ddh = -float(np.trace(rho1@L1)+np.trace(rho@L2))
    return dh,dj,ddh,rho

def literal_scene_checks():
    require('original scene has 359 edges and 718 oriented histories',len(EDGES)==359)
    w = np.ones(359)
    T,L = scene(w)
    eig = np.linalg.eigvalsh(T)
    rad = np.sqrt(10)/40
    target = np.sort(np.array([1,-.5-rad,-.5+rad]+[0.]*30))
    close('literal normalized adjacency full spectrum',eig,target,2e-14)
    # Actual 718-history retained isometry, reversal and feedback.
    histories = [(i,j) for i,j in EDGES]+[(j,i) for i,j in EDGES]
    V = np.zeros((718,33))
    degree = adjacency(w).sum(axis=1)
    for k,(i,j) in enumerate(histories):
        V[k,j] = 1/np.sqrt(degree[j])
    RV = np.vstack((V[359:],V[:359]))
    close('all718 history isometry',V.T@V,np.eye(33),2e-14)
    close('literal retained reversal compression',V.T@RV,T,2e-14)
    C = RV-V@T
    F = np.eye(33)-T@T
    close('true complement not positive response surrogate',C.T@C,F,3e-14)
    FH = V@F@V.T
    _,logdet718 = np.linalg.slogdet(np.eye(718)-ZETA*FH)
    _,logdet33 = np.linalg.slogdet(np.eye(33)-ZETA*F)
    close('full718 determinant includes complementary identity modes',logdet718,logdet33,1e-12)
    H,J,Z = price(T)
    kap = Fraction(39,160)
    coeffs = {(0,1):Fraction(91,278784), (0,2):Fraction(1,57600),
              (1,2):Fraction(-93,387200)}
    require('exact complete weight-scale source zero',
            99*coeffs[(0,1)]+117*coeffs[(0,2)]+143*coeffs[(1,2)]==0)
    cH = -(np.exp(-BETA*(1.5-rad))-np.exp(-BETA*(1.5+rad)))/(2*rad*Z)
    k = float(kap)
    cJ = 2*ZETA*(1-(1+k)*ZETA)/((1-ZETA)*(1-2*k*ZETA)+k*k*ZETA**2)
    rho = source(T,np.zeros((33,33)))[2]
    M = rho-2*ZETA*T@np.linalg.inv((1-ZETA)*np.eye(33)+ZETA*T@T)
    max_edge_error = 0.
    for e,(i,j) in enumerate(EDGES):
        alpha = np.zeros(359);alpha[e]=1
        _,_,T1,L1,_,_ = scene(w,alpha)
        dk = -float(np.trace(T@T1))
        ref = float(coeffs[tuple(sorted((int(ZONES[i]),int(ZONES[j]))))])
        close('each original edge kappa source',dk,ref,3e-16)
        dh = -float(np.trace(rho@L1))
        dj = float(np.trace((M-rho)@T1))
        err = abs(dh+dj-(cH+cJ)*ref)
        max_edge_error = max(max_edge_error,err)
        require('all359 complete shared-scene sources',err<3e-16)
    require('literal heat is not paired-incidence heat',
            abs(H-(np.log(33+2*np.exp(-BETA*np.linalg.eigvalsh(F)).sum())/BETA))>1e-2)
    require('literal heat is nonzero and dominates single-scene feedback',abs(cH)>1000*cJ>0)
    replicas=[]
    for n in [1,16,256,4096,8192,65536]:
        # Exactly n identical DIRECT-SUM scene copies; no circuit admission implied.
        normalized_coeff = cJ+cH/n
        replicas.append({'copies':n,'normalized_full_kappa_source':normalized_coeff,
                         'normalized_heat_part':cH/n})
        close('direct-sum heat source divided by n',
              (n*cJ+cH)/n,normalized_coeff,1e-16)
    require('replica sign change not hidden by taking absolute values',
            replicas[0]['normalized_full_kappa_source']<0<replicas[-2]['normalized_full_kappa_source'])
    # Tensor-sum H_n=n H, hence H_n/n=H: direct-sum suppression cannot be reused.
    require('tensor-sum negative control retains original heat source',abs(cH)>0.01)
    return {'heat':H,'feedback':J,'kappa':str(kap),'heat_kappa_source':cH,
            'feedback_kappa_source':cJ,'source_dominance_abs_ratio':abs(cH/cJ),
            'all359_source_max_error':max_edge_error,'replica_diagnostic':replicas}

def noncommuting_checks():
    rng = np.random.default_rng(20261022)
    max_first = max_second = max_fd = max_fd2 = 0.
    max_comm = 0.
    for k in range(18):
        w = np.exp(rng.uniform(-3,3,359))
        alpha = rng.uniform(-1,1,359)
        gamma = rng.uniform(-.4,.4,359)
        T,L,T1,L1,T2,L2 = scene(w,alpha,gamma)
        a = float(np.max(np.abs(alpha))); b=float(np.max(np.abs(gamma)))
        norm1 = float(np.linalg.norm(L1,2)); norm2=float(np.linalg.norm(L2,2))
        require('normalized graph operator first bound',norm1<=2*a+1e-13)
        require('normalized graph operator second bound',norm2<=5*a*a+2*b+1e-13)
        dh,dj,ddh,rho = source(T,L1,L2)
        require('dimension-free Gibbs first source bound',abs(dh)<=2*a+1e-13)
        require('dimension-free Gibbs second source bound',abs(ddh)<=(5+4*BETA)*a*a+2*b+1e-13)
        max_first=max(max_first,abs(dh)/(2*a))
        max_second=max(max_second,abs(ddh)/((5+4*BETA)*a*a+2*b))
        max_comm=max(max_comm,float(np.linalg.norm(L@L1-L1@L)))
        step=2e-4
        def val(t):
            return price(scene(w*np.exp(t*alpha+t*t*gamma/2))[0])[0]
        H0,Hplus,Hminus=val(0),val(step),val(-step)
        fd=(Hplus-Hminus)/(2*step)
        fd2=(Hplus-2*H0+Hminus)/step**2
        max_fd=max(max_fd,abs(fd-dh));max_fd2=max(max_fd2,abs(fd2-ddh))
        close('heat first source versus rebuilt actual graph',fd,dh,3e-9)
        close('heat second source versus rebuilt actual graph',fd2,ddh,1e-6)
        # A scalar rescaling of actual edges must disappear after moving degrees.
        _,_,_,Lscale,_,Lscale2=scene(w,np.ones(359))
        close('actual degree normalization first scale zero',Lscale,0,1e-15)
        close('actual degree normalization second scale zero',Lscale2,0,2e-15)
    require('tests genuinely include noncommuting field jets',max_comm>0.01)
    # A rapidly moving legal edge map disproves dimension-only suppression.
    alpha=np.zeros(359);alpha[0]=1
    T,_,_,L1,_,_=scene(np.ones(359),alpha)
    base=source(T,L1)[0]
    N=1000
    _,_,_,Lfast,_,_=scene(np.ones(359),N*alpha)
    fast=source(T,Lfast)[0]/N
    close('growing writer jets defeat naive multiplicity suppression',fast,base,1e-16)
    require('hostile writer source stays nonzero',abs(fast)>1e-8)
    return {'max_first_bound_ratio':max_first,'max_second_bound_ratio':max_second,
            'max_first_fd_error':max_fd,'max_second_fd_error':max_fd2,
            'max_noncommutator_frobenius':max_comm,
            'dimension_only_counterexample_source':fast}

def golden_expansion_checks():
    mp.dps=70
    p=(mp.sqrt(5)-1)/2;z=mp.mpf(2)**-20
    def j(x,y):
        E=p*p*(1+x);L=4*E*(1-E);b=p-p*p*y
        B=4*b*b*(1-b*b);A=L+(1-L)*B
        return -mp.log1p(-z*A)-mp.log1p(-z*B)
    j0=j(0,0)
    jx=mp.diff(lambda x:j(x,0),0);jy=mp.diff(lambda y:j(0,y),0)
    lam=jy/jx
    require('unchanged original lambda_minus',abs(lam+mp.mpf('23.416406751884074972895582'))<mp.mpf('1e-23'))
    rho=[mp.mpf('.5'),mp.mpf('1.5')]
    def fields(t):
        return [(mp.mpf('.2')+mp.mpf('.3')*t+mp.mpf('.05')*t*t,
                 -mp.mpf('.03')+mp.mpf('.02')*t-mp.mpf('.01')*t*t),
                (-mp.mpf('.1')-mp.mpf('.2')*t+mp.mpf('.02')*t*t,
                 mp.mpf('.04')-mp.mpf('.01')*t+mp.mpf('.03')*t*t)]
    def affine(t):return sum(f+lam*q for f,q in fields(t))/2
    target1=mp.diff(affine,0);target2=mp.diff(affine,0,2)
    rows=[]
    for L in [8,16,32,64,128,256]:
        h=mp.mpf(1)/L;tau=h*h
        def normfeedback(t):
            return sum(r*(j(tau*f/r,tau*q/r)-j0)
                       for r,(f,q) in zip(rho,fields(t)))/(2*tau*jx)
        e1=abs(mp.diff(normfeedback,0)-target1)
        e2=abs(mp.diff(normfeedback,0,2)-target2)
        require('nonlinear feedback first Taylor source bound',e1<tau)
        require('nonlinear feedback second Taylor source bound',e2<10*tau)
        scale=h**4/(528*tau*jx)
        rows.append({'L':L,'first_error':mp.nstr(e1,15),
                     'second_error':mp.nstr(e2,15),
                     'first_error_div_tau':mp.nstr(e1/tau,15),
                     'second_error_div_tau':mp.nstr(e2/tau,15),
                     'thermal_first_bound_for_log_edge_jet_one':mp.nstr(2*scale,15)})
    require('first Taylor error shrinks with refinement',mp.mpf(rows[-1]['first_error'])<mp.mpf(rows[0]['first_error'])/900)
    require('second Taylor error shrinks with refinement',mp.mpf(rows[-1]['second_error'])<mp.mpf(rows[0]['second_error'])/900)
    return {'j_x_origin':mp.nstr(jx,35),'lambda_minus':mp.nstr(lam,35),
            'affine_first_source':mp.nstr(target1,25),'affine_second_source':mp.nstr(target2,25),
            'diagnostic_two_cell_ratios':rows,
            'scope':'Scalar operand derivatives, NOT a newly executed all42 geometry or common physical program.'}

def main():
    literal=literal_scene_checks()
    noncommuting=noncommuting_checks()
    golden=golden_expansion_checks()
    result={'status':'PASS_LITERAL_SCENE_HEAT_AND_CONDITIONAL_SOURCE_DESCENT',
      'upstream_read_commit':'5a9764b20c2b7b481ec90d06a711ce3739f4e773',
      'scene_vertices':33,'scene_edges':359,'retained_oriented_histories':718,
      'parameters':{'beta':'2 phi^-2','zeta':'2^-20'},
      'literal_scene':literal,'noncommuting_field_tests':noncommuting,
      'original_two_band_expansion':golden,'checks':len(CHECKS),
      'validation_kind':'Floating matrix diagnostics plus high precision scalar differentiation; proof bounds are analytical, no interval/full-Lean claim.',
      'full42_constructor_replayed':False,'actual_writer_scale_window_proved':False,
      'full_independent_internal_Euler_solved':False,'GR_closed':False}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
