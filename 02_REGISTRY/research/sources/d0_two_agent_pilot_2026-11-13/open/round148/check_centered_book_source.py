"""Check B148's native mixing, Bellman identities and spectral tolerance."""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import sympy as sp


RESEARCH = Path(__file__).resolve().parents[4]
SOURCES = (
    "A4D_NATIVE_BOOK03_BORN_ENTROPY_BELLMAN_VERTEX_INFORMATION_WELD_2026_10_22.md",
    "sources/d0_two_agent_pilot_2026-11-13/open/round147/RESULT.json",
    "sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
    "NATIVE_FOUR_COPY_MATTER_RESPONSE.md",
    "sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
    "PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE.md",
    "sources/d0_two_agent_pilot_2026-11-13/direct/round75/work/RETAINED_WORK_RU.md",
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def equal(expression, message):
    require(sp.simplify(expression) == 0, message)


def check_switches():
    for selector, zero_port, live_port in product(range(2), repeat=3):
        flag = zero_port ^ (selector & zero_port) ^ (selector & live_port) ^ selector
        expected = 1 ^ live_port if selector else zero_port
        require(flag == expected, "Reversible port comparison on live flags")
        passed = zero_port ^ (selector & zero_port) ^ (selector & live_port)
        require(passed == (live_port if selector else zero_port), "Attenuation mux")


def reporter(length, p):
    h = sp.Rational(1, length)
    alpha = p**3 * h**2 / 64
    kappa = p**(-11) * h**6
    wave_acceptance = sp.Rational(1, 8) * p * (p**2)**5
    address_count = (length // 2)**4
    port_acceptance = (3 + 2*p) / address_count
    beta = h**6 / 16
    equal(wave_acceptance*kappa/2 - beta, "Outer choice and wave attenuation")
    equal(port_acceptance*alpha/4 - beta, "Two fair port choices and port attenuation")
    require(address_count >= 16, "Physical fair selector has space for five labels")
    require(Q(3, address_count) + Q(2, address_count)*Q(5, 8) < 1,
            "Port acceptance is a probability")
    return beta


def check_bellman(p):
    q, ln_phi = sp.symbols("q ln_phi", positive=True)
    h = -((1-q)*sp.log(1-q) + q*sp.log(q)) / ln_phi
    free_action = 1 + q - 2*h
    equal(sp.diff(free_action, q) - 1 - 2*(sp.log(q)-sp.log(1-q))/ln_phi,
          "Sign of the complete scalar derivative")
    equal(sp.diff(free_action, q, 2) - 2/(ln_phi*q*(1-q)), "Entropy curvature")
    equal(free_action - free_action.subs(q, 1-q) - (2*q-1), "Complement contrast")
    i0 = h - q*(1+(sp.log(q)-sp.log(1-q))/ln_phi)
    i1 = h + (1-q)*(1+(sp.log(q)-sp.log(1-q))/ln_phi)
    equal((1-q)*i0 + q*i1 - h, "Conditional Shannon gain")
    equal((2-i1)-(1-i0) + (sp.log(q)-sp.log(1-q))/ln_phi, "Normalized Born odds")
    equal(p + 2*p**2 - p*(1+1) - (3*p**2-1),
          "Least gain in the flipped native binary factory")
    require(Q(11, 9)**2 < Q(8, 5) and p < sp.Rational(5, 8), "Strict log-odds margin")
    terminal_margin = 1 - Q(11, 20)*Q(3, 2)
    require(terminal_margin == Q(7, 40), "Terminal gain margin")
    require(Q(5, 8)*Q(1, 5) == Q(1, 8) and sp.Rational(1, 8) < 3*p**2-1,
            "Exact comparison of factory perturbation and lower margin")
    future, f_parent, f_child = sp.symbols("future f_parent f_child")
    equal((f_parent + future) - (f_child + future) - (f_parent-f_child),
          "Old Bellman charges invariant under a common independent factor")
    return terminal_margin


def check_spectrum(length):
    root = sp.Symbol("z")
    modulus = root**(2*length) - root**length + 1
    require(sp.cyclotomic_poly(6*length, root) == modulus,
            "Cyclotomic field includes all wave phases")
    # k=0, b=c=1: one actual normalized positive transverse eigenvalue.
    transverse = 4 - 2*(root**4 + root**(6*length-4))
    norm = sp.resultant(modulus, sp.rem(transverse, modulus, root), root)
    require(norm.is_Integer and 1 <= abs(norm) <= 16**(2*length), "Exact spectral norm")
    h = Q(1, length)
    inverse_bound = h**2 * 16**(2*length-1)
    beta = h**6 / (16*16**(2*length))
    require(inverse_bound * beta / h**4 == h**4 / 256, "Rate after the wave inverse")
    return str(norm)


def main():
    p = (sp.sqrt(5)-1)/2
    equal(p**(-3) - (3+2*p), "Exact Golden weights")
    check_switches()
    margin = check_bellman(p)
    tests = {}
    for length in (4, 8, 16):
        beta = reporter(length, p)
        tests[str(length)] = {
            "calibrated_beta": str(beta),
            "ideal_complete_repetitions": int(1/beta),
            "extra_fair_checks_for_spectral_bound": 8*length,
            "cyclotomic_spectral_test_norm": check_spectrum(length),
        }
    print(json.dumps({
        "GR_closed": False,
        "old_Info_preserved_with_independent_complete_price": True,
        "new_terminal_Info_strict_lower_bound_near_center": str(margin),
        "actual_full_factory_tariff_admitted": False,
        "physical_kernel_compatibility_proved": False,
        "nonzero_mode_inverse_times_calibration_error_order": "h^4",
        "proof_controls": tests,
        "source_sha256": {path: sha256((RESEARCH / path).read_bytes()).hexdigest()
                          for path in SOURCES},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
