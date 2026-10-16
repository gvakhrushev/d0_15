"""Numerical full-Y pure-memory field symbol, not an interval certificate.

The complete old scalar heat moments are reused, never an old run().  Only
the <=16 occupied incoming/predecessor nodes carry full16 matrices.  The
actual canonical sphere/return mixed second jet is retained.  All signs of
the Q resolvent, fullZ, reference128 and16 Fock coordinates remain.

API prepare_shared(repo=None), pure_field_symbol(q,shared=None,repo=None),
matter_operator(q,v,shared=None,repo=None,symbol=None), run(repo=None).
Only q outside Omega-Omega has an automatic zero shell-compatibility row;
inside it this API supplies the field block, not a kerT restriction.
"""
from __future__ import annotations

import os
for _key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"

import hashlib
import importlib.util
import json
from pathlib import Path
import time

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
L, FOCK, REFERENCE = 8, 16, 128
PINS = {
    "nonzero_symbol_algebra.py": "b74c1a10ab6e1051dfb50942abf019cb19aeb890460bc98b919d2e848deecba1",
    "ordered_operator_check.py": "f2f9903685c2c522d4c850d335dfb9435c932182962402da499ff8a7a10a9418",
    "native_chart_check.py": "1cb2bd82796634b414b76a5396b629c98c3679aee3ce7aa63dfc34647ab84b65",
    "full_symbol_diagnostic.py": "6084660c02a1012a4beb619e71e61015dda0d7ebb44207bf6faa7d5281404b25",
}


def require(value, label):
    if not bool(value):
        raise ArithmeticError("pure_memory_symbol:" + label)


