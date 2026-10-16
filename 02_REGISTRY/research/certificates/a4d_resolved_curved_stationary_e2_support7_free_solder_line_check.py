#!/usr/bin/env python3
"""Free homogeneous solder on the exact support-5 Newton line.

Classifies every real solder-critical point on the open Cayley chart. The
22 nonzero critical roots have corank one and nondegenerate solder, but no
full stationary configuration on the matched homogeneous translation ray
b_0=s*e0, b_1=b_2=b_3=0, for any four channel coefficients. This ray/line
result does not retire the independent seven amplitudes or arbitrary b.
Stored polynomial data is checked against reconstructed owner matrices;
there is no floating root, trusted symbolic solve, or new invariant.
"""
from __future__ import annotations
import contextlib, importlib.util, io, json
from pathlib import Path
import sympy as sp
from sympy.polys.matrices import DomainMatrix

def check(name, condition):
    if not condition: raise AssertionError(name)
    print('PASS_' + name, flush=True)

here=Path(__file__).parent
spec=importlib.util.spec_from_file_location('finite_owner',here/'a4d_resolved_curved_stationary_e2_support7_finite_solder_check.py')
f=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(f)
o=f.owner;t=sp.Symbol('t');D=f.chart
C=sp.prod(d.as_expr()**2 for d in D)
# Q rescales column u of the absolute solder by D_u^2.
H=f.mz(16)
for face,response in f.curves.items():
    u,v=[i for i in range(4)if i not in face]
    for a in range(4):
        for b in range(4):
            ea=[f.one if i==a else f.zero for i in range(4)]
            eb=[f.one if i==b else f.zero for i in range(4)]
            value=16*o.orientation(face)*sum((x*y for x,y in zip(f.wedge(ea,eb),response)),f.zero)
            common=f.K.from_expr(C)
            value=value*common/(D[u]**2*D[v]**2)
            check_name=f'H_{a}_{u}_{b}_{v}'
            assert value.denom.degree()==0,check_name
            H[4*a+u][4*b+v]+=value;H[4*b+v][4*a+u]+=value
H=sp.Matrix([[v.as_expr()for v in row]for row in H]);DM=DomainMatrix.from_Matrix(H)
check('NORMALIZED_HESSIAN_SYMMETRIC_POLYNOMIAL_DEGREE_8',H==H.T and max(sp.degree(v,t)for v in H if v)==8)
asset=json.loads(here.joinpath('a4d_resolved_curved_stationary_e2_support7_free_solder_root_data.json').read_text())
V=sp.Matrix([sp.sympify(v)for v in asset['numerator']]);d=sp.Poly(sp.sympify(asset['denominator']),t)
VD=DomainMatrix.from_Matrix(V).convert_to(DM.domain)
e0=DomainMatrix.from_Matrix(sp.eye(16)[:,0]).convert_to(DM.domain)
check('EXACT_POLYNOMIAL_INVERSE_COLUMN_IDENTITY',DM.matmul(VD)==e0.scalarmul(DM.domain.from_sympy(d.as_expr())))
P=next(poly.monic()for poly,m in sp.factor_list(d)[1]if poly.degree()==78)
check('DENOMINATOR_IS_UNIT_TIMES_T_SQUARED_P',d.exquo(P).monic().as_expr()==t*t)
hdet=sp.Poly(DM.domain.to_sympy(DM.det()),t)
hfactor=sp.Poly(t**12*(173*t-13)**2*(173*t+13)**2,t)*P
check('NORMALIZED_DETERMINANT_FACTOR_EXACT',hdet.degree()==94 and hdet.monic()==hfactor.monic())
check('P_SQUAREFREE',sp.gcd(P,P.diff()).degree()==0)
chart=sp.Poly(sp.prod(d.as_expr()for d in D),t)
check('ALL_P_ROOTS_OPEN_CHART_AND_NONZERO',sp.gcd(P,chart*sp.Poly(t,t)).degree()==0)
check('V0_NONZERO_AT_EVERY_P_ROOT',sp.gcd(P,sp.Poly(V[0],t)).degree()==0)
# Fraction-free determinant over QQ[t]. Reducing each intermediate factor
# modulo P would introduce enormous rational denominators unnecessarily.
VD4=DomainMatrix.from_Matrix(sp.Matrix(4,4,list(V))).convert_to(DM.domain)
theta_det=sp.Poly(DM.domain.to_sympy(VD4.det()),t)
check('NONDEGENERATE_CRITICAL_SOLDER_AT_EVERY_P_ROOT',sp.gcd(P,theta_det).degree()==0)
intervals=P.intervals()
check('EXACT_REAL_ROOT_COUNT_22',len(intervals)==22 and all(m==1 for _,m in intervals))
print('REAL_ROOT_ISOLATING_INTERVALS',intervals,flush=True)
# Simple determinant roots imply rank 15. At them H V=0 and V0 !=0,
# so V spans the entire critical kernel. Differentiating H V=d e0 gives
# V^T H' V=d' V0. Since S=Z^T H Z/(2 C) and Z=Q vec(Theta),
# criticality removes Q'/C' terms: partial_t S=d' V0/(2 C).
check('STAR_PATH_SOURCE_NONZERO_AT_ALL_CRITICAL_ROOTS',sp.gcd(P,d.diff()*sp.Poly(V[0],t)).degree()==0)
# Nonzero curvature on the same roots, independently of Euler stationarity.
curv=f.curves[(0,2)][0]
check('CURVATURE_COMPONENT_NONZERO_AT_ALL_CRITICAL_ROOTS',sp.gcd(P,sp.Poly(curv.numer.as_expr(),t)).degree()==0)

