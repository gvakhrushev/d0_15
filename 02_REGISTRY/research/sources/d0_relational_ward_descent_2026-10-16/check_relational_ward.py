#!/usr/bin/env python3
"""Exact checks: complete-experiment pullback, Ward blocks, metric selector.
This does not select the physical D0 action or prove GR/refinement.
"""
from __future__ import annotations
from itertools import combinations
import json
import sympy as S

CHECKS: list[str] = []
ETA = S.diag(1, -1, -1, -1)

def eq(name, left, right=0):
    if isinstance(left, S.MatrixBase) or isinstance(right, S.MatrixBase):
        valid = all(S.cancel(S.expand(z)) == 0 for z in S.Matrix(left)-S.Matrix(right))
    else:
        valid = S.simplify(left-right) == 0
    if not valid:
        raise ArithmeticError(name)
    CHECKS.append(name)

def require(name, condition):
    if not condition:
        raise ArithmeticError(name)
    CHECKS.append(name)

def substitute(matrix, variables, values):
    return matrix.subs(dict(zip(variables, values)), simultaneous=True)

def exterior(A):
    out = S.zeros(16)
    for degree in range(5):
        indices = list(combinations(range(4), degree))
        for a in indices:
            for b in indices:
                i, j = sum(1 << q for q in a), sum(1 << q for q in b)
                out[i, j] = A.extract(a, b).det() if a else 1
    return out

def creator(v):
    out = S.zeros(16)
    for r in range(4):
        for mask in range(16):
            if not mask & (1 << r):
                out[mask | (1 << r), mask] = v[r]*(-1)**((mask & ((1 << r)-1)).bit_count())
    return out

