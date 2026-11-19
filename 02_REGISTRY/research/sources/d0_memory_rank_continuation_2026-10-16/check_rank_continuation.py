#!/usr/bin/env python3
"""Exact new source-capacity and rank-stratified continuation identities.
Consumes the literal prior CAR definitions; never runs its old suite.
No claim of a new curved native root or a physically chosen preparation law.
"""
from pathlib import Path
import hashlib, importlib.util, json
from itertools import combinations
import sympy as s
ROOT=Path(__file__).resolve().parents[4]
PARENT=ROOT/'02_REGISTRY/research/sources/d0_native_memory_source_2026-10-16/check_memory_source.py'
EXPECTED_PARENT='dbffbc21bd1e7d4f194eca4dbc0f9819b0839d6b233a2a74460155d8ba7de26b'
checks=[]
def require(name,v):
    if not bool(v): raise ArithmeticError(name)
    checks.append(name)
require('literal_CAR_parent_exact_bytes',hashlib.sha256(PARENT.read_bytes()).hexdigest()==EXPECTED_PARENT)
spec=importlib.util.spec_from_file_location('owned_memory_source_definitions',PARENT)
o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
A,B=o.A,o.B
I=s.eye(16)
def red(v): return o.reduce(v)
def eq(name,x,y=0):
    if isinstance(x,s.MatrixBase) or isinstance(y,s.MatrixBase):
        good=all(red(v)==0 for v in s.Matrix(x)-s.Matrix(y))
    else:good=red(x-y)==0
    require(name,good)

