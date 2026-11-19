#!/usr/bin/env python3
"""Strict joint Q8 comparison source, using frozen outward entropy intervals.

Standard library only. No old native, spectral, geometry or entropy suite is
rerun. The existing Interval class is imported after its bytes are checked;
only the new algebra, interval composition and exact cap tail are evaluated.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from decimal import Decimal as D
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = []


def check(name, condition):
    if not condition:
        raise RuntimeError(name)
    CHECKS.append(name)


def verify_inputs(repo):
    pins = json.loads((HERE / 'SOURCE_PINS.json').read_text())
    located = {}
    for item in pins['inputs']:
        path = HERE / item['snapshot_path'] if 'snapshot_path' in item else repo / item['path']
        data = path.read_bytes()
        check('sha256_' + item['name'], hashlib.sha256(data).hexdigest() == item['sha256'])
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        check('git_blob_' + item['name'], blob == item['git_blob'])
        located[item['name']] = path
    return pins, located


def trim(poly):
    out = list(map(F, poly))
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def add(left, right):
    result = [F(0)] * max(len(left), len(right))
    for i, value in enumerate(left):
        result[i] += value
    for i, value in enumerate(right):
        result[i] += value
    return trim(result)


def scale(poly, factor):
    return trim([F(factor) * value for value in poly])


def mul(left, right):
    result = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return trim(result)


def derivative(poly):
    return trim([i * poly[i] for i in range(1, len(poly))] or [0])


def remainder(poly, modulus):
    value, divisor = trim(poly), trim(modulus)
    while len(value) >= len(divisor):
        factor = value[-1] / divisor[-1]
        shift = len(value) - len(divisor)
        for i, coefficient in enumerate(divisor):
            value[i + shift] -= factor * coefficient
        value = trim(value)
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    pins, paths = verify_inputs(args.repo.resolve())
    spec = importlib.util.spec_from_file_location(
        'frozen_complete_return_entropy_interval', paths['existing_outward_interval_engine'])
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    I = engine.Interval

    # An exact polynomial identity, with independent differentiation.
    numerator = list(map(F, [0, 0, 4, 0, 4]))
    denominator = list(map(F, [1, 0, 6, 0, 1]))
    quotient_numerator = add(mul(derivative(numerator), denominator),
                             scale(mul(numerator, derivative(denominator)), -1))
    stated_derivative = list(map(F, [0, 8, 0, 16, 0, 40]))
    check('exact_w_derivative_polynomial', quotient_numerator == stated_derivative)
    native_modulus = list(map(F, [-1, 4, 1]))  # c0^2+4c0-1=0.
    check('native_w_exact_value', remainder(add(numerator, scale(
        mul(denominator, [F(1, 3), F(-2, 3)]), -1)), native_modulus) == [0])
    check('native_w_prime_exact_value', remainder(add(stated_derivative, scale(
        mul(mul(denominator, denominator), [F(10, 9), F(1, 3)]), -1)), native_modulus) == [0])
    # Refining one abort leaf into two terminal codes and a new abort has
    # total reference multiplier p^2+p^3+p^2=1. Both bit leaves are kept,
    # even when a return parity forces their actual probability to zero.
    check('joint_reference_all_caps_induction',
          remainder([-1, 0, 2, 1], [-1, 1, 1]) == [0])

    root5 = I(5).sqrt()
    c0 = root5 - 2
    p = (root5 - 1) / 2
    logphi = ((root5 + 1) / 2).log()
    qg = 4 * p * p * p
    hg = -(qg * qg.log() + (1 - qg) * (1 - qg).log()) / logphi
    alpha = qg - hg
    w = 4 * c0 * c0 * (1 + c0 * c0) / (1 + 6 * c0 * c0 + c0 * c0 * c0 * c0)
    dw = 8 * c0 * (1 + 2 * c0 * c0 + 5 * c0 * c0 * c0 * c0) / (
        1 + 6 * c0 * c0 + c0 * c0 * c0 * c0).square()
    check('fixed_Golden_selector_probability', 0 < qg.lo < qg.hi < 1)
    check('comparison_price_coefficient_between_zero_and_one', 0 < alpha.lo < alpha.hi < 1)
    check('native_odd_weight_and_derivative_positive', 0 < w.lo < w.hi < 1 and dw.lo > 0)
    correction = alpha * dw

    old = json.loads(paths['existing_certified_entropy_result'].read_text())
    check('consumed_entropy_result_status', old['status'] == 'PASS_COMPLETE_RETURN_ENTROPY_C1')
    native = old['native_interval']
    check('consumed_entropy_native_parameter', native['native_parameter'] == 'sqrt(5)-2')
    check('consumed_entropy_cap', native['cap'] == 320)
    check('consumed_entropy_physical_admission_not_claimed',
          native['physical_gate_variation_admitted'] is False)
    # These serialized endpoints are already outward rounded by the pinned
    # engine's endpoints(): ROUND_FLOOR for lo, ROUND_CEILING for hi.
    entropy_source = I(*native['infinite_source_interval'])
    entropy_value = I(*native['infinite_entropy_interval'])
    source = -entropy_source + correction
    value = 8 - entropy_value + alpha * w
    check('strict_infinite_joint_record_source_band',
          D('-10.03') < source.lo < source.hi < D('-10.02'))

    n0 = 320
    r, const, velocity = F(31, 32), F(7, 6), F(16, 15)
    rr = r * r
    t0, t1, t2 = engine.tails(n0)
    entropy_tail = 10 * const ** 3 * (
        r ** -3 * (t1 + t2 / 31)
        + r ** -1 * (n0 + F(n0 * n0, 31)) * rr ** n0)
    odd_weight_tail = 2 * const ** 3 * r ** -3 * t1
    full_cost_tail = 16 * n0 * const ** 3 * r ** -1 * rr ** n0
    total = velocity * (entropy_tail + odd_weight_tail + full_cost_tail)
    check('inherited_entropy_tail_regime', n0 >= 5)
    check('tail_monomials_decrease_for_every_N_ge_320',
          n0 >= 31 and r * (1 + F(1, n0)) < 1)
    check('cap_source_error_below_0_001837', total < F(1837, 1000000))
    error = engine.fraction_interval(total)
    all_caps = I((source.lo - error.hi).next_minus(),
                 (source.hi + error.hi).next_plus())
    check('strict_joint_record_source_band_for_all_caps_ge_320',
          D('-10.03') < all_caps.lo < all_caps.hi < D('-10.02'))

    # This is a hostile scope control, not an admitted native variation.
    # Incorrectly replacing fixed qG by 4c would add this nonzero term.
    hprime = ((1 - qg) / qg).log() / logphi
    moving_selector_extra = 4 * w * (1 - hprime)
    check('moving_selector_cannot_be_silently_treated_as_fixed', moving_selector_extra.lo > 1)

    out = {
        'status': 'PASS_TEMPORAL_COMPARISON_STRICT_SOURCE',
        'checks': CHECKS,
        'count': len(CHECKS),
        'concurrent_commit': pins['concurrent_commit'],
        'verified_source_pins': len(pins['inputs']),
        'decimal_precision': 180,
        'native_parameter': 'c0=sqrt(5)-2=p^3; p and comparison splitter held fixed',
        'qG': engine.endpoints(qg),
        'h_phi_qG': engine.endpoints(hg),
        'qG_minus_h_phi_qG': engine.endpoints(alpha),
        'odd_return_probability': engine.endpoints(w),
        'odd_return_derivative': engine.endpoints(dw),
        'joint_source_correction': engine.endpoints(correction),
        'consumed_infinite_entropy_source_interval': engine.endpoints(entropy_source),
        'joint_record_price_value_interval': engine.endpoints(value),
        'infinite_joint_record_source_interval': engine.endpoints(source),
        'all_caps_N_ge_320_joint_record_source_interval': engine.endpoints(all_caps),
        'strict_source_band': '-10.03 < d_c S_records,N(c0) < -10.02 for N=infinity and every integer N>=320',
        'cap_source_error_at_320': engine.endpoints(error),
        'cap_source_error_exact_fraction': str(total),
        'cap_tail_formula': 'B[E_N+2 C^3 r^-3 T1(N)+16 N C^3 r^-1 R^N]',
        'tail_constants': {'r': str(r), 'R': str(rr), 'C': str(const), 'B': str(velocity)},
        'moving_selector_extra_if_wrongly_set_qG_equal_4c': engine.endpoints(moving_selector_extra),
        'complete_abort_included': True,
        'terminal_bit_recorded_on_abort': False,
        'zero_probability_even_bit_one_reference_leaves_retained': True,
        'work_trace_dimension': 4,
        'CAR16_spectator_probability_multiplier': 1,
        'old_entropy_certificate_rerun': False,
        'native_CAR16_transport_consumed_not_replayed': True,
        'overlapping_C1_derivations_acknowledged': True,
        'same_execution_complete_Book_price_selected': False,
        'continuous_native_c_writer_admitted': False,
        'additional_price_source_retained': True,
        'GR_closed': False,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
