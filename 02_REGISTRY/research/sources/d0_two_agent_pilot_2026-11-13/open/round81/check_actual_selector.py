#!/usr/bin/env python3
"""Independent high-precision check of actual A41 selector on ±π/8."""
from pathlib import Path
from hashlib import sha256
import importlib.util,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
OPEN=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round41'))
import exact_target as e, sam_only_compiler as c
path=OPEN/'round75/verify_post_angles_independent.py'
spec=importlib.util.spec_from_file_location('b81_independent_rectangles',path);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
target,_=b.targets();tc,ts=target['pi8'];rows={}
for sign in (1,-1):
    # Input star angle ±π/4; m=2 divides it to ±π/8.
    x=e.root(e.expr(1)/2); cc,ss=c.divided_angle(x,sign*x,2)
    k=c.select_positive_power(cc,ss)
    scale,rc,rs=b.rectangle_rotation(k,b.BITS)
    assert scale==1<<61000
    if sign<0:st=(-ts[1],-ts[0])
    else:st=ts
    dc=max(abs(u-v) for u in rc for v in tc)
    ds=max(abs(u-v) for u in rs for v in st);err=dc+ds
    assert err*(1<<20000)<scale
    rows['plus' if sign>0 else 'minus']={'power_hex':hex(k),'power_bits':k.bit_length(),
         'L1_error_numerator_hex':hex(err),'denominator_pow2':61000,
         'operator_error_strict_lt':'2^-20000'}
    print('selector verified',sign,'power bits',k.bit_length(),flush=True)
out={'status':'PASS_A41_SELECTOR_TWO_SIGNS_INDEPENDENT_61000_BIT_RECTANGLES',
     'selector_sha256':sha256((D/'round41/sam_only_compiler.py').read_bytes()).hexdigest(),
     'exact_target_sha256':sha256((D/'round41/exact_target.py').read_bytes()).hexdigest(),
     'independent_rectangle_sha256':sha256(path.read_bytes()).hexdigest(),
     'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
     'samples':rows,'actual_production_target_evaluated':False,'physical_C_closed':False,'GR_closed':False}
(P/'B81_SELECTOR_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
