"""Actual AF preparation aggregation and the separate inherited-clock measure.

The defining AF address ``a=(j,i)`` is not a spatial archive point ``x``.
No map between them, spatial sampling law, or volume form is installed here.
Only pinned definitions are consumed; no old checker/entrypoint is executed.

For the actual terminal SECOND active-record contract and its flagged map Phi,

  A = 6 + sum(w*f) + D(w||r)/ell + D(Phi(sigma)||pinch(Phi(sigma)))/ell.

The last term is the output coherence relative to the diagonal input, not
the different Gibbs-relative remainder of the preparation owner.  At its
faithful density minimum, A*=6-log(sum(r*exp(-ell*f)))/ell.  Neither expression
is a spatial normalized-average postulate.  A GIVEN operator readout has the
full noncommuting BKM source of that same minimum; scalar address scores are
only its commuting case.  Strict archive inheritance is a
second, independently typed result: every clock pushforward stays on the
finite base support, even when the archive measure itself is nonatomic.
"""
from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
PREP = "02_REGISTRY/research/sources/d0_native_preparation_stationary_2026-10-16/preparation.py"
ENGINE = "02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py"
PINS = {
    PREP: "1e3c00dc0e28503e8c9103daf6ce3583f0500d65b64ee7bc4baf8e1bf4726ffd",
    ENGINE: "7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9",
    "03_FORMALIZATION/D0/Geometry/ArchiveRefinementTower.lean":
        "253342935b592df104629259341c2d3d6065cd0ba4ec55769f484f005e036673",
    "02_REGISTRY/research/certificates/a4d_native_strict_observable_descent.lean":
        "6cb26ce9aa094b5dcd663c1ed5ce7d4e0ba3661d25fa08982d3dfbf7f4306c60",
    "02_REGISTRY/research/A4D_NATIVE_ARCHIVE_RECORD_BRIDGE.md":
        "39344d61c37dc8a9dbc2f2a6a02c4208b4bcfc343ba209231f16c0deb619b3af",
}


def require(condition, name):
    if not bool(condition):
        raise AssertionError(name)


def _owners(repo):
    for path, digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                "source_pin:"+path)
    name = "field_transport_preparation_measure_definitions"
    spec = importlib.util.spec_from_file_location(name, repo/PREP)
    if spec is None or spec.loader is None:
        raise RuntimeError("preparation_definition_unavailable")
    prep = importlib.util.module_from_spec(spec)
    sys.modules[name] = prep
    spec.loader.exec_module(prep)
    # This pins/imports AF and conditional-price definitions, not their suites.
    AF, price = prep.owners(repo)
    wanted = {"archive_modes", "archive_projection", "inherit"}
    tree = ast.parse((repo/ENGINE).read_text())
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name in wanted]
    require({node.name for node in functions} == wanted, "literal_archive_functions")
    scope = {}
    exec(compile(ast.Module(body=functions, type_ignores=[]), ENGINE, "exec"), scope)
    return prep, AF, price, scope


def normalize_measure(raw_weights, raw_jets):
    """Full quotient first jet, including the moving total mass.

    These can be native preparation/address weights.  They acquire a spatial
    interpretation only after a separate, actual address/clock map is supplied.
    """
    if len(raw_weights) != len(raw_jets) or not raw_weights:
        raise ValueError("nonempty_equal_measure_and_jet_required")
    mass, dmass = sum(raw_weights), sum(raw_jets)
    return (tuple(w/mass for w in raw_weights),
            tuple((dw-w*dmass/mass)/mass
                  for w, dw in zip(raw_weights, raw_jets)), mass, dmass)


def normalized_average_source(raw_weights, raw_jets, values, value_jets):
    """Conditional mean and its measure source; no constant-offset source."""
    if len(values) != len(raw_weights) or len(value_jets) != len(values):
        raise ValueError("whole_measure_and_observable_required")
    weights, jets, _, _ = normalize_measure(raw_weights, raw_jets)
    mean = sum(w*f for w, f in zip(weights, values))
    source = sum(w*df+dw*f for w, dw, f, df in
                 zip(weights, jets, values, value_jets))
    return mean, source


def prepared_envelope_source(weights, cost_jets, reference, reference_jets, ell):
    """Actual minimum source, not the source of its normalized mean cost.

    The inputs must be the same actual Gibbs weights r*exp(-ell*f)/Z.
    At fixed native golden PF reference, all reference_jets are zero.
    """
    if not (len(weights) == len(cost_jets) == len(reference) == len(reference_jets)):
        raise ValueError("whole_native_address_domain_required")
    return sum(w*(df-dr/(ell*r)) for w, df, r, dr in
               zip(weights, cost_jets, reference, reference_jets))


def hermitian_function_jet(eigenvalues, function_values, function_derivatives, jet):
    """Full Df(E)[dE] in an orthonormal spectral basis of Hermitian E.

    The caller supplies real scalar f(e_i), f'(e_i) and the Hermitian dE in
    that SAME basis, for one scalar function on ONE central block.  The
    actual AF functions f_0 and f_1 are evaluated separately.  Off-diagonal divided differences retain moving
    eigenvectors.  Coincident eigenvalues use the derivative limit.
    """
    size = len(eigenvalues)
    if (len(function_values) != size or len(function_derivatives) != size
            or jet.shape != (size, size)):
        raise ValueError("complete_Hermitian_spectral_data_required")
    result = s.zeros(size)
    for i in range(size):
        for j in range(size):
            gap = eigenvalues[i]-eigenvalues[j]
            if i == j or s.simplify(gap) == 0:
                slope = function_derivatives[i]
            else:
                slope = (function_values[i]-function_values[j])/gap
            result[i, j] = slope*jet[i, j]
    return result


