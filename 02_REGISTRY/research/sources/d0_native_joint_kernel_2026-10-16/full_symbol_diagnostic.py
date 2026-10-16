"""Numerical full-q3300 diagnostic at the owned v8 root CENTER only.

This is not an interval certificate, root search, kernel theorem, physical
admission or GR claim.  It assembles Eq.(20) of the existing full-joint owner
on ALL4096 momenta and ALL16 exterior components.  The three exactly zero
whitened observer columns are removed; the three proved spatial-frame
representation directions are checked before taking their orthogonal
coefficient-space complement.  No other eigenvector is removed.

The returned thirteen eigenvalues use the Euclidean norm of the remaining
native-chart coefficients, not an invariant metric on the field quotient.
Only the diagnostic inertia is unchanged by invertible chart coordinates.
All output is stdout; no result/receipt file is written and no old run()
function is called. Set BLAS threads before importing NumPy for a bounded
small-matrix diagnostic, rather than launching many workers per 16x16 block.
"""
from __future__ import annotations

import os
for _name in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"

import ast
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import time

import mpmath as mp
import numpy as np
import sympy as s


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
CHART = HERE/"native_chart_check.py"
ORDERED = HERE/"ordered_operator_check.py"
WAVE = "02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py"
PINS = {
    "native_chart_check.py": "1cb2bd82796634b414b76a5396b629c98c3679aee3ce7aa63dfc34647ab84b65",
    "ordered_operator_check.py": "f2f9903685c2c522d4c850d335dfb9435c932182962402da499ff8a7a10a9418",
    WAVE: "2b12f26d814a57cc99084e904deeac69a8f64a8d9a0eb9ee765e8104ef50bc37",
}
Q = (3, 3, 0, 0)
L, FOCK, REFERENCE, ROUNDS = 8, 16, 128, 8192
EXPECTED_COSINE_SECOND = 0.08996033859210392


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("full_symbol_diagnostic:"+label)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_features(repo):
    """Extract only owned exact Q(sqrt2) energy-feature definitions."""
    source = (repo/WAVE).read_bytes()
    require(hashlib.sha256(source).hexdigest() == PINS[WAVE], "wave_source_pin")
    tree = ast.parse(source)
    names = {"qadd", "qsub", "qmul", "qsum", "_z", "_real_inner", "_feature"}
    nodes = [node for node in tree.body
             if (isinstance(node, ast.FunctionDef) and node.name in names)
             or (isinstance(node, ast.Assign)
                 and any(isinstance(target, ast.Name) and target.id in {"RE", "IM"}
                         for target in node.targets))]
    require(len(nodes) == 9, "only_exact_energy_feature_definitions")
    scope = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), WAVE, "exec"), scope)
    return lambda mode: scope["_feature"](scope["_z"](mode))


def _numeric(matrix):
    return np.array(matrix.evalf(18).tolist(), dtype=np.complex128)


