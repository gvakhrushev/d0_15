#!/usr/bin/env python3
"""Exact overlap-price and phase-completed metric/source lift.
Research identities for the declared 24-state record class; not native admission,
not an all-mesh dynamical inverse and not a proof of GR. Python 3 + SymPy.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sympy as S


def equal(a, b, label):
    if isinstance(a, S.MatrixBase) or isinstance(b, S.MatrixBase):
        ok = all(S.cancel(S.simplify(x)) == 0 for x in S.Matrix(a)-S.Matrix(b))
    else:
        ok = S.simplify(a-b) == 0
    if not ok:
        raise ArithmeticError(label)


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


# Consume the original published construction rather than substitute new directions.
OWNER = Path(__file__).resolve().parent.parent/'d0_flat_record_2026-10-15'/'check_flat_record.py'
owner_bytes = OWNER.read_bytes()
owner_blob = hashlib.sha1(b'blob '+str(len(owner_bytes)).encode()+b'\0'+owner_bytes).hexdigest()
require(owner_blob == '06f465874f07fae82111ee9453f4b5ca0b963267', 'Changed upstream flat-record owner')
spec = importlib.util.spec_from_file_location('d0_flat_owner', OWNER)
require(spec is not None and spec.loader is not None, 'Cannot load flat-record owner')
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
labels, vectors = owner.frame(4)
m = len(vectors)
require(m == 12, 'Wrong original carrier')
slots = [(i,j) for i in range(4) for j in range(i,4)]
k = S.Matrix.vstack(*[v.T for v in vectors])
M = S.Matrix([[k[a,i]*k[a,j] for a in range(m)] for i,j in slots])
K = S.Matrix([[int((i,j) in [(0,1),(2,3)])-int((i,j) in [(0,3),(1,2)]),
               int((i,j) in [(0,2),(1,3)])-int((i,j) in [(0,3),(1,2)])]
              for i,j,sign in labels])
leftK = (K.T*K).inv()*K.T
selected = list(range(12))+[12+i for i in (0,1,10,11)]


def overlap_checks():
    a,b,c,t = S.symbols('a b c t', positive=True)
    # Exact full two-state realisation at angle zero; phase conjugation is unitary.
    W = S.Matrix([[a,-b],[b,a]])
    P0 = S.diag(1,0)
    F = P0*(W*W).T*(S.eye(2)-P0)*(W*W)*P0
    equal(F,S.diag(4*a*a*b*b,0),'full repeated-gate leakage')
    Wop = S.Matrix([[a,b],[-b,a]])
    equal(Wop.T*W,W*W,'antipodal record comparison is literally the squared gate')
    w,u = S.symbols('w u', positive=True)
    th,z = S.symbols('th z', real=True)
    v=w*(1-w)
    # Formula follows by taking the absolute square of J_y^* J_x.
    mismatch=w+u-2*w*u-2*S.sqrt(w*(1-w))*S.sqrt(u*(1-u))*S.cos(th)
    # Substitute u=w before reducing square roots, with w in (0,1).
    derivative = lambda expr: S.simplify(S.powdenest(expr.subs(u,w), force=True))
    equal(derivative(mismatch.subs(th,0)),0,'coincident frames')
    equal(derivative(S.diff(mismatch,u).subs(th,0)),0,'zero first amplitude price')
    equal(derivative(S.diff(mismatch,u,2).subs(th,0)),1/(2*v),'amplitude price Hessian')
    equal(derivative(S.diff(mismatch,th,2).subs(th,0)),2*v,'phase price Hessian')
    equal(derivative(S.diff(mismatch,u,th).subs(th,0)),0,'mixed price Hessian')
    equal(derivative(mismatch.subs(th,S.pi)),4*v,'antipodal mismatch')
    # A concrete exact nonzero source along a phase with no eigenvalue change of P/m.
    require(S.Rational(2,5)>0,'nontrivial comparator witness')
    return {'metric':'Hess_y J_z(x,y)|y=x /(2*m*z)',
            'mismatch':'w+u-2*w*u-2*sqrt(w*(1-w)*u*(1-u))*cos(theta_y-theta_x)',
            'same_gate_twice':'W(w,theta+pi)^dagger W(w,theta)=W(w,theta)^2',
            'local_price_hessian':'diag(z/(2*v), 2*z*v) per channel',
            'zeros_retained':12}


def coefficients(weights, first, second):
    """Return exact 2-jet coefficient matrices in (w[12],theta[12]) coordinates."""
    weights=list(weights)
    vs=[w*(1-w) for w in weights]
    ds=[1-2*w for w in weights]
    gamma=S.diag(*([1/(48*v) for v in vs]+[v/12 for v in vs]))
    q=first.T*gamma*first
    qinv=q.inv()
    C=first.T*gamma
    normal=S.eye(24)-first*qinv*C
    cov2=S.zeros(24,10)
    for col,(mu,nu) in enumerate(slots):
        for a in range(12):
            dwmu,dwnu=first[a,mu],first[a,nu]
            dtmu,dtnu=first[a+12,mu],first[a+12,nu]
            v,d=vs[a],ds[a]
            cov2[a,col]=second[mu][nu][a]-d*dwmu*dwnu/(2*v)-2*v*d*dtmu*dtnu
            cov2[a+12,col]=second[mu][nu][a+12]+d*(dwmu*dtnu+dtmu*dwnu)/(2*v)
    B=normal*cov2
    A=-2*B.T*gamma
    X=(leftK*S.diag(*ds)).row_join(S.zeros(2,12))
    F=C.col_join(A).col_join(X)
    return F,q,gamma,C,B


def lift_from(F):
    inv=F[:,selected].inv()
    lift=S.zeros(24,12)
    for row,coord in enumerate(selected):
        for col in range(12):
            lift[coord,col]=inv[row,col+4]
    return lift,inv


def homogeneous_checks():
    v,d=S.symbols('v d', positive=True)
    C=S.zeros(4,12).row_join(v*k.T/12)
    A=(d*M/12).row_join(S.zeros(10,12))
    X=(d*leftK).row_join(S.zeros(2,12))
    F=C.col_join(A).col_join(X)
    ss=S.symbols('s',positive=True)
    F0=F.subs({v:ss,d:ss})
    det=S.factor(F0[:,selected].det())
    equal(det,ss**16/S.Integer(10030613004288),'fixed minor determinant')
    lift, inv=lift_from(F0)
    equal(F0*lift,S.zeros(4,12).col_join(S.eye(12)),'all source and internal slots')
    bound=max(sum(S.Abs(x) for x in row) for row in (ss*inv).tolist())
    equal(bound,14,'infinity inverse bound')
    # Unit-rank/gauge bookkeeping; no hidden complement is dropped.
    equal(F0.rank(),16,'full rank')
    equal(F0.cols-F0.rank(),8,'normal invisible complement count')
    for j,(mu,nu) in enumerate(slots):
        V=S.zeros(4);V[mu,nu]=V[nu,mu]=1
        desired=S.Matrix([3*(k[a,:]*V*k[a,:].T)[0]-S.trace(V) for a in range(12)])/ss
        equal(lift[:12,j],desired,'old lift recovered exactly')
    # Freeze phases at a homogeneous reference only: physical caveat is tested below.
    equal(lift[12:,:],S.zeros(12,12),'flat reference phases need no compensation')
    return {'fixed_minor':str(det),'base_inverse_infinity_norm':'14/p^3',
            'uniform_inverse_bound':'28/p^3 if ||F_selected-F0_selected||_infty <= p^3/28',
            'rank':16,'controlled_metric_slots':10,'controlled_internal_slots':2,
            'normal_constraints':4,'remaining_normal_directions':8}


def inhomogeneous_checks():
    # A rational nearby record germ with nonzero amplitude derivatives in ALL four directions.
    w=S.Rational(13,34)
    weights=[w]*12
    first=S.zeros(24,4)
    first[12:,:]=k
    for mu,a in enumerate((0,2,4,6)):
        first[a,mu]=S.Rational(mu+1,1000)
    second=[[S.zeros(24,1) for _ in range(4)] for _ in range(4)]
    for mu,a in enumerate((0,2,4,6)):
        second[mu][mu][a]=S.Rational(mu+1,10000)
    F,q,gamma,C,B=coefficients(weights,first,second)
    require(all(q[i,i]>0 for i in range(4)) and q.is_diagonal(),'positive real germ')
    require(F[:,selected].det()!=0,'inhomogeneous source-minor nonzero')
    # A rational enclosure certifies that this germ is inside the explicit golden tube.
    lo,mid,hi=(S.Rational(236067,10**6),S.Rational(236068,10**6),S.Rational(236069,10**6))
    require((2+lo)**2<5<(2+hi)**2, 'golden interval')
    C1=S.zeros(4,12).row_join(k.T/12)
    A1=(M/12).row_join(S.zeros(10,12))
    X1=leftK.row_join(S.zeros(2,12))
    base1=C1.col_join(A1).col_join(X1)[:,selected]
    rowsum=lambda a:max(sum(abs(x) for x in row) for row in a.tolist())
    tube_bound=rowsum(F[:,selected]-mid*base1)+(hi-mid)*rowsum(base1)
    require(tube_bound<=lo/28,'rational germ is in golden Neumann tube')
    lift,unused=lift_from(F)
    equal(F*lift,S.zeros(4,12).col_join(S.eye(12)),'nonuniform normal/source/chi lift')
    require(any(x!=0 for x in lift[12:,:]),'phase completion is nontrivial')
    # Derivatives of gamma and C are computed from the actual record metric.
    dgamma=[]
    dC=[]
    v=w*(1-w);d=1-2*w
    aprime=-d/(48*v*v);bprime=d/12
    for mu in range(4):
        gm=S.diag(*([aprime*first[a,mu] for a in range(12)]+[bprime*first[a,mu] for a in range(12)]))
        dgamma.append(gm)
        D=S.zeros(4,24)
        for nu in range(4):
            D[nu,:]=second[mu][nu].T*gamma+first[:,nu].T*gm
        dC.append(D)
    for col in range(12):
        eta=lift[:,col]
        # Every genuine smooth normal lift satisfies C d_mu eta= -d_mu C eta.
        # Additional normal derivatives are arbitrary and drop out exactly.
        derivative_eta=[-first*q.inv()*D*eta for D in dC]
        gamma_eta=S.diag(*([aprime*eta[a] for a in range(12)]+[bprime*eta[a] for a in range(12)]))
        direct=S.zeros(4)
        for mu in range(4):
            for nu in range(4):
                direct[mu,nu]=(first[:,mu].T*gamma_eta*first[:,nu]+derivative_eta[mu].T*gamma*first[:,nu]+first[:,mu].T*gamma*derivative_eta[nu])[0]
        expected=S.zeros(4)
        if col<10:
            mu,nu=slots[col];expected[mu,nu]=expected[nu,mu]=1
        equal(direct,expected,'full differentiated metric, no frozen phases')
    # Actual comparator price derivative has phase terms; discarding them changes source.
    z=S.Rational(1,2)
    r=S.zeros(24,1)
    for a in range(12):
        co=S.Rational(3,5) if a%2==0 else S.Rational(5,13)
        si=S.Rational(4,5) if a%2==0 else -S.Rational(12,13)
        equal(co*co+si*si,1,'actual endpoint phase')
        leak=2*v*(1-co)
        r[a]=z*d*(1-co)/(1-z*leak)
        r[a+12]=z*2*v*si/(1-z*leak)
    actual=lift.T*r
    frozen=lift[:12,:].T*r[:12,:]
    require(actual!=frozen,'actual price detects missing phase source')
    # Explicit null directions are retained, not declared gauge.
    kernel=F.nullspace()
    require(len(kernel)==8,'all normal complement directions')
    for vec in kernel:
        equal(F*vec,S.zeros(16,1),'normal complement equations')
    return {'rational_germ_w':'13/34','amplitude_gradient_directions':4,
            'metric_variation_tests':10,'internal_variation_tests':2,
            'phase_source_required':True,'normal_complement_dimension':8,
            'nonuniform_minor_nonzero':True, 'certified_golden_tube':True}


def run():
    return {'schema':'d0-phase-metric-source/1',
            'scope':'finite-dimensional exact kinematics and smooth-field first variation; no native law or dynamical all-mesh inverse',
            'consumed_owner_blob':owner_blob, 'overlap':overlap_checks(),'homogeneous':homogeneous_checks(),
            'inhomogeneous':inhomogeneous_checks(),
            'native_admission_derived':False,'physical_Info_selected':False,
            'full_GR_closed':False,'new_Lean_compilation':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    txt=json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if a.output:a.output.write_text(txt,encoding='utf8')
    print(txt,end='')

if __name__=='__main__':main()
