#!/usr/bin/env python3
"""Concrete powers for the native Choi address/Bell prefix."""
from pathlib import Path
import hashlib,importlib.util,json,sys
import mpmath as mp
import choi_prefix as compiler
P=Path(__file__).resolve().parent;D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
def load(name,path):
    sp=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(sp);sys.modules[name]=obj;sp.loader.exec_module(obj);return obj
b37=load('a19_b37',B/'round37/build_car_ustar.py')
ivmod=load('a19_dyadic',D/'round18/material_targets.py')
power=load('a19_integer_power',D/'round18/interval_rotation.py')
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()

def enclosure_record(k,multiple,target,bits):
    S,c,s=power.rotation_intervals(multiple*k,bits);tc,ts=target
    error=max(abs(c[0]-tc[1]),abs(c[1]-tc[0]))+max(abs(s[0]-ts[1]),abs(s[1]-ts[0]))
    return {'multiple':multiple,'native_cos_hex':[hex(x) for x in c],'native_sin_hex':[hex(x) for x in s],
            'target_cos_hex':[hex(x) for x in tc],'target_sin_hex':[hex(x) for x in ts],
            'error_L1_numerator_hex':hex(error),'denominator_power_of_two':bits},error

def main():
    bits=4096;precision=16640;iv=ivmod.Dyadic(precision);R=iv.rational;S=iv.scale
    k,proposal=b37.propose_target(bits+4,2,lambda:mp.mpf(1)/8)
    halfroot=iv.sqrt(R(1,2));targets={4:(halfroot,halfroot),8:(R(0),R(1)),16:(R(-1),R(0))}
    enclosures={};errors={}
    for mult,target in targets.items():
        enclosures[str(mult)],errors[mult]=enclosure_record(k,mult,target,precision)
        print('certified Choi common-power multiplier',mult,flush=True)
    assert errors[4]+errors[16]<=2**(precision-bits)
    assert errors[8]+errors[16]<=2**(precision-bits)
    ka,pa=b37.propose_target(bits+4,1,lambda:mp.atan(1/mp.sqrt(2048))/(2*mp.pi))
    ac=iv.sqrt(R(2048,2049));ass=iv.sqrt(R(1,2049));ae,erra=enclosure_record(ka,2,(ac,ass),precision)
    assert erra<=2**(precision-bits)
    bound=erra+16*(errors[4]+errors[16])+5*(errors[8]+errors[16])
    assert bound<2**(precision-4091)
    cert={'status':'CERTIFIED_ACTUAL_CONTROLLED_CHOI_ADDRESS_BELL_PREFIX',
          'precision_bits':precision,'boolean_common_power':{'k':str(k),'k_bits':k.bit_length(),'proposal_not_proof':proposal,'enclosures':enclosures},
          'address_power':{'k':str(ka),'k_bits':ka.bit_length(),'proposal_not_proof':pa,'enclosure':ae},
          'uniform_H_and_X_error_le':'2^-4096','uniform_address_error_le':'2^-4096',
          'uniform_full_prefix_error_lt':'2^-4091','prefix_error_L1_numerator_hex':hex(bound),
          'control_disabled_exact_identity':True,'control_enabled_equals_actual_uncontrolled_operator':True,
          'full_Julia_SELECT_compiled':False,'full_Omega_preparation_compiled':False,
          'source_sha256':h(Path(__file__)),'input_sha256':{str(f):h(f) for f in [P/'choi_prefix.py',B/'round37/build_car_ustar.py',D/'round18/material_targets.py',D/'round18/interval_rotation.py',D/'round14/native_boolean.py']},
          'physical_C_closed':False,'GR_closed':False}
    (P/'CHOI_PREFIX_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
    result={'certificate_sha256':h(P/'CHOI_PREFIX_CERTIFICATE.json'),'layout':compiler.layout(),
            'logical_schedule':list(compiler.instructions(compiler.layout(),True)),
            'actual_native_resources':compiler.inventory(cert),'target_address_support':[0,2048],
            'target_address_amplitude':'1/sqrt(2049)','Bell_pairs':5,'private_clean_work':0,
            'all_SAM_and_oldRIGHT_are_spectators':True,'exact_h0_identity':True,
            'remaining_operator':'branch/SAM/address-controlled full Julia SELECT on last five Choi wires',
            'full_Omega_preparation_compiled':False,'physical_C_closed':False,'GR_closed':False}
    (P/'CHOI_PREFIX_PLAN.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':cert['status'],'common_k_bits':k.bit_length(),'address_k_bits':ka.bit_length(),'prefix_error_lt':'2^-4091'}))

if __name__=='__main__':main()
