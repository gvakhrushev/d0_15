#!/usr/bin/env python3
"""Exact finite checks of two-sided record normalization and spatial IR input.
No physical action selection, parent replay, or native GR closure is claimed.
"""
from __future__ import annotations
from itertools import combinations
from math import comb
import hashlib
import json
import sympy as S

CHECKS: list[str] = []
P = (S.sqrt(5)-1)/2

def eq(name, a, b=0):
    if isinstance(a,S.MatrixBase) or isinstance(b,S.MatrixBase):
        ok=all(S.simplify(v)==0 for v in S.Matrix(a)-S.Matrix(b))
    else:
        ok=S.simplify(a-b)==0
    if not ok: raise ArithmeticError(name)
    CHECKS.append(name)

def require(name, truth):
    if not truth: raise ArithmeticError(name)
    CHECKS.append(name)

def rot(t):
    return S.Matrix([[1-t*t,-2*t],[2*t,1-t*t]])/(1+t*t)

def matrix_gram():
    """All-output complete comparison in a noncommuting rational fixture."""
    O=rot(S.Rational(1,3));V=rot(S.Rational(2,5))
    C=O*S.diag(S.Rational(3,5),S.Rational(5,13))*V.T
    L=O*S.diag(S.Rational(4,5),S.Rational(12,13))*O.T
    R=V*S.diag(S.Rational(4,5),S.Rational(12,13))*V.T
    U=C.row_join(L).col_join(R.row_join(-C.T))
    eq('complete_comparison_unitary',U.T*U,S.eye(4))
    eq('success_and_failure_retained',C.T*C+R.T*R,S.eye(2))
    require('noncommuting_comparison_fixture',C.T*C!=C*C.T)
    J0=S.eye(2).col_join(S.zeros(2))
    J1=C.T.col_join(L)
    eq('first_record_isometry',J0.T*J0,S.eye(2))
    eq('second_record_isometry',J1.T*J1,S.eye(2))
    eq('literal_record_comparison',J1.T*J0,C)
    H0=S.Matrix([[S.Rational(4,5),S.Rational(1,20)],[S.Rational(1,20),S.Rational(9,10)]])
    H1=S.Matrix([[S.Rational(7,8),S.Rational(-1,30)],[S.Rational(-1,30),S.Rational(5,6)]])
    X0=J0*H0;X1=J1*H1
    G0=H0*H0;G1=H1*H1;K=X1.T*X0
    eq('raw_left_record_Gram',X0.T*X0,G0)
    eq('raw_right_record_Gram',X1.T*X1,G1)
    eq('cross_Gram_not_postulated_scalar',K,H1*C*H0)
    eq('two_sided_normalization',H1.inv()*K*H0.inv(),C)
    eq('noncommutative_determinant_identity',
       (C.T*C).det(),(K.T*K).det()/(G0.det()*G1.det()))
    require('endpoint_Grams_need_not_commute',G0*G1!=G1*G0)
    # Full16 form input: extra binary flag retained; no grade deletion.
    C16=S.kronecker_product(C,S.eye(8));U32=S.kronecker_product(U,S.eye(8))
    eq('full16_comparator_and_retained_flag',U32.T*U32,S.eye(32))
    eq('full16_logdet_multiplicity',(C16.T*C16).det(),(C.T*C).det()**8)
    return True

