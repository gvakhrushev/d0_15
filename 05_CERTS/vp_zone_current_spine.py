#!/usr/bin/env python3
"""vp_zone_current_spine.py - D0-V15-ZONE-CURRENT-SPINE-001 certificate (exact rational LA)

CLAIM (THE, derived from frozen D0): on the 3-dim row space ran(A) of the frozen scene K(9,11,13),
with D_W = diag(24,22,20) and the part-quotient adjacency A_W = [[0,11,13],[9,0,13],[9,11,0]], the zone
current J_zone = i*[D_W,A_W] has:
  * commutator comm = [D_W,A_W] = [[0,22,52],[-18,0,26],[-36,-22,0]];
  * annihilating polynomial comm^3 = -2840*comm  (char.poly of [D,A] is t^3 + 2840 t),
    so J_zone = i*comm satisfies J^3 = 2840*J and spec(J) = {0, +-2*sqrt(710)} (2840 = 4*710);
  * a genuine orthogonal spectral split: P_act = (-1/2840)*comm^2, P0 = I + (1/2840)*comm^2 are
    idempotent, complementary (P0+P_act=I), orthogonal (P0*P_act=0), with tr P_act = 2 (active),
    tr P0 = 1 (neutral); the integer vector (143,-234,99) spans ker(comm) (neutral sector).

All values are COMPUTED from the frozen D_W, A_W (no posited 2840/sqrt710). Exact Fraction arithmetic.

FIREWALL: this is the spectral decomposition of the frozen commutator on the 3-dim row space; it is NOT a
physical neutral-current / neutrino-count / charge / generation-mixing claim.
"""
from fractions import Fraction as F

def mat(rows):
    return [[F(x) for x in r] for r in rows]

def matmul(X, Y):
    n, m, p = len(X), len(Y), len(Y[0])
    return [[sum(X[i][k] * Y[k][j] for k in range(m)) for j in range(p)] for i in range(n)]

def scal(c, X):
    return [[F(c) * X[i][j] for j in range(len(X[0]))] for i in range(len(X))]

def add(X, Y):
    return [[X[i][j] + Y[i][j] for j in range(len(X[0]))] for i in range(len(X))]

def sub(X, Y):
    return [[X[i][j] - Y[i][j] for j in range(len(X[0]))] for i in range(len(X))]

def eq(X, Y):
    return all(X[i][j] == Y[i][j] for i in range(len(X)) for j in range(len(X[0])))

def trace(X):
    return sum(X[i][i] for i in range(len(X)))

def matvec(X, v):
    return [sum(X[i][j] * v[j] for j in range(len(v))) for i in range(len(X))]

