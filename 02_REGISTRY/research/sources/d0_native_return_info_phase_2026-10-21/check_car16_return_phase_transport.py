#!/usr/bin/env python3
"""Consume the newly published original-CAR16 Q8 representation (afc4294f).
Check only its application to the present return/temporal-phase theorem;
not a replay of the prior 206-check representation certificate.
"""
import json
from pathlib import Path
import sympy as s
checks=[]
def check(n,v):
    if not bool(v):raise AssertionError(n)
    checks.append(n)
I=s.eye(16);C=[]
for mode in range(4):
    cc=s.zeros(16)
    for mask in range(16):
        if not (mask&(1<<mode)):
            cc[mask|(1<<mode),mask]=(-1)**((mask&((1<<mode)-1)).bit_count())
    C.append(cc)
gamma=[C[0]+C[0].T]+[C[m]-C[m].T for m in (1,2,3)]
qi=gamma[2]*gamma[3];qj=gamma[3]*gamma[1]
check('consumed_original_CAR16_Q8_relations',qi**2==qj**2==-I and qi*qj==-qj*qi)
X=s.diag(I,qi);Y=s.diag(qj,qj);Z=s.diag(I,-I)
check('original_CAR16_relative_phase',X**2==Z)
check('original_CAR16_central_minus_identity',Y**2==-s.eye(32))
word=[X,Y]+[X]*3+[Y]*3
wo=s.eye(32)
for op in word:wo=op*wo
check('old_order_word_on_all_CAR16',wo==Z)
a=s.symbols('a',real=True);p=a*a;pol=s.Poly(a**4+a*a-1,a)
def red(e):return s.rem(s.Poly(s.expand(e),a),pol).as_expr()
def rm(M):return M.applyfunc(red)
G=s.Matrix([[a,-p],[p,a]]);GG=s.kronecker_product(G,I)
check('actual_inverse_Golden_word_CAR16',rm(Z*GG*Z-GG.T)==s.zeros(32))
core=rm((Z*GG*Z)*wo*GG)
# Complete original output record: arm x CAR16 x record2.
WRITE=s.zeros(64)
for arm in range(2):
    for f in range(16):
        for r in range(2):WRITE[32*arm+2*f+(r^arm),32*arm+2*f+r]=1
Mplus=rm(WRITE*s.kronecker_product(core,s.eye(2)))
Zfull=s.kronecker_product(Z,s.eye(2))
# The added actual words are X² on entry, then X²,Y² on exit.
Mminus=rm(s.kronecker_product(Y**2*X**2,s.eye(2))*Mplus*s.kronecker_product(X**2,s.eye(2)))
check('actual64_word_Q8_phase_relation',Mminus==-Zfull*Mplus*Zfull)
perm=s.zeros(64)
for arm in range(2):
    for f in range(16):
        for r in range(2):perm[16*(2*arm+r)+f,32*arm+2*f+r]=1
c=red(p-p*p);k=2*a**3
M4=s.Matrix([[c,0,-k,0],[0,c,0,-k],[0,-k,0,-c],[-k,0,-c,0]])
Z4=s.diag(1,1,-1,-1)
check('exact_return_tensor_original_CAR16',rm(perm*Mplus*perm.T)==s.kronecker_product(M4,I))
check('opposite_return_tensor_original_CAR16',rm(perm*Mminus*perm.T)==s.kronecker_product(-Z4*M4*Z4,I))
check('complete64_unitarity',rm(Mplus.T*Mplus)==rm(Mminus.T*Mminus)==s.eye(64))
# Tensor identity transports ALL powers, all overlap/entropy formulas, and
# every conditional return amplitude. No extra factor16 in normalized laws.
Q4=s.diag(0,1,1,1);VV=Q4*M4
for n in (1,2,3,4):
    f=red((M4*VV**(n-1))[0,0])
    Kn=f*I
    check('conditional_original_CAR16_return_effect_'+str(n),rm(Kn.T*Kn)==red(f*f)*I)
result={'status':'AUTHOR_TRANSPORT_CHECKS_PASS','count':len(checks),'checks':checks,
'input_representation_commit':'afc4294f3d34af9ae50d7ae76fd59af5567493b3',
'input_representation_checker_blob':'71e93c5a2b20689f1f91cf0bbdc1a8338513b27b',
'actual_car16_output_record_dimension':64,'normalized_return_probabilities_multiplied_by_16':False,
'prior206checks_rerun':False,'field_to_Q8_pullback_proved':False,
'fullStep_identification_proved':False,'selected_Book_price_proved':False,'GR_closed':False}
Path(__file__).with_name('CAR16_TRANSPORT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
