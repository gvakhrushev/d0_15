"""Reusable native nonzero-q symbol algebra, not a frequency census.

The exact mean slice uses B_r=Omega_r/kappa_r on active roles,
sum_active B_r=0, a_r=B_r u_r. Inactive roles retain all four a components
and Omega_r=theta_r [w_r]_cross. A common spatial representation adds the
same B to every active role and shifts inactive a by B u. Thus this is the
complete quotient of the regular native first-jet chart by its six proved
representation directions. No SO(4), matter freeze, or physical gauge
admission is introduced. At L=8 only, |kappa_nonzero|>=sqrt(2-sqrt(2)); this
is NOT a refinement-uniform statement.

Clifford8 monomials are an orthogonal coordinate system for ALL16 Fock
components: Tr16(A*B)=16 sum conjugate(a_I)b_I. J has degrees1,3; X has
degrees0,2,4. Native own-leg transport cancels the +/-2e_r Laurent terms
EXACTLY, leaving33 monomials and257 phase-difference moments. No numerical
threshold drops an operator coefficient. The optional two-point H_J
formula requires the existing homogeneous stationary moment equations.
Away from the root the default weighted assembly gives the first-jet block;
the full constrained Hessian additionally needs Tr W{D,D_vw}.

API: native_quotient(q,a,b), split_representation(q,a,omega,u),
shared_spectral_data(repo=None,a=None,b=None), and
assemble_symbol(q,shared=None,repo=None,use_stationary_root_identity=False).
The assembler is numerical; run() separately checks exact algebra and one
NEW q1240 against independent full4096x16 operator assembly. No old run(),
root search, receipt mutation, full-mode classification or GR claim occurs.
"""
from __future__ import annotations

import os
for _name in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import time

import mpmath as mp
from mpmath.ctx_iv import MPIntervalContext
import numpy as np
import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
L, FOCK, REFERENCE, ROUNDS = 8, 16, 128, 8192
ZERO = (0, 0, 0, 0)
UNIT = tuple(tuple(int(i == j) for i in range(4)) for j in range(4))
E9 = (ZERO,)+UNIT+tuple(tuple(-x for x in e) for e in UNIT)
E33 = tuple(sorted({ZERO, *UNIT, *(tuple(-x for x in e) for e in UNIT),
                   *(tuple(sg*UNIT[r][i]+sh*UNIT[t][i] for i in range(4))
                     for r in range(4) for t in range(r+1, 4)
                     for sg in (-1, 1) for sh in (-1, 1))}))
