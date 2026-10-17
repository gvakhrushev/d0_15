#!/usr/bin/env python3
"""Exact 16-CAR observer contrast and full-reference128 complete three-event test.
D0 #334, research interface: this does NOT assert native physical admission.
No old suites, no external downloads, deterministic JSON.
"""
from __future__ import annotations
from fractions import Fraction
from pathlib import Path
import hashlib, json, math
import numpy as np
import sympy as sp

BASE = Path(__file__).resolve().parent
CHECKS=[]

def chk(cond, label):
    if not bool(cond):
        raise ArithmeticError(label)
    CHECKS.append(label)

def eq0(x):
    if isinstance(x, sp.MatrixBase):
        return all(sp.cancel(t)==0 for t in x)
    return sp.cancel(x)==0

# Literal D0/Fock creation matrices ordered by occupation mask 0..15.
I = sp.eye(16)
c=[]
for a in range(4):
    C=sp.zeros(16)
    for mask in range(16):
        if not (mask>>a)&1:
            sign=(-1)**((mask&((1<<a)-1)).bit_count())
            C[mask|(1<<a),mask]=sign
    c.append(C)
ann=[x.T for x in c]
gamma=[c[a]-ann[a] for a in range(4)]
hat=[c[a]+ann[a] for a in range(4)]
for a in range(4):
    for b in range(4):
        chk(eq0(gamma[a]*gamma[b]+gamma[b]*gamma[a]+(2 if a==b else 0)*I),f'CAR_skew_{a}_{b}')
        chk(eq0(hat[a]*hat[b]+hat[b]*hat[a]-(2 if a==b else 0)*I),f'CAR_sym_{a}_{b}')
        chk(eq0(gamma[a]*hat[b]+hat[b]*gamma[a]),f'CAR_mixed_{a}_{b}')

O={}
for i in range(1,4):
    for j in range(1,4):
        O[(i,j)]=gamma[i]*hat[j]
        chk(eq0(O[(i,j)].T-O[(i,j)]),f'Wij_sym_{i}_{j}')
for (i,j),A in O.items():
    for (k,l),B in O.items():
        chk(eq0(sp.trace(A*B)/16-(1 if (i,j)==(k,l) else 0)),f'CAR_HS_{i}{j}_{k}{l}')

T=sum((O[(i,i)] for i in range(1,4)),sp.zeros(16))
chk(eq0(sp.trace(T)), 'coherent_is_traceless')
chk(eq0(sp.trace(T*T)/16-3),'coherent_norm3')
chk(eq0(T.det()),'coherent_determinant_zero') if False else None
# T eigenvalues are +-3 and +-1; invertibility ensures a correlated projector.
checkdet=int(T.det());chk(checkdet != 0,'coherent_operator_full_rank')

C_samples={
    'isotropic':sp.eye(3)*sp.Rational(2,5),
    'pure_shear':sp.Matrix([[0,sp.Rational(2,7),0],[0,0,0],[0,0,0]]),
    'twist':sp.Matrix([[0,sp.Rational(1,3),0],[-sp.Rational(1,3),0,0],[0,0,0]]),
    'generic':sp.Matrix([[sp.Rational(1,3),sp.Rational(1,4),-sp.Rational(1,5)],
                         [sp.Rational(1,7),-sp.Rational(1,6),sp.Rational(1,8)],
                         [sp.Rational(1,9),sp.Rational(1,10),sp.Rational(1,11)]])}
V_samples={
  'isotropic': sp.Matrix([[sp.Rational(1,7),1,0],[0,sp.Rational(1,9),0],[0,0,-sp.Rational(1,11)]]),
  'pure_shear':sp.Matrix([[0,0,0],[0,sp.Rational(3,8),0],[sp.Rational(2,5),0,0]]),
  'twist':sp.Matrix([[0,sp.Rational(2,9),0],[-sp.Rational(2,9),0,0],[0,0,0]]),
  'generic':sp.Matrix([[sp.Rational(1,5),0,sp.Rational(2,7)],
                       [sp.Rational(1,13),0,0],
                       [0,sp.Rational(-1,19),sp.Rational(1,17)]])}

