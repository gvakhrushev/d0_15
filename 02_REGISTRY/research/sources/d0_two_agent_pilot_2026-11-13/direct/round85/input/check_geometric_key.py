"""An original-field meter on the full 4^4 x CAR16 material operand.

Run with python3 check_geometric_key.py. NumPy is the only dependency.
The analytic bounds in the accompanying note use exact expressions.
"""
import itertools
import json
import math

import numpy as np


L = 4
H = 1 / L
P = (math.sqrt(5) - 1) / 2
A0 = math.sqrt(P)
ETA = 4 * P**3
AXES = 4
SITES = (L,) * AXES
PHASE = ((1, 0, -1, 0), (0, 1, 0, -1))
F = 16517734400 / 162621047169
Z = 2**-20
RF = 4 * P**2 * (1 - 2*P**2) * Z * (1 - Z*4*P**3) * (1 - 4*P**3)
RQ = 8 * P**3 * (1 - 2*P**2) * (
    Z*(2 - 4*P**3) - Z**2*(4*P**3 + 2*(1 - 4*P**3)*4*P**3)
)
AMP = H * math.sqrt(F * RF / RQ) / (2*math.sin(math.pi*H))
# Midpoint of the primary interval for the common compiled angle,
# used only in the numerical replay of the exact phased endpoint word.
AMP_COMPILED = P * math.sin(math.asin(AMP/P) + 3.8579280010880284e-8)


def close(lhs, rhs):
    np.testing.assert_allclose(lhs, rhs, rtol=5e-12, atol=1e-13)


def norm2(ket):
    return np.vdot(ket, ket).real


def circular_mode(axis):
    n = np.indices(SITES)[axis]
    return np.stack(tuple(np.take(side, n) for side in PHASE), axis=-1)


MODES = tuple(circular_mode(axis) for axis in range(AXES))


def encode(chi, mode):
    """chi[site,RIGHT], mode[site,2]. Keep all 16 CAR coordinates."""
    ket = np.zeros(chi.shape + (16,), dtype=chi.dtype)
    ket[..., 1] = A0 * chi
    filler = np.sqrt(P**2 - np.sum(mode**2, axis=-1))
    ket[..., 14] = filler[..., None] * chi
    for j, car in enumerate((0, 15)):
        ket[..., car] = mode[..., j, None] * chi
    return ket


def plus_register():
    # A full-Schmidt-rank reference for all sixteen independent low-bit addresses.
    chi = np.zeros(SITES + (16,), dtype=complex)
    amplitudes = np.arange(1, 17) * np.exp(0.21j * np.arange(16))
    amplitudes /= np.linalg.norm(amplitudes)
    for site in np.ndindex(SITES):
        low = sum((x % 2) << j for j, x in enumerate(site))
        chi[site + (low,)] = amplitudes[low] / 4
    close(norm2(chi), 1)
    return chi


