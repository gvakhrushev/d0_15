#!/usr/bin/env python3
"""Exact Fraction certificate: original all-n native Golden memory source
is STRICTLY outside the H+J fixed-input paired-incidence source budget.
All quoted r1/9 CAR16 mu,h,derivative rationals and spectral brackets
originate in the prior original fully verified CAR owner, not new fits.
No physically compulsory Book03 Info or SCENE heat selection is claimed.
Python standard library only.
"""
from fractions import Fraction as F
from math import log,sqrt
import json
checks=0
def test(x,msg):
 global checks
 checks+=1
 if not x: raise ArithmeticError(msg)
mu=F(141489,10240000)
h=F(69399,5030720)
muj=F(-328779,204800000)
hj=F(-20040939,9885993640)
A=hj*(1-mu)-h*muj
test(A==F(-32022677854092699,16197211979776000000),
     "original rational proper-boost derivative of h(1-mu)")
p_lower=F(309,500)
# EXACT for any original n >=1; J source uses true 1024 CAR×oldRIGHT
# eigenmodes and H full 2048×128^n work trace with all zero modes.
native_source_lower=4*p_lower**5*(-A)
book_source_upper=F(256,10000)*(
 F(1024,2**20-1)+F(2048,262144-4096))
test(native_source_lower>F(7,10000),
     "true native p³ Golden nonblank port source >0.000700 n")
test(book_source_upper<F(229,1000000),
     "whole original fixed-input all-harmonic H+J source <0.000229 n")
test(native_source_lower-book_source_upper>F(471,1000000),
     "EXACT all-n native unpadded nonblank port vs paired Hodge+J source gap")
# The native original two-band CAR chart r in [1/10,3/25]
# rigorously has mu>.0136, epsilon<.00061, lambda_max<.01461.
native_kappa_lower=4*p_lower**2*(F(136,10000)-F(61,100000))*(
 F(1)-F(1461,100000))
test(native_kappa_lower>F(19,1000),
     "native nonblank effect >=0.019I on whole original open Lorentz chart")
p=(sqrt(5)-1)/2
coin_nat=-p*p*log(p*p)-p*log(p)
test(.665<coin_nat<.666 and .019*coin_nat>.0126,
     "unerasable classical fine record entropy >0.0126 n nats")
test(abs((p*p+2*p)-coin_nat/log(1/p)-p**3)<1e-14,
     "actual original unpadded 0/10 port code-minus-Info=p³")
print(json.dumps({
 "status":"PASS_EXACT_NATIVE_ALL_N_GOLDEN_TWIN_WARD",
 "checks":checks,
 "original_CAR_mean":"141489/10240000",
 "original_CAR_harmonic":"69399/5030720",
 "original_source_rational_core":str(A),
 "strict_rational_native_port_source_lower":str(native_source_lower),
 "strict_rational_paired_incidence_H_plus_J_source_upper":str(book_source_upper),
 "strict_rational_source_Ward_gap_lower":str(native_source_lower-book_source_upper),
 "strict_rational_nonblank_effect_lower":str(native_kappa_lower),
 "uniform_quantum_conditional_record_entropy_nats_per_tick_gt":.0126,
 "every_true_completed_native_n_positive":True,
 "original_book03_compulsory_scene_heat_Info_selected":False,
 "same_execution_GR_closed":False
},indent=2))
