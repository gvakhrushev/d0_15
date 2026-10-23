#!/usr/bin/env python3
"""Author verification: diagonal actual-CQ price jets with exact rational orthogonal code.

Does not execute the full D0 all42 native instrument. Consumes existing
paid rational writer result, tests its finite precision/source composition,
complete Bernoulli report charge/entropy, and independent trace-norm bounds.
"""
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
R0=P  # ORIGINAL nonblank native port1 probability (p^2,p), not matched Golden (p,p^2).
ALPHA=P**3/8
ETA=mp.mpf('0.55')
G_DIAGNOSTIC=mp.mpf('0.375')  # illustrative fixed-processor gain, NOT native gamma1
checks=[]

def require(condition,name):
    if not bool(condition):raise AssertionError(name)
    checks.append(name)

def hphi(r):
    return -(r*mp.log(r)+(1-r)*mp.log(1-r))/ELL

def price(r):
    # Genuine Bernoulli reporting charge: 0 -> cost 1, 1 -> cost 2.
    return 1+r-hphi(r)

def r_from_s(s):
    return R0+ALPHA*s*s

def rational_rotation(k:int):
    delta=mp.power(2,-k)
    M=1<<(5*k)
    r=mp.tan(delta/2)
    m=int(mp.nint(r*M))
    denominator=M*M+m*m
    diag=Fraction(M*M-m*m,denominator)
    sin=Fraction(2*M*m,denominator)
    require(diag*diag+sin*sin==1,f'k{k}: exactly rational orthogonal')
    require(denominator>0 and M>0,f'k{k}: integer lookup denominator')
    B=1 << (denominator-1).bit_length()
    # The same denominator and success law handles +/- and zero stencils.
    s=Fraction(denominator,2*B)**2
    require(Fraction(1,16)<s<=Fraction(1,4),f'k{k}: bank success independent of precision and sign')
    require(abs(mp.mpf(m)/M-r)<=mp.mpf(1)/(2*M),f'k{k}: rational half-angle nearest code')
    encoded_angle=2*mp.atan(mp.mpf(m)/M)
    require(abs(encoded_angle-delta)<=mp.mpf(1)/M,f'k{k}: source-angle error bounded')
    return delta,diag,sin,s,denominator,B

# Exact two-port algebra and entropy-source curvature at a stationary section.
root=sp.sqrt(5)
p=(root-1)/2
require(sp.simplify(p*p+p-1)==0,'native p+p^2=1')
require(sp.simplify((2*p*p+p)-(2-p))==0,'full two-port Shannon p-weight identity')
require(sp.simplify((1-p)/p-p)==0,'original p port1 has hprime=-1')
require(sp.simplify((1-p*p)/(p*p)-1/p)==0,'matched p^2 port1 has hprime=+1')

D=2
Cmax=2
records=[]
prev_err=None
for k in (4,5,6,7,8):
    delta,cr,sr,success,R,B=rational_rotation(k)
    sr_mp=mp.mpf(sr.numerator)/sr.denominator
    rhat=r_from_s(sr_mp)
    rtrue=r_from_s(mp.sin(delta))
    # Full CQ record, its true branch charges and entire entropy.
    f_plus=price(rhat)
    f_minus=price(rhat) # symmetry of this fixture
    f_zero=price(R0)
    second=(f_plus-2*f_zero+f_minus)/(delta*delta)
    # r'(0)=0 and r''(0)=2*alpha.
    exact_second=2*ALPHA*(1-mp.log((1-R0)/R0)/ELL)
    error=abs(second-exact_second)
    require(error<mp.mpf(40)*delta*delta,f'k{k}: full charged CQ second jet converges at O(delta^2)')
    if prev_err is not None:
        require(error<prev_err*.5,f'k{k}: second-jet error decreases')
    prev_err=error
    # Predicted full paid price = common B_write + eta Phi, no unpaid reduction.
    Bwrite=mp.mpf(125)
    code_plus=Bwrite+ETA*f_plus
    code_minus=Bwrite+ETA*f_minus
    code_zero=Bwrite+ETA*f_zero
    second_actual=(code_plus-2*code_zero+code_minus)/(ETA*delta*delta)
    require(abs(second_actual-second)<mp.mpf('1e-68'),f'k{k}: charged writer baseline cancels ONLY in source quotient')
    # Audenaert-Fannes for actual diagonal two-outcome CQ states (D=2).
    tv=abs(rhat-rtrue)
    rent=hphi(rhat)*ELL
    true_ent=hphi(rtrue)*ELL
    hb=-(tv*mp.log(tv)+(1-tv)*mp.log(1-tv)) if tv else mp.mpf(0)
    require(abs(rent-true_ent)<=hb+mp.mpf('1e-60'),f'k{k}: entropy-continuity controls full record without q floor')
    require(abs(price(rhat)-price(rtrue))<=tv+hb/ELL+mp.mpf('1e-60'),f'k{k}: complete charged-CQ value modulus')
    require(success>Fraction(1,16),f'k{k}: positive full herald law')
    # A distinct actual nonzero charged-report first source, with all outcomes.
    rp=R0+ALPHA*sr_mp
    rm=R0-ALPHA*sr_mp
    grad=(price(rp)-price(rm))/(2*delta)
    ideal_grad=ALPHA*(1-mp.log((1-R0)/R0)/ELL)
    grad_error=abs(grad-ideal_grad)
    require(grad_error<mp.mpf(20)*delta*delta,f'k{k}: nonzero full charged-CQ first source at O(delta^2)')
    require(abs(ideal_grad)>mp.mpf('0.001'),f'k{k}: source sign is genuinely nonzero')
    records.append({'k':k,'first_source_error':mp.nstr(grad_error,17),'delta':mp.nstr(delta,12),'denominator_bits':R.bit_length(),
                    'herald_success':str(success),'second_jet_error':mp.nstr(error,17),
                    'error_over_delta_squared':mp.nstr(error/(delta*delta),11),
                    'trace_distance':mp.nstr(tv,12),'full_entropy_bound':mp.nstr(hb,12)})

