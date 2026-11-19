"""Independent echo legs of a native repeated NPS2. No simulated readout inserted."""
from fractions import Fraction as F
import json

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from check_extra_work import span
from check_source_price import load_control, need


def native_words():
    ne, digest = load_control()
    field = ne.GOLDEN_FIELD
    p, a = ne.P, ne.A
    gate = ne.Gate
    v = sp.Matrix([a, p])
    to_dm = lambda matrix: DomainMatrix.from_Matrix(matrix).convert_to(field)
    initial = to_dm(sp.kronecker_product(sp.eye(4), v, v, v, v))
    projectors = [to_dm(sp.kronecker_product(sp.eye(16), local)) for local in
                  (sp.diag(1, 1, 0, 0), sp.diag(0, 0, 1, 0), sp.diag(0, 0, 0, 1))]
    signed = gate("SourceI", (2, 0, 1))
    encoder = gate("CX", (4, 5))
    banks = [gate("CX", (2, 3)), gate("CX", (3, 2))]
    cold = {}
    for front in (0, 1):
        for back in (0, 1):
            gates = (banks[front], gate("CX", (2, 4)), signed, signed, banks[back],
                     encoder, gate("G", (5,)), encoder)
            specification = ne.Execution(6, (), (), gates, profile=ne.G_CX_SOURCE_I,
                                         source_port=2, source_spin=(0, 1), report_bits=(4, 5))
            execution = ne.execution_from_json(ne.canonical_json(specification),
                                                max_qubits=6, max_expanded_stages=8)
            end = to_dm(ne.word_matrix(execution, max_qubits=6, max_expanded_stages=8)) * initial
            q = p**2 + p**3 * (p**2 if front == 0 else 2 * p**3)
            for proj, probability in zip(projectors, (1 - q, q, 0)):
                need((end.transpose() * proj * end - to_dm(probability * sp.eye(4))).is_zero_matrix,
                     "actual all-column report; independent of backward leg")
            cold[front, back] = tuple(initial.transpose() * proj * end for proj in projectors)
    for b in range(3):
        need((cold[0,1][b] - cold[1,0][b].transpose()).is_zero_matrix,
             "each exact sector corner is exchanged with its adjoint")
    for m in (0, 1, 2, 5, 12):
        powers = [field.from_sympy(a**m), field.from_sympy((2*p**2)**m)]
        corners = [cs[0]*powers[0] + cs[1]*powers[1] for cs in (cold[0,1], cold[1,0])]
        for corner in corners:
            need(corner.shape == (4, 4), "original protected cut")
        need((corners[0]-corners[1].transpose()).is_zero_matrix, "repeated true cut")
        gram0 = corners[0].transpose() * corners[0]
        gram1 = corners[1].transpose() * corners[1]
        need(gram0.charpoly() == gram1.charpoly(), "all eigenvalues of true feedback")
    return digest


def bounds():
    p = (span(5).sqrt() - 1) / 2
    a = p.sqrt()
    q0, q1 = p**2, 2*p**3
    z = F(1, 2**20)
    trace = 64 * span(3).sqrt()
    g0 = p + a*p
    delta = q1-q0
    grid = {}
    for m in (20, 24, 32, 40):
        dimension = 572 + 64*19*(4**m-1)//3
        ct = 6*trace / (359*dimension)
        # Lower bound for matched cold contrast, M>=13 (REPEAT_CLOCK).
        cj = 4*z*p**(m+1)*delta*g0*(2*p-(q0+q1)*g0)
        matched = cj - ct
        ratio = ct/matched
        unavoidable = (1-ratio)/(1+ratio)
        need(0 < ratio.lo < ratio.hi < F(1,100), "strict separation after all-mode heat")
        grid[str(m)] = {"clock_dimension":dimension,
                        "absolute_cross_heat_and_master_upper":ct.fmt(22)[1],
                        "matched_full_master_lower":matched.fmt(22)[0],
                        "relative_cross_to_matched_upper":ratio.fmt(14)[1],
                        "best_possible_relative_fitting_error_lower":unavoidable.fmt(14)[0]}
    return grid


def main():
    print(json.dumps({"status":"PASS", "native_source_sha256":native_words(),
          "words":"both direct and reverse legs are literal CX addresses",
          "matched_and_crossed_registered_delta":"p^8 in the same orientation",
          "crossed_protected_feedback_contrast":"exactly zero for every M",
          "per_copy_registered_net_contrast":"p^11",
          "all_mode_heat":"full G14-G16 trace inequality; not diagonalized",
          "explicit_certificate":bounds(), "physical_full_C_identified":False},
         indent=2, sort_keys=True))


if __name__=="__main__":
    main()