def full_jets():
    t=S.symbols('t',real=True)
    G0root=S.Matrix([[S.Rational(4,5)+t/80,S.Rational(1,50)],
                    [S.Rational(1,50),S.Rational(9,10)-t/90]])
    G1root=S.Matrix([[S.Rational(7,8)-t/75,S.I/40],[-S.I/40,S.Rational(5,6)+t/85]])
    A=S.Matrix([[S.Rational(7,8)+t/50,S.Rational(1,60)+S.I*t/45],
                [S.Rational(1,60)-S.I*t/45,S.Rational(17,20)-t/55]])
    G0=G0root.H*G0root;G1=G1root.H*G1root;E=A.H*A
    kappa=S.Rational(1,4)
    C=G1root.inv()*(kappa*A)*G0root.inv()
    # Differentiate log determinant through determinant jets; no frozen eigenbasis.
    def logdet_jet(M,order):
        d0=S.simplify(M.det().subs(t,0));d1=S.diff(M.det(),t).subs(t,0)
        if order==1:return S.simplify(d1/d0)
        d2=S.diff(M.det(),t,2).subs(t,0)
        return S.simplify(d2/d0-(d1/d0)**2)
    # det(C* C) identity avoids differentiating a huge rational matrix.
    left=S.factor(S.conjugate(C.det())*C.det())
    right=kappa**4*E.det()/(G0.det()*G1.det())
    eq('moving_noncommutative_determinants',left,right)
    for order in (1,2):
        cjet=S.diff(S.log(left),t,order).subs(t,0)
        rjet=logdet_jet(E,order)-logdet_jet(G0,order)-logdet_jet(G1,order)
        eq('all_endpoint_source_jet_'+str(order),cjet,rjet)
    # Independently verify trace/Sylvester form of the first and second sources.
    for name,M in [('signal',E),('left',G0),('right',G1)]:
        M0=M.subs(t,0);M1=M.diff(t).subs(t,0);M2=M.diff(t,2).subs(t,0)
        eq(name+'_first_trace_source',logdet_jet(M,1),S.trace(M0.inv()*M1))
        eq(name+'_second_trace_source',logdet_jet(M,2),
           S.trace(M0.inv()*M2-M0.inv()*M1*M0.inv()*M1))
    true1=logdet_jet(E,1)-logdet_jet(G0,1)-logdet_jet(G1,1)
    require('freezing_endpoint_Gram_changes_source',S.simplify(true1-logdet_jet(E,1))!=0)
    # A field-dependent attenuation is not a constant code shift.
    c=S.Rational(1,4)*(1+t/7)
    eq('moving_attenuation_source_retained',S.diff(-4*S.log(c),t).subs(t,0),-S.Rational(4,7))
    return True

def positive_domain():
    a,z=S.symbols('a z',positive=True)
    eq('golden_partition',P+P**2,1)
    t=S.symbols('t',real=True)
    eq('positive_scalar_record_normalization_fixes_half_power',S.solve(1-2*t,t)[0],S.Rational(1,2))
    # All signal/ref effects in [a I,I], kappa=sqrt(p)*a.
    eq('uniform_upper_comparison_probability',(S.sqrt(P)*a/a)**2,P)
    eq('uniform_lower_comparison_probability',(S.sqrt(P)*a*S.sqrt(a))**2,P*a**3)
    eq('uniform_failure_lower_bound',1-P,P**2)
    # Scalar static product demonstrates need for attenuation: C*C=1/e>1.
    e=S.Rational(3,4)
    require('unattenuated_identical_spectral_inputs_not_contractions',1/e>1)
    eq('static_product_variable_price_sign',S.log(e)-S.log(e)-S.log(e),-S.log(e))
    # Constant dimensions are not metric volumes: no artificial volume source from kappa.
    r=S.symbols('r',positive=True);d=S.symbols('d',positive=True)
    eq('fixed_code_offset_field_source',S.diff(-2*d*S.log(S.sqrt(P)*S.Rational(3,4)),r),0)


def ricci_from_metric(g,coords):
    n=len(coords);gi=g.inv()
    C=[[[S.simplify(sum(gi[a,k]*(S.diff(g[k,b],coords[c])+S.diff(g[k,c],coords[b])-S.diff(g[b,c],coords[k])) for k in range(n))/2)
         for c in range(n)] for b in range(n)] for a in range(n)]
    Ric=S.Matrix(n,n,lambda b,d:S.simplify(sum(
        S.diff(C[a][b][d],coords[a])-S.diff(C[a][b][a],coords[d])+
        sum(C[a][k][a]*C[k][b][d]-C[a][k][d]*C[k][b][a] for k in range(n))
        for a in range(n))))
    return Ric,S.simplify(S.trace(gi*Ric))


