"""Corrected C7-C9 information geometry and a normalized-source consumer.

The density below is the supplied THREE-LEVEL diagnostic family. It is not
the native sixteen-grade matter carrier, an admitted field map, or a new heat
action. A nonzero source on one classical-readout fibre disproves descent for
that readout; it does not require injectivity, tomography, or five returns.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import sympy as s

PULLBACK_PATH = ("02_REGISTRY/research/sources/d0_record_source_pullback_2026-10-15/"
                 "record_source.py")
PULLBACK_SHA256 = "daf55b5f98525dac7e376489fcd061f2849eb49430fc5543a9d9cd9320196e7e"


def clean(expression):
    # Every logarithm used here has an explicitly positive argument.
    return s.simplify(s.expand_log(expression, force=True))


def require(label, condition):
    if not bool(condition):
        raise AssertionError(label)


def classical_readout_jacobian(p):
    """Rows are outcome probabilities; columns are eta, xi, zeta."""
    return s.Matrix([[p * p, 0, 0], [-p * p, 0, 0], [0, 0, 0]])


def radial_hessian_coefficients(r, c):
    """Radial and transverse eigenvalues for A(w)=c*g(|w|), 0<r<1."""
    return 2 * c / (1 - r * r), c * s.log((1 + r) / (1 - r)) / r


def load_pullback(repo):
    path = repo / PULLBACK_PATH
    require("previous normalized-source evaluator unchanged",
            hashlib.sha256(path.read_bytes()).hexdigest() == PULLBACK_SHA256)
    spec = importlib.util.spec_from_file_location("d0_information_source_consumer", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned source evaluator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # definitions only; no prior checker replay
    return module


def run_checks(repo: Path | None = None):
    repo = Path(repo) if repo is not None else Path(__file__).resolve().parents[4]
    p = (s.sqrt(5) - 1) / 2
    phi = (s.sqrt(5) + 1) / 2
    c = p * p / s.log(phi)
    a = c * s.log(4)
    r = s.Symbol("r", positive=True)
    g = (1 + r) * s.log(1 + r) + (1 - r) * s.log(1 - r)
    require("radial first derivative", clean(s.diff(g, r) - s.log((1 + r) / (1 - r))) == 0)
    require("radial second derivative", clean(s.diff(g, r, 2) - 2 / (1 - r * r)) == 0)
    require("working-point value identity, not a gradient maximum",
            clean(s.diff(g, r).subs(r, s.Rational(3, 5)) - 2 * s.log(2)) == 0)
    require("gradient is unbounded at the faithful boundary", s.limit(s.diff(g, r), r, 1, dir="-") == s.oo)

    # A complete positive chart r=u/(1+u) covers 0<r<1. Positivity is
    # checked symbolically, not inferred from samples of the open ball.
    u, scale = s.symbols("u scale", positive=True)
    lr, lt = radial_hessian_coefficients(u / (1 + u), scale)
    radial_positive = s.factor(lr)
    tangent_positive = clean(lt)
    require("positive radial Hessian on entire interior chart", radial_positive.is_positive is True)
    require("positive transverse Hessian on entire interior chart", tangent_positive.is_positive is True)
    require("isotropic smooth central Hessian", s.limit(2 * scale / (1 - r * r), r, 0) == 2 * scale
            and s.limit(scale * s.log((1 + r) / (1 - r)) / r, r, 0) == 2 * scale)

    eta, xi, zeta = s.symbols("eta xi zeta", real=True)
    norm = s.sqrt(eta * eta + xi * xi + zeta * zeta)
    potential = scale * g.subs(r, norm)
    point = {eta: 0, xi: s.Rational(3, 5), zeta: 0}
    H = s.hessian(potential, (eta, xi, zeta)).subs(point).applyfunc(clean)
    lr0, lt0 = radial_hessian_coefficients(s.Rational(3, 5), scale)
    require("full Hessian distinguishes radial and transverse directions",
            (H - s.diag(lt0, lr0, lt0)).applyfunc(clean) == s.zeros(3) and clean(lr0 - lt0) != 0)
    radial_readout_jet = s.Matrix([s.diff(norm, w).subs(point) for w in (eta, xi, zeta)])
    require("one scalar radial readout suffices for this functional differential",
            (s.Matrix([s.diff(potential, w).subs(point) for w in (eta, xi, zeta)])
             - scale * s.diff(g, r).subs(r, s.Rational(3, 5)) * radial_readout_jet).applyfunc(clean) == s.zeros(3, 1))
    distance = s.sqrt(2 * scale) * s.asin(r)
    require("radial distance integrand exactly matches Hessian metric",
            clean(s.diff(distance, r) ** 2 - 2 * scale / (1 - r * r)) == 0)
    require("distance starts at the centre", distance.subs(r, 0) == 0)
    require("finite boundary distance is a limit, not an interior endpoint",
            s.limit(distance, r, 1, dir="-") == s.sqrt(2 * scale) * s.pi / 2)

    J = classical_readout_jacobian(p)
    t0, t1, t2, b = s.symbols("t0 t1 t2 b", real=True)
    pulled = J.T * s.Matrix([t0, t1, t2])
    require("readout cotangent is pulled back into state coordinates",
            (pulled - s.Matrix([p * p * (t0 - t1), 0, 0])).applyfunc(clean) == s.zeros(3, 1))
    gradient = s.Matrix([0, a, 0])
    error_squared = (s.Matrix([b, 0, 0]) - gradient).dot(s.Matrix([b, 0, 0]) - gradient)
    require("Euclidean best covector error is a, not a over sqrt2",
            clean(error_squared - (b * b + a * a)) == 0)
    require("xi is on a classical-readout fibre but source visible",
            J * s.Matrix([0, 1, 0]) == s.zeros(3, 1) and gradient[1] != 0)

    sigma = s.Matrix([[p * p, 3 * p * p / 5, 0],
                      [3 * p * p / 5, p * p, 0], [0, 0, p ** 3]])
    dsigma = s.Matrix([[0, p * p, 0], [p * p, 0, 0], [0, 0, 0]])
    require("diagnostic density normalized", clean(s.trace(sigma) - 1) == 0 and s.trace(dsigma) == 0)
    require("diagnostic density faithful on all three supplied levels", sigma.is_positive_definite is True)
    purity_jet = clean(2 * s.trace(sigma * dsigma))
    require("radial coherence changes spectrum", clean(purity_jet - 12 * p ** 4 / 5) == 0 and purity_jet != 0)
    h = s.symbols("h0:9", real=True)
    generator = s.Matrix([[h[0], h[3] + s.I * h[4], h[5] + s.I * h[6]],
                          [h[3] - s.I * h[4], h[1], h[7] + s.I * h[8]],
                          [h[5] - s.I * h[6], h[7] - s.I * h[8], h[2]]])
    commutator_jet = s.I * (generator * sigma - sigma * generator)
    require("every Hermitian commutator preserves purity", clean(2 * s.trace(sigma * commutator_jet)) == 0)

    # At this base, L=log(sigma)-log(mu) is elementary because the
    # first two reference weights both equal p². This constant observable
    # represents only the FIRST relative-entropy differential at the base.
    lp, lm = s.log(s.Rational(8, 5)), s.log(s.Rational(2, 5))
    observable = s.Matrix([[(lp + lm) / 2, (lp - lm) / 2, 0],
                           [(lp - lm) / 2, (lp + lm) / 2, 0], [0, 0, 0]]) / s.log(phi)
    require("entropy gradient invisible on all unitary state tangents",
            clean(s.trace(observable * commutator_jet)) == 0)
    source = load_pullback(repo)
    # Diagnostic scalar flag instrument, all outcomes retained. Its probability
    # moves independently; normalizing the accepted event must cancel that jet.
    prob, dprob = s.Rational(2, 5), s.Rational(1, 7)
    instrument = source.CountInstrument([
        [source.KrausJet(s.eye(3), s.zeros(3), prob, dprob)],
        [source.KrausJet(s.eye(3), s.zeros(3), 1 - prob, -dprob)]], clean)
    instrument.validate_trace_preservation()
    tape = source.forward_count(instrument, sigma, 1, dsigma)
    event = source.condition_event(instrument, tape, {0}, observable)
    require("same classical fibre has a nonzero actual normalized source",
            clean(event.source - a) == 0 and event.probability_tangent == dprob
            and (event.density_tangent - dsigma).applyfunc(clean) == s.zeros(3))
    omitted_normalizer = clean(s.trace(observable * event.weight_tangent) / event.probability)
    require("normalizer subtraction is essential even for this fibre",
            clean(omitted_normalizer - event.source - event.value * dprob / prob) == 0
            and clean(omitted_normalizer - event.source) != 0)

    return {"status": "PASS", "corrected_error": "a = p^2*log(4)/log(phi)",
            "hessian": "radial 2c/(1-r^2); transverse c*log((1+r)/(1-r))/r",
            "radial_distance_from_centre": "sqrt(2c)*asin(r)",
            "gradient_at_3_over_5": "equals boundary supremum of A, not a maximum gradient",
            "purity_jet": "12*p^4/5, incompatible with every i[H,sigma]",
            "normalized_event_source": "a on the same diagonal-readout fibre; dP=1/7 retained",
            "weak_descent": "scalar radius suffices for this radial functional; physical readout admission remains open",
            "pullback_owner_sha256": PULLBACK_SHA256,
            "scope": "three-level diagnostic only; not native16 or physical Phi; no tomography/five-return requirement"}


if __name__ == "__main__":
    print(json.dumps(run_checks(), sort_keys=True))
