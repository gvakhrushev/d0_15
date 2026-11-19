"""Two paid material selectors: exact L=4 quadrature, calibration and secants."""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json


@dataclass(frozen=True)
class Golden:
    """a+b*p, p**2=1-p."""
    a: F = F(0)
    b: F = F(0)

    def __add__(self, other):
        y = scalar(other)
        return Golden(self.a+y.a, self.b+y.b)

    __radd__ = __add__

    def __neg__(self):
        return Golden(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-scalar(other))

    def __rsub__(self, other):
        return scalar(other) - self

    def __mul__(self, other):
        y = scalar(other)
        return Golden(self.a*y.a+self.b*y.b, self.a*y.b+self.b*y.a-self.b*y.b)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a**2-self.a*self.b-self.b**2
        return Golden(F(self.a-self.b, norm), F(-self.b, norm))

    def __pow__(self, n):
        result = scalar(1)
        for _ in range(n):
            result *= self
        return result


def scalar(x):
    return x if isinstance(x, Golden) else Golden(F(x))


def positive(x):
    # 2x=(2a-b)+b sqrt(5). Compare opposite signs by exact squaring.
    c, b = 2*x.a-x.b, x.b
    if not b:
        return c > 0
    if b > 0:
        return c >= 0 or 5*b*b > c*c
    return c > 0 and c*c > 5*b*b


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


P = Golden(F(0), F(1))
CORNERS = list(product((0, 1), repeat=2))
SITES = list(product(range(4), repeat=4))
PHASE = ((1, 0), (0, 1), (-1, 0), (0, -1))


def quadrature(s, t):
    # The mean field / A_* and its physical forward differences on all 256 sites.
    weights = [((1-s, s)[u]*(1-t, t)[v]) for u, v in CORNERS]
    field = {}
    for x in SITES:
        vectors = [PHASE[(x[1] + u*x[0] + v*x[2]) % 4] for u, v in CORNERS]
        field[x] = [sum(w*v[j] for w, v in zip(weights, vectors)) for j in (0, 1)]
    energy = 0
    for x in SITES:
        for mu, sign in enumerate((1, -1, -1, -1)):
            other = list(x)
            other[mu] = (x[mu]+1) % 4
            neighbor = field[tuple(other)]
            energy += sign * sum((z-y)**2 for y, z in zip(field[x], neighbor))
    # e=4I and H=1/4 cancel. Divide by 2 to get mean q/(2*A_*^2).
    return energy * F(1, 2*len(SITES))


def symbolic(s, t):
    def b(x):
        return 1-2*x+2*x*x
    return -(b(s)-s*s)*b(t)-t*t*b(s)


def native_levels():
    r = P**2
    delta = P**9
    q = {}
    for u, v in CORNERS:
        sharp = quadrature(scalar(u), scalar(v))
        need(sharp == scalar(u-1-v), "physical sharp quadrature")
        s, t = r + u*delta, r + v*delta
        q[u,v] = quadrature(s,t)
        need(q[u,v] == symbolic(s,t), "independently regenerated quadrature")
    ds = (q[1,0]-q[0,0])*delta.inverse()
    dt = (q[0,1]-q[0,0])*delta.inverse()
    need(ds == 40*P-24+(10*P-7)*delta, "s secant")
    need(dt == 32*P-20+(6*P-5)*delta, "t secant")
    need(positive(ds) and positive(-dt), "secant signs")
    need(sum((P,r)[u]*(P,r)[v] for u,v in CORNERS) == scalar(1), "all sharp programs")
    # Two physical seeds sharing k are independent only after k is fixed.
    mixture_square = P*r*r + r*(r+delta)**2
    square_mixture = (P*r + r*(r+delta))**2
    need(mixture_square - square_mixture == P*r*delta**2, "shared-program covariance")
    return ds, dt


def calibration():
    # Exact Chebyshev recurrence in Q(p). Compute delta_x without dividing by k0.
    c = P**3
    prev, cur = scalar(1), c
    for _ in range(1,712):
        prev, cur = cur, 2*c*cur-prev
    amplitude2 = P**2 * (1-cur) * F(1,2)
    z = scalar(F(1,2**20))
    def report(x,y):
        e = P**2*(1+x)
        l = 4*e*(1-e)
        u = P+P**2*y
        b = 4*u*u*(1-u*u)
        a = l+(1-l)*b
        return z*(a+b)-z*z*a*b
    l = 4*P**3
    rf = 4*P**2*(1-2*P**2)*z*(1-z*l)*(1-l)
    rq = 8*P**3*(1-2*P**2)*(z*(2-l)-z*z*(l+2*(1-l)*l))
    k0 = rq*rf.inverse()
    grid = F(16517734400,162621047169)
    gx, gy = scalar(grid / (16*4096)), 2*amplitude2*F(1,4096)
    dx = report(gx,0)-report(-gx,0)
    dy = report(0,gy)-report(0,-gy)
    alpha = dy*dx.inverse()
    for x, lo, hi in ((2*amplitude2,".0002478931746221468",".0002478931746221470"),
                      (alpha,".914389183500842",".914389183500844")):
        need(positive(x-F(lo)) and positive(F(hi)-x), "exact calibration enclosure")
    need(positive(k0) and positive(2*amplitude2*k0*alpha.inverse()), "physical scale")


def rotation_controls():
    # Native CX from an actual sharp input into the register being rotated.
    # An integer is the exponent of a common Golden rotation.
    def sector(word, bits):
        power = flip = 0
        for gate,arg in word:
            if gate == "G":
                power += arg
            elif bits[arg]:
                power, flip = -power, 1-flip
        return power, flip

    def controlled(word, bit):
        inverse = [(s, -k if s == "G" else k) for s,k in reversed(word)]
        return word+[("X",bit)]+inverse+[("X",bit)]
    base = [("G",7)]
    for u,v in CORNERS:
        need(sector(controlled(base,0),(u,v)) == (14*u,0), "first sharp control")
        need(sector(controlled(controlled(base,0),1),(u,v)) == (28*u*v,0), "mixed control")


if __name__ == "__main__":
    calibration()
    ds, dt = native_levels()
    rotation_controls()
    print(json.dumps({"status":"PASS", "sites_per_quadrature":256, "quadratures":8,
                      "N":8, "seed_secant_s_in_Qp":[int(ds.a),int(ds.b)],
                      "seed_secant_t_in_Qp":[int(dt.a),int(dt.b)],
                      "sharp_q_over_2A2":[-1,-2,0,-1], "order_ks_kt":["00","01","10","11"],
                      "exact_SC1_calibration":True,"same_site_coordinate_source":False,
                      "physical_CW1_cost_proved":False,"GR_closed":False},
                     indent=2, sort_keys=True))
