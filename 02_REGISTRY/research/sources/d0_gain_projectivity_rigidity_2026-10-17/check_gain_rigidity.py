#!/usr/bin/env python3
"""Scalar branch-gain rigidity and its exact scope controls.

The native fixture copies the pinned literal creator/Walsh formulas; it
executes no earlier certificate.  The analytic uniqueness theorem still
requires scalar-event locality and an admitted composition domain.
"""
import argparse
import json
from itertools import product
import sympy as s

p=s.Symbol('p', positive=True)
REL=p*p+p-1
CHECKS=[]

def alg(x):
    num, den=s.fraction(s.cancel(x))
    if den.has(p):
        return s.cancel(s.rem(s.rem(num,REL,p)*s.invert(s.rem(den,REL,p),REL,p),REL,p))
    return s.cancel(s.rem(num,REL,p)/den)

def eq(name,a,b=0,logarithms=False):
    entries=list(a-b) if isinstance(a,s.MatrixBase) else [a-b]
    fn=(lambda x:s.simplify(s.expand_log(x,force=True))) if logarithms else alg
    if not all(fn(x)==0 for x in entries):
        raise ArithmeticError(name)
    CHECKS.append(name)

def yes(name,x):
    if not bool(x):raise ArithmeticError(name)
    CHECKS.append(name)

ORDER=(0,2,3,1)
def creator(r):
    C=s.zeros(16)
    for mask in range(16):
        if not mask&(1<<r):
            C[mask|(1<<r),mask]=(-1)**sum(bool(mask&(1<<j)) for j in ORDER[:ORDER.index(r)])
    return C


def rows(C,nu,b,phases):
    I=s.eye(16); numbers=[c*c.H for c in C]
    L=[I+(b-1)*a for a in numbers];R=[b*I+(1-b)*a for a in numbers]
    tops=[]
    for r in range(4):
        P=phases[r]*nu*C[r]
        for pair in ((P,L[r]),(P.H,R[r]),(-nu*C[r],-L[r]),(-nu*C[r].H,-R[r])):
            tops.extend((pair,pair))
    return {(label,co):sum(((-1)**((label&j).bit_count())*tops[j][co] for j in range(32)),s.zeros(16))/32
            for label in range(32) for co in range(2)}


def native_fixture():
    # Actual ACDB full16 representation, all8 momenta; no rank reduction.
    C=[creator(r) for r in range(4)];I=s.eye(16)
    for i,j in product(range(4),repeat=2):
        eq('CAR_%d%d'%(i,j),C[i]*C[j].H+C[j].H*C[i],I if i==j else s.zeros(16))
    nu,b,h=s.Rational(3,5),s.Rational(4,5),s.Rational(1,4)
    epsilon=p*p*h*h/64
    lam=2*nu*nu/(h*h)
    scalar=lam*(1-b)**2/16
    averages=[]
    native_v=None
    for r,sign in product(range(4),(-1,1)):
        phases=[s.S.One]*4;phases[r]=sign*s.I
        D=nu/h*sum(((phases[j]-1)*C[j]+(s.conjugate(phases[j])-1)*C[j].H for j in range(4)),s.zeros(16))
        eq('shell_Delta_%d_%d'%(r,sign),D*D,lam*I)
        Ns=rows(C,nu,b,phases)
        N=Ns[(6,1)]
        E=D*N*N.H*D
        eq('marked_average_%d_%d'%(r,sign),s.trace(E)/16,scalar)
        averages.append(s.trace(E))
        if (r,sign)==(0,1):
            eq('marked_vacuum_probability',E[0,0],scalar)
            eq('marked_spatial_oneform_probability',E[2,2],0)
            A=h*D/16
            B=I-2*p*p*A*A
            effects=[B*B,4*p**3*A**4]
            for label,co in product(range(32),range(2)):
                if (label,co)==(0,0):continue
                V=A*Ns[label,co]*Ns[label,co].H*A
                effects.extend((4*p**4*V,4*p**3*V))
            eq('actual128_outcomes_complete',sum(effects,s.zeros(16)),I)
            yes('all128_outcomes_retained',len(effects)==128)
            native_v=E[0,0]-E[2,2]
    eq('full128_shell_marked_mean',sum(averages)/128,scalar)
    eq('full128_shell_nonzero_marked_velocity',native_v,scalar)
    yes('marked_preparation_family_is_not_constant',scalar>0)
    e=epsilon*lam-epsilon**2*lam**2/4
    for depth in (1,2,4):
        coeff=epsilon*scalar*sum((1-e)**j for j in range(depth))
        eq('same_tape_first_exit_mark_%d'%depth,coeff,epsilon*scalar*(1-(1-e)**depth)/e)
    return {'all_outcomes':128,'shell_momenta':8,'forms':16,'reference':128,
            'mark':'label6/coefficient1/both ports',
            'readout_family':'P(first mark)=C_h (1+t), |t|<1/128',
            'native_preparation_admission_proved':False}


