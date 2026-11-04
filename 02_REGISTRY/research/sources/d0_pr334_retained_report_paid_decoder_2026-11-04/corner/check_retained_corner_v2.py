#!/usr/bin/env python3
"""V1 plus the paid reader's exact omitted rows and feedback-source gain.

This proves a scalar/same-rank feedback-source identity on a fixed calibration
chart. The full heat, other controls and physical task selection remain separate.
"""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy

import sympy as sp


base = Path(__file__).resolve().parent
v1_path = base / "check_retained_corner.py"
v1_hash = hashlib.sha256(v1_path.read_bytes()).hexdigest()
if v1_hash != "b3e30df8587ebde0e3141bd7b74de145dcd557245135c2fcdd50cb51aa2ecfee":
    raise RuntimeError("The pinned V1 checker has changed")
captured = io.StringIO()
with contextlib.redirect_stdout(captured):
    ns = runpy.run_path(str(v1_path), run_name="__main__")
result = json.loads(captured.getvalue())
if result["status"] != "PASS" or result["checks"] != 60:
    raise RuntimeError("V1 did not reproduce its 60 checks")
extras = []


def require(condition, label):
    if not bool(condition):
        raise RuntimeError("FAILED: " + label)
    extras.append(label)


def zero(expression, label):
    require(sp.expand(expression) == 0, label)


ag, pg = sp.symbols("a_G p_G", positive=True)
beta = ns["beta"]
lam, P0 = ns["lam"], ns["P0"]
Dy, Dx, D = ns["Dy"], ns["Dx"], ns["D"]
c_old, c_keep = ns["expected_old"], ns["expected_kept"]
c_read = pg * c_old + (ag - pg) * c_keep
k = ag - (ag - pg) * beta
for variable in (lam, ns["a"], P0, beta, *ns["other_probabilities"]):
    residual = sp.diff(c_read, variable) - k * sp.diff(c_old, variable)
    retained_rows = -(ag - pg) * (
        D * sp.diff(beta, variable)
        + 2 * (1 - beta) * sp.diff(lam * P0 * (Dy + Dx), variable)
    )
    zero(residual - retained_rows, "exact completed-reader omitted row: " + str(variable))

c, calibration_shift = sp.symbols("c calibration_shift", real=True)
fixed_keep = (1 - beta) * (c - calibration_shift)
fixed_read = pg * c + (ag - pg) * fixed_keep
zero(sp.diff(fixed_read, c) - k, "offshell fixed-calibration reader derivative is k dc_old")
zero(k - pg - (ag - pg) * (1 - beta), "gain k lower margin")
zero(ag - k - (ag - pg) * beta, "gain k upper margin")

A, D_drop = sp.symbols("A D_drop", nonnegative=True)
read_from_branches = ag * A + pg * D_drop
zero(read_from_branches - pg * (A + D_drop) - (ag - pg) * A, "reader corner is a_G A plus p_G D_drop")
zero(read_from_branches - pg * (A + D_drop) - (ag - pg) * A, "reader-to-old ratio lower-margin numerator")
zero(ag * (A + D_drop) - read_from_branches - (ag - pg) * D_drop, "reader-to-old ratio upper-margin numerator")

# Feedback identity is a covector identity, including at source zeros; it does
# not divide by dJ_old. The actual old corner c must be strictly positive.
cr, kk, zeta, rank = sp.symbols("c_read k zeta rank", positive=True)
d = 1 - zeta
J_old = -rank * sp.log(d + zeta * c**2)
J_read = -rank * sp.log(d + zeta * cr**2)
gain = kk * (cr / c) * (d + zeta * c**2) / (d + zeta * cr**2)
require(sp.simplify(kk * sp.diff(J_read, cr) - gain * sp.diff(J_old, c)) == 0,
        "exact same-rank feedback covector identity")

# Exact positive-factor certificates for the conservative requested bounds.
# Assumptions: 0<p_G<a_G<1, a_G^2=p_G; p_G<=k,t<=a_G;
# 0<c<=1, 0<zeta<1. Here t=c_read/c_old.
t = sp.symbols("t", positive=True)
old_den = d + zeta * c**2
read_den = d + zeta * t**2 * c**2
zero(kk * t - pg**2 - ((kk - pg) * t + pg * (t - pg)), "kt lower bound positive-factor certificate")
zero((pg - kk * t - (ag * (ag - kk) + kk * (ag - t))).subs(pg, ag**2),
     "kt upper bound positive-factor certificate using a_G squared equals p_G")
zero(old_den - d * read_den - (zeta * c**2 + d * zeta * (1 - t**2 * c**2)),
     "denominator lower-ratio positive-factor certificate")
zero(read_den - d * old_den - (zeta * t**2 * c**2 + d * zeta * (1 - c**2)),
     "denominator upper-ratio positive-factor certificate")
lower_numerator = kk * t * old_den - pg**2 * d * read_den
lower_certificate = ((kk * t - pg**2) * old_den
                     + pg**2 * (zeta * c**2 + d * zeta * (1 - t**2 * c**2)))
zero(lower_numerator - lower_certificate, "G greater than or equal to p_G squared times one-minus-zeta")
upper_numerator = pg * read_den - d * kk * t * old_den
upper_certificate = ((pg - kk * t) * read_den
                     + kk * t * (zeta * t**2 * c**2 + d * zeta * (1 - c**2)))
zero(upper_numerator - upper_certificate, "G less than or equal to p_G divided by one-minus-zeta")

p_exact = (sp.sqrt(5) - 1) / 2
a_exact = sp.sqrt(p_exact)
require(bool(p_exact > 0) and bool(p_exact < 1), "original Golden p lies strictly between zero and one")
require(bool(a_exact > p_exact) and bool(a_exact < 1), "original paid reader has p below a_G below one")
require(sp.simplify(a_exact**2 - p_exact) == 0, "original paid reader satisfies a_G squared equals p")
require(0 < sp.Rational(1, 2**20) < 1, "original feedback fugacity lies in the positive interval")

result["version"] = 2
result["v1_checks"] = result["checks"]
result["v1_checker_sha256"] = v1_hash
result["checks"] += len(extras)
result["check_labels"] += extras
result["reader_feedback"] = {
    "C_read": "p*C_old+(a_G-p)*C_keep=a_G*A+p*D_drop",
    "k": "a_G-(a_G-p)*beta",
    "full_omitted_rows": "dc_read-k*dc_old=-(a_G-p)*(d0*d_beta+2*(1-beta)*d[lambda*P0*(Delta_y+Delta_x)])",
    "fixed_calibration_identity": "dc_read=k*dc_old, off shell and including source zeros",
    "J": "-rank*log(1-zeta+zeta*c^2)",
    "G": "k*(c_read/c_old)*(1-zeta+zeta*c_old^2)/(1-zeta+zeta*c_read^2)",
    "feedback_covectors": "dJ_read=G*dJ_old",
    "bounds": "p^2*(1-zeta) <= G <= p/(1-zeta)",
    "assumptions": [
        "Same physical input rank and fixed zeta for the compared feedback terms.",
        "Scalar sector or each commuting SAM block treated separately.",
        "A=C_keep>=0, D_drop>=0, C_old=A+D_drop in (0,1].",
        "Original paid reader has a_G=sqrt(p), with 0<p<a_G<1.",
        "beta and lambda*P0*(Delta_y+Delta_x) are constant on the asserted chart.",
        "A common factor after SITE/SAM averaging requires common fixed beta and calibration.",
        "Full heat and all omitted control rows remain genuine normalized residuals; no full-price source equivalence is claimed.",
    ],
}
print(json.dumps(result, indent=2, sort_keys=True))
