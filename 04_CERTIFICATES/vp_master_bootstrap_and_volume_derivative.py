#!/usr/bin/env python3
"""Finite rank/pressure identities with feedback derived from P,Q,U.

One golden orthogonal matrix and nested projections on a fixed 6D test
carrier realize both stages, including golden active compression and
nonempty active/archive sectors. A separate rank-only control loses
golden compression and reverses the loop-pressure increment.
The heat profiles remain supplied finite test data, not a law Delta(P),
a native preparation/refinement, a stationary solution or GR. This test
carrier does not add a physical D0 role. Exact symbolic feedback checks
are separate from numerical exponential/logarithmic identity checks.
BOOK_03's action and BOOK_08's pressure have distinct beta normalizations.
The endpoint resolvent response is also distinct from a finite rank-step
logdet secant. Resolvent interpolation proves a matrix identity, not a
native projector path between two different ranks.
"""
import numpy as np
import sympy as sp

TOL = 1e-9


def exact_feedback_checks():
    a, p = sp.symbols("a p", real=True)
    eye = sp.eye(6)
    gate = sp.BlockMatrix([[a * sp.eye(3), -p * sp.eye(3)],
                           [p * sp.eye(3), a * sp.eye(3)]]).as_explicit()
    assert gate.T * gate == (a*a + p*p) * eye
    for diagonal in ([1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0]):
        proj = sp.diag(*diagonal)
        assert proj * gate.T * (eye - proj) * gate * proj == p*p * proj
        assert proj * gate * proj == a * proj
    other_endpoint = sp.diag(1, 1, 0, 1, 0, 0)
    assert other_endpoint * gate.T * (eye - other_endpoint) * gate * other_endpoint == sp.diag(0, p*p, 0, 0, 0, 0)
    golden_p = (sp.sqrt(5) - 1) / 2
    assert sp.simplify(golden_p + golden_p**2 - 1) == 0
    z = sp.symbols("z", real=True)
    for diagonal, power in [([p*p, p*p, 0, 0, 0, 0], 2),
                            ([p*p, p*p, p*p, 0, 0, 0], 3),
                            ([0, p*p, 0, 0, 0, 0], 1)]:
        assert sp.expand((eye - z * sp.diag(*diagonal)).det()
                         - (1 - z * p*p)**power) == 0
    # Universal polynomial identities: the legacy fibres are empty for every U.
    arbitrary = sp.Matrix(3, 3, sp.symbols("u0:9", real=True))
    old_proj = sp.diag(1, 1, 0)
    possible = old_proj * arbitrary.T * (sp.eye(3) - old_proj) * arbitrary * old_proj
    assert sp.expand(possible[:2, :2].det()) == 0
    assert sp.diag(sp.Rational(1, 10), sp.Rational(1, 5)).det() == sp.Rational(1, 50)
    assert arbitrary.T * (sp.eye(3) - sp.eye(3)) * arbitrary == sp.zeros(3)
    assert sp.diag(sp.Rational(3, 25), sp.Rational(11, 50), sp.Rational(1, 20)) != sp.zeros(3)
    print("PASS_EXACT_PQU_RANK_STAGES_AND_EMPTY_LEGACY_FIBERS")
    # On 0<x<1, these derivatives prove x < -log(1-x) < x/(1-x),
    # with lower gap at least x^2/2. All three differences vanish at x=0.
    x = sp.symbols("x", real=True)
    lower_gap = -sp.log(1-x) - x - x*x/2
    upper_gap = x/(1-x) + sp.log(1-x)
    assert sp.simplify(sp.diff(lower_gap, x) - x*x/(1-x)) == 0
    assert sp.simplify(sp.diff(upper_gap, x) - x/(1-x)**2) == 0
    assert lower_gap.subs(x, 0) == upper_gap.subs(x, 0) == 0
    t = sp.symbols("t", real=True)
    interpolated_projection = sp.diag(1, 1, t, 0, 0, 0)
    assert interpolated_projection**2 - interpolated_projection == sp.diag(0, 0, t*t-t, 0, 0, 0)
    print("PASS_EXACT_SECANT_GAP_IDENTITIES_AND_PROJECTOR_INTERPOLATION_DEFECT")


