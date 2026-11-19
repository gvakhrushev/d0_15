import sys,json,math,hashlib
from pathlib import Path
from flint import arb,acb,arb_mat,ctx,fmpq
import numpy as np
from fractions import Fraction
ctx.prec=160
src=Path(__file__).with_name('COLLAR_HESSIAN_ARB.json')
j=json.loads(src.read_text())
def parse(v):
 if ' + ' in v:
  re,im=v.split(' + ');return acb(arb(re),arb(im[:-1]))
 return acb(arb(v))
K=[[[parse(x) for x in row] for row in mat] for mat in j['K9']]
sq=arb(2).sqrt()
T=[acb(1),acb(sq/2,sq/2),acb(0,1),acb(-sq/2,sq/2),acb(-1),acb(-sq/2,-sq/2),acb(0,-1),acb(sq/2,-sq/2)]
cache={}
def H(d,i,j):
 key=(d%8,i,j)
 if key not in cache:
  out=K[0][i][j]+((-1)**d)*K[4][i][j]
  for q in range(1,4):
   phase=T[q*d%8];out+=phase*K[q][i][j]+phase.conjugate()*K[q][i][j].conjugate()
  assert out.imag.contains(0)
  cache[key]=out.real/8
 return cache[key]
width=7;collar=7
positions=[t for t in range(width) for c in range(9)]+[collar]
components=list(range(9))*width+[5];n=len(positions)
A=arb_mat([[H(positions[i]-positions[k],components[i],components[k]) for k in range(n)] for i in range(n)])
b=arb_mat([[H(positions[i]-collar,components[i],2)] for i in range(n)])
An=np.array([[float(A[i,k].mid()) for k in range(n)] for i in range(n)]);bn=np.array([float(b[i,0].mid()) for i in range(n)])
eig=np.linalg.eigvalsh((An+An.T)/2)
Rn=np.linalg.inv(An)
print(json.dumps({'n':n,'min_abs_eig':float(np.min(np.abs(eig))),'max_abs_eig':float(np.max(np.abs(eig))),'condition2':float(np.linalg.cond(An)),'symmetry_err':float(np.max(np.abs(An-An.T))),'float_response':np.linalg.solve(An,-bn).tolist()},indent=2),flush=True)
rs=[[format(Rn[i,k],'.17g') for k in range(n)] for i in range(n)]
R=arb_mat([[arb(fmpq(Fraction(v).numerator,Fraction(v).denominator)) for v in row] for row in rs])
E=-(R*A)
for i in range(n):E[i,i]+=1
rowbounds=[sum(abs(E[i,k]) for k in range(n)) for i in range(n)]
# Every row is certified independently, avoiding max comparisons on overlapping balls.
upper=max(float(v.upper()) for v in rowbounds)
print('Neumann row upper',upper,flush=True)
assert all(v<arb(1) for v in rowbounds)
assert all(v<arb(3)/1000 for v in rowbounds)
xnum=np.linalg.solve(An,-bn)
xs=[format(v,'.17g') for v in xnum]
x0=arb_mat([[arb(fmpq(Fraction(v).numerator,Fraction(v).denominator))] for v in xs])
residual=R*(-b-A*x0)
rbound=max(float(abs(residual[i,0]).upper()) for i in range(n))
# Choose an explicit rational upperbound, then verify it for EVERY row.
rcount=math.ceil(rbound*10**9)+1
rb=arb(rcount)/10**9
assert all(abs(residual[i,0])<rb for i in range(n))
err=rb/(1-arb(3)/1000)
response=arb_mat([[x0[i,0]+arb(0,err)] for i in range(n)])
assert all(not response[(width-1)*9+c,0].contains(0) for c in [6,7,8])
assert err<arb(1)/100
windows=[('-1.24','-1.21'),('-.21','-.18'),('.19','.22')]
for c,(lo,hi) in zip([6,7,8],windows):
 v=response[(width-1)*9+c,0]
 assert v>arb(lo) and v<arb(hi)
rrows=[sum(abs(R[i,k]) for k in range(n)) for i in range(n)]
rnorm=math.ceil(max(float(v.upper()) for v in rrows))+1
assert all(v<rnorm for v in rrows)
invnorm=arb(rnorm)/(1-arb(3)/1000)
print('responseerr',str(err),'residual',rbound,flush=True)
out={'status':'RIGOROUS_W7_BULK_COLLAR_PASS','source':src.name,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'root_box':j['root_box'],'precision_bits':ctx.prec,'source_certificate_status':j['status'],'L':8,'interior_slices':list(range(7)),'fixed_collar_slice':7,'unknowns':n,'positions':positions,'components':components,'min_abs_mid_eig':float(np.min(np.abs(eig))),'condition2_mid':float(np.linalg.cond(An)),'rational_preconditioner':rs,'neumann_row_bounds':[str(v) for v in rowbounds],'neumann_strict_upper':'3/1000','response_candidate_decimal':xs,'response_preconditioned_residual_bounds':[str(abs(residual[i,0])) for i in range(n)],'response_residual_rational_upper':f'{rcount}/1000000000','response_error_inf':str(err),'response_error_rational_upper':'1/100','inverse_norm_inf_upper':str(invnorm),'rational_preconditioner_norm_upper':rnorm,'curvature_response_windows':windows,'response':[str(response[i,0]) for i in range(n)],'boundary_adjacent_transverse_response':[str(response[(width-1)*9+c,0]) for c in [6,7,8]],'b':[str(b[i,0]) for i in range(n)]}
if '--output' in sys.argv:
 Path(sys.argv[sys.argv.index('--output')+1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','min_abs_mid_eig','condition2_mid','boundary_adjacent_transverse_response']},indent=2),flush=True)
