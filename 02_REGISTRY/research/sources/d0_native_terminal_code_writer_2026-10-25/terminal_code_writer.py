"""A literal terminal 0/10 container and its complete finite Book carrier.

The parser defines a registered code-length component. It does not identify
that component with the full physical Cost or with elapsed primitive time.
All fresh wires, both CX stages, dirty spin and all clock modes are retained.
"""
from dataclasses import dataclass, replace
from pathlib import Path
import sys
import mpmath as mp

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "d0_native_recorded_info_source_2026-10-25"))
import recorded_info as ri
native = ri.native


@dataclass(frozen=True)
class TerminalWriter:
    execution: object
    code_wires: tuple


def append_terminal_writer(prefix, report, *, max_qubits, max_expanded_stages):
    bounds = dict(max_qubits=max_qubits, max_expanded_stages=max_expanded_stages)
    native.validate_execution(prefix, **bounds)
    if (type(report) is not int or not 0 <= report < prefix.qubits
            or report in set(prefix.old_right) | set(prefix.source_spin or ())):
        raise native.DomainError("writer needs an active ordinary report wire")
    first, tail, length = range(prefix.qubits, prefix.qubits + 3)
    execution = replace(prefix, qubits=prefix.qubits + 3,
        blank_wires=tuple(prefix.blank_wires) + (first, tail, length),
        gates=tuple(prefix.gates) + (native.Gate("CX", (report, first)),
                                   native.Gate("CX", (report, length))),
        report_bits=tuple(prefix.report_bits) + (first, tail, length))
    native.validate_execution(execution, **bounds)
    return TerminalWriter(execution, (first, tail, length))


def parse_container(container):
    """Return (RAW direct/return word, BINARY encoded word), with typed order."""
    if (type(container) not in (tuple, list) or len(container) != 3
            or any(type(x) is not int or x not in (0, 1) for x in container)):
        raise native.DomainError("three binary integer container coordinates required")
    first, tail, length = container
    if tail != 0 or length != first:
        raise native.DomainError("outside the actual terminal code subspace")
    # Lean weightExp uses TRUE for DIRECT, FALSE for RETURN. Binary digits
    # have a different type/meaning: the encoded return is the string 10.
    return (not bool(first),), ((0,) if first == 0 else (1, 0))


def rotation(angle):
    return mp.matrix([[mp.cos(angle), -mp.sin(angle)],
                      [mp.sin(angle), mp.cos(angle)]])


def full_history_factor(theta, phi, u):
    """The full historical eight-dimensional factor on the positive-sine chart.

    This is a mathematical differentiable extension of the literal integer
    native words. It does not assert continuous native-pulse admission.
    Coordinate order: DATA, report, oldR. The bank and dirty spin are separate.
    """
    if not -1 < u < 1:
        raise ValueError("full-history source needs an interior u chart")
    angle = mp.acos(u) / 2
    a = ri.kron(rotation(angle), mp.eye(4))
    cq = mp.zeros(4)
    for d, multiplier in enumerate((3, 1)):
        r = rotation(multiplier * phi)
        for i in range(2):
            for j in range(2): cq[2*d+i, 2*d+j] = r[i, j]
    cx_dr = mp.zeros(8)
    for x in range(8): cx_dr[x ^ ((x >> 2) & 1), x] = 1
    history = cx_dr * ri.kron(rotation(theta), mp.eye(4))
    return a.T * ri.kron(cq, mp.eye(2)) * a * history


def full_phases(theta, phi, u):
    """ALL sixteen phase roots; each has multiplicity32 in the 512 fibre.

    A simultaneous X basis on the two written coordinates is only a proof
    basis. No physical Hadamard or removal of unprepared columns is used.
    """
    f = full_history_factor(theta, phi, u)
    zh = mp.diag([1, 1, -1, -1, 1, 1, -1, -1])
    return tuple(mp.arg(x) for matrix in (f, zh * f)
                 for x in mp.eig(matrix, left=False, right=False))