def check_feedback(proj, gate, feedback):
    eye = np.eye(proj.shape[0])
    assert proj.shape == gate.shape == feedback.shape == eye.shape
    assert all(np.all(np.isfinite(x)) for x in (proj, gate, feedback))
    assert np.allclose(proj.T, proj, atol=TOL, rtol=0)
    assert np.allclose(proj @ proj, proj, atol=TOL, rtol=0)
    assert np.allclose(gate.T @ gate, eye, atol=TOL, rtol=0)
    assert 0 < np.linalg.matrix_rank(proj) < len(proj)
    complement = eye - proj
    leakage = complement @ gate @ proj
    assert np.allclose(feedback, leakage.T @ leakage, atol=TOL, rtol=0)
    assert np.allclose(feedback, proj @ gate.T @ complement @ gate @ proj, atol=TOL, rtol=0)
    assert np.allclose(feedback.T, feedback, atol=TOL, rtol=0)
    eigenvalues = np.linalg.eigvalsh(feedback)
    assert min(eigenvalues) >= -TOL and max(eigenvalues) <= 1 + TOL
    assert np.linalg.matrix_rank(feedback, tol=TOL) <= min(
        np.linalg.matrix_rank(proj), np.linalg.matrix_rank(complement))


def logdet_I_minus(z, feedback):
    assert np.allclose(feedback.T, feedback, atol=TOL, rtol=0)
    operator = np.eye(len(feedback)) - z * feedback
    assert np.min(np.linalg.eigvalsh(operator)) > 0
    sign, logabs = np.linalg.slogdet(operator)
    assert sign > 0
    return logabs


def check_golden_compression(proj, gate, p):
    retained = proj @ gate @ proj
    assert np.allclose(retained.T @ retained, p * proj, atol=TOL, rtol=0)


def log_heat(beta, laplacian):
    assert beta > 0
    assert np.allclose(laplacian.T, laplacian, atol=TOL, rtol=0)
    eigenvalues = np.linalg.eigvalsh(laplacian)
    assert min(eigenvalues) >= -TOL
    # Ordinary trace on the entire carrier, including every zero mode.
    return np.log(np.exp(-beta * eigenvalues).sum())


def require_close(actual, expected):
    assert abs(actual - expected) < TOL


def rejected(name, check):
    try:
        check()
    except AssertionError:
        print("REJECTED_" + name)
        return
    raise AssertionError("Negative control was accepted: " + name)


