#!/usr/bin/env python3
"""Exact bounded native retention controls and their original growing clock.
Only canonical births, G, CX are executed. No inverse or continuous gate.
This is a fixture, not a full XF compile or a selected physical valuation.
"""
import hashlib
import json
from math import comb
from pathlib import Path
import sympy as s

checks = []
def need(condition, label):
    if not bool(condition):
        raise ArithmeticError(label)
    checks.append(label)

a = s.symbols('a', positive=True)
p = a*a
modulus = a**4+a**2-1

def red(x):
    if x == 0:
        return s.S.Zero
    num, den = s.fraction(s.cancel(x))
    num = s.rem(num, modulus, a)
    den = s.rem(den, modulus, a)
    return s.rem(s.expand(num*s.invert(den, modulus, a)), modulus, a)

def reduced(M):
    return M.applyfunc(red)

def equal(A, B):
    return A.shape == B.shape and all(red(x) == 0 for x in A-B)

v = s.Matrix([a,p])
G = s.Matrix([[a,-p],[p,a]])
need(red((v.T*v)[0]-1) == 0, 'original canonical birth vector is normalized')
need(equal(G.T*G,s.eye(2)), 'original Golden G is orthogonal over its exact field')

# At the final 3-bit carrier use little-endian labels. The first two
# canonical births create the helpers; the third creates retention bit 0.
# Each physical birth is still the original J:x -> x tensor v.
def cx(control, target):
    M = s.zeros(8)
    for col in range(8):
        row = col ^ (1 << target) if col & (1 << control) else col
        M[row, col] = 1
    return M

def gate(op):
    if op[0] == 'G':
        bit = op[1]
        M = s.zeros(8)
        for col in range(8):
            M[col,col] = a
            M[col ^ (1 << bit), col] = -p if col & (1 << bit) else p
        return M
    if op[0] == 'CX':
        return cx(op[1],op[2])
    raise ValueError('unsupported native instruction')

def execute(word):
    U = s.eye(8)
    for op in word:
        U = reduced(gate(op)*U)
    return U

I2 = [('CX',0,1),('CX',0,1)]
I5 = [('CX',0,1),('CX',1,2),('CX',0,1),('CX',1,2),('CX',0,2)]
words = {
    'minus': I2*3,
    'zero': [('G',0)]+I5,
    'plus': [('G',0),('G',0)]+I2*2,
}
need(equal(execute(I2),s.eye(8)), 'I2 identity is exact on all eight columns')
need(equal(execute(I5),s.eye(8)), 'chronological I5 identity is exact on all eight columns')
for label, word in words.items():
    need(len(word) == 6, label+' macro has exactly six actual native calls')
    need(all(op[0] in ('G','CX') for op in word),
         label+' macro uses no inverse, reset, measurement or new primitive')
U = {label: execute(word) for label, word in words.items()}
G0 = gate(('G',0))
need(equal(U['minus'],s.eye(8)), 'minus endpoint is identity on every column')
need(equal(U['zero'],G0), 'zero endpoint is original G on retention and identity on helpers')
need(equal(U['plus'],G0*G0), 'plus endpoint is G squared on retention and identity on helpers')
born = s.kronecker_product(v,v,v)
expected = {'minus':s.S.One, 'zero':a, 'plus':red(p**3)}
for label in words:
    need(red((born.T*U[label]*born)[0]-expected[label]) == 0,
         label+' initialized proper return equals '+str(expected[label]))

# Actual before-step spaces for three distinct births followed by all six
# stages of W_zero. The sixth native call is the real final closing g.
dims = [1,2,4]+[8]*6
N = len(dims)
D = sum(dims)
starts = [sum(dims[:j]) for j in range(N)]
need((N,D) == (9,55), 'literal original clock has N=9 stages and D=55 without padding fibres')
J0 = v
J1 = s.kronecker_product(s.eye(2),v)
J2 = s.kronecker_product(s.eye(4),v)
F = [J0,J1,J2]+[gate(op) for op in words['zero'][:-1]]
g = gate(words['zero'][-1])
need(len(F) == N-1 and words['zero'][-1] == ('CX',0,2),
     'last real CX is retained as closing gate, not a free closing identity')
