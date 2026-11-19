"""Check addressed CX words, recoverable records and all masks of the A82 apparatus."""
from collections import Counter
from itertools import product
from math import comb

import sympy as sp


def cx_run(bits, gates):
    out = list(bits)
    for control, target in gates:
        out[target] ^= out[control]
    return tuple(out)


def toggle(source, enabled):
    # 0=old Y, 1=x, 2=y, 3=u, 4=t. Restore u even on a nonzero input.
    a, b = (source, 3), (3, 4)
    return (a,b,a,b) if enabled else (a,a,b,b)


def switches(mask):
    alpha, beta = mask
    return toggle(1, alpha) + toggle(0, beta)


def loss_and_read(old, flags, mask):
    x, y = flags
    alpha, beta = mask
    g = y ^ (alpha & x) ^ (beta & old)
    bank = [x, y, x, g]
    for lost in range(4):
        out = bank.copy()
        moved = out[lost]
        out[lost] = 0       # SWAP into a fresh sharp cell, moved is archived.
        if lost % 2 == 0:
            out[lost] ^= out[2-lost]
        else:
            out[lost] ^= out[4-lost]
            # Apply exactly the addressed switch rule with the surviving x.
            out[lost] = cx_run([old, out[0], 0, 0, out[lost]], switches(mask))[4]
        assert out == bank and out[lost] == moved
    assert (bank[2], bank[3] ^ (alpha & bank[2]) ^ (beta & old)) == flags
    return sum(1+i for i in bank)


def main():
    masks = list(product(range(2), repeat=2))
    assert all(Counter(switches(m)) == Counter(switches(masks[0])) for m in masks)
    for bits in product(range(2), repeat=5):
        old, x, y, u, t = bits
        for a,b in masks:
            assert cx_run(bits, switches((a,b))) == (old,x,y,u,t^(a&x)^(b&old))
    outcomes = ((0,0),(0,1),(1,0))
    for old in (0,1):
        for m in masks:
            for flags in outcomes:
                loss_and_read(old, flags, m)
    printed = {m: [loss_and_read(1, o, m) for o in outcomes] for m in masks}
    assert printed[(0,0)] == [4,6,6]
    assert printed[(1,0)] == [4,6,7]
    assert printed[(1,1)] == [5,5,6]
    for m in masks:
        # Future actually prints the recovered original x,y rather than just promising it.
        extra = [2+sum(o) for o in outcomes]
        assert extra[2] - extra[1] == 0

    p = (sp.sqrt(5)-1)/2
    eta = sp.expand(1-sp.chebyshevt(6, sp.expand(p**3))**2)
    assert (eta-p).is_positive
    probs = [1-eta, sp.expand(eta*p), sp.expand(eta*p**2)]
    cost = {m: sp.expand(sum(a*b for a,b in zip(lengths, probs)))
            for m,lengths in printed.items()}
    assert all((cost[m]-cost[(1,1)]).is_positive for m in masks if m != (1,1))
    assert sp.expand(cost[(1,1)]-cost[(0,0)] - (1-eta*(1+p))) == 0

    # Verify factorization without floating point or exponential symbolic polynomials.
    # The two powers of p on each active nonempty mask sum to a unit, p+p^2=1.
    assert sp.expand(p+p**2) == 1
    assert sp.expand(p+2*p**2 - (1+p**2)) == 0
    t = sp.Symbol("eta")
    leaves = 0
    for n in range(1,9):
        # For every efficiency: the mean number of successes is n*t and the
        # one-off printed exponent on a revealed bit has mean 1+p^2.
        mass = [comb(n,m)*t**m*(1-t)**(n-m) for m in range(n+1)]
        assert sp.expand(sum(m*prob for m,prob in enumerate(mass)) - n*t) == 0
        assert sp.expand(sum(mass[1:]) - 1 + (1-t)**n) == 0
        for mask in product(range(2), repeat=n):
            hits = sum(mask)
            for old in (0,1):
                powers = []
                base = 4*n+2*hits+2
                for b in ((0,1) if old and hits else (0,)):
                    xs = [old*b*t for t in mask]
                    ys = [t-x for t,x in zip(mask,xs)]
                    h, d = int(old and any(mask)), int(any(xs))
                    # A selected terminal copies the true old Y or a true zero.
                    assert (old if h else 0) == h and (old if d else 0) == d
                    length = sum(4+2*(x+y) for x,y in zip(xs,ys)) + 2+h+d
                    powers.append(length-base)
                    leaves += 1
                assert powers == ([1,2] if old and hits else [0])
    print("PASS all addressed CX columns, both banks, four lost slots, four extensions")
    print(f"eta={float(eta):.12f}; length-field difference={float(1-eta*(1+p)):.12f}")
    print(f"PASS two final records, {leaves} full leaves, n=1..8, equal sector weights")


if __name__ == "__main__":
    main()
