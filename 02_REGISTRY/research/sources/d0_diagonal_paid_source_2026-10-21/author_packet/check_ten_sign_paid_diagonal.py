#!/usr/bin/env python3
"""Full 1024-sign native Golden two-band report and finite rational paid secants.

Reconstructs the exact ten-sign report polynomial of the published fixed
processor. Tests all 1024 strictly positive conditional branches, the actual
unconditional report, two material orientations, and the first/second price
secants of finite rational input qubits. Signs are COHERENT/unread work:
this script sums over their Born basis probabilities only, and the CQ entropy
counts the final report, not 1024 spurious measured sign labels.

Not a new all42/moving-field-input/Book03 realization.
"""
from __future__ import annotations
import itertools,json,argparse
from pathlib import Path
import mpmath as mp
from fractions import Fraction

mp.mp.dps=65
phi=(1+mp.sqrt(5))/2
p=1/phi
ell=mp.log(phi)
z=mp.mpf(1)/2**20
eps=mp.mpf(1)/64
checks=[]
def require(v,label):
    if not bool(v):raise AssertionError(label)
    checks.append(label)
def plus(*polys):
    out={}
    for poly in polys:
        for k,v in poly.items():out[k]=out.get(k,mp.mpf(0))+v
    return {k:v for k,v in out.items() if v}
def scale(poly,k):return {a:v*k for a,v in poly.items()}
def times(a,b):
    out={}
    for (i,j),v in a.items():
        for (k,l),w in b.items():out[(i+k,j+l)]=out.get((i+k,j+l),mp.mpf(0))+v*w
    return {k:v for k,v in out.items() if v}
ONE={(0,0):mp.mpf(1)}
X={(1,0):mp.mpf(1)}
Y={(0,1):mp.mpf(1)}
def report_poly(sigma):
    E=plus(scale(ONE,p**2),scale(X,p**2*eps))
    u=plus(scale(ONE,p),scale(Y,mp.mpf(sigma)*p**2*eps))
    B=plus(scale(times(u,u),4),scale(times(times(u,u),times(u,u)),-4))
    L=plus(scale(E,4),scale(times(E,E),-4))
    A=plus(L,times(plus(ONE,scale(L,-1)),B))
    return plus(scale(B,z),scale(A,z),scale(times(B,A),-z*z))

def direct_report(s,t,sigma):
    E=p**2*(1+eps*s)
    u=p+sigma*p**2*eps*t
    B=4*u*u*(1-u*u)
    l=4*E*(1-E)
    A=l+(1-l)*B
    return 1-(1-z*B)*(1-z*A)

def hphi(r):return -(r*mp.log(r)+(1-r)*mp.log(1-r))/ell

def beta(c,signs):
    S1,S2=signs[:2]
    Ts=signs[2:]
    b=mp.mpf(0)
    for (a,k),v in c.items():
        pp=(S1 if a>=1 else 1)*(S2 if a>=2 else 1)
        for j in range(k):pp*=Ts[j]
        b+=v*pp
    return b

coeff_plus=report_poly(1)
coeff_minus=report_poly(-1)
require(len(coeff_plus)<=27 and max(k[0] for k in coeff_plus)==2 and max(k[1] for k in coeff_plus)==8,
        'exact two-band 2 by 8 polynomial support')
require(abs(sum(coeff_plus.values())-direct_report(1,1,1))<mp.mpf('1e-55'),
        'polynomial equals literal original nonlinear response at s=t=1')
require(abs(sum(coeff_minus.values())-direct_report(1,1,-1))<mp.mpf('1e-55'),
        'opposite original material orientation')
require(abs(coeff_plus[(0,1)]+coeff_minus[(0,1)])<mp.mpf('1e-55'),
        'original matter orientation is an odd source')
require(coeff_plus[(0,1)]!=0,'genuine nonzero material source')
Q=1-z*4*p**3
R0=1-z*4*p**3*(1+p**6)
require(abs(coeff_plus[(0,1)]/coeff_plus[(1,0)]-2*p**(-5)*(R0/Q+p**6))<mp.mpf('1e-50'),
        'original exact positive material/source ratio')
require(abs(coeff_plus[(1,0)]-4*z*(1-z*4*p**3)*p**11/64)<mp.mpf('1e-55'),
        'owned Golden coframe coefficient 4zQp11/64')
all_signs=list(itertools.product((1,-1),repeat=10))
bs=[beta(coeff_plus,seq) for seq in all_signs]
require(len(bs)==1024,'whole actual ten-sign conditional alphabet retained')
require(min(bs)>0 and max(bs)<1,'all1024 Golden conditional reports strictly positive')
for seq,v in zip(all_signs,bs):
    require(0<v<1,'actual sign-conditioned report and complement positive')
