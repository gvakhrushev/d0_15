#!/usr/bin/env python3
"""Exact original native four-word test; not physical X_N admission.

Run from the repository root, or pass --repo PATH.  No assertions: the exact
checks execute unchanged under python -O.  The all-mode heat is bounded by
the proof, not numerically truncated or replaced by a cut heat.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import factorial, log1p, sqrt
import argparse
import hashlib
import importlib.util
import json
import sys

import sympy as S
from sympy.polys.matrices import DomainMatrix


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    args = ap.parse_args()
    root = args.repo.resolve()
    source = root / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
    pin = hashlib.sha256(source.read_bytes()).hexdigest()
    require(pin == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c", "native owner changed")
    spec = importlib.util.spec_from_file_location("native_retained_memory", source)
    n = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = n
    spec.loader.exec_module(n)

    def eq(A, B):
        return DomainMatrix.from_Matrix(S.Matrix(A-B)).convert_to(n.GOLDEN_FIELD).is_zero_matrix

    X = n.Gate("SourceI", (0, 1, 2))
    G = n.Gate("G", (0,))
    macro = {1: (X, X, X, X, G), -1: (X, X, G, X, X)}

    def execution(word):
        return n.Execution(4, (0,), (3,), tuple(word), n.G_CX_SOURCE_I, 0, (1, 2))

    params = dict(max_qubits=4, max_expanded_stages=1000)
    eG, eX = execution((G,)), execution((X,))
    GM = S.Matrix(n.word_matrix(eG, **params))
    XM = S.Matrix(n.word_matrix(eX, **params))
    I = S.eye(16)
    require(eq(XM**4, I), "paid X^4 is not identity")
    require(eq(XM**2 * GM * XM**2, GM.T), "original inverse identity")
    require(eq(GM.T*GM, I), "original Golden gate orthogonality")
    ips = S.Matrix(n.input_isometry(eG, **params))
    P = ips*ips.T
    require(P.trace() == 8, "actual free input rank")
    alpha = 4*n.P**3
    require(S.simplify(alpha-(4*S.sqrt(5)-8)) == 0, "exact return factor")
    rows = []
    for L in (1, 2, 4):
        counts = []
        for sigma, tau in ((1,1), (1,-1), (-1,1), (-1,-1)):
            word = macro[sigma] + (X,)*(4*L) + macro[tau] + (X,)*(4*L)
            ex = execution(word)
            n.validate_execution(ex, **params)
            inv = n.inventory(ex, **params)
            require((inv.gate_count, inv.g_count, inv.source_i_count,
                     inv.cx_count, inv.cut_rank, inv.full_dimension)
                    == (10+8*L, 2, 8+8*L, 0, 8, 16), "actual inventory")
            U = S.Matrix(n.word_matrix(ex, **params))
            target = GM**2 if sigma+tau == 2 else (GM.T**2 if sigma+tau == -2 else I)
            require(eq(U, target), "full-column endpoint differs")
            require(eq(U.T*U, I), "full-column orthogonality")
            C = (I-P)*U*P
            F = C.T*C
            expected = alpha*P if sigma == tau else S.zeros(16)
            require(eq(F, expected), "original full feedback F")
            require(eq(ips.T*F*ips, alpha*S.eye(8) if sigma == tau else S.zeros(8)), "compressed original return")
            counts.append((inv.gate_count, inv.g_count, inv.source_i_count))
        require(len(set(counts)) == 1, "inventories not identical")
        rows.append({"L":L,"N":10+8*L,"full_dimension":16,"cut_rank":8,
                     "four_full_column_endpoints": "G^2,I,I,G^-2",
                     "four_full_feedbacks": "4p^3 P,0,0,4p^3 P"})

    # Exact tail and derivative bounds. beta=3-sqrt5 lies in (1/2,1).
    require(Q(2)**2 < 5 < Q(5,2)**2, "beta interval")
    exp1_upper = Q(5,2) + Q(1,6)/(1-Q(1,4))
    require(exp1_upper < 3, "exp(beta)<3 rational majorant")
    require(Q(89,40)**2 < 5, "A=4sqrt5-8 > 9/10")
    z = Q(1, 2**20)
    r = 8
    N0 = 18
    error = Q(24*(N0+1), N0*factorial(N0))
    normalized_error = error/(r*z)
    require(normalized_error < Q(1,100), "native full B contrast lower bound")
    require(Q(9,5)-normalized_error > Q(179,100), "uniform normalized contrast >1.79")
    # b_N=(N+1)/(N N!) strictly decreases for every N>=2:
    # b_(N+1)/b_N=N(N+2)/(N+1)^3<1, since difference=N^3+2N^2+N+1>0.
    t1 = Q(N0,(N0-1)*factorial(N0))
    t2 = Q(N0*N0,(N0*N0-N0-1)*factorial(N0))
    hessian_bound = 6*t2+18*t1*t1
    require(hessian_bound < Q(11,10**16), "full thermal Hessian bound")
    require(hessian_bound/(r*z) < Q(1,100), "relative thermal Hessian bound")
    # The negative feedback Hessian is < -3 r z/2; 0<A<1 and A>9/10.
    require(z/(1-z)**2 < Q(1,10), "feedback Hessian sign margin")
    require(-Q(3,2)+hessian_bound/(r*z) < -Q(149,100), "full ambient mixed Hessian sign")

    pf = (sqrt(5)-1)/2
    af = 4*pf**3
    zf = float(z)
    cj = -2*r*log1p(-zf*af)
    f2 = 2*zf*(1-2*af)/(1-zf*af) + 4*zf*zf*af*(1-af)/(1-zf*af)**2
    print(json.dumps({
        "status":"PASS",
        "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "native_owner_sha256":pin,
        "actual_native_words":rows,
        "all_raw_stages_paid":True,
        "all_unknown_spin_and_oldRIGHT_columns_retained":True,
        "price":"unchanged H+J on declared INTERNAL incidence or fixed default tensor heat",
        "heat_grades":"H0 and H01; index 359 N d remains inside logarithm",
        "exact_four_corner_return":"-2 r log(1-4 z p^3)",
        "return_contrast_float":cj,
        "return_contrast_over_r_z_float":cj/(r*zf),
        "full_heat_contrast_error_bound_at_N18":str(error),
        "full_heat_contrast_error_float":float(error),
        "relative_full_heat_contrast_error_float":float(normalized_error),
        "uniform_full_price_contrast_over_r_z_lower":"179/100 for all L>=1",
        "ambient_full_heat_mixed_hessian_bound":str(hessian_bound),
        "ambient_full_heat_mixed_hessian_bound_float":float(hessian_bound),
        "ambient_feedback_mixed_hessian_float":r*f2,
        "ambient_full_mixed_hessian_over_r_z_upper":"-149/100 for all L>=1",
        "full_Hodge_numeric_diagonalization":False,
        "physical_continuous_gate_admission":False,
        "metric_or_spatial_locality_no_go":False,
        "scope":"rules out bounded clock-range gate-only elimination of shared retained memory; no physical task selection, geometric gain, continuum or HDA closure",
        "GR_closed":False,
    },indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