def _spectral_data(features, outgoing, root):
    """Fixed-Z kappa and divided differences; equality is EXACT features.

    Unequal features with a numerically unresolved energy gap are rejected,
    never reclassified as equal eigenvalues by a tolerance. Scalar functions
    and analytic diagonal derivatives are evaluated at seventy digits.
    """
    with mp.workdps(70):
        d, o = map(mp.mpf, root)
        p = (mp.sqrt(5)-1)/2
        alpha, beta, fugacity = p*p/ROUNDS, 2*p*p, mp.mpf(2)**-20
        m, M = 2*ROUNDS, REFERENCE
        sqrt2 = mp.sqrt(2)
        def real_pair(pair):
            return pair[0]+pair[1]*sqrt2
        unique = set(features)
        energy = {f: d*real_pair(f[0])+o*real_pair(f[1]) for f in unique}
        powers = {f: mp.exp(m*mp.log1p(-alpha*energy[f])) for f in unique}
        counts = {f: 0 for f in unique}
        for f in features:
            counts[f] += 1
        Z = FOCK*mp.fsum(counts[f]*powers[f] for f in unique)
        kappa, derivative = {}, {}
        for f in unique:
            b, e = 1-alpha*energy[f], powers[f]
            require(b > 0, "all_modes_positive_survival")
            h = 1-fugacity+fugacity*e
            heat = -e/(Z*b)
            feedback = M*beta*fugacity*e/(h*b)
            kappa[f] = heat+feedback
            derivative[f] = ((m-1)*alpha*e/(Z*b*b)
                +M*beta*fugacity*alpha*e/(h*b*b)
                 *(-(m-1)+m*fugacity*e/h))
        equal_count, gaps, dd, pairs = 0, [], [], {}
        for k, l in enumerate(outgoing):
            fk, fl = features[k], features[l]
            key = (fk, fl)
            if fk == fl:
                equal_count += 1
                value = derivative[fk]
            elif key in pairs:
                value = pairs[key]
            else:
                gap = energy[fl]-energy[fk]
                scale = max(mp.mpf(1), abs(energy[fk]), abs(energy[fl]))
                require(abs(gap) > mp.mpf("1e-10")*scale,
                        "unequal_exact_features_have_double_resolved_gap")
                gaps.append(abs(gap))
                value = (kappa[fl]-kappa[fk])/gap
                pairs[key] = value
            dd.append(float(value))
        shell_features = features[1]  # index1=(0,0,0,1), an actual shell mode.
        shell = np.array([f == shell_features for f in features])
        require(int(shell.sum()) == 8, "all_and_only_eight_shell_modes")
        epsilon = energy[shell_features]
        eigenvalues = np.array([float(energy[f]) for f in features])
        rho = shell.astype(float)/REFERENCE
        resolvent = np.array([0.0 if shell[j] else float(1/(energy[f]-epsilon))
                              for j, f in enumerate(features)])
        require(resolvent[0] < 0, "ground_state_indefinite_resolvent_is_retained")
        kappas = np.array([float(kappa[f]) for f in features])
        a, b = ((mp.sqrt(d+3*o)+3*mp.sqrt(d-o))/4,
                (mp.sqrt(d+3*o)-mp.sqrt(d-o))/4)
        return {"lambda": eigenvalues, "kappa": kappas, "rho": rho,
                "resolvent": resolvent, "dd": np.array(dd),
                "a": str(mp.nstr(a, 50)), "b": str(mp.nstr(b, 50)),
                "Z": float(Z), "epsilon": float(epsilon),
                "unique_features": len(unique), "equal_edges": equal_count,
                "minimum_distinct_gap": float(min(gaps)),
                "alpha": float(alpha), "beta": float(beta), "fugacity": float(fugacity)}


