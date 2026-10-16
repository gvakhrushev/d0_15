"""Exact count-event source pullback for a supplied finite instrument.

This is an evaluator, not a field-to-instrument selection law.  A term (w,B)
means w B rho B*, with its genuine first jet (dw,dB).  This representation
avoids unnecessary square roots in the literal golden Kraus operators.
The two outcome branches and every Kraus/direction label are summed exactly.
Only an observable depending on the stated terminal state and count event is
evaluated; a general archive observable requires its actual history labels.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import sympy as s


@dataclass(frozen=True)
class KrausJet:
    operator: s.MatrixBase
    tangent: s.MatrixBase
    weight: s.Expr = s.Integer(1)
    weight_tangent: s.Expr = s.Integer(0)


class CountInstrument:
    """Two-outcome CP instrument with supplied, unrestricted matrix first jets.

The caller owns positivity, total-channel trace preservation, field admission,
and compatibility of these jets with its physical constraints.  Channels may
be nonunital.  `validate_trace_preservation` checks the finite first-jet law.
"""

    def __init__(self, branches: Iterable[Iterable[KrausJet]],
                 reduce_scalar: Callable = s.cancel):
        self.branches = tuple(tuple(branch) for branch in branches)
        if len(self.branches) != 2 or not all(self.branches):
            raise ValueError("exactly two nonempty outcome branches required")
        self.reduce_scalar = reduce_scalar
        self.dimension = self.branches[0][0].operator.rows
        for branch in self.branches:
            for term in branch:
                if term.operator.shape != (self.dimension, self.dimension):
                    raise ValueError("Kraus dimensions disagree")
                if term.tangent.shape != term.operator.shape:
                    raise ValueError("Kraus tangent dimension disagrees")

    def scalar(self, value):
        return self.reduce_scalar(value)

    def matrix(self, value):
        return s.Matrix(value).applyfunc(self.reduce_scalar)

    def zero(self):
        return s.zeros(self.dimension)

    def channel(self, outcome, state, *, adjoint=False):
        total = self.zero()
        for term in self.branches[outcome]:
            B = term.operator
            total += term.weight * (B.H * state * B if adjoint else B * state * B.H)
        return self.matrix(total)

    def channel_tangent(self, outcome, state):
        total = self.zero()
        for term in self.branches[outcome]:
            B, dB, w, dw = (term.operator, term.tangent,
                            term.weight, term.weight_tangent)
            total += dw * B * state * B.H + w * (dB * state * B.H + B * state * dB.H)
        return self.matrix(total)

    def validate_trace_preservation(self):
        effect, tangent = self.zero(), self.zero()
        for branch in self.branches:
            for term in branch:
                B, dB, w, dw = (term.operator, term.tangent,
                                term.weight, term.weight_tangent)
                effect += w * B.H * B
                tangent += dw * B.H * B + w * (dB.H * B + B.H * dB)
        if self.matrix(effect - s.eye(self.dimension)) != self.zero():
            raise ValueError("total Kraus effect is not identity")
        if self.matrix(tangent) != self.zero():
            raise ValueError("total Kraus effect jet is not zero")


@dataclass
class CountTape:
    states: list[list[s.MatrixBase]]
    tangents: list[list[s.MatrixBase]] | None = None

    @property
    def rounds(self):
        return len(self.states) - 1


@dataclass
class EventSource:
    weight: s.MatrixBase
    weight_tangent: s.MatrixBase
    probability: s.Expr
    probability_tangent: s.Expr
    density: s.MatrixBase
    density_tangent: s.MatrixBase
    value: s.Expr
    source: s.Expr
    operator_source: s.Expr
    preparation_source: s.Expr


def _event(event, rounds):
    event = frozenset(event)
    if not event or any(not isinstance(k, int) or k < 0 or k > rounds for k in event):
        raise ValueError("fixed event must contain counts in 0,...,T")
    return event


def forward_count(instrument: CountInstrument, initial, rounds: int,
                  initial_tangent=None, *, propagate_tangents=True) -> CountTape:
    """Propagate count weights, optionally with full matrix directional jets.

    The states-only option never calls channel_tangent.  Use it once, then
    reuse the base states/costates/generator covectors for physical directions.
    """
    if not isinstance(rounds, int) or rounds < 0:
        raise ValueError("rounds must be a nonnegative integer")
    if not propagate_tangents and initial_tangent is not None:
        raise ValueError("pass initial_tangent to reverse_event for a states-only tape")
    M = instrument.matrix
    states = [[M(initial)]]
    tangents = ([[instrument.zero() if initial_tangent is None else M(initial_tangent)]]
                if propagate_tangents else None)
    for n in range(rounds):
        row, drow = [], []
        for k in range(n + 2):
            x, dx = instrument.zero(), instrument.zero()
            for b in (0, 1):
                j = k - b
                if 0 <= j <= n:
                    x += instrument.channel(b, states[n][j])
                    if propagate_tangents:
                        dx += (instrument.channel(b, tangents[n][j])
                               + instrument.channel_tangent(b, states[n][j]))
            row.append(M(x))
            if propagate_tangents:
                drow.append(M(dx))
        states.append(row)
        if propagate_tangents:
            tangents.append(drow)
    return CountTape(states, tangents)


def forward_states(instrument: CountInstrument, initial, rounds: int) -> CountTape:
    """Base count weights only, without constructing any directional jet."""
    return forward_count(instrument, initial, rounds, propagate_tangents=False)


def _event_base(instrument, tape, event, operator):
    M, r = instrument.matrix, instrument.scalar
    W = M(sum((tape.states[-1][k] for k in event), instrument.zero()))
    P = r(s.trace(W))
    if P == 0 or P.is_nonpositive is True:
        raise ValueError("event probability must be positive")
    density = M(W / P)
    return W, P, density, r(s.trace(density * operator))


def condition_event(instrument: CountInstrument, tape: CountTape, event,
                    operator, operator_tangent=None) -> EventSource:
    """Full normalized source, including moving initial state and normalizer.

    Zero/nonpositive event probabilities are outside the conditional domain.
    For a symbolic algebraic number, positivity is the caller's responsibility;
    exact zero is always rejected.
    """
    event = _event(event, tape.rounds)
    if tape.tangents is None:
        raise ValueError("forward event jets require tangents; use reverse_event on a states-only tape")
    M, r = instrument.matrix, instrument.scalar
    W, P, density, value = _event_base(instrument, tape, event, operator)
    dW = M(sum((tape.tangents[-1][k] for k in event), instrument.zero()))
    dP = r(s.trace(dW))
    ddensity = M((dW - density * dP) / P)
    doperator = instrument.zero() if operator_tangent is None else operator_tangent
    direct = r(s.trace(density * doperator))
    preparation = r(s.trace((operator - value * s.eye(instrument.dimension)) * dW) / P)
    return EventSource(W, dW, P, dP, density, ddensity,
                       value, r(direct + preparation), direct, preparation)


@dataclass
class ReverseSource:
    source: s.Expr
    initial_source: s.Expr
    instrument_source: s.Expr
    costates: list[list[s.MatrixBase]]


def reverse_event(instrument: CountInstrument, tape: CountTape, event,
                  operator, operator_tangent=None, *, initial_tangent=None) -> ReverseSource:
    """Reverse/count adjoint, reusable with a supplied native field jet.

    Time cost is O(T^2) matrix channel applications for this fixed count
    observable.  It replaces enumeration of (2q)^T labels, not the physical
    record.  No forward directional tape is needed.  The initial tangent can
    be supplied separately; otherwise a directional tape supplies its initial
    jet, and a states-only tape defaults to zero.  Costates and G_r from
    generator_contractions depend only on base data and may be reused.
    """
    event = _event(event, tape.rounds)
    M, r = instrument.matrix, instrument.scalar
    _, probability, density, value = _event_base(instrument, tape, event, operator)
    terminal = M((operator - value * s.eye(instrument.dimension)) / probability)
    C = [None] * (tape.rounds + 1)
    C[-1] = [terminal if k in event else instrument.zero() for k in range(tape.rounds + 1)]
    for n in range(tape.rounds - 1, -1, -1):
        C[n] = [M(instrument.channel(0, C[n + 1][k], adjoint=True)
                  + instrument.channel(1, C[n + 1][k + 1], adjoint=True))
                for k in range(n + 1)]
    if initial_tangent is None:
        initial_tangent = instrument.zero() if tape.tangents is None else tape.tangents[0][0]
    initial = r(s.trace(C[0][0] * initial_tangent))
    action = s.Integer(0)
    for n in range(tape.rounds):
        for k in range(n + 1):
            for b in (0, 1):
                action += s.trace(C[n + 1][k + b]
                                  * instrument.channel_tangent(b, tape.states[n][k]))
    action = r(action)
    doperator = instrument.zero() if operator_tangent is None else operator_tangent
    operator_source = r(s.trace(density * doperator))
    return ReverseSource(r(operator_source + initial + action), initial, action, C)


def generator_contractions(instrument: CountInstrument, tape: CountTape,
                           reverse: ReverseSource, returns, coefficients):
    """Return Hermitian G_r with sum Tr(G_r H_r) equal to the return source.

    Requires dB_(b,r)=i c_(b,r) H_r U_r, real c and fixed real Kraus weights.
    Returns and coefficients are inputs, not a chosen physical map.  The
    complete source also retains moving rho0, Delta and any other action term.
    """
    if any(term.weight_tangent != 0 for branch in instrument.branches for term in branch):
        raise ValueError("generator contractions require fixed Kraus weights")
    if any(len(branch) != len(returns) for branch in instrument.branches):
        raise ValueError("one supplied return per direction/Kraus term required")
    G = [instrument.zero() for _ in returns]
    for n in range(tape.rounds):
        for k in range(n + 1):
            rho = tape.states[n][k]
            for b in (0, 1):
                C = reverse.costates[n + 1][k + b]
                for j, (U, term) in enumerate(zip(returns, instrument.branches[b])):
                    M = U * rho * term.operator.H * C
                    G[j] += s.I * term.weight * coefficients[b][j] * (M - M.H)
    return [instrument.matrix(g) for g in G]


def prepared_action_source(instrument: CountInstrument, event_source: EventSource,
                           thermal_density, operator_tangent,
                           feedback, feedback_tangent, z):
    """Assemble the specified H_beta + J + R_A first differential.

    The caller supplies the actual Gibbs density of the SAME full heat operator,
    fixed beta/z, and the actual full feedback and its jet, including moving
    cuts/adjoints.  This does not derive any of those ownership identifications.
    A reduced retained heat requires its separately owned archive remainder;
    that remainder is not fitted or silently supplied by this function.
    """
    M, r = instrument.matrix, instrument.scalar
    if r(s.trace(thermal_density)) != 1:
        raise ValueError("thermal density must have trace one")
    Q = M(s.eye(feedback.rows) - z * feedback)
    if r(Q.det()) == 0:
        raise ValueError("feedback resolvent is singular")
    # Real positive logdet domain is an independent input condition.
    heat = r(-s.trace(thermal_density * operator_tangent))
    memory = r(z * s.trace(M(Q.inv()) * feedback_tangent))
    return {"heat_source": heat, "feedback_source": memory,
            "prepared_matter_source": event_source.source,
            "total_source": r(heat + memory + event_source.source)}
