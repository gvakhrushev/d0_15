"""Shared outward validator for a fixed decimal congruence at nonzero q.

Only q outside the occupied-shell difference set is accepted. The complete
native mean slice has n=17-2p coordinates, and B is an arbitrary FIXED n x n
matrix of finite decimal complex pairs. Numerical choices are not trusted:
evaluate() bounds ||B*H(theta)B-diag(signs)|| on the ENTIRE owned root box.

All119 feature energies,7140 scalar pairs,4096 momenta,16 Fock states,
fullZ/reference128 and the signed ground resolvent remain. No old run()
or per-q4096x16 matrix is used. Geometry is enclosed through the actual
scalar a/omega/u*omega formulas, not through fitted derivatives. Clifford
linear multiplication satisfies ||D J||_2 <= ||D||_1 ||J||_2. Thus uniform
errors on the nine J and33 X coefficient vectors suffice. For c_i=sum||x_i||
and coefficient error e_i, a moment error deltaM gives the entry bound
16[deltaM*c_i*c_j+(Mmax+deltaM)(e_i*c_j+c_i*e_j+e_i*e_j)].

Moment and compressed-Gram roundoff are separately covered below. This is
a fixed L8 theorem, not a refinement-uniform inverse or a GR construction.
"""
from __future__ import annotations

import os
for _name in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"

import hashlib
import importlib.util
from pathlib import Path
import re
import time

import mpmath as mp
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PINS = {
    "nonzero_symbol_algebra.py": "b74c1a10ab6e1051dfb50942abf019cb19aeb890460bc98b919d2e848deecba1",
    "full_symbol_interval.py": "2bb2f26be6d6484d087a2e2e2591b681c793b5932790e3552c2b9fdc5021c84d",
    "full_symbol_interval_weights.py": "0d8651dae3b6b7ba2049a1c71ac47895e536f9ccc5f85bf9978c133c75ccfc18",
    "native_chart_check.py": "1cb2bd82796634b414b76a5396b629c98c3679aee3ce7aa63dfc34647ab84b65",
}
DECIMAL = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
L, N, TRACE = 8, 4096, 16


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("uniform_symbol_bounds:"+label)


