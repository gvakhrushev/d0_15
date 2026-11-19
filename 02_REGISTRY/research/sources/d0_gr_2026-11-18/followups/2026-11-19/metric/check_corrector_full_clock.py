"""Exact SourceI tail word, two clock degrees and retained NC1 source."""
import json
import math
import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

from check_source_price import load_control, need
from check_local_gibbs_records import scene, scene_heat


def main():
    ne, digest = load_control()
    gate = ne.Gate
    spec = dict(profile=ne.G_CX_SOURCE_I, source_port=2, source_spin=(3, 4))
    one = ne.Execution(5, (), (), (gate('G', (1,)),), **spec)
    inv = ne.inverse_word(one, max_qubits=5, max_expanded_stages=100)
    word = inv + (gate('CX', (0,1)), gate('G', (1,)), gate('CX', (0,1)))
    actual = ne.Execution(5, (), (), word, **spec)
    inventory = ne.inventory(actual, max_qubits=5, max_expanded_stages=100)
    U = ne.word_matrix(actual, max_qubits=5, max_expanded_stages=100)
    P, A = ne.P, ne.A
    e = sp.Matrix([[1,0],[0,0],[0,(ne.G_LOCAL**2)[0,0]],[0,(ne.G_LOCAL**2)[1,0]]])
    E = sp.kronecker_product(e, sp.eye(8))
    C = E.T * U * E
    expected_C = sp.diag(sp.eye(8), P**3 * sp.eye(8))
    dm = lambda mat: DomainMatrix.from_Matrix(mat).convert_to(ne.GOLDEN_FIELD)
    need(dm(C) == dm(expected_C), 'actual rank-16 NC1 cut return')
    F = sp.eye(16) - C.T * C
    expected_F = sp.diag(sp.zeros(8), 4 * P**3 * sp.eye(8))
    need(dm(F) == dm(expected_F), 'full return and all orthogonal complements')
    target_U = sp.kronecker_product(sp.diag(sp.eye(2), ne.G_LOCAL.T**2), sp.eye(8))
    need(dm(U) == dm(target_U), 'actual 32-column SourceI holonomy')

    p, a = float(P), float(A)
    beta, z = 2*p*p, 2**-20
    J = -8 * math.log1p(-z * 4*p**3)
    need(J > 0, 'conditional physical cut has nonzero feedback')
    # The all-column cut is a separate graph choice; there F vanishes.
    need(dm(U.T * U) == dm(sp.eye(32)), 'full-column cut has zero feedback')

    # Complete fixed-rank square-stage cyclic clock for all 14 real letters.
    matrices = [np.array(ne.gate_matrix(actual,g,max_qubits=5,max_expanded_stages=100),
                         dtype=float) for g in word]
    L, d = len(word), 32
    clock = np.zeros((L*d,L*d))
    for j, mat in enumerate(matrices):
        need(np.max(np.abs(np.einsum('ki,kj->ij',mat,mat)-np.eye(d)))<1e-12,
             'every clock stage unitary on all spin and port columns')
        clock[((j+1)%L)*d:((j+1)%L+1)*d,j*d:(j+1)*d] = mat
    theta = math.asin(p)
    actual_modes = np.linalg.eigvalsh(clock + clock.T)
    B, scene_diag = scene()
    predicted_modes = []
    ZH = 359*L*d
    for phase, multiplicity in ((0.0,16), (2*theta,8), (-2*theta,8)):
        for k in range(L):
            mode = 2*math.cos((phase+2*math.pi*k)/L)
            predicted_modes += [mode] * multiplicity
            ZH += 2*multiplicity*float(np.trace(scene_heat(B,scene_diag,mode,beta)))
    spectrum_error = float(max(abs(actual_modes-np.sort(predicted_modes))))
    need(spectrum_error < 2e-12, 'entire clock spectrum from true holonomy')
    need(L == 14 and len(actual_modes) == 448, 'all stages and full dimension')
    need(359*L*d < ZH < 425*L*d, 'both-degree heat trace')
    x = beta/11
    local_diff_upper = 4*x**L / (math.factorial(L)*(1-x/(L+1)))
    # Vertex 32 has d=22. Its all-forward C path is an explicit positive term.
    local_diff_lower = (2*math.exp(-beta)*(beta/22)**L / math.factorial(L)
                        * (1-math.cos(2*theta)))
    need(3e-32 < local_diff_lower < local_diff_upper < 2.9e-27,
         'strict heat separation and analytic winding bound')

    # Actual NC1 on an incoming Golden bit controlled by a recorded old T.
    G = np.array([[a,-p],[p,a]])
    X = np.array([[0.,1.],[1.,0.]])
    CX = np.eye(4); CX[2,2]=CX[3,3]=0; CX[2,3]=CX[3,2]=1
    Uread = CX @ np.kron(np.eye(2),G) @ CX
    golden = np.array([a,p])
    probs = []
    for t in (0,1):
        inputN = golden if not t else X @ golden
        state = Uread @ np.kron(inputN,golden)
        vals = [float(np.sum(state[0:2]**2)),float(state[2]**2),float(state[3]**2)]
        need(abs(vals[1]-(p*p+p**3*t)) < 1e-13, 'both real Born sectors')
        need(vals[2] < 1e-25, 'invalid report explicitly retained with zero mass')
        probs.append(vals)
    h = lambda y: -y*math.log(y)-(1-y)*math.log1p(-y)
    ell = math.log(1/p)
    need(abs(h(p*p)/ell-(1+p*p)) < 1e-12, 'exact golden Shannon equality')
    need(abs(h(p)/ell-(1+p*p)) < 1e-12, 'both T conditional entropies')
    gain = probs[1][1]-probs[0][1]
    need(abs(gain-p**3)<1e-13, 'actual recorded code minus CQ source')
    q = 0.37
    def recorded(q):
        prob = (1-q)*probs[0][1]+q*probs[1][1]
        entropy = ((1-q)*h(probs[0][1])+q*h(probs[1][1]))/ell
        return 1+prob-entropy
    diff = (recorded(q+1e-6)-recorded(q-1e-6))/(2e-6)
    need(abs(diff-gain)<2e-9, 'full conditional recorded source derivative')

    print(json.dumps({
        'status':'PASS', 'native_source_sha256':digest,
        'word_inventory':{'G':inventory.g_count,'CX':inventory.cx_count,
                          'SourceI':inventory.source_i_count,'total':inventory.gate_count},
        'true_cut_rank':16,'true_cut_return_eigenvalues':[1,round(p**3,12)],
        'true_cut_feedback_eigenvalues':[0,round(4*p**3,12)],
        'true_cut_feedback_J':round(J,15),
        'unrestricted_32_cut_feedback_J':0,
        'clock_stages':L,'clock_dimension':L*d,'clock_two_grade_modes':425*L*d,
        'clock_spectrum_max_error':spectrum_error,'heat_trace':round(ZH,8),
        'both_growing_clock_degrees':True,
        'local_thermal_difference_lower':'{:.12e}'.format(local_diff_lower),
        'local_thermal_difference_upper':'{:.12e}'.format(local_diff_upper),
        'conditional_record_probabilities':probs,
        'conditional_record_gain_wrt_old_T_probability':round(gain,12),
        'record_gain_finite_difference_error':abs(diff-gain),
        'incoming_NC1_measurement_in_this_14_stage_clock':False,
        'factory_failure_flags_in_this_14_stage_clock':False,
        'full_physical_cost_info_identified':False,
        'GR_closed':False,
    },sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
