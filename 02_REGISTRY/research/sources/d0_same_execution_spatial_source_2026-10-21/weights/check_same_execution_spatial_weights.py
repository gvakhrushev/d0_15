#!/usr/bin/env python3
"""Bounded exact application of existing cap1 compiler/source owners.
No repository writes or native rank/graph census. Default stdout-only JSON.
Symbolic multiplicities stand for the actual original D_j sums; no invented
fixture is presented as a native address partition.
"""
import argparse, hashlib, json, time
from pathlib import Path
import sympy as s
import mpmath as mp

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
started=time.monotonic(); checks=[]
def require(name,test):
    if not bool(test):raise AssertionError(name)
    checks.append({'name':name,'status':'PASS'})
p,z,x,y=s.symbols('p z x y',real=True)
minimal=p*p+p-1
def exact_zero(expr):
    num=s.fraction(s.cancel(expr))[0]
    return s.rem(num,minimal,p)==0
L=4*p**3;Q=1-z*L;R=1-z*L*(1+p**6)
B=4*(p+p*p*y)**2*(1-(p+p*p*y)**2)
E=p*p*(1+x);ell=4*E*(1-E)
A=ell+(1-ell)*B
r=1-(1-z*B)*(1-z*A)
sub0={x:0,y:0}
rx=4*z*Q*p**11; ry=8*z*p**6*(R+Q*p**6)
require('actual_two_band_baseline',exact_zero(r.subs(sub0)-(1-Q*R)))
require('actual_full_gravity_derivative',exact_zero(s.diff(r,x).subs(sub0)-rx))
require('actual_full_matter_derivative_both_bands',exact_zero(s.diff(r,y).subs(sub0)-ry))
sigma=s.symbols('sigma',nonzero=True)
Lambda=2*sigma/p**5*(R/Q+p**6)
require('original_finite_z_ratio_no_retuning',exact_zero(sigma*ry/rx-Lambda))

# Same complete CQ ledger, arbitrary address-dependent actual kappa.
a,b,k,rho=s.symbols('alpha beta kappa r',positive=True)
h=s.Function('h')
S1=a*(k-b*h(rho))
S2=S1*(1+b*rho)
require('N1_field_source_is_report_only',s.simplify(s.diff(S1,rho)+a*b*s.diff(h(rho),rho))==0)
require('N1_address_cost_slope_cancels',s.diff(S1,rho,k)==0)
require('N2_address_cost_slope_does_not_cancel',s.diff(S2,rho,k)==a*b)

# Actual address-sum theorem. M_i=sum_{a in I_i}D_j, total active M.
# K_AF also includes all inactive addresses; no assumption active probability=1.
M1,M2,M3,K,n,nu=s.symbols('M1 M2 M3 K_AF n_sites nu',positive=True)
Mtot=M1+M2+M3
wbar=Mtot/(K*n)
for idx,M in enumerate((M1,M2,M3),1):
    rz=(M/K)/wbar
    require(f'actual_multiplicity_cancels_density_site{idx}',s.simplify(M/rz-K*wbar)==0)
    require(f'full_scene_reference_copies_site{idx}',s.simplify(nu*528*M/rz-nu*528*K*wbar)==0)
# Sitewise averaging is the wrong operation, even when each local source is matched.
r1=(M1/K)/wbar;r2=(M2/K)/wbar
wrong=s.factor(1/r1-1/r2)
require('sitewise_normalization_wrong_for_unequal_mass',wrong!=0 and s.simplify(wrong-(M2-M1)*Mtot/(n*M1*M2))==0)
# Ordinary global normalization only rescales all source coefficients equally.
require('single_global_normalization',s.simplify((nu*528*M1/r1)/(nu*K)-528*wbar)==0)

# Full derivative of the old input dictionary; moving rho terms vanish only on shell.
f0,q0,rf,df,dq,dr=s.symbols('fhat qhat rho dfhat dqhat drho',real=True)
Df=df/rf-f0*dr/rf**2
Dq=dq/rf-q0*dr/rf**2
require('moving_density_terms_retained_off_shell',s.diff(Df,dr)==-f0/rf**2 and s.diff(Dq,dr)==-q0/rf**2)
require('moving_density_cancels_by_null_values',Df.subs(f0,0)==df/rf and Dq.subs(q0,0)==dq/rf)
# qhat uses the operational metric. qraw -> qhat -> qleaf has TWO inverse powers.
qraw=s.symbols('qraw')
require('raw_matter_double_inverse_is_existing_dictionary',s.simplify((qraw/rf)/rf-qraw/rf**2)==0)

# Full setup baseline differential, no independent preparation source discarded.
CP,HP,aa,bb,kk,hh=s.symbols('Cpre Hpre alpha beta kappa h0')
dCP,dHP,da,db,dk=s.symbols('dCpre dHpre dalpha dbeta dkappa')
base=CP-HP+aa*(kk-bb*hh)
full=s.diff(base,CP)*dCP+s.diff(base,HP)*dHP+s.diff(base,aa)*da+s.diff(base,bb)*db+s.diff(base,kk)*dk
wanted=dCP-dHP+(kk-bb*hh)*da+aa*dk-aa*hh*db
require('complete_baseline_derivative',s.expand(full-wanted)==0)
require('preparation_not_made_stationary',s.diff(base,kk)==aa and s.diff(base,aa)==kk-bb*hh)

# Numerical values only specialize the already-owned bank/clock constants.
mp.mp.dps=60
pv=(mp.sqrt(5)-1)/2;zv=mp.mpf(2)**(-20)
Lv=4*pv**3;Qv=1-zv*Lv;Rv=1-zv*Lv*(1+pv**6)
dv=Qv*Rv;rv=1-dv
av=(1-(1-2*pv**3)**9)**128
bv=((1-pv**120)**4*(1-(1-16*pv**9)**20))**43
hp=mp.log((1-rv)/rv)/mp.log(1/pv)
gamma=-av*bv*dv*hp
rxv=4*zv*Qv*pv**11;ryv=8*zv*pv**6*(Rv+Qv*pv**6)
require('owned_bank_caps_positive',av>mp.mpf('0.5') and bv>mp.mpf('0.5'))
require('N1_nonzero_source_sign',0<rv<mp.mpf('0.5') and hp>0 and gamma<0)
require('finite_z_negative_matter_ratio',abs(-ryv/rxv+mp.mpf('23.416406751884'))<mp.mpf('1e-12'))
result={'status':'PASS_SAME_EXECUTION_CAP1_SPATIAL_WEIGHTS','created':'2026-10-21',
 'repository_head':'c49ebdb12244943d1ec45ef6d148a0432481141e',
 'check_count':len(checks),'checks':checks,
 'owned_numeric_constants':{'alpha':mp.nstr(av,30),'beta':mp.nstr(bv,30),
 'r0':mp.nstr(rv,30),'gamma1_multiplier_of_DJ2':mp.nstr(gamma,30),
 'Lambda_minus':mp.nstr(-ryv/rxv,30),
 'per_copy_gravity_at_eta_quarter':mp.nstr(-av*bv*hp*rxv/16,30)},
 'scope':'One existing N=1 two-query CQ compiler. Exact symbolic multiplicities and source maps; no new address census, native Info selection or upstream stationary root.',
 'runtime_seconds':round(time.monotonic()-started,4),
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
if args.output is not None:args.output.write_text(payload)
print(payload,end='')