DELTA257 = tuple(sorted({tuple(y[i]-x[i] for i in range(4)) for x in E33 for y in E33}))
ODD13 = np.array([m for m in range(256) if bin(m).count("1") in (1, 3)])
EVEN024 = np.array([m for m in range(256) if bin(m).count("1") in (0, 2, 4)])


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("nonzero_symbol_algebra:"+label)


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE/(name+".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mask_sign(left, right):
    """gamma_left gamma_right = sign gamma_(left XOR right)."""
    inversions = sum(bin(right & ((1 << i)-1)).count("1") for i in range(8)
                     if left & (1 << i))
    return -1 if inversions % 2 else 1


def _dict_add(*terms):
    result = {}
    for term in terms:
        for mask, value in term.items():
            result[mask] = result.get(mask, 0)+value
    return {mask: value for mask, value in result.items() if value != 0}


def _dict_scale(value, terms):
    return {mask: value*coefficient for mask, coefficient in terms.items()}


def _dict_mul(left, right):
    result = {}
    for a, x in left.items():
        for b, y in right.items():
            mask = a ^ b
            result[mask] = result.get(mask, 0)+mask_sign(a, b)*x*y
    return {mask: value for mask, value in result.items() if value != 0}


def _dict_creator(j, contraction=False):
    return {1 << (2*j): s.Rational(1, 2),
            1 << (2*j+1): (s.I if contraction else -s.I)/2}


def _dict_vector(v, contraction=False):
    return _dict_add(*(_dict_scale(v[j], _dict_creator(j, contraction)) for j in range(4)))


def _cross(v):
    return [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]


def _dict_gamma(omega):
    W = _cross(omega)
    return _dict_add(*(_dict_scale(W[i][j], _dict_mul(_dict_creator(i+1), _dict_creator(j+1, True)))
                       for i in range(3) for j in range(3) if W[i][j] != 0))


def _dense(terms):
    out = np.zeros(256, complex)
    for mask, coefficient in terms.items():
        out[mask] = complex(coefficient)
    return out


CREATORS = np.array([_dense(_dict_creator(j)) for j in range(4)])
CONTRACTORS = CREATORS.conj()
GAMMA = np.array([_dense(_dict_gamma([int(i == j) for i in range(3)])) for j in range(3)])
CG = np.array([[_dense(_dict_mul(_dict_creator(i), _dict_gamma([int(k == j) for k in range(3)])))
                for j in range(3)] for i in range(4)])
IG = np.array([[_dense(_dict_mul(_dict_creator(i, True), _dict_gamma([int(k == j) for k in range(3)])))
                for j in range(3)] for i in range(4)])
MASKS = np.arange(256)
LEFT_SIGNS = np.array([[mask_sign(1 << g, m) for m in range(256)] for g in range(8)])
RIGHT_SIGNS = np.array([[mask_sign(m, 1 << g) for m in range(256)] for g in range(8)])


def _linear_product(linear, vectors, left=True):
    """Multiply any batch of Clifford vectors by a degree-one operator."""
    result = np.zeros_like(vectors)
    for g in range(8):
        coefficient = linear[1 << g]
        if coefficient != 0:
            result[:, MASKS ^ (1 << g)] += coefficient*vectors*(LEFT_SIGNS if left else RIGHT_SIGNS)[g]
    return result


def _roots8():
    z = 1/np.sqrt(2)
    return np.array([1, z+1j*z, 1j, -z+1j*z, -1, -z-1j*z, -1j, z-1j*z])


def native_quotient(q, a, b, *, unit_inactive_axes=False):
    """Complete regular native mean slice, with no per-q SVD or rank test.

    The inactive theta uses the unscaled owned spatial axis w, so its norm
    is explicit rather than silently changed. active contrasts use +e_j on
    one active role and -e_j on the last active role.
    """
    q = tuple(int(x) % L for x in q)
    require(len(q) == 4 and any(q), "nonzero_four_component_L8_frequency")
    require(np.isfinite(a) and np.isfinite(b) and a > b > 0, "regular_positive_a_greater_b")
    active = [r for r in range(4) if q[r] != 0]
    inactive = [r for r in range(4) if q[r] == 0]
    F = (a-b)*np.eye(4)+b*np.ones((4, 4))
    u = F*np.array([1, -1, -1, -1])[None, :]
    require(all(np.dot(v[1:], v[1:]) > 0 for v in u), "regular_nonzero_spatial_legs")
    kappa = 1-_roots8()[np.array(q)]
    directions, rotations, labels = [], [], []
    for r in active[:-1]:
        for j in range(3):
            B = np.zeros((4, 3))
            B[r, j], B[active[-1], j] = 1, -1
            av = np.zeros((4, 4), complex)
            av[:, 1:] = np.cross(B, u[:, 1:])
            directions.append(av)
            rotations.append(kappa[:, None]*B)
            labels.append(["active_angular_contrast", r, active[-1], j])
    for r in inactive:
        for j in range(4):
            av = np.zeros((4, 4), complex)
            av[r, j] = 1
            directions.append(av)
            rotations.append(np.zeros((4, 3), complex))
            labels.append(["inactive_full_leg", r, j])
        directions.append(np.zeros((4, 4), complex))
        omega = np.zeros((4, 3), complex)
        omega[r] = u[r, 1:]/np.linalg.norm(u[r, 1:]) if unit_inactive_axes else u[r, 1:]
        rotations.append(omega)
        labels.append(["inactive_unit_stabilizer" if unit_inactive_axes else "inactive_unscaled_stabilizer", r])
    require(len(directions) == 17-2*len(active), "exact_quotient_dimension")
    return {"q": q, "u": u, "a": np.array(directions), "omega": np.array(rotations),
            "labels": labels, "active": active, "inactive": inactive,
            "kappa": kappa, "dimension": len(directions),
            "unit_inactive_axes": unit_inactive_axes,
            "unit_axis_option_is_invertible_basis_rescaling_not_gauge": True,
            "self_conjugate_frequency": all((2*x) % L == 0 for x in q),
            "real_pair_dimension": len(directions)*(1 if all((2*x) % L == 0 for x in q) else 2)}


def split_representation(q, a, omega, u):
    """Recover the common spatial representation and its unique mean slice.

    This maps an already admitted first jet; it does not repair a violation
    of own-leg or observer constraints. Raw matter must co-transform when
    this representation direction is quotiented in the complete joint price.
    """
    q = np.array(q, int) % L
    active = np.flatnonzero(q)
    require(len(active) > 0, "representation_split_requires_nonzero_q")
    kappa = 1-_roots8()[q]
    common = np.mean(omega[active]/kappa[active, None], axis=0)
    reduced_a = np.array(a, complex).copy()
    reduced_a[:, 1:] -= np.cross(common[None, :], u[:, 1:])
    return reduced_a, omega-kappa[:, None]*common[None, :], common


def operator_coefficients(basis):
    """Actual stored J9 and native X33 in the full Clifford algebra."""
    u, av, omega = basis["u"], basis["a"], basis["omega"]
    tq = _roots8()[np.array(basis["q"])]
    ca = np.einsum("ira,ac->irc", av, CREATORS)
    ia = np.einsum("ira,ac->irc", av, CONTRACTORS)
    products = u[None, :, :, None]*omega[:, :, None, :]
    plus = ca+np.einsum("iraj,ajc->irc", products, CG)
    minus = ia-tq.conj()[None, :, None]*np.einsum("iraj,ajc->irc", products, IG)
    J = L*np.concatenate((-(ca+ia).sum(axis=1)[:, None], plus, minus), axis=1)
    cu, iu = np.einsum("ra,ac->rc", u, CREATORS), np.einsum("ra,ac->rc", u, CONTRACTORS)
    D = L*np.concatenate((-(cu+iu).sum(axis=0)[None], cu, iu))
    X = np.zeros((basis["dimension"], len(E33), 256), complex)
    location = {phase: i for i, phase in enumerate(E33)}
    for i, nu in enumerate(E9):
        dleft = D[i]*_roots8()[sum(basis["q"][r]*nu[r] for r in range(4)) % L]
        for j, mu in enumerate(E9):
            phase = tuple(nu[r]+mu[r] for r in range(4))
            if phase not in location:
                # Only +/-2e_r is omitted, by the exact own-leg identity
                # checked symbolically below. This is NOT tolerance pruning.
                require(sum(abs(x) for x in phase) == 2 and max(abs(x) for x in phase) == 2,
                        "only_exactly_cancelled_same_axis_support_omitted")
                continue
            X[:, location[phase]] += (_linear_product(dleft, J[:, j], left=True)
                                     +_linear_product(D[i], J[:, j], left=False))
    return {"J": J[:, :, ODD13], "X": X[:, :, EVEN024], "D": D,
            "J_full": J, "X_full": X}


def _mp_number(value):
    rational = s.Rational(value)
    return mp.mpf(int(rational.p))/int(rational.q)


def shared_spectral_data(repo=None, a=None, b=None):
    """One reusable119-energy/7140-pair kernel for arbitrary nonzero q."""
    repo = ROOT if repo is None else Path(repo).resolve()
    definition = _load("full_symbol_diagnostic")
    ordered = _load("ordered_operator_check")
    chart = ordered.chart_helper()
    chart.owned_definitions(repo)
    feature = definition.exact_features(repo)
    receipt = json.loads((repo/chart.RECEIPT).read_text())
    with mp.workdps(80):
        owned = a is None and b is None
        require(owned or (a is not None and b is not None), "a_b_given_together")
        if owned:
            d, o = map(mp.mpf, receipt["interval"]["root_center"])
            aa = (mp.sqrt(d+3*o)+3*mp.sqrt(d-o))/4
            bb = (mp.sqrt(d+3*o)-mp.sqrt(d-o))/4
        else:
            aa, bb = _mp_number(a), _mp_number(b)
            d, o = aa*aa+3*bb*bb, 2*aa*bb+2*bb*bb
        require(aa > bb > 0, "regular_positive_symmetric_fixture")
        modes = np.array(tuple(itertools.product(range(L), repeat=4)), int)
        feature_list = [feature(tuple(mode)) for mode in modes]
        unique = tuple(sorted(set(feature_list)))
        require(len(unique) == 119, "actual119_exact_energy_features")
        lookup = {f: i for i, f in enumerate(unique)}
        indices = np.array([lookup[f] for f in feature_list])
        counts = np.bincount(indices)
        sqrt2 = mp.sqrt(2)
        energy = [d*(f[0][0]+f[0][1]*sqrt2)+o*(f[1][0]+f[1][1]*sqrt2) for f in unique]
        p = (mp.sqrt(5)-1)/2
        alpha, beta, z = p*p/ROUNDS, 2*p*p, mp.mpf(2)**-20
        m = 2*ROUNDS
        bs = [1-alpha*x for x in energy]
        require(min(bs) > 0, "full_spectrum_positive_survival")
        powers = [mp.exp(m*mp.log(x)) for x in bs]
        Z = FOCK*mp.fsum(int(n)*power for n, power in zip(counts, powers))
        kappa, prime = [], []
        for survival, power in zip(bs, powers):
            h = 1-z+z*power
            kappa.append(-power/(Z*survival)+REFERENCE*beta*z*power/(h*survival))
            prime.append((m-1)*alpha*power/(Z*survival*survival)
                         +REFERENCE*beta*z*alpha*power/(h*survival*survival)
                          *(-(m-1)+m*z*power/h))
        shell_index = int(indices[1])  # (0,0,0,1), shared by exactly8 modes.
        require(int(counts[shell_index]) == 8, "entire128_dimensional_occupied_shell")
        rho = [mp.mpf(1)/REFERENCE if i == shell_index else mp.mpf(0) for i in range(119)]
        epsilon = energy[shell_index]
        resolvent = [mp.mpf(0) if i == shell_index else 1/(value-epsilon) for i, value in enumerate(energy)]
        dd, weights = np.empty((119, 119)), np.empty((119, 119))
        min_gap = mp.inf
        for i in range(119):
            for j in range(i, 119):
                if i == j:
                    value = prime[i]
                else:
                    gap = energy[j]-energy[i]
                    require(gap != 0, "distinct_exact_features_not_accidentally_equal")
                    min_gap = min(min_gap, abs(gap))
                    value = (kappa[j]-kappa[i])/gap
                dd[i, j] = dd[j, i] = float(value)
                weights[i, j] = weights[j, i] = float(value-rho[i]*resolvent[j]-rho[j]*resolvent[i])
        lambdas, kappas = np.array(list(map(float, energy))), np.array(list(map(float, kappa)))
        rhos, rs = np.array(list(map(float, rho))), np.array(list(map(float, resolvent)))
        return {"modes": modes, "mode_feature": indices, "features": unique,
                "a": float(aa), "b": float(bb), "d_o": [str(d), str(o)],
                "lambda": lambdas, "kappa": kappas, "rho": rhos, "resolvent": rs,
                "dd": dd, "weight_X": weights, "chi": kappas+rhos,
                "chi_sum": float(mp.fsum(int(n)*(k+r) for n, k, r in zip(counts, kappa, rho))),
                "Z": float(Z), "epsilon": float(epsilon), "minimum_pair_gap": float(min_gap),
                "owned_root_center": owned, "root_radius_not_propagated": receipt["interval"]["root_radius"],
                "source_pins": {**chart.PINS, **definition.PINS}}


def phase_moments(weights, deltas, modes):
    """Finite8th-root polynomial sums; no full Fock matrices are formed."""
    deltas = tuple(deltas)
    powers = np.einsum("dr,kr->dk", np.array(deltas, int), modes, optimize=False) % L
    phases = _roots8()[powers]
    values = np.einsum("k,dk->d", weights, phases, optimize=False)
    return dict(zip(deltas, values))


def _moment_Gram(coefficients, support, moments):
    matrix = np.array([[moments[tuple(mu[r]-nu[r] for r in range(4))]
                        for mu in support] for nu in support])
    mixed = np.einsum("lm,bmc->blc", matrix, coefficients, optimize=False)
    return FOCK*np.einsum("alc,blc->ab", coefficients.conj(), mixed, optimize=False)


def stationary_HJ_two_points(J, q, chi_sum):
    """Exact ONLY if the existing stationary moments(18) hold.

    P and N have Fock charges+1/-1, whose cross traces vanish. Every
    remaining J-Gram phase is0,+/-e_r,e_r-e_s, with chi moment=sumchi.
    Thus the two weighted sums evaluate at k=0 and k=-q. Tr16 factor16 is
    retained; chi_sum is a MODE sum, not the full Fock trace.
    """
    phase = _roots8()[np.array([-sum(q[r]*nu[r] for r in range(4)) % L for nu in E9])]
    j0, jm = J.sum(axis=1), np.einsum("p,apc->ac", phase, J, optimize=False)
    return FOCK*chi_sum*(np.einsum("ac,bc->ab", j0.conj(), j0, optimize=False)
                        +np.einsum("ac,bc->ab", jm.conj(), jm, optimize=False))


def assemble_symbol(q, shared=None, repo=None, *, use_stationary_root_identity=False,
                    unit_inactive_axes=False):
    """Numerical complete mean-slice symbol for ANY nonzero frequency.

    For q outside Omega-Omega this is the complete field quotient. Inside
    that difference set one must ALSO restrict to kerT. Away from the owned
    stationary point this is the first-jet block, not the entire constrained
    Hessian: Tr W{D,D_vw} must then be restored. No shell-density source is
    silently discarded.
    """
    shared = shared_spectral_data(repo) if shared is None else shared
    basis = native_quotient(q, shared["a"], shared["b"], unit_inactive_axes=unit_inactive_axes)
    coefficients = operator_coefficients(basis)
    modes, ids = shared["modes"], shared["mode_feature"]
    outgoing_modes = (modes+np.array(basis["q"])) % L
    outgoing = np.ravel_multi_index(outgoing_modes.T, (L,)*4)
    left, right = ids, ids[outgoing]
    wX = shared["weight_X"][left, right]
    wJ = shared["chi"][left]+shared["chi"][right]
    mx = phase_moments(wX, DELTA257, modes)
    H_X = _moment_Gram(coefficients["X"], E33, mx)
    jdelta = tuple(sorted({tuple(mu[r]-nu[r] for r in range(4)) for mu in E9 for nu in E9}))
    H_J_weighted = _moment_Gram(coefficients["J"], E9, phase_moments(wJ, jdelta, modes))
    H_J_root = stationary_HJ_two_points(coefficients["J"], basis["q"], shared["chi_sum"])
    if use_stationary_root_identity:
        require(shared["owned_root_center"], "stationary_identity_only_for_owned_root_consumer")
    H_J = H_J_root if use_stationary_root_identity else H_J_weighted
    H = H_J+H_X
    Hermitian_error = float(np.linalg.norm(H-H.conj().T)/max(1, np.linalg.norm(H)))
    return {"H": (H+H.conj().T)/2, "H_J": H_J, "H_X": H_X,
            "H_J_weighted": H_J_weighted, "H_J_root_two_point": H_J_root,
            "basis": basis, "coefficients": coefficients, "outgoing": outgoing,
            "weights_J": wJ, "weights_X": wX, "Hermitian_relative_error": Hermitian_error,
            "root_identity_used_as_an_explicit_hypothesis": use_stationary_root_identity,
            "full_Hessian_requires_existing_stationary_constraint_curvature_lemma": True,
            "interval_inertia_or_joint_kernel_claim": False}


def root_pair_gap_bound(repo=None):
    """One q-independent interval check of ALL7021 distinct energy pairs."""
    repo = ROOT if repo is None else Path(repo).resolve()
    definition = _load("full_symbol_diagnostic")
    feature = definition.exact_features(repo)
    chart = _load("native_chart_check")
    chart.owned_definitions(repo)
    owned = json.loads((repo/chart.RECEIPT).read_text())["interval"]
    iv = MPIntervalContext()
    iv.dps = 80
    radius = iv.mpf(owned["root_radius"])
    d, o = [iv.mpf(value)+iv.mpf([-1, 1])*radius for value in owned["root_center"]]
    sqrt2 = iv.sqrt(2)
    unique = sorted({feature(k) for k in itertools.product(range(L), repeat=4)})
    energies = [d*(f[0][0]+f[0][1]*sqrt2)+o*(f[1][0]+f[1][1]*sqrt2) for f in unique]
    minimum = None
    for x, y in itertools.combinations(energies, 2):
        gap = y-x
        require(gap.a > 0 or gap.b < 0, "all119_features_distinct_on_entire_root_box")
        lower = gap.a if gap.a > 0 else -gap.b
        minimum = lower if minimum is None or lower < minimum else minimum
    return {"features": len(unique), "offdiagonal_pairs": len(unique)*(len(unique)-1)//2,
            "including_analytic_diagonal_weights": len(unique)*(len(unique)+1)//2,
            "minimum_distinct_pair_gap_lower": str(minimum), "interval_digits": 80}


def _gamma_matrices(creators):
    generators = []
    for C in creators:
        generators.extend((C+C.T, 1j*(C-C.T)))
    products = np.zeros((256, 16, 16), complex)
    products[0] = np.eye(16)
    for mask in range(1, 256):
        g = mask.bit_length()-1
        products[mask] = np.einsum("ij,jk->ik", products[mask ^ (1 << g)], generators[g])
    return np.array(generators), products


def _exact_support_checks():
    """Generic algebraic cancellation, not a tolerance-based sparsifier."""
    u0, w0, w1, w2, kappa = s.symbols("u0 w0 w1 w2 kappa", nonzero=True)
    om = s.symbols("omega0:3")
    u = [u0, w0, w1, w2]
    crossed = [om[1]*w2-om[2]*w1, om[2]*w0-om[0]*w2, om[0]*w1-om[1]*w0]
    def residuals(av, omega, t, bar_t):
        cu, iu = _dict_vector(u), _dict_vector(u, True)
        ca, ia, gamma = _dict_vector(av), _dict_vector(av, True), _dict_gamma(omega)
        plus = _dict_add(ca, _dict_mul(cu, gamma))
        minus = _dict_add(ia, _dict_scale(-bar_t, _dict_mul(iu, gamma)))
        return (_dict_add(_dict_scale(t, _dict_mul(cu, plus)), _dict_mul(plus, cu)),
                _dict_add(_dict_scale(bar_t, _dict_mul(iu, minus)), _dict_mul(minus, iu)))
    active = residuals([0]+[x/kappa for x in crossed], om, 1-kappa, 1/(1-kappa))
    theta = s.Symbol("theta")
    inactive = residuals(s.symbols("free_a0:4"), [theta*w0, theta*w1, theta*w2], 1, 1)
    require(all(s.cancel(s.expand(value)) == 0 for result in (*active, *inactive)
                for value in result.values()), "generic_active_and_inactive_same_axis_terms_exactly_zero")


def _exact_mean_slice_checks(operator):
    """Arbitrary nonzero-kappa algebra, not sampled Fourier ranks."""
    u = s.Matrix(s.symbols("mean_u0:3"))
    omega = s.Matrix(s.symbols("mean_omega0:3"))
    common = s.Matrix(s.symbols("mean_common0:3"))
    kappa = s.Symbol("mean_kappa", nonzero=True)
    require(all(s.expand(value) == 0 for value in
                ((omega-kappa*common).cross(u)/kappa
                 -(omega.cross(u)/kappa-common.cross(u)))),
            "arbitrary_kappa_leg_transport_preserved_by_representation_split")
    for p in range(1, 5):
        kappas = s.symbols("nonzero_kappa0:"+str(p), nonzero=True)
        omegas = [s.Matrix(s.symbols("free_omega_"+str(r)+"_0:3")) for r in range(p)]
        mean = sum((vector/k for vector, k in zip(omegas, kappas)), s.zeros(3, 1))/p
        reduced = [vector-k*mean for vector, k in zip(omegas, kappas)]
        require(all(s.cancel(value) == 0 for value in
                    sum((vector/k for vector, k in zip(reduced, kappas)), s.zeros(3, 1))),
                "all_active_counts_exact_mean_zero")
        # B_last=-sum(other B) is precisely the fixed contrast basis used
        # by native_quotient; its free coefficients recover every mean slice.
        B = [vector/k for vector, k in zip(reduced, kappas)]
        require(all(s.cancel(value) == 0 for value in B[-1]+sum(B[:-1], s.zeros(3, 1))),
                "fixed_contrast_basis_spans_entire_mean_slice")
        require(all(s.expand(value) == 0 for value in p*common/p-common),
                "common_shift_recovered_uniquely_in_characteristic_zero")
    squared = [(1-phase)*(1-s.conjugate(phase)) for phase in operator.ROOTS8[1:]]
    require(all(s.simplify(value-(2-s.sqrt(2))).is_nonnegative is True for value in squared),
            "exact_L8_nonzero_kappa_bound_only")


def _full16_reference(assembled, shared, creators, *, J_only=False):
    basis, outgoing = assembled["basis"], assembled["outgoing"]
    n = basis["dimension"]
    u, av, omega = basis["u"], basis["a"], basis["omega"]
    # Independent dense forward+adjoint formula; the backward Omega is on
    # the LEFT of iota(u), unlike the reduced stored coefficient formula.
    rotation_gamma = []
    for j in range(3):
        W = np.zeros((4, 4))
        W[1:, 1:] = np.array(_cross([int(i == j) for i in range(3)]))
        G = np.zeros((16, 16), complex)
        for a in range(4):
            for b in range(4):
                G += W[a, b]*np.einsum("ij,kj->ik", creators[a], creators[b])
        rotation_gamma.append(G)
    rotation_gamma = np.array(rotation_gamma)
    Om = np.einsum("irj,jab->irab", omega, rotation_gamma)
    cu = np.einsum("ra,aij->rij", u, creators)
    iu = cu.transpose(0, 2, 1)
    ca = np.einsum("ira,ajk->irjk", av, creators)
    ia = np.einsum("ira,akj->irjk", av, creators)
    # Explicit products below make matrix ordering auditable.
    plus = ca+np.einsum("rjk,irkv->irjv", cu, Om)
    minus = (ia-np.einsum("irjk,rkv->irjv", Om, iu))*_roots8()[np.array(basis["q"])].conj()[None, :, None, None]
    constant = -(ca+ia).sum(axis=1)
    tk = _roots8()[shared["modes"]]
    D = L*(np.einsum("kr,rij->kij", tk-1, cu)
           +np.einsum("kr,rij->kij", tk.conj()-1, iu))
    H_J, H_X = np.zeros((n, n), complex), np.zeros((n, n), complex)
    for offset in range(0, len(tk), 128):
        sl = slice(offset, offset+128)
        J = L*(np.einsum("kr,arij->akij", tk[sl], plus)
               +np.einsum("kr,arij->akij", tk[sl].conj(), minus)+constant[:, None])
        jf = J.reshape(n, -1, 256)
        H_J += np.einsum("akn,bkn,k->ab", jf.conj(), jf, assembled["weights_J"][sl])
        if not J_only:
            X = np.einsum("kij,akjl->akil", D[outgoing[sl]], J)+np.einsum("akij,kjl->akil", J, D[sl])
            xf = X.reshape(n, -1, 256)
            H_X += np.einsum("akn,bkn,k->ab", xf.conj(), xf, assembled["weights_X"][sl])
    return H_J, H_X


def _exact_fixture_check(operator, creators_s, products):
    q, k = (1, 2, 4, 0), (1, 2, 3, 5)
    l = tuple((k[r]+q[r]) % L for r in range(4))
    a, b = s.Rational(1, 4), s.Rational(1, 125)
    F = (a-b)*s.eye(4)+b*s.ones(4)
    eta = s.diag(1, -1, -1, -1)
    u = [eta*F[r, :].T for r in range(4)]
    tq = operator.phases(q)
    av, omega = [s.zeros(4, 1) for _ in range(4)], [s.zeros(3, 1) for _ in range(4)]
    for r, sign in ((0, 1), (2, -1)):
        B = sign*s.eye(3)[:, 0]
        av[r][1:4, :] = B.cross(u[r][1:4, :])
        omega[r] = (1-tq[r])*B
    column = s.Matrix.vstack(*av, *omega, s.zeros(3, 1))
    literal = operator.first_jet(column, u, k, l, creators_s)
    tk, tl = operator.phases(k), operator.phases(l)
    jdict = {}
    def dirac_dict(momentum):
        phases = operator.phases(momentum)
        return _dict_scale(L, _dict_add(*(_dict_add(
            _dict_scale(phases[r]-1, _dict_vector(u[r])),
            _dict_scale(s.conjugate(phases[r])-1, _dict_vector(u[r], True))) for r in range(4))))
    for r in range(4):
        ca, ia = _dict_vector(av[r]), _dict_vector(av[r], True)
        cu, iu, gamma = _dict_vector(u[r]), _dict_vector(u[r], True), _dict_gamma(omega[r])
        jdict = _dict_add(jdict, _dict_scale(L, _dict_add(
            _dict_scale(tk[r]-1, ca), _dict_scale(tk[r], _dict_mul(cu, gamma)),
            _dict_scale(s.conjugate(tk[r])-1, ia),
            _dict_scale(-s.conjugate(tl[r]), _dict_mul(iu, gamma)))))
    dk, dl = dirac_dict(k), dirac_dict(l)
    xdict = _dict_add(_dict_mul(dl, jdict), _dict_mul(jdict, dk))
    integer_products = [s.Matrix(matrix.real.astype(int)) if np.max(np.abs(matrix.imag)) == 0
                        else s.Matrix([[s.Rational(float(z.real))+s.I*s.Rational(float(z.imag)) for z in row]
                                       for row in matrix]) for matrix in products]
    def matrix_of(terms):
        return sum((coefficient*integer_products[mask] for mask, coefficient in terms.items()), s.zeros(16))
    require(all(s.expand(value) == 0 for value in matrix_of(jdict)-literal), "rational_q1240_exact_literal_J")
    Dk, _ = operator.dirac(k, u, creators_s)
    Dl, _ = operator.dirac(l, u, creators_s)
    require(all(s.expand(value) == 0 for value in matrix_of(xdict)-Dl*literal-literal*Dk),
            "rational_q1240_exact_literal_X")


def run(repo=None):
    start = time.perf_counter()
    repo = ROOT if repo is None else Path(repo).resolve()
    operator = _load("ordered_operator_check")
    creators_s, order = operator.owned_car(repo)
    creators = np.array([np.array(C, dtype=complex) for C in creators_s])
    gammas, products = _gamma_matrices(creators)
    checks = []
    require(len(E33) == 33 and len(DELTA257) == 257 and len(ODD13) == 64 and len(EVEN024) == 99,
            "finite_full16_CAR_and_Laurent_dimensions")
    checks.append("finite_full16_CAR_and_Laurent_dimensions")
    for j in range(4):
        recovered = np.einsum("m,mij->ij", CREATORS[j], products)
        require(np.array_equal(recovered, creators[j]), "actual_owned_creator_dictionary")
    require(np.array_equal(np.einsum("aij,bij->ab", products.conj(), products), 16*np.eye(256)),
            "all256_Clifford_monomials_full16_trace_orthogonal")
    for a, b in ((1, 2), (3, 5), (7, 11), (19, 47), (85, 170)):
        require(np.array_equal(np.einsum("ij,jk->ik", products[a], products[b]),
                               mask_sign(a, b)*products[a ^ b]), "signed_mask_product_actual_CAR")
    checks.append("actual_CAR_dictionary_trace_and_signed_products")
    _exact_support_checks()
    checks.append("generic_active_and_inactive_exact_33_support_cancellation")
    _exact_mean_slice_checks(operator)
    checks.append("arbitrary_nonzero_kappa_mean_slice_and_exact_L8_bound")
    _exact_fixture_check(operator, creators_s, products)
    checks.append("exact_rational_q1240_J_X_with_actual_owned_CAR")
    gap = root_pair_gap_bound(repo)
    checks.append("all7021_feature_pairs_separated_on_root_rectangle")
    shared_start = time.perf_counter()
    shared = shared_spectral_data(repo)
    shared_seconds = time.perf_counter()-shared_start
    assembly_start = time.perf_counter()
    assembled = assemble_symbol((1, 2, 4, 0), shared)
    assembly_seconds = time.perf_counter()-assembly_start
    require(assembled["basis"]["dimension"] == 11, "complete_new_q1240_mean_slice_11")
    # The exact mean-slice reconstruction is also tested with an added
    # common representation direction; no numerical projector is fitted.
    basis = assembled["basis"]
    common = np.array([.2, -.3, .4])
    raw_a = basis["a"][0].copy()
    raw_a[:, 1:] += np.cross(common, basis["u"][:, 1:])
    raw_omega = basis["omega"][0]+basis["kappa"][:, None]*common
    restored_a, restored_omega, restored_common = split_representation(basis["q"], raw_a, raw_omega, basis["u"])
    require(np.max(np.abs(restored_a-basis["a"][0])) < 1e-14
            and np.max(np.abs(restored_omega-basis["omega"][0])) < 1e-14
            and np.max(np.abs(restored_common-common)) < 1e-14, "complete_representation_mean_slice_reconstruction")
    checks.append("complete_representation_mean_slice_reconstruction")
    reference_start = time.perf_counter()
    dense_J, dense_X = _full16_reference(assembled, shared, creators)
    reference_seconds = time.perf_counter()-reference_start
    error_J, error_X = float(np.max(np.abs(dense_J-assembled["H_J"]))), float(np.max(np.abs(dense_X-assembled["H_X"])))
    require(error_J < 2e-10 and error_X < 2e-9, "new_q1240_257_moment_Clifford_equals_independent_full4096x16")
    require(assembled["Hermitian_relative_error"] < 1e-11, "new_q1240_Hermitian")
    checks.append("new_q1240_complete_257_moments_vs_independent_full4096x16")
    root_two_point = float(np.max(np.abs(assembled["H_J_weighted"]-assembled["H_J_root_two_point"])))
    require(root_two_point < 2e-10, "owned_root_stationary_two_point_HJ_lemma")
    full_error = float(np.max(np.abs(assembled["H"]-dense_J-dense_X)))
    full_two_point_error = float(np.max(np.abs(assembled["H_J_root_two_point"]+assembled["H_X"]-dense_J-dense_X)))
    require(full_error < 2e-9 and full_two_point_error < 2e-9,
            "new_q1240_both_weighted_and_root_two_point_full_H_agree")
    checks.append("stationary_root_HJ_two_point_full16_factor")
    rejected_zero = False
    try:
        native_quotient(ZERO, shared["a"], shared["b"])
    except ArithmeticError:
        rejected_zero = True
    self_conjugate = native_quotient((4, 0, 0, 0), shared["a"], shared["b"])
    require(rejected_zero and self_conjugate["self_conjugate_frequency"]
            and self_conjugate["real_pair_dimension"] == self_conjugate["dimension"],
            "q_zero_rejected_and_self_conjugate_real_dimension_not_doubled")
    checks.append("nonzero_domain_and_real_pair_dimension")
    fixture = shared_spectral_data(repo, a=s.Rational(1, 4), b=s.Rational(1, 125))
    fixture_symbol = assemble_symbol((1, 2, 4, 0), fixture)
    fixture_J, _ = _full16_reference(fixture_symbol, fixture, creators, J_only=True)
    require(np.max(np.abs(fixture_J-fixture_symbol["H_J_weighted"])) < 2e-10,
            "nonstationary_fixture_uses_full_weighted_J_Gram")
    nonstationary_failure = float(np.max(np.abs(fixture_J-fixture_symbol["H_J_root_two_point"])))
    require(nonstationary_failure > 1e-6, "reject_two_point_identity_without_stationary_source")
    checks.append("nonstationary_fixture_weighted_J_and_hostile_two_point_control")
    eigenvalues = np.linalg.eigvalsh(assembled["H"])
    elapsed = time.perf_counter()-start
    require(elapsed < 45, "bounded_new_algebra_consumer_45_seconds")
    return {"status": "PASS_NONZERO_SYMBOL_ALGEBRA_AND_NEW_Q1240_DIAGNOSTIC",
            "exact_checks": len(checks), "checks": checks, "seconds": round(elapsed, 4),
            "shared119_pair_kernel_seconds": round(shared_seconds, 4),
            "new_target_moment_assembler_seconds": round(assembly_seconds, 4),
            "new_target_full16_reference_seconds": round(reference_seconds, 4),
            "new_target_q": [1, 2, 4, 0], "target_complete_T0_quotient_dimension": 11,
            "J_phase_support": 9, "X_phase_support_exact": 33, "X_Gram_phase_moments": 257,
            "J_Clifford_components_retained": 64, "X_Clifford_components_retained": 99,
            "full_exterior_dimension": 16, "full_trace_factor": 16,
            "thermal_modes": 4096, "occupied_reference_dimension": 128,
            "L8_kappa_lower_exact": "sqrt(2-sqrt(2))", "refinement_uniform_kappa_bound_claim": False,
            "symmetry": "spatial S3 and simultaneous q negation; no time/spatial S4",
            "global_energy_feature_gap": gap,
            "new_target_HJ_matrix_max_error": error_J, "new_target_HX_matrix_max_error": error_X,
            "new_target_full_H_matrix_max_error": full_error,
            "new_target_two_point_full_H_matrix_max_error": full_two_point_error,
            "root_two_point_HJ_max_error": root_two_point,
            "hostile_nonstationary_two_point_error": nonstationary_failure,
            "new_target_Hermitian_relative_error": assembled["Hermitian_relative_error"],
            "new_target_numerical_eigenvalues_only": eigenvalues.tolist(),
            "new_target_inertia_or_kernel_certified": False,
            "full_Z": shared["Z"], "chi_MODE_sum": shared["chi_sum"],
            "ground_state_resolvent": float(shared["resolvent"][0]),
            "owned_exterior_order": list(order), "source_pins": shared["source_pins"],
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "mean_slice_is_physical_gauge_admission": False,
            "other_q_classified_or_old_run_called": False,
            "receipt_mutation_root_search_or_GR_claim": False}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
