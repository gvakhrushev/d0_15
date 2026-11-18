#!/usr/bin/env python3
"""Level-nine adapter phase correction; level-eight power is not reused."""
from pathlib import Path
from hashlib import sha256
import json,sys
sys.dont_write_bytecode=True
import two_bit_source_targets as t
from source_angle_certifier import Certifier
P=Path(__file__).resolve().parent

def target(iv,levels=9):
    one=iv.rational(1);zero=iv.rational(0);two=iv.rational(2)
    h=iv.div(iv.sqrt(iv.rational(3)),two)
    eps=iv.div(iv.sub(one,iv.sqrt(iv.rational(1,65568))),two)
    assert 0<eps[0]<=eps[1]<iv.scale//2
    z=(one,zero);e=eps
    for _ in range(levels):
        g=(iv.div(iv.sub(e,one),two),iv.mul(h,iv.add(one,e)))
        z=(iv.sub(iv.mul(z[0],g[0]),iv.mul(z[1],g[1])),
           iv.add(iv.mul(z[0],g[1]),iv.mul(z[1],g[0])))
        e=iv.pow(e,3)
    norm=iv.sqrt(iv.add(iv.pow(z[0],2),iv.pow(z[1],2)))
    assert norm[0]>0
    return iv.div(z[0],norm),iv.neg(iv.div(z[1],norm))

def main():
    cert=Certifier(0,bits=4096,precision=9216)
    c,s=target(cert.iv);aid=cert.certify(c,s)
    out={'status':'CERTIFIED_LEVEL_NINE_NATIVE_PHASE_CORRECTION',**cert.metadata(),
      'levels':9,'correction_l':cert.records[aid]['k'],
      'target_cos_hex':[hex(int(x)) for x in c],'target_sin_hex':[hex(int(x)) for x in s],
      'target_formula':'conj(product(j=0..8, t^2+t*epsilon_j))/abs(product), t=exp(i*pi/3)',
      'epsilon_0':'(1-1/sqrt(65568))/2','recurrence':'epsilon_next=epsilon^3',
      'ideal_failure_lt':'2^-19683','ideal_phase_corrected_vector_error_lt':'2^-9841',
      'failure_bound_proof':'epsilon_0<1/2; epsilon_9=epsilon_0^(3^9); norm_error_squared<=2*epsilon_9',
      'source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),P/'source_angle_certifier.py',P/'two_bit_source_targets.py']},
      'physical_C_closed':False,'GR_closed':False}
    (P/'LEVEL9_CORRECTION_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'levels':9,'correction_error_le':'2^-4096'}))

if __name__=='__main__':main()
