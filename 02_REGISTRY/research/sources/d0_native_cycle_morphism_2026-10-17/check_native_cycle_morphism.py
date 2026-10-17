#!/usr/bin/env python3
"""D0 #334: exact scene-history cycles, signed native trace and all-source control.

Only certified mathematical identities of the *declared* 33-vertex record
model; no physical programme admission, no external Fock, no Einstein claims.
Run with python and python -O; all controls are explicit, never `assert`.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sympy as s

HERE = Path(__file__).resolve().parent
N = 33
SIZES = (9, 11, 13)
M = 128
Z_PHYSICAL = s.Rational(1, 2**20)
Z_TEST = s.Rational(1, 8)
checks: list[str] = []

def require(ok, label):
    if ok is not True and ok != s.true:
        raise ArithmeticError(label)
    checks.append(label)

def zero(x):
    if isinstance(x, s.MatrixBase):
        return all(s.cancel(y) == 0 for y in x)
    return s.cancel(x) == 0

def zone(i):
    return 0 if i < 9 else 1 if i < 20 else 2

# The literal 359-undirected-edge K(9,11,13) and all 718 directed arrows.
A0 = s.zeros(N)
for i in range(N):
    for j in range(N):
        if zone(i) != zone(j):
            A0[i, j] = 1
require(A0 == A0.T, "native_scene_adjacency_reversible")
require(int(sum(A0)) == 718, "scene_has_718_directed_edges")
degrees = [int(sum(A0[i, j] for j in range(N))) for i in range(N)]
require(set(degrees[:9]) == {24} and set(degrees[9:20]) == {22} and set(degrees[20:]) == {20},
        "actual_three_zone_degrees_24_22_20")

E = s.zeros(N)
for i, j, v in [(0, 9, 1), (9, 0, 1), (0, 20, -1), (20, 0, -1)]:
    E[i, j] = v
require(E == E.T and sum(E) == 0, "native_edge_perturbation_is_balanced_global_mass")

def eulerian_record(Ncounts):
    """Construct one *entire* recorded word from integer directed counts."""
    outgoing = [Counter({j: int(Ncounts[i,j]) for j in range(N) if Ncounts[i,j] != 0})
                for i in range(N)]
    L = sum(sum(cs.values()) for cs in outgoing)
    require(all(v >= 0 for cs in outgoing for v in cs.values()), "record_counts_nonnegative")
    require(all(sum(outgoing[i].values()) == sum(int(Ncounts[j,i]) for j in range(N)) for i in range(N)),
            "record_counts_eulerian_balance")
    stack, path = [0], []
    while stack:
        u = stack[-1]
        if outgoing[u]:
            v = min(outgoing[u])
            outgoing[u][v] -= 1
            if not outgoing[u][v]:
                del outgoing[u][v]
            stack.append(v)
        else:
            path.append(stack.pop())
    word = path[::-1]
    require(len(word) == L+1 and word[0] == word[-1], "complete_cyclic_word_length_and_closure")
    require(all(not c for c in outgoing), "no_unused_native_record_arrows")
    counts = s.zeros(N)
    for a,b in zip(word[:-1], word[1:]):
        counts[a,b] += 1
    require(counts == Ncounts, "each_actual_record_arrow_count_reproduced")
    return word

base_word = eulerian_record(2*A0)
plus_word = eulerian_record(2*A0+E)
minus_word = eulerian_record(2*A0-E)
require(len(base_word) == 1437 and len(plus_word) == 1437 and len(minus_word) == 1437,
        "same_period_L1436_three_full_words")
require(len(set(base_word[:-1])) == N, "all_33_labels_retained")
require(base_word != plus_word and plus_word != minus_word, "native_history_variation_is_genuine")

# The exact reduced interface in A4D_NATIVE_CYCLIC_HISTORY_PRICE_PREPARATION:
# J(t,i)=1_{word_t=i}, D=J.T J, C=D^-1 J.T, P=JC,
# T=C U J =D^-1 N1, F=I - T_dag T, T_dag=D^-1 T.T D.
D = s.diag(*degrees)
Di = D.inv()
T = Di * A0
Tdag = Di*T.T*D
require(Tdag == T, "scene_chain_is_D_reversible")
F = s.eye(N)-Tdag*T
require(F == s.eye(N)-T*T, "native_archive_feedback_F_equals_I_minus_T2")
require(D*F == F.T*D, "native_feedback_D_selfadjoint")
# 0<= F <= I by contraction of row stochastic T in stationary weighted L2.
# Independent finite eigenvalue check on the complete 33x33 rational matrix.
TG = s.zeros(3)
for i, size in enumerate(SIZES):
    for j, v in enumerate(SIZES):
        if i != j: TG[i,j] = s.Rational(v, degrees[sum(SIZES[:i])])
require(all(sum(TG[i,j] for j in range(3)) == 1 for i in range(3)),
        "complete_reversible_scene_quotient_row_stochastic")
l=s.Symbol('lambda')
require(T.rank() == 3 and
        s.factor(TG.charpoly(l).as_expr()) ==
        (l-1)*(160*l*l+160*l+39)/160,
        "scene_rank_three_and_exact_3x3_quotient_spectrum")
# The other 30 modes are killed by T and have F=1; the three
# quotient eigenvalues are 1, -1/2 +- sqrt(10)/40, hence rank(F)=32.
NATIVE_F_RANK=32
# Independent determinant on the FULL 33x33 carrier confirms the exact
# quotient factorization including thirty unit-feedback eigen-directions.
for zz in (Z_TEST,Z_PHYSICAL):
    direct_det=(s.eye(N)-zz*F).det(method='domain-ge')
    factor_det=(1-zz)**30*(1-s.Rational(119,80)*zz+s.Rational(14001,25600)*zz**2)
    require(zero(direct_det-factor_det),
            f"full33_native_determinant_equal_exact_3zone_quotient_at_{str(zz).replace('/', '_')}")
require(F*s.ones(N,1) == s.zeros(N,1), "constant_mode_is_zero_feedback")
# Exact norm proof: T is Markov, D-stationary and reversible.  Its
# row-stochastic Jensen inequality yields T^T D T <= D, hence
# 0 <= F=I-T^2 <= I in the D inner product without spectral numerics.
require(T.T*D == D*T, "exact_markov_detailed_balance")
require(D*F == F.T*D, "D_metric_feedback_selfadjoint")
print("stage: native scene verified",flush=True)

c = s.Rational(23,480)
require(all(F[i,j] == -c for i,j in ((0,1),(1,2),(2,0))),
        "native_same_zone_off_diagonals_are_exactly_minus_23_over_480")
tri = F[0,1]*F[1,2]*F[2,0]
require(tri == -c**3 and tri < 0, "exact_negative_three_cycle_of_positive_native_feedback")
# Every diagonal phase similarity leaves the directed triangle product fixed.
q0,q1,q2=s.symbols('q0 q1 q2',nonzero=True)
phase=(q0**-1*F[0,1]*q1)*(q1**-1*F[1,2]*q2)*(q2**-1*F[2,0]*q0)
require(zero(phase-tri), "negative_cycle_gauge_invariant_under_native_label_rephasing")

# A genuine smooth family of balanced scene conductances, realized at all
# rational t=r/m with m even by finite *complete* Eulerian words.
t=s.symbols('t')
A=A0+t*E
degree_t=s.Matrix([sum(A[i,j] for j in range(N)) for i in range(N)])
require(all(zero(degree_t[i]-degrees[i]) for i in list(range(1,9))+list(range(10,20))+list(range(21,33))),
        "only_three_vertex_degrees_move")
# The three needed smooth entries are evaluated directly from the
# actual record-frequency formula F_ij=delta_ij-(1/sqrt(d_i*d_j))
# sum_k A_ik A_kj / d_k. Here d_0=d_1=d_2=24 fixed.
s01 = (s.Rational(10,22)+s.Rational(12,20)
       +(1+t)/(22+t)+(1-t)/(20-t))/24
s12 = (s.Rational(10,22)+s.Rational(12,20)
       +1/(22+t)+1/(20-t))/24
tri_t=s.cancel(-s01**2*s12)
tri_dot=s.factor(s.diff(tri_t,t).subs(t,0))
require(tri_dot==s.Rational(199433,267632640000) and tri_dot>0,
        "negative_three_cycle_nonzero_first_jet_on_actual_record_frequency_family")
require(tri_t.subs(t,s.Rational(1,2))<0 and tri_t.subs(t,-s.Rational(1,2))<0,
        "both_realized_plus_minus_record_frequencies_have_negative_triangle")
print("stage: negative triangle & frequency first jet verified",flush=True)

# Direct matrix-source formula, with moving D and noncommuting T.
dD=s.diag(*[sum(E[i,j] for j in range(N)) for i in range(N)])
dT=Di*(E-dD*T)
dF=-(dT*T+T*dT)
require(zero(dF[0,1]+s.diff(s01,t).subs(t,0))
        and zero(dF[1,2]+s.diff(s12,t).subs(t,0)),
        "full_native_compressed_F_derivative_including_moving_fibers")
require(zero(tri_dot-(dF[0,1]*F[1,2]*F[2,0]
                          +F[0,1]*dF[1,2]*F[2,0]
                          +F[0,1]*F[1,2]*dF[2,0])),
        "independent_matrix_product_source_matches_triangle_first_jet")
require(not zero(dD),"record_visit_density_moves_nonnegligibly")
wrong_dT=Di*E
wrong_dF=-(wrong_dT*T+T*wrong_dT)
require(not zero(wrong_dF-dF), "frozen_visit_density_mutation_rejected")

print("stage: full matrix response jet verified",flush=True)
source={}
for zz,label in ((Z_TEST,'test_1_over_8'),(Z_PHYSICAL,'native_z_2powminus20')):
    B=s.eye(N)-zz*F
    rhs=s.factor(zz*s.trace(B.inv()*dF))
    # Independently *different* determinant construction from the recorded
    # integer N1 (A) and moving D, with no exterior/fermionic carrier.
    # det(I-zF) = det[(1-z)D+z A.T D^-1 A] / det D.
    C=(1-zz)*D+zz*A0.T*Di*A0
    dDi=-Di*dD*Di
    dC=(1-zz)*dD+zz*(E.T*Di*A0+A0.T*dDi*A0+A0.T*Di*E)
    separate=s.factor(s.trace(C.inv()*dC)-s.trace(Di*dD))
    require(zero(rhs+separate),f"record_fiber_det_source_equals_trace_log_source_{label}")
    frozen_density=s.factor(s.trace(C.inv()*((1-zz)*dD+zz*(E.T*Di*A0+A0.T*Di*E)))-s.trace(Di*dD))
    require(not zero(frozen_density+rhs), f"full_source_rejects_frozen_fiber_inverse_{label}")
    source[label]={"z":str(zz),"d_logdet_weighted":str(-rhs),"d_minus_logdet":str(rhs),
                   "d_minus_M_logdet":str(M*rhs),"d_minus_M_logdet_float":float(M*rhs),
                   "wrong_freeze_delta":str(s.factor(frozen_density+rhs))}

print("stage: full 33×33 determinant source verified",flush=True)
# Universal native finite-source ownership under simultaneous genuine
# projector and orthogonal-link tangents, with no frozen endpoint projector.
Qrat=s.Rational
I4=s.eye(4)
C4=s.diag(Qrat(3,5),Qrat(5,13))
S4=s.diag(Qrat(4,5),Qrat(12,13))
Ubase=C4.row_join(-S4).col_join(S4.row_join(C4))
Rmix=I4.copy()
Rmix[0,0]=Rmix[3,3]=Qrat(3,5)
Rmix[0,3]=-Qrat(4,5)
Rmix[3,0]=Qrat(4,5)
U=Rmix*Ubase
P=s.diag(1,1,0,0)
G=s.zeros(4); H=s.zeros(4)
for i,j,v in ((0,2,Qrat(1,10)),(0,3,Qrat(1,5)),(1,2,Qrat(1,8))):
    G[i,j]=v;G[j,i]=-v
for i,j,v in ((0,2,Qrat(1,7)),(1,3,Qrat(1,9))):
    H[i,j]=v;H[j,i]=-v
dP=G*P-P*G;dU=H*U
Q4=I4-P
require(U.T*U==I4 and P*P==P and P==P.T,
        "explicit_native_projector_and_orthogonal_link")
require(dP.T==dP and P*dP*P==s.zeros(4) and Q4*dP*Q4==s.zeros(4),
        "moving_projector_tangent_integrable_as_rotation")
require(dU.T*U+U.T*dU==s.zeros(4),
        "moving_link_unitarity_tangent_integrable_as_rotation")
F4=P*U.T*Q4*U*P
partP=(dP*U.T*Q4*U*P+P*U.T*Q4*U*dP-P*U.T*dP*U*P)
partU=P*dU.T*Q4*U*P+P*U.T*Q4*dU*P
dF4=partP+partU
u=s.symbols('u')
P_u=P+u*dP;U_u=U+u*dU
rawF_u=P_u*U_u.T*(I4-P_u)*U_u*P_u
require(rawF_u.diff(u).subs(u,0)==dF4,
        "all_five_real_F_source_terms_match_direct_product_differentiation")
B4=I4-Z_TEST*F4
sourceP=s.factor(Z_TEST*s.trace(B4.inv()*partP))
sourceU=s.factor(Z_TEST*s.trace(B4.inv()*partU))
sourcePU=s.factor(Z_TEST*s.trace(B4.inv()*dF4))
require(sourceP==-s.Rational(3303,904070) and
        sourceU==-s.Rational(10820,632849) and
        sourcePU==-s.Rational(131321,6328490),
        "both_independent_moving_P_and_U_sources_are_exact_and_nonzero")
require(F4*dF4 != dF4*F4,
        "actual_PU_joint_source_does_not_assume_commuting_F_and_dF")
require(sourcePU!=sourceU and sourcePU!=sourceP,
        "freezing_either_endpoint_or_link_changes_physical_source")
poly4=(I4-Z_TEST*rawF_u).det()
deriv4=s.cancel(-s.diff(poly4,u).subs(u,0)/poly4.subs(u,0))
require(zero(sourcePU-deriv4),
        "moving_PU_Jacobi_first_variation_matches_direct_finite_determinant")

print("stage: moving P,U and full source verified",flush=True)
# Exact determinant = signed disjoint *simple-cycle-cover* polynomial,
# and trace-log = weighted all closed rooted walks; no second Fock space.
sub=F[:3,:3]
x=s.symbols('x')
poly=(s.eye(3)-x*sub).det().expand()
leibniz=s.Integer(1)
for r in range(1,4):
    for subset in combinations(range(3),r):
        minor=s.Integer(0)
        for permutation in permutations(range(r)):
            inv=sum(permutation[i]>permutation[j] for i in range(r) for j in range(i+1,r))
            contribution=(-1)**inv
            for i,j in enumerate(permutation):
                contribution*=sub[subset[i],subset[j]]
            minor+=contribution
        leibniz+=(-x)**r*minor
require(zero(leibniz-poly),"finite_signed_cycle_cover_permutation_expansion_no_fock")
positive_sub=sub.applyfunc(lambda v: abs(v))
require(zero(s.trace(positive_sub)-s.trace(sub))
        and zero(s.trace(positive_sub**2)-s.trace(sub**2)),
        "naive_sign_erasure_passes_moments_one_and_two")
require(zero(s.trace(positive_sub**3)-s.trace(sub**3)-12*c**3),
        "naive_sign_erasure_first_fails_at_three_cycle_order")
require(s.trace(sub**2)/2 != s.trace(sub**2),
        "forgetting_cycle_stabilizers_fails_at_second_order")

rooted_counts={}
for k in range(1,7):
    orbits={}
    for word in product(range(3),repeat=k):
        canon=min(word[i:]+word[:i] for i in range(k))
        weight=s.prod(sub[word[i],word[(i+1)%k]] for i in range(k))
        if canon in orbits and orbits[canon][0]!=weight:
            raise ArithmeticError("rotation_changes_closed_walk_weight")
        else: orbits[canon]=(weight, sum(canon[i:]+canon[:i]==canon for i in range(k)))
    require(all(v[0]==s.prod(sub[canon[i],canon[(i+1)%k]] for i in range(k)) for canon,v in orbits.items()),
            f"all_cyclic_rotation_orbits_have_same_weight_len_{k}")
    orbit_sum=sum(weight/s.Integer(stab) for weight,stab in orbits.values())
    expected=s.trace(sub**k)/k
    require(zero(orbit_sum-expected),f"rooted_walk_cyclic_stabilizer_1_over_k_len_{k}")
    print(f"stage: cyclic groupoid length {k}",flush=True)
    rooted_counts[str(k)]={"rooted":3**k,"cyclic_classes":len(orbits),
                            "trace_Fk_over_k":str(expected),
                            "repeats_have_stabilizers":sum(stab>1 for _,stab in orbits.values())}

series=sum(x**k*s.trace(sub**k)/k for k in range(1,7))
expanded=s.series(-s.log(poly),x,0,7).removeO()
require(zero(expanded-series),"trace_log_all_cyclic_classes_to_order_six")
# Newton trace reconstruction on the SAME r=3 recorded-label subspace,
# with first variations propagated without diagonalization or new Hilbert space.
powers=[s.Integer(3)]+[s.trace(sub**k) for k in range(1,4)]
es=[s.Integer(1)]
for k in range(1,4):
    es.append(s.expand(sum((-1)**(j-1)*es[k-j]*powers[j] for j in range(1,k+1))/k))
newton_det=sum((-x)**k*es[k] for k in range(4))
require(zero(newton_det-poly),"newton_traces_recover_exact_finite_no_click_polynomial")
# A noncommuting three-by-three direction of the actual recorded source.
dsub=dF[:3,:3]
require(not zero(sub*dsub-dsub*sub),"native_33_scene_compressed_minor_source_is_noncommuting")
dp=[s.Integer(0)]+[k*s.trace(sub**(k-1)*dsub) for k in range(1,4)]
de=[s.Integer(0)]
for k in range(1,4):
    de.append(s.expand(sum((-1)**(j-1)*(de[k-j]*powers[j]+es[k-j]*dp[j]) for j in range(1,k+1))/k))
detnewton=sum((-x)**k*de[k] for k in range(4))
detdirect=s.trace((s.eye(3)-x*sub).adjugate()*(-x*dsub))
require(zero(detnewton-detdirect),"newton_trace_determinant_first_source_matches_adjugate")
require(zero(s.diff(-s.log(poly),x)-s.trace(sub*(s.eye(3)-x*sub).inv())),
        "Jacobi_source_exact_without_diagonalizing_native_minor")

# The complete matrix trace stays >=0 at every power despite negative cycle
# contributions; a path-by-path positive probability law is not the trace sum.
require(all(s.trace(F**k)>0 for k in range(1,5)),
        "positive_native_trace_powers_do_not_make_each_walk_positive")
require(s.trace(dF)!=0 and s.trace(F**2*dF)!=0,
        "native_record_variations_act_on_first_and_third_trace_moments")

result={
 "scope":"actual K(9,11,13) complete recorded Eulerian words; conditional finite operator readout, NOT physical action admission or Einstein source",
 "input":"A4D_NATIVE_CYCLIC_HISTORY_PRICE_PREPARATION.md, 33-node symmetric scene and its full record projection",
 "status":"exact symbolic/graph checks PASS",
 "record_length":len(base_word)-1,"whole_scene_vertices":N,"directed_edges_per_repeat":718,
 "record_repetitions":2,"all_33_visit_degrees":dict(Counter(degrees)),
 "return_rank":NATIVE_F_RANK,"trace_return":str(s.trace(F)),
 "three_cycle_weight":str(tri),"three_cycle_float":float(tri),
 "three_cycle_derivative":str(tri_dot),"three_cycle_derivative_float":float(tri_dot),
 "source":source,
 "simultaneous_native_projector_and_link_source":{"dJ_from_P":str(sourceP),"dJ_from_U":str(sourceU),"dJ_total":str(sourcePU),"noncommuting":True},"small_principal_minor":{"det_pencil":str(s.factor(poly)),"trace_class_orbits":rooted_counts},
 "sign_obstruction":"the 3-cycle has negative product in native label basis and survives label phase gauge; raw per-cycle probabilities cannot equal products of F_ij",
 "physical_gates_open":["native admission of signed/phase-coherent return cycle weighting", "cyclic origin unobservability under complete future readouts", "Cost-Info = minus log of this grouped event with retained controller/archive costs", "moving coframe/link/observer/retained history source plus h^-2 GR refinement"],
 "checks":checks,"checks_count":len(checks)
}
jsonfile=HERE/'RESULT.json'
jsonfile.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
print('PASS',len(checks),'result',jsonfile)
print('triangle',tri,'derivative',tri_dot)
print('native z dJ',source['native_z_2powminus20']['d_minus_M_logdet'])