# Actual finite affine Euler matrix for the four existing channels.
def adj(M):
    return [[(-1)**(i+j)*f.md([[M[r][c]for c in range(4)if c!=i]for r in range(4)if r!=j])for j in range(4)]for i in range(4)]
faces={}
for r,s in o.PAIRS:
    p=f.mmul(f.mmul(f.mmul(f.U[r],f.U[s]),f.Ui[r]),f.Ui[s]);m=f.madd(f.I,f.mscale(-f.one,p))
    faces[r,s]=(p,m,f.md(m),adj(m))
def residual(first,second,component):
    def trans(face):
        r,s=face;p=faces[face][0]
        e=[[f.one if i==component else f.zero]for i in range(4)]
        br=e if r==0 else f.mz(4,1);bs=e if s==0 else f.mz(4,1)
        aa=f.madd(br,f.mmul(f.U[r],bs));bb=f.madd(bs,f.mmul(f.U[s],br))
        return f.madd(aa,f.mscale(-f.one,f.mmul(p,bb)))
    _,mf,det,af=faces[first];_,mg,_,_=faces[second]
    return f.madd(f.mscale(det,trans(second)),f.mscale(-f.one,f.mmul(f.mmul(mg,af),trans(first))))
B=[[f.zero for _ in range(4)]for _ in range(4)]
for first in o.PAIRS:
    for second in o.PAIRS:
        if first==second:continue
        cls=0 if len(set(first)&set(second))==1 else 1
        vectors=[residual(first,second,k)for k in range(4)];v=vectors[0]
        for k,w in enumerate(vectors):
            for kind,metric in enumerate((o.ETA,sp.eye(4))):
                B[k][2*kind+cls]+=32*sum((int(metric[i,i])*v[i][0]*w[i][0]for i in range(4)),f.zero)
minor=f.md(B)
check('FINITE_AFFINE_MINOR_DEGREES_125_120',minor.numer.degree()==125 and minor.denom.degree()==120)
check('FINITE_AFFINE_MINOR_NONZERO_AT_ALL_CRITICAL_ROOTS',sp.gcd(P,sp.Poly(minor.numer.as_expr(),t)).degree()==0)
check('FINITE_AFFINE_DENOMINATOR_ONLY_CHART_UNITS',sp.gcd(P,sp.Poly(minor.denom.as_expr(),t)).degree()==0)
# b=s e0: for s !=0 these four necessary affine rows force c=0.
# For s=0 every channel and its link gradient vanish. Either way the
# nonzero star path source excludes full stationarity with det Theta !=0.
print('EXACT_RESULT: 22 real curved nondegenerate critical solder roots; no full stationary point on this line and matched translation ray',flush=True)
print('SCOPE: arbitrary four-channel coefficients; homogeneous free solder; b0=s*e0, b1=b2=b3=0; independent seven amplitudes and arbitrary b remain open',flush=True)
