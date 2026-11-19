"""Certify the common positive cone and passive overlap of one reused-bit readout."""
from fractions import Fraction as F
from pathlib import Path
from contextlib import redirect_stdout
import io
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "device"))
import check_prepaid_report as device


def main():
    with redirect_stdout(io.StringIO()):
        eta, registered, coherent, first_motion = device.numerical_data(1)
    add, sub, mul = device.plus, device.minus, device.times
    p, r = map(device.enclosure, (device.p, device.p*device.p))
    def known_motion(y, u):
        return device.checked_sum(1, y, u)
    collapsed = add(mul(p, known_motion(1,0)), mul(r, known_motion(1,1)))
    nc1 = mul(mul(eta,r), add(1,device.enclosure(device.p3)))
    late_motion = add(sub(collapsed,known_motion(0,device.v)),nc1)
    assert registered[0] > F(".038") and coherent[0] > F(".330")
    assert first_motion[0] > F("6.89") and late_motion[0] > F(".367")
    failure = sub(1,eta)
    unresolved = device.interval(1)
    floors = {}
    for n in range(1,19):
        survival = mul(unresolved,failure)
        slope = sub(mul(n,mul(eta,r)),mul(sub(1,survival),add(1,r)))
        if n in (16,17,18):
            floors[n]=round(float(slope[0]),9)
        if n==16:
            assert slope[1]<0
        if n==17:
            assert slope[0]>F(".00969")
            assert sub(r,mul(unresolved,add(1,r)))[0]>0
        unresolved=survival
    # Golden exact identities, no probabilities of histories inserted in the cold compression.
    a=device.p
    assert a*a+device.p3==a and a+a*a==device.one
    for n in range(1,9):
        from itertools import product
        total=[device.Golden(),device.Golden()]
        for mask in product((0,1), repeat=n):
            weight=device.one
            for hit in mask:
                weight=weight*(device.p3 if hit else a*a)
            for y in (0,1):
                projections=(a,a*a) if y and any(mask) else (device.one,)
                for overlap in projections:
                    total[y]+=weight*overlap
        printed=device.one
        expected=device.one
        for _ in range(n):
            printed=printed*device.p3
            expected=expected*device.p3*a
        assert all(value*printed==expected for value in total)
    print(json.dumps({"slope_without_work":floors,
                      "motion_before_first_success":round(float(first_motion[0]),9),
                      "motion_after_first_success":round(float(late_motion[0]),9),
                      "uniform_positive_threshold_k1":17,
                      "cold_factor_after_n_calls":"p^(4n)",
                      "shared_memory_and_input_conditions_required":True},indent=2))


if __name__ == "__main__":
    main()
