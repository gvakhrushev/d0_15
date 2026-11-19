#!/usr/bin/env python3
"""Internal reference comparison for the previously declared D0 report family.

Exact selector/truth-table algebra, complete finite unitaries, retained-price
sources and matched-reference error controls.  A mathematical full-column
target is executed, not a newly emitted G/CX/SourceI programme or a GR PDE.
No prior result file is copied or treated as an executed result.
"""
from __future__ import annotations
import hashlib
import json
import math
import platform
from fractions import Fraction as F
from itertools import product
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy.linalg as la
import sympy as sp

CHECKS = 0
P_GOLD = (math.sqrt(5)-1)/2
CHI = P_GOLD**3
ZETA = 2**-20


def check(ok: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not bool(ok):
        raise ArithmeticError(label)


def near(a, b, label: str, tol: float = 2e-11) -> float:
    error = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    check(error < tol, f'{label}: {error}')
    return error


def exact_factory() -> dict:
    p = (sp.sqrt(5)-1)/2
    P, B, delta, theta = sp.symbols('P B delta theta', real=True)
    # The two selector bits are ACTUAL old raw births with weights (p,p^2).
    selector = [p*p, p**3, p**3, p**4]
    q = 0
    for s, x, y in product(range(4), range(2), range(2)):
        accept = (s == 1 and x == 1) or (s == 2 and y == 0)
        if accept:
            q += selector[s]*(P if x else 1-P)*(B if y else 1-B)
    q = sp.simplify(sp.expand(q))
    target = p**3*(1+P-B)
    check(sp.simplify(q-target) == 0, 'literal finite selector table')
    check(sp.simplify(sum(selector)-1) == 0, 'no branch discarded or conditioned away')
    check(sp.simplify(q.subs(P,B)-p**3) == 0, 'reference is constant for ALL baselines')
    check(sp.simplify(q.subs({P:P+delta,B:B+delta})-q) == 0,
          'linked additive baseline cancels exactly')
    check(sp.simplify(sp.diff(q,P)-p**3) == 0, 'current source is nonzero')
    check(sp.simplify(sp.diff(q,B)+p**3) == 0, 'reference source retained with its actual sign')
    check(sp.simplify(1-4*p**3-p**6) == 0, 'global cold margin equals intrinsic p^6')
    check(bool((1-2*p**3).is_positive), 'nonzero reference cold amplitude')
    check(bool((sp.Rational(1,2)-2*p**3).is_positive), 'all target report probabilities below one half')
    # Not every alteration of the selector is benign.
    eta = sp.symbols('eta', real=True)
    unbalanced = (p**3+eta)*P+(p**3-eta)*(1-B)
    check(sp.simplify(sp.diff(unbalanced.subs(P,B),B)-2*eta) == 0,
          'unequal selector weights restore baseline sensitivity')
    return {
        'report': 'Q(P,B)=p^3*(1+P-B)',
        'reference_probability': str(sp.simplify(p**3)),
        'cold_minimum': str(sp.simplify(p**6)),
        'cold_at_reference': str(sp.simplify(1-2*p**3)),
        'raw_selector_weights': [str(sp.simplify(v)) for v in selector],
        'no_unknown_probability_evaluation_required_by_factory': True,
        'negative_weight_or_postselection_used': False,
    }


def rotation(t: float) -> np.ndarray:
    return np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])


def coin_rotation(probability: float) -> np.ndarray:
    if not 0 < probability < 1:
        raise ValueError('The differentiable matrix control requires 0<P<1.')
    return np.array([[math.sqrt(1-probability),-math.sqrt(probability)],
                     [math.sqrt(probability),math.sqrt(1-probability)]])


def lift_gate(gate: np.ndarray, wires: tuple[int,...], width: int) -> np.ndarray:
    size = 2**width
    out = np.zeros((size,size))
    k = len(wires)
    for col in range(size):
        bits = [(col >> (width-1-i)) & 1 for i in range(width)]
        source = sum(bits[w] << (k-1-i) for i,w in enumerate(wires))
        for target in range(2**k):
            v = gate[target,source]
            if v == 0:
                continue
            bb = bits[:]
            for i,w in enumerate(wires):
                bb[w] = (target >> (k-1-i)) & 1
            row = sum(bb[i] << (width-1-i) for i in range(width))
            out[row,col] = v
    return out