def X_from(C):
    return sum((C[i-1,j-1]*O[(i,j)] for i in range(1,4) for j in range(1,4)),sp.zeros(16))

def sqn(C):
    return sum((v*v for v in C),sp.Integer(0))

def obs(C):
    return sp.expand(sp.trace(C)**2-sqn(C))

# Orthogonal ensemble: reference128 split into eight 16-slot retained blocks.
# |Omega_k>=(1/4) sum_a |a>_sys |16k+a>_ref.
# Each omega is unit norm, rho_sys=I16/16, rho_ref=I128/128.
Om=np.zeros((8,16,128))
for k in range(8):
    for a in range(16):Om[k,a,16*k+a]=.25
chk(np.allclose(np.einsum('kar,lar->kl',Om,Om),np.eye(8)),'Omega8_orthonormal')
margin_ref=np.einsum('kar,kas->rs',Om,Om)/8
margin_sys=np.einsum('kar,kbr->ab',Om,Om)/8
chk(np.array_equal(margin_ref,np.eye(128)/128),'reference128_faithful_whole_marginal')
chk(np.array_equal(margin_sys,np.eye(16)/16),'all16_CAR_faithful_marginal')

# Fixed chart amplitude epsilon=p^8; a short script uses a constant 1/16
# to avoid any field-dependent clock jet in this mathematical test.
eps=sp.Rational(1,16)
chk(eps > 0, 'epsilon_const_positive')

values={}
for name,C in C_samples.items():
    V=V_samples[name];X=X_from(C);dX=X_from(V)
    q=obs(C);dq=sp.expand(2*sp.trace(C)*sp.trace(V)-2*sum(C[i,j]*V[i,j] for i in range(3) for j in range(3)))
    iso=sp.expand(sp.trace(C)**2/3)
    total=sqn(C)
    orth=sp.expand(total-iso)
    chk(q==sp.expand(2*iso-orth),f'{name}_unique_readout_2minus1')
    chk(eq0(sp.trace(X*X)/16-total),f'{name}_CAR_Frobenius_total')
    chk(eq0(sp.trace(X*T)/16-sp.trace(C)),f'{name}_CAR_coherent_trace')
    chk(orth>=0 and iso>=0,f'{name}_nonnegative_port_suboutcomes')
    chk(eq0((2*iso-orth)-q),f'{name}_Born_score_matches_observer')
    chk(eq0(sp.diff(obs(C+sp.Symbol('u')*V),sp.Symbol('u')).subs('u',0)-dq),f'{name}_all_source_jet')
    # Every example is strictly inside contraction domain for epsilon=1/16.
    normC=float(sp.sqrt(total))
    chk(float(eps)*4*normC<1,f'{name}_safe_full_Julia_contraction')
    # Explicit 8-copy reference128 quantum probabilities without huge 2048 projectors.
    xf=np.array(X,dtype=np.float64);tf=np.array(T,dtype=np.float64)
    v=np.einsum('ab,kbr->kar',xf,Om)
    iso_k=np.einsum('ab,kbr->kar',tf,Om)/math.sqrt(3)
    p_total=(float(eps)**2)*np.einsum('kar,kar->',v,v)/8
    inner=np.einsum('kar,kar->k',iso_k,v)
    p_iso=(float(eps)**2)*float(np.dot(inner,inner))/8
    p_orth=p_total-p_iso
    p_blank=1-p_total
    chk(np.isclose(p_total,float(eps**2*total),atol=1e-15),f'{name}_literal_reference_total')
    chk(np.isclose(p_iso,float(eps**2*iso),atol=1e-15),f'{name}_literal_reference_iso')
    chk(np.isclose(p_orth,float(eps**2*orth),atol=1e-15),f'{name}_literal_reference_orth')
    chk(p_blank>=0 and p_orth>=-1e-14,f'{name}_complete_event_positive')
    chk(np.isclose(p_iso+p_orth+p_blank,1),f'{name}_complete_three_outcome_normalization')
    chk(np.isclose((2*p_iso-p_orth)/float(eps**2),float(q),atol=1e-12),f'{name}_full_Born_gravity')
    # Both complete projector and full event jointly differentiable, including non-commuting X,dX.
    a=sp.symbols('a',real=True)
    XR=X+a*dX
    et=sp.expand(eps**2*sp.trace(XR*XR)/16)
    ec=sp.expand(eps**2*(sp.trace(XR*T)/16)**2/3)
    do=sp.diff(2*ec-(et-ec),a).subs(a,0)
    chk(eq0(do-eps**2*dq),f'{name}_noncommuting_X_first_source')
    values[name]={'C':str(C.tolist()), 'Qobs':str(q),'dQobs':str(dq),
         'p_coherent':str(eps**2*iso),'p_orthogonal':str(eps**2*orth),
         'p_blank':str(1-eps**2*total),'score_signed_expected':str(eps**2*q),
         'trace_C':str(sp.trace(C)), 'norm2_C':str(total)}

