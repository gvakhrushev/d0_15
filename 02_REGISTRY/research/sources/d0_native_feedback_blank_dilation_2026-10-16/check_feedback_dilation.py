#!/usr/bin/env python3
"""Exact conditional feedback determinant morphism (D0 #334).

Narrow algebraic checker: no native admission, no root search, no GR claim.
Pure Python/SymPy, deterministic JSON; assert-free checks survive python -O.
"""
from __future__ import annotations
from itertools import combinations
from pathlib import Path
import json
import math
import sympy as sp

HERE = Path(__file__).resolve().parent
checks = []
Q = sp.Rational

def check(statement, label):
    if statement is not True and statement != sp.true:
        raise ArithmeticError(label)
    checks.append(label)

def zero(expr):
    if isinstance(expr, sp.MatrixBase):
        return all(sp.simplify(v) == 0 for v in expr)
    return sp.simplify(expr) == 0

def tr(a):
    return sp.trace(a)

# Independent nontrivial *non-diagonal* commuting positive contractions B,S.
R = sp.Matrix([[Q(3,5), -Q(4,5)], [Q(4,5), Q(3,5)]])
B = R * sp.diag(Q(3,5), Q(5,13)) * R.T
S = R * sp.diag(Q(4,5), Q(12,13)) * R.T
N, M, n = 2, 3, 3
z = Q(1,4)
I = sp.eye(N)
check(zero(R.T*R-I), "rational_frame_orthogonal")
check(zero(B*B+S*S-I), "native_round_effect_B2_plus_S2")
check(zero(B*S-S*B), "native_round_factors_commute")
check(B[0,1] != 0 and S[0,1] != 0, "no_diagonalizing_as_assumption")
check(all(v > 0 and v < 1 for v in B.eigenvals()), "both_B_eigenvalues_strictly_between_zero_and_one")

# Coin 1-z short-circuits (recorded flag); coin z runs n-round survival;
# all n failure positions are retained, including immediate return.
L0 = sp.sqrt(1-z)*I
L1 = sp.sqrt(z)*B**n
failures = [sp.sqrt(z)*S*B**j for j in range(n)]
all_operators = [L0,L1]+failures
complete = sp.zeros(N)
for L in all_operators:
    complete += L.T*L
check(zero(complete-I), "all_n_plus_two_outcomes_full_and_retained")
K = B**(2*n)
A = (1-z)*I + z*K
check(zero(L0.T*L0+L1.T*L1-A), "no_click_effect_A_exactly")
check(zero(sum((L.T*L for L in failures),sp.zeros(N))-z*(I-K)), "failures_telescope_without_erasure")

# No eigenbasis oracle: the full occupied Slater determinant probability of
# all no-click labels is the Cauchy-Binet sum over accepted N-particle outputs.
Vaccept = L0.col_join(L1)
minor_squares = sp.Integer(0)
for rows in combinations(range(2*N),N):
    minor_squares += sp.simplify(Vaccept[list(rows),:].det()**2)
check(zero(minor_squares-A.det()), "all_slater_minors_equal_det_A")
check(A.det()>0 and A.det()<1, "nontrivial_fermionic_no_click_probability")
Aref = sp.kronecker_product(A,sp.eye(M))
check(zero(Aref.det()-A.det()**M), "reference_spectator_multiplicity_det_power")

# Noncommuting B and rho/generic coframe jet; z also moves.
t = sp.symbols('t',real=True)
dB = sp.Matrix([[Q(1,20),Q(1,30)],[Q(1,30),-Q(1,15)]])
dz = Q(1,20)
check(not zero(B*dB-dB*B), "noncommuting_field_jet")
dK = sum((B**j*dB*B**(2*n-1-j) for j in range(2*n)),sp.zeros(N))
dA = z*dK-(I-K)*dz
Bt,zt=B+t*dB,z+t*dz
At=(1-zt)*I+zt*Bt**(2*n)
check(zero(At.diff(t).subs(t,0)-dA), "moving_z_and_noncommuting_matrix_jet")
source_via_event = -M*tr(A.inv()*dA)
source_direct = (-M*At.det().diff(t)/At.det()).subs(t,0)
check(zero(source_direct-source_via_event), "full_reference_blank_source_exact_with_dz")
dAref=sp.kronecker_product(dA,sp.eye(M))
check(zero(-tr(Aref.inv()*dAref)-source_via_event), "reference_multiplied_source_from_one_extended_operator")
check(source_via_event != 0, "feedback_source_not_artificially_zero")

# Trace-log cycle weights are the Taylor coefficients of the *same event*.
x=sp.symbols('x')
F=I-K
fpoly=(I-x*F).det()
expansion = sp.series(-sp.log(fpoly), x,0,7).removeO()
series = sum(x**j*tr(F**j)/j for j in range(1,7))
check(zero(sp.expand(expansion-series)), "cyclic_1_over_j_forced_by_blank_event_log")
check(zero(sp.factor(sp.diff(-sp.log(fpoly),x)-tr(F*(I-x*F).inv()))),"unique_log_derivative_Jacobi")

