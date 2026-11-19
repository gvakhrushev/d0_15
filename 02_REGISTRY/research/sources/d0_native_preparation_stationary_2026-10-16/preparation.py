#!/usr/bin/env python3
"""Faithful preparation minimum of the inherited SECOND AF operator price.

The actual four-copy frame induces the flagged CP channel below for arbitrary
coherent square-GNS amplitudes.  This is an optimization inside that preparation
domain, not a physical preparation/admission law.  Proper-support amplitude
critical points are retained; density-minimum uniqueness does not remove them.
Only pinned definitions are loaded.  No old certificate is executed.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
AF_PATH = "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py"
PRICE_PATH = "02_REGISTRY/research/sources/d0_jacobian_controlled_record_2026-10-16/controlled_record.py"
TRANSFER_PATH = "02_REGISTRY/research/sources/d0_canonical_trace_record_source_2026-10-15/canonical_source.py"
PINS = {
    AF_PATH: "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    PRICE_PATH: "dd3b7aa6f661dbef4117b2913e62136447a14e2d08a16b08b325cb688874f4ff",
    TRANSFER_PATH: "e192cfccbe09daef50dbddddb0f9725a48b88ca485105389bb85fa801611154b",
}


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def owners(repo: Path):
    """Pin all consumed sources; import only the two needed definition modules."""
    for path, digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                "source_pin:" + path)
    loaded = []
    for index, path in enumerate((AF_PATH, PRICE_PATH)):
        name = "preparation_stationary_owned_definition_" + str(index)
        spec = importlib.util.spec_from_file_location(name, repo/path)
        if spec is None or spec.loader is None:
            raise RuntimeError("owner_definition_unavailable:" + path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        loaded.append(module)
    return tuple(loaded)


def flagged_paths(AF, n: int, roots):
    """(fine block, offset, old type, A) in ACTUAL three-inclusion order.

    roots[j]=(sqrt(I-E_j),sqrt(E_j)) act on old LEFT rows.  Each output
    factor is A*C_j, retaining all coherences and both native blocks.
    """
    if len(roots) != 2:
        raise ValueError("both_native_blocks_required")
    sizes = AF.counts(n)
    result = []
    for v, segments in enumerate(AF.frame(n)["segments"]):
        seen = [0, 0]
        for j, _path, offset in segments:
            r, b = roots[j]
            if r.shape != (sizes[j], sizes[j]) or b.shape != r.shape:
                raise ValueError("whole_old_left_blocks_required")
            A = AF.root_weight(3+v-j)*r
            if v == 0 and seen[j] < 2:
                A += (1 if seen[j] == 0 else -1)*b/s.sqrt(2)
            seen[j] += 1
            result.append((v, offset, j, A))
    return tuple(result)


def flagged_factors(AF, n: int, roots, amplitudes):
    """Fine normalized-HS factor matrices, including every native path."""
    out = [s.zeros(d) for d in AF.counts(n+3)]
    for v, offset, j, A in flagged_paths(AF, n, roots):
        d = A.rows
        out[v][offset:offset+d, offset:offset+d] = A*amplitudes[j]
    return tuple(out)


def flagged_density(AF, n: int, roots, densities):
    """Linear CP map Phi_E on defining AF densities, not on B(H_n) states."""
    out = [s.zeros(d) for d in AF.counts(n+3)]
    for v, offset, j, A in flagged_paths(AF, n, roots):
        d = A.rows
        out[v][offset:offset+d, offset:offset+d] = A*densities[j]*A.H
    return tuple(out)


def flagged_adjoint(AF, n: int, roots, observables):
    out = [s.zeros(d) for d in AF.counts(n)]
    for v, offset, j, A in flagged_paths(AF, n, roots):
        d = A.rows
        out[j] += A.H*observables[v][offset:offset+d, offset:offset+d]*A
    return tuple(out)


def normalized_density_jet(amplitudes, jets):
    """Exact moving-normalizer density jet, with arbitrary raw scale/phase."""
    tau = sum(s.trace(C.H*C) for C in amplitudes)
    dtau = sum(s.trace(dC.H*C+C.H*dC) for C, dC in zip(amplitudes, jets))
    density = tuple(C*C.H/tau for C in amplitudes)
    jet = tuple((dC*C.H+C*dC.H)/tau-C*C.H*dtau/tau**2
                for C, dC in zip(amplitudes, jets))
    return density, jet, tau, dtau


def faithful_preparation(AF, price_owner, n: int, resolutions, log_phi):
    """Evaluate the exact spectral formula from supplied Hermitian resolutions.

    resolutions[j]=(U_j,(e_1,...,e_d)); U is unitary, 0<e_i<1, and the
    minus-flag amplitudes must be nonzero for this faithful log chart.  The
    caller supplies these spectral-domain facts.  No fitted costs enter.
    Right multiplication of returned amplitudes by arbitrary U(d_j) remains.
    """
    densities, amplitudes, costs, derivatives, unnormalized = [], [], [], [], []
    x = s.Symbol("effect_eigenvalue", positive=True)
    for j, (U, eigenvalues) in enumerate(resolutions):
        if U.shape != (AF.counts(n)[j],)*2 or len(eigenvalues) != U.rows:
            raise ValueError("complete_native_spectral_resolution_required")
        f = price_owner.conditional_old_price(AF, j, x, log_phi)
        fs = tuple(f.subs(x, e) for e in eigenvalues)
        fp = tuple(s.diff(f, x).subs(x, e) for e in eigenvalues)
        q = tuple(s.exp(-log_phi*y) for y in fs)
        mu = AF.p**(n+1+j)
        unnormalized.append(mu*U*s.diag(*q)*U.H)
        amplitudes.append(AF.root_weight(n+1+j)*U*
                          s.diag(*(s.exp(-log_phi*y/2) for y in fs))*U.H)
        costs.append(U*s.diag(*fs)*U.H)
        derivatives.append(U*s.diag(*fp)*U.H)
    Z = sum(s.trace(M) for M in unnormalized)
    densities = tuple(M/Z for M in unnormalized)
    amplitudes = tuple(C/s.sqrt(Z) for C in amplitudes)
    return {"normalizer": Z, "density": densities, "amplitude": amplitudes,
            "conditional_cost": tuple(costs), "conditional_derivative": tuple(derivatives),
            "minimum": 6-s.log(Z)/log_phi}


def envelope_source(densities, conditional_derivatives, effect_jets):
    """Full noncommuting effect source after faithful preparation stationarity."""
    return sum(s.trace(rho*fp*dE) for rho, fp, dE in
               zip(densities, conditional_derivatives, effect_jets))


def addressed_envelope(log_phi, blank_normalizer, native_pair_weight,
                       conditional_price, parameters):
    """ONE global log for a single addressed native effect; no price summation."""
    q0 = s.exp(-log_phi*conditional_price(0))
    Z = blank_normalizer+native_pair_weight*sum(
        s.exp(-log_phi*conditional_price(u))-q0 for u in parameters)
    return 6-s.log(Z)/log_phi, Z


def run_checks(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    AF, owner = owners(repo)
    checks = []

    def zero(expr):
        # Polynomial/rational exact arithmetic over Q(a), with real symbolic
        # log and exponential abbreviations retained as coefficient symbols.
        return AF.red(s.fraction(s.cancel(s.together(expr)))[0]) == 0

    def eq(actual, expected, name):
        difference = actual-expected
        require(all(zero(x) for x in difference) if isinstance(difference, s.MatrixBase)
                else zero(difference), name)
        checks.append(name)

    p, n = AF.p, 1
    ell = s.Symbol("log_phi", positive=True)
    U = s.Matrix([[3, 4*s.I], [4*s.I, 3]])/5
    us = (U, s.eye(1))
    es = ((s.Rational(9, 25), s.Rational(16, 25)), (s.Rational(9, 25),))
    rs = ((s.Rational(4, 5), s.Rational(3, 5)), (s.Rational(4, 5),))
    bs = ((s.Rational(3, 5), s.Rational(4, 5)), (s.Rational(3, 5),))
    roots = tuple((W*s.diag(*r)*W.H, W*s.diag(*b)*W.H)
                  for W, r, b in zip(us, rs, bs))
    effects = tuple(W*s.diag(*e)*W.H for W, e in zip(us, es))
    C = (s.Matrix([[1, s.I], [2, 1+s.I]])/3, s.Matrix([[s.Rational(1, 3)]]))
    sigma = tuple(M*M.H for M in C)
    require(not all(zero(x) for x in sigma[0]*effects[0]-effects[0]*sigma[0]),
            "fixture_is_genuinely_coherent_and_noncommuting")
    eq(sum(s.trace(M) for M in sigma), 1, "coherent_seed_normalized")
    for j, (r, b) in enumerate(roots):
        eq(us[j].H*us[j], s.eye(us[j].rows), "spectral_unitary_"+str(j))
        eq(r.H, r, "positive_root_hermitian_"+str(j))
        eq(r*r+b*b, s.eye(r.rows), "positive_roots_complete_"+str(j))
        eq(b*b, effects[j], "positive_root_actual_effect_"+str(j))
    frame = AF.frame(n)
    V, d = frame["V"], frame["old_dimension"]
    eq(V.H*V, s.eye(4*d), "literal_89_by_20_frame_isometry")
    require(V.shape == (89, 20) and V.rows-V.cols == 69, "all_69_complement_modes_retained")

    def vec(blocks):
        return s.Matrix([x for M in blocks for x in M])

    def literal(amplitudes, rr):
        x = V[:, :d]*vec(tuple(r*Cj for (r, _b), Cj in zip(rr, amplitudes)))
        x += V[:, 3*d:]*vec(tuple(b*Cj for (_r, b), Cj in zip(rr, amplitudes)))
        return x, owner.working_blocks(AF, n, x)

    x, factors = literal(C, roots)
    predicted = flagged_factors(AF, n, roots, C)
    rho = flagged_density(AF, n, roots, sigma)
    for j in range(2):
        eq(factors[j], predicted[j], "literal_coherent_factor_"+str(j))
        eq(factors[j]*factors[j].H, rho[j], "literal_coherent_density_"+str(j))
    eq((x.H*x)[0], 1, "whole_89_record_norm")
    eq(sum(s.trace(M) for M in rho), 1, "coherent_channel_trace_preserving")
    completeness = flagged_adjoint(AF, n, roots, tuple(s.eye(k) for k in AF.counts(4)))
    for j in range(2):
        eq(completeness[j], s.eye(C[j].rows), "all_paths_adjoint_unital_"+str(j))
    right = (s.Matrix([[0, s.I], [s.I, 0]]), s.Matrix([[s.I]]))
    rotated = tuple(M*R for M, R in zip(C, right))
    rx, rf = literal(rotated, roots)
    require(not all(zero(z) for z in rx-x), "right_unitary_fiber_changes_full_GNS_vector")
    for j in range(2):
        eq(rf[j]*rf[j].H, rho[j], "whole_right_unitary_fiber_keeps_defining_density_"+str(j))

    # Exact log abbreviations are bound to every actual scalar probability.
    # q_i abbreviates exp(-D_i), never a freely selected thermal law.
    logs, probabilities, D, fprime = {}, {}, {}, {}
    def log_probability(prob):
        value = AF.red(s.expand(prob))
        key = str(value)
        if key not in logs:
            logs[key] = s.Symbol("log_actual_probability_"+str(len(logs)), real=True)
            probabilities[key] = value
        return logs[key]

    def bind_logs(expr):
        substitutions = {}
        for item in expr.atoms(s.log):
            matches = [key for key, value in probabilities.items() if zero(item.args[0]-value)]
            require(len(matches) == 1, "log_is_bound_to_one_actual_probability")
            substitutions[item] = logs[matches[0]]
        return expr.xreplace(substitutions)

    for j in range(2):
        for i, e in enumerate(es[j]):
            fine = owner.conditional_probabilities(AF, j, e)
            pairs = [(v, q) for v in range(2) for q in fine[v]]
            require(all(not zero(q) for _v, q in pairs), "all_actual_flag_probabilities_positive")
            D[j, i] = sum(q*(log_probability(q)+(3+v-j)*ell) for v, q in pairs)
            price = owner.conditional_old_price(AF, j, e, ell)
            eq(bind_logs(ell*price), D[j, i], "actual_owned_conditional_cost_"+str((j, i)))
            variable = s.Symbol("scalar_effect", positive=True)
            derivative = s.diff(owner.conditional_old_price(AF, j, variable, ell), variable)
            fprime[j, i] = bind_logs(derivative.subs(variable, e))

    qsymbols = {(j, i): s.Symbol("exp_minus_actual_D_"+str(j)+"_"+str(i), positive=True)
                for j in range(2) for i in range(len(es[j]))}
    Z = sum(p**(n+1+j)*q for (j, _i), q in qsymbols.items())
    zn = s.Symbol("positive_actual_normalizer", positive=True)
    logZ = s.Symbol("log_actual_normalizer", real=True)
    opt = tuple(us[j]*s.diag(*(p**(n+1+j)*qsymbols[j, i]/zn
                              for i in range(len(es[j]))))*us[j].H for j in range(2))
    amp = tuple(AF.root_weight(n+1+j)*us[j]*
                s.diag(*(s.sqrt(qsymbols[j, i]) for i in range(len(es[j]))))/s.sqrt(zn)
                for j in range(2))
    eq(sum(s.trace(M) for M in opt).subs(zn, Z), 1, "one_global_optimizer_normalizer")
    for j in range(2):
        eq(amp[j]*amp[j].H, opt[j], "actual_square_GNS_optimizer_lift_"+str(j))

    # Construct full fine log gradients by spectral functional calculus, then
    # pull back through the ACTUAL channel adjoint, not a diagonal mass model.
    fine_log = [s.zeros(k) for k in AF.counts(4)]
    for v, offset, j, A in flagged_paths(AF, n, roots):
        eig = us[j].H*A*us[j]
        entries = [log_probability(eig[i, i]**2)+(3+v-j)*ell-D[j, i]-logZ+1
                   for i in range(len(es[j]))]
        fine_log[v][offset:offset+A.rows, offset:offset+A.rows] = us[j]*s.diag(*entries)*us[j].H
    pulled = flagged_adjoint(AF, n, roots, fine_log)
    for j in range(2):
        eq(pulled[j], (1-logZ)*s.eye(C[j].rows), "faithful_EL_all_coherences_and_masses_"+str(j))
    # Subtracting I gives the exact coherent relative-entropy gap identity.
    for j in range(2):
        eq(pulled[j]-s.eye(C[j].rows), -logZ*s.eye(C[j].rows),
           "coherent_gap_adjoint_identity_"+str(j))

    eig_dE = (s.Matrix([[1, 1+s.I], [1-s.I, -s.Rational(1, 2)]]), s.Matrix([[s.Rational(1, 3)]]))
    dE = tuple(W*M*W.H for W, M in zip(us, eig_dE))
    require(not all(zero(t) for t in effects[0]*dE[0]-dE[0]*effects[0]),
            "effect_source_is_noncommuting")
    jets = []
    for W, de, r, b in zip(us, eig_dE, rs, bs):
        dr = s.Matrix(de.rows, de.cols, lambda i, j: -de[i, j]/(r[i]+r[j]))
        db = s.Matrix(de.rows, de.cols, lambda i, j: de[i, j]/(b[i]+b[j]))
        jets.append((W*dr*W.H, W*db*W.H))
    ox, of = literal(amp, roots)
    dx, df = literal(amp, tuple(jets))
    eq((dx.H*ox+ox.H*dx)[0], 0, "noncommuting_effect_literal_normalizer_jet")
    drho = tuple(dM*M.H+M*dM.H for M, dM in zip(of, df))
    source = sum(s.trace(M*G) for M, G in zip(drho, fine_log))/ell
    fp = tuple(us[j]*s.diag(*(fprime[j, i] for i in range(len(es[j]))))*us[j].H
               for j in range(2))
    expected = envelope_source(opt, fp, dE)
    eq(source, expected, "literal_89_noncommuting_source_equals_envelope")
    require(not all(zero(t) for t in drho[0]-s.diag(*[drho[0][i, i] for i in range(8)])),
            "effect_source_keeps_coherent_fine_density_jets")
    # Raw radial plus phase motion must cancel through moving tau.
    _r, rawjet, tau, dtau = normalized_density_jet(C, tuple((2+s.I)*M for M in C))
    eq(tau, 1, "raw_seed_tau")
    eq(dtau, 4, "moving_raw_seed_tau_not_frozen")
    for j in range(2):
        eq(rawjet[j], s.zeros(C[j].rows), "radial_and_phase_source_centered_"+str(j))

    # Hostile rank-one branch: amplitude-critical although NOT minimizing.
    P = s.diag(1, 0)
    faceC = (U*P, s.zeros(1))
    faceLog = [s.zeros(k) for k in AF.counts(4)]
    for v, offset, j, A in flagged_paths(AF, n, roots):
        if j == 0:
            eig = U.H*A*U
            entries = [log_probability(eig[0, 0]**2)+(n+4+v)*ell+1,
                       (n+4+v)*ell+1]
            # log_+ on the absent eigenmode is zero; log(mu_f)=-(n+4+v)ell.
            entries[1] = (n+4+v)*ell+1
            faceLog[v][offset:offset+2, offset:offset+2] = U*s.diag(*entries)*U.H
        else:
            faceLog[v][offset, offset] = (n+4+v)*ell+1
    faceG = flagged_adjoint(AF, n, roots, faceLog)
    faceD = D[0, 0]+2*ell  # log(1/mu_old)+conditional D.
    for j in range(2):
        eq((faceG[j]-(faceD+1)*s.eye(C[j].rows))*faceC[j], s.zeros(C[j].rows),
           "rank_one_full_amplitude_EL_zero_"+str(j))
    epsilon = s.Symbol("epsilon", positive=True)
    dcost = D[0, 1]-D[0, 0]  # same native old PF block weight.
    delta = ((1-epsilon)*s.log(1-epsilon)+epsilon*s.log(epsilon)+epsilon*dcost)/ell
    direct = ((1-epsilon)*((s.log(1-epsilon)+2*ell+D[0, 0]))+
              epsilon*(s.log(epsilon)+2*ell+D[0, 1])-faceD)/ell
    eq(delta, direct, "rank_birth_exact_binary_descent_not_first_order_minimum")

    # A quadratic scalar price tests the GLOBAL-log mixed Hessian, not merely
    # a local Gibbs diagonal gradient.  Its coefficients stand for psi jets.
    l, z0, w = s.symbols("ell z0 w", positive=True)
    b0, b1, b2 = s.symbols("psi0 psi1 psi2", real=True)
    u, v = s.symbols("u v", real=True)
    psi = lambda x: b0+b1*x+b2*x*x/2
    action, norm = addressed_envelope(l, z0, w, psi, (u, v))
    a0 = w*s.exp(-l*b0)/z0
    eq(s.diff(action, u).subs({u: 0, v: 0}), a0*b1, "global_log_address_gradient")
    eq(s.diff(action, u, v).subs({u: 0, v: 0}), l*a0*a0*b1*b1,
       "global_log_nonzero_mixed_setting_Hessian")
    eq(s.diff(action, u, 2).subs({u: 0, v: 0}), a0*b2-l*(a0-a0*a0)*b1*b1,
       "global_log_diagonal_covariance_Hessian")
    return {"exact_checks": len(checks), "literal_working_dimension": 89,
            "old_block_sizes": [2, 1], "fine_block_sizes": [8, 5],
            "identity_complement_dimension": 69, "source_pins": PINS,
            "coherent_channel_and_noncommuting_source": True,
            "faithful_density_minimum_unique": True,
            "proper_support_amplitude_critical_branches_retained": True,
            "all_amplitude_critical_points_classified": False,
            "objective": "terminal second complete price: 6+D(Phi_E sigma||mu_f)/log(phi)",
            "native_field_preparation_admission_derived": False,
            "arbitrary_mixed_B_H_state_optimization_claimed": False}
