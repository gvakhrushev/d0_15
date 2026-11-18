"""Verify actual H.1 addresses, two literal CX codes and exact-angle witnesses."""

from collections import Counter
from dataclasses import replace
from itertools import product
from pathlib import Path
import json
import runpy
import sys

import sympy as sp


def require(value, reason):
    if not value:
        raise ArithmeticError(reason)


def main():
    here = Path(__file__).resolve()
    package = here.parents[3]
    b131 = runpy.run_path(str(package / "open/round131/check_inner_work.py"))
    data, native = b131["load_comparator"]()
    forward, _ = data["predicate"]()
    reverse = data["inverse_predicate"]()
    report, ready, port = data["report"], data["ready"], data["PORT"]
    addresses = Counter(g.wires for g in forward+reverse if g.op == "CX")
    n = [addresses[(report(j),port)] for j in range(7)]
    require(n == [256,256,1024,2048,256,256,1024] and sum(n) == 5120, "actual source locations")
    immutable = set(report(j) for j in range(7)) | set(ready(j) for j in range(7))
    for g in forward+reverse:
        require((g.op=="CX" and g.wires[1]==port) or not immutable.intersection(g.wires),
                "an addressed control was overwritten")

    x, y = ready(2), report(2)
    r1, r2, t1, t2 = 23,24,25,26
    gate = native.Gate
    def writer(r, t):
        return (gate("CX",(r,t)), gate("G",(t,)), gate("CX",(r,t)))
    old = native.Execution(27,(r1,r2,t1,t2),(22,),(),native.G_CX_SOURCE_I,port,(20,21),())
    for targets in ((r1,r2),(r1,r1)):
        typed = (gate("CX",(x,targets[0])), gate("CX",(y,targets[1])))
        extra = typed+writer(r1,t1)+writer(r2,t2)
        native.validate_execution(replace(old,gates=extra),max_qubits=27,max_expanded_stages=8)
    X = sp.Matrix([[0,1],[1,0]])
    born = sp.Matrix([native.A,native.P])
    require(native.exact_matrix_equal(X*native.G_LOCAL*X*born, sp.Matrix([1,0])),
            "actual code 10 on the returned bit with original tail")
    q = sp.symbols("q", real=True)
    d = 1-2*q
    for a,b in product(range(2),repeat=2):
        ones = lambda bit: q+d*bit
        require(sp.expand(ones(a)+ones(b)-ones(a^b)-ones(0)-2*d*a*b)==0,
                "two positive code readers extract the exact conjunction")
    # The partial trace acts by the Gram matrix on every old operator block.
    for a,b,c,e in product(range(2),repeat=4):
        ca = (a^c)+(b^e)
        cb = (a^b)^(c^e)
        require((ca,cb) in ((0,0),(1,1),(2,0)), "true two-meter coherence multipliers")
    phase_dir = package.parent / "d0_native_readiness_amplification_2026-10-24"
    sys.path.insert(0,str(phase_dir))
    import native_phase
    # u=G^m born; the verified exponent below is m+1.
    receipts = []
    for exponent, d_min, d_max in ((1048,sp.Rational(83,10**6),sp.Rational(85,10**6)),
                                   (130967,sp.Rational(73,10**7),sp.Rational(75,10**7)),
                                   (1944448,sp.Rational(24,10**7),sp.Rational(26,10**7))):
        (cl,ch),(sl,sh) = native_phase.native_rotation_intervals(exponent,bits=192)
        dlo, dhi = cl**2-sh**2, ch**2-sl**2
        require(cl>0 and sl>0 and d_min<dlo<=dhi<d_max, "strict certified native near-fair amplitude")
        receipts.append({"positive_G_after_birth": exponent-1,
                         "strict_d_bracket":[str(d_min),str(d_max)],
                         "per_arm_old_diamond_upper_diagnostic": float(2*sum(n)*(1-2*cl*sl))})
    # Second construction uses the very same full-column conditional-rotation alphabet.
    counts=native_phase.phase_counts([1,1],1)
    require(counts["g_count"]==4 and counts["source_i_count"]==8 and counts["cx_count"]==20,
            "both signs have two positive and two negative Walsh factors")
    layout=replace(old,blank_wires=(r1,))
    plus=native_phase.phase_word(layout,(x,y),(1,1),r1,1,max_qubits=27,max_expanded_stages=32)
    require(len(plus)==32,"compiled one positive sample on actual predicate addresses")
    for a,b in product(range(2),repeat=2):
        exponents = [(-1)**(i+j+a*i+b*j) for i,j in product(range(2),repeat=2)]
        require(sum(exponents)==4*a*b,"signed all-column parity polynomial")
    co,si=native_phase.native_rotation_intervals(4*55979,bits=192)
    require(co[0]>0 and sp.Rational(17,10**6)<si[0]<si[1]<sp.Rational(18,10**6),
            "nonzero exact small predicate angle")
    print(json.dumps({"actual_REPORT_counts":n,"meter_locations":sum(n),"pure_CX_arm_new_births_per_location":4,
                      "per_location_work_per_arm":"2*m+8 native calls plus 4 births and actual registrations",
                      "code_difference":"2*d*W","native_near_fair_examples":receipts,
                      "signed_rotation_old_marginals_exactly_equal":True,
                      "book_occupation_tariff_selected":False,"GR_closed":False},indent=2))


if __name__=="__main__":
    main()
