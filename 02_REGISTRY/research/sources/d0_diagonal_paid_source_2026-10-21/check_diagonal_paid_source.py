#!/usr/bin/env python3
"""Author checks for finite paid rational-CQ secants. Not a physical Book03 source."""
from __future__ import annotations
import json
import math
from fractions import Fraction
from pathlib import Path
import argparse
import mpmath as mp
import sympy as sp

mp.mp.dps=90
PHI=(1+mp.sqrt(5))/2
P=1/PHI
ELL=mp.log(PHI)
R0=P
ALPHA=P**3/8
ETA=mp.mpf('0.55')
G_DIAGNOSTIC=mp.mpf('0.375')  # diagnostic only, NOT native cap-one gamma1
checks=[]

def require(condition,name):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)

def hphi(r):
    return -(r*mp.log(r)+(1-r)*mp.log(1-r))/ELL

def price(r):
    # Both original report costs (1,2), full measured CQ entropy.
    return 1+r-hphi(r)

def r_from_s(s):
    return R0+ALPHA*s*s

def rational_rotation(k):
    delta=mp.power(2,-k)
    M=1<<(5*k)
    r=mp.tan(delta/2)
    m=int(mp.nint(r*M))
    denominator=M*M+m*m
    diag=Fraction(M*M-m*m,denominator)
    sin=Fraction(2*M*m,denominator)
    require(diag*diag+sin*sin==1,f'k{k}: exact rational orthogonal')
    require(denominator>0 and M>0,f'k{k}: integer denominator')
    B=1 << (denominator-1).bit_length()
    success=Fraction(denominator,2*B)**2
    require(Fraction(1,16)<success<=Fraction(1,4),f'k{k}: precision independent herald lower bound')
    require(abs(mp.mpf(m)/M-r)<=mp.mpf(1)/(2*M),f'k{k}: rounded half angle')
    angle=2*mp.atan(mp.mpf(m)/M)
    require(abs(angle-delta)<=mp.mpf(1)/M,f'k{k}: angular accuracy')
    return delta,diag,sin,success,denominator,B

root=sp.sqrt(5)
p=(root-1)/2
require(sp.simplify(p*p+p-1)==0,'native p+p2=1')
require(sp.simplify((2*p*p+p)-(2-p))==0,'two port Shannon identity')
require(sp.simplify((1-p)/p-p)==0,'original nonblank port1 has hprime=-1')
require(sp.simplify((1-p*p)/(p*p)-1/p)==0,'other Golden orientation has hprime=+1')

records=[]
prev_err=None
for k in (4,5,6,7,8):
    delta,cr,sr,success,R,B=rational_rotation(k)
    sr_mp=mp.mpf(sr.numerator)/sr.denominator
    rhat=r_from_s(sr_mp)
    rtrue=r_from_s(mp.sin(delta))
    fplus=price(rhat)
    fminus=price(rhat)
    fzero=price(R0)
    second=(fplus-2*fzero+fminus)/(delta*delta)
    exact_second=2*ALPHA*(1-mp.log((1-R0)/R0)/ELL)
    err=abs(second-exact_second)
    require(err<mp.mpf(40)*delta*delta,f'k{k}: full charged-CQ Hessian secant O(delta2)')
    if prev_err is not None:
        require(err<prev_err*.5,f'k{k}: Hessian error decreases')
    prev_err=err

    Bwrite=mp.mpf(125)
    code_plus=Bwrite+ETA*fplus
    code_minus=Bwrite+ETA*fminus
    code_zero=Bwrite+ETA*fzero
    actual_second=(code_plus-2*code_zero+code_minus)/(ETA*delta*delta)
    require(abs(actual_second-second)<mp.mpf('1e-68'),f'k{k}: common PAID baseline cancels in numerical quotient')

    tv=abs(rhat-rtrue)
    ent=hphi(rhat)*ELL
    true_ent=hphi(rtrue)*ELL
    hb=-(tv*mp.log(tv)+(1-tv)*mp.log(1-tv)) if tv else mp.mpf(0)
    require(abs(ent-true_ent)<=hb+mp.mpf('1e-60'),f'k{k}: full quantum entropy without outcome floor')
    require(abs(price(rhat)-price(rtrue))<=tv+hb/ELL+mp.mpf('1e-60'),f'k{k}: full charged CQ value continuity')
    require(success>Fraction(1,16),f'k{k}: positive herald effect')
    rp=R0+ALPHA*sr_mp
    rm=R0-ALPHA*sr_mp
    grad=(price(rp)-price(rm))/(2*delta)
    ideal_grad=ALPHA*(1-mp.log((1-R0)/R0)/ELL)
    grad_error=abs(grad-ideal_grad)
    require(grad_error<mp.mpf(20)*delta*delta,f'k{k}: full charged CQ first secant O(delta2)')
    require(abs(ideal_grad)>mp.mpf('0.001'),f'k{k}: diagnostic source nonzero')
    records.append({'k':k,'delta':mp.nstr(delta,12),
                    'first_source_error':mp.nstr(grad_error,17),
                    'denominator_bits':R.bit_length(),
                    'herald_success':str(success),
                    'second_jet_error':mp.nstr(err,17),
                    'trace_distance':mp.nstr(tv,12),
                    'full_entropy_bound':mp.nstr(hb,12)})

