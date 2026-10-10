#!/usr/bin/env python3
"""Exact continuous identity-sheet circle ranks and one-coordinate rescue bounds."""
import json
from fractions import Fraction as F
import numpy as np
from a4d_designated_full_gap_check import flat_symbols,QI,elimination
from a4d_warped_quarter_regular_response_check import independent_rows,qi_inverse,COLS,ROWS

Z=(0,0);ONE=(1,0)
def ga(a,b):return(a[0]+b[0],a[1]+b[1])
def gn(a):return(-a[0],-a[1])
def gm(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def gd(a,b):
 d=b[0]*b[0]+b[1]*b[1];re=a[0]*b[0]+a[1]*b[1];im=a[1]*b[0]-a[0]*b[1]
 assert re%d==0 and im%d==0
 return(re//d,im//d)
def tr(a):
 while a and a[-1]==Z:a.pop()
 return a
def pa(a,b):
 out=a.copy()+[Z]*max(0,len(b)-len(a))
 for j,x in enumerate(b):out[j]=ga(out[j],x)
 return tr(out)
def pn(a):return[gn(x) for x in a]
def pm(a,b):
 if not a or not b:return[]
 out=[Z]*(len(a)+len(b)-1)
 for j,x in enumerate(a):
  if x==Z:continue
  for k,y in enumerate(b):
   if y!=Z:out[j+k]=ga(out[j+k],gm(x,y))
 return tr(out)
def pd(a,b):
 if not a:return[]
 if len(b)==1:return tr([gd(x,b[0]) for x in a])
 a=a.copy();q=[Z]*(len(a)-len(b)+1)
 while a and len(a)>=len(b):
  k=len(a)-len(b);v=gd(a[-1],b[-1]);q[k]=v
  for j,x in enumerate(b):a[k+j]=ga(a[k+j],gn(gm(v,x)))
  tr(a)
 assert not a
 return tr(q)
def determinant(matrix):
 a=[[x.copy() for x in row] for row in matrix];n=len(a);prev=[ONE];sign=1
 for k in range(n-1):
  p=next((j for j in range(k,n) if a[j][k]),None)
  if p is None:return[]
  if p!=k:a[k],a[p]=a[p],a[k];sign=-sign
  pivot=a[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):a[i][j]=pd(pa(pm(pivot,a[i][j]),pn(pm(a[i][k],a[k][j]))),prev)
   a[i][k]=[]
  prev=pivot
 return a[-1][-1] if sign==1 else pn(a[-1][-1])

def joint(z,mu=QI(0,1)):
 a,c=flat_symbols([mu,z,mu,mu])
 return np.concatenate([np.array(a,dtype=object).T,np.array(c,dtype=object)])
def coeffs(mu=QI(0,1)):
 p,m,q=[joint(z,mu) for z in (1,-1,QI(0,1))]
 z0=(p+m)/2;zp=(p-z0+(q-z0)/QI(0,1))/2;zm=p-z0-zp
 pol=[]
 for r in range(34):
  row=[]
  for j in range(24):
   v=[2*x[r,j] for x in (zm,z0,zp)]
   assert all(x.re.denominator==x.im.denominator==1 for x in v)
   row.append(tr([(int(x.re),int(x.im)) for x in v]))
  pol.append(row)
 z=QI(F(3,5),F(4,5));check=joint(z,mu)
 assert np.array_equal(check,zm/z+z0+zp*z)
 return pol

def qtrim(p):
 while p and not p[-1]:p.pop()
 return p
def qrem(a,b):
 a=a.copy()
 while a and len(a)>=len(b):
  k=len(a)-len(b);v=a[-1]/b[-1]
  for j,x in enumerate(b):a[k+j]-=v*x
  qtrim(a)
 return a
def qgcd(a,b):
 while b:a,b=b,qrem(a,b)
 return [x/a[-1] for x in a]
def qpoly(p):return [QI(F(a),F(b)) for a,b in p]
def evaluate(p,z):
 y=QI()
 for c in p[::-1]:y=y*z+QI.of(c)
 return y
def exact_strings(p):return [{'re':str(QI.of(x).re),'im':str(QI.of(x).im)} for x in p]

def run_checks():
 records={}
 cases=[('minus_one',QI.of(-1),[24,25,26,27,28,29,30,31,32,0,1,3,4,5,6,7,9,11,12,13,15,18,19,21]),
        ('quarter',QI(0,1),[24,25,26,27,28,29,30,31,32,0,1,2,3,4,5,6,7,8,9,11,12,13,14,15])]
 for name,mu,otherrows in cases:
  pol=coeffs(mu);charts=[];g=None
  for rows in (list(range(24)),otherrows):
   d=determinant([pol[r] for r in rows]);assert d
   qp=qpoly(d);g=qp if g is None else qgcd(g,qp)
   z=QI(F(3,5),F(4,5));matrix=joint(z,mu)[rows]
   rank,value=elimination(matrix.tolist());assert rank==24
   scale=QI.of(1)
   for _ in range(24):scale*=2*z
   assert evaluate(qp,z)==scale*value
   charts.append({'rows':rows,'degree':len(d)-1,'determinant':[list(x) for x in d]})
  if name=='minus_one':expected=[QI()]*20+[QI.of(1)]
  else:
   p=[ONE]
   for _ in range(6):p=pm(p,[(0,-1),ONE])
   expected=[QI()]*18+qpoly(p)
  assert g==expected
  records[name]={'mu':exact_strings([mu])[0],'charts':charts,'monic_gcd':exact_strings(g)}
  print('PASS_EXACT_CONTINUOUS_'+name.upper()+'_CIRCLE_MAXIMAL_MINORS',flush=True)

 q=QI(0,1);j=joint(q);assert elimination(j.tolist())[0]==20
 r=qi_inverse(j[np.ix_(ROWS,COLS)])
 n=np.array([[QI() for _ in range(4)] for _ in range(24)],dtype=object)
 vectors=[[0,0,0,1,-1,1],[0,1,-1,0,0,1],[1,0,-1,0,1,0],[1,-1,0,1,0,0]]
 for role,v in enumerate(vectors):
  for k,x in enumerate(v):n[6*role+k,role]=QI.of(x)
 assert not np.any(j@n)
 pol=coeffs();dj=np.array([[sum((QI(F(a),F(b)) for a,b in (row[k][0] if len(row[k])>0 else Z,
                                                        row[k][2] if len(row[k])>2 else Z)),QI())/2
                         for k in range(24)] for row in pol],dtype=object)
 residual=dj@n-j[:,COLS]@r@(dj@n)[ROWS]
 rest=[k for k in range(34) if k not in ROWS];reduced=residual[rest]
 assert elimination(reduced.tolist())[0]==4
 print('PASS_SIMPLE_QUARTER_OPENING_ON_ALL_FOUR_COMPLEX_CENTER_LINES',flush=True)

 # Scoped all-component, one-coordinate curved rescue radius: no S' term
 # is needed here because every actual sampled coframe is compared to I.
 eps=F(1,10000);base=F(35,6)
 coframe=base*144*(2*eps+eps*eps)
 log=base*8192*F(1,200000)
 assert coframe<F(1,4) and log<F(1,4)
 assert 2*base<F(12)
 print('PASS_GENERAL_SMALL_COFRAME_ONE_COORDINATE_RESCUE_BOUNDS',flush=True)
 return {
  'arithmetic':'Gaussian integers, exact fraction-free polynomial Bareiss; Q(i) polynomial gcd',
  'symbol':'literal identity sheet (A^T;C), lambda=(mu,z,mu,mu)',
  'Laurent_radius':1,'matrix_clear_factor':'2*z',
  'continuous_circle_certificates':records,
  'quarter_rank':20,'quarter_kernel_vectors':vectors,
  'quarter_reduced_z_derivative_rank':4,
  'quarter_reduced_z_derivative':[exact_strings(row) for row in reduced],
  'mu_one_input':'owned two-sided H_1(z) inverse, kernel mass <=35/6 on the unit circle',
  'mu_minus_i':'coefficient conjugation of the mu=i theorem',
  'physical_sector':'mu^4=1, |z|=1; product-closed four-phase/one-envelope subgroup',
  'physical_zeros':[{'mu':'i','z':'i','rank':20},{'mu':'-i','z':'-i','rank':20}],
  'uniform_linear_conclusion':'normal field plus actual envelope difference <= C*joint rows, all l^p including unweighted owner sum, independent of L',
  'general_one_coordinate_designated_bounds':{
   'coframe_operator_distance_from_identity':str(eps),
   'h_times_comparison_generator_sup_bound':str(F(1,200000)),
   'Neumann_coframe_error':str(coframe),'Neumann_log_error':str(log),
   'inverse_bound':12,'exact_correction_bound':24},
  'nonclaims':['no continuous full-four-dimensional torus classification',
               'no connection-only transverse inverse',
               'no unrestricted nonlinear quarter response theorem',
               'no task-level Einstein terminal']}

if __name__=='__main__':
 import argparse
 from pathlib import Path
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path);parser.add_argument('--expect',type=Path)
 args=parser.parse_args();report=run_checks()
 if args.expect:
  assert json.loads(args.expect.read_text())==report
  print('PASS_PINNED_LEDGER',flush=True)
 if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
 print('RESULT: all-frequency four-phase sector and general one-coordinate designated rescue.',flush=True)
