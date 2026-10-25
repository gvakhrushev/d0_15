"""Literal native completion edits and their complete terminal label law.

Only G/CX/SourceI stages are emitted.  Matrices and scalar charges below are
comparison/evaluation helpers, not extra physical primitives or Cost tariffs.
"""
from dataclasses import replace
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

SOURCES = Path(__file__).resolve().parent.parent
DOMAIN = SOURCES / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0, str(DOMAIN))
import native_execution as native
if Path(native.__file__).resolve() != (DOMAIN / "native_execution.py").resolve():
    raise ImportError("the owned native_execution module is required")

HELPER, CONTROL, PORT, JUNK, SPIN = 0, 1, 2, 3, (4, 5)
BOUNDS = dict(max_qubits=9, max_expanded_stages=10000)


def layout(*, algorithmic=False):
    blanks = (CONTROL, JUNK) if algorithmic else (HELPER, CONTROL, PORT, JUNK)
    return native.Execution(6, blanks, (), (), native.G_CX_SOURCE_I,
                            source_port=HELPER, source_spin=SPIN)


def _positive(n, name):
    if type(n) is not int or n < 1:
        raise native.DomainError(name+" must be a positive integer")
    return n


def inverse_g(wire, n=1):
    n = _positive(n, "inverse multiplicity")
    code = replace(layout(), gates=(native.Gate("G", (wire,)),)*n)
    return native.inverse_word(code, **BOUNDS)


def controlled(target, L=1, *, inverse=False):
    """Optimized symbolic W_1(L), or its reversed symbolic inverse.

    Reuse the already exact G^-L block; do not invert its expanded SourceI
    letters recursively. Both words have 12L+2 actual primitive stages.
    """
    L = _positive(L, "controlled repeat")
    if target not in (PORT, JUNK):
        raise native.DomainError("this fixture has only the declared private targets")
    g = (native.Gate("G", (target,)),)*L
    gi = inverse_g(target, L)
    cx = (native.Gate("CX", (CONTROL, target)),)
    return cx+g+cx+gi if inverse else g+cx+gi+cx


def controlled_junk(L, *, inverse=False):
    return controlled(JUNK, L, inverse=inverse)


def forward_execution(L, r=5):
    """A_L=A R_L^dagger, chronological R_L^-1; G_control^r."""
    r = _positive(r, "source exponent")
    word = controlled_junk(L, inverse=True)+(native.Gate("G", (CONTROL,)),)*r
    code = replace(layout(algorithmic=True), gates=word)
    native.validate_execution(code, **BOUNDS)
    return code


def execution(L, r=5, *, recorded=False):
    """The two compared L=1,2 words have the SAME true gate inventory."""
    if type(L) is not int or L not in (1, 2):
        raise native.DomainError("this bounded comparison declares L=1 or L=2")
    r = _positive(r, "source exponent")
    a = (native.Gate("G", (CONTROL,)),)*r
    word = (controlled_junk(L, inverse=True)+a+controlled(PORT)
            +inverse_g(CONTROL, r)+controlled_junk(L))
    if L == 1:
        identity = (native.Gate("G", (JUNK,)),)+inverse_g(JUNK)
        word += identity*2
    code = replace(layout(), gates=word)
    if recorded:
        records = (6, 7, 8)
        copies = tuple(native.Gate("CX", (q, t))
                       for q, t in zip((CONTROL, PORT, JUNK), records))
        code = replace(code, qubits=9, blank_wires=(*code.blank_wires, *records),
                       gates=copies+word+copies, report_bits=records)
    native.validate_execution(code, **BOUNDS)
    return code


def rotation(n):
    n = _positive(n, "rotation power")
    return DomainMatrix.from_Matrix(native.G_LOCAL).convert_to(
        native.GOLDEN_FIELD).pow(n).to_Matrix()


def expected_private(L, r=5):
    """Private order (control,port,junk); this is a comparison matrix."""
    s = sp.kronecker_product(rotation(r), sp.eye(4))
    w = sp.diag(sp.eye(4), sp.kronecker_product(rotation(2), sp.eye(2)))
    rot = sp.diag(sp.eye(4), sp.kronecker_product(sp.eye(2), rotation(2*L)))
    return rot*s.T*w*s*rot.T


def data(L, r=5):
    p = native.P
    q = rotation(r)[1, 0]**2
    c, b = p**3, rotation(2)[1, 0]
    d, v = 1-c, rotation(2*L)[1, 0]**2
    s = 1-d*q
    return dict(q=q, c=c, b=b, d=d, v=v, s=s, mu=2*d*q*(1-q))


def probabilities(L, r=5):
    """Actual complete label law in binary private order 000,...,111."""
    z = data(L, r)
    q, d, b, v, s = (z[k] for k in ("q", "d", "b", "v", "s"))
    return (s*s, 0, b*b*q*q, 0,
            d*d*q*(1-q)*(1-v), d*d*q*(1-q)*v,
            b*b*q*(1-q)*(1-v), b*b*q*(1-q)*v)


def base_probabilities(r=5):
    z = data(1, r)
    q, d, b, s = (z[k] for k in ("q", "d", "b", "s"))
    return (s*s, b*b*q*q, d*d*q*(1-q), b*b*q*(1-q))


def private_copy():
    """Actual six-wire CX copy on private3 tensor fresh-record3 only."""
    return native.Execution(6, tuple(range(6)), (),
        tuple(native.Gate("CX", (q, q+3)) for q in range(3)), native.G_CX)


def reduced_recorded(private):
    """All64 private/record columns; shared helper/spin are not simulated."""
    indices = tuple(8*w+(record ^ w) for w in range(8) for record in range(8))
    return sp.kronecker_product(private, sp.eye(8)).extract(indices, indices)


def marked_scalar(probabilities, charges, t):
    if len(probabilities) != len(charges):
        raise ValueError("one actual supplied charge per complete label is required")
    return sum(sp.exp(-t*c)*p for p, c in zip(probabilities, charges))