def binary_entropy(t):
    return -t*mp.log(t)-(1-t)*mp.log(1-t) if 0<t<1 else mp.mpf(0)

def charged_modulus(eps,m,D,cmax):
    t=mp.mpf(m)*eps
    if t >= mp.mpf('.5'):
        return mp.inf
    return 2*cmax*t+(t*mp.log(D-1)+binary_entropy(t))/ELL

def select_precision(L,m,D,cmax,jet3,jet4,gain,normfactor):
    h=mp.mpf(1)/L
    target=abs(gain)*h**3/(1+normfactor)
    for k in range(2,500):
        delta=mp.power(2,-k)
        eps=delta**5
        omega=charged_modulus(eps,m,D,cmax)
        grad=jet3*delta*delta/6+omega/delta
        hess=jet4*delta*delta/12+4*omega/(delta*delta)
        if max(grad,hess)<target:
            return {'L':L,'k':k,'delta':mp.nstr(delta,9),
                    'eps':mp.nstr(eps,9),
                    'gradient_error_bound':mp.nstr(grad,12),
                    'hessian_error_bound':mp.nstr(hess,12),
                    'normalized_bound':mp.nstr(target,12),
                    'precision_bits':5*k}
    raise AssertionError('sample finite diagonal budget did not terminate')

schedule=[]
for L in (4,8,16,32):
    # Diagnostic constants deliberately NOT claimed as native mesh bounds.
    m=3*L*L
    D=2**(6+2*int(math.log2(L)))
    cmax=25*L**3
    jet3=100*L**4
    jet4=150*L**5
    normfactor=L**4
    gain=ETA*G_DIAGNOSTIC
    selection=select_precision(L,m,D,cmax,jet3,jet4,gain,normfactor)
    require(int(selection['precision_bits'])>0,f'L{L}: finite rational precision')
    require(mp.mpf(selection['gradient_error_bound'])<mp.mpf(selection['normalized_bound']),
            f'L{L}: gradient bound')
    require(mp.mpf(selection['hessian_error_bound'])<mp.mpf(selection['normalized_bound']),
            f'L{L}: Hessian bound')
    schedule.append(selection)

require(ETA*G_DIAGNOSTIC>0,'illustrative gain only, actual ten-sign gain is separate')
y=sp.symbols('y',real=True)
report=sp.Rational(1,2)*y*y
upstream=y
require(sp.diff(report+upstream,y).subs(y,0)==1 and
        sp.diff(report,y).subs(y,0)==0,
        'moving upstream work/source NOT cancelled by downstream stationarity')
sel=sp.symbols('sel',real=True)
require(sp.diff(((1+sel)+(1-sel))/2,sel)==0 and
        sp.diff(1+sel,sel)==1,
        'uniform selector average is not one conditional code Euler')

result={'status':'PASS_DIAGONAL_PAID_CQ_SOURCE_AUTHOR_CHECKS',
        'checks_count':len(checks),'checks':checks,
        'rational_orthogonal_writer_controls':records,
        'sample_diagonal_budget':schedule,
        'gain_scope':{'native_fixed_ten_sign':'gamma_10,h !=0 (external theorem)',
                      'native_fixed_processor':'g_h=a_pi gamma_F s0>0 (external theorem)',
                      'different_cap1_gamma1':'-12.444... NOT reused',
                      'synthetic_budget_gain':str(G_DIAGNOSTIC)},
        'scope':{'cross_program_secants_not_native_Euler':True,
                 'complete_counted_CQ_only':True,
                 'no_outcome_probability_floor':True,
                 'exact_native_42_stationarity':False,
                 'common_initial_controller':False,
                 'Book03_Info_selected':False,
                 'GR_closed':False}}
parser=argparse.ArgumentParser()
parser.add_argument('--json',type=Path)
args=parser.parse_args()
payload=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
if args.json:
    args.json.write_text(payload,encoding='utf-8')
print(payload,end='')
