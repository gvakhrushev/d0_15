#!/usr/bin/env python3
"""D0 original return record: exact Q8 temporal-phase transfer, full Info,
source-safe infinite history, and conditional native code Cost-Info.

Consumes the preceding native word/reachability theorem at dfc0275e.
Does not claim selected Book Info, a new field writer, or physical GR.
All checks survive python -O. No stochastic sampling is used.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from fractions import Fraction as Fr
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

HERE=Path(__file__).resolve().parent
CHECKS: list[str]=[]
def check(name: str, condition) -> None:
    if not bool(condition):
        raise AssertionError(name)
    CHECKS.append(name)

def find_input(path: str | None) -> Path:
    if path:
        return Path(path)
    fallback=HERE/'inputs/check_native_nested_return.py'
    if fallback.exists():
        return fallback
    return HERE.parents[3]/'02_REGISTRY/research/sources/d0_native_nested_return_source_2026-10-21/check_native_nested_return.py'

parser=argparse.ArgumentParser()
parser.add_argument('--input-source')
parser.add_argument('--output',type=Path,default=HERE/'RESULT.json')
args=parser.parse_args()
source=find_input(args.input_source)
source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
check('pinned_original_word_reachability_input',source_sha=='727e4ae3e113f1195e0fb9c330dadeb7a01154424c80c0b2816a11b740b14cb7')

# Literal original quaternion/G/WRITE palette, exact Golden quotient.
a=sp.symbols('a', real=True)
fpoly=sp.Poly(a**4+a*a-1,a)
def gold(x):
    return sp.rem(sp.Poly(sp.expand(x),a),fpoly).as_expr()
def gm(M):
    return M.applyfunc(gold)
p=a*a
G=sp.Matrix([[a,-p],[p,a]])
Li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
Lj=sp.Matrix([[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]])
X=sp.diag(sp.eye(4),Li)
Y=sp.diag(Lj,Lj)
Z=sp.diag(sp.eye(4),-sp.eye(4))
W=sp.zeros(16)
for arm in range(2):
    for spin in range(4):
        for bit in range(2):
            W[8*arm+2*spin+(bit^arm),8*arm+2*spin+bit]=1
palette={'G':sp.kronecker_product(G,sp.eye(8)),
         'X':sp.kronecker_product(X,sp.eye(2)),
         'Y':sp.kronecker_product(Y,sp.eye(2)),
         'WRITE':W,'idle':sp.eye(16)}
order=['G','X','Y']+['X']*3+['Y']*3+['X']*2+['G']+['X']*2+['WRITE','idle']
check('native_sixteen_stage_word',len(order)==16)
plus=['idle']*2+order+['idle']*4
minus=['X']*2+order+['X']*2+['Y']*2
check('both_declared_words_have_22_stages',len(plus)==len(minus)==22)
def execute(word):
    M=sp.eye(16)
    for name in word:
        M=gm(palette[name]*M)
    return M
Mp=execute(plus);Mm=execute(minus)
Zfull=sp.kronecker_product(Z,sp.eye(2))
check('central_Q8_minus_identity',palette['Y']**2==-sp.eye(16))
check('native_relative_Q8_phase',palette['X']**2==Zfull)
check('literal_word_phase_transform',gm(Mm+Zfull*Mp*Zfull)==sp.zeros(16))
check('complete_native_words_are_unitary',gm(Mp.T*Mp)==gm(Mm.T*Mm)==sp.eye(16))

# The analytic extension parameter c is not a newly admitted arbitrary gate.
c,k,d,q=sp.symbols('c k d q', real=True)
rel=sp.Poly(k*k-(1-c*c),k)
def red(x):
    n,den=sp.fraction(sp.cancel(x))
    return sp.factor(sp.rem(sp.Poly(n,k),rel).as_expr()/sp.rem(sp.Poly(den,k),rel).as_expr())
def rm(A):
    return A.applyfunc(red)
M=sp.Matrix([[c,0,-k,0],[0,c,0,-k],[0,-k,0,-c],[-k,0,-c,0]])
Q=sp.diag(0,1,1,1);P=sp.eye(4)-Q;j=sp.eye(4)[:,0];V=Q*M
Z4=sp.diag(1,1,-1,-1)
check('analytic_sign_pair_matches_Q8_word',M.subs(c,-c)==-Z4*M*Z4)
perm=sp.zeros(16)
for arm in range(2):
    for spin in range(4):
        for bit in range(2):perm[4*(2*arm+bit)+spin,8*arm+2*spin+bit]=1
Mn=gm(M.subs({c:p-p*p,k:2*a**3}))
check('native_factorization_preserved',gm(perm*Mp*perm.T)==sp.kronecker_product(Mn,sp.eye(4)))
check('native_reference_Q8_conjugation',gm(perm*Mm*perm.T)==sp.kronecker_product(-Z4*Mn*Z4,sp.eye(4)))
check('complete_Kac_defect',rm(sp.eye(4)-V*V.T)==P)
for n in (1,2,3,4,7):
    f=(M*V**(n-1))[0,0]
    fn=red(f)
    check('temporal_phase_parity_'+str(n),red(fn.subs(c,-c)-(-1)**n*fn)==0)

# Rational realization of the exact native transfer; cross-kernel via a
# finite 9x9 Stein equation, not a fit to sampled amplitudes.
D=lambda x:sp.Matrix([[x,0,-1],[-(1-x*x),0,-x],[0,-x,0]])
b=lambda x:sp.Matrix([[0,-(1-x*x),0]])
C=sp.Matrix([0,0,-1])
Theta=(c-c*c*q-c*q*q+q**3)/(1-c*q-c*c*q*q+c*q**3)
check('rational_original_transfer',sp.factor(c+q*(b(c)*(sp.eye(3)-q*D(c)).inv()*C)[0]-Theta)==0)
unknowns=sp.symbols('x:9');XX=sp.Matrix(3,3,unknowns)
Aeq,beq=sp.linear_eq_to_matrix(list(XX-D(c)*XX*D(d).T-C*C.T),unknowns)
solution=list(sp.linsolve((Aeq,beq),unknowns))[0]
XS=sp.Matrix(3,3,solution)
check('cross_kernel_Stein_exact',all(sp.factor(t)==0 for t in XS-D(c)*XS*D(d).T-C*C.T))
K=sp.factor(c*d+(b(c)*XS*b(d).T)[0])
check('whole_return_amplitude_norm',sp.factor(K.subs(d,c)-1)==0)
check('zero_diagonal_Berry_for_real_family',sp.factor(sp.diff(K,c).subs(d,c))==0)
QFI=sp.factor(4*sp.diff(K,c,d).subs(d,c))
check('exact_whole_record_QFI',sp.factor(QFI-16*(1+c*c)/(1-c*c)**2)==0)
Kopp=sp.factor(K.subs(d,-c))
Kopp_expected=(1-2*c*c-7*c**4)/(1+6*c*c+c**4)
check('exact_opposite_orientation_overlap',sp.factor(Kopp-Kopp_expected)==0)
wodd=sp.factor((1-Kopp)/2)
check('actual_odd_duration_probability',sp.factor(wodd-4*c*c*(1+c*c)/(1+6*c*c+c**4))==0)
p0=(sp.sqrt(5)-1)/2;c0=sp.simplify(p0**3)
check('native_Golden_Fisher',sp.simplify(QFI.subs(c,c0)-(10+4*sp.sqrt(5)))==0)
check('native_opposite_overlap',sp.simplify(Kopp.subs(c,c0)-(4*sp.sqrt(5)-7)/3)==0)
bright=sp.simplify(4*p0**3*wodd.subs(c,c0))
check('native_Golden_comparison_flag',sp.simplify(bright-(12*sp.sqrt(5)-sp.Rational(80,3)))==0)
Z2=sp.diag(1,-1)
check('native_inverse_Golden_identity',gm(Z2*G*Z2-G.T)==sp.zeros(2))
seed=sp.Matrix([a,p])
for parity in (0,1):
    out=gm(G.T*(Z2**parity)*seed)
    check('same_time_reference_flag_'+str(parity),gold(out[1]**2-(4*p**3 if parity else 0))==0)

# Full finite-cap prefix code and occupied-state accounting.
N=sp.symbols('N',integer=True,positive=True)
for nv in (1,2,4,8):
    kraft=sum(p0**(2*n-1) for n in range(1,nv+1))+p0**(2*nv)
    check('complete_status_code_including_abort_'+str(nv),sp.simplify(kraft-1)==0)
# Nonnegative code redundancy identity is checked formally, including zeros by limit.
P1,P2,L=sp.symbols('P1 P2 L',positive=True)
check('KL_cost_information_identity',sp.expand((P1+2*P2)+(P1*sp.log(P1)+P2*sp.log(P2))/L
 - (P1*(sp.log(P1)+L)+P2*(sp.log(P2)+2*L))/L)==0)

# Explicit rational C1 tail bound: ||V^n|| <=2*(31/32)^n in the previously
# proved open contraction neighborhood, and derivative ||dot M||<=B.
aR=Fr(31,32);rR=aR*aR
check('rational_rate_covers_previous_block_contraction',aR**8>Fr(3,4))
check('amplitude_tail_in_monotone_entropy_domain',2*aR**63<Fr(1,2))
def bounds(n:int,B:Fr=Fr(2)):
    den=1-rR
    S1=rR**(n+1)*(Fr(n+1)/den+rR/den**2)
    S2=rR**(n+1)*(Fr((n+1)**2)/den+2*(n+1)*rR/den**2+rR*(1+rR)/den**3)
    val=2*S1
    source=80*B*(S1+Fr(2,31)*S2+(n+Fr(2,31)*n*n)*rR**n)
    code_source=288*B*n*rR**n
    return val,source,source+code_source
bound= bounds(1024)
check('rigorous_rational_tail_value_lt_2e_24',bound[0]<Fr(2,10**24))
check('rigorous_rational_source_tail_lt_11e_21',bound[2]<Fr(11,10**21))

# Complete amplitudes and their ordered source, high precision; old support
# zeros are evaluated by the exact continuous entropy derivative at zero.
mp.mp.dps=90
pp=(mp.sqrt(5)-1)/2;cc=pp**3;lg=mp.log(1/pp)
def compute(cval,Ncap:int):
    kval=mp.sqrt(1-cval*cval)
    MM=mp.matrix([[cval,0,-kval,0],[0,cval,0,-kval],
                  [0,-kval,0,-cval],[-kval,0,-cval,0]])
    DM=mp.matrix([[1,0,cval/kval,0],[0,1,0,cval/kval],
                  [0,cval/kval,0,-1],[cval/kval,0,-1,0]])
    QQ=mp.diag([0,1,1,1]);VV=QQ*MM;DV=QQ*DM
    xx=mp.matrix([1,0,0,0]);dx=mp.matrix(4,1)
    prob=mp.mpf(0);mean=mp.mpf(0);H=mp.mpf(0);DH=mp.mpf(0)
    phase=mp.mpf(0);odds=mp.mpf(0);record_qfi=mp.mpf(0)
    code=mp.mpf(0);dcode=mp.mpf(0);deriv_norm=mp.mpf(0)
    hist=[]
    for n in range(1,Ncap+1):
        ff=(MM*xx)[0];df=(DM*xx+MM*dx)[0]
        pn=ff*ff;dpn=2*ff*df
        if pn>0:
            H-=pn*mp.log(pn)/lg
            DH-=dpn*(1+mp.log(pn))/lg
        record_qfi+=4*df*df
        prob+=pn;mean+=n*pn
        code+=(2*n-1)*pn;dcode+=(2*n-1)*dpn
        phase+=(-1)**n*pn
        if n%2:odds+=pn
        hist.append((ff,df,pn,dpn))
        dx=DV*xx+VV*dx;xx=VV*xx
    surv=sum(v*v for v in xx);ds=2*sum(xx[i]*dx[i] for i in range(4))
    Hcap=H-(surv*mp.log(surv)/lg if surv else 0)
    DHcap=DH-(ds*(1+mp.log(surv))/lg if surv else 0)
    hcoh=-(surv*mp.log(surv)+(1-surv)*mp.log1p(-surv))/lg if 0<surv<1 else mp.mpf(0)
    dhcoh=ds*mp.log((1-surv)/surv)/lg if 0<surv<1 else mp.mpf(0)
    codecap=code+2*Ncap*surv;dcodecap=dcode+2*Ncap*ds
    return dict(prob=prob,mean=mean,H=H,DH=DH,Hcap=Hcap,DHcap=DHcap,
                phase=phase,odd=odds,QFI=record_qfi,survival=surv,ds=ds,
                code=codecap,dcode=dcodecap,coherent_flags_entropy=hcoh,
                d_coherent_flags_entropy=dhcoh,hist=hist,M=MM)
res=compute(cc,1024)
check('whole_probability_and_paid_mean',abs(res['prob']-1)<mp.mpf('1e-70') and abs(res['mean']-4)<mp.mpf('1e-70'))
check('all_status_code_average_seven',abs(res['code']-7)<mp.mpf('1e-70'))
check('paid_code_first_source_zero',abs(res['dcode'])<mp.mpf('1e-70'))
check('whole_record_QFI_rational_formula',abs(res['QFI']-(10+4*mp.sqrt(5)))<mp.mpf('1e-70'))
check('opposite_program_phase_overlap',abs(res['phase']-(4*mp.sqrt(5)-7)/3)<mp.mpf('1e-70'))
check('first_return_second_history_structurally_zero',res['hist'][1][2]==0)
check('nonzero_full_pointer_source',res['DH']>10 and res['DH']<11)
# Central finite differences validate independent derivatives; not a proof
# of the tail and not a finite-difference source substituted for the formula.
h=mp.mpf('1e-14');rp=compute(cc+h,320);rm_=compute(cc-h,320)
fd=(rp['Hcap']-rm_['Hcap'])/(2*h)
check('independent_entropy_source_difference',abs(fd-res['DH'])<mp.mpf('1e-23'))
# Coherent time record vs pointer, identical original amplitudes.
rsmall=compute(cc,12)
fs=np.array([complex(float(z[0])) for z in rsmall['hist']])
surv=float(rsmall['survival'])
rho=np.zeros((13,13),dtype=complex);rho[:12,:12]=np.outer(fs,fs.conj());rho[12,12]=surv
EV=np.linalg.eigvalsh(rho)
check('finite_coherent_record_spectrum',[round(x,12) for x in EV[-2:]]==sorted([round(surv,12),round(1-surv,12)]))
def entropy(probs):
    return -sum(float(t)*np.log(float(t))/float(lg) for t in probs if t>1e-15)
check('coherent_pointer_gap_is_dephasing_coherence',abs(entropy(np.diag(rho).real)-entropy(EV)
 -(float(rsmall['Hcap'])-float(rsmall['coherent_flags_entropy'])))<1e-12)
# Every actual terminal branch preserves oldRIGHT128 even with arbitrary
# entanglement of the fresh selector and logical128 input.
rng=np.random.default_rng(334211)
AA=rng.normal(size=(256,128))+1j*rng.normal(size=(256,128))
CC=np.linalg.qr(AA)[0]/np.sqrt(128)
for n in (1,3,4,7):
    fval=float(res['hist'][n-1][0]);phase_n=(-1)**n
    CN=fval*np.vstack((CC[:128],phase_n*CC[128:]))
    check('conditional_oldRIGHT128_gram_'+str(n),np.linalg.norm(CN.conj().T@CN-fval*fval*CC.conj().T@CC,2)<2e-15)
# Exact c=0 hostile control: probability support changes although M is smooth.
f0=q*Theta
ser=sp.series(f0,q,0,9).removeO().expand()
check('support_birth_amplitudes',[(sp.factor(ser.coeff(q,n)).subs(c,0)) for n in range(1,9)]==[0,0,0,1,0,0,0,0])
born=sum(sp.diff(ser.coeff(q,n),c).subs(c,0)**2 for n in range(1,9))
check('new_probability_mass_coefficient',born==4)
check('nonC2_entropy_coefficient',born!=0) # H ~ -4c² log(c²)/ln(phi)

qG=4*pp**3
hG=-(qG*mp.log(qG)+(1-qG)*mp.log1p(-qG))/lg
odd=(5-2*mp.sqrt(5))/3
dodd=mp.mpf(4)/9+mp.sqrt(5)/3
compare_flag= qG*odd
Hjoint=res['H']+odd*hG
record_cost=8+compare_flag
source_compare=-res['DH']+(qG-hG)*dodd
check('recorded_phase_comparison_positive_probability',0<compare_flag<1)
check('full_comparison_information_not_marginal_bit',Hjoint-(-(compare_flag*mp.log(compare_flag)+(1-compare_flag)*mp.log1p(-compare_flag))/lg)>0)

out={
 'status':'AUTHOR_CHECKS_PASS','checks':CHECKS,'count':len(CHECKS),
 'source_ref':'dfc0275eea67ebc21ffe539de9b6ea96713863a5','source_sha256':source_sha,
 'native_c':str(cc),'return_pointer_entropy_phi':mp.nstr(res['H'],35),
 'return_pointer_entropy_c_source':mp.nstr(res['DH'],35),
 'status_Cost_minus_pointer_Info':mp.nstr(7-res['H'],35),
 'status_Cost_minus_Info_source':mp.nstr(-res['DH'],35),
 'whole_record_QFI_exact':'10+4sqrt(5)',
 'opposite_phase_overlap_exact':'(4sqrt(5)-7)/3',
 'odd_return_probability_exact':'(5-2sqrt(5))/3',
 'Golden_comparison_click_exact':'12sqrt(5)-80/3',
 'Golden_comparison_click':mp.nstr(compare_flag,30),
 'comparison_full_pointer_entropy_phi':mp.nstr(Hjoint,30),
 'comparison_record_Cost_minus_Info':mp.nstr(record_cost-Hjoint,30),
 'comparison_record_first_source':mp.nstr(source_compare,30),
 'N':1024,'entropy_value_tail_bound':float(bound[0]),
 'entropy_source_tail_bound':float(bound[1]),'code_minus_Info_source_tail_bound':float(bound[2]),
 'oldRIGHT128_test_scope':'one common original logical return with spectator identity; arbitrary normalized source columns',
 'negative_control':'coherent parity vs probability equality; c=0 entropy not C2',
 'analysis_parameter_c_not_automatically_admitted_field':True,
 'selected_Book_Info':False,'same_cost_of_22_stage_words_assumed':False,
 'primitive_gate_costs_and_generated_state_sources_remaining':True,
 'independent_review':False,'GR_closed':False
}
args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
