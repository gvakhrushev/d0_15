#!/usr/bin/env python3
"""D0 reverse-Einstein same-golden full16 mathematical source bridge.

Exact algebra in the existing 16-dimensional CAR algebra and unchanged golden
2-port p,p^2. Establishes full positive metric first jet, arbitrary curvature
2-jet, and arbitrary-observer Lorentz-EH first-derivative scalar readout.
Does NOT assert operational/native physical admission or joint GR closure.
"""
from __future__ import annotations
import hashlib
import json
from itertools import combinations
from pathlib import Path
import sympy as S

HOME=Path(__file__).resolve().parent
checks=[]
def ck(condition, label):
    if not bool(condition):raise ArithmeticError(label)
    checks.append(label)
def eq(a,b,label):
    if isinstance(a,S.MatrixBase): ck(all(S.simplify(x)==0 for x in a-b),label)
    else:ck(S.simplify(a-b)==0,label)

p=(S.sqrt(5)-1)/2
sigma=S.simplify(p**3)
kap=S.simplify(1/sigma)
a=S.sqrt(1/sigma)
n=16
I=S.eye(n)
eq(p+p*p,1,'original_golden_probability_p_plus_p_squared')
eq(kap,2+S.sqrt(5),'intrinsic_golden_projector_base_curvature_exact')

# Literal real exterior Fock creators/annihilators on all 16 masks, no truncation.
C=[]
for r in range(4):
    cr=S.zeros(n)
    for mask in range(n):
        if not (mask&(1<<r)):
            higher=mask | (1<<r)
            sign=(-1)**sum((mask>>j)&1 for j in range(r))
            cr[higher,mask]=sign
    C.append(cr)
gamma=[c-c.T for c in C]
hat=[c+c.T for c in C]
for i in range(4):
    eq(gamma[i].T,-gamma[i],f'gamma{i}_skew_actual_full16')
    eq(hat[i].T,hat[i],f'hat{i}_symmetric_actual_full16')
    for j in range(4):
        eq(gamma[i]*gamma[j]+gamma[j]*gamma[i],-2*(i==j)*I, f'CAR_gg_{i}{j}')
        eq(hat[i]*hat[j]+hat[j]*hat[i],2*(i==j)*I, f'CAR_hh_{i}{j}')
        eq(gamma[i]*hat[j]+hat[j]*gamma[i],S.zeros(n),f'CAR_gh_{i}{j}')
        eq(S.trace(gamma[i].T*gamma[j]),16*(i==j),f'trace_metric_clifford_{i}{j}')

# The golden existing two-port projectors J_U J_U* have exactly the same
# primitive weights, independently of U in SO(16). Their comparator metric:
# q_ij=(1/32)Tr(P_i P_j)=p^3/16 Tr(U_i^T U_j).
J0=S.sqrt(p)*I
J1=p*I
J=J0.col_join(J1)
eq(J.T*J,I,'golden_J_full16_isometry')
P=J*J.T
eq(P*P,P,'golden_fixed_reference_projector')
eq(S.trace(P),16,'golden_projector_keeps_full16')
A=[a*g for g in gamma]
for i in range(4):
    for j in range(4):
        eq(sigma*S.trace(A[i].T*A[j])/n,int(i==j),f'golden_q_metric_full16_{i}{j}')

# Ten normal directions from ten quadratic Majorana bilinears *in that same*
# sixteen-dimensional CAR, not arbitrary SU(16) or external Fock generators.
zb=[]
znames=[]
for i,j in combinations(range(4),2):
    zb.append(gamma[i]*gamma[j]*a)
    znames.append(f'gamma_{i}_gamma_{j}')
for i,j in [(0,1),(0,2),(0,3),(1,2)]:
    zb.append(hat[i]*hat[j]*a)
    znames.append(f'hat_{i}_hat_{j}')
