#!/usr/bin/env python3
"""W8 Charge B verification: the holomorph pair (L_i, alpha=(ijk)) on C[Q8] carries BOTH
the (1,4,3) Fourier isotypes AND the (4,3) terminal return cycles, with E0 the common
fixed block. Exact rational arithmetic; exits 1 on any failure.
Basis order {1,i,j,k,-1,-i,-j,-k} matching D0/UnifiedFiniteCore/Q8Terminal.lean."""
from fractions import Fraction
import sys

names = ['1','i','j','k','-1','-i','-j','-k']
def mul(a, b):
    sa, xa = (1 if a<4 else -1), a%4
    sb, xb = (1 if b<4 else -1), b%4
    T = {(0,0):(1,0),(0,1):(1,1),(0,2):(1,2),(0,3):(1,3),
         (1,0):(1,1),(1,1):(-1,0),(1,2):(1,3),(1,3):(-1,2),
         (2,0):(1,2),(2,1):(-1,3),(2,2):(-1,0),(2,3):(1,1),
         (3,0):(1,3),(3,1):(1,2),(3,2):(-1,1),(3,3):(-1,0)}
    s, x = T[(xa,xb)]; s *= sa*sb
    return x if s==1 else x+4

assert mul(1,2)==3 and mul(2,1)==7  # i*j=k, j*i=-k

def Lmat(g):
    M = [[0]*8 for _ in range(8)]
    for h in range(8): M[mul(g,h)][h] = 1
    return M
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
def madd(A,B,c=1): return [[A[i][j]+c*B[i][j] for j in range(8)] for i in range(8)]
def msca(c,A): return [[c*A[i][j] for j in range(8)] for i in range(8)]
def eq(A,B): return all(A[i][j]==B[i][j] for i in range(8) for j in range(8))
I8 = [[1 if i==j else 0 for j in range(8)] for i in range(8)]

E0 = msca(Fraction(1,8), [[1]*8 for _ in range(8)])
E4 = msca(Fraction(1,2), madd(I8, Lmat(4), -1))
E3 = madd(msca(Fraction(1,2), madd(I8, Lmat(4))), E0, -1)

def alpha_idx(g):
    s, x = (0 if g<4 else 4), g%4
    return s + (x if x==0 else (x%3)+1)
Pa = [[0]*8 for _ in range(8)]
for g in range(8): Pa[alpha_idx(g)][g] = 1
PaT = [list(r) for r in zip(*Pa)]
conj = lambda M: mm(mm(Pa,M),PaT)

def chi_idem(axis):
    M = [[Fraction(0)]*8 for _ in range(8)]
    for g in range(8):
        ch = 1 if (g%4==0 or g%4==axis) else -1
        Lg = Lmat(g)
        for a in range(8):
            for b in range(8): M[a][b] += Fraction(ch,8)*Lg[a][b]
    return M
eB, eC, eD = chi_idem(1), chi_idem(2), chi_idem(3)

Li = Lmat(1); L2 = mm(Li,Li); L4 = mm(L2,L2)
Pa3 = mm(mm(Pa,Pa),Pa)
sub = [0,1,4,5]
Umu_lit = [[0,0,0,1],[1,0,0,0],[0,1,0,0],[0,0,1,0]]  # TerminalReturn.Umu verbatim

checks = {
 "alpha preserves E0": eq(conj(E0), E0),
 "alpha preserves E4": eq(conj(E4), E4),
 "alpha preserves E3": eq(conj(E3), E3),
 "eB+eC+eD = E3": eq(madd(madd(eB,eC),eD), E3),
 "alpha 3-cycles eB->eC->eD->eB": eq(conj(eB),eC) and eq(conj(eC),eD) and eq(conj(eD),eB),
 "L_i order exactly 4": eq(L4,I8) and not eq(L2,I8),
 "L_i | <i>-span == Umu literal": [[Li[a][b] for b in sub] for a in sub] == Umu_lit,
 "alpha^3 = id": eq(Pa3,I8),
 "E0 fixed by L_i (electron = common fixed block)": eq(mm(Li,E0), E0),
 # block-typing signatures (feed the type-keyed matching, T2' scene half):
 # E4 = the UNIQUE block where translation has order exactly 4 (L_-1 acts as -1 there);
 # on E0+E3 translation has order <= 2 (L_-1 acts as +1); E0 = the unique both-fixed block.
 "typing: L_-1 E4 = -E4 (translation order exactly 4 on E4)": eq(mm(Lmat(4),E4), msca(-1,E4)),
 "typing: L_-1 (E0+E3) = +(E0+E3) (translation order <= 2 off E4)": eq(mm(Lmat(4),madd(E0,E3)), madd(E0,E3)),
 "typing: alpha preserves E4 but is not identity on it": eq(mm(Pa,E4), mm(E4,Pa)) and not eq(mm(Pa,E4), E4),
 # 13-leg (representation-home) checks: functions on the role-square classes {±1},{±i},{±j},{±k}
 # embed in C[Q8] exactly as the ±-pair symmetrizer = E0+E3; this home is orthogonal to E4,
 # and role classes are ill-defined on E4 (L_-1 = -1 there forces f(-g) = -f(g)).
 "13-leg: E0+E3 = half(I+L_-1) (the C[ABCD] projector, definitional)": eq(madd(E0,E3), msca(Fraction(1,2), madd(I8, Lmat(4)))),
 "13-leg: trace of the C[ABCD] projector = |ABCD| = 4": sum(madd(E0,E3)[i][i] for i in range(8)) == 4,
 "13-leg: (E0+E3) E4 = 0 (role-class home orthogonal to E4)": eq(mm(madd(E0,E3), E4), [[Fraction(0)]*8 for _ in range(8)]),
 # 11-leg bonus: Q8 has a UNIQUE 2-element subgroup {1,-1} (unique involution), so a dyad
 # embedded as a subgroup is forced to be the structural Z2; its antisymmetric character
 # lives exactly in the L_-1 = -1 sector = E4.
 "11-leg: -1 is the unique involution of Q8": [g for g in range(8) if g != 0 and mul(g,g) == 0] == [4],
}
# alpha is a genuine algebra automorphism: it intertwines the regular representation,
# P_a L_g P_a^-1 = L_{alpha(g)} for ALL g. The bare i<->j swap is NOT an automorphism
# (i*j=k but j*i=-k) and must fail this intertwining for some g, even though it happens
# to permute the character idempotents (those only see +/- cosets, not the full table).
checks["alpha intertwines regular rep: P L_g P^-1 = L_alpha(g), all g"] = all(
    eq(mm(mm(Pa, Lmat(g)), PaT), Lmat(alpha_idx(g))) for g in range(8))
Pbad = [[0]*8 for _ in range(8)]
swap = {0:0,1:2,2:1,3:3,4:4,5:6,6:5,7:7}
for g in range(8): Pbad[swap[g]][g] = 1
PbadT = [list(r) for r in zip(*Pbad)]
checks["negative control: i<->j swap fails regular-rep intertwining"] = not all(
    eq(mm(mm(Pbad, Lmat(g)), PbadT), Lmat(swap[g])) for g in range(8))

ok = True
for k,v in checks.items():
    print(("PASS " if v else "FAIL ")+k); ok = ok and v
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