def law_checks(mutant):
    q,mu,r,nu=s.symbols('q mu r nu', positive=True)
    ell=s.Symbol('ell',positive=True)
    alpha=s.Symbol('alpha',real=True)
    I=lambda x,y:alpha*s.log(x/y)/ell
    eq('neutral_local_gain',I(q,q),0,True)
    eq('independent_branch_additivity',I(q*r,mu*nu),I(q,mu)+I(r,nu),True)
    t=s.Symbol('t',real=True)
    qs=[s.Rational(1,5)+t/7,s.Rational(3,10)-t/11,s.Rational(1,2)-4*t/77]
    ms=[s.Rational(1,4),s.Rational(1,3),s.Rational(5,12)]
    eq('affine_probability_curve_normalized',sum(qs),1)
    eq('positive_reference_normalized',sum(ms),1)
    Z=sum(m*(u/m)**alpha for u,m in zip(qs,ms))
    F=sum(m*(u/m)**alpha*(s.diff(u,t)/u)**2 for u,m in zip(qs,ms))
    eq('exact_raw_normalizer_second_source',s.diff(Z,t,2),alpha*(alpha-1)*F,True)
    eq('trivial_gain_projective',Z.subs(alpha,0),1,True)
    exponent=2 if mutant=='wrong_exponent' else 1
    eq('nontrivial_normalized_local_law',Z.subs(alpha,exponent),1,True)
    eq('squared_gain_has_nonzero_normalizer_curvature',
       s.diff(Z.subs(alpha,2),t,2),2*sum(s.diff(u,t)**2/m for u,m in zip(qs,ms)),True)
    yes('squared_gain_source_strictly_nonzero',s.diff(Z.subs(alpha,2),t,2)>0)
    # Moving code terms cancel pointwise only for the matched same-branch law.
    qt=s.Rational(1,3)+t/9;mt=s.Rational(2,5)+t/13
    cost=-s.log(mt)/ell
    gain=s.log(qt/mt)/ell
    price=cost-gain
    eq('all_moving_code_source_terms_cancel',s.diff(price,t),-s.diff(qt,t)/(ell*qt),True)
    eq('second_moving_code_source_terms_cancel',s.diff(price,t,2),-s.diff(s.log(qt),t,2)/ell,True)
    # Full terminal price and source, with normalized probabilities.
    act=sum(u*(-s.log(u)/ell) for u in qs)
    grad=-sum(s.diff(u,t)*s.log(u) for u in qs)/ell
    eq('whole_cut_source',s.diff(act,t),grad,True)
    eq('affine_preparation_Fisher_source',s.diff(act,t,2),-sum(s.diff(u,t)**2/u for u in qs)/ell,True)
    # A two-level complete experiment, all four leaves and both local laws.
    roots=[s.Rational(2,7),s.Rational(5,7)]
    children=[[s.Rational(1,3),s.Rational(2,3)],[s.Rational(3,5),s.Rational(2,5)]]
    leaves=[roots[i]*children[i][j] for i,j in product(range(2),repeat=2)]
    eq('all_finite_tree_leaves_kept',sum(leaves),1)
    H=lambda ps:-sum(z*s.log(z) for z in ps)
    eq('full_entropy_chain_no_postselection',H(leaves),H(roots)+sum(roots[i]*H(children[i]) for i in range(2)),True)
    # An accepted subset is not a complete cut; N and dN must be kept.
    raw=[s.Rational(1,5)+t/20,s.Rational(1,10)-t/30]
    N=sum(raw);conditional=[u/N for u in raw]
    accepted_price=-sum(u/N*s.log(u) for u in raw)
    rhs=H(conditional)-(0 if mutant=='drop_return_normalizer' else s.log(N))
    eq('incomplete_cut_keeps_actual_normalizer',accepted_price,rhs,True)
    return {'possible_exponents':[0,1],'nontrivial_exponent':1,
            'new_hypotheses_are_native_theorems':False}


