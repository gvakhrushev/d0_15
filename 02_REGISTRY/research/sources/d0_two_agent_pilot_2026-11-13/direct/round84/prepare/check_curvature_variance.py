"""Field-flat Weyl mode on the pinned geometric bank and its actual registered CX."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json
import os
import subprocess
import sys
import types

sys.dont_write_bytecode = True
PIN = "2350117b469890c04b8ff5d8987b224a863e844a"
METRIC = "02_REGISTRY/research/sources/d0_gr_2026-11-18/followups/2026-11-19/metric/"
REPO = os.environ.get("D0_PILOT_OBJECT_REPO", str(Path(__file__).resolve().parents[7]))


def pinned(name):
    data = subprocess.check_output(["git", "-C", REPO, "show", PIN+":"+METRIC+name+".py"])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(compile(data, name+".py", "exec", optimize=0), module.__dict__)
    return module


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def check_anchor_transport():
    import sympy as sp
    e=sp.Matrix([1,0,0]); c=sp.Rational(1,8)
    n=sp.sqrt(1-c*c)
    b=sp.Matrix([c,n,0])
    s=sp.Matrix([[1,0,0],[0,sp.Rational(3,5),-sp.Rational(4,5)],
                 [0,sp.Rational(4,5),sp.Rational(3,5)]])
    def full(target):
        k=target*e.T-e*target.T
        return sp.eye(3)+k+k*k/(1+c)
    check(s*e==e and s*s.T==sp.eye(3), "orthogonal fixed anchor")
    check(full(s*b)==s*full(b)*s.T and full(b)*e==b, "full-column anchored transport")


G = pinned("check_boundary_experiment").Golden
pinned("check_shared_site_union")
geometry = pinned("check_smooth_twofield_reference").geometry
o, p, z = G(1), G(0,1), G(F(1,2**20))
phi = o+p
r = p*p


def inv(x):
    n = x.a*x.a-x.a*x.b-x.b*x.b
    return G(F(x.a-x.b)/n, -F(x.b)/n)


def sign(x):
    # Exact sign in Q(sqrt(5)), including tiny odd-polynomial differences.
    a, b = 2*x.a-x.b, x.b
    if a*b >= 0:
        return (a+b>0)-(a+b<0)
    disc = a*a-5*b*b
    return ((a>0)-(a<0))*((disc>0)-(disc<0))


def display(x):
    # Used only for display, all assertions use exact algebra.
    a,b = F(x.a),F(x.b)
    with localcontext() as ctx:
        ctx.prec = max(len(str(abs(a.numerator)))+len(str(a.denominator)),
                       len(str(abs(b.numerator)))+len(str(b.denominator)))+30
        conv=lambda f:Decimal(f.numerator)/Decimal(f.denominator)
        return format(conv(a)+conv(b)*(Decimal(5).sqrt()-1)/2, ".12E")


def report(x,y):
    e = r*(o+x)
    L = G(4)*e*(o-e)
    u = p+r*y
    B = G(4)*u*u*(o-u*u)
    A = L+(o-L)*B
    return z*(A+B)-z*z*A*B


L0 = G(4)*p**3
rf = G(4)*r*(o-G(2)*r)*z*(o-z*L0)*(o-L0)
rq = G(8)*p**3*(o-G(2)*r)*(z*(G(2)-L0)-z*z*(L0+G(2)*(o-L0)*L0))
k0 = rq*inv(rf)
H = F(1,4)
Fgrid = geometry(4)  # Full CAR16 trace, both orientations, six actual faces.
check(Fgrid==F(16517734400,162621047169), "full CAR moment")
b = G(Fgrid/16)*inv(k0)
f = G(Fgrid/64)
zero=G()
r0=report(zero,zero)


def one_input(t):
    sites=list(product(range(4),repeat=4))
    # Original F2 links; only the local scalar inverse-coframe is modulated.
    # mu=v_x*rho_x=1/256. All elementary grid faces including wrap are present.
    c=(1,0,-1,0)
    xs=[f*(o+G(t*c[site[0]])) for site in sites]
    mean=sum(xs,zero)*G(F(1,256))
    second=sum((x*x for x in xs),zero)*G(F(1,256))
    check(mean==f and second==f*f*G(1+t*t/2), "both moments on all cells")
    return mean,second


def main():
    check_anchor_transport()
    h=G(F(1,32768)); t=F(1,4); dt=F(1,16)
    U, V = one_input(t)
    left,right = one_input(t-dt),one_input(t+dt)
    derivative=(right[1]-left[1])*G(1/(2*dt))
    check(derivative==f*f*G(t), "centered physical tangent")
    signed=zero; unsigned=zero
    sizes=[705600*comb(8,j)//j**2 for j in range(1,9)]
    samples=[]
    normalized_gain=G(2)*b*rf*rq*h*h
    for j,n in enumerate(sizes,1):
        eps=G(j)*h
        A=report(zero,b*eps)-report(zero,zero-b*eps)
        check(sign(A)>0, "reference response sign")
        def raw(pair):
            mean,second=pair
            return A*rf*(eps*mean-phi*eps*eps*second)
        # Independent evaluation of the original SC1 table from the three site values.
        vals=[f*G(1+t*i) for i in (1,0,-1,0)]
        mean_click=sum((report(eps*x,zero)-r0 for x in vals),zero)*G(F(1,4))
        check(raw((U,V))==A*mean_click, "polynomial equals 4 distinct-site evaluations")
        slope=(raw(right)-raw(left))*G(1/(2*dt))
        check(slope==zero-A*rf*phi*eps*eps*derivative and sign(slope)<0, "raw finite jet sign and identity")
        signed += G(((-1)**(j-1))*n)*slope
        unsigned += G(n)*slope
        samples.append(display(slope))
    check(signed==zero and sign(unsigned)<0, "signed cancellation with unsigned motion")
    ratio=unsigned*inv(G(705600)*normalized_gain)
    leading=zero-G(1024)*phi*h*derivative
    relative=(ratio-leading)*inv(leading)
    check(sign(G(F(1,10**10))-relative)>0 and sign(G(F(1,10**10))+relative)>0, "finite normalized deviation")
    # On arbitrary prior copies/ref, CNOT on sharp B,T changes orthogonal
    # basis vectors iff B=1. Second CNOT depends only on parity of j.
    for b0,neg,initial in product((0,1),repeat=3):
        first=initial^b0; last=first^neg
        check((first!=initial)==bool(b0) and (last!=first)==bool(neg), "full sharp CX costs")
    for raw,neg in product((0,1),repeat=2):
        t_before=raw
        t_opposite=t_before^1
        duplicate=t_opposite
        restored=t_opposite^1
        check(restored^neg==raw^neg and duplicate==1-raw, "old truth table and duplicate")
        check(raw+duplicate==1 and (1+raw)+(1+duplicate)==3, "branchwise compensation and two emitted lengths")
        check(((p**2,p)[raw])==((p,p**2)[duplicate]), "cold duplicate overlap")
    check(sum(F(comb(8,j),j*j)*j**2 for j in range(1,9))==255, "leading absolute sum")
    check(sum(F(comb(8,j),j*j)*j**3 for j in range(1,9))==1024, "leading unsigned correction")
    print(json.dumps({"source":PIN,"anchored_full_column_conjugacy_checked":True,"grid":"4^4","F_H":str(Fgrid),
          "strict_negative_each_of_8_raw_slopes":True,
          "raw_head_slopes_divided_by_p3_vis_alpha2":samples,
          "signed_T_slope_exact":"0",
          "CX_B_work_slope_divided_by_physical_T_gain":display(ratio),
          "leading_small_h_slope_divided_by_gain":display(leading),
          "relative_difference_to_leading":display(relative),
          "old_right_arbitrary_after_retained_B":True,
          "complete_compiled_geometry_and_Book_price":False},indent=2))


if __name__=="__main__":
    main()