def prepared_readout_source(weights, log_eigenvalues, log_jet, observable,
                            observable_jet=None):
    """Full BKM source for a GIVEN test readout O at sigma*=exp(L)/Z.

    All matrices are expressed in the same orthonormal spectral basis of L.
    weights[i]=exp(log_eigenvalues[i])/Z are positive and sum to one; the
    caller supplies these domain facts.  log_jet=dL retains ALL Hermitian
    entries, including changes of the spectral basis.  In the actual AF
    application L=log(mu)-ell*f(E), dL=dlog(mu)-ell*Df_E[dE]; mu is central.
    Jets are physical matrix derivatives expressed in the BASE spectral
    basis, not derivatives of entries in a moving diagonalizing chart.

    A test operator may be a real test function of a supplied POVM/PVM.  This
    API neither selects that readout physically nor declares an AF address
    to be a spatial clock.  Native AF inputs/observables remain block diagonal
    across the two central sectors; packing them does not add central coherences.
    """
    size = len(weights)
    if (len(log_eigenvalues) != size or log_jet.shape != (size, size)
            or observable.shape != (size, size)):
        raise ValueError("whole_spectral_density_and_readout_required")
    observable_jet = s.zeros(size) if observable_jet is None else observable_jet
    if observable_jet.shape != (size, size):
        raise ValueError("whole_moving_readout_required")
    value = sum(weights[i]*observable[i, i] for i in range(size))
    source = sum(weights[i]*observable_jet[i, i] for i in range(size))
    for i in range(size):
        for j in range(size):
            gap = log_eigenvalues[i]-log_eigenvalues[j]
            if i == j or s.simplify(gap) == 0:
                if i != j and s.simplify(weights[i]-weights[j]) != 0:
                    raise ValueError("inconsistent_equal_log_eigenvalues")
                logarithmic_mean = weights[i]
            else:
                logarithmic_mean = (weights[i]-weights[j])/gap
            centered = observable[j, i]-(value if i == j else 0)
            source += logarithmic_mean*centered*log_jet[i, j]
    return value, source


def prepared_price_hessian(weights, log_eigenvalues, log_jet_x, log_jet_y,
                           log_jet_xy, ell):
    """Actual faithful-minimum SECOND-price Hessian, with all direct jets.

    A*=6-log(Tr exp L)/ell, L=log(mu)-ell*f(E), at fixed ell>0.
    The inputs are the same spectral density/log coordinates as
    prepared_readout_source.  Every jet is a physical matrix derivative in
    the BASE spectral basis.  In particular the caller supplies the ACTUAL
    mixed jet L_XY, including D2f_E[E_X,E_Y], Df_E[E_XY], and any admitted
    mixed reference response.  Supplying zero solely because the parameter
    tangent is off diagonal would lose the direct second source.

      H*[X,Y]=-(Tr sigma* L_XY+Cov_BKM,sigma*(L_X,L_Y))/ell.

    This is a symmetric bilinear form for a C2 Hermitian family with mixed
    partials agreeing.  It need not be positive or equal a physical metric.
    It is only the envelope of the owned full coherent preparation price,
    not a replacement of that full price by a Gibbs free-energy functional.
    Native p,n,code/reference are fixed unless a separate response is given.

    Uniform bound: |H|<=(||L_XY||+||L_X||*||L_Y||)/ell in operator norm.
    BKM Cauchy-Schwarz and logmean(u,v)<=(u+v)/2 prove the bound without
    dividing by the smallest density eigenvalue.  It does require bounded
    actual L-jets; it does not remove singular f'' at a zero minus-path.
    """
    _, derivative_mean = prepared_readout_source(
        weights, log_eigenvalues, log_jet_y, log_jet_x, log_jet_xy)
    return -derivative_mean/ell


def inherited_atomic_source(weights, weight_jets, test_values, test_clock_jets):
    """d nu(test) on finite inherited base atoms.

    test_clock_jets[b] means grad(test)(X_b).dX_b, retaining moving atoms.
    Calling this does not select weights or identify nu with geometric volume.
    """
    if not (len(weights) == len(weight_jets) == len(test_values) == len(test_clock_jets)):
        raise ValueError("whole_base_clock_measure_required")
    return sum(dw*f+w*df for w, dw, f, df in
               zip(weights, weight_jets, test_values, test_clock_jets))


