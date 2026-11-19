#!/usr/bin/env python3
"""Exact native-interface checks; default read-only, no historical run().

Consumes literal full16 CAR and actual64 row definitions. Proves the finite
CAR expression for the existing Lorentz-star pairing, and tests the two
specific obstructions to composing the configured price with stored v8.
An algebraic word identity is not physical admission or a GR derivation.
"""
from __future__ import annotations

import argparse
import ast
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import platform

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RESEARCH = ROOT / "02_REGISTRY/research"
CURVED = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
ROWS = "sources/d0_complete_record_channel_2026-10-17/check_flat_relaxation.py"
PINS = {
    "certificates/a4d_native_curved_soldered_heat.py": "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
    ROWS: "0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9",
    "A4D_NATIVE_AUTONOMOUS_SCENE_RECORD.md": "b9ee5c65cd94cd22760d49eef2d6f30d1d7eeb48e8afff2ee5188f61038a5539",
    "A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md": "7b82d30d0d8ec451f768bf0b92aa0e4daaad1f2600497ae7d855bf370c96a338",
    "A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md": "a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915",
}
CHECKS = []


def require(name, condition):
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def equal(name, actual, expected):
    difference = actual - expected
    entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
    require(name, all(s.cancel(s.expand(x)) == 0 for x in entries))


def literal_inputs():
    for path, digest in PINS.items():
        require("pin:" + path, hashlib.sha256((RESEARCH / path).read_bytes()).hexdigest() == digest)
    nodes = [n for n in ast.parse((RESEARCH / ROWS).read_text()).body
             if isinstance(n, ast.FunctionDef) and n.name in {"_creators", "_native_rows"}]
    require("only_two_literal_helpers", len(nodes) == 2)
    scope = {"s": s, "ast": ast, "lru_cache": lru_cache, "CURVED": CURVED}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), ROWS, "exec"), scope)
    C, order = scope["_creators"](ROOT)
    require("actual_exterior_order", order == (0, 2, 3, 1))
    return C, order, scope["_native_rows"]


def exterior(P, order):
    """Full exterior lift in the actual A,C,D,B basis, including grades0,4."""
    indices = [[i for i in order if mask & (1 << i)] for mask in range(16)]
    U = s.zeros(16)
    for i, rows in enumerate(indices):
        for j, cols in enumerate(indices):
            if len(rows) == len(cols):
                U[i, j] = P.extract(rows, cols).det() if rows else 1
    return U


