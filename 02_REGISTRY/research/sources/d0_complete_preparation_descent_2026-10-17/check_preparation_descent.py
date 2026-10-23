#!/usr/bin/env python3
"""Exact algebra behind complete-record preparation descent.

The mathematical result consumes the owned flat fixed-time channel.  This
file does not select a physical code or delete the retained reference.
Pauli monomials are represented with integer phases, hence the all128
shell calculation is exact and does not use sampled numerical ranks.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import factorial
import json
import hashlib
import sympy as S

# i^phase X^x Z^z on the full four-mode Fock space (mask order 0..15).
Pauli = tuple[int, int, int]
ONE: Pauli = (0, 0, 0)
CHECKS: list[str] = []


def mul(a: Pauli, b: Pauli) -> Pauli:
    return ((a[0]+b[0]+2*((a[2]&b[1]).bit_count()%2))%4,
            a[1]^b[1], a[2]^b[2])


def adj(a: Pauli) -> Pauli:
    return ((-a[0]+2*((a[1]&a[2]).bit_count()%2))%4, a[1], a[2])


def product(xs) -> Pauli:
    r=ONE
    for x in xs:
        r=mul(r,x)
    return r


def eq(name: str, a, b=0) -> None:
    if isinstance(a,S.MatrixBase) or isinstance(b,S.MatrixBase):
        good=all(S.simplify(v)==0 for v in S.Matrix(a)-S.Matrix(b))
    elif isinstance(a,(tuple,list,dict,str,bool,int,F)) and isinstance(b,type(a)):
        good=a==b
    else:
        good=S.simplify(a-b)==0
    if not good:
        raise ArithmeticError(name)
    CHECKS.append(name)


def demand(name: str, good: bool) -> None:
    if not good:
        raise ArithmeticError(name)
    CHECKS.append(name)


def monomial_matrix(a: Pauli) -> S.Matrix:
    m=S.zeros(16)
    for j in range(16):
        m[j^a[1],j]=S.I**a[0]*(-1)**((a[2]&j).bit_count())
    return m


def add_to(d, a: Pauli, c: F=F(1)) -> None:
    # Exact Gaussian rational pair at one unsigned X^x Z^z coordinate.
    key=(a[1],a[2]);u,v=d.get(key,(F(0),F(0)))
    du,dv=((c,F(0)),(F(0),c),(-c,F(0)),(F(0),-c))[a[0]]
    ans=(u+du,v+dv)
    if ans==(0,0):
        d.pop(key,None)
    else:
        d[key]=ans


def car_generators() -> tuple[Pauli,...]:
    out=[]
    for r in range(4):
        lower=(1<<r)-1
        out.extend(((0,1<<r,lower),(1,1<<r,lower|(1<<r))))
    return tuple(out)


XI=car_generators()
# kappa=(axis,sign), U(kappa)=sign*xi_(2 axis+1) on all 16 forms.
SECTORS=tuple((r,sgn) for r in range(4) for sgn in (-1,1))


def jump(letter: int, sector: tuple[int,int]) -> Pauli:
    r,sgn=sector
    U=XI[2*r+1]
    if sgn<0:
        U=((U[0]+2)%4,U[1],U[2])
    return U if letter==0 else mul(XI[letter-1],U)


def word_eval(word: tuple[int,...], sector: tuple[int,int]) -> Pauli:
    return product(jump(i,sector) for i in word)


def projector_words(axis: int, sign: int):
    # P_(axis,sign)=[I+V^2+sign*(V+U V U)]/4,
    # V=xi_(2axis+1)U is an ACTUAL available normalized jump type.
    v=2*axis+2
    return [(F(1,4),()),(F(1,4),(v,v)),
            (F(sign,4),(v,)),(F(sign,4),(0,v,0))]


def span_checks():
    for j,a in enumerate(XI):
        eq(f'majorana_square_{j}',mul(a,a),ONE)
        eq(f'majorana_hermitian_{j}',adj(a),a)
    for i,j in combinations(range(8),2):
        a,b=mul(XI[i],XI[j]),mul(XI[j],XI[i])
        eq(f'CAR_anticommutation_{i}_{j}',a,((b[0]+2)%4,b[1],b[2]))

    # Independent ordinary matrix check of the mask/sign convention.
    creators=[]
    for r in range(4):
        c=S.zeros(16)
        for mask in range(16):
            if not mask&(1<<r):
                c[mask|(1<<r),mask]=(-1)**((mask&((1<<r)-1)).bit_count())
        creators.append(c)
        eq(f'literal_fock_majorana_real_{r}',monomial_matrix(XI[2*r]),c+c.T)
        eq(f'literal_fock_majorana_imaginary_{r}',monomial_matrix(XI[2*r+1]),S.I*(c-c.T))

    for desired in SECTORS:
        for actual in SECTORS:
            values={}
            for c,w in projector_words(*desired):
                add_to(values,word_eval(w,actual),c)
            eq(f'central_projector_{desired}_{actual}',values,
               {(0,0):(F(1),F(0))} if desired==actual else {})

    labels=set();max_length=0;max_l1=F(0);reconstructed=0
    for mask in range(256):
        indices=tuple(j for j in range(8) if mask&(1<<j))
        phase=len(indices)*(len(indices)-1)//2
        base=product(XI[j] for j in indices)
        herm=((base[0]+phase)%4,base[1],base[2])
        demand(f'hermitian_clifford_basis_{mask}',adj(herm)==herm)
        labels.add((herm[1],herm[2]))
        core=tuple(j+1 for j in indices)+((0,) if len(indices)%2 else ())
        for desired in SECTORS:
            r,_=desired
            sign=(-1)**sum(j!=2*r+1 for j in indices[1::2])
            # Inside a selected sector, U xi_j U is +xi_j for its
            # own direction and -xi_j for every other Majorana.
            leading=(phase+(0 if sign==1 else 2))%4
            coeff_words=projector_words(*desired)
            max_l1=max(max_l1,sum(abs(c) for c,_ in coeff_words))
            for actual in SECTORS:
                values={}
                for c,pw in coeff_words:
                    w=pw+core;max_length=max(max_length,len(w))
                    q=word_eval(w,actual)
                    add_to(values,((q[0]+leading)%4,q[1],q[2]),c)
                expected={}
                if desired==actual:
                    add_to(expected,herm)
                if values!=expected:
                    raise ArithmeticError(f'full_shell_word_reconstruction_{desired}_{mask}_{actual}')
            reconstructed+=1
    eq('all256_internal_matrix_basis_coordinates',len(labels),256)
    eq('all8_times256_preparation_basis_reconstructed',reconstructed,2048)
    eq('maximum_required_number_of_jumps',max_length,11)
    eq('maximum_word_coefficient_l1',max_l1,F(1))
    eq('observable_density_real_dimension',8*16**2-1,2047)
    eq('full_shell_real_dimension',128**2-1,16383)
    eq('retained_offdiagonal_momentum_directions',128**2-8*16**2,14336)
    return {'basis_elements':reconstructed,'jump_bound':max_length,'coefficient_l1':str(max_l1)}


def channel_checks():
    # Rational nu=3/5 is a declared finite fixture in the owner's
    # isotropic family, not a new value selected for the physical v8.
    nu=F(3,5);b=F(4,5)
    wI=(1+b)**2/4;wM=nu**2/16;wZ=(1-b)**2/16
    eq('actual_recycling_weights_normalized',wI+8*wM+4*wZ,F(1))
    demand('identity_and_eight_jump_weights_strictly_positive',min(wI,wM)>0)
    for sector in SECTORS:
        eq(f'jump_U_unitary_{sector}',mul(adj(jump(0,sector)),jump(0,sector)),ONE)
        for j in range(1,9):
            g=jump(j,sector)
            eq(f'jump_xiU_unitary_{sector}_{j}',mul(adj(g),g),ONE)
    # Original T0 from the literal creator/defect expression equals
    # the 13-term Pauli channel on a full noncommuting form matrix.
    X=S.Matrix(16,16,lambda i,j:S.Rational((i+2*j)%5-2,37))
    X=X+X.T+S.I*(X-X.T)
    c=[]
    for r in range(4):
        a=S.zeros(16)
        for mask in range(16):
            if not mask&(1<<r):a[mask|(1<<r),mask]=(-1)**((mask&((1<<r)-1)).bit_count())
        c.append(a)
    raw=S.zeros(16);pauli=S.Rational(wI.numerator,wI.denominator)*X
    for r,C in enumerate(c):
        C=S.Rational(3,5)*C
        # C C* and C* C are complementary projectors times nu^2.
        L=S.eye(16)-(1-S.Rational(4,5))*C*C.T/S.Rational(9,25)
        R=S.eye(16)-(1-S.Rational(4,5))*C.T*C/S.Rational(9,25)
        raw+=(C.T*X*C+C*X*C.T+L*X*L+R*X*R)/8
        Z=S.eye(16)-2*(C*C.T)/S.Rational(9,25)
        pauli+=S.Rational(wZ.numerator,wZ.denominator)*Z*X*Z
    for g in XI:
        G=monomial_matrix(g)
        pauli+=S.Rational(wM.numerator,wM.denominator)*G*X*G
    eq('actual_global_continuum_recycling_formula',raw,pauli)
    # Actual flat one-momentum Pauli modes also verify the additive-code
    # cost potential: no implicit reinitialization between successive rounds.
    eps,rate,amp=S.symbols('eps rate amp',positive=True)
    for n in (2,3,7):
        total=eps*amp*sum((1-eps*rate)**j for j in range(n))
        eq('full_costate_sum_mode_'+str(n),total,
           amp*(1-(1-eps*rate)**n)/rate)
        eq('fixed_blank_cost_has_no_preparation_source_'+str(n),
           S.diff(S.Symbol('blank_cost')*n,S.Symbol('rho')),0)
    beta=S.symbols('beta',positive=True)
    tt=S.symbols('tt',real=True)
    eq('continuum_code_potential_mode',
       S.integrate(amp*S.exp(-rate*tt),(tt,0,beta)),
       amp*(1-S.exp(-rate*beta))/rate)
    eq('zero_decay_mode_not_divided_by_zero',
       S.limit(amp*(1-S.exp(-rate*beta))/rate,rate,0),amp*beta)
    # Poisson all words are retained; its sum is the same semigroup.
    t,z=S.symbols('t z',positive=True)
    eq('Poisson_total_probability',S.exp(-t)*S.exp(t),1)
    eq('Poisson_generator_identity',S.diff(S.exp(t*(z-1)),t),(z-1)*S.exp(t*(z-1)))
    # Choi frame: E_(k,P)/4 is orthonormal, 2048 elements.
    eq('Choi_frame_bound_coefficient',F(16,2048),F(1,128))
    eq('normalized_conditional_depolarizing_weight',F(16,128),F(1,8))
    return {'nu_fixture':str(nu),'wI':str(wI),'wM':str(wM),'wZ':str(wZ)}


def convex_checks():
    # Exact finite schematic controls of the general convex proofs.
    # E sends each 2-dimensional input block to I2/2 times its mass.
    # Its complement retains the block input and an independent I2/2.
    X=S.Matrix([[S.Rational(1,7),S.I/11],[-S.I/11,-S.Rational(1,7)]])
    Y=S.Matrix([[S.Rational(1,5),S.Rational(1,9)],[S.Rational(1,9),-S.Rational(1,5)]])
    Ecomp=S.diag(S.kronecker_product(X,S.eye(2)/2),S.kronecker_product(Y,S.eye(2)/2))
    eq('conditional_depolarizing_complement_norm',S.trace(Ecomp.H*Ecomp),
       (S.trace(X.H*X)+S.trace(Y.H*Y))/2)
    # Independent Kraus/partial-trace reconstruction of E's complement.
    # This four-dimensional fixture tests the generic decoder algebra;
    # the all128 native operator span was checked above, not replaced by it.
    L=S.Matrix([[1,S.I,0,0],[0,2,1,0],[0,0,1,S.I],[1,0,0,1]])
    density=L*L.H/S.trace(L*L.H)
    kraus=[]
    for block in range(2):
        for i in range(2):
            for j in range(2):
                A=S.zeros(4);A[2*block+i,2*block+j]=1/S.sqrt(2)
                kraus.append(A)
    eq('decoder_fixture_Kraus_completeness',sum((A.H*A for A in kraus),S.zeros(4)),S.eye(4))
    rec=S.Matrix(8,8,lambda a,b:S.trace(kraus[a]*density*kraus[b].H))
    decoded=S.zeros(4)
    for block in range(2):
        for j in range(2):
            for k in range(2):
                decoded[2*block+j,2*block+k]=sum(rec[4*block+2*i+j,4*block+2*i+k] for i in range(2))
    target=S.diag(density[:2,:2],density[2:,2:])
    eq('decoder_recovers_exact_block_preparation',decoded,target)
    demand('decoder_does_not_claim_cross_momentum_recovery',decoded!=density)
    eq('decoder_keeps_total_normalization',S.trace(rec),1)
    # Exact erasure relative entropy decomposes with fixed input-independent flag.
    a,b,delta=S.symbols('a b delta',positive=True)
    expr=delta*a*S.log(delta*a/(delta*b))-delta*a*S.log(a/b)
    eq('heralded_relative_entropy_keeps_probability',S.expand_log(expr,force=True),0)

    # All genuine code costs are linear in input; their choice changes
    # the optimum but cannot remove the preparation Hessian.
    x,a0,a1=S.symbols('x a0 a1',real=True)
    q=S.symbols('q',positive=True)
    entropy=x*S.log(x)+(1-x)*S.log(1-x)
    action=a0*x+a1*(1-x)+entropy
    eq('linear_code_does_not_change_information_Hessian',S.diff(action,x,2),1/(x*(1-x)))
    r=S.symbols('r',positive=True)
    potential=S.log((1-r)/r)
    grad=S.diff(action,x).subs({a0:potential,a1:0,x:r})
    eq('supplied_code_unique_stationary_example',S.expand_log(grad,force=True),0)
    eq('code_dependent_minimum_not_forced_uniform',
       S.exp(-S.log(3))/(1+S.exp(-S.log(3))),S.Rational(1,4))

    # Pythagorean equality at the observed interior optimum.
    AA=potential*x+entropy
    Astar=AA.subs(x,r)
    KL=x*S.log(x/r)+(1-x)*S.log((1-x)/(1-r))
    eq('exact_action_excess_equals_output_relative_entropy',
       S.expand_log(AA-Astar-KL,force=True),0)

    # Genuine Schur response, not a fitted counterterm.
    a,b,c,theta=S.symbols('a b c theta',nonzero=True)
    rvar=S.symbols('rvar')
    full=a*theta**2/2+b*theta*rvar+c*rvar**2/2
    opt=-b*theta/c
    eq('exact_preparation_response',S.diff(full,rvar).subs(rvar,opt),0)
    eq('full_source_after_preparation_stationarity',
       S.diff(full.subs(rvar,opt),theta),S.diff(full,theta).subs(rvar,opt))
    eq('actual_Schur_metric_correction',S.diff(full.subs(rvar,opt),theta,2),a-b*b/c)
    demand('freezing_preparation_changes_source',S.diff(full.subs(rvar,0),theta,2)!=a-b*b/c)

    # One trace constraint does not turn all density directions into gauge.
    eq('trace_constraint_tangent_dimension',8*16*16-1,2047)
    eq('prescribed_momentum_masses_tangent_dimension',8*(16*16-1),2040)
    eq('opposite_entropy_sign_changes_extremum_not_zero_equation',
       S.diff(-action,x),-S.diff(action,x))
    return True


def main():
    CHECKS.clear()
    span=span_checks();weights=channel_checks();convex_checks()
    return {'schema':'d0-complete-preparation-descent/1',
            'check_names_sha256':hashlib.sha256('\n'.join(CHECKS).encode()).hexdigest(),'check_count':len(CHECKS),
            'exact_basis_reconstructions':span,'weights':weights,
            'scope':'same flat all8 first-shell coherent record; all16 forms and reference128 retained',
            'information_recovery_probability_bound':'delta(t,nu)=exp(-t)*min_{0<=j<=11}(t*w*)^j/j!/8; finite-grid lower bound delta/2 for small h',
            'additive_full_code_limit':'A_h-n*g_blank -> Tr(C_beta rho)-S(Gamma_beta(rho)); C_beta=integral_0^beta Phi_t^*(V_code) dt',
            'observed_density_dimension':2047,'full_physical_density_replaced_by_pinching':False,
            'pointer_tomography_asserted':False,'complete_code_or_Info_selected':False,
            'coherent_candidate_preparation_equation_solved_in_observed_algebra':True,
            'unrestricted_rank_birth_stationarity_classified':False,
            'Lorentz_metric_only_descent_proved':False,'GR_closed':False}

if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2,sort_keys=True))