def _load(name):
    path = HERE/(name+".py")
    require(path.name in PINS and hashlib.sha256(path.read_bytes()).hexdigest() == PINS[path.name],
            "immutable_definition:"+name)
    spec = importlib.util.spec_from_file_location("uniform_"+name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _abs(value, iv):
    return iv.sqrt(value.real**2+value.imag**2).b


def _point(value, iv):
    value = complex(value)
    return iv.mpc(iv.mpf(float(value.real)), iv.mpf(float(value.imag)))


def _roots(context):
    z = context.sqrt(2)/2
    return [context.mpc(1), context.mpc(z, z), context.mpc(0, 1), context.mpc(-z, z),
            context.mpc(-1), context.mpc(-z, -z), context.mpc(0, -1), context.mpc(z, -z)]


def _phase_table(support, modes, roots):
    powers = np.einsum("dr,kr->dk", np.array(support, int), modes, optimize=False) % L
    return roots[powers]


def prepare_shared(repo=None):
    """Build q-independent interval pair data and phase tables exactly once."""
    start = time.perf_counter()
    repo = ROOT if repo is None else Path(repo).resolve()
    mp.mp.dps, mp.iv.dps = 100, 80
    algebra, arithmetic, owner = (_load(name) for name in
                                  ("nonzero_symbol_algebra", "full_symbol_interval", "full_symbol_interval_weights"))
    _load("native_chart_check").owned_definitions(repo)
    info = np.finfo(np.float64)
    require(info.eps == 2.0**-52 and info.nmant == 52 and info.maxexp == 1024
            and np.dtype(np.complex128).itemsize == 16, "IEEE_binary64_storage")
    core = owner.spectral_intervals(repo)  # immutable definitions/guards, NOT old run().
    iv = core["iv_ctx"]
    features = tuple(sorted(core["feature_data"]))
    lookup = {f: i for i, f in enumerate(features)}
    ids = np.array([lookup[f] for f in core["features"]], int)
    wref, werr = (np.zeros((2, 119, 119)) for _ in range(2))
    min_gap = None
    for i, left in enumerate(features):
        dl = core["feature_data"][left]
        for j in range(i, 119):
            right = features[j]
            dr = core["feature_data"][right]
            if i == j:
                dd = dl["derivative"]
            else:
                da, dc = (tuple(right[k][r]-left[k][r] for r in range(2)) for k in (0, 1))
                difference = core["d"]*(da[0]+da[1]*iv.sqrt(2))+core["o"]*(dc[0]+dc[1]*iv.sqrt(2))
                require(owner._separated(difference), "all7021_exact_feature_gaps_separated")
                lower = owner._absolute_lower(difference)
                min_gap = lower if min_gap is None or lower < min_gap else min_gap
                dd = (dr["kappa"]-dl["kappa"])/difference
            values = (dl["chi"]+dr["chi"],
                      dd-dl["rho"]*dr["resolvent"]-dr["rho"]*dl["resolvent"])
            for part, value in enumerate(values):
                reference = arithmetic.midpoint(value)
                error = arithmetic.upper(abs(value-iv.mpf(reference)))
                wref[part, i, j] = wref[part, j, i] = reference
                werr[part, i, j] = werr[part, j, i] = error
    with mp.workdps(100):
        roots0 = _roots(mp)
        roots = np.array([complex(x) for x in roots0])
        roots_iv = _roots(iv)
        phase_error = max((_abs(exact-_point(value, iv), iv)
                           for exact, value in zip(roots_iv, roots)), key=lambda x: float(x.b))
        d0, o0 = map(mp.mpf, core["root_box"]["center"])
        a0 = (mp.sqrt(d0+3*o0)+3*mp.sqrt(d0-o0))/4
        b0 = (mp.sqrt(d0+3*o0)-mp.sqrt(d0-o0))/4
    supports = (algebra.E9, algebra.E33)
    deltas = [tuple(sorted({tuple(mu[r]-nu[r] for r in range(4)) for mu in support for nu in support}))
              for support in supports]
    modes = np.array(core["modes"], int)
    tables, matrix_indices = [], []
    for support, delta in zip(supports, deltas):
        tables.append(_phase_table(delta, modes, roots))
        indices = {phase: k for k, phase in enumerate(delta)}
        matrix_indices.append(np.array([[indices[tuple(mu[r]-nu[r] for r in range(4))]
                                         for mu in support] for nu in support]))
    require([len(delta) for delta in deltas] == [41, 257], "exact_phase_moment_supports")
    # Template norms are outward evaluated once, not recomputed per q.
    templates = {"C": algebra.CREATORS[:, algebra.ODD13],
                 "I": algebra.CONTRACTORS[:, algebra.ODD13],
                 "CG": algebra.CG[:, :, algebra.ODD13], "IG": algebra.IG[:, :, algebra.ODD13]}
    norms = {}
    for key, value in templates.items():
        norm = np.empty(value.shape[:-1], object)
        for index in np.ndindex(norm.shape):
            norm[index] = iv.sqrt(sum((iv.mpf(float(z.real))**2+iv.mpf(float(z.imag))**2
                                      for z in value[index]), iv.mpf(0))).b
        norms[key] = norm
    shell = tuple(tuple(sign if r == a else 0 for r in range(4)) for a in range(4) for sign in (1, 7))
    differences = {tuple((x[r]-y[r]) % L for r in range(4)) for x in shell for y in shell}
    require(len(differences) == 33, "complete_shell_difference_domain")
    return {"algebra": algebra, "arithmetic": arithmetic, "core": core, "iv": iv,
            "features": features, "feature_ids": ids, "weight_reference": wref,
            "weight_error": werr, "modes": modes, "roots": roots, "roots_iv": roots_iv,
            "phase_error": phase_error, "a0": a0, "b0": b0,
            "phase_tables": tables, "moment_matrix_indices": matrix_indices,
            "templates": templates, "template_norms": norms, "shell_differences": differences,
            "ones": np.ones((1, N)), "seconds": time.perf_counter()-start,
            "minimum_pair_gap_lower": str(min_gap), "source_pins": {**PINS, **core["source_pins"]}}


def _base_fields(q, a, b, roots):
    """Sparse actual mean-slice formulas, polynomial degree<=1 at input."""
    u = [[a if r == 0 else b]+[-(a if r == j+1 else b) for j in range(3)] for r in range(4)]
    active, inactive = [r for r in range(4) if q[r]], [r for r in range(4) if not q[r]]
    kappa = [1-roots[q[r]] for r in range(4)]
    columns = []
    for r in active[:-1]:
        for j in range(3):
            column = {}
            for role, sign in ((r, 1), (active[-1], -1)):
                axis = [sign*int(i == j) for i in range(3)]
                w = u[role][1:]
                cross = [axis[1]*w[2]-axis[2]*w[1], axis[2]*w[0]-axis[0]*w[2],
                         axis[0]*w[1]-axis[1]*w[0]]
                for k in range(3):
                    if k != j:
                        column[(0, role, k+1)] = cross[k]
                column[(1, role, j)] = sign*kappa[role]
            columns.append(column)
    for r in inactive:
        columns.extend({(0, r, j): 1} for j in range(4))
        columns.append({(1, r, j): u[r][j+1] for j in range(3)})
    return u, columns


def _combine(columns, B, context):
    n = len(B[0])
    av = [[[context.mpc(0) for _ in range(4)] for _ in range(4)] for _ in range(n)]
    omega = [[[context.mpc(0) for _ in range(3)] for _ in range(4)] for _ in range(n)]
    for i, column in enumerate(columns):
        for j in range(n):
            coefficient = context.mpc(*B[i][j])
            for (kind, r, k), value in column.items():
                (av if kind == 0 else omega)[j][r][k] += coefficient*value
    return av, omega


def _coefficient_norm_sum(coefficients, shared):
    arithmetic, iv = shared["arithmetic"], shared["iv"]
    norms = arithmetic.frobenius_upper(coefficients[:, :, None, :])
    return [sum((iv.mpf(float(value)) for value in row), iv.mpf(0)).b for row in norms]


def _geometry(q, B, shared):
    algebra, arithmetic, iv = shared["algebra"], shared["arithmetic"], shared["iv"]
    u, columns = _base_fields(q, shared["core"]["a"], shared["core"]["b"], shared["roots_iv"])
    with mp.workdps(100):
        u0, columns0 = _base_fields(q, shared["a0"], shared["b0"], _roots(mp))
        av, omega = _combine(columns, B, iv)
        av0, omega0 = _combine(columns0, B, mp)
        n = len(B)
        J = np.zeros((n, 9, 64), complex)
        err, majorant = [iv.mpf(0) for _ in range(n)], [iv.mpf(0) for _ in range(n)]
        templates, norms = shared["templates"], shared["template_norms"]
        def term(i, phase, value, center, family, index):
            point = complex(center)
            require(np.isfinite(point) and abs(point) < 2.0**100, "bounded_geometry_term")
            J[i, phase] += L*point*templates[family][index]
            norm = norms[family][index]
            err[i] += L*_abs(value-_point(point, iv), iv)*norm
            majorant[i] += L*_abs(_point(point, iv), iv)*norm
        for i in range(n):
            for r in range(4):
                for j in range(4):
                    term(i, 1+r, av[i][r][j], av0[i][r][j], "C", j)
                    term(i, 5+r, av[i][r][j], av0[i][r][j], "I", j)
                    term(i, 0, -av[i][r][j], -av0[i][r][j], "C", j)
                    term(i, 0, -av[i][r][j], -av0[i][r][j], "I", j)
                    for k in range(3):
                        value, center = u[r][j]*omega[i][r][k], u0[r][j]*omega0[i][r][k]
                        term(i, 1+r, value, center, "CG", (j, k))
                        barq = shared["roots_iv"][(-q[r]) % L]
                        barq0 = _roots(mp)[(-q[r]) % L]
                        term(i, 5+r, -barq*value, -barq0*center, "IG", (j, k))
        # Each J coefficient entry has <4096 real operations; factor2
        # combines componentwise real/imaginary errors in the complex norm.
        eJ = [(err[i]+2*arithmetic.gamma(4096)*majorant[i]+arithmetic.TINY).b for i in range(n)]
        cJ = _coefficient_norm_sum(J, shared)
        # D has only8 Clifford coefficients per phase. Construct them at
        # 100dps, declare the resulting binary64 values as exact references,
        # and compare directly with their outward interval expressions.
        D = np.zeros((9, 256), complex)
        eD = iv.mpf(0)
        for r in range(4):
            for j in range(4):
                for phase, imaginary, sign in ((1+r, False, 1), (1+r, True, -1),
                                                (5+r, False, 1), (5+r, True, 1)):
                    g = 2*j+int(imaginary)
                    value = L*u[r][j]*sign/2*(iv.mpc(0, 1) if imaginary else 1)
                    center = L*u0[r][j]*sign/2*(mp.j if imaginary else 1)
                    point = complex(center)
                    D[phase, 1 << g] = point
                    eD += _abs(value-_point(point, iv), iv)
        for j in range(4):
            value, center = -L*sum(u[r][j] for r in range(4)), -L*sum(u0[r][j] for r in range(4))
            point = complex(center)
            D[0, 1 << (2*j)] = point
            eD += _abs(value-_point(point, iv), iv)
        cD = sum((_abs(_point(value, iv), iv) for value in D.ravel() if value != 0), iv.mpf(0)).b
        Jfull = np.zeros((n, 9, 256), complex)
        Jfull[:, :, algebra.ODD13] = J
        X = np.zeros((n, 33, 256), complex)
        location = {phase: i for i, phase in enumerate(algebra.E33)}
        Dleft = np.zeros_like(D)
        for i, nu in enumerate(algebra.E9):
            Dleft[i] = D[i]*shared["roots"][sum(q[r]*nu[r] for r in range(4)) % L]
            for j, mu in enumerate(algebra.E9):
                phase = tuple(nu[r]+mu[r] for r in range(4))
                if phase not in location:
                    continue  # exact proven +/-2e_r cancellation, not pruning.
                X[:, location[phase]] += (algebra._linear_product(Dleft[i], Jfull[:, j], True)
                                         +algebra._linear_product(D[i], Jfull[:, j], False))
        X = X[:, :, algebra.EVEN024]
        cDl = sum((_abs(_point(value, iv), iv) for value in Dleft.ravel() if value != 0), iv.mpf(0)).b
        eDl = (eD+shared["phase_error"]*cD+2*arithmetic.gamma(32)*(1+shared["phase_error"])*cD
               +arithmetic.TINY).b
        eX = [(2*(cD+eD)*eJ[i]+(eDl+eD)*cJ[i]
               +2*arithmetic.gamma(16384)*(cDl+cD)*cJ[i]+arithmetic.TINY).b for i in range(n)]
        cX = _coefficient_norm_sum(X, shared)
        require(all(np.isfinite(array).all() and np.max(np.abs(array)) < 2.0**100 for array in (J, X, D)),
                "finite_bounded_reference_operator_coefficients")
        return {"J": J, "X": X, "eJ": eJ, "eX": eX, "cJ": cJ, "cX": cX,
                "eD_L1": eD.b, "D_reference_L1": cD}


def _moments(q, shared):
    arithmetic, iv = shared["arithmetic"], shared["iv"]
    outgoing = np.ravel_multi_index(((shared["modes"]+np.array(q)) % L).T, (L,)*4)
    left, right = shared["feature_ids"], shared["feature_ids"][outgoing]
    result = []
    for part in range(2):
        weight = shared["weight_reference"][part, left, right]
        dw = shared["weight_error"][part, left, right]
        values = np.einsum("k,dk->d", weight, shared["phase_tables"][part], optimize=False)
        sum_dw = arithmetic.positive_sum(dw, shared["ones"], shared["ones"])[0, 0]
        sum_abs = arithmetic.positive_sum(np.abs(weight), shared["ones"], shared["ones"])[0, 0]
        error = (iv.mpf(float(sum_dw))+(shared["phase_error"]+2*arithmetic.gamma(16384))
                 *iv.mpf(float(sum_abs))+arithmetic.TINY).b
        max_reference = max(arithmetic.frobenius_upper(values[:, None, None]))
        result.append({"values": values, "error": error, "max_reference": iv.mpf(float(max_reference)),
                       "matrix": values[shared["moment_matrix_indices"][part]]})
    return result


def evaluate(q, B, shared, *, signs=None, strict=False):
    """Validate ONE arbitrary fixed decimal B, without choosing or fitting it.

    B may also be {'B': decimalmatrix,'signs': comparison_signs}. If signs
    are absent, the reference diagonal chooses a +/-1 COMPARISON only; the
    interval distance, not that numerical choice, proves the conclusion.
    """
    start = time.perf_counter()
    arithmetic, iv = shared["arithmetic"], shared["iv"]
    q = tuple(int(x) % L for x in q)
    require(len(q) == 4 and q not in shared["shell_differences"], "field_only_nonzero_q_outside_shell_difference")
    if isinstance(B, dict):
        signs = B.get("signs", signs)
        B = B["B"]
    n = 17-2*sum(bool(x) for x in q)
    require(len(B) == n and all(len(row) == n for row in B), "full_square_fixed_decimal_congruence")
    require(all(len(pair) == 2 and all(isinstance(x, str) and DECIMAL.fullmatch(x) for x in pair)
                for row in B for pair in row), "exact_finite_complex_decimal_entries")
    geometry, moments = _geometry(q, B, shared), _moments(q, shared)
    H = np.zeros((n, n), complex)
    for key, moment in zip(("J", "X"), moments):
        coefficients = geometry[key]
        mixed = np.einsum("lm,bmc->blc", moment["matrix"], coefficients, optimize=False)
        H += TRACE*np.einsum("alc,blc->ab", coefficients.conj(), mixed, optimize=False)
    require(np.isfinite(H).all(), "finite_compressed_Gram_reference")
    if signs is None:
        signs = [1 if H[i, i].real >= 0 else -1 for i in range(n)]
    signs = np.array(signs, int)
    require(signs.shape == (n,) and all(x in (-1, 1) for x in signs), "comparison_is_nonsingular_signature")
    rows, residuals, variations, roundings = [], [], [], []
    for i in range(n):
        residual, variation, rounding = iv.mpf(0), iv.mpf(0), iv.mpf(0)
        for j in range(n):
            target = int(signs[i]) if i == j else 0
            residual += _abs(_point(H[i, j], iv)-target, iv)
            for ckey, ekey, moment in zip(("cJ", "cX"), ("eJ", "eX"), moments):
                ci, cj = geometry[ckey][i], geometry[ckey][j]
                ei, ej = geometry[ekey][i], geometry[ekey][j]
                variation += TRACE*(moment["error"]*ci*cj+(moment["max_reference"]+moment["error"])
                                    *(ei*cj+ci*ej+ei*ej))
                # <2^22 real operations affect one entry of the two-stage
                #33x33x99 Gram contraction (including its final J+X sum).
                # Factor2 covers complex real/imaginary component errors.
                rounding += TRACE*2*arithmetic.gamma(2**22)*moment["max_reference"]*ci*cj+arithmetic.TINY
        residuals.append(arithmetic.upper(residual))
        variations.append(arithmetic.upper(variation))
        roundings.append(arithmetic.upper(rounding))
        rows.append(arithmetic.upper(residual+variation+rounding))
    delta = max(rows)
    validated = delta < 1
    if strict:
        require(validated, "entire_root_box_distance_from_signature_below_one")
    BF2 = sum((iv.mpf(real)**2+iv.mpf(imag)**2 for row in B for real, imag in row), iv.mpf(0))
    return {"q": list(q), "status": "VALIDATED" if validated else "NOT_VALIDATED",
            "dimension": n, "distance_from_signature_upper": delta,
            "positive": int(sum(signs > 0)) if validated else None,
            "negative": int(sum(signs < 0)) if validated else None,
            "zero": 0 if validated else None,
            "inverse_native_coefficient_norm_upper": arithmetic.upper(BF2/(iv.mpf(1)-iv.mpf(delta))) if validated else None,
            "comparison_signs": signs.tolist(), "residual_rows": residuals,
            "variation_rows": variations, "compressed_Gram_roundoff_rows": roundings,
            "total_rows": rows, "seconds": round(time.perf_counter()-start, 4),
            "moment_error_upper_J_X": [arithmetic.upper(m["error"]) for m in moments],
            "geometry_error_upper_J_X": [[arithmetic.upper(x) for x in geometry[key]] for key in ("eJ", "eX")],
            "phase_error_upper": arithmetic.upper(shared["phase_error"]),
            "root_box": shared["core"]["root_box"], "source_pins": shared["source_pins"],
            "full_Fock_trace_factor": TRACE, "momenta": N, "reference_dimension": 128,
            "fixed_L8_only": True, "all10_and_all16_admission_or_GR_claim": False}