def phase_representatives(theta, phi, u):
    """Eight +/- representatives for the ORIGINAL Golden theta only.

    Every new input sector is kept. theta is passed to share the same
    numerical precision/angle convention, not to assert a generic-angle law.
    """
    p = (mp.sqrt(5)-1)/2
    c = mp.cos(theta)*u+mp.sin(theta)*mp.sqrt(1-u*u)
    plus = mp.acos(mp.cos(theta)*mp.cos(phi))
    minus = mp.asin(c*mp.sin(phi))
    omega = (2*phi+plus, 2*phi-plus, 2*phi+minus, 2*phi+mp.pi-minus)
    psi_plus = mp.acos(p-p*p*mp.cos(2*phi))/2
    psi_minus = mp.acos(c*c+(1-c*c)*mp.cos(2*phi))/2
    nu = (psi_plus, mp.pi-psi_plus, psi_minus, mp.pi-psi_minus)
    return omega+nu


def full_partition(theta, phi, u, stages, beta_clock):
    if type(stages) is not int or stages < 1 or beta_clock <= 0:
        raise ValueError("positive literal clock and heat parameter required")
    # 32 fibre multiplicity * TWO Hodge degrees * each +/- phase pair.
    return 128 * mp.fsum(mp.exp(-beta_clock * (1-mp.cos((angle+2*mp.pi*k)/stages)))
        for angle in phase_representatives(theta, phi, u) for k in range(stages))


def full_heat_and_source(theta, phi, u, stages, beta_clock):
    """Raw H and unit-u covector for original Golden theta on regular phases.

    beta and literal N stay fixed. The published source application has
    nonzero phi_Q and u in[1/5,3/10]. Removable phase collisions elsewhere
    are not handled by these scalar derivative expressions.
    """
    c = mp.cos(theta)*u+mp.sin(theta)*mp.sqrt(1-u*u)
    dc = mp.cos(theta)-mp.sin(theta)*u/mp.sqrt(1-u*u)
    dm = dc*mp.sin(phi)/mp.sqrt(1-c*c*mp.sin(phi)**2)
    v = c*c+(1-c*c)*mp.cos(2*phi)
    dp = -c*dc*(1-mp.cos(2*phi))/mp.sqrt(1-v*v)
    derivatives = (0, 0, dm, -dm, 0, 0, dp, -dp)
    masses, slopes = [], []
    for angle, derivative in zip(phase_representatives(theta, phi, u), derivatives):
        terms = [(mp.exp(-beta_clock*(1-mp.cos((angle+2*mp.pi*k)/stages))),
                  mp.sin((angle+2*mp.pi*k)/stages)) for k in range(stages)]
        masses.append(mp.fsum(t[0] for t in terms))
        slopes.append(derivative*mp.fsum(t[0]*t[1] for t in terms))
    mass = mp.fsum(masses)
    return mp.log(128*mass)/beta_clock, -mp.fsum(slopes)/(stages*mass)


def full_feedback(phi, u, z):
    if not 0 < z < 1:
        raise ValueError("feedback parameter must lie in (0,1)")
    p = (mp.sqrt(5)-1)/2
    g = (mp.cos(3*phi)+mp.cos(phi)+(mp.cos(3*phi)-mp.cos(phi))*u)/2
    return -4 * mp.log(1-z*(1-p*g*g))


def full_feedback_source(phi, u, z):
    p = (mp.sqrt(5)-1)/2
    c0, c1 = mp.cos(3*phi), mp.cos(phi)
    g = (c0+c1+(c0-c1)*u)/2
    return 4*z*p*g*(c1-c0)/(1-z*(1-p*g*g))


def registered_components(phi, u):
    """Full registered entropy and the declared terminal code-length charge."""
    p = (mp.sqrt(5)-1)/2
    e0, e1 = mp.sin(3*phi)**2, mp.sin(phi)**2
    average, b = (e0+e1)/2, (e0-e1)/2
    qr = (average+b*u, average-b*u)
    q = p*qr[0]+p*p*qr[1]
    entropy = lambda t: -t*mp.log(t)-(1-t)*mp.log1p(-t)
    info = entropy(p)+p*entropy(qr[0])+p*p*entropy(qr[1])
    return {"q": q, "C_code": 1+q, "I_reg_full": info,
            "Dq": b*p**3,
            "DI_reg": b*(p*mp.log((1-qr[0])/qr[0])
                           -p*p*mp.log((1-qr[1])/qr[1]))}
