"""Actual primary preparation and original single-round Julia row actions.

The pinned predecessor supplies definitions only; its main/replay is not run.
Every output record and every reference column remains in the calculation.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import math
import os
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
PRIOR = (ROOT / "02_REGISTRY/research/sources/"
         "d0_primary_native_domain_source_2026-10-20/check_primary_domain_source.py")
PRIOR_SHA256 = "c67285c7469db49ff61f3e52597d0bcc6aad991ec1f7af025d6daeb065a43edf"
if hashlib.sha256(PRIOR.read_bytes()).hexdigest() != PRIOR_SHA256:
    raise ArithmeticError("primary predecessor source pin")
_spec = importlib.util.spec_from_file_location("owned_primary_definitions", PRIOR)
OWNED = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(OWNED)
P = OWNED.P


def require(condition, message):
    if not bool(condition):
        raise ArithmeticError(message)


def adjoint(a):
    return a.swapaxes(-1, -2).conj()


def square_root_jet(radicand, derivative=None):
    values, vectors = np.linalg.eigh((radicand + adjoint(radicand)) / 2)
    require(float(values.min()) > .5, "strict actual local Julia radicands")
    roots = np.sqrt(values)
    matrix = (vectors * roots[..., None, :]) @ adjoint(vectors)
    if derivative is None:
        return matrix, None, 0.
    inside = adjoint(vectors) @ derivative @ vectors
    delta = vectors @ (inside / (roots[..., :, None] + roots[..., None, :])) @ adjoint(vectors)
    residual = float(np.max(np.abs(matrix @ delta + delta @ matrix - derivative)))
    require(residual < 8e-14, "actual local Sylvester defect derivative")
    return matrix, delta, residual


def physical_isometry():
    """Original Walsh/Golden 128 outputs from exactly 33 compressed vectors."""
    integer_g = np.zeros((64, 32), dtype=np.int64)
    for label in range(32):
        for coefficient in range(2):
            for word in range(16):
                first = (-1) ** ((label & (2 * word)).bit_count())
                second = (-1) ** ((label & (2 * word + 1)).bit_count())
                integer_g[2 * label + coefficient, 2 * word + coefficient] = (first + second) // 2
    require(np.array_equal(integer_g.T @ integer_g, 16 * np.eye(32, dtype=np.int64)),
            "exact dyadic Walsh G*G identity")
    g = integer_g / 4.
    b = np.zeros((128, 33))
    b[0, 0], b[1, 0] = math.sqrt(P), -P
    b[0::2, 1:], b[1::2, 1:] = P * g, math.sqrt(P) * g
    require(np.max(np.abs(b.T @ b - np.eye(33))) < 5e-16,
            "physical128 by33 Golden isometry")
    return b, g


class PrimaryFixture:
    def __init__(self):
        self.size, self.sites, self.ell = 4, 256, .25
        self.indices = np.array(list(itertools.product(range(4), repeat=4)))
        self.forward, self.backward = [], []
        for role in range(4):
            plus, minus = self.indices.copy(), self.indices.copy()
            plus[:, role] = (plus[:, role] + 1) % 4
            minus[:, role] = (minus[:, role] - 1) % 4
            self.forward.append(np.ravel_multi_index(plus.T, (4,) * 4))
            self.backward.append(np.ravel_multi_index(minus.T, (4,) * 4))
        self.counts = OWNED.original_counts(20, 4)
        self.rho = 256 * self.counts / int(self.counts.sum())
        self.characters = OWNED.reference_characters(4, self.indices)
        self.chart_bound = (math.sqrt(float(self.rho.max())) *
                            (math.sqrt(2) + .2 / (2 * math.sqrt(2))) *
                            math.exp(.2 * max(np.linalg.norm(a, 2) for a in OWNED.GN)))
        self.exponent, self.scale = 0, 1.
        while self.scale * self.chart_bound > P:
            self.exponent += 1
            self.scale = P ** self.exponent
        require(self.exponent == 3, "same original fixed primary Golden scale")
        self.alpha = P * P * self.ell ** 2 / 128
        self.epsilon = 2 * self.alpha
        self.amplitude = self.scale ** 2 * .005
        self.history = [np.array([self.amplitude, 0.])]
        for j in range(4):
            self.history.append(self.history[-1] + self.ell * self.psi_prime((j + .5) * self.ell))
        q = 1 - 2 ** -20 * 4 * P ** 3
        r = 1 - 2 ** -20 * 4 * P ** 3 * (1 + P ** 6)
        self.lam = -2 * P ** -5 * (r / q + P ** 6)
        self.b, self.g = physical_isometry()
        selected = np.all(self.indices == np.array([1, 1, 2, 2]), axis=1)
        self.edge = int(np.flatnonzero(selected)[0])

    def psi_prime(self, time):
        return self.amplitude * np.array([-2 * math.pi * math.sin(2 * math.pi * time),
                                          1.2 * math.pi * math.cos(2 * math.pi * time)])

    def preparation(self, flat):
        psi = np.zeros((256, 2)) if flat else np.array(self.history[:-1])[self.indices[:, 0]]
        psi_s = psi / self.scale ** 2
        state = np.zeros((256, 16))
        state[:, 0], state[:, 15] = psi_s[:, 0], psi_s[:, 1]
        state[:, 1] = math.sqrt(P)
        state[:, 14] = np.sqrt(1 - P - np.sum(psi_s ** 2, axis=1))
        prepared = self.characters[:, None, :] * state[:, :, None] / math.sqrt(128)
        matrix = prepared.reshape(4096, 128)
        require(np.max(np.abs(matrix.T @ matrix - np.eye(128) / 128)) < 3e-16,
                "same fullRIGHT128 preparation with original rest-clock state")
        return prepared

    def geometry(self, amplitude):
        if amplitude is None:
            return np.zeros(256), np.zeros((256, 2))
        time = self.indices[:, 0] * self.ell
        x, y = self.indices[:, 2] * self.ell - .5, self.indices[:, 3] * self.ell - .5

        def profile(tau, xx, yy):
            energy = np.array([np.dot(self.psi_prime(t), self.psi_prime(t)) for t in tau])
            return (-self.lam * energy * (xx * xx + yy * yy) + amplitude *
                    (1 + .2 * np.sin(2 * math.pi * tau)) * (xx * xx - yy * yy))

        h = profile(time - self.ell / 2, x, y)
        advance = profile(time + self.ell / 2, x, y)
        k = np.stack((.5 * (advance - profile(time + self.ell / 2, x - self.ell, y)),
                      .5 * (advance - profile(time + self.ell / 2, x, y - self.ell))), axis=1)
        return h, k

    def base(self, amplitude):
        h, k = self.geometry(amplitude)
        e = np.broadcast_to(np.eye(4), (256, 4, 4)).copy()
        e[:, 1, 0] = h / 2
        rest = OWNED.T @ e
        legs = self.scale * np.sqrt(self.rho)[:, None, None] * (
            OWNED.ETA @ np.linalg.inv(rest).transpose(0, 2, 1))
        c = np.einsum("zar,aij->zrij", legs, OWNED.CREATORS)
        x = c.copy()
        x[:, 0] = c[:, 0] @ OWNED.lift(k)
        return {"c": c, "x": x, "k": k, "prep": self.preparation(amplitude is None)}

    def varied(self, base, variation, parameter, with_jet):
        c, x = base["c"].copy(), base["x"].copy()
        dc, dx = np.zeros_like(c), np.zeros_like(x)
        if variation == "uniform_coframe" or variation.startswith("coframe_role_"):
            roles = range(4) if variation == "uniform_coframe" else (int(variation[-1]),)
            for role in roles:
                c[:, role] *= math.exp(-parameter)
                x[:, role] *= math.exp(-parameter)
                if with_jet:
                    dc[:, role], dx[:, role] = -c[:, role], -x[:, role]
        elif variation == "interior_u_link_N2":
            k = base["k"][self.edge].copy()
            k[0] += parameter
            ll = OWNED.lift(k)
            x[self.edge, 0] = c[self.edge, 0] @ ll
            if with_jet:
                dx[self.edge, 0] = c[self.edge, 0] @ ll @ OWNED.GN[0]
        else:
            raise ValueError(variation)
        require(max(float(np.linalg.svd(c, compute_uv=False).max()),
                    float(np.linalg.svd(x, compute_uv=False).max())) < P,
                "actual Julia contractions retain same strict chart")
        return c, x, dc, dx

    def dirac(self, c, x, state):
        output = np.zeros_like(state)
        for role in range(4):
            output += x[:, role] @ state[self.forward[role]] - c[:, role] @ state
            output += (adjoint(x[:, role]) @ state)[self.backward[role]]
            output -= adjoint(c[:, role]) @ state
        return output / self.ell

    def compressed_vectors(self, base, variation, parameter=0., with_jet=False, with_literal=False):
        c, x, dc, dx = self.varied(base, variation, parameter, with_jet)
        prep = base["prep"]
        d_state = self.dirac(c, x, prep)
        a_state = self.ell / 16 * d_state
        da_state = self.ell / 16 * self.dirac(dc, dx, prep) if with_jet else None
        output = np.empty((33,) + prep.shape)
        delta = np.empty_like(output) if with_jet else None
        primitive = np.empty((32,) + prep.shape) if with_literal else None
        primitive_jet = np.empty_like(primitive) if with_literal and with_jet else None
        output[0] = math.sqrt(P) * prep
        if with_jet:
            delta[0] = 0
        max_sylvester = 0.
        blank_action = np.zeros_like(prep)
        blank_delta = np.zeros_like(prep) if with_jet else None
        for role in range(4):
            cr, xr, dcr, dxr = c[:, role], x[:, role], dc[:, role], dx[:, role]
            roots, root_jets = [], []
            for aa, daa in ((xr, dxr), (cr, dcr)):
                for left in (True, False):
                    radicand = np.eye(16) - (aa @ adjoint(aa) if left else adjoint(aa) @ aa)
                    tangent = None
                    if with_jet:
                        tangent = -(daa @ adjoint(aa) + aa @ adjoint(daa) if left else
                                    adjoint(daa) @ aa + adjoint(aa) @ daa)
                    root, jet, residual = square_root_jet(radicand, tangent)
                    roots.append(root)
                    root_jets.append(jet)
                    max_sylvester = max(max_sylvester, residual)
            # R_P is shifted backwards as an operator.  Its derivative
            # carries the SAME shift; no inverse-Lorentz adjoint is used.
            roots[1] = roots[1][self.backward[role]]
            if with_jet:
                root_jets[1] = root_jets[1][self.backward[role]]

            def apply_word(item, state, tangent=False):
                ac, ax = (dcr, dxr) if tangent else (cr, xr)
                if item == 0:
                    return (adjoint(ax) @ state)[self.backward[role]]
                if item == 1:
                    return ax @ state[self.forward[role]]
                if item == 2:
                    return -adjoint(ac) @ state
                return -ac @ state

            for item in range(4):
                word = 4 * role + item
                action = apply_word(item, a_state)
                if with_literal:
                    primitive[2 * word] = action
                blank_action += action / 16
                output[1 + 2 * word] = P / 4 * (prep - 2 * action)
                sign = 1 if item < 2 else -1
                root_action = sign * roots[item] @ a_state
                if with_literal:
                    primitive[2 * word + 1] = root_action
                output[2 + 2 * word] = -P / 2 * root_action
                if with_jet:
                    d_action = apply_word(item, da_state) + apply_word(item, a_state, tangent=True)
                    if with_literal:
                        primitive_jet[2 * word] = d_action
                    blank_delta += d_action / 16
                    delta[1 + 2 * word] = -P / 2 * d_action
                    d_root_action = sign * (root_jets[item] @ a_state + roots[item] @ da_state)
                    if with_literal:
                        primitive_jet[2 * word + 1] = d_root_action
                    delta[2 + 2 * word] = -P / 2 * d_root_action
        blank_expected = self.ell / 16 * self.dirac(c, x, a_state)
        require(np.max(np.abs(blank_action - blank_expected)) < 3e-17,
                "all original row blocks give N0=A with true shifts")
        if with_jet:
            blank_expected_delta = self.ell / 16 * (
                self.dirac(dc, dx, a_state) + self.dirac(c, x, da_state))
            require(np.max(np.abs(blank_delta - blank_expected_delta)) < 3e-17,
                    "full original N0 tangent equals actual A tangent")
        rayleigh = float(np.vdot(d_state, d_state).real)
        rayleigh_jet = None
        if with_jet:
            rayleigh_jet = float(2 * np.vdot(d_state, self.dirac(dc, dx, prep)).real)
        literal = None
        if with_literal:
            # Independent original Kraus calculation: no use of B, G or
            # compressed L vectors. Sum the literal 32 duplicated words
            # with Walsh normalization 1/32, then apply both Golden ports.
            probabilities, probability_jets = [], []
            for label in range(32):
                for coefficient in range(2):
                    n_action = np.zeros_like(prep)
                    n_jet = np.zeros_like(prep) if with_jet else None
                    for word in range(16):
                        first = (-1) ** ((label & (2 * word)).bit_count())
                        second = (-1) ** ((label & (2 * word + 1)).bit_count())
                        factor = (first + second) / 32
                        if factor:
                            n_action += factor * primitive[2 * word + coefficient]
                            if with_jet:
                                n_jet += factor * primitive_jet[2 * word + coefficient]
                    for port in range(2):
                        value = -2 * (P ** 2 if port == 0 else P ** 1.5) * n_action
                        if label == coefficient == port == 0:
                            value += prep
                        probabilities.append(float(np.sum((value.conj() * value).real)))
                        if with_jet:
                            dvalue = -2 * (P ** 2 if port == 0 else P ** 1.5) * n_jet
                            probability_jets.append(float(2 * np.sum((value.conj() * dvalue).real)))
            literal = {"probabilities": np.array(probabilities),
                       "probability_jets": np.array(probability_jets) if with_jet else None}
        return output, delta, rayleigh, rayleigh_jet, max_sylvester, literal
