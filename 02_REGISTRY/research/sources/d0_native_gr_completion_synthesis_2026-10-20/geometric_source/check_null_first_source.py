#!/usr/bin/env python3
"""Exact native CAR first-source substitution on the owned Brinkmann null stratum.

Only the new substitution and complete Golden port are checked. The imported
all40 theorem is NOT replayed. Every proof-critical check survives python -O.
"""
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json

import sympy as s

HERE = Path(__file__).resolve().parent
COUNTS = {}


def require(name, condition):
    if not bool(condition):
        raise RuntimeError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1


def zero(name, value):
    if isinstance(value, s.MatrixBase):
        require(name, all(s.cancel(v) == 0 for v in value))
    else:
        require(name, s.cancel(value) == 0)


pins = json.loads((HERE / "INPUTS.json").read_text())
for name, record in pins["inputs"].items():
    data = (HERE / "inputs" / name).read_bytes()
    require("owned_input_pin", hashlib.sha256(data).hexdigest() == record["sha256"])

spec = importlib.util.spec_from_file_location(
    "literal_null_owner", HERE / "inputs/literal_null_all40.py")
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
# Import executes definitions only. In particular theorem() and harmonic()
# from the old owner are not called.
eta = owner.eta
I4 = s.eye(4)
PAIRS = list(itertools.combinations(range(4), 2))
N2, N3 = owner.N2, owner.N3
H, h, nu, x, y = s.symbols("H h nu x y", real=True, nonzero=True)
E = I4.copy()
E[1, 0] = H / 2
V = nu * eta * E.inv().T
detV = V.det()
zero("native_det_on_whole_null_stratum", detV + nu**4)


def wedge(u, v):
    return u * v.T - v * u.T


def elementary(i, j):
    out = s.zeros(4)
    out[i, j] = 1
    return out


LIE = []
for i, j in PAIRS:
    LIE.append((elementary(i, j) - elementary(j, i)) * eta)


def original_density(frame, face, R):
    r, t = face
    u, v = [j for j in range(4) if j not in face]
    return s.LeviCivita(r, t, u, v) * owner.pair(frame, u, v, R)


def base_dual(frame, face):
    # Literal null-owner orientation, not the diagonal-eta sign copied blindly.
    invlegs = eta * frame.inv().T
    r, t = face
    return -wedge(invlegs[:, r], invlegs[:, t]) * eta / invlegs.det()


def R(P):
    return (P - eta * P.T * eta) / 2


def trace_amplitude(B, P):
    # Exact exterior character identity, B is traceless.
    A = I4 + P
    return -s.det(A) * s.trace(B * P * A.inv()) / 8


def amplitude_jet(B, P, dB, dP):
    Ainv = (I4 + P).inv()
    D = (I4 + P).det()
    W = P * Ainv
    return -D * (
        s.trace(dB * W)
        + s.trace(Ainv * dP) * s.trace(B * W)
        + s.trace(B * Ainv * dP * Ainv)
    ) / 8


def geometric_jet(B, P, dB, dP):
    Pi = eta * P.T * eta
    return -s.trace(dB * (P - Pi)) / 4 - s.trace(
        B * (dP + Pi * dP * Pi)) / 4


X = x * N2 + y * N3
Pnull = I4 + X + X * X / 2
zero("common_null_nilpotency", X**3)
zero("common_null_lorentz", Pnull.T * eta * Pnull - eta)
zero("common_null_character", (I4 + Pnull).det() - 16)
zero("common_null_resolvent", (I4 + Pnull).inv() - (I4 / 2 - X / 4))

random_frame = s.Matrix([[2, 1, 0, 1], [0, 2, 1, 0],
                         [1, 0, 2, 1], [0, 1, 0, 2]])
for frame in (h * E, random_frame):
    for face in PAIRS:
        B = base_dual(frame, face)
        for Y in LIE:
            zero("literal_null_pair_sign", original_density(frame, face, Y)
                 + s.trace(B * Y) / 2)

