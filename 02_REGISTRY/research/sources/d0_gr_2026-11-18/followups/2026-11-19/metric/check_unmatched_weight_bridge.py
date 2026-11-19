"""Full H.1 clock score plus exact unmatched-weight source checks."""
import json
import math
import numpy as np

from check_clock_coherence import mm
from check_local_gibbs_records import build, scene, scene_heat
from check_source_price import load_control, need


def main():
    ne, digest = load_control()
    p = float(ne.P)
    beta = 2 * p * p
    phi = (1 + math.sqrt(5)) / 2
    ell = math.log(phi)

    # Physical native m=0 schedule from LOCAL_GIBBS_RECORDS, both Hodge grades.
    T, cuts, last, V, determinant = build(ne, 0)
    B, C = scene()
    eigen, U = np.linalg.eigh(T + T.T)
    modes = np.array([scene_heat(B, C, q, beta)[32, 32] for q in eigen])
    local = mm(U * modes[None, :], U.T)
    K = mm(last, local[cuts[-1], cuts[-1]], last.T)
    eigK, Kbasis = np.linalg.eigh(K)
    rootK = mm(Kbasis * np.sqrt(eigK)[None, :], Kbasis.T)
    need(eigK.min() >= math.exp(-2 * beta), 'native positive heat bound')

    # Same entangled old input and masks used by the original full-clock check.
    # theta moves the old/reference Schmidt weights; whether it is a free
    # physical row in another closure task is an admission question.
    old = np.array([1.0, 0, 0, 1.0]) / math.sqrt(2)
    dotold = np.array([-1.0, 0, 0, 1.0]) / math.sqrt(2)
    out = mm(np.kron(V, np.eye(2)), old)
    dotout = mm(np.kron(V, np.eye(2)), dotold)
    masks = [np.diag(x) for x in ((1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))]
    amplitudes, derivatives = [], []
    for mask in masks:
        projector = np.kron(np.eye(2), np.kron(mask, np.eye(2)))
        effect = mm(np.kron(rootK, np.eye(2)), projector)
        amplitudes.append(mm(effect, out))
        derivatives.append(mm(effect, dotout))
    weights = np.array([v @ v for v in amplitudes])
    dotweights = np.array([2 * v @ dv for v, dv in zip(amplitudes, derivatives)])
    s = float(sum(weights))
    dots = float(sum(dotweights))
    Q = weights / s
    dotQ = (dotweights - weights * dots / s) / s
    positive = weights > 1e-22
    need(positive.tolist() == [True, True, False], 'real invalid LC1 is dark')
    FI = float(sum(dotQ[positive] ** 2 / Q[positive]))
    amp_bound = float(4 * sum(dv @ dv for dv in derivatives) / s)
    need(FI <= amp_bound + 1e-12, 'Born Fisher <= full physical amplitude bound')
    need(abs(FI - 0.2229123599343674) < 5e-10, 'native full clock score')

    # Test general identity, including moving gauge and nontrivial economic law.
    # These parameters are diagnostic and not a claimed Book valuation.
    Q2, dQ2 = Q[:2], dotQ[:2]
    score = dQ2 / Q2
    gauge, dgauge = 0.27, 0.03
    defect = np.array([-0.12, 0.1])
    ddefect = np.array([0.07, -0.02])
    unscaled = Q2 * np.exp(-defect)
    economic = unscaled / sum(unscaled)
    logZratio_derivative = (-dgauge + float(dQ2 @ np.exp(-defect)) / sum(unscaled)
                            - float(economic @ ddefect))
    formula = -dgauge + float((economic - Q2) @ score) - float(economic @ ddefect)
    need(abs(logZratio_derivative - formula) < 1e-12, 'full source identity')
    R = float(max(defect) - min(defect))
    chi2 = float(sum((economic - Q2) ** 2 / Q2))
    need(chi2 <= math.sinh(R / 2) ** 2 + 1e-12, 'bounded likelihood chi squared')
    bound = abs(dgauge) + max(abs(ddefect)) + math.sinh(R / 2) * math.sqrt(FI)
    need(abs(formula) <= bound + 1e-12, 'source transfer bound')

    # Check an actual tiny positive branch without omitting it, in a separate
    # two-outcome square-root heat instrument; precision is stable at 1e-8.
    a = 1e-8
    amp = np.array([math.cos(a), math.sin(a) / 2])
    damp = np.array([-math.sin(a), math.cos(a) / 2])
    w = amp * amp
    dw = 2 * amp * damp
    rareQ = w / sum(w)
    rare_dQ = (dw - w * sum(dw) / sum(w)) / sum(w)
    rareFI = float(sum(rare_dQ * rare_dQ / rareQ))
    rareBound = float(4 * (damp @ damp) / sum(w))
    need(0 < rareQ[1] < 3e-17 and rareFI <= rareBound + 1e-12,
         'positive rare outcome remains in Fisher, no probability cutoff')

    # Native LIVE two-end conditional Born laws; the constant defect is only
    # an analytic test and is not a physical price for the native full graph.
    u = p * p
    v = math.sin(29 * math.asin(p)) ** 2
    epsilon = 0.1
    secant = abs(math.log1p(u * math.expm1(-epsilon))
                  - math.log1p(v * math.expm1(-epsilon)))
    secant_bound = (math.sinh(epsilon / 2) * 2
                    * abs(math.asin(math.sqrt(u)) - math.asin(math.sqrt(v))))
    need(secant <= secant_bound, 'native two-end diagnostic')
    result = {
        'status': 'PASS',
        'native_source_sha256': digest,
        'native_clock_dimension': len(T),
        'native_heat_rank_both_grades': 425 * len(T),
        'native_feedback_J': round(determinant, 12),
        'native_kept_probabilities': [round(float(x), 12) for x in Q],
        'native_graph_fisher': round(FI, 12),
        'native_full_amplitude_fisher_upper': round(amp_bound, 10),
        'native_acceptance': round(s, 10),
        'native_normalized_source_score': round(math.sqrt(FI) / ell, 10),
        'identity_abs_error': round(abs(logZratio_derivative - formula), 15),
        'example_source_abs': round(abs(formula), 12),
        'example_source_bound': round(bound, 12),
        'rare_probability': '{:.12e}'.format(rareQ[1]),
        'rare_fisher': round(rareFI, 12),
        'rare_amplitude_fisher_upper': round(rareBound, 12),
        'native_live_two_endpoint_diagnostic': {
            'plus_u': round(u, 12),
            'minus_v': round(v, 12),
            'log_secant': round(secant, 12),
            'upper_bound': round(secant_bound, 12),
            'defect_is_physical_book_price': False,
        },
        'note': 'the actual Cost-Info and admissibility of the input-variation row remain open',
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
