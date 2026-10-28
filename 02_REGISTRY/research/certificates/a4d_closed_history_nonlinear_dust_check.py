"""Exact original-click / nonlinear-dust composition checks.

Consumes the existing full LTB curvature/Cartan owner; does not replay it.
The interval calculation certifies one point of the exact algebraic trace
branch, not a finite native stationary history or a GR closure certificate.
Run from the repository root, with SymPy available. No asserts are used.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json

import sympy as S


checks = []


def need(ok, label):
    if not ok:
        raise RuntimeError(label)
    checks.append(label)


class I:
    """Closed rational intervals; every arithmetic endpoint is exact."""
    def __init__(self, lo, hi=None):
        self.lo = Q(lo)
        self.hi = self.lo if hi is None else Q(hi)
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def coerce(x):
        return x if isinstance(x, I) else I(x)

    def __add__(self, other):
        other = self.coerce(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        ends = (self.lo * other.lo, self.lo * other.hi,
                self.hi * other.lo, self.hi * other.hi)
        return I(min(ends), max(ends))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        if other.lo <= 0 <= other.hi:
            raise ZeroDivisionError("interval contains zero")
        return self * I(1 / other.hi, 1 / other.lo)

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __pow__(self, n):
        if n < 0:
            return I(1) / (self ** (-n))
        result = I(1)
        for _ in range(n):
            result = result * self
        return result

    def sqrt(self, bits=160):
        if self.lo < 0:
            raise ValueError("negative square-root interval")
        scale = 1 << bits
        floor_lo = isqrt((self.lo.numerator * scale * scale)
                         // self.lo.denominator)
        floor_hi = isqrt((self.hi.numerator * scale * scale)
                         // self.hi.denominator)
        return I(Q(floor_lo, scale), Q(floor_hi + 1, scale))

    def outward_decimal(self, digits=30):
        scale = 10 ** digits
        lo = (self.lo.numerator * scale) // self.lo.denominator
        hi = -((-self.hi.numerator * scale) // self.hi.denominator)

        def render(n):
            sign = "-" if n < 0 else ""
            whole, rest = divmod(abs(n), scale)
            return f"{sign}{whole}.{rest:0{digits}d}"

        return [render(lo), render(hi)]


p, z, x, y = S.symbols("p z x y")
E = p**2 * (1 + x)
b = p - p**2 * y
ell = 4 * E * (1 - E)
B = 4 * b**2 * (1 - b**2)
A = ell + (1 - ell) * B
r = S.expand(z * (A + B) - z**2 * A * B)
poly_r = S.Poly(r, x)
need(poly_r.degree() == 2, "original sigma-minus click is exactly quadratic in curvature")
A0, A1, A2 = (poly_r.nth(k) for k in range(3))
need(S.expand(r - (A0 + A1*x + A2*x*x)) == 0,
     "exact original-click quadratic decomposition")
T = S.expand(x*S.diff(r, x) - y*S.diff(r, y))
H = r - x*S.diff(r, x)
at = S.expand(2*A2 - y*S.diff(A2, y))
bt = S.expand(A1 - y*S.diff(A1, y))
ct = S.expand(-y*S.diff(A0, y))
need(S.expand(T - (at*x*x + bt*x + ct)) == 0,
     "full independent-coframe trace is the displayed quadratic")


def golden_zero(expr):
    numerator = S.fraction(S.cancel(expr))[0]
    return S.rem(S.Poly(numerator, p), S.Poly(p*p + p - 1, p)).is_zero


rx0 = S.diff(r, x).subs({x: 0, y: 0})
ry0 = S.diff(r, y).subs({x: 0, y: 0})
L = 4*p**3
qe = 1 - z*L
re = 1 - z*L*(1 + p**6)
need(golden_zero(rx0 - 4*z*p**11*qe), "original positive curvature slope, with Golden relation")
need(golden_zero(ry0 + 8*z*p**6*(re + p**6*qe)),
     "original negative material slope, with Golden relation")
need(golden_zero(-ry0/rx0 - 2*p**(-5)*(re/qe + p**6)),
     "original ratio kappa0, not a fitted Einstein coefficient")
jac0 = S.Matrix([T, H]).jacobian([x, y]).subs({x: 0, y: 0})
need(S.expand(jac0.det() - rx0*ry0) == 0,
     "radial and Ward Jacobian equals r_x(0) r_y(0)")

# An exact small nonlinear sector, at a fixed original-number aperture.
# Polynomial interval evaluation includes the actual Golden p and its error.
pi = (I(5).sqrt() - 1) / 2
zi, yi = I(Q(1, 1 << 20)), I(Q(1, 1 << 20))


def evaluate(poly, values):
    variables = tuple(values)
    result = I(0)
    for powers, coefficient in S.Poly(S.expand(poly), *variables).terms():
        term = I(Q(int(S.numer(coefficient)), int(S.denom(coefficient))))
        for variable, power in zip(variables, powers):
            term = term * values[variable]**power
        result = result + term
    return result


base = {p: pi, z: zi, y: yi}
ati, bti, cti = (evaluate(v, base) for v in (at, bt, ct))
disc = bti*bti - 4*ati*cti
need(ati.hi < 0 and bti.lo > 0 and cti.lo > 0 and disc.lo > 0,
     "exact native y0=2^-20 lies on a regular positive-discriminant branch")
xi = -2*cti / (bti + disc.sqrt())
ki = -xi / yi
values = {p: pi, z: zi, x: xi, y: yi}
rxi = evaluate(S.diff(r, x), values)
ryi = evaluate(S.diff(r, y), values)
ri = evaluate(r, values)
Ei = evaluate(E, values)
bi = evaluate(b, values)
need(xi.hi < 0 and ki.lo > 0, "explicit nonlinear trace branch has x0<0 and kappa_sector>0")
need(rxi.lo > 0 and ryi.hi < 0, "both exact native source slopes keep their required signs")
need(0 < Ei.lo < Ei.hi < 1 and 0 < bi.lo < bi.hi < 1,
     "original geometric and matter rotation inputs stay inside their native chart")
need(0 < ri.lo < ri.hi < Q(1, 2), "original complete click stays on the monotone direct-return branch")
jdet = S.det(S.Matrix([T, H]).jacobian([x, y]))
jdi = evaluate(jdet, values)
need(jdi.hi < 0, "nonlinear Ward/trace map remains locally invertible at this sector")

# The exact algebraic root, rather than an interval zero test, proves T=0.
aa, bb, cc, dd = S.symbols("aa bb cc dd", nonzero=True)
root_expr = -2*cc/(bb + dd)
num = S.together(aa*root_expr**2 + bb*root_expr + cc).as_numer_denom()[0]
need(S.rem(S.Poly(num, dd), S.Poly(dd**2 - (bb**2 - 4*aa*cc), dd)).is_zero,
     "explicit radical branch solves the trace equation exactly")

# Consume the already verified arbitrary-function LTB source, with R/2.
kappa, q0, a3, timeT, timeD = S.symbols("kappa q0 a3 T D", positive=True)
volume = a3*timeT*timeD/3
Gtt = 4/(3*timeT*timeD)
R = -4/(3*timeT*timeD)
a3_true = S.Rational(9, 2)*kappa*q0
need(S.simplify((volume*Gtt/2 - kappa*q0).subs(a3, a3_true)) == 0,
     "owned non-VSI LTB solves the original R/2 metric equation")
need(S.simplify((volume*R/2 + kappa*q0).subs(a3, a3_true)) == 0,
     "LTB curvature and kinetic densities obey the exact nonlinear trace branch")
need(S.simplify((volume*Gtt/2 - kappa*q0).subs(a3, S.Rational(9, 4)*kappa*q0)) != 0,
     "negative control detects the wrong imported factor of two")
need(S.simplify((2*q0/volume)*volume - 2*q0) == 0,
     "derived dust density-volume relation leaves the volume free")
q0i = yi / (pi*pi)
need(4*q0i.hi < (pi*pi/16).lo,
     "fixed aperture tau=p^2 and 1<=t<=2 keep both CAR amplitude coordinates in the owned chart")

owners = [
    "02_REGISTRY/research/A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md",
    "02_REGISTRY/research/A4D_COMPLETE_PRICE_ONSHELL_DENSITY_RIGIDITY_2026_10_21.md",
    "02_REGISTRY/research/A4D_ORIGINAL_STAR_NULL_CART_SIGN_AND_ALL_ORDER_CQ_RETYPE_2026_10_21.md",
]
receipt = {
    "input_head": "46ebed17ddfa04faa8ab1a07a6a822b717f993ef",
    "checks_count": len(checks),
    "checks": checks,
    "exact_sector": {"z": "2^-20", "y0": "2^-20", "fixed_tau": "p^2"},
    "outward_rational_interval_decimals": {
        "x0": xi.outward_decimal(),
        "kappa_sector": ki.outward_decimal(),
        "r_x": rxi.outward_decimal(),
        "r_y": ryi.outward_decimal(),
        "ward_trace_jacobian": jdi.outward_decimal(),
    },
    "owner_sha256": {path: sha256(Path(path).read_bytes()).hexdigest() for path in owners},
    "scope": "Exact original polynomial, rational interval branch and changed LTB coefficient checks. The existing full curvature/Cartan proof is consumed, not rerun. No complete native-word execution, exact finite stationary recovery, physical selection or GR closure is certified by this script.",
    "GR_closed": False,
}
print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