def finite_target(P: float, B: float):
    """Selector1,selector2,current-report,reference-report,protected-DATA.

    Both instruments have scalar effects on ALL DATA inputs, but have distinct,
    noncommuting outcome-conditioned DATA operations.  No input is cloned.
    """
    p = P_GOLD
    golden = np.array([[math.sqrt(p),-p],[p,math.sqrt(p)]])
    phase = np.diag([1.,-1.])
    vx = [rotation(.17),phase@rotation(.41)]
    vy = [phase@rotation(-.23),rotation(.37)]
    check(la.norm(vx[1]@vy[0]-vy[0]@vx[1]) > .1, 'DATA disturbances really noncommute')
    current = la.block_diag(*vx)@np.kron(coin_rotation(P),np.eye(2))
    reference = la.block_diag(*vy)@np.kron(coin_rotation(B),np.eye(2))
    reset = lift_gate(golden.T,(2,),5)@lift_gate(golden.T,(3,),5)
    T = lift_gate(reference,(3,4),5)@lift_gate(current,(2,4),5)@reset
    diagonal = []
    for bits in product(range(2),repeat=5):
        s = 2*bits[0]+bits[1]
        diagonal.append(int((s == 1 and bits[2] == 1) or (s == 2 and bits[3] == 0)))
    effect = np.diag(diagonal)
    U = T.T@(np.eye(32)-2*effect)@T
    born = np.array([1.])
    for _ in range(4):
        born = np.kron(born,np.array([math.sqrt(p),p]))
    i = np.kron(born[:,None],np.eye(2))
    q = CHI*(1+P-B)
    near(T.T@T,np.eye(32),'complete target preparation')
    near(U@U,np.eye(32),'complete reflected operator')
    near(i.T@i,np.eye(2),'true raw-born input isometry')
    err = near(i.T@T.T@effect@T@i,q*np.eye(2),'all-input effect, not one observed number')
    near(i.T@U@i,(1-2*q)*np.eye(2),'full cold operator')
    check(int(np.trace(effect)) == 8, 'fixed sign rank on entire work')
    near(np.trace(U),16.,'unchanged full reflection signature')
    return U,i,q,err


def scene_data():
    counts = [9,11,13]
    edges = np.zeros((33,33))
    starts = np.cumsum([0]+counts)
    for i in range(3):
        for j in range(3):
            if i != j:
                edges[starts[i]:starts[i+1],starts[j]:starts[j+1]] = 1
    degree = edges.sum(1)+2
    R = np.diag(1/np.sqrt(degree))
    check(int(edges.sum()/2) == 359, 'same complete scene')
    return R@edges@R,R@R


def whole_scene_heat(U: np.ndarray, N: int) -> float:
    """All scene/clock modes via exact phase-reduction identity, no low-mode cut."""
    b,c = scene_data()
    phases = np.angle(la.eigvals(U))
    beta = 2*P_GOLD**2
    Z0 = 0.
    for theta in phases:
        for j in range(N):
            x = math.cos((theta+2*math.pi*j)/N)
            eigen = la.eigvalsh(np.eye(33)-b-2*x*c)
            Z0 += np.exp(-beta*eigen).sum()
    Z01 = 2*Z0+359*N*len(U)
    return math.log(Z01)/beta


