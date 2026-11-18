#!/usr/bin/env python3
"""Independent numerical whole-word replay on the actual 9-wire born cut.

The exact field proof is in check_open.py. This check runs the concatenation
without materializing a 512 by 512 matrix: the 16 port/Spin/pointer input
columns and five canonical births are retained throughout.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="raise")

HERE = Path(__file__).resolve().parent
NATIVE = HERE / "inputs" / "native_execution.py"
PIN = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
if hashlib.sha256(NATIVE.read_bytes()).hexdigest() != PIN:
    raise RuntimeError("native executor pin differs")
spec = importlib.util.spec_from_file_location("full_h1_native", NATIVE)
nt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)

p = float(nt.P)
a = float(nt.A)
v = np.array([[a], [p]])
G = np.asarray(nt.G_LOCAL, dtype=float)
S = np.asarray(nt.SOURCE_I_LOCAL, dtype=float)
CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
               [0, 0, 0, 1], [0, 0, 1, 0]], dtype=float)
P, S1, S2, r, t, c, dc, f, df = range(9)
source = nt.Gate("SourceI", (P, S1, S2))

def gg(j):
    return nt.Gate("G", (j,))

def cx(i, j):
    return nt.Gate("CX", (i, j))

def inverse(target, n):
    sw = (cx(P, target), cx(target, P), cx(P, target))
    return sw + (source, source) + (gg(P),)*n + (source, source) + sw

def enc(pointer, tail):
    return (cx(pointer, tail), gg(tail), cx(pointer, tail))

E0 = enc(r, t)
def echo(k):
    return (gg(t),)*k + (cx(r, t),) + (gg(t),)*k + (cx(r, t),)

def plan(k, n):
    prefixes = (E0 + echo(k) + (cx(r, t),)*(2*n), E0 + echo(k+n))
    extra = (inverse(c, 1) + (cx(r, c),) + enc(c, dc) + inverse(t, 2*(k+1))
             + (cx(t, f),) + enc(f, df))
    if len(prefixes[0]) != len(prefixes[1]) or len(prefixes[0]) != 2*(k+n)+5:
        raise AssertionError("equal-length original prefixes")
    if len(extra) != 31+2*k:
        raise AssertionError("actual suffix gate inventory")
    for word in prefixes:
        nt.validate_execution(nt.Execution(9, (), (), word + extra, nt.G_CX_SOURCE_I,
                                           P, (S1, S2), (c, f)),
                              max_qubits=9, max_expanded_stages=len(word)+len(extra))
    return prefixes, extra

# Canonical births may be mathematically tensored at input because no operation
# addresses a wire before its actual birth; check_open verifies chronology.
J = np.eye(16)
for _ in range(5):
    J = np.kron(J, v)
if J.shape != (512, 16):
    raise AssertionError("proper input/birth cut")


def apply(state, gate):
    wires = list(gate.wires)
    local = {"G": G, "CX": CX, "SourceI": S}[gate.op]
    axes = wires + [x for x in range(9) if x not in wires] + [9]
    inverse_axes = np.argsort(axes)
    moved = state.reshape((2,)*9 + (16,)).transpose(axes).reshape(2**len(wires), -1)
    # Elementwise implementation avoids the host BLAS, which raises floating-
    # point exceptions even for an identity-times-zero diagnostic here.
    after = np.zeros_like(moved)
    for row in range(local.shape[0]):
        for column in range(local.shape[1]):
            if local[row, column] != 0:
                after[row] += local[row, column] * moved[column]
    return after.reshape((2,)*9 + (16,)).transpose(inverse_axes).reshape(512, 16)


def run(word):
    out = J.copy()
    for g in word:
        out = apply(out, g)
    return out


def bit(x, wire):
    return (x >> (8-wire)) & 1


def valid_b(x, ptr, tail, value):
    return bit(x, ptr) == 0 if value == 0 else bit(x, ptr) == 1 and bit(x, tail) == 0


def gram(x, indexes):
    z = x[indexes, :]
    return (z[:, :, None] * z[:, None, :]).sum(axis=0)


def target(b, v):
    slot = np.diag([v, 0.0]) if b == 0 else np.diag([0.0, v])
    return np.kron(np.eye(8), slot)

theta = math.atan2(p, a)
worst = 0.0
checks = 0
summaries = []
for k, n in ((0, 1), (9, 33)):
    prefixes, extra = plan(k, n)
    sn = p*p + p**3 * math.sin(2*n*theta)**2
    s1 = p*p + p**3 * math.sin(2*(k+1)*theta)**2
    for which in (0, 1):
        out = run(prefixes[which] + extra)
        if not np.isfinite(out).all():
            raise AssertionError("non-finite state")
        err = np.max(np.abs(gram(out, range(512)) - np.eye(16)))
        worst = max(worst, float(err))
        checks += 1
        if not np.isfinite(err) or err > 2e-12:
            raise AssertionError("complete word is not an input isometry")
        for b in (0, 1):
            for z in (0, 1):
                indices = [i for i in range(512)
                           if valid_b(i, c, dc, b) and valid_b(i, f, df, z)]
                qb = (p*p if which == 0 else sn) if b == 0 else s1
                chance = qb if z == 1 else 1-qb
                err = np.max(np.abs(gram(out, indices) - target(b, chance)))
                worst = max(worst, float(err))
                checks += 1
                if not np.isfinite(err) or err > 2e-12:
                    raise AssertionError("full all-column joint event mismatch")
        for ptr, tail in ((c, dc), (f, df)):
            bad = [i for i in range(512) if bit(i, ptr) == bit(i, tail) == 1]
            err = np.max(np.abs(gram(out, bad)))
            worst = max(worst, float(err))
            checks += 1
            if not np.isfinite(err) or err > 2e-12:
                raise AssertionError("invalid output was not zero")
    summaries.append({"k": k, "n": n, "prefix_calls_each": len(prefixes[0]),
                      "added_calls_each": len(extra), "added_births": 4,
                      "earlier_tail_effect_gap": sn-p*p,
                      "polar_operator_distance_base": 2*abs(math.sin((2*k+1)*theta/2)),
                      "polar_operator_distance_shift": 2*abs(math.sin((2*(k+n)+1)*theta/2))})

print(json.dumps({"status": "PASS", "checks": checks,
                  "programmes": 4, "input_columns": 16, "output_rows": 512,
                  "births_including_original_tail": 5,
                  "cases": summaries, "maximum_matrix_error": worst,
                  "native_sha256": PIN,
                  "readers_and_full_physical_price_proved": False,
                  "GR_closed": False}, sort_keys=True, indent=2))