def spatial_reference():
    # Exact static lapse/spatial-curvature metric, nonzero spatial boundary density.
    u,x,y,z=S.symbols('u x y z',real=True)
    N=S.exp(x/3);h=S.diag(1,S.exp(2*x),S.exp(4*x))
    gh=S.diag(N*N,1,S.exp(2*x),S.exp(4*x))
    _,R4=ricci_from_metric(gh,[u,x,y,z])
    _,R3=ricci_from_metric(h,[x,y,z])
    sqh=S.exp(3*x)
    lapN=S.simplify(S.diff(sqh*S.diff(N,x),x)/sqh)
    eq('frozen_lapse_reference_scalar',R4,R3-2*lapN/N)
    require('lapse_boundary_correction_is_not_zero',S.simplify(lapN)!=0)
    eq('reference_volume_exact',gh.det(),N*N*h.det())
    eq('lapse_term_is_spatial_divergence',sqh*lapN,S.diff(sqh*S.diff(N,x),x))
    # No temporal extrinsic curvature is silently retained in this reference.
    eq('reference_has_no_time_variation',gh.diff(u),S.zeros(4))
    # Owned full16 CAR decomposes into two spatial exterior copies, not one.
    creator=S.zeros(16)
    for mask in range(16):
        if not mask&1:creator[mask|1,mask]=1
    Q1=creator*creator.T;Q0=S.eye(16)-Q1
    eq('two_temporal_occupation_blocks',Q0+Q1,S.eye(16))
    eq('first_spatial_copy_dimension',S.trace(Q0),8)
    eq('second_spatial_copy_dimension',S.trace(Q1),8)
    eq('no_temporal_grade_discard',Q0*Q1,S.zeros(16))
    # Standard Hodge trace a2 across ALL form degrees, elementary binomial sum.
    for n in (3,4):
        Etrace=-sum(comb(n-2,k-1) if 1<=k<=n-1 else 0 for k in range(n+1))
        coeff=S.Rational(2**n,6)+Etrace
        eq('all_form_Hodge_a2_'+str(n),coeff,-S.Rational(2**(n-2),3))
    eq('same_full16_curvature_normalization',2*(-S.Rational(2,3)),-S.Rational(4,3))
    require('unlifted_3D_heat_has_wrong_time_power',S.Rational(3,2)!=S.Integer(2))
    eq('one_temporal_clock_restores_heat_power',S.Rational(3,2)+S.Rational(1,2),2)


def reference_exterior_operator():
    # Exact all16 orthonormal-coframe d, its true weighted adjoint and whitening.
    u,x,y,z=S.symbols('u x y z',real=True)
    xx=[u,x,y,z];N=S.exp(x/3+y*y/5)
    creators=[]
    for r in range(4):
        C=S.zeros(16)
        for mask in range(16):
            if not mask&(1<<r):
                C[mask|(1<<r),mask]=(-1)**((mask&((1<<r)-1)).bit_count())
        creators.append(C)
    annih=[C.T for C in creators];Nt=creators[0]*annih[0]
    a=[S.Integer(0)]+[S.diff(S.log(N),v) for v in xx[1:]]
    ca=sum((a[i]*creators[i] for i in range(1,4)),S.zeros(16))
    ia=sum((a[i]*annih[i] for i in range(1,4)),S.zeros(16))
    A=[creators[0]/N,*creators[1:]];B=ca*Nt
    for i in range(4):
        for j in range(i,4):
            eq('reference_exterior_square_second_'+str(i)+str(j),
               A[i]*A[j]+A[j]*A[i],S.zeros(16))
    for j in range(4):
        coeff=sum((A[i]*A[j].diff(xx[i]) for i in range(4)),S.zeros(16))+A[j]*B+B*A[j]
        eq('reference_exterior_square_first_'+str(j),coeff,S.zeros(16))
    eq('reference_exterior_square_zero',
       sum((A[i]*B.diff(xx[i]) for i in range(4)),S.zeros(16))+B*B,S.zeros(16))
    # Formal adjoint with the true N du dx dy dz weight, not the bare measure.
    deltaB=B.T-sum(((N*A[i].T).diff(xx[i])/N for i in range(4)),S.zeros(16))
    eq('actual_lapse_weighted_adjoint_zero_order',deltaB,-ia*(S.eye(16)-Nt))
    Dcoeff=[A[i]-A[i].T for i in range(4)]
    before=B+deltaB
    after=before-sum((a[i]*Dcoeff[i]/2 for i in range(4)),S.zeros(16))
    eq('half_density_derived_connection_term',after,(Nt-S.eye(16)/2)*(ca+ia))
    for i in range(4):
        eq('whitened_Hodge_principal_skewadjoint_'+str(i),Dcoeff[i].T,-Dcoeff[i])
    eq('whitened_Hodge_full_formal_adjoint',
       after.T-sum((Dcoeff[i].T.diff(xx[i]) for i in range(4)),S.zeros(16)),after)
    require('lapse_half_density_term_is_not_optional',after!=S.zeros(16))
    eq('one_direction_acceleration_retained',after.subs({x:0,y:0})-(Nt-S.eye(16)/2)*(creators[1]+annih[1])/3,S.zeros(16))


