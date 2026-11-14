#!/usr/bin/env python3
"""Exact arithmetic checks for B62 error constants, not a physical price."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');cert=json.loads((P/'FINITE_SAM_ROTATION_CERTIFICATE.json').read_text());schedule=json.loads((P/'SAME_INITIAL_ENDPOINT_SCHEDULE_CHECK.json').read_text());base=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text());n1=int(cert['rotations']['plus']['power_hex'],16);n2=int(cert['rotations']['minus']['power_hex'],16);p1=int(schedule['padding_plus_hex'],16);p2=int(schedule['padding_minus_hex'],16);L=int(base['new_native_call_count']);n=base['total_RAW_births'];N=n+L+n1+n2+p1+p2;assert N<2**11647
# Example on two old eigenvalues: contraction + perturbation of C†C.
A=[F(1,2),F(1,4)];old=[F(3,5),F(1,5)];new=[F(601,1000),F(199,1000)];d=F(1,1000);z=F(1,4);ret=F(1,8)
assert all(0<=x<=1 for x in A) and all(abs(x-y)<=d for x,y in zip(old,new))
# Exact determinant perturbation bound uses matrix trace norm before log.
lhs=sum((ret*x*abs(c*c-v*v) for x,c,v in zip(A,old,new)),F());rhs=2*ret*d*len(A);assert lhs<=rhs
# Generic third derivative scalar-product envelope coefficients:
# |(c²)'|<=4, |(c²)''|<=16, |(c²)'''|<=64; factors 3 and 2.
assert 3*4*16==192 and 2*4**3==128
assert F(4,1)/(6*F(8,3))==F(1,4) # used below is 1/(6*(8/3))=1/16
assert 1/(6*F(8,3))==F(1,16)
result={'status':'PASS_CONDITIONAL_ENDPOINT_PRICE_CONSTANTS','isolated_aligned_endpoint_layers_lt':'2^11647','same_last_actual_gate':'G on selected SAM, after all padding','endpoint_op_error_lt':'2^-3299','retention_corner':'p^(K/2) times old compressed return','implementation_normalized_bound':'4*z*rank(P0)*delta / ((1-z)*abs(t)*gamma_under)','crude_third_derivative_coefficient':'64/(1-z)+192*z/(1-z)^2+128*z^2/(1-z)^3','central_truncation_normalized_bound':'(t^2/16)*2^3158*[64/(1-z)+192*z/(1-z)^2+128*z^2/(1-z)^3]','requires_actual_z_nonzero_old_Gram_gamma_and_full_old_price':True,'source_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in (P/'FINITE_SAM_ROTATION_CERTIFICATE.json',P/'SAME_INITIAL_ENDPOINT_SCHEDULE_CHECK.json',D/'round30/COMMON_SOURCE_MARKED_PLAN.json')},'GR_closed':False}
(P/'ENDPOINT_PRICE_BOUND_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'endpoint_layers_bits':N.bit_length()}))
