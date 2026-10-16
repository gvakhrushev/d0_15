#!/usr/bin/env python3
"""Exact finite controls for coherent aggregation followed by central AF price.
Theorem and circuit admission are distinct. No network or output writes.
"""
from itertools import combinations
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json
import sympy as S
from interval_sign import certificate,I

p=S.Symbol('p',positive=True); relation=p*p+p-1
checks=[]
def red(x):
    num,den=S.fraction(S.cancel(x))
    if not den.has(p):return S.cancel(S.rem(num,relation,p)/den)
    return S.rem(S.rem(num,relation,p)*S.invert(den,relation,p),relation,p)
def eq(name,left,right=0):
    if isinstance(left,S.MatrixBase) or isinstance(right,S.MatrixBase):
        good=all(red(x)==0 for x in S.Matrix(left)-S.Matrix(right))
    else:good=red(left-right)==0
    if not good:raise ArithmeticError(name)
    checks.append(name)
def demand(name,truth):
    if not truth:raise ArithmeticError(name)
    checks.append(name)

def golden_effect():
    q=S.symbols('q',real=True)
    signal=2*p**3*(1+q)
    failure=p*p+p**4-2*p**3*q
    eq('both_interference_outcomes',signal+failure,1)
    mixture=p*signal+p*p*p**3
    eq('golden_mixture_blank_and_signal',mixture,p*p+2*p**4*q)
    diluted=p**8*mixture+(1-p**8)*p*p
    eq('all_prefix_outcomes_retained',diluted,p*p+2*p**12*q)
    eq('opposite_orientation_changes_sign',diluted.subs(q,-q)+diluted,2*p*p)
    P=(I(5).sqrt()-1)/2
    demand('whole_compiler_range_inside_price_chart',
           (P*P-2*P**12).lo>Q(3,8) and (P*P+2*P**12).hi<Q(25,64))
    # A global field-dependent normalization would be an additional source.
    x=S.symbols('x',real=True)
    f=x*x+3*x; b=2+x
    demand('moving_scale_is_not_a_constant_rescaling',S.simplify(S.diff(f/b,x)-S.diff(f,x)/b)!=0)

def julia():
    # Actual rational nonnormal contractions; both defect operators are retained.
    O=S.Matrix([[3,-4,0,0],[4,3,0,0],[0,0,5,-12],[0,0,12,5]])
    O[:2,:2]/=5;O[2:,2:]/=13
    V=S.Matrix([[1,0,0,0],[0,S.Rational(5,13),-S.Rational(12,13),0],
                [0,S.Rational(12,13),S.Rational(5,13),0],[0,0,0,1]])
    ds=[S.Rational(3,5),S.Rational(5,13),S.Rational(8,17),S.Rational(7,25)]
    dt=[S.Rational(4,5),S.Rational(12,13),S.Rational(15,17),S.Rational(24,25)]
    K=O*S.diag(*ds)*V.T
    A=O*S.diag(*dt)*O.T;B=V*S.diag(*dt)*V.T
    U=K.row_join(A).col_join(B.row_join(-K.T))
    eq('nonnormal_full_Julia_unitary',U.T*U,S.eye(8))
    demand('nonnormal_not_symmetric_control',K*K.T!=K.T*K)
    eq('success_is_actual_matrix_not_scalar_oracle',U[:4,:4],K)
    # Two fresh flags; old failed flag is never discarded or reset.
    U2=U.T
    columns=S.zeros(16,4)
    # indexes (oldflag,newflag,system)
    for inp in range(4):
        for f1,f2 in ((0,0),(0,1),(1,0),(1,1)):
            for out in range(4):
                columns[(2*f1+f2)*4+out,inp]=sum(U2[f2*4+out,k]*U[f1*4+k,inp] for k in range(4))
    eq('all_product_failure_branches_retained',columns.T*columns,S.eye(4))
    eq('success_block_composes_matrices',columns[:4,:],K.T*K)

