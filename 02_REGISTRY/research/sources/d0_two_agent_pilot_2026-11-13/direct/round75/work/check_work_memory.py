"""Local spectral confirmations on the retained, non-reset A74 port tape."""
import hashlib
import json
from decimal import Decimal
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path

from mpmath import iv
import sympy as sp


def check(condition, label):
    if not condition:
        raise AssertionError(label)


def exact():
    p = (sp.sqrt(5) - 1) / 2
    eta = 2 * p**sp.Rational(3, 2)
    require_zero = lambda v: sp.simplify(v) == 0
    check(require_zero(1 - eta**2 - p**6), "discriminant of the Green function")
    check(require_zero((1 - p**3) / eta - sp.sqrt(p)), "decaying Green root")
    q, v, w = sp.symbols("q v w", positive=True)
    f = q*(1-q)*v*w/((1-q)*v+q*w)
    check(require_zero(sp.diff(f,q,2) + 2*v**2*w**2/((1-q)*v+q*w)**3),
          "strict Bayes risk concavity")
    r = p**2 + p**3*q
    check(require_zero(r*(1-r) - p**3 - p**6*q*(1-q)), "one real read")
    for bits in product((0, 1), repeat=3):
        port, ctl, target = bits
        left = target ^ ctl
        right = target ^ port
        check(left ^ port == right ^ ctl, "commuting addressed CX all columns")
        check(((left ^ port) ^ port) == left and ((right ^ ctl) ^ ctl) == right,
              "interior bit recovered on registered controls")
    # Direct Bayes enumeration on a small tape, checking the hidden port is
    # shared for the whole trajectory rather than redrawn at each symbol.
    prob = (sp.Rational(3,5), sp.Rational(2,5))
    qe = sp.Rational(1,7)
    for j in range(5):
        direct = 0
        by_count = 0
        for bits in product((0,1), repeat=j):
            u = sp.prod(prob[k] for k in bits)
            v = sp.prod(prob[1-k] for k in bits)
            d = (1-qe)*u + qe*v
            post = qe*v/d
            direct += d*post*(1-post)
        for k in range(j+1):
            u = prob[0]**(j-k)*prob[1]**k
            v = prob[1]**(j-k)*prob[0]**k
            by_count += comb(j,k)*qe*(1-qe)*u*v/((1-qe)*u+qe*v)
        check(direct == by_count, "sequential full-prefix law")


def bounds():
    iv.dps = 55
    root = Path(__file__).resolve().parents[7]
    cert = root / "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json"
    check(hashlib.sha256(cert.read_bytes()).hexdigest() ==
          "3fc747be8d27a7b581cfa7a2e9b58da5ff87058a4e3b76199dd2e9483a674b6a", "physical full128 receipt")
    rows = json.loads(cert.read_text(), parse_float=Decimal)["spectral_certificates"]
    pairs = [v["q0"] for v in rows if v["physical_index"] % 2 == 1]
    check(len(pairs) == 32, "all positive fine port-one outcomes")
    # The owner's decimal numbers serialize outward-rounded binary endpoints;
    # widening to this rational window covers their exact binary values.
    for side in (0,1):
        v = sum(Fraction.from_float(float(r[side])) for r in pairs)
        check(Fraction(15806843717,10**13) < v < Fraction(15806843720,10**13),
              "calibrated port probability")
    q = iv.mpf(["0.0015806843717","0.0015806843720"])
    p = (iv.sqrt(5)-1)/2
    m = 1024
    alpha = p**3/m
    n = 21*m
    eta = 2*p*iv.sqrt(p)
    radius = 150
    deriv = 1-2*q
    # Green function pairs +k and -k, with c=1 and c=p^k respectively.
    for k in range(1,radius+1):
        v = p**k
        for a,b in ((1,v),(v,1)):
            deriv += v*(a*(1-q)**2-b*q**2)/(a*(1-q)+b*q)**2
    deriv *= 2*p**3
    lattice_tail = 4*p**3 * p**(radius+1)/((1-p)*q**2)
    time_tail = p**6*iv.sqrt((1-q)/q)*eta**n/(1-eta)
    check(lattice_tail < iv.mpf("1e-24"), "tail in the integer Green function")
    check(time_tail < iv.mpf("1e-250"), "tail beyond 21504 real outcomes")
    error = lattice_tail + time_tail
    serial = alpha * (deriv + iv.mpf([-1,1])*error)
    snapshot = 42*p**9*(1-2*q)
    check(iv.mpf("0.00146286057") < serial < iv.mpf("0.00146286059"), "serial source")
    check(iv.mpf("0.55078916") < snapshot < iv.mpf("0.55078917"), "single-output algebra")
    check(-1+iv.sqrt(22)*serial < 0 and -1+iv.sqrt(22)*snapshot > 0,
          "opposite calibrated responses on one physical tape")
    return {"physical_port_range":[0.0015806843717,0.0015806843720],
            "full_history_gain":0,"sequential_gain":[0.00146286057,0.00146286059],
            "one_current_bit_gain":[0.55078916,0.55078917],
            "physical_work_identified":False}


if __name__ == "__main__":
    exact()
    print(json.dumps(bounds(), sort_keys=True))