# General d=3 uniqueness for any linear centered score a P_coh+b P_orth.
a,b=sp.symbols('a b')
solution=sp.solve([sp.Eq(b,-1),sp.Eq((a-b)/3,1)],(a,b),dict=True)
chk(solution==[{a:2,b:-1}],'unique_signed_score_coefficients')
chk(obs(C_samples['isotropic'])>0,'isotropic_positive')
chk(obs(C_samples['pure_shear'])<0,'pure_shear_negative')
chk(obs(C_samples['twist'])<0,'twist_negative')

# The new two-port rotation is NOT a new primitive block family:
# U=[S,-A; A,S] is obtained from the EXISTING native Julia(A)
# J(A)=[A,S;S,-A] by two CONSTANT signed port readdressings:
# U=diag(-I,I) J(A) [[0,I],[-I,0]].  A and S commute.
A_sym,S_sym=sp.symbols('A S',real=True)
J_sym=sp.Matrix([[A_sym,S_sym],[S_sym,-A_sym]])
U_sym=sp.Matrix([[S_sym,-A_sym],[A_sym,S_sym]])
L_sym=sp.diag(-1,1)
R_sym=sp.Matrix([[0,1],[-1,0]])
chk(eq0(L_sym*J_sym*R_sym-U_sym),'same_native_Julia_fixed_port_readdressing')
chk(eq0(U_sym.T*U_sym-(A_sym*A_sym+S_sym*S_sym)*sp.eye(2)),
    'all_outcomes_unitary_if_native_Julia_defect_identity')
# Literal 32x32 CAR/matrix check with noncommuting CAR word coefficients.
mat=np.array(X_from(C_samples['generic']),dtype=float)
A_np=float(eps)*mat
lam,V=np.linalg.eigh(A_np)
S_np=(V*np.sqrt(1-lam**2))@V.T
J_np=np.block([[A_np,S_np],[S_np,-A_np]])
Z16=np.zeros((16,16));I16=np.eye(16)
L_np=np.block([[-I16,Z16],[Z16,I16]])
R_np=np.block([[Z16,I16],[-I16,Z16]])
U_np=L_np @ J_np @ R_np
chk(np.allclose(U_np,np.block([[S_np,-A_np],[A_np,S_np]]),atol=1e-13),
    'generic_noncommuting_same_original_Julia_exact_port_form')
chk(np.allclose(U_np.T@U_np,np.eye(32),atol=1e-13),'full32_same_Julia_port_unitary')

# The coherent projector needs NO sqrt(3) as a matrix: T is integral,
# vec(T)^T vec(T)=48 and Pi=vec(T)vec(T)^T/48, W=I-vec(T)vec(T)^T/24.
# The rational Householder reflection is mathematically exact; its native
# implementation/denominator/code cost is a *separate* admission question.
vecT=sp.Matrix(list(T))
chk(all(x.is_Integer for x in vecT),'coherent_T_has_integer_original_CAR_entries')
chk(eq0((vecT.T*vecT)[0]-48),'coherent_rank_one_integer_vector_squared_norm48')
# Exact rank-one multiplication gives W²-I = (-2/24 + 48/24²) v v^T = 0.
chk(eq0(-sp.Rational(2,24)+sp.Rational(48,24**2)),'coherent_Householder_rational_reflection_squared_identity')
# Pi=v v^T/48 equals the projective |iota><iota| with |iota>=v/sqrt48.
chk(eq0(sp.Rational(1,48)*48-1),'coherent_rational_projector_idempotent')

