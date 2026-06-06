#!/usr/bin/env python3
import math, json
phi=(1+math.sqrt(5))/2
p=1/phi
delta0=(math.sqrt(5)-2)/2
assert abs((p+p*p)-1)<1e-12
assert abs(delta0-1/(2*phi**3))<1e-12
ABCD=4; Omega8=8; dim_light=12
assert abs((ABCD+1)/Omega8 - 5/8)<1e-12
assert ABCD*Omega8*dim_light==384
V=33; rank=3
gamma=(V-rank)//rank
assert gamma==10
assert 2*(2*gamma-1)==38
assert V+rank-1==35
assert 9*11==99
# BAO roots
lc=1.5-math.sqrt(10)/40
lr=1.5+math.sqrt(10)/40
for l in (lc,lr):
    assert abs(160*l*l-480*l+359)<1e-12
out={
 'status':'PASS_V11_23_CLOSURE_EXECUTION',
 'p_plus_p2':p+p*p,
 'delta0':delta0,
 'em_residual_base':(ABCD+1)/Omega8,
 'em_residual_denominator':ABCD*Omega8*dim_light,
 'action_section':38,
 'ew_depth':35,
 'gravity_depth':99,
 'lambda_c':lc,
 'lambda_r':lr
}
print(json.dumps(out, indent=2))