def operator_and_heat_controls() -> dict:
    K = np.array([[.53,.13],[.03,.27]])
    old = np.block([[K,la.sqrtm(np.eye(2)-K@K.T)],
                    [la.sqrtm(np.eye(2)-K.T@K),-K.T]])
    near(old.T@old,np.eye(4),'complete nonnormal past unitary')
    check(la.norm(K.T@K-K@K.T) > .01,'actual old contraction is nonnormal')
    records=[]
    heat_values=[]
    baseline_prices=[]
    N=3
    for P,B in ((.12,.12),(.35,.35),(.78,.78),(.46,.31),(.18,.63)):
        U,i,q,err = finite_target(P,B)
        full = np.kron(old,U)
        j = np.kron(np.eye(4)[:,:2],i)
        cold = j.T@full@j
        near(cold,(1-2*q)*np.kron(K,np.eye(2)),'true retained old/current cold matrix')
        projector = j@j.T
        Fwhole = projector@full.T@(np.eye(128)-projector)@full@projector
        Fsmall = np.eye(4)-cold.T@cold
        Jwhole = -np.log1p(-ZETA*la.eigvalsh((Fwhole+Fwhole.T)/2)).sum()
        Jsmall = -np.log1p(-ZETA*la.eigvalsh((Fsmall+Fsmall.T)/2)).sum()
        je = near(Jwhole,Jsmall,'whole return determinant and its real input rank',1e-19)
        H = whole_scene_heat(full,N)
        heat_values.append(H)
        if P == B:
            baseline_prices.append(Jwhole)
        records.append({'current':P,'reference':B,'Q':q,'source_effect_error':err,
                        'return_price':float(Jwhole),'determinant_error':je,'full_heat':H})
    near(baseline_prices,np.repeat(baseline_prices[0],len(baseline_prices)),
         'shared baseline can change finitely without changing return price',1e-19)
    he = near(heat_values,np.repeat(heat_values[0],len(heat_values)),
              'fixed-layout full heat retained and isospectral',3e-13)
    return {'complete_target_dimension':32,'whole_past_current_dimension':128,'protected_rank':4,
            'stage_count_in_structural_heat_control':N,'all_Hodge_modes':425*N*128,
            'unobserved_record_branches_retained':True,'unknown_DATA_cloned':False,
            'full_heat_error':he,'controls':records,'new_native_words_emitted':False}


def exact_joint_bound() -> dict:
    """Nonconstant baseline on each site, correlated PF and independent shape jets."""
    x,y,t,u = sp.symbols('x y t u',real=True)
    # Reference shares t,u at the SAME site; no common scalar baseline assumption.
    r = sp.Rational(2,5)+t/17+u*u/31+x/11+2*y/7+x*y/9+u*(x*x+2*x*y+3*y*y)/37
    R = sp.expand(r-r.subs({x:0,y:0})-x/11-2*y/7)
    check(sp.diff(r,t) == sp.Rational(1,17),'uncompared baseline really has a nonzero row')
    check(sp.diff(R,t) == 0,'linked baseline removed by the actual comparison')
    H = F(2,37)+2*(F(1,9)+F(2,37))+F(6,37)
    Hshape = F(12,37)
    values=[]
    for eps in (F(1,16),F(1,64),F(1,256)):
        mu=[F(1,2),F(1,2)];rho=[F(3,4),F(5,4)];drho=[F(1,7),-F(1,7)]
        f=[[F(1,5),-F(1,6)],[F(1,7),F(1,4)]]
        df=[[F(2,9),-F(1,3)],[F(1,11),F(1,6)]]
        sig=[F(3,2),F(4,5)];ds=[F(1,9),-F(1,7)]
        tt=[F(1,5),-F(2,5)];dt=[F(2,7),F(1,3)]
        uu=[F(2,3),-F(1,2)];du=[F(3,5),-F(2,7)]
        source=F(0);leading=F(0);bound=F(0)
        for j in range(2):
            a=[sig[j]*v for v in f[j]]
            da=[ds[j]*f[j][k]+sig[j]*df[j][k] for k in range(2)]
            arg=[eps*v/rho[j] for v in a]
            darg=[eps*(da[k]/rho[j]-a[k]*drho[j]/rho[j]**2) for k in range(2)]
            at={x:arg[0],y:arg[1],t:tt[j],u:uu[j]};ref={x:0,y:0,t:tt[j],u:uu[j]}
            diff=F(r.subs(at)-r.subs(ref))
            derivative=F(sp.diff(r,x).subs(at))*darg[0]+F(sp.diff(r,y).subs(at))*darg[1]
            derivative+=F(sp.diff(r,t).subs(at)-sp.diff(r,t).subs(ref))*dt[j]
            derivative+=F(sp.diff(r,u).subs(at)-sp.diff(r,u).subs(ref))*du[j]
            source+=mu[j]*(drho[j]*diff+rho[j]*derivative)
            leading+=eps*mu[j]*(F(1,11)*da[0]+F(2,7)*da[1])
            an=max(map(abs,a));dn=max(map(abs,da))
            bound+=eps**2*mu[j]/rho[j]*(H*an*dn+H*an*an*abs(drho[j]/rho[j])/2+Hshape*an*an*abs(du[j])/2)
        check(abs(source-leading)<=bound,'whole PF/field/scale/shape reference bound')
        values.append({'epsilon':str(eps),'normalized_source_error':str(abs(source-leading)/eps),
                       'normalized_bound':str(bound/eps)})
    check(F(values[2]['normalized_source_error']) < F(values[0]['normalized_source_error'])/10,
          'true normalized source convergence')
    return {'site_dependent_baseline_and_PF_varied':True,'tests':values}


