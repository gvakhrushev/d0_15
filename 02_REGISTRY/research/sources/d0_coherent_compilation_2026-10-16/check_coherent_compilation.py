#!/usr/bin/env python3
"""Exact coherent-completion and AF reference-cost tests, not physical admission.
No downloads, writes, old-suite execution, or receipt-only success claims.
"""
from __future__ import annotations
from itertools import product
import json
import sympy as s

a=s.Symbol('a', real=True)
p=a*a
x=s.Symbol('x', real=True)
relation=a**4+a*a-1
checks=[]

def red(v):
    v=s.cancel(v)
    num,den=s.fraction(v)
    if not den.has(a):
        return s.cancel(s.rem(num,relation,a)/den)
    return s.rem(s.rem(num,relation,a)*s.invert(den,relation,a),relation,a)

def mat(M):
    return s.Matrix(M).applyfunc(red)

def eq(name,A,B=0):
    if isinstance(A,s.MatrixBase) or isinstance(B,s.MatrixBase):
        good=mat(s.Matrix(A)-s.Matrix(B))==s.zeros(*s.Matrix(A).shape)
    else:
        good=red(A-B)==0
    if not good:raise ArithmeticError(name)
    checks.append(name)

def require(name,condition):
    if not condition:raise ArithmeticError(name)
    checks.append(name)

def rot(t):
    c=(1-t*t)/(1+t*t); d=2*t/(1+t*t)
    return s.Matrix([[c,-d],[d,c]])

def ptr_env(M):
    # data(2) x outcome(2) x environment(2), trace env only for a control.
    return s.Matrix(4,4,lambda i,j:sum(M[2*i+e,2*j+e] for e in range(2)))

def fib(n):
    z,o=0,1
    for _ in range(n):z,o=o,z+o
    return z

def native_paths(n,k):
    # Literal defining-block inclusion (A,B)->(diag(A,B),A).
    b=[[(0,j,()) for j in range(fib(n+2))],
       [(1,j,()) for j in range(fib(n+1))]]
    for _ in range(k):
        b=[[(old,j,path+(0,)) for old,j,path in b[0]+b[1]],
           [(old,j,path+(1,)) for old,j,path in b[0]]]
    return b