for face in PAIRS:
    r, t = face
    B = base_dual(h * E, face)
    N = wedge(V[:, r], V[:, t]) * eta
    P = Pnull if face in ((0, 2), (0, 3)) else I4
    zero("native_cofactor_identity", B + h**2 * nu**2 * N / detV)
    zero("zero_original_density", original_density(h * E, face, R(P)))
    zero("zero_native_trace_amplitude", trace_amplitude(N, P))
    if face in ((0, 2), (0, 3)):
        expected = h**2 * (N2 if face == (0, 2) else N3)
        zero("actual_curved_face_dual_is_common_null", B - expected)
        zero("common_null_BXX", B * X * X)
        zero("common_null_XBX", X * B * X)
        zero("common_null_XXB", X * X * B)
    # ALL 16 actual independent physical-coframe columns, not delta H alone.
    for i, j in itertools.product(range(4), repeat=2):
        dE = elementary(i, j)
        dV = -nu * eta * E.inv().T * dE.T * E.inv().T
        dd = detV * s.trace(V.inv() * dV)
        dN = (wedge(dV[:, r], V[:, t])
              + wedge(V[:, r], dV[:, t])) * eta
        dB = -h**2 * nu**2 * (dN / detV - N * dd / detV**2)
        da = amplitude_jet(N, P, dN, s.zeros(4))
        dfhat = geometric_jet(B, P, dB, s.zeros(4)) / h**4
        zero("all_16_coframe_first_source_per_face", da - nu**2 * h**2 * dfhat)
        u, v = [a for a in range(4) if a not in face]
        # Independently differentiate the imported owner's literal pair.
        dframe = h * dE
        frame_u, frame_v = h * E, h * E
        frame_u[:, u] = dframe[:, u]
        frame_v[:, v] = dframe[:, v]
        d_literal = s.LeviCivita(r, t, u, v) * (
            owner.pair(frame_u, u, v, R(P))
            + owner.pair(frame_v, u, v, R(P)))
        zero("all_16_literal_pair_derivatives", d_literal / h**4 - dfhat)
    # Full Lorentz tangent at P. Pullback through arbitrary four-edge words
    # therefore includes all 24 link directions and all based incidences.
    for Y in LIE:
        dP = Y * P
        zero("all_6_holonomy_first_sources_per_face",
             amplitude_jet(N, P, s.zeros(4), dP)
             - nu**2 * h**2 * geometric_jet(B, P, s.zeros(4), dP) / h**4)

# A second check uses each of the four original edge occurrences explicitly,
# with inverse-occurrence derivative -W Y, and six ambient Lorentz generators.
ka, kb, la, lb = s.symbols("ka kb la lb", real=True)
Xa, Xb = ka * N2 + kb * N3, la * N2 + lb * N3
Ua = I4 + Xa + Xa**2 / 2
Ub_inv = I4 - Xb + Xb**2 / 2
for face in PAIRS:
    B = base_dual(h * E, face)
    if face == (0, 1):
        words = [Ua, I4, eta * Ua.T * eta, I4]
    elif face in ((0, 2), (0, 3)):
        words = [Ua, I4, Ub_inv, I4]
    else:
        words = [I4, I4, I4, I4]
    P = words[0] * words[1] * words[2] * words[3]
    for position, Y in itertools.product(range(4), LIE):
        derivatives = [s.zeros(4) for _ in range(4)]
        derivatives[position] = (Y * words[position] if position < 2
                                 else -words[position] * Y)
        dP = s.zeros(4)
        for j in range(4):
            term = I4
            for k in range(4):
                term = term * (derivatives[k] if k == j else words[k])
            dP += term
        zero("all_24_original_edge_occurrences_per_face",
             amplitude_jet(B, P, s.zeros(4), dP)
             - geometric_jet(B, P, s.zeros(4), dP))

# Full native CAR16 basis: the original predecessor order is (0,2,3,1).
ORDER = (0, 2, 3, 1)
creators = []
for i in range(4):
    C = s.zeros(16)
    pred = ORDER[:ORDER.index(i)]
    for mask in range(16):
        if not mask & (1 << i):
            C[mask | (1 << i), mask] = (-1)**sum((mask >> j) & 1 for j in pred)
    creators.append(C)


def creation(v):
    return sum((v[j] * creators[j] for j in range(4)), s.zeros(16))


def dgamma(B):
    return sum((B[i, j] * creators[i] * creators[j].T
                for i, j in itertools.product(range(4), repeat=2)), s.zeros(16))


def exterior(A):
    out = s.zeros(16)
    for i, j in itertools.product(range(16), repeat=2):
        ri = [a for a in ORDER if i & (1 << a)]
        rj = [a for a in ORDER if j & (1 << a)]
        if len(ri) == len(rj):
            out[i, j] = A.extract(ri, rj).det() if ri else 1
    return out


P16, eta16 = exterior(Pnull), exterior(eta)
zero("native_full16_metric_involution", eta16.T * eta16 - s.eye(16))
for Y in LIE:
    zero("native_full16_exterior_trace", -s.trace(dgamma(Y) * P16) / 8
         - trace_amplitude(Y, Pnull))
for r, t in PAIRS:
    cr, ct = creation(V[:, r]), creation(V[:, t])
    polynomial = cr * eta16 * ct.T * eta16 - ct * eta16 * cr.T * eta16
    zero("native_creation_polynomial_full16", polynomial
         - dgamma(wedge(V[:, r], V[:, t]) * eta))

# Matter is the already-owned real CAR Clifford-square operand, not a new q.
z = s.symbols("z0:4", real=True)
zv = s.Matrix(z)
clifford = creation(zv) + creation(eta * zv).T
zero("owned_matter_clifford_square_all16",
     clifford * clifford - (zv.T * eta * zv)[0] * s.eye(16))

