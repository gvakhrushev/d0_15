#!/usr/bin/env python3
"""Exact first-source check for the complete golden exterior readout.

Default execution is read-only.  --output writes the JSON receipt.
The finite fixture retains every occupation outcome, including zero-mass
outcomes at the base point, and includes a noncommuting first perturbation.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import hashlib
import json
import math
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
OWNERS = {
    "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md":
        "748f723516dead3a713f31dd5a49dcbde7805ef0a15e7450f3026790abefa5e2",
    "02_REGISTRY/research/A4D_ONE_FEEDBACK_NONFLAT_NULL_SCALAR_EINSTEIN_SOURCE_2026_10_18.md":
        "80bdb2a3ab6189b37ea9cebe1545cfebea2d7300037f4d3e21fa5e1479a5ce84",
}


def run() -> dict:
    checks: list[str] = []

    def ck(name: str, condition: bool) -> None:
        if not bool(condition):
            raise ArithmeticError(name)
        checks.append(name)

    owner_hashes = {}
    for rel, expected in OWNERS.items():
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        ck("pinned owner " + Path(rel).name, actual == expected)
        owner_hashes[rel] = actual

    # Full occupation POVM in the minimal N=4, d=2 exterior lift.
    # The base compression is K=w0(I-rF); B*B=I-K*K.  B is in its
    # polar basis at the base point, while its derivative is unrestricted
    # subject to the isometry equation.
    f = sp.diag(sp.Rational(1, 4), sp.Rational(1, 3))
    df = sp.Matrix([
        [sp.Rational(2, 9), sp.Rational(1, 11)],
        [sp.Rational(1, 11), -sp.Rational(1, 13)],
    ])
    r = sp.Rational(1, 7)
    w0 = sp.Rational(3, 4)
    q = sp.eye(2) - r * f
    k = w0 * q
    dk = -w0 * r * df
    bdiag = [sp.sqrt(1 - k[i, i] ** 2) for i in range(2)]
    b = sp.diag(*bdiag)
    # Differentiate B^2=I-K^2 by its Sylvester equation.
    db = sp.Matrix(2, 2, lambda i, j: sp.cancel(
        -(k[i, i] * dk[i, j] + dk[i, j] * k[j, j])
        / (bdiag[i] + bdiag[j])
    ))
    v = k.col_join(b)
    dv = dk.col_join(db)

    expected_jet = 2 * sum(
        k[i, i] ** 2
        * sp.log(k[i, i] ** 2 / (1 - k[i, i] ** 2))
        * r / q[i, i]
        * df[i, i]
        for i in range(2)
    )

    def complete_jet(db_actual: sp.Matrix, label: str) -> None:
        dv_actual = dk.col_join(db_actual)
        ck(label + " preserves isometry to first order",
           sp.simplify(v.T * dv_actual + dv_actual.T * v) == sp.zeros(2))
        total0 = sp.S.Zero
        total1 = sp.S.Zero
        entropy_jet = sp.S.Zero
        positive = 0
        zero = 0
        for rows in combinations(range(4), 2):
            minor = v.extract(rows, [0, 1])
            dminor = dv_actual.extract(rows, [0, 1])
            amp = sp.factor(minor.det())
            damp = sp.factor(
                dminor[0, 0] * minor[1, 1]
                + minor[0, 0] * dminor[1, 1]
                - dminor[0, 1] * minor[1, 0]
                - minor[0, 1] * dminor[1, 0]
            )
            mass = sp.factor(amp ** 2)
            dmass = sp.factor(2 * amp * damp)
            total0 += mass
            total1 += dmass
            if mass == 0:
                zero += 1
                ck(label + " zero-support outcome has zero first jet " + str(rows), dmass == 0)
            else:
                positive += 1
                entropy_jet -= dmass * sp.log(mass)
        ck(label + " all six occupation outcomes normalize", sp.simplify(total0 - 1) == 0)
        ck(label + " complete-law probability derivative sums to zero", sp.simplify(total1) == 0)
        ck(label + " fixture has four positive and two born-zero outcomes", positive == 4 and zero == 2)
        ck(label + " full Shannon first jet equals weighted determinant source",
           sp.simplify(sp.expand_log(entropy_jet - expected_jet, force=True)) == 0)

    complete_jet(db, "polar-root tangent")
    # A field-dependent output polar rotation is invisible to the diagonal
    # good/bad marginals at first order, but changes the full amplitude jet.
    omega = sp.Matrix([[0, sp.Rational(2, 7)], [-sp.Rational(2, 7), 0]])
    complete_jet(db + omega * b, "admissible bad-space rotation")
    ck("noncommuting tangent retained", f * df - df * f != sp.zeros(2))

    # General product law on the positive support: every input mode selects
    # exactly one good/bad output at the isotropic reference point.
    a1, a2, a3 = sp.symbols("a1 a2 a3", positive=True)
    probs = [
        sp.prod((a if bit == 0 else 1 - a)
                for a, bit in zip((a1, a2, a3), bits))
        for bits in __import__("itertools").product((0, 1), repeat=3)
    ]
    ck("all 2^d paired outputs sum to one", sp.expand(sum(probs) - 1) == 0)

    # Golden three-coin constants and the two native AF x scene spectral blocks.
    p = (sp.sqrt(5) - 1) / 2
    p6 = p ** 6
    rg = p ** 3 / 4
    wgold = 1 - p6
    lscene = 4 * p ** 3
    q0 = sp.simplify(1 - rg * lscene)
    r0 = sp.simplify(1 - rg * (1 - p ** 12))
    ck("golden weight equals 4p^3", sp.simplify(wgold - 4 * p ** 3) == 0)
    ck("Q block is 1-p^6", sp.simplify(q0 - (1 - p ** 6)) == 0)
    ck("R block is 1-p^6-p^12", sp.simplify(r0 - (1 - p ** 6 - p ** 12)) == 0)
    ck("second AF x scene eigenvalue is 1-p^12",
       sp.simplify(lscene * (1 + p ** 6) - (1 - p ** 12)) == 0)

    # A mode has good probability a_i=|k_i|^2, not Q_i itself:
    # k_i=w0(1-r f_i) in the complete golden exterior instrument.
    ag_q = sp.simplify((wgold * q0) ** 2)
    ag_r = sp.simplify((wgold * r0) ** 2)
    kap_q = ag_q * sp.log(ag_q / (1 - ag_q))
    kap_r = ag_r * sp.log(ag_r / (1 - ag_r))
    min_k_sq = (1 - 2 * p6) ** 2
    ck("all golden mode probabilities exceed one half",
       float(sp.N(min_k_sq, 30)) > 0.5)
    ck("both retained block mean weights are positive",
       float(sp.N(kap_q, 30)) > 0 and float(sp.N(kap_r, 30)) > 0)

    sigma = sp.symbols("sigma", real=True, nonzero=True)
    cstar = 4 * p ** 11 / r0
    cm_q = sigma * 8 * p ** 6 / q0
    cm_r = sigma * 8 * p ** 12 / r0
    # Check the reweighting identity before substituting logarithmic kappa's;
    # simplifying the transcendental expression itself is needlessly costly.
    ps, qs, rs, kqs, krs, sigmas = sp.symbols(
        "p q0 r0 kappa_q kappa_r sigma", nonzero=True
    )
    symbolic_cstar = 4 * ps ** 11 / rs
    symbolic_cm_q = sigmas * 8 * ps ** 6 / qs
    symbolic_cm_r = sigmas * 8 * ps ** 12 / rs
    symbolic_weighted = (kqs * symbolic_cm_q + krs * symbolic_cm_r) / (krs * symbolic_cstar)
    symbolic_expected = 2 * sigmas * ps ** (-5) * ((kqs / krs) * rs / qs + ps ** 6)
    ck("reweighted two-block source has the stated exact coupling",
       sp.cancel(symbolic_weighted - symbolic_expected) == 0)
    lambda_expected = 2 * sigma * p ** (-5) * (
        kap_q / kap_r * r0 / q0 + p ** 6
    )

    # Numeric values are diagnostic only; exact formulas above carry the result.
    qv, rv = float(sp.N(q0, 30)), float(sp.N(r0, 30))
    wv = float(sp.N(wgold, 30))
    aqv, arv = float(sp.N(ag_q, 30)), float(sp.N(ag_r, 30))
    kqv, krv = float(sp.N(kap_q, 30)), float(sp.N(kap_r, 30))
    lmean_plus = float(sp.N(lambda_expected.subs(sigma, 1), 30))
    lmode_plus = float(sp.N(2 * p ** (-5) * (r0 / q0 + p ** 6), 30))

    return {
        "status": "PASS_EXACT_COMPLETE_SHANNON_FIRST_SOURCE",
        "checks": checks,
        "check_count": len(checks),
        "owner_sha256": owner_hashes,
        "instrument": "Gamma(W) on a filled d-mode input; complete occupation-basis readout of every d-particle output; no outcome is discarded.",
        "first_source_identity": "DH = 2 sum_i kappa(a_i) D[-log(1-r f_i)], a_i=[w0(1-r f_i)]^2, kappa(a)=a log(a/(1-a)); evaluated in a fixed output polar basis at the reference point.",
        "golden_blocks": {
            "r": "p^3/4",
            "w0": "1-p^6=4p^3",
            "Q0": "1-p^6",
            "R0": "1-p^6-p^12=1-r(1-p^12)",
            "good_probability_Q": float(sp.N(ag_q, 16)),
            "good_probability_R": float(sp.N(ag_r, 16)),
            "kappa_Q": kqv,
            "kappa_R": krv,
            "kappa_Q_over_kappa_R": kqv / krv,
            "lambda_mean_sigma_plus": lmean_plus,
            "lambda_mode_sigma_plus": lmode_plus,
            "lambda_mean_exact": "sigma*2*p^(-5)*[(kappa_Q/kappa_R)*(R0/Q0)+p^6]",
        },
        "finite_pp_root": "A+D=-2*lambda_mean*s^2 with psi=s*u, c_x=-A/2, c_y=-D/2; at s=0 this gives the exact vacuum trace A+D=0. Reverse sigma gives positive Ric_uu in the owned convention.",
        "scope": [
            "The first variation uses the entire exterior occupation law, including outcomes with zero base probability; such outcomes contribute o(||delta||), so the statement is C1, not C2.",
            "The complete occupation basis is fixed at the reference root and aligned with the polar mode pairs. Implementing and pricing that readout remains an execution premise.",
            "This is a detector-only mean-source consumer on the owned two-tick AF x scene branch. It does not establish the full same-history H+J+R price, native compulsory selection, joint preparation/clock/observer/work stationarity, physical refinement, or raw #216 closure.",
            "Existing exact finite all-row pp-wave identities are reused with the two independent spectral source blocks reweighted by positive kappa_Q and kappa_R; this checker validates the full-law first jet and coefficient algebra, not the historical 40-row lattice replay.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result["checker_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
