#!/usr/bin/env python3
"""Certify the actual K7 pi/2 power used by every original Fourier rotation."""
from pathlib import Path
import hashlib,importlib.util,json,sys
import mpmath as mp
P=Path(__file__).resolve().parent;D=P.parent;sys.path.insert(0,str(D/'round20'))
import coframe_targets as t
s=importlib.util.spec_from_file_location('a23_power',D/'round20/certify_coframe_angles.py');power=importlib.util.module_from_spec(s);sys.modules[s.name]=power;s.loader.exec_module(power)
bits=3264;precision=7168;K=7;iv=t.Dyadic(precision);c=t.constants(iv);S=iv.scale
with mp.workprec(3*bits+256):
    pn,qn,steps=power.candidate_grid(bits+4,K);inverse=pow(pn,-1,qn);grid=int(mp.nint(mp.mpf(qn)/4))%qn;k=(grid*inverse)%qn;assert k>0
    nc,ns=power.native_power((1<<K)*k,iv,c);tc,ts=iv.rational(0),iv.rational(1)
    err=max(abs(nc[0]-tc[1]),abs(nc[1]-tc[0]))+max(abs(ns[0]-ts[1]),abs(ns[1]-ts[0]));assert err<=S>>bits
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out={'status':'CERTIFIED_ACTUAL_K7_QUARTER_TURN','controls':K,'k':str(k),'k_binary_length':k.bit_length(),'native_multiplier':1<<K,
     'native_cos_hex':[hex(z) for z in nc],'native_sin_hex':[hex(z) for z in ns],'target_cos':'0','target_sin':'1',
     'error_numerator_hex':hex(err),'denominator_power_of_two':precision,'uniform_operator_error_le':'2^-3264',
     'coefficient_a_bound':'||R(a*128*k*theta)-R(a*pi/2)||<=a*2^-3264, a=1,2,3',
     'candidate_grid_not_proof':{'numerator':str(pn),'denominator':str(qn),'steps':steps},'source_sha256':h(Path(__file__)),
     'input_sha256':{str(p):h(p) for p in [D/'round20/certify_coframe_angles.py',D/'round20/coframe_targets.py',D/'round18/material_targets.py',D/'round14/native_boolean.py']},
     'full_giant_word_executed':False,'physical_C_closed':False,'GR_closed':False}
(P/'FOURIER_PHASE_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'k_bits':k.bit_length()}))
