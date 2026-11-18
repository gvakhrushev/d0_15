#!/usr/bin/env python3
"""B116: exact two-site RAW stabilizer and frozen source/mark scope."""
from hashlib import sha256
from pathlib import Path
import json
import sympy as s

here = Path(__file__).resolve().parent
op = here.parent
direct_repo = Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13')
direct = direct_repo / '02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct'
owner = direct_repo / '02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
files = {
    'owner': owner,
    'A23': direct / 'round23/CAR_VACUUM_FOURIER_RU.md',
    'A54': direct / 'round54/REGULAR_GLOBAL_SOURCE_RU.md',
    'A55': direct / 'round55/REGULAR_FIELD_TASK_AND_FRONTIERS_RU.md',
    'A58': direct / 'round58/FIELD_SOURCE_PULLBACK_RU.md',
    'B91': op / 'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md',
    'B114': op / 'round114/B114_PHYSICAL_CHART_PULLBACK_RU.md',
    'B115': op / 'round115/B115_A58_INDEPENDENT_REVIEW_RU.md',
}
content = {k: p.read_text() for k, p in files.items()}
assert 'identity on RIGHT\non ALL columns' in content['owner']
assert 'A_nu(Y)=D_nu B(Y) is its full prefix map on every input column' in content['owner']
assert '## 7fu.' in content['owner']
assert 'восьмой current bank' in content['A54']
assert 'SOURCE_after_Qf' in content['A55'] and 'SC6' in content['A55']
assert '6*2^5374' in content['A58']
assert 'canonical source-private' in content['B91']

# a=sqrt(p), p^2+p=1, G e0=v=(a,p).
# Reduce in Q[a]/(a^4+a^2-1) to avoid floating-point evidence.
a = s.Symbol('a', real=True)
mod = a**4 + a**2 - 1
def red(z):
    return s.rem(s.Poly(s.expand(z), a), s.Poly(mod, a)).as_expr()
def matred(m):
    return m.applyfunc(red)
p = a*a
G = s.Matrix([[a, -p], [p, a]])
I = s.eye(2)
v = s.Matrix([a, p])
K = s.kronecker_product(G, G)
CX = s.Matrix([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]])
Q = matred(K * CX * K.T)
born = s.kronecker_product(v, v)
w = matred(K * s.Matrix([0, 0, 1, -1]))  # unnormalised, ||w||²=2
assert matred(G.T*G) == I and matred(G*s.Matrix([1,0])-v) == s.zeros(2,1)
assert matred(Q.T*Q) == s.eye(4)
assert matred(Q*born-born) == s.zeros(4,1)
assert matred(Q*w+w) == s.zeros(4,1)
assert red((w.T*w)[0]) == 2
assert matred((Q-s.eye(4))*w+2*w) == s.zeros(4,1)
assert s.factor(CX.det()) == -1  # 17 untouched DATA bits make full determinant +1
# J_birth is an isometry of an arbitrary two-dimensional coherent spectator,
# illustrating the exact tensor identity for arbitrary SAM/old/reference.
J_birth = s.kronecker_product(born, I)
Q_full = s.kronecker_product(Q, I)
assert matred((Q_full-s.eye(8))*J_birth) == s.zeros(8,2)
assert matred(J_birth.T*J_birth) == s.eye(2)
# Exact cold-cut and finite first-jet control for arbitrary, generally
# noncommuting 8x8 matrices.  These finite surrogates verify the algebra;
# the product argument in the note applies on the full source Hilbert space.
F0 = s.Matrix(8, 8, lambda i,j: ((i+1)*(j+2)+i*j) % 7 - 3)
F1 = s.Matrix(8, 8, lambda i,j: ((i+2)*(j+1)+i+2*j) % 11 - 5)
O = s.diag(*range(1, 9))
for F in (F0, F1):
    T = matred(F*J_birth)
    Tq = matred(F*Q_full*J_birth)
    assert Tq == T
    assert matred(Tq.T*O*Tq - T.T*O*T) == s.zeros(2)
    W = F.T*O*F
    assert matred(J_birth.T*(Q_full.T*W*Q_full-W)*J_birth) == s.zeros(2)
assert matred((F1-F0)*Q_full*J_birth - (F1-F0)*J_birth) == s.zeros(8,2)

result = {
    'claim': 'one CAR DATA RAW-state match does not imply full DATA matrix or marked-map match',
    'proof_field': 'Q[a]/(a^4+a^2-1), physical root a=sqrt((sqrt(5)-1)/2)',
    'raw_two_site_state_fixed_exactly': True,
    'unitary_stabilizer_Q_exact': True,
    'explicit_nonzero_minus_one_eigenvector_norm_squared': 2,
    'full_input_operator_distance': '2, preserved under common unitary prefix and processor',
    'all_initialized_bank_and_common_processor_marks_same': True,
    'initialized_prepared_first_jet_and_joint_effects_same': True,
    'inverse_wrapper_cold_cut_same': True,
    'paid_history_clock_heat_cost_equivalence': False,
    'initialized_scope': 'canonical DATA/WORK birth; arbitrary coherent SAM and protected old/reference',
    'arbitrary_DATA_physically_admitted_in_H1': 'not established',
    'other_17_CAR_DATA_wires_and_private_untouched': True,
    'genuine_A54_eighth_bank_present': True,
    'original_owner_differs_from_A23': 'not established',
    'alternative_word_admitted_or_priced': False,
    'B114_B115_A58_physical_admission': False,
    'physical_C_closed': False,
    'GR_closed': False,
    'source_sha256': {str(path):sha256(path.read_bytes()).hexdigest() for path in files.values()},
}
(here / 'B116_ORIGINAL_FULL_INPUT_CHECK.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'source_sha256'}, ensure_ascii=False, indent=2))