for j, Fj in enumerate(F):
    need(Fj.shape == (dims[j+1],dims[j]) and equal(Fj.T*Fj,s.eye(dims[j])),
         'actual chronological prefix step '+str(j)+' is an isometry on its true spaces')

passive = [J0,J1,J2]+[s.eye(8) for _ in range(N-4)]
B = [None]*N
B[-1] = s.eye(8)
for j in range(N-2,-1,-1):
    B[j] = reduced(B[j+1]*passive[j])
details = [s.eye(1)]
for j in range(1,N):
    details.append(reduced(s.eye(dims[j])-passive[j-1]*passive[j-1].T))
Rblocks = [B[0].T]+[reduced(details[j]*B[j].T) for j in range(1,N)]
R = s.Matrix.vstack(*Rblocks)
need(equal(R.T*R,s.eye(8)), 'full original closure R retains every final birth complement')
need(equal(R*R.T,s.diag(*details)), 'closure range is initial carrier plus complete birth-detail blocks')
T = s.zeros(D)
for j,Fj in enumerate(F):
    T[starts[j+1]:starts[j+1]+dims[j+1],starts[j]:starts[j]+dims[j]] = Fj
T[:,starts[-1]:starts[-1]+dims[-1]] += reduced(R*g)
T = reduced(T)
need(equal(T.T*T,s.eye(D)), 'complete 55-dimensional original growing clock is unitary on all columns')
state = s.zeros(D,1)
state[0] = 1
states = [state]
compressed = []
for r in range(1,N+1):
    state = reduced(T*state)
    states.append(state)
    compressed.append(red(state[0]))
    if r < N:
        need(compressed[-1] == 0, 'original initial cut has no return at positive depth '+str(r))
need(red(compressed[-1]-a) == 0,
     'first possible full original return at N=9 has its actual coefficient a')

# All coherent pairs of this actual prepared clock at its true return depth.
zones = [0]*9+[1]*11+[2]*13
A_scene = s.Matrix(33,33,lambda i,j:int(zones[i]!=zones[j]))
need(sum(A_scene)==718, 'full original scene retains all 718 directed edges')
Ap = [s.eye(33)]
for j in range(1,2*N+1):
    Ap.append(Ap[-1]*A_scene)
u, w = s.symbols('u w',positive=True)
full_prepared = 0
survivors = []
for i in range(N+1):
    for j in range(N+1):
        cij = red((states[i].T*states[j])[0])
        if i!=j and cij!=0:
            survivors.append((i,j))
        full_prepared += comb(N,i)*comb(N,j)*u**(2*N-i-j)*w**(i+j)*Ap[2*N-i-j][0,0]*cij
bdiag = sum(comb(N,j)**2*u**(2*N-2*j)*w**(2*j)*Ap[2*N-2*j][0,0]
            for j in range(N+1))
moment = Ap[N][0,0]
expected_prepared = bdiag+2*(u*w)**N*moment*a
need(survivors==[(0,N),(N,0)],
     'all one hundred prepared quadratic pairs leave exactly two full-return cross terms')
need(all(red(x)==0 for x in s.Poly(s.expand(full_prepared-expected_prepared),u,w).coeffs()),
     'actual N=9 prepared response equals its exact diagonal plus full-return formula')
need(moment>0, 'the illustrative original coordinate-vertex scene cut has positive N-return moment')

# Owned XF scalar corner; identities include its independent retention row.
theta=s.symbols('theta',real=True)
rot=s.Matrix([[s.cos(theta),-s.sin(theta)],[s.sin(theta),s.cos(theta)]])
corner=a*s.cos(theta)-p*s.sin(theta)
need(equal(G.T*v,s.Matrix([1,0])), 'the original transpose G, not G, undoes the canonical born vector')
need(all(red(x)==0 for x in s.Poly(s.expand((v.T*rot*G*v)[0]-corner),s.cos(theta),s.sin(theta)).coeffs()),
     'actual retention corner has the exact minus-sine sign')