def source_capacity():
    F=(A-B)*s.eye(4)+B*s.ones(4);u=[F.row(i).T for i in range(4)]
    # Physical sources are c_L(A-B)(A+3B) times these dimensionful operators.
    g=[s.Matrix([0,0,-1,1]),s.Matrix([0,1,0,-1]),s.Matrix([0,-1,1,0])]
    J=[o.gamma(g[i])*o.kappa(u[i+1]) for i in range(3)]
    # A single exact grade-four tangent can disprove the faithful-fibre
    # condition M_v in span{I,B_r}; no 252-direction enumeration is needed.
    majoranas=[]
    for r in range(2):
        c=o.C[r]
        majoranas.extend((c+c.T,s.I*(c-c.T)))
    W=majoranas[0]*majoranas[1]*majoranas[2]*majoranas[3]
    eq('grade_four_obstruction_witness_is_hermitian',W,W.H)
    eq('grade_four_obstruction_witness_squares_to_identity',W*W,I)
    eq('grade_four_obstruction_witness_is_trace_free',s.trace(W),0)
    for i,Ji in enumerate(J):
        eq('grade_four_obstruction_witness_source_neutral_'+str(i),s.trace(W*Ji),0)
    chi=s.zeros(16,1);chi[1]=1/s.sqrt(2);chi[15]=-1/s.sqrt(2)
    eq('own_seed_whitening_and_normalization',(chi.T*chi)[0],1)
    for i,Ji in enumerate(J):
        eq('full_symmetric_source_'+str(i),Ji,Ji.T)
        eq('seed_source_zero_'+str(i),(chi.T*Ji*chi)[0],0)
    G=s.Matrix(3,3,lambda i,j:(chi.T*J[i]*J[j]*chi)[0])
    d=A*A+3*B*B;off=A*A-4*A*B-B*B
    Gformula=(2*d-off)*s.eye(3)+off*s.ones(3)
    eq('actual_source_seed_covariance',G,Gformula)
    eq('covariance_parallel_eigenvalue',G*s.ones(3,1),4*(A-B)**2*s.ones(3,1))
    q=s.Matrix([1,-1,0]);eq('covariance_transverse_eigenvalue',G*q,(A*A+4*A*B+7*B*B)*q)
    h=s.Matrix(s.symbols('h0:3',real=True));D=sum((h[i]*J[i] for i in range(3)),s.zeros(16));v=D*chi
    den=1+(h.T*G*h)[0]
    eq('source_preparation_norm',(chi+v).dot(chi+v),den)
    for i,Ji in enumerate(J):
        eq('all_symmetric_cubic_moments_zero_'+str(i),(v.T*Ji*v)[0],0)
        eq('exact_pure_source_numerator_'+str(i),((chi+v).T*Ji*(chi+v))[0],2*(G*h)[i])
    # General inverse reduces to this scalar norm identity; no target fitted to Einstein.
    t=s.symbols('t',positive=True);qvar=1-t*t
    norm=qvar/(1+t)**2
    eq('exact_ellipsoid_inverse',2/(1+t)/(1+norm),1)
    # The old order/history forces are strictly inside this attainable ellipsoid.
    direction=s.Matrix([2*B,-A,-A])
    inverse_quad=s.factor((direction.T*G.inv()*direction)[0])
    ratio=(A*A+4*A*B+5*B*B)/(A*A+4*A*B+7*B*B)
    require('actual_history_ellipsoid_norm',s.cancel(inverse_quad-ratio)==0)
    eq('golden_uniform_source_margin',1-4*o.p**3,o.p**6)
    require('ellipsoid_ratio_margin_exact',s.cancel(1-ratio-2*B*B/(A*A+4*A*B+7*B*B))==0)
    # General source pencil has rank <=2 in its actual Majorana coefficient.
    C=sum((h[i]*g[i]*u[i+1].T for i in range(3)),s.zeros(4))
    eq('source_coeff_no_time_row',C.row(0),s.zeros(1,4))
    eq('source_coeff_spatial_row_sum',C.row(1)+C.row(2)+C.row(3),s.zeros(1,4))
    pencil=sum((h[i]*J[i] for i in range(3)),s.zeros(16))
    Csource=sum((C[i,j]*o.gamma(s.eye(4)[:,i])*o.kappa(s.eye(4)[:,j]) for i in range(4) for j in range(4)),s.zeros(16))
    eq('full_clifford_source_pencil',pencil,Csource)
    t2=s.expand(s.trace(C*C.T));det2=s.expand((t2*t2-s.trace((C*C.T)**2))/2)
    square=pencil*pencil
    eq('complete_sixteen_state_quartic_identity',square*square-2*t2*square+(t2*t2-4*det2)*I,s.zeros(16))
    # Actual full determinant at a rational nonzero multi-source setting.
    fix={A:s.Rational(3,5),B:s.Rational(1,10),h[0]:s.Rational(1,3),h[1]:s.Rational(-2,5),h[2]:s.Rational(4,7)}
    z=s.symbols('z');T=s.factor(t2.subs(fix));D2=s.factor(det2.subs(fix))
    eq('full_characteristic_polynomial_multiplicities',pencil.subs(fix).charpoly(z).as_expr(),(z**4-2*T*z*z+T*T-4*D2)**4)
    # Exact nonzero pure preparation with exact recovered source, not randomized tomography.
    Gf=G.subs({A:s.Rational(3,5),B:s.Rational(1,10)})
    hf=s.Matrix([s.Rational(1,11),s.Rational(-1,13),s.Rational(2,17)])
    Jf=[Ji.subs({A:s.Rational(3,5),B:s.Rational(1,10)}) for Ji in J]
    vf=chi+sum((hf[i]*Jf[i]*chi for i in range(3)),s.zeros(16,1));normf=s.simplify((vf.T*vf)[0])
    state=vf/s.sqrt(normf);want=2*Gf*hf/(1+(hf.T*Gf*hf)[0])
    actual=s.Matrix([(state.T*Ji*state)[0] for Ji in Jf])
    eq('nonzero_exact_pure_source_witness',actual,want)
    eq('all_sixteen_prepared_state_kept',state.rows,16)
    # The already-owned stationary preparation fibre supplies a new second-order test.
    neutral=chi*chi.T-I/16
    for i,Ji in enumerate(J):eq('memory_fibre_source_neutral_'+str(i),s.trace(neutral*Ji),0)
    Mgood=3*I+J[0]+2*J[1]-J[2]
    eq('full_memory_fibre_second_order_neutrality',s.trace(neutral*Mgood),0)
    eq('fullrank_fibre_detects_quadratic_obstruction',s.trace(neutral*neutral),s.Rational(15,16))
    eq('same_operator_allowed_by_pure_rank_test',neutral*chi,s.Rational(15,16)*chi)
    zeroform=s.eye(16)[:,0]
    for i,Ji in enumerate(J):eq('zeroform_is_true_pure_fibre_tangent_'+str(i),(zeroform.T*Ji*chi)[0],0)
    Mpure=zeroform*chi.T+chi*zeroform.T
    eq('pure_fibre_still_has_a_real_obstruction',Mpure*chi,zeroform)
    eq('pure_obstruction_detected_by_allowed_path',(zeroform.T*Mpure*chi)[0],1)
    return {'physical_source_units':'c_L (A-B)(A+3B)',
            'attainable_pure_source':'y^T Gamma^-1 y <= 1',
            'history_source_margin':'at least p^6 in normalized ellipsoid',
            'full_support_function':'sqrt(tr(C C^T)+2 sqrt(sum_2x2_minors(C)^2))',
            'whole_source_spectrum':'four signs +/-s1+/-s2, each multiplicity 4'}