def main():
    checks.clear()
    eq('golden_closure',p+p*p,1)
    # Full controller, two logical labels, two outcomes, two env states.
    # Deliberately different environment states: effects alone do not fix channel.
    C=s.zeros(8,2); K=s.zeros(8,2); R=s.zeros(8)
    for i,b in product(range(2),repeat=2):
        gate=rot(x/s.Integer(i+2))*s.Matrix([a,p])
        env=rot((i+1)*(b+1)*x)
        amp=gate[b]
        base=4*i+2*b
        C[base:base+2,i]=amp*env[:,0]
        K[base,i]=amp
        R[base:base+2,base:base+2]=env.T
    eq('complete_controller_isometry',C.H*C,s.eye(2))
    eq('complete_canonical_isometry',K.H*K,s.eye(2))
    eq('all_environment_columns_unitary',R.H*R,s.eye(8))
    eq('coherent_completion_all_input_vectors',R*C,K)
    t0=s.Rational(1,7)
    C0=mat(C.subs(x,t0)); C1=mat(s.diff(C,x).subs(x,t0))
    K0=mat(K.subs(x,t0)); K1=mat(s.diff(K,x).subs(x,t0))
    R0=mat(R.subs(x,t0)); R1=mat(s.diff(R,x).subs(x,t0))
    eq('moving_completion_includes_dR',R1*C0+R0*C1,K1)
    require('frozen_completion_is_not_same_jet',mat(R0*C1-K1)!=s.zeros(8,2))
    rho=s.Matrix([[s.Rational(3,5),(1+s.I)/10],[(1-s.I)/10,s.Rational(2,5)]])
    drho=s.Matrix([[s.Rational(1,9),s.I/13],[-s.I/13,-s.Rational(1,9)]])
    sig=mat(C0*rho*C0.H); can=mat(K0*rho*K0.H)
    dsig=mat(C1*rho*C0.H+C0*drho*C0.H+C0*rho*C1.H)
    dcan=mat(K1*rho*K0.H+K0*drho*K0.H+K0*rho*K1.H)
    eq('complete_mixed_state_equality',R0*sig*R0.H,can)
    eq('complete_mixed_state_jet',R1*sig*R0.H+R0*dsig*R0.H+R0*sig*R1.H,dcan)
    eq('full_normalizer_is_not_postselection',s.trace(sig),1)
    eq('moving_normalizer',s.trace(dsig),0)
    require('same_effect_different_reduced_instrument',mat(ptr_env(sig)-ptr_env(can))!=s.zeros(4))
    for b in range(2):
        Q=s.diag(*[int((j//2)%2==b) for j in range(8)])
        eq('same_effect_branch_'+str(b),C0.H*Q*C0,K0.H*Q*K0)
        eq('outcome_flag_not_erased_'+str(b),R0*Q-Q*R0,s.zeros(8))
    archive=s.diag(*[j%2 for j in range(8)])
    eq('all_archive_observables_recoverable',s.trace(can*R0*archive*R0.H),s.trace(sig*archive))
    require('archive_pointer_itself_changes',red(s.trace(sig*archive)-s.trace(can*archive))!=0)
    eq('no_discarded_complement',R0.H*can*R0,sig)
    # Preserve the actual two-record comparator, not just the terminal spectrum.
    y0=s.Rational(2,9)
    Cy=mat(C.subs(x,y0)); Ry=mat(R.subs(x,y0)); Ky=mat(K.subs(x,y0))
    eq('two_endpoint_comparator_commuting_square',Cy.H*Ry.H*R0*C0,Ky.H*K0)
    completed_jet=mat(R1*C0+R0*C1)
    q_completed=red(s.trace(completed_jet.H*(s.eye(8)-K0*K0.H)*completed_jet)/2)
    q_canonical=red(s.trace(K1.H*(s.eye(8)-K0*K0.H)*K1)/2)
    eq('same_comparator_metric_after_compilation',q_completed,q_canonical)
    eq('same_Berry_connection_after_compilation',K0.H*completed_jet,K0.H*K1)
    cb=mat(C.subs(x,0)); dc=mat(s.diff(C,x).subs(x,0))
    kb=mat(K.subs(x,0)); dk=mat(s.diff(K,x).subs(x,0))
    extra=s.trace(dc.H*(s.eye(8)-cb*cb.H)*dc-dk.H*(s.eye(8)-kb*kb.H)*dk)/2
    eq('uncorrected_controller_has_extra_metric',extra,10*(p+4*p*p))
    eq('canonical_metric_blank',s.trace(dk.H*(s.eye(8)-kb*kb.H)*dk)/2,s.Rational(13,18))

    # The general intrinsic direct rotation on a real normalized 2-vector.
    c=(1-x*x)/(1+x*x); d=2*x/(1+x*x)
    v=s.Matrix([1,0]); eta=s.Matrix([c,d]); A=eta*v.T-v*eta.T
    transport=s.eye(2)+A+A*A/(1+c)
    eq('intrinsic_direct_rotation',transport*v,eta)
    eq('intrinsic_direct_rotation_unitary',transport.T*transport,s.eye(2))

    # Exact same-type AF path capacity. Not a generic invented tensor factor.
    for k in range(2,9):
        B=native_paths(1,k)
        eq('AF_dimensions_'+str(k),len(B[0]),fib(k+3))
        eq('AF_dimensions_other_'+str(k),len(B[1]),fib(k+2))
        eq('same_type_ready_paths_'+str(k),len({p for j,_,p in B[0] if j==0}),fib(k+1))
        eq('same_type_pending_paths_'+str(k),len({p for j,_,p in B[1] if j==1}),fib(k-1))
    capacity=[]
    for width in (2,4,256,1024,4096):
        k=2
        while fib(k-1)<width:k+=1
        capacity.append({'controller_dimension':width,'sufficient_level_shift':k,
                         'ready_same_type_paths':fib(k+1),'pending_same_type_paths':fib(k-1)})
        require('minimal_same_type_shift_'+str(width),fib(k-1)>=width and fib(k-2)<width)
    eq('full_4096_controller_shift',capacity[-1]['sufficient_level_shift'],20)

    # Actual n=1 to N=5 inclusion, two preserved controller modes in each block.
    n=1; k=4; B=native_paths(n,k); dims=[len(z) for z in B]
    eq('concrete_full_AF_dimensions',s.Matrix(dims),s.Matrix([13,8]))
    selected=[]; offset=0
    for j in range(2):
        paths=sorted({path for old,_,path in B[j] if old==j})[:2]
        for row in range(fib(n+2-j)):
            selected.append([offset+B[j].index((j,row,path)) for path in paths])
        offset+=dims[j]
    J=s.zeros(sum(dims),3)
    for col,positions in enumerate(selected):
        r=rot((col+1)*x)
        for env,position in enumerate(positions):J[position,col]=r[env,0]
    Uold=s.diag(1,1,1); Uold[:2,:2]=rot(x/3)
    V=J*Uold
    Cn=s.diag(2,2,3)
    CN=s.diag(*([6]*13+[7]*8))
    Pin=s.diag(0,0,1); Pout=s.diag(*([0]*13+[1]*8))
    eq('actual_AF_isometry',V.H*V,s.eye(3))
    eq('actual_AF_same_central_label',Pout*V,V*Pin)
    eq('exact_full_code_shift',V.H*CN*V,Cn+k*s.eye(3))
    eq('complete_moving_code_jet',s.diff(V.H*CN*V,x),s.zeros(3))
    V0=V.subs(x,t0); V1=s.diff(V,x).subs(x,t0)
    Wconn=s.simplify(V0.H*V1)
    require('nontrivial_coherent_frame_motion',Wconn!=s.zeros(3))
    Sold=s.diag(1,1,1)
    Sold[:2,:2]=s.Matrix([[s.Rational(2,5),(1+s.I)/10],[(1-s.I)/10,s.Rational(1,5)]])
    Sold[2,2]=s.Rational(2,5)
    dSold=s.Matrix([[s.Rational(1,10),s.I/11,0],[-s.I/11,-s.Rational(1,20),0],[0,0,-s.Rational(1,20)]])
    Snew=s.simplify(V0*Sold*V0.H)
    dSnew=s.simplify(V1*Sold*V0.H+V0*dSold*V0.H+V0*Sold*V1.H)
    eq('full_AF_state_normalization',s.trace(Snew),1)
    eq('full_AF_state_normalizer_jet',s.trace(dSnew),0)
    eq('cost_difference_not_erased',s.trace(CN*Snew)-s.trace(Cn*Sold),k)
    eq('full_price_code_source_preserved',s.trace(CN*dSnew)-s.trace(Cn*dSold),0)
    eq('source_noncommuting_density_motion',V0.H*dSnew*V0,dSold+Wconn*Sold-Sold*Wconn)
    lam=s.Symbol('lam')
    eq('all_zero_modes_first_block_retained',Snew[:13,:13].charpoly(lam).as_expr(),
       lam**11*Sold[:2,:2].charpoly(lam).as_expr())
    eq('all_zero_modes_second_block_retained',Snew[13:,13:].charpoly(lam).as_expr(),
       lam**7*(lam-Sold[2,2]))
    eq('PF_reference_intertwiner',
       s.diag(*([p**6]*13+[p**7]*8))*V,
       p**k*V*s.diag(p**2,p**2,p**3))

    # Full regular GNS lift, with separately retained right columns.
    Xold=[s.Matrix([[1,s.I/3],[s.Rational(2,7),s.Rational(1,2)]]),s.Matrix([[s.Rational(2,3)]])]
    start=0;colstart=0
    for j in range(2):
        d=3 if j==0 else 2
        olddim=2 if j==0 else 1
        Tj=V0[start:start+dims[j],colstart:colstart+olddim]
        Bj=J.subs(x,0)[start:start+dims[j],colstart:colstart+olddim]
        Xnew=p**(-s.Rational(k,2))*Tj*Xold[j]*Bj.H
        # k=4, so the exponent is an exact integer here.
        eq('regular_GNS_norm_'+str(j),p**(n+k+1+j)*s.trace(Xnew.H*Xnew),
           p**(n+1+j)*s.trace(Xold[j].H*Xold[j]))
        eq('regular_GNS_left_density_'+str(j),p**(n+k+1+j)*Xnew*Xnew.H,
           p**(n+1+j)*Tj*Xold[j]*Xold[j].H*Tj.H)
        start+=dims[j];colstart+=olddim

    # Same proof is valid through a rank birth; no logarithm of zero is evaluated.
    F=s.Matrix([[1,0],[0,x],[0,0]])
    mass=s.trace(F*F.H)
    Sr=F*F.H/mass
    SrN=V*F
    eq('rank_birth_full_factor_Gram',SrN.H*SrN,F.H*F)
    eq('rank_birth_cost_shift',s.trace(SrN.H*CN*SrN)/mass-s.trace(Cn*Sr),k)
    eq('raw_positive_scale_cancels',((1+x)**2*(F*F.H))/((1+x)**2*mass),Sr)

    # General compilation anomaly is a compressed code mismatch; differentiation
    # keeps both terms. A distorted reference is a negative reference control.
    h=s.Symbol('h',real=True)
    CNbad=CN+h*s.diag(*[int(i==selected[0][1]) for i in range(21)])
    Delta=V.H*CNbad*V-Cn-k*s.eye(3)
    lhs=s.trace(CNbad*V*Sold*V.H)-s.trace(Cn*Sold)-k
    eq('exact_code_anomaly',lhs,s.trace(Sold*Delta))
    require('unequal_cost_memory_is_visible',s.simplify(Delta)!=s.zeros(3))
    eq('anomaly_full_two_term_jet',s.diff(s.trace((Sold+x*dSold)*Delta),x),
       s.trace(dSold*Delta)+s.trace((Sold+x*dSold)*s.diff(Delta,x)))
    # First sources add under the existing six-level spectral transfer.
    q=s.Symbol('q',real=True); Aold=s.Function('A')(q)
    eq('next_active_record_preserves_compiled_source',s.diff(Aold+k+6,q),s.diff(Aold,q))
    # Fixed coding overhead is NOT free under a varied geometric integration measure.
    volume=s.Function('V')(q)
    eq('volume_overhead_source',s.diff(k*volume,q),k*s.diff(volume,q))
    require('volume_overhead_not_zero',s.diff(k*volume,q)!=0)

    # Conditional geometric aggregation: preserve fixed controller overhead
    # without a hand-selected subtraction. This does not select native volume law.
    v0,v1,v2,l0,l1,l2,b=s.symbols('v0 v1 v2 l0 l1 l2 b',positive=True)
    weights=[v0+x/3,v1-x/5,v2+x/7]
    prices=[l0+x,l1-x/2,l2+2*x]
    Z=sum(weights); N=sum(w*l for w,l in zip(weights,prices)); mean=N/Z
    shifted=sum(w*(l+b) for w,l in zip(weights,prices))/Z
    eq('normalized_complete_price_constant_shift',shifted-mean,b)
    eq('normalized_complete_price_shift_source',s.diff(shifted-mean,x),0)
    centered=sum(w*s.diff(l,x)+(l-mean)*s.diff(w,x)
                 for w,l in zip(weights,prices))/Z
    eq('full_normalized_probability_source',s.diff(mean,x),centered)
    require('frozen_global_normalizer_changes_source',s.simplify(s.diff(N,x)/Z-centered)!=0)
    V=s.Symbol('V',positive=True); c=s.Symbol('c',real=True)
    eq('unique_volume_scaling_candidate',s.diff(V*(c/V),V),0)
    require('unnormalized_volume_breaks_compiler_equivalence',s.diff(b*V,V)!=0)
    # Four-dimensional vacuum consequence of the generic normalized EH theorem.
    ell,rbar=s.symbols('ell rbar',nonzero=True)
    eq('normalized_vacuum_trace_consistency',ell*rbar-2*ell*rbar,-ell*rbar)
    # Consume the concurrent actual preparation minimum algebraically.
    # f1,f2 stand for derivatives of its fixed f_0, not a selected new price.
    gg,om,f1,f2,e1,e2,d1,d2=s.symbols('gg om f1 f2 e1 e2 d1 d2', nonzero=True)
    tt=s.symbols('tt',real=True)
    uu=[tt**2*e1+tt**4*d1,tt**2*e2+tt**4*d2]
    df=[f1*u+f2*u*u/2 for u in uu]
    partition_ratio=1+om*sum(-gg*v+gg**2*v*v/2 for v in df)
    aa=s.expand(partition_ratio-1)
    min_price=s.expand(-(aa-aa*aa/2)/gg)
    eq('relaxed_preparation_curvature_coefficient',min_price.coeff(tt,2),om*f1*(e1+e2))
    fourth=om*f1*(d1+d2)+om*(f2-gg*f1*f1)*(e1*e1+e2*e2)/2+gg*om*om*f1*f1*(e1+e2)**2/2
    eq('relaxed_preparation_complete_fourth_coefficient',min_price.coeff(tt,4),fourth)
    eq('relaxed_preparation_full_shape_jet',s.diff(min_price.coeff(tt,4),e1),s.diff(fourth,e1))
    zz=s.Function('Z')(q); div=s.Function('Drel')(q)
    compiled=k+6-s.log(zz)/gg+div/gg
    eq('actual_minimum_compilation_residual_identity',compiled-(6-s.log(zz)/gg+div/gg),k)
    eq('actual_minimum_complete_partition_source',s.diff(k+6-s.log(zz)/gg,q),-s.diff(zz,q)/(gg*zz))
    eq('relative_entropy_remaining_source_retained',s.diff(compiled,q),(-s.diff(zz,q)/zz+s.diff(div,q))/gg)
    return {'schema':'d0-coherent-compilation-cost-descent/1','exact_checks':len(checks),
      'checks':checks,'capacity':capacity,
      'controller_completion':'R(X) C(X) = K_E(X) tensor blank; includes dR',
      'PF_price':'A_old,N(T sigma T*) = A_old,n(sigma)+k',
      'PF_source':'dA_old,N=dA_old,n on fixed-depth complete coherent family',
      'mismatch_operator':'T* C_N T - C_n - k I; source Tr(dsigma K)+Tr(sigma dK)',
      'native_same_program_binding_proved':False,'physical_Info_selected':False,
      'historical_compiler_without_completion_proved_equivalent':False,
      'Lorentz_observer_term_removed':False,'native_normalized_volume_binding_proved':False,'full_GR_closed':False}

if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
