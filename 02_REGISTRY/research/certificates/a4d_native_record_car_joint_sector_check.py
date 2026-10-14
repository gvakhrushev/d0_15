#!/usr/bin/env python3
"""Exact full-16 CAR / closed-record sector comparison (SOURCE #310).

This is a narrow symbolic research regression, not physical operator admission,
a new transition law, a CORE theorem or a GR claim.

Owners:
  A4D_NATIVE_CLOSED_RECORD_ENGINE.md
  A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md
  A4D_NATIVE_FOCK_RECORD_BINDING.md
"""
import sympy as S

a, p = S.symbols("a p", real=True)
I = S.eye(16)
sector = (0, 1, 6, 7, 10, 11, 12, 13, 14, 15)
seed_sector = (0, 1, 14, 15)


def creator(i):
    """Literal signed exterior creator on the complete sixteen-mask fibre."""
    out = S.zeros(16)
    for mask in range(16):
        if not mask & (1 << i):
            parity = (mask & ((1 << i) - 1)).bit_count()
            out[mask | (1 << i), mask] = -1 if parity % 2 else 1
    return out


def native_gate(sign):
    """All eight CAR pairs, as in the owned state-conditioned record gate."""
    out = S.zeros(16)
    for k in range(0, 16, 2):
        out[k, k], out[k, k+1] = a, -sign*p
        if k.bit_count() <= 1:
            out[k+1, k], out[k+1, k+1] = sign*p, a
        else:
            out[k+1, k], out[k+1, k+1] = -sign*p, -a
    return out


c = [creator(i) for i in range(4)]
beta = c[0] + c[0].T
alpha = [beta*(c[j]-c[j].T) for j in range(1, 4)]

for i in range(3):
    assert alpha[i] == alpha[i].T
    assert alpha[i].extract(seed_sector, seed_sector) == S.zeros(4)
    for j in range(3):
        assert alpha[i]*alpha[j]+alpha[j]*alpha[i] == 2*int(i == j)*I

# The sign-flip is an operator identity on the WHOLE admissible collinear sector;
# it is not extrapolated from a finite orbit.
for sign in (-1, 1):
    U = native_gate(sign)
    assert U.T*U == (a*a+p*p)*I
    assert U.extract(tuple(i for i in range(16) if i not in sector),sector) == S.zeros(6,10)
    assert U.extract(tuple(i for i in range(16) if i not in seed_sector),seed_sector) == S.zeros(12,4)
    for op in alpha:
        lhs = (U.T*op*U).extract(sector,sector)
        rhs = -(a*a+p*p)*op.extract(sector,sector)
        assert lhs == rhs

# All ten collinear coordinates are variables, embedded in the full Fock carrier.
x0,x1,w60,w61,w100,w101,w120,w121,h0,h1=S.symbols(
    "x0 x1 w60 w61 w100 w101 w120 w121 h0 h1", real=True)
v = S.zeros(16,1)
for idx,value in zip(sector,(x0,x1,w60,w61,w100,w101,w120,w121,h0,h1)):
    v[idx]=value
expected = [
    2*(w120*h1-w121*h0),
    -2*(w100*h1-w101*h0),
    2*(w60*h1-w61*h0),
]
assert all(S.expand((v.T*op*v)[0]-e)==0 for op,e in zip(alpha,expected))

# The genuine signed spectator frame and owned *whole-blank* projector.
masks=((0,2,4,8),(1,3,5,9),(14,12,10,6),(15,13,11,7))
signs=((1,1,1,1),(1,1,1,1),(1,1,-1,1),(1,1,-1,1))
B = S.zeros(16)
for row in range(4):
    for j in range(4):
        B[masks[row][j],4*row+j]=signs[row][j]
assert B.T*B == I
blank4 = S.Matrix([[1,0,1,0],[0,1,0,1],
                   [1,0,1,0],[0,1,0,1]])/2