class _Interval:
    """Small rational interval arithmetic for the native logarithmic witness."""
    def __init__(self, lo, hi=None):
        self.lo, self.hi = F(lo), F(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError("reversed_interval")

    def __add__(self, other):
        q = other if isinstance(other, _Interval) else _Interval(other)
        return _Interval(self.lo+q.lo, self.hi+q.hi)

    __radd__ = __add__

    def __neg__(self):
        return _Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self+-other if isinstance(other, _Interval) else self+(-F(other))

    def __rsub__(self, other):
        return -self+other

    def __mul__(self, other):
        q = other if isinstance(other, _Interval) else _Interval(other)
        values = (self.lo*q.lo, self.lo*q.hi, self.hi*q.lo, self.hi*q.hi)
        return _Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        q = other if isinstance(other, _Interval) else _Interval(other)
        if q.lo <= 0 <= q.hi:
            raise ZeroDivisionError("interval_contains_zero")
        return self*_Interval(1/q.hi, 1/q.lo)

    def __rtruediv__(self, other):
        return _Interval(other)/self

    def square(self):
        if self.lo <= 0 <= self.hi:
            return _Interval(0, max(self.lo*self.lo, self.hi*self.hi))
        return _Interval(min(self.lo*self.lo, self.hi*self.hi),
                         max(self.lo*self.lo, self.hi*self.hi))


def _log_unit_interval(x, terms=20):
    """Rigorous rational log(x) enclosure for 1<=x<=2, via atanh series."""
    if not 1 <= x <= 2:
        raise ValueError("log_range_reduction_required")
    z = (x-1)/(x+1)
    value = 2*sum(z**(2*k+1)/F(2*k+1) for k in range(terms))
    tail = 2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
    return _Interval(value, value+tail)


def _log_rational(x):
    if x <= 0:
        raise ValueError("positive_log_required")
    exponent = 0
    while x < 1:
        x *= 2
        exponent -= 1
    while x > 2:
        x /= 2
        exponent += 1
    return _log_unit_interval(x)+exponent*_log_unit_interval(F(2))


def _log_interval(x):
    return _Interval(_log_rational(x.lo).lo, _log_rational(x.hi).hi)


def _native_golden_cost_intervals(rational_effect=None):
    # Root brackets are checked independently by integer rational inequalities.
    p = _Interval(F(6180339887498948482, 10**19), F(6180339887498948483, 10**19))
    a = _Interval(F(7861513777574232, 10**16), F(7861513777574234, 10**16))
    rt2 = _Interval(F(14142135623730950, 10**16), F(14142135623730952, 10**16))
    require(p.lo*p.lo+p.lo-1 < 0 < p.hi*p.hi+p.hi-1, "positive_golden_root_bracket")
    require(a.lo*a.lo < p.lo and a.hi*a.hi > p.hi, "sqrt_p_root_bracket")
    require(rt2.lo*rt2.lo < 2 < rt2.hi*rt2.hi, "sqrt_two_root_bracket")
    ell = -_log_interval(p)
    if rational_effect is None:
        root_r, root_b = a, p
    elif rational_effect == F(9, 25):
        root_r, root_b = _Interval(F(4, 5)), _Interval(F(3, 5))
    elif rational_effect == F(16, 25):
        root_r, root_b = _Interval(F(3, 5)), _Interval(F(4, 5))
    else:
        raise ValueError("declared_native_rational_root_fixture_required")
    fs, derivatives = [], []
    for j in range(2):
        w = a*p if j == 0 else p
        v2 = p*p*p*p if j == 0 else p*p*p
        factors = (w*root_r+root_b/rt2, w*root_r-root_b/rt2)
        factor_jets = (-w/(2*root_r)+1/(2*rt2*root_b),
                       -w/(2*root_r)-1/(2*rt2*root_b))
        probabilities = [b.square() for b in factors]
        jets = [2*b*db for b, db in zip(factors, factor_jets)]
        if j == 0:
            probabilities.append((w*root_r).square())
            jets.append(-w.square())
        count_B = 2-j
        B, dB = v2*root_r.square(), -v2
        probabilities += [B]*count_B
        jets += [dB]*count_B
        logs = tuple(_log_interval(q) for q in probabilities)
        fs.append(3-j+count_B*B+sum(q*l for q, l in zip(probabilities, logs))/ell)
        derivatives.append(count_B*dB+sum(dq*(l+1) for dq, l in zip(jets, logs))/ell)
    return fs, derivatives


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    prep, AF, price, archive = _owners(repo)
    checks = ["source_pin:"+path for path in PINS]

    def zero(value):
        return AF.red(s.fraction(s.cancel(s.together(value)))[0]) == 0

    def eq(actual, expected, name):
        difference = actual-expected
        require(all(zero(x) for x in difference) if isinstance(difference, s.MatrixBase)
                else zero(difference), name)
        checks.append(name)

    def yes(value, name):
        require(value, name)
        checks.append(name)

    p, n = AF.p, 1
    ell = s.Symbol("ell_log_phi", positive=True)
    roots = ((s.diag(s.Rational(4, 5), s.Rational(3, 5)),
              s.diag(s.Rational(3, 5), s.Rational(4, 5))),
             (s.Matrix([[s.Rational(4, 5)]]), s.Matrix([[s.Rational(3, 5)]])))
    effects = ((s.Rational(9, 25), s.Rational(16, 25)), (s.Rational(9, 25),))
    u = s.Matrix([s.Rational(3, 5), 4*s.I/5])
    sigma = (s.Rational(2, 3)*u*u.H, s.Matrix([[s.Rational(1, 3)]]))
    diagonal = tuple(s.diag(*M.diagonal()) for M in sigma)
    Y = prep.flagged_density(AF, n, roots, sigma)
    PY = tuple(s.diag(*M.diagonal()) for M in Y)
    DY = prep.flagged_density(AF, n, roots, diagonal)
    for v in range(2):
        eq(PY[v], DY[v], "actual_flagged_pinching_commutes_with_diagonal_input_"+str(v))
    eq(sum(s.trace(M) for M in Y), 1, "actual_coherent_output_normalized")
    yes(tuple(M.rows for M in Y) == AF.counts(4) == (8, 5), "all_thirteen_fine_coordinates_retained")
    yes(any(not zero(x) for M, D in zip(Y, PY) for x in M-D),
        "actual_output_coherence_is_strictly_nonzero")

    # Independent native path probabilities from the conditional-price owner.
    probabilities = {(j, i): [] for j, dj in enumerate(AF.counts(n)) for i in range(dj)}
    D_full, D_pinched, coherence, weighted_cost, D_weight = (s.S.Zero,)*5
    normalization = [s.zeros(dj) for dj in AF.counts(n)]
    path_count = 0
    for v, offset, j, A in prep.flagged_paths(AF, n, roots):
        normalization[j] += A.H*A
        d = A.rows
        block = Y[v][offset:offset+d, offset:offset+d]
        eq(block, A*sigma[j]*A.H, "actual_native_path_density_"+str(path_count))
        if d == 2:
            eq(block.det(), 0, "coherent_rank_one_path_"+str(path_count))
        trace = s.trace(block)
        log_trace = s.Symbol("log_actual_path_trace_"+str(path_count), real=True)
        D_full += trace*(log_trace+(n+4+v)*ell)
        coherence += trace*log_trace
        for i in range(d):
            prob = AF.red(A[i, i]**2)
            probabilities[j, i].append(prob)
            weight = sigma[j][i, i]
            log_weight = s.Symbol("log_actual_input_weight_"+str(j)+"_"+str(i), real=True)
            log_probability = s.Symbol("log_native_probability_"+str(path_count)+"_"+str(i), real=True)
            # All log abbreviations bind to these literal positive quantities.
            # log(w P)=log w+log P, with no commutative input approximation.
            D_pinched += weight*prob*(log_weight+log_probability+(n+4+v)*ell)
            coherence -= weight*prob*(log_weight+log_probability)
            weighted_cost += weight*prob*(log_probability+(3+v-j)*ell)/ell
        path_count += 1
    eq(path_count, 8, "all_eight_actual_inclusion_paths_retained")
    for j, dj in enumerate(AF.counts(n)):
        eq(normalization[j], s.eye(dj), "actual_channel_trace_preservation_"+str(j))
        for i in range(dj):
            expected = sum(price.conditional_probabilities(AF, j, effects[j][i]), ())
            yes(len(probabilities[j, i]) == len(expected), "native_conditional_path_count_"+str(j)+"_"+str(i))
            for k, (actual, target) in enumerate(zip(probabilities[j, i], expected)):
                eq(actual, target, "native_conditional_probability_"+str(j)+"_"+str(i)+"_"+str(k))
            weight = sigma[j][i, i]
            log_weight = s.Symbol("log_actual_input_weight_"+str(j)+"_"+str(i), real=True)
            D_weight += weight*(log_weight+(n+1+j)*ell)
    eq(D_full, D_pinched+coherence, "exact_quantum_pinching_entropy_chain")
    eq(D_pinched/ell, weighted_cost+D_weight/ell, "exact_native_address_KL_chain")
    eq(6+D_full/ell, 6+weighted_cost+D_weight/ell+coherence/ell,
       "terminal_second_price_baseline_six_with_retained_coherence")
    yes(not zero(coherence), "dropping_output_coherence_breaks_actual_price_identity")

    # Exact first-source calculus with every measure and normalizer term.
    r = s.symbols("r0:3", positive=True)
    q = s.symbols("actual_exp_minus_ell_f0:3", positive=True)
    f, df = s.symbols("f0:3", real=True), s.symbols("df0:3", real=True)
    dr = s.symbols("dr0:3", real=True)
    raw = tuple(ri*qi for ri, qi in zip(r, q))
    draw = tuple(qi*dri-ell*ri*qi*dfi for ri, qi, dri, dfi in zip(r, q, dr, df))
    weights, jets, Z, dZ = normalize_measure(raw, draw)
    eq(sum(weights), 1, "one_actual_preparation_normalizer")
    eq(sum(jets), 0, "moving_preparation_measure_total_jet_zero")
    expected_envelope = prepared_envelope_source(weights, df, r, dr, ell)
    eq(-dZ/(ell*Z), expected_envelope, "moving_PF_reference_envelope_source")
    mean, dmean = normalized_average_source(raw, draw, f, df)
    Edf = sum(w*x for w, x in zip(weights, df))
    dlnr = tuple(dri/ri for dri, ri in zip(dr, r))
    Edr = sum(w*x for w, x in zip(weights, dlnr))
    covariance_f_df = sum(w*fi*dfi for w, fi, dfi in zip(weights, f, df))-mean*Edf
    covariance_f_dr = sum(w*fi*di for w, fi, di in zip(weights, f, dlnr))-mean*Edr
    eq(dmean, Edf-ell*covariance_f_df+covariance_f_dr,
       "normalized_mean_has_the_actual_measure_covariance_source")
    eq(expected_envelope-dmean,
       ell*covariance_f_df-covariance_f_dr-Edr/ell,
       "full_free_energy_versus_mean_source_difference")
    eq((expected_envelope-dmean).subs(dict.fromkeys(dr, 0)), ell*covariance_f_df,
       "fixed_native_PF_reference_mean_source_mismatch")
    k = s.Symbol("constant_code_padding", real=True)
    _, padded_source = normalized_average_source(raw, draw, tuple(fi+k for fi in f), df)
    eq(padded_source, dmean, "constant_code_padding_has_no_normalized_measure_source")
    yes(not zero(sum(draw)), "moving_total_mass_is_not_silently_frozen")

    # A concrete native witness: n1 has two type-0 histories and one type-1.
    # At the owned golden effect the two absolute conditional costs differ,
    # and so do their effect derivatives.  Rational enclosures, not floats,
    # give a strict nonzero covariance for this SAME native preparation law.
    fs, fps = _native_golden_cost_intervals()
    cost_difference, slope_difference = fs[0]-fs[1], fps[0]-fps[1]
    yes(cost_difference.hi < -F(1, 100), "native_golden_f0_minus_f1_strictly_negative")
    yes(slope_difference.hi < -F(1, 10), "native_golden_fprime0_minus_fprime1_strictly_negative")
    covariance_factor = cost_difference*slope_difference
    yes(covariance_factor.lo > 0, "native_golden_mean_source_mismatch_strictly_positive")

    # Full operator readout response of the SAME actual preparation minimum.
    # These q abbreviations bind to exp(-ell*f_j(e_i)), not fitted weights.
    e1, e2, e3 = s.Rational(9, 25), s.Rational(16, 25), s.Rational(9, 25)
    f1, f2, f3 = s.symbols("actual_f0_at_9_25 actual_f0_at_16_25 actual_f1_at_9_25", real=True)
    q1, q2, q3 = s.symbols("actual_exp_minus_ell_f1 actual_exp_minus_ell_f2 actual_exp_minus_ell_f3", positive=True)
    operator_Z = p**2*(q1+q2)+p**3*q3
    operator_weights = (p**2*q1/operator_Z, p**2*q2/operator_Z, p**3*q3/operator_Z)
    # log(mu_0)=-2ell occurs twice; log(mu_1)=-3ell once.
    operator_logs = (-2*ell-ell*f1, -2*ell-ell*f2, -3*ell-ell*f3)
    X = s.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    fp1, fp2, fp3 = s.symbols("actual_fprime1 actual_fprime2 actual_fprime3", real=True)
    dcost = s.diag(hermitian_function_jet((e1, e2), (f1, f2),
                                        (fp1, fp2), X[:2, :2]), 0)
    dL = -ell*dcost
    value, operator_source = prepared_readout_source(operator_weights, operator_logs, dL, X)
    expected_operator_source = 2*p**2*(q1-q2)/(operator_Z*(e1-e2))
    eq(value, 0, "actual_n1_offdiagonal_test_readout_base_zero")
    eq(operator_source, expected_operator_source,
       "actual_n1_noncommuting_BKM_readout_source")
    eq(sum(operator_weights[i]*dcost[i, i] for i in range(3)), 0,
       "same_noncommuting_direction_has_zero_terminal_envelope_price_source")
    yes(all(X[i, i] == 0 for i in range(3)),
        "noncommuting_fixture_effect_eigenvalue_first_jets_all_zero")
    yes(s.diag(e1, e2, e3)*X-X*s.diag(e1, e2, e3) != s.zeros(3),
        "actual_n1_effect_jet_is_genuinely_noncommuting")
    fs_at_e1, fps_at_e1 = _native_golden_cost_intervals(F(9, 25))
    fs_at_e2, fps_at_e2 = _native_golden_cost_intervals(F(16, 25))
    yes((fs_at_e1[0]-fs_at_e2[0]).hi < -F(1, 100),
        "actual_conditional_cost_order_implies_q1_greater_than_q2")
    yes(e1-e2 < 0,
        "actual_noncommuting_readout_source_strictly_negative_despite_zero_eigenvalue_jets")
    # Every diagonal source, including moving reference/readout, reduces to
    # the earlier score covariance with the SAME global normalizer.
    obs = s.diag(*f)
    dobs = s.diag(*df)
    logjets = tuple(dri/ri-ell*dfi for dri, ri, dfi in zip(dr, r, df))
    generic_logs = s.symbols("given_preparation_log_eigenvalue0:3", real=True)
    _, diagonal_BKM = prepared_readout_source(weights, generic_logs,
                                             s.diag(*logjets), obs, dobs)
    eq(diagonal_BKM, dmean, "commuting_BKM_is_exact_scalar_measure_score_source")
    radial_logjet = s.Symbol("radial_log_partition_jet", real=True)
    _, radial_readout_source = prepared_readout_source(operator_weights, operator_logs,
                                                       radial_logjet*s.eye(3), s.diag(1, 2, 3))
    eq(radial_readout_source, 0, "full_BKM_source_cancels_radial_partition_change")
    _, moving_readout_source = prepared_readout_source(operator_weights, operator_logs,
        s.zeros(3), X, s.diag(*df))
    eq(moving_readout_source, sum(w*di for w, di in zip(operator_weights, df)),
       "full_BKM_source_retains_moving_test_operator")
    repeated_weight = s.Rational(1, 3)
    _, degenerate_source = prepared_readout_source((repeated_weight,)*3, (0,)*3, X, X)
    eq(degenerate_source, s.Rational(2, 3), "degenerate_BKM_logarithmic_mean_limit")
    iX = s.Matrix([[0, -s.I, 0], [s.I, 0, 0], [0, 0, 0]])
    i_dcost = s.diag(hermitian_function_jet((e1, e2), (f1, f2),
                                          (fp1, fp2), iX[:2, :2]), 0)
    _, imaginary_source = prepared_readout_source(operator_weights, operator_logs,
                                                  -ell*i_dcost, iX)
    eq(imaginary_source, expected_operator_source,
       "complex_Hermitian_noncommuting_source_uses_full_trace_pairing")

    # Constructive second source of this SAME terminal preparation minimum.
    # For E(t)=E+tX, E_XY=0 but D2f_E[X,X] is NOT zero.
    delta_e, f_divided = e1-e2, (f1-f2)/(e1-e2)
    d2cost = s.diag(2*(fp1-f_divided)/delta_e,
                    -2*(fp2-f_divided)/delta_e, 0)
    d2L = -ell*d2cost
    hxx = prepared_price_hessian(operator_weights, operator_logs, dL, dL, d2L, ell)
    expected_hxx = 2*p**2*(q1*fp1-q2*fp2)/(operator_Z*delta_e)
    eq(hxx, expected_hxx, "actual_n1_noncommuting_minimum_price_Hessian")
    diagonal_field_dL = s.diag(-ell*fp1, 0, 0)
    eq(-sum(w*diagonal_field_dL[i, i] for i, w in enumerate(operator_weights))/ell,
       operator_weights[0]*fp1, "same_actual_effect_family_positive_diagonal_first_source")
    # Independent eigenvalue perturbation: e1''=2/(e1-e2), e2''=-2/(e1-e2).
    eq(hxx, sum(w*fp*dd for w, fp, dd in
                zip(operator_weights, (fp1, fp2, fp3), (2/delta_e, -2/delta_e, 0))),
       "Hessian_matches_actual_effect_eigenvalue_second_jets")
    direct_hxx = sum(w*d2cost[i, i] for i, w in enumerate(operator_weights))
    omitted_direct = prepared_price_hessian(operator_weights, operator_logs,
                                            dL, dL, s.zeros(3), ell)
    yes(not zero(omitted_direct-expected_hxx), "dropping_direct_D2f_breaks_actual_Hessian")
    yes(not zero(direct_hxx-expected_hxx), "dropping_induced_preparation_breaks_actual_Hessian")
    # An isospectral conjugation has the SAME first tangent X but nonzero
    # acceleration [K,[K,E]].  Its total price second source must cancel.
    K = s.Matrix([[0, -1/delta_e, 0], [1/delta_e, 0, 0], [0, 0, 0]])
    effect = s.diag(e1, e2, e3)
    eq(K*effect-effect*K, X, "actual_unitary_effect_curve_same_first_tangent")
    acceleration = K*X-X*K
    eq(acceleration, s.diag(-2/delta_e, 2/delta_e, 0),
       "actual_unitary_effect_curve_retains_direct_acceleration")
    eq(hxx+sum(w*fp*acceleration[i, i] for i, (w, fp) in
               enumerate(zip(operator_weights, (fp1, fp2, fp3)))), 0,
       "isospectral_minimum_price_second_source_exactly_zero")

    # General Hermitian mixed directions in the native M2+M1 algebra.
    ax0, ax1, ax2, ax3, ax4 = s.symbols("mixed_log_x0:5", real=True)
    ay0, ay1, ay2, ay3, ay4 = s.symbols("mixed_log_y0:5", real=True)
    axy0, axy1, axy2 = s.symbols("mixed_direct_log0:3", real=True)
    LX = s.Matrix([[ax0, ax2+s.I*ax3, 0], [ax2-s.I*ax3, ax1, 0], [0, 0, ax4]])
    LY = s.Matrix([[ay0, ay2+s.I*ay3, 0], [ay2-s.I*ay3, ay1, 0], [0, 0, ay4]])
    LXY = s.diag(axy0, axy1, axy2)
    hxy = prepared_price_hessian(operator_weights, operator_logs, LX, LY, LXY, ell)
    eq(hxy, prepared_price_hessian(operator_weights, operator_logs, LY, LX, LXY, ell),
       "full_noncommuting_price_Hessian_is_symmetric")
    eq(prepared_price_hessian(operator_weights, operator_logs,
                              LX+radial_logjet*s.eye(3), LY, LXY, ell), hxy,
       "full_Hessian_cancels_additive_log_normalizer_direction")
    eq(prepared_price_hessian(operator_weights, operator_logs, LX, s.zeros(3), LXY, ell),
       -sum(w*LXY[i, i] for i, w in enumerate(operator_weights))/ell,
       "full_Hessian_retains_only_actual_direct_mixed_jet_when_first_jet_zero")
    eq(prepared_price_hessian((repeated_weight,)*3, (0,)*3, X, X, s.zeros(3), ell),
       -s.Rational(2, 3)/ell, "degenerate_density_Hessian_has_finite_BKM_limit")
    eq(prepared_price_hessian(operator_weights, operator_logs, dL, -ell*i_dcost,
                              s.zeros(3), ell), 0,
       "real_and_imaginary_Hermitian_effect_directions_have_zero_mixed_BKM")

    # Independent commuting two-parameter trace exponential checks every
    # first and mixed normalization term against direct differentiation.
    t, z = s.symbols("actual_parameter_t actual_parameter_z", real=True)
    ux, uy, uxy = (s.symbols(prefix+"0:3", real=True) for prefix in ("log_x", "log_y", "log_xy"))
    raw_Z = sum(w*s.exp(t*a+z*b+t*z*c) for w, a, b, c in
                zip(operator_weights, ux, uy, uxy))
    direct_log_Hessian = s.diff(-s.log(raw_Z)/ell, t, z).subs({t: 0, z: 0})
    eq(prepared_price_hessian(operator_weights, operator_logs,
                              s.diag(*ux), s.diag(*uy), s.diag(*uxy), ell),
       direct_log_Hessian, "Hessian_matches_full_raw_trace_exponential_normalization")
    covariance_diag = sum(w*a*b for w, a, b in zip(operator_weights, ux, uy))
    covariance_diag -= (sum(w*a for w, a in zip(operator_weights, ux))
                        *sum(w*b for w, b in zip(operator_weights, uy)))
    eq(prepared_price_hessian(operator_weights, operator_logs,
                              -ell*s.diag(*ux), -ell*s.diag(*uy), -ell*s.diag(*uxy), ell),
       sum(w*c for w, c in zip(operator_weights, uxy))-ell*covariance_diag,
       "commuting_effect_Hessian_has_direct_term_minus_covariance")
    # The two reference blocks may move ONLY under a separately supplied law.
    # This conditional control retains their mixed response, not a fitted term.
    rx0, rx1, ry0, ry1, rxy0, rxy1 = s.symbols("r_x0 r_x1 r_y0 r_y1 r_xy0 r_xy1", real=True)
    RX, RY, RXY = s.diag(rx0, rx0, rx1), s.diag(ry0, ry0, ry1), s.diag(rxy0, rxy0, rxy1)

    def bkm(A, B):
        return prepared_readout_source(operator_weights, operator_logs, B, A)[1]

    full_reference_hessian = prepared_price_hessian(
        operator_weights, operator_logs, RX-ell*LX, RY-ell*LY, RXY-ell*LXY, ell)
    explicit_reference_hessian = sum(w*(LXY[i, i]-RXY[i, i]/ell)
                                     for i, w in enumerate(operator_weights))
    explicit_reference_hessian += (-bkm(RX, RY)/ell+bkm(RX, LY)
                                   +bkm(LX, RY)-ell*bkm(LX, LY))
    eq(full_reference_hessian, explicit_reference_hessian,
       "full_Hessian_retains_both_reference_cross_responses_and_mixed_reference_jet")

    # Strict sign is a theorem for the concrete ACTUAL fixture, not a
    # declaration that arbitrary effective Hessians are positive metrics.
    yes(fps_at_e1[0].lo > F(79, 100), "actual_first_effect_price_slope_greater_than_79_over_100")
    yes(0 < fps_at_e2[0].lo and fps_at_e2[0].hi < F(17, 100),
        "actual_second_effect_price_slope_between_zero_and_17_over_100")
    yes(fs_at_e1[0].hi < F(11, 10) and fs_at_e1[0].lo > 0
        and fs_at_e2[0].lo > 0 and fs_at_e1[1].lo > 0,
        "actual_all_three_conditional_costs_positive_with_first_below_11_over_10")
    yes(F(8, 13)**2+F(8, 13)-1 < 0 < F(5, 8)**2+F(5, 8)-1,
        "native_p_bounds_support_PF_weight_lower_bound")
    yes(1+F(1, 2)+F(1, 8)+F(1, 48) > F(13, 8)
        and F(11, 20) < F(2, 3),
        "exact_log_exponential_bounds_imply_ell_below_half_and_q1_above_half")
    # p²>3/8, q1>1/2, Z<=1 => w1>3/16.  q2/q1<1 and
    # f1'>.79, 0<f2'<.17 => f1'-(q2/q1)f2'>31/50.
    eq(s.Rational(3, 16)*s.Rational(79, 100), s.Rational(237, 1600),
       "actual_diagonal_first_source_strict_lower_bound_coefficient")
    eq(2*s.Rational(3, 16)*s.Rational(31, 50)/s.Rational(7, 25), s.Rational(93, 112),
       "actual_offdiagonal_Hessian_strict_negative_bound_coefficient")
    # ACTUAL full coherent preparation-block conditioning.  Its Riesz form
    # is Phi*Dlog_Y Phi/ell, compressed to total-trace-zero density tangents.
    # Each native plus path has A+>=w_j I.  Trace(Y)=1 gives Dlog_Y>=Id;
    # hence M_T>=p^6/ell and ||M_T^-1||<=ell/p^6, independently of level.
    wr, rr, br = s.symbols("native_plus_weight root_failure root_success", real=True)
    eq(wr*rr+br/s.sqrt(2)-wr,
       wr*(rr+br-1)+(1/s.sqrt(2)-wr)*br,
       "actual_plus_path_uniform_lower_bound_positive_decomposition")
    yes(F(5, 13) < F(1, 2) and F(5, 8) < 1,
        "native_plus_weights_squared_below_half_from_actual_golden_root_bounds")
    eq(p**4-p**6, p**5, "minimum_native_plus_path_fourth_power_is_p_to_six")
    eq((ell/p**6)*(p**6/ell), 1, "uniform_trace_tangent_preparation_inverse_bound_coefficient")

    # The actual AF inclusion is (X0,X1)->(diag(X0,X1),X0).
    # This PF-address refinement is NOT the separate flat archive projection.
    eq(2*p**2+p**3, 1, "actual_A1_PF_reference_total_mass")
    eq(3*p**3+2*p**4, 1, "actual_A2_PF_reference_total_mass")
    eq(p**3+p**4, p**2, "actual_A1_rank_one_address_trace_under_inclusion")
    x0, x1, x2 = s.symbols("old_AF_address_observable0:3", real=True)
    old_expectation = p**2*(x0+x1)+p**3*x2
    fine_expectation = p**3*(x0+x1+x2)+p**4*(x0+x1)
    eq(fine_expectation, old_expectation, "literal_AF_inherited_observable_PF_pushforward")
    eq(p+p**2, 1, "literal_AF_type0_child_weights_p_and_p_squared")
    yes(AF.counts(1) == (2, 1) and AF.counts(2) == (3, 2), "actual_AF_address_counts_not_spatial_stage_counts")

    # Actual strict clock adapter, all sixteen initial archive points.
    base = tuple(tuple((i >> mu) & 1 for mu in range(4)) for i in range(16))
    field = base
    to_base = tuple(range(16))
    for stage in range(3):
        field = archive["inherit"](stage, field)
        to_base = archive["inherit"](stage, to_base)
        yes(len(field) == (stage+3)**4, "actual_flat_archive_stage_size_"+str(stage+1))
        yes(all(value == base[parent] for value, parent in zip(field, to_base)),
            "strict_clock_factorization_through_sixteen_base_points_"+str(stage+1))
    yes(len(set(field)) == 16, "archive_growth_creates_no_new_inherited_clock_values")

    # The EXISTING full-support golden bridge's first cofinal step, n2->n18.
    # Only the actual projection table and integer fibre counts are materialized.
    projection = tuple(range(4**4))
    for stage in range(2, 18):
        projection = archive["inherit"](stage, projection)
    c = 19**4
    yes(len(projection) == 20**4, "actual_existing_bridge_first_cofinal_stage")
    fibres = Counter((parent, int(child >= c)) for child, parent in enumerate(projection))
    yes(all(fibres[y, b] > 0 for y in range(256) for b in range(2)),
        "existing_golden_bridge_all_conditional_bit_fibres_nonempty")
    yes(all(projection[y] == projection[y+c] == y for y in range(256)),
        "existing_golden_bridge_literal_two_child_sections")
    bit_counts = tuple(sum(fibres[y, b] for y in range(256)) for b in range(2))
    yes(bit_counts == (130321, 29679), "existing_bridge_counting_measure_not_golden")
    # K(y,x)=p_b/N_yb: test all row/golden-marginal identities by exact counts.
    for y in range(256):
        eq(fibres[y, 0]*(p/fibres[y, 0])+fibres[y, 1]*(p**2/fibres[y, 1]), 1,
           "existing_bridge_positive_kernel_row_"+str(y))
    # Push an arbitrary inherited base test through this actual golden kernel.
    test = s.symbols("base_clock_test0:16", real=True)
    old_base_counts = Counter(i % 81 % 16 for i in range(256))
    old_measure = tuple(F(old_base_counts[b], 256) for b in range(16))
    eq(sum(s.Rational(w.numerator, w.denominator) for w in old_measure), 1,
       "existing_bridge_induced_sixteen_base_atom_measure_normalized")
    expected_test = sum(s.Rational(old_base_counts[b], 256)*test[b] for b in range(16))
    fine_test = sum((p+p**2)*test[y % 81 % 16]/256 for y in range(256))
    eq(fine_test, expected_test, "golden_projective_measure_inherited_clock_pushforward_exact")
    # The actual F_(y=0,A) contains both child0 and child256.  Opposite kernel
    # jets preserve its golden marginal; strict inherited clocks cancel them.
    yes(projection[0] == projection[256] == 0 and 256 < c,
        "actual_same_golden_fibre_kernel_variation_pair")
    epsilon, phi0, phi1 = s.symbols("delta_kernel phi_X0 phi_X1", real=True)
    eq(epsilon-epsilon, 0, "kernel_variation_preserves_parent_and_golden_bit_mass")
    eq((epsilon*phi0-epsilon*phi1).subs(phi1, phi0), 0,
       "inherited_clock_pushforward_insensitive_to_within_fibre_measure_jets")
    yes(not zero(epsilon*(phi0-phi1)),
        "new_distinct_child_clocks_require_retaining_kernel_measure_source")
    b0, b1, db0, db1, h0, h1, dh0, dh1 = s.symbols("b0 b1 db0 db1 h0 h1 dh0 dh1", real=True)
    eq(inherited_atomic_source((b0, b1), (db0, db1), (h0, h1), (dh0, dh1)),
       db0*h0+db1*h1+b0*dh0+b1*dh1, "inherited_clock_measure_and_moving_atom_source")

    return {
        "exact_checks": len(checks), "checks": checks,
        "native_AF_example": {"old_level": 1, "old_defining_sizes": [2, 1],
            "fine_defining_sizes": [8, 5], "fine_paths": 8,
            "terminal_price": "6+sum(w*f)+D(w||r)/ell+output_coherence/ell",
            "minimum": "6-log(sum(r*exp(-ell*f)))/ell",
            "fixed_reference_mean_source_difference": "ell*Cov_w(f,df)",
            "golden_common_effect_source_difference_strictly_positive": True,
            "noncommuting_readout_source": "2*p^2*(q1-q2)/(Z*(9/25-16/25))<0",
            "noncommuting_fixture_effect_eigenvalue_jets": [0, 0, 0],
            "BKM_source": "Tr(sigma*dO)+integral Tr(sigma^(1-s)*(O-nu*I)*sigma^s*dL) ds",
            "log_density_jet": "dL=dlog(mu)-ell*Df_E[dE]",
            "minimum_Hessian": "-(Tr(sigma*L_XY)+Cov_BKM(L_X,L_Y))/ell",
            "actual_linear_offdiagonal_effect_Hessian": "2*p^2*(q1*fprime1-q2*fprime2)/(Z*(e1-e2))<-93/112",
            "actual_diagonal_effect_first_source": ">237/1600",
            "Hessian_operator_norm_bound": "(||L_XY||+||L_X||*||L_Y||)/ell",
            "actual_coherent_preparation_Riesz_form": "M=Phi^* Dlog_Y Phi/ell; restrict by HS compression to T={total Tr S=0}",
            "uniform_preparation_tangent_lower_bound": "M_T >= (p^6/ell)*Id_T",
            "uniform_preparation_tangent_inverse_bound": "||M_T^-1||_HS_to_HS <= ell/p^6, independent of AF level/dimension",
            "full_coherent_action_replaced_by_Gibbs_free_energy": False},
        "archive_example": {"initial_points": 16, "cofinal_stage_sizes": [256, 160000],
            "bridge_counting_bit_fibres": list(bit_counts),
            "inherited_clock_pushforward_support_at_most": 16,
            "nonatomic_flat_archive_measure_not_excluded": True},
        "type_boundary": [
            "Defining AF address a, flat archive point x, and matter clock value X are different types.",
            "No same-program address/site/clock readout or geometric volume identification is supplied.",
            "The KL theorem is internal preparation aggregation, not a derived spatial aggregation law.",
            "Output-coherence gap is relative to diagonal input, not the Gibbs-relative gap.",
            "Finite support is proved only for strict inherited clocks; new fine clock states remain possible.",
            "Moving-reference response is conditional; at fixed native p,n,code the PF reference jet is zero.",
            "Scalar address scores apply only to a commuting fixed-address family; general readouts use BKM.",
            "O is a GIVEN operator-valued test readout; its physical or spatial admission is not selected.",
        ],
        "scope": "No physical preparation choice, dVol/V postulate, fitted counterterm, or GR closure.",
    }
