#!/usr/bin/env python3
"""Reusable short positive-power grid for G^(2^K), rigorous B80 interval."""
from pathlib import Path
from hashlib import sha256
from math import gcd
import json,argparse
P=Path(__file__).resolve().parent;B=P.parent
source=B/'round80/UNIFORM_GOLDEN_GRID_CERTIFICATE.json';raw=source.read_bytes()
assert sha256(raw).hexdigest()=='3a73d409941cb916b36df5a2046e36499cc094fa338912a2c662a4c2a5d14ed9'
j=json.loads(raw);prec=j['precision_bits'];S=1<<prec

def build(K,error_bits=3460,min_q_bits=3476):
 assert type(K) is int and 0<=K<=10000 and 0<error_bits<min_q_bits-5
 lo,hi=[int(v,16)<<K for v in j['gamma_interval_hex']]
 a,b=lo+hi,2*S;p0,p1=0,1;q0,q1=1,0
 while b:
  quot,a,b=a//b,b,a%b
  pn=quot*p1+p0;qn=quot*q1+q0
  p0,p1=p1,pn;q0,q1=q1,qn
  if qn.bit_length()>=min_q_bits:
   E=max(abs(qn*lo-pn*S),abs(qn*hi-pn*S))
   if gcd(pn,qn)==1 and qn*E<S and 16*(1<<error_bits)<qn:break
 else:raise ValueError('B80 interval too coarse for these parameters')
 return {'status':'PASS_SHORT_UNIFORM_WALSH_GRID','precision_bits':prec,'walsh_common_controls':K,'numerator_hex':hex(pn),'denominator_hex':hex(qn),'denominator_bits':qn.bit_length(),'error_numerator_hex':hex(E),'original_grid_sha256':sha256(raw).hexdigest(),'actual_orbit':f'G^(2^{K}*k), 1<=k<=q','uniform_rotation_error_lt':f'2^-{error_bits}','proof':'B80 gamma interval, exact continued fraction on midpoint, gcd and q*max|q gammaK-pn|<1, 16/q<2^-error_bits','physical_C_closed':False,'GR_closed':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--controls',type=int,default=29);ap.add_argument('--error-bits',type=int,default=3460);ap.add_argument('--min-q-bits',type=int,default=3476);args=ap.parse_args()
 out=build(args.controls,args.error_bits,args.min_q_bits)
 path=P/('SHORT_GRID_CERTIFICATE.json' if args.controls==29 and args.error_bits==3460 and args.min_q_bits==3476 else f'SHORT_GRID_K{args.controls}_E{args.error_bits}.json')
 path.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['walsh_common_controls'],out['denominator_bits'])