def original_report(x,y):
    p=(mp.sqrt(5)-1)/2;zz=mp.mpf(2)**-20
    E=p*p*(1+x);ell=4*E*(1-E);u=p+p*p*y
    B=4*u*u*(1-u*u);A=ell+(1-ell)*B
    return zz*(A+B)-zz*zz*A*B


def retained_source_controls() -> dict:
    mp.mp.dps=100
    pp=(mp.sqrt(5)-1)/2;chi=pp**3;z=mp.mpf(2)**-20;a=mp.mpf(17)/50
    r0=original_report(0,0);rf=mp.diff(lambda x:original_report(x,0),0)
    rq=mp.diff(lambda y:original_report(0,y),0);lam=-rq/rf
    K=mp.matrix([[mp.mpf('.53'),mp.mpf('.13')],[mp.mpf('.03'),mp.mpf('.27')]])
    A=K.T*K;eta=pp**80
    def r(x,y,b,scale,shape):
        return r0*(1+b/4)+(1+scale/3)*(original_report(x,y)-r0)+shape*rf*(x*x+x*y+2*y*y)
    params=[[mp.mpf('.2'),mp.mpf('.1'),mp.mpf('.4'),mp.mpf('.3'),mp.mpf('.6')],
            [-mp.mpf('.1'),mp.mpf('.07'),-mp.mpf('.3'),-mp.mpf('.2'),-mp.mpf('.8')]]
    rows=[]
    for eps in (mp.mpf(2)**-4,mp.mpf(2)**-7,mp.mpf(2)**-10,mp.mpf(2)**-13):
        def corner(v):
            f,q,b,scale,shape=v
            current=a*r(eps*f,-eps*q,b,scale,shape)
            reference=a*r(0,0,b,scale,shape)
            return 1-2*chi*(1+current-reference)
        cs=[corner(v) for v in params];ss=mp.fprod(c*c for c in cs)
        D=(1-z)*mp.eye(2)+z*eta*ss*A;Di=D**-1
        tr=sum((Di*A)[i,i] for i in range(2));w=z*eta*ss*tr
        L=sum(1/c for c in cs);Gamma=4*chi*a*eps*rf*w*L
        weights=[(1/c)/L for c in cs]
        def full_price(vs):
            s=mp.fprod(corner(v)**2 for v in vs)
            return -mp.log(mp.det((1-z)*mp.eye(2)+z*eta*s*A))
        field_error=mp.mpf(0);shape_norm=mp.mpf(0);base_norm=mp.mpf(0);source_error=mp.mpf(0)
        for j in range(2):
            f,q,b,scale,shape=params[j]
            for n in range(5):
                def local(t):
                    vs=[v[:] for v in params];vs[j][n]=t
                    return full_price(vs)
                dg=mp.diff(local,params[j][n])
                dc=mp.diff(lambda t:corner(params[j][:n]+[t]+params[j][n+1:]),params[j][n])
                analytic=-2*w*dc/cs[j]
                source_error=max(source_error,abs(dg-analytic))
                check(abs(dg-analytic)<mp.mpf('1e-90'),'complete noncommuting-past source, actual gain')
                got=dg/Gamma
                if n==0:expected=weights[j]*(1+scale/3)
                elif n==1:expected=weights[j]*(1+scale/3)*lam
                elif n==2:expected=mp.mpf(0);base_norm+=abs(got)
                elif n==3:expected=weights[j]*(f+lam*q)/3
                else:expected=mp.mpf(0);shape_norm+=abs(got)
                if n in (0,1,3):field_error+=abs(got-expected)
        check(base_norm<mp.mpf('1e-65'),'free linked baseline source exactly zero, not O(epsilon)')
        rows.append({'epsilon':mp.nstr(eps,12),'actual_Gamma':mp.nstr(Gamma,24),
                     'independent_baseline_dual_norm':mp.nstr(base_norm,12),
                     'shape_dual_norm':mp.nstr(shape_norm,24),
                     'field_and_scale_l1_error':mp.nstr(field_error,24),
                     'matrix_source_error':mp.nstr(source_error,8)})
    check(mp.mpf(rows[-1]['shape_dual_norm'])<mp.mpf(rows[0]['shape_dual_norm'])/100,
          'shape decay before any dilution')
    check(mp.mpf(rows[-1]['field_and_scale_l1_error'])<mp.mpf(rows[0]['field_and_scale_l1_error'])/100,
          'original geometric source and scale retained')
    return {'reference_r0_diagnostic_only':mp.nstr(r0,30),'r_f':mp.nstr(rf,30),
            'lambda':mp.nstr(lam,30),'retention_blocks':80,'tests':rows,
            'no_evaluation_of_r0_needed_to_build_selector':True,
            'large_native_history_or_PDE_executed':False}


