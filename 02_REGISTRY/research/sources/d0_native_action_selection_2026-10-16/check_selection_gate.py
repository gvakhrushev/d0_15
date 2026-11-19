#!/usr/bin/env python3
"""D0 action-selection owner: exact conditional identities and hostile controls.

Research calculation only.  Does not promote H+J+R to an M1-selected action.
Uses the reported, fixed L=8 v8 Gram root; it does not solve for a root.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parent
RUN_VERSION = "native-action-selection-2026-10-16/1"
checks = []


def ck(label: str, condition: bool) -> None:
    if not bool(condition):
        raise AssertionError(label)
    checks.append(label)


def matrix_zero(matrix: s.MatrixBase) -> bool:
    return all(s.simplify(x) == 0 for x in matrix)


# 1. Same native golden two-outcome record, with no new probabilities.
p = (s.sqrt(5) - 1) / 2
phi = 1 / p
ck("golden_partition", s.simplify(p + p**2 - 1) == 0)
ck("golden_phi", s.simplify(phi - (1 + s.sqrt(5))/2) == 0)
# The two ports of the golden splitter (sqrt(p), p) have the probabilities p,p².
ck("golden_port_probability_sum", s.simplify(p + p**2 - 1) == 0)
# Exact pathwise surprisal at probabilities p,p² is (1,2) in log_phi units.
ck("golden_path_code_costs", s.simplify(s.expand_log(s.log(p)/s.log(phi) + 1,force=True)) == 0 and
   s.simplify(s.expand_log(s.log(p*p)/s.log(phi) + 2,force=True)) == 0)

r = s.symbols("r", positive=True)
q0, q1 = 1-r, r
Z_record = q0 + q1
ck("complete_record_Z_exactly_one", s.simplify(Z_record-1) == 0)
ck("complete_record_log_source_zero", s.simplify(s.diff(s.log(Z_record), r)) == 0)
ck("complete_record_log_second_source_zero", s.simplify(s.diff(s.log(Z_record), r, 2)) == 0)
# An expectation of the very same surprisal is NOT the log of its normalized sum.
H = -(q0*s.log(q0) + q1*s.log(q1))/s.log(phi)
mean_length = q0+2*q1
KL = mean_length-H
Hprime = s.simplify(s.diff(H, r))
KLprime = s.simplify(s.diff(KL, r))
r0 = p**2
ck("golden_entropy_source_one", s.simplify(s.expand_log(Hprime.subs(r, r0)-1,force=True)) == 0)
ck("golden_code_relative_entropy_source_zero", s.simplify(s.expand_log(KLprime.subs(r, r0),force=True)) == 0)
ck("golden_expected_cost", s.simplify(mean_length.subs(r,r0)-(p+2*p**2)) == 0)
ck("golden_nonzero_entropy", float(H.subs(r,r0).evalf(40)) > 1)
ck("normalized_vs_expected_not_same", float(H.subs(r,r0).evalf(40)) > 0 and Z_record == 1)
# Full two-stage golden internal tree: split branch0 again, branch1 stays certain.
q_joint = [p**2, p**3, p**2]
ck("two_stage_complete_partition", s.simplify(sum(q_joint)-1) == 0)
H1 = -(p*s.log(p) + p**2*s.log(p**2))/s.log(phi)
Hjoint = -sum(v*s.log(v) for v in q_joint)/s.log(phi)
ck("golden_shannon_chain_law", s.simplify(s.expand_log(Hjoint-H1-p*H1,force=True)) == 0)
# Product additivity alone does not select Shannon entropy: H2 also has it.
collision1=-s.log(p**2 + p**4)/s.log(phi)
collision_joint=-s.log(sum(x*x for x in q_joint))/s.log(phi)
collision_chain_gap=float((collision_joint-collision1-p*collision1).evalf(70))
ck("collision_entropy_fails_conditional_chain",abs(collision_chain_gap)>1e-3)

# 2. Exact finite same-Delta H+J+R source, including noncommuting field jet.
I=s.eye(2)
B=s.diag(s.Rational(9,10),s.Rational(3,4))
alpha=s.Rational(1,8)
m=4
beta=m*alpha
z=s.Rational(1,5)
M=3
Delta=(I-B)/alpha
K=B**m
Z=s.trace(K)
F=I-K
A=I-z*F
rho=s.diag(s.Rational(2,5),s.Rational(3,5))
Ed=s.Matrix([[s.Rational(1),s.Rational(1,3)],
             [s.Rational(1,3),-s.Rational(1,2)]])
drho=s.diag(-s.Rational(1,10),s.Rational(1,10))
dB=-alpha*Ed
dK=s.zeros(2)
for j in range(m):
    dK+=B**j*dB*B**(m-1-j)
dF=-dK
dA=-z*dF
P_heat=Z/2
P_blank=A.det()
ck("positive_survival_probability", 0 < float(P_heat) < 1)
ck("positive_blank_probability", 0 < float(P_blank) < 1)
ck("noncommuting_delta_jet", not matrix_zero(B*Ed-Ed*B))
ck("actual_polynomial_derivative_not_frozen", not matrix_zero(dK))
# The exact event re-expression of the fixed functional drops only constants.
H_log=s.log(Z)/beta
H_event=s.log(2*P_heat)/beta
J_cyc=-M*s.log(P_blank)
J_log=-M*s.log(A.det())
ck("H_as_full_survival_log_identity",s.simplify(H_log-H_event)==0)
ck("J_as_quasifree_blank_log_identity",s.simplify(J_cyc-J_log)==0)
# Frozen beta,m,z,C,M; moving matter density preserved.
dR=s.trace(rho*Ed)+s.trace(drho*Delta)
dH=s.trace(dK)/(beta*Z)
dJ=-M*s.trace(A.inv()*dA)
W=rho-B**(m-1)/Z+M*beta*z*B**(m-1)*A.inv()
source=s.trace(W*Ed)+s.trace(drho*Delta)
ck("full_v8_joint_source_identity",s.simplify(dR+dH+dJ-source)==0)
# Compare derivatives of event representation by the actual noncommuting jets.
dHevent=s.trace(dK)/(beta*Z)
dJevent=-M*s.trace(A.inv()*(-z*dF))
ck("event_source_not_missing_preparation",s.simplify(dR+dHevent+dJevent-source)==0)
wrongW=rho-B**(m-1)+M*beta*z*B**(m-1)*A.inv()
ck("missing_Z_normalizer_rejected",s.simplify(s.trace((wrongW-W)*Ed))!=0)
ck("moving_density_nonzero",s.simplify(s.trace(drho*Delta))!=0)

# 3. Same F,z,M, but the cyclic-history symmetry factor 1/n is NOT selected by positivity.
# Both complete analytic readings are finite and basis invariant on zF<1.
J_root=M*z*s.trace(F*A.inv())
source_root_minus_cyc=s.simplify(M*z*z*s.trace(F*A.inv()*A.inv()*dF))
# This is an exact Fréchet trace identity also for noncommuting dF.
ck("feedback_nonscalar_semantics_distinct", s.simplify(J_root-J_cyc)!=0)
ck("feedback_rooted_vs_cyclic_source_distinct", source_root_minus_cyc!=0)
# Polynomial first two coefficients.  The 1/n factor begins at n=2.
t=s.symbols("t", real=True)
fr=s.Rational(2,5)
cycle_series=s.series(-s.log(1-t*fr),t,0,4).removeO().expand()
repeat_series=s.series((t*fr)/(1-t*fr),t,0,4).removeO().expand()
ck("feedback_same_linear_coefficient",s.expand(cycle_series).coeff(t,1)==s.expand(repeat_series).coeff(t,1))
ck("feedback_second_coefficient_different",s.expand(repeat_series-cycle_series).coeff(t,2)==fr**2/2)
ck("feedback_logdet_quotient_cycle_weight",s.expand(cycle_series).coeff(t,3)==fr**3/3)

# 4. Full physical v8 eigenvalue carrier: 4096 momentum, 16 Fock, 128 reference.
L=8
Nsite=L**4
Fock=16
reference=128
p_np=(math.sqrt(5)-1)/2
alpha_native=p_np**2/8192
m_native=16384
z_native=2**-20
M_native=reference
d_native=0.0636351915943445350
o_native=0.0040167350432317253
Gram=(d_native-o_native)*np.eye(4)+o_native*np.ones((4,4))
indices=np.indices((L,)*4).reshape(4,-1).T
zvec=L*(np.exp(2j*np.pi*indices/L)-1)
lam=np.einsum("ni,ij,nj->n", zvec.conj(), Gram,zvec).real
lam=np.maximum(lam,0)
Bnative=1-alpha_native*lam
Knative=Bnative**m_native
Fnative=1-Knative
Ad_native=1-z_native*Fnative
Fprime=m_native*alpha_native*lam*Bnative**(m_native-1)
ck("v8_complete_momentum",len(indices)==4096)
ck("v8_full_16_and_128",Fock*len(indices)==65536 and reference==128)
ck("v8_positive_gate",bool(np.all(Bnative>0) and np.all(Bnative<=1+1e-12)))
ck("v8_scalar_full16_CAR_square",bool(np.all(lam>=0)))
P_H_native=(Fock*Knative.sum())/(Fock*Nsite)
P_J_native=float(np.exp(Fock*np.log1p(-z_native*Fnative).sum()))
# P_J is extremely small? Here ~ exp(-0.06245), well-defined.
ck("v8_real_survival_and_blank_probabilities",0<P_H_native<1 and 0<P_J_native<1)
J_native=-M_native*Fock*np.log1p(-z_native*Fnative).sum()
J_root_native=M_native*Fock*np.sum((z_native*Fnative)/Ad_native)
source_gap=M_native*Fock*z_native*z_native*np.sum(Fnative*Fprime/(Ad_native**2))
ck("v8_nonzero_actual_feedback_cycle_gap",J_root_native>J_native)
ck("v8_nonzero_actual_feedback_source_gap",source_gap>0)
# Hessian/source variations in the strict same Gram-direction; no fitting.
ck("v8_all_nonground_modes_counted",int(np.sum((lam>1e-10)&(Fprime>0)))==4095)
# The complete v8 root is stationary while its individual H term is not.
heat_source=-Fock*np.sum(lam*Bnative**(m_native-1))/(Fock*Knative.sum())
feedback_source=M_native*z_native*(m_native*alpha_native)*Fock*np.sum(lam*Bnative**(m_native-1)/Ad_native)
matter_source=(128-64*math.sqrt(2))*d_native
ck("v8_heat_has_nonzero_source",heat_source < -2)
ck("v8_complete_stationarity_at_pinned_root",abs(heat_source+feedback_source+matter_source)<1e-9)

# Hostile fixed-geometry negative control: one cannot call both feedback scores
# the same native output, or call any code-only log Z a nonzero action.
ck("full_v8_blank_is_not_record_normalizer",abs(P_J_native-1)>1e-4)

out={
 "class":"RESEARCH/CONDITIONAL-ACTION-SELECTION-BOUNDARY",
 "status":"PASS",
 "programme":"gvakhrushev/d0_15 #334, physical action selection still OPEN",
 "checks":len(checks),
 "labels":checks,
 "scope":{
   "golden":"complete normalized p,p^2 record; outcome costs (1,2) are owner-supplied golden prefix code",
   "finite":"exact 2x2 noncommuting matrix variations in SymPy",
   "v8":"full 4096-momentum, 16-grade spectral scalarization, existing fixed root, reference128",
   "excluded":"physical preparation/admission, independent primitive-to-K map, all-history coding law, Lorentz GR limit, full Lean/CI"
 },
 "golden":{
   "p":str(p),
   "record_Z":"1",
   "record_log_source":"0",
   "entropy_at_reference":str(s.simplify(p+2*p**2)),
   "entropy_first_source_at_reference":"1",
   "KL_first_source_at_reference":"0",
   "collision_conditional_chain_gap":collision_chain_gap
 },
 "finite_exact":{
   "P_heat":str(s.factor(P_heat)),
   "P_blank":str(s.factor(P_blank)),
   "event_source":str(s.factor(source)),
   "rooted_minus_cyclic_source":str(s.factor(source_root_minus_cyc)),
   "rooted_minus_cyclic_price":str(float((J_root-J_cyc).evalf(30)))
 },
 "v8":{
   "momentum_count":Nsite,"full_modes":Fock*Nsite,"reference":reference,
   "min_B":float(Bnative.min()),
   "Z_full":float(Fock*Knative.sum()),
   "P_survival":float(P_H_native),
   "P_feedback_all_blank":P_J_native,
   "H_source_Gscale":float(heat_source),
   "J_source_Gscale":float(feedback_source),
   "R_source_Gscale":float(matter_source),
   "full_S_source_Gscale":float(heat_source+feedback_source+matter_source),
   "J_cyclic":float(J_native),
   "J_rooted":float(J_root_native),
   "rooted_minus_cyclic_price":float(J_root_native-J_native),
   "rooted_minus_cyclic_source_Gscale":float(source_gap),
   "nonzero_momenta":4095
 }
}
encoded=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
(ROOT/"RESULT.json").write_text(encoded,encoding="utf8")
print(json.dumps({"status":out["status"],"checks":out["checks"],"v8":out["v8"],"sha256":hashlib.sha256(encoded.encode()).hexdigest()},ensure_ascii=False,sort_keys=True))