# Group all T signs: no premature sign-record entropy.
rows={}
for (S1,S2) in itertools.product((1,-1),repeat=2):
    observed=sum(v for seq,v in zip(all_signs,bs) if seq[0]==S1 and seq[1]==S2)/256
    expected=coeff_plus[(0,0)]+coeff_plus[(1,0)]*S1+coeff_plus[(2,0)]*S1*S2
    require(abs(observed-expected)<mp.mpf('1e-51'),f'coherent T marginals exact at signs {S1},{S2}')
    rows[(S1,S2)]=observed
r0=direct_report(0,0,1)
require(abs(r0-coeff_plus[(0,0)])<mp.mpf('1e-50'),'original zero-source r0')
require(r0>0 and r0<1,'report entropy smooth along real two-band source')

def encoded_mean(s,k):
    # PHYSICAL rational R(theta) on |0>: the Z-sign mean is cos(2 theta),
    # not the matrix diagonal cos(theta). Approximate tan(theta/2).
    M=1<<(5*k)
    target=mp.tan(mp.acos(s)/4)
    m=int(mp.nint(M*target))
    den=M*M+m*m
    cos=Fraction(M*M-m*m,den)
    sn=Fraction(2*M*m,den)
    assert cos*cos+sn*sn==1
    mean=cos*cos-sn*sn
    return mp.mpf(mean.numerator)/mean.denominator,mean,den

def from_complete_signs(s):
    total=mp.mpf(0)
    for (S1,S2),val in rows.items():
        total+=val*(1+S1*s)*(1+S2*s)/4
    return total

def price(r):return mp.mpf(125)-mp.mpf('.55')*hphi(r)
records=[]
for k in (4,5,6,7,8):
    delta=mp.mpf(2)**(-k)
    splus,qplus,denplus=encoded_mean(delta,k)
    sminus,qminus,denminus=encoded_mean(-delta,k)
    # Common denominator for all three paid writer codes; same herald law.
    s0,q0,den0=encoded_mean(mp.mpf(0),k)
    R=denplus*denminus*den0
    B=1<<(R-1).bit_length()
    success=Fraction(R,2*B)**2
    require(Fraction(1,16)<success<=Fraction(1,4),f'k{k}: finite common-herald law')
    require(abs(splus-delta)<mp.mpf(3)/2**(5*k),f'k{k}: positive rational source-moment accuracy')
    require(abs(sminus+delta)<mp.mpf(3)/2**(5*k),f'k{k}: negative rational source-moment accuracy')
    q1=from_complete_signs(splus)
    q2=from_complete_signs(sminus)
    q0r=from_complete_signs(s0)
    require(abs(q1-direct_report(splus,0,1))<mp.mpf('1e-49'),f'k{k}: complete1024 positive report matches original nonlinear r')
    require(abs(q2-direct_report(sminus,0,1))<mp.mpf('1e-49'),f'k{k}: opposite sign complete report')
    grad=(price(q1)-price(q2))/(2*delta)
    grad_true=-mp.mpf('.55')*mp.diff(hphi,r0)*coeff_plus[(1,0)]
    require(abs(grad-grad_true)<abs(grad_true)*delta*delta*10,f'k{k}: paid ten-sign first source O(delta2)')
    second=(price(q1)-2*price(q0r)+price(q2))/(delta*delta)
    sec_true=-mp.mpf('.55')*(mp.diff(hphi,r0,2)*coeff_plus[(1,0)]**2 +
                           mp.diff(hphi,r0)*2*coeff_plus[(2,0)])
    require(abs(second-sec_true)<abs(sec_true)*delta*delta*50,f'k{k}: paid ten-sign full CQ Hessian O(delta2)')
    records.append({'k':k,'delta':mp.nstr(delta,12),'uniform_herald_success':str(success),
                    'common_denominator_bits':R.bit_length(),'central_source_approx':mp.nstr(s0,10),'source_error':mp.nstr(abs(grad-grad_true),15),
                    'hessian_error':mp.nstr(abs(second-sec_true),15)})
result={'status':'PASS_ORIGINAL_GOLDEN_TEN_SIGN_PAID_CQ_DIAGONAL_AUTHOR_CHECK',
        'checks_count':len(checks),'checks':checks,
        'r0':mp.nstr(r0,25),'conditional_beta_min':mp.nstr(min(bs),25),
        'conditional_beta_max':mp.nstr(max(bs),25),
        'real_field_source_coefficient':mp.nstr(coeff_plus[(1,0)],25),
        'orientation_odd_material_source_coefficient':mp.nstr(coeff_plus[(0,1)],25),
        'stencil':records,'scope':{'all1024_signs_coherently_unmeasured':True,
          'two_original_source_moments':True,'distinct_code_secants_not_native_Euler':True,
          'source_gain_is_fixed_ten_sign_only':True,'actual_full42_replay':False,
          'Book03_Info_selected':False,'GR_closed':False}}
parser=argparse.ArgumentParser();parser.add_argument('--json',type=Path)
args=parser.parse_args()
payload=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
if args.json:args.json.write_text(payload,encoding='utf-8')
print(payload,end='')