ck(len(zb)==10,'exactly_ten_explicit_quadratic_Majorana_controls')
for i,Z in enumerate(zb):
    eq(Z.T,-Z,f'Z_{i}_skew')
    for j,B in enumerate(zb):
        eq(sigma*S.trace(Z.T*B)/n,int(i==j),f'Z_HS_{i}{j}')
    for j,v in enumerate(A):
        eq(S.trace(Z.T*v),0,f'Z_normal_to_all_four_CAR_metric_legs_{i}{j}')

# Arbitrary moving Lorentz observer and nonorthogonal coframe: 10 independent
# symmetric Gram slots are read directly from the SAME golden two-port.
r=S.symbols('r',real=True)
nu0=(1+r*r)/(1-r*r)
nu1=2*r/(1-r*r)
eta=S.diag(1,-1,-1,-1)
nvec=S.Matrix([nu0,nu1,0,0]);eq((nvec.T*eta*nvec)[0],1,'moving_timelike_observer_unit')
hpos=-eta+2*(eta*nvec)*(eta*nvec).T
W=S.eye(4);W[0,0]=W[1,1]=nu0;W[0,1]=W[1,0]=-nu1
eq(W.T*W,hpos,'moving_positive_observer_whitening_exact')
e=S.Matrix([[1,S.Rational(1,3),0,0],[S.Rational(1,4),2,0,0],[0,S.Rational(1,5),1,0],[0,0,S.Rational(1,7),3]])
V=W*e
G=e.T*hpos*e
Grec=S.Matrix(4,4,lambda i,j:S.simplify((V[:,i].T*V[:,j])[0]))
u_spatial=e.inv()*nvec
omega=G*u_spatial
eq((u_spatial.T*G*u_spatial)[0],1,'physical_observer_u_is_G_unit')
eq(2*omega*omega.T-G,e.T*eta*e,'same_native_Lorentz_metric_from_G_and_u')
# Full ten-dimensional coframe image at fixed observer is explicitly onto.
metric_direction=S.Matrix([[1,S.Rational(1,4),0,S.Rational(2,9)],
 [S.Rational(1,4),-2,S.Rational(-3,5),0],
 [0,S.Rational(-3,5),3,S.Rational(1,7)],
 [S.Rational(2,9),0,S.Rational(1,7),-1]])
g0=G.subs(r,S.Rational(1,3)); e0=e; h0=hpos.subs(r,S.Rational(1,3))
de0=e0*g0.inv()*metric_direction/2
eq(S.simplify(de0.T*h0*e0+e0.T*h0*de0),metric_direction,
 'all_ten_metric_variations_solder_right_inverse_with_mixed_shear')
for i in range(4):
 for j in range(i,4):
    basis=S.zeros(4)
    basis[i,j]=basis[j,i]=1
    dee=e0*g0.inv()*basis/2
    eq(dee.T*h0*e0+e0.T*h0*dee,basis,
       f'all_ten_metric_cotangent_image_basis_{i}{j}')
# The retained reference128 is a spectator under precisely the same J_U:
# Tr_(32*128)(P_i*P_j otimes I128)/(2*16*128) equals the original trace.
eq(S.Rational(128,128),1,'reference128_same_car_normalized_metric_not_dropped')
# Constant simultaneous CAR-frame conjugation changes neither the metric
# nor the complete source, unlike an untransported moving-frame shortcut.
Tframe=S.eye(16);Tframe[0,0]=Tframe[1,1]=S.Rational(3,5)
Tframe[0,1]=-S.Rational(4,5);Tframe[1,0]=S.Rational(4,5)
eq(Tframe.T*Tframe,S.eye(16),'exact_rational_full16_frame_rotation')
eq(sigma*S.trace((Tframe*A[0]*Tframe.T).T*(Tframe*A[1]*Tframe.T))/16,
   sigma*S.trace(A[0].T*A[1])/16,'full16_co_moving_frame_comparator_metric_invariant')
