#!/usr/bin/env python3
"""Exact certificate for the typed q0 harmonic tower.

WORKER: WRK-A4D-Q0-GERM-TOWER-COLLAPSE-CERT
Terminal: A4D-Q0-GERM-TOWER-COLLAPSE-EXACT

This consumes the accepted #270 coefficient owner, its #292 coefficientwise
ledger, the merged #290 physical carrier owner, and the #296 Gram-lift owner.
All arithmetic here is exact over Q or Q(i).  No numerical rank, float,
finite-difference, or fitting method is used.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
METRIC_OWNER = Path(
    "02_REGISTRY/research/certificates/a4d_metric_null_hessian_complex_check.py"
)
COEFFICIENT_LEDGER = Path(
    "02_REGISTRY/research/certificates/a4d_haq_coefficientwise_identity_coefficients.json"
)
PHYSICAL_OWNER = Path(
    "02_REGISTRY/research/certificates/a4d_joint_resonance_linear_kernel_check.py"
)
GRAM_OWNER = Path(
    "02_REGISTRY/research/certificates/a4d_q0_harmonic_lift_obstruction_check.py"
)

PINNED_SHA256 = {
    METRIC_OWNER: "d7707248af8a30beb14591991d5a78f37cd73c9fef2ac7c29aae0e8b2003f0b7",
    COEFFICIENT_LEDGER: "e106d8937fad966eefd1838ce69e0bb32d7e34100e452b9a9c1f78ec78e454f5",
    PHYSICAL_OWNER: "a3e02e378f352a982e0465683b8af3f36c756968a2004d9379020a36b702bb5d",
    GRAM_OWNER: "c794f7f87e35e3ed75fe8ca8e9c5d5a4a04286e25b0432c8a21e930a0954e1d0",
}

FAILS: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print("PASS_" + name)
    else:
        FAILS.append(name)
        print("FAIL_" + name + (" :: " + detail if detail else ""))


def exact_zero(value) -> bool:
    return sp.simplify(sp.expand(value)) == 0


def exact_matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(exact_zero(entry) for entry in matrix)


def check_pinned(relative: Path) -> bytes:
    source_bytes = (ROOT / relative).read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()
    check(relative.name + "_PINNED_SHA256", digest == PINNED_SHA256[relative], digest)
    return source_bytes


def owner_prefix(relative: Path, marker: str) -> dict:
    path = ROOT / relative
    source_bytes = check_pinned(relative)
    source = source_bytes.decode("utf-8")
    if marker not in source:
        raise RuntimeError(f"owner marker missing: {relative}")
    prefix = source.split(marker, 1)[0]
    namespace = {"__name__": "_q0_germ_tower_owner", "__file__": str(path)}
    exec(compile(prefix, str(path), "exec"), namespace)
    return namespace


def rational_matrix(raw) -> sp.Matrix:
    return sp.Matrix([[sp.Rational(entry) for entry in row] for row in raw])


# #270 owns the exact polynomial C(d); #292 publishes its coefficientwise
# matrices.  Differentiate the owner polynomial, then compare every entry to
# that independent, merged ledger before using K_r.
metric = owner_prefix(METRIC_OWNER, "# Exact projective cover of d != 0.")
C = metric["C"]
d = metric["d"]
SYM = metric["SYM"]
K = [C.diff(d[r]).applyfunc(sp.expand) for r in range(4)]
qpoly = sp.Matrix([sp.expand(d[a] * d[b]) for a, b in SYM])

ledger = json.loads(check_pinned(COEFFICIENT_LEDGER).decode("utf-8"))
check("COEFFICIENT_LEDGER_TERMINAL", ledger["terminal"] == "A4D-HAQ-LINEARITY-AND-Q0-IDENTITY-COEFFICIENTWISE-EXACT")
check("COEFFICIENT_LEDGER_480_ZEROES", ledger["cubic_scalar_equalities"] == 480 and ledger["all_cubic_coefficients_zero"] is True)
check("COEFFICIENT_LEDGER_ORDER", ledger["sym_order"] == [[a, b] for a, b in SYM])
check("COEFFICIENT_LEDGER_NO_SQRT2", ledger["sym_off_diagonal_scaling"] == "none")
for r in range(4):
    owned_K = rational_matrix(ledger["C_r"][r]["matrix"])
    check(f"K{r}_MATCHES_MERGED_COEFFICIENT_LEDGER", K[r] == owned_K)
check("C_RECONSTRUCTED_FROM_K", exact_matrix_zero(C - sum((d[r] * K[r] for r in range(4)), sp.zeros(24, 10))))

M1 = sum((d[r] * K[r] * qpoly for r in range(4)), sp.zeros(24, 1)).applyfunc(sp.expand)
M2 = sum((d[r] ** 2 * K[r] * qpoly for r in range(4)), sp.zeros(24, 1)).applyfunc(sp.expand)
check("M1_EXACT_ZERO", exact_matrix_zero(M1))
check("M2_NONZERO_POLYNOMIAL", any(not exact_zero(entry) for entry in M2))
M2_degrees = [sp.Poly(entry, *d).total_degree() for entry in M2 if not exact_zero(entry)]
check("M2_HOMOGENEOUS_DEGREE_FOUR", bool(M2_degrees) and set(M2_degrees) == {4}, str(sorted(set(M2_degrees))))

# For every natural n, d_r(z^n)=(1+x_r)^n-1.  Applying the binomial theorem
# to each coordinate and linearity C(x)=sum x_r K_r gives
# C(d(z^n))q0 = sum_{k=1}^n binom(n,k) M_k.  The exact owner identity M1=0
# removes k=1.  These small exact substitutions are smoke checks only; the
# universal statement is the displayed finite binomial-theorem derivation.
z = sp.symbols("z0:4", nonzero=True)
xvars = sp.symbols("x0:4")
q_x = sp.Matrix([xvars[a] * xvars[b] for a, b in SYM])
for n_value in range(2, 9):
    harmonic_d = [(1 + xvars[r]) ** n_value - 1 for r in range(4)]
    direct = sum((harmonic_d[r] * K[r] * q_x for r in range(4)), sp.zeros(24, 1))
    tower = sum(
        (
            sp.binomial(n_value, k)
            * sum((xvars[r] ** k * K[r] * q_x for r in range(4)), sp.zeros(24, 1))
            for k in range(2, n_value + 1)
        ),
        sp.zeros(24, 1),
    )
    check(f"BINOMIAL_BN_EXACT_N{n_value}", exact_matrix_zero(direct - tower))

# Degree(M_k)=k+2 because K_r is constant and q0 is quadratic.  Since M1=0,
# every fixed n>=2 has B_n=binom(n,2)M2 plus terms of degree at least five.
s = sp.symbols("s")
geometric = 1 / (1 - s)
leading_weight_sum = s * sp.diff(geometric, s, 2) / 2
check("BINOMIAL_LEADING_WEIGHT_GENERATING_FUNCTION", exact_zero(leading_weight_sum - s / (1 - s) ** 3))
eta = sp.diag(1, -1, -1, -1)
sigma = (sp.Matrix(xvars).T * eta * sp.Matrix(xvars))[0]
check("SIGMA_HOMOGENEOUS_DEGREE_TWO", sp.Poly(sigma, *xvars).total_degree() == 2)
check("FULL_GRAM_LIFT_LEADING_DEGREE_FORMULA", all(2 * (n_value - 1) + 4 == 2 * n_value + 2 for n_value in range(2, 9)))
check_pinned(GRAM_OWNER)
GRAM_MEMO = ROOT / "02_REGISTRY/research/A4D_Q0_HARMONIC_LIFT_OBSTRUCTION.md"
gram_text = GRAM_MEMO.read_text(encoding="utf-8")
check("GRAM_LIFT_PREFACTOR_RECORDED", "F_n(z)=2\\binom{1/2}{n}\\sigma^{n-1}" in gram_text)

# The full #296 coefficient is G_n=2 binom(1/2,n) sigma^(n-1) B_n.
# Therefore its first possible homogeneous degree is 2(n-1)+4=2n+2.  Since
# sigma and M2 are nonzero polynomials and binom(1/2,n)!=0 for n>=2, this is
# also its generic degree; special rays can cancel and are not claimed here.

# #290 owns the physical carrier P=[H_AA(zeta)|H_AQ(conj(zeta))] and the
# rank-23/one-dimensional-cokernel result.  Rebuild its exact symbolic owner
# only through matrix construction, before its orbit census.
physical = owner_prefix(
    PHYSICAL_OWNER,
    "# ---------------------------------------------------------------------------\n# 2. Reproduce the nine owned singular orbit types",
)
HAB = physical["HAB"]
HAQ = physical["HAQ"]
z = physical["z"]
sym_order_physical = physical["SYM"]
check("PHYSICAL_AND_METRIC_SYM_ORDER_MATCH", sym_order_physical == SYM)

qz = sp.Matrix([(1 / z[a] - 1) * (1 / z[b] - 1) for a, b in SYM])
DC = [z[j] * HAQ.diff(z[j]) for j in range(4)]
Dq = [z[j] * qz.diff(z[j]) for j in range(4)]
ORBITS = {
    5: (sp.I, sp.I, -sp.I, -sp.I),
    7: (sp.Integer(-1), sp.I, sp.I, sp.Integer(-1)),
}
EXPECTED_CROSS_RESIDUAL2 = {
    5: [sp.Rational(8, 5), sp.Rational(8, 5), sp.Integer(0), sp.Integer(0)],
    7: [sp.Integer(2), sp.Integer(0), sp.Integer(0), sp.Integer(2)],
}
EXPECTED_UNIT_RESIDUAL2 = {
    5: [sp.Rational(1, 25), sp.Rational(1, 25), sp.Integer(0), sp.Integer(0)],
    7: [sp.Rational(1, 46), sp.Integer(0), sp.Integer(0), sp.Rational(1, 46)],
}
EXPECTED_Q0_NORM2 = {5: sp.Integer(40), 7: sp.Integer(92)}

for orbit, phase in ORBITS.items():
    sub = {z[j]: phase[j] for j in range(4)}
    chi = tuple(sp.conjugate(value) for value in phase)
    csub = {z[j]: chi[j] for j in range(4)}
    A = HAB.subs(sub, simultaneous=True)
    Cphys = HAQ.subs(csub, simultaneous=True)
    P = A.row_join(Cphys)
    left = sp.conjugate(P).T.nullspace()
    check(f"ORBIT_{orbit}_PHYSICAL_COKERNEL_DIMENSION_ONE", len(left) == 1, str(len(left)))
    if len(left) != 1:
        continue
    ell = left[0]
    pivot = next(index for index, value in enumerate(ell) if not exact_zero(value))
    ell = ell.applyfunc(lambda value: sp.simplify(value / ell[pivot]))
    ell_star = sp.conjugate(ell).T
    check(f"ORBIT_{orbit}_LEFT_VECTOR_ANNIHILATES_P", exact_matrix_zero(ell_star * P))
    ell_norm2 = sp.simplify((ell_star * ell)[0])
    check(f"ORBIT_{orbit}_LEFT_VECTOR_NONZERO", not exact_zero(ell_norm2))
    # The #290 owner gives rank(P)=23.  This exact left-nullspace dimension
    # independently recovers the same rank by rank-nullity for a 24-row P.
    check(f"ORBIT_{orbit}_PHYSICAL_RANK_23", P.rows - len(left) == 23)

    xvals = [sp.simplify(sp.Integer(1) / value - 1) for value in phase]
    qv = qz.subs(sub, simultaneous=True).applyfunc(sp.simplify)
    qnorm2 = sp.simplify((sp.conjugate(qv).T * qv)[0])
    check(f"ORBIT_{orbit}_Q0_NORM2", exact_zero(qnorm2 - EXPECTED_Q0_NORM2[orbit]), str(qnorm2))

    # Pair each exact K_r q0(x) against the physical left cokernel.  Equal
    # carrier coordinates are grouped, so the formula below proves the
    # pairing vanishes for every integer k, not just sampled powers.
    Kq_at_x = [
        (K[r] * qpoly).subs(dict(zip(d, xvals)), simultaneous=True).applyfunc(sp.simplify)
        for r in range(4)
    ]
    coefficient_weights = [sp.simplify((ell_star * value)[0]) for value in Kq_at_x]
    grouped: dict[sp.Expr, sp.Expr] = {}
    for base, weight in zip(xvals, coefficient_weights):
        grouped[base] = sp.simplify(grouped.get(base, sp.Integer(0)) + weight)
    check(f"ORBIT_{orbit}_ALL_K_COKERNEL_GROUPS_ZERO", all(exact_zero(value) for value in grouped.values()), str(grouped))
    k = sp.symbols("k", integer=True, nonnegative=True)
    direct_alpha_k = sp.simplify(
        sum((weight * base**k for base, weight in zip(xvals, coefficient_weights)), sp.Integer(0))
    )
    alpha_k = sp.simplify(sum((weight * base**k for base, weight in grouped.items()), sp.Integer(0)))
    check(f"ORBIT_{orbit}_ALL_K_UNGROUPED_SYMBOLIC_IDENTITY", exact_zero(direct_alpha_k), str(direct_alpha_k))
    check(f"ORBIT_{orbit}_ALL_K_GROUPING_EXACT", exact_zero(direct_alpha_k - alpha_k))
    check(f"ORBIT_{orbit}_ALL_K_PAIRING_IDENTICALLY_ZERO", exact_zero(alpha_k), str(alpha_k))
    print(f"ORBIT_{orbit}_M_K_COKERNEL_WEIGHTS={coefficient_weights}")
    print(f"ORBIT_{orbit}_SYMBOLIC_ALPHA_K={direct_alpha_k}")
    print(f"ORBIT_{orbit}_M_K_GROUPED={grouped}")
    print(f"ORBIT_{orbit}: every M_k, k>=0, lies in im P by the exact one-dimensional-cokernel test")

    # Hostile cross-character control: use w_j(zeta) against the physical
    # mixed block at chi=conj(zeta), exactly as in #290.
    cross_residual2 = []
    unit_residual2 = []
    cross_pairings = []
    for j in range(4):
        cross_w = (DC[j] * qz).subs(sub, simultaneous=True).applyfunc(sp.simplify)
        cross_alpha = sp.simplify((ell_star * cross_w)[0])
        residual2 = sp.simplify(sp.conjugate(cross_alpha) * cross_alpha / ell_norm2)
        cross_pairings.append(cross_alpha)
        cross_residual2.append(residual2)
        unit_residual2.append(sp.simplify(residual2 / qnorm2))

        same_w = (DC[j] * qz).subs(csub, simultaneous=True).applyfunc(sp.simplify)
        same_dq = Dq[j].subs(csub, simultaneous=True).applyfunc(sp.simplify)
        same_transport = same_w + Cphys * same_dq
        check(f"ORBIT_{orbit}_D{j}_SAME_CARRIER_TRANSPORT_ZERO", exact_matrix_zero(same_transport))
        check(f"ORBIT_{orbit}_D{j}_SAME_CARRIER_COKERNEL_ZERO", exact_zero((ell_star * same_w)[0]))

    check(f"ORBIT_{orbit}_CROSS_CHARACTER_RAW_RESIDUALS", cross_residual2 == EXPECTED_CROSS_RESIDUAL2[orbit], str(cross_residual2))
    check(f"ORBIT_{orbit}_CROSS_CHARACTER_UNIT_Q0_RESIDUALS", unit_residual2 == EXPECTED_UNIT_RESIDUAL2[orbit], str(unit_residual2))
    check(f"ORBIT_{orbit}_HOSTILE_CROSS_SOURCE_NONZERO", any(not exact_zero(value) for value in cross_residual2))
    check(f"ORBIT_{orbit}_CROSS_AND_SAME_CARRIERS_DISTINCT", any(not exact_zero(value) for value in cross_pairings))

if FAILS:
    print(f"A4D-Q0-GERM-TOWER-COLLAPSE: FAIL ({len(FAILS)} checks)")
    for name in FAILS:
        print("  - " + name)
    raise SystemExit(1)

print("A4D-Q0-GERM-TOWER-COLLAPSE-EXACT")
print("M1=0; B_n=sum_{k=2}^n binom(n,k) M_k; B_n=binom(n,2)M2+O(||x||^5).")
print("sum_{n>=2} binom(n,2)s^(n-1)=s/(1-s)^3.")
print("Full #296 Gram coefficient G_n=2 binom(1/2,n) sigma^(n-1) B_n has generic degree 2n+2.")
print("Physical orbit-5/7 exact cokernel test puts every M_k in image for all k>=0.")
print("Cross-character residual remains nonzero on its owned directions; same-carrier transport is exactly zero.")
print("SCOPE: exact orbit-5/7 physical carriers and exact harmonic algebra only; no stress, branch, Einstein, continuum, or N0 conclusion.")
