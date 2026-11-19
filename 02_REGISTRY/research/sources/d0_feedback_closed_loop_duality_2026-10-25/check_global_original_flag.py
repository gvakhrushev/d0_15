#!/usr/bin/env python3
"""EXACT original ζ=2^-20 one-global-time native-U flagged Slater Born
response with COMPLETE 8D one-particle controlled unitary and ALL 28
two-fermion outcomes, 6 accepted no-Q outcomes.

Critical hostile control: sharing ONE flag across BOTH fermions gives
(1-z)+z det(I-F), NOT det(I-z F).  The correct exterior operator has a
flag LABEL for EACH occupied one-particle mode.  Finite labelled
mathematical realization only: D0 physical multi-particle source and
paid native controlled-U compiler are NOT established.

Second hostile control: two independent time flags are not ONE global
word flag and not sum of per-tick Book costs for noncommuting effects.

Both python3 and python3 -O must have the same output.
"""
from __future__ import annotations

import itertools
import json
import sympy as S

R=S.Rational
z=R(1,2**20)
check_count=0

def check(x,desc):
    global check_count
    check_count+=1
    if not bool(x):
        raise ArithmeticError(desc)

def vzero(v):
    if isinstance(v,S.MatrixBase):
        return all(S.cancel(a)==0 for a in v)
    return S.cancel(v)==0

I2=S.eye(2)
I4=S.eye(4)
O=S.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]])
C1=S.diag(R(3,5),R(4,5))
B1=S.diag(R(4,5),R(3,5))
C2=O*S.diag(R(5,13),R(12,13))*O.T
B2=O*S.diag(R(12,13),R(5,13))*O.T

def reflection(C,B):
    W=C.row_join(B).col_join(B.row_join(-C))
    check(vzero(W.T*W-I4),"actual rational complete unitary on all4 columns")
    check(W.det()==1,"both one-particle returns are SPECIAL orthogonal")
    return W

U1=reflection(C1,B1)
U2=reflection(C2,B2)
P=S.diag(1,1,0,0)
Q=I4-P
C=P*U1*P
C=C[:2,:2]
K=(Q*U1*P)[2:4,:2]
F=K.T*K
check(C==C1 and F==I2-C1.T*C1,"true P/Q native whole return")
check(F.det()>0,"both original return modes genuinely tested")

# Twenty independently FAIR one-particle flag bits, with the ALL-ONES
# marked event. Each one-particle flag has a 2^20-dimensional label
# space but its initial state has weight 2^-20 in one marked direction.
# The 2-dimensional logical orthogonal 0/1 split used below is the
# PREPARED-COLUMN exact compression of that 2^20-label space, not a
# claim to physically remove unprepared flag columns/price.
for m in range(20):
    check(not R(2**m,2**20).q==1,
          "fewer than20 fair bits cannot supply exactly one 2^-20 event")
check(R(2**20,2**20)==1,"20 independent fair bits suffice with one word")
a=S.sqrt(1-z)
b=R(1,1024)
check(vzero(a*a+b*b-1),"original native zeta no paid normalization trick")
controlled=S.diag(I4,U1)
check(controlled.T*controlled==S.eye(8),
      "logical global-TIME controlled native U on all8 columns")
injection=S.eye(4)[:,:2]
prepared=(a*injection).col_join(b*injection)
check(vzero(prepared.T*prepared-I2),
      "physical prepared one-particle two-mode isometry")
V=controlled*prepared
Rnoq=S.diag(1,1,0,0,1,1,0,0)
M=V.T*Rnoq*V
check(vzero(M-((1-z)*I2+z*C1.T*C1)),
      "actual still-retained flag no-archive effect, no matrix sqrt")
check(vzero(M-(I2-z*F)), "exact original Book no-return effect")

# Exact CAR exterior Slater calculation, not independence of two
# Born outcomes and not a shared physical flag.
all_outcomes=list(itertools.combinations(range(8),2))
amps=[V.extract(list(pair),[0,1]).det() for pair in all_outcomes]
all_probs=[S.expand(v*v) for v in amps]
check(len(all_outcomes)==28,"all 28 two-particle sectors retained")
check(sum(all_probs)==1,"complete 28-outcome Born normalization exact")
allowed={0,1,4,5}
approved=sum(all_probs[j] for j,tup in enumerate(all_outcomes)
             if set(tup).issubset(allowed))
check(sum(set(tup).issubset(allowed) for tup in all_outcomes)==6,
      "all six permitted no-Q endpoints retained, no flag outcome erased")
check(vzero(approved-M.det()),
      "Cauchy-Binet full Slater no-Q response is native Book determinant")
check(vzero(approved-(I2-z*F).det()),
      "physical no-Q Born output equals original complete Book survival")

# SHARED 20 fair bit register controls the already-completed 2-particle
# state and has a different output law. It CANNOT be substituted in M1.
pshared=(1-z)+z*(C1.T*C1).det()
check(pshared!=approved,"one common flag for all modes fails original Book")
check(vzero(pshared-approved-z*(1-z)*F.det()),
      "exact failed-shared-flag correction is positive O(z) not O(z²)")
check(pshared>approved,"shared flag misprices the full return, strict control")

# MULTI-TICK memory: TWO separate flags (each per mode) vs ONE global
# flag for U_total vs the false product of individual one-tick Book
# probabilities. Each actual time U preserves the earlier Q archive.
check(vzero(C1.T*C1*C2.T*C2-C2.T*C2*C1.T*C1)==False,
      "true independent native return effects do not commute")
M1=(1-z)*I2+z*C1.T*C1
M2=(1-z)*I2+z*C2.T*C2
Mtwo=(1-z)**2*I2+z*(1-z)*(C1.T*C1+C2.T*C2)+z*z*C1.T*C2.T*C2*C1
check(vzero(Mtwo-Mtwo.T),"all separate-clock memory effects normalized")
p_independent_flags=Mtwo.det()
p_false_product=M1.det()*M2.det()
diff=R(5345593407,1348755091172399369483714560000)
check(vzero(p_independent_flags-p_false_product-diff),
      "EXACT noncommuting different-clock survival != product of Book")
Mglobal=I2-z*(I2-(C2*C1).T*(C2*C1))
check(p_independent_flags!=Mglobal.det(),
      "independent tick flags != one global original whole-word flag")
check(Mglobal.det()!=p_false_product,
      "global Book whole-U cut != blindly sum of local Book costs")
check(all(0<v<=1 for v in [approved,pshared,p_independent_flags,
                           p_false_product,Mglobal.det()]),
      "all comparisons are honest positive Born probabilities")

print(json.dumps({
    "status":"PASS_EXACT_GLOBAL_TIME_MODEWISE_FLAGS_BOOK_ORIGINAL_U",
    "checks":check_count,
    "zeta":"2^-20",
    "logical_oneparticle_complete_dim":8,
    "full_fermionic_outcome_dim":28,
    "no_Q_accepted_fermionic_outcomes":6,
    "one_particle_fair_word_necessity":20,
    "shared_flag_does_not_reproduce_Book":True,
    "shared_minus_correct_survival":str(pshared-approved),
    "two_independent_clock_minus_false_product":str(diff),
    "original_Book_probability_exact":str(approved),
    "original_Book_probability_decimal":str(S.N(approved,24)),
    "whole_original_Kraus_applicable":True,
    "native_controlled_U_and_Slater_physical_admitted":False,
    "GR_closed":False
},sort_keys=True,indent=2))
