"""Fixed-reference polynomial interpolation for the native H.1 report."""
from fractions import Fraction as F
from math import comb, lcm
import json

from check_boundary_experiment import Golden as G
from check_eight_readers import inv, sci
from check_extra_work import span


def require(test, text):
    if not test:
        raise ArithmeticError(text)


def main():
    zero, one = G(0), G(1)
    p, z = G(0, 1), G(F(1, 2**20))

    def report(x, y):
        E = p**2*(one+x)
        L = G(4)*E*(one-E)
        u = p+p**2*y
        B = G(4)*u**2*(one-u**2)
        A = L+(one-L)*B
        return z*(A+B)-z**2*A*B

    L0 = B0 = G(4)*p**3
    rf = G(4)*p**2*(one-G(2)*p**2)*z*(one-z*B0)*(one-B0)
    ry = G(8)*p**3*(one-G(2)*p**2)*(z*(G(2)-L0)-z**2*(L0+G(2)*(one-L0)*B0))
    k = ry*inv(rf)
    # Verify the four fixed reference inputs lie strictly inside SC1's
    # scalar E,u domains by rational outward-rounded arithmetic.
    pi = (span(5).sqrt()-1)/2
    zi = span(F(1,2**20))
    B0i = 4*pi**3
    rfi = 4*pi**2*(1-2*pi**2)*zi*(1-zi*B0i)*(1-B0i)
    ryi = 8*pi**3*(1-2*pi**2)*(zi*(2-B0i)-zi**2*(B0i+2*(1-B0i)*B0i))
    ki = ryi/rfi
    di = span(F(1,32))
    require((1-ki*di).lo>0 and (1-pi**2*(1+ki*di)).lo>0,
            "geometric reference effects strictly interior")
    require((pi-pi**2*di).lo>0 and (1-pi-pi**2*di).lo>0,
            "material reference effects strictly interior")
    h = G(F(1, 256))
    d = G(F(1, 32))
    dy = report(zero, d)-report(zero, zero-d)
    dx = report(k*d, zero)-report(zero-k*d, zero)
    adjust = dy*inv(G(2)*d*ry)
    require(dx == G(2)*k*d*rf, "geometric reference is exactly linear")
    require(dy == dx*adjust, "exact material pre-calibration")
    ready = G(2*10946)*p**23
    c = one-G(2)*p**2
    for _ in range(9):
        c = G(2)*c**2-one
    vis = (one-c)*G(F(1, 2))*p**7
    factor = p**3*vis*ready**2
    base = p**2+G(4)*p**3*vis
    weights = [F((-1)**(j-1)*comb(8,j),j) for j in range(1,9)]
    D = lcm(*(w.denominator for w in weights))
    allocation = [int(D*abs(w)) for w in weights]
    require(D==840 and sum(allocation)==63253, "selector weights")
    fib = [0,1]
    for _ in range(25):
        fib.append(fib[-1]+fib[-2])
    require(fib[25]==75025 and fib[24]==46368, "golden stopping counts")
    require(G(fib[25])*p**24+G(fib[24])*p**25==one, "all selector paths")

    def mark(e, parts):
        total = zero
        for volume, rho, f, m in parts:
            u = e*inv(rho)
            total += volume*rho*(dy*(report(u*f,zero)-report(zero,zero))+
                                  dx*(report(zero,zero-u*adjust*m)-report(zero,zero)))
        return base+factor*total

    sets = [[(one,p,G(F(2,9)),G(F(1,7))),(one,p**2,G(F(3,11)),G(F(-1,8)))],
            [(one,p,G(F(3,11)),G(F(-1,8))),(one,p**2,G(F(2,9)),G(F(1,7)))],
            [(G(F(1,2)),G(F(4,3)),G(F(-1,7)),G(F(2,9))),
             (G(F(1,3)),one,G(F(1,8)),G(F(1,12)))]]
    gain = factor*dy*rf
    physical_gain = p**24*G(D)*h*gain
    for parts in sets:
        require(sum((v*r for v,r,_,_ in parts),zero)==one, "normalized SITE")
        target = sum((v*(f-k*m) for v,_,f,m in parts),zero)
        qs = [mark(G(j)*h,parts) for j in range(1,9)]
        combined = sum((G(w)*(q-base) for w,q in zip(weights,qs)),zero)
        require(combined==h*gain*target, "fixed-reference polynomial identity")
    for n in range(8):
        require(sum((-1)**(j-1)*comb(8,j)*j**n for j in range(1,9))==(n==0),
                "interpolation for each polynomial coefficient")
    print(json.dumps({"status":"PASS",
                      "fixed_reference_d":sci(d),
                      "material_input_adjustment":sci(adjust),
                      "selector_price_cut":24,
                      "selector_exact_cut_paths":fib[25],
                      "selector_active_paths":sum(allocation),
                      "selector_active_probability":sci(G(sum(allocation))*p**24),
                      "selector_allocations":allocation,
                      "positive_mark_gain_SC2":sci(physical_gain),
                      "conditional_on_physical_material_calibration":True,
                      "physical_controller_compiled":False,
                      "complete_Cost_Info_proved":False},indent=2,sort_keys=True))


if __name__=="__main__":
    main()