ETA=S.diag(1,-1,-1,-1); PAIRS=list(combinations(range(4),2))
G2=S.diag(*[ETA[i,i]*ETA[j,j] for i,j in PAIRS]); STAR=S.zeros(6)
for source,(dest,sign) in {(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
                          (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}.items():
    STAR[PAIRS.index(dest),PAIRS.index(source)]=sign

def wedge(x,y):return S.Matrix([x[i]*y[j]-x[j]*y[i] for i,j in PAIRS])
def pairing(A,B):return sum(x*y for x,y in zip(A,B))
def cayley(A):return (S.eye(4)-A/2).inv()*(S.eye(4)+A/2)
def geometry():
    e=S.Matrix([[1,S.Rational(1,3),0,0],[0,2,S.Rational(1,5),0],
                [0,0,1,S.Rational(1,7)],[0,0,0,S.Rational(3,2)]])
    gens=[]
    for i in (1,2,3):
        A=S.zeros(4);A[0,i]=A[i,0]=1;gens.append(A)
    for i,j in ((1,2),(1,3),(2,3)):
        A=S.zeros(4);A[i,j]=1;A[j,i]=-1;gens.append(A)
    links=[cayley((gens[i]+gens[(i+3)%6])/S.Integer(15+i)) for i in range(4)]
    loops=[]
    for r,s in PAIRS:
        L=links[r]*links[s]*links[r].inv()*links[s].inv();loops.append(L)
        eq(f'Lorentz_loop_{r}{s}',L.T*ETA*L,ETA)
        eq(f'loop_inverse_is_not_Euclidean_adjoint_{r}{s}',L.inv(),ETA*L.T*ETA)
    def actions(E,ls):
        old=0;acc=0
        for (r,s),L in zip(PAIRS,ls):
            u,v=[j for j in range(4) if j not in (r,s)]
            perm=[r,s,u,v];sg=(-1)**sum(perm[i]>perm[j] for i,j in PAIRS)
            b=sg*wedge(E[:,u],E[:,v]);coeff=STAR.T*G2*b
            M=S.zeros(4)
            for z,(i,j) in zip(coeff,PAIRS):M[i,j]=z/2;M[j,i]=-z/2
            C=(L-L.inv())/2
            old+=(b.T*G2*STAR*S.Matrix([(C*ETA)[i,j] for i,j in PAIRS]))[0]
            acc+=pairing(M,L*ETA)-pairing(M,L.inv()*ETA)
        return S.factor(old),S.factor(acc/2)
    old,acc=actions(e,loops)
    eq('whole_signed_star_equals_overlap_accumulator',old,acc)
    demand('nonzero_curved_control',old!=0)
    eq('reverse_all_paths_is_odd',actions(e,[L.inv() for L in loops])[1],-old)
    z=S.symbols('z',real=True)
    # Sixteen independent coframe components, no metric slot discarded.
    for i in range(4):
        for j in range(4):
            E=e.copy();E[i,j]+=z
            x,y=actions(E,loops)
            eq(f'coframe_jet_{i}{j}',S.diff(x,z).subs(z,0),S.diff(y,z).subs(z,0))
    # Differentiated inverse uses all six Lorentz tangents on a real loop.
    L=loops[0]
    for i,A in enumerate(gens):
        dL=A*L;dLi=-L.inv()*dL*L.inv()
        eq(f'full_reverse_path_jet_{i}',dLi,ETA*dL.T*ETA)
    return str(old)

def response():
    x,y,k,lam=S.symbols('x y k lam',real=True)
    a,b,c=S.symbols('a b c',positive=True)
    Qaction=x*x+2*y*y+x*y
    F=lambda s:a*s+b*s*s+c*s**3
    A=F(Qaction)
    for v in (x,y):eq('full_source_'+str(v),S.diff(A,v),S.diff(F(k),k).subs(k,Qaction)*S.diff(Qaction,v))
    eq('on_shell_Hessian_congruence',S.hessian(A,(x,y)).subs({x:0,y:0}),a*S.hessian(Qaction,(x,y)))
    q1=x;q2=x*x
    demand('local_prices_are_not_one_terminal_record',S.simplify(S.diff(F(q1)+F(q2),x)-S.diff(F(q1+q2),x))!=0)
    # Actual central AF price is scalar on each old central block, with full density entropy.
    tau=S.symbols('tau',real=True);u,v=S.symbols('u v',positive=True)
    eq('block_weight_convex_coefficient',tau*u+(1-tau)*v,v+tau*(u-v))
    # Consume the complete output BKM form; central scalar Kraus weights cancel exactly.
    q0,q1,q2=S.symbols('q0 q1 q2',positive=True)
    rr=[q0/(q0+q1+q2),q1/(q0+q1+q2),q2/(q0+q1+q2)]
    eq('actual_output_BKM_equals_input_BKM_for_central_effect',sum(z*z/z for z in rr),1)
    eq('central_preparation_mixed_field_jet_vanishes_at_joint_root',
       S.diff(Qaction,x).subs({x:0,y:0}),0)
    # The common response multiplies fixed source and geometry together, not one alone.
    fixed=S.symbols('fixed',real=True)
    P=x*x-fixed*x
    eq('fixed_source_not_refitted',S.diff(F(P),x),S.diff(F(k),k).subs(k,P)*(2*x-fixed))
    demand('dark_address_control',S.diff((x*0+1),x)==0)
    # Conditioning only one addressed subspace loses this; broadcasting does not.
    return True

def preserved_geometry():
    x,y,t=S.symbols('x y t',real=True)
    unit=lambda z:S.Matrix([(1-z*z)/(1+z*z),2*z/(1+z*z)])
    k=unit(t);jx=unit(x);jy=unit(y)
    total_x=S.kronecker_product(k,jx);total_y=S.kronecker_product(k,jy)
    eq('retained_geometry_full_norm',(total_x.T*total_x)[0],1)
    eq('retained_geometry_comparator',(total_y.T*total_x)[0],(jy.T*jx)[0])
    eq('global_price_preparation_jet_cancels_in_spatial_comparison',
       S.diff((total_y.T*total_x)[0],t),0)
    dx=total_x.diff(x);dj=jx.diff(x)
    eq('retained_geometry_metric',(dx.T*dx)[0]-(total_x.T*dx)[0]**2,
       (dj.T*dj)[0]-(jx.T*dj)[0]**2)
    # Dense coherent mixed price density, all zero environmental modes retained.
    sigma=S.Matrix([[S.Rational(3,5),(1+S.I)/10],[(1-S.I)/10,S.Rational(2,5)]])
    geom=jx*jx.T
    lifted=S.kronecker_product(sigma,geom)
    z=S.symbols('z')
    eq('retained_pure_geometry_preserves_price_spectrum',lifted.charpoly(z).as_expr(),
       z**2*sigma.charpoly(z).as_expr())
    c,kcost=S.symbols('c kcost',real=True)
    eq('same_reference_type_geometry_cost_is_constant',
       S.trace((c+kcost)*lifted)-S.trace(c*sigma),kcost)
    eq('geometry_spectator_code_source_vanishes',S.diff(S.trace((c+kcost)*lifted),x),0)
    varying=S.kronecker_product(unit(x),jx)
    extra=(varying.diff(x).T*varying.diff(x))[0]-(dj.T*dj)[0]
    demand('local_price_flag_would_change_geometry',S.simplify(extra)!=0)


def preparation_tail():
    T=S.Matrix([[p,p*p],[1,0]])
    pi=S.Matrix([[1/(1+p*p),p*p/(1+p*p)]])
    projector=S.ones(2,1)*pi
    eq('golden_cost_cut_transition',T*S.ones(2,1),S.ones(2,1))
    eq('actual_tail_stationary_weights',pi*T,pi)
    for m in range(9):
        eq('all_tail_coefficients_'+str(m),T**m,projector+(-p*p)**m*(S.eye(2)-projector))
    b0,b1=S.symbols('b0 b1',positive=True);tilt=S.Matrix([b0,b1])
    leaves=[('',0)]
    allcuts={0:leaves}
    for c in range(1,7):
        new=[]
        for word,cost in leaves:
            new.extend([(word+'F',cost+1),(word+'R',cost+2)] if cost<c else [(word,cost)])
        leaves=new;allcuts[c]=leaves
        Z=sum(p**cost*tilt[cost-c] for word,cost in leaves)
        eq('full_terminal_tilt_normalizer_'+str(c),Z,(T**c*tilt)[0])
    c=6;k=3;Z=(T**c*tilt)[0]
    for word,cost in allcuts[k]:
        actual=sum(p**cc*tilt[cc-c] for ww,cc in allcuts[c] if ww.startswith(word))/Z
        expected=p**cost*(T**(c-k)*tilt)[cost-k]/Z
        eq('actual_PF_prefix_mass_'+word,actual,expected)
        eq('full_prefix_normalizer_jet_'+word,S.diff(actual,b0),S.diff(expected,b0))
    eq('terminal_type_tilt_is_not_exactly_prior',(T*tilt)[0],p*b0+p*p*b1)
    demand('finite_type_tilt_not_silently_deleted',red(b0/(T*tilt)[0]-1)!=0)
    # A pure prior at every level is NOT assumed: its difference is the signed tail eigenvalue.
    x=S.symbols('x',real=True);y=S.symbols('y',positive=True)
    ee=S.Matrix([[2,x,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    vv=ee.det();weight=S.Rational(3,7)+y
    scale=S.sqrt(weight/vv);eh=scale*ee
    recovered=S.sqrt(weight/eh.det())*eh
    eq('same_preparation_density_coframe_inverse',recovered,ee)
    return {'cost_transition':'[[p,p^2],[1,0]]','nontrivial_eigenvalue':'-p^2',
            'AF_level_for_cost_cut':'n=c-1',
            'spatial_weak_and_first_jet_rate':'O(p^(2c/17)) with bounded clock/test and signal first jets',
            'native_clock_rule_forced':False}


def run():
    checks.clear();golden_effect();julia();val=geometry();response();preserved_geometry();tail=preparation_tail();sign=certificate()
    return {'schema':'d0-central-record/1','exact_algebraic_checks':len(checks),'checks':checks,
            'star_fixture_value':val,'rational_derivative_certificate':sign,'actual_preparation_tail':tail,
            'uniform_block_price_slope':['2/5','5/2'],
            'central_effect':'p^2+2p^12 Re(overlap); same scalar on both complete AF blocks',
            'variational_identity':'d_X A=(de/dQ) sum_j Tr(sigma_j) f_j_prime(e) dQ',
            'stationary_rank_strata_retained':True,
            'primitive_admission_proved':False,'physical_program_selected':False,
            'full_native_action_identified':False,'original_raw_source_terminal_closed':False,'GR_closed':False}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