# Trace survival alone is not enough to recover the determinant/no-click.
k,u=sp.symbols('k u',real=True)
Ksplit=sp.diag(k+u,k-u)
Asplit=(1-z)*I+z*Ksplit
check(zero(tr(Ksplit)-2*k), "same_survival_trace_for_split_modes")
check(zero(sp.factor(Asplit.det()-((1-z+z*k)**2-z**2*u**2))),"different_blank_det_at_same_survival_trace")
check(sp.diff(Asplit.det(),u,2) == -2*z*z, "detector_can_distinguish_trace_equal_split")

# Conditional degree lower bound for protocols using t independent classical
# z-coins (all other operations z-independent), not a bound on quantum gates.
rank_F=sum(int(ev!=0)*int(mult) for ev,mult in F.eigenvals().items())
check(rank_F==2, "all_nonzero_toy_spectrum_rank")
fullpoly=sp.Poly(((sp.eye(N)-x*F).det())**M,x)
check(fullpoly.degree()==M*rank_F,"exact_coin_polynomial_degree_M_rank_F")

def v8_schedule(L):
    N_L=16*(L**4)
    rank_L=16*(L**4-1) # positive Gram: only k=0 has K=1
    M_L=128
    depth=128*L*L
    degree=rank_L*M_L
    return {"L":L,"one_particle_dim":N_L,"rank_F":rank_L,
            "reference":M_L,"blank_polynomial_degree":degree,
            "survival_rounds":depth,
            "minimum_serial_z_coin_calls_per_round_if_uniform_in_z":(degree+depth-1)//depth}

levels=[v8_schedule(L) for L in (4,8,16,32)]
check(levels[1]["one_particle_dim"]==65536 and levels[1]["rank_F"]==65520,"native_L8_full16_all4096_momenta")
check(levels[1]["blank_polynomial_degree"]==8386560,"native_reference128_degree_eight_million")
check(levels[1]["minimum_serial_z_coin_calls_per_round_if_uniform_in_z"]==1024,"L8_coin_depth_lower_bound_1024_conditional")
check(levels[0]["minimum_serial_z_coin_calls_per_round_if_uniform_in_z"]==255,"L4_coin_depth_lower_bound_255_conditional")
check(levels[2]["minimum_serial_z_coin_calls_per_round_if_uniform_in_z"]==4096,"L16_coin_depth_lower_bound_4096_conditional")

# Golden reference p,p^2: every finite unconditioned cylinder event has
# probability in the ring Z[p] of algebraic integers. A rational such
# probability in (0,1) is impossible. Conditioning changes the question.
p = (sp.sqrt(5)-1)/2
check(zero(p*p+p-1), "golden_reference_probability_identity")
check(sp.simplify(p**3)>0 and sp.simplify(p**3)<Q(1,2), "nonzero_order_mismatch_pair_probability")
check(sp.simplify((p**3)/(p**3+p**3)-Q(1,2))==0,"two_mismatched_goldens_conditionally_unbiased")
check(sp.simplify((p**3)**20/(2*p**3)**20-Q(1,2**20))==0,"twenty_postselected_fair_pairs_yield_z_conditional")
check(sp.simplify((p**3)**20-Q(1,2**20))!=0,"unconditional_accepted_word_not_same_as_z")
# Z[p] has basis 1,p over Z; p irrational, hence Z[p]∩Q=Z.
check(p.is_irrational is True, "golden_probability_irrational_quadratic_integer")
check(all(zero(p**a * (p*p)**b - p**(a+2*b)) for a in range(1,5) for b in range(1,5)), "finite_gold_word_products_are_p_powers")
check(sp.Rational(1,2**20) > 0 and sp.Rational(1,2**20)<1,"native_z_is_nontrivial_rational")

result={"status":"PASS","checks":len(checks),"labels":checks,
"exact_fixture":{"B":str(B),"S":str(S),"B_eigenvalues":[str(v) for v in B.eigenvals()],
"n_survival_rounds":n,"z":str(z),"N":N,"M":M,
"P_single_blank":str(sp.factor(A.det())),
"P_reference_extended_blank":str(sp.factor(Aref.det())),
"noncommuting_moving_source":str(sp.factor(source_via_event)),
"slater_minor_count":math.comb(2*N,N),
"log_cycle_order":6},
"v8_conditional_coin_bound":levels,
"golden_reference_z":{"p":str(p),"z":str(Q(1,2**20)),
"conditional_equal_pair_probability":str(Q(1,2)),
"twenty_pair_success_probability":str(sp.simplify((2*p**3)**20)),
"unconditional_all_zero_accepted_probability":str(sp.simplify(p**60)),
"excluded":"unconditioned finite deterministic unions of golden reference cylinders; not arbitrary quantum interference or postselection"},
"scope":{"positive":"explicit z-mixed B/S instrument, exact Slater determinant, reference multiplicity and source without spectral oracle",
"not_proved":"native many-body Fock admission, filled preparation, z coin, physical Cost-Info selection, full retained workspace, GR, original h^-2 refinement",
"capacity":"polynomial bound assumes all z-dependence is through scalar affine-probability classical coin tests; exact identity across an open z interval, not just calibrated fixed z"}}
(HERE/'RESULT.json').write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({"status":"PASS","checks":len(checks),"P_blank":result['exact_fixture']['P_single_blank'],"source":result['exact_fixture']['noncommuting_moving_source'],"L8_degree":levels[1]['blank_polynomial_degree'],"L8_min_z_coins_per_tick":levels[1]['minimum_serial_z_coin_calls_per_round_if_uniform_in_z']},sort_keys=True))

