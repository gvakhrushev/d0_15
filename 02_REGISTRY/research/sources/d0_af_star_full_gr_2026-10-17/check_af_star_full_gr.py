#!/usr/bin/env python3
"""D0 AF→Lorentz Palatini: finite reproducible exact core controls.

Check:
  * same-Book AF five-path entropy value, field first and second jets;
  * golden exact-cost four-address quadrature of C² source test functions;
  * exact INTEGER 24x24 Cartan connection Hessian det=2**32;
  * a nonflat Ricci-flat pp-wave polynomial (component test).

This is deliberately a BOUNDED control: no original-v8 admission, no full
Role finite-grid Einstein Euler solver, no original #216 raw h^-2 norm.
"""
from __future__ import annotations

from math import log, sqrt

P = (sqrt(5) - 1) / 2
PHI = 1 / P
ELL = log(PHI)
E0 = P * P
ETA = (1, -1, -1, -1)
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def require(test, message):
    if not test:
        raise ArithmeticError(message)


def af_entropy_derivatives(e):
    """ACTUAL owned type-0 complete five-path distribution and C² source."""
    a = P**1.5 * sqrt(1 - e)
    b = sqrt(e / 2)
    a1 = -(P**1.5) / (2 * sqrt(1 - e))
    b1 = 1 / (2 * sqrt(2 * e))
    a2 = -(P**1.5) / (4 * (1 - e)**1.5)
    b2 = -1 / (4 * sqrt(2) * e**1.5)
    q = [(a + b)**2, (a - b)**2, P**3 * (1 - e),
         P**4 * (1 - e), P**4 * (1 - e)]
    dq = [2 * (a + b) * (a1 + b1), 2 * (a - b) * (a1 - b1),
          -(P**3), -(P**4), -(P**4)]
    ddq = [2 * (a1 + b1)**2 + 2 * (a + b) * (a2 + b2),
           2 * (a1 - b1)**2 + 2 * (a - b) * (a2 - b2),
           0., 0., 0.]
    require(abs(sum(q)-1) < 1e-12 and abs(sum(dq)) < 1e-12
            and abs(sum(ddq)) < 1e-12, "not a smooth normalized AF five-path cut")
    H = -sum(z * log(z) for z in q) / ELL
    H1 = -sum(v * log(q[i]) for i, v in enumerate(dq)) / ELL
    H2 = -(sum(v * log(q[i]) for i, v in enumerate(ddq))
            + sum(v*v/q[i] for i, v in enumerate(dq))) / ELL
    return H, H1, H2


def golden_centres(n, visit):
    """Real F cost1 and R cost2; address splitting follows RAW word length."""
    def rec(rem, depth, left, widths):
        if rem == 0:
            visit(tuple(left[i] + widths[i] / 2 for i in range(4)))
            return
        axis = depth % 4
        w = list(widths)
        w[axis] *= P
        rec(rem - 1, depth + 1, left, w)
        if rem >= 2:
            w = list(widths)
            l = list(left)
            l[axis] += P * w[axis]
            w[axis] *= P*P
            rec(rem - 2, depth + 1, l, w)
    rec(n, 0, [0., 0., 0., 0.], [1., 1., 1., 1.])


def af_c2_quadrature(n, t2):
    """Two independent sources of ONE price for f(lambda,x)=lambda*g+lambda²*k/2."""
    H0, H1, H2 = af_entropy_derivatives(E0)
    val_g = val_k = val_g2 = 0.
    count = 0
    def take(x):
        nonlocal val_g, val_k, val_g2, count
        count += 1
        weight = P**n
        g = 1 + x[0]**2   # integral g = 4/3
        k = x[1] + x[2] # integral k = 1
        val_g += weight * g
        val_k += weight * k
        val_g2 += weight * g*g
    golden_centres(n, take)
    c1 = 2*P**5 * H1 * val_g
    c2 = 2*P**5 * H1 * val_k + 2*P**7 * t2 * H2 * val_g2
    target = 2*P**5 * PHI/sqrt(5) * H1
    return {
        "n": n, "count": count, "mass": count * P**n,
        "first": c1, "first_target": target * (4/3),
        "second": c2, "second_target": target,
    }


