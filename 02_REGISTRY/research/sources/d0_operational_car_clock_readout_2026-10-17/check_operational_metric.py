#!/usr/bin/env python3
"""D0: exact CAR/clock metrology and complete AF/scene observations.

Self-contained finite identities, NOT physical admission, a full Cost-Info
selector, an independent Einstein stress tensor, or a new solution family.
All tests use explicit exceptions and survive python -O. Source inputs are
pinned in RESULT_RU.md. No historical certificate or repository code is run.
"""
from __future__ import annotations
import json
import sympy as s

CHECKS: list[str] = []

def eq(name, lhs, rhs=0):
    d = lhs-rhs
    xs = list(d) if isinstance(d, s.MatrixBase) else [d]
    if any(s.cancel(s.expand(x)) != 0 for x in xs):
        raise ArithmeticError(name)
    CHECKS.append(name)

def yes(name, value):
    if not bool(value):
        raise ArithmeticError(name)
    CHECKS.append(name)

def neq(name,lhs,rhs=0):
    d=lhs-rhs
    xs=list(d) if isinstance(d,s.MatrixBase) else [d]
    yes(name,any(s.cancel(s.expand(x)) != 0 for x in xs))

def creators():
    # Fixed ordered exterior basis: bits 0,1,2,3. The statements depend on
    # the CAR, not on a potentially different physical Role enumeration.
    out=[]
    for r in range(4):
        C=s.zeros(16)
        for m in range(16):
            if not ((m>>r)&1):
                parity=sum((m>>j)&1 for j in range(r))
                C[m|(1<<r),m]=(-1)**parity
        out.append(C)
    return out

def lin(v, matrices):
    return sum((v[i]*matrices[i] for i in range(4)),s.zeros(16))

def boost(r):
    c=(1+r*r)/(1-r*r); a=2*r/(1-r*r)
    return s.Matrix([[c,a,0,0],[a,c,0,0],[0,0,1,0],[0,0,0,1]])

def block(a,b,c,d):
    return a.row_join(b).col_join(c.row_join(d))

