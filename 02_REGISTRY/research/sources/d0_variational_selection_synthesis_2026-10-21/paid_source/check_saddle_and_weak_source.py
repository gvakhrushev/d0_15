#!/usr/bin/env python3
"""Narrow new identities: paid three-node descent and weak PF-jump source.

Standard library only. Analytical proofs and source scopes are in PROOF.md.
The exact ring check is a diagnostic of the source jet, not a simulation of
the complete large factory or a uniform whole-slab inverse certificate.
"""
from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys


def require(test, message):
    if not test:
        raise RuntimeError(message)


@dataclass(frozen=True)
class Qp:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Qp) else Qp(x)

    def __add__(self, other):
        q = self.coerce(other)
        return Qp(self.a + q.a, self.b + q.b)

    __radd__ = __add__

    def __neg__(self):
        return Qp(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        q = self.coerce(other)
        return Qp(self.a*q.a + self.b*q.b,
                  self.a*q.b + self.b*q.a - self.b*q.b)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a*self.a - self.a*self.b - self.b*self.b
        require(norm != 0, 'zero field divisor')
        return Qp((self.a-self.b)/norm, -self.b/norm)

    def __truediv__(self, other):
        return self*self.coerce(other).inverse()

    def __rtruediv__(self, other):
        return self.coerce(other)*self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse()**(-n)
        ans = Qp(1)
        x = self
        while n:
            if n & 1:
                ans = ans*x
            x = x*x
            n >>= 1
        return ans

    def sign(self):
        # 2(a+b p)=(2a-b)+b sqrt(5); all comparisons are rational.
        A, B = 2*self.a-self.b, self.b
        sg = lambda x: (x > 0)-(x < 0)
        if not B:
            return sg(A)
        if not A or sg(A) == sg(B):
            return sg(B)
        return sg(A*A-5*B*B) if A > 0 else sg(5*B*B-A*A)

    def dec(self):
        dd = lambda x: Decimal(x.numerator)/Decimal(x.denominator)
        pp = (Decimal(5).sqrt()-1)/2
        return dd(self.a)+dd(self.b)*pp

    def pair(self):
        return [str(self.a), str(self.b)]


class Jet:
    """Commutative two-variable Taylor polynomial, truncated at total degree 2."""
    def __init__(self, entries=None):
        self.c = {k: Qp.coerce(v) for k, v in (entries or {}).items()
                  if Qp.coerce(v) != Qp()}

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Jet) else Jet({(0, 0): x})

    def __add__(self, other):
        q = self.coerce(other)
        keys = set(self.c)|set(q.c)
        return Jet({k: self.c.get(k, Qp())+q.c.get(k, Qp()) for k in keys})

    __radd__ = __add__

    def __neg__(self):
        return Jet({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self+(-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other)-self

    def __mul__(self, other):
        q = self.coerce(other)
        out = {}
        for (i, j), a in self.c.items():
            for (k, l), b in q.c.items():
                if i+j+k+l <= 2:
                    pos = (i+k, j+l)
                    out[pos] = out.get(pos, Qp())+a*b
        return Jet(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        ans = Jet.coerce(1)
        for _ in range(n):
            ans = ans*self
        return ans

    def at(self, i, j):
        return self.c.get((i, j), Qp())


def exact_detector_check():
    p, z, h, tau = Qp(0, 1), Qp(F(1, 2**20)), Qp(F(1, 8)), Qp(F(1, 64))
    require(p+p*p == Qp(1), 'Golden defining equation')
    f, q = Jet({(1, 0): 1}), Jet({(0, 1): 1})
    # Put scalar coefficients on the right so Jet arithmetic owns the product.
    E = (1+f*tau)*(p*p)
    b = (Jet.coerce(p)-q*(p*p*tau))**2
    ell = E*(1-E)*4
    B = b*(1-b)*4
    A = ell+(1-ell)*B
    report = 1-(1-A*z)*(1-B*z)
    r0, rf, rq = report.at(0, 0), report.at(1, 0), report.at(0, 1)
    Q, R = 1-z*4*p**3, 1-z*4*p**3*(1+p**6)
    lam = -2*p**(-5)*(R/Q+p**6)
    require(rf.sign() > 0 and rq.sign() < 0, 'actual sigma-minus source signs')
    require(rq/rf == lam, 'finite-z original source ratio')
    require(r0.sign() > 0 and (Qp(F(1, 2))-r0).sign() > 0,
            'strict increasing-entropy report chart')
    # Owned profile-normal exact scalar pair: f=r(2 lambda E_m/h+2s/h^3), q=-2E_m r/h.
    energy = Qp(F(5, 4))*p**12*Qp(F(1, 2**20))
    dfdr, dqdr = 2*lam*energy/h, -2*energy/h
    require(rf*dfdr+rq*dqdr == Qp(), 'full primary first-source cancellation')
    mixed = rf*2/h**3
    rr = (2*report.at(2, 0)*dfdr**2
          +2*report.at(1, 1)*dfdr*dqdr+2*report.at(0, 2)*dqdr**2)
    require(mixed.sign() > 0, 'nonzero source mixed block')
    require((-mixed*mixed).sign() < 0, 'exact indefinite 2x2 determinant')
    require((2*mixed+rr).sign() > 0,
            'actual reduced report has a rational positive-curvature direction')
    # Price is minus entropy; its Hessian at the stationary point is -h_phi'(r0) times this report Hessian.
    return {'r0': str(r0.dec()), 'lambda_finite': str(lam.dec()),
            'rf': str(rf.dec()), 'mixed_report_hessian': str(mixed.dec()),
            'report_second_along_1_1': str((2*mixed+rr).dec()),
            'scope': 'Exact source-jet diagnostic at tau=1/64; general paid theorem uses the owned negative cone and any strict fixed tau.'}


def exact_three_node_check():
    nu, M4, delta, gamma = F(41, 64), F(100), F(1, 128), F(1, 3)
    baseline = F(10**9)
    price = lambda t: -nu*t*t/2+17*t**3+M4*t**4/24
    require(delta**2 < 6*nu/M4, 'small finite rational step')
    S0, Sp, Sm = baseline, baseline+gamma*price(delta), baseline+gamma*price(-delta)
    require(Sp+Sm-2*S0 < -gamma*nu*delta**2/2, 'central paid inequality')
    require(min(Sp, Sm) < S0-gamma*nu*delta**2/4, 'strict paid competitor')
    require(price(1)+price(-1) > 0, 'oversized-step hostile control')
    surcharge = -gamma*min(price(delta), price(-delta))+1
    require(min(Sp+surcharge, Sm+surcharge) > S0,
            'unequal baseline can defeat comparison; common paid bank is essential')
    return {'nu': str(nu), 'delta': str(delta), 'gamma': str(gamma),
            'central_price_difference': str(Sp+Sm-2*S0),
            'strict_witness_advantage': str(S0-min(Sp, Sm)),
            'scope': 'Exact Taylor-inequality diagnostic; no full factory size or field M4 bound is asserted.'}


def sbp_check():
    n, h = 8, F(1, 8)
    flux = [F(j*j+2*j, 17) for j in range(n)]
    test = [F((-1)**j*j, 11) for j in range(n)]
    source = [-2*(flux[j]-flux[(j-1)%n])/h for j in range(n)]
    grad = [(test[(j+1)%n]-test[j])/h for j in range(n)]
    lhs = h*sum(source[j]*test[j] for j in range(n))
    rhs = 2*h*sum(flux[j]*grad[j] for j in range(n))
    require(lhs == rhs, 'original factor-two discrete summation by parts')
    modes = []
    for n in (8, 16, 32, 64):
        h = F(1, n)
        ka, kb = 3+h/7, 3-h/7
        kk = [ka if j%2 == 0 else kb for j in range(n)]
        ee = [-2*(kk[j]-kk[(j-1)%n])/h for j in range(n)]
        strong2 = h*sum(x*x for x in ee)
        dual2 = strong2*h*h/4
        require(strong2 == F(16, 49), 'strong residual does not vanish')
        require(dual2 == (ka-kb)**2, 'exact Nyquist H-minus-one norm')
        modes.append({'n': n, 'strong_norm_squared': str(strong2),
                      'dual_norm_squared': str(dual2)})
    return {'summation_by_parts_value': str(lhs), 'alternating_exact_controls': modes}


def nonlinear_pf_check():
    getcontext().prec = 75
    D = Decimal
    p, z = (D(5).sqrt()-1)/2, D(1)/D(2**20)
    tau, cf = D(1)/20, D(1)/5

    def data(x):
        E = p*p*(1+x)
        ell = 4*E*(1-E)
        ellx = 4*p*p*(1-2*E)
        b = p*p
        B = 4*b*(1-b)
        Bq = 4*(1-2*b)*(-2*p**3)
        A = ell+(1-ell)*B
        rr = 1-(1-z*A)*(1-z*B)
        rx = z*ellx*(1-B)*(1-z*B)
        rq = z*Bq*((1-ell)*(1-z*B)+(1-z*A))
        rxq = -z*ellx*Bq*(1+z-2*z*B)
        return rr, rx, rq, rxq

    r0, rx0, rq0, rxq0 = data(D(0))
    log0 = ((1-r0)/r0).ln()
    kp0 = -rxq0/rx0+rq0/(r0*(1-r0)*log0)

    def slope(x):
        rr, _, rq, _ = data(x)
        return -(((1-rr)/rr).ln()*rq)/(log0*rx0)

    expected_strong = -kp0*tau*cf
    require(expected_strong > 0, 'actual nonlinear F_yx is nonzero with correct source sign')
    rows = []
    for n in (16, 32, 64, 128, 256, 512, 1024):
        h = D(1)/n
        ka, kb = slope(-tau*cf*h), slope(-tau*cf*h/2)
        jump = abs(ka-kb)
        strong, dual = 2*jump/h, jump
        require(abs(strong-expected_strong) < D('0.1')*h,
                'actual nonlinear source approaches nonzero strong limit')
        require(dual < expected_strong*h, 'actual nonlinear weak source is O(h)')
        rows.append({'n': n, 'strong_norm': str(strong),
                     'negative_norm': str(dual), 'negative_norm_over_h': str(dual/h)})
    return {'original_price': 'sigma-minus N=1 minus binary entropy; fixed positive prefactor cancels in F_y/F_x0',
            'canonical_pullback': 'x=-tau*f/rho, y=0',
            'test_f': 'f_h=h/5; actual geometry is not resimulated',
            'rho_values': [1, 2], 'slope_derivative_at_zero': str(kp0),
            'predicted_strong_limit': str(expected_strong), 'rows': rows}


def source_pins(repo):
    paths = [
        '02_REGISTRY/research/A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md',
        '02_REGISTRY/research/sources/d0_paid_moment_field_writer_2026-10-21/code/PAID_CODE_AND_MOMENT_WRITER.md',
        '02_REGISTRY/research/sources/d0_paid_moment_field_writer_2026-10-21/moments/EXACT_MOMENT_SOURCE_CONSTRUCTION.md',
        '02_REGISTRY/research/A4D_SAME_EXECUTION_SPATIAL_WEIGHTS_AND_COMPLETE_SOURCE_2026_10_21.md',
        '02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/JOINT_FIELD_MINIMUM_OBSTRUCTION.md',
        '02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_global_star_pf_jump.py',
    ]
    return {path: hashlib.sha256((repo/path).read_bytes()).hexdigest() for path in paths}


def main():
    getcontext().prec = 75
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/workspace/scratch/323a1a75ae17/d0_15')
    out = {
        'status': 'PASS_PAID_THREE_NODE_AND_WEAK_MATERIAL_SOURCE_IDENTITIES',
        'source_snapshot': '441bdef5a02bef09a74ebe48dcf4d5527ba18988',
        'source_sha256': source_pins(repo),
        'exact_detector': exact_detector_check(),
        'paid_three_node': exact_three_node_check(),
        'discrete_weak_identity': sbp_check(),
        'actual_nonlinear_pf_slopes': nonlinear_pf_check(),
        'scope': {'autonomous_controller_selection_proved': False,
                  'best_separately_compiled_root_excluded': False,
                  'raw216_norm_changed': False,
                  'whole42_finite_root_or_inverse_proved': False,
                  'actual_AF_uniform_PF_lower_bound_proved': False,
                  'GR_closed': False}
    }
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
