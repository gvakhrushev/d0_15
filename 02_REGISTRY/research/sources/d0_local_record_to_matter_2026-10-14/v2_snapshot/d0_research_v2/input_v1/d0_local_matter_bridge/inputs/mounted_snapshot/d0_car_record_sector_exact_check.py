#!/usr/bin/env python3
"""D0 #310: exact full-16 CAR current on the native record collinear sector.
Standalone symbolic research check; not a CORE certificate or a physical law.
Requires: sympy. Source formulas: A4D_NATIVE_CLOSED_RECORD_ENGINE.md
and A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md.
"""
import sympy as S

a, p = S.symbols("a p", real=True)
I = S.eye(16)
sector = (0,1,6,7,10,11,12,13,14,15)
tiny = (0,1,14,15)

def creator(i):
    out = S.zeros(16)
    for mask in range(16):
        if not mask & (1 << i):
            parity = (mask & ((1 << i) - 1)).bit_count()
            out[mask | (1 << i),mask] = -1 if parity % 2 else 1
    return out

def native_gate(sign):
    out = S.zeros(16)
    for k in range(0,16,2):
        out[k,k],out[k,k+1] = a,-sign*p
        if k.bit_count()<=1:
            out[k+1,k],out[k+1,k+1] = sign*p,a
        else:
            out[k+1,k],out[k+1,k+1] = -sign*p,-a
    return out

c = [creator(i) for i in range(4)]
beta = c[0]+c[0].T
alpha = [beta*(c[j]-c[j].T) for j in range(1,4)]

for i in range(3):
    assert alpha[i]==alpha[i].T
    assert alpha[i].extract(tiny,tiny)==S.zeros(4)
    for j in range(3):
        assert alpha[i]*alpha[j]+alpha[j]*alpha[i]==2*int(i==j)*I

for sign in (-1,1):
    U=native_gate(sign)
    assert U.T*U==(a*a+p*p)*I
    assert U.extract(tuple(i for i in range(16) if i not in sector),sector)==S.zeros(6,10)
    assert U.extract(tuple(i for i in range(16) if i not in tiny),tiny)==S.zeros(12,4)
    for op in alpha:
        lhs=(U.T*op*U).extract(sector,sector)
        rhs=-(a*a+p*p)*op.extract(sector,sector)
        assert lhs==rhs

# General collinear state; no coordinates have been discarded from its ambient Fock16.
x0,x1,w60,w61,w100,w101,w120,w121,h0,h1=S.symbols(
    'x0 x1 w60 w61 w100 w101 w120 w121 h0 h1', real=True)
v=S.zeros(16,1)
for idx,value in zip(sector,(x0,x1,w60,w61,w100,w101,w120,w121,h0,h1)):
    v[idx]=value
assert all(S.expand(r-e)==0 for r,e in zip(
    [(v.T*op*v)[0] for op in alpha],
    [2*(w120*h1-w121*h0), -2*(w100*h1-w101*h0),
     2*(w60*h1-w61*h0)]))
# These quadratic expectations all flip sign under either native gate;
# m norm is preserved after a²=p, p²+p=1 => a²+p²=1.

# Native signed apparatus-frame whole-blank projector.
masks=((0,2,4,8),(1,3,5,9),(14,12,10,6),(15,13,11,7))
signs=((1,1,1,1),(1,1,1,1),(1,1,-1,1),(1,1,-1,1))
B=S.zeros(16)
for row in range(4):
    for k in range(4):
        B[masks[row][k],4*row+k]=signs[row][k]
assert B.T*B==I
projector_rows=S.Matrix([
    [1,0,1,0],[0,1,0,1],[1,0,1,0],[0,1,0,1]])/2
blank=B*S.kronecker_product(projector_rows,S.eye(4))*B.T
assert blank.T==blank and blank**2==blank
nulls=(I-blank).extract(tuple(range(16)),sector).nullspace()
assert len(nulls)==2
assert all(
    S.simplify((w.T*op*w)[0])==0
    for t in nulls for op in alpha
    for w in [S.Matrix([t[sector.index(i)] if i in sector else 0 for i in range(16)])]
)

whole_blank=S.zeros(16,1)
whole_blank[1]=whole_blank[15]=1
assert blank*whole_blank==whole_blank
assert [(whole_blank.T*op*whole_blank)[0] for op in alpha]==[0,0,0]

active=whole_blank.copy()
active[6]=1
assert blank*active!=active
assert (active.T*active)[0]==3
assert [(active.T*op*active)[0] for op in alpha]==[0,0,2]
assert 1-S.Rational(2,3)**2==S.Rational(5,9)

# If the new CAR current were imposed as the observer's positive exterior
# pairing while retaining the old U_(sign*e0), the full gate would NOT be
# an endpoint isometry. On the scalar basis column, Ue_empty =
# a e_empty + p e_temporal.  The resulting Gram norm is a^2 + p^2*h00.
eta=S.diag(1,-1,-1,-1)
J=S.Matrix([1,0,0,S.Rational(2,3)])
k=(J.T*eta*J)[0]
h=-eta+2*eta*J*J.T*eta/k
assert h.det()==1
assert h[0,0]==S.Rational(13,5)
assert sorted(h.eigenvals())==[S.Rational(1,5),S.Integer(1),S.Integer(5)]
defect=S.expand(a*a+p*p*h[0,0]-1)
# By a²=p, p²+p=1, this becomes +8*p²/5 > 0.
assert S.expand(defect.subs(a*a,p)-S.Rational(8,5)*p*p)==p*p+p-1

print("PASS FULL_16_CAR_CLIFFORD_AND_NATIVE_GATE_SIGNS")
print("PASS CLOSED_4D_BLANK_ORBIT_ZERO_SPATIAL_CURRENT")
print("PASS CLOSED_10D_SECTOR_ALL_TIME_CURRENT_SIGN_FLIP")
print("PASS BLANK_INTERSECTION_DIM_2")
print("PASS NONBLANK_CORRELATED_ORBIT_J3_ALTERNATES_PLUS_MINUS_2_3")
print("PASS UNIFORM_FUTURE_TIMELIKE_NORM_5_9")
print("PASS CAR_PAIRING_OLD_GATE_ENDPOINT_ISOMETRY_DEFECT_8P2_OVER5")
print("PHYSICAL_ADMISSION_AND_FULL_SOURCE_REMAIN_OPEN")
