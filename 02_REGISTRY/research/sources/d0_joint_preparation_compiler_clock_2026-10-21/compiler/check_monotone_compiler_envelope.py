#!/usr/bin/env python3
"""Focused checks for the actual N=1 compiler-envelope/cap comparison.

Readiness uses outward-rounded INTEGER intervals, not floating-point signs.
Only owned word constructors are imported; the old full suites are not run.
The universal prefix-price and source statements are analytical in the note.
Checks remain active under -O.  The script writes only JSON to stdout.
"""

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


D = 10**50


def ceildiv(a, b):
    return -((-a) // b)


@dataclass(frozen=True)
class Interval:
    """Both endpoints are integers divided by the single positive D."""

    lo: int
    hi: int

    def __post_init__(self):
        require(self.lo <= self.hi, "ordered interval")

    @staticmethod
    def point(value):
        require(isinstance(value, int), "only exact integer scalar input")
        return Interval(value * D, value * D)

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Interval) else Interval.point(value)

    def __add__(self, other):
        other = self.coerce(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        products = [a * b for a in (self.lo, self.hi)
                    for b in (other.lo, other.hi)]
        return Interval(min(products) // D, ceildiv(max(products), D))

    __rmul__ = __mul__

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, "nonnegative integer power")
        result, base = self.point(1), self
        while n:
            if n % 2:
                result = result * base
            base = base * base
            n //= 2
        return result

    def certificate(self):
        # Endpoint integers, rather than rounded decimal displays, certify signs.
        return {"lower_numerator": str(self.lo),
                "upper_numerator": str(self.hi), "denominator": str(D)}


def verify_inputs(repo, pins_path):
    pins = json.loads(pins_path.read_text())
    for item in pins["files"]:
        digest = hashlib.sha256((repo / item["path"]).read_bytes()).hexdigest()
        require(digest == item["sha256"], "pinned input changed: " + item["path"])
    return {"input_ref": pins["input_ref"], "sha256_verified_files": len(pins["files"])}


def readiness_intervals():
    root_floor = math.isqrt(5 * D * D)
    p = Interval((root_floor - D) // 2,
                 ceildiv(root_floor + 1 - D, 2))
    # The increasing polynomial x^2+x-1 brackets its unique positive root.
    require(0 < p.lo < p.hi < D, "p in (0,1)")
    polynomial = lambda n: n*n + n*D - D*D
    require(polynomial(p.lo) < 0 < polynomial(p.hi), "exact golden root bracket")
    require((p**2).hi * 2 < D, "p^2 < 1/2, hence log_phi(2) < 2")
    s, s2, s3 = 2 * p**3, 4 * p**3, 16 * p**9
    require(0 < s.lo <= s.hi < D, "fair preparation success in (0,1)")
    require(0 < s2.lo <= s2.hi < D, "CZ/X-cycle success in (0,1)")
    require(0 < s3.lo <= s3.hi < D, "CCZ success in (0,1)")

    # Exact Q[p]/(p^2+p-1) multiplication independently checks s2+p^6=1.
    def ringmul(x, y):
        a, b = x
        c, d = y
        return (a*c+b*d, a*d+b*c-b*d)

    def ringpower(x, n):
        result = (1, 0)
        for _ in range(n):
            result = ringmul(result, x)
        return result

    p3, p6 = ringpower((0, 1), 3), ringpower((0, 1), 6)
    require((4*p3[0]+p6[0], 4*p3[1]+p6[1]) == (1, 0), "4p^3+p^6=1")
    alpha = {k: (1-(1-s)**k)**128 for k in (8, 9, 10)}
    beta = {l: (1-p**(6*l))**172 * (1-(1-s3)**l)**43
            for l in (17, 18, 19, 20, 21)}
    require(2*alpha[8].hi < D < 2*alpha[9].lo, "K=8 fails and K=9 passes half readiness")
    require(2*beta[17].hi < D < 2*beta[18].lo, "L=17 fails and L=18 passes half readiness")
    require(alpha[8].hi < alpha[9].lo < alpha[10].lo, "ordered local alpha checks")
    require(all(beta[l].hi < beta[l+1].lo for l in range(17, 21)), "ordered local beta checks")
    stage_gaps = {l: 2*alpha[9]*(1-beta[l]) for l in (18, 20)}
    bank_gap = 1-alpha[9]
    require(all(x.lo > 0 for x in stage_gaps.values()) and bank_gap.lo > 0,
            "strict positive analytical prefix-price bounds")
    return {"method": "outward-rounded integer rational intervals",
            "p": p.certificate(),
            "alpha": {str(k): x.certificate() for k, x in alpha.items()},
            "beta": {str(l): x.certificate() for l, x in beta.items()},
            "selected_gain": (alpha[9]*beta[18]).certificate(),
            "strict_stage_extension_lower_bounds": {
                str(l): x.certificate() for l, x in stage_gaps.items()},
            "strict_bank_9_to_10_extension_lower_bound": bank_gap.certificate(),
            "smallest_separately_half_ready_caps": {"K": 9, "L": 18}}


def original_atom_ledger(repo):
    book = repo / ("02_REGISTRY/research/sources/"
                   "d0_native_gr_completion_synthesis_2026-10-20/book_source")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(book))
    spec = importlib.util.spec_from_file_location("owned_golden_detector", book / "check_golden_exact_detector.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    counts = {}
    for k, label in ((2, "CZ"), (3, "CCZ")):
        target = k
        trial = [("GT", target)]*(1 << (k-1)) + module.controlled_word(list(range(k)), target)
        counts[label] = module.gate_counts(module.native_word(trial, k+1))
    counts["full_X_cycle"] = module.gate_counts(module.native_word(module.x_cycle_word(True), 3))
    fair_plus = [("G", 0), ("G", 1), ("CX", 0, 2), ("CX", 1, 2), ("CX", 0, 1)]
    fair_minus = [fair_plus[0], ("GT", 1)] + fair_plus[2:]
    counts["fair_plus"] = module.gate_counts(fair_plus)
    counts["fair_minus"] = module.gate_counts(module.native_word(fair_minus, 3))
    expected = {"CZ": {"G": 6, "CX": 14}, "CCZ": {"G": 12, "CX": 30},
                "full_X_cycle": {"G": 4, "CX": 4},
                "fair_plus": {"G": 2, "CX": 3}, "fair_minus": {"G": 2, "CX": 5}}
    require(counts == expected, "actual native word counts including inverse echoes")
    bits = {"CZ": 1, "CCZ": 1, "full_X_cycle": 2, "fair_plus": 1, "fair_minus": 1}
    bounds = {key: sum(count.values())-2*bits[key] for key, count in counts.items()}
    require(bounds == {"CZ": 18, "CCZ": 40, "full_X_cycle": 4, "fair_plus": 3, "fair_minus": 5},
            "strict net lower bounds using ell2<2")
    require(bounds["full_X_cycle"]-2 == 2 and bounds["fair_plus"]-2 == 1,
            "pay sole final-report entropy once in extension")
    return {"expanded_words": counts, "measured_bits": bits,
            "strict_net_lower_bounds": bounds,
            "sign_transcript": "already in the two X-cycle bits; not charged twice",
            "subsequent_deterministic_H_operations": {"X_correction_CNOT": [0, 1], "canonical_SWAP_CNOT": 3},
            "old_fixture_used_as_physical_baseline": False}


def finite_envelope_and_boundary_controls():
    lines = [(Q(2, 7), Q(1)), (Q(1, 3), Q(2)), (Q(-1, 5), Q(3, 2))]
    value = lambda s: min(b+g*s for b, g in lines)
    slopes = [g for _, g in lines]
    sample = [Q(n, 3) for n in range(-9, 10)]
    for s1, s2 in zip(sample, sample[1:]):
        difference = value(s2)-value(s1)
        require(min(slopes)*(s2-s1) <= difference <= max(slopes)*(s2-s1),
                "finite monotone envelope slope bounds")

    # F=x^2-y^2, B1=B2=0, slopes 1 and 3, at the common critical point.
    qdir = lambda v: 2*(v[0]**2-v[1]**2)
    envelope_dir = lambda v: min(qdir(v), 3*qdir(v))
    v, w, vpw, vmw = (1, 0), (0, 1), (1, 1), (1, -1)
    require(envelope_dir(v) == 2 and envelope_dir(w) == -6, "tied envelope keeps both saddle signs")
    require(envelope_dir(vpw)+envelope_dir(vmw) != 2*envelope_dir(v)+2*envelope_dir(w),
            "unequal-slope indefinite tie has no quadratic Hessian")

    # B(z)=(z-1)^2/2, g(z)=1+z, z*=1-F, V=2F-F^2/2.
    # At F=x^2-y^2 and point (1/2,1/3), the Schur coefficient is c=1.
    x, y = Q(1, 2), Q(1, 3)
    f, df, hf = x*x-y*y, (2*x, -2*y), ((Q(2), Q(0)), (Q(0), Q(-2)))
    gain = 2-f
    schur = tuple(tuple(gain*hf[i][j]-df[i]*df[j] for j in range(2)) for i in range(2))
    direct = ((4-6*x*x+2*y*y, 4*x*y), (4*x*y, -4+2*x*x-6*y*y))
    require(schur == direct, "genuine stationary section Schur away from criticality")
    require((2*hf[0][0], 2*hf[1][1]) == (4, -4), "stationary field inertia preserved at origin")

    # Instructive false extensions: each is decisively rejected.
    require(Q(1)+Q(-1) == 0 and 1*Q(1)+2*Q(-1) == -1,
            "unequal site gains spoil total-source cancellation")
    alpha, beta = Q(2, 3), Q(3, 4)
    require(alpha*beta != 0, "N=2 E2 factor gives nonzero kappa/r mixed derivative")
    require(min(Q(0), Q(1)) == min(Q(0), Q(2)), "zero-gain candidate can flatten a finite envelope")
    require(Q(5)-Q(9) < 0, "positive extension cost need not beat a disappearing abort penalty")
    return {"finite_envelope_sample_pairs": len(sample)-1,
            "tied_saddle_directional_coefficients": [2, -6, 0, 0],
            "tied_hessian_parallelogram_rejected": True,
            "smooth_schur_fixture": "PASS",
            "rejected_false_extensions": ["unequal local gains", "N=2 off-shell factorization",
                                           "zero-gain alternatives", "disappearing abort charge"]}


def diagnostics():
    with localcontext() as ctx:
        ctx.prec = 65
        p = (Decimal(5).sqrt()-1)/2
        phi = 1/p
        alpha = lambda k: (1-(1-2*p**3)**k)**128
        beta = lambda l: (1-p**(6*l))**172 * (1-(1-16*p**9)**l)**43
        z0 = Decimal(1)/(2**20)
        l0 = 4*p**3
        d0 = (1-z0*l0)*(1-z0*l0*(1+p**6))
        r0 = 1-d0
        h = -(r0*r0.ln()+(1-r0)*(1-r0).ln())/phi.ln()
        return {"proof_status": "diagnostics only; exact sign certificates above",
                "alpha8": str(alpha(8)), "alpha9": str(alpha(9)),
                "beta17": str(beta(17)), "beta18": str(beta(18)), "beta20": str(beta(20)),
                "selected_gain": str(alpha(9)*beta(18)), "r0": str(r0), "h_phi_r0": str(h)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    results = {"status": "PASS", "scope": "bounded N=1 actual-word compiler-envelope/cap analysis",
               "physical_admission_proved": False, "GR_closed": False,
               "inputs": verify_inputs(args.repo, Path(__file__).with_name("SOURCE_PINS.json")),
               "readiness": readiness_intervals(), "atoms": original_atom_ledger(args.repo),
               "controls": finite_envelope_and_boundary_controls(), "diagnostics": diagnostics()}
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
