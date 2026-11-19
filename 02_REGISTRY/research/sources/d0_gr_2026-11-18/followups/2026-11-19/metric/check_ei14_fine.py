"""Exact (2,8) native truth table, a dimension-free entropy bound, and actual noisy CX."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from math import isqrt
import json
import sympy as sp

from check_boundary_experiment import Golden as G
from check_golden_work_gauge import load_owner


P, Z, ONE, ZERO = G(0, 1), G(F(1, 2**20)), G(1), G(0)
def plus(*ps):
    d = {}
    for p in ps:
        for k,v in p.items():
            d[k] = d.get(k,ZERO)+v
    return {k:v for k,v in d.items() if v != ZERO}


def mul(p,q):
    return plus(*({(a+c,b+d):x*y} for (a,b),x in p.items() for (c,d),y in q.items()))


def scale(p,s):
    return {k:v*s for k,v in p.items()}


def betas(sign):
    one = {(0,0):ONE}
    e = {(0,0):P**2,(1,0):P**2*G(F(1,64))}
    u = {(0,0):P,(0,1):P**2*G(F(sign,64))}
    u2 = mul(u,u)
    b = scale(plus(u2,scale(mul(u2,u2),G(-1))),G(4))
    l = scale(plus(e,scale(mul(e,e),G(-1))),G(4))
    a = plus(l,b,scale(mul(l,b),G(-1)))
    poly = plus(scale(plus(a,b),Z),scale(mul(a,b),ZERO-Z**2))
    data = [ZERO]*1024
    for (i,j),coef in poly.items():
        data[((1<<i)-1) | (((1<<j)-1)<<2)] = coef
    # Evaluate every ten-sign word by exact Walsh transform.
    for bit in range(10):
        stride=1<<bit
        for base in range(0,1024,2*stride):
            for j in range(stride):
                c,d=data[base+j],data[base+j+stride]
                data[base+j],data[base+j+stride]=c+d,c-d
    return data


def enclosure(x):
    scale=10**90
    low=F(isqrt(5*scale**2)-scale,2*scale)
    high=low+F(1,2*scale)
    return min(x.a+x.b*low,x.a+x.b*high),max(x.a+x.b*low,x.a+x.b*high)


def actual_cx():
    n, _ = load_owner()
    gate=n.Gate("CX",(2,3))
    ex=n.Execution(4,(),(),(gate,),profile=n.G_CX_SOURCE_I,source_port=2,source_spin=(0,1),report_bits=(3,))
    V=n.word_matrix(ex)*sp.kronecker_product(sp.eye(8),sp.Matrix([n.A,n.P]))
    eff=V.T*sp.kronecker_product(sp.eye(8),sp.diag(0,1))*V
    assert n.exact_matrix_equal(eff,sp.kronecker_product(sp.eye(4),sp.diag(n.P**2,n.P)))
    return eff.rows


def main():
    xs,ys=betas(1),betas(-1)
    assert all(xs[i]==ys[i^1020] for i in range(1024))
    lo=min(enclosure(x)[0] for x in xs)
    hi=max(enclosure(x)[1] for x in xs)
    assert 0<lo<hi<1
    coarse_bound=(hi-lo)**2/(8*lo*(1-hi))
    assert coarse_bound < F(155,10**13)
    with localcontext() as ctx:
        ctx.prec=70
        ell=((1+D(5).sqrt())/2).ln()
        def dec(x):
            return D(x.numerator)/D(x.denominator)
        def h(x):
            return -x*x.ln()-(1-x)*(1-x).ln()
        l,u=dec(lo),dec(hi)
        sec=(h(u)-h(l))/(u-l)
        r=1/(1+sec.exp())
        cap=h(r)-((u-r)*h(l)+(r-l)*h(u))/(u-l)
        assert l<r<u and 0<cap<dec(coarse_bound)
        kmin=28-((1-l)/l).ln()/ell
        kmax=28-((1-u)/u).ln()/ell
        assert D(".5614")<kmin<kmax<D(".5785")
        # Independent evaluation of the binary channel capacity on its
        # extremal commuting two-dimensional ensemble. Marginal B~Bern(r).
        weights=[(u-r)/(u-l),(r-l)/(u-l)]
        mi=sum(w*(t*(t/r).ln()+(1-t)*((1-t)/(1-r)).ln()) for w,t in zip(weights,(l,u)))
        assert abs(mi-cap)<D("1e-60")
        p=(D(5).sqrt()-1)/2
        cx_loss=D(2).ln()-h(p**2)
        cx_born_loss=h(2*p**3)-h(p**2)
        threshold=dec(coarse_bound)/(ell*kmin)
        assert D("0")<threshold<D("5.7e-11") and cx_born_loss>0
        print(json.dumps({"status":"PASS","sign_words_each_orientation":1024,
              "native_table_min":format(l,".18E"),"native_table_max":format(u,".18E"),
              "universal_capacity_nats_numeric":format(cap,".15E"),
              "certified_quadratic_majorant_nats":format(dec(coarse_bound),".15E"),
              "absolute_CQ_source_code_slope_27_range":[format(kmin,".12f"),format(kmax,".12f")],
              "actual_noisy_CX_old_compression_dimension":actual_cx(),
              "actual_noisy_CX_hidden_entropy_nats":format(cx_loss,".14f"),
              "actual_native_born_and_dephased_gap_nats":format(cx_born_loss,".14f"),
              "sufficient_report_increment_for_positive_ledger":format(threshold,".15E"),
              "generated_bank_all_180_plus_16_resources_replayed":False,
              "full_physical_Cost_minus_Info":False},indent=2,sort_keys=True))


if __name__=="__main__":
    main()