def limitation_controls() -> dict:
    eps,b,s,theta,chi,a=sp.symbols('eps b s theta chi a',positive=True)
    current=b+eps*s
    # Independent reference drift remains an actual source, no declaration of gauge.
    ref=b+theta
    Q=chi*(1+a*(current-ref))
    check(sp.simplify(sp.diff(Q,theta)/(chi*a*eps)+1/eps)==0,
          'unlinked reference drift retains its full pole')
    # Using current as its own reference kills the desired field source as well.
    self_compare=chi*(1+a*(current-current))
    check(sp.diff(self_compare,s)==0,'self-reference negative control')
    # A wrong leading matter/gravity ratio survives a proper subtraction.
    f,q,k=sp.symbols('f q k',real=True)
    P=chi*(1+a*eps*(f-(k+theta)*q))
    check(sp.simplify(sp.diff(P,theta)/(chi*a*eps)+q)==0,
          'independent relative coupling not erased')
    fast=eps**2*sp.sin(theta/eps**2)
    check(sp.simplify(sp.diff(fast,theta).subs(theta,0)/eps-1/eps)==0,
          'true mixed derivative hypothesis still needed')
    for M in (1,2,9,100):
        check(sum(F(1,M) for _ in range(M))==1,'no 1/M suppression of a repeated nonzero current row')
    # Compiled endpoint error is a finite comparison budget, not a tangent.
    dc,dr,t=sp.symbols('delta_current delta_reference t',positive=True)
    check(sp.expand(chi*a*(dc+dr)/(chi*a*eps*t)-(dc+dr)/(eps*t))==0,
          'real endpoint precision relative to epsilon and step retained')
    return {'unlinked_reference_normalized_source':'-1/epsilon',
            'self_comparison_geometric_source':0,
            'free_relative_coupling_source':'-q',
            'fast_shape_source':'1/epsilon',
            'endpoint_requirement':'(delta_current+delta_reference)/(epsilon*|t|) -> 0 with actual constants'}



def cross_table_exact() -> dict:
    """No probabilities are inverted or estimated: eight signed products become
    one positive event using eight equal-weight raw histories of five births.
    """
    p=(sp.sqrt(5)-1)/2;chi=p**7
    yp,ym,cur,base,xp,xm,mat=sp.symbols('yp ym current baseline xp xm material',real=True)
    probabilities=[yp,ym,cur,base,xp,xm,mat]
    # sign, first report index, second report index
    terms=[(1,0,2),(1,1,3),(-1,0,3),(-1,1,2),
           (1,4,6),(1,5,3),(-1,4,3),(-1,5,6)]
    selectors=[w for w in range(32) if w.bit_count()==2][:8]
    check(len(selectors)==8,'eight genuine distinct equal-weight raw selector histories')
    for word in selectors:
        weight=sp.prod(p**(1+((word>>(4-i))&1)) for i in range(5))
        check(sp.simplify(weight-chi)==0,'same raw probability p^7, no fair-coin primitive')
    q=sum(chi*(probabilities[i]*probabilities[j] if sign==1 else 1-probabilities[i]*probabilities[j])
          for sign,i,j in terms)
    xi=(yp-ym)*(cur-base)+(xp-xm)*(mat-base)
    check(sp.expand(q-chi*(4+xi))==0,'complete positive cross-calibration truth table')
    check(sp.simplify(q.subs({cur:base,mat:base})-4*chi)==0,'all reference baselines cancel exactly')
    check(bool((1-16*chi).is_positive),'complete outcome has positive cold margin')
    check(sp.simplify(chi-(13*p-8))==0,'intrinsic selector weight exactly identified')
    # These bounds use the probability of all selected paths, not a signed measure.
    return {'formula':'Q_cross=p^7*[4+(P_yplus-P_yminus)*(P_f-P_0)+(P_xplus-P_xminus)*(P_q-P_0)]',
            'selector_words':[format(w,'05b') for w in selectors],
            'true_selector_weight':str(sp.simplify(chi)),
            'reference_probability':str(sp.simplify(4*chi)),
            'conservative_cold_lower_bound':str(sp.simplify(1-16*chi)),
            'report_terms':terms}