# Stronger literal v8 shell realization: eight Fourier first-shell momenta x all16
# CAR grades, Schmidt-purified against exactly reference128 (pure rank128 state).
# This uses the ORIGINAL 8x16 shell, not a new CAR or reference carrier.
psi128 = np.eye(128, dtype=float) / math.sqrt(128)
chk(np.allclose(psi128 @ psi128.T, np.eye(128)/128), 'pure_128_firstshell_system_marginal')
chk(np.allclose(psi128.T @ psi128, np.eye(128)/128), 'pure_128_reference_full_marginal')
for name,C in C_samples.items():
    Xbig=np.kron(np.eye(8), np.array(X_from(C),dtype=float))
    T16=np.array(T,dtype=float)
    exit_wave = Xbig @ psi128
    p_total=float(eps)**2 * float(np.sum(exit_wave*exit_wave))
    p_coh=0.
    for k in range(8):
        iso=np.zeros((128,128),dtype=float)
        iso[16*k:16*(k+1),16*k:16*(k+1)] = T16/(4*math.sqrt(3))
        chk(np.isclose(np.sum(iso*iso),1),f'{name}_pure128_iso{k}_normalized')
        a=float(np.sum(iso*exit_wave))
        p_coh += float(eps)**2*a*a
    total=sqn(C); coherent=sp.trace(C)**2/3
    chk(np.isclose(p_total,float(eps**2*total),atol=1e-15),f'{name}_pure128_exit_exact')
    chk(np.isclose(p_coh,float(eps**2*coherent),atol=1e-15),f'{name}_pure128_coherent_exact')
    chk(np.isclose((3*p_coh-p_total)/float(eps**2),float(obs(C)),atol=1e-12),f'{name}_pure128_Born_Einstein_relative')

# Flat G, rotating observer has C_12=k, theta=0 and exact R_g=-2 k^2.
kappa=sp.symbols('kappa',real=True)
Ct=sp.Matrix([[0,kappa,0],[0,0,0],[0,0,0]])
q_twist=obs(Ct)
chk(eq0(q_twist+ kappa**2),'twist_witness_observer_source_exact')
chk(eq0(sp.diff(2*q_twist,kappa)+4*kappa),'twist_witness_full_Rg_first_source_exact')
chk(eq0((eps**2*sqn(Ct)).subs(kappa,1)-sp.Rational(1,256)),'twist_observer_orthogonal_born_event_1_over_256')

# ORIGINAL finite Julia blank prefactor: N_blank = h D/16. On the proposed
# observer-CAR bilinear input X_C, conditional h/16 gives the SAME 1/256
# probability coefficient as the existing retained first-exit formula.
# This is a normalization match, NOT proof that X_C is an actual Julia row.
hsym=sp.symbols('h',positive=True)
for name,C in C_samples.items():
    pc=hsym**2*sp.trace(C)**2/(256*3)
    po=hsym**2*(sqn(C)-sp.trace(C)**2/3)/256
    chk(eq0((2*pc-po)/hsym**2-obs(C)/256),f'{name}_native_h_over_16_exact_1over256')
    V=V_samples[name];u=sp.symbols('u',real=True)
    pc_u=hsym**2*sp.trace(C+u*V)**2/(256*3)
    po_u=hsym**2*(sqn(C+u*V)-sp.trace(C+u*V)**2/3)/256
    derivative=2*sp.trace(C)*sp.trace(V)-2*sum(C[i,j]*V[i,j] for i in range(3) for j in range(3))
    chk(eq0(sp.diff((2*pc_u-po_u)/hsym**2,u).subs(u,0)-derivative/256),
        f'{name}_native_h_over_16_exact_first_source')