def main():
    I=s.eye(16); Z=s.zeros(16)
    cs=creators(); zs=[c-c.T for c in cs]
    for r in range(4):
        for k in range(r,4):
            eq(f'CAR_{r}_{k}',cs[r]*cs[k].T+cs[k].T*cs[r],I if r==k else Z)
            eq(f'real_Clifford_{r}_{k}',zs[r]*zs[k]+zs[k]*zs[r],-2*I if r==k else Z)
    eta=s.diag(1,-1,-1,-1)
    F=s.Matrix([[2,s.Rational(1,3),0,s.Rational(1,5)],
                [0,s.Rational(3,2),s.Rational(1,4),0],
                [s.Rational(1,7),0,s.Rational(5,4),s.Rational(1,6)],
                [0,s.Rational(1,8),0,s.Rational(7,6)]])
    q=F*eta*F.T; g=q.inv()
    yes('nondegenerate_full_coefficient_frame',F.det()!=0)
    delta=s.Rational(1,64)
    recovered=[]
    for tag,rval in [('rest',s.Rational(0)),('boost',s.Rational(1,3))]:
        H=boost(rval); n=H[:,0]; L=H.inv(); nu=L*n
        hn=-eta+2*(eta*n)*(eta*n).T
        eq(f'{tag}_positive_whitening',L.T*L,hn)
        eq(f'{tag}_clock_norm',(nu.T*nu)[0],1)
        U=F*eta*L.T
        Q=U*U.T; b=U*nu
        eq(f'{tag}_Lorentz_reconstruction',2*b*b.T-Q,q)
        eq(f'{tag}_clock_constraint',(b.T*Q.inv()*b)[0],1)
        readings={}
        vv=[U[r,:].T for r in range(4)]
        # Only five elementary dilations. Cross terms use coherent PRODUCTS
        # of the same coefficient-qubit operations, not a new sum opcode.
        base={'clock':nu, **{f'single_{r}':vv[r] for r in range(4)}}
        amps={}; roots={}
        for name,v in base.items():
            A=lin(delta*v,zs); pr=delta*delta*v.dot(v)
            yes(f'{tag}_{name}_positive_dilation_window',0<pr<1)
            eq(f'{tag}_{name}_scalar_effect',A.T*A,pr*I)
            eq(f'{tag}_{name}_full_dilation_diagonal',(1-pr)*I+A.T*A,I)
            eq(f'{tag}_{name}_full_dilation_offdiag',A+A.T,Z)
            readings[name]=pr; amps[name]=A; roots[name]=s.sqrt(1-pr)
        for r in range(4):
            for k in range(r+1,4):
                nr,nk=f'single_{r}',f'single_{k}'
                bot=roots[nr]*amps[nk]+roots[nk]*amps[nr]
                pr=readings[nr]+readings[nk]-2*readings[nr]*readings[nk]+2*delta**2*roots[nr]*roots[nk]*vv[r].dot(vv[k])
                eq(f'{tag}_composed_pair_{r}_{k}_effect',bot.T*bot,pr*I)
                readings[f'pair_{r}_{k}']=pr
            nr,nk=f'single_{r}','clock'
            bot=roots[nr]*amps[nk]+roots[nk]*amps[nr]
            pr=readings[nr]+readings[nk]-2*readings[nr]*readings[nk]+2*delta**2*roots[nr]*roots[nk]*vv[r].dot(nu)
            eq(f'{tag}_composed_clock_pair_{r}_effect',bot.T*bot,pr*I)
            readings[f'clock_pair_{r}']=pr
        r0=readings['clock']; Qr=s.zeros(4); br=s.zeros(4,1)
        for r in range(4):
            rr=readings[f'single_{r}']
            Qr[r,r]=rr/r0
            br[r]=s.cancel((readings[f'clock_pair_{r}']-rr-r0+2*rr*r0)/(2*r0*roots[f'single_{r}']*roots['clock']))
            for k in range(r+1,4):
                rk=readings[f'single_{k}']
                Qr[r,k]=Qr[k,r]=s.cancel((readings[f'pair_{r}_{k}']-rr-rk+2*rr*rk)/(2*r0*roots[f'single_{r}']*roots[f'single_{k}']))
        decohered=readings['single_0']+readings['single_1']-2*readings['single_0']*readings['single_1']
        neq(f'{tag}_premature_flag_dephasing_loses_cross_metric',readings['pair_0_1'],decohered)
        eq(f'{tag}_all_ten_positive_entries',Qr,Q)
        eq(f'{tag}_all_four_clock_correlations',br,b)
        eq(f'{tag}_all_ten_Lorentz_entries',2*br*br.T-Qr,q)
        recovered.append(2*br*br.T-Qr)
        if tag=='boost':
            nq=-Q
            neq('positive_metric_without_clock_does_not_recover_Lorentz',nq,q)
    eq('observer_change_cancels_in_all_Lorentz_slots',*recovered)

    # Any density/purification works because the effect is scalar on ALL16.
    C=s.zeros(16,128)
    for j in range(128): C[j%16,j]=s.Rational(1+(j%7),1)
    N=s.trace(C.T*C)
    E=(delta**2*(F.row(0)*F.row(0).T)[0])*I
    eq('full128_reference_no_column_selection',s.trace(C.T*E*C)/N,E[0,0])
    Cr=s.zeros(16,128); Cr[7,127]=3
    eq('rank_one_reference_still_reads_metric',s.trace(Cr.T*E*Cr)/s.trace(Cr.T*Cr),E[0,0])
    yes('full128_fixture_all_columns_retained',all(C[:,j]!=s.zeros(16,1) for j in range(128)))

    # Full ten-slot tangent right inverse, no restriction to a wave ansatz.
    for r in range(4):
        for k in range(r,4):
            V=s.zeros(4); V[r,k]=1; V[k,r]=1
            dF=V*q.inv()*F/2
            eq(f'metric_lift_{r}_{k}',dF*eta*F.T+F*eta*dF.T,V)
    ch=s.Rational(4)
    Fhat=F/2
    Hhat=boost(s.Rational(1,3)); nhat=Hhat[:,0]; Lhat=Hhat.inv()
    Uhat=Fhat*eta*Lhat.T; bhat=Uhat*(Lhat*nhat)
    qhat_from_readout=2*bhat*bhat.T-Uhat*Uhat.T
    eq('normal_form_changes_operational_inverse_metric',qhat_from_readout,q/ch)
    eq('normal_form_changes_operational_covariant_metric',qhat_from_readout.inv(),ch*g)
    neq('frame_factor_is_not_unchanged_readout',qhat_from_readout,q)

    # Complete moving-clock ratio derivative: a shared detector sensitivity
    # and probe strength both cancel before taking a metric derivative.
    u=s.symbols('u')
    Qx=1+u+u**2; sensitivity=2+3*u; strength=1+s.Rational(1,3)*u
    x=sensitivity*strength**2*Qx; clock=sensitivity*strength**2
    eq('moving_sensitivity_and_probe_scale_cancel',s.diff(x/clock,u),s.diff(Qx,u))
    neq('frozen_clock_jet_rejected',s.diff(x,u).subs(u,0)/clock.subs(u,0),s.diff(Qx,u).subs(u,0))

    # Independent operational source on coordinates (q,b), with its exact
    # unit-clock constraint. T,sb are arbitrary pre-existing price sources.
    n=s.Matrix([1,0,0,0]); b=F*n; Q=2*b*b.T-q; ub=q.inv()*b
    T=s.Matrix([[2,1,0,0],[1,3,1,0],[0,1,5,1],[0,0,1,7]])
    sb=s.Matrix([1,2,3,4]); V=s.Matrix([[2,1,3,0],[1,-1,2,1],[3,2,4,1],[0,1,1,-2]])
    w=s.Matrix([0,1,2,3]); w=w-b*(ub.T*w)[0]
    db=V*ub/2+w; dQ=-V+2*(db*b.T+b*db.T)
    kk=sb+4*T*b
    Sq=-T+(kk*ub.T+ub*kk.T)/4
    eq('full_source_in_operational_metric_and_clock',s.trace(T*dQ)+(sb.T*db)[0],s.trace(Sq*V)+(kk.T*w)[0])
    eq('clock_tangent_constraint',2*(ub.T*db)[0]-(ub.T*V*ub)[0],0)
    neq('deleting_clock_source_changes_metric_source',s.trace(Sq*V),s.trace(-T*V))

    # One actual two-projector programme. Alternate U,Q then U^T,P.
    a=s.diag(s.Rational(3,5),s.Rational(4,5)); root=s.diag(s.Rational(4,5),s.Rational(3,5))
    O=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
    unit=s.diag(O,s.eye(2))*block(root,-a,a,root)
    P=s.diag(1,1,0,0); Qp=s.eye(4)-P; inc=s.eye(4)[:,:2]; B=a.T*a
    eq('return_program_unitarity',unit.T*unit,s.eye(4))
    word=inc; wrong=inc
    for j in range(1,7):
        gate=Qp*unit if j%2 else P*unit.T
        word=gate*word
        wrong=(Qp*unit if j%2 else P*unit)*wrong
        eq(f'alternating_history_effect_{j}',word.T*word,B**j)
    neq('repeating_forward_is_not_the_alternating_history',wrong.T*wrong,B**6)

    z=s.Rational(2,7); e=s.Rational(3,8); e0=s.Rational(2,5)
    # Noncommuting B and its true tangent. Normalized full-trace preparation.
    B=O*s.diag(s.Rational(1,5),s.Rational(2,3))*O.T
    Y=s.Matrix([[1,s.Rational(2,3)],[s.Rational(2,3),-1]])
    neq('source_test_is_noncommuting',B*Y,Y*B)
    C0=s.eye(2)-B; K=(1-z)*s.eye(2)+z*(1-e)*C0
    R=K.inv(); d0=1-z*e; beta=z*(1-e)/d0; k0=e0*z/d0
    chi=e0*z*s.trace(C0*R)
    eq('susceptibility_factorization',K,d0*(s.eye(2)-beta*B))
    opder=-e0*z*Y*R+e0*z*z*(1-e)*C0*R*Y*R
    eq('moving_scene_susceptibility_source',opder,-e0*z*(1-z)*R*Y*R)
    for cutoff in (0,1,3,6):
        partial=k0*sum((beta**j*s.trace((s.eye(2)-B)*B**j) for j in range(cutoff+1)),s.Rational(0))
        rem=chi-partial
        yes(f'positive_return_tail_{cutoff}',rem>=0)
        yes(f'dimension_kept_in_return_tail_{cutoff}',rem<=2*k0*beta**(cutoff+1))
        eq(f'exact_return_tail_{cutoff}',rem,k0*beta**(cutoff+1)*s.trace((s.eye(2)-B)*B**(cutoff+1)*(s.eye(2)-beta*B).inv()))
    # Price-comparison Hessian in a scalar Clifford direction. F_cmp=Q u^2
    # to second order, so this derivative computes that coefficient exactly.
    lam=s.symbols('lam')
    Kmeter=(1-z)*s.eye(2)+z*(1-e)*(1-lam)*C0
    derivative=-s.diff(Kmeter.det(),lam).subs(lam,0)/K.det()
    eq('meter_hessian_equals_own_susceptibility',derivative,(1-e)*chi/e0)
    p,t,f,zz,bb0=s.symbols('p t f zz bb0')
    ee0=p*p; ee_actual=ee0*(1+t*t*f)
    KK=1-zz+zz*(1-ee_actual)*(1-bb0)
    chi_exact=ee0*zz*(1-bb0)/KK
    meter_exact=p*zz*(1-ee_actual)*(1-bb0)/KK
    numerator=s.fraction(s.cancel(meter_exact-(1-p*t*t*f)*chi_exact))[0]
    eq('finite_response_mismatch_derived_at_golden_root',s.rem(numerator,p*p+p-1,p),0)
    badnum=s.fraction(s.cancel(meter_exact-chi_exact))[0]
    neq('missing_finite_response_factor_rejected',s.rem(badnum,p*p+p-1,p),0)

    # Four retained flags vs one union flag on the parent's compensation.
    ee,bb,cc=s.symbols('ee bb cc',positive=True)
    probabilities=s.Matrix([(1-ee)*(1-bb),(1-ee)*bb,ee*(1-bb),ee*bb])
    eq('all_four_flags_normalized',sum(probabilities),1)
    dq=probabilities.jacobian([ee,bb])
    fisher=dq.T*s.diag(*[1/v for v in probabilities])*dq
    eq('complete_flags_Fisher_rank_two',fisher,s.diag(1/(ee*(1-ee)),1/(bb*(1-bb))))
    hidden=1-cc/(1-ee)
    eq('aggregate_feedback_exact_cancellation',(1-ee)*(1-hidden),cc)
    tangent=s.Matrix([1,-(1-bb)/(1-ee)])
    eq('complete_flags_see_cancelled_source',(tangent.T*fisher*tangent)[0],1/(ee*(1-ee))+(1-bb)/(bb*(1-ee)**2))
    eq('aggregate_flag_blind_to_same_tangent',(s.Matrix([[(1-bb),(1-ee)]])*tangent)[0],0)
    yes('four_flag_law_changes_on_exact_compensation',dq.subs({ee:s.Rational(2,5),bb:s.Rational(2,5)})*s.Matrix([1,-1])!=s.zeros(4,1))
    # Original 0/10 port-code length, for these TWO actual binary records.
    code=2+ee+hidden
    eq('full_two_flag_code_second_source',s.diff(code,ee,2),-2*cc/(1-ee)**3)

    # The bare scalar AF register does NOT become a full spacetime metric.
    ev,ev2=s.symbols('ev ev2',positive=True)
    overlap=s.sqrt(1-ev)*s.sqrt(1-ev2)+s.sqrt(ev)*s.sqrt(ev2)
    leak=1-overlap**2
    eq('actual_AF_comparator_scalar_metric',s.diff(leak,ev2,2).subs(ev2,ev),1/(2*ev*(1-ev)))
    # A finite map of one scalar has outer-product pullback, rank at most1.
    grad=s.Matrix([1,2,3,4])
    yes('scalar_AF_pullback_rank_at_most_one',(grad*grad.T).rank()==1)

    print(json.dumps({'status':'PASS_SCOPED_EXACT_IDENTITIES','source_ref':'ccfbbe1abcc98a1d68e5f93b2bbaba5a01415fb5',
        'checks':len(CHECKS),'check_names':CHECKS,
        'coefficient_probe_settings':15,'independent_metric_slots':10,
        'reference_dimension_tested':128,'new_physical_opcode_admission':False,
        'full_Cost_Info_selected':False,'independent_full_matter_stress_derived':False,
        'full_joint_refinement_proved':False,'GR_closed':False},ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__': main()
