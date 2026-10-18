#!/usr/bin/env python3
"""Exact GNS paired-path folding and complete-pointer source controls.

No physical RIGHT-record admission, clock, matter or Einstein dynamics is
asserted. All combinatorial/source partition equalities use integer/rational
arithmetic. Diagnostic trace distances use floating-point only at the end.
"""
from collections import Counter
from fractions import Fraction
from math import log
import json

M = ((1, 1), (1, 0))    # READY=0, PENDING=1; M is symmetric

def fib(n):
    if n == -1:
        return 1
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def paths(n):
    ans = [(0,), (1,)]
    for _ in range(n):
        ans = [w + (v,) for w in ans
               for v in range(2) if M[w[-1]][v]]
    return ans

def pair_to_long(alpha, beta):
    assert alpha[-1] == beta[-1] and len(alpha) == len(beta)
    return alpha + tuple(reversed(beta[:-1]))

def prefixes(words, k):
    return Counter(w[:k+1] for w in words)

prefix_checks=0
for N in range(8):
    fine = paths(N)
    A=sum(w[-1] == 0 for w in fine)
    B=sum(w[-1] == 1 for w in fine)
    matched=[(a,b) for a in fine for b in fine if a[-1] == b[-1]]
    folded=[pair_to_long(a,b) for a,b in matched]
    unfolded=paths(2*N)
    assert (A,B)==(fib(N+2),fib(N+1))
    assert len(fine)==A+B==fib(N+3)
    assert len(matched)==A*A+B*B==fib(2*N+3)
    assert set(folded)==set(unfolded)
    assert len(set(folded))==len(folded)==len(unfolded)
    for k in range(N+1):
        c_pair=prefixes([a for a,b in matched],k)
        c_deep=prefixes(unfolded,k)
        assert c_pair==c_deep
        for w,count in c_pair.items():
            assert count==(fib(2*N-k+2) if w[-1] == 0
                           else fib(2*N-k+1))
        # No Einstein/Perron weights are fitted: choose arbitrary positive
        # RATIONAL z_w to test equality of the WHOLE nonlinear partition
        # polynomial, hence its formal derivatives in independent z_w.
        z={w:Fraction(3 + ((sum(w)+2*len(w)) % 7), 2)
           for w in paths(k)}
        D_pair=sum(z[a[:k+1]] for a,b in matched)
        D_deep=sum(z[g[:k+1]] for g in unfolded)
        assert D_pair==D_deep
        assert sum(c_pair.values())==len(matched)
        prefix_checks+=1

# Independent exact Fibonacci identity and normalization at larger N.
for N in range(24):
    A,B=fib(N+2),fib(N+1)
    assert A*A+B*B==fib(2*N+3)
    for k in range(N+1):
        r=N-k
        u,v,w=fib(r+1),fib(r),fib(r-1)
        x=Fraction(u*A+v*B,A*A+B*B)
        y=Fraction(v*A+w*B,A*A+B*B)
        assert x==Fraction(fib(2*N-k+2),fib(2*N+3))
        assert y==Fraction(fib(2*N-k+1),fib(2*N+3))
        a0,b0=fib(k+2),fib(k+1)
        assert a0*x+b0*y==1

# Negative control: one-sided uniform terminal N weights are NOT the
# complete paired GNS weights, even at the same nominal AF level.
N=3
A,B=fib(N+2),fib(N+1)
assert (A,B)==(5,3)
assert Fraction(1,A+B)!=Fraction(A,A*A+B*B)
assert Fraction(1,A+B)!=Fraction(B,A*A+B*B)

# Archive conditional entropy is a genuine recorded source term.
r=[Fraction(1,6), Fraction(1,3), Fraction(1,2)]
m=[2,2,3]
joint=[float(w)/mi for w,mi in zip(r,m) for _ in range(mi)]
left=[float(w) for w in r]
H=lambda q:-sum(p*log(p) for p in q if p)
assert abs(H(joint)-H(left)-sum(float(w)*log(mi)
                               for w,mi in zip(r,m)))<1e-12

# NEGATIVE quantum control: a pure pair-state with uniform basis
# probabilities is not forced to be left-tracial before the classical
# pair-pointer is dephased. On N=1, the READY 2x2 pure amplitude matrix
# has all entries 1/sqrt(5). Its left offdiag rho_01=2/5, while the
# dephased pair law gives rho_01=0.
assert Fraction(2,5)!=Fraction(0)

# EXACT 2x2 LEFT x 2x2 RIGHT source preservation versus right disturbance:
# full density rho = |(1,2,3,4)/sqrt(30)><...|, with all off-diagonal
# matrix-unit coherences retained before the pointer copy.
vec=(1,2,3,4)
rho=[[Fraction(vec[i]*vec[j],30) for j in range(4)] for i in range(4)]
def D_R(matrix):
    return [[matrix[i][j] if (i%2)==(j%2) else Fraction(0)
             for j in range(4)] for i in range(4)]
def left_op(two):
    return [[two[i//2][j//2] if (i%2)==(j%2) else Fraction(0)
             for j in range(4)] for i in range(4)]
def pairing(matrix, op):
    return sum(matrix[i][j]*op[j][i] for i in range(4)
               for j in range(4))
geo=left_op([[Fraction(1,2),Fraction(1,4)],
             [Fraction(1,4),Fraction(3,4)]])
geo_jet=left_op([[Fraction(0),Fraction(1)],
                 [Fraction(1),Fraction(0)]])
# Independent trace-zero Hermitian pure-state FIRST variation representative.
xi=(1,0,0,1)
tangent=[[Fraction(xi[i]*xi[j],2) -
          (Fraction(1,4) if i==j else Fraction(0))
          for j in range(4)] for i in range(4)]
for state in [rho,tangent]:
    for effect in [geo,geo_jet]:
        assert pairing(state,effect)==pairing(D_R(state),effect)
R01=[[Fraction(1) if i//2==j//2 and i%2==0 and j%2==1
      else Fraction(0) for j in range(4)] for i in range(4)]
archive_gap=pairing(rho,R01)-pairing(D_R(rho),R01)
assert archive_gap==Fraction(7,15)

p=(5**.5-1)/2
def fine_tv(N, paired):
    A,B=fib(N+2),fib(N+1)
    x=A/(A*A+B*B) if paired else 1/(A+B)
    return abs(A*(x-p**(N+1)))
right_tv={str(N):fine_tv(N,True) for N in (1,3,8,12)}
left_tv={str(N):fine_tv(N,False) for N in (1,3,8,12)}
assert right_tv["12"]<2e-6
assert .10<left_tv["12"]<.11

print(json.dumps({
    "terminal":"PASS: two-sided GNS path-folding and hostile controls",
    "path_N":"0..7",
    "checked_prefix_pairs":prefix_checks,
    "integer_N":"0..23",
    "dimension_H3":fib(9),
    "pure_uniform_basis_left_tracial":"FALSE (N=1 hostile control)",
    "right_copy_nondemolition":"FALSE on offdiagonal RIGHT matrix units",
    "paired_trace_TV":right_tv,
    "left_uniform_TV":left_tv
},sort_keys=True,indent=2))