def read(ket, axis, click):
    # v birth, literal controlled high-bit X, G inverse, computational result.
    shifted = np.roll(ket, L//2, axis=axis)
    if click:
        return A0*P * (shifted - ket)
    return P*ket + P**2*shifted


def split_even(ket):
    result = ket.copy()
    for car in range(16):
        if bin(car).count("1") % 2:
            result[..., car] = 0
    return result


def entropy(probabilities):
    return -sum(q*math.log(q)/math.log(1/P) for q in probabilities if q > 0)


def check_native_kraus():
    rot = np.array([[A0, -P], [P, A0]])
    xgate = np.array([[0., 1.], [1., 0.]])
    close(xgate @ rot @ xgate, rot.T)
    for i in (0, 1):
        old = np.eye(2)[:, i]
        coupling = np.stack((A0*old, P*(xgate @ old)))
        close(rot.T @ coupling, np.stack((P*old + P**2*xgate @ old,
                                          A0*P*(xgate @ old - old))))
    close(ETA + P**6, 1)


def endpoint_recovery():
    chi = plus_register()
    for mu in range(AXES):
        mode = MODES[mu]
        old = encode(chi, AMP_COMPILED * mode)
        for nu in range(AXES):
            close(norm2(read(old, nu, True)), AMP_COMPILED**2*ETA*(mu == nu))
        # All three other probes preceding or following a mu click fix this wave.
        returned = read(old, mu, True) / (-2*A0*P*AMP_COMPILED)
        for nu in range(AXES):
            if nu != mu:
                close(read(returned, nu, False), returned)
        c, s = (mode[..., j, None] for j in (0, 1))
        decoded0 = c*returned[..., 0] + s*returned[..., 15]
        decoded15 = -s*returned[..., 0] + c*returned[..., 15]
        close(decoded15, 0)
        close(returned[..., 1:15], 0)
        close(decoded0, chi)
        close(encode(decoded0, AMP_COMPILED*mode), old)
    # The original word on a classical material site is identical for both signs.
    sharp = np.zeros(SITES + (1,))
    sharp[(0, 0, 0, 0, 0)] = 1
    close(encode(sharp, AMP*MODES[0]), encode(sharp, AMP*MODES[1]))
    close(norm2(read(encode(sharp, AMP*MODES[0]), 1, True)), 2*P**3)


def geometric_meter():
    uniform = np.ones(SITES + (1,)) / L**2
    states = {}
    entropies = {}
    gain = AMP**2 * ETA
    for t in (0., 0.25, 0.5, 0.75, 1.):
        mode = AMP*(math.sqrt(1-t)*MODES[0] + math.sqrt(t)*MODES[1])
        old = encode(uniform, mode)
        states[t] = old
        close(norm2(old), 1)
        signs = (1, -1, -1, -1)
        kinetic = np.zeros(SITES)
        for j, sign in enumerate(signs):
            diff = (np.roll(mode, -1, axis=j) - mode)/H
            kinetic += sign*np.sum(diff**2, axis=-1)
        close(kinetic, (1 - 2*t)*4*AMP**2*math.sin(math.pi*H)**2/H**2)
        even = split_even(old)
        close(norm2(even), AMP**2)
        by_axis = np.zeros(AXES)
        failures = norm2(old - even)
        full_records = [failures]
        printed_length = 2*failures  # odd parity physically prints 10
        for flags in itertools.product((False, True), repeat=AXES):
            branch = even
            for axis, click in enumerate(flags):
                branch = read(branch, axis, click)
            probability = norm2(branch)
            full_records.append(probability)
            printed_length += probability*(1 + AXES + sum(flags))
            if sum(flags) == 1:
                by_axis[flags.index(True)] += probability
            elif any(flags):
                close(probability, 0)
            else:
                failures += probability
        close(by_axis, (gain*(1-t), gain*t, 0, 0))
        close(failures, 1-gain)
        close(printed_length, 2-AMP**2 + AMP**2*(4+ETA))
        entropies[t] = entropy(full_records)
        close(entropies[t], entropies[0.] + gain*entropy([t, 1-t]))
    close(states[0.25][..., 14], states[0.75][..., 14])
    overlap = float(np.vdot(states[0.25], states[0.75]).real)
    b = math.sqrt(3)/2
    close(overlap, 1 - AMP**2*(1-b))
    record_overlap = 1 - gain*(1-b)
    assert record_overlap**2 < overlap < record_overlap
    reference_gram = np.array([
        [np.vdot(encode(uniform, AMP*u), encode(uniform, AMP*v)).real for u in MODES]
        for v in MODES
    ])
    close(np.linalg.eigvalsh(reference_gram)[:3], np.full(3, AMP**2))
    compiled_input_overlap = 1 - AMP_COMPILED**2
    compiled_output_overlap = 1 - AMP_COMPILED**2*ETA
    assert compiled_output_overlap**2 < compiled_input_overlap < compiled_output_overlap
    return {
        "all_sites_per_field": L**4,
        "compiled_endpoint_preserved_low_SITE_RIGHT_columns": 16,
        "physical_endpoint_axes_tested": AXES,
        "material_source_sample_efficiency_given_even": round(ETA, 12),
        "ideal_reference_squared_amplitude": round(AMP**2, 14),
        "one_pass_conclusive_probability": round(gain, 14),
        "expected_full_printed_length": round(2-AMP**2 + AMP**2*(4+ETA), 14),
        "symmetric_CQ_entropy_slope_at_midpoint": 0,
        "two_independent_records_overlap_deficit": round(overlap - record_overlap**2, 14),
        "compiled_F5_F6_two_records_overlap_deficit":
            round(compiled_input_overlap - compiled_output_overlap**2, 14),
        "closes_full_cost_info": False,
        "GR_closed": False,
    }


if __name__ == "__main__":
    check_native_kraus()
    endpoint_recovery()
    print(json.dumps(geometric_meter(), ensure_ascii=False, indent=2))