def cross_full_target_control() -> dict:
    p=P_GOLD;chi=p**7
    terms=[(1,0,2),(1,1,3),(-1,0,3),(-1,1,2),(1,4,6),(1,5,3),(-1,4,3),(-1,5,6)]
    selectors=[w for w in range(32) if w.bit_count()==2][:8]
    sign=np.ones(4096)
    for s,(sgn,i,j) in zip(selectors,terms):
        for record in range(128):
            outcome=((record>>(6-i))&1) and ((record>>(6-j))&1)
            accept=bool(outcome) if sgn>0 else not bool(outcome)
            if accept:sign[s*128+record]=-1
    check(int(np.sum(sign<0))==512,'entire fixed cross-predicate rank')
    golden=np.array([[math.sqrt(p),-p],[p,math.sqrt(p)]])
    birth=np.array([math.sqrt(p),p]);v=np.array([1.])
    for _ in range(12):v=np.kron(v,birth)
    rng=np.random.default_rng(20261031)
    probe=rng.normal(size=4096)+1j*rng.normal(size=4096);probe/=la.norm(probe)
    def gate_on_vector(vector,gate,wire):
        x=vector.reshape((2,)*12)
        y=np.tensordot(gate,x,axes=(1,wire))
        y=np.moveaxis(y,0,wire)
        return y.reshape(-1)
    values=[]
    for probs in ([.31,.27,.44,.35,.39,.23,.28],[.48,.44,.55,.51,.61,.45,.46]):
        operators=[coin_rotation(t)@golden.T for t in probs]
        def A_apply(vec,inverse=False):
            work=vec.copy()
            for j in (reversed(range(7)) if inverse else range(7)):
                work=gate_on_vector(work,operators[j].T if inverse else operators[j],5+j)
            return work
        def U_apply(vec):return A_apply(sign*A_apply(vec),True)
        near(A_apply(A_apply(probe),True),probe,'full4096 preparation inverse, not a retained-column projection',2e-13)
        near(U_apply(U_apply(probe)),probe,'complete4096 reflected target action',2e-13)
        psi=A_apply(v);q=float(np.sum(np.abs(psi[sign<0])**2))
        yplus,yminus,f,b,xplus,xminus,m=probs
        expected=chi*(4+(yplus-yminus)*(f-b)+(xplus-xminus)*(m-b))
        err=near(q,expected,'all4096 outcome probabilities, no erased branches',2e-13)
        near(np.vdot(v,U_apply(v)),1-2*expected,'canonical raw-born cold amplitude of entire cross-reporter',2e-13)
        values.append({'report_probabilities':probs,'actual_output':q,'formula_error':err})
    return {'mathematical_work_dimension':4096,'raw_births':12,'source_report_calls':7,
            'negative_sign_rank':512,'full_square_matrix_materialized':False,
            'full_operator_defined_by_unitary_tensor_factors':True,
            'data_factor_identity_in_this_control':True,'controls':values,
            'native_compilation_executed':False}


