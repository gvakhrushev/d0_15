"""Exact G1--G6 clock, written in the last birth basis (v,v-perp)."""
from collections import Counter
from fractions import Fraction
from math import factorial
import json

D = 16  # ordinary port, ordinary helper, quaternion Spin


def gate(name, state):
    p, b, s = state >> 3, (state >> 2) & 1, state & 3
    if name == "C":
        return (p << 3) + ((p ^ b) << 2) + s, 1
    if name == "S" and p:
        # Left i on (1,i,j,k).
        return (p << 3) + (b << 2) + (s ^ 1), 1 if s % 2 == 0 else -1
    return state, 1


def spectrum_cycles(prefix, pre, post):
    word = prefix + pre + "J" + post
    birth = word.index("J") + 1
    n = len(word)
    states = {(j, t, k) for j in range(n)
              for t in range(1 + (j >= birth)) for k in range(D)}
    jump = {}
    for j, t, k in states:
        kp, sign = gate(word[j], k)
        jp = j+1 if j+1 < n else (0, birth)[t]
        jump[j,t,k] = ((jp,t,kp),sign)
    assert set(dest for dest, _ in jump.values()) == states
    cycles = Counter()
    while states:
        x0 = x = next(iter(states))
        length, phase = 0, 1
        while x in states:
            states.remove(x)
            x, sig = jump[x]
            phase *= sig
            length += 1
        assert x == x0
        cycles[length,phase] += 1
    return cycles


def trace(cycles, n):
    return sum(m * length * sign**(n//length)
               for (length,sign),m in cycles.items() if n % length == 0)


prefixes = ["", "S", "CCS", "SCSCS", "SCCCSSCCSCSSS"]
for prefix in prefixes:
    ca = spectrum_cycles(prefix, "SS", "CCSS")
    cb = spectrum_cycles(prefix, "CC", "SSSS")
    for n in range(1, 161):
        assert trace(ca,n)-trace(cb,n) == (-4*D if n % 8 == 4 else 0)
    assert Counter("SSCCSS") == Counter("CCSSSS")

# Rigorous margins replacing the infinite CT7 geometric tail in the rotating probe.
x = Fraction(2,55)
exp_upper = 1/(1-x)
assert exp_upper - 1 < Fraction(1,25)
print(json.dumps(dict(prefixes=len(prefixes), exact_moments_per_prefix=160,
                      carrier_before_last_birth=D, last_birth_age=4,
                      winding_delta_n4=-4*D, winding_delta_n8=0,
                      CT7_relative_tail_upper=str(exp_upper-1)), indent=2))
