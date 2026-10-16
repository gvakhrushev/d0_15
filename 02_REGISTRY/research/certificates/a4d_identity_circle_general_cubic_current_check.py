#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""General cubic current on one physical resonance-circle envelope.

This lifts the all-period Boolean sign calculation to ordinary commuting real
envelope amplitudes r_n.  It reuses the literal shared-link jet, exact even
Laurent inverses, and the certified finite left witness.  No Fourier scan is
performed.

The output is the exact local cubic polynomial obtained after:
  1. inserting the general circle center field with envelope r_n,
  2. solving both even quadratic connection blocks by their exact Laurent
     inverses,
  3. forming the positive-q cubic joint source,
  4. applying the all-period left witness L(T).

Reducing r_n^2 -> 1 recovers the owned Boolean obstruction i*T*epsilon/4.
"""
from __future__ import annotations

from fractions import Fraction as F
import sympy as sp
import numpy as np

import a4d_identity_circle_sign_cubic_gate_check as C
import a4d_identity_physical_resonance_circles_check as P


class Poly:
    """Sparse commutative Q-polynomial in finitely many shifted amplitudes r_n."""
    def __init__(self, d=None):
        self.d = {}
        for mon, val in (d or {}).items():
            v = F(val)
            if v:
                key = tuple(sorted(mon))
                self.d[key] = self.d.get(key, F(0)) + v
        self.d = {k:v for k,v in self.d.items() if v}

    @classmethod
    def of(cls, v):
        return v if isinstance(v, cls) else cls({(): v})

    @classmethod
    def eps(cls, n):
        return cls({(int(n),): F(1)})

    def __bool__(self):
        return bool(self.d)

    def __neg__(self):
        return Poly({k:-v for k,v in self.d.items()})

    def __add__(self, other):
        other = self.of(other)
        d = self.d.copy()
        for k,v in other.d.items():
            d[k] = d.get(k, F(0)) + v
        return Poly(d)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-self.of(other))

    def __rsub__(self, other):
        return self.of(other) - self

    def __mul__(self, other):
        other = self.of(other)
        d = {}
        for k,v in self.d.items():
            for l,w in other.d.items():
                mon = tuple(sorted(k+l))
                d[mon] = d.get(mon, F(0)) + v*w
        return Poly(d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * (F(1) / F(other))

    def shift(self, j):
        j = int(j)
        return Poly({tuple(i+j for i in mon):v for mon,v in self.d.items()})

    def boolean_reduce(self):
        """Quotient by r_n^2=1, retaining parity of every exponent."""
        out = {}
        for mon,v in self.d.items():
            counts = {}
            for i in mon:
                counts[i] = counts.get(i,0)+1
            key = tuple(sorted(i for i,n in counts.items() if n % 2))
            out[key] = out.get(key,F(0))+v
        return Poly(out)

    def sympy(self):
        ids = sorted({i for mon in self.d for i in mon})
        syms = {i:sp.Symbol("r"+("m"+str(-i) if i<0 else str(i)), real=True)
                for i in ids}
        out = 0
        for mon,v in self.d.items():
            term = sp.Rational(v.numerator,v.denominator)
            for i in mon:
                term *= syms[i]
            out += term
        return sp.factor(out)


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name, flush=True)


def main():
    # The imported functions resolve BP dynamically from their module globals.
    # Replace only the coefficient algebra; literal face/jet assembly is reused.
    C.BP = Poly
    C.leading.cache_clear()

    # Linear circle field is an exact joint kernel for arbitrary envelope.
    for q in range(4):
        k,v = C.source(q,1)
        check(f"GENERAL_ENVELOPE_LINEAR_ZERO_Q{q}",
              not any(k) and not any(v))

    # Exact period-independent quadratic range solve.
    fk = [C.source(q,2)[0] for q in (0,1)]
    correction = C.correct((fk[0]+fk[1])/2, (fk[0]-fk[1])/2)

    # Verify complete degree-two joint cancellation after that correction.
    for q in range(4):
        k,v = C.source(q,2,correction)
        check(f"GENERAL_ENVELOPE_QUADRATIC_CONNECTION_ZERO_Q{q}", not any(k))
        # The metric part is the known quadratic envelope gate and need not
        # vanish off its cone, so it is retained rather than asserted zero.

    sources = []
    for q in range(4):
        k,v = C.source(q,3,correction)
        sources.append(np.concatenate([k,v]))

    # Positive q Fourier source S=(source_q0 - i source_q1)/2.
    # Apply L(T)=sum_{j=0}^2 L_j T^j directly in real space.
    left = [[P.QI() for _ in range(34)] for _ in range(3)]
    for power,row,re,im in C.LEFT_WITNESS:
        left[power][row] = P.QI(F(re),F(im))

    wre, wim = Poly(), Poly()
    for power,row in enumerate(left):
        for r,l in enumerate(row):
            if not l:
                continue
            s0 = sources[0][r].shift(power)
            s1 = sources[1][r].shift(power)
            wre += (l.re*s0 + l.im*s1)/2
            wim += (l.im*s0 - l.re*s1)/2

    check("GENERAL_CUBIC_WITNESS_REAL_PART_BOOLEAN_ZERO",
          not wre.boolean_reduce())
    target = Poly.eps(1)/4
    check("GENERAL_CUBIC_WITNESS_BOOLEAN_REDUCES_TO_I_T_EPS_OVER4",
          wim.boolean_reduce().d == target.d)

    # The current is homogeneous cubic and local.
    check("GENERAL_CUBIC_WITNESS_HOMOGENEOUS_DEGREE3",
          all(len(mon)==3 for mon in wre.d) and
          all(len(mon)==3 for mon in wim.d))
    support = sorted({i for p in (wre,wim) for mon in p.d for i in mon})
    check("GENERAL_CUBIC_WITNESS_FINITE_SHIFT_SUPPORT",
          support and support[0] >= -8 and support[-1] <= 8)

    print("WITNESS_REAL", wre.sympy(), flush=True)
    print("WITNESS_IMAG", wim.sympy(), flush=True)
    print("SHIFT_SUPPORT", support, flush=True)
    print("MONOMIAL_COUNTS", len(wre.d), len(wim.d), flush=True)
    print("RESULT A4D-IDENTITY-CIRCLE-GENERAL-CUBIC-CURRENT-EXACT", flush=True)


if __name__ == "__main__":
    main()