def cross_symbolic_source_bound() -> dict:
    e,d,f,q,a,b,t=sp.symbols('epsilon delta f q a b theta',real=True)
    k=sp.Rational(22,7)
    # A cubic axis jet with arbitrary positive first slopes and independent shape.
    x,y=sp.symbols('x y',real=True)
    r=sp.Rational(2,5)+t/17+a*x+b*y+(1+t)*x*x/9+(1-2*t)*y*y/11+x**3/13+t*y**3/19
    base=r.subs({x:0,y:0})
    dy=r.subs({x:0,y:d})-r.subs({x:0,y:-d})
    dx=r.subs({x:k*d,y:0})-r.subs({x:-k*d,y:0})
    Fcur=r.subs({x:e*f,y:0})-base
    Mcur=r.subs({x:0,y:-e*q})-base
    normalized=sp.expand((dy*Fcur+dx*Mcur)/(2*d*e))
    rem=sp.expand(normalized-a*b*(f-k*q))
    variables=[f,q,a,b,t]
    C=sp.Rational(0)
    for var in variables:
        polynomial=sp.Poly(sp.diff(rem,var),e,d,f,q,a,b,t)
        bound=0
        for exponents,coefficient in polynomial.terms():
            if coefficient==0:continue
            check(exponents[0]>=1 or exponents[1]>=2,'every complete-source error monomial has epsilon or delta^2')
            bound+=abs(coefficient)
        C+=bound
    check(C>0,'actual rational derivative bound computed')
    # On |f|,|q|,|a|,|b|,|theta|<=1 and0<eps,delta<=1:
    # ||D rem||_{infinity,*} <= C*(epsilon+delta^2).
    for ev,dv in ((F(1,16),F(1,64)),(F(1,64),F(1,128)),(F(1,256),F(1,256))):
        at={e:ev,d:dv,f:F(1,5),q:-F(1,6),a:F(2,3),b:F(4,5),t:F(1,3)}
        actual=sum(abs(F(sp.diff(rem,v).subs(at))) for v in variables)
        check(actual<=F(C)*(ev+dv*dv),'exact rational bound for all independent field and coefficient sources')
    return {'structural_kappa':str(k),'source_remainder_bound':'||D remainder|| <= C*(epsilon+delta^2)',
            'C_exact':str(C),'independent_first_slopes_varied':True,
            'no_preselected_source_zero':True}


