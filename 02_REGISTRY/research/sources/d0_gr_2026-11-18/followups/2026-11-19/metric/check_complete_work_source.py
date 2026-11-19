"""All 34 actual LIVE_PARSER stages, with arbitrary local work insertions.

This is an exact compiler for a DECLARED additive, field-independent local
work model.  It does not identify that model with native Book03 Cost-Info.

Convention: W_s is charged on the operation wires immediately AFTER stage s.
Pre-gate charges are also tabulated.  A birth is genuinely rectangular: its
post-birth mark is compressed by the canonical born isometry.  No operation
is cancelled, and the six births are included separately from the 28 gates.
The literal LIVE_PARSER uses its allowed deferred joint terminal-check
variant: the four slot projectors are transported to the terminal check.
There is no intervening physical dephasing.  W_s denotes an expected work
mark, not an additional invasive measurement inserted in the native word.

All arithmetic in the proof is in Z[a], a^4+a^2-1=0, a>0, p=a^2.  Exact
integer contractions use checked int64 bounds; rational Pauli coefficients
are recorded in the basis (1,a,a^2,a^3).  Floating values are diagnostics.
Run with ordinary Python or python -O; neither uses removable assertions.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import numpy as np

from check_live_parser import controller
from check_source_price import load_control, need


LIMIT = 2**61
REDUCE = np.array([
    [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1],
    [1, 0, -1, 0], [0, 1, 0, -1], [-1, 0, 2, 0],
], dtype=np.int64)
ONE = REDUCE[0]
A = REDUCE[1]
P = REDUCE[2]
PAULIS = "IXYZ"
GLOBAL_BASIS = (["I"] + ["S."+s for s in map("".join, product(PAULIS, repeat=2))
                         if s != "II"] + ["P."+s for s in "XYZ"]
                + ["T."+s for s in "XYZ"])


def maxabs(x):
    return int(np.max(np.abs(x))) if x.size else 0


def add(x, y):
    need(maxabs(x)+maxabs(y) < LIMIT, "exact integer addition bound")
    return x+y


def scale(x, c):
    """Multiply a field-valued array by one field element."""
    out = np.zeros_like(x)
    need(32*maxabs(x)*maxabs(c) < LIMIT, "exact scalar-product bound")
    for i in range(4):
        for j in range(4):
            if c[j] and np.any(x[i]):
                term = c[j]*x[i]
                for k in range(4):
                    if REDUCE[i+j, k]:
                        out[k] += REDUCE[i+j, k]*term
    return out


def power_a(n):
    base = A if n >= 0 else np.array([0, 1, 0, 1], dtype=np.int64)
    out = ONE.copy()
    for _ in range(abs(n)):
        out = scale(out, base)
    return out


def power_p(n):
    return power_a(2*n)


def dot(x, y):
    """x^T y for real matrices over the exact field."""
    need(x.shape[1] == y.shape[1], "typed exact contraction")
    out = np.zeros((4, x.shape[2], y.shape[2]), dtype=np.int64)
    need(32*x.shape[1]*maxabs(x)*maxabs(y) < LIMIT,
         "no integer contraction or field-reduction overflow")
    for i in range(4):
        for j in range(4):
            if np.any(x[i]) and np.any(y[j]):
                term = x[i].T @ y[j]
                for k in range(4):
                    if REDUCE[i+j, k]:
                        out[k] += REDUCE[i+j, k]*term
    return out


def matmul(x, y):
    return dot(x.transpose(0, 2, 1), y)


def trace(x):
    need(x.shape[1]*maxabs(x) < LIMIT, "exact trace cannot overflow")
    return np.trace(x, axis1=1, axis2=2)


def eye(n):
    out = np.zeros((4, n, n), dtype=np.int64)
    out[0] = np.eye(n, dtype=np.int64)
    return out


def equal(x, y, what):
    need(np.array_equal(x, y), what)


def element(ne, value):
    coeffs = list(ne.GOLDEN_FIELD.from_sympy(value).to_list())
    coeffs = [Fraction(c.numerator, c.denominator) for c in coeffs]
    coeffs = [Fraction(0)]*(4-len(coeffs))+coeffs
    need(all(c.denominator == 1 for c in coeffs), "native integral gate entry")
    return np.array([int(c) for c in reversed(coeffs)], dtype=np.int64)


def native_local(ne, op):
    """Read the actual pinned native matrix, including SourceI frame order."""
    arity = {"G": 1, "CX": 2, "SourceI": 3}[op]
    gate = ne.Gate(op, tuple(range(arity)))
    ex = ne.Execution(arity, (), (), (gate,),
                      profile=ne.G_CX_SOURCE_I if op == "SourceI" else ne.G_CX,
                      source_port=0 if op == "SourceI" else None,
                      source_spin=(1, 2) if op == "SourceI" else None)
    matrix = ne.gate_matrix(ex, gate, max_qubits=3, max_expanded_stages=1)
    out = np.zeros((4, 2**arity, 2**arity), dtype=np.int64)
    for i in range(2**arity):
        for j in range(2**arity):
            out[:, i, j] = element(ne, matrix[i, j])
    equal(dot(out, out), eye(2**arity), "full-column native local unitary")
    return out


def support_indices(n, wires):
    rest = tuple(i for i in range(n) if i not in wires)
    indices = np.zeros((2**len(wires), 2**len(rest)), dtype=np.int64)
    for local in range(2**len(wires)):
        for tail in range(2**len(rest)):
            row = 0
            for j, wire in enumerate(wires):
                row |= ((local >> (len(wires)-1-j)) & 1) << (n-1-wire)
            for j, wire in enumerate(rest):
                row |= ((tail >> (len(rest)-1-j)) & 1) << (n-1-wire)
            indices[local, tail] = row
    return indices


def apply_local(v, matrix, n, wires):
    indices = support_indices(n, wires)
    out = np.zeros_like(v)
    for i in range(len(indices)):
        for j in range(len(indices)):
            c = matrix[:, i, j]
            if np.any(c):
                out[:, indices[i], :] = add(out[:, indices[i], :],
                                             scale(v[:, indices[j], :], c))
    return out


def born(v):
    out = np.zeros((4, 2*v.shape[1], v.shape[2]), dtype=np.int64)
    out[:, 0::2, :] = scale(v, A)
    out[:, 1::2, :] = scale(v, P)
    equal(dot(out, out), dot(v, v), "rectangular birth preserves every input column")
    return out


def pauli_rule(n, wires, label):
    rows = np.arange(2**n, dtype=np.int64)
    targets = rows.copy()
    signs = np.ones(2**n, dtype=np.int64)
    phase = 0
    for wire, letter in zip(wires, label):
        bit = (rows >> (n-1-wire)) & 1
        if letter in "XY":
            targets ^= 1 << (n-1-wire)
        if letter in "YZ":
            signs *= 1-2*bit
        if letter == "Y":
            phase += 1
    return targets, signs, phase % 4


def compress_pauli(v, n, wires, label):
    targets, signs, phase = pauli_rule(n, wires, label)
    changed = np.zeros_like(v)
    changed[:, targets, :] = v*signs[None, :, None]
    return dot(v, changed), phase


def decompose(matrix, phase, qubits):
    """Complete Hermitian Pauli expansion, with exact reconstruction."""
    d = 2**qubits
    need(d**3*maxabs(matrix) < LIMIT,
         "Pauli traces and full reconstruction cannot overflow")
    answer = {}
    rec = [np.zeros_like(matrix), np.zeros_like(matrix)]
    for label in map("".join, product(PAULIS, repeat=qubits)):
        targets, signs, qphase = pauli_rule(qubits, tuple(range(qubits)), label)
        c = np.sum(matrix[:, np.arange(d), targets]*signs[None, :], axis=1)
        totalphase = (phase+qphase) % 4
        if totalphase % 2:
            equal(c, np.zeros(4, dtype=np.int64), "Hermitian expansion has real coefficients")
            continue
        if totalphase == 2:
            c = -c
        if np.any(c):
            answer[label] = (c, d)
            sign = -1 if qphase >= 2 else 1
            for j, target in enumerate(targets):
                rec[qphase % 2][:, target, j] += sign*int(signs[j])*c
    target = [np.zeros_like(matrix), np.zeros_like(matrix)]
    target[phase % 2] = (-1 if phase >= 2 else 1)*d*matrix
    equal(rec[0], target[0], "exact complete Pauli reconstruction, real part")
    equal(rec[1], target[1], "exact complete Pauli reconstruction, imaginary part")
    return answer


def globalize(mapping, which):
    out = {}
    for label, coefficient in mapping.items():
        if set(label) == {"I"}:
            name = "I"
        elif which == "T":
            name = "T."+label
        elif label[2] == "I":
            name = "S."+label[:2]
        elif label[:2] == "II":
            name = "P."+label[2]
        else:
            raise ArithmeticError("unproved mixed Spin x port work component: "+label)
        out[name] = coefficient
    return out


def coefficient_text(c, denominator=1):
    terms = []
    for i, value in enumerate(c):
        v = Fraction(int(value), int(denominator))
        if not v:
            continue
        atom = "" if i == 0 else ("a" if i == 1 else "a^"+str(i))
        if atom and abs(v) == 1:
            text = atom
        else:
            text = str(abs(v))+("*"+atom if atom else "")
        terms.append(("-" if v < 0 else ("+" if terms else ""))+text)
    return "".join(terms) or "0"


def encode_mapping(mapping):
    return {k: coefficient_text(c, d) for k, (c, d) in mapping.items()}


def scalar_value(c, denominator=1):
    av = np.sqrt((np.sqrt(5.)-1.)/2.)
    return float(sum(int(v)*av**i for i, v in enumerate(c))/denominator)


def reduced_delta(v, n, wires):
    indices = support_indices(n, wires)
    states = []
    for t in (0, 1):
        array = v[:, indices, t].transpose(0, 2, 1)
        states.append(dot(array, array))
    equal(trace(states[0]), ONE, "T=0 complete conditional state has trace one")
    equal(trace(states[1]), ONE, "T=1 complete conditional state has trace one")
    return states[1]-states[0]


def classical_t_intertwiner(v, n):
    """Check Z_T V = V Z_T on every old column, not one input state."""
    targets, signs, phase = pauli_rule(n, (1,), "Z")
    need(phase == 0, "classical T intertwiner is real")
    left = np.zeros_like(v)
    left[:, targets, :] = v*signs[None, :, None]
    right = v*np.array([1, -1], dtype=np.int64)[None, None, :]
    equal(left, right, "every prefix through marked stage 7 intertwines the old T projection")
    # The two corresponding pure conditional states, and hence arbitrary
    # block-diagonal mixtures with reference/old-bank states, commute with
    # P_T.  Checking all columns proves this without a spectator choice.
    for t in (0, 1):
        wrong_rows = [i for i in range(2**n) if ((i >> (n-2)) & 1) != t]
        equal(v[:, wrong_rows, t], np.zeros((4, len(wrong_rows)), dtype=np.int64),
              "each full prefix column lies in its original T eigenspace")


def spectral_bound(v, n, wires):
    """Exact extrema over 0 <= W <= I for a fixed common old spectator."""
    delta = reduced_delta(v, n, wires)
    equal(trace(delta), np.zeros(4, dtype=np.int64), "contrast is traceless")
    if not np.any(delta):
        return np.zeros(4, dtype=np.int64), {"type": "zero", "positive_projector": "0"}
    if 1 in wires:  # Original classical T is the second local WORK wire.
        bit = wires.index(1)
        d = 2**len(wires)
        plus = np.zeros((4, d, d), dtype=np.int64)
        for i in range(d):
            if (i >> (len(wires)-1-bit)) & 1:
                plus[0, i, i] = 1
        # T is never a target; the two positive conditional states occupy
        # disjoint T sectors.  The projector is an exact optimal effect.
        equal(matmul(plus, plus), plus, "positive spectral effect is a projector")
        equal(trace(matmul(delta, plus)), ONE, "T projector attains the exact upper extremum")
        for i in range(d):
            for j in range(d):
                if ((i ^ j) >> (len(wires)-1-bit)) & 1:
                    equal(delta[:, i, j], np.zeros(4, dtype=np.int64),
                          "opposite T sectors have no coherence")
        return ONE.copy(), {"type": "orthogonal_T_sectors",
                            "positive_projector": "P(T=1) on the operation support",
                            "positivity_proof": "two genuine partial states on orthogonal T sectors"}
    squared = matmul(delta, delta)
    candidate = None
    for k in range(13):
        if np.array_equal(trace(squared), 2*power_p(2*k)):
            candidate = k
            break
    need(candidate is not None, "exact local contrast has identified native spectral radius")
    k = candidate
    r = power_p(k)
    equal(matmul(squared, delta), scale(delta, power_p(2*k)),
          "exact cubic polynomial of the local contrast")
    # Twice the two rank-one spectral projectors, avoiding division in
    # matrix arithmetic.  Hermitian idempotence proves positivity.
    for sign in (1, -1):
        twice = add(scale(squared, power_p(-2*k)), sign*scale(delta, power_p(-k)))
        equal(matmul(twice, twice), 2*twice, "exact spectral-projector idempotence")
        equal(twice, twice.transpose(0, 2, 1), "exact Hermitian spectral projector")
        equal(trace(twice), 2*ONE, "each nonzero spectral projector has rank one")
        equal(matmul(delta, twice), sign*scale(twice, r), "spectral effect attains signed extremum")
    return r, {"type": "two_nonzero_eigenvalues", "positive_eigenvalue": "p^"+str(k),
               "negative_eigenvalue": "-p^"+str(k),
               "positive_projector": "(delta^2/p^(2k)+delta/p^k)/2, k="+str(k),
               "verified": "Hermitian idempotence, rank one, and delta Pi_+=p^k Pi_+ exactly"}


def all_maps(v, n, wires, which):
    maps = {}
    exact = {}
    contrast = {}
    for label in map("".join, product(PAULIS, repeat=len(wires))):
        matrix, phase = compress_pauli(v, n, wires, label)
        mapping = globalize(decompose(matrix, phase, 1 if which == "T" else 3), which)
        maps[label] = encode_mapping(mapping)
        exact[label] = mapping
        if "T.Z" in mapping:
            c, d = mapping["T.Z"]
            if np.any(c):
                contrast[label] = coefficient_text(-2*c, d)
    identity = "I"*len(wires)
    need(maps[identity] == {"I": "1"}, "work identity charges exactly one at this actual stage")
    return maps, exact, contrast


def modular_rank(rows, basis):
    # A nonzero modular minor gives a characteristic-zero lower bound;
    # the complete sparse-support calculation gives the matching upper.
    prime, root = None, None
    for modulus in (101, 103, 107, 109, 127, 131):
        for a in range(modulus):
            if (a**4+a*a-1) % modulus == 0:
                prime, root = modulus, a
                break
        if prime is not None:
            break
    need(prime is not None, "finite-field image of native exact coefficient ring")
    data = []
    for row in rows:
        data.append([sum(int(v)*pow(root, i, prime) for i, v in enumerate(row.get(k, (ONE*0, 1))[0]))
                     * pow(int(row.get(k, (ONE*0, 1))[1]), -1, prime) % prime for k in basis])
    pivots = []
    r = 0
    origins = list(range(len(data)))
    for c in range(len(basis)):
        pivot = next((i for i in range(r, len(data)) if data[i][c]), None)
        if pivot is None:
            continue
        data[r], data[pivot] = data[pivot], data[r]
        origins[r], origins[pivot] = origins[pivot], origins[r]
        v = pow(data[r][c], -1, prime)
        data[r] = [(x*v) % prime for x in data[r]]
        for j in range(r+1, len(data)):
            if data[j][c]:
                z = data[j][c]
                data[j] = [(x-z*y) % prime for x, y in zip(data[j], data[r])]
        pivots.append({"column": basis[c], "original_row": origins[r]})
        r += 1
    return {"rank": r, "prime": prime, "a_mod_prime": root, "pivots": pivots}


def run():
    ne, native_digest = load_control()
    checked_digest, listed = controller()
    need(native_digest == checked_digest, "same pinned physical native executor")
    local = {op: native_local(ne, op) for op in ("G", "CX", "SourceI")}
    equal(element(ne, ne.A**4+ne.A**2-1), np.zeros(4, dtype=np.int64), "native field relation")
    word = [ne.Gate(row[0], tuple(row[1:])) for row in listed]
    # WORK arena is [H,T,D,F_D,C,F_C,F_X,F_T].  H=1, T is a full
    # two-column input, so off-diagonal T maps are not silently lost.
    v = np.zeros((4, 4, 2), dtype=np.int64)
    v[0, 2, 0] = v[0, 3, 1] = 1
    n = 2
    stages, all_rows, row_names = [], [], []
    radii = np.zeros(4, dtype=np.int64)

    def append_stage(number, op, original_wires, post, before, wires, arena_n, which):
        nonlocal radii
        maps, exact, contrast = all_maps(post, arena_n, wires, which)
        old_maps = None
        if before is not None:
            old_maps, _, _ = all_maps(before, arena_n, wires, which)
        if which == "T":
            radius, witness = spectral_bound(post, arena_n, wires)
            if before is not None:
                preradius, _ = spectral_bound(before, arena_n, wires)
                equal(radius, preradius, "pre/post local trace distance is unitarily invariant")
            if number <= 7:
                classical_t_intertwiner(post, arena_n)
        else:
            radius = np.zeros(4, dtype=np.int64)
            witness = {"type": "zero_T_contrast_for_every_common_spectator_state",
                       "reason": "this actual blank prefix acts only on Spin, dirty port and independent C"}
            need(not contrast, "blank has no T-dependent local-work insertion")
        radii = add(radii, radius)
        for label, mapping in exact.items():
            all_rows.append(mapping)
            row_names.append({"stage": number, "local_Pauli": label})
        record = {"stage": number, "operation": op, "wires_in_original_order": list(original_wires),
                  "local_Hermitian_basis_size": 4**len(wires),
                  "post_work_pullback": maps,
                  "T1_minus_T0_nonzero_Pauli_coefficients": contrast,
                  "max_effect_T_source_exact": coefficient_text(radius),
                  "max_effect_T_source_decimal": format(scalar_value(radius), ".16g"),
                  "spectral_witness": witness}
        if number <= 7:
            record["positive_ledger_current_tangent_witness"] = {
                "checked_exactly": "Z_T V_s = V_s Z_T and each conditional old-T column remains in its own T sector",
                "implication": "the full prefix state commutes with P_T for every classically correlated Spin-port-reference input",
                "arbitrary_tangent_source": 0,
                "argument": "unitary tangent: Tr(rho [P_T,X])=0; isometric birth tangent: X=J^dagger dJ is anti-Hermitian and PJ=JP",
            }
        else:
            record["positive_ledger_current_tangent_witness"] = {
                "arbitrary_tangent_source": 0,
                "argument": "stage-7 marked charge has already been paid; each other stage is the identity mark and all subsequent maps preserve trace",
            }
        if old_maps is not None:
            record["pre_work_pullback"] = old_maps
        else:
            record["pre_work_convention"] = "new wire does not exist before birth; use the displayed rectangular post compression"
        stages.append(record)

    for i in range(6):
        v = born(v)
        n += 1
        append_stage(i+1, "birth(v)", (5+i,), v, None, (n-1,), n, "T")

    # Independent four-wire blank arena [Spin0,Spin1,port,C].  Its old
    # input is the complete Spin4 x dirty-port2, including entanglement.
    blank = born(eye(8))
    blank_remap = {0: 0, 1: 1, 2: 2, 7: 3}
    for i, gate in enumerate(word):
        stage = i+7
        if 11 <= stage <= 21:
            wires = tuple(blank_remap[q] for q in gate.wires)
            before = blank.copy()
            blank = apply_local(blank, local[gate.op], 4, wires)
            equal(dot(blank, blank), eye(8), "all-column dirty-port/Spin blank prefix isometry")
            append_stage(stage, gate.op, gate.wires, blank, before, wires, 4, "R")
            if stage == 21:
                expected = np.zeros_like(blank)
                expected[0, 0::2, :] = np.eye(8, dtype=np.int64)
                equal(blank, expected, "complete actual eleven-gate blank restores Spin and dirty port exactly")
                # The same full-column word is I_Spin,port x G_C^{-1}.
                # Thus the WORK calculation continues with its actual C=0,
                # preserving every other old and new correlation.
                v = apply_local(v, local["G"].transpose(0, 2, 1), n, (7-3,))
                equal(dot(v, v), eye(2), "native blank substitution preserves full T columns")
        else:
            need(all(q >= 3 for q in gate.wires), "nonblank stage never touches protected old Spin/port")
            wires = tuple(q-3 for q in gate.wires)
            before = v.copy()
            v = apply_local(v, local[gate.op], n, wires)
            equal(dot(v, v), eye(2), "all-column actual WORK prefix isometry")
            append_stage(stage, gate.op, gate.wires, v, before, wires, n, "T")

    need(len(stages) == 34 and sum(s["local_Hermitian_basis_size"] for s in stages) == 604,
         "every birth and every gate has its entire local Hermitian basis")
    # The factorization is verified by complete basis maps, not by one
    # maximally mixed spectator state.  Dimension: 16 Spin +4 port +4 T,
    # with two duplicated identities; dephasing old T removes X and Y.
    coherent = modular_rank(all_rows, GLOBAL_BASIS)
    classical_basis = [s for s in GLOBAL_BASIS if s not in ("T.X", "T.Y")]
    classical = modular_rank(all_rows, classical_basis)
    need(coherent["rank"] == 22 and classical["rank"] == 20,
         "all-stage local-work source image has exactly 22 coherent /20 classical dimensions")
    for certificate in (coherent, classical):
        for pivot in certificate["pivots"]:
            pivot["witness"] = row_names[pivot["original_row"]]
    equal(radii, 9*ONE-4*P, "sharp total independently marked effect-source budget")

    # All 34 stages cost I; only stage 7 has a local extra lambda P(T=0).
    # Since that real CX leaves its control unchanged, the full-input
    # compression is exact, even with an arbitrary dirty entangled old bank.
    stage7 = stages[6]
    need(stage7["wires_in_original_order"] == [4, 5] and stage7["operation"] == "CX",
         "the actual seventh stage is the original live-T readout")
    need(stage7["post_work_pullback"]["ZI"] == {"T.Z": "1"},
         "stage-seven T mark pulls back exactly on every old input column")
    need(stage7["post_work_pullback"]["IZ"] == {"T.Z": coefficient_text(power_p(3))},
         "actual first readout D occupancy retains the exact p^3 Dpi source")
    equal(ONE-power_p(3), 2*power_p(2), "first readout occupancy is p^2+p^3 pi")
    # Concrete positive spectator-sensitive ledgers, in addition to the
    # complete rank proof.  These contributions repeat with the word.
    need(stages[13]["post_work_pullback"]["IZI"] == {"S.ZI": "1"},
         "actual stage-14 Spin mark retains an unsuppressed old Spin source")
    need(stages[10]["post_work_pullback"]["ZI"] == {"P.Z": "1"},
         "actual stage-11 port mark retains an unsuppressed dirty-port source")
    # Any anti-Hermitian current tangent through stage 7 has zero scalar
    # work derivative on a dephased T input: the marked projection commutes
    # with that whole state, including arbitrary conditional old banks.
    # Earlier births intertwine that projection and preserve isometry;
    # later operations cannot alter a charge already incurred.
    examples = []
    for lam in (0, 1, 2):
        examples.append({"lambda": lam, "nonparsed_work_operator": f"34 I + {lam} P(T=0)",
                         "nonparsed_mean": f"{34+lam} - {lam} pi",
                         "parsed_CQ_mean": "4 + pi",
                         "total_declared_mean": f"{38+lam} + ({1-lam}) pi",
                         "pi_source": 1-lam,
                         "nonparsed_current_unitary_tangent_source": 0,
                         "current_work_tangent_proof": "dephased-T commutator through stage 7; isometric birth derivatives; later marks already paid",
                         "local_stage_charge_spectra": "[1,1+lambda] at stage 7; {1} at every other stage"})

    # Independent full terminal parsed lengths, rather than double counting
    # the per-operation work as already paid printed symbols.
    expected_lengths = []
    for t in (0, 1):
        total = np.zeros(4, dtype=np.int64)
        for d in (0, 1):
            mass = power_p(1 if d == t else 2)
            total = add(total, (5+(d != t)+t)*mass)
        equal(total, (5+t)*ONE+power_p(2), "full four-code expected terminal length")
        expected_lengths.append(coefficient_text(total))
    # H_phi(p,p^2)=p+2p^2=1+p^2, exactly from -log_phi p^k=k.
    equal(P+2*power_p(2), ONE+power_p(2), "canonical complete noise entropy")

    here = Path(__file__).resolve()
    dependencies = [here.with_name("check_live_parser.py"), here.with_name("check_source_price.py")]
    return {
        "status": "PASS",
        "statement": "complete 34-stage local-work pullback on the literal guarded native word",
        "scientific_status": {"native_physical_price_identified": False, "obligation_C_discharged": False,
                              "GR_closed": False, "model": "declared additive field-independent Hermitian local marks"},
        "source_sha256": {"native_execution.py": native_digest,
                          **{q.name: sha256(q.read_bytes()).hexdigest() for q in dependencies}},
        "exact_field": {"basis": ["1", "a", "a^2", "a^3"],
                        "relation": "a^4+a^2-1=0", "embedding": "a>0, p=a^2=(sqrt(5)-1)/2"},
        "input": {"H": 1, "old_input_order": ["Spin0", "Spin1", "dirty_port", "T"],
                  "old_input_dimension": 16, "full_output_dimension": 2048,
                  "classical_scope": "T dephased, with arbitrary conditional Spin-port states and arbitrary external references",
                  "no_spectator_state_substitution": True,
                  "conditional_extrema_scope": "vary T=0/1 with the same arbitrary fixed spectator state; its source is separately retained"},
        "history_variant": {
            "terminal_check": "one deferred joint terminal check, with the four original slot projectors transported to the end",
            "intermediate_physical_dephasing": False,
            "work_marks_are_additional_instruments": False,
            "other_variant": "actual early measurements require their own Kraus-propagated prefix work maps; this table does not silently identify the two histories",
        },
        "work_convention": "post-stage W_s on the listed actual operation wires; all six births and all 28 square calls charged",
        "pre_gate_equivalence": "W_pre corresponds to U_s W_pre U_s^dagger post-stage; both full basis maps are recorded",
        "Pauli_convention": "label order equals listed wire order, Y=[[0,-i],[i,0]]; W=sum_P Tr(PW)/2^k P; missing coefficients are exactly zero",
        "global_basis": GLOBAL_BASIS,
        "complete_maps": stages,
        "image": {"form": "K_full = B_Spin tensor I_port,T + I_Spin tensor B_port tensor I_T + I_Spin,port tensor A_T",
                  "classical_form": "K_full = B_old + d P(T=1), B_old=B_Spin+B_port+c I",
                  "coherent_exact_dimension": 22, "classical_exact_dimension": 20,
                  "coherent_rank_certificate": coherent, "classical_rank_certificate": classical,
                  "source": "D E(work)=Tr(B_Spin D rho_Spin)+Tr(B_port D rho_port)+d D pi for fixed marks on the canonical word",
                  "repetition": "repeating the same suffix adds M times each spectator marginal source as well as M d D pi; no 1/M suppression of new work",
                  "moving_marks_or_words": "additional derivatives of the maps, marks and independently varied gate/birth occurrences remain; this fixed-word table does not solve them"},
        "sharp_effect_budget": {"each_mark_constraint": "0<=W_s<=I independently, no negative price required",
                                "T_source_range": ["-(9-4p)", "9-4p"],
                                "radius_exact": coefficient_text(radii),
                                "radius_decimal": format(scalar_value(radii), ".16g"),
                                "attainment": "sum the verified positive (or negative) spectral effects in the 34 rows"},
        "complete_positive_ledgers": examples,
        "actual_readout_work_witnesses": [
            {"stage": 7, "extra_local_mark": "P(D=1)=(II-IZ)/2 on (T,D)",
             "complete_work_operator": "34 I + p^2 I + p^3 P(T=1)",
             "old_classical_T_source": "p^3 Dpi",
             "all_other_stage_marks": "I; the indicated effect is added to the identity mark at stage 7"},
            {"stage": 7, "extra_local_mark": "P(T=1)=(II-ZI)/2 on (T,D)",
             "complete_work_operator": "34 I + P(T=1)",
             "old_classical_T_source": "Dpi",
             "all_other_stage_marks": "I; the indicated effect is added to the identity mark at stage 7"},
        ],
        "spectator_positive_ledgers": [
            {"marked_stage": 14, "extra_local_mark": "P(Spin0=0) = (III+IZI)/2 on (port,Spin0,Spin1)",
             "other_stage_marks": "I at all 34 stages, with the displayed projector added at stage 14",
             "complete_work_operator": "34 I + P(Spin0=0)",
             "repeated_work_source": "M D Pr(Spin0=0), for M copies with this retained old marginal"},
            {"marked_stage": 11, "extra_local_mark": "P(port=0) = (II+ZI)/2 on (port,C)",
             "other_stage_marks": "I at all 34 stages, with the displayed projector added at stage 11",
             "complete_work_operator": "34 I + P(old dirty port=0)",
             "repeated_work_source": "M D Pr(old dirty port=0), for M copies with this retained old marginal"},
        ],
        "known_terminal_ledger": {"mean_lengths_T0_T1": expected_lengths,
                                  "CQ_entropy_increment_phi": "1+p^2",
                                  "full_registered_net": "4+pi",
                                  "old_hypothesis_info": "zero incremental information conditional on retained T; its difference from CQ is constant on fixed canonical-noise pi variations",
                                  "separation": "all stage marks are additional nonparsed work, so the terminal charge is counted exactly once"},
        "verification": "pinned native matrices; all 604 local Hermitian basis insertions; exact pre/post pullbacks and reconstruction; all input columns; verified sharp spectral projectors; modular nonzero minors plus exact support upper bounds",
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
