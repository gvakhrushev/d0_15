"""The recorded instrument, its sources, and a state-preserving archive handoff.

Entropy is a declared reduced/CQ component, not global entropy production.
No physical Cost, registration convention or permitted variation is selected.
"""
from dataclasses import dataclass, replace
from pathlib import Path
import sys
import mpmath as mp

DOMAIN = Path(__file__).resolve().parent.parent / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0, str(DOMAIN))
import native_execution as native


def kron(a, b):
    return mp.matrix([[a[i // b.rows, j // b.cols] * b[i % b.rows, j % b.cols]
                       for j in range(a.cols * b.cols)] for i in range(a.rows * b.rows)])


def trace(a):
    return mp.fsum(a[i, i] for i in range(a.rows))


def entropy(a):
    tol = mp.eps ** mp.mpf(".7")
    values = mp.eighe((a + a.H) / 2, eigvals_only=True)
    if min(values) < -tol: raise ValueError("entropy input is not positive")
    return -mp.fsum(x * mp.log(x) for x in values if x > tol)


def log_positive(a):
    values, u = mp.eighe((a + a.H) / 2)
    if min(values) <= 0: raise ValueError("source formula requires the faithful support chart")
    return u * mp.diag([mp.log(x) for x in values]) * u.H


def functions(K, delta, V=None):
    values, u = mp.eigsy(K)
    fs = ((lambda x: mp.cos(delta * x), lambda x: -delta * mp.sin(delta * x)),
          (lambda x: mp.sin(delta * x), lambda x: delta * mp.cos(delta * x)))
    operators, derivatives = [], []
    h = u.T * V * u if V is not None else None
    for f, df in fs:
        operators.append(u * mp.diag([f(x) for x in values]) * u.T)
        if V is not None:
            derivatives.append(u * mp.matrix([[(df(values[i]) if values[i] == values[j]
                else (f(values[i]) - f(values[j])) / (values[i] - values[j])) * h[i, j]
                for j in range(K.rows)] for i in range(K.rows)]) * u.T)
    return operators, derivatives


def instrument(K, delta, omega):
    if omega.rows % K.rows: raise ValueError("input/reference dimension mismatch")
    ls, _ = functions(K, delta)
    ls = [kron(l, mp.eye(omega.rows // K.rows)) for l in ls]
    blocks = [l * omega * l for l in ls]
    cq = mp.zeros(2 * omega.rows)
    for b in range(2):
        for i in range(omega.rows):
            for j in range(omega.rows): cq[b * omega.rows + i, b * omega.rows + j] = blocks[b][i, j]
    ps = [mp.re(trace(x)) for x in blocks]
    conditional = mp.fsum(p * entropy(x / p) for p, x in zip(ps, blocks) if p > 0)
    return {"blocks": blocks, "cq": cq, "p": ps, "conditional": conditional,
            "gain": entropy(cq) - entropy(omega)}


def sources(K, delta, omega, V):
    """Faithful fixed-support formulas; V is the actual K direction."""
    ls, ds = functions(K, delta, V)
    ref = mp.eye(omega.rows // K.rows)
    ls, ds = [kron(l, ref) for l in ls], [kron(d, ref) for d in ds]
    logs = [log_positive(l * omega * l) for l in ls]
    g = log_positive(omega) - sum((l * x * l for l, x in zip(ls, logs)), mp.zeros(omega.rows))
    field = -sum((trace((d * omega * l + l * omega * d) * x)
                  for l, d, x in zip(ls, ds, logs)), mp.mpf(0))
    return g, mp.re(field)


def partial_trace(a, qubits, keep):
    keep = tuple(keep); gone = tuple(q for q in range(qubits) if q not in keep)
    if (a.rows != 2 ** qubits or a.cols != a.rows or len(set(keep)) != len(keep)
            or any(type(q) is not int or not 0 <= q < qubits for q in keep)):
        raise ValueError("partial trace must retain a typed subset of the same carrier")
    def index(x, y):
        bits = {q: (x >> (len(keep) - 1 - j)) & 1 for j, q in enumerate(keep)}
        bits.update({q: (y >> (len(gone) - 1 - j)) & 1 for j, q in enumerate(gone)})
        return sum(bits[q] << (qubits - 1 - q) for q in range(qubits))
    return mp.matrix([[mp.fsum(a[index(i, t), index(j, t)] for t in range(1 << len(gone)))
                       for j in range(1 << len(keep))] for i in range(1 << len(keep))])


def conjugate_record_word(layout, Q, n, *, max_qubits, max_expanded_stages):
    bounds = dict(max_qubits=max_qubits, max_expanded_stages=max_expanded_stages)
    if type(Q) is not int or Q < 1 or type(n) is not int: raise native.DomainError("integer Q,n required")
    prep = (native.Gate("G", (0,)),) * abs(n)
    if n < 0: prep = native.inverse_word(replace(layout, gates=prep), **bounds)
    inverse = native.inverse_word(replace(layout, gates=prep), **bounds)
    u = ((native.Gate("G", (1,)),) * (4 * Q) + (native.Gate("CX", (0, 1)),)
         + (native.Gate("G", (1,)),) * (2 * Q) + (native.Gate("CX", (0, 1)),))
    c = (native.Gate("CX", (1, 2)),)
    result = replace(layout, gates=c + prep + u + inverse + c)
    native.validate_execution(result, **bounds)
    return result


def full_history_phases(theta, phi, n):
    """Four +/- pairs for the fixed two-band word WITH historical prep."""
    plus = mp.acos(mp.cos(theta) * mp.cos(phi))
    minus = mp.asin(mp.cos((1 - 2 * n) * theta) * mp.sin(phi))
    return (2 * phi + plus, 2 * phi - plus, 2 * phi + minus, 2 * phi + mp.pi - minus)


def full_history_partition(theta, phi, n, N, beta_clock):
    # Four +/- pairs, bank2 * dirtySpin4, both Hodge degrees; all N roots.
    return 32 * mp.fsum(mp.exp(-beta_clock * (1 - mp.cos((angle + 2 * mp.pi * k) / N)))
                       for angle in full_history_phases(theta, phi, n) for k in range(N))


@dataclass(frozen=True)
class Handoff:
    execution: object
    state: object


def seal_handoff(prefix, actual_state, bank, *, max_qubits, max_expanded_stages):
    """Policy only: caller supplies actual prefix output; no simulation/reset.

    The prefix Book cut stays the prefix cut. The returned empty suffix
    begins at this correlated state and declares no new blank allocation.
    """
    bounds = dict(max_qubits=max_qubits, max_expanded_stages=max_expanded_stages)
    native.validate_execution(prefix, **bounds)
    if type(bank) is not int or bank not in prefix.blank_wires or bank in set(prefix.old_right) | set(prefix.source_spin or ()) or bank == prefix.source_port:
        raise native.DomainError("archive bank must have been ordinary blank work")
    if actual_state.rows != 2 ** prefix.qubits or actual_state.cols != actual_state.rows:
        raise native.DomainError("handoff must retain the entire correlated carrier")
    suffix = replace(prefix, gates=(), blank_wires=(), old_right=tuple(sorted(set(prefix.old_right) | {bank})))
    native.validate_execution(suffix, **bounds)
    return Handoff(suffix, actual_state)