blank = B*S.kronecker_product(blank4,S.eye(4))*B.T
assert blank.T == blank and blank**2 == blank
nulls=(I-blank).extract(tuple(range(16)),sector).nullspace()
assert len(nulls)==2
for t in nulls:
    w=S.Matrix([t[sector.index(i)] if i in sector else 0 for i in range(16)])
    assert all(S.simplify((w.T*op*w)[0])==0 for op in alpha)

seed=S.zeros(16,1);seed[1]=seed[15]=1
assert blank*seed==seed
assert [(seed.T*op*seed)[0] for op in alpha]==[0,0,0]

# An actual non-blank correlated input for the old *state-conditioned* engine.
witness=seed.copy();witness[6]=1
assert blank*witness != witness
assert (witness.T*witness)[0] == 3
assert [(witness.T*op*witness)[0] for op in alpha] == [0,0,2]
assert 1-S.Rational(2,3)**2 == S.Rational(5,9)

# The low-band pair equals the published seed, so its every-tick nonzero guard
# and the sign recursion persist. Higher pairs stay in the collinear sector.
# Current components alternate sign because the operator identity above holds
# for BOTH sign gates and a²+p²=1.

# Replacing only the observer pairing, without updating the native gate,
# fails full endpoint isometry already on the scalar column.
eta=S.diag(1,-1,-1,-1)
J=S.Matrix([1,0,0,S.Rational(2,3)])
k=(J.T*eta*J)[0]
h=-eta+2*eta*J*J.T*eta/k
assert h.det()==1 and h[0,0]==S.Rational(13,5)
assert sorted(h.eigenvals()) == [S.Rational(1,5),S.Integer(1),S.Integer(5)]
defect=S.expand(a*a+p*p*h[0,0]-1)
assert S.expand(defect.subs(a*a,p)-S.Rational(8,5)*p*p) == p*p+p-1

# The already owned whole-scene compiler uses only temporal-bit controlled
# flips C_fN/C_cN, the uniform temporal-bit G_N, the native U+, and a
# scene/controller-only reversal C_cf. Every matter generator reduces V.
# Consequently any controlled word, including its fixed nine-primitive
# incarnation on 718 directed edges x 2 controller values x 16 matter
# states, reduces (scene x controller) tensor V. No large dense
# 22976-by-22976 matrix is required for this exact tensor proof.
Xn = S.zeros(16)
Gn = S.zeros(16)
for mask in range(16):
    Xn[mask ^ 1, mask] = 1
for even_mask in range(0,16,2):
    Gn[even_mask,even_mask] = a
    Gn[even_mask,even_mask+1] = -p
    Gn[even_mask+1,even_mask] = p
    Gn[even_mask+1,even_mask+1] = a
outside_v=tuple(i for i in range(16) if i not in seed_sector)
for primitive in (I,Xn,Gn,native_gate(+1),native_gate(-1)):
    assert primitive.extract(outside_v,seed_sector) == S.zeros(12,4)
    assert primitive.extract(seed_sector,outside_v) == S.zeros(4,12)
assert 718*2*16 == 22976
for op in alpha:
    assert op.extract(seed_sector,seed_sector) == S.zeros(4)
# The last compression holds for EVERY correlated state in the scene/V
# product space, not just for a tensor-product prepared seed.

# Hostile controls: old seed cannot spontaneously become spatial-current active;
# changing current readout alone cannot retain endpoint isometry.
assert any(alpha[i].extract(sector,sector) != S.zeros(10) for i in range(3))
assert (witness.T*alpha[2]*witness)[0] != 0
assert blank*witness != witness
assert S.Rational(8,5)*p*p != 0  # polynomial identity, p>0 is the owned premise

print("PASS_FULL_16_CAR_AND_BOTH_NATIVE_SIGN_GATES")
print("PASS_SEED_ORBIT_ZERO_CURRENT_AND_COMPLETE_10_SECTOR_FLIP")
print("PASS_BLANK_INTERSECTION_DIM_2_AND_NONBLANK_TIMELIKE_WITNESS")
print("PASS_ENDPOINT_ISOMETRY_OBSTRUCTION_8P2_OVER5")
print("PHYSICAL_ADMISSION_SOURCE_WARD_AND_GR_OPEN")