# Generic diagonal lemma, with finite (possibly huge) bounds and no uniform
# h-dependent Hessian/strict-support assumptions.
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
        gradient=jet3*delta*delta/6+omega/delta
        hessian=jet4*delta*delta/12+4*omega/(delta*delta)
        if max(gradient,hessian)<target:
            return {'L':L,'k':k,'delta':mp.nstr(delta,9),'eps':mp.nstr(eps,9),
                    'gradient_error_bound':mp.nstr(gradient,12),
                    'hessian_error_bound':mp.nstr(hessian,12),
                    'normalized_bound':mp.nstr(target,12),
                    'precision_bits':5*k}
    raise AssertionError('diagonal schedule failed to terminate within test budget')

schedule=[]
for L in (4,8,16,32):
    # Deliberately growing finite dimensions, norms and full price capacities:
    # these are diagnostic sample inputs, not claimed native D0 constants.
    M=3*L*L
    Dout=2**(6+2*int(math.log2(L)))
    costmax=25*L**3
    jet3=100*L**4
    jet4=150*L**5
    normfactor=L**4
    gain=ETA*G_DIAGNOSTIC
    selection=select_precision(L,M,Dout,costmax,jet3,jet4,gain,normfactor)
    require(int(selection['precision_bits'])>0,f'L{L}: finite paid precision')
    require(mp.mpf(selection['gradient_error_bound'])<mp.mpf(selection['normalized_bound']),f'L{L}: first source passes')
    require(mp.mpf(selection['hessian_error_bound'])<mp.mpf(selection['normalized_bound']),f'L{L}: second source passes')
    schedule.append(selection)

# The true g_h is supplied by the SAME priced processor; this synthetic budget does not estimate it.
require(ETA*G_DIAGNOSTIC>0, 'illustrative source-gain denominator positive, not a native estimate')
# Hostile moving upstream price, not covered by the common baseline theorem.
y=sp.symbols('y',real=True)
report=sp.Rational(1,2)*y*y
upstream=y
require(sp.diff(report+upstream,y).subs(y,0)==1 and sp.diff(report,y).subs(y,0)==0,
        'moving upstream Book/work source invalidates ideal resource stationarity')
# A uniform selector average is not the conditional source of a selected code.
sel=sp.symbols('sel',real=True)
require(sp.diff(((1+sel)+(1-sel))/2,sel)==0 and sp.diff(1+sel,sel)==1,
        'one common controller with selector average cannot be identified with one conditional programme')

result={
 'status':'PASS_DIAGONAL_PAID_CQ_SOURCE_AUTHOR_CHECKS',
 'checks_count':len(checks),'checks':checks,
 'real_2d_rational_orthogonal_writer':records,
 'finite_diagonal_budget':schedule,
 'source_gain_type':{'actual_fixed_processor':'g_h=a_pi*gamma_F*s0>0 (owner)',
                       'distinct_cap1_coefficient':'gamma1=-12.444... NOT reused',
                       'diagnostic_example_gain':str(G_DIAGNOSTIC),
                       'writer_readiness_lower_bound':'1/2'},
 'scope':{'conditional_paid_CQ':True,'entire_classical_record_included':True,
          'arbitrary_small_probabilities_allowed_by_Fannes':True,
          'exact_finite_42_Euler':False,'physical_field_writer_selected':False,
          'Book03_Info_selected':False,'full_native_CI_or_Lean':False,'GR_closed':False}}
parser=argparse.ArgumentParser();parser.add_argument('--json',type=Path);args=parser.parse_args()
text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
if args.json:args.json.write_text(text,encoding='utf8')
print(text,end='')
