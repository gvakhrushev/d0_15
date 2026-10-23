#!/usr/bin/env python3
"""Reproducible interval witness for the q=(3,3,0,0) mixed crossing.

This checker consumes the pinned native interval owner and fixed finite-decimal
B/R inputs. It performs no eigensolver, root search, basis optimization, or file
write. The only certified conclusion is the local source-neutral grade-four
nonstationarity stated in README.md.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OWNER_REL = Path("02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/pure_memory_interval.py")
OWNER_SHA256 = "19d4e33f7c74465da9079ec4e3c90e0b20b3b1aad448a0cdb1957a3fc61ef41f"
B_SHA256 = "79cd5a423a68b6d47cc41853a840c3caef06895ab85e1781ef15cb2fc6a47a8d"
R_SHA256 = "5ffe4cc73949b455c3e8643d1cae0bf35ece226179278ad05d578f67c720fc90"
Q = (3, 3, 0, 0)
L = 8
N = 13
TLO = 0.43032
THI = 0.430405
ORDER = (0, 2, 3, 1)


def require(condition: bool, label: str) -> None:
    if not bool(condition):
        raise ArithmeticError("q3300_mixed_crossing:" + label)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_owner():
    path = ROOT / OWNER_REL
    require(sha256(path) == OWNER_SHA256, "pinned_interval_owner")
    spec = importlib.util.spec_from_file_location("q3300_pinned_interval_owner", path)
    require(spec is not None and spec.loader is not None, "load_interval_owner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_source_neutrality():
    """Exact Sympy CAR proof in the owned ACDB order and the source basis."""
    identity = sp.eye(16)

    def creators(order):
        result = []
        for mode in range(4):
            matrix = sp.zeros(16)
            predecessors = order[:order.index(mode)]
            for mask in range(16):
                if not mask & (1 << mode):
                    sign = (-1) ** sum(1 for j in predecessors if mask & (1 << j))
                    matrix[mask | (1 << mode), mask] = sign
            result.append(matrix)
        return result

    def make_sources(cars):
        annihilators = [matrix.T for matrix in cars]

        def create(vector):
            return sum((vector[i] * cars[i] for i in range(4)), sp.zeros(16))

        def annihilate(vector):
            return sum((vector[i] * annihilators[i] for i in range(4)), sp.zeros(16))

        def gamma(vector):
            return create(vector) + annihilate(vector)

        def kappa(vector):
            return create(vector) - annihilate(vector)

        A, B = sp.symbols("A B", real=True)
        frame = (A - B) * sp.eye(4) + B * sp.ones(4)
        legs = [frame.row(r).T for r in range(4)]
        total = sum(legs, sp.zeros(4, 1))
        coeff = 8 * (2 - sp.sqrt(2))
        sources = []
        for r in range(4):
            x, y, z = legs[r][1], legs[r][2], legs[r][3]
            skew = sp.zeros(4)
            skew[1, 2], skew[1, 3] = -z, y
            skew[2, 1], skew[2, 3] = z, -x
            skew[3, 1], skew[3, 2] = -y, x
            sources.append(coeff * gamma(skew * total) * kappa(legs[r]))
        return sources

    standard = creators((0, 1, 2, 3))
    actual = creators(ORDER)
    U = sp.diag(*[(-1) ** (int(bool(mask & 2)) *
                            (int(bool(mask & 4)) + int(bool(mask & 8))))
                  for mask in range(16)])
    require(all(actual[r] == U * standard[r] * U.T for r in range(4)),
            "standard_to_ACDB_intertwiner")

    annihilators = [matrix.T for matrix in actual]
    gammas = [actual[i] + annihilators[i] for i in range(4)]
    kappas = [actual[i] - annihilators[i] for i in range(4)]
    majors = [gammas[0], sp.I * kappas[0], gammas[1], sp.I * kappas[1]]
    W = majors[0] * majors[1] * majors[2] * majors[3]

    def exact_zero(value):
        return sp.simplify(sp.expand_complex(value)) == 0

    def matrix_zero(matrix):
        return all(exact_zero(value) for value in matrix)

    require(W.conjugate().T == W, "grade4_witness_hermitian")
    require(W * W == identity, "grade4_witness_square_identity")
    require(sp.trace(W) == 0, "grade4_witness_trace_zero")
    pairings = [sp.trace(W * gammas[i] * kappas[j])
                for i in range(4) for j in range(4)]
    require(all(exact_zero(value) for value in pairings),
            "orthogonal_to_all_16_grade0_grade2_source_generators")

    chi = sp.zeros(16, 1)
    chi[1], chi[15] = 1 / sp.sqrt(2), 1 / sp.sqrt(2)
    require(U * chi == chi, "source_seed_ACDB_phase")
    source_std = make_sources(standard)
    source_actual = make_sources(actual)
    for r, (old, new) in enumerate(zip(source_std, source_actual)):
        require(matrix_zero(new - U * old * U.T), "source_intertwining_%d" % r)
        require(exact_zero(sp.trace(new)), "source_trace_zero_%d" % r)
        require(exact_zero((chi.T * new * chi)[0]), "seed_source_zero_%d" % r)
        require(exact_zero(sp.trace(W * new)), "witness_source_pairing_zero_%d" % r)

    # rho_t=(1-t)I/16+t|chi><chi| has minimum eigenvalue (1-t)/16.
    # W^2=I and the exact source pairings above make W a two-sided tangent
    # throughout each 0<t<1 interior point for |epsilon|<(1-t)/16.
    t = sp.symbols("t", real=True)
    rho = (1 - t) * identity / 16 + t * (chi * chi.T)
    for r, source in enumerate(source_actual):
        require(exact_zero(sp.trace(rho * source)), "full_rank_source_fibre_%d" % r)
    return {
        "status": "PASS_EXACT",
        "CAR_order": list(ORDER),
        "basis_intertwiner_diagonal_signs": [int(U[i, i]) for i in range(16)],
        "witness": "W=(gamma_0 i*kappa_0)(gamma_1 i*kappa_1)",
        "witness_hermitian_square_identity_trace_zero": True,
        "grade0_grade2_generator_pairings": 16,
        "native_source_rows_checked": 4,
        "seed_source_expectations_zero": True,
        "full_rank_source_fibre_tangent": True,
        "positivity_radius": "abs(epsilon)<(1-t)/16 for 0<t<1",
    }


def interval_certificate():
    owner = load_owner()
    shared = owner.prepare_shared(ROOT)
    iv = shared["iv"]
    arithmetic = shared["arithmetic"]
    alg = shared["pure_interval_owner"]

    def lower(value):
        return -arithmetic.upper(-value)
    b_path, r_path = HERE / "fixed_B.json", HERE / "fixed_schur_R.json"
    require(sha256(b_path) == B_SHA256, "fixed_B_sha256")
    require(sha256(r_path) == R_SHA256, "fixed_R_sha256")
    b_data, r_data = load_json(b_path), load_json(r_path)
    require(b_data["dimension"] == N and r_data["dimension"] == 12,
            "fixed_input_dimensions")
    Bflat = b_data["row_major_B"]
    B = [Bflat[N * i:N * (i + 1)] for i in range(N)]
    Rpairs = r_data["row_major_R"]
    require(len(Bflat) == N * N and len(B) == N
            and all(len(row) == N for row in B), "B_shape")
    require(len(Rpairs) == 144, "R_shape")
    require(all(isinstance(x, str) and alg.DECIMAL.fullmatch(x)
                for row in B for pair in row for x in pair), "B_decimal_strings")
    require(all(isinstance(x, str) and alg.DECIMAL.fullmatch(x)
                for pair in Rpairs for x in pair), "R_decimal_strings")

    _, full, indices, on_shell = owner._section(Q, {"B": B}, shared)
    require(not on_shell and indices == list(range(N)), "complete_q3300_native_mean_slice")
    H, E0, geometry = owner._old_symbol(Q, full, N, shared)
    correction, EC, finite_data = owner._finite_correction(Q, geometry, shared)
    scalars = owner._scalars(Q, full, shared)
    Sref = np.array([[complex(arithmetic.midpoint(scalars[i][j].real),
                                arithmetic.midpoint(scalars[i][j].imag))
                      for j in range(N)] for i in range(N)])

    # Symmetrize only floating centres. The exact Hessian is Hermitian; taking
    # the larger mirrored source interval preserves an enclosure of that exact
    # matrix while removing irrelevant floating anti-Hermitian roundoff.
    H0raw = H
    H1raw = H + correction + Sref
    H0 = (H0raw + H0raw.conj().T) / 2
    H1 = (H1raw + H1raw.conj().T) / 2

    def abs_upper(value):
        return arithmetic.upper(alg._abs(value, iv))

    def sym_round(left, right):
        mag = (alg._abs(alg._point(left, iv), iv)
               + alg._abs(alg._point(right, iv), iv))
        return arithmetic.upper(2 * arithmetic.gamma(32) * mag + arithmetic.TINY)

    r0 = np.zeros((N, N), float)
    r1 = np.zeros((N, N), float)
    for i in range(N):
        for j in range(N):
            old_ij = arithmetic.upper(E0[i][j])
            old_ji = arithmetic.upper(E0[j][i])
            r0[i, j] = max(old_ij, old_ji) + sym_round(H0raw[i, j], H0raw[j, i])

            scalar_ij = abs_upper(scalars[i][j] - alg._point(Sref[i, j], iv))
            scalar_ji = abs_upper(scalars[j][i] - alg._point(Sref[j, i], iv))
            add_ij = arithmetic.upper(
                2 * arithmetic.gamma(32) *
                (alg._abs(alg._point(H[i, j], iv), iv)
                 + alg._abs(alg._point(correction[i, j], iv), iv)
                 + alg._abs(alg._point(Sref[i, j], iv), iv)) + arithmetic.TINY)
            add_ji = arithmetic.upper(
                2 * arithmetic.gamma(32) *
                (alg._abs(alg._point(H[j, i], iv), iv)
                 + alg._abs(alg._point(correction[j, i], iv), iv)
                 + alg._abs(alg._point(Sref[j, i], iv), iv)) + arithmetic.TINY)
            err_ij = old_ij + arithmetic.upper(EC[i][j]) + scalar_ij + add_ij
            err_ji = old_ji + arithmetic.upper(EC[j][i]) + scalar_ji + add_ji
            r1[i, j] = max(err_ij, err_ji) + sym_round(H1raw[i, j], H1raw[j, i])

    def interval_radius(value, radius):
        re, im, radius = float(value.real), float(value.imag), float(radius)
        lo_re = float(np.nextafter(re - radius, -np.inf))
        hi_re = float(np.nextafter(re + radius, np.inf))
        lo_im = float(np.nextafter(im - radius, -np.inf))
        hi_im = float(np.nextafter(im + radius, np.inf))
        return iv.mpc(iv.mpf([repr(lo_re), repr(hi_re)]),
                      iv.mpf([repr(lo_im), repr(hi_im)]))

    H0i = [[interval_radius(H0[i, j], r0[i, j]) for j in range(N)] for i in range(N)]
    H1i = [[interval_radius(H1[i, j], r1[i, j]) for j in range(N)] for i in range(N)]
    zero = iv.mpc(0)

    def mix(tbox):
        return [[(1 - tbox) * H0i[i][j] + tbox * H1i[i][j]
                 for j in range(N)] for i in range(N)]

    R = [[complex(float(Rpairs[12 * i + j][0]), float(Rpairs[12 * i + j][1]))
          for j in range(12)] for i in range(12)]
    Riv = [[iv.mpc(Rpairs[12 * i + j][0], Rpairs[12 * i + j][1])
            for j in range(12)] for i in range(12)]
    T = iv.mpf([repr(TLO), repr(THI)])
    GT = mix(T)
    Cbox = [[GT[i][j] for j in range(12)] for i in range(12)]
    E = [[iv.mpc(int(i == j)) - sum((Riv[i][k] * Cbox[k][j]
                                     for k in range(12)), zero)
          for j in range(12)] for i in range(12)]
    eps_box = max(sum((alg._abs(E[i][j], iv) for j in range(12)), iv.mpf(0))
                  for i in range(12))
    eps = arithmetic.upper(eps_box)
    require(eps < 1, "uniform_R_C_invertibility")
    Rnorm_box = max(sum((alg._abs(Riv[i][j], iv) for j in range(12)), iv.mpf(0))
                    for i in range(12))
    invnorm_box = Rnorm_box / (1 - iv.mpf(repr(eps)))
    invnorm = arithmetic.upper(invnorm_box)

    def center(value):
        return complex(arithmetic.midpoint(value.real), arithmetic.midpoint(value.imag))

    def point_complex(value):
        return iv.mpc(repr(float(value.real)), repr(float(value.imag)))

    def endpoint(t_value):
        G = mix(iv.mpf(repr(t_value)))
        Aint = G[12][12]
        b = [G[i][12] for i in range(12)]
        C = [[G[i][j] for j in range(12)] for i in range(12)]
        bc = [center(value) for value in b]
        x0 = [sum((R[i][j] * bc[j] for j in range(12)), 0j) for i in range(12)]
        x0i = [point_complex(x) for x in x0]
        residual = [b[i] - sum((C[i][j] * x0i[j] for j in range(12)), zero)
                    for i in range(12)]
        residual_norm = max(abs_upper(value) for value in residual)
        xerr = arithmetic.upper(iv.mpf(repr(invnorm)) * iv.mpf(repr(residual_norm)))
        ac = center(Aint)
        err_a = abs_upper(Aint - alg._point(ac, iv))
        err_b = [abs_upper(b[i] - alg._point(bc[i], iv)) for i in range(12)]

        def conj(z):
            return iv.mpc(z.real, -z.imag)

        schur_center = iv.mpc(repr(float(ac.real))) - sum(
            (conj(point_complex(bc[i])) * point_complex(x0[i]) for i in range(12)), zero)
        err = iv.mpf(repr(err_a)) + sum(
            (iv.mpf(repr(abs(bc[i]))) * iv.mpf(repr(xerr))
             + iv.mpf(repr(err_b[i])) *
             (iv.mpf(repr(abs(x0[i]))) + iv.mpf(repr(xerr)))
             for i in range(12)), iv.mpf(0))
        lo = lower(schur_center.real - err)
        hi = arithmetic.upper(schur_center.real + err)
        return {"lower": lo, "upper": hi, "center": float(schur_center.real.mid),
                "error": arithmetic.upper(err), "kernel_coordinate_radius": xerr}

    left, right = endpoint(TLO), endpoint(THI)
    require(left["lower"] > 0 and right["upper"] < 0,
            "opposite_schur_signs_at_fixed_bracket")

    midpoint = (TLO + THI) / 2
    Gmid = mix(iv.mpf(repr(midpoint)))
    bmid = [center(Gmid[i][12]) for i in range(12)]
    x0 = [sum((R[i][j] * bmid[j] for j in range(12)), 0j) for i in range(12)]
    x0i = [point_complex(x) for x in x0]
    bT = [GT[i][12] for i in range(12)]
    residualT = [bT[i] - sum((Cbox[i][j] * x0i[j] for j in range(12)), zero)
                 for i in range(12)]
    residualTnorm = max(abs_upper(value) for value in residualT)
    xradius = arithmetic.upper(iv.mpf(repr(invnorm)) * iv.mpf(repr(residualTnorm)))
    xi = [interval_radius(-x0[i], xradius) for i in range(12)] + [iv.mpc(1)]
    Gp = [[H1i[i][j] - H0i[i][j] for j in range(N)] for i in range(N)]
    derivative = sum((iv.mpc(xi[i].real, -xi[i].imag) * Gp[i][j] * xi[j]
                      for i in range(N) for j in range(N)), zero)
    derivative_interval = derivative.real
    derivative_lo = lower(derivative_interval)
    derivative_hi = arithmetic.upper(derivative_interval)
    require(derivative_hi < 0, "strictly_negative_schur_derivative_on_bracket")

    # The fixed B congruence maps the Schur kernel coordinates to a native
    # tangent. The full16 operator below includes all occupied/predecessor nodes
    # and the actual mixed second chart jet D2.
    P = [[iv.mpc(pair[0], pair[1]) for pair in row] for row in B]
    native = [sum((P[i][j] * xi[j] for j in range(N)), zero) for i in range(N)]
    u, columns = alg._base_fields(Q, shared["core"]["a"], shared["core"]["b"],
                                  shared["roots_iv"])
    av = [[[zero for _ in range(4)] for _ in range(4)]]
    omega = [[[zero for _ in range(3)] for _ in range(4)]]
    for i, column in enumerate(columns):
        for (kind, r, k), value in column.items():
            if kind == 0:
                av[0][r][k] += native[i] * value
            else:
                omega[0][r][k] += native[i] * value

    def conj(z):
        return iv.mpc(z.real, -z.imag)

    def mm(A, C):
        return [[sum((A[i][k] * C[k][j] for k in range(len(C))), zero)
                 for j in range(len(C[0]))] for i in range(len(A))]

    def dagger(A):
        return [[conj(A[j][i]) for j in range(len(A))]
                for i in range(len(A[0]))]

    def madd(A, C):
        return [[A[i][j] + C[i][j] for j in range(len(A[0]))]
                for i in range(len(A))]

    def mscale(scalar, A):
        return [[scalar * A[i][j] for j in range(len(A[0]))]
                for i in range(len(A))]

    def cross_vec(a, b):
        return [a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0]]

    creators = []
    for r in range(4):
        C = [[0 for _ in range(16)] for _ in range(16)]
        predecessors = ORDER[:ORDER.index(r)]
        for mask in range(16):
            if not mask & (1 << r):
                sign = (-1) ** sum(1 for j in predecessors if mask & (1 << j))
                C[mask | (1 << r)][mask] = sign
        creators.append([[iv.mpc(value) for value in row] for row in C])

    def create(vector):
        result = [[zero for _ in range(16)] for _ in range(16)]
        for a in range(4):
            if vector[a] != 0:
                result = madd(result, mscale(vector[a], creators[a]))
        return result

    def annihilate(vector):
        result = [[zero for _ in range(16)] for _ in range(16)]
        for a in range(4):
            if vector[a] != 0:
                result = madd(result, mscale(vector[a], dagger(creators[a])))
        return result

    def cross_matrix(v):
        return [[zero, -v[2], v[1]], [v[2], zero, -v[0]], [-v[1], v[0], zero]]

    def gamma_skew(w):
        result = [[zero for _ in range(16)] for _ in range(16)]
        for a in range(3):
            for b in range(3):
                if w[a][b] != 0:
                    result = madd(result, mscale(w[a][b],
                                                  mm(creators[a + 1], dagger(creators[b + 1]))))
        return result

    def phase(momentum, r):
        return shared["roots_iv"][int(momentum[r]) % L]

    def D(momentum):
        result = [[zero for _ in range(16)] for _ in range(16)]
        for r in range(4):
            t = phase(momentum, r)
            leg = [iv.mpc(x) for x in u[r]]
            result = madd(result, mscale(L * (t - 1), create(leg)))
            result = madd(result, mscale(L * (conj(t) - 1), annihilate(leg)))
        return result

    def J(momentum):
        result = [[zero for _ in range(16)] for _ in range(16)]
        for r in range(4):
            tk = phase(momentum, r)
            outgoing = tuple((momentum[j] + Q[j]) % L for j in range(4))
            tl = phase(outgoing, r)
            leg = [iv.mpc(x) for x in u[r]]
            a = av[0][r]
            G = gamma_skew(cross_matrix(omega[0][r]))
            terms = [((tk - 1), create(a)), (tk, mm(create(leg), G)),
                     ((conj(tk) - 1), annihilate(a)),
                     (-conj(tl), mm(annihilate(leg), G))]
            for coeff, matrix in terms:
                result = madd(result, mscale(L * coeff, matrix))
        return result

    def X(momentum):
        outgoing = tuple((momentum[r] + Q[r]) % L for r in range(4))
        return madd(mm(D(outgoing), J(momentum)), mm(J(momentum), D(momentum)))

    def D2(momentum):
        constant = [[zero for _ in range(16)] for _ in range(16)]
        plus = []
        for r in range(4):
            leg = [iv.mpc(x) for x in u[r]]
            a = av[0][r]
            om = omega[0][r]
            rho = iv.sqrt(sum((iv.mpf(u[r][k + 1]) ** 2 for k in range(3)), iv.mpf(0)))
            z = [iv.mpf(u[r][k + 1]) / rho for k in range(3)]
            radial = sum((z[k] * a[k + 1] for k in range(3)), zero)
            beta = [(a[k + 1] - radial * z[k]) / rho for k in range(3)]
            theta = sum((z[k] * om[k] for k in range(3)), zero)
            beta_bar = [conj(x) for x in beta]
            theta_bar = conj(theta)
            radial_bar = conj(radial)
            beta_norm = sum((beta[k] * beta_bar[k] for k in range(3)), zero)
            u2 = [iv.mpc(0)] + [radial * beta_bar[k] + radial_bar * beta[k]
                                  - rho * beta_norm * z[k] for k in range(3)]
            qt = shared["roots_iv"][Q[r] % L]
            qtbar = conj(qt)
            VA = cross_matrix([(1 - qt) * x for x in cross_vec(z, beta)])
            VB = cross_matrix([(1 - qtbar) * x for x in cross_vec(z, beta_bar)])
            Z = cross_matrix(z)
            Z2 = mm(Z, Z)
            beta_cross = cross_matrix(cross_vec(beta, beta_bar))
            R2 = [[theta * cross_matrix(beta_bar)[i][j]
                   + theta_bar * cross_matrix(beta)[i][j]
                   + theta * theta_bar * Z2[i][j]
                   + theta * mm(Z, VB)[i][j]
                   + theta_bar * mm(Z, VA)[i][j]
                   + (qt - qtbar) * beta_cross[i][j]
                   + (mm(VA, VB)[i][j] + mm(VB, VA)[i][j]) / 2
                   for j in range(3)] for i in range(3)]
            WA = cross_matrix(om)
            WB = cross_matrix([conj(x) for x in om])
            K2 = [[R2[i][j] - (mm(WA, WB)[i][j] + mm(WB, WA)[i][j]) / 2
                   for j in range(3)] for i in range(3)]
            GA, GB = gamma_skew(WA), gamma_skew(WB)
            E2 = madd(gamma_skew(K2),
                      mscale(iv.mpf("0.5"), madd(mm(GA, GB), mm(GB, GA))))
            c2 = create(u2)
            constant = madd(constant, mscale(-L, c2))
            plus.append(mscale(L, madd(c2, madd(mm(create(a), GB),
                              madd(mm(create([conj(x) for x in a]), GA),
                                   mm(create(leg), E2))))))
        result = madd(constant, dagger(constant))
        for r in range(4):
            t = phase(momentum, r)
            result = madd(result, madd(mscale(t, plus[r]),
                                       mscale(conj(t), dagger(plus[r]))))
        return result

    majoranas = []
    for j in range(2):
        majoranas.extend((madd(creators[j], dagger(creators[j])),
                          mscale(iv.j, madd(creators[j], mscale(-1, dagger(creators[j]))))))
    W = mm(mm(mm(majoranas[0], majoranas[1]), majoranas[2]), majoranas[3])
    M = [[zero for _ in range(16)] for _ in range(16)]
    shell = shared["core"]["shell_modes"]
    for momentum in shell:
        predecessor = tuple((momentum[r] - Q[r]) % L for r in range(4))
        Jout, Jpre = J(momentum), J(predecessor)
        Xout, Xpre = X(momentum), X(predecessor)
        piece = madd(mm(dagger(Jout), Jout), mm(Jpre, dagger(Jpre)))
        mode_out = np.ravel_multi_index(tuple((momentum[r] + Q[r]) % L
                                              for r in range(4)), (L,) * 4)
        mode_pre = np.ravel_multi_index(predecessor, (L,) * 4)
        r_out = shared["core"]["resolvent"][mode_out]
        r_pre = shared["core"]["resolvent"][mode_pre]
        piece = madd(piece, mscale(-r_out, mm(dagger(Xout), Xout)))
        piece = madd(piece, mscale(-r_pre, mm(Xpre, dagger(Xpre))))
        M = madd(M, mscale(iv.mpf("0.125"), piece))
        d, d2 = D(momentum), D2(momentum)
        M = madd(M, mscale(iv.mpf("0.125"), madd(mm(d, d2), mm(d2, d))))

    pairing = sum((W[i][j] * M[j][i] for i in range(16) for j in range(16)), zero) / 16
    pairing_lo = lower(pairing.real)
    pairing_hi = arithmetic.upper(pairing.real)
    require(pairing_lo > 0, "strictly_positive_real_grade4_pairing_at_actual_kernel")

    def fmt(value):
        return format(float(value), ".17g")

    return {
        "status": "PASS_LOCAL_Q3300",
        "q": list(Q),
        "carrier": {"L": L, "Fock_dimension": 16, "native_tangent_dimension": N,
                    "occupied_shell_nodes": len(shared["core"]["shell_modes"])},
        "fixed_inputs": {"B_sha256": B_SHA256, "R_sha256": R_SHA256,
                         "interval_owner_sha256": OWNER_SHA256},
        "external_full_lorentz_boundary": {
            "owner_sha256": "0ca27a97b7e8fa5653242415c4bcbe0e946fccd95bb277024fcbe79222c927a8",
            "result_sha256": "8920803d185af11132dfa274a42d0e307ad43db150ef8e87d7ab83c9bf2f4d0d",
            "status": "CONTEXT_ONLY_NOT_A_CHECKER_INPUT",
            "legacy_pure_seed_fails_12_independent_boost_rows": True,
        },
        "schur": {
            "bracket": [TLO, THI],
            "lower_endpoint_interval": [fmt(left["lower"]), fmt(left["upper"])],
            "upper_endpoint_interval": [fmt(right["lower"]), fmt(right["upper"])],
            "uniform_preconditioned_residual_norm_upper": fmt(eps),
            "uniform_inverse_norm_upper": fmt(invnorm),
            "kernel_coordinate_radius_upper": fmt(xradius),
            "derivative_interval": [fmt(derivative_lo), fmt(derivative_hi)],
            "unique_crossing_in_bracket": True,
        },
        "source_neutrality": exact_source_neutrality(),
        "grade4_pairing_real_interval": [fmt(pairing_lo), fmt(pairing_hi)],
        "actual_mixed_second_chart_jet_included": True,
        "finite_operator_data": finite_data,
        "source_interface": "legacy four-link-source rows only; not the 12 canonical full-Lorentz boost Euler rows",
        "conclusion": "For the legacy four-source interpolation only, the unique q=(3,3,0,0) crossing in this fixed local chart has a strictly positive real pairing of the full native second-order matter operator with an exact source-neutral grade-four tangent.",
        "scope_limits": {
            "only_this_q_and_this_fixed_native_chart": True,
            "only_legacy_four_source_interpolation": True,
            "canonical_full_lorentz_12_boost_rows_not_checked_here": True,
            "not_a_feasible_full_lorentz_faithful_to_old_pure_seed_path": True,
            "not_a_convergent_nonlinear_branch": True,
            "not_an_admission_or_recovery_theorem": True,
            "not_a_full_general_relativity_result": True,
            "does_not_close_global_D0_obligations": True,
        },
    }


def run():
    result = interval_certificate()
    result["schema"] = "d0-q3300-mixed-crossing-grade4-witness/1"
    return result


if __name__ == "__main__":
    try:
        print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
    except Exception as exc:
        print("FAIL: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        raise
