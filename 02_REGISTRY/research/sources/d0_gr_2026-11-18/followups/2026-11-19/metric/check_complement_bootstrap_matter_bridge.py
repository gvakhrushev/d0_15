"""Conditional finite algebra: actual native writer RAW vs independent CAR moment.

Uses the separately verified full-cut word and its full two-Hodge bound;
this is not a compiled physical 16-copy Hq/Choi clock or Book03 price.
"""
import json
import math
import subprocess
import sys
from itertools import product
from pathlib import Path
import numpy as np
import sympy as sp
from mpmath import iv
from check_source_price import need


def main():
    p=(math.sqrt(5)-1)/2;a=math.sqrt(p);A=p*math.sin(712*math.asin(p))
    need(A>0,'actual owner signed amplitude')
    # Consume the complete separately retained input/NC1/CX+SourceI replay.
    argv=[sys.executable,'-B','-W','error',str(Path(__file__).with_name('check_complement_bootstrap_cancellation.py'))]
    receipt=json.loads(subprocess.check_output(argv,text=True))
    need(receipt['old_input_rank']==16 and not receipt['GR_closed'],'actual writer owner checked')
    s,t,d,gp,gm=sp.symbols('s t d gp gm',real=True)
    B=lambda x:(1-x)**2+x**2
    Q=sp.expand(-(B(s)-s*s)*B(t)-t*t*B(s))
    Qp=sp.expand(Q.subs({s:sp.Rational(1,2)+d,t:sp.Rational(1,2)}))
    Qm=sp.expand(Q.subs({s:sp.Rational(1,2)-d,t:sp.Rational(1,2)}))
    need(Qp==-sp.Rational(1,4)+d/2-d*d,'exact plus independent two-copy moment')
    need(Qm==-sp.Rational(1,4)-d/2-d*d,'exact minus independent two-copy moment')
    need(sp.simplify((gp*Qp-gm*Qm)/(2*d)-((gp+gm)/4+(-sp.Rational(1,4)-d*d)*(gp-gm)/(2*d)))==0,
         'all terms for independently moving gain')
    coords=list(product(range(4),repeat=4));idx={y:i for i,y in enumerate(coords)}
    fields={}
    for u,v in product((0,1),repeat=2):
        fields[u,v]=np.array([[A*round(math.cos(math.pi/2*(y[1]+u*y[0]+v*y[2]))),
                               A*round(math.sin(math.pi/2*(y[1]+u*y[0]+v*y[2])))] for y in coords])
    def physical_moment(sv,tv):
        # Linear field extraction for each copy; bilinearity gives q(E psi)
        # only when two entire CAR/Fourier/descriptor copies are independent.
        mean=sum(((sv if u else 1-sv)*(tv if v else 1-tv))*fields[u,v]
                 for u,v in product((0,1),repeat=2))
        out=[]
        for y in coords:
            val=0.
            for r in range(4):
                yn=list(y);yn[r]=(yn[r]+1)%4
                dpsi=(mean[idx[tuple(yn)]]-mean[idx[y]])/.25
                val+=(1 if r==0 else -1)*float(dpsi@dpsi)/16
            out.append(val)
        return float(np.mean(out))
    iv.dps=70;pv=(iv.sqrt(5)-1)/2;av=iv.sqrt(pv);theta=iv.atan2(pv,av)
    Av=pv*iv.sin(712*theta);beta=2*pv**2;z=iv.mpf(1)/(2**20)
    c=pv**3*(1+av);w=av*pv**2
    def J(x):
        v0=w*((av+pv)*iv.cos(x)+(av-pv)*iv.sin(x))
        v1=w*((av+pv)*iv.cos(x)-(av-pv)*iv.sin(x))
        return -8*(iv.log(1-z*(1-v0*v0))+iv.log(1-z*(1-v1*v1)))
    checks=[]
    for item in receipt['actual_finite_word_checks']:
        q=int(item['q']);turn=int(item['turn']);epsilon=q*theta-2*iv.pi*turn
        dv=av*pv*iv.sin(2*epsilon);dd=float(dv.mid);ds=2*dd
        x=physical_moment(.5+dd,.5);y=physical_moment(.5-dd,.5)
        need(abs((x-y)/ds-A*A)<1e-13,'full 256-site independent matter secant')
        need(abs(float((J(epsilon)-J(-epsilon)).mid))<1e-60,'exact exchanged-block full RAW')
        # Demonstrate the moving-gain term; this is only a symbolic test case.
        gpnum,gmnum=2.0,3.0
        lhs=(gpnum*x-gmnum*y)/ds
        rhs=A*A*((gpnum+gmnum)/2+2*(-.25-dd*dd)*(gpnum-gmnum)/ds)
        need(abs(lhs-rhs)<1e-12,'moving gain product rule')
        checks.append({'q':q,'turn':turn,'delta_s':ds,
                       'qphysical_plus':x,'qphysical_minus':y,
                       'qphysical_secant_per_descriptor':(x-y)/ds,
                       'claimed_target_gain_is_physically_selected':False})
    out={'status':'PASS: conditional exact local bootstrap vs independent 2-copy CAR algebra',
         'local_raw_J_secant_per_descriptor':0,
         'matter_actual_factor': '2*A_star^2; original uncalibrated divide by a_star',
         'A_star':A,'matter_secant':A*A,
         'independent_matter_copies_required':2,
         'target_real_gain_sign_and_normalization_selected':False,
         'complete_same_history_matters_compiled':False,
         'full_combined_bootstrap_computed':False,
         'full_Hodge_continuation_requires_paid_padding':True,
         'GR_closed':False,'finite_checks':checks}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
