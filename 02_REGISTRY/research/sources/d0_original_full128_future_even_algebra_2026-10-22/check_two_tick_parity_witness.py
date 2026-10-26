#!/usr/bin/env python3
"""ORIGINAL CAR16 two-tick positivity, sharp parity discrimination horizon.

Consumes unchanged ORIGINAL fully exact modular CAR/Walsh/Julia/Kraus
source check_future_even_algebra_modprime.py in this same directory.
Mathematically NEW result: all 128 one-tick parity supertraces have
EXACT zero on this original chart (analytical CAR proof in parent note);
the fine two-tick chronological history (9,91) has a rigorously
NONZERO real/complex parity response, certified by nonzero reduction
at the original eight good split primes (especially p=1009).

Modular zeros alone would not prove a characteristic-zero zero:
the one-step statement is proved separately by the CAR factorization.
No new gate, oracle, field fit, free 65-label erasure or GR theorem.
Works with python3 and python3 -O (no disabled asserts).
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
import numpy as np

from check_future_even_algebra_modprime import (
    SPLIT_PRIMES, original_kraus_mod, effect_of_word,
)

WITNESS = (9, 91)
EXPECTED = {
    229:115, 401:83, 521:353, 709:31,
    761:380, 809:504, 941:256, 1009:593,
}
CHECKS = 0


def require(condition, description):
    global CHECKS
    CHECKS += 1
    if not bool(condition):
        raise ArithmeticError(description)


def supertrace(X, par, mod):
    return int(np.dot(par, np.diag(X)) % mod)


def matrix_product_mod(*matrices, mod):
    val = matrices[0].copy()
    for m in matrices[1:]:
        val = val @ m % mod
    return val


def main():
    actual = {}
    for data in SPLIT_PRIMES:
        q, sqrt5, p, sqrtp, sqrt_julia, sqrt_i = data
        D = original_kraus_mod(data)
        par = np.array([(-1) ** k.bit_count()
                        for k in range(16)], dtype=np.int64)
        require(len(D["K"]) == len(D["Kd"]) == 128,
                "every ORIGINAL fine Kraus and dagger column retained")
        require(len(D["even"]) == len(D["odd"]) == 8,
                "real CAR16 future parity eigenspaces 8+8")
        one = []
        for alpha in range(128):
            E = matrix_product_mod(D["Kd"][alpha], D["K"][alpha], mod=q)
            one.append(supertrace(E,par,q))
        require(one == [0]*128,
                "all ORIGINAL one-tick full128 parity supertraces zero in good reduction")

        E2 = effect_of_word(WITNESS,D)
        require(np.array_equal(E2,
                matrix_product_mod(D["Kd"][9],D["Kd"][91],
                                   D["K"][91],D["K"][9],mod=q)),
                "TRUE chronological two-tick no-DATA-reset effect K9^dag K91^dag K91 K9")
        st=supertrace(E2,par,q)
        require(st==EXPECTED[q] and st != 0,
                "EXACT algebraic nonzero two-tick parity result mod every good prime")
        ptr=int(np.trace(E2)%q)
        qplus=((ptr+st)*pow(16,-1,q))%q
        qminus=((ptr-st)*pow(16,-1,q))%q
        require((qplus-qminus)%q==(st*pow(8,-1,q))%q and qplus!=qminus,
                "same physical original Born cylinder separates both parity mixtures")

        # The ORIGINAL j>0 fine Golden pair has K_(2j+1)=sqrt(p)*L_j.
        # In predictor indices L_4->5, L_45->46. The merging takes
        # along the genuine full-record positive effect, not a reset.
        invp=pow(p,-1,q)
        L4=D["K"][8]*invp%q
        L45=D["K"][90]*invp%q
        LD4=D["Kd"][8]*invp%q
        LD45=D["Kd"][90]*invp%q
        require(np.array_equal(D["K"][9],sqrtp*L4%q) and
                np.array_equal(D["K"][91],sqrtp*L45%q),
                "literal original 128 fine odd-port labels are sqrt(p) times 65 rows")
        E65=matrix_product_mod(LD4,LD45,L45,L4,mod=q)
        require(np.array_equal(E2,p*p*E65%q),
                "EXACT original 65 merged two-tick Kraus effect scales by p²")
        require(st==(p*p*supertrace(E65,par,q))%q,
                "parity witness remains visible after paid Golden 128->65 merge")

        actual[str(q)] = {
            "full_source_primitive_parity_one_tick": "zero_all_128",
            "fine_two_tick_labels": [9,91],
            "supertrace_mod_q":st,
            "qplus_minus_qminus_mod_q":(qplus-qminus)%q,
            "65_merged_labels":[5,46],
            "65_coarse_rescaling":"1/p²",
        }

    # Independent ordinary original complex source implementation:
    # not used to certify algebraic nonzero, only to show physical signs.
    source=Path(__file__).resolve().parent.parent/"d0_native65_causal_source_2026-10-22"
    sys.path.insert(0,str(source))
    from native_excerpt import native
    K, _ = native(float(np.log(5/4)), 0.6, (1j,1j,-1.0,-1j))
    require(K.shape==(128,16,16),"source ORIGINAL actual all128 K unchanged")
    A=K[91] @ K[9]
    E=A.conj().T @ A
    par=np.diag([(-1)**k.bit_count() for k in range(16)])
    Pplus=(np.eye(16)+par)/2
    Pminus=(np.eye(16)-par)/2
    plus=float((np.trace(Pplus @ E)/8).real)
    minus=float((np.trace(Pminus @ E)/8).real)
    require(0<plus<minus and minus-plus>2.8e-11,
            "physical real-source 2tick Born distributions separated in proper order")
    require(abs((plus-minus)+2.8164178574538e-11)<1e-18,
            "original independent double precision Born source agrees with algebraic sign")
    require(abs(sum(np.trace(x.conj().T@x).real for x in K)-16)<1e-10,
            "actual 128 Kraus preserves total input trace")

    print(json.dumps({
        "status":"PASS_ORIGINAL_FULL128_SHARP_TWO_TICK_PARITY_HISTORY",
        "checks":CHECKS,
        "original_full128_native_Kraus":128,
        "same_actual_unreset_DATA":True,
        "one_tick_parity_blind":"proved by CAR decomposition; mod checks support only",
        "two_tick_parity_separating_word":[9,91],
        "modular_good_prime_nonzero_certificates":actual,
        "actual_Born_even":plus,
        "actual_Born_odd":minus,
        "actual_parity_probability_difference":plus-minus,
        "same_original_65_predictor_Golden_cost_retained":True,
        "general_complete_PARITY_M8_plus_M8_tomography_horizon_proved_minimal":False,
        "physical_compulsory_original_Book_action_selected":False,
        "GR_closed":False,
    },sort_keys=True,indent=2))


if __name__=="__main__":
    main()