def geometric_words(C, order):
    I, O, eta = s.eye(16), s.zeros(16), s.diag(1, -1, -1, -1)
    gamma = [C[i] + eta[i, i] * C[i].H for i in range(4)]
    chi = gamma[0] * gamma[1] * gamma[2] * gamma[3]
    for i in range(4):
        for j in range(4):
            equal(f"Lorentz_CAR:{i}:{j}", gamma[i]*gamma[j]+gamma[j]*gamma[i], 2*eta[i, j]*I)
    pairs = list(combinations(range(4), 2))

    def lie_lift(R):
        return sum((R[i,j]*C[i]*C[j].H for i in range(4) for j in range(4)), O)

    def star(v, w, R):
        B = R * eta
        return sum(s.LeviCivita(a,b,c,d)*(v[a]*w[b]-v[b]*w[a])*B[c,d]
                   for a,b in pairs for c,d in pairs)

    for c,d in pairs:
        B = s.zeros(4); B[c,d] = 1; B[d,c] = -1
        R = B * eta
        lifted = lie_lift(R)
        for a in range(4):
            for b in range(4):
                equal(f"star_basis:{a}:{b}:{c}:{d}",
                      -s.trace(chi*gamma[a]*gamma[b]*lifted)/8,
                      star(s.eye(4)[:,a],s.eye(4)[:,b],R))

    B=s.zeros(4); B[2,3]=1; B[3,2]=-1
    query=chi*gamma[0]*gamma[1]*lie_lift(B*eta)
    equal("vacuum_query_expectation_zero", query[0,0], 0)
    equal("same_query_trace_nonzero", s.trace(query), -8)

    # Finite, noninfinitesimal, commuting boost and spatial rotation.
    P = s.Matrix([[s.Rational(5,4),s.Rational(3,4),0,0],
                  [s.Rational(3,4),s.Rational(5,4),0,0],
                  [0,0,s.Rational(3,5),-s.Rational(4,5)],
                  [0,0,s.Rational(4,5),s.Rational(3,5)]])
    equal("proper_Lorentz_test", P.T*eta*P, eta)
    equal("proper_orientation", P.det(), 1)
    U, Ui = exterior(P,order), exterior(P.inv(),order)
    equal("full_exterior_inverse", U*Ui, I)
    for i in range(4):
        equal(f"actual_CAR_covariance:{i}", U*C[i]*Ui,
              sum((P[j,i]*C[j] for j in range(4)), O))
    R = (P-P.inv())/2
    word = sum(((U*C[i]*Ui-Ui*C[i]*U)*C[i].H/2 for i in range(4)), O)
    equal("eight_conjugation_words", word, lie_lift(R))
    require("not_naive_exterior_odd_part", word != (U-Ui)/2)
    bad = sum(((U*C[i]*U.H-U.H*C[i]*U)*C[i].H/2 for i in range(4)), O)
    require("inverse_not_positive_adjoint", bad != word)
    for a,b in pairs:
        equal(f"finite_plaquette_star:{a}:{b}", -s.trace(chi*gamma[a]*gamma[b]*word)/8,
              star(s.eye(4)[:,a],s.eye(4)[:,b],R))
    # Exact pp-wave loop; no positive form can make a nonidentity unipotent unitary.
    null_eta = s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    N=s.zeros(4); N[1,2]=1; N[2,0]=1
    k=s.Rational(1,5); Pp=s.eye(4)+k*N+k*k*N*N/2
    equal("null_rotation_Lorentz", Pp.T*null_eta*Pp, null_eta)
    equal("null_rotation_nilpotent", (Pp-s.eye(4))**3, s.zeros(4))
    require("null_rotation_nonidentity", Pp != s.eye(4))
    equal("null_rotation_all_eigenvalues_one", Pp.charpoly().as_expr(),
          (Pp.charpoly().gen-1)**4)


def common_car_obstruction(C, native_rows):
    I=s.eye(16); beta=C[0]+C[0].H; Pm=I-C[0]*C[0].H
    rows, _, _=native_rows(C,s.Rational(3,5),s.Rational(4,5),[-1,1,1,1])
    N={(label,coefficient):row for label,coefficient,row in rows}
    equal("all64_rows_normalized", sum((M*M.H for M in N.values()),s.zeros(16)), I)
    A=-s.Rational(3,40)*beta
    equal("actual_blank_row", N[0,0], A)
    equal("actual_flip_row", N[4,1], s.Rational(9,10)*I)
    p=s.Symbol("p",positive=True)
    equal("actual_blank_Kraus", I-2*p*p*A*A, (1-9*p*p/800)*I)
    equal("actual_flip_Kraus", -2*s.sqrt(p)*p*N[4,1].H*A, 27*s.sqrt(p)*p*beta/200)
    equal("CAR_exchanges_scene_cut", beta*Pm*beta, I-Pm)
    pe=(s.sqrt(5)-1)/2
    L=4*pe**3; L3=1-(130*pe-81)**2; Lv=1-((854*pe-531)/11)**2
    for name,value in [("L",L),("L3",L3),("Lv",Lv)]:
        require("strict_scene_effect_"+name, bool(value>0) and bool(value<1))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,help="Explicit opt-in receipt; default read-only")
    args=parser.parse_args()
    C,order,native_rows=literal_inputs()
    geometric_words(C,order)
    common_car_obstruction(C,native_rows)
    result={"status":"PASS","input_commit":"c14e587ca1a344e7faaee03e1e46053d8b440950",
            "python":platform.python_version(),"sympy":s.__version__,
            "checks":CHECKS,"check_count":len(CHECKS),"source_sha256":PINS,
            "scope":"Full16 CAR star identity; stored-unitary and conditional-scene gluing obstructions",
            "physical_admission":False,"native_price_selection":False,"gr_closure":False}
    text=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text,end="")


if __name__=="__main__":
    main()
