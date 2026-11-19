#!/usr/bin/env python3
"""Exact original unpadded42 -> fixed-P input lift, with read-only replay.

Default: recompute the new preparation interval bounds and compare RESULT.json.
Only an explicit --output PATH writes a receipt. The old 42x42 field Hessian
certificate is byte-pinned and consumed, not expensively recomputed here.

Run from any directory in a normal repository checkout:
    python3 path/to/check_joint_input_lift.py
or supply its root explicitly with --repo PATH. Dependency: mpmath 1.3.0;
NumPy/SciPy are not used by this rigorous path.
"""
from __future__ import annotations

import argparse
import base64
from decimal import Decimal, getcontext
import hashlib
import importlib.util
import json
from math import factorial
from pathlib import Path
import sys
import zlib

import mpmath
from mpmath import iv

HERE = Path(__file__).resolve().parent
PINNED_COMMIT = "af6e7eb8952564d86ddbfe910eb5f41d4a1b4e4b"
SOURCES = "02_REGISTRY/research/sources/"
PINS = {
    "model": (SOURCES + "d0_full42_interval_banach_2026-10-22/certified_model.py",
              "6d5b41ce11a941fde95e722e708ebb02d689985c"),
    "inputs": (SOURCES + "d0_full42_interval_banach_2026-10-22/inputs.py",
               "2c12d84fb3454dbf3cda6d71852d0cd4e57e1f65"),
    "unpadded_price": (SOURCES + "d0_original_unpadded42_2026-10-22/certified_unpadded.py",
                       "a8bcb1a32be09d1b45b8626278e014e7288bce2f"),
    "center": (SOURCES + "d0_original_unpadded42_2026-10-22/center_new.json",
               "6b520fbd6218444601d90d7e30b738f8c828bd22"),
    "field_root_receipt": (SOURCES + "d0_original_unpadded42_2026-10-22/RESULT.json",
                           "0ac76b58522d84f5bcc787fb6b6da0c99e1211cd"),
}


def require(condition, name):
    if not condition:
        raise RuntimeError(name)


def gitblob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def locate_repo(explicit):
    if explicit is not None:
        root = explicit.resolve()
        require((root / PINS["model"][0]).is_file(),
                "--repo must contain the original source directories")
        return root
    for root in HERE.parents:
        if (root / PINS["model"][0]).is_file():
            return root
    raise RuntimeError("Original sources not found; use --repo REPOSITORY_ROOT")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "module loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_original(root):
    raw, provenance = {}, {}
    for key, (relative, expected) in PINS.items():
        data = (root / relative).read_bytes()
        require(gitblob(data) == expected, "Exact original Git blob mismatch: " + relative)
        raw[key] = data
        provenance[key] = {"path": relative, "git_blob": expected,
                           "sha256": hashlib.sha256(data).hexdigest()}
    # Pinned source imports 'inputs'; bind that name to the checked file before
    # loading the original model, avoiding accidental imports from the cwd.
    inputs = load_module("inputs", root / PINS["inputs"][0])
    recovered = {}
    for name, encoded in (("rational_collar.json", inputs._COLLAR),
                          ("rational_center.json", inputs._CENTER)):
        data = zlib.decompress(base64.b64decode(encoded))
        require(hashlib.sha256(data).hexdigest() == inputs._SHA[name],
                "Explicit original rational input digest: " + name)
        recovered[name] = json.loads(data)
    center = json.loads(raw["center"])
    require(len(center["z42"]) == 42, "Original 42-dimensional rational center")
    require(center["h"] == recovered["rational_collar.json"]["h"],
            "Exact original collar/center mesh equality")
    receipt = json.loads(raw["field_root_receipt"])
    require(receipt["status"] == "PASS_LOCAL_OUTWARD_INTERVAL_BANACH_ORIGINAL_UNPADDED_42_ROOT",
            "Consumed original field-root status")
    cert = receipt["certificate"]
    require(cert["original_full_Hessian_entries"] == 1764, "Consumed full field Hessian")
    require(cert["real_exact_root_ball_radius_infinity"] == "1e-24", "Consumed exact ball")
    require(cert["certified_new_Banach_contraction_infinity"] == "<0.036600",
            "Consumed strict contraction")
    require(all(value is False for value in receipt["assumptions_open"].values()),
            "Preserve original physical-scope flags")
    original = load_module("_pinned_original_cq", root / PINS["model"][0])
    return original.CQ, center, provenance


def enclosure(x):
    return iv.nstr(x, 45)


