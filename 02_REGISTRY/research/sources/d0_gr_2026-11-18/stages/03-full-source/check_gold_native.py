"""Exact all-column replay of two golden gate gadgets and their capped records.

Run with optional first argument pointing to the pinned native_execution.py.
The unitary grammar and the subsequent measured CQ protocol are checked separately.
"""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "primary" / "native_execution.py"
owner = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
digest = hashlib.sha256(owner.read_bytes()).hexdigest()
assert digest == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = importlib.util.spec_from_file_location("gold_primary", owner)
native = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = native
spec.loader.exec_module(native)
F = native.GOLDEN_FIELD
a, p = native.A, native.P
v, w = sp.Matrix([a, p]), sp.Matrix([-p, a])
e0, e1 = sp.eye(2)[:, 0], sp.eye(2)[:, 1]
identity = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
J = sp.Matrix([[0, -1], [1, 0]])
Z = sp.diag(1, -1)
plus, minus = (identity + X) / 2, (identity - X) / 2
G, Gminus = native.G_LOCAL, native.G_LOCAL.T
A, probe, data, s1, s2 = range(5)
source = native.Gate("SourceI", (A, s1, s2))
kron = sp.kronecker_product


def dm(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(F).to_sparse()


def eq(left, right):
    assert dm(left) == dm(right)


def execution(gates):
    return native.Execution(5, (), (), tuple(gates), native.G_CX_SOURCE_I, A, (s1, s2))


def full(gates):
    return native.word_matrix(execution(gates), max_qubits=5, max_expanded_stages=200)


def inv(gates):
    return native.inverse_word(execution(gates), max_qubits=5, max_expanded_stages=200)


def counts(gates):
    return dict(sorted(Counter(gate.op for gate in gates).items()))


def cx(control, target):
    return native.Gate("CX", (control, target))


def swap(i, j):
    return (cx(i, j), cx(j, i), cx(i, j))


def b_insertion(vector):
    return kron(identity, vector, sp.eye(8))


cz = (source,) + swap(A, data) + (source,) + swap(A, data)
cz += (cx(data, A),) + (source,) * 3 + (cx(data, A),)
W = cz + (cx(A, data),)
Wb = W + (cx(A, probe),)
CZlogical = kron(e0 * e0.T, sp.eye(16)) + kron(e1 * e1.T, identity, Z, sp.eye(4))
Wlogical = kron(e0 * e0.T, sp.eye(16)) + kron(e1 * e1.T, identity, J, sp.eye(4))
assert full(cz) == CZlogical and full(W) == Wlogical
U = full(Wb)
target = kron(e0 * e0.T, sp.eye(16)) + kron(e1 * e1.T, X, J, sp.eye(4))
assert U == target
assert full(inv(Wb)) == U.T and full(inv(W)) == Wlogical.T
assert counts(Wb) == {"CX": 10, "SourceI": 5}
assert counts(inv(Wb)) == {"CX": 10, "SourceI": 15}
assert counts(W) == {"CX": 9, "SourceI": 5}
assert counts(inv(W)) == {"CX": 9, "SourceI": 15}
input_ab = kron(v, e1, sp.eye(8))
output_ab = kron(v, v, sp.eye(8))
operator_good = output_ab.T * U * input_ab
eq(operator_good, a * p * kron(G, sp.eye(4)))
eq(operator_good.T * operator_good, p**3 * sp.eye(8))

# The TWO probes use the same address successively, each on fresh work.
# A remains the only source port: reaching the probe costs two literal SWAPs.
sensor1 = (cx(probe, A),)
route = swap(A, probe)
sensor2 = sensor1 + route + (source,) * 2 + route
U1, U2 = full(sensor1), full(sensor2)
assert U2 == kron(identity, Z, sp.eye(8)) * U1


def probe_kraus(word, outcome):
    return b_insertion(outcome).T * word * b_insertion(v)


k1w, k1v = probe_kraus(U1, w), probe_kraus(U1, v)
k2w, k2v = probe_kraus(U2, w), probe_kraus(U2, v)
d = p - p**2
eq(k1w, -2*a*p*kron(minus, sp.eye(8)))
eq(k2w, -2*a*p*kron(plus, sp.eye(8)))
eq(k1v, kron(plus + d*minus, sp.eye(8)))
eq(k2v, kron(d*plus + minus, sp.eye(8)))
eq(k2w*k1v, -2*a*p*kron(plus, sp.eye(8)))
eq(k2v*k1v, d*sp.eye(16))
eq((k1w.T*k1w + (k2w*k1v).T*(k2w*k1v) + (k2v*k1v).T*(k2v*k1v)),
   sp.eye(16))
eq(sp.Matrix([d, 4*a**2*p**2]), sp.Matrix([p**3, 1-p**6]))

# Golden-basis measurements require an actual computational read. Its two
# unitary rotations in a retained Lüders read are available at either address.
rotation_checks = {}
for axis in (A, probe):
    gate = (native.Gate("G", (axis,)),)
    inverse_g = inv(gate)
    actual_g = kron(sp.eye(2**axis), G, sp.eye(2**(4-axis)))
    eq(full(inverse_g), actual_g.T)
    rotation_checks[str(axis)] = counts(inverse_g)

# Native factorization above places the identity on every Spin basis vector.
# Work now on exact A x DATA blocks. The unnormalized column [1, ±1] avoids
# adjoining sqrt(2) to the primary number field; its norm squared is two.
Uw = dm(sp.diag(identity, J))
Pv, Pw = dm(kron(v*v.T, identity)), dm(kron(w*w.T, identity))
Pm, Pp = dm(kron(minus, identity)), dm(kron(plus, identity))
start = dm(kron(v, identity))
ok = dm(kron(e0+e1, G))
bad = dm(kron(e0-e1, Gminus))
I2 = dm(identity)


def identify(op, template):
    # A full Kraus-map equality checks polar action, including relative signs.
    key, base = next((k, b) for k, b in template.to_dok().items() if b != F.zero)
    coefficient = op.to_dok().get(key, F.zero) / base
    assert op == template.scalarmul(coefficient)
    probability = (op.transpose() * op).to_dok()[(0, 0)]
    assert op.transpose() * op == I2.scalarmul(probability)
    return probability


def q(num, den=1):
    return F.from_sympy(sp.Rational(num, den))


cap_audits = []
for cap in range(6):
    ok_leaves = [Pp*Uw*start]
    pending = [Pm*Uw*start]
    signs_read = 1
    for cycle in range(cap):
        following = []
        for prior in pending:
            parent_probability = identify(prior, bad)
            for inner in (Pv, Pw):
                # Keep the double binary history; both v and w continue.
                state = Uw*inner*Uw.transpose()*prior
                positive, negative = Pp*state, Pm*state
                assert identify(positive, ok) == parent_probability*q(1, 4)
                assert identify(negative, bad) == parent_probability*q(1, 4)
                ok_leaves.append(positive)
                following.append(negative)
                signs_read += 1
        pending = following
    successes = sum((identify(op, ok) for op in ok_leaves), F.zero)
    failures = sum((identify(op, bad) for op in pending), F.zero)
    assert successes + failures == F.one
    assert failures == q(1, 2**(cap+1))
    cap_audits.append({"extra_cycles":cap,"success_transcripts":len(ok_leaves),
                       "minus_at_cap_transcripts":len(pending),"binary_tests_in_tree":signs_read,
                       "abort":str(Fraction(1, 2**(cap+1)))})

# Finite X implementation. A pair per residual is a scalar d I; all its
# attempts, actual clicks and cap aborts therefore extend to any reference.
def geometric_success(cap, paircap):
    """Recursively sum all class probabilities for the finite two-cap CP instrument."""
    d2 = q(1) - F.from_sympy(4*a**2*p**2)
    half = q(1, 2)
    pending = F.one
    total = F.zero
    read_abort = F.zero
    for _ in range(cap+1):
        unresolved = pending
        pos = F.zero
        neg = F.zero
        for _ in range(paircap):
            pos += unresolved*(F.one-d2)*half
            neg += unresolved*(F.one-d2)*half
            unresolved *= d2
        total += pos
        read_abort += unresolved
        pending = neg
    assert total + read_abort + pending == F.one
    g = (F.one - d2**paircap)*half
    assert total == sum((g**j for j in range(1, cap+2)), F.zero)
    return {"extra_cycles": cap, "max_probe_pairs_per_X": paircap,
            "raw_read_abort": float(F.to_sympy(read_abort)),
            "minus_at_cap": float(F.to_sympy(pending)),
            "total_abort": float(F.to_sympy(F.one-total))}


report = {"status":"PASS","primary_sha256":digest,"full_hardware_columns":32,
          "arbitrary_data_spin_input_columns":8,
          "full_gadget":{"forward":counts(Wb),"cheap_inverse_expansion":counts(inv(Wb)),
                         "good_compression":"a*p*G tensor I_spin","good_probability":"p^3"},
          "controlled_J":{"forward":counts(W),"inverse_expansion":counts(inv(W))},
          "two_probe_X":{"pair_stage_1":counts(sensor1),"pair_stage_2":counts(sensor2),
                         "minus_click":"-2*a*p*Pminus","plus_click_after_noclick":"-2*a*p*Pplus",
                         "both_noclick":"p^3 I","unresolved_after_L_pairs":"p^(6L)",
                         "mean_pairs_unlimited":"1/(1-p^6)"},
          "golden_basis_inverse_rotations":rotation_checks,
          "no_multi_controlled_gates":True,"native_unitary_gates_used":["CX","SourceI","G"],
          "restoration":{"binary_X":"Pplus/Pminus Lueders","all_ok":"G tensor I_spin",
                         "terminal_minus":"G^T tensor I_spin",
                         "ideal_X_caps":cap_audits,
                         "uncapped_fair_records":{
                             "mean_X_calls":2,"mean_forward_W":2,"mean_inverse_W":1,
                             "mean_intermediate_v_w_tests":1,
                             "mean_total_probes":"(3+p^6)/(1-p^6)",
                             "shannon_entropy_complete_transcript_nats":
                                 "3 ln(2)+2[-ln(1-p^6)-(p^6/(1-p^6))*ln(p^6)]",
                             "meaning":"All clicks, inconclusive pairs, and intermediate v/w outcomes retained; input preparations and external hardware records excluded."},
                         "finite_X_success_formula":"sum_{j=1}^{N+1} ((1-p^(6L))/2)^j",
                         "finite_X_caps":[geometric_success(n,l) for n in (0,1,2,3) for l in (1,2,3)]},
          "scope":"Verified complete unitary columns plus a CQ protocol with external projective readings, fresh probes, recorded branches and conditional repetition. Stage counts omit preparations, readout, archive, irreversible resources, and physical weight assignment. Neither full Cost-Info nor universal admission is derived."}
encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
(HERE / "gold_native_result.json").write_text(encoded)
print(encoded, end="")
