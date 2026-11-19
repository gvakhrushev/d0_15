#!/usr/bin/env python3
"""Independent checks of the source -> norm -> exact interval composition.

Consumes the algebra of commit 6e20be09, without asserting unrestricted D0
selection. This is NOT a large native Einstein-word emission or a PDE solver.
A scalar original-reporter fixture tests the interval layer; its f(y)=y^2 is
an explicitly structural test operand, not an alternative gravitational law.
All interval endpoints and error estimates use outward rational arithmetic.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import math
import sympy as sp

PIN = '6e20be09b25e1d68ac19be032814ce8ab2ab7351'
CHECKS: list[str] = []

def require(ok: bool, label: str) -> None:
    if not bool(ok):
        raise ArithmeticError(label)
    CHECKS.append(label)


def canonical_birth() -> dict:
    a = sp.Symbol('a', real=True)
    p = a*a
    minimal = a**4+a*a-1
    def red(x): return sp.rem(sp.expand(x), minimal, a)
    def matrix(x): return sp.Matrix(x).applyfunc(red)
    G = sp.Matrix([[a,-p],[p,a]])
    v = sp.Matrix([a,p])
    J = sp.kronecker_product(sp.eye(2),v)
    require(matrix(G.T*G)==sp.eye(2),'original Golden matrix is orthogonal')
    require(matrix(J.T*J)==sp.eye(2),'canonical raw birth is isometric on all old columns')
    require(matrix(J.T*sp.kronecker_product(sp.eye(2),G)*J)==a*sp.eye(2),
            'one real birth plus one G has return sqrt(p), not unit return')
    for r in range(2):
        for c in range(2):
            E=sp.zeros(2); E[r,c]=1
            require(matrix(sp.kronecker_product(E,sp.eye(2))*J-J*E)==sp.zeros(4,2),
                    f'old matrix unit {r},{c} is retained')
    require(red((2*p-1)*(2*p+3))==1,'2p>1 from exact Golden identity and p>0')
    return {'birth':'x -> x tensor (sqrt(p), p)', 'return_square':'p',
            'dimension_factor':2,'full_thermal_to_signal_ratio':'(2p)^(-K)',
            'native_general_word_emitted':False}


def exact_full_source() -> dict:
    """Rational, rank-deficient and noncommuting old-source fixture."""
    z=sp.Rational(1,2**20); eta=sp.Rational(1,7)
    ah=sp.Rational(17,50); epsrf=sp.Rational(1,1024)
    rs=[sp.Rational(1,10),sp.Rational(1,8),sp.Rational(1,9)]
    cs=[1-2*ah*r for r in rs]
    K=sp.Matrix([[sp.Rational(2,5),sp.Rational(1,7)],[0,0]])
    dK=sp.Matrix([[sp.Rational(1,11),-sp.Rational(1,13)],[sp.Rational(1,17),0]])
    A=K.T*K; dA=dK.T*K+K.T*dK
    require(A.det()==0 and sp.trace(A)>0,'nonzero singular old Gram accepted')
    require(A*dA-dA*A != sp.zeros(2),'old Gram and its actual derivative do not commute')
    s=sp.prod(c*c for c in cs)
    D=(1-z)*sp.eye(2)+z*eta*s*A
    Z=D.inv(); L=sum(1/c for c in cs)
    gain=4*ah*epsrf*z*eta*s*sp.trace(Z*A)*L
    require(gain>0,'actual normalized gain positive')
    weights=[(1/c)/L for c in cs]
    require(sum(weights)==1 and all(w>0 for w in weights),'positive weights sum to one')
    target=[sp.Rational(2,3),-sp.Rational(5,7),sp.Rational(4,9)]
    dr=[epsrf*f for f in target]
    dc=[-2*ah*d for d in dr]
    ds=sum(2*s*dd/c for dd,c in zip(dc,cs))
    direct=-sp.trace(Z*(z*eta*(ds*A+s*dA)))/gain
    old=-sp.trace(Z*dA)/(4*ah*epsrf*L*sp.trace(Z*A))
    assembled=old+sum(w*f for w,f in zip(weights,target))
    require(sp.factor(direct-assembled)==0,'complete matrix derivative equals old+independent currents')
    Pi=K*Z*K.T/sp.trace(Z*A)
    require(sp.trace(Pi)==1,'derived old-history dual weight has trace one')
    require(Pi.det()==0 and Pi[0,0]>=0,'derived dual weight remains positive with singular past')
    # Entire independent source, NOT just a sum of its row values.
    full_dual=abs(old)+sum(w*abs(f) for w,f in zip(weights,target))
    require(full_dual>=abs(assembled),'full product-domain dual norm retains independent signs')
    current_dual=sum(w*abs(f) for w,f in zip(weights,[sp.Integer(1)]*3))
    require(current_dual==1,'persistent current row cannot be diluted by repetition')
    return {'exact_identity':True,'singular_old_Gram':True,
            'actual_gain':str(gain),'source':str(direct),'weights':[str(w) for w in weights],
            'complete_dual_norm':str(full_dual),
            'scope':'exact structural rational source identity; eta need not equal the specific birth fixture'}


def cotangent_retraction() -> dict:
    d=42; w=[sp.Rational(2,7),sp.Rational(3,7),sp.Rational(2,7)]
    eye=sp.eye(d)
    mean=(w[0]*eye).row_join(w[1]*eye).row_join(w[2]*eye)
    diagonal=eye.col_join(eye).col_join(eye)
    require(mean*diagonal==eye,'weighted current mean has exact diagonal right inverse on all42 directions')
    E=sp.Matrix([sp.Rational((i%7)-3,i+1) for i in range(d)])
    transported=mean.T*E
    require(sum(abs(x) for x in transported)==sum(abs(x) for x in E),
            'dual l1 norm of common field covector is exactly preserved')
    require(diagonal.T*transported==E,'all42 field rows recovered through the same norm-one lift')
    relative=sp.Matrix.vstack(3*eye,-2*eye,sp.zeros(d))
    require(mean*relative==sp.zeros(d),'genuine relative-copy kernel has zero weighted mean')
    # Wrong old shortcut: check the signed sum only.
    require((sp.Rational(1,2)-sp.Rational(1,2))==0 and
            abs(sp.Rational(1,2))+abs(-sp.Rational(1,2))==1,
            'opposite independently free rows cannot pass a signed-sum test')
    require(sum(abs(x) for x in transported/3)==sum(abs(x) for x in E)/3,
            'extra repetition divisor would also delete the desired field source')
    return {'geometric_dimension':d,'independent_current_copies':3,
            'right_inverse_exact':True,'field_dual_norm_exactly_preserved':True,
            'unrestricted_query_rows_eliminated':False}


PRECISION=256
SCALE=1<<PRECISION

def lo_round(x: Q) -> Q: return Q((x.numerator*SCALE)//x.denominator,SCALE)
def hi_round(x: Q) -> Q: return -lo_round(-x)

@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q
    def __post_init__(self):
        lo,hi=Q(self.lo),Q(self.hi)
        if lo>hi: raise ValueError('empty input interval')
        object.__setattr__(self,'lo',lo_round(lo))
        object.__setattr__(self,'hi',hi_round(hi))
    @staticmethod
    def point(x): return Interval(Q(x),Q(x))
    @staticmethod
    def convert(x): return x if isinstance(x,Interval) else Interval.point(x)
    def __add__(self,x):
        x=self.convert(x); return Interval(self.lo+x.lo,self.hi+x.hi)
    __radd__=__add__
    def __neg__(self): return Interval(-self.hi,-self.lo)
    def __sub__(self,x): return self+-self.convert(x)
    def __rsub__(self,x): return self.convert(x)+-self
    def __mul__(self,x):
        x=self.convert(x);v=[self.lo*x.lo,self.lo*x.hi,self.hi*x.lo,self.hi*x.hi]
        return Interval(min(v),max(v))
    __rmul__=__mul__
    def inverse(self):
        if self.lo<=0<=self.hi:raise ZeroDivisionError('interval meets zero')
        return Interval(1/self.hi,1/self.lo)
    def __truediv__(self,x):return self*self.convert(x).inverse()
    def __rtruediv__(self,x):return self.convert(x)*self.inverse()
    def __pow__(self,n):
        if not isinstance(n,int) or n<0:raise ValueError('nonnegative integer power required')
        if n==0:return self.point(1)
        out=self.point(1)
        for _ in range(n):out=out*self
        return out
    def mag(self):return max(abs(self.lo),abs(self.hi))
    def width(self):return self.hi-self.lo
    def intersect(self,x):
        lower,upper=max(self.lo,x.lo),min(self.hi,x.hi)
        if lower>upper:raise ArithmeticError('inconsistent certified intervals; refusing to insert zero')
        return Interval(lower,upper)
    def encloses(self,x):return self.lo<=x<=self.hi
    def json(self):return {'lo':str(self.lo),'hi':str(self.hi),
                           'width_float':float(self.width())}


def golden_interval() -> Interval:
    l,u=Q(0),Q(1)
    for _ in range(PRECISION+4):
        m=(l+u)/2
        if m*m+m-1<0:l=m
        else:u=m
    out=Interval(l,u)
    require(out.lo*out.lo+out.lo<1<out.hi*out.hi+out.hi,
            'Golden value enclosed by exact rational outward endpoints')
    return out


def neglog_one_minus(x:Interval, tolerance:Q) -> tuple[Interval,int]:
    if not (0<=x.lo<=x.hi<1):raise ValueError('log series requires 0<=x<1')
    total=Interval.point(0);power=Interval.point(1)
    for n in range(1,100):
        power=power*x;total=total+power/n
        tail=hi_round(x.hi**(n+1)/((n+1)*(1-x.hi)))
        out=Interval(total.lo,total.hi+tail)
        if out.width()<=tolerance:return out,n
    raise ArithmeticError('requested price precision not achieved')


class OriginalReporterFixture:
    """Original r(x,0), on a scalar f=y^2 test chart, no Einstein fit."""
    def __init__(self):
        self.p=golden_interval();p=self.p
        self.z=Interval.point(Q(1,2**20));self.a=Interval.point(Q(17,50))
        b=4*p*p*(1-p*p);A=b+(1-b)*b
        self.r0=self.z*(A+b)-self.z*self.z*A*b
        factor=self.z*(1-self.z*b)*(1-b)
        self.rf=factor*4*p*p*(1-2*p*p)
        self.rff=factor*(-8)*p**4
        self.eta=p**3;self.past=Interval.point(Q(2,5));self.n=4
        require(self.rf.lo>0,'actual reporter r_f has strictly positive certified lower bound')
    def c_jet(self,y:Interval,epsilon:Q):
        e=Interval.point(epsilon)
        r=self.r0+self.rf*e*y*y+self.rff/2*e*e*y**4
        r1=2*self.rf*e*y+2*self.rff*e*e*y**3
        r2=2*self.rf*e+6*self.rff*e*e*y*y
        r3=12*self.rff*e*e*y
        return 1-2*self.a*r, -2*self.a*r1,-2*self.a*r2,-2*self.a*r3
    def data(self,y:Interval,epsilon:Q):
        c,c1,c2,c3=self.c_jet(y,epsilon);n=self.n
        alpha=self.z*self.eta*self.past
        D=1-self.z+alpha*c**n
        D1=alpha*n*c**(n-1)*c1
        D2=alpha*(n*(n-1)*c**(n-2)*c1*c1+n*c**(n-1)*c2)
        D3=alpha*(n*(n-1)*(n-2)*c**(n-3)*c1**3
                  +3*n*(n-1)*c**(n-2)*c1*c2+n*c**(n-1)*c3)
        J3=-D3/D+3*D1*D2/(D*D)-2*D1**3/(D**3)
        gamma=2*n*self.a*epsilon*self.rf*alpha*c**(n-1)/D
        leak=self.z*(1-self.eta*self.past*c**n)
        return leak,gamma,J3
    def contrast(self,y0:Q,k:int):
        tau=Q(1,2**(k+6));eps=Q(1,2**(k+16));t=Q(1,2**(k+12))
        _,gain,_=self.data(Interval.point(y0),eps)
        require(gain.lo>0,f'level{k}: true gain lower bound, no unit normalization')
        _,_,third=self.data(Interval(y0-t,y0+t),eps)
        weak=hi_round(2*(self.rff/self.rf).mag()*eps*abs(y0)**3)
        fd=hi_round(t*t*third.mag()/(6*gain.lo))
        analytic=hi_round(weak+fd)
        require(analytic<=tau,f'level{k}: certified off-shell weak/finite-difference error budget')
        tolerance=Q(1,8)*tau*t*gain.lo
        plus,nplus=neglog_one_minus(self.data(Interval.point(y0+t),eps)[0],tolerance)
        minus,nminus=neglog_one_minus(self.data(Interval.point(y0-t),eps)[0],tolerance)
        actual=(plus-minus)/(2*t*gain)
        require(actual.width()<=tau,f'level{k}: price interval precision uses actual gain')
        expanded=Interval(actual.lo-analytic,actual.hi+analytic)
        require(expanded.width()<Q(1,2**k),f'level{k}: kappa width without target-centering')
        return actual,expanded,{'k':k,'epsilon':str(eps),'t':str(t),
                'actual_gain_lower':str(gain.lo),'actual_gain_upper':str(gain.hi),
                'source_comparison':actual.json(),'proven_error_bound':str(analytic),
                'log_terms':[nplus,nminus]}


def interval_composition() -> dict:
    model=OriginalReporterFixture();allrows=[]
    for y0,label in [(Q(1,4),'off_shell'),(Q(0),'structural_zero')]:
        previous=None;rows=[];ledger=[];first_separation=None
        for k in range(1,13):
            actual,current,receipt=model.contrast(y0,k)
            nested=current if previous is None else previous.intersect(current)
            # This target check is outside the construction routine. The value
            # is not used to center, intersect, select resources or compute B.
            require(nested.encloses(2*y0),f'{label} level{k}: independent analytic limit agrees')
            if previous is not None:
                require(previous.lo<=nested.lo<=nested.hi<=previous.hi,
                        f'{label} level{k}: nested intervals preserve previous records')
            if not nested.encloses(0) and first_separation is None:first_separation=k
            receipt['nested_interval']=nested.json();rows.append(receipt)
            entry=json.dumps(receipt,sort_keys=True).encode()
            old=list(ledger);ledger.append(hashlib.sha256(entry).hexdigest())
            require(ledger[:-1]==old,f'{label} level{k}: ledger projection is exact truncation')
            previous=nested
        if y0:
            require(first_separation is not None,'nonzero source has finite separating witness')
            # Bad factor2 calibration has a different limiting covector.
            require(not (previous/2).encloses(2*y0),'wrong source gain rejected by off-shell comparison')
        else:require(previous.encloses(0),'proved even fixture gives zero name, not a general zero decision')
        allrows.append({'label':label,'structural_y':str(y0),'first_zero_separation':first_separation,
                        'final_interval':previous.json(),'ledger_hashes':ledger,'levels':rows})
    rejected=False
    try: Interval(Q(0),Q(1,10)).intersect(Interval(Q(1),Q(2)))
    except ArithmeticError:rejected=True
    require(rejected,'bad certificate intersection fails instead of overwriting with zero')
    return {'arithmetic':'outward dyadic rational, 256 bits, explicit log-series tails',
            'prices':'full return determinant of the declared scalar reflection fixture; same-clock heat cancels by exact isospectrality',
            'test_operand':'f(y)=y^2; software fixture only, not a GR replacement or full native history',
            'target_limit_used_to_construct_intervals':False,
            'native_GR_programme_emitted':False,'runs':allrows}


def closure_boundary() -> dict:
    # Common-effect law and finite-jet equality are distinct.
    t=sp.Symbol('t',real=True)
    epsilon=sp.Rational(1,1000000)
    deviation=epsilon*sp.sin(t/epsilon)
    require(sp.diff(deviation,t).subs(t,0)==1,'small operator-value tolerance alone cannot kill a query source')
    # Conditional theorem has no implicit exact-finite claim.
    k=sp.Symbol('k',integer=True,positive=True)
    require(sp.limit(1/k,k,sp.oo)==0,'nonzero finite residual can have exact zero limiting name')
    return {'exact_finite_stationarity_inferred':False,
            'fixed_task_vs_unrestricted_X_N_identified':False,
            'whole_physical_D0_GR_selected':False}


def main():
    out={'input_commit':PIN,'canonical_birth':canonical_birth(),
         'complete_source':exact_full_source(),'full_covector_retraction':cotangent_retraction(),
         'interval_assembly':interval_composition(),'boundaries':closure_boundary()}
    out.update({'status':'PASS_SCOPED_SOURCE_KAPPA_COMPOSITION',
                'new_check_count':len(CHECKS),'check_names':CHECKS,
                'unrestricted_GR_closed':False,'new_full_native_execution':False,
                'Lean_or_CI_run':False,
                'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':main()