def main():
    exact_feedback_checks()
    p = (np.sqrt(5.) - 1.) / 2.
    a = np.sqrt(p)
    gate = np.block([[a * np.eye(3), -p * np.eye(3)],
                     [p * np.eye(3), a * np.eye(3)]])
    projections = [np.diag([1., 1., 0., 0., 0., 0.]),
                   np.diag([1., 1., 1., 0., 0., 0.])]
    feedbacks = []
    for proj in projections:
        leakage = (np.eye(6) - proj) @ gate @ proj
        feedback = leakage.T @ leakage
        check_feedback(proj, gate, feedback)
        check_golden_compression(proj, gate, p)
        feedbacks.append(feedback)
    volumes = [int(round(np.trace(proj))) for proj in projections]
    assert volumes == [np.linalg.matrix_rank(proj) for proj in projections] == [2, 3]
    assert np.array_equal(projections[0] @ projections[1], projections[0])
    assert volumes[1] - volumes[0] == 1
    print("PASS_DISCRETE_VOLUME_RANK_PROJECTOR")
    assert np.allclose(feedbacks[1] - feedbacks[0], np.diag([0, 0, p*p, 0, 0, 0]))
    print("PASS_DISCRETE_VOLUME_DERIVATIVE_FORWARD_DIFFERENCE")

    # Supplied profiles on the same full carrier; no law Delta(V) is inferred.
    profiles = [np.diag([1., 2., 0., 0., 0., 0.]),
                np.diag([1., 2., 3., 0., 0., 0.])]
    loops = [-logdet_I_minus(0.25, feedback) for feedback in feedbacks]
    dloop = loops[1] - loops[0]
    assert dloop > TOL
    # BOOK_08 08.49's endpoint resolvent expression is a first response,
    # not the exact finite difference of the loop price at a rank step.
    df = feedbacks[1] - feedbacks[0]
    left_response = np.trace(np.linalg.solve(np.eye(6) - 0.25*feedbacks[0], 0.25*df))
    right_response = np.trace(np.linalg.solve(np.eye(6) - 0.25*feedbacks[1], 0.25*df))
    x = 0.25*p*p
    require_close(left_response, x)
    require_close(right_response, x/(1-x))
    require_close(dloop, -np.log(1-x))
    assert left_response < dloop < right_response
    assert dloop - left_response > x*x/2
    rejected("LEFT_RESOLVENT_RESPONSE_AS_FINITE_SECANT", lambda: require_close(left_response, dloop))
    rejected("RIGHT_RESOLVENT_RESPONSE_AS_FINITE_SECANT", lambda: require_close(right_response, dloop))
    rejected("INTERPOLATED_RANK_STEP_AS_PROJECTOR_PATH", lambda: check_feedback(
        (projections[0]+projections[1])/2, gate, (feedbacks[0]+feedbacks[1])/2))
    print("PASS_FINITE_RANK_SECANT_DIFFERS_FROM_ENDPOINT_PRESSURE")
    # One fixed calibration DOES repair this feedback-only nested golden
    # reading. Do not promote the uncalibrated gap to a transfer no-go.
    calibration = -np.log(1-x)/x
    rank_one = np.diag([1., 0., 0., 0., 0., 0.])
    rank_one_feedback = rank_one @ gate.T @ (np.eye(6)-rank_one) @ gate @ rank_one
    check_feedback(rank_one, gate, rank_one_feedback)
    check_golden_compression(rank_one, gate, p)
    for initial, channels in [(feedbacks[0], 1), (rank_one_feedback, 2)]:
        increment = feedbacks[1] - initial
        response = np.trace(np.linalg.solve(np.eye(6)-0.25*initial, 0.25*increment))
        secant = loops[1] + logdet_I_minus(0.25, initial)
        require_close(response, channels*x)
        require_close(secant, channels*(-np.log(1-x)))
        require_close(calibration*response, secant)
    print("PASS_FIXED_FEEDBACK_CALIBRATION_ON_NESTED_GOLDEN_STEPS")
    # Same U and initial P, same ranks 2 -> 3; no golden-compression premise here.
    alternate = np.diag([1., 1., 0., 1., 0., 0.])
    leakage = (np.eye(6) - alternate) @ gate @ alternate
    alternate_feedback = leakage.T @ leakage
    check_feedback(alternate, gate, alternate_feedback)
    assert np.linalg.matrix_rank(alternate) == volumes[1]
    assert np.array_equal(projections[0] @ alternate, projections[0])
    alternate_dloop = -logdet_I_minus(0.25, alternate_feedback) - loops[0]
    assert alternate_dloop < -TOL
    require_close(alternate_dloop, -dloop)
    rejected("RANK_ONLY_TRANSITION_LOSES_GOLDEN_COMPRESSION",
             lambda: check_golden_compression(alternate, gate, p))
    print("PASS_RANK_DATA_DO_NOT_FIX_LOOP_PRESSURE_SIGN")
    for beta in (0.5, 1., 2.):
        heats = [log_heat(beta, profile) for profile in profiles]
        log_partitions = [heat + loop for heat, loop in zip(heats, loops)]
        pressure = (log_partitions[1] - log_partitions[0]) / beta
        dheat = heats[1] - heats[0]
        require_close(pressure, dheat / beta + dloop / beta)
        bootstrap = [heat / beta + loop for heat, loop in zip(heats, loops)]
        require_close(bootstrap[1] - bootstrap[0] - pressure, (1 - 1 / beta) * dloop)
        if beta != 1:
            rejected("WRONG_FEEDBACK_BETA_" + str(beta),
                     lambda: require_close(pressure, dheat / beta + dloop))
    print("PASS_MASTER_BOOTSTRAP_PRESSURE_SPLIT")
    print("PASS_MASTER_BOOTSTRAP_VOLUME_VARIATION")
    print("PASS_DISTINCT_BOOK03_ACTION_AND_BOOK08_PRESSURE_NORMALIZATIONS")

    old_proj = np.diag([1., 1., 0.])
    old_feedback = np.diag([0.10, 0.20, 0.0])
    rejected("LEGACY_INITIAL_FEEDBACK_RANK", lambda: require_close(
        max(0, np.linalg.matrix_rank(old_feedback) -
            np.linalg.matrix_rank(np.eye(3) - old_proj)), 0))
    rejected("LEGACY_FULL_PROJECTOR_NONZERO_FEEDBACK", lambda: require_close(
        np.linalg.norm(np.diag([0.12, 0.22, 0.05])), 0))
    bad_proj = projections[0].copy()
    bad_proj[0, 0] = 0.5
    rejected("NONPROJECTOR", lambda: check_feedback(bad_proj, gate, feedbacks[0]))
    rejected("NONORTHOGONAL_GATE", lambda: check_feedback(projections[0], gate / 2, feedbacks[0]))
    rejected("ALTERED_FEEDBACK", lambda: check_feedback(projections[0], gate, feedbacks[0] + np.eye(6)))
    rejected("EVEN_NEGATIVE_RESOLVENT", lambda: logdet_I_minus(1., 2 * np.eye(4)))
    rejected("NONPOSITIVE_BETA", lambda: log_heat(0., profiles[0]))
    rejected("ZERO_MODES_REMOVED", lambda: require_close(
        log_heat(1., profiles[0]), np.log(np.exp(-np.array([1., 2.])).sum())))
    print("SCOPE_FINITE_IDENTITIES_ONLY_NATIVE_PREPARATION_AND_GR_OPEN")


if __name__ == '__main__':
    main()
