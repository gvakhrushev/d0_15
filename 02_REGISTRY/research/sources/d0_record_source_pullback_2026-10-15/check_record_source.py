"""Focused exact forward/reverse/full-history checks; no prior-suite replay."""
from __future__ import annotations

import ast
from functools import lru_cache
import hashlib
from pathlib import Path

import sympy as s

from record_source import (CountInstrument, KrausJet, condition_event,
                           forward_count, forward_states, generator_contractions,
                           prepared_action_source, reverse_event)


SOURCE = ("02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14/"
          "continuation_v3/src/moving_preparation_exact.py")
SOURCE_SHA256 = "1b3d0f5e10a59ca97daaf06744d6fe1429e7643dd350523b897ca9e2b287bc06"
SOURCE_HEAD = "f0a6a85111c28f21a18ebf6ad9276eaa713abbd8"


def require(label, condition):
    if not bool(condition):
        raise AssertionError(label)


def pinned_fixture(repo):
    """Load only the owned reducer, literal fixture and channel definitions.

    The owner run()/main() and immutable receipt checks are never called.
    Whole-file pinning makes the selected AST definitions reviewable at the
    stated source head without starting the transitive prior certificate.
    """
    raw = (repo / SOURCE).read_bytes()
    require("moving preparation owner hash", hashlib.sha256(raw).hexdigest() == SOURCE_SHA256)
    tree = ast.parse(raw)
    run = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "run")
    reducer = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "red")
    p = s.Symbol("p", real=True)
    env = {"s": s, "p": p, "MIN": p * p + p - 1}
    exec(compile(ast.Module(body=[reducer], type_ignores=[]), SOURCE, "exec"), env)
    env["red"] = lru_cache(maxsize=65536)(env["red"])
    env["mat"] = lambda x: x.applyfunc(env["red"])
    assignments = {"I", "dim", "q", "gamma", "Us", "Hs", "dUs", "Delta", "dDelta"}
    selected = []
    for node in run.body:
        names = {n.id for n in node.targets if isinstance(n, ast.Name)} if isinstance(node, ast.Assign) else set()
        if names & assignments or isinstance(node, ast.FunctionDef) and node.name in {"channel", "dchannel"}:
            selected.append(node)
    exec(compile(ast.Module(body=selected, type_ignores=[]), SOURCE, "exec"), env)
    return env


def full_history_event(instrument, initial, initial_tangent, rounds, event):
    """Independent product-rule enumeration of complete Kraus label words.

    It multiplies word operators and scalar path weights, not count-state
    channels or costates.  Direction and outcome labels are retained until
    each complete word's terminal count is tested.
    """
    M, r = instrument.matrix, instrument.scalar
    W, dW = instrument.zero(), instrument.zero()
    selected, total = 0, 0

    def visit(n, count, B, dB, weight, dweight):
        nonlocal W, dW, selected, total
        if n == rounds:
            total += 1
            if count in event:
                selected += 1
                state = M(B * initial * B.H)
                dstate = M(dB * initial * B.H + B * initial_tangent * B.H + B * initial * dB.H)
                W += weight * state
                dW += dweight * state + weight * dstate
            return
        for b, branch in enumerate(instrument.branches):
            for term in branch:
                visit(n + 1, count + b,
                      M(term.operator * B),
                      M(term.tangent * B + term.operator * dB),
                      r(term.weight * weight),
                      r(term.weight_tangent * weight + term.weight * dweight))

    visit(0, 0, s.eye(instrument.dimension), instrument.zero(), s.Integer(1), s.Integer(0))
    return M(W), M(dW), selected, total


