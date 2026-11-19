"""Literal native adjugate pair, private prefixes and small source helpers.

Forward logical words never touch immutable oldRIGHT. The dedicated helper
is excluded from the logical encoder and only borrowed by exact inverse/
phase macros, which restore it and the source spin on every column.
"""
from pathlib import Path
import sys
import sympy as sp
import mpmath as mp

SOURCES = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOURCES / "d0_native_bilinear_return_echo_2026-10-25"))
import native_echo as en
ne = en.native


def specification(helper=False, request=False):
    if request:
        return (dict(qubits=10, programmes=(1, 2, 6, 7), data=5, spin=(3, 4),
                     helper=0, keys=(8, 9)) if helper else
                dict(qubits=9, programmes=(0, 1, 5, 6), data=2, spin=(3, 4),
                     helper=None, keys=(7, 8)))
    return (dict(qubits=8, programmes=(1, 2, 3, 4), data=5, spin=(6, 7),
                 helper=0, keys=()) if helper else
            dict(qubits=7, programmes=(0, 1, 2, 3), data=4, spin=(5, 6),
                 helper=None, keys=()))


def execution(spec, gates=(), *, protected_keys=False):
    blanks = list(spec["programmes"])
    if spec["helper"] is not None:
        blanks.append(spec["helper"])
    if not protected_keys:
        blanks.extend(spec["keys"])
    return ne.Execution(spec["qubits"], tuple(sorted(blanks)), (), tuple(gates),
                        ne.G_CX_SOURCE_I, source_port=0, source_spin=spec["spin"])


def bounds(spec):
    return dict(max_qubits=spec["qubits"], max_expanded_stages=100000)


def inv_g(q, spec):
    return ne.inverse_word(execution(spec, (ne.Gate("G", (q,)),)), **bounds(spec))


def z_word(q, spec):
    si = (ne.Gate("SourceI", (0, *spec["spin"])),) * 2
    if q == 0:
        return si
    swap = (ne.Gate("CX", (0, q)), ne.Gate("CX", (q, 0)), ne.Gate("CX", (0, q)))
    return swap + si + swap


def middle_word(spec):
    e1, b1, e2, b2 = spec["programmes"]
    return (z_word(e1, spec) + z_word(b1, spec) + z_word(b2, spec)
            + (ne.Gate("CX", (e1, spec["data"])), ne.Gate("CX", (e2, spec["data"]))))


def pair_execution(helper=False, correlated=False, *, stages=None):
    spec = specification(helper)
    e1, b1, e2, b2 = spec["programmes"]
    if correlated:
        forward = (ne.Gate("G", (e1,)), ne.Gate("CX", (e1, b1)),
                   ne.Gate("G", (e2,)), ne.Gate("CX", (e2, b2)))
    else:
        forward = tuple(ne.Gate("G", (q,)) for q in (e1, b1, e2, b2))
    backward = ne.inverse_word(execution(spec, forward), **bounds(spec))
    body = forward + middle_word(spec) + backward
    if stages is None:
        stages = len(body)
    if type(stages) is not int or stages < len(body) or (stages-len(body)) % 2:
        raise ne.DomainError("only a real even number of cancelling CX may pad this pair")
    result = execution(spec, body+(ne.Gate("CX", (e1, spec["data"])),)*(stages-len(body)))
    ne.validate_execution(result, **bounds(spec))
    return spec, result


def request_cell(q, c, spec, *, inverse=False):
    """Exact control0 G/control1 G cubed, or its actual native inverse."""
    g, cx = ne.Gate("G", (q,)), ne.Gate("CX", (c, q))
    if inverse:
        return (cx, g, cx) + inv_g(q, spec) + inv_g(q, spec)
    return (g, g, cx) + inv_g(q, spec) + (cx,)


def request_execution(helper=False, *, protected_keys=False):
    spec = specification(helper, True)
    e1, b1, e2, b2 = spec["programmes"]
    cE, cB = spec["keys"]
    cells = ((e1, cE), (b1, cB), (e2, cE), (b2, cB))
    forward = sum((request_cell(q, c, spec) for q, c in cells), ())
    backward = sum((request_cell(q, c, spec, inverse=True) for q, c in reversed(cells)), ())
    result = execution(spec, forward+middle_word(spec)+backward, protected_keys=protected_keys)
    ne.validate_execution(result, **bounds(spec))
    return spec, result, len(forward), len(backward)