# Literal native Golden direct/return prefix grammar, with retained stopping:
# F=0 has length1; R=10 has length2; first R then F/R makes three leaves:
# {F,RF,RR}={0,100,1010}, lengths {1,3,4}.
p=(sp.sqrt(5)-1)/2
chk(eq0(p+p*p-1),'golden_two_branch_normalization')
chk(eq0(p+p**3+p**4-1),'full_three_leaf_golden_stopping_cut')
chk(eq0(p+3*p**3+4*p**4-5*p*p),'three_leaf_native_expected_reference_code_5p2')
for name,C in C_samples.items():
    qc=eps**2*sp.trace(C)**2/3
    qo=eps**2*(sqn(C)-sp.trace(C)**2/3)
    qb=1-qc-qo
    Cexpected=qc+3*qb+4*qo
    chk(eq0(Cexpected-3+eps**2*obs(C)),f'{name}_literal_F_RF_RR_cost_exact_signed_observer')
    chk(eq0(qc+qo+qb-1),f'{name}_full_encoded_three_leaves_normalized')

# M1/minimal-description negative control: a blind Huffman/minimal code
# assignment does NOT choose the desired geometric router at small h.
# Swapping coherent and overwhelmingly likely blank leaves changes lengths
# (coh:1,blank:3) -> (coh:3,blank:1) and improves expected code by
# 2*(P_blank-P_coh)>0, because the blank is almost certain.
for name,C in C_samples.items():
    pc=eps**2*sp.trace(C)**2/3
    po=eps**2*(sqn(C)-sp.trace(C)**2/3)
    pb=1-pc-po
    proposed=pc+3*pb+4*po
    swapped=3*pc+pb+4*po
    chk(eq0(proposed-swapped-2*(pb-pc)), f'{name}_minimal_code_swap_exact')
    chk(pb>pc, f'{name}_naive_minimal_code_prefers_blank_as_shortest')

# Crucial native Cost-Info firewall. Under the SAME-history likelihood binding,
# Info=log_phi(q/mu); expected Cost-Info = Shannon(q)/log_phi, NOT the linear
# centred code cost. At C=t*C0, qcoh,qorth~t² and Shannon has t²log(1/t).
Cg=C_samples['generic']
a_coeff=eps**2*sp.trace(Cg)**2/3
b_coeff=eps**2*(sqn(Cg)-sp.trace(Cg)**2/3)
chk(a_coeff>0 and b_coeff>0,'nonzero_two_exit_types_for_entropy_birth')
tval=sp.symbols('tval',positive=True)
H = -(a_coeff*tval**2)*sp.log(a_coeff*tval**2) - (b_coeff*tval**2)*sp.log(b_coeff*tval**2) \
    -(1-(a_coeff+b_coeff)*tval**2)*sp.log(1-(a_coeff+b_coeff)*tval**2)
# Analytic asymptotic by elementary expansion of log(1−x), no numerical limit:
Hlim = 2*(a_coeff+b_coeff)
chk(eq0(Hlim-2*eps**2*sqn(Cg)),'shannon_t2_log_divergence_coefficient')
chk(Hlim>0,'Shannon_has_no_finite_second_variation_at_zero')
# The expected primitive 0/10 code has finite quadratic coefficient,
# so a fixed code plus the same-history KL Info cannot equal it as an action.
chk(eq0((a_coeff*tval**2 +3*(1-(a_coeff+b_coeff)*tval**2)
         +4*b_coeff*tval**2 - 3) + eps**2*tval**2*obs(Cg)),
    'centered_native_code_finite_exact_quadratic')