def _load(name):
    path = HERE / (name + ".py")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[path.name],
            "immutable_definition:" + name)
    spec = importlib.util.spec_from_file_location("pure_memory_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _cross(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]], complex)


def _dagger(value):
    return value.conj().swapaxes(-1, -2)


def _mm(left, right):
    # Avoid the platform BLAS path for these bounded tiny products.
    if right.ndim == 1:
        return np.einsum("ij,j->i", left, right, optimize=False)
    return np.einsum("ij,jk->ik", left, right, optimize=False)


def _hermitian_error(value):
    return float(np.linalg.norm(value - _dagger(value)) / max(1, np.linalg.norm(value)))


def _decorate(spectral, repo):
    algebra, ordered = _load("nonzero_symbol_algebra"), _load("ordered_operator_check")
    _load("native_chart_check")
    _load("full_symbol_diagnostic")
    creators_s, order = ordered.owned_car(repo)  # AST defining nodes only.
    creators = np.array([np.array(value, complex) for value in creators_s])
    _, products = algebra._gamma_matrices(creators)
    chi = np.zeros(16, complex)
    chi[1] = chi[15] = 1 / np.sqrt(2)
    shell = tuple(tuple(sign if r == a else 0 for r in range(4))
                  for a in range(4) for sign in (1, 7))
    differences = {tuple((x[r] - y[r]) % L for r in range(4)) for x in shell for y in shell}
    gamma = []
    for j in range(3):
        W = np.zeros((4, 4), complex)
        W[1:, 1:] = _cross(np.eye(3)[j])
        gamma.append(sum((W[a, b] * _mm(creators[a], creators[b].T)
                          for a in range(4) for b in range(4)), np.zeros((16, 16), complex)))
    return {"pure_memory_prepared": True, "spectral": spectral, "algebra": algebra,
            "creators": creators, "clifford_products": products, "gamma_axes": np.array(gamma),
            "chi": chi, "shell": shell, "shell_differences": differences, "repo": Path(repo),
            "source_pins": {**PINS, **spectral["source_pins"]}, "exterior_order": order}


def prepare_shared(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    algebra = _load("nonzero_symbol_algebra")
    return _decorate(algebra.shared_spectral_data(repo), repo)


def _shared(shared, repo):
    if shared is None:
        return prepare_shared(repo)
    if shared.get("pure_memory_prepared"):
        return shared
    return _decorate(shared, ROOT if repo is None else Path(repo).resolve())


def canonical_chart_components(basis):
    """Invert the first jet to the actual additive-radius/sphere/spin chart."""
    u, av, omega = basis["u"], basis["a"], basis["omega"]
    rho = np.linalg.norm(u[:, 1:], axis=1)
    z = u[:, 1:] / rho[:, None]
    radial = np.einsum("rj,irj->ir", z, av[:, :, 1:])
    beta = (av[:, :, 1:] - radial[:, :, None] * z[None]) / rho[None, :, None]
    theta = np.einsum("rj,irj->ir", z, omega)
    reconstructed = basis["kappa"][None, :, None] * np.cross(z[None], beta) + theta[:, :, None] * z[None]
    return {"rho": rho, "z": z, "radial": radial, "beta": beta, "theta": theta,
            "tau": av[:, :, 0],
            "first_link_reconstruction_error": float(np.max(np.abs(reconstructed - omega)))}


def mixed_second_chart(basis, shared):
    """Actual D_ij,0, with row i conjugate and column j unconjugated.

    D2 coefficients are F2_ij+F2_ji^dagger, not F2+F2^dagger entrywise.
    K2 is the mixed logarithmic one-body jet, a skew4x4 matrix. The
    exterior jet retains its quadratic representation term.
    """
    u, av, omega = basis["u"], basis["a"], basis["omega"]
    chart = canonical_chart_components(basis)
    n = basis["dimension"]
    creators, gammas = shared["creators"], shared["gamma_axes"]
    create = lambda v: np.einsum("a,aij->ij", v, creators, optimize=False)
    lift = lambda W: np.einsum("a,aij->ij", np.array([W[2, 1], W[0, 2], W[1, 0]]), gammas,
                                optimize=False)
    # lift(W) below is used only for skew matrices. For the logarithmic K2
    # this follows from differentiating an actual SO3 return, not a choice.
    Fconstant = np.zeros((n, n, 16, 16), complex)
    Fplus = np.zeros((n, n, 4, 16, 16), complex)
    u2_all = np.zeros((n, n, 4, 4), complex)
    K2_all = np.zeros((n, n, 4, 4, 4), complex)
    expression = np.zeros((n, n), complex)
    sum_u = u.sum(axis=0)
    phases = shared["algebra"]._roots8()[np.array(basis["q"])]
    for i in range(n):
        for j in range(n):
            for r in range(4):
                z, rho = chart["z"][r], chart["rho"][r]
                bA, bB = chart["beta"][j, r], chart["beta"][i, r].conj()
                thA, thB = chart["theta"][j, r], chart["theta"][i, r].conj()
                aA, aB = av[j, r], av[i, r].conj()
                drA, drB = chart["radial"][j, r], chart["radial"][i, r].conj()
                u2 = np.r_[0, drA * bB + drB * bA - rho * np.dot(bA, bB) * z]
                VA = _cross((1 - phases[r]) * np.cross(z, bA))
                VB = _cross((1 - phases[r].conjugate()) * np.cross(z, bB))
                Z = _cross(z)
                R2 = (thA * _cross(bB) + thB * _cross(bA) + thA * thB * _mm(Z, Z)
                      + thA * _mm(Z, VB) + thB * _mm(Z, VA)
                      + _cross((phases[r] - phases[r].conjugate()) * np.cross(bA, bB))
                      + (_mm(VA, VB) + _mm(VB, VA)) / 2)
                WA, WB = np.zeros((4, 4), complex), np.zeros((4, 4), complex)
                WA[1:, 1:], WB[1:, 1:] = _cross(omega[j, r]), _cross(omega[i, r].conj())
                R2full = np.zeros((4, 4), complex)
                R2full[1:, 1:] = R2
                K2 = R2full - (_mm(WA, WB) + _mm(WB, WA)) / 2
                GA, GB = lift(WA[1:, 1:]), lift(WB[1:, 1:])
                E2 = lift(K2[1:, 1:]) + (_mm(GA, GB) + _mm(GB, GA)) / 2
                c2 = create(u2)
                product = _mm(create(aA), GB) + _mm(create(aB), GA) + _mm(create(u[r]), E2)
                Fconstant[i, j] -= L * c2
                Fplus[i, j, r] = L * (c2 + product)
                u2_all[i, j, r], K2_all[i, j, r] = u2, K2
                vector = (-4 * _mm(WB, aA) - 4 * _mm(WA, aB)
                          + 2 * u[r] * np.trace(_mm(WA, WB)) - 4 * _mm(K2, u[r]))
                expression[i, j] += 16 * np.dot(u[r], u2) + np.dot(2 * u[r] - sum_u, vector)
    D2 = np.zeros((n, n, 9, 16, 16), complex)
    D2[:, :, 0] = Fconstant + _dagger(Fconstant.swapaxes(0, 1))
    D2[:, :, 1:5] = Fplus
    D2[:, :, 5:9] = _dagger(Fplus.swapaxes(0, 1))
    lambda1 = L * L * (2 - np.sqrt(2))
    closed_curvature = lambda1 * (expression + expression.conj().T) / 64
    inactive = basis["inactive"]
    raw_pure = lambda1 / 2 * (
        _mm(chart["tau"][:, inactive].conj(), chart["tau"][:, inactive].T)
        + _mm(chart["radial"][:, inactive].conj(), chart["radial"][:, inactive].T))
    return {"D2_coefficients": D2, "forward_constant": Fconstant, "forward_plus": Fplus,
            "u2": u2_all, "K2": K2_all, "chart": chart,
            "faithful_curvature_closed": closed_curvature, "raw_pure_closed": raw_pure}


def _phases(support, nodes, algebra):
    return algebra._roots8()[np.einsum("pr,kr->kp", np.array(support, int),
                                     np.array(nodes, int), optimize=False) % L]


def pure_field_symbol(q, shared=None, repo=None):
    """One numerical full-Y symbol, retaining all native first-jet columns."""
    start = time.perf_counter()
    shared = _shared(shared, repo)
    algebra, spectral = shared["algebra"], shared["spectral"]
    assembled = algebra.assemble_symbol(q, shared=spectral)
    basis, coefficients = assembled["basis"], assembled["coefficients"]
    q = basis["q"]
    shell = shared["shell"]
    predecessors = tuple(tuple((k[r] - q[r]) % L for r in range(4)) for k in shell)
    nodes = tuple(sorted(set(shell) | set(predecessors)))
    lookup = {k: i for i, k in enumerate(nodes)}
    incoming = np.array([lookup[k] for k in shell])
    previous = np.array([lookup[k] for k in predecessors])
    product_basis = shared["clifford_products"]
    jp = _phases(algebra.E9, nodes, algebra)
    xp = _phases(algebra.E33, nodes, algebra)
    Jcoef = np.einsum("kp,apc->akc", jp, coefficients["J"], optimize=False)
    Xcoef = np.einsum("kp,apc->akc", xp, coefficients["X"], optimize=False)
    J = np.einsum("akc,cij->akij", Jcoef, product_basis[algebra.ODD13], optimize=False)
    X = np.einsum("akc,cij->akij", Xcoef, product_basis[algebra.EVEN024], optimize=False)
    n = basis["dimension"]
    raw_J = np.zeros((n, n, 16, 16), complex)
    schur = np.zeros_like(raw_J)
    node_schur_weights = []
    for k, at, before in zip(shell, incoming, previous):
        outgoing = tuple((k[r] + q[r]) % L for r in range(4))
        predecessor = nodes[before]
        index_out = np.ravel_multi_index(outgoing, (L,) * 4)
        index_pre = np.ravel_multi_index(predecessor, (L,) * 4)
        rout = spectral["resolvent"][spectral["mode_feature"][index_out]]
        rpre = spectral["resolvent"][spectral["mode_feature"][index_pre]]
        A, B, U, V = J[:, at], J[:, before], X[:, at], X[:, before]
        raw_J += (np.einsum("aji,bjk->abik", A.conj(), A, optimize=False)
                  + np.einsum("bij,akj->abik", B, B.conj(), optimize=False)) / 8
        schur += (rout * np.einsum("aji,bjk->abik", U.conj(), U, optimize=False)
                  + rpre * np.einsum("bij,akj->abik", V, V.conj(), optimize=False)) / 8
        node_schur_weights.append([float(rout), float(rpre)])
    second = mixed_second_chart(basis, shared)
    phase_shell = _phases(algebra.E9, shell, algebra)
    D2 = np.einsum("kp,abpij->abkij", phase_shell, second["D2_coefficients"], optimize=False)
    Dcoef = np.einsum("pc,cij->pij", coefficients["D"], product_basis, optimize=False)
    Dshell = np.einsum("kp,pij->kij", phase_shell, Dcoef, optimize=False)
    curvature = (np.einsum("kij,abkjl->abil", Dshell, D2, optimize=False)
                 + np.einsum("abkij,kjl->abil", D2, Dshell, optimize=False)) / 8
    raw_Y = raw_J + curvature
    M = raw_Y - schur
    chi = shared["chi"]
    ell = lambda value: np.einsum("i,abij,j->ab", chi.conj(), value, chi, optimize=False)
    tr = lambda value: np.trace(value, axis1=-2, axis2=-1) / FOCK
    Ypure, Yfaithful = ell(raw_Y), tr(raw_Y)
    Qpure, Qfaithful = ell(schur), tr(schur)
    Cpure, Cfaithful = ell(curvature), tr(curvature)
    # The spectral curvature is only nine degree-one operator moments.
    # No4096 full16 matrix occurs; this also retains the tiny midpoint
    # stationary residual rather than silently declaring the midpoint exact.
    sums = tuple(sorted({tuple(x[r] + y[r] for r in range(4))
                         for x in algebra.E9 for y in algebra.E9}))
    kappas = spectral["kappa"][spectral["mode_feature"]]
    kmom = algebra.phase_moments(kappas, sums, spectral["modes"])
    PD = np.array([sum((kmom[tuple(nu[r] + mu[r] for r in range(4))] * Dcoef[j]
                       for j, mu in enumerate(algebra.E9)), np.zeros((16, 16), complex))
                   for nu in algebra.E9])
    Cthermal = 2 * np.einsum("pij,abpji->ab", PD, second["D2_coefficients"], optimize=False)
    Hfirst = assembled["H"]
    Hthermal = Hfirst - tr(raw_J) + Qfaithful + Cthermal
    Hfaithful = Hfirst + Cthermal + Cfaithful
    Hpure = Hfaithful + Ypure - Yfaithful - Qpure + Qfaithful
    Hclosed = Hthermal + second["raw_pure_closed"] - Qpure
    hermitian_error = _hermitian_error(Hpure)
    return {"H_pure": (Hpure + Hpure.conj().T) / 2,
            "H_faithful": Hfaithful, "H_faithful_firstjet_root_formula": Hfirst,
            "H_thermal": Hthermal, "H_pure_closed_raw_Y": Hclosed,
            "raw_Y_pure": Ypure, "raw_Y_faithful": Yfaithful,
            "QSchur_pure": Qpure, "QSchur_faithful": Qfaithful,
            "curvature_pure": Cpure, "curvature_faithful": Cfaithful,
            "curvature_difference": Cpure - Cfaithful, "curvature_thermal": Cthermal,
            "Mij": M, "raw_Y_operator": raw_Y, "QSchur_operator": schur,
            "curvature_operator": curvature, "J_nodes": J, "X_nodes": X,
            "nodes": nodes, "occupied_indices": incoming, "predecessor_indices": previous,
            "node_signed_resolvents": node_schur_weights, "second_chart": second,
            "basis": basis, "chi": chi, "source_pins": shared["source_pins"],
            "Hermitian_relative_error": hermitian_error,
            "raw_Y_pure_formula_error": float(np.max(np.abs(Ypure - second["raw_pure_closed"]))),
            "faithful_curvature_closed_formula_error": float(np.max(np.abs(Cfaithful - second["faithful_curvature_closed"]))),
            "full_field_quotient_outside_shell_difference": q not in shared["shell_differences"],
            "inside_shell_difference_requires_rank8_T_restriction": q in shared["shell_differences"],
            "full_Z": spectral["Z"], "epsilon": spectral["epsilon"],
            "owned_root_center_only_not_interval_certificate": True,
            "seconds": time.perf_counter() - start}


def matter_operator(q, v, shared=None, repo=None, *, symbol=None):
    """Full16 sesquilinear M(q;v), before real q/-q normalization factors."""
    symbol = pure_field_symbol(q, shared=shared, repo=repo) if symbol is None else symbol
    require(tuple(int(x) % L for x in q) == tuple(symbol["basis"]["q"]), "matching_symbol_frequency")
    v = np.asarray(v, complex)
    require(v.shape == (symbol["basis"]["dimension"],), "full_native_quotient_vector")
    M = np.einsum("a,b,abij->ij", v.conj(), v, symbol["Mij"], optimize=False)
    return {"M": M, "M_chi": _mm(M, symbol["chi"]),
            "expectation_pure": complex(np.vdot(symbol["chi"], _mm(M, symbol["chi"]))),
            "expectation_faithful": complex(np.trace(M) / 16),
            "Hermitian_relative_error": _hermitian_error(M),
            "real_nonselfconjugate_velocity_v_exp_plus_conjugate_factor": 2,
            "real_cosine_velocity_factor": 0.5,
            "selfconjugate_uses_real_polarization": symbol["basis"]["self_conjugate_frequency"]}


def run(repo=None):
    """One fresh pure q3300 numerical diagnostic; no old certificate run."""
    start = time.perf_counter()
    shared = prepare_shared(repo)
    symbol = pure_field_symbol((3, 3, 0, 0), shared)
    checks = []

    def check(value, label):
        require(value, label)
        checks.append(label)

    check(symbol["basis"]["dimension"] == 13 and len(symbol["nodes"]) <= 16,
          "complete_thirteen_native_quotient_directions_finite_nodes")
    check(symbol["second_chart"]["chart"]["first_link_reconstruction_error"] < 1e-12,
          "canonical_chart_reconstructs_owned_first_link")
    check(symbol["raw_Y_pure_formula_error"] < 2e-11,
          "finite_full16_raw_Y_matches_exact_E0_energy_formula")
    check(symbol["faithful_curvature_closed_formula_error"] < 2e-11,
          "actual_full16_D2_matches_independent_scalar_trace_formula")
    check(symbol["Hermitian_relative_error"] < 2e-12,
          "full_pure_field_symbol_Hermitian")
    check(np.max(np.abs(symbol["H_pure"] - symbol["H_pure_closed_raw_Y"])) < 2e-11,
          "full_operator_correction_equals_thermal_plus_true_pure_Y_minus_signed_Schur")
    index = next(i for i, label in enumerate(symbol["basis"]["labels"])
                 if label == ["inactive_unscaled_stabilizer", 2])
    v = np.eye(13)[index]
    operator = matter_operator((3, 3, 0, 0), v, symbol=symbol)
    expected = (L * L * (1 - 1 / np.sqrt(2)) / 4
                * (float(shared["spectral"]["d_o"][0]) - 3 * float(shared["spectral"]["d_o"][1]))
                * np.dot(symbol["basis"]["u"][2, 1:], symbol["basis"]["u"][2, 1:]))
    check(abs(symbol["curvature_difference"][index, index] - expected) < 1e-12 and expected > 0,
          "inactive_stabilizer_nonzero_full_Y_correction_retained")
    check(operator["Hermitian_relative_error"] < 2e-12,
          "full16_matter_operator_Hermitian")
    check(abs(operator["expectation_pure"] - np.vdot(v, _mm(symbol["raw_Y_pure"], v))
              + np.vdot(v, _mm(symbol["QSchur_pure"], v))) < 1e-12,
          "matter_operator_expectation_matches_field_block")
    eigenvalues = np.linalg.eigvalsh(symbol["H_pure"])
    return {"schema": "d0-pure-memory-field-symbol/1", "status": "PASS_NUMERICAL_DIAGNOSTIC",
            "exact_checks": len(checks), "checks": checks, "q": [3, 3, 0, 0],
            "dimension": 13, "all_Fock_components": 16, "thermal_momenta": 4096,
            "reference_dimension": 128, "prepared_rank": 8, "finite_operator_nodes": len(symbol["nodes"]),
            "eigenvalues_float": eigenvalues.tolist(),
            "Hermitian_relative_error": symbol["Hermitian_relative_error"],
            "raw_Y_pure_formula_error": symbol["raw_Y_pure_formula_error"],
            "faithful_curvature_closed_formula_error": symbol["faithful_curvature_closed_formula_error"],
            "theta_curvature_correction_float": float(expected),
            "faithful_root_curvature_residual_float": float(np.max(np.abs(
                symbol["curvature_thermal"] + symbol["curvature_faithful"]))),
            "source_pins": symbol["source_pins"], "old_suite_or_root_search_executed": False,
            "interval_inertia_or_joint_branch_proved": False,
            "physical_admission_or_GR_claim": False, "seconds": round(time.perf_counter() - start, 6)}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
