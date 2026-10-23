#!/usr/bin/env python3
"""Exact full16 source-code identities. No new native dynamics or GR claim.
Only SymPy and the standard library; no network, parent-suite run or file writes.
"""
from __future__ import annotations
from itertools import product
import json
import sympy as s

A, B = s.symbols('A B', real=True)
p, a = s.symbols('p a', positive=True)
I16 = s.eye(16)
CHECKS: list[str] = []


def red(x):
    x = s.expand(x)
    x = s.rem(x, a*a-p, a)
    return s.expand(s.rem(x, p*p+p-1, p))


def zero(M):
    if isinstance(M, s.MatrixBase):
        return all(s.cancel(red(v)) == 0 for v in M)
    return s.cancel(red(M)) == 0


def eq(label, left, right=0):
    if not zero(left-right):
        raise ArithmeticError(label)
    CHECKS.append(label)


def require(label, condition):
    if not bool(condition):
        raise ArithmeticError(label)
    CHECKS.append(label)


def source_data():
    creators = []
    for r in range(4):
        C = s.zeros(16)
        for mask in range(16):
            if not mask & (1 << r):
                C[mask | (1 << r), mask] = (-1)**((mask & ((1 << r)-1)).bit_count())
        creators.append(C)
    def gamma(v):
        return sum((v[i]*(creators[i]+creators[i].T) for i in range(4)), s.zeros(16))
    def minus(v):
        return sum((v[i]*(creators[i]-creators[i].T) for i in range(4)), s.zeros(16))
    frame = (A-B)*s.eye(4)+B*s.ones(4)
    axes = [s.Matrix(v) for v in ((0,0,-1,1),(0,1,0,-1),(0,-1,1,0))]
    J = [gamma(axes[r])*minus(frame[:,r+1]) for r in range(3)]
    Q = I16[:,[0,1,14,15]]
    Z = s.diag(-1,-1,1,1)
    d = A*A+3*B*B
    off = A*A-4*A*B-B*B
    G = (2*d-off)*s.eye(3)+off*s.ones(3)
    return creators, J, Q, Z, G