def compare_three(instrument, rho0, drho0, rounds, event, Delta, dDelta):
    instrument.validate_trace_preservation()
    M, r = instrument.matrix, instrument.scalar
    require("initial trace one", r(s.trace(rho0)) == 1)
    require("initial jet trace zero", r(s.trace(drho0)) == 0)
    tape = forward_count(instrument, rho0, rounds, drho0)
    fwd = condition_event(instrument, tape, event, Delta, dDelta)
    rev = reverse_event(instrument, tape, event, Delta, dDelta)
    W, dW, selected, words = full_history_event(instrument, rho0, drho0, rounds, event)
    require("count weights equal complete history words", M(fwd.weight - W) == instrument.zero())
    require("count weight jets equal complete history word product rule", M(fwd.weight_tangent - dW) == instrument.zero())
    N, dN, P, dP = (r(s.trace(W * Delta)), r(s.trace(dW * Delta + W * dDelta)),
                     r(s.trace(W)), r(s.trace(dW)))
    history_source = r(dN / P - N * dP / (P * P))
    require("forward equals reverse source", r(fwd.source - rev.source) == 0)
    require("reverse equals independent quotient of complete history moments", r(rev.source - history_source) == 0)
    require("density tangent keeps full normalization", r(s.trace(fwd.density_tangent)) == 0)
    require("source agrees with normalized matrix derivative", r(fwd.source - s.trace(fwd.density * dDelta + fwd.density_tangent * Delta)) == 0)
    require("all outcome weights trace one", r(s.trace(sum(tape.states[-1], instrument.zero()))) == 1)
    require("all outcome weight jets trace zero", r(s.trace(sum(tape.tangents[-1], instrument.zero()))) == 0)
    return tape, fwd, rev, selected, words


