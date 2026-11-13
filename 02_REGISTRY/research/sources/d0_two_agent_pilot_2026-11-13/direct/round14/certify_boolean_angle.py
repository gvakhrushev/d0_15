#!/usr/bin/env python3
"""Find a candidate numerically, then CERTIFY only by outward integer powers.

The continued-fraction candidate finder is not trusted evidence. Final cosine
and sine enclosures consume the owning native phase compiler and exact roots.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import hashlib,importlib.util,json,sys
import mpmath as mp
P=Path(__file__).resolve().parent;ROOT=P.parents[5]
OWNER=ROOT/'02_REGISTRY/research/sources/d0_native_readiness_amplification_2026-10-24/native_phase.py'
spec=importlib.util.spec_from_file_location('a14_native_phase',OWNER)
phase=importlib.util.module_from_spec(spec);sys.modules[spec.name]=phase;spec.loader.exec_module(phase)


def candidate(bits):
    # k*theta approaches pi/8 modulo 2pi; hence 2k approaches pi/4,
    # 4k pi/2, and 8k pi with one shared exact integer.
    with mp.workprec(3*bits+256):
        p=(mp.sqrt(5)-1)/2;gamma=mp.acos(mp.sqrt(p))/(2*mp.pi)
        x=gamma;p0,p1=0,1;q0,q1=1,0;steps=0
        while True:
            a=int(mp.floor(x));pn=a*p1+p0;qn=a*q1+q0;steps+=1
            if qn.bit_length()>=bits+16:
                j=(qn+8)//16;k=(j*pow(pn,-1,qn))%qn
                assert k>0
                return k,{'steps':steps,'convergent_numerator':str(pn),
                          'convergent_denominator':str(qn),'target_fraction':'1/16'}
            p0,p1=p1,pn;q0,q1=q1,qn;x=1/(x-a)


def certify(k,bits,precision):
    scale=1<<precision
    results={};bounds={}
    sqrt2half=isqrt((scale*scale)//2)
    for multiple in (2,4,8):
        scale0,c,s=phase._rotation_intervals(multiple*k,precision)
        assert scale0==scale
        if multiple==2:
            target=(sqrt2half,sqrt2half+1)
            error=max(abs(c[0]-target[1]),abs(c[1]-target[0]))+max(abs(s[0]-target[1]),abs(s[1]-target[0]))
        elif multiple==4:
            error=max(abs(c[0]),abs(c[1]))+max(abs(s[0]-scale),abs(s[1]-scale))
        else:
            error=max(abs(c[0]+scale),abs(c[1]+scale))+max(abs(s[0]),abs(s[1]))
        bounds[multiple]=F(error,scale)
        results[str(multiple)]={'cosine_endpoints_hex':[hex(v) for v in c],
                                'sine_endpoints_hex':[hex(v) for v in s],
                                'denominator_power_of_two':precision,
                                'operator_error_L1_upper':str(bounds[multiple])}
    combined=bounds[4]+bounds[8]
    maximum=max(bounds[2],bounds[4],combined)
    assert maximum<=F(1,2**bits),'candidate not certified at required tolerance'
    return {'rotation_enclosures':results,'H_error_upper':str(bounds[2]),'X_error_upper':str(bounds[4]),
            'CCX_error_upper':str(combined),'every_macro_error_upper':f'1/{2**bits}',
            'certified_error_bits':bits,'precision_bits':precision}


def main(bits=4096):
    k,proposal=candidate(bits)
    certificate=certify(k,bits,4*bits+256)
    result={'status':'CERTIFIED_NATIVE_BOOLEAN_COMMON_POWER','k':str(k),'k_binary_length':k.bit_length(),
            'candidate_proposal_not_a_proof':proposal,'certificate':certificate,
            'native_phase_owner_sha256':hashlib.sha256(OWNER.read_bytes()).hexdigest(),
            'uses_float_for_certificate':False,'uses_pi_in_executed_word':False,
            'new_physical_selector':False,'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'NATIVE_BOOLEAN_ANGLE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'k_binary_length':k.bit_length(),'error_bits':bits,
                      'precision_bits':certificate['precision_bits'],'candidate_steps':proposal['steps']}),flush=True)


if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 4096)