def pullback():
    x = S.Matrix(S.symbols('x0:4', real=True))
    y = S.Matrix(S.symbols('y0:4', real=True))
    t = S.symbols('t', real=True)
    shear = x[1]**2 + x[1]*x[2]
    f = S.Matrix([x[0]+t*shear, x[1], x[2], x[3]])
    X = S.Matrix([y[0]-t*(y[1]**2+y[1]*y[2]), y[1], y[2], y[3]])
    Jf, JX = f.jacobian(x), X.jacobian(y)
    eq('opposite_embedding_restores_every_point', substitute(f,x,X), y)
    eq('opposite_embedding_restores_every_tangent', substitute(Jf,x,X)*JX, S.eye(4))
    e = S.Matrix([[2+x[1]/5,x[2]/7,0,0], [0,3+x[0]/11,x[3]/13,0],
                  [0,0,2+x[2]/17,x[1]/19], [0,0,0,3+x[3]/23]])
    eprime = substitute(e,x,f)*Jf
    label_e = (substitute(eprime,x,X)*JX).applyfunc(S.cancel)
    ebase = substitute(e,x,y)
    eq('full_coframe_pullback', label_e, ebase)
    eq('full_metric_pullback', label_e.T*ETA*label_e, ebase.T*ETA*ebase)
    eq('inverse_coframe_and_all_creator_coefficients', label_e.inv(), ebase.inv())
    require('frozen_embedding_changes_coframe', substitute(eprime,x,y)!=ebase)
    q=x[0]/10
    n=S.Matrix([(1+q*q)/(1-q*q),2*q/(1-q*q),0,0])
    nlabel=substitute(substitute(n,x,f),x,X).applyfunc(S.cancel)
    nbase=substitute(n,x,y)
    eq('moving_observer_is_not_frozen',nlabel,nbase)
    h=lambda a: -ETA+2*ETA*a*a.T*ETA
    eq('positive_observer_pairing_pullback',h(nlabel),h(nbase))
    # Noncommuting connection one-form; equality of its path generators gives
    # equality of path-ordered proper transports, not of a first-order proxy.
    B01=S.zeros(4);B01[0,1]=B01[1,0]=1
    B02=S.zeros(4);B02[0,2]=B02[2,0]=1
    J12=S.zeros(4);J12[1,2]=1;J12[2,1]=-1
    Om=[(1+x[1])*B01+x[2]*J12,(1+x[0])*B02,x[0]*J12,B01/7]
    require('actual_connection_generators_noncommute',Om[0]*Om[1]!=Om[1]*Om[0])
    Op=[sum((substitute(Om[a],x,f)*Jf[a,r] for a in range(4)),S.zeros(4)) for r in range(4)]
    for r in range(4):
        label=sum((substitute(Op[a],x,X)*JX[a,r] for a in range(4)),S.zeros(4))
        eq('ordered_path_generator_'+str(r),label,substitute(Om[r],x,y))
        eq('path_generator_first_jet_'+str(r),label.diff(t),S.zeros(4))
        eq('path_generator_second_jet_'+str(r),label.diff(t,2),S.zeros(4))
    # All grades and two independent reference columns are explicitly retained.
    C=S.Matrix(16,2,lambda i,j:S.Rational((i+2)*(j+1),31)+x[(i+j)%4]/(i+j+7))
    Cback=substitute(substitute(C,x,f),x,X)
    eq('all_sixteen_grades_and_reference_columns',Cback,substitute(C,x,y))
    eq('full_preparation_normalizer',S.trace(Cback.T*Cback),S.trace(substitute(C,x,y).T*substitute(C,x,y)))
    # Density, not an invariant coordinate scalar: include its actual Jacobian.
    mu=1+x[0]**2+x[2]**2
    muprime=substitute(S.Matrix([[mu]]),x,f)[0]*Jf.det()
    muback=muprime.subs(dict(zip(x,X)), simultaneous=True)*JX.det()
    eq('density_and_cell_measure_pullback',muback,mu.subs(dict(zip(x,y)),simultaneous=True))
    # Full16 finite operator fixture in restored labels, with genuine Lorentz links.
    point={z:0 for z in y}
    E0=ebase.subs(point);Ep=label_e.subs(point)
    generator=[B01/13,B02/17,J12/19,(B01+J12)/23]
    links=[(S.eye(4)-A/2).inv()*(S.eye(4)+A/2) for A in generator]
    d0=S.zeros(16);dp=S.zeros(16)
    for r,A in enumerate(links):
        eq('proper_Lorentz_fixture_'+str(r),A.T*ETA*A,ETA)
        d0+=creator((ETA*E0.inv().T)[:,r])*(exterior(A)-S.eye(16))
        dp+=creator((ETA*Ep.inv().T)[:,r])*(exterior(A)-S.eye(16))
    D0=d0+d0.T;Dp=dp+dp.T
    eq('whole16_true_adjoint_Dirac',Dp,D0)
    eq('whole16_square',Dp*Dp,D0*D0)
    eq('whole16_first_and_second_coordinate_jets',Dp.diff(t)+Dp.diff(t,2),S.zeros(16))
    return {'native_dimension_fixture':16,'reference_columns_fixture':2}

def cone():
    scale, phi=S.symbols('s phi',positive=True)
    g0=scale**2*ETA;G0=scale**2*S.eye(4);a0=scale*S.eye(4)[:,0]
    da=scale*S.Matrix([0,phi,phi,0])
    dg=2*(da*a0.T+a0*da.T)
    J=S.zeros(4);J[0,1]=J[0,2]=2*phi
    eq('old_metric_velocity_is_coordinate_velocity',dg,J.T*g0+g0*J)
    relative_a=da-J.T*a0
    eq('old_observer_velocity_is_not_joint_coordinate_velocity',relative_a,-da)
    require('fixed_positive_metric_is_not_dragged',J.T*G0+G0*J!=S.zeros(4))
    dginv=-g0.inv()*dg*g0.inv()
    eq('relational_clock_gram_joint_variation',dginv+J*g0.inv()+g0.inv()*J.T,S.zeros(4))
    eq('fixed_clock_has_real_relational_strain',dginv[0,1],2*phi/scale**2)
    eq('fixed_clock_second_spatial_strain',dginv[0,2],2*phi/scale**2)
    require('old_contrast_not_removed',dginv!=S.zeros(4))

