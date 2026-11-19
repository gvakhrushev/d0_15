"""Exact conditional sector averages on the full paired-pointer archive."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import runpy


PILOT = Path("02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13")
B170 = PILOT / "open/round170/thermal"
PINS = {
    B170 / "check_paired_pointer_gibbs.py": "8c132df110913ca31f161e620e31a235a5963fd7fc06ab1a6320cb1641ac3b36",
    B170 / "PAIRED_POINTER_GIBBS_RU.md": "d961ee4b1437706b06fc3e464ef3cea2f9714e157e3155101ed2c93622c71bf3",
}


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def enumerate_terminal_moment(owner, cycles, y, c, s, moment_01, moment_00):
    p = owner["p"]
    zero = owner["Golden"]()
    one = owner["one"]
    eta = s*s
    histories = [((), (p, p*p))]
    for _ in range(cycles):
        next_histories = []
        for tape, (u0, u1) in histories:
            # Only diagonal masses are needed for the first moment. In the
            # all-00 leaf the physical U is still one coherent v, with one tape.
            outcomes = (("00", (c*c*u0, c*c*u1)),
                        ("01", (eta*u0, eta*u1 if y == 0 else zero)),
                        ("10", (zero, eta*u1 if y == 1 else zero)))
            for mark, mass in outcomes:
                if mass[0] + mass[1] != 0:
                    next_histories.append((tape + (mark,), mass))
        histories = next_histories
    expected_count = 2**cycles if y == 0 else 2**(cycles+1)-1
    require(len(histories) == expected_count, "full positive support including the single empty mask")
    require(sum((u0 + u1 for _, (u0, u1) in histories), zero) == one, "complete normalized archive")
    require(sum(tape == ("00",)*cycles for tape, _ in histories) == 1, "never-revealed U is one leaf")
    moments = {"01": moment_01, "00": moment_00, "10": zero}
    return sum((moments[tape[-1]] * (u0 + u1 if y == 0 else u0)
                for tape, (u0, u1) in histories), zero)


def verify_normalization():
    import sympy as sp

    q, k0, k1, qdot, rootdot, clockdot = sp.symbols("q k0 k1 qdot rootdot clockdot", positive=True)
    u = (1-q)*k0 + q*k1
    born = (1-q, q)
    thermal = ((1-q)*k0/u, q*k1/u)
    scores = [sp.diff(value, q)/value*qdot for value in thermal]
    score_Q = sum(weight*score for weight, score in zip(thermal, scores))
    score_P = sum(weight*score for weight, score in zip(born, scores))
    require(sp.simplify(score_Q) == 0, "thermal normalized score mean")
    local = sp.diff(u, q)/u*qdot
    require(sp.simplify(score_P - score_Q + local) == 0, "actual unmatched covariance")
    require(sp.simplify(rootdot + clockdot - local - (score_P - score_Q) - rootdot - clockdot) == 0,
            "full normalization cancels the separate covariance")
    x = (k1-k0)/k0
    gain = x*(1-2*q-q*q*x)/(1+q*x)**2
    require(sp.simplify(sp.diff(thermal[1], q) - 1 - gain) == 0, "weighted marginal derivative")
    require(sp.simplify(thermal[1]/thermal[0] / (born[1]/born[0]) - k1/k0) == 0, "unchanged log-odds derivative")


def main():
    for path, expected in PINS.items():
        require(sha256(path.read_bytes()).hexdigest() == expected, f"pinned input {path}")
    prior = runpy.run_path(str(B170 / "check_paired_pointer_gibbs.py"))
    for path, expected in prior["PINS"].items():
        require(sha256(path.read_bytes()).hexdigest() == expected, f"pinned B170 input {path}")
    owner = runpy.run_path(str(PILOT / "direct/round82/device/check_prepaid_report.py"))
    detector, c, s = prior["verify_detector"](owner)
    one, a, p = owner["one"], owner["a"], owner["p"]
    powers = prior["power"]
    m01, m00 = powers(p, 9, one)*c, powers(p, 7, one)*a*s
    B = s*s*m01 + c*c*m00
    for cycles in range(1, 7):
        for y, factor in ((0, one), (1, p)):
            actual = enumerate_terminal_moment(owner, cycles, y, c, s, m01, m00)
            require(actual == factor*B, f"exact sector mean for cycle cap {cycles} and y={y}")
    leading = -p*p*B
    require(leading.coefficients == (-399847363302522492, 0, 646966624135508796, 0), "exact weighted moment gap")
    lo, hi = owner["enclosure"](leading)
    require(F(4898, 10**7) < lo <= hi < F(4899, 10**7), "strict rational moment enclosure")
    require(detector == 194, "actual tester word")
    n = 363
    y = F(1, 22)
    tail = 2*y/(n+1)/(1-y/(n+2))
    require(tail < F(25, 10**5), "relative tail less than 0.00025")
    require(2*(lo-tail) > F(47, 10**5), "strict aggregate heat gap")
    require(32*y*y/(1-y/(n+1)) < F(1, 10), "upper relative tilt")
    q_max, x_max = F(19, 50), F(1, 10)
    require((1-2*q_max-q_max*q_max*x_max)/(1+q_max*x_max)**2 > F(1, 5), "uniform H.1 marginal derivative")
    verify_normalization()
    print(json.dumps({
        "status": "PASS",
        "actual_detector_calls": detector,
        "old_columns_per_defect": 32,
        "exact_cycle_caps_and_sectors": 12,
        "leading_sector_moment_difference": "-399847363302522492 + 646966624135508796 p",
        "leading_difference_enclosure": ["0.0004898", "0.0004899"],
        "strict_sector_heat_difference": "> 0.00047 f_363",
        "H1_marginal_derivative_minus_one": "> 0.000094 f_363 (fixed apparatus)",
        "full_normalization_cancels_local_unmatched_score": True,
        "GR_closed": False,
        "source_sha256": {str(path): value for path, value in PINS.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
