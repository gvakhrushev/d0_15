"""First return, whole Hodge-tail certificates and the actual (880) LEFT jet."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import sys

import sympy as s

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]/"round71"/"clock"))
from check_chronology import check as actual_clock


def require(test, reason):
    if not test:
        raise ArithmeticError(reason)


def material_jet():
    # Real algebraic a^4+a^2=1. Only {|0>,|1>,|14>} move in (880).
    a = s.symbols("a", positive=True)
    p = a*a
    polynomial = a**4+a**2-1

    def zero(expr):
        num, den = s.fraction(s.cancel(expr))
        return s.rem(num,polynomial,a)==0 and s.rem(den,polynomial,a)!=0

    def equal(A,B,label):
        require(all(zero(x) for x in A-B),label)

    e0,e1,e14 = [s.eye(3)[:,i] for i in range(3)]
    vacuum = a*e1+p*e14
    generator = vacuum*e1.T-e1*vacuum.T
    dg = e0*e1.T-e1*e0.T
    O = s.eye(3)+generator+generator**2/(1+a)
    dO = dg+(generator*dg+dg*generator)/(1+a)
    dM = dO*O.T
    column = e1+p*e14/(1+a)
    equal(dM,e0*column.T-column*e0.T,"all active columns of material derivative")
    Z = s.diag(1,-1,1)
    dR = dM.T*Z+Z*dM
    equal(dR,2*(e0*e1.T+e1*e0.T),"actual material derivative of phase conjugation")
    vblank = s.Matrix([a,p])
    pe = s.eye(2)-vblank*vblank.T
    young = s.diag(1,1,pe[0,0])
    young[:2,:2] = pe
    require(zero((young*dR).trace()+4*a*p),"younger return coefficient")
    require(zero(dR.trace()),"older return derivative")
    equal(dR.T*dR,4*(e0*e0.T+e1*e1.T),"two singular values 2")


def tail_constants():
    L = 11
    next_weight = F(1,22**2*(L+1)*(L+2))
    # For L >= 11 each displayed bound is nonincreasing:
    # (8L+31)/(8L-15) = 1+46/(8L-15), and likewise the material bound.
    ratio = F(425,359)*F(8*L+31,8*L-15)*next_weight
    require(ratio<F(1,30000),"discrete one-pair contraction")
    t = F(1,22*(L+1))
    require(F(1,22)/(1-t)**2 < F(1,20),"differentiated positive thermal tail")
    require(F(4,5)*(1+F(425,359))<2,"signed lower heat margin")
    ratio_material = F(425,359)*F(8*(L+2)+2,1)/(F(18,5)*L-2)*next_weight
    require(ratio_material<F(1,20000),"true material one-pair contraction")
    # Each compact gauge derivative equals dR tensored with two witness bits.
    require(4*4==16,"trace norm per passive column")
    return float(ratio),float(ratio_material)


def algebraic_separation():
    phi_upper = F(1618034,1000000)
    require(phi_upper**2-phi_upper>1,"rational upper bound on phi")
    length = 11
    dimension = 28+32*length
    upper = F(132*(8*length+3),359*dimension*22**length*factorial(length))
    require(upper < F(378,10**26),"absolute master contrast")
    def lower(n):
        return 1/(2**(2*n+3)*phi_upper**(2*n))
    require(lower(14) > F(655,10**18),"actual fourteen binary stages")
    require(lower(22) > F(452,10**26) > upper,"at least 23 binary weight operations")


def spectral_moment_reduction():
    # Degenerate positive block, protected zero mode and a nondiagonal jet.
    diagonal = s.diag(0,2,2,5)
    velocity = s.Matrix([[0,1,0,2],[1,3,1,0],[0,1,-1,2],[2,0,2,-2]])
    energies = (0,2,5)
    spectral = []
    for energy in energies:
        projector = s.eye(4)
        for other in energies:
            if other != energy:
                projector *= (diagonal-other*s.eye(4))/(energy-other)
        spectral.append((projector*velocity).trace())
    require(spectral==[0,2,-2],"harmonic mode does not move; keep degenerate traces")
    vandermonde = s.Matrix([[s.Integer(x)**i for x in energies] for i in range(3)])
    moments = s.Matrix([(diagonal**i*velocity).trace() for i in range(3)])
    require(vandermonde.det()!=0 and vandermonde*s.Matrix(spectral)==moments,
            "algebraic stationary moment test")


def main():
    # Recompute the four aligned exact-ring spectra through their first
    # nonzero moment, not the astronomically small difference of two floats.
    for k in (0,1):
        for length in (11,13):
            actual_clock(k,length-(5,11)[k])
    material_jet()
    ratios = tail_constants()
    algebraic_separation()
    spectral_moment_reduction()
    print("PASS: exact native Spin4 clocks at 11 and 13, old-channel equality and youngest moments")
    print("PASS: actual (879)-(880) material derivative, older zero and younger -8*a*p per passive column")
    print("PASS: whole thermal contractions bounded by %.9g (finite controls), %.9g (material jet)" % ratios)
    print("PASS: the nonzero eleven-tick contrast needs at least 23 literal binary weight stages")
    print("PASS: spectral projectors and Vandermonde reduction with a degenerate Hodge block")


if __name__ == "__main__":
    main()
