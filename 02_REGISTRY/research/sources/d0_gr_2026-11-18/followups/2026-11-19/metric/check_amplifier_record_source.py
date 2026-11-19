"""Amplification readiness source: exact recurrences and retained flags.

Numerics are high-precision evaluations of exact rational amplification
polynomials.  These are scoped recorded code-minus-CQ operands, not Book Info.
"""
from fractions import Fraction as F
from itertools import product
import json
import mpmath as mp
import sympy as sp

mp.mp.dps=100
p=(mp.sqrt(5)-1)/2
ell=mp.log(1/p)


def poly(a,j):
    g=b=F(1); dg=db=F(0)
    for _ in range(j):
        ng=(1-2*a)*g+2*(1-a)*b
        nb=-2*a*g+(1-2*a)*b
        ndg=-2*g+(1-2*a)*dg-2*b+2*(1-a)*db
        ndb=-2*g-2*a*dg-2*b+(1-2*a)*db
        g,b,dg,db=ng,nb,ndg,ndb
    prob=a*g*g
    deriv=g*g+2*a*g*dg
    assert prob+(1-a)*b*b==1
    return prob,deriv


def m(x):return mp.mpf(x.numerator)/x.denominator

def entropy(q):return -q*mp.log(q)-(1-q)*mp.log1p(-q)

def cost(q):return 1+q-entropy(q)/ell

def slope(q):return 1+mp.log(q/(1-q))/ell

def exact_record(c,gamma,j):
    a=c*gamma;qr,dqr=poly(a,j)
    q=m(qr); dq=m(c*dqr)
    theta=mp.asin(mp.sqrt(m(a)))
    assert abs(mp.sin((2*j+1)*theta)**2-q)<mp.mpf('1e-95')
    assert abs((2*j+1)*mp.sin(2*(2*j+1)*theta)/(2*mp.sqrt(m(a)*(1-m(a))))-m(dqr))<mp.mpf('1e-90')
    assert q>=1-m(a)
    bound=(2*j+1)*m(c)*(1+mp.log((1-m(a))/m(a))/ell)
    assert abs(slope(q)*dq)<bound
    return q,dq,cost(q),slope(q)*dq,bound


def stopped(records):
    reach=mp.mpf(1);drF=mp.mpf(0);drJ=mp.mpf(0)
    total=mp.mpf(0);dF=mp.mpf(0);dJ=mp.mpf(0)
    for q,dqf,dqj,f,df,dj in records:
        total+=reach*f;dF+=drF*f+reach*df;dJ+=drJ*f+reach*dj
        drF,drJ=drF*q+reach*dqf,drJ*q+reach*dqj
        reach*=q
    return total,dF,dJ,reach


def main():
    # Golden entropy for a scalar retained two-branch instrument.
    assert sp.simplify(((-1+sp.sqrt(5))/2)**2+(-1+sp.sqrt(5))/2-1)==0
    # A fixed-rate scalar-effect instrument remains scalar on old states,
    # even with entangled oldRIGHT, since the success effect is q I.
    q=sp.Rational(3,7); K0=sp.sqrt(1-q)*sp.eye(4)
    swap=sp.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    K1=sp.sqrt(q)*swap
    assert K0.T*K0==(1-q)*sp.eye(4) and K1.T*K1==q*sp.eye(4)
    for n in range(1,5):
        s=sum((q**sum(bits))*(1-q)**(n-sum(bits)) for bits in product((0,1),repeat=n))
        assert s==1
    # Published sample values are hypothetical raw seed probabilities.
    qF,dqF,fF,dfF,bF=exact_record(F(1,256),F(1,4),25)
    qJ,dqJ,fJ,dfJ,bJ=exact_record(F(21,2049),F(1,9),23)
    Q=[(qF,dqF,mp.mpf(0),fF,dfF,mp.mpf(0))]*80 + [(qJ,mp.mpf(0),dqJ,fJ,mp.mpf(0),dfJ)]*180
    total,dF,dJ,success=stopped(Q)
    all_total=80*fF+180*fJ
    # Independently differentiate full stopped formula with fixed j.
    def evaluated(gf,gj):
        af=gf/256; aj=gj*mp.mpf(21)/2049
        qf=mp.sin(51*mp.asin(mp.sqrt(af)))**2
        qj=mp.sin(47*mp.asin(mp.sqrt(aj)))**2
        reach=mp.mpf(1); total=mp.mpf(0)
        for v in [qf]*80+[qj]*180:
            total+=reach*cost(v);reach*=v
        return total
    numF=mp.diff(lambda t:evaluated(t,mp.mpf(1)/9),mp.mpf(1)/4)
    numJ=mp.diff(lambda t:evaluated(mp.mpf(1)/4,t),mp.mpf(1)/9)
    assert abs(dF-numF)<mp.mpf('1e-75') and abs(dJ-numJ)<mp.mpf('1e-75')
    assert abs(success-mp.mpf('0.9170139265807568526114826078090785699732634633133951417728'))<mp.mpf('1e-56')
    # At exact amplitude peak the derivative of the composed f(P_j) tends
    # to zero despite f' itself diverging, since 1-P_j is quadratic.
    a=sp.symbols('a', positive=True)
    q_peak=sp.expand(a*(3-4*a)**2)
    assert sp.simplify(q_peak.subs(a,sp.Rational(1,4))-1)==0
    assert sp.simplify(sp.diff(q_peak,a).subs(a,sp.Rational(1,4)))==0
    def s(x):return mp.nstr(x,28)
    print(json.dumps({
      'status':'PASS','GR_closed':False,
      'scope':'conditional scalar effects, full retained branch isometries, actual orthogonal coarse flag; code-CQ is not Book03 Info',
      'gamma_F_test':'1/4','gamma_J_test':'1/9','iterations_F':25,'iterations_J':23,
      'q_F':s(qF),'q_J':s(qJ),'bank_success':s(success),
      'single_flag_source_F_dgamma':s(dfF),'single_flag_source_J_dgamma':s(dfJ),
      'single_flag_abs_bound_F':s(bF),'single_flag_abs_bound_J':s(bJ),
      'all_flags_code_CQ':s(all_total),'all_flags_slope_gamma_F':s(80*dfF),'all_flags_slope_gamma_J':s(180*dfJ),
      'first_failure_code_CQ':s(total),'first_failure_slope_gamma_F':s(dF),'first_failure_slope_gamma_J':s(dJ),
      'constant_scalar_gamma_coarse_flag_source_exactly_zero':True,
      'full_fine_flag_cost_and_independent_rows_selected':False,
      'physical_book_cost_info_bound_and_lift_proved':False
    },indent=2,ensure_ascii=False))

if __name__=='__main__':main()
