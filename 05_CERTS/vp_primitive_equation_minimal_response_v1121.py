#!/usr/bin/env python3
import math
p=(math.sqrt(5)-1)/2
phi=(1+math.sqrt(5))/2
assert 0<p<1
assert abs(p+p*p-1)<1e-14
assert abs(p-1/phi)<1e-14
for x in [i/100 for i in range(1,100)]:
    assert 2*x+1>0
p_plus=1/phi
p_minus=1/(phi*phi)
delta0=(p_plus-p_minus)/2
assert abs(delta0-1/(2*phi**3))<1e-14
for D in range(1,8):
    assert abs(2*delta0*(phi**(D-1))-phi**(D-4))<1e-12
print('PASS_D0_PRIMITIVE_EQUATION_MINIMAL_RESPONSE_CLOSURE_V11_21')
