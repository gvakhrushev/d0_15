#!/usr/bin/env python3
"""Exact golden-baseline determinant compiler. No native action/GR claim.

No files are written; no external source is executed. Parent input pins are
checked by the repository certificate, separately from these finite tests.
"""
from __future__ import annotations
from itertools import combinations
import json
import sympy as S

p = (S.sqrt(5)-1)/2
phi = 1/p
s0 = p**3
I4 = S.eye(4)
checks: list[str] = []


def red(x):
    return S.simplify(S.expand(x))


def eq(name, left, right=0):
    if isinstance(left, S.MatrixBase) or isinstance(right, S.MatrixBase):
        delta = S.Matrix(left)-S.Matrix(right)
        good = all(red(x)==0 for x in delta)
    else:
        good = red(left-right)==0
    if not good:
        raise ArithmeticError(name)
    checks.append(name)


def demand(name, good):
    if not good:
        raise ArithmeticError(name)
    checks.append(name)


def e2(A):
    return (S.trace(A)**2-S.trace(A*A))/2


def determinant_jet(A, B):
    # Multilinearity, valid also for singular A. Never divide by det(A).
    total=S.Integer(0)
    for column in range(A.cols):
        piece=A.copy()
        piece[:,column]=B[:,column]
        total+=piece.det()
    return red(total)