def rank_geometry():
    # All calculations use full shell and reference, no deletion of empty modes.
    r=4;k=2;ref=4;C0=s.zeros(r,ref)
    for i in range(k):C0[i,i]=1/s.sqrt(k)
    occupied=s.diag(1,1,0,0);perp=s.eye(r)-occupied
    x=s.symbols('x0:32',real=True)
    Z=s.Matrix(r,ref,lambda i,j:x[2*(i*ref+j)]+s.I*x[2*(i*ref+j)+1])
    drho=Z*C0.H+C0*Z.H
    image=[]
    for i in range(r):
        image.append(s.re(drho[i,i]))
        for j in range(i+1,r): image.extend([s.re(drho[i,j]),s.im(drho[i,j])])
    unnorm_rank=s.Matrix(image).jacobian(x).rank()
    eq('full_rank_stratum_density_derivative_rank',unnorm_rank,2*r*k-k*k)
    eq('normalized_rank_stratum_dimension',unnorm_rank-1,11)
    # An arbitrary trace-zero Hermitian density tangent with no empty-empty block.
    t=s.symbols('t0:12',real=True)
    S=s.zeros(r);S[0,0]=t[0];S[1,1]=-t[0];S[0,1]=t[1]+s.I*t[2];S[1,0]=s.conjugate(S[0,1])
    off=3
    for i in range(2,r):
        for j in range(k):S[i,j]=t[off]+s.I*t[off+1];S[j,i]=s.conjugate(S[i,j]);off+=2
    DeltaC=s.zeros(r,ref);DeltaC[:k,:k]=s.sqrt(k)*S[:k,:k]/2;DeltaC[k:,:k]=s.sqrt(k)*S[k:,:k]
    eq('all_density_tangents_lift_to_real_amplitudes',DeltaC*C0.H+C0*DeltaC.H,S)
    eq('normalization_tangent_retained',s.re(s.trace(C0.H*DeltaC)),0)
    birth=s.zeros(r,ref);birth[2,2]=1
    eq('rank_birth_is_invisible_to_first_density',birth*C0.H+C0*birth.H,s.zeros(r))
    eq('rank_birth_changes_second_density',s.trace(birth*birth.H),1)
    # The shell constraint is T_k(X), not the full128 trace-free compression.
    z=s.symbols('z0:16',real=True)
    X=s.zeros(4);at=0
    for i in range(4):
        X[i,i]=z[at];at+=1
        for j in range(i+1,4):X[i,j]=z[at]+s.I*z[at+1];X[j,i]=s.conjugate(X[i,j]);at+=2
    ek=s.trace(occupied*X)/k
    Tk=occupied*X*occupied-ek*occupied+perp*X*occupied+occupied*X*perp
    eq('all_occupied_shell_equations',Tk*C0,(X-ek*s.eye(r))*C0)
    eq('true_shell_constraint_trace',s.trace(Tk),0)
    eq('true_shell_constraint_no_empty_empty_block',perp*Tk*perp,s.zeros(r))
    eq('true_saddle_pairing',s.trace(S*Tk),s.trace(S*X))
    fake=s.diag(0,0,2,3)
    eq('empty_shell_is_not_falsely_fixed',fake*C0,s.zeros(r,ref))
    require('fullrank_trace_condition_is_stronger',fake-s.trace(fake)*s.eye(r)/r!=s.zeros(r))
    eq('actual_rank8_constraint_count',2*128*8-8*8-1,1983)
    eq('actual_fullrank_constraint_count',128*128-1,16383)
    eq('actual_rank8_visible_dimension_saved',16383-1983,14400)
    eq('rank8_invisible_amplitude_tangent_count',2*128*128-1-1983,30784)
    eq('rank8_reference_orbit_dimension',2*8*128-8*8,1984)
    eq('rank8_true_birth_coordinates',2*(128-8)*(128-8),28800)
    return {'occupied_rank':8,'shell_dimension':128,'reference_dimension':128,
            'shell_constraint_target_dimension':1983,'previous_full_rank_constraints':16383,
            'zero_first_density_amplitudes':30784,'rank_birth_directions_not_gauge':28800}

