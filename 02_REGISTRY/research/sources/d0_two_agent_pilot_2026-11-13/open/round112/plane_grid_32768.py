#!/usr/bin/env python3
"""Precision input for existing A42 CODE-only plane_blocks/plane_upper.

Public API: uniform_grid(), Macros().ks['pi8'], Macros().x(q,helper),
plane_power(sign,m=5376,step_bits=6000). No SOURCE/post is altered.
"""
from pathlib import Path
from hashlib import sha256
from math import gcd
import importlib.util,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
CERT=P/'GRID_32768_CERTIFICATE.json'
CERT_SHA='110b849fc77d04725786a0cb96ac9cc3276eae72f9a5492ea5ff23763a88e54d'
sys.path.insert(0,str(D/'round38'));import gcx_post_macros as native
sys.path.insert(0,str(O/'round80/.deps'));import gmpy2

def uniform_grid():
    raw=CERT.read_bytes()
    if sha256(raw).hexdigest()!=CERT_SHA:raise ValueError('grid certificate hash mismatch')
    cert=json.loads(raw)
    assert cert['status']=='PASS_32768_POSITIVE_G_GRID_AND_PI8'
    for path,h in cert['input_sha256'].items():assert sha256(Path(path).read_bytes()).hexdigest()==h
    pn=int(cert['numerator_hex'],16);q=int(cert['denominator_hex'],16)
    S=1<<cert['precision_bits'];lo,hi=[int(x,16) for x in cert['gamma_interval_hex']]
    E=max(abs(q*lo-pn*S),abs(q*hi-pn*S))
    assert E==int(cert['error_numerator_hex'],16) and S-q*E==int(cert['strict_margin_hex'],16)>0
    assert gcd(pn,q)==1 and 16*(1<<32768)<q and 0<lo<=hi<S//4
    k8=int(cert['pi8_exponent_hex'],16);j8=int(cert['pi8_cell_hex'],16)
    assert abs(16*j8-q)<=8 and 1<=k8<=q and (k8*pn-j8)%q==0
    return pn,q,cert

class Macros:
    """Only A42 plane's x/Z/pi8 template; no stale A38 20000-bit powers."""
    power=native.Macros.power
    pi8=native.Macros.pi8
    z=native.Macros.z
    x=native.Macros.x
    def __init__(self):
        _,_,cert=uniform_grid()
        self.ks={'pi8':int(cert['pi8_exponent_hex'],16)}

def _select(sign,m,step_bits):
    if type(sign) is not int or sign not in (-1,1):raise ValueError('sign must be -1 or 1')
    if type(m) is not int or not 3<=m<=5376:raise ValueError('3 <= m <= 5376')
    if type(step_bits) is not int or not 1<=step_bits<=32768:raise ValueError('invalid dyadic step')
    pn,q,cert=uniform_grid();bits=cert['precision_bits'];S=gmpy2.mpz(1)<<bits
    spec=importlib.util.spec_from_file_location('b112_select_b80',O/'round80/certify_uniform_golden_grid.py')
    b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.BITS=bits;b.S=S
    # Target physical plane angle is 2*atan(sign*2^(-step_bits-1));
    # A42 Walsh star divides this by L=2^(m-1), hence turns are
    # sign*atan(2^(-step_bits-1))/(pi*L).
    angle,terms=b.atan_enclosure(b.rational(1,1<<(step_bits+1)))
    pi=tuple(gmpy2.mpz(int(x,16)) for x in cert['pi_interval_hex'])
    low,high=b.div(angle,b.scale(pi,1<<(m-1)))
    if sign<0:low,high=-high,-low
    if 2*q*(high-low)>S:raise ArithmeticError('certified target interval needs more bits')
    j=int((q*(low+high)+S)//(2*S))
    k=(j*pow(pn,-1,q))%q or q
    assert 1<=k<=q
    return {'k':k,'cell':j,'interval_low':int(low),'interval_high':int(high),
            'precision_bits':bits,'series_terms':terms}

def plane_power(sign,m=5376,step_bits=6000):
    """Select actual positive G exponent for signed Cayley plane target."""
    return _select(sign,m,step_bits)['k']
