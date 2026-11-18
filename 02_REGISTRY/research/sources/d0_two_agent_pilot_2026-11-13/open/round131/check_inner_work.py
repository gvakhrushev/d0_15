"""Replay the primary addressed comparator and price discrimination at its fixed mark."""

from collections import Counter
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import mpmath as mp
import numpy as np
import sympy as sp

REPO = Path(__file__).resolve().parents[6]
COMMIT = "15f5b786ed912a0e91d660e337bf60a7c15c7cfa"
OWNER = "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
NATIVE = REPO / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
PRIMARY_SHA = "561dfba7503c86b2fdf20e121be44681ac98d9ca9759d59150cc1e864b0fb03b"
NATIVE_SHA = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"


def require(condition, reason):
    if not bool(condition):
        raise AssertionError(reason)


def load_comparator():
    source = subprocess.check_output(["git", "show", f"{COMMIT}:{OWNER}"], cwd=REPO)
    fence = bytes([96]) * 3
    marker = b"7ef SEVEN REFERENCE CHECKER"
    raw = source.split(b"<!-- BEGIN " + marker + b" -->\n" + fence + b"python\n")[1]
    raw = raw.split(fence + b"\n<!-- END " + marker + b" -->")[0]
    require(sha256(raw).hexdigest() == PRIMARY_SHA, "Unexpected primary comparator")
    require(sha256(NATIVE.read_bytes()).hexdigest() == NATIVE_SHA, "Unexpected literal gate alphabet")
    sys.path.insert(0, str(NATIVE.parent))
    import native_execution as native

    # Change only the Python implementation of population count for compatibility.
    raw = raw.replace(b"w.bit_count()", b'bin(w).count("1")')
    raw = raw.replace(b"(g&b).bit_count()", b'bin(g&b).count("1")')
    tree = ast.parse(raw)
    constants = {"PORT", "SPIN", "terms", "selectors"}
    routines = {"ready", "report", "gate", "z_word", "rot_small", "predicate", "inverse_predicate"}
    selected = [
        node for node in tree.body
        if (isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id in constants for t in node.targets))
        or (isinstance(node, ast.FunctionDef) and node.name in routines)
    ]
    data = {"need": require, "np": np, "ne": native, "Counter": Counter}
    exec(compile(ast.Module(body=selected, type_ignores=[]), f"{OWNER}#7ef", "exec"), data)
    return data, native


def verify_comparator():
    data, native = load_comparator()
    forward, _ = data["predicate"]()
    inverse = data["inverse_predicate"]()
    port, report = data["PORT"], data["report"]
    inventory = Counter(g.op for g in forward)
    require(inventory == {"G": 5888, "CX": 4096, "SourceI": 8192},
            "The actual predicate inventory changed")
    require(Counter(g.op for g in inverse) == inventory, "The actual paid inverse changed")
    addresses = Counter(g.wires for g in forward + inverse if g.op == "CX")
    counts = [addresses[(report(j), port)] for j in range(7)]
    require(counts == [256, 256, 1024, 2048, 256, 256, 1024],
            "The field operands have different actual REPORT controls")

    # The first four listed blocks give precisely the matching y/f/0 comparison.
    data["terms"] = data["terms"][:4]
    data["selectors"] = data["selectors"][:4]
    y_body, _ = data["predicate"]()
    y_inverse = data["inverse_predicate"]()
    y_counts = Counter(g.wires for g in y_body+y_inverse if g.op == "CX")
    require(y_counts[(report(2), port)] == y_counts[(report(3), port)] == 1024,
            "The matched reference is not equally used")

    # The existing 0/10 writer acts on a truly born tail, without zero blanks.
    p, a = native.P, native.A
    v = sp.Matrix([a, p])
    g = sp.Matrix(native.G_LOCAL)
    sx = sp.Matrix([[0, 1], [1, 0]])
    require(native.exact_matrix_equal(sx*g*sx*v, sp.Matrix([1, 0])),
            "The return branch is not the valid original 10 container")
    require(native.exact_matrix_equal(g*v, sp.Matrix([p**3, 2*a*p])),
            "The direct branch does not preserve its real unused tail")
    return dict(inventory), counts


def verify_conditioning():
    a, b, q, left, right = sp.symbols("A B q q_minus q_plus", positive=True)
    conditional = a*q / (a*q + b*(1-q))
    expected = a*b/(a*q + b*(1-q))**2
    require(sp.cancel(sp.diff(conditional, q) - expected) == 0, "Wrong same-output jet")
    secant = a*b*(right-left)/((a*right+b*(1-right))*(a*left+b*(1-left)))
    require(sp.cancel(conditional.subs(q, right)-conditional.subs(q, left)-secant) == 0,
            "Wrong same-output finite contrast")
    return "A*B/(A*q+B*(1-q))^2"


def verify_n1_bound():
    iv = mp.iv
    iv.dps = 60
    p = (iv.sqrt(5)-1)/2
    s = 4*p**3
    z = iv.mpf(1)/2**20
    r = z*(3*s-s*s)-z*z*s*(2*s-s*s)
    ell = -iv.ln(p)
    h = -((1-r)*iv.ln(1-r)+r*iv.ln(r))/ell
    bounds = ((1, "27.42997215", "27.42997217"), (2, "13.71495876", "13.71495877"))
    for exponent, lower, upper in bounds:
        threshold = (-iv.ln(r)/ell - (exponent+1)*h)/(exponent*(1-r))
        require(iv.mpf(lower) < threshold and threshold < iv.mpf(upper),
                "Original flat N1 sibling cost threshold lost its strict interval")
    return {e: [lo, hi] for e, lo, hi in bounds}


def main():
    inventory, counts = verify_comparator()
    print(json.dumps({
        "status": "PASS",
        "primary_commit": COMMIT,
        "primary_checker_sha256": PRIMARY_SHA,
        "native_gate_sha256": NATIVE_SHA,
        "one_direction_predicate_inventory": inventory,
        "both_direction_report_controls_y_plus_y_minus_f_ref_x_plus_x_minus_q": counts,
        "matched_f_and_reference_controls": [1024, 1024],
        "same_registered_outcome_occupation_slope_in_q": verify_conditioning(),
        "n1_nonnegative_info_minimum_total_sibling_gap": verify_n1_bound(),
        "book03_occupation_price_selected": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