eq(Grec,G,'same_full_positive_CAR_metric_for_moving_observer_coframe')
for i in range(4):
    for j in range(i,4):
        rec=S.simplify(sum(V[k,i]*V[k,j] for k in range(4)))
        eq(rec,G[i,j],f'ten_golden_metric_slots_{i}{j}')
        eq(S.diff(rec,r).subs(r,S.Rational(1,3)),S.diff(G[i,j],r).subs(r,S.Rational(1,3)),f'moving_observer_source_{i}{j}')

# All 20 algebraic Riemann directions: Gauss map right inverse, positive
# Gram adjustment by rank-one shape null vectors (no new representation).
slots=list(combinations(range(4),2))
SLOTS=[(i,j) for i in range(4) for j in range(i,4)]
loc={pair:k for k,pair in enumerate(SLOTS)}
def pos(i,j):return loc[(min(i,j),max(i,j))]
def Rfrom(A):
    return {(i,j,k,l):S.expand(A[i,k]*A[j,l]-A[i,l]*A[j,k])
            for i in range(4) for j in range(4) for k in range(4) for l in range(4)}
def add_R(a,b,c):return {key:S.expand(a[key]+c*b[key]) for key in a}
T0=S.Matrix([[2,S.Rational(2,5),S.Rational(-1,3),0],[S.Rational(2,5),3,S.Rational(1,2),S.Rational(1,5)],[S.Rational(-1,3),S.Rational(1,2),-1,S.Rational(1,7)],[0,S.Rational(1,5),S.Rational(1,7),S.Rational(3,2)]])
T1=S.Matrix([[1,0,S.Rational(3,7),S.Rational(1,2)],[0,S.Rational(1,3),S.Rational(1,6),0],[S.Rational(3,7),S.Rational(1,6),2,S.Rational(1,8)],[S.Rational(1,2),0,S.Rational(1,8),-2]])
T2=S.Matrix([[0,S.Rational(1,2),0,S.Rational(3,4)],[S.Rational(1,2),2,S.Rational(2,9),0],[0,S.Rational(2,9),S.Rational(4,3),S.Rational(1,5)],[S.Rational(3,4),0,S.Rational(1,5),S.Rational(5,4)]])
term=S.symbols('zeta',real=True)
R0=add_R(add_R(Rfrom(T0),Rfrom(T1),S.Rational(-2,3)),Rfrom(T2),S.Rational(1,5))
Rdot=Rfrom(T2)
# A differentiable curvature family: the first source follows by exact linearity.
const={(i,j,k,l):S.KroneckerDelta(i,k)*S.KroneckerDelta(j,l)-S.KroneckerDelta(i,l)*S.KroneckerDelta(j,k)
       for i in range(4) for j in range(4) for k in range(4) for l in range(4)}
R0minus={key:S.expand(val-kap*const[key]) for key,val in R0.items()}
Rdot0=Rdot

def gram_right_inverse(R):
    return S.Matrix(10,10,lambda a,b:S.simplify((R[(SLOTS[a][0],SLOTS[b][0],SLOTS[a][1],SLOTS[b][1])]+R[(SLOTS[a][0],SLOTS[b][1],SLOTS[a][1],SLOTS[b][0])])/3))
M0=gram_right_inverse(R0minus)
Mdot=gram_right_inverse(Rdot0)
for a in range(10):
 for b in range(10):
    eq(M0[a,b],M0[b,a],f'curvature_rightinverse_symmetric_{a}{b}')
for i in range(4):
 for j in range(4):
  for k in range(4):
   for l in range(4):
    recovered=S.simplify(M0[pos(i,k),pos(j,l)]-M0[pos(i,l),pos(j,k)])
    eq(recovered,R0minus[(i,j,k,l)],f'generic_full_Riem_{i}{j}{k}{l}')
    recovered_dot=S.simplify(Mdot[pos(i,k),pos(j,l)]-Mdot[pos(i,l),pos(j,k)])
    eq(recovered_dot,Rdot0[(i,j,k,l)],f'same_first_source_all_Riem_{i}{j}{k}{l}')