def contextual_control():
    # Normalization+composition+neutrality do NOT force scalar-event locality.
    # alpha=2 is fixed once, not a fitted source or a catalogue of theories.
    def tilted(q,m):
        w=[q0*q0/m0 for q0,m0 in zip(q,m)]
        Z=sum(w)
        return [u/Z for u in w],Z
    q=[s.Rational(1,3),s.Rational(2,3)];m=[s.Rational(2,5),s.Rational(3,5)]
    r=[s.Rational(1,4),s.Rational(3,4)];n=[s.Rational(3,7),s.Rational(4,7)]
    tq,Z=tilted(q,m);tr,W=tilted(r,n)
    tprod,ZW=tilted([a*b for a in q for b in r],[a*b for a in m for b in n])
    eq('contextual_gain_normalized',sum(tq),1)
    eq('contextual_gain_independent_composition',s.Matrix(tprod),s.Matrix([a*b for a in tq for b in tr]))
    eq('contextual_gain_normalizer_factorizes',ZW,Z*W)
    eq('contextual_gain_neutral_reference',s.Matrix(tilted(m,m)[0]),s.Matrix(m))
    yes('contextual_gain_not_likelihood',tq!=q)
    # Same single-event q0,mu0; different siblings -> a different event weight.
    qA=[s.Rational(1,4),s.Rational(1,4),s.Rational(1,2)]
    qB=[s.Rational(1,4),s.Rational(1,8),s.Rational(5,8)]
    ref=[s.Rational(1,3)]*3
    yes('locality_hypothesis_has_independent_content',tilted(qA,ref)[0][0]!=tilted(qB,ref)[0][0])
    return {'all_but_scalar_locality_hold':True,'same_native_Born_law_claimed':False}


def birth_checks(mutant):
    x,c=s.symbols('x c',positive=True)
    # Analytic regular terms cannot cancel the unique x^2 log x^2 from births.
    q=c*x*x
    birth=-q*s.log(q)
    eq('true_birth_first_source',s.diff(birth,x),-2*c*x*(s.log(c*x*x)+1),True)
    expected=-2*c*s.log(c*x*x)-(0 if mutant=='drop_birth_constant' else 6*c)
    eq('true_birth_second_source',s.diff(birth,x,2),expected,True)
    eq('birth_C1_but_not_C2_first_limit',s.limit(s.diff(birth,x),x,0,dir='+'),0,True)
    yes('birth_second_source_diverges',s.limit(s.diff(birth,x,2),x,0,dir='+')==s.oo)
    h=s.Symbol('h',positive=True);r=s.Symbol('r',positive=True)
    eq('refinement_rare_log_coefficient',-h*h*r*s.log(h*h*r),2*r*h*h*s.log(1/h)-h*h*r*s.log(r),True)
    eq('rare_coefficient_variation',s.diff(-h*h*r*s.log(h*h*r),r),-h*h*(s.log(h*h*r)+1),True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mutant',default='');args=ap.parse_args()
    CHECKS.clear()
    fixture=native_fixture()
    law=law_checks(args.mutant)
    contextual=contextual_control()
    birth_checks(args.mutant)
    print(json.dumps({'schema':'d0-local-gain-projectivity/1','checks':CHECKS,
      'check_count':len(CHECKS),'native_fixture':fixture,'law':law,'scope_control':contextual,
      'physical_Info_selected':False,'all_pointer_births_computed':False,
      'Einstein_source_identity_proved':False,'GR_closed':False},indent=2,ensure_ascii=False,sort_keys=True))

if __name__=='__main__':main()
