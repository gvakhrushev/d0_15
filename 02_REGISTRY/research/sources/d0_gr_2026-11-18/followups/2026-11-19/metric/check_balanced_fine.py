"""Complete registered canonical SC3 journal, exact balanced selector and paid copies."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from math import comb, isqrt
import json
import sympy as sp

from check_address_readers import check_front
from check_boundary_experiment import Golden as G
from check_eight_readers import inv
from check_golden_work_gauge import load_owner
from check_shared_site_union import sci


def copy_gate():
    n, _ = load_owner()
    cx = lambda u,v: n.Gate("CX",(u,v))
    getg = lambda u: n.Gate("G",(u,))
    source = n.Gate("SourceI",(2,0,1))
    swap = (cx(3,2),cx(2,3),cx(3,2))
    word = swap+(source,source,getg(2),source,source)+swap
    word += (cx(2,3),cx(3,4),getg(4),cx(3,4))
    ex = n.Execution(5,(),(),word,profile=n.G_CX_SOURCE_I,source_port=2,source_spin=(0,1),report_bits=(3,4))
    U = n.word_matrix(ex)
    v = sp.Matrix([n.A,n.P])
    e0,e1=sp.eye(2)[:,0],sp.eye(2)[:,1]
    for tag,tail in [(e0,sp.Matrix(n.G_LOCAL)*v),(e1,e0)]:
        cols=sp.kronecker_product(sp.eye(4),tag,v,v)
        target=sp.kronecker_product(sp.eye(4),tag,tag,tail)
        assert n.exact_matrix_equal(U*cols,target)
    inventory=n.inventory(ex,max_qubits=5,max_expanded_stages=15)
    assert (inventory.g_count,inventory.cx_count,inventory.source_i_count)==(2,9,4)
    return {"calls":15,"G":2,"CX":9,"SourceI":4,"fresh_born":2,"native_matrix_dimension":U.rows}


def probability_interval(n):
    # sin²((n+1) theta) from consecutive Chebyshev values, outward fixed-point integers.
    scale=10**55
    p0=(isqrt(5*scale*scale)-scale)//2
    def mul(a,b):
        vals=[x*y for x in a for y in b]
        return min(vals)//scale, -((-max(vals))//scale)
    def twice_minus(a,b):
        return 2*a[0]-b[1],2*a[1]-b[0]
    one=(scale,scale)
    # cos(2theta)=1-2p²=2p-1.
    x=(2*p0-scale,2*(p0+1)-scale)
    u,v=one,x
    for bit in bin(n+1)[2:]:
        middle=twice_minus(mul(u,v),x)
        if bit=="0":
            u,v=twice_minus(mul(u,u),one),middle
        else:
            u,v=middle,twice_minus(mul(v,v),one)
    return F(scale-u[1],2*scale),F(scale-u[0],2*scale)


def main():
    p,one,z=G(0,1),G(1),G(F(1,2**20))
    weights=[("f",7,F(8,7)),("f",8,F(15)),("f",8,-F(127,8))]
    weights += [("m",j,F((-1)**(j-1)*comb(8,j),j)) for j in range(1,9)]
    for tag,degree in (("f",2),("m",8)):
        assert sum(abs(c)*j for s,j,c in weights if s==tag)==255
        for d in range(1,degree+1):
            assert sum(c*j**d for s,j,c in weights if s==tag)==(d==1)
    assert all(F(1,j)>=F(15-j,56) for j in range(1,9))
    assert sum(abs(c) for s,j,c in weights if s=="f")==F(15*128-8*127,56)+F(127,8)
    alloc=[int(840*abs(c)) for s,j,c in weights]
    b,cls=check_front(42,alloc)
    alpha=G(2*10946)*p**23
    B=G(4)*p**3
    A=B+(one-B)*B
    r=z*(A+B)-z**2*A*B
    rf=G(4)*p**2*(one-G(2)*p**2)*z*(one-z*B)*(one-B)
    phi=one+p
    odds=(one-r)*inv(r)
    # Positive/negative signs in Q(p), certified by interval evaluation below.
    def positive(x):
        denominator=10**120
        low=F(isqrt(5*denominator**2)-denominator,2*denominator)
        high=low+F(1,2*denominator)
        return min(x.a+x.b*low,x.a+x.b*high)>0
    assert positive(odds**4-phi**109) and positive(phi**55-odds**2)
    samples={n:probability_interval(n) for n in (15574,19766)}
    for l,u in samples.values():
        assert F(18,10**7)<l<u<F(24,10**7)
    assert positive(phi**28-G((1-F(18,10**7))/F(18,10**7)))
    assert positive(G((1-F(24,10**7))/F(24,10**7))-phi)
    def gd(x):
        return D(x.a.numerator)/D(x.a.denominator)+D(x.b.numerator)/D(x.b.denominator)*pd
    def entropy(t):
        return -t*t.ln()-(1-t)*(1-t).ln()
    with localcontext() as ctx:
        ctx.prec=60
        pd=(D(5).sqrt()-1)/2
        ell=-pd.ln()
        # Avoid cancellation in large Golden coefficients by obtaining the mark
        # gain as a high-precision certified display from the shared field utility.
        rd=gd(r)
        eta=((1-rd)/rd).ln()/ell
        gains=[gd(alpha)+D(255)*(D(n+1)-eta) for n in (0,26,27)]
        rate=G(840)*b*G(F(1,256))*rf
        # Enumerate all four fine labels of one canonical native pair. A retained
        # deterministic extra print gives no new entropy, also for signed marks.
        aa=pd*pd
        rr=((D(3)*pd-D(4)*pd**3)**2)
        for sign in (False,True):
            full={}
            for a in (0,1):
                for s in (0,1):
                    prob=(aa if a else 1-aa)*(rr if s else 1-rr)
                    t=int(bool(a*s)^sign)
                    full[(a,s,t,(s,)*27)]=prob
            assert abs(sum(full.values())-1)<D("1e-55")
            assert abs(-sum(x*x.ln() for x in full.values())-entropy(aa)-entropy(rr))<D("1e-55")
            length=sum(prob*(2+a+s+1+t+27*(1+s)) for (a,s,t,copies),prob in full.items())
            tmean=(1-aa*rr) if sign else aa*rr
            assert abs(length-(2+aa+rr+1+tmean+27*(1+rr)))<D("1e-54")
        # The sign of a literal, equal-length, non-infinitesimal SC5 comparison.
        l0,u0=samples[15574]
        l1,u1=samples[19766]
        dec=lambda x:D(x.numerator)/D(x.denominator)
        r0,r1=(dec(l0)+dec(u0))/2,(dec(l1)+dec(u1))/2
        sec=(entropy(r1)-entropy(r0))/((r1-r0)*ell)
        assert sec>1 and sec<28
        out={"status":"PASS","absolute_first_moments":{"geometry":255,"matter":255},
            "old_unbalanced_absolute_first_moments":["11/5","255"],
            "selector_42_class_repetitions":cls,"selector_active":sci(G(sum(alloc))*b),
            "geometric_l1_optimum":str(F(15*128-8*127,56)+F(127,8)),
            "report_entropy_slope_at_SC1":str(+eta)[:18],
            "complete_ledger_coefficients_0_26_27_copies":[format(x,".12f") for x in gains],
            "leading_slope_SC2_27_copies_at_h_1_256":format(gains[-1]*D(sci(rate)),".12E"),
            "fixed_n_actual_SC5_report_probabilities":[format(val,".14E") for val in (r0,r1)],
            "fixed_n_entropy_secant_in_code_units":format(sec,".12f"),
            "fixed_n_common_SC5_L":19766,"fixed_n_positive_27_copies":True,
            "actual_noiseless_NC1_copy":copy_gate(),"full_geometric_Cost_Info_proved":False}
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