def compute(root):
    require(mpmath.__version__ == "1.3.0", "Replay uses mpmath 1.3.0")
    getcontext().prec = 160
    iv.dps = 90
    CQ, center, provenance = load_original(root)
    model = CQ(iv)
    radius = Decimal("1e-24")
    ball = [iv.mpf([str(Decimal(t)-radius), str(Decimal(t)+radius)])
            for t in center["z42"]]
    # Explicitly retain the original interval exponential proof guards even
    # when Python -O removes assertions inside the byte-pinned old module.
    require(2*10**120 < factorial(31)*2048**31, "Exact original exponential tail")
    for r in range(4):
        X = iv.zeros(4)
        for k in range(6):
            X += model.h * ball[16+6*r+k] * model.L[k]
        norm = max(sum((abs(X[i,j]).b for j in range(4)), iv.mpf(0))
                   for i in range(4))
        require(norm < 1, "Original whole-box link exponential domain")
    e, U, ps = model.nodes(ball)
    sites = []
    for j in (0, 1):
        co = model.E[0] if j == 0 else e
        us = model.U[0] if j == 0 else U
        vs = U if j == 0 else model.U[2]
        f = model.curvature(co, us, vs).real
        gi = (co.T*model.eta*co)**-1
        material = iv.mpf(0)
        for a in (0, 1):
            v = iv.matrix([(ps[j+1][a]-ps[j][a])/model.h,
                           model.amp if a == 1 else iv.mpf(0), 0, 0])
            material += (v.T*gi*v)[0]
        x, y = -model.tau*f, model.tau*material
        E = model.p**2*(1+x)
        ell = 4*E*(1-E)
        b = model.p-model.p**2*y
        B = 4*b*b*(1-b*b)
        A = ell+(1-ell)*B
        gap = A-B
        dplus, dminus = 1-model.Z*A, 1-model.Z*B
        r = model.Z*(A+B)-model.Z**2*A*B
        hp = iv.log((1-r)/r)/model.lp
        Fprime = model.norm*(hp-1)
        plus_eig = -2*model.Z*gap*dminus*Fprime
        minus_eig = 2*model.Z*gap*dplus*Fprime
        normal_plus = -2*model.Z*Fprime*dminus*iv.sqrt(A*(1-A))
        normal_minus = -2*model.Z*Fprime*dplus*iv.sqrt(B*(1-B))
        require(E.a > 0 and E.b < 1, "Strict original E chart")
        require(B.a > 0 and B.b < 1, "Strict original B chart")
        require(A.a > B.b and A.b < 1, "Strict distinct input eigenbands")
        require(gap.a > iv.mpf(".0526"), "Uniform preparation eigenband gap")
        require(r.a > 0 and r.b < model.p**2, "True unpadded price slope")
        require(Fprime.b < 0, "Negative normalized unpadded input slope")
        require(plus_eig.a > 100 and minus_eig.b < -100,
                "All eight preparation Hessian eigenvalues separated from zero")
        require(normal_plus.a > 0 and normal_minus.a > 0,
                "All four ambient normal reactions nonzero")
        sites.append({
            "site": j, "E": enclosure(E), "b_amplitude": enclosure(b),
            "A": enclosure(A), "B": enclosure(B), "A_minus_B": enclosure(gap),
            "r": enclosure(r), "normalized_unpadded_Fprime": enclosure(Fprime),
            "prep_H_plus_eigenvalue_multiplicity_2": enclosure(plus_eig),
            "prep_H_minus_eigenvalue_multiplicity_2": enclosure(minus_eig),
            "ambient_normal_plus_norm": enclosure(normal_plus),
            "ambient_normal_minus_norm": enclosure(normal_minus),
        })
    return {
        "status": "PASS_ORIGINAL_UNPADDED42_FIXED_P_INPUT_LIFT",
        "input_commit": PINNED_COMMIT,
        "source_pins": provenance,
        "source_byte_rule": "Exact canonical original Git blobs; no newline or content normalization",
        "mpmath_version": mpmath.__version__,
        "field_root_existence": "Consumed original exact 42-root certificate, not replayed",
        "field_root_ball_inf": "1e-24",
        "outward_arithmetic": "mpmath.iv at 90 decimal digits; original rigorous matrix exponential",
        "complex_fixed_P_prep_real_dimension": 8,
        "conditional_joint_dimension": 50,
        "real_fixed_P_prep_dimension": 4,
        "real_conditional_joint_dimension": 46,
        "prep_H_inertia_negative_zero_positive": [4, 0, 4],
        "uniform_prep_H_min_abs_eigenvalue_gt": 100,
        "mixed_field_prep_H": "Exactly zero by the constant stationary section, not a numerical tolerance",
        "ambient_four_CP7_input_real_dimension": 56,
        "fixed_P_normal_real_constraints": 48,
        "sites": sites,
        "whole_native_input_domain_admitted": False,
        "whole_Book03_price_selected": False,
        "J2_independent_input_extension_proved": False,
        "new_field_root_certified_here": False,
        "GR_closed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, help="Repository root; auto-detected by default")
    parser.add_argument("--receipt", type=Path, default=HERE/"RESULT.json",
                        help="Reviewed receipt to verify without writing")
    parser.add_argument("--output", type=Path,
                        help="Explicitly regenerate a receipt at this path instead of verifying")
    args = parser.parse_args()
    result = compute(locate_repo(args.repo))
    if args.output is not None:
        args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
        mode = "EXPLICIT_RECEIPT_REGENERATION"
    else:
        require(args.receipt.is_file(), "Reviewed receipt missing; use --output only to author it")
        expected = json.loads(args.receipt.read_text(encoding="utf-8"))
        require(result == expected, "Recomputed result differs from reviewed receipt; no file changed")
        mode = "READ_ONLY_REVIEWED_RECEIPT_VERIFIED"
    print(json.dumps({"status": result["status"], "mode": mode,
                      "conditional_joint_dimension": 50,
                      "uniform_prep_H_min_abs_eigenvalue_gt": 100,
                      "prep_H_inertia_negative_zero_positive": [4, 0, 4],
                      "whole_native_input_domain_admitted": False,
                      "whole_Book03_price_selected": False, "GR_closed": False}, indent=2))


if __name__ == "__main__":
    main()