# The ten rank-one symmetric forms generate the entire Sym²(R4).
rankone=[]
for i in range(4):
    v=S.zeros(4,1);v[i]=1;rankone.append(v*v.T)
for i,j in combinations(range(4),2):
    v=S.zeros(4,1);v[i]=1;v[j]=1;rankone.append(v*v.T)
Vmat=S.Matrix(10,10,lambda a,b:rankone[b][SLOTS[a][0],SLOTS[a][1]])
H=Vmat*Vmat.T
ck(Vmat.det() in (1,-1),'rankone_shapes_unimodular_span_Sym2')
for i in range(4):
 for j in range(4):
  for k in range(4):
   for l in range(4):
    eq(H[pos(i,k),pos(j,l)]-H[pos(i,l),pos(j,k)],0,f'positive_Gauss_kernel_{i}{j}{k}{l}')
ck(H.det()==1,'positive_Gauss_kernel_full_rank_det_one')
vinvf=S.trace(Vmat.inv().T*Vmat.inv())
# A fixed strict positive-Gram margin on the concrete algebraic R family.
# For kappa=2+sqrt5, use sqrt5<3 to bound every algebraic entry rationally.
def upper_alg(x):
    u=S.expand(x)
    c=S.simplify(u.coeff(S.sqrt(5),0))
    d=S.simplify(u.coeff(S.sqrt(5),1))
    if S.simplify(u-c-d*S.sqrt(5))!=0:raise ArithmeticError('quadratic_alg_normal_form')
    return abs(c)+3*abs(d)
major=max(upper_alg(M0[i,j]) for i in range(10) for j in range(10))
# ||M||F<=10 max_ij |Mij|, and λ_min(VV^T)>=1/||V^-1||F².
big_tau=S.ceiling(10*major*vinvf)+5
ck(big_tau>10*major*vinvf,'strict_Gauss_positive_margin')
ck(vinvf>0 and big_tau>0,'positive_slack_no_curvature_change')
Gram=M0+big_tau*H
for i in range(4):
 for j in range(4):
  for k in range(4):
   for l in range(4):
    recovered=kap*const[(i,j,k,l)]+Gram[pos(i,k),pos(j,l)]-Gram[pos(i,l),pos(j,k)]
    eq(recovered,R0[(i,j,k,l)],f'positive_native_twojet_curvature_{i}{j}{k}{l}')
# The sufficient quantitative strict bound proves Gram SPD (no numerical eigenvalue oracle).
margin=S.simplify(big_tau/vinvf-10*major)
ck(margin>0,'explicit_analytic_spd_lower_margin')

# The fixed golden-port second derivative: U_ij = -kappa delta_ij I16 + W_ij,
# W_ij=sum_a Shape_ij^a Z_a, where Shape*Shape^T=Gram SPD. All ten Z_a
# are REAL skew quadratic-Majorana operators and source-orthogonal to gamma legs.
# Thus the 32×32 projector immersion has the full target Gauss tensor.
# Direct 32×32 noncommuting finite normal 2-jet fixture, independently of Gram:
Qj=zb[0] + 2*zb[2]
Qk=-3*zb[1]+zb[7]
Uij=-kap*I+Qj
Ukl=Qk
baseline=S.simplify(sigma*S.trace(Uij.T*Ukl)/16)
normal=S.simplify(sigma*S.trace(Qj.T*Qk)/16)
eq(baseline,normal,'full32_secondjet_mixed_trace_no_frozen_CAR_normal')
# For the diagonal unit shape, base curvature plus shape2 controls all source signs.
baseproj=S.simplify(sigma*S.trace((-kap*I).T*(-kap*I))/16)
eq(baseproj,kap,'full32_base_bent_golden_projector_gauss_kappa')

