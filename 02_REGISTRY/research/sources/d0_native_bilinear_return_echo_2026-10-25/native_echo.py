"""An exact native bilinear return adapter, including its dirty-spin inverse.

It realizes the original rank-two return CORNER with four protected spin
copies. It does not realize the original full8 logical query channel.
"""
from pathlib import Path
import sys
import sympy as sp

DOMAIN = Path(__file__).resolve().parent.parent / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0, str(DOMAIN))
import native_execution as native

BOUNDS = dict(max_qubits=5, max_expanded_stages=10000)


def layout(gates=()):
    return native.Execution(5, (0, 1), (), tuple(gates), native.G_CX_SOURCE_I,
                            source_port=0, source_spin=(3, 4))


def middle_word():
    si = native.Gate("SourceI", (0, 3, 4))
    swap = (native.Gate("CX", (0, 1)), native.Gate("CX", (1, 0)),
            native.Gate("CX", (0, 1)))
    return (si, si)+swap+(si, si)+swap+(native.Gate("CX", (0, 2)),)


def echo(kE, kB, stages=None):
    if any(type(k) is not int or k < 0 for k in (kE, kB)):
        raise native.DomainError("nonnegative literal Golden powers required")
    forward = (native.Gate("G", (0,)),)*kE+(native.Gate("G", (1,)),)*kB
    reverse = native.inverse_word(layout(forward), **BOUNDS)
    body = forward+middle_word()+reverse
    if stages is None:
        stages = len(body)
    if type(stages) is not int or stages < len(body) or (stages-len(body)) % 2:
        raise native.DomainError("padding requires an actual even number of CX stages")
    padded = body+(native.Gate("CX", (0, 2)),)*(stages-len(body))
    execution = layout(padded)
    native.validate_execution(execution, **BOUNDS)
    return execution


def exact_bias(k):
    return (native.G_LOCAL**k)[1, 0]**2


def correlated_echo(stages=51):
    forward = (native.Gate("G", (0,)), native.Gate("CX", (0, 1)))
    body = forward+middle_word()+native.inverse_word(layout(forward), **BOUNDS)
    if type(stages) is not int or stages < len(body) or (stages-len(body)) % 2:
        raise native.DomainError("padding requires actual even CX stages")
    execution = layout(body+(native.Gate("CX", (0, 2)),)*(stages-len(body)))
    native.validate_execution(execution, **BOUNDS)
    return execution


def corner(E, b):
    x = sp.Matrix([[0, 1], [1, 0]])
    return (1-2*b)*((1-E)*sp.eye(2)-E*x)


def feedback_bands(E, b):
    B, ell = 4*b*(1-b), 4*E*(1-E)
    return ell+(1-ell)*B, B
