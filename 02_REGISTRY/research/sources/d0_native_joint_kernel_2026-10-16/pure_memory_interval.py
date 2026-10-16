"""Outward pure-memory normal symbols from the same fixed conditional v8.

The old full-trace scalar moments and their complete root/geometry/roundoff
budgets are consumed as definitions, never by calling a historical run().
Only sixteen occupied/predecessor nodes enter the NEW correction.  In the
Clifford99 coordinates its exact memory-minus-trace functional is K=Schi-I:
K is Hermitian, has at most seven Gaussian-unit entries per row, ||K||<=7.
For x0 and coefficient error e this gives the sharp pair error
 e_i||Kx0_j||+||Kx0_i||e_j+7e_i e_j.

The full constrained second jet is retained. Its old-trace contraction and
the pure fixed-preparation energy are evaluated directly by outward scalar
four-vector arithmetic, including the moving native chart and EXACT decimal
congruence. Incoming memory Grams have the intentional transposed ordering.
All4096 heat modes, fullZ, reference128, all16 CAR and signed Q remain.

API prepare_shared(repo=None), evaluate(q,choice,shared,strict=True).
choice={'B':square finite-decimal complex matrix,'signs':+/-1 list}.
Outside Omega-Omega B acts on the entire canonical native mean slice.
At a nonzero shell transfer it acts ONLY on the proved complete inactive
coframe kerT section; no unconstrained shell block is silently deleted.
The enclosure is an analytic extension over the root box; it equals the
native constrained Hessian at the owned stationary root. No old run(),
root solve, physical admission, all-frequency claim or file write occurs.
"""
from __future__ import annotations

import os
for _key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"

import hashlib
import importlib.util
from pathlib import Path
import time

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PINS = {
    "uniform_symbol_bounds.py": "53b0d77d2d2102a5960769a2be90b02760defc0602eba8a22430375c909ab4fe",
    "pure_memory_curvature_check.py": "2c3ff9a9efa8920c958999e090e81fd3c2ee2f4448bc2e34868766e4ffbb6db9",
    "pure_memory_symbol.py": "1ef97d8f72d5133c75c2c071ed75b8b9ce295322c407c49e91bf589afd2af9fd",
    "shell_transfer_all_orbits.py": "d8db3de5b34e4ee4ac7a9efb4676072d18b455dec5a72f0beb6b46b40a99eb1a",
    "rank8_source_submersion.py": "04d5fba2d34538e2c7e4b41748fafb4e88e041174f4380bd0e7990111ffc6afd",
}
L, TRACE = 8, 16


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("pure_memory_interval:"+label)


