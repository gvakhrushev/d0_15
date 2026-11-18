#!/usr/bin/env python3
"""Recompute saved powers with independent owner rectangular intervals."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import importlib.util,json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');owner=D/'round14/certify_boolean_angle.py';sp=importlib.util.spec_from_file_location('b63_direct_owner',owner);mod=importlib.util.module_from_spec(sp);sys.modules[sp.name]=mod;sp.loader.exec_module(mod);cert=json.loads((P/'SUFFICIENT_ENDPOINT_G_CERTIFICATE.json').read_text());assert cert['status']=='PASS_SUFFICIENT_POSITIVE_ENDPOINT_G_POWERS'
for p,h in cert['source_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h
n=1618;bits=4852;precision=4*bits+256;S=1<<precision
def trig(start,cosine):
 t=F(1,2**n);term=start;acc=F(0);j=0
 while True:
  acc+=term;term=-term*t*t/((2*j+1)*(2*j+2) if cosine else (2*j+2)*(2*j+3))
  if abs(term)<F(1,2**(bits+80)):
   lo,hi=sorted((acc,acc+term));return lo.numerator*S//lo.denominator,-((-hi.numerator*S)//hi.denominator)
  j+=1
co=trig(F(1),True);si=trig(F(1,2**n),False);out={}
for name,sign in (('plus',1),('minus',-1)):
 k=int(cert['rotations'][name]['power_hex'],16);print('independent owner interval',name,flush=True);scale,c,s=mod.phase._rotation_intervals(k,precision);assert scale==S;target=si if sign==1 else (-si[1],-si[0]);e=max(abs(c[0]-co[1]),abs(c[1]-co[0]))+max(abs(s[0]-target[1]),abs(s[1]-target[0]));assert e*(1<<bits)<S
 out[name]={'power_bits':k.bit_length(),'operator_error_strict_lt_pow2':precision-e.bit_length()}
result={'status':'PASS_INDEPENDENT_RECTANGULAR_ENDPOINT_G_CERTIFICATE','precision_bits':precision,'rotations':out,'both_errors_lt':'2^-4852','candidate_or_integer_ball_result_not_trusted':True,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in (owner,Path(mod.phase.__file__),P/'SUFFICIENT_ENDPOINT_G_CERTIFICATE.json')},'GR_closed':False}
(P/'SUFFICIENT_G_INDEPENDENT_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
