"""Exact Bernstein readout on two separately prepared groups of N original records."""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb

import sympy as sp


P, q = sp.symbols("P q", real=True)
p = (sp.sqrt(5)-1)/2


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def basis(n, i, x):
    return comb(n,i)*x**i*(1-x)**(n-i)


def coefficients(f, n):
    # x^r = sum_i choose(i,r)/choose(n,r) times the i-th Bernstein basis polynomial.
    terms = sp.Poly(f,P,q).terms()
    return [[sum(value*sp.Rational(comb(i,r),comb(n,r))*sp.Rational(comb(j,s),comb(n,s))
                 for (r,s),value in terms if r<=i and s<=j)
             for j in range(n+1)] for i in range(n+1)]


def mean_and_derivatives(b, n):
    # Enumerate the raw Bernoulli strings before replacing them by counts.
    counts = Counter((sum(word[:n]),sum(word[n:])) for word in product((0,1),repeat=2*n))
    check(all(counts[i,j]==comb(n,i)*comb(n,j) for i in range(n+1) for j in range(n+1)),
          "two independent preparations per trial count")
    avg = sum(count*b[i][j]*P**i*(1-P)**(n-i)*q**j*(1-q)**(n-j)
              for (i,j),count in counts.items())
    dp = sum(n*(b[i+1][j]-b[i][j])*basis(n-1,i,P)*basis(n,j,q)
             for i in range(n) for j in range(n+1))
    dq = sum(n*(b[i][j+1]-b[i][j])*basis(n,i,P)*basis(n-1,j,q)
             for i in range(n+1) for j in range(n))
    return avg, dp, dq


def reused_records(n):
    # y=19 has port 1. Categories on the same original shot have probabilities
    # outside port 1, inside port 1 but y!=19, and y=19, respectively.
    law = (1-P,P-q,q)
    wrong = 0
    for word in product(range(3), repeat=n):
        mass = sp.prod(law[label] for label in word)
        ports = sum(label!=0 for label in word)
        fine = word.count(2)
        wrong += mass*sp.Rational(ports*fine,n*n)
    check(sp.expand(wrong-P*q-q*(1-P)/n)==0,"exact same-shot covariance")


def choose_k(n, epsilon):
    if n<1 or epsilon<=0:
        raise ValueError("positive Bernstein degree and tolerance required")
    # p<2/3, hence this rational stopping test works at every positive tolerance.
    k = 0
    bound = Fraction(10*n)
    while bound >= epsilon:
        k += 1
        bound *= Fraction(2,3)
    return k


def verify_quantization(b, n, epsilon):
    k = choose_k(n,epsilon)
    delta = sp.expand(5*p**k)
    largest = max(max(row) for row in b)
    # A common independent k-zero event can thin all repetitions on a count
    # at once. Each then contributes -5*p^k in expectation.
    copies = [[sp.floor(sp.radsimp((largest-v)/delta)) for v in row] for row in b]
    errors = [[sp.expand(largest-delta*copies[i][j]-b[i][j]) for j in range(n+1)]
              for i in range(n+1)]
    check(all(c.is_Integer and c>=0 for row in copies for c in row),"physical repetitions")
    check(all(0<=e<delta for row in errors for e in row),"one common exact Golden mesh")
    # Each derivative is a convex combination of N times adjacent coefficient
    # differences. This checks the standard 2*N*delta sup-norm bound for either
    # coordinate. One-sided rounding here actually gives N*delta.
    px = [errors[i+1][j]-errors[i][j] for i in range(n) for j in range(n+1)]
    qx = [errors[i][j+1]-errors[i][j] for i in range(n+1) for j in range(n)]
    check(all(-2*n*delta<n*e<2*n*delta for e in px+qx),"two uniform derivative bounds")
    check(sp.expand(2*n*delta)<epsilon,"requested global precision")
    return k


def main():
    n = 3
    f = (sp.Rational(2,7)+3*P/5-4*q/9+P*q/2-2*P**2*q/3+5*P*q**2/11+q**3/17)
    b = coefficients(f,n)
    val, dp, dq = mean_and_derivatives(b,n)
    for observed, wanted in zip((val,dp,dq),(f,f.diff(P),f.diff(q))):
        check(sp.expand(observed-wanted)==0,"exact nonseparable polynomial and full differential")
    point = {P:sp.Rational(1,7),q:sp.Rational(1,13)}
    check(f.diff(P,q)!=0 and dp.subs(point)!=0 and dq.subs(point)!=0,"two effective record coordinates")
    reused_records(n)
    eps = Fraction(1,25)
    k = verify_quantization(b,n,eps)
    check(choose_k(n,Fraction(1,10**16))>k,"arbitrary tighter tolerance")
    # Separate prices: the deterministic switch (1,0) and (-5,-5) span two axes.
    check(sp.Matrix([[1,-5],[0,-5]]).det()==-5,"independence of the two archive transfers")
    print("PASS on 2N=6 genuine count slots; f and both source rows agree exactly.")
    print(f"dP={dp.subs(point)}, dq={dq.subs(point)}; shared-shot bias=q(1-P)/{n}.")
    print(f"For epsilon={eps}, k={k} certifies both uniform derivative errors < epsilon.")


if __name__=="__main__":
    main()