def native_prefix(length):
    """Private five-bit blocks, ONE shared clean helper and ONE spin4."""
    if type(length) is not int or length < 1:
        raise ne.DomainError("a nonempty finite prefix is required")
    qubits, spin = 5*length+3, (5*length+1, 5*length+2)
    gates, blanks, private_sets = (), [0], []
    for j in range(length):
        spec = dict(qubits=qubits, programmes=tuple(range(1+5*j, 5+5*j)),
                    data=5+5*j, spin=spin, helper=0, keys=())
        forward = tuple(ne.Gate("G", (q,)) for q in spec["programmes"])
        gates += forward + middle_word(spec) + ne.inverse_word(execution(spec, forward), **bounds(spec))
        blanks.extend(spec["programmes"])
        private_sets.append(set((*spec["programmes"], spec["data"])))
    result = ne.Execution(qubits, tuple(sorted(blanks)), (), gates, ne.G_CX_SOURCE_I,
                          source_port=0, source_spin=spin)
    ne.validate_execution(result, max_qubits=qubits, max_expanded_stages=100000)
    return result, private_sets


def exact_columns(exe):
    """Propagate its true input isometry in Q(sqrt(p)); never a full256 word.

    This sparse gate action retains every output row of the protected input
    columns. Other columns are covered by separately checked native macros.
    """
    field = sp.QQ.algebraic_field(ne.A)
    aa, pp = field.from_sympy(ne.A), field.from_sympy(ne.P)
    zero, one = field.zero, field.one
    dimension = 1 << exe.qubits
    free = tuple(q for q in range(exe.qubits) if q not in exe.blank_wires)
    rank = 1 << len(free)
    rows = [[zero]*rank for _ in range(dimension)]
    input_rows = []
    for column in range(rank):
        row = sum(((column >> (len(free)-1-j)) & 1) << (exe.qubits-1-q)
                  for j, q in enumerate(free))
        rows[row][column] = one
        input_rows.append(row)
    for gate in exe.gates:
        if gate.op == "G":
            bit = 1 << (exe.qubits-1-gate.wires[0])
            out = [None]*dimension
            for r in range(dimension):
                if r & bit:
                    continue
                left, right = rows[r], rows[r | bit]
                out[r] = [aa*x-pp*y for x, y in zip(left, right)]
                out[r | bit] = [pp*x+aa*y for x, y in zip(left, right)]
        else:
            out = [None]*dimension
            for r, values in enumerate(rows):
                dest, sign = basis_action(exe, gate, r)
                out[dest] = values if sign == 1 else [-x for x in values]
        rows = out
    to_matrix = lambda selected: sp.Matrix([[field.to_sympy(v) for v in row] for row in selected])
    return to_matrix([rows[r] for r in input_rows]), to_matrix(rows)


def basis_action(exe, gate, row):
    """Signed-permutation primitive action, including every dirty spin."""
    if gate.op == "CX":
        control, target = (1 << (exe.qubits-1-q) for q in gate.wires)
        return row ^ (target if row & control else 0), 1
    if gate.op != "SourceI":
        raise ValueError("G is not a signed permutation")
    port, spin0, spin1 = gate.wires
    if not row & (1 << (exe.qubits-1-port)):
        return row, 1
    bits = (1 << (exe.qubits-1-spin0), 1 << (exe.qubits-1-spin1))
    source = 2*bool(row & bits[0])+bool(row & bits[1])
    dest = next(j for j in range(4) if ne.L_I[j, source] != 0)
    result = row & ~bits[0] & ~bits[1]
    result |= ((dest >> 1) & 1)*bits[0] + (dest & 1)*bits[1]
    return result, int(ne.L_I[dest, source])


def signed_word(exe):
    images = []
    for column in range(1 << exe.qubits):
        row, sign = column, 1
        for gate in exe.gates:
            row, phase = basis_action(exe, gate, row)
            sign *= phase
        images.append((row, sign))
    return images


def scalar(E, b):
    return (1-2*E)*(1-2*b)**2


def prefix_price(scalars, zeta):
    product = mp.fprod(scalars)
    rank = 4*2**len(scalars)
    return -rank*mp.log(1-zeta+zeta*product**2)


def prefix_gain(p, zeta, length, tau=1):
    rank = 4*2**length
    return 4*rank*zeta*p**(18*length-1)*tau/(1-zeta+zeta*p**(18*length))