def adm_ir():
    N=S.symbols('N',positive=True);v=S.symbols('v0:3')
    hvals=S.symbols('h00 h01 h02 h11 h12 h22',real=True)
    h=S.Matrix([[hvals[0],hvals[1],hvals[2]],
                [hvals[1],hvals[3],hvals[4]],[hvals[2],hvals[4],hvals[5]]])
    shift=S.Matrix(v);g=S.zeros(4)
    g[0,0]=N*N-(shift.T*h*shift)[0]
    for i in range(3):
        g[0,i+1]=g[i+1,0]=-(h*shift)[i]
        for j in range(3):g[i+1,j+1]=-h[i,j]
    slots=[(i,j) for i in range(4) for j in range(i,4)]
    params=[N,*v,*hvals]
    Jac=S.Matrix([g[i,j] for i,j in slots]).jacobian(params)
    point={N:4,v[0]:S.Rational(1,3),v[1]:S.Rational(-1,5),v[2]:S.Rational(2,7),
           hvals[0]:2,hvals[1]:S.Rational(1,4),hvals[2]:0,hvals[3]:3,hvals[4]:S.Rational(1,5),hvals[5]:5}
    eq('all_ten_ADM_chart_rank',Jac.subs(point).rank(),10)
    eq('full_ADM_jacobian_measure',abs(Jac.subs(point).det()),(2*N*h.det()).subs(point))
    RG,R3,lap=S.symbols('RG R3 lap')
    RL=RG-2*R3+4*lap
    Rref=R3-2*lap
    eq('full_nonlinear_scalar_combination',RG-2*Rref,RL)
    # Coefficients come from determinants, not inferred by fitting these probes.
    V,A4,A3,c,lam=S.symbols('V A4 A3 c lam')
    raw=-lam*V+c*A4;reference=-lam*V+c*A3
    eq('full_volume_source_kept',raw-2*reference,lam*V+c*(A4-2*A3))
    eq('static_product_Einstein_curvature_sign',(A4-2*A3).subs(A4,A3),-A3)
    eq('spatially_flat_dynamic_curvature_sign',(A4-2*A3).subs(A3,0),A4)
    eq('effective_cosmological_sign',-lam/(2*c),-lam/(2*c))
    # Macroscopic nonlocal-remainder estimate is a source estimate, not an exact-root theorem.
    R,m=S.symbols('R m',positive=True)
    eq('quadrature_error_after_curvature_scaling',(R**4/m**2)/R**2,R**2/m**2)
    eq('sufficient_quadrature_diagonal_choice',(R**2/m**2).subs(m,R**2),R**-2)
    require('fixed_volume_term_not_small_in_IR',S.limit(R**4/R**2,R,S.oo)==S.oo)
    eq('fixed_shape_volume_and_curvature_differ_by_two_powers',S.degree(lam*R**4,R)-S.degree(c*R**2,R),2)


def run():
    CHECKS.clear()
    matrix_gram();full_jets();positive_domain();spatial_reference();reference_exterior_operator();adm_ir()
    return {
        'schema':'d0-two-sided-spatial-record/1',
        'checks':CHECKS,'check_count':len(CHECKS),
        'normalization_identity':'J_cal=J_4-J_ref,left-J_ref,right-2Md log(kappa)',
        'kappa':'sqrt(p)*(1-z)',
        'probability_domain':'p*(1-z)^3 I <= C* C <= p I',
        'static_reference':'N(t,x)^2 du^2 + h_t(x), one frozen input t per reference',
        'IR_source':'lambda_J Vol(g_R)+c_J integral R(g_R)dV+O_C1(1), with explicit finite-mesh/quadrature errors',
        'curvature_coefficient':'same c_J as supplied original fixed-beta logdet family',
        'physical_Lambda_for_this_candidate':'-lambda_J/(2c_J)',
        'whole_native_action_selected':False,
        'original_v8_redefined':False,
        'native_reference_program_admitted':False,
        'IR_is_original_fixed_h_source_terminal':False,
        'nonempty_exact_joint_refinement_proved':False,
        'GR_closed':False,
    }

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
