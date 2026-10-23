#!/usr/bin/env python3
"""Outward evaluation of the normalized marked HJR source on the OWNED root.

The root existence proof is inherited, not rerun. Every original L8 Fourier
mode and every CAR grade is retained. New calculations evaluate the altered
full stack source on the ENTIRE inherited radius-1e-12 enclosure.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from decimal import Decimal,Context,ROUND_FLOOR,ROUND_CEILING

def require(c,m):
    if not bool(c): raise ArithmeticError(m)

# Outward Decimal intervals. Operations explicitly round both endpoints.
PREC = 85
LO = Context(prec=PREC, rounding=ROUND_FLOOR)
HI = Context(prec=PREC, rounding=ROUND_CEILING)

class I:
    def __init__(self, lo, hi=None):
        self.lo = lo if isinstance(lo,Decimal) else Decimal(str(lo))
        self.hi = self.lo if hi is None else (hi if isinstance(hi,Decimal) else Decimal(str(hi)))
        if self.lo > self.hi:
            raise ValueError('reversed interval')
    @staticmethod
    def lift(x):
        return x if isinstance(x,I) else I(x)
    def __add__(self, other):
        b=I.lift(other)
        return I(LO.add(self.lo,b.lo), HI.add(self.hi,b.hi))
    __radd__=__add__
    def __neg__(self):
        return I(self.hi.copy_negate(), self.lo.copy_negate())
    def __sub__(self, other):
        return self + (-I.lift(other))
    def __rsub__(self, other):
        return I.lift(other) + (-self)
    def __mul__(self, other):
        b=I.lift(other)
        pairs=list(itertools.product([self.lo,self.hi],[b.lo,b.hi]))
        return I(min(LO.multiply(a,c) for a,c in pairs),
                 max(HI.multiply(a,c) for a,c in pairs))
    __rmul__=__mul__
    def __truediv__(self, other):
        b=I.lift(other)
        if b.lo <= 0 <= b.hi:
            raise ZeroDivisionError('interval contains zero')
        inv=I(LO.divide(Decimal(1),b.hi), HI.divide(Decimal(1),b.lo))
        return self*inv
    def __rtruediv__(self, other):
        return I.lift(other)/self
    def __pow__(self, n):
        if not isinstance(n,int) or n<0:
            raise ValueError('nonnegative integer power required')
        out=I(1); b=self
        while n:
            if n&1: out=out*b
            b=b*b; n//=2
        return out
    def bounds(self):
        return [str(self.lo),str(self.hi)]

def sqrt_interval(n: int) -> I:
    # Decimal.sqrt is correctly rounded to nearest; one adjacent representable
    # number on either side supplies an outward enclosure.
    ctx=Context(prec=PREC)
    root=ctx.sqrt(Decimal(n))
    return I(ctx.next_minus(root),ctx.next_plus(root))

def pair_add(x,y):
    return (x[0]+y[0],x[1]+y[1])

def pair_mul(x,y):
    return (x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])

def native_features():
    # Exact z_r=8(exp(2 pi i k_r/8)-1), represented over Q(sqrt2).
    phase=[((0,0),(0,0)),((-8,4),(0,4)),((-8,0),(8,0)),
           ((-8,-4),(0,4)),((-16,0),(0,0)),((-8,-4),(0,-4)),
           ((-8,0),(-8,0)),((-8,4),(0,-4))]
    out=Counter()
    for k in itertools.product(range(8),repeat=4):
        re=(0,0); im=(0,0); av=(0,0)
        for j in k:
            a,b=phase[j]
            re=pair_add(re,a); im=pair_add(im,b)
            av=pair_add(av,pair_add(pair_mul(a,a),pair_mul(b,b)))
        norm=pair_add(pair_mul(re,re),pair_mul(im,im))
        cv=(norm[0]-av[0],norm[1]-av[1])
        out[(av[0],av[1],cv[0],cv[1])] += 1
    return out



def high_precision_crosscheck():
    import mpmath as mp
    mp.mp.dps=80
    p=(mp.sqrt(5)-1)/2
    d=mp.mpf('0.063635191594344535042829697433316630182693569761541')
    o=mp.mpf('0.0040167350432317252873844519148251220686807163526359')
    alpha=p**2/8192;beta=2*p**2;z=mp.mpf(2)**-20;n=8192
    modes=[]
    for (a0,a1,c0,c1),mult in sorted(native_features().items()):
        modes.append((d*(a0+a1*mp.sqrt(2))+o*(c0+c1*mp.sqrt(2)),16*mult))
    energy=d*(128-64*mp.sqrt(2))
    out=[]
    for label,u in [('unmarked',mp.mpf(1)),('marker_log_phi',p),('marker_2_log_phi',p**2)]:
        def value(s):
            scale=mp.exp(2*s);zz=mp.mpf(0);jj=mp.mpf(0)
            for lam,mult in modes:
                ll=scale*lam
                k=mp.exp(2*n*mp.log1p(-alpha*ll)-n*mp.log1p(-2*p*alpha*(1-u)*ll))
                zz+=mult*k;jj-=128*mult*mp.log1p(z*(k-1))
            return mp.log(zz)/beta+jj+energy*scale
        step=mp.mpf('1e-15')
        fd=(value(step)-value(-step))/(2*step)
        dz=mp.mpf(0);zz=mp.mpf(0);dj=mp.mpf(0)
        for lam,mult in modes:
            b=1-alpha*lam;h=1-2*p*alpha*(1-u)*lam
            k=mp.exp(2*n*mp.log(b)-n*mp.log(h));slope=1/b-p*(1-u)/h
            zz+=mult*k;dz+=mult*lam*k*slope
            dj+=mult*lam*k*slope/(1-z+z*k)
        analytical=-2*dz/zz+2*128*z*beta*dj+2*energy
        error=abs(fd-analytical)
        require(error<mp.mpf('1e-25'),'80-digit independent full-value finite difference')
        out.append({'marker':label,'center_analytic_source':mp.nstr(analytical,55),
                    'full_value_finite_difference_error':mp.nstr(error,15)})
    return out


def evaluate():
    r2=sqrt_interval(2); p=(sqrt_interval(5)-1)/2
    dc=I('0.063635191594344535042829697433316630182693569761541')
    oc=I('0.0040167350432317252873844519148251220686807163526359')
    rr=I('1e-12'); d=I((dc-rr).lo,(dc+rr).hi); o=I((oc-rr).lo,(oc+rr).hi)
    alpha=p**2/8192; beta=2*p**2; z=I(1)/1048576
    n=8192; m=2*n; ref=128
    groups=native_features()
    require(len(groups)==119 and sum(groups.values())==4096,'all exact native spectral classes')
    rows=[]
    for label,u in [('unmarked',I(1)),('marker_log_phi',p),('marker_2_log_phi',p**2)]:
        Z=I(0); heatmom=I(0); loopmom=I(0); min_h=Decimal(1); min_b=Decimal(1)
        # Shared normalization formula is proved on the full scalar invariant
        # Fourier block, not assumed for arbitrary off-diagonal link variations.
        for (a0,a1,c0,c1),mult in sorted(groups.items()):
            aa=I(a0)+a1*r2; cc=I(c0)+c1*r2
            lam=d*aa+o*cc; b=1-alpha*lam
            h=1-2*p*alpha*(1-u)*lam
            require(b.lo>0 and h.lo>0,'strict denominator throughout root box')
            min_h=min(min_h,h.lo); min_b=min(min_b,b.lo)
            k=(b**m)/(h**n)
            # -beta^{-1} derivative_lambda log(k)
            slope=1/b-p*(1-u)/h
            ff=1-z+z*k
            Z=Z+16*mult*k
            heatmom=heatmom+16*mult*lam*k*slope
            loopmom=loopmom+16*mult*lam*k*slope/ff
        R=d*(128-64*r2)
        dsH=-2*heatmom/Z
        dsJ=2*ref*z*beta*loopmom
        dsR=2*R
        total=dsH+dsJ+dsR
        if label=='unmarked': require(total.lo<=0<=total.hi,'original known root scale equation')
        else: require(total.lo>0 or total.hi<0,'marked total source excludes zero on entire root enclosure')
        rows.append({'marker':label,'heat_partition':Z.bounds(),
                     'radial_H':dsH.bounds(),'radial_J':dsJ.bounds(),'radial_R':dsR.bounds(),
                     'radial_total':total.bounds(),'min_blank_lower':str(min_b),
                     'min_one_step_normalizer_lower':str(min_h)})
    return {'status':'PASS','root_radius':'1e-12','decimal_precision':PREC,
            'root_existence_proof_consumed_not_reproved':True,'fourier_modes':4096,
            'CAR_per_mode':16,'thermal_dimension':65536,'oldRIGHT_multiplicity':128,
            'actual_rounds':n,'rows':rows,
            'independent_formula_crosscheck':high_precision_crosscheck(),
            'scope':'same supplied HJR formula on normalized cost-marked channel; no physical tilt selection and no GR closure'}

if __name__=='__main__': print(json.dumps(evaluate(),indent=2,sort_keys=True))
