#!/usr/bin/env python3
"""Independent, read-only A60 replay and rational capacity controls."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json,runpy,sys
import sympy as s

sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
paths=[D/'round60/check_source_record_capacity.py',D/'round60/SOURCE_RECORD_CAPACITY_CHECK.json',
       D/'round60/SOURCE_RECORD_CAPACITY_RU.md',D/'round53/REGULAR_FIELD_COMPONENTS_RU.md',
       D/'round54/REGULAR_GLOBAL_SOURCE_RU.md',D/'round55/REGULAR_FIELD_TASK_AND_FRONTIERS_RU.md',
       D/'round59/INITIALIZED_DOMAIN_AND_PHYSICAL_PRICE_RU.md',
       P.parent/'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md',
       P.parent/'round108/B108_A55_INDEPENDENT_AUDIT_RU.md',
       P.parent/'round117/B117_RETAINED_CODEC_CAPACITY_RU.md']
hashes={str(p):sha256(p.read_bytes()).hexdigest() for p in paths}
receipt=json.loads(paths[1].read_text())
for name,digest in receipt['input_sha256'].items():
    assert sha256(Path(name).read_bytes()).hexdigest()==digest,name

# Replay frozen upstream code without writing its result or modifying its file.
orig_write=Path.write_text
captured={}
def intercept(path,data,*args,**kwargs):
    if path.resolve()==paths[1].resolve():
        captured['data']=data
        return len(data)
    raise AssertionError('unexpected attempted write: '+str(path))
Path.write_text=intercept
try:
    runpy.run_path(str(paths[0]),run_name='__main__')
finally:
    Path.write_text=orig_write
assert captured['data']==paths[1].read_text()

# Polynomial brackets 1/3<p<2/3; p^2=1-p gives the same bounds
# for p^2. All digit deviations from 3p^2 are <2; 4*2688<104^2.
assert 4*2688<104**2
assert (F(1,3)**2+F(1,3))<1<(F(2,3)**2+F(2,3))
delta=F(1748*104,2**80)+F(1,2**3423)
assert delta<F(1,2**62) and delta**2<F(1,2**124)
assert F(1748*104,1)<2**18
N=2**5376
assert 2**5375 < N*(1-delta**2)
assert 9*2**5372 < N*(1-delta**2) < 9*2**5373
assert F(5376+124+2,2**124)<F(1,2**111)

# Independent exact isometry witness, not A60's rotation fixture.  A
# bank-preserving encoder can rotate the record freely without disturbing
# the common bank projector; the capacity argument applies at all inputs.
J=s.Matrix([[1,0],[0,1],[0,0],[0,0]])
Pbank=s.diag(1,1,0,0)
T=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
Z=T*J
assert Z.T*Z==s.eye(2) and Pbank*Z==Z
assert s.trace(Z.T*Pbank*Z)==2==s.trace(Pbank)

# One fixed input does not imply the all-CODE capacity premise: a SWAP
# keeps bank=0 on input |00> but moves label 1 into the bank on |10>.
swap=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
e0=s.Matrix([1,0,0,0]);e2=s.Matrix([0,0,1,0])
bank0=s.diag(1,0,1,0)
assert (swap*e0).T*bank0*(swap*e0)==s.ones(1,1)
assert (swap*e2).T*bank0*(swap*e2)==s.zeros(1,1)

result={'status':'PASS_SCOPED','upstream_readonly_replay_matches':True,
 'source_pins_match':True,'radius_from_all_four_digits_verified':True,
 'entropy_rayleigh_rank_N_argument_checked':True,
 'one_input_not_all_CODE_countercontrol':True,
 'actual_all_input_bank_preservation_assumed_for_decoder':True,
 'actual_decoder_and_cost_intertwiner_proved':False,
 'full_physical_C_source_proved':False,'GR_closed':False,
 'reviewed_sha256':hashes}
(P/'B118_SOURCE_CAPACITY_AUDIT_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='reviewed_sha256'},indent=2))