def run(repo=None, *, return_data=False):
    start = time.perf_counter()
    repo = ROOT if repo is None else Path(repo).resolve()
    for path in (CHART, ORDERED):
        require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[path.name],
                "definition_pin:"+path.name)
    chart_owner = load(CHART, "diagnostic_native_chart")
    operator = load(ORDERED, "diagnostic_ordered_operator")
    # Verifies stable source/Lean/receipt SHA only; no run() is called.
    chart_owner.owned_definitions(repo)
    receipt = json.loads((repo/chart_owner.RECEIPT).read_text())
    root = receipt["interval"]["root_center"]
    features_of = exact_features(repo)
    modes = tuple(itertools.product(range(L), repeat=4))
    index = {mode: i for i, mode in enumerate(modes)}
    outgoing = np.array([index[tuple((k[r]+Q[r]) % L for r in range(4))]
                         for k in modes])
    features = tuple(features_of(k) for k in modes)
    spectral = _spectral_data(features, outgoing, root)
    creators_s, exterior_order = operator.owned_car(repo)
    creators = np.array([_numeric(C) for C in creators_s])
    phase_s = operator.phases(Q)
    differences = tuple(1-z for z in phase_s)
    # Rational DECIMAL root-derived a,b make exact columnspace independent
    # of floating-point rank decisions. This is still the root CENTER only.
    a, b = map(s.Rational, (spectral["a"], spectral["b"]))
    F = (a-b)*s.eye(4)+b*s.ones(4)
    native = chart_owner.regular_fourier_chart(F, differences)
    basis_s, legs_s = native["basis31"][:, :16], native["legs"]
    B = _numeric(basis_s)
    legs = np.array([_numeric(v).reshape(4) for v in legs_s])
    require(B.shape == (31, 16) and native["basis31"].shape == (31, 19),
            "only_three_proved_whitened_observer_columns_removed")
    require(float(np.linalg.norm(_numeric(native["basis31"][:28, 16:]))) == 0,
            "three_observer_operator_inputs_are_exactly_zero")
    cu = np.einsum("ra,aij->rij", legs, creators)
    iu = cu.conj().transpose(0, 2, 1)  # u is real.
    tq = np.array([complex(s.sympify(z).evalf(18)) for z in phase_s])
    coefficients_plus, coefficients_minus, constants = [], [], []
    for j in range(16):
        av, omega_s = operator.unpack(basis_s[:, j], creators_s)
        av = np.array([_numeric(v).reshape(4) for v in av])
        omega = np.array([_numeric(W) for W in omega_s])
        ca = np.einsum("ra,aij->rij", av, creators)
        ia = np.einsum("ra,aji->rij", av, creators)  # complex-linear, NO bar(av).
        coefficients_plus.append(ca+np.einsum("rij,rjk->rik", cu, omega))
        coefficients_minus.append(ia-tq.conj()[:, None, None]
                                  *np.einsum("rij,rjk->rik", iu, omega))
        constants.append(-(ca+ia).sum(axis=0))
    plus, minus, constant = map(np.array,
                                (coefficients_plus, coefficients_minus, constants))
    # Exact eighth roots evaluated once avoid exp(2pi i) numerical phase noise.
    roots = np.array([complex(z.evalf(18)) if hasattr(z, "evalf") else complex(z)
                      for z in operator.ROOTS8])
    tk = roots[np.array(modes)]
    D = L*(np.einsum("kr,rij->kij", tk-1, cu)
           +np.einsum("kr,rij->kij", tk.conj()-1, iu))
    lam = spectral["lambda"]
    require(np.max(np.abs(np.einsum("kij,kjl->kil", D, D)
                          -lam[:, None, None]*np.eye(16))) < 2e-11,
            "all4096_CAR_squares_match_exact_feature_energies")
    rho, chi = spectral["rho"], spectral["rho"]+spectral["kappa"]
    r = spectral["resolvent"]
    weight_J = chi+chi[outgoing]
    weight_X = spectral["dd"]-rho*r[outgoing]-rho[outgoing]*r
    H_J, H_X = np.zeros((16, 16), complex), np.zeros((16, 16), complex)
    maximum_X = 0.0
    for offset in range(0, len(modes), 128):
        sl = slice(offset, offset+128)
        J = L*(np.einsum("kr,arij->akij", tk[sl], plus, optimize=True)
               +np.einsum("kr,arij->akij", tk[sl].conj(), minus, optimize=True)
               +constant[:, None, :, :])
        X = (np.einsum("kij,akjl->akil", D[outgoing[sl]], J)
             +np.einsum("akij,kjl->akil", J, D[sl]))
        maximum_X = max(maximum_X, float(np.max(np.abs(X))))
        jf, xf = J.reshape(16, -1, 256), X.reshape(16, -1, 256)
        # Conventional c^* H c orientation; transpose of Eq20's displayed
        # bilinear indices, with identical real quadratic forms/inertia.
        H_J += np.einsum("akn,bkn,k->ab", jf.conj(), jf, weight_J[sl])
        H_X += np.einsum("akn,bkn,k->ab", xf.conj(), xf, weight_X[sl])
    H = H_J+H_X
    hermitian_error = float(np.linalg.norm(H-H.conj().T)/max(1, np.linalg.norm(H)))
    require(hermitian_error < 2e-12, "entire16_chart_matrix_Hermitian")
    H = (H+H.conj().T)/2

    gauges = []
    J23 = np.zeros((4, 4))
    J23[2, 3], J23[3, 2] = -1, 1
    for j in range(3):
        S = s.diag(0, operator.cross(s.eye(3)[:, j]))
        column = s.zeros(31, 1)
        for rr in range(4):
            column[4*rr:4*rr+4, :] = S*legs_s[rr]
            column[16+3*rr:19+3*rr, :] = differences[rr]*s.eye(3)[:, j]
        target = _numeric(column).reshape(31)
        solution, _, _, _ = np.linalg.lstsq(B, target, rcond=None)
        require(np.linalg.norm(B@solution-target) < 2e-12,
                "spatial_representation_is_in_complete_native_basis")
        gauges.append(solution)
    gauge = np.array(gauges).T
    left, singular, _ = np.linalg.svd(gauge, full_matrices=True)
    require(singular[-1] > 1e-6, "three_spatial_representation_directions_independent")
    normalized_ward = float(np.linalg.norm(H@left[:, :3])/max(1, np.linalg.norm(H)))
    require(normalized_ward < 2e-8, "all_three_spatial_representation_Ward_rows")
    complement = left[:, 3:]
    quotient = np.einsum("ia,ij,jb->ab", complement.conj(), H, complement)
    eigenvalues = np.linalg.eigvalsh(quotient)
    diagnostic_tolerance = 1e-8*max(1.0, float(np.max(np.abs(eigenvalues))))
    inertia = {"positive": int(np.sum(eigenvalues > diagnostic_tolerance)),
               "negative": int(np.sum(eigenvalues < -diagnostic_tolerance)),
               "unresolved_at_diagnostic_tolerance": int(np.sum(np.abs(eigenvalues)
                                                               <= diagnostic_tolerance))}

    row_column = np.zeros(31, complex)
    row_column[8:12] = J23@legs[2]
    row_coordinate, _, _, _ = np.linalg.lstsq(B, row_column, rcond=None)
    require(np.linalg.norm(B@row_coordinate-row_column) < 2e-12,
            "owned_row_wave_in_complete_chart")
    row_complex = float(np.real(row_coordinate.conj()@H@row_coordinate))
    row_cosine = row_complex/2  # two conjugate Fourier amplitudes 1/2.
    require(abs(row_cosine-EXPECTED_COSINE_SECOND) < 2e-8,
            "owned_row_wave_second_variation_including_cosine_half_factor")
    # Root-center residual is printed: (19)'s cancellation uses stationary
    # source equations, not a generic permission to drop constraint curvature.
    z = tk-1
    moments = np.einsum("k,kr,ks->rs", chi, z.conj(), z)
    elapsed = time.perf_counter()-start
    require(elapsed < 45, "bounded_diagnostic_computational_budget_45_seconds")
    result = {"status": "NUMERICAL_DIAGNOSTIC_ONLY", "seconds": round(elapsed, 4),
            "q": list(Q), "momenta": len(modes), "exterior_dimension": FOCK,
            "reference_dimension": REFERENCE, "rounds": ROUNDS, "power": 2*ROUNDS,
            "root_center_d_o": root, "root_center_a_b_decimal": [str(a), str(b)],
            "root_radius_not_propagated": receipt["interval"]["root_radius"],
            "source_pins": {**PINS, **chart_owner.PINS},
            "owned_exterior_order": list(exterior_order),
            "full_Z": spectral["Z"], "shell_epsilon": spectral["epsilon"],
            "exact_feature_groups": spectral["unique_features"],
            "exact_equal_energy_directed_edges": spectral["equal_edges"],
            "minimum_distinct_energy_gap": spectral["minimum_distinct_gap"],
            "negative_ground_resolvent": float(r[0]),
            "all19_columns": 19, "proved_zero_observer_columns": 3,
            "proved_spatial_representation_columns": 3, "quotient_dimension": 13,
            "Hermitian_relative_error": hermitian_error,
            "spatial_Ward_relative_residual": normalized_ward,
            "homogeneous_stationarity_moment_max": float(np.max(np.abs(moments))),
            "row_wave_complex_symbol_contraction": row_complex,
            "row_wave_real_cosine_second_variation": row_cosine,
            "owned_row_wave_reference": EXPECTED_COSINE_SECOND,
            "quotient_eigenvalues_coefficient_norm": eigenvalues.tolist(),
            "diagnostic_signature": inertia,
            "diagnostic_eigenvalue_tolerance": diagnostic_tolerance,
            "maximum_X_entry": maximum_X,
            "kernel_certified": False, "physical_admission_or_GR_claim": False,
            "large_Hilbert_dense_matrix_created": False,
            "old_runs_or_receipt_regeneration": False}
    if return_data:
        # An arbitrary fixed preconditioner may be CHOSEN numerically.  A
        # consumer must validate its entries as exact finite decimals and
        # bound the resulting congruence independently over the root box.
        # Nothing returned here certifies an eigenvalue or an error bound.
        return result, {"H": H, "complement": complement, "basis31": B,
                        "plus": plus, "minus": minus, "constant": constant,
                        "D": D, "tk": tk, "outgoing": outgoing,
                        "spectral": spectral, "modes": modes}
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
