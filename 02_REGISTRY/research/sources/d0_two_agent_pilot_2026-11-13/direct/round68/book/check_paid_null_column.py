"""Replay the six-wire anchor and its two unequal context lifts to the true scene."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import runpy

import sympy as sp


direct = Path(__file__).resolve().parents[2]
base = runpy.run_path(str(direct/"round67/check_measured_source.py"))
field, scalar = base["field"], base["scalar"]
cx, native = base["cx"], base["nt"]
p = base["p"]
port, bank, report, tail = (base[name] for name in ("port", "bank", "report", "tail"))
proj = sp.diag(1, 0, 0, 0)
mask = field(sp.kronecker_product(sp.eye(4), proj, sp.eye(4)))
mask0 = field(sp.kronecker_product(sp.eye(4), proj, sp.diag(1,1,0,0)))
mask1 = field(sp.kronecker_product(sp.eye(4), proj, sp.diag(0,0,1,0)))
for active in (cx(bank, port), cx(port, bank)):
    matrices = []
    for word in (base["identity"], base["commutator"]):
        sign = base["sign"]
        gates = (active, cx(port, report), sign, sign, *word, active,
                 cx(report, tail), native.Gate("G", (tail,)), cx(report, tail))
        full = base["full_matrix"](gates)
        incoming = full * base["incoming"]
        for marked, expected in ((mask,p**2),(mask0,p**3),(mask1,p**4)):
            columns = marked*incoming
            assert columns.transpose()*columns == scalar(expected)
        matrices.append(mask*full)
    assert matrices[0] == matrices[1]  # every incoming column, not a chosen Spin state


Z = "ABAUUABA"
P, K = Z+Z+"AA", Z+"A"+Z+"A"
alphabet = {cx(port, bank): "A", cx(bank, port): "B", base["sign"]: "U"}
assert P == "".join(alphabet[g] for g in base["identity"])
assert K == "".join(alphabet[g] for g in base["commutator"])


def windows(word, size):
    return Counter(word[i:i+size] for i in range(len(word)-size+1))


for n in (1,2,3):
    assert windows(P,n) == windows(K,n)
    assert windows("UAB"+P+"UBA",n) == windows("UAB"+K+"UBA",n)
assert windows(K,4)-windows(P,4) == {"AAAB": 1}
assert windows(P,4)-windows(K,4) == {"BAAB": 1}
assert P[:2] == K[:2] and P[-2:] == K[-2:]

zones = [0]*9 + [1]*11 + [2]*13
deg = [sum(b != a for b in zones) for a in zones]
assert sum(deg) == 718


def markov(i,j):
    if zones[i] == zones[j]:
        return F(0)
    if i == 0:
        return F(1 + int(j == 11), 25)
    return F(1, deg[i])


def edge(i,j):
    return F(2+i,2+j)*markov(i,j)/2


assert all(sum(markov(i,j) for j in range(33)) == 1 for i in range(33))
assert all(edge(i,i) == 0 for i in range(33))


def raw_path(word, contextual, transfer):
    result = F(1)
    for i,g in enumerate(word):
        target = {"A":9,"B":10,"U":20}[g]
        if contextual and g == "B" and word[max(0,i-3):i] == "AAA":
            target = 11
        result *= transfer(0,target)*transfer(target,0)
    return result


assert raw_path(P,False,edge) == raw_path(K,False,edge)
for transfer in (edge,markov):
    ratio = raw_path(K,True,transfer)/raw_path(P,True,transfer)
    assert ratio**2 == 4

# Noncommuting repeatable operations, complete faithful input and filter.
C = sp.Matrix([[2,1],[0,1]])
Zop = sp.Matrix([[1,0],[1,3]])
words = (C*C*Zop*Zop, C*Zop*C*Zop)
prep = sp.diag(2,1)/3
filter_ = sp.Matrix([[1,1],[0,1]])
outputs = [filter_*w*prep*w.T*filter_.T for w in words]
totals = [o.trace() for o in outputs]
assert totals[0] != totals[1] and outputs[0].det() == outputs[1].det()
normalized = [o / z for o,z in zip(outputs,totals)]
assert normalized[0].det()/normalized[1].det() == (totals[1]/totals[0])**2
assert scalar(1 - 4*p**3) == scalar(p**6)
assert F(619,1000)**6 < F(1,10) and F(619,1000)**2+F(619,1000) > 1
assert F(3,5)**2 + F(3,5) < 1 and F(3,4)**2 < F(3,5)
assert 2*F(3,5)*F(9,20)*F(99,100) > F(1,2)
assert F(3,5)**2/8 > F(1,24)
D = sp.diag(1,0)
terminal = sp.Matrix([[4,1],[1,3]])/6
eta = sp.Rational(1,3)
assert terminal*D != D*terminal
assert (terminal-eta*sp.eye(2)).is_positive_definite
assert (terminal-eta*D).is_positive_definite and (eta*D).is_positive_semidefinite
assert terminal-eta*D+eta*D == terminal
print("PASS: identical terminal 00 blocks, p^2/p^3/p^4 on both preparations, "
      "three-letter tariff invariance, 36-edge contrast, determinant scale recovery.")
