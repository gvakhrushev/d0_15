#!/usr/bin/env python3
"""Exact finite accounting checks; no physical operation or Info admission.

The literal all128 Kraus expansion is owned by check_paid_port_cost.py.
This checker consumes its exact Phi_t and checks the new clock/Schur/source
identities, including arbitrary-carrier one/two-round formulas.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import time
from pathlib import Path
import sympy as s

checks: dict[str, bool] = {}

def eq(name, a, b):
    value = s.cancel(s.expand(a - b))
    if value != 0:
        raise AssertionError(f'{name}: residual {value}')
    checks[name] = True

def nonzero(name, a):
    value = s.cancel(a)
    if value == 0:
        raise AssertionError(f'{name}: unexpectedly zero')
    checks[name] = True

def mat_eq(name, a, b):
    if a.shape != b.shape:
        raise AssertionError((name, a.shape, b.shape))
    for e in a-b:
        if s.cancel(s.expand(e)) != 0:
            raise AssertionError((name, e))
    checks[name] = True

def check_joint_schur():
    # Eliminated two-stage DAG; nonzero eliminated boundaries make all three
    # reduced contributions material. y moves actual algebraic inputs.
    y, u = s.symbols('y u')
    N = s.Matrix([[0,0],[y,0]])
    TRR=s.Matrix([[y/31]])
    TRE=s.Matrix([[s.Rational(1,5),s.Rational(1,7)]])
    TER=s.Matrix([[y/11],[s.Rational(1,13)]])
    T=TRR.row_join(TRE).col_join(TER.row_join(N))
    rR=s.Matrix([s.Rational(2,3)])
    rE=s.Matrix([y/17,s.Rational(1,19)])
    ellR=s.Matrix([[s.Rational(3,5)]])
    ellE=s.Matrix([[s.Rational(2,7),y/23]])
    r=rR.col_join(rE)
    ell=ellR.row_join(ellE)
    G=(s.eye(2)-N).inv()
    F=TRR+TRE*G*TER
    re=rR+TRE*G*rE
    le=ellR+ellE*G*TER
    zac=(ellE*G*rE)[0]
    R=(s.eye(3)-T).inv()
    Z=(ell*R*r)[0]
    Ze=zac+(le*(s.eye(1)-F).inv()*re)[0]
    eq('acyclic_internal_determinant', (s.eye(2)-N).det(), 1)
    eq('full_schur_determinant', (s.eye(3)-T).det(), (s.eye(1)-F).det())
    eq('full_schur_open_boundary', Z, Ze)
    eq('full_schur_open_source', s.diff(Z,y), s.diff(Ze,y))
    eq('joint_closed_open_determinant', (s.eye(3)-T-u*r*ell).det(),
       (s.eye(3)-T).det()*(1-u*Z))
    dZ=(ell.diff(y)*R*r+ell*R*r.diff(y)+ell*R*T.diff(y)*R*r)[0]
    eq('full_resolvent_source',s.diff(Z,y),dZ)
    naive=(ellR*(s.eye(1)-F).inv()*rR)[0]
    nonzero('dropping_transformed_boundaries_loses_source',
            s.diff(Z-naive,y).subs(y,s.Rational(1,2)))
    nonzero('direct_acyclic_boundary_source_is_real',s.diff(zac,y).subs(y,s.Rational(1,2)))


def check_weighted_cycle():
    a,b,c=s.symbols('a b c')
    K0=s.Matrix([[1,1],[0,1]])
    K1=s.Matrix([[0,-1],[1,0]])
    K2=s.Matrix([[1,0],[1,1]])
    T=s.zeros(6)
    T[2:4,0:2]=a*K0
    T[4:6,2:4]=b*K1
    T[0:2,4:6]=c*K2
    F=K2*K1*K0
    ze=a*b*c
    M=s.eye(2)-ze*F
    eq('weighted_all_clock_first_return', (s.eye(6)-T).det(), M.det())
    source=(M.inv()*F*s.diff(ze,a)).trace()
    eq('weighted_fugacity_source_retained',-s.diff(M.det(),a)/M.det(),source)
    # Rectangular stages, to catch an accidental equal-dimension premise.
    A=s.Matrix([[1],[2]])
    B=s.Matrix([[1,0],[0,1],[1,1]])
    C=s.Matrix([[1,-1,2]])
    Trect=s.zeros(6)
    Trect[1:3,0:1]=a*A
    Trect[3:6,1:3]=b*B
    Trect[0:1,3:6]=c*C
    eq('rectangular_clock_first_return',(s.eye(6)-Trect).det(),1-ze*(C*B*A)[0])


def check_actual_native_one_two_rounds():
    # Consume exact native trace identities from the full128 Kraus owner.
    # R,G,H remain independent: this is not a scalar-shell specialization.
    x,p,e,R,G,H,u=s.symbols('x p e R G H u')
    ax=1+p*(x-1)  # equals p^2+p*x on the Golden root.
    q1=x*(1+e*p*(x-1)*R)
    R1=x*(R+e*(ax*G-H))
    q2=s.expand(x*(q1+e*p*(x-1)*R1))
    claimed=x**2*(1+2*p*e*(x-1)*R+p*e**2*(x-1)*(ax*G-H))
    eq('actual_native_Z2_full_carrier',q2,claimed)
    C1=1+p*e*R
    C2=2+2*p*e*R+p*e**2*(G-H)
    eq('actual_native_one_round_cost',(x*s.diff(q1,x)).subs(x,1),C1)
    eq('actual_native_two_round_cost',(x*s.diff(q2,x)).subs(x,1),C2)
    e1,Rd,Gd,Hd=s.symbols('e1 Rd Gd Hd')
    dy=lambda f: sum(s.diff(f,v)*dv for v,dv in [(e,e1),(R,Rd),(G,Gd),(H,Hd)])
    expected=2*p*(e1*R+e*Rd)+p*(2*e*e1*(G-H)+e**2*(Gd-Hd))
    eq('actual_native_two_round_full_source',dy(C2),expected)
    eq('native_field_mark_derivatives_commute',(x*s.diff(dy(q2),x)).subs(x,1),expected)
    # K=-log(1-u Z): partial_t=-x partial_x; no choice of physical action.
    kt=-u*x*s.diff(q2,x)/(1-u*q2)
    eq('joint_unmarked_normalizer',q2.subs(x,1),1)
    eq('joint_marked_cost_insertion',kt.subs(x,1),-u*C2/(1-u))
    eq('joint_mixed_source_survives',dy(kt).subs(x,1),-u*expected/(1-u))
    eq('joint_moving_boundary_fugacity',s.diff(kt.subs(x,1),u),-C2/(1-u)**2)
    nonzero('scalar_clock_replacement_loses_native_cost',C2-2)
    lam=s.symbols('lambda')
    eq('native_two_round_scalar_shell_specialization',
       q2.subs({R:lam,G:lam**2,H:lam**2}),
       x**2*(1+p*e*lam*(x-1))**2)


def check_actual_native_scalar_shell_clock():
    # This is the exact invariant ORIGINAL full16 shell trace factor, not a
    # scalar replacement for the arbitrary-carrier channel.
    x,r,u=s.symbols('x r u')
    k=x*(1+r*(x-1))
    for n in (1,2,3,4):
        A=s.zeros(n+1)
        for j in range(n): A[j+1,j]=k
        initial=s.zeros(n+1,1); initial[0]=1
        final=s.zeros(1,n+1); final[0,n]=1
        R=(s.eye(n+1)-A).inv()
        Z=(final*R*initial)[0]
        eq(f'native_shell_clock_{n}_all_histories',Z,k**n)
        eq(f'native_shell_clock_{n}_joint_determinant',
           (s.eye(n+1)-A-u*initial*final).det(),1-u*k**n)
        eq(f'native_shell_clock_{n}_cost',(x*s.diff(Z,x)).subs(x,1),n*(1+r))
        eq(f'native_shell_clock_{n}_source',
           s.diff((x*s.diff(Z,x)).subs(x,1),r),n)
        insertion=(final*R*A.diff(x)*R*initial)[0]
        eq(f'native_shell_clock_{n}_marked_resolvent',s.diff(Z,x),insertion)


def check_full_work_marker_scope():
    y,z=s.symbols('y z')
    W=s.Matrix([[1-y*y,-2*y],[2*y,1-y*y]])/(1+y*y)
    E=s.diag(s.Rational(1,5),s.Rational(3,4))
    F=W.T*E*W
    mat_eq('fixed_marker_full_work_unitary',W.T*W,s.eye(2))
    eq('fixed_marker_full_work_isospectral',
       (s.eye(2)-z*F).det(),(s.eye(2)-z*E).det())
    K=W.T*W.diff(y)
    mat_eq('fixed_marker_source_commutator',F.diff(y),F*K-K*F)
    nonzero('fixed_marker_prepared_source_can_vary',s.diff(F[0,0],y).subs(y,s.Rational(1,3)))


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--native-proof',type=Path,
                        default=Path(__file__).with_name('paid_port_history.md'))
    parser.add_argument('--output',type=Path,
                        help='Optional explicit receipt destination; otherwise stdout only.')
    args=parser.parse_args()
    start=time.perf_counter()
    check_joint_schur()
    check_weighted_cycle()
    check_actual_native_one_two_rounds()
    check_actual_native_scalar_shell_clock()
    check_full_work_marker_scope()
    result={
        'status':'PASS','check_count':len(checks),'checks':checks,
        'elapsed_seconds':round(time.perf_counter()-start,3),
        'proof_sha256':sha(Path(__file__).with_name('clock_source_reduction.md')),
        'checker_sha256':sha(Path(__file__)),
        'native_proof_sha256':sha(args.native_proof) if args.native_proof else None,
        'scope':[
            'Exact Schur/clock/source identities and native all128 Phi_t specialization.',
            'Literal native Kraus expansion is separately checked by check_paid_port_cost.py.',
            'No complete Info selection, physical reset, new price or GR closure asserted.'
        ]}
    if args.output is not None:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