def obstruction():
    # Exact eigenbranch with moving shell support and an indefinite outer resolvent.
    t=s.symbols('t',real=True)
    R=s.Matrix([[(1-t*t)/(1+t*t),-2*t/(1+t*t)],[2*t/(1+t*t),(1-t*t)/(1+t*t)]])
    U=s.eye(4);U[:2,:2]=R
    V=s.eye(4);V[0,0]=V[2,2]=(1-t*t)/(1+t*t);V[2,0]=2*t/(1+t*t);V[0,2]=-2*t/(1+t*t)
    W=V*U;Delta=W*s.diag(2,2+t,0,5)*W.T;eps=2
    P=s.eye(4)[:,:2];Q=s.eye(4)[:,2:]
    M=Delta-eps*s.eye(4);Gq=(Q.T*M*Q).inv();J=P-Q*Gq*Q.T*Delta*P
    E=P.T*M*P-P.T*Delta*Q*Gq*Q.T*Delta*P
    E0=E.subs(t,0);E1=E.diff(t).subs(t,0).applyfunc(s.simplify);E2=E.diff(t,2).subs(t,0).applyfunc(s.simplify)
    psi=W[:,0];C=P.T*psi;C0=C.subs(t,0);C1=C.diff(t).subs(t,0)
    eq('old_degenerate_shell_retained',E0,s.zeros(2))
    eq('rankfree_first_eigen_jet',E1*C0,s.zeros(2,1))
    eq('complete_rankfree_second_eigen_jet',E2*C0+2*E1*C1,s.zeros(2,1))
    require('freeze_shell_amplitude_fails_second_order',E2*C0!=s.zeros(2,1))
    eq('entire_exact_branch_reconstructed',(J*C-psi).applyfunc(s.cancel),s.zeros(4,1))
    eq('entire_exact_branch_norm',(psi.T*psi)[0],1)
    # Second Feshbach jet includes the actual inverse on both spectral sides.
    X=Delta.diff(t).subs(t,0);Y=Delta.diff(t,2).subs(t,0)
    Rq=Q*((Q.T*(Delta.subs(t,0)-2*s.eye(4))*Q).inv())*Q.T
    eq('actual_second_Feshbach_curvature',E2,P.T*(Y-2*X*Rq*X)*P)
    require('both_resolvent_signs_remain',Rq[2,2]<0<Rq[3,3])
    # Crossing of a transverse eigenvalue is NOT a bifurcation when memory is varied too.
    a,z=s.symbols('a z',real=True)
    S=a*z*z/2+z**4/4
    eq('whole_trivial_critical_fibre',s.Matrix([s.diff(S,a),s.diff(S,z)]).subs(z,0),s.zeros(2,1))
    eq('transverse_Hessian_crosses',s.diff(S,z,2).subs(z,0),a)
    eq('full_preparation_row_blocks_fake_branch',s.diff(S,a),z*z/2)
    eq('explicit_quadratic_bifurcation_obstruction',s.diff(S,a,z,z),1)
    # Algebraic source block: kernel projection is necessary AND sufficient for second-jet correction.
    H=s.diag(0,2,-3);b=s.Matrix([0,4,6]);acc=s.Matrix([7,-2,2])
    eq('second_jet_range_equation_exact',H*acc+b,s.zeros(3,1))
    bad=s.Matrix([1,4,6]);eq('obstruction_independent_of_acceleration',(s.Matrix([[1,0,0]])*(H*acc+bad))[0],1)
    return {'all_rank_second_matter_equation':'E2 C0+2 E1 C1=0',
            'full_joint_second_jet':'H eta + D^3 S[xi,xi,.]=0',
            'necessary_and_sufficient_formal_condition':'projection to ker(H) of D^3 S[xi,xi,.] vanishes',
            'convergent_native_curved_branch_proved':False}

def run():
    cap=source_capacity();rank=rank_geometry();obs=obstruction()
    return {'schema':'d0-memory-rank-continuation/1','exact_checks':len(checks),'checks':checks,
            'source_capacity':cap,'rank_geometry':rank,'nonlinear_obstruction':obs,
            'original_full_carrier_changed':False,'native_price_changed':False,
            'positive_source_preparation_is_a_derived_native_law':False,
            'new_curved_native_stationary_solution':False,'physical_GR_closed':False}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