def ward_and_schur():
    # Exact coupled, not fixed-reference, source: S=Q(g)+1/2(z+A g)^T B(z+A g).
    B=S.Matrix([[3,1],[1,2]])
    A=S.Matrix([[1,2,-1],[2,0,3]])
    Q=S.diag(0,5,0)
    Hgg=Q+A.T*B*A;Hgz=A.T*B;Hzz=B
    H=Hgg.row_join(Hgz).col_join(Hgz.T.row_join(Hzz))
    xi=S.Matrix([S.Symbol('u'),0,S.Symbol('w')])
    gauge=xi.col_join(-A*xi)
    eq('full_joint_Ward_kernel',H*gauge,S.zeros(5,1))
    require('fixed_detector_partial_Hessian_is_not_zero',Hgg*xi!=S.zeros(3,1))
    reduced=Hgg-Hgz*Hzz.inv()*Hgz.T
    eq('same_action_reduced_Hessian',reduced,Q)
    eq('reduced_metric_gauge_kernel',reduced*xi,S.zeros(3,1))
    # Defective block equations: exact residual relation before any bound.
    v=S.Matrix(S.symbols('v0:3'));z=S.Matrix(S.symbols('z0:2'))
    r1=Hgg*v+Hgz*z;r2=Hgz.T*v+Hzz*z
    eq('Ward_residual_transfers_without_projection',reduced*v,r1-Hgz*Hzz.inv()*r2)
    D=S.diag(2,0);C=S.eye(2);vbad=S.Matrix([0,1])
    Pker=S.diag(0,1)
    require('singular_reference_block_has_real_compatibility',Pker*C*vbad!=S.zeros(2,1))
    # Offshell gauge Hessian needs acceleration. L=F(x^2+y^2), rotation orbit.
    x,y,t=S.symbols('x y t',real=True)
    fun=(x*x+y*y)**2+3*(x*x+y*y)
    vel=S.Matrix([-y,x]);acc=S.Matrix([-x,-y])
    grad=S.Matrix([S.diff(fun,x),S.diff(fun,y)])
    hess=S.hessian(fun,[x,y])
    eq('off_shell_second_Ward_includes_acceleration',(vel.T*hess*vel)[0]+(grad.T*acc)[0],0)
    require('off_shell_partial_gauge_Hessian_not_zero',S.expand((vel.T*hess*vel)[0])!=0)

def metric_selector():
    a,b,c,d,e=S.symbols('a b c d e')
    qs=S.Matrix(S.symbols('q0:4'));qu=ETA*qs;q2=(qs.T*qu)[0]
    packed=[(i,j) for i in range(4) for j in range(i,4)]
    hs=S.symbols('h0:10');h=S.zeros(4)
    for value,(i,j) in zip(hs,packed):h[i,j]=h[j,i]=value
    ht=S.trace(ETA*h);hv=h*qu;double=(qu.T*h*qu)[0]
    E=a*q2*h+b*(qs*hv.T+hv*qs.T)+c*qs*qs.T*ht+d*ETA*double+e*ETA*q2*ht
    div=E*qu
    expected=(a+b)*q2*hv+(b+d)*qs*double+(c+e)*q2*qs*ht
    eq('all_ten_metric_general_symbol_divergence',div,expected)
    symbols=list(qs)+list(hs)
    coeff=[]
    for component in div:
        coeff.extend(S.Poly(S.expand(component),*symbols).coeffs())
    solution=S.linsolve(coeff+[c-d],(a,b,c,d,e))
    eq('one_dimensional_Einstein_selector',S.Matrix(next(iter(solution))),S.Matrix([-e,e,-e,-e,e]))
    normalized=E.subs({a:1,b:-1,c:1,d:1,e:-1})
    xi=S.Matrix(S.symbols('xi0:4'))
    pure=qs*xi.T+xi*qs.T
    substitution={hs[k]:pure[i,j] for k,(i,j) in enumerate(packed)}
    eq('selected_operator_annihilates_all_coordinate_velocities',normalized.subs(substitution),S.zeros(4))
    eq('selected_operator_full_Bianchi',normalized*qu,S.zeros(4,1))
    R=S.Matrix([[1,1,0,0,0],[0,1,0,1,0],[0,0,1,0,1],[0,0,1,-1,0]])
    Rp=R.T*(R*R.T).inv()
    direction=S.Matrix([1,-1,1,1,-1])
    eq('coefficient_defect_kernel',R*direction,S.zeros(4,1))
    eq('coefficient_Einstein_projection',S.eye(5)-Rp*R,direction*direction.T/5)
    eq('quantitative_coefficient_error_bound',S.trace(Rp.T*Rp),4)
    # Equality of the cross terms is a variational condition, not imposed by
    # dropping a matter row. Check it on arbitrary symmetric test tensors.
    ks=S.symbols('k0:10');k=S.zeros(4)
    for value,(i,j) in zip(ks,packed):k[i,j]=k[j,i]=value
    Ek=E.subs(dict(zip(hs,ks)))
    defect=S.trace(ETA*k*ETA*E)-S.trace(ETA*h*ETA*Ek)
    eq('variational_selfadjointness_requires_c_equals_d',defect.subs(d,c),0)
    require('Bianchi_without_variational_hypothesis_not_enough',defect!=0)
    # Covariance alone allows a higher-derivative transverse invariant.
    transverse=q2*ETA-qs*qs.T
    high=transverse*(q2*ht-double)
    eq('higher_derivative_counterexample_is_transverse',high*qu,S.zeros(4,1))
    require('two_derivative_hypothesis_is_indispensable',S.Poly(high[0,0],*list(qs)).total_degree()==4)