def cross_original_source() -> dict:
    mp.mp.dps=100
    p=(mp.sqrt(5)-1)/2;chi=p**7;z=mp.mpf(2)**-20;a=mp.mpf(17)/50
    r0=original_report(0,0);rf=mp.diff(lambda x:original_report(x,0),0)
    rq=mp.diff(lambda y:original_report(0,y),0);kappa=rq/rf
    oldK=mp.matrix([[mp.mpf('.53'),mp.mpf('.13')],[mp.mpf('.03'),mp.mpf('.27')]])
    oldA=oldK.T*oldK;retention=p**80
    def probability(x,y,theta):
        baseline,sa,sb,shape=theta
        result=r0*(1+baseline/4)+(1+sa/3)*(original_report(x,0)-r0)
        result+=(1+sb/5)*(original_report(0,y)-r0)+shape*rf*(x*x+2*y*y)
        return a*result
    pars=[[mp.mpf('.2'),mp.mpf('.1'),mp.mpf('.4'),mp.mpf('.3'),-mp.mpf('.2'),mp.mpf('.6')],
          [-mp.mpf('.1'),mp.mpf('.07'),-mp.mpf('.3'),-mp.mpf('.4'),mp.mpf('.7'),-mp.mpf('.8')]]
    result=[]
    for eps in (mp.mpf(2)**-4,mp.mpf(2)**-7,mp.mpf(2)**-10,mp.mpf(2)**-13):
        delta=eps/(2*kappa)  # fixed during each comparison; both limits tend to zero
        def q(v):
            f,qq,*theta=v
            base=probability(0,0,theta)
            dy=probability(0,delta,theta)-probability(0,-delta,theta)
            dx=probability(kappa*delta,0,theta)-probability(-kappa*delta,0,theta)
            Fcur=probability(eps*f,0,theta)-base
            Mcur=probability(0,-eps*qq,theta)-base
            return chi*(4+dy*Fcur+dx*Mcur)
        cs=[1-2*q(v) for v in pars];ss=mp.fprod(c*c for c in cs)
        D=(1-z)*mp.eye(2)+z*retention*ss*oldA
        Di=D**-1;trace=sum((Di*oldA)[i,i] for i in range(2))
        w=z*retention*ss*trace;L=sum(1/c for c in cs)
        Gamma=8*chi*delta*eps*a*a*rf*rq*w*L
        weights=[1/c/L for c in cs]
        def price(vs):
            s=mp.fprod((1-2*q(v))**2 for v in vs)
            return -mp.log(mp.det((1-z)*mp.eye(2)+z*retention*s*oldA))
        error=mp.mpf(0);shape=mp.mpf(0);baseline=mp.mpf(0);matrix_error=mp.mpf(0)
        for j,values in enumerate(pars):
            f,qq,bb,sa,sb,sh=values
            sig=(1+sa/3)*(1+sb/5)
            for n in range(6):
                def J(t):
                    copies=[v[:] for v in pars];copies[j][n]=t
                    return price(copies)
                actual=mp.diff(J,values[n])
                dq=mp.diff(lambda t:q(values[:n]+[t]+values[n+1:]),values[n])
                direct=4*w*dq/cs[j]
                matrix_error=max(matrix_error,abs(actual-direct))
                check(abs(actual-direct)<mp.mpf('1e-90'),'cross-calibrated derivative of actual full determinant')
                got=actual/Gamma
                if n==0:expected=weights[j]*sig
                elif n==1:expected=-weights[j]*sig*kappa
                elif n==2:expected=0;baseline+=abs(got)
                elif n==3:expected=weights[j]*(1+sb/5)*(f-kappa*qq)/3
                elif n==4:expected=weights[j]*(1+sa/3)*(f-kappa*qq)/5
                else:expected=0;shape+=abs(got)
                if n in (0,1,3,4):error+=abs(got-expected)
        check(baseline<mp.mpf('1e-55'),'entire correlated baseline row remains zero')
        # The raw slope ratios really differ from the inherited coupling.
        ratios=[kappa*(1+v[4]/5)/(1+v[3]/3) for v in pars]
        check(all(abs(v-kappa)>1 for v in ratios),'input leading ratios are not pre-matched')
        result.append({'epsilon':mp.nstr(eps,12),'delta':mp.nstr(delta,20),
                       'actual_Gamma':mp.nstr(Gamma,24),'input_slope_ratios':[mp.nstr(v,18) for v in ratios],
                       'baseline_dual_norm':mp.nstr(baseline,10),'independent_shape_dual_norm':mp.nstr(shape,24),
                       'field_and_independent_slope_source_error':mp.nstr(error,24),
                       'full_matrix_derivative_error':mp.nstr(matrix_error,8)})
    check(mp.mpf(result[-1]['field_and_independent_slope_source_error'])<mp.mpf(result[0]['field_and_independent_slope_source_error'])/100,
          'changed slope controls recover the same full coframe pullback')
    check(mp.mpf(result[-1]['independent_shape_dual_norm'])<mp.mpf(result[0]['independent_shape_dual_norm'])/100,
          'cross-calibrated nonlinear shape row decays')
    # The reference aspect ratio is an honest calibration, not physically selected here.
    check(kappa>23 and kappa<24,'inherited fixed calibration, not fitted to a solution')
    return {'reference_aspect_ratio':mp.nstr(kappa,30),'calibration_from_original_source':True,
            'arbitrary_reference_aspect_ratio_would_change_matter_coupling':True,
            'general_selection_of_this_protocol_from_M1_proved':False,'tests':result}


def main():
    out={'input_commit':'188755d5fe9adb565a32ab3adfc371ee7e43ba11',
         'selector':exact_factory(),'all_input_operator_and_heat':operator_and_heat_controls(),
         'joint_source_bound':exact_joint_bound(),'retained_source':retained_source_controls(),
         'negative_controls':limitation_controls(),
         'cross_selector':cross_table_exact(),'cross_full_target':cross_full_target_control(),
         'cross_exact_source_bound':cross_symbolic_source_bound(),'cross_original_source':cross_original_source()}
    out.update({'status':'PASS_SCOPED_INTERNAL_REFERENCE_AND_CROSS_CALIBRATION','checks':CHECKS,
        'unrestricted_D0_GR_closed':False,'new_native_G_CX_SourceI_words_emitted':False,
        'general_physical_domain_derived':False,'fine_record_equivalence_claimed':False,
        'Lean_or_CI_run':False,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'environment':{'python':platform.python_version(),'numpy':np.__version__,
                       'sympy':sp.__version__,'mpmath':mp.__version__}})
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
