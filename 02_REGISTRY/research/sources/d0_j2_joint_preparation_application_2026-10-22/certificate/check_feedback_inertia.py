#!/usr/bin/env python3
"""Rigorous full saddle inertia from the saved outward interval Hessian.

Q is only a rational proposal. ||I-Q^T Q||<1 proves its invertibility.
The true symmetric congruence Q^T H Q is strictly diagonally dominant with
signed diagonal. Turning off its off-diagonal part cannot cross zero;
Sylvester's law gives the exact inertia of H. All bounds are outward iv.
"""
from decimal import Decimal,getcontext
from pathlib import Path
import argparse,hashlib,json,sys
sys.dont_write_bytecode=True
from mpmath import iv
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--audit',action='store_true',help='Read-only audit (also the default)')
parser.add_argument('--recompute',action='store_true',help='Explicitly write a new inertia receipt')
parser.add_argument('--output',type=Path,help='New receipt path required with --recompute')
opts=parser.parse_args()
iv.dps=100;getcontext().prec=140
receipt=json.loads((HERE/'J2_INTERVAL_RESULT.json').read_text())
data=json.loads((HERE/'J2_INTERVAL_HESSIAN_ENDPOINTS.json').read_text())
N=42
def require(condition, message="certificate predicate failed"):
    if not condition:
        raise AssertionError(message)
def recover(v):
    out=iv.mpf(0);out._mpi_=tuple(tuple(t) for t in v);return out
H=iv.matrix([[recover(x) for x in row] for row in data])
qfile=HERE/'J2_RATIONAL_CONGRUENCE_FRAME.json'
require(qfile.is_file(),'The published exact rational congruence frame is required')
qr=json.loads(qfile.read_text())['entries']
require(len(qr) == N and all((len(row) == N for row in qr)))
Q=iv.matrix([[iv.mpf(x) for x in row] for row in qr])
I=iv.eye(N);defect=Q.T*Q-I
qdef=max(sum(abs(defect[i,j]).b for j in range(N)) for i in range(N))
require(qdef < iv.mpf('1e-12'))
B=Q.T*H*Q
rowmargin=[];inertia=[0,0,0]
for i in range(N):
    off=sum(abs(B[i,j]).b for j in range(N) if j!=i)
    margin=abs(B[i,i]).a-off
    require(margin > iv.mpf('.04'), (i, margin))
    rowmargin.append(margin)
    if B[i,i].b<0:inertia[0]+=1
    elif B[i,i].a>0:inertia[2]+=1
    else:raise AssertionError(('zero diagonal',i))
require(inertia == [16, 0, 26], inertia)
Qinf=max(sum(abs(Decimal(x)) for x in row) for row in qr)
QTinf=max(sum(abs(Decimal(qr[i][j])) for i in range(N)) for j in range(N))
congruence_shift=Qinf*QTinf*Decimal(receipt['Hessian_Lipschitz_times_radius'])
ballmargin=min(rowmargin)-iv.mpf(str(congruence_shift))
require(ballmargin > iv.mpf('.04'))
out={
 'status':'PASS_RIGOROUS_FULL_SADDLE_INERTIA_16_0_26_ON_ENDPOINT_BALL',
 'interval_Hessian_sha256':hashlib.sha256((HERE/'J2_INTERVAL_HESSIAN_ENDPOINTS.json').read_bytes()).hexdigest(),
 'rational_frame_invertibility_defect_inf':str(qdef),
 'congruence_minimum_signed_diagonal_dominance':str(min(rowmargin)),
 'congruence_variation_bound_on_root_ball':str(congruence_shift),
 'minimum_dominance_on_root_ball':str(ballmargin),
 'normalized_endpoint_inertia_negative_zero_positive':inertia,
 'literal_J2_inertia_negative_zero_positive':[26,0,16],
 'reason_for_inertia_reversal':'comparison gain aJ<0; physical J2 has opposite signs',
 'exact_root_ball_inf':receipt['exact_root_ball_inf'],
 'rational_frame':qr,
 'GR_closed':False
}
require(not(opts.audit and opts.recompute),'Choose audit or recompute')
if opts.recompute:
    require(opts.output is not None,'--recompute requires --output')
    require(opts.output.resolve()!=(HERE/'J2_INERTIA_RESULT.json').resolve(),'Frozen inertia receipt may not be overwritten')
    opts.output.write_text(json.dumps(out,indent=2)+'\n')
else:
    require(opts.output is None,'Audit is read-only and accepts no output path')
    frozen=json.loads((HERE/'J2_INERTIA_RESULT.json').read_text())
    require(frozen['interval_Hessian_sha256'] == out['interval_Hessian_sha256'])
    require(frozen['normalized_endpoint_inertia_negative_zero_positive'] == inertia)
print(json.dumps({k:v for k,v in out.items() if k!='rational_frame'},indent=2))