def shell_covariance():
    Delta=S.diag(1,1,2,3);P=S.diag(1,1,0,0)
    K=S.Matrix([[0,1,2,S.I],[-1,0,S.I,3],[-2,S.I,0,1],[S.I,-3,-1,0]])
    eq('true_comparison_frame_generator_is_antiHermitian',K.H,-K)
    A1=S.Matrix([[1,2,S.I,0],[2,-1,0,1],[-S.I,0,2,1],[0,1,1,0]])
    rotated=A1+K*Delta-Delta*K
    eq('full_shell_split_invariant_under_coordinate_transport',P*rotated*P,P*A1*P)
    eq('pure_coordinate_first_jet_has_zero_shell_compression',P*(K*Delta-Delta*K)*P,S.zeros(4))
    require('coordinate_transport_does_not_cancel_real_shell_split',P*rotated*P!=S.zeros(4))
    epsilon=S.symbols('eps')
    eq('compressed_characteristic_polynomial_unchanged',rotated[:2,:2].charpoly(epsilon).as_expr(),A1[:2,:2].charpoly(epsilon).as_expr())

def clock_ward():
    x=S.Matrix(S.symbols('t x y z'))
    clock=x[0]**2+x[1]*x[2]+x[3]**3
    grad=S.Matrix([S.diff(clock,q) for q in x]); up=ETA*grad
    norm=(grad.T*up)[0]
    metric_source=ETA*norm/4-up*up.T/2
    clock_source=-sum(ETA[i,i]*S.diff(clock,x[i],2) for i in range(4))
    div=S.Matrix([sum(S.diff(metric_source[i,j],x[i]) for i in range(4))*ETA[j,j] for j in range(4)])
    eq('full_clock_metric_Noether_identity',-2*div+clock_source*grad,S.zeros(4,1))
    require('metric_source_not_conserved_with_frozen_unsolved_clock',div!=S.zeros(4,1))

def run():
    CHECKS.clear()
    fixture=pullback();cone();ward_and_schur();metric_selector();clock_ward();shell_covariance()
    return {'schema':'d0-full-experiment-ward/1','checks':CHECKS,'exact_checks':len(CHECKS),
            'fixture':fixture,'metric_selector':'(a,b,c,d,e)=c0*(1,-1,1,1,-1)',
            'finite_same_experiment_naturality':True,'old_fixed_detector_contrast_cancelled':False,
            'physical_clock_dynamics_selected':False,'physical_retained_fields_eliminated':False,
            'native_metric_only_locality_proved':False,'GR_closed':False}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
