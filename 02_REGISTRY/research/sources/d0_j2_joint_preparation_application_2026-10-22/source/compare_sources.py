#!/usr/bin/env python3
"""Reproduce the actual same-carrier 42-covector at the unpadded center.

Run from repository root with Python and mpmath 1.3.0:
  python3 <this file> --repo .
Default verifies the immutable adjacent numerical receipt. --write-result
authors it explicitly. This diagnostic is not the interval endpoint proof.
The original source/collar/center are imported at their actual repository
paths and checked at their immutable Git blob SHA before any computation.
"""
from pathlib import Path
import argparse,hashlib,json,sys

HERE=Path(__file__).resolve().parent
PINS={'certified_model.py':'6d5b41ce11a941fde95e722e708ebb02d689985c',
      'inputs.py':'2c12d84fb3454dbf3cda6d71852d0cd4e57e1f65',
      'center_new.json':'6b520fbd6218444601d90d7e30b738f8c828bd22'}

def run(repo):
    base=repo/'02_REGISTRY/research/sources'
    original=base/'d0_full42_interval_banach_2026-10-22'
    centerfile=base/'d0_original_unpadded42_2026-10-22/center_new.json'
    for name,pin in PINS.items():
        path=centerfile if name=='center_new.json' else original/name
        data=path.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if blob!=pin:raise RuntimeError('Original input blob changed: '+str(path))
    sys.path.insert(0,str(original))
    from mpmath import mp
    from certified_model import CQ
    mp.dps=100
    m=CQ(mp)
    y=mp.matrix([mp.mpf(v) for v in json.loads(centerfile.read_text())['z42']])
    m.price(y);r=list(m.last_clicks)
    dr=[[],[]];step=mp.mpf('1e-45')
    for k in range(42):
        w=y.copy();w[k]+=mp.j*step;m.price(w)
        for j in range(2):dr[j].append(mp.im(m.last_clicks[j])/step)
    hp=lambda x:mp.log((1-x)/x)/m.lp
    gain=m.norm*(hp(m.r0)-1)*(1-m.r0)/528
    g0=[sum(m.norm*(hp(r[j])-1)*dr[j][k] for j in range(2)) for k in range(42)]
    gj=[528*sum(dr[j][k]/(1-r[j]) for j in range(2)) for k in range(42)]
    res=[gain*gj[k]-g0[k] for k in range(42)]
    return {'status':'HIGH_PRECISION_SAME_CARRIER_ALL42_COVECTOR_COMPUTED',
        'input_commit':'af6e7eb8952564d86ddbfe910eb5f41d4a1b4e4b',
        'input_blobs':PINS,
        'literal_feedback':'-528 sum_j [log(1-zeta*A_j)+log(1-zeta*B_j)]',
        'exact_factorization':'(1-zeta*A_j)(1-zeta*B_j)=1-r_j',
        'r':[mp.nstr(mp.re(t),80) for t in r],
        'rref':mp.nstr(m.r0,80),'comparison_gain':mp.nstr(gain,80),
        'dr':[[mp.nstr(v,80) for v in row] for row in dr],
        'original_unpadded_gradient':[mp.nstr(mp.re(v),80) for v in g0],
        'raw_J2_gradient':[mp.nstr(mp.re(v),80) for v in gj],
        'normalized_additional_residual':[mp.nstr(mp.re(v),80) for v in res],
        'raw_J2_gradient_inf':mp.nstr(max(abs(v) for v in gj),80),
        'normalized_additional_residual_inf':mp.nstr(max(abs(v) for v in res),80),
        'original_unpadded_gradient_inf':mp.nstr(max(abs(v) for v in g0),80),
        'max_component_zero_based':max(range(42),key=lambda k:abs(res[k])),
        'precision_decimal_digits':mp.dps,'complex_step':str(step),
        'scope':'Addressed original J2 component only; total selected H+J+R is not assigned by this computation',
        'physical_Book03_selected':False,'GR_closed':False}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,default=HERE.parents[4])
    parser.add_argument('--write-result',action='store_true')
    args=parser.parse_args()
    result=run(args.repo.resolve())
    encoded=json.dumps(result,indent=2)+'\n'
    receipt=HERE/'J2_SOURCE_AT_UNPADDED.json'
    if args.write_result:receipt.write_text(encoded)
    else:
        expected=json.loads(receipt.read_text())
        if result!=expected:raise RuntimeError('Computed full42 covector differs from frozen receipt')
    summary={k:result[k] for k in ('status','raw_J2_gradient_inf',
        'normalized_additional_residual_inf','original_unpadded_gradient_inf',
        'max_component_zero_based','physical_Book03_selected','GR_closed')}
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
