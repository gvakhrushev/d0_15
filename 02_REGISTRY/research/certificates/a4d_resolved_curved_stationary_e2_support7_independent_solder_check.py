#!/usr/bin/env python3
"""Exact finite solder equations on seven independent controlled amplitudes.

This constructs the genuine multivariate Cayley ansatz, its Lorentz inverses,
and its full homogeneous free-solder linear equation H(x) vec(Theta)=0 over
QQ[x0,...,x6], after clearing ONLY the declared Cayley chart product.

At the fixed stored solder ETA, a four-equation necessary subsystem depends
only on (x0,x3,x4,x6); its compact rational polynomials are stored alongside
this certificate. The subsystem is NOT the full stationary system. Its exceptional leading-
coefficient component is reduced exactly; the remaining three-variable
finite system has not been classified. The 3-dimensional tangent range kernel of
the separate cokernel certificate is not imposed as a nonlinear ansatz here.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from itertools import permutations
from pathlib import Path

import sympy as sp
from sympy import QQ
from sympy.polys.rings import ring
from sympy.polys.fields import field


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print('PASS_' + name)


p = Path(__file__).with_name('a4d_resolved_curved_stationary_e2_support7_order1_check.py')
s = importlib.util.spec_from_file_location('support7_order1_owner', p)
m = importlib.util.module_from_spec(s)
with contextlib.redirect_stdout(io.StringIO()):
    s.loader.exec_module(m)

R,*x=ring('x0,x1,x2,x3,x4,x5,x6',QQ)
zero,one=R.zero,R.one

def mc(a):return [[R.from_expr(a[i,j]) for j in range(a.cols)] for i in range(a.rows)]
def mz(n,k=None):return [[zero for _ in range(n if k is None else k)] for _ in range(n)]
def ma(a,b):return [[a[i][j]+b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def ms(s,a):return [[s*z for z in row] for row in a]
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),zero) for j in range(len(b[0]))] for i in range(len(a))]
def mt(a):return [list(z) for z in zip(*a)]
def md(a):
 n=len(a);out=zero
 for perm in permutations(range(n)):
  val=one
  for i in range(n):val*=a[i][perm[i]]
  out+=(-1 if sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2 else 1)*val
 return out

def adj(a):
 n=len(a)
 return [[(-1)**(i+j)*md([[a[k][l] for l in range(n) if l!=i] for k in range(n) if k!=j]) for j in range(n)]for i in range(n)]
def wedge(a,b):return [a[i]*b[j]-a[j]*b[i] for i,j in m.PAIRS]
I=mc(sp.eye(4)); eta=mc(m.ETA)
A=[mc(a)for a in m.generators0]
for k,(_,q,h)in enumerate(m.SELECTED_SPECS):A[q]=ma(A[q],ms(x[k],mc(h)))
Den=[ma(I,ms(-QQ(1,2),a))for a in A]
D=[md(d)for d in Den]
U=[mm(ma(I,ms(QQ(1,2),a)),adj(d))for a,d in zip(A,Den)]
Ui=[mm(mm(eta,mt(u)),eta)for u in U]
for u,ui,d in zip(U,Ui,D):assert mm(u,ui)==ms(d*d,I)
common=one
for d in D:common*=d*d
curves={}
for r,s in m.PAIRS:
 P=mm(mm(mm(U[r],U[s]),Ui[r]),Ui[s])
 Pi=mm(mm(eta,mt(P)),eta)
 C=ms(QQ(1,2),ma(P,ms(-one,Pi)))
 Ce=mm(C,eta)
 response=mm(mc(m.G2*m.STAR),[[Ce[i][j]]for i,j in m.PAIRS])
 factor=common.exquo((D[r]*D[s])**2)
 curves[(r,s)]=[row[0]*factor for row in response]

grad=mz(4)
for f,resp in curves.items():
 u,v=[i for i in range(4)if i not in f]
 for a in range(4):
  ea=[one if i==a else zero for i in range(4)]
  for b in range(4):
   dw=[zero]*6
   if b==u:dw=[z+y for z,y in zip(dw,wedge(ea,[eta[i][v]for i in range(4)]))]
   if b==v:dw=[z+y for z,y in zip(dw,wedge([eta[i][u]for i in range(4)],ea))]
   grad[a][b]+=16*m.orientation(f)*sum((z*y for z,y in zip(dw,resp)),zero)

check('EXACT_CHART_FACTORS', D == [
    2-x[0]**2/2, R(2), 1-x[5]-(x[1]**2+x[2]**2)/4, 1-x[6]**2/4])
check('ALL_ROLE_POLYNOMIAL_LORENTZ_INVERSE_IDENTITIES', all(
    mm(u,ui)==ms(d*d,I) for u,ui,d in zip(U,Ui,D)))

# Arbitrary absolute solder: the linear Euler map is constructed without
# choosing a solder path. At homogeneous links it is the same local equation
# on every site; the factor 16 below just sums identical site densities.
H = mz(16)
for f,response in curves.items():
    u0,v0 = [i for i in range(4) if i not in f]
    for a in range(4):
        for c in range(4):
            ea=[one if i==a else zero for i in range(4)]
            ec=[one if i==c else zero for i in range(4)]
            value=16*m.orientation(f)*sum((z*y for z,y in zip(wedge(ea,ec),response)),zero)
            H[4*a+u0][4*c+v0] += value
            H[4*c+v0][4*a+u0] += value
check('FREE_SOLDER_POLYNOMIAL_HESSIAN_SYMMETRIC', H==mt(H))
vec_eta=[[R.from_expr(z)]for z in m.ETA]
check('POLYNOMIAL_HESSIAN_GRADIENT_AT_ETA',
      mm(H,vec_eta)==[[z]for row in grad for z in row])
check('BASE_FIXED_SOLDER_EULER_ZERO', all(
    z.get((0,)*7,QQ.zero)==0 for row in grad for z in row))

# A compact necessary subsystem comes from the column-2 solder equations.
# They see only roles 0,1,3: complementary faces omit role 2.
variables = tuple(R.symbols)
reduced_variables = (variables[0],variables[3],variables[4],variables[6])
data_path=Path(__file__).with_name(
    'a4d_resolved_curved_stationary_e2_support7_solder_reduced4.json')
data=json.loads(data_path.read_text())
check('REDUCED_ARTIFACT_VARIABLE_ORDER', data['variables']==[str(z)for z in reduced_variables])
polys=[]
for a in range(4):
    z=grad[a][2]
    divisor=z.gcd(common)
    num,den=z.exquo(divisor),common.exquo(divisor)
    stored=data['equations'][a]
    check(f'REDUCED_SOLDER_{a}_2_EXACT_STORED_RATIONAL_FUNCTION',
          R.from_expr(sp.sympify(stored['numerator']))*den
          ==R.from_expr(sp.sympify(stored['denominator']))*num)
    check(f'REDUCED_SOLDER_{a}_2_ONLY_FOUR_AMPLITUDES',
          num.as_expr().free_symbols.issubset(set(reduced_variables))
          and den.as_expr().free_symbols.issubset(set(reduced_variables)))
    check(f'REDUCED_SOLDER_{a}_2_ONLY_CHART_DENOMINATORS',
          common.rem(den)==R.zero)
    polys.append(sp.Poly(num.as_expr(),*reduced_variables))
check('REDUCED_SUBSYSTEM_POLYNOMIAL_DEGREES',
      [z.total_degree()for z in polys]==[8,6,9,8])

Jfixed=sp.Matrix(16,7,lambda i,j:
    grad[i//4][i%4].get(tuple(1 if k==j else 0 for k in range(7)),QQ.zero)
    /common.get((0,)*7,QQ.zero))
check('SEVEN_AMPLITUDE_FIXED_SOLDER_TANGENT_RANK_7', Jfixed.rank()==7)
Jfour=Jfixed.extract([2,6,10,14],[0,3,4,6])
check('REDUCED_FOUR_AMPLITUDE_TANGENT_JACOBIAN_INVERTIBLE', Jfour.det()==-131072)
print('REDUCED_FOUR_JACOBIAN', Jfour.tolist())

# Independent exact nonlinear path specialization, not just an order-one test.
fp=Path(__file__).with_name('a4d_resolved_curved_stationary_e2_support7_finite_solder_check.py')
fs=importlib.util.spec_from_file_location('finite_solder_owner',fp)
f=importlib.util.module_from_spec(fs)
with contextlib.redirect_stdout(io.StringIO()):
    fs.loader.exec_module(f)
F,t=field('t',QQ)
def path(poly):
    out=F.zero
    for monomial,coefficient in poly.items():
        scale=coefficient
        for power,amplitude in zip(monomial,m.EXPECTED_V):
            scale*=QQ.from_sympy(amplitude)**power
        out+=F(scale)*t**sum(monomial)
    return out
for a in range(4):
    for b in range(4):
        check(f'FINITE_PATH_SPECIALIZATION_SOLDER_{a}_{b}',
              path(grad[a][b])/path(common)==F.from_expr(f.grad[a][b].as_expr()))

# An actual nonlinear elimination, separately from the tangent range split.
# The column-2 equation at row 1 is linear in x0: a*x0+b=0.
y0,y3,y4,y6=reduced_variables
integer_polys=[z.clear_denoms()[1].as_expr()for z in polys]
p1=sp.Poly(integer_polys[1],y0)
a=sp.diff(integer_polys[1],y0)
b=integer_polys[1].subs(y0,0)
check('NONLINEAR_ELIMINATION_EQUATION_LINEAR_IN_X0', p1.degree()==1)
check('EXACT_BRANCH_SPLIT_IDENTITY',
      sp.expand(b-2*a-2*y4*(y6**2-4)**2)==0)
check('EXCEPTIONAL_LEADING_COEFFICIENT_AT_X4_ZERO',
      sp.expand(a.subs(y4,0)-32*y6**2)==0)
# On the chart y6^2!=4, a=b=0 forces y4=y6=0. The remaining two-variable
# ideal gives chart-unit multiples of y0 and y3, hence both zero as well.
exceptional=[sp.expand(z.subs({y4:0,y6:0}))for z in integer_polys]
Gexceptional=sp.groebner([z for z in exceptional if z],y3,y0,order='lex')
check('EXCEPTIONAL_COMPONENT_FORCES_X0_ZERO_IN_CHART',
      Gexceptional.reduce(y0*(y0**2-4)**2)[1]==0)
check('EXCEPTIONAL_COMPONENT_FORCES_X3_ZERO_IN_CHART',
      Gexceptional.reduce(y3*(y0**2-4)**2)[1]==0)
check('EXCEPTIONAL_COMPONENT_CONTAINS_ORIGINAL_BASE', all(
      z.subs({y0:0,y3:0})==0 for z in exceptional))

reduced3=[]
for index in (0,2,3):
    p0=sp.Poly(integer_polys[index],y0)
    degree=p0.degree()
    horner=sp.S.Zero
    for k,coefficient in enumerate(p0.all_coeffs()):
        horner=sp.expand(-b*horner+coefficient*a**k)
    direct=sum(coefficient*(-b)**power*a**(degree-power)
               for (power,),coefficient in p0.terms())
    check(f'MAIN_BRANCH_{index}_EXACT_HOMOGENIZED_SUBSTITUTION',
          sp.Poly(sp.expand(horner-direct),y3,y4,y6).is_zero)
    reduced3.append(sp.Poly(horner,y3,y4,y6))
check('THREE_VARIABLE_FINITE_REDUCTION_DEGREES',
      [z.total_degree()for z in reduced3]==[19,25,24])
print('NONLINEAR_ELIMINATION_A', str(a))
print('NONLINEAR_ELIMINATION_B_MINUS_2A', '2*x4*(x6^2-4)^2')
# Complete the exceptional branch with the remaining row-major solder
# equations. In the three amplitudes left on role 2, a tiny exact Groebner
# basis yields x2^2+x5^2 and the two factors needed after the chart exclusion.
z1,z2,z5=variables[1],variables[2],variables[5]
remaining=[sp.expand(g.as_expr().subs({y0:0,y3:0,y4:0,y6:0}))
           for row in grad for g in row]
remaining=[g for g in remaining if g!=0]
Gremaining=sp.groebner(remaining,z1,z2,z5,order='lex')
check('EXCEPTIONAL_ROLE2_SUM_OF_SQUARES_IN_IDEAL',
      Gremaining.reduce(z2**2+z5**2)[1]==0)
check('EXCEPTIONAL_ROLE2_X5_FACTOR_IN_IDEAL',
      Gremaining.reduce((z1-z5+2)**2*z5**2)[1]==0)
role2_factor=((z1-z5+2)*(z1**3+z1**2*z5+z1*z5**2-2*z1*z5-4*z1+z5**3-4*z5**2+8*z5))
check('EXCEPTIONAL_ROLE2_X1_FACTOR_IN_IDEAL',
      Gremaining.reduce(role2_factor)[1]==0)
check('REAL_SPECIALIZATION_GIVES_X1_CHART_FACTOR',
      sp.expand(role2_factor.subs({z2:0,z5:0})-z1*(z1+2)**2*(z1-2))==0)
real_univariates=[sp.Poly(sp.expand(g.subs({z2:0,z5:0})),z1,domain=sp.QQ) for g in remaining]
real_univariates=[g for g in real_univariates if not g.is_zero]
common_real_gcd=real_univariates[0]
for g in real_univariates[1:]:common_real_gcd=sp.gcd(common_real_gcd,g)
check('ALL_REMAINING_EQUATIONS_HAVE_EXACT_REAL_ROOT_FACTOR',
      sp.factor(common_real_gcd.as_expr())==z1*(z1+2)**2*(z1-2))
check('EXCEPTIONAL_ROLE2_BASE_IS_SOLDER_CRITICAL',
      all(g.subs({z1:0,z2:0,z5:0})==0 for g in remaining))
check('EXCEPTIONAL_ROOT_RETAINS_NONZERO_FULL_LINK_DEFECT',
      list(m.base_missing)==[-16,0,16,0,-32,64,0,-32])
print('EXCEPTIONAL_ROLE2_GROEBNER_BASIS',
      [sp.factor(g.as_expr())for g in Gremaining.polys])
print('EXCEPTIONAL_BRANCH_REAL_ROOTS', 'z2^2+z5^2=0 => z2=z5=0; D2!=0 => z1 not +/-2; ideal => z1=0')
print('EXCEPTIONAL_A_ZERO_FINAL', 'all seven support amplitudes are zero')
print('MAIN_BRANCH', 'a!=0; x0=-b/a; F_i=a^deg_x0(p_i)*p_i(-b/a,x3,x4,x6)=0 for i=0,2,3')
print('MAIN_BRANCH_CHART', 'a!=0; x6^2!=4; b^2-4*a^2!=0; role-2 D2!=0 retained')
print('THREE_VARIABLE_REDUCTION_DEGREES', [z.total_degree()for z in reduced3])

print('CHART_FACTORS', [str(z.as_expr())for z in D])
print('FINITE_SOLDER_SYSTEM', 'H_num(x) vec(Theta)=0, chart product nonzero')
print('FIXED_ETA_NECESSARY_SUBSYSTEM', 'four rational equations in (x0,x3,x4,x6), degrees 8,6,9,8')
print('SCOPE: exact equation construction and branch split; main finite zero set not classified; the exceptional branch is killed at the origin')
print('STATUS: full link/affine Euler and R=R_*(C)!=0 remain open; IN_PROGRESS')
