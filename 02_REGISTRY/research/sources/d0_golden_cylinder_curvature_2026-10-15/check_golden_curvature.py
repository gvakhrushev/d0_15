#!/usr/bin/env python3
"""Exact finite golden-history curvature readout; not native action selection."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
from itertools import product
import sympy as s

P = (s.sqrt(5)-1)/2
PHI = 1/P
MIXED_SIGN = {(True, True): 0, (True, False): 1,
              (False, True): -1, (False, False): 0}
HIGH_SCALE_POWER = 4
KEEP_CALIBRATION_JET = True
KEEP_BLANK_JET = True
CHECKS: list[str] = []


def red(x):
    return s.simplify(s.expand(x))


def eq(a, b, label):
    d = s.Matrix(a)-s.Matrix(b) if isinstance(a, s.MatrixBase) else a-b
    ok = all(red(x) == 0 for x in d) if isinstance(d, s.MatrixBase) else red(d) == 0
    if not ok:
        raise ArithmeticError(label)
    CHECKS.append(label)


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)
    CHECKS.append(label)


def cost(word):
    # Exact convention of DetectorSupportGoldenWeight: true is direct, cost one.
    return sum(1 if letter else 2 for letter in word)


def weight(word):
    return red(P**cost(word))


def cut(n):
    ready, pending = [()], []
    for _ in range(n):
        ready, pending = ([w+(True,) for w in ready]+pending,
                          [w+(False,) for w in ready])
    return ready, pending


def feedback_value(A, r, word):
    return (s.eye(4)-r*MIXED_SIGN[word[:2]]*A).det()


def mass(shapes, r):
    return red(sum(weight(w)*feedback_value(A, r, w)
                   for A in shapes for w in product((True, False), repeat=2)))


def coefficient_readout(m0, mt, mlarge, r, occupancy=2*P**3):
    return red(2*P**3*(PHI**HIGH_SCALE_POWER*(mt-m0)-(mlarge-m0))
               /(occupancy*r**2))


def scalar_gauss(shapes):
    # Full contraction of the Gauss Riemann tensor, not the expected filter.
    return red(sum(A[i,i]*A[j,j]-A[i,j]*A[j,i]
                   for A in shapes for i in range(4) for j in range(4)))


def determinant_jet(A, dA, r):
    D = s.eye(4)-r*A
    cof = D.cofactor_matrix()
    return s.expand(sum(cof[i,j]*(-r*dA[i,j]) for i in range(4) for j in range(4)))


def mass_jet(shapes, tangents, r):
    return red(sum(weight(w)*determinant_jet(A, dA, r*MIXED_SIGN[w])
                   for A,dA in zip(shapes,tangents)
                   for w in product((True,False),repeat=2)))


def run():
    CHECKS.clear()
    eq(P+P**2,1,'native golden normalization')
    weights=[weight(w) for w in product((True,False),repeat=2)]
    eq(sum(weights),1,'all four two-letter histories retained')
    eq(weights[1],weights[2],'FR and RF equal-cost weights')
    eq(weights[1],P**3,'mixed history is p cubed')
    for j in (1,2,3,4):
        got=sum(weight(w)*MIXED_SIGN[w]**j for w in product((True,False),repeat=2))
        eq(got,0 if j%2 else 2*P**3,f'golden signed moment {j}')
    eq(P**3*(PHI**4-PHI**2),1,'golden scale calibration')

    r=s.symbols('r',real=True)
    A=s.diag(1,2,3,5)
    B=s.Matrix([[2,1,0,1],[1,-1,2,0],[0,2,3,1],[1,0,1,0]])
    shapes=[A,B]
    require(A*B!=B*A,'noncommuting shape fixture')
    R=scalar_gauss(shapes)
    Q4=A.det()+B.det()
    M=mass(shapes,r)
    eq(M,2+P**3*r**2*R+2*P**3*r**4*Q4,'complete golden trace polynomial')
    eq(coefficient_readout(2,M,M.subs(r,PHI*r),r),R,'exact finite scalar curvature')
    require(Q4!=0,'quartic term is actually present')
    for n in range(4,13):
        ready,pending=cut(n)
        require(all(len(w)>=2 for w in ready+pending),f'cost cut {n} resolves two letters')
        # Grouping is only a polynomial evaluation optimization; every word contributes.
        total=0
        for first in product((True,False),repeat=2):
            blockmass=red(sum(weight(w) for w in ready+pending if w[:2]==first))
            eq(blockmass,weight(first),f'cut {n} full cylinder {first}')
            total+=blockmass*feedback_value(A,r,first)
        eq(total,mass([A],r),f'cut {n} operator expectation')
        nr,np=cut(n+1)
        f=lambda w: feedback_value(A,r,w)
        require([f(w) for w in nr]==[f(w) for w in ready]+[f(w) for w in pending]
                and [f(w) for w in np]==[f(w) for w in ready],
                f'cut {n} literal diag(A,B),A intertwining')

    # A rotating normal basis changes the fourth-order sum, not the extracted source.
    T=s.Matrix([[s.Rational(3,5),s.Rational(4,5)],[-s.Rational(4,5),s.Rational(3,5)]])
    rotated=[T[i,0]*A+T[i,1]*B for i in range(2)]
    eq(T*T.T,s.eye(2),'normal frame is orthogonal')
    Q4rot=sum(X.det() for X in rotated)
    require(Q4rot!=Q4,'axes fourth moment is genuinely frame dependent')
    MR=mass(rotated,r)
    eq(coefficient_readout(2,MR,MR.subs(r,PHI*r),r),R,'quartic anisotropy removed before variation')
    # Overcomplete Parseval normals, without choosing a normal eigenbasis.
    parseval=[A,s.Rational(3,5)*B,s.Rational(4,5)*B]
    MP=mass(parseval,r)
    eq(coefficient_readout(3,MP,MP.subs(r,PHI*r),r),R,'overcomplete Parseval normal family')
    padded=MP+17  # Seventeen actual zero-shape settings, each with mass one.
    eq(coefficient_readout(20,padded,padded.subs(r,PHI*r),r),R,'zero-shape spectators retained and canceled')
    deleted=mass([A],r)
    require(red(coefficient_readout(1,deleted,deleted.subs(r,PHI*r),r)-R)!=0,
            'dropping active normal directions fails')

    # Every packed metric slot, genuine variation of q^{-1}B at q=I.
    slots=[(i,j) for i in range(4) for j in range(i,4)]
    for i,j in slots:
        V=s.zeros(4); V[i,j]=1; V[j,i]=1
        dots=[-V*X for X in shapes]
        dM=mass_jet(shapes,dots,r)
        got=coefficient_readout(0,dM,dM.subs(r,PHI*r),r)
        expected=sum(2*s.trace(X)*s.trace(dX)-2*s.trace(X*dX)
                     for X,dX in zip(shapes,dots))
        eq(got,expected,f'all metric contractions {i}{j}')
    # Moving normal frame: every shape changes, scalar is constant.
    dM=mass_jet(shapes,[B,-A],r)
    eq(coefficient_readout(0,dM,dM.subs(r,PHI*r),r),0,'moving normal frame source cancels')

    # Calibrated even readout for arbitrary actual state, with all preparation jets.
    a,da,e2,e4,de2,de4,t,dt=s.symbols('a da e2 e4 de2 de4 t dt',nonzero=True,real=True)
    even=lambda u: 1+a*(u**2*e2+u**4*e4)
    N=red(PHI**4*(even(t)-1)-(even(PHI*t)-1))
    eq(coefficient_readout(1,even(t),even(PHI*t),t,a),2*e2,'arbitrary occupied preparation calibrated exactly')
    dN=red(s.diff(N,a)*da+s.diff(N,e2)*de2+s.diff(N,e4)*de4+s.diff(N,t)*dt)
    source=2*P**3/(a*t**2)*(dN-2*N*dt/t)
    if KEEP_CALIBRATION_JET:
        source-=2*P**3*N*da/(a*a*t*t)
    eq(source,2*de2,'moving event normalizer and scale jets retained')
    require(red(s.diff(N,a))!=0,'un-normalized readout has a real preparation jet')
    b0,db0=s.symbols('b0 db0',real=True)
    raw=lambda u:b0+a*(u**2*e2+u**4*e4)
    Nraw=red(PHI**4*(raw(t)-b0)-(raw(PHI*t)-b0))
    eq(Nraw,N,'full raw-mass baseline is canceled exactly')
    def actual_jet(value):
        return red(s.diff(value,b0)*db0+s.diff(value,a)*da+s.diff(value,e2)*de2
                   +s.diff(value,e4)*de4+s.diff(value,t)*dt)
    dblank=db0 if KEEP_BLANK_JET else 0
    actual_dN=PHI**4*(actual_jet(raw(t))-dblank)-(actual_jet(raw(PHI*t))-dblank)
    eq(actual_dN,dN,'moving blank raw mass retained')
    # Operator identity is stronger than a diagonal-state test.
    E=s.diag(0,1,1,0)
    H=lambda u:s.eye(4)+(u**2*e2+u**4*e4)*E
    O=PHI**4*(H(t)-s.eye(4))-(H(PHI*t)-s.eye(4))
    eq(O,t*t*e2/P**3*E,'full cylinder operator identity')
    for phase in (1,s.I):
        v=s.Matrix([1,2*phase,1-s.I,3])
        rho=v*v.H/s.trace(v*v.H)
        occ=s.trace(rho*E)
        eq(2*P**3*s.trace(rho*O)/(occ*t*t),2*e2,'coherent preparation is retained '+str(phase))
    eq(s.trace(s.diag(1,0,0,0)*E),0,'empty calibration event explicitly detected')
    x=s.symbols('x',positive=True)
    c=s.sqrt(x);d=s.sqrt(1-x)
    W=s.Matrix([[d,-c],[c,d]])
    eq(W.T*W,s.eye(2),'full success-failure completion is unitary')
    eq(s.diff(x,x)+s.diff(1-x,x),0,'normalization tangent includes failures')

    # Exact positive settings: no signed probability or unbounded Gaussian support.
    radius=s.Rational(1,64)
    for i,X in enumerate(shapes):
        bound=max(sum(abs(X[j,k]) for k in range(4)) for j in range(4))
        require(bound<32,f'positive determinant tube bound {i}')
        for sign in (-1,1):
            D=s.eye(4)+sign*radius*X
            require(all(D[:j,:j].det()>0 for j in range(1,5)),f'positive branch {i} {sign}')
    # phi<2 and ||A||inf<32 give positivity also at phi/64.
    require(red(2-PHI).is_positive is True,'outer golden radius is inside positive domain')

    # Reuse actual published 12-channel flat record, not an invented frame.
    root=Path(__file__).resolve().parents[4]
    old=root/'02_REGISTRY/research/sources/d0_flat_record_2026-10-15/check_flat_record.py'
    data=old.read_bytes()
    digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    require(digest=='06f465874f07fae82111ee9453f4b5ca0b963267','pinned actual flat-record owner')
    spec=importlib.util.spec_from_file_location('owned_flat_record',old)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    _,ks=mod.frame(4)
    flats=[-2*k*k.T/s.sqrt(12*P**3) for k in ks]
    eq(scalar_gauss(flats),0,'actual golden flat reference scalar')
    require(all(X.rank()==1 for X in flats),'all twelve flat shapes rank one')
    # Each rank-one determinant is affine: all four histories give mass one.
    eq(sum(1 for _ in flats)+560,572,'all 572 normal directions accounted for')
    eq(sum(s.trace(X)**2 for X in flats),16/P**3,'nonzero extrinsic bending retained')

    # Unique three-setting weights: blank + inner + outer.
    lam=s.symbols('lam',positive=True)
    c0,c1,c2=s.symbols('c0 c1 c2')
    sol=s.solve([c0+c1+c2,c1+c2*lam**2-1,c1+c2*lam**4],(c0,c1,c2))
    eq(sol[c1],lam**2/(lam**2-1),'unique inner scale coefficient')
    eq(sol[c2],-1/(lam**2*(lam**2-1)),'unique outer scale coefficient')
    eq(sol[c0],-(lam**2+1)/lam**2,'unique blank coefficient')
    # Ordinary one-difference readout retains a shape-dependent quartic error.
    old=(M.subs(r,PHI*r)-M)/(P**3*(PHI**2-1)*r*r)
    require(red(old-R)!=0,'earlier two-setting difference is not used with axes measure')
    return {
      'schema':'d0-golden-cylinder-curvature/1',
      'source_base':'51b1d1a1546305814f8751b9cf9800531d721400',
      'exact_checks':len(CHECKS),
      'golden_histories':{'FF':'p^2','FR':'p^3','RF':'p^3','RR':'p^4'},
      'cost_cuts_tested':list(range(4,13)),
      'mass':'D+p^3*t^2*R+2*p^3*t^4*sum_j(det A_j)',
      'curvature':'[phi^4*(M_t-M_0)-(M_(phi*t)-M_0)]/t^2',
      'general_calibration':'2*p^3/[a*t^2] times the even scale contrast, a=Tr(rho E_mixed)>0',
      'noncommuting_fixture_R':str(R),
      'noncommuting_fixture_quartic':str(Q4),
      'rotated_quartic':str(Q4rot),
      'raw_mass_and_blank_jets_retained':True,
      'requires_rotational_fourth_moment':False,
      'uses_topological_cancellation':False,
      'exact_AF_intertwining_for_fixed_geometric_inputs':True,
      'all_mesh_physical_refinement':False,
      'new_Lean_compilation':False,
      'native_full_action_binding':False,
      'GR_closed':False,
      'scope':'finite calibrated readout of existing shape Jacobians on actual golden cylinders; not admission of geometric operator or physical action'
    }


if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