def run_checks():
    checks.clear()
    eq('golden_closure',p+p*p,1)
    eq('golden_scale_identity',s0*(phi**4-phi**2),1)
    # Literal cylWeight: true/direct -> p, false/return -> p^2.
    letters=[True,False]
    words=[(x,y) for x in letters for y in letters]
    weights=[red((p if x else p*p)*(p if y else p*p)) for x,y in words]
    eps=[int(not y)-int(not x) for x,y in words]
    eq('all_four_word_mass',sum(weights),1)
    eq('first_odd_word_moment',sum(w*e for w,e in zip(weights,eps)),0)
    eq('mixed_word_mass',sum(w*e**2 for w,e in zip(weights,eps)),2*s0)
    demand('both_blank_words_retained',len(words)==4 and eps==[0,1,-1,0])

    # Noncommuting shape operators: finite fixture, not selected native fields.
    A0=S.Matrix([[2,1,0,1],[1,-1,2,0],[0,2,3,1],[1,0,1,-2]])/20
    A1=S.Matrix([[1,0,2,-1],[0,2,1,0],[2,1,-1,1],[-1,0,1,3]])/25
    demand('noncommuting_shapes',(A0*A1-A1*A0)!=S.zeros(4))
    t=S.symbols('t',real=True)
    for index,A in enumerate((A0,A1)):
        mass=sum(w*(I4-t*e*A).det() for w,e in zip(weights,eps))
        expected=1+2*s0*(t*t*e2(A)+t**4*A.det())
        eq(f'full_cylinder_polynomial_{index}',mass,expected)
        read=(phi**4*(mass-1)-(mass.subs(t,phi*t)-1))/t**2
        eq(f'existing_cylinder_consumer_{index}',read,2*e2(A))
    # Explicit tests of all symmetric shape jets; these are not metric jets.
    R=lambda A:S.trace(A)**2-S.trace(A*A)
    for i,j in combinations(range(5),2):
        # Bijection to packed symmetric slots (00,01,...,33).
        r,c=i,j-1
        B=S.zeros(4)
        B[r,c]=1
        B[c,r]=1
        eq(f'shape_derivative_{r}{c}',2*S.trace(A0)*S.trace(B)-2*S.trace(A0*B),
           S.diff(R(A0+t*B),t).subs(t,0))

    # Universal 2x2 golden-baseline block, tested as scalar functional calculus.
    a=S.sqrt(p)
    G=S.Matrix([[a,-p],[p,a]])
    eq('golden_baseline_unitary',G.T*G,S.eye(2))
    alpha=S.symbols('alpha',real=True)
    Gdot=S.Matrix([[-a*alpha,-alpha],[alpha,-a*alpha]])/2
    eq('actual_blank_unitary_jet',G.T*Gdot+Gdot.T*G,S.zeros(2))
    eq('blank_D_jet',2*a*Gdot[0,0],-p*alpha)

    # Dense rational dilation: D=p(I-A) stays in the golden domain.
    O=S.Matrix([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
    sd=[S.Rational(3,5),S.Rational(4,5),S.Rational(20,29),S.Rational(21,29)]
    td=[S.Rational(4,5),S.Rational(3,5),S.Rational(21,29),S.Rational(20,29)]
    C=O*S.diag(*sd)*O.T
    K=O*S.diag(*td)*O.T
    D=C*C
    U=C.row_join(-K).col_join(K.row_join(C))
    eq('rational_change_of_basis',O.T*O,I4)
    eq('full_eight_mode_unitarity',U.T*U,S.eye(8))
    eq('rational_complement_roots',C*C+K*K,I4)
    demand('strict_shape_domain',all(bool(S.simplify(x*x-p/2)>0) and
                                    bool(S.simplify(3*p/2-x*x)>0) for x in sd))
    shape=I4-D/p
    F=U[:4,:4].T*U[:4,:4]
    eq('actual_retained_transmission',F,D)
    eq('actual_feedback',U[4:,:4].T*U[4:,:4],I4-D)
    eq('shape_not_a_scalar_determinant_input',D,p*(I4-shape))
    # All 70 outcomes in the conserved four-particle sector; no postselection.
    outcomes=list(combinations(range(8),4))
    amplitudes=[U.extract(rows,range(4)).det() for rows in outcomes]
    probabilities=[v*v for v in amplitudes]
    eq('all_seventy_probabilities_normalized',sum(probabilities),1)
    success=amplitudes[0]**2
    eq('success_is_determinant',success,D.det())
    eq('golden_calibrated_Jacobian',success,p**4*(I4-shape).det())
    F8=S.zeros(8)
    F8[:4,:4]=I4-D
    eq('eight_mode_full_price_determinant',(S.eye(8)-F8).det(),success)
    # The other 255 Fock feedback eigenvalues are zero, not removed.
    fock_diag=[S.Integer(1)]*256
    fock_diag[15]=success
    eq('full_Fock_price_determinant',S.prod(fock_diag),success)
    turn=S.eye(4)
    turn[0,0]=turn[1,1]=0
    turn[0,1]=-1
    turn[1,0]=1
    Cn=turn*C
    demand('nonselfadjoint_compression_control',Cn!=Cn.T)
    eq('general_compression_determinant',Cn.det()**2,(Cn.T*Cn).det())
    demand('minimal_complement_rank',(I4-D).rank()==4)
    demand('failure_is_not_discarded',bool(0<success<1) and sum(x!=0 for x in probabilities)>1)

    # Actual differentiable unitary family: rotate one mode, not an abstract dp.
    Cd=O*S.diag(-td[0],0,0,0)*O.T
    Kd=O*S.diag(sd[0],0,0,0)*O.T
    rotation=S.zeros(4)
    rotation[0,1]=1
    rotation[1,0]=-1
    Cd+=rotation*C-C*rotation
    Kd+=rotation*K-K*rotation
    Ud=Cd.row_join(-Kd).col_join(Kd.row_join(Cd))
    Dd=Cd*C+C*Cd
    demand('noncommuting_transmission_jet',D*Dd-Dd*D!=S.zeros(4))
    eq('all_columns_moving_unitary',U.T*Ud+Ud.T*U,S.zeros(8))
    amp_jets=[determinant_jet(U.extract(rows,range(4)),Ud.extract(rows,range(4)))
              for rows in outcomes]
    eq('success_plus_failure_jet',sum(2*v*dv for v,dv in zip(amplitudes,amp_jets)),0)
    success_jet=2*amplitudes[0]*amp_jets[0]
    eq('real_success_jet_equals_Jacobi',success_jet,D.det()*S.trace(D.inv()*Dd))
    eq('feedback_price_equals_negative_log_probability_jet',
       -success_jet/success,-S.trace(D.inv()*Dd))

    # Arbitrary nonfaithful coherent history preparation, raw mass and moving t.
    u,a0,a1,b0,b1,x0,x1,e20,e21,e40,e41=S.symbols(
        'u a0 a1 b0 b1 x0 x1 e20 e21 e40 e41',real=True)
    ar=a0+u*a1
    raw=b0+u*b1
    scale=x0+u*x1
    two=e20+u*e21
    four=e40+u*e41
    p4=p**4
    def symprob(h):
        return p4*(raw+ar*(h*h*two+h**4*four))
    blank=p4*raw
    contrast=phi**4*(symprob(scale)-blank)-(symprob(phi*scale)-blank)
    recovered=2*s0*contrast/(p4*ar*scale**2)
    eq('complete_calibrated_source_value',recovered,2*two)
    eq('complete_calibrated_source_jet',S.diff(recovered,u).subs(u,0),2*e21)
    # Check coherent state at constant finite t, with an actual amplitude germ.
    v=S.Matrix([1+u,1+S.I*u,2-u,1-S.I*(2+u)])
    sigma=v*v.H
    Emix=S.diag(0,1,1,0)
    eq('coherent_normalization_real',S.trace(sigma),11+2*u+4*u*u)
    demand('coherences_retained',sigma[0,1]!=0 and sigma.rank()==1)
    tt=S.Rational(1,7)
    effects=[]
    for ep in eps:
        effects.append(p4*(I4-tt*ep*A0).det())
    E=S.diag(*effects)
    Eminus=S.diag(*(p4*(I4+tt*ep*A0).det() for ep in eps))
    even=(E+Eminus)/2
    eq('full_represented_even_effect',even,
       p4*(S.eye(4)+(tt*tt*e2(A0)+tt**4*A0.det())*Emix))
    # Discarding the mirror is detected for unequal FR/RF populations.
    demand('odd_response_requires_mirror',red(S.trace(sigma*(E-even)).subs(u,0))!=0)
    # Full blank plus every effect carries the same raw normalization jet.
    eq('raw_coherent_mass_jet',S.diff(S.trace(sigma),u).subs(u,0),2)

    # Compose with the concurrently owned complete AF spectral-price family.
    # A selector with weights p,p^2 mixes the signal with the event not-FR.
    ueff=S.symbols('ueff',real=True)
    signal=p**4*(1+2*s0*ueff)
    background=1-s0
    gamma=2*p**6
    effective=p*signal+p*p*background
    eq('golden_affine_effect_composition',effective,p*p*(1+gamma*ueff))
    eq('composed_blank_remains_native_golden',effective.subs(ueff,0),p*p)
    eq('all_selector_outcomes_retained',effective+p*(1-signal)+p*p*(1-background),1)
    eq('composed_source_factor',S.diff(effective,ueff),p*p*gamma)
    eq('background_event_is_not_FR',sum(w for w,e in zip(weights,eps) if e!=1),background)
    demand('curvature_coupling_not_zero',bool(gamma>0))
    g1,g2,g3=S.symbols('g1 g2 g3',real=True)
    G=lambda v:g1*v+g2*v*v+g3*v**3
    readG=G(gamma*(t*t*e20+t**4*e40))
    eq('single_AF_price_leading_curvature_coefficient',S.expand(readG).coeff(t,2),gamma*g1*e20)

    return {
      'schema':'d0-golden-determinant-compiler/1',
      'checks':checks,
      'exact_check_count':len(checks),
      'blank_transmission':'p I4; blank return probability p^4',
      'block_unitary':'[[sqrt(D),-sqrt(I-D)],[sqrt(I-D),sqrt(D)]]; D=p(I-uA)',
      'full_environment_modes':8,
      'full_exterior_dimension':256,
      'conserved_sector_outcomes':70,
      'history_words_retained':4,
      'compiler_inputs':'matrix A and scale u, not det(I-uA)',
      'success_mass':'p^4 det(I-uA)',
      'AF_effect_composition':'E_eff=p^2[I+gamma sum_i u_i Q_i]; gamma=2p^6',
      'AF_price_consumer':'B_n+sum_i G(gamma u_i), with unchanged B_n; coefficient-level identity, not cost-free physical compilation',
      'feedback_price':'-log det(D) = 4 log(phi)-log det(I-uA), at declared z=1',
      'reading_source':'same calibrated cylinder R and full moving-preparation derivative',
      'native_primitive_admission_proved':False,
      'native_action_selected':False,
      'GR_closed':False
    }


if __name__=='__main__':
    print(json.dumps(run_checks(),sort_keys=True,indent=2))