I3 = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
Z3 = mat([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

# --- frozen inputs (degrees 24,22,20 and part sizes 9,11,13 -> part-quotient adjacency) ---
DW = mat([[24, 0, 0], [0, 22, 0], [0, 0, 20]])
AW = mat([[0, 11, 13], [9, 0, 13], [9, 11, 0]])

comm = sub(matmul(DW, AW), matmul(AW, DW))   # [D_W, A_W]
assert eq(comm, mat([[0, 22, 52], [-18, 0, 26], [-36, -22, 0]])), comm
print("[1] comm = [D_W,A_W] = [[0,22,52],[-18,0,26],[-36,-22,0]]  PASS")

# annihilating polynomial: comm^3 = -2840*comm  (computed coefficient, not posited)
comm3 = matmul(matmul(comm, comm), comm)
assert eq(comm3, scal(-2840, comm)), "annihilator failed"
print("[2] comm^3 = -2840*comm  => spec(J=i*comm) = {0, +-2*sqrt(710)}, 2840=4*710  PASS")

# --- canonical part-size inner product G = diag(9,11,13) (frozen equitable-partition cell sizes) ---
# An operator T is G-self-adjoint iff G*T is symmetric. This is the Hermiticity correction that
# upgrades the split from oblique (CONDITIONAL) to a genuine G-orthogonal spectral split (THE).
G = mat([[9, 0, 0], [0, 11, 0], [0, 0, 13]])
def transpose(X): return [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
def is_sym(X): return eq(X, transpose(X))
def is_anti(X): return eq(X, scal(-1, transpose(X)))
assert is_sym(matmul(G, DW)), "G*DW not symmetric"     # D_W G-self-adjoint
assert is_sym(matmul(G, AW)), "G*AW not symmetric"     # A_W G-self-adjoint (entries n_i n_j)
assert is_anti(matmul(G, comm)), "G*comm not antisymmetric"  # comm G-skew -> J=i*comm G-Hermitian
print("[3] canonical G=diag(9,11,13): G*D_W, G*A_W symmetric; G*[D,A] antisymmetric => J G-Hermitian  PASS")

# spectral projectors (now genuine G-orthogonal, not oblique)
comm2 = matmul(comm, comm)
Pact = scal(F(-1, 2840), comm2)
P0 = add(I3, scal(F(1, 2840), comm2))
assert eq(matmul(Pact, Pact), Pact), "Pact not idempotent"
assert eq(matmul(P0, P0), P0), "P0 not idempotent"
assert eq(add(P0, Pact), I3), "P0+Pact != I"
assert eq(matmul(P0, Pact), Z3), "P0*Pact != 0"
assert is_sym(matmul(G, Pact)), "G*Pact not symmetric (Pact not G-orthogonal)"
assert is_sym(matmul(G, P0)), "G*P0 not symmetric (P0 not G-orthogonal)"
assert trace(Pact) == 2, trace(Pact)
assert trace(P0) == 1, trace(P0)
print("[4] P_act,P0 idempotent; P0+P_act=I; G-ORTHOGONAL (G*P sym); tr P_act=2 (active), tr P0=1 (neutral)  PASS")

# neutral kernel vector
vneu = [143, -234, 99]
assert matvec(comm, vneu) == [0, 0, 0], matvec(comm, vneu)
assert matvec(Pact, vneu) == [0, 0, 0]
print("[5] neutral vector (143,-234,99) in ker(comm), killed by P_act  PASS")

# --- FAIL controls (must trigger; guards against a vacuous cert) ---
def must_fail(fn, label):
    try:
        fn()
    except AssertionError:
        print(f"[FAIL-CONTROL] {label}: correctly rejected  PASS")
        return
    raise SystemExit(f"FAIL-CONTROL DID NOT TRIGGER: {label}")

# wrong annihilator coefficient (2839 instead of 2840) must be rejected
def _bad_coeff():
    assert eq(comm3, scal(-2839, comm))
must_fail(_bad_coeff, "FAIL_WRONG_ANNIHILATOR_COEFF")

# a symmetric A_W (would make comm symmetric -> different spectrum) must change comm
def _bad_symmetric_quotient():
    AWsym = mat([[0, 11, 13], [11, 0, 13], [13, 13, 0]])
    bad = sub(matmul(DW, AWsym), matmul(AWsym, DW))
    assert eq(bad, comm)
must_fail(_bad_symmetric_quotient, "FAIL_SYMMETRIZED_QUOTIENT_CHANGES_COMM")

# a non-neutral vector must NOT be in the kernel
def _bad_kernel_vec():
    assert matvec(comm, [1, 0, 0]) == [0, 0, 0]
must_fail(_bad_kernel_vec, "FAIL_NONNEUTRAL_IN_KERNEL")

# the CANONICAL weight is necessary: in the NAIVE Euclidean inner product (G=I) the generator is NOT
# G-Hermitian (comm is not skew), which is exactly why the naive split is oblique (CONDITIONAL, not THE).
def _naive_euclidean_is_hermitian():
    Gid = I3
    assert is_anti(matmul(Gid, comm))   # comm antisymmetric under G=I ?  -> it is NOT
must_fail(_naive_euclidean_is_hermitian, "FAIL_NAIVE_EUCLIDEAN_NOT_HERMITIAN")

print("\n[STATUS] THE: zone generator J=i[D,A] is G-Hermitian in the canonical part-size inner product")
print("         G=diag(9,11,13); spec {0,+-2sqrt710}; genuine G-orthogonal neutral(1)+active(2) split.")
print("[CERT-CLOSED] PASS_ZONE_CURRENT_SPINE")