def run():
    CHECKS.clear()
    creators, J, Q, Z, G = source_data()
    for i,j in product(range(4), repeat=2):
        eq(f'full_CAR_{i}{j}', creators[i]*creators[j].T+creators[j].T*creators[i],
           I16 if i==j else s.zeros(16))
    eq('code_whole_four_columns', Q.T*Q, s.eye(4))
    for r in range(3):
        eq(f'actual_source_Hermitian_{r}', J[r].T, J[r])
        eq(f'zero_source_on_entire_code_{r}', Q.T*J[r]*Q, s.zeros(4))
        for t in range(3):
            eq(f'code_KL_Gram_{r}{t}', Q.T*J[r]*J[t]*Q, G[r,t]*s.eye(4))
    gp = A*A+4*A*B+7*B*B
    eq('Gram_singlet', (G*s.ones(3,1))[0], 4*(A-B)**2)
    eq('Gram_transverse', G*s.Matrix([1,-1,0]), gp*s.Matrix([1,-1,0]))
    scale = 2*(A-B)*gp
    T = [s.diag(0,-scale,scale),s.diag(scale,0,-scale),s.diag(-scale,scale,0)]
    for i,r,j in product(range(3), repeat=3):
        expected = T[r][i,j]*Z
        eq(f'full_third_moment_{i}{r}{j}', Q.T*J[i]*J[r]*J[j]*Q, expected)
    h=s.Matrix(s.symbols('h0:3',real=True))
    D=Q+sum((h[r]*J[r]*Q for r in range(3)),s.zeros(16,4))
    N=1+(h.T*G*h)[0]
    eq('one_linear_encoding_preserves_every_memory_inner_product',D.T*D,N*s.eye(4))
    for r in range(3):
        eq(f'full_source_pullback_{r}',D.T*J[r]*D,
           2*(G*h)[r]*s.eye(4)+(h.T*T[r]*h)[0]*Z)
    require('not_all_words_are_logically_invisible',not zero(Q.T*J[0]*J[1]*J[0]*Q))

    # A bounded rational creator-frame fixture. Its G^(1/2) is rational.
    sub={A:s.Rational(7,48),B:s.Rational(1,16)}
    jj=[j.subs(sub) for j in J]; gg=G.subs(sub)
    sing=s.ones(3)/3; trans=s.eye(3)-sing
    gs=s.Rational(1,6)*sing+s.Rational(7,24)*trans
    gi=6*sing+s.Rational(24,7)*trans
    eq('rational_Gram_root',gs*gs,gg)
    eq('rational_Gram_inverse_root',gi*gs,s.eye(3))
    VV=[Q]+[sum((jj[r]*Q*gi[r,t] for r in range(3)),s.zeros(16,4)) for t in range(3)]
    W=s.Matrix.hstack(*VV)
    eq('full_sixteen_dimensional_decoder_unitary',W.T*W,I16)
    eq('no_discarded_complement',W*W.T,I16)
    for r in range(3):
        eq(f'source_syndrome_column_{r}',W.T*jj[r]*Q,
           s.Matrix.vstack(s.zeros(4),*[gs[t,r]*s.eye(4) for t in range(3)]))

    # Exact source choice via a complete four-syndrome rotation, not a reset.
    hs=gi*s.Matrix([s.Rational(3,4),0,0]); nn=1+(hs.T*gg*hs)[0]
    Ds=Q+sum((hs[r]*jj[r]*Q for r in range(3)),s.zeros(16,4))
    V=s.Rational(4,5)*Ds
    syndrome=s.Matrix([s.Rational(4,5),s.Rational(3,5),0,0])
    R=s.eye(4);R[:2,:2]=s.Matrix([[s.Rational(4,5),-s.Rational(3,5)],[s.Rational(3,5),s.Rational(4,5)]])
    U=W*s.kronecker_product(R,s.eye(4))*W.T
    eq('complete_source_encoding_unitary',U.T*U,I16)
    eq('complete_source_encoding_is_actual_code_isometry',U*Q,V)
    eq('source_syndrome_and_memory_both_retained',W.T*V,s.kronecker_product(syndrome,s.eye(4)))
    y=2*gg*hs/nn; radius=(y.T*gg.inv()*y)[0]
    recovered=gg.inv()*y/(1+s.sqrt(1-radius))
    eq('exact_inverse_source_choice',recovered,hs)
    logical=s.Matrix([1,s.I,1,-s.I])/2
    logical2=s.Matrix([1,0,0,1])/s.sqrt(2)
    eq('balanced_unknown_logical_state', (logical.H*Z*logical)[0],0)
    eq('balanced_different_logical_state',(logical2.H*Z*logical2)[0],0)
    for i,l in enumerate((logical,logical2)):
        for r in range(3): eq(f'same_target_source_different_memory_{i}{r}',(l.H*V.T*jj[r]*V*l)[0],y[r])
    eq('history_overlap_preserved',(logical.H*V.T*V*logical2)[0],(logical.H*logical2)[0])

    # A trace-preserving full-carrier error channel with errors in span{I,J_r}.
    logical_rho=logical*logical.H
    code_rho=Q*logical_rho*Q.T
    normj=gg[0,0]
    channel=(code_rho+jj[0]*code_rho*jj[0]/normj)/2
    sv=s.Matrix([0,*list(gs[:,0])])/s.sqrt(normj)
    env_rho=(s.diag(1,0,0,0)+sv*sv.H)/2
    eq('decoder_preserves_logical_density_without_erasing_syndrome',W.T*channel*W,
       s.kronecker_product(env_rho,logical_rho))
    eq('full_channel_trace',s.trace(channel),1)
    eq('full_channel_Kraus_normalization',(I16+jj[0]*jj[0]/normj)/2,I16)

    # Moving source encoding: include the derivative of normalization.
    t=s.symbols('t',real=True)
    ht=t*gi[:,0]
    Dt=Q+sum((ht[r]*jj[r]*Q for r in range(3)),s.zeros(16,4))
    Nt=1+t*t
    t0=s.Rational(3,4)
    V0=Dt.subs(t,t0)*s.Rational(4,5)
    V1=Dt.diff(t).subs(t,t0)*s.Rational(4,5)-V0*(t0/(1+t0*t0))
    eq('moving_source_encoding_full_normalizer',V1.T*V0+V0.T*V1,s.zeros(4))
    eq('golden_source_margin',1-4*p**3,p**6)

    # Whole actual even-tail orbit: no census of arbitrary histories.
    rr=2*p-1; ss=2*a*p
    rot=s.Matrix([[rr,-ss],[ss,rr]])
    upper=s.Matrix([0,1]); states=[]
    for n in range(4):
        l=s.Matrix([-ss,rr,-upper[0],-upper[1]]).applyfunc(red)
        states.append(l)
        eq(f'actual_engine_balanced_memory_{n}',(l.T*Z*l)[0],0)
        eq(f'actual_engine_norm_{n}',(l.T*l)[0],2)
        upper=(rot*upper).applyfunc(red)
    qcoef=1+2*rr
    eq('four_states_have_nonzero_relation_coefficients',qcoef,4*p-1)
    eq('exact_three_mode_orbit_recurrence',states[3],states[0]-qcoef*states[1]+qcoef*states[2])
    minor=s.Matrix.hstack(*states[:3]).extract([0,2,3],[0,1,2]).det()
    eq('three_state_span_minor',minor,red(-2*ss*ss*(1-rr)))

    # Density, hence every fixed affine preparation-dependent Hessian, has order five.
    upper=s.Matrix([0,1]); densities=[]
    for n in range(6):
        l=s.Matrix([-ss,rr,-upper[0],-upper[1]]).applyfunc(red)
        densities.append((l*l.T/2).applyfunc(red))
        upper=(rot*upper).applyfunc(red)
    tt=s.symbols('tt')
    polynomial=s.Poly(s.expand((tt-1)*(tt*tt-2*rr*tt+1)*(tt*tt-2*(2*rr*rr-1)*tt+1)),tt)
    coeff=[red(x) for x in polynomial.all_coeffs()]
    eq('five_state_density_recurrence',sum((coeff[j]*densities[5-j] for j in range(6)),s.zeros(4)),s.zeros(4))
    eq('constant_spectral_Hessian_term_obeys_same_recurrence',sum(coeff),0)
    logical_test=s.Matrix([[1,2,0,1],[2,-1,3,0],[0,3,2,4],[1,0,4,-2]])
    sequence=[3+s.trace(logical_test*rho) for rho in densities]
    eq('affine_full_row_reading_obeys_density_recurrence',sum(coeff[j]*sequence[5-j] for j in range(6)),0)

    # Nonlinear common-eigenvector condition, including REAL coefficients.
    def residual_blocks(M,l):
        col=W.T*M*Q
        parts=[]
        for i in range(4):
            L=col[4*i:4*i+4,:]
            val=(l.H*L*l)[0]/(l.H*l)[0]
            real=s.re(val)
            parts.append((L*l-real*l).applyfunc(s.simplify))
        return s.Matrix.vstack(*parts)
    # Good M is a diagnostic coefficient, NOT asserted to be a native M_v.
    MM=s.zeros(16);MM[4:8,4:8]=s.diag(1,2,3,4)
    Mg=W*MM*W.T
    eq('new_class_not_limited_to_span_I_J',residual_blocks(Mg,logical),s.zeros(16,1))
    require('nonzero_operator_can_pass_entire_code_column',Mg!=s.zeros(16) and Mg*Q==s.zeros(16,4))
    Bad=Q*Z*Q.T
    require('zero_scalar_expectation_is_not_nonlinear_compatibility',
            zero((logical.H*Q.T*Bad*Q*logical)[0]) and not zero(residual_blocks(Bad,logical)))
    imag=s.zeros(16);imag[4:8,:4]=s.I*s.eye(4);imag[:4,4:8]=-s.I*s.eye(4)
    require('complex_span_is_not_real_cotangent_condition',not zero(residual_blocks(W*imag*W.T,logical)))

    # Four states are necessary in general; first three can have distinct real eigenvalues.
    r0=s.Rational(3,5);s0=s.Rational(4,5);R0=s.Matrix([[r0,-s0],[s0,r0]])
    lows=s.Matrix([-s0,r0]);up=s.Matrix([0,1]);ls=[]
    for _ in range(4):
        ls.append(s.Matrix([*lows,-up[0],-up[1]]));up=R0*up
    ortho=s.Matrix([r0,s0,0,0]);C=s.Matrix.hstack(*ls[:3],ortho)
    Lbad=C*s.diag(0,1,2,3)*C.inv()
    for i in range(3):eq(f'three_tests_are_insufficient_{i}',Lbad*ls[i],i*ls[i])
    ratio=(ls[3].T*Lbad*ls[3])[0]/2
    require('fourth_test_detects_false_history_closure',not zero(Lbad*ls[3]-ratio*ls[3]))
    # A fixed Hermitian M can realize this non-Hermitian off-diagonal code block.
    MM=s.zeros(16);MM[4:8,:4]=Lbad;MM[:4,4:8]=Lbad.T
    eq('nonlinear_test_operator_still_Hermitian',MM.T,MM)
    for k,expected in ((1,229),(3,173),(4,148)):
        eq(f'dimension_of_history_uniform_operator_class_{k}',(16-k)**2+4,expected)
    return {'schema':'d0-memory-preserving-source-code/1','exact_check_count':len(CHECKS),
      'checks':CHECKS,'general_creator_frame':'F=(A-B)I+B11^T, A>B>0',
      'full_internal_dimension':16,'memory_code_dimension':4,'syndrome_dimension':4,
      'memory_masks':[0,1,14,15],
      'source_map':'y=2 Gamma h/(1+h^T Gamma h) on balanced logical preparations',
      'retained_history':'same isometry for every own balanced orbit state',
      'nonlinear_history_test':'four even-tail states for memory-kernel projection; five for every affine first-order Hessian row',
      'fixture':{'A':'7/48','B':'1/16','is_native_root':False},
      'new_native_kernel_or_curved_root':False,'physical_encoder_admission':False,'GR_closed':False}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