def _load(name):
    path = HERE/(name+".py")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[path.name],
            "immutable_definition:"+name)
    spec = importlib.util.spec_from_file_location("pure_interval_"+name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_shared(repo=None):
    """Q-independent old scalar data and the exact NEW memory functional."""
    start = time.perf_counter()
    repo = ROOT if repo is None else Path(repo).resolve()
    for name, digest in PINS.items():
        require(hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest,
                "immutable_input:"+name)
    owner = _load("uniform_symbol_bounds")
    old = owner.prepare_shared(repo)  # scalar/geometry definitions, NOT run().
    algebra = old["algebra"]
    masks = algebra.EVEN024
    expectation = {0: 1, 3: -1j, 60: -1, 63: 1j,
                   204: -1, 207: 1j, 240: -1, 243: 1j}
    adjoint = np.array([(-1)**(bin(int(m)).count("1")*(bin(int(m)).count("1")-1)//2)
                        for m in masks], int)
    K = np.array([[adjoint[i]*algebra.mask_sign(int(m), int(n))
                   *expectation.get(int(m)^int(n), 0)-(1 if i == j else 0)
                   for j, n in enumerate(masks)] for i, m in enumerate(masks)], complex)
    require(K.shape == (99, 99) and np.array_equal(K, K.conj().T)
            and np.all(np.diag(K) == 0), "exact_Hermitian_memory_minus_trace_K99")
    require(np.all(np.sum(np.abs(K), axis=1) <= 7)
            and set(K.ravel()) <= {0, 1, -1, 1j, -1j},
            "exact_seven_Gaussian_unit_entries_imply_operator_norm_at_most_seven")
    old.update(pure_interval_owner=owner, pure_K=K, pure_adjoint_sign=adjoint,
               pure_interval_prepared=True, repo=repo)
    old["source_pins"] = {**old["source_pins"], **PINS}
    old["pure_prepare_seconds"] = time.perf_counter()-start
    return old


def _dot(left, right, zero):
    return sum((x*y for x, y in zip(left, right)), zero)


def _cross(x, y):
    return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]


def _conj(value, iv):
    # mpmath's ivmpc.conjugate() is broken on the supported runtime.
    # Construct in the SAME outward interval context, with no float cast.
    return iv.mpc(value.real, -value.imag)


def _scalars(q, B, shared):
    """Entire-box Ypure-Cold, without dense D2 or omitting its curvature."""
    owner, iv = shared["pure_interval_owner"], shared["iv"]
    u, columns = owner._base_fields(q, shared["core"]["a"], shared["core"]["b"],
                                    shared["roots_iv"])
    av, omega = owner._combine(columns, B, iv)
    n, zero = len(B[0]), iv.mpc(0)
    rho = [iv.sqrt(sum((x*x for x in ur[1:]), iv.mpf(0))) for ur in u]
    require(all(float(x.a) > 0 for x in rho), "nonzero_native_spatial_legs_on_whole_box")
    z = [[x/rho[r] for x in u[r][1:]] for r in range(4)]
    radial = [[_dot(z[r], av[i][r][1:], zero) for r in range(4)] for i in range(n)]
    beta = [[[(av[i][r][k+1]-radial[i][r]*z[r][k])/rho[r] for k in range(3)]
             for r in range(4)] for i in range(n)]
    theta = [[_dot(z[r], omega[i][r], zero) for r in range(4)] for i in range(n)]
    total = [sum((ur[k] for ur in u), iv.mpf(0)) for k in range(4)]
    expression = [[zero for _ in range(n)] for _ in range(n)]
    pure = [[zero for _ in range(n)] for _ in range(n)]
    lam = L*L*(2-iv.sqrt(2))
    for i in range(n):
        for j in range(n):
            for r in range(4):
                # A=column j unconjugated, B=row i conjugated.
                aA, aB = av[j][r], [_conj(x, iv) for x in av[i][r]]
                bA, bB = beta[j][r], [_conj(x, iv) for x in beta[i][r]]
                omA, omB = omega[j][r], [_conj(x, iv) for x in omega[i][r]]
                thA, thB = theta[j][r], _conj(theta[i][r], iv)
                drA, drB = radial[j][r], _conj(radial[i][r], iv)
                u2 = [zero]+[drA*bB[k]+drB*bA[k]-rho[r]*_dot(bA, bB, zero)*z[r][k]
                              for k in range(3)]
                t = shared["roots_iv"][q[r]]
                crossed = _cross(bA, bB)
                # Logarithmic mixed SO3 jet of the literal sphere/spin chart.
                k2 = [thA*(1+_conj(t, iv))*bB[k]/2
                      +thB*(1+t)*bA[k]/2+(t-_conj(t, iv))*crossed[k] for k in range(3)]
                tr = -2*_dot(omA, omB, zero)
                ba, ab, ku = _cross(omB, aA[1:]), _cross(omA, aB[1:]), _cross(k2, u[r][1:])
                vector = [2*u[r][0]*tr]+[-4*ba[k]-4*ab[k]+2*u[r][k+1]*tr-4*ku[k]
                                        for k in range(3)]
                expression[i][j] += 16*_dot(u[r], u2, zero)+_dot(
                    [2*u[r][k]-total[k] for k in range(4)], vector, zero)
                if not q[r]:
                    pure[i][j] += lam/2*(_conj(av[i][r][0], iv)*av[j][r][0]
                                        +_conj(radial[i][r], iv)*radial[j][r])
    correction = [[pure[i][j]-lam/64*(expression[i][j]+_conj(expression[j][i], iv))
                   for j in range(n)] for i in range(n)]
    return correction


def _section(q, choice, shared):
    owner = shared["pure_interval_owner"]
    qdim = 17-2*sum(bool(x) for x in q)
    on_shell = q in shared["shell_differences"]
    require(any(q), "zero_mode_requires_its_separate_amplitude_KKT_not_this_symbol")
    if on_shell:
        active = [r for r in range(4) if q[r]]
        require(len(active) in (1, 2), "literal_nonzero_shell_transfer")
        offset = 3*(len(active)-1)
        inactive = [r for r in range(4) if not q[r]]
        indices = [offset+5*i+j for i, _ in enumerate(inactive) for j in range(4)]
    else:
        indices = list(range(qdim))
    B = choice["B"] if isinstance(choice, dict) else choice
    n = len(indices)
    require(len(B) == n and all(len(row) == n for row in B),
            "square_decimal_congruence_on_complete_required_section")
    require(all(len(pair) == 2 and all(isinstance(x, str) and owner.DECIMAL.fullmatch(x) for x in pair)
                for row in B for pair in row), "exact_finite_complex_decimal_B")
    if isinstance(choice, dict) and "basis_indices" in choice:
        require(list(choice["basis_indices"]) == indices, "specified_section_matches_proved_native_kernel")
    # Immutable old geometry's n=len(B) assumes square. Pad with zero
    # columns, then retain the first n outputs. Do not edit that old owner.
    full = [[["0", "0"] for _ in range(qdim)] for _ in range(qdim)]
    for i, row in enumerate(indices):
        for j in range(n):
            full[row][j] = list(B[i][j])
    return B, full, indices, on_shell


def _old_symbol(q, full, n, shared):
    owner, arithmetic, iv = shared["pure_interval_owner"], shared["arithmetic"], shared["iv"]
    geometry = owner._geometry(q, full, shared)
    for key in ("J", "X", "eJ", "eX", "cJ", "cX"):
        geometry[key] = geometry[key][:n]
    moments = owner._moments(q, shared)
    H = np.zeros((n, n), complex)
    errors = [[iv.mpf(0) for _ in range(n)] for _ in range(n)]
    for key, moment in zip(("J", "X"), moments):
        coefficients = geometry[key]
        mixed = np.einsum("lm,bmc->blc", moment["matrix"], coefficients, optimize=False)
        H += TRACE*np.einsum("alc,blc->ab", coefficients.conj(), mixed, optimize=False)
    for i in range(n):
        for j in range(n):
            for ckey, ekey, moment in zip(("cJ", "cX"), ("eJ", "eX"), moments):
                ci, cj = geometry[ckey][i], geometry[ckey][j]
                ei, ej = geometry[ekey][i], geometry[ekey][j]
                errors[i][j] += TRACE*(moment["error"]*ci*cj+(moment["max_reference"]+moment["error"])
                                      *(ei*cj+ci*ej+ei*ej))
                errors[i][j] += TRACE*2*arithmetic.gamma(2**22)*moment["max_reference"]*ci*cj+arithmetic.TINY
    return H, errors, geometry


def _norm(array, shared):
    # Last coordinate vector is at most99 complex coefficients, below the
    # immutable Frobenius majorant's256-coordinate allowance.
    return shared["arithmetic"].frobenius_upper(array[:, None, :])


def _finite_correction(q, geometry, shared):
    owner, arithmetic, iv = shared["pure_interval_owner"], shared["arithmetic"], shared["iv"]
    n = len(geometry["J"])
    K, adjoint = shared["pure_K"], shared["pure_adjoint_sign"]
    core = shared["core"]
    shell = core["shell_modes"]
    predecessors = [tuple((k[r]-q[r]) % L for r in range(4)) for k in shell]
    nodes = tuple(sorted(set(shell) | set(predecessors)))
    lookup = {k: i for i, k in enumerate(nodes)}
    coefficients, node_errors = {}, {}
    for name, support in (("J", shared["algebra"].E9), ("X", shared["algebra"].E33)):
        exponents = np.einsum("pr,kr->kp", np.array(support, int), np.array(nodes, int), optimize=False) % L
        phases = shared["roots"][exponents]
        coefficients[name] = np.einsum("kp,apc->akc", phases, geometry[name], optimize=False)
        node_errors[name] = [(geometry["e"+name][i]
                             +(shared["phase_error"]+2*arithmetic.gamma(512))*geometry["c"+name][i]
                             +arithmetic.TINY).b for i in range(n)]
    result = np.zeros((n, n), complex)
    error = [[iv.mpf(0) for _ in range(n)] for _ in range(n)]
    max_mode_errors = {"J": max(node_errors["J"], key=lambda x: float(x.b)),
                       "X": max(node_errors["X"], key=lambda x: float(x.b))}
    for k, predecessor in zip(shell, predecessors):
        for node, incoming in ((k, False), (predecessor, True)):
            index = lookup[node]
            jref, xref = coefficients["J"][:, index], coefficients["X"][:, index]
            nj, nx = _norm(jref, shared), _norm(xref, shared)
            gram_j = np.einsum("ic,jc->ij", jref.conj(), jref, optimize=False)
            # Incoming pure expectation is <X_j^dagger chi,X_i^dagger chi>.
            y = adjoint[None, :]*xref.conj() if incoming else xref
            Ky = np.einsum("cd,id->ic", K, y, optimize=False)
            gram_x = np.einsum("ic,jc->ij", y.conj(), Ky, optimize=False)
            if incoming:
                gram_x = gram_x.T
            nk = _norm(Ky, shared)
            # Exact K is Gaussian-unit, at most7 nonzeros/row. Even a
            # dense99-term loop uses <4096 real operations per component.
            ek = [2*arithmetic.gamma(4096)*7*iv.mpf(float(nx[i]))+arithmetic.TINY for i in range(n)]
            nk_upper = [iv.mpf(float(nk[i]))+ek[i] for i in range(n)]
            target = node if incoming else tuple((k[r]+q[r]) % L for r in range(4))
            mode = np.ravel_multi_index(target, (L,)*4)
            r_iv = core["resolvent"][mode]
            r0 = arithmetic.midpoint(r_iv)
            dr = abs(r_iv-iv.mpf(r0)).b
            rmax = abs(r_iv).b
            result -= (gram_j+r0*gram_x)/8
            for i in range(n):
                for j in range(n):
                    ej_i, ej_j = node_errors["J"][i], node_errors["J"][j]
                    ex_i, ex_j = node_errors["X"][i], node_errors["X"][j]
                    nji, njj, nxi, nxj = (iv.mpf(float(value)) for value in (nj[i], nj[j], nx[i], nx[j]))
                    gj = ej_i*njj+nji*ej_j+ej_i*ej_j
                    gx = ex_i*nk_upper[j]+nk_upper[i]*ex_j+7*ex_i*ex_j
                    # <2^18 real operations per entry covers all sixteen
                    # finite99-component signed Grams and their additions.
                    # Sparse-K assembly errors are included via the7 norm.
                    rounding = 2*arithmetic.gamma(2**18)*(nji*njj+7*rmax*nxi*nxj)+arithmetic.TINY
                    error[i][j] += (gj+dr*owner._abs(owner._point(gram_x[i, j], iv), iv)
                                    +rmax*gx+rounding)/8
    return result, error, {"nodes": len(nodes), "directed_edges": 2*len(shell),
                           "mode_error_upper_J_X": [arithmetic.upper(max_mode_errors[key]) for key in ("J", "X")]}


def evaluate(q, choice, shared, *, strict=True):
    """Prove distance<1 for a supplied FIXED decimal pure congruence."""
    start = time.perf_counter()
    require(shared.get("pure_interval_prepared"), "prepare_shared_required")
    q = tuple(int(x) % L for x in q)
    require(len(q) == 4, "four_native_momentum_coordinates")
    B, full, indices, on_shell = _section(q, choice, shared)
    n, iv = len(B), shared["iv"]
    owner, arithmetic = shared["pure_interval_owner"], shared["arithmetic"]
    H, old_error, geometry = _old_symbol(q, full, n, shared)
    correction, finite_error, finite_data = _finite_correction(q, geometry, shared)
    scalar = _scalars(q, full, shared)
    scalar_reference = np.array([[complex(arithmetic.midpoint(scalar[i][j].real),
                                          arithmetic.midpoint(scalar[i][j].imag))
                                  for j in range(n)] for i in range(n)])
    reference = H+correction+scalar_reference
    require(np.isfinite(reference).all(), "finite_pure_reference_symbol")
    signs = choice.get("signs") if isinstance(choice, dict) else None
    if signs is None:
        signs = [1 if reference[i, i].real >= 0 else -1 for i in range(n)]
    signs = np.array(signs, int)
    require(signs.shape == (n,) and all(x in (-1, 1) for x in signs), "nonsingular_signature_comparison")
    rows, residual_rows, old_rows, finite_rows, scalar_rows = [], [], [], [], []
    for i in range(n):
        residual, inherited, new, scal = (iv.mpf(0) for _ in range(4))
        for j in range(n):
            target = int(signs[i]) if i == j else 0
            residual += owner._abs(owner._point(reference[i, j], iv)-target, iv)
            inherited += old_error[i][j]
            new += finite_error[i][j]
            scal += owner._abs(scalar[i][j]-owner._point(scalar_reference[i, j], iv), iv)
            # Final addition H+finite+scalar is separate from either Gram.
            scal += 2*arithmetic.gamma(32)*(owner._abs(owner._point(H[i, j], iv), iv)
                                            +owner._abs(owner._point(correction[i, j], iv), iv)
                                            +owner._abs(owner._point(scalar_reference[i, j], iv), iv))+arithmetic.TINY
        residual_rows.append(arithmetic.upper(residual))
        old_rows.append(arithmetic.upper(inherited))
        finite_rows.append(arithmetic.upper(new))
        scalar_rows.append(arithmetic.upper(scal))
        rows.append(arithmetic.upper(residual+inherited+new+scal))
    delta = max(rows)
    valid = delta < 1
    if strict:
        require(valid, "pure_entire_root_box_distance_from_signature_below_one")
    BF2 = sum((iv.mpf(real)**2+iv.mpf(imag)**2 for row in B for real, imag in row), iv.mpf(0))
    return {"schema": "d0-pure-memory-symbol-interval/1", "q": list(q),
            "status": "VALIDATED" if valid else "NOT_VALIDATED", "dimension": n,
            "distance_from_signature_upper": delta,
            "positive": int(sum(signs > 0)) if valid else None,
            "negative": int(sum(signs < 0)) if valid else None, "zero": 0 if valid else None,
            "inverse_native_coefficient_norm_upper": arithmetic.upper(BF2/(1-iv.mpf(delta))) if valid else None,
            "comparison_signs": signs.tolist(), "total_rows": rows, "residual_rows": residual_rows,
            "inherited_full_trace_error_rows": old_rows, "new_finite_error_rows": finite_rows,
            "new_true_second_jet_scalar_error_rows": scalar_rows, "finite_data": finite_data,
            "basis_indices": indices, "section": "complete_inactive_coframe_kerT" if on_shell else "complete_native_mean_slice",
            "root_box": shared["core"]["root_box"], "source_pins": shared["source_pins"],
            "carrier": {"thermal_momenta": 4096, "Fock": 16, "reference": 128, "prepared_rank": 8},
            "scope": {"Hessian_identity_only_at_owned_stationary_root": True,
                      "incoming_memory_Gram_transpose_retained": True, "true_chart_second_jet_retained": True,
                      "signed_Q_and_full_Z_retained": True, "old_runs_or_root_search": False,
                      "all_q_inverse_or_curved_branch_claim": False, "physical_admission_or_GR_claim": False},
            "seconds": round(time.perf_counter()-start, 4)}