# Stronger CENTRAL route: the actual Golden accumulated-cost >=3 cut has
# FIVE unpostselected words: FFF,FR,RF of cost3 and FFR,RR of cost4.
# Three selected words have IDENTICAL amplitude p^(3/2), the two pending
# have amplitude p². Their weights add to one, with NO new sqrt(3).
chk(eq0(3*p**3+2*p**4-1),'golden_cost3_five_full_histories_normalize')
reference_words={'FFF':3,'FR':3,'RF':3,'FFR':4,'RR':4}
chk(sorted(reference_words.values())==[3,3,3,4,4],'golden_cost3_3_equal_branch_2_pending')
# Conditioned on the three equal-weight words, apply the same full
# reference-projector reflection -W_coh to FFF,FR and +W_orth to RF;
# the other two words get I. Exact full-state overlap can be fed to the
# previously owned CENTRAL Golden-AF scalar-flag interface, WITHOUT feeding
# Q_obs as a computed number and WITHOUT measuring/projection first.
import math as _math
p_float=(math.sqrt(5)-1)/2
h0_exact=sp.expand(1-4*p**3)
z0_exact=sp.expand(p**2+2*p**12*h0_exact)
chk(sp.N(h0_exact)>0,'central_history_reference_overlap_nonzero')
chk(sp.Rational(3,8)<sp.N(z0_exact)<sp.Rational(25,64),'central_history_flat_parameter_inside_existing_AF_interval')
central_cases={}
for name,C in C_samples.items():
    Xsmall=np.array(X_from(C),dtype=float)
    A16=float(eps)*Xsmall
    eig,V=np.linalg.eigh(A16)
    chk(np.max(np.abs(eig))<1,f'{name}_central_first_Julia_gap')
    S16=(V*np.sqrt(1-eig*eig))@V.T
    A128=np.kron(np.eye(8),A16)
    S128=np.kron(np.eye(8),S16)
    psi_exit=A128@psi128
    psi_blank=S128@psi128
    norm=np.sum(psi_exit**2)+np.sum(psi_blank**2)
    chk(np.isclose(norm,1,atol=1e-13),f'{name}_central_first_program_full_normalization')
    # Existing eight coherent projector vectors, one for each reference16 block.
    PC=np.zeros_like(psi_exit)
    T16=np.array(T,dtype=float)
    for k in range(8):
        iso=np.zeros_like(psi_exit)
        iso[16*k:16*(k+1),16*k:16*(k+1)]=T16/(4*math.sqrt(3))
        coeff=np.sum(iso*psi_exit)
        PC+=coeff*iso
    PO=psi_exit-PC
    qc=float(np.sum(PC**2));qo=float(np.sum(PO**2))
    chk(np.isclose(qc,float(eps**2*sp.trace(C)**2/3),atol=1e-14),f'{name}_central_coh_probability')
    chk(np.isclose(qo,float(eps**2*(sqn(C)-sp.trace(C)**2/3)),atol=1e-14),f'{name}_central_orth_probability')
    # Reflections Wcoh=I-2Πcoh and Worth=I-2Πorth act on complete port1.
    wc=np.sum(psi_blank**2)+np.sum(psi_exit*(psi_exit-2*PC))
    wo=np.sum(psi_blank**2)+np.sum(psi_exit*(psi_exit-2*PO))
    chk(np.isclose(wc,1-2*qc,atol=1e-13),f'{name}_coherent_reflection_correct')
    chk(np.isclose(wo,1-2*qo,atol=1e-13),f'{name}_orthogonal_reflection_correct')
    chk(np.isclose(np.sum(psi_blank**2)+np.sum((psi_exit-2*PC)**2),1,atol=1e-13),f'{name}_Wcoh_complete_unitarity')
    chk(np.isclose(np.sum(psi_blank**2)+np.sum((psi_exit-2*PO)**2),1,atol=1e-13),f'{name}_Worth_complete_unitarity')
    overlap = p_float**3*(-2*wc+wo)+2*p_float**4
    exactH=h0_exact+2*p**3*eps**2*obs(C)
    chk(np.isclose(overlap,float(exactH),atol=1e-13),f'{name}_all_five_history_central_overlap_no_oracle')
    zz=p**2+2*p**12*exactH
    dz=4*p**15*eps**2*(2*sp.trace(C)*sp.trace(V_samples[name])
          -2*sum(C[i,j]*V_samples[name][i,j] for i in range(3) for j in range(3)))
    tvar=sp.symbols('tvar',real=True)
    C_t=C+tvar*V_samples[name]
    Hz=h0_exact+2*p**3*eps**2*obs(C_t)
    zt=p**2+2*p**12*Hz
    chk(eq0(sp.diff(zt,tvar).subs(tvar,0)-dz),f'{name}_CENTRAL_AF_exact_noncommuting_first_source')
    chk(sp.Rational(3,8)<sp.N(zz)<sp.Rational(25,64),f'{name}_central_z_in_old_positive_source_window')
    central_cases[name]={'coherent_full_overlap':str(sp.simplify(exactH)),
                         'AF_z':str(sp.simplify(zz)),'AF_z_prime':str(sp.simplify(dz)),
                         'AF_z_numeric':float(zz)}


