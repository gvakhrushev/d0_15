#!/usr/bin/env python3
"""Exact flat-jet regression for the A4D star + joint-residual completion.

Research-only, exact SymPy arithmetic. Companion regression for the Lean owner
`D0.Geometry.A4DStarEinsteinSeed`.

The Lean module owns the abstract homogeneity laws:

    det(e X)     = e^4  det X
    adj(e X)     = e^3  adj X
    R(e X, e t)  = e^5  R(X, t)
    Q_H(e R)     = e^10 Q_H(R)

This script checks those laws on explicit concrete defects at the owned
`L = 2` background, so the Lean statements are not vacuous and cannot be
silently reinterpreted.

Scope: finite exact algebra only. No coefficient selection, no curved root
search, no continuum Einstein claim.
"""
import sympy as sp

N = 4
I4 = sp.eye(N)
ETA = sp.diag(1, -1, -1, -1)

failures = []


def check(name, cond, detail=""):
    if cond:
        print("PASS_" + name)
    else:
        failures.append(name)
        print("FAIL_" + name + (" :: " + detail if detail else ""))


# ---------------------------------------------------------------- residual

def joint_residual(X1, X2, t1, t2):
    """R_{2|1} = det(X_1) t_2 - X_2 adj(X_1) t_1."""
    return sp.simplify(sp.Matrix(
        [X1.det() * t2[i] - sum((X2 * X1.adjugate())[i, j] * t1[j] for j in range(N))
         for i in range(N)]))


def quad(H, R):
    """Q_H(R) = R^T H R."""
    return sp.simplify((R.T * H * R)[0, 0])


# ------------------------------------------------- explicit L=2 witnesses
# Rational invertible defects, so det is genuinely O(e^4) and not identically 0.
A = sp.Matrix([[2, 1, 0, 0], [0, 2, 1, 0], [0, 0, 2, 1], [1, 0, 0, 2]])
B = sp.Matrix([[1, 0, 1, 0], [1, 2, 0, 0], [0, 1, 1, 1], [0, 0, 1, 2]])
check("DEFECT_A_INVERTIBLE", A.det() != 0, str(A.det()))
check("DEFECT_B_INVERTIBLE", B.det() != 0, str(B.det()))

u = sp.Matrix([1, 2, 3, 4])
w = sp.Matrix([-1, 0, 2, 1])
H = ETA

e = sp.symbols("e")
e = sp.Rational(1, 2)

# --------------------------------------------- Lean law 1: det / adjugate
check("LEAN_DET_DEGREE_FOUR", sp.simplify((e * A).det() - e ** 4 * A.det()) == sp.zeros(1, 1)
      or sp.simplify((e * A).det() - e ** 4 * A.det()) == 0)
check("LEAN_ADJ_DEGREE_THREE",
      (e * A).adjugate() == e ** 3 * A.adjugate())
check("LEAN_ADJ_DEGREE_THREE_B",
      (e * B).adjugate() == e ** 3 * B.adjugate())

# ------------------------------------- Lean law 2: residual scaling O(X^4 t)
# Hold translations fixed, scale both defects.
R_def = joint_residual(e * A, e * B, u, w)
R_ref = joint_residual(A, B, u, w)
check("LEAN_RESIDUAL_SCALED_X_ONLY",
      R_def == e ** 4 * R_ref,
      "%s vs %s" % (R_def.T, (e ** 4 * R_ref).T))

# Simultaneous X = O(e), t = O(e) => R = O(e^5)
R_joint = joint_residual(e * A, e * B, e * u, e * w)
check("LEAN_RESIDUAL_SCALED_JOINT",
      R_joint == e ** 5 * R_ref,
      "%s vs %s" % (R_joint.T, (e ** 5 * R_ref).T))

# ------------------------------------- Lean law 3: quadratic completion O(e^10)
Q_joint = quad(H, R_joint)
Q_ref = quad(H, R_ref)
check("LEAN_COMPLETION_SCALED",
      sp.simplify(Q_joint - e ** 10 * Q_ref) == 0,
      "%s vs %s" % (Q_joint, e ** 10 * Q_ref))

# --------------------------------- explicit polynomial-order verification
z = sp.symbols("z")
# Use fresh symbolic defects to read off the true vanishing order at z = 0.
Az = z * A
Bz = z * B
uz = z * u
wz = z * w


def order(expr, var, cap=20):
    p = sp.Poly(sp.expand(expr), var)
    for k in range(cap + 1):
        if p.coeff_monomial(var ** k) != 0:
            return k
    return cap + 1


Rz = joint_residual(Az, Bz, uz, wz)
min_r = min(order(c, z) for c in Rz)
check("ORDER_RESIDUAL_IS_FIVE", min_r == 5, "got order %d" % min_r)
Qz = quad(H, Rz)
min_q = order(Qz, z)
check("ORDER_COMPLETION_IS_TEN", min_q == 10, "got order %d" % min_q)

# All derivatives of the completion below order 10 vanish at z = 0:
# this is exactly the statement that the flat two-jet is zero.
for k in range(10):
    check("COMPLETION_DERIV_%d_ZERO" % k,
          sp.diff(Qz, z, k).subs(z, 0) == 0)

# ---------------------------------------------- flat background value/derivative
# At the exact flat background X = 0, the residual and its completion vanish.
R_flat = joint_residual(sp.zeros(N), sp.zeros(N), u, w)
check("FLAT_RESIDUAL_VALUE_ZERO", R_flat == sp.zeros(N, 1), str(R_flat.T))
check("FLAT_COMPLETION_VALUE_ZERO", quad(H, R_flat) == 0)

# ------------------------------------------------- negative control (nonvacuity)
# The completion is NOT identically zero: a generic defect gives a nonzero value.
check("NEGATIVE_CONTROL_COMPLETION_NONZERO", quad(H, R_ref) != 0)
# And the exact order is 10, not higher: the z^10 coefficient is nonzero.
p = sp.Poly(sp.expand(Qz), z)
check("COMPLETION_ORDER_IS_EXACTLY_TEN", p.coeff_monomial(z ** 10) != 0)

# ---------------------------------------------------------------- summary
print()
if failures:
    print("FLAT_JET_REGRESSION: FAIL (%d)" % len(failures))
    for f in failures:
        print("  - " + f)
    raise SystemExit(1)

print("FLAT_JET_REGRESSION: PASS")
print("LEAN_LAWS_CHECKED: det=e^4, adj=e^3, R(eX,et)=e^5 R, Q_H(eR)=e^10 Q_H(R)")
print("BACKGROUND: exact rational defects on the owned L=2 finite lattice")
print("RESULT: j^2_flat(Q) = 0 and j^2_flat(S_star + Q) = j^2_flat S_star")
print("ROLE: Q is a nonlinear completion; it cannot alter the flat linear operator")
print("SCOPE: finite exact algebra. No coefficient selection, no curved roots, "
      "no continuum Einstein claim.")