def run_checks(repo: Path | None = None):
    repo = Path(repo) if repo is not None else Path(__file__).resolve().parents[4]
    src = pinned_fixture(repo)
    p, red, mat, I = (src[k] for k in ("p", "red", "mat", "I"))
    Us, Hs, dUs = (src[k] for k in ("Us", "Hs", "dUs"))
    gamma, q = src["gamma"], src["q"]
    branches = [[], []]
    for U, dU in zip(Us, dUs):
        branches[0].append(KrausJet(p * I + p * p * U, p * p * dU, s.Rational(1, q)))
        branches[1].append(KrausJet(U - I, dU, gamma / q))
    instrument = CountInstrument(branches, red)
    test_state = s.Matrix([[2, s.I, 1, 0], [-s.I, 3, 0, 1], [1, 0, 4, 1], [0, 1, 1, 5]]) / 14
    for b in (0, 1):
        require("literal owned CP channel", mat(instrument.channel(b, test_state) - src["channel"](b, test_state)) == s.zeros(4))
        require("literal owned noncommuting CP channel jet", mat(instrument.channel_tangent(b, test_state) - src["dchannel"](b, test_state)) == s.zeros(4))
    require("reference commute", mat(Us[0] * Us[1] - Us[1] * Us[0]) == s.zeros(4))
    require("genuine noncommuting return first jet", mat(dUs[0] * Us[1] + Us[0] * dUs[1] - dUs[1] * Us[0] - Us[1] * dUs[0]) != s.zeros(4))
    rho0 = I / 4
    # Faithful base admits this genuine two-sided moving initial density jet.
    drho0 = s.diag(1, -1, 2, -2) / 100
    tape, fwd, rev, selected, words = compare_three(
        instrument, rho0, drho0, 3, {1, 2}, src["Delta"], src["dDelta"])
    require("actual event probability", red(fwd.probability - (144 * p - s.Rational(177, 2))) == 0)
    require("moving normalizer visible", fwd.probability_tangent != 0)
    require("moving prepared density contributes", fwd.preparation_source != 0)
    require("moving initial preparation contributes", rev.initial_source != 0)
    require("conditional state jet is not confined to isospectral commutators", red(s.trace(fwd.density * fwd.density_tangent)) != 0)
    G = generator_contractions(instrument, tape, rev, Us,
                               [[p * p] * q, [s.Integer(1)] * q])
    require("source visible generator contractions", red(sum(s.trace(g * h) for g, h in zip(G, Hs)) - rev.instrument_source) == 0)
    require("source generator covectors Hermitian", all(mat(g - g.H) == s.zeros(4) for g in G))

    class NoForwardJets(CountInstrument):
        def channel_tangent(self, outcome, state):
            raise AssertionError("states-only forward must not evaluate a channel jet")

    base_tape = forward_states(NoForwardJets(branches, red), rho0, 3)
    base_reverse = reverse_event(instrument, base_tape, {1, 2}, src["Delta"],
                                 src["dDelta"], initial_tangent=drho0)
    base_G = generator_contractions(instrument, base_tape, base_reverse, Us,
                                    [[p * p] * q, [s.Integer(1)] * q])
    contracted_source = red(fwd.operator_source + base_reverse.initial_source
                            + sum(s.trace(g * h) for g, h in zip(base_G, Hs)))
    require("states-only adjoint and reusable contractions equal independent full source",
            base_tape.tangents is None and red(base_reverse.source - fwd.source) == 0
            and red(contracted_source - fwd.source) == 0)

    # Exact complete differential for the declared H+J+R_A functional.
    # beta=log(2)/2 and Delta=diag(0,6,4,6) give exact rational Gibbs weights.
    gibbs = s.diag(1, s.Rational(1, 8), s.Rational(1, 4), s.Rational(1, 8))
    gibbs /= s.trace(gibbs)
    require("owned literal kinetic reference spectrum", src["Delta"] == s.diag(0, 6, 4, 6))
    cut = s.Matrix([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]) / 2
    require("diagnostic full retained cut", cut * cut == cut and cut.H == cut)
    K = Us[1] * Us[0]
    dK = dUs[1] * Us[0] + Us[1] * dUs[0]
    F = mat(cut * K.H * (I - cut) * K * cut)
    dF = mat(cut * (dK.H * (I - cut) * K + K.H * (I - cut) * dK) * cut)
    z = s.Rational(1, 3)
    action = prepared_action_source(instrument, fwd, gibbs, src["dDelta"], F, dF, z)
    # Independent exact determinant differentiation, not the trace-resolvent implementation.
    t = s.Symbol("t", real=True)
    determinant = s.expand((I - z * (F + t * dF)).det())
    independent_feedback = red(-s.diff(determinant, t).subs(t, 0) / determinant.subs(t, 0))
    require("full determinant log derivative", red(independent_feedback - action["feedback_source"]) == 0)
    require("actual nonzero diagnostic feedback source", action["feedback_source"] != 0)
    require("full declared action retains all three sources", red(action["total_source"] - rev.source + s.trace(gibbs * src["dDelta"]) - independent_feedback) == 0)

    # These are executed false simplifications with different exact results.
    require("reject frozen density source", red(fwd.source - fwd.operator_source) != 0)
    unnormalized_source = red(fwd.operator_source + s.trace(src["Delta"] * fwd.weight_tangent) / fwd.probability)
    require("reject frozen normalizer source", red(fwd.source - unnormalized_source) != 0)
    frozen_initial_source = red(fwd.operator_source + rev.instrument_source)
    require("reject frozen initial preparation", red(fwd.source - frozen_initial_source) != 0)
    E = src["mat"](gamma * sum(((U - I).H * (U - I) for U in Us), s.zeros(4)) / q)
    dE = src["mat"](gamma * sum((dU.H * (U - I) + (U - I).H * dU for U, dU in zip(Us, dUs)), s.zeros(4)) / q)
    # For T=3,A={1,2}, f(E)=3E-3E².  The diagonal drho0 cannot
    # affect this off-diagonal history-jet counterexample.
    polynomial_jet = mat((3 * dE - 3 * (E * dE + dE * E)) / 4)
    difference = mat(fwd.weight_tangent - polynomial_jet)
    require("reject full polynomial-state jet at commuting reference", any(difference[i, j] != 0 for i in range(4) for j in range(4) if i != j))

    # Synthetic rational 16D CP fixture with exterior-mask labels: every
    # mask 0,...,15 has positive weight.  The cyclic/parity matrices are
    # diagnostic CP data, not the literal native CAR operation or field map.
    d = 16
    U0 = s.zeros(d)
    for j in range(d):
        U0[(j + 1) % d, j] = 1
    U1 = s.diag(*[(-1) ** j for j in range(d)])
    H0 = s.diag(*[s.Rational(j + 1, 32) for j in range(d)])
    H1 = s.diag(*[s.Rational((-1) ** j, 8) for j in range(d)])
    for j in range(d - 1):
        H0[j, j + 1] = H0[j + 1, j] = s.Rational(1, 16)
    H1[0, 15] = H1[15, 0] = s.Rational(1, 8)
    full = CountInstrument([
        [KrausJet(U0, s.I * H0 * U0, s.Rational(1, 3), s.Rational(1, 10))],
        [KrausJet(U1, s.I * H1 * U1, s.Rational(2, 3), -s.Rational(1, 10))]])
    full_rho = s.eye(d) / 16
    full_rho[0, 15] = full_rho[15, 0] = s.Rational(1, 128)
    require("full16 faithful initial density without discarded grades",
            full_rho.eigenvals() == {s.Rational(7, 128): 1, s.Rational(9, 128): 1, s.Rational(1, 16): 14})
    full_drho = s.diag(*[s.Rational(2 * j - 15, 1000) for j in range(d)])
    full_drho[2, 3] = full_drho[3, 2] = s.Rational(1, 100)
    D = s.diag(*range(1, 17))
    dD = s.diag(*[s.Rational((-1) ** j * (j + 1), 30) for j in range(d)])
    D[0, 15] = D[15, 0] = s.Rational(1, 16)
    dD[2, 3] = dD[3, 2] = s.Rational(1, 12)
    _, ff, fr, full_selected, full_words = compare_three(full, full_rho, full_drho, 2, {0, 1}, D, dD)
    require("full16 every mask retained", all(ff.density[j, j] > 0 for j in range(d)))
    require("full16 retained coherences", any(ff.density[i, j] != 0 for i in range(d) for j in range(d) if i != j))
    require("full16 exact event probability and moving normalizer", ff.probability == s.Rational(5, 9) and ff.probability_tangent == s.Rational(2, 15))
    require("full16 moving initial state and preparation visible", fr.initial_source != 0 and ff.preparation_source != 0)
    # Endpoint and full-event cases exercise recursion boundaries.
    for rounds, event in ((0, {0}), (1, {0, 1})):
        compare_three(full, full_rho, full_drho, rounds, event, D, dD)
    return {
        "status": "PASS",
        "exact_arithmetic": "Q(p,i), p^2+p=1; rational full16",
        "source_head": SOURCE_HEAD,
        "owned_source_sha256": SOURCE_SHA256,
        "golden4": {"fixture": "literal pinned v3 instrument; diagnostic initial-state jet",
                    "feedback_scope": "diagnostic return-product/cut; not native chronology",
                    "event_probability": str(fwd.probability),
                    "normalizer_jet": str(fwd.probability_tangent),
                    "source": str(fwd.source),
                    "heat_source": str(action["heat_source"]),
                    "diagnostic_feedback_source": str(action["feedback_source"]),
                    "declared_action_source": str(action["total_source"]),
                    "generator_contraction": "exact; states-only forward reusable", "full_history_words": words,
                    "accepted_words": selected},
        "full16": {"fixture": "synthetic rational CP fixture; all exterior-mask labels; not native CAR",
                   "event_probability": str(ff.probability),
                   "normalizer_jet": str(ff.probability_tangent), "source": str(ff.source),
                   "full_history_words": full_words, "accepted_words": full_selected},
        "equalities": "forward = reverse = full Kraus-word quotient derivative",
        "rejected": ["frozen density", "frozen normalizer", "frozen initial state", "full polynomial-state jet"],
        "scope": "supplied finite count-event observable; native field map and complete archive action remain open",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_checks(), sort_keys=True))