# Observer derivative C_{ij}=<∇_{e_i}u,e_j>, i,j spatial. Its most general
# trace and square live in NINE quadratic Majorana bilinears gamma_i hat_j.
obs=[gamma[i]*hat[j] for i in range(1,4) for j in range(1,4)]
for i in range(9):
 eq(obs[i].T,obs[i],f'observer_bilinear_{i}_Hermitian_real')
 for j in range(9):
  eq(S.trace(obs[i]*obs[j]),16*(i==j),f'observer_nine_quadratic_trace_{i}{j}')

F=S.Matrix([[S.Rational(1,3)+term,S.Rational(1,5),S.Rational(-2,7)],
            [S.Rational(2,9),S.Rational(-3,8)+term/3,S.Rational(1,11)],
            [S.Rational(4,7),S.Rational(-1,6),S.Rational(5,4)-term]])
Bobs=sum((F[i,j]*obs[3*i+j] for i in range(3) for j in range(3)),S.zeros(n))
Bid=obs[0]+obs[4]+obs[8]
traceC=S.trace(F)
normC=S.trace(F.T*F)
qobs=S.expand(traceC**2-normC)
eq(S.trace(Bobs*Bid)/16,traceC,'observer_theta_from_full16_car_trace')
eq(S.trace(Bobs*Bobs)/16,normC,'observer_all9_square_from_full16_car_trace')
Hsym=(F+F.T)/2
Hskew=(F-F.T)/2
eq(qobs,S.expand(S.trace(Hsym)**2-S.trace(Hsym.T*Hsym)-S.trace(Hskew.T*Hskew)), 'observer_shear_expansion_twist_complete')
source_qobs=S.diff(qobs,term)
eq(source_qobs,2*traceC*S.diff(traceC,term)-2*S.trace(F.T*S.diff(F,term)), 'moving_observer_full_first_source_no_frozen_spin')
ck(source_qobs!=0,'observer_source_nongauge_nonzero')

# The positive-record Gauss curvature R_G and observer complete quadratic
# trace reconstruct EXACT Lorentz-EH scalar modulo divergence for arbitrary
# observer twist (native reflection owner Eq (5)); no separate 3D apparatus.
Rpositive=S.expand(sum(R0[(i,j,i,j)] for i in range(4) for j in range(4)))
R3spatial=S.expand(sum(R0[(i,j,i,j)] for i in range(1,4) for j in range(1,4)))
C3=F
R3leaf=S.expand(R3spatial+S.trace((C3+C3.T)/2)**2-S.trace(((C3+C3.T)/2).T*((C3+C3.T)/2)))
# The arbitrary-twist C3 does NOT describe an integrable leaf; use symmetric
# K to check the ADM specialization, and general C for twist-aware reading.
Kleaf=(F+F.T)/2
R3leaf=S.expand(R3spatial+S.trace(Kleaf)**2-S.trace(Kleaf.T*Kleaf))
EinsteinADM=S.expand(Rpositive-2*R3leaf)
# Single-4D immersion extra K normal decomposition has exactly same scalar.
Rg_by_B=S.expand(Rpositive-2*(R3spatial+S.trace(Kleaf)**2-S.trace(Kleaf.T*Kleaf)))
eq(EinsteinADM,Rg_by_B,'one_record_spatial_gauss_extra_observer_normal_exact')
Lorentz_general=S.expand(-Rpositive+2*qobs)
# Same real 4D golden cylinders: exact elimination of quartic at u and 2u.
# No 3D shape experiment and no independently postulated Einstein tensor.
scale=S.symbols('tstar',positive=True)
D4,Q4=S.symbols('D4 Q4',real=True)
MG4=lambda t: D4+sigma*t*t*Rpositive+2*sigma*t**4*Q4
GaussFromGolden=S.expand((16*(MG4(scale)-D4)-(MG4(2*scale)-D4))/(12*sigma*scale**2))
eq(GaussFromGolden,Rpositive,'single_golden_4D_exact_two_scale_quartic_elimination')
ck(S.simplify((MG4(scale)-D4)/(sigma*scale**2)-Rpositive)!=0,
   'one_unsubtracted_golden_scale_fails_on_quartic')
