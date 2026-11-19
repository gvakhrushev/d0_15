#!/usr/bin/env python3
"""D0 #334: derived saddle/Prospective-minimum no-go and residual norm bridge.
Consumes published certified scalar Hessian margins, does NOT certify Book03.
All tests use Python standard library exact rationals.
"""
from fractions import Fraction as F
from itertools import product

checks=[]
def check(label,condition):
    if not condition:raise AssertionError(label)
    checks.append(label)

# Strict LOWER and UPPER signed Hessian bounds, not claimed as actual Hessian entries.
pos_lower=F(30283,10000)
neg_upper=-F(10912,10000)
ball_motion=F(169344,10_000_000)
book_hessian_max=F(1,1000)
pos_robust=pos_lower-ball_motion-book_hessian_max
neg_robust=neg_upper+ball_motion+book_hessian_max
check('certified lower coframe curvature preserved',pos_robust==F(30103656,10_000_000))
check('certified upper coframe curvature preserved',neg_robust==-F(10732656,10_000_000))
check('indefinite even with C2 actual-source perturbation within declared bounds',pos_robust>0 and neg_robust<0)
check('constant physical source rescaling positive cannot give PSD',pos_robust>0 and neg_robust<0)
check('constant physical source rescaling negative cannot give PSD',-pos_robust<0 and -neg_robust>0)
check('required independent compiler Hessian negative-direction threshold',-neg_robust==F(10732656,10_000_000))
check('required independent compiler Hessian positive-direction threshold',pos_robust==F(30103656,10_000_000))

# A rigorous elementary 2-dimensional representative of the general congruence theorem.
H=[[F(3),F(0)],[F(0),F(-1)]]
W=[[F(2),F(1)],[F(1),F(2)]]

def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def transpose(a):return [list(x) for x in zip(*a)]
def quad(a,v):return sum(v[i]*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))
def det(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]

HV=mm(transpose(H),mm(W,H))
check('toy stationary original action is strict saddle',quad(H,[1,0])>0 and quad(H,[0,1])<0)
check('native-positive verification metric SPD',W[0][0]>0 and det(W)>0)
check('source-verification Hessian exact JtWJ',HV==[[F(18),F(-3)],[F(-3),F(2)]])
check('source-verification Hessian positive definite',HV[0][0]>0 and det(HV)>0)
for s,t in product(range(-4,5),repeat=2):
    if s==0 and t==0:continue
    check(f'positive verified source norm at {s},{t}',quad(HV,[F(s),F(t)])>0)

# A full-rank history writer (invertible J) conserves the saddle inertia.
J=[[F(1),F(1)],[F(0),F(1)]]
Hpull=mm(transpose(J),mm(H,J))
check('genuinely two-sided rank-two physical writer',det(J)!=0)
check('full-rank writer retains positive physical curvature',quad(Hpull,[1,0])>0)
check('full-rank writer retains negative physical curvature',quad(Hpull,[-1,1])<0)

# Allowing a source-neutral-at-the-root setup charge DOES NOT imply a neutral Hessian.
# Its minimum stabilizing second-order cost on a normalized negative writer tangent
# must exceed the negative Hessian margin.  Testing threshold exactly:
for eps,expected in [(F(1,2),False),(F(10732656,10_000_000),True),(F(2),True)]:
    check('native-extra-price necessary second-variation wall '+str(eps),
          (neg_robust+eps>=0)==expected)

print('PASS: D0 #334 saddle/minimum/verification strategic bridge',len(checks),'exact-rational assertions')
print('strict positive coframe lower >',float(pos_robust))
print('strict negative coframe upper <',float(neg_robust))
print('verified residual Hessian Ht W H',[[str(v) for v in row] for row in HV])
print('verified residual Hessian determinant',str(det(HV)))
print('physical writer pullback Hessian',[[str(v) for v in row] for row in Hpull])
print('STATUS: new algebraic consumer only, Book03 price/cut/Info/admissibility and GR remain open')