# Coherent full Pauli scalarization: exact group identity on every matrix unit.
# The complete control/work outputs are not measured or discarded in this sum.
for r, t in itertools.product(range(16), repeat=2):
    accum = {}
    for a, b in itertools.product(range(16), repeat=2):
        key = (r ^ a, t ^ a)
        sign = (-1)**((b & (r ^ t)).bit_count())
        accum[key] = accum.get(key, 0) + sign
    target = {(j, j): 16 for j in range(16)} if r == t else {}
    accum = {k: v for k, v in accum.items() if v}
    require("coherent_scalarizer_all256_matrix_units", accum == target)

# Literal Golden reflection R=[[p,sqrt(p)],[sqrt(p),-p]], complete port1.
# K1=p*sqrt(p)*(I-U). Therefore E1=p^3(2I-U-U*) and the identity
# uses ALL work-output columns, not only the good amplitude.
p, sig, A = s.symbols("p sigma A", real=True)


def golden_reduce(expr):
    return s.rem(s.Poly(s.expand(expr), p), s.Poly(p**2 + p - 1, p)).as_expr()


zero("complete_golden_port_normalization", golden_reduce(p**4 + p**2 + 2 * p**3 - 1))
signal = -sig * A / 2
q1 = 2 * p**3 * (1 - signal)
zero("literal_0_10_reporter_cost", 1 + q1 - (1 + 2*p**3 + sig*p**3*A))
zero("literal_reporter_first_source", s.diff(1 + q1, A) - sig*p**3)
D_h, sumA, nu0, h0 = s.symbols("D_h sumA nu0 h0", positive=True)
global_t = -8*sig*sumA/D_h
one_global_cost = 1 + 2*p**3*(1-global_t)
repeated_cost = D_h/16 * one_global_cost
zero("full_address_rank_and_repetition",
     repeated_cost - (D_h/16*(1+2*p**3) + sig*p**3*sumA))
zero("full_address_fhat_coefficient",
     s.diff(repeated_cost, sumA)*nu0**2*h0**2 - p**3*sig*nu0**2*h0**2)
for t0, t1 in ((s.Rational(0), s.Rational(1)),
               (s.Rational(3, 5), s.Rational(4, 5))):
    U = s.Matrix([[t0, -t1], [t1, t0]])
    I2 = s.eye(2)
    zero("complete_workspace_unitary_fixture", U.T * U - I2)
    K0 = p**2 * I2 + p * U
    # The sqrt(p) in K1 cancels in its positive effect.
    E1 = p**3 * (I2 - U).T * (I2 - U)
    zero("complete_workspace_port_effect", E1 - p**3 * (2*I2 - U - U.T))
    zero("complete_workspace_all_outputs_normalized",
         (K0.T*K0 + E1 - I2).applyfunc(golden_reduce))
    zero("complete_workspace_clean_compression", E1[0, 0] - 2*p**3*(1-t0))
    if t0 == 0:
        require("dropping_work_would_change_port_price", E1[0, 0] != p**3*(1-t0)**2)

# Hostile control: Choi's constant null marked probability is NOT a scalar
# input effect. A legal LEFT-unitary prep tangent preserves old RIGHT Gram.
r2 = x*x + y*y
zero("null_choi_norm_formula", (I4 + Pnull.T * Pnull).det() - 16*(1+r2/4)**2)
skew = (P16.T - P16) / 2
zero("canonical_choi_prep_tangent",
     2*s.trace(P16*skew)/16 - ((1+r2/4)**2 - 1))

# Scalar compression does not justify varying a task-fixed clean-work input.
c = s.symbols("c", positive=True)
leak = s.sqrt(c*(1-c))
effect = s.Matrix([[c, leak], [leak, 1-c]])
zero("interior_scalar_compression_projector", effect**2 - effect)
zero("interior_work_leakage", effect[1, 0]**2 - c*(1-c))

result = {
    "status": "PASS",
    "source_commit": pins["source_commit"],
    "checks": COUNTS,
    "exact_native_first_source": "d A_nu = nu^2 h^2 d fhat on all null-family ambient coframe/link directions",
    "literal_reporter_source": "d mean_length(0/10) = p^3 sigma nu^2 h^2 d fhat",
    "geometric_rows_consumed": "owned all40 theorem; not rerun",
    "history_handling": "all control/query/work outcomes retained; complete final-port marginal",
    "source_scope": "signal and literal reused reporter component; full Book Cost-Info remains a separate residual",
    "preparation_scope": "original normalized input/oldRIGHT variations on task-fixed clean-work cut",
    "physical_selection_proved": False,
    "exact_finite_Golden_compilation_proved": False,
    "GR_closed": False,
}
print(json.dumps(result, indent=2, sort_keys=True))
