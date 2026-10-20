#!/usr/bin/env python3
"""Reproducible full-CAR16 stopped Golden17 terminal-readout checks.

This builds the declared fixed square-root instrument, not a moving Bell
programme.  Exact algebra checks the Golden leaf code and the dark outcome;
finite-dimensional numerical checks use analytic state/amplitude jets.  The
universal no-floor inequalities are proved in RESULT.md, not established by
this finite sample.  No compulsory physical price or native admission is chosen.

Run from any directory with Python, NumPy and SymPy.  Optional --receipt PATH
writes the same JSON printed on stdout.  No other checker is imported.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp


DIM, OUTCOMES = 256, 17
P = (math.sqrt(5.0) - 1.0) / 2.0
G = P * P
ELL = -math.log(P)
BELL = 1.0 / 4096.0
KAPPA = G * G * BELL / 24.0
# These are roundoff/error tolerances, never probability or spectral floors.
MATRIX_ATOL = 3e-13
SOURCE_ATOL = 2e-11
SINGULAR_ROUNDOFF = 1e-15
SUBSETS = [a for degree in range(5) for a in combinations(range(4), degree)]


def close(a, b, atol=MATRIX_ATOL):
    error = float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
    assert error <= atol, (error, atol)
    return error


def stopped_leaves(m, cap):
    """All actual chronological leaves, including every incomplete cap word."""
    leaves = []

    def visit(word, successes):
        if successes == m or len(word) == cap:
            leaves.append((word, successes))
        else:
            visit(word + (0,), successes)
            visit(word + (1,), successes + 1)

    visit((), 0)
    return leaves


def golden_prefix_code():
    # Genuine complete binary prefix tree: B has Golden length 1 and G length 2.
    # Expand the B leaf sixteen times: G, BG, ..., B^15 G, B^16.
    words = [(0,) * j + (1,) for j in range(16)] + [(0,) * 16]
    lengths = np.array([len(w) + sum(w) for w in words], dtype=float)
    return words, lengths, P ** lengths


def exact_checks():
    x = sp.Symbol("p")
    relation = sp.Poly(x * x + x - 1, x)

    def golden_zero(expression):
        return sp.rem(sp.Poly(sp.expand(expression), x), relation).is_zero

    tree_counts = []
    for m, cap in [(1, 4), (2, 7), (3, 7)]:
        leaves = stopped_leaves(m, cap)
        mass = cost = attempts = successes = sp.S.Zero
        by_k = [sp.S.Zero for _ in range(m + 1)]
        for word, k in leaves:
            t = len(word)
            w = x ** (t + k)
            assert w == (x * x) ** k * x ** (t - k)
            mass += w
            cost += (t + k) * w
            attempts += t * w
            successes += k * w
            by_k[k] += w
        assert golden_zero(mass - 1)
        assert golden_zero(successes - x * x * attempts)
        assert golden_zero(cost - (1 + x * x) * attempts)
        for k in range(m):
            assert golden_zero(by_k[k] - sp.binomial(cap, k) * x ** (cap + k))
        # H_phi(w)=sum w L follows exactly from w=p^L, with no renormalization.
        tree_counts.append({"m": m, "cap": cap, "leaves": len(leaves)})

    words, lengths, _ = golden_prefix_code()
    assert all(not (len(a) <= len(b) and b[:len(a)] == a)
               for i, a in enumerate(words) for j, b in enumerate(words) if i != j)
    assert golden_zero(sum(x ** int(n) for n in lengths) - 1)
    assert lengths[0] != lengths[1]

    # Exact full effect decomposition on Pi's sixteen-dimensional block.
    I4, I16 = sp.eye(4), sp.eye(16)
    metric = sp.diag(1, -1, -1, -1)
    generators = []
    for i, j in combinations(range(4), 2):
        J = sp.zeros(4)
        J[i, j] = 1
        J[j, i] = -metric[i, i] * metric[j, j]
        generators.append(J)
    vec = lambda A: sp.Matrix(list(A))
    u = vec(I4) / 2
    vs = [vec(J) / sp.sqrt(2) for J in generators]
    frame = sp.Matrix.hstack(u, *vs)
    assert frame.T * frame == sp.eye(7)
    pu = u * u.T
    pv = sum((v * v.T for v in vs), sp.zeros(16))
    prem = I16 - pu - pv
    marks_over_kappa = [4 * (u + sign * v) * (u + sign * v).T
                        for v in vs for sign in (1, -1)]
    marks_sum = sum(marks_over_kappa, sp.zeros(16))
    assert marks_sum == 48 * pu + 8 * pv
    assert 96 * I16 - marks_sum == 48 * pu + 88 * pv + 96 * prem
    assert prem * prem == prem and sp.trace(prem) == 9
    # Complementary 240 dimensions have marks=rest=0.  These two exact scalar
    # identities therefore check completeness on the WHOLE joint carrier.
    b = sp.Rational(1, 4096)
    kap = x ** 4 * b / 24
    assert golden_zero(96 * kap + 2 * x ** 3 * b + x * x * b
                       + 1 - b * (1 + 3 * x ** 4) - 1)
    assert golden_zero(2 * x ** 3 * b + x * x * b
                       + 1 - b * (1 - x ** 4) - 1)

    # An exact dark marked outcome in the declared full-CAR16 instrument.
    # J23 is the last generator, with the same sign as the numerical chart.
    c, sn = sp.Rational(1, 3), 2 * sp.sqrt(2) / 3
    rotation = I4.copy()
    rotation[2, 2] = rotation[3, 3] = c
    rotation[2, 3], rotation[3, 2] = sn, -sn
    chi_block = vec(rotation) / 4
    dchi_block = vec(generators[-1] * rotation) / 4
    dark_vector = 2 * (u - vs[-1])
    assert sp.simplify(dark_vector.dot(chi_block)) == 0
    dark_amplitude_jet = sp.simplify(dark_vector.dot(dchi_block))
    assert dark_amplitude_jet != 0
    assert sp.simplify(2 * dark_vector.dot(chi_block) * dark_amplitude_jet) == 0
    # The zero is a rank/probability birth, not an identically absent effect.
    assert dark_vector.dot(dark_vector) == 8

    return {"complete_exact_trees": tree_counts,
            "golden_code_words": ["".join("G" if z else "B" for z in w) for w in words],
            "golden_code_lengths": lengths.astype(int).tolist(),
            "exact_dark_cos": "1/3", "exact_dark_sin": "2*sqrt(2)/3",
            "exact_dark_amplitude_jet_over_sqrt_kappa": str(dark_amplitude_jet),
            "full_rest_eigenvalues_over_kappa": {"48": 1, "88": 6, "96": 9, "0": 240}}


def exterior(A):
    result = np.zeros((16, 16))
    for i, a in enumerate(SUBSETS):
        for j, b in enumerate(SUBSETS):
            if len(a) == len(b):
                result[i, j] = np.linalg.det(A[np.ix_(a, b)]) if a else 1.0
    return result


def induced_generator(J):
    """Derivative of the exterior representation at I, by multilinearity."""
    result = np.zeros((16, 16))
    for i, a in enumerate(SUBSETS):
        for j, b in enumerate(SUBSETS):
            if not a or len(a) != len(b):
                continue
            base = np.eye(4)[np.ix_(a, b)]
            jet = J[np.ix_(a, b)]
            for column in range(len(a)):
                term = base.copy()
                term[:, column] = jet[:, column]
                result[i, j] += np.linalg.det(term)
    return result


def instrument():
    """All seventeen actual positive square-root Kraus matrices on C^256."""
    block = [16 * i + j for i in range(1, 5) for j in range(1, 5)]

    def embed(A):
        v = np.zeros(DIM)
        v[block] = A.reshape(-1)
        return v

    u = embed(np.eye(4)) / 2
    vs = []
    metric = [1, -1, -1, -1]
    for i, j in combinations(range(4), 2):
        J = np.zeros((4, 4))
        J[i, j], J[j, i] = 1, -metric[i] * metric[j]
        vs.append(embed(J) / math.sqrt(2))
    pu = np.outer(u, u)
    pv = sum((np.outer(v, v) for v in vs), np.zeros((DIM, DIM)))
    pi = np.zeros((DIM, DIM))
    pi[block, block] = 1
    prem = pi - pu - pv
    identity = np.eye(DIM)
    effects, kraus = [], []
    for v in vs:
        for sign in (1, -1):
            f = 2 * (u + sign * v)
            effects.append(KAPPA * np.outer(f, f))
            kraus.append(math.sqrt(KAPPA / 8) * np.outer(f, f))
    effects.append(48 * KAPPA * pu + 88 * KAPPA * pv + 96 * KAPPA * prem)
    kraus.append(math.sqrt(48 * KAPPA) * pu + math.sqrt(88 * KAPPA) * pv
                 + math.sqrt(96 * KAPPA) * prem)
    for scale in [G * P * BELL, P * G * BELL, P * P * BELL]:
        effects.append(scale * identity)
        kraus.append(math.sqrt(scale) * identity)
    bell_block = 1 - BELL * (1 + 3 * G * G)
    bell_complement = 1 - BELL * (1 - G * G)
    effects.append(bell_block * pi + bell_complement * (identity - pi))
    kraus.append(math.sqrt(bell_block) * pi + math.sqrt(bell_complement) * (identity - pi))
    assert bell_block > 0 and bell_complement > 0
    close(sum(effects), identity)
    for E, M in zip(effects, kraus):
        close(M.T @ M, E)
    close(sum(M.T @ M for M in kraus), identity)
    return np.asarray(kraus), np.asarray(effects), pi


J23 = np.zeros((4, 4))
J23[2, 3], J23[3, 2] = 1, -1
CAR_J23 = induced_generator(J23)


def state_jets(theta, m):
    """Fixed preparation Omega16; P(theta)=exp(theta J23/m), all k<=m.

    The scalar field norm is |dtheta|.  ||dpsi_k||=k/(m sqrt(2)), so
    B=1/sqrt(2) bounds EVERY actual prefix and ideal completed state.
    Preparation/reference/fiber jets are supplied as zero in this fixture.
    """
    states, jets = [], []
    for k in range(m + 1):
        a = k * theta / m
        Pk = np.eye(4)
        Pk[2, 2] = Pk[3, 3] = math.cos(a)
        Pk[2, 3], Pk[3, 2] = math.sin(a), -math.sin(a)
        V = exterior(Pk)
        DV = (k / m) * CAR_J23 @ V
        close(V.T @ V, np.eye(16))
        close(V.T @ V / 16, np.eye(16) / 16)
        states.append(V.reshape(-1) / 4)
        jets.append(DV.reshape(-1) / 4)
        close(np.linalg.norm(jets[-1]), k / (m * math.sqrt(2)))
        # The mass on EACH grade is present and unchanged, including grades0,4.
        for degree in range(5):
            rows = [i for i, s in enumerate(SUBSETS) if len(s) == degree]
            close(np.sum(V[rows] ** 2) / 16, math.comb(4, degree) / 16)
    return np.asarray(states), np.asarray(jets)


def distribution_entropy(probabilities, jets=None):
    probabilities = np.asarray(probabilities)
    assert float(np.min(probabilities)) >= 0
    nonzero = probabilities > 0  # Exact zero extension, no positive floor.
    entropy = -float(np.sum(probabilities[nonzero] * np.log(probabilities[nonzero])))
    if jets is None:
        return entropy
    # When q=||a||^2=0 its actual analytic first jet is zero.
    assert np.max(np.abs(np.asarray(jets)[~nonzero]), initial=0) <= SOURCE_ATOL
    source = -float(np.sum(np.asarray(jets)[nonzero] * np.log(probabilities[nonzero])))
    return entropy, source


def readout(kraus, states, jets):
    amplitude = np.einsum("rij,kj->kri", kraus, states)
    derivative = np.einsum("rij,kj->kri", kraus, jets)
    q = np.einsum("kri,kri->kr", amplitude, amplitude)
    dq = 2 * np.einsum("kri,kri->kr", amplitude, derivative)
    close(np.sum(q, axis=1), 1)
    close(np.sum(dq, axis=1), 0)
    return amplitude, derivative, q, dq


def prefix_masses(m, cap):
    failed = np.array([math.comb(cap, k) * G ** k * P ** (cap - k) for k in range(m)])
    epsilon = float(np.sum(failed))
    return np.append(failed, 1 - epsilon), epsilon


def trace_norm_hermitian(A):
    return float(np.sum(np.abs(np.linalg.eigvalsh((A + A.T.conj()) / 2))))


def spectral_source(A, DA, eta=None):
    """Full amplitude derivative with a bounded numerical SVD resolution.

    Any singular value below roundoff is omitted with an explicit gradient
    error budget; no positive probability/eigenvalue is replaced by a floor.
    Eigenvalues down to 5.7e-23 are actually retained in rank-birth controls.
    All full output matrices remain DIM x DIM.
    """
    U, singular, _ = np.linalg.svd(A, full_matrices=False)
    active = singular > SINGULAR_ROUNDOFF
    omitted_gradient_bound = (2 * math.sqrt(int(np.sum(~active))) * SINGULAR_ROUNDOFF
                              * abs(math.log(SINGULAR_ROUNDOFF ** 2)))
    assert omitted_gradient_bound * np.linalg.norm(DA) < SOURCE_ATOL
    U, singular = U[:, active], singular[active]
    lam = singular * singular
    coords = U.T.conj() @ A
    if eta is None:
        logs = np.log(lam)
        entropy = -float(np.sum(lam * logs))
    else:
        assert 0 < eta <= 1
        logs = np.log(lam + eta)
        entropy = float(np.sum(-(lam + eta) * logs + eta * math.log(eta)))
    # The +1 term cancels because Tr D(AA*)=0 in this normalized fixture.
    close(2 * np.vdot(A, DA).real, 0)
    source = -2 * float(np.vdot(DA, U @ (logs[:, None] * coords)).real)
    return entropy, source, lam


def spectral_diagnostics(A, DA):
    """Expose the finite precision resolution separately from the theorem."""
    singular = np.linalg.svd(A, compute_uv=False)
    retained = singular[singular > SINGULAR_ROUNDOFF]
    discarded = singular[singular <= SINGULAR_ROUNDOFF]
    bound = (2 * math.sqrt(len(discarded)) * SINGULAR_ROUNDOFF
             * abs(math.log(SINGULAR_ROUNDOFF ** 2)) * np.linalg.norm(DA))
    return {"retained_singular_values": len(retained),
            "discarded_roundoff_singular_values": len(discarded),
            "smallest_retained_singular_value": float(min(retained)),
            "largest_discarded_singular_value": float(max(discarded, default=0)),
            "omitted_source_absolute_bound": float(bound)}


def direct_leaf_checks(m, cap, theta, kraus, amplitudes, derivatives, q, dq, mu):
    states, jets = state_jets(theta, m)
    single_V = (states[1] * 4).reshape(16, 16)
    single_DV = (jets[1] * 4).reshape(16, 16)
    leaves = stopped_leaves(m, cap)
    ws, ks, all_q, all_dq = [], [], [], []
    archive_columns, archive_jets = [], []
    raw_code = real_clock = 0.0
    for word, k in leaves:
        branch = np.eye(16) / 4
        dbranch = np.zeros((16, 16))
        for flag in word:
            if flag:
                dbranch = P * (single_DV @ branch + single_V @ dbranch)
                branch = P * single_V @ branch
            else:
                branch *= math.sqrt(P)
                dbranch *= math.sqrt(P)
        w = P ** (len(word) + k)
        close(np.linalg.norm(branch) ** 2, w)
        close(branch.reshape(-1), math.sqrt(w) * states[k])
        close(dbranch.reshape(-1), math.sqrt(w) * jets[k])
        actual_a = np.einsum("rij,j->ri", kraus, branch.reshape(-1))
        actual_da = np.einsum("rij,j->ri", kraus, dbranch.reshape(-1))
        actual_q = np.sum(actual_a * actual_a, axis=1)
        actual_dq = 2 * np.sum(actual_a * actual_da, axis=1)
        close(actual_q, w * q[k])
        close(actual_dq, w * dq[k])
        ws.append(w)
        ks.append(k)
        all_q.append(actual_q)
        all_dq.append(actual_dq)
        archive_columns.append(actual_a.T)
        archive_jets.append(actual_da.T)
        raw_code += w * (len(word) + k)
        real_clock += w * len(word)
    ws, ks = np.array(ws), np.array(ks)
    Q, DQ = np.asarray(all_q), np.asarray(all_dq)
    close(sum(ws), 1)
    close(distribution_entropy(ws) / ELL, raw_code)
    close(raw_code, (1 + G) * real_clock)
    Hw = distribution_entropy(ws)
    Hk = [distribution_entropy(q[k], dq[k]) for k in range(m + 1)]
    Hjoint, DHjoint = distribution_entropy(Q, DQ)
    close(Hjoint, Hw + sum(w * Hk[k][0] for w, k in zip(ws, ks)))
    close(DHjoint, sum(w * Hk[k][1] for w, k in zip(ws, ks)), SOURCE_ATOL)
    reference = ws[:, None] * mu[None, :]
    positive = Q > 0
    relative = float(np.sum(Q[positive] * np.log(Q[positive] / reference[positive]))) / ELL
    drelative = float(np.sum(DQ[positive] * np.log(Q[positive] / reference[positive]))) / ELL
    Dk = [relative_code(q[k], dq[k], mu) for k in range(m + 1)]
    close(relative, sum(w * Dk[k][0] for w, k in zip(ws, ks)), SOURCE_ATOL)
    close(drelative, sum(w * Dk[k][1] for w, k in zip(ws, ks)), SOURCE_ATOL)

    A = np.concatenate(archive_columns, axis=1)
    DA = np.concatenate(archive_jets, axis=1)
    # Full archive FR is retained.  Explicit Gram spectra are checked where
    # its actual dimension is small; cap7 still uses every word in AA*.
    rho = A @ A.T
    derivative = DA @ A.T + A @ DA.T
    masses, _ = prefix_masses(m, cap)
    grouped_A = np.concatenate([math.sqrt(w) * a.T for w, a in zip(masses, amplitudes)], axis=1)
    grouped_DA = np.concatenate([math.sqrt(w) * a.T for w, a in zip(masses, derivatives)], axis=1)
    close(rho, grouped_A @ grouped_A.T)
    close(derivative, grouped_DA @ grouped_A.T + grouped_A @ grouped_DA.T)
    S, DS, spectrum = spectral_source(A, DA)
    Sg, DSg, _ = spectral_source(grouped_A, grouped_DA)
    close(S, Sg, SOURCE_ATOL)
    close(DS, DSg, SOURCE_ATOL)
    code_lengths = -np.log(mu) / ELL
    coherent_relative = -S / ELL - float(np.sum(Q * np.log(reference))) / ELL
    coherent_relative_source = -DS / ELL - float(np.sum(DQ * np.log(reference))) / ELL
    close(coherent_relative,
          Hw / ELL + sum(w * np.dot(q[k], code_lengths) for w, k in zip(ws, ks)) - S / ELL,
          SOURCE_ATOL)
    close(coherent_relative_source,
          sum(w * np.dot(dq[k], code_lengths) for w, k in zip(ws, ks)) - DS / ELL,
          SOURCE_ATOL)
    archive_dimension = A.shape[1]
    if cap <= 4:
        archive = A.T @ A
        archive_lam = np.linalg.eigvalsh(archive)
        complement_lam = np.linalg.eigvalsh(rho)
        # Compare with padded spectra, including all exact zero modes.
        padded = np.pad(archive_lam, (DIM - len(archive_lam), 0))
        close(padded, complement_lam)
    return {"cap": cap, "all_leaf_words": len(leaves), "FR_dimension": archive_dimension,
            "raw_golden_flag_code": raw_code, "actual_expected_attempts": real_clock,
            "classical_joint_entropy": Hjoint, "classical_joint_source": DHjoint,
            "relative_code_source": drelative, "coherent_archive_entropy": S,
            "coherent_archive_source": DS, "coherent_relative_code_value": coherent_relative,
            "coherent_relative_code_source": coherent_relative_source,
            "nonzero_complement_rank": len(spectrum)}


def relative_code(q, dq, mu):
    positive = q > 0
    value = float(np.sum(q[positive] * np.log(q[positive] / mu[positive]))) / ELL
    source = float(np.sum(dq[positive] * np.log(q[positive] / mu[positive]))) / ELL
    return value, source


def cap_checks(m, cap, amplitudes, derivatives, q, dq, mu):
    B = 1 / math.sqrt(2)
    masses, epsilon = prefix_masses(m, cap)
    Hk = [distribution_entropy(a, da) for a, da in zip(q, dq)]
    Dk = [relative_code(a, da, mu) for a, da in zip(q, dq)]
    H, DH = np.array(masses) @ np.array(Hk)
    D, DD = np.array(masses) @ np.array(Dk)
    H0, DH0 = Hk[-1]
    D0, DD0 = Dk[-1]
    shannon_bound = 8 * epsilon * B * math.sqrt(OUTCOMES) / math.e
    code_lengths = -np.log(mu) / ELL
    code_bound = epsilon * B * (4 * max(code_lengths)
                                + 8 * math.sqrt(OUTCOMES) / (math.e * ELL))
    assert abs(H - H0) <= epsilon * math.log(OUTCOMES) + MATRIX_ATOL
    assert abs(DH - DH0) <= shannon_bound + SOURCE_ATOL
    assert abs(DD - DD0) <= code_bound + SOURCE_ATOL
    for _, source in Hk:
        assert abs(source) <= 4 * B * math.sqrt(OUTCOMES) / math.e + SOURCE_ATOL
    A = np.concatenate([math.sqrt(w) * a.T for w, a in zip(masses, amplitudes)], axis=1)
    DA = np.concatenate([math.sqrt(w) * a.T for w, a in zip(masses, derivatives)], axis=1)
    A0, DA0 = amplitudes[-1].T, derivatives[-1].T
    rho, rho0 = A @ A.T, A0 @ A0.T
    drho = DA @ A.T + A @ DA.T
    drho0 = DA0 @ A0.T + A0 @ DA0.T
    distance = trace_norm_hermitian(rho - rho0)
    jet_distance = trace_norm_hermitian(drho - drho0)
    assert distance <= 2 * epsilon + MATRIX_ATOL
    assert jet_distance <= 4 * epsilon * B + MATRIX_ATOL
    assert trace_norm_hermitian(drho0) <= 2 * B + MATRIX_ATOL
    assert np.linalg.norm(DA) <= B + MATRIX_ATOL
    assert np.linalg.norm(DA0) <= B + MATRIX_ATOL
    S, DS, spectrum = spectral_source(A, DA)
    S0, DS0, ideal_spectrum = spectral_source(A0, DA0)
    regularization = []
    for eta in [1e-3, 1e-6, epsilon ** (2 / 3)]:
        _, DSeta, _ = spectral_source(A, DA, eta)
        _, DS0eta, _ = spectral_source(A0, DA0, eta)
        approximation_bound = 2 * B * math.sqrt(DIM * eta)
        assert abs(DS - DSeta) <= approximation_bound + SOURCE_ATOL
        assert abs(DS0 - DS0eta) <= approximation_bound + SOURCE_ATOL
        channel_bound = 4 * epsilon * B * (math.log(1 / eta) + math.log(2) + 1 / eta)
        assert abs(DSeta - DS0eta) <= channel_bound + SOURCE_ATOL
        full_bound = 4 * B * math.sqrt(DIM * eta) + channel_bound
        assert abs(DS - DS0) <= full_bound + SOURCE_ATOL
        regularization.append({"eta": eta, "source_regularization_error": abs(DS - DSeta),
                               "ideal_regularization_error": abs(DS0 - DS0eta),
                               "each_amplitude_bound": approximation_bound,
                               "regularized_source_difference": abs(DSeta - DS0eta),
                               "regularized_difference_bound": channel_bound})
    no_floor_bound = 4 * B * ((math.sqrt(DIM) + 1) * epsilon ** (1 / 3)
                             + epsilon * ((2 / 3) * math.log(1 / epsilon) + math.log(2)))
    assert abs(DS - DS0) <= no_floor_bound + SOURCE_ATOL
    coherent_code_source = float(masses @ (dq @ code_lengths)) - DS / ELL
    coherent_code_ideal_source = float(dq[-1] @ code_lengths) - DS0 / ELL
    coherent_code_bound = 4 * epsilon * B * max(code_lengths) + no_floor_bound / ELL
    assert abs(coherent_code_source - coherent_code_ideal_source) <= coherent_code_bound + SOURCE_ATOL
    # With epsilon=0 use the SAME grouped construction, including exact zero
    # failed columns; this verifies the first derivative at its rank change.
    zero_masses = [0] * m + [1]
    zero_A = np.concatenate([math.sqrt(w) * a.T for w, a in zip(zero_masses, amplitudes)], axis=1)
    zero_DA = np.concatenate([math.sqrt(w) * a.T for w, a in zip(zero_masses, derivatives)], axis=1)
    close(zero_A @ zero_A.T, rho0)
    close(zero_DA @ zero_A.T + zero_A @ zero_DA.T, drho0)
    zero_S, zero_DS, _ = spectral_source(zero_A, zero_DA)
    close(zero_S, S0, SOURCE_ATOL)
    close(zero_DS, DS0, SOURCE_ATOL)
    assert abs(DD0) > 1e-7  # Hostile control: successful price source survives.
    return {"cap": cap, "failure_probability": epsilon,
            "shannon_source_error": abs(DH - DH0), "shannon_source_bound": shannon_bound,
            "fixed_code_source": DD, "ideal_fixed_code_source": DD0,
            "fixed_code_source_error": abs(DD - DD0), "fixed_code_source_bound": code_bound,
            "coherent_entropy": S, "ideal_coherent_entropy": S0,
            "coherent_source": DS, "ideal_coherent_source": DS0,
            "coherent_source_error": abs(DS - DS0), "coherent_no_floor_bound": no_floor_bound,
            "coherent_relative_code_source": coherent_code_source,
            "ideal_coherent_relative_code_source": coherent_code_ideal_source,
            "coherent_relative_code_source_error": abs(coherent_code_source - coherent_code_ideal_source),
            "coherent_relative_code_source_bound": coherent_code_bound,
            "channel_trace_distance": distance, "channel_jet_trace_distance": jet_distance,
            "nonzero_output_rank": len(spectrum), "ideal_nonzero_output_rank": len(ideal_spectrum),
            "actual_SVD_resolution": spectral_diagnostics(A, DA),
            "ideal_SVD_resolution": spectral_diagnostics(A0, DA0),
            "regularization": regularization}


def dark_checks(theta, m, kraus, mu):
    # The exact SymPy computation above proves this is an actual zero, despite
    # the unavoidable sin/cos roundoff in the numerical representative.
    dark_index = 11
    states, jets = state_jets(theta, m)
    a, da, q, dq = readout(kraus, states, jets)
    assert q[m, dark_index] < 1e-30
    assert abs(dq[m, dark_index]) < 1e-18
    assert np.linalg.norm(da[m, dark_index]) > 1e-4
    # Entropy's derivative at the zero block is exactly zero.  Check continuity
    # on both actual sides, using analytic jets, without replacing q by a floor.
    controls = []
    for delta in [1e-2, 1e-3, 1e-4, 1e-5]:
        side_sources = []
        for sign in [-1, 1]:
            s, ds = state_jets(theta + sign * delta, m)
            _, _, qs, dqs = readout(kraus, s, ds)
            z, dz = qs[m, dark_index], dqs[m, dark_index]
            assert z > 0
            side_sources.append(-dz * (math.log(z) + 1))
        controls.append({"distance": delta, "dark_entropy_derivatives": side_sources})
    maximums = [max(abs(v) for v in row["dark_entropy_derivatives"]) for row in controls]
    assert all(a > b > 0 for a, b in zip(maximums, maximums[1:]))
    assert maximums[-1] < 1e-8
    _, full_source = distribution_entropy(q[m], dq[m])
    _, price_source = relative_code(q[m], dq[m], mu)
    # Full Shannon and fixed-code derivatives agree with central differences
    # across the rank birth.  Finite differences are only an independent check
    # of analytic jets, never the primary source calculation.
    finite_differences = []
    for step in [1e-3, 1e-4, 1e-5]:
        results = []
        for sign in [-1, 1]:
            s, ds = state_jets(theta + sign * step, m)
            aa, daa, qq, dqq = readout(kraus, s, ds)
            H = distribution_entropy(qq[m])
            D = relative_code(qq[m], dqq[m], mu)[0]
            S = spectral_source(aa[m].T, daa[m].T)[0]
            results.append(np.array([H, D, S]))
        finite_differences.append((results[1] - results[0]) / (2 * step))
    coherent_source = spectral_source(a[m].T, da[m].T)[1]
    close(finite_differences[-1], [full_source, price_source, coherent_source], 1e-9)
    return {"marked_label_index": dark_index, "actual_probability_roundoff": float(q[m, dark_index]),
            "actual_probability_jet_roundoff": float(dq[m, dark_index]),
            "nonzero_amplitude_jet_norm": float(np.linalg.norm(da[m, dark_index])),
            "exact_dark_entropy_first_derivative": 0,
            "two_sided_rank_birth_controls": controls,
            "analytic_sources_at_dark": [full_source, price_source, coherent_source],
            "central_difference_last": finite_differences[-1].tolist()}


def moving_instrument_checks(theta, m, kraus, mu):
    """Supply, rather than silently freeze, two actual instrument first jets."""
    states, jets = state_jets(theta, m)
    amplitudes, derivatives, q, dq = readout(kraus, states, jets)
    A, DA = amplitudes[-1].T, derivatives[-1].T
    S, DS, _ = spectral_source(A, DA)
    J12 = np.zeros((4, 4))
    J12[1, 2], J12[2, 1] = 1, -1
    output_generator = np.kron(induced_generator(J12), np.eye(16))
    close(output_generator.T, -output_generator)
    close(np.linalg.norm(output_generator, ord=2), 1)
    # Local moving residual isometry (I_R tensor exp(t L_Q))W.  The
    # complement acquires [L,rho]; entropy is unchanged under that unitary.
    moving_DA = DA + output_generator @ A
    Sm, DSm, _ = spectral_source(A, moving_DA)
    rho = A @ A.T
    drho = DA @ A.T + A @ DA.T
    moving_drho = moving_DA @ A.T + A @ moving_DA.T
    commutator = output_generator @ rho - rho @ output_generator
    close(moving_drho - drho, commutator)
    channel_jet_change = trace_norm_hermitian(commutator)
    assert channel_jet_change > 0.1
    close(Sm, S)
    close(DSm, DS, SOURCE_ATOL)
    total_B = 1 / math.sqrt(2) + 1
    assert np.linalg.norm(moving_DA) <= total_B + MATRIX_ATOL
    close(2 * np.sum(A * moving_DA, axis=0), dq[-1])

    # A moving pointer basis mixes marks with Bellfail.  This preserves C
    # exactly but changes the actually read probability law and code source.
    # The state is held fixed for this second variation: all derivative is DW.
    pointer_DA = np.zeros_like(A)
    pointer_DA[:, 0], pointer_DA[:, 16] = A[:, 16], -A[:, 0]
    close(pointer_DA @ A.T + A @ pointer_DA.T, 0)
    _, pointer_entropy_source, _ = spectral_source(A, pointer_DA)
    close(pointer_entropy_source, 0, SOURCE_ATOL)
    moving_dq = 2 * np.sum(A * pointer_DA, axis=0)
    close(sum(moving_dq), 0)
    assert np.linalg.norm(moving_dq) > 1e-4
    lengths = -np.log(mu) / ELL
    _, moving_shannon_source = distribution_entropy(q[-1], moving_dq)
    moving_coherent_code_source = float(moving_dq @ lengths) - pointer_entropy_source / ELL
    assert abs(moving_coherent_code_source) > 1e-3
    # Analytic isometry-jet condition W*DW+(DW)*W=0, on the FULL input carrier.
    moving_kraus = np.zeros_like(kraus)
    moving_kraus[0], moving_kraus[16] = kraus[16], -kraus[0]
    close(sum(M.T @ DM + DM.T @ M for M, DM in zip(kraus, moving_kraus)), 0)
    return {"residual_output_unitary": {
                "actual_channel_jet_change_trace_norm": channel_jet_change,
                "entropy_source_before": DS, "entropy_source_after": DSm,
                "supplied_state_plus_instrument_jet_bound": total_B},
            "pointer_rotation": {
                "complement_channel_jet": 0,
                "actual_probability_jet_norm": float(np.linalg.norm(moving_dq)),
                "actual_Shannon_source": moving_shannon_source,
                "actual_coherent_relative_code_source": moving_coherent_code_source,
                "frozen_instrument_would_give": 0}}


def coherent_rank_birth_checks(kraus):
    m, cap = 2, 7
    masses, _ = prefix_masses(m, cap)

    def actual(theta):
        states, jets = state_jets(theta, m)
        amplitudes, derivatives, _, _ = readout(kraus, states, jets)
        A = np.concatenate([math.sqrt(w) * a.T for w, a in zip(masses, amplitudes)], axis=1)
        DA = np.concatenate([math.sqrt(w) * a.T for w, a in zip(masses, derivatives)], axis=1)
        return spectral_source(A, DA)

    _, source0, spectrum0 = actual(0)
    # At theta=0, all prefixes coincide.  Their images span the six v_a,
    # u and the full Omega16 (whose other grades are nonzero): rank exactly8.
    assert len(spectrum0) == 8
    close(source0, 0, SOURCE_ATOL)
    rows = []
    for delta in [1e-2, 1e-3, 1e-4]:
        sides, minima = [], []
        for sign in [-1, 1]:
            _, source, spectrum = actual(sign * delta)
            assert len(spectrum) == 11
            sides.append(source)
            minima.append(float(min(spectrum)))
        close(sides[0], -sides[1], SOURCE_ATOL)
        rows.append({"distance": delta, "actual_coherent_sources": sides,
                     "smallest_retained_positive_eigenvalues": minima,
                     "actual_output_rank": 11})
    maxima = [max(abs(s) for s in row["actual_coherent_sources"]) for row in rows]
    assert all(a > b > 0 for a, b in zip(maxima, maxima[1:]))
    assert max(rows[-1]["smallest_retained_positive_eigenvalues"]) < 1e-20
    return {"m": m, "cap": cap, "rank_at_zero": len(spectrum0),
            "source_at_zero_roundoff": source0, "two_sided_controls": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    exact = exact_checks()
    kraus, effects, pi = instrument()
    theta, m = math.acos(1 / 3), 2
    states, jets = state_jets(theta, m)
    amplitudes, derivatives, q, dq = readout(kraus, states, jets)
    _, lengths, mu = golden_prefix_code()
    close(sum(mu), 1)
    # Actual all-grade Choi readout, including grade-one mass1/4 and all
    # completion labels, agrees with the declared seventeen probabilities.
    close(np.einsum("ki,ij,kj->k", states, pi, states), 1 / 4)
    for k in range(m + 1):
        close(np.einsum("i,rij,j->r", states[k], effects, states[k]), q[k])
    # A genuine pointer coherence is retained.  Neither archive entropy is
    # silently replaced by entropy of the measured probability diagonal.
    pointer = amplitudes[-1] @ amplitudes[-1].T
    pointer_coherence = float(np.linalg.norm(pointer - np.diag(np.diag(pointer))))
    assert pointer_coherence > 1e-3
    H0 = distribution_entropy(q[-1])
    S0 = spectral_source(amplitudes[-1].T, derivatives[-1].T)[0]
    assert abs(H0 - S0) > 1e-4
    generic_states, generic_jets = state_jets(0.73, m)
    generic_a, generic_da, generic_q, generic_dq = readout(kraus, generic_states, generic_jets)
    generic_H, generic_DH = distribution_entropy(generic_q[-1], generic_dq[-1])
    generic_S, generic_DS, _ = spectral_source(generic_a[-1].T, generic_da[-1].T)
    assert abs(generic_H - generic_S) > 1e-4
    assert abs(generic_DH - generic_DS) > 1e-8
    leaf_checks = [direct_leaf_checks(m, cap, theta, kraus, amplitudes, derivatives, q, dq, mu)
                   for cap in [3, 4, 7]]
    caps = [cap_checks(m, cap, amplitudes, derivatives, q, dq, mu) for cap in [7, 20, 40, 60]]
    assert all(a["failure_probability"] > b["failure_probability"] for a, b in zip(caps, caps[1:]))
    assert caps[-1]["fixed_code_source_error"] < caps[0]["fixed_code_source_error"] * 1e-6
    assert abs(caps[-1]["fixed_code_source"] - caps[-1]["ideal_fixed_code_source"]) < 1e-10
    # The owned N=ceil(2m/g) tail theorem is checked independently of entropy.
    tails = []
    for successes in [1, 2, 3, 5, 10, 25, 100]:
        cap = math.ceil(2 * successes / G)
        _, epsilon = prefix_masses(successes, cap)
        bound = math.exp(-successes / 4)
        assert epsilon <= bound
        tails.append({"m": successes, "cap": cap, "failure_probability": epsilon,
                      "exp_minus_m_over_4": bound})
    receipt = {"status": "PASS", "exact": exact,
               "carrier": {"CAR_dimension": 16, "joint_Choi_dimension": DIM,
                           "all_grades": [1, 4, 6, 4, 1], "pre_readout_right_Gram": "I16/16",
                           "Kraus_count": OUTCOMES, "instrument": "fixed positive square roots",
                           "field_chart": "P(theta)=exp(theta*J23/m), scalar norm abs(dtheta)",
                           "prefix_jet_bound_B": 1 / math.sqrt(2),
                           "supplied_preparation_reference_fiber_jets": "zero"},
               "tolerances": {"matrix_absolute": MATRIX_ATOL, "source_absolute": SOURCE_ATOL,
                              "SVD_roundoff_singular_value": SINGULAR_ROUNDOFF,
                              "finite_difference_absolute": 1e-9,
                              "probability_floor_used": False, "spectral_floor_used": False},
               "numerical_resolution_scope": (
                   "spectral_floor_used=false describes the analytic theorem and the absence of "
                   "positive eigenvalue replacement; numerical SVD omits singular values at or "
                   "below 1e-15 with the reported source error budget, below source_absolute. "
                   "Rank-birth controls retain positive eigenvalues below 1e-20."),
               "ideal_pointer_off_diagonal_Frobenius_norm": pointer_coherence,
               "ideal_pointer_Shannon_entropy": H0, "ideal_complementary_entropy": S0,
               "generic_distinct_Shannon_coherent": {
                   "theta": 0.73, "Shannon_entropy": generic_H, "coherent_entropy": generic_S,
                   "Shannon_source": generic_DH, "coherent_source": generic_DS},
               "full_leaf_checks": leaf_checks, "cap_source_checks": caps,
               "owned_exponential_cap_checks": tails, "dark_outcome": dark_checks(theta, m, kraus, mu),
               "moving_instrument": moving_instrument_checks(theta, m, kraus, mu),
               "coherent_rank_birth": coherent_rank_birth_checks(kraus),
               "scope": "conditional mathematical terminal component; physical Book Info/admission and GR closure not derived"}
    result = json.dumps(receipt, indent=2, ensure_ascii=False, allow_nan=False)
    print(result)
    if args.receipt:
        args.receipt.write_text(result + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