need(red(s.diff(corner,theta).subs(theta,0)+p)==0,
     'actual unit retention derivative at the canonical G is minus p')
need(red(s.trigsimp(corner**2+s.diff(corner,theta)**2)-1)==0,
     'retention corner and its derivative obey the unit-circle identity')
bb,kk,old,other,Q,ss,gg,ell=s.symbols('bb kk old other Q ss gg ell',positive=True)
f=ss+(1-ss)*Q
response=bb+2*kk*old*other*corner*f
rcenter=response.subs(theta,0)
score=-s.log(response)/(2*ell)
gain=kk*old*other*a*(1-ss)*gg/(ell*rcenter)
need(s.simplify(-s.diff(score,Q).subs(theta,0)*gg/gain-1)==0,
     'full prepared target has its true positive field gain when old and scene signs are positive')
need(s.simplify(-s.diff(score,theta).subs(theta,0)/gain+p*f/(a*(1-ss)*gg))==0,
     'normalized retention source is independent of all attenuation and old-overlap factors')
need(s.simplify(s.diff(response,Q).subs(theta,0)
                +a*(1-ss)*s.diff(response,theta).subs(theta,0)/(p*f))==0,
     'field derivative factors through the genuine retention row for every scalar aggregation')
need(s.simplify(-s.diff(score,old).subs(theta,0)/gain-f/((1-ss)*gg*old))==0,
     'true independent old preparation and corner source survives normalization')
need(s.simplify(-s.diff(score,other).subs(theta,0)/gain-f/((1-ss)*gg*other))==0,
     'all other retention factors keep their actual normalized row')

# Exact algebra underlying stationary-section and finite-contrast bounds.
c1,c2,c3=s.symbols('c1 c2 c3',real=True)
product=c1*c2*c3
need(s.diff(product,c1).subs(c1,0)==c2*c3,
     'one zero retention factor leaves its own nonzero derivative when the others survive')
need(all(s.diff(product,x).subs({c1:0,c2:0})==0 for x in (c1,c2,c3)),
     'two zero retention factors screen every rotor derivative and the field product')
t1,t2,t3=s.symbols('t1 t2 t3',nonnegative=True)
need(s.expand((t1+t2+t3)**2-(t1*t1+t2*t2+t3*t3)-2*(t1*t2+t1*t3+t2*t3))==0,
     'full row-sum norm controls the sum of squares in the attenuation bound')
need(s.Rational(5,6)*s.Rational(7,8)-s.Rational(1,8)==s.Rational(29,48),
     'compiled finite-source margin retains the central normalization correction')
need(s.Rational(29,48)-s.Rational(1,16)>s.Rational(1,2),
     'certified price-reading error leaves a strict half-margin')
need(s.Rational(4,5)**4+s.Rational(4,5)**2-1>0,
     'positive-root monotonicity gives the used bound a less than four fifths')
need(red((1-2*p*a)-(a-p)**2)==0,
     'one minus the full comparison baseline equals a strictly positive square')

result = {
    'status':'PASS', 'number_of_checks':len(checks), 'checks':checks,
    'arithmetic':'Q[a]/(a^4+a^2-1), a positive and p=a^2; exact symbolic reduction',
    'macros':words,
    'same_layout':{'native_calls_each':6,'wire_count':3,'endpoints':['I','G','G^2'],
                   'cold_scalars':['1','a','p^3']},
    'clock':{'word':'birth;birth;birth;G0;CX01;CX12;CX01;CX12;CX02',
             'stage_widths':dims,'N':N,'D':D,
             'initial_compressed_moments':[str(x) for x in compressed]},
    'input_head':'567e3806c58861eeebadf57ae34e8c4b2142141a',
    'not_claimed':['full XF compiled','unchanged bare-one-G clock price',
                   'equal G/CX inventory or physical native tariffs',
                   'a continuous primitive is admitted','full Cost-Info or GR closure'],
    'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
print(json.dumps(result,sort_keys=True,indent=2))
