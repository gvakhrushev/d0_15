#!/usr/bin/env python3
"""Literal original G/CX/SourceI native corpus witness:
two actual complete N=51 programmes have exactly the same primitive
inventory AND the same 1589-byte canonical_json code length, but DIFFERENT
whole Book H+J prices. Their lexical code order is opposite the Book order.

Uses unchanged source-owned native_execution.py and native_echo.py.
This is a proof of failure for a particular naive program-serialization
proxy, NOT a counterexample to physical D_min on one equivalent goal/future
history; the programmes have distinct actual return/future effects.

No new D0 gate, information price, equal-goal assumption, GR conclusion.
Run both python3 and python3 -O.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

import sympy as sp

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/"d0_native_bilinear_return_echo_2026-10-25"))
import native_echo as echo

native=echo.native
CHECKS=0

def require(ok,msg):
    global CHECKS
    CHECKS+=1
    if not bool(ok):
        raise ArithmeticError(msg)

def main():
    w21=echo.echo(2,1,stages=51)
    w12=echo.echo(1,2,stages=51)
    code21=native.canonical_json(w21)
    code12=native.canonical_json(w12)
    inv21=native.inventory(w21,**echo.BOUNDS)
    inv12=native.inventory(w12,**echo.BOUNDS)
    require(inv21.gate_count==inv12.gate_count==51,
            "REAL same native full forward/inverse 51-stage clock")
    require(inv21.g_count==inv12.g_count==6,
            "same REAL Golden primitive count")
    require(inv21.cx_count==inv12.cx_count==29,
            "same REAL CX primitive count INCLUDING paid padding")
    require(inv21.source_i_count==inv12.source_i_count==16,
            "same REAL SourceI primitive count")
    require(w21.qubits==w12.qubits==5 and
            w21.blank_wires==w12.blank_wires==(0,1) and
            w21.source_spin==w12.source_spin==(3,4) and
            w21.old_right==w12.old_right==(),
            "same original closed source inventory, blanks, spin and input domain")
    require(len(code21.encode("utf-8"))==
            len(code12.encode("utf-8"))==1589,
            "EXACT equality of literal source-owned compact UTF8 code lengths")
    require(code21!=code12 and code21<code12,
            "literal lexicographic code tie-break chooses (2,1)")
    counts21=Counter(g.op for g in w21.gates)
    counts12=Counter(g.op for g in w12.gates)
    require(counts21==counts12==Counter({"G":6,"CX":29,"SourceI":16}),
            "both real native words have identical entire inventory")
    require(w21.gates!=w12.gates,
            "identical inventory does NOT erase physically different word")

    p=native.P
    z=sp.Rational(1,2**20)
    E1=p*p
    E2=4*p**3
    L=lambda x:4*x*(1-x)
    A=lambda E,b:L(E)+L(b)-L(E)*L(b)
    require(sp.simplify(L(E1)-E2)==0,
            "exact Golden p+p²=1 ties the first branch to E2")
    require(sp.simplify(A(E2,E1)-A(E1,E2))==0,
            "both actual logical return FIRST bands are identical")
    B21=L(E1)
    B12=L(E2)
    exact_difference=sp.simplify(B21-B12)
    require(exact_difference==600-268*sp.sqrt(5),
            "exact native CAR/Golden second-feedback-band source gap")
    # 600 - 268sqrt5 = 4(150 - 67sqrt5)>0 because
    # 150^2 = 22500 > 67^2*5 = 22445.
    require(150**2>67**2*5 and bool(exact_difference>0),
            "native second-band strict price ordering is CERTIFIED algebraically")
    require(bool(1-z*B21>0) and bool(1-z*B12>0),
            "true zeta-return log determinant regular on both words")
    # Actual full paired-clock heat is the SAME by conjugacy to the
    # one native involutive middle and common N=51: see source PROOF §3.
    # Four spin replicas of both actual feedback bands remain paid.
    J21=-4*(sp.log(1-z*A(E2,E1))+sp.log(1-z*B21))
    J12=-4*(sp.log(1-z*A(E1,E2))+sp.log(1-z*B12))
    exact_logdiff=sp.simplify(J21-J12)
    require(bool(sp.N(exact_logdiff,40)>0),
            "whole original native paired Book J21 > J12")
    require(bool(J21!=J12),
            "equal gate histogram cannot determine finite Book price")
    require(code21<code12 and bool(sp.N(J21-J12,40)>0),
            "fixed naive code lex order is OPPOSITE complete Book J order")

    print(json.dumps({
        "status":"PASS_ORIGINAL_TWO_NATIVE_WORDS_EQUAL_CODE_LENGTH_DIFFERENT_BOOK_PRICE",
        "checks":CHECKS,
        "original_source_native_echo":"d0_native_bilinear_return_echo_2026-10-25/native_echo.py",
        "original_execution_grammar":"d0_native_execution_domain_2026-10-24/native_execution.py",
        "same_full_native_N":51,
        "both_canonical_json_bytes":len(code21.encode("utf-8")),
        "each_native_inventory":dict(counts21),
        "native_logical_B21_minus_B12":str(exact_difference),
        "full_Book_21_minus_12_at_fixed_heat":str(sp.N(exact_logdiff,24)),
        "literal_JSON_tie_lex_winner":"(2,1)",
        "Book_H_plus_J_winner":"(1,2)",
        "same_required_future_task_proved":False,
        "JSON_is_D_min_universal_code_proved":False,
        "physical_full_price_selection_proved":False,
        "GR_closed":False
    },sort_keys=True,indent=2))

if __name__=="__main__":
    main()
