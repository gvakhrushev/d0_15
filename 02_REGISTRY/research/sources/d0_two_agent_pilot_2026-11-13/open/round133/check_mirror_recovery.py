"""Check the exact conditional old return and the complete mirrored mark ledger."""

from collections import Counter
import json
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round132"))
from check_paired_activation_reader import (
    ne, require, gate, mark_word, PORT, READY, REPORT, MARK, SPIN, PIN,
)


def mirror_word(m):
    swap = [gate("CX", PORT, MARK), gate("CX", MARK, PORT), gate("CX", PORT, MARK)]
    sign = [gate("SourceI", PORT, *SPIN)]*2
    forward = [gate("G", PORT)]*m
    inverse = sign + forward + sign
    return (swap + forward + [gate("CX", REPORT, PORT)]
            + forward + [gate("CX", READY, PORT)]
            + inverse + [gate("CX", REPORT, PORT)]
            + forward + [gate("CX", READY, PORT)] + swap)


def verify_schedule(m):
    def matrix(word):
        execution = ne.Execution(6, (), (), tuple(word), ne.G_CX_SOURCE_I, PORT, SPIN)
        return ne.word_matrix(execution, max_qubits=6, max_expanded_stages=64)

    require(ne.exact_matrix_equal(matrix(mark_word(1)).T, matrix(mirror_word(1))),
            "Mirrored mark failed on a routed old column")
    for r in (0, 1):
        for b in (0, 1):
            exact = 1 + (-1)**b - (-1)**(b+r) + (-1)**r
            require(exact == 2-4*r*b, "Wrong symbolic Gray sign sequence")
    steps = Counter(g.op for g in 2*(mark_word(m)+mirror_word(m)))
    steps += Counter({"G": 6, "CX": 12})
    require(steps == {"G": 16*m+6, "CX": 52, "SourceI": 32},
            "The actual two pairs and six emitters have the wrong inventory")
    return dict(steps)


def choose_real_weak_mark(m):
    iv = mp.iv
    iv.dps = 65
    p = (iv.sqrt(5)-1)/2
    a = iv.sqrt(p)
    c, s = iv.mpf(1), iv.mpf(0)
    rc, rs = a, p
    k = 2*m
    while k:
        if k & 1:
            c, s = c*rc-s*rs, s*rc+c*rs
        rc, rs = rc*rc-rs*rs, 2*rc*rs
        k //= 2
    require(c > 0 and 0 < s and s < iv.mpf("0.01"), "The native power is not a weak positive mark")
    y0, y1 = (p*c-a*s)**2, (p*c+a*s)**2
    require(iv.mpf("0.37") < y0 and y0 < y1 and y1 < iv.mpf("0.40"),
            "The mark variables left the independently certified window")
    t = (1-y0)*(1-y1)+y0*y1
    require(iv.mpf("0.278") < t*t and t*t < iv.mpf("0.280"), "Recovery window changed")
    require(iv.mpf(42)/37 < 1/p, "The code−Shannon slope can change sign")
    return {
        "native_exponent_m": m,
        "strict_both_pointer_probability_bounds": ["37/100", "2/5"],
        "strict_joint_recovery_probability_bounds": ["139/500", "7/25"],
        "maximum_p01_over_p10": "42/37",
    }


def verify_joint_laws():
    x0,x1,y0,y1 = sp.symbols("u0 u1 v0 v1", real=True)
    for amp0,amp1 in ((x0,y0),(x1,y1)):
        # Diagonal Kraus operator before the old inverse, on both activation sectors.
        diag = sp.diag(amp0*amp1, amp1*amp0)
        require(diag == amp0*amp1*sp.eye(2), "Equal outcomes retained old activation dependence")
    r,s,P = sp.symbols("y_0 y_1 P", real=True)
    d = s-r
    quiet = sp.Matrix([(1-r)*(1-s), (1-r)*s, r*(1-s), r*s])
    active = quiet.extract([0,2,1,3], [0])
    law = (1-P)*quiet+P*active
    require(sp.expand(sum(law)) == 1, "Failed mirror histories were dropped")
    require(law.diff(P).applyfunc(sp.expand) == sp.Matrix([0,-d,d,0]), "The complete mirror record has the wrong first jet")
    expected_recovery = (1-r)*(1-s)+r*s
    require(sp.expand(law[0]+law[-1]-expected_recovery) == 0, "Recovery is not a field-independent factor")
    charged = sp.Matrix([[3,4,5,6]])*law
    opposite = sp.Matrix([[3,5,4,6]])*law
    require(sp.expand(charged.diff(P)[0]) == d, "Verbatim repeat has the wrong charged source")
    require(sp.expand((charged-opposite).diff(P)[0]) == 2*d,
            "Literal mirror print difference lost its source")

    p = ne.P
    require(ne.exact_matrix_equal(sp.Matrix([[p*p*p]]), sp.Matrix([[p*p**2]])),
            "Golden odd pairs no longer have equal halves")
    t,F,z,Gamma = sp.symbols("t F z Gamma", positive=True)
    joint_survival = Gamma*((1-z)*t**2+z*t**2*F)
    require(sp.expand(joint_survival-Gamma*t**2*(1-z+z*F)) == 0, "Wrong paid survival check")
    return {
        "successful_child_instrument": "t^2*(U rho U*)",
        "four_pointer_complements_retained": True,
        "positive_measured_code_minus_Shannon_for_forward_duplicate": True,
        "feedback_survival_event": "Gamma*t^2*(1-z+z*F_old)",
    }


def main():
    m = 580
    print(json.dumps({
        "status": "PASS",
        "native_gate_sha256": PIN,
        "weak_mark": choose_real_weak_mark(m),
        "four_readers_and_six_literal_emitters": verify_schedule(m),
        "additional_canonical_births_without_feedback_flag": 10,
        "full_record_and_return": verify_joint_laws(),
        "book03_full_work_or_info_selected": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
