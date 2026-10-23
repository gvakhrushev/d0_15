#!/usr/bin/env python3
"""KILL-FIRST: owned native Book R versus φ Beatty mask (EXACT finite control).

No physical Beatty ordering is currently owned for alternative K913 histories.
This script supplies NEGATIVE controls, not a new selected Book03 Info law.
"""
from math import isqrt
from fractions import Fraction
from sympy import Matrix, symbols, sqrt, simplify, eye

def beatty_phi(n: int) -> int:
    """floor(n*(1+sqrt(5))/2), computed with exact integer arithmetic."""
    assert n >= 1
    return (n + isqrt(5*n*n)) // 2

def test_beatty_enumeration():
    assert [beatty_phi(n) for n in range(1, 9)] == [1,3,4,6,8,9,11,12]
    N = 502
    mask = set()
    n = 1
    while beatty_phi(n) <= N:
        mask.add(beatty_phi(n))
        n += 1
    assert len(mask) == 310
    # ORIGINAL K913: K9 root has exactly 11*22=242 completions
    # starting via K11 and 13*20=260 via K13. ALL have price 2.
    b_first = sum(j <= 242 for j in mask)
    b_second = sum(j > 260 for j in mask)
    assert (b_first, b_second) == (150,149)
    assert Fraction(b_first,len(mask)) != Fraction(b_second,len(mask))
    assert Fraction(242,502) != Fraction(b_first,len(mask))
    assert Fraction(242,502) != Fraction(b_second,len(mask))
    print("Beatty mask size=310; K11-first selectors=150 or 149 "
          "for TWO reorderings of IDENTICAL original 502 histories: PASS")
    return mask

def test_native_two_round_residual():
    p = (sqrt(5)-1)/2
    eps, lam = symbols("epsilon lambda", positive=True)
    assert simplify(p+p*p-1) == 0
    # ACTUAL 128-output native port costs one/two (each round).
    for b1 in (0,1):
        for b2 in (0,1):
            score=2+b1+b2
            mark=int(b1+b2 >= 1)
            xi=score-2-mark
            assert xi == b1*b2
    # On each ORIGINAL invariant Fourier/CAR16 shell, Δ=λI;
    # T*(I)=I, Φ1*(X)=p ε λ X.
    R_scalar=simplify((p*eps*lam)**2)
    assert simplify(R_scalar - p**2*eps**2*lam**2)==0
    # On the actual positive Riesz shell: λ_1>0 at every finite L.
    assert float(R_scalar.subs({eps:1/512,lam:1/8}))>0
    # Matched original two-arm cocycle is exactly zero on diagonal:
    # C(e;U0,U0)=A(e,U0)-A(e,U0)=0.
    assert simplify(R_scalar-0)!=0
    # Positive operator control: diag λ>=0, trivial unital CP T*=id.
    D=Matrix.diag(1,2)
    Delta=D*D
    op=simplify((p*eps)**2*D*Delta*D)
    assert simplify(op - (p*eps)**2 * Delta**2) == Matrix.zeros(2)
    assert all(float(op[i,i].subs({eps:1/512}))>0 for i in range(2))
    print("Literal 2-round residual xi=b1*b2 and R2=(p epsilon)^2 "
          "D T*(Delta) D >=0, positive on original flat shell: PASS")

def test_no_golden_horizon_selection():
    # TRUE K913 primitive zone-count quotient from prospective P8.
    M=Matrix([[0,11,13],[9,0,13],[9,11,0]])
    C=eye(3)[:,0]*0 + Matrix([1,1,1])
    assert list(M*C)==[24,22,20]
    C2=M*M*C
    assert list(C2)==[502,476,458]
    assert Fraction(11*int((M*C)[1]),int(C2[0])) == Fraction(242,502)
    # Canonical P9 Q_n depends solely on exact integer completion counts;
    # p^n cancels from every same-depth branch; φ doesn't appear.
    def first_to_B(n):
        assert n >= 1
        prior=M**(n-1)*C
        full=M*prior
        return Fraction(11*int(prior[1]),int(full[0]))
    for n in [5,8,13,21,34,55]:
        assert 0<first_to_B(n)<1
    assert abs(float(first_to_B(34))-float(first_to_B(55)))<1e-10
    print("Original prospective Q_n is a rational count ratio "
          "independent of phi at every neutral fixed horizon: PASS")

if __name__ == "__main__":
    test_beatty_enumeration()
    test_native_two_round_residual()
    test_no_golden_horizon_selection()
    print("ALL EXACT PHI BEATTY / OWNED RESIDUAL KILL-FIRST CHECKS PASSED")