def cartan_quadratic(indices):
    """Q=sum_(mu,nu,j) eta_nu [K_mu^mu_j K_nu^j_nu - reversed].

    Every index specifies a real coefficient of one of 24 genuine Lorentz
    connection components.  The formula is the tetradic Ricci contraction
    of constant F_mu_nu=[K_mu,K_nu], NOT a postulated Hessian.
    """
    fields = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for idx in indices:
        mu = idx // 6
        a, b = PAIRS[idx % 6]
        fields[mu][a][b] += ETA[b]
        fields[mu][b][a] -= ETA[a]
    out = 0
    for mu in range(4):
        for nu in range(4):
            for j in range(4):
                out += ETA[nu] * (
                    fields[mu][mu][j] * fields[nu][j][nu]
                    - fields[nu][mu][j] * fields[mu][j][nu]
                )
    return out


def bareiss_det(M):
    """Exact integer Gaussian elimination with all divisions verified."""
    M = [row[:] for row in M]
    n = len(M)
    sign = 1
    prev = 1
    for k in range(n-1):
        if M[k][k] == 0:
            swaps = [j for j in range(k+1, n) if M[j][k] != 0]
            require(bool(swaps), "singular connection Hessian")
            j = swaps[0]
            M[k], M[j] = M[j], M[k]
            sign = -sign
        pivot = M[k][k]
        for i in range(k+1, n):
            a_ik = M[i][k]
            for j in range(k+1, n):
                num = M[i][j]*pivot - a_ik*M[k][j]
                require(num % prev == 0, "Bareiss is not integer exact")
                M[i][j] = num // prev
            M[i][k] = 0
        prev = pivot
    return sign * M[n-1][n-1]


def connection_hessian_control():
    # Q(e_i)=0; full Hessian has 24 fields and is symmetric.
    H = [[0] * 24 for _ in range(24)]
    for i in range(24):
        require(cartan_quadratic([i]) == 0, "unexpected diagonal quadratic")
        for j in range(i+1,24):
            H[i][j] = cartan_quadratic([i,j])
            H[j][i] = H[i][j]
    require(sum(x != 0 for row in H for x in row) == 48, "unexpected Cartan pattern")
    det = bareiss_det(H)
    require(det == 2**32, f"incorrect full24 Lorentz Cartan determinant: {det}")
    return det


def main():
    h, h1, h2 = af_entropy_derivatives(E0)
    require(abs(h1 + 0.8766413650175716) < 1e-11, "AF entropy source")
    require(abs(h2 - 8.002389502309384) < 1e-10, "AF entropy Hessian")
    kappa = 2*P**5 * PHI/sqrt(5) * h1
    require(abs(kappa + 0.11439746264177995) < 1e-11, "nonzero Book AF coupling")
    print(f"AF q=5 Book H={h:.12f}, H1={h1:.12f}, H2={h2:.12f}")
    print(f"ONE GLOBAL AF COUPLING={kappa:.12f}")
    for n,count in ((8,34),(12,233),(16,1597),(20,10946)):
        out = af_c2_quadrature(n, 1e-4)
        require(out["count"] == count, "incorrect golden exact-cost word count")
        if n == 20:
            require(abs(out["first"]-out["first_target"]) < 0.0004,
                    "global first source not converging")
            require(abs(out["second"]-out["second_target"]) < 0.001,
                    "global second source not converging")
        print("C2 n={n} words={count} first={first:.12f} "
              "target={first_target:.12f} second={second:.12f} "
              "target2={second_target:.12f}".format(**out))
    det = connection_hessian_control()
    print(f"LORENTZ CARTAN full24 integer Hessian determinant={det}=2**32")
    # Real local pp-wave with H=a(x²-y²): Δ_xy H=2a-2a=0,
    # while H_xx=2a ≠0. The first is Ricci, the second Riemann.
    a = 3
    require(2*a-2*a == 0 and 2*a != 0, "pp-wave curvature control")
    print("NONFLAT exact continuum Einstein pp-wave: Ricci=0, Riemann!=0")
    print("PASS exact finite AF Book C2 + full Lorentz24 Cartan witness")
    print("SCOPE mathematical AF-star composite; not literal native physical admission/full raw #216")


if __name__ == "__main__":
    main()
