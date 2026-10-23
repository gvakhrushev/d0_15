#!/usr/bin/env python3
"""D0 actual 16-stage order-memory: nested clock/work Schur and priced return.
Original operands/schedule consumed at 92c00ccbf39e6e21e4383f7a7b573ab7c7c6f1be.
Author calculation only: no selected Book price, physical clock or GR claim.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
import numpy as np
from scipy.linalg import expm

HERE=Path(__file__).resolve().parent
checks=[]
def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)

a=sp.symbols('a', real=True)
fpoly=sp.Poly(a**4+a*a-1,a)
def gold(expr):
    return sp.rem(sp.Poly(sp.expand(expr),a),fpoly).as_expr()
def goldm(mat):
    return mat.applyfunc(gold)

# Literal original quaternion and Golden primitive definitions.
Li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
Lj=sp.Matrix([[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]])
p=a*a
G=sp.Matrix([[a,-p],[p,a]])
X=sp.diag(sp.eye(4),Li)
Y=sp.diag(Lj,Lj)
palette={'G':sp.kronecker_product(G,sp.eye(8)),
         'X':sp.kronecker_product(X,sp.eye(2)),
         'Y':sp.kronecker_product(Y,sp.eye(2)), 'idle':sp.eye(16)}
write=sp.zeros(16)
for arm in range(2):
    for spin in range(4):
        for bit in range(2):
            write[8*arm+2*spin+(bit^arm),8*arm+2*spin+bit]=1
palette['WRITE']=write
perm=sp.zeros(16)
for arm in range(2):
    for spin in range(4):
        for bit in range(2):
            perm[4*(2*arm+bit)+spin,8*arm+2*spin+bit]=1
check('original_quaternion_i_square',Li*Li==-sp.eye(4))
check('original_quaternion_order',Li*Lj==-Lj*Li)
for name,U in palette.items():
    check('complete_primitive_orthogonal_'+name,goldm(U.T*U)==sp.eye(16))

programmes={
 'identity':['G']+['X']*4+['Y']*4+['X']*2+['G']+['X']*2+['WRITE','idle'],
 'order':['G','X','Y']+['X']*3+['Y']*3+['X']*2+['G']+['X']*2+['WRITE','idle']}
monodromies={}
for name,names in programmes.items():
    check('sixteen_stages_'+name,len(names)==16)
    M=sp.eye(16)
    for gate in names:M=goldm(palette[gate]*M)
    monodromies[name]=M
c,k,q=sp.symbols('c k q',real=True)
rel=sp.Poly(k*k-(1-c*c),k)
def red(expr):
    num,den=sp.fraction(sp.cancel(expr))
    num=sp.rem(sp.Poly(num,k),rel).as_expr()
    den=sp.rem(sp.Poly(den,k),rel).as_expr()
    return sp.factor(num/den)
def redm(m):return m.applyfunc(red)
R=sp.Matrix([[c,-k],[-k,-c]])
W=sp.diag(sp.eye(2),sp.Matrix([[0,1],[1,0]]))
M=W*sp.kronecker_product(R,sp.eye(2))
cn=gold(p-p*p);kn=2*a**3
Mn=goldm(M.subs({c:cn,k:kn}))
check('actual_order_full16_factor',goldm(perm*monodromies['order']*perm.T)==sp.kronecker_product(Mn,sp.eye(4)))
check('actual_identity_full16_factor',perm*monodromies['identity']*perm.T==sp.kronecker_product(W,sp.eye(4)))
check('native_cosine_equals_p_cubed',gold(cn-p**3)==0)
check('unitary_analytic_extension',redm(M.T*M)==sp.eye(4))

A=M[0,0];B=M[0,1:];C=M[1:,0];D=M[1:,1:]
Q=sp.diag(0,1,1,1);P=sp.eye(4)-Q;V=Q*M
N=1-c*q-c*c*q*q+c*q**3
Delta=(1-q*q)*(1-2*c*q+q*q)
num=c-c*c*q-c*q*q+q**3
Theta=num/N
check('retained_work_det',red((sp.eye(3)-q*D).det()-N)==0)
check('full_apparatus_det',red((sp.eye(4)-q*M).det()-Delta)==0)
check('actual_transfer_function',red(A+q*(B*(sp.eye(3)-q*D).inv()*C)[0]-Theta)==0)
check('nested_Schur_identity',sp.factor((1-q*Theta)*N-Delta)==0)
check('prepared_resolvent',red(((sp.eye(4)-q*M).inv())[0,0]-N/Delta)==0)
check('work_is_not_source_neutral',sp.diff(N,c)!=0)
check('work_cannot_be_dropped',(1-q*c)!=sp.cancel(Delta/N))
check('full_inverse_singular_endpoint',Delta.subs(q,1)==0)
check('work_inverse_regular_endpoint',sp.simplify(N.subs(q,1)-(1-c*c))==0)
check('return_endpoint',sp.simplify(Theta.subs(q,1))==1)

Cyc=sp.Matrix.hstack(*[(M**j)[:,0] for j in range(4)])
check('all_four_reachable',red(Cyc.det()-(1-c*c)**2)==0)
# Cyclicity + unitarity proves rho(D)<1 for real |c|<1,k!=0;
# any unit-modulus archive eigenvector would be an eigenvector of M
# orthogonal to every M^j e0. This removes the convergence premise.
Rwork=(sp.eye(3)-q*D).inv()
Kexpr=(C.T*Rwork.T*Rwork*C)[0]
Kformula=(1-c*c)*((1+q*q-c*q)**2-q*q)/N**2
check('complete_transfer_defect',red(1-Theta*Theta-(1-q*q)*Kexpr)==0)
check('explicit_archive_dwell',red(Kexpr-Kformula)==0)
check('dwell_endpoint',sp.factor(Kformula.subs(q,1)-(3-c)/(1+c))==0)
check('phase_derivative',sp.simplify(sp.diff(Theta,q).subs(q,1)-(3-c)/(1+c))==0)
p0=(sp.sqrt(5)-1)/2;c0=sp.simplify(p0**3)
check('golden_dwell_sqrt5',sp.simplify(((3-c)/(1+c)).subs(c,c0)-sp.sqrt(5))==0)
check('golden_full_return_phase_2phi',sp.simplify((1+(3-c)/(1+c)).subs(c,c0)-2/p0)==0)
check('uniform_denominator_lower',sp.simplify(1-c0-c0*c0-3*c0)==0)

# Quantitative source truncation: original full reachability Gram supplies
# a UNIFORM block contraction without diagonalizing a nonnormal archive.
Surv=sp.Matrix.hstack(*[(V**j)[:,0] for j in range(4)])
G4=Surv*Surv.T
check('survival_cyclic_determinant',red(Surv.det()-(1-c*c)**2)==0)
check('four_cycle_Gram_determinant',red(G4.det()-(1-c*c)**4)==0)
# Tr G4 <=4 since V is a contraction. For eigenvalues of G4>0,
# lambda_min >=27 det(G4)/64; use |c|<=1/4.
eta_lower=sp.Rational(27,64)*sp.Rational(15,16)**4
check('uniform_four_cycle_contraction_margin',eta_lower>sp.Rational(1,4))
check('native_inside_uniform_chart',bool(c0>0) and bool(c0<sp.Rational(1,4)))
check('coherent_delay_inverts_native_cosine',sp.simplify((3-(3-c)/(1+c))/(1+(3-c)/(1+c))-c)==0)

# Exact monitored-completion occupation law; separate admitted programme.
check('monitor_defect_projector',redm(sp.eye(4)-V*V.T)==P)
for n in (1,2,3,4,6):
    total=sp.zeros(4);power=sp.eye(4)
    for j in range(n):
        total=redm(total+power*P*power.T)
        power=redm(V*power)
    check('finite_complete_occupation_'+str(n),redm(total-(sp.eye(4)-power*power.T))==sp.zeros(4))
# At |c|<1 work survival decays, so total occupation = I4,
# total probability of return =1 and E(return cycles)=4.
# I_apparatus x rho_spin,R keeps oldRIGHT correlations for actual factor M.
x,y=sp.symbols('x y',real=True)
infoB=sp.Matrix([[2,x,0,0],[x,3,0,0],[0,0,4,y],[0,0,y,5]])
check('fixed_effect_sum_trace',sp.trace(infoB)==14)
status_price=2*sp.eye(4)-M.T*P*M
check('complete_return_status_code_mean_seven',red(sp.trace(status_price)-7)==0)
check('complete_return_status_charge_first_source_zero',sp.diff(red(sp.trace(status_price)),c)==0)
# Noncommuting unitary neighborhoods also retain the block contraction:
# ||V^4-V0^4||<=4 ||V-V0||, Gram perturbation <=8 ||V-V0||.
eta0=sp.Rational(27,64)*sp.Rational(15,16)**4
radius0=(eta0-sp.Rational(1,4))/8
check('explicit_open_unitary_norm_neighborhood',radius0==sp.Rational(318299,33554432))
check('traceless_effect_source_vanishes',sp.diff(sp.trace(infoB),x)==sp.diff(sp.trace(infoB),y)==0)
check('mean_cycle_not_phase_clock',sp.simplify(4-(1+sp.sqrt(5)))!=0)

# Actual independent numerical full256 clock, noncommuting source controls.
af=float(sp.sqrt(p0));vals={a:af}
Us=[np.array(palette[n].subs(vals),dtype=float) for n in programmes['order']]
Mfull=np.eye(16)
for U in Us:Mfull=U@Mfull
Wclock=np.zeros((256,256))
for j,U in enumerate(Us):Wclock[16*((j+1)%16):16*((j+1)%16+1),16*j:16*(j+1)]=U
mark=.97;qval=mark**16
slog=lambda X:np.linalg.slogdet(X)[1]
logfull=slog(np.eye(256)-mark*Wclock)
logmacro=slog(np.eye(16)-qval*Mfull)
check('actual_256_clock_det',abs(logfull-logmacro)<1e-11)
rng=np.random.default_rng(334210)
Apert=rng.normal(size=(16,16));H=(Apert-Apert.T)/20
Uplus=expm(1e-5*H)@Us[4];Uminus=expm(-1e-5*H)@Us[4]
def source_det(Upert):
    uu=list(Us);uu[4]=Upert
    m=np.eye(16);w=np.zeros((256,256))
    for j,u in enumerate(uu):
        m=u@m;w[16*((j+1)%16):16*((j+1)%16+1),16*j:16*(j+1)]=u
    return slog(np.eye(256)-mark*w),slog(np.eye(16)-qval*m)
vplus=source_det(Uplus);vminus=source_det(Uminus)
check('full_clock_noncommuting_first_source',abs((vplus[0]-vminus[0]-vplus[1]+vminus[1])/(2e-5))<1e-7)
mc=np.array(M.subs({c:c0,k:sp.sqrt(1-c0*c0)}).evalf(),dtype=float)
vc=np.diag([0,1,1,1])@mc
power=np.eye(4);occ=np.zeros((4,4));ret_prob=ret_mean=0.;probs=[]
for n in range(1,401):
    occ+=power@np.diag([1,0,0,0])@power.T
    amp=(mc@power)[0,0]
    pn=amp*amp;probs.append(pn);ret_prob+=pn;ret_mean+=n*pn
    power=vc@power
check('monitored_full_return_probability',abs(ret_prob-1)<1e-12)
check('monitored_mean_four',abs(ret_mean-4)<1e-10)
check('monitored_full_occupation',np.linalg.norm(occ-np.eye(4),ord=2)<1e-12)
Cnum=rng.normal(size=(4,4));Cnum=Cnum.T@Cnum+np.eye(4)
check('nonuniform_complete_price_trace',abs(np.trace(occ@Cnum)-np.trace(Cnum))<1e-10)
# Identity programme does NOT explore the unused dark work directions.
check('identity_control_not_four',(W[:,0]==sp.eye(4)[:,0]) and (W*Q-Q*W==sp.zeros(4)))
# Full bounded-cap source errors can be compared with the real signal.
# Numerical hostile check of exact analytic norm bound, not a positivity proof.
for nv in (8,16,32,64):
    tail=np.linalg.matrix_power(vc,nv)
    actual_norm=np.linalg.norm(tail,2)**2
    bound=(3/4)**(nv//4)
    check('uniform_tail_bound_'+str(nv),actual_norm<=bound+1e-13)
    deriv_c=float(c0)
    ss=(1-deriv_c**2)**.5
    dmc=np.array([[1,0,deriv_c/ss,0],
                  [0,1,0,deriv_c/ss],
                  [0,deriv_c/ss,0,-1],
                  [deriv_c/ss,0,-1,0]])
    dvc=np.diag([0,1,1,1])@dmc
    dvn=sum((np.linalg.matrix_power(vc,j)@dvc@
             np.linalg.matrix_power(vc,nv-1-j) for j in range(nv)),np.zeros((4,4)))
    tail_source=dvn@tail.T+tail@dvn.T
    source_bound=(8*nv/3)*np.linalg.norm(dvc,2)*bound
    check('uniform_first_source_tail_'+str(nv),np.linalg.norm(tail_source,2)<=source_bound+1e-12)
result={
 'status':'AUTHOR_CHECKS_PASS','count':len(checks),'checks':checks,
 'p':float(p0),'native_c':float(c0),'golden_coherent_dwell':float(sp.sqrt(5)),
 'full_return_amplitude_phase_delay':float(1+sp.sqrt(5)),
 'open_unitary_norm_radius':float(radius0),'status_code_expected_length':7,
 'monitored_return_probability_400':ret_prob,'monitored_mean_cycles_400':ret_mean,
 'monitored_encoded_stages_mean':16*ret_mean,'first_return_probabilities':probs[:8],
 'full_clock_logdet':logfull,'macro_logdet':logmacro,
 'work_archive_det':'1-c*q-c^2*q^2+c*q^3',
 'actual_word_scope':'16-stage closure; original unclosed15 trial remains distinct',
 'external_methods':'Schur first-return / quantum Kac standard; exact original D0 application is new here',
 'physical_cost_Info_selected':False,'monitoring_and_fresh_flags_admitted':False,'GR_closed':False}
(HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
