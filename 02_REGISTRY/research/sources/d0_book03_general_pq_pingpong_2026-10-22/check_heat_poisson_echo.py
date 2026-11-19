#!/usr/bin/env python3
"""Exact positive Poisson-echo heat kernel from a genuine coarse P/Q return.

Math theorem: original full128 port supplies one-step heat B=I-alpha Delta.
Its N-step P/Q echo survival is B^N even for fully curved noncommuting Delta.
Poisson(beta/alpha) mixture returns exp(-beta Delta) exactly, and its
first trace-source. This is NOT a proof of preserving ALL fine 128 history
labels when echo uncomputes the instrument work; literal repeated CP has Gamma.
"""
import sympy as s
from functools import reduce
from mpmath import mp

D=6;q=s.Rational
P=s.diag(1,1,1,0,0,0)
Q=s.diag(1,0,0,1,1,0) # NOT complement of P: tests the general two-projector theorem.

def rot(i,j,a,b):
    out=s.eye(D);out[i,i]=out[j,j]=a;out[i,j]=-b;out[j,i]=b;return out
U=reduce(lambda x,y:x*y,[
  rot(0,3,q(3,5),q(4,5)),rot(1,4,q(5,13),q(12,13)),
  rot(2,5,q(3,5),q(4,5)),rot(0,1,q(3,5),q(4,5)),
  rot(1,5,q(5,13),q(12,13))],s.eye(D))
assert U.T*U==s.eye(D)
V=Q*U*P
B=V.T*V
assert B==P*U.T*Q*U*P
assert B==B.T and B[:3,:3]!=s.diag(*[B[i,i] for i in range(3)])
T=P
for n in range(1,13):
    T=(Q*U if n%2 else P*U.T)*T
    assert T.T*T==B**n
print('PASS general Q != I-P projected U/Udagger echo: all noncommuting heat powers B^n exact')

mp.dps=80
alpha=mp.mpf('0.1');beta=mp.mpf('0.35');mu=beta/alpha
Bm=mp.matrix([[mp.mpf(str(s.N(B[i,j],80))) for j in range(3)] for i in range(3)])
Id=mp.eye(3);Delta=(Id-Bm)/alpha
exact=mp.expm(-beta*Delta)
for K in (15,25,40):
    mat=mp.zeros(3)
    weight=mp.exp(-mu)
    power=Id
    poiss_cdf=mp.mpf(0)
    for n in range(0,K+1):
        mat+=weight*power
        poiss_cdf+=weight
        weight=weight*mu/(n+1)
        power=power*Bm
    err=max(abs(mat[i,j]-exact[i,j]) for i in range(3) for j in range(3))
    assert err<1-poiss_cdf+mp.mpf('1e-60')
    print('PASS exact Poisson heat operator via finite echo K',K,'component err',mp.nstr(err,12),'tail',mp.nstr(1-poiss_cdf,12))

# FULL field derivative with D Delta noncommuting with Delta; original heat
# first trace source is -beta Tr exp(-beta Delta) D Delta EXACTLY.
X=s.zeros(D)
for i,j,v in ((0,4,q(2,7)),(1,3,q(1,3))):X[i,j]=-v;X[j,i]=v
DB=P*U.T*(X.T*Q+Q*X)*U*P
DM=mp.matrix([[mp.mpf(str(s.N(DB[i,j],80))) for j in range(3)] for i in range(3)])
DDelta=-DM/alpha
lhs=beta*sum((exact*DM)[i,i] for i in range(3))/alpha
rhs=-beta*sum((exact*DDelta)[i,i] for i in range(3))
assert abs(lhs-rhs)<mp.mpf('1e-70')
tailK=40
series=mp.mpf(0);w=mp.exp(-mu);power=Id
for n in range(0,tailK):
    series+=mu*w*sum((power*DM)[i,i] for i in range(3))
    power=power*Bm
    w*=mu/(n+1)
assert abs(series-rhs)<mp.mpf('1e-22')
print('PASS literal original heat trace variation is Poisson mixture of noncommuting P/Q echo survival FIRST derivatives')
print('SCOPE: original 128 fine-labeled CP archive would add Gamma unless coherent echo label discipline proved; full HJR/G0/GR OPEN')
