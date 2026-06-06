#!/usr/bin/env python3
import math, json
phi=(1+math.sqrt(5))/2
delta=(math.sqrt(5)-2)/2
# action section
V=33; rank=3; nullity=30; gamma=nullity//rank
assert gamma==10
assert 2*(2*gamma-1)==38
# EM residual exponent
ABCD=4; Omega8=8; dim_g=12
assert (ABCD+1)/Omega8==5/8
assert Omega8*ABCD*dim_g==384
eta=5/8+delta/384
# archive roots
lc=1.5-math.sqrt(10)/40
lr=1.5+math.sqrt(10)/40
for lam in (lc,lr):
    assert abs(160*lam*lam-480*lam+359)<1e-12
assert abs(lc+lr-3)<1e-12
assert abs(lc*lr-359/160)<1e-12
# ladder
for D in range(1,8):
    assert abs(2*delta*phi**(D-1)-phi**(D-4))<1e-12
res={
 'status':'PASS_V11_22_CRITIC_CLOSURE_ARITHMETIC',
 'gamma':gamma,
 'N_act':38,
 'eta_EM':eta,
 'lambda_c':lc,
 'lambda_r':lr,
 'archive_polynomial':'160 lambda^2 - 480 lambda + 359',
 'em_cell_denominator':Omega8*ABCD*dim_g,
}
print(json.dumps(res, indent=2))
