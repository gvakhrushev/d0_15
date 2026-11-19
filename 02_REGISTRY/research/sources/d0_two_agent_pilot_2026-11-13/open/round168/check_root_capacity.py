"""Rational certificates for the B168 root-capacity and thermal bounds."""

from fractions import Fraction as Q
from hashlib import sha256
from math import ceil, floor, isqrt
from pathlib import Path
import json
import subprocess


ROOT = Path(__file__).resolve().parents[6]
METRIC = (
    "02_REGISTRY/research/sources/d0_gr_2026-11-18/"
    "followups/2026-11-19/metric/"
)
PILOT = "02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/"
SCALE = 10**28


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def outward(lower, upper):
    return Q(floor(lower*SCALE), SCALE), Q(ceil(upper*SCALE), SCALE)


def exp_nonnegative_bounds(value):
    require(0 <= value < 2, "outside exponential bound range")
    term = Q(1)
    total = term
    for k in range(1, 35):
        term = term*value/k
        total += term
    next_term = term*value/35
    tail = next_term/(1-value/36)
    return outward(total, total+tail)


def log_unit_bounds(value):
    require(1 <= value <= 2, "outside normalized logarithm interval")
    z = (value-1)/(value+1)
    total = 2*sum(z**(2*k+1)/(2*k+1) for k in range(35))
    tail = 2*z**71/(71*(1-z*z))
    return outward(total, total+tail)


def log_bounds(value):
    require(value > 0, "natural logarithm requires positive input")
    exponent = 0
    while value < 1:
        value *= 2
        exponent -= 1
    while value > 2:
        value /= 2
        exponent += 1
    lower, upper = log_unit_bounds(value)
    shifts = [exponent*endpoint for endpoint in log_unit_bounds(Q(2))]
    return outward(lower+min(shifts), upper+max(shifts))


def golden_endpoints():
    scale = 10**24
    low = Q(isqrt(5*scale**2)-scale, 2*scale)
    high = low+Q(1, 2*scale)
    require(low*low+low < 1 < high*high+high, "wrong Golden interval")
    return low, high


def thermodynamic_bounds():
    p_low, p_high = golden_endpoints()
    ell_low = log_bounds(1/p_high)[0]
    ell_high = log_bounds(1/p_low)[1]
    tau_low, tau_high = outward(4*p_low*p_low, 4*p_high*p_high)
    a_low = 1/exp_nonnegative_bounds(tau_high)[1]
    a_high = 1/exp_nonnegative_bounds(tau_low)[0]
    a_low, a_high = outward(a_low, a_high)
    k_low, k_high = outward(tau_low/(1-a_low), tau_high/(1-a_high))
    require(k_low > 1, "capacity expression lost monotonicity")
    gap_low = k_low-1-log_bounds(k_low)[1]
    gap_high = k_high-1-log_bounds(k_high)[0]
    require(Q("0.2828001692") < gap_low < gap_high < Q("0.282800170"),
            "wrong sharp Gibbs divergence enclosure")

    spectral_minimum = 359+66*a_low
    capacity_minimum = spectral_minimum/exp_nonnegative_bounds(gap_high)[1]
    require(capacity_minimum > Q("281.361667"), "wrong relative archive capacity")
    floor_targets = {
        (1, 1): "11.7196640",
        (1, 4): "14.6005042",
        (425, 2): "0.58331676",
        (425, 4): "2.02373685",
    }
    verified = {}
    for (dimension_ratio, rank), target in floor_targets.items():
        bare = log_bounds(spectral_minimum*rank/dimension_ratio)[0] - gap_high
        require(bare > 0 and bare/ell_high > Q(target), "wrong positive root floor")
        verified[f"Darc_per_D_{dimension_ratio}_rank_{rank}"] = target

    beta_lower = tau_low/2
    mode_energy_lower = 66*beta_lower*a_low/425
    z = Q(1, 2**20)
    determinant_upper = 4*log_bounds(1/(1-z))[1]
    require(mode_energy_lower > Q("0.02574345"), "wrong mode energy lower bound")
    require(determinant_upper < Q("0.000003815"), "wrong determinant upper bound")
    require((mode_energy_lower-determinant_upper)/ell_high > Q("0.05348920"),
            "wrong positive rank-one mode redundancy")
    require(ell_low > 0, "nonpositive Golden log")
    return {
        "KL_upper_nats": "0.282800170",
        "required_Darc_per_D_per_rank_lower": "281.361667",
        "nu_times_root_residual_lower": verified,
        "rank_one_mode_redundancy_times_nu_lower": "0.05348920",
    }


def exact_tree_factors():
    # Exponents are in log_phi units. W_w are p**w; spectral normalization
    # cancels in the leaf check, so rational exponents suffice.
    spectral_exponents = [Q(2), Q(4), Q(5)]
    prices = [Q(1), Q(3), Q(2)]
    for nu in (1, 2):
        root = Q(7, 3)
        gains = [c-w/nu-root for c, w in zip(prices, spectral_exponents)]
        reconstructed = [nu*(c-i) for c, i in zip(prices, gains)]
        require(reconstructed == [w+nu*root for w in spectral_exponents],
                "wrong unshifted absolute root factor")
        shifted = [nu*(c-root-i) for c, i in zip(prices, gains)]
        require(shifted == spectral_exponents, "wrong sign for absolute root offset")
    return [1, 2]


def source_pins():
    pins = {
        ("2fe4d3901", METRIC+"SPECTRAL_TREE_BALANCE_RU.md"):
            "e523b1053ab5632243d9c87950f9479db4a11a2e7eed1f6c5a537704844c007d",
        ("2fe4d3901", METRIC+"LOCAL_GIBBS_RECORDS_RU.md"):
            "a7272d3df4e2cdb2d24bf12a046576242781205de572fb626400113cb4f9b51c",
        ("82e2486f6", PILOT+"open/round167/B167_MEASURED_REPORT_RETURN_RU.md"):
            "2eb8bd1b74e4af7e272a8f00dfe9a65aeae0050fb1c4001483ac6a768ec71bc5",
    }
    for (revision, path), expected in pins.items():
        raw = subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)
        require(sha256(raw).hexdigest() == expected, path)
    return len(pins)


def main():
    payload = thermodynamic_bounds()
    payload.update(
        verified_root_exponent_conventions=exact_tree_factors(),
        source_pins=source_pins(),
        field_constancy_established=False,
        full_physical_cost_minus_info_proved=False,
        GR_closed=False,
        status="PASS",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