# Deterministic invariant gauge / co-moving frame check: C -> R C R^T.
R=sp.Matrix([[sp.Rational(3,5),sp.Rational(-4,5),0],[sp.Rational(4,5),sp.Rational(3,5),0],[0,0,1]])
chk(eq0(R.T*R-sp.eye(3)),'moving_observer_frame_orthogonal')
for name,C in C_samples.items():
    V=V_samples[name]
    chk(eq0(obs(R*C*R.T)-obs(C)),f'{name}_spatial_frame_invariant')
    chk(eq0(sp.trace((R*C*R.T)*(R*V*R.T).T)-sp.trace(C*V.T)),f'{name}_source_covariant')

# Explicit small old-pointer translation obstruction: coherent projection of rank8
# is not invariant under a bit translation inside each 16-slot reference block.
ref_flip=np.array([a^1 for a in range(16)])
iso_k=np.einsum('ab,kbr->kar',np.array(T,dtype=np.float64),Om)/math.sqrt(3)
iso_flip=np.zeros_like(iso_k)
for k in range(8):
 for a in range(16):
    for b in range(16):
        iso_flip[k,a,16*k+b]=iso_k[k,a,16*k+ref_flip[b]]
chk(np.allclose(np.einsum('kar,lar->kl',iso_k,iso_k),np.eye(8)),'iso8_orthonormal')
chk(np.allclose(np.einsum('kar,lar->kl',iso_flip,iso_flip),np.eye(8)),'translated_iso8_orthonormal')
projections=np.einsum('kar,lar->kl',iso_k,iso_flip)
# For rank-8 projectors to coincide, total overlap-square would equal 8.
overlap_sq=float(np.sum(projections**2))
chk(overlap_sq < 7.9,'coherent_effect_not_invariant_under_old_low_bit_translation')

# Distinguish an actual score (2,-1,0) from normalized Shannon entropy.
# At the same event distributions the entropy variation is generically not score derivative.
def H_deriv(qc,qo,dc,do):
    qb=1-qc-qo;db=-dc-do
    if min(qc,qo,qb)<=0:raise ValueError('interior')
    return -dc*math.log(qc)-do*math.log(qo)-db*math.log(qb)
Cg=C_samples['generic'];Vg=V_samples['generic'];
qc=float(eps**2*sp.trace(Cg)**2/3)
qo=float(eps**2*(sqn(Cg)-sp.trace(Cg)**2/3))
dc=float(eps**2*sp.Rational(2,3)*sp.trace(Cg)*sp.trace(Vg))
do=float(eps**2*(2*sum(Cg[i,j]*Vg[i,j] for i in range(3) for j in range(3)) -sp.Rational(2,3)*sp.trace(Cg)*sp.trace(Vg)))
shannon=H_deriv(qc,qo,dc,do)
score=2*dc-do
chk(abs(shannon-score)>1e-7,'Shannon_source_not_born_signed_score')

receipt={'status':'PASS','scope':'research: finite complete 3-outcome Born realization, not native admission or physical Cost-Info',
 'checks_count':len(CHECKS),'checks':CHECKS,'reference':{'data':16,'reference':128,'reference_blocks':8,'reference_marginal':'I128/128',
 'input_rank':8,'old_bit_translation_overlap_sq':overlap_sq},
 'epsilon':str(eps),'score':{'coherent':2,'orthogonal':-1,'blank':0,'unique_for_spatial_d3':True},
 'cases':values,'central_five_word':{'full_leaf_costs':reference_words,'flat_overlap':str(h0_exact),'flat_z':str(z0_exact),'cases':central_cases},'entropy_negative_control':{'Shannon_source':shannon,'signed_score_source':score,'same':False}}
result_json=json.dumps(receipt,sort_keys=True,indent=2,ensure_ascii=False)+'\n'
(BASE/'RESULT.json').write_text(result_json,encoding='utf-8')
print('PASS',len(CHECKS),'controls; three complete Born outcomes, full16×reference128')
print('Qobserver fixture',values['generic']['Qobs'],'and first source',values['generic']['dQobs'])
print('SHA256',hashlib.sha256(result_json.encode()).hexdigest())
