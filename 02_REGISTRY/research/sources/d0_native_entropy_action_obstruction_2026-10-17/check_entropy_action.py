#!/usr/bin/env python3
"""D0 #334: exact actual-shell exit-count obstruction to normalized history selection.

No native action changes; full pointer source asymptotics are consumed from
A4D_COMPLETE_HISTORY_INFORMATION_SCALE, not inferred from coarse-bit entropy.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
import sympy as s

OUT = Path(__file__).resolve().parent
checks = []
def require(ok, label):
    if not bool(ok):
        raise ArithmeticError(label)
    checks.append(label)

root5 = s.sqrt(5)
p = (root5-1)/2
p2 = s.simplify(p*p)
beta = s.simplify(2*p2)
require(s.simplify(p+p2-1)==0,'golden_split')
require(s.simplify(beta-(3-root5))==0,'unchanged_v8_beta')
require(s.simplify(p2-(3-root5)/2)==0,'golden_p2')

# Check full 16-state CAR Clifford square, no single-grade reduction.
def creator(i):
    c=s.zeros(16)
    for mask in range(16):
        if not mask & (1<<i):
            sign=(-1)**(sum(bool(mask&(1<<j)) for j in range(i)))
            c[mask|(1<<i),mask]=sign
    return c
cs=[creator(i) for i in range(4)]
for i in range(4):
    for j in range(4):
        require(cs[i]*cs[j].T+cs[j].T*cs[i]==(s.eye(16) if i==j else s.zeros(16)),f'CAR_{i}_{j}')
coeff=[s.Integer(1)+2*s.I,s.Rational(2,3)-s.I,s.Integer(-3),s.I/2]
D=sum((v*c+s.conjugate(v)*c.T for v,c in zip(coeff,cs)),s.zeros(16))
lam=s.expand(sum(s.conjugate(v)*v for v in coeff))
require(all(s.expand(t)==0 for t in (D*D-lam*s.eye(16))),'all16_clifford_square_scalar')
require(s.simplify(lam-s.Rational(17*1,1))!=0, 'nontrivial_clifford_fixture')

# Exact 128-shell eigenvalue and actual repeat/clock relation.
d=s.Float('0.063635191594344535042829697433316630182693569761541',50)
o=s.Float('0.0040167350432317253',50)
G=s.eye(4)*(d-o)+s.ones(4)*o
require(G[0,0]==G[1,1] and G[0,0]==G[2,2] and G[0,0]==G[3,3], 'shell_all_four_axes_same_gram')
require(all(s.N(v)>0 for v in (d-o,d+3*o)), 'positive_gram')
require(all(G[i,i]==d for i in range(4)), 'shell_diag_d')
require(8*16==128,'shell_x_fock_equals_reference128')

# Every coarse exit pattern follows from the scalar full-shell effects,
# independently of changing conditional Fock/reference states.
q=s.symbols('q',positive=True)
Nsmall=5
require(s.expand(sum(s.binomial(Nsmall,k)*q**k*(1-q)**(Nsmall-k) for k in range(Nsmall+1)))==1,
        'complete_five_tick_coarse_exit_law')
require(s.simplify(sum(k*s.binomial(Nsmall,k)*q**k*(1-q)**(Nsmall-k) for k in range(Nsmall+1))-Nsmall*q)==0,
        'total_exits_not_first_exit')
require(s.simplify(s.diff(-q*s.log(q)-(1-q)*s.log(1-q),q)-s.log((1-q)/q))==0,
        'exact_binary_entropy_source')
require(s.simplify((1-(1-q)**Nsmall)-Nsmall*q)!=0,'hostile_first_exit_miscount_rejected')


ell=[]
for L in (4,8,12,16,24,32):
    ep=p2/(64*L*L)
    n=128*L*L
    m=2*n
    alpha=ep/2
    gam=4*L*L*s.sin(s.pi/L)**2
    la=gam*d
    require(s.simplify(n*ep-beta)==0, f'actual_clock_n_epsilon_L{L}')
    require(s.simplify(m*alpha-beta)==0,f'actual_clock_m_alpha_L{L}')
    if L==8:
        require(s.simplify(gam-(128-64*s.sqrt(2)))==0, 'exact_eighth_root_shell_gamma')
    ev=s.expand(ep*la*(1-ep*la/4))
    evprime=s.expand(ep*la*(1-ep*la/2))
    mcount=s.expand(n*ev)
    mprime=s.expand(n*evprime)
    require(0<float(ev)<1, f'proper_effect_L{L}')
    require(float(mprime)>0, f'exit_source_positive_L{L}')
    require(float(mprime)<float(beta*la), f'finite_clock_source_strictly_less_asymptotic_L{L}')
    # One coarse bit at every tick: exact expectation of iid Bernoulli exits.
    entropy_bit_prime=float(mprime)*math.log((1-float(ev))/float(ev))
    require(entropy_bit_prime>0, f'actual_bit_entropy_source_positive_L{L}')
    ell.append({'L':L,'shell_lambda':float(la),'epsilon':float(ep),'n':n,
      'total_exit_mean':float(mcount),'total_exit_first_source':float(mprime),
      'log_inverse_clock':math.log(1/float(ep)),
      'coarse_exit_bit_entropy_source_nats':entropy_bit_prime,
      'asymptotic_full_pointer_source_per_log_in_phi_units':float(mprime)/(math.log(1/float(p)))})

require(ell[0]['total_exit_first_source']<ell[-1]['total_exit_first_source'], 'exit_first_source_increasing_fixture')
require(ell[-1]['asymptotic_full_pointer_source_per_log_in_phi_units']>3.9, 'positive_full_pointer_log_coefficient')

pfloat=float(p);p2float=float(p2);bfloat=float(beta)
df=float(d);of=float(o);zeta=2.0**-20;M=128
GF=(df-of)*np.eye(4)+of*np.ones((4,4))
roots=[]
for L in (8,12,16,24,32):
    # Exact same L^4 Fourier momenta; each momentum has 16 CAR grades.
    axes=np.arange(L,dtype=np.float64)
    phase=L*np.expm1(2j*np.pi*axes/L)
    # Vectorized 4D tensor using broadcasting; generate one 4xN phase array.
    idx=np.indices((L,)*4,dtype=np.int16).reshape(4,-1)
    w=phase[idx].T
    La=np.einsum('bi,ij,bj->b',w.conj(),GF,w,optimize=True).real
    La=np.maximum(La,0)
    eps=p2float/(64*L*L)
    n=128*L*L;m=2*n;alpha=eps/2
    B=1-alpha*La
    require(np.min(B)>0,f'full_B_positive_L{L}')
    K=np.power(B,m)
    T=float(np.sum(K,dtype=np.float64))
    Z=16*T
    den=1-zeta+zeta*K
    sum_response=float(np.sum(La*K/B,dtype=np.float64))
    # d/dt on G(t)=(1+t)G, at t=0.
    Hprime=-sum_response/T
    Jprime=16*M*bfloat*zeta*float(np.sum(La*K/B/den,dtype=np.float64))
    Rprime=float(4*L*L*math.sin(math.pi/L)**2*df)
    SPR=Hprime+Jprime+Rprime
    dsurv=bfloat*Hprime
    dblank=-Jprime/M
    require(np.isfinite(dsurv) and np.isfinite(dblank),f'both_event_normalizers_sources_finite_L{L}')
    require(abs(dsurv)<100 and abs(dblank)<100,f'both_event_normalizers_sources_bounded_fixture_L{L}')
    require(np.isfinite(SPR),f'price_source_finite_L{L}')
    require(abs(SPR)<10.0,f'price_source_bounded_observed_L{L}')
    roots.append({'L':L,'modes':L**4,'full_thermal_dimension':16*L**4,
      'Z':Z,'min_B':float(np.min(B)),'Hprime':Hprime,'Jprime':Jprime,
      'Rprime':Rprime,'dlog_survival_event':dsurv,'dlog_blank_event':dblank,'v8_radial_source':SPR,
      'v8_source_over_loginverse_epsilon':SPR/math.log(1/eps)})

require(abs(roots[0]['v8_radial_source'])<2e-6,'certified_L8_root_stationary_radial_numeric_control')
require(max(abs(x['v8_radial_source']) for x in roots)<5.,'fixed_beta_source_stable_across_cutoffs')
# Direct numerical check full price is differentiated correctly at L8 without C.
L=8;alpha=p2float/(128*L*L);m=256*L*L
phase=L*np.expm1(2j*np.pi*np.arange(L)/L)
idx=np.indices((L,)*4,dtype=np.int16).reshape(4,-1)
w=phase[idx].T
La=np.einsum('bi,ij,bj->b',w.conj(),GF,w,optimize=True).real
La=np.maximum(La,0)
def action(t):
    b=1-alpha*(1+t)*La
    k=b**m
    return math.log(16*np.sum(k))/bfloat-16*M*np.sum(np.log1p(-zeta*(1-k)))+(1+t)*roots[0]['Rprime']
for h in (1e-4,2e-4):
    slope=(action(h)-action(-h))/(2*h)
    require(abs(slope-roots[0]['v8_radial_source'])<1e-3,f'finite_diff_native_price_h{h}')

# Analytic fixed-beta bound of the entire thermal source:
# gamma_min: |L(exp(2pi i k/L)-1)| >=4|wrap(k)|, hence
# Delta(k)>=16*b*|k|^2; B>=1-(p^2/8)*a where a=d+3o.
bmin=df-of;amax=df+3*of
Bfloor=1-p2float*amax/8
require(Bfloor>0.99,'all_L_uniform_B_floor')
require(bmin>0.05,'all_L_uniform_G_floor')
# Positive 4D Gaussian sum controls every numerator, independent of L.
# Sum_j |k|² exp(-16 beta b |k|²) is finite as an ordinary lattice Gaussian.
const=16*bfloat*bmin
# Factorizable one-dimensional moments for an explicit (conservative) uniform bound.
S0=1+2*sum(math.exp(-const*j*j) for j in range(1,50))
S2=2*sum(j*j*math.exp(-const*j*j) for j in range(1,50))
Gauss4=4*S2*S0**3
upper_num=4*math.pi**2*amax*Gauss4/Bfloor
price_bound=upper_num/1.0+(16*M*bfloat*zeta/(1-zeta))*upper_num +4*math.pi**2*df
require(price_bound<1e8,'gaussian_finite_uniform_price_bound')

limit_lambda=4*math.pi**2*df
limit_mprime=bfloat*limit_lambda
phi=1/pfloat
limit_src_phi=limit_mprime/math.log(phi)
require(limit_src_phi>3.9,'actual_full_history_positive_log_slope')
require(limit_src_phi<4.1,'actual_full_history_log_slope_not_fitted')

record={'scope':'Native full128 Julia/golden complete record, homogeneous flat CAR eigenshell and original fixed beta/M/z v8 price; source asymptotic invokes existing full-tape theorem, not a reconstructed 128^n probability table',
  'inputs':{'d':str(d),'o':str(o),'p2':str(p2),'beta':str(beta),'zeta':'2^-20','M':128},
  'analytic':{'epsilon':'p^2/(64 L^2)','n':'128 L^2','m':'256 L^2','beta':'n epsilon=m alpha=2p^2',
    'lambda_shell':'4 L^2 sin(pi/L)^2 d, multiplicity 8*16=128',
    'q_exit':'epsilon lambda(1-epsilon lambda/4)',
    'm_exit_prime':'beta lambda(1-epsilon lambda/2)',
    'full_pointer_source_limit':'H_pointer_prime/log(1/epsilon)->beta*4*pi^2*d, requires complete-history theorem inputs',
    'v8_source_limit':'S_v8_prime/log(1/epsilon)->0 by uniformly convergent fixed-beta thermal sums',
    'event_normalizer_limit':'dlog P_surv=beta Hprime and dlog P_blank= -Jprime/M are uniformly bounded; fixed linear combinations cannot cancel the history logarithmic source',
    'phi_unit_source_limit':limit_src_phi,
    'strict_obstruction':'If normalized same-history Cost-Info=H_pointer/log(phi), its source cannot equal unchanged v8 source up to field-independent terms or o(log clock) remainder on this family',
    'gaussian_bound':{'b':bmin,'a':amax,'Bfloor':Bfloor,'sum_prefactor':const,'coarse_upper_price_source':price_bound}},
  'shell_sequence':ell,'full_temperature_sequence':roots,
  'checks_count':len(checks),'checks':checks,
  'status':'EXACT algebra with numeric v8 control; scoped conditional action-selection NO-GO, NOT GR, NOT physical law selection; full tape analytic theorem consumed, not numerically replayed'}
(OUT/'RESULT.json').write_text(json.dumps(record,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print(json.dumps({'checks':len(checks),'L8_radial_source':roots[0]['v8_radial_source'],
 'L32_radial_source':roots[-1]['v8_radial_source'],
 'full_pointer_phi_units_coefficient':limit_src_phi,'bound':price_bound},sort_keys=True))