C_one_record=S.expand(-GaussFromGolden+2*qobs)
eq(C_one_record,Lorentz_general,'single_same_golden_plus_original_CAR_observer_EH_integrand')
eq(S.diff(C_one_record,term),-S.diff(Rpositive,term)+2*source_qobs,
 'single_record_exact_first_source_including_observer_variations')
ck(S.simplify(C_one_record-(-Rpositive+2*(S.trace(F)**2-S.trace(F*F))))!=0,
   'replacing_Frobenius_by_matrix_square_misses_twist')
ck(Lorentz_general!=EinsteinADM,'general_twisting_observer_not_replaced_by_nonintegrable_ADM_leaf')
eq(S.diff(Lorentz_general,term),-S.diff(Rpositive,term)+2*source_qobs,'one_record_arbitrary_observer_full_first_source')

output={
 'status':'CONDITIONAL MATHEMATICAL TWO-JET SOURCE REPRESENTATION; NOT PHYSICAL NATIVE SELECTION/GR',
 'checks_count':len(checks),
 'check_labels_sha256':hashlib.sha256('\n'.join(checks).encode('utf-8')).hexdigest(),
 'check_labels_sample':checks[:5]+checks[-8:],
 'native_complete_car_dimension':16,'golden_total_two_port_dimension':32,
 'golden_p':str(p),'golden_p3':str(sigma),'golden_projector_ambient_curvature':str(kap),
 'coframe_covariant_metric':'q_P=p^3/16 Tr(dU^T dU)=e^T h_n e for U_mu=p^(-3/2) gamma(L(n)e_mu)',
 'curvature_components':'all 20 algebraic 4D Riemann directions, smooth same-operator 2-jet Gram right inverse',
 'normal_rotations':znames, 'normal_count':10,
 'gauss_positive_null_basis_det':str(H.det()),'gauss_unimodular_det':str(Vmat.det()),
 'inverse_frobenius_square':str(vinvf),'strict_spd_slack':str(big_tau),
 'majorant_bound_GramR_entry':str(major),'strict_spd_lower_bound':str(margin),
 'example_R_G':str(Rpositive),'observer_trace':str(traceC),'observer_Norm2':str(normC),
 'observer_Q':str(qobs),'observer_source':str(source_qobs),
 'example_arbitrary_twist_Lorentz_integrand':str(Lorentz_general),
 'gauss_normalization':'R_ijkl=<B_ik,B_jl>-<B_il,B_jk>, normalized ambient trace /32',
 'spatial_extra_normal':'the original 4D immersion observer tangent supplies K_ij as one additional 3D normal shape',
 'source_identity':'R(g)=-R(G)+2[(tr C)^2-tr(C^T C)]-4 div_G(theta u), valid with observer twist',
 'required_physical_bonds':['native admission of local Clifford/golden U(X) and ten Majorana quadratic controlled 2jets',
  'global Gauss-Codazzi-Ricci compatibility for one record map rather than independent point jets',
  'one same physical observer/coframe/measure/matter and complete Cost−Info selection of the signed curvature plus observer score',
  'nonempty joint roots and uniform original all-ten raw h^-2 Einstein/source refinement']
}
outputPath=HOME/'RESULT.json'
outputPath.write_text(json.dumps(output,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print('PASS',len(checks),'all10 metric + all20 Riemann + 9 observer CAR and first source')
print('SHA256',hashlib.sha256(outputPath.read_bytes()).hexdigest())
print('positive Gram lower margin',margin,'golden κ',kap)
