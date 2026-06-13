#!/usr/bin/env python3
"""vp_q8_dedekind_minimality.py - D0 certificate (exact finite group enumeration)

CLAIM (THE): the role group Omega8 is FORCED to be the quaternion group Q8, not
chosen. M1 forbids a catalog of conjugate copies, so every subgroup must be
normal (Hamiltonian); order-preserving records force non-abelian. Among the
non-abelian groups of order <= 8 only Q8 is Hamiltonian:
    S3 (order 6): 3 non-normal subgroups
    D4 (order 8): 4 non-normal subgroups
    Q8 (order 8): 0 non-normal subgroups   <- unique minimal Hamiltonian non-abelian
By Dedekind (1897) every Hamiltonian group contains Q8, so this minimality is
global. Triple identity: [Q8,Q8] = Z(Q8) = Phi(Q8) = {+-1} (one Z2).
Exact: no floats, explicit multiplication tables.
"""
from itertools import product, combinations


def build(elements, mul, ident):
    """Return (idx, table, inv, e) for a finite group given elements + mul."""
    idx = {e: i for i, e in enumerate(elements)}
    n = len(elements)
    table = [[idx[mul(a, b)] for b in elements] for a in elements]
    e = idx[ident]
    inv = [next(j for j in range(n) if table[i][j] == e) for i in range(n)]
    return idx, table, inv, e


def subgroups(table, inv, e):
    n = len(table)

    def closure(gens):
        s = {e}
        frontier = [e] + list(gens)
        s.update(gens)
        changed = True
        while changed:
            changed = False
            cur = list(s)
            for a in cur:
                for b in cur:
                    x = table[a][b]
                    if x not in s:
                        s.add(x); changed = True
        return frozenset(s)

    subs = {frozenset({e})}
    elems = list(range(n))
    for r in (1, 2):
        for combo in combinations(elems, r):
            subs.add(closure(combo))
    return subs


def is_normal(H, table, inv, n):
    return all(table[table[g][h]][inv[g]] in H for g in range(n) for h in H)


def count_non_normal(elements, mul, ident):
    idx, table, inv, e = build(elements, mul, ident)
    n = len(elements)
    subs = subgroups(table, inv, e)
    proper = [H for H in subs if 1 < len(H) < n]   # exclude {e} and whole group
    non_normal = [H for H in proper if not is_normal(H, table, inv, n)]
    return len(non_normal), n, idx, table, inv, e


# --- Q8 via quaternion multiplication on +-1, +-i, +-j, +-k ---
def qmul(x, y):
    (a, b, c, d), (e, f, g, h) = x, y
    return (a*e - b*f - c*g - d*h,
            a*f + b*e + c*h - d*g,
            a*g - b*h + c*e + d*f,
            a*h + b*g - c*f + d*e)
Q8 = [(1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,-1,0,0),(0,0,1,0),(0,0,-1,0),(0,0,0,1),(0,0,0,-1)]

# --- S3 as permutations of (0,1,2) ---
from itertools import permutations as _perm
S3 = list(_perm((0,1,2)))
def pmul(x, y):  # (x after y): (x*y)(i) = x[y[i]]
    return tuple(x[y[i]] for i in range(len(x)))

# --- D4 as the 8 symmetries of a square (permutations of 4 corners) ---
def _gen(gens, mul, ident):
    s = {ident}
    changed = True
    while changed:
        changed = False
        for a in list(s):
            for g in gens:
                x = mul(a, g)
                if x not in s:
                    s.add(x); changed = True
    return list(s)
r = (1,2,3,0)            # rotation
sflip = (1,0,3,2)        # reflection
D4 = _gen([r, sflip], pmul, (0,1,2,3))
assert len(D4) == 8, len(D4)

nn_q8, n_q8, idx, table, inv, e = count_non_normal(Q8, qmul, (1,0,0,0))
nn_s3, *_ = count_non_normal(S3, pmul, (0,1,2))
nn_d4, *_ = count_non_normal(D4, pmul, (0,1,2,3))

assert (n_q8, nn_q8) == (8, 0), (n_q8, nn_q8)
assert nn_s3 == 3, nn_s3
assert nn_d4 == 4, nn_d4
print(f"[1] non-normal proper subgroups: S3={nn_s3}, D4={nn_d4}, Q8={nn_q8}  PASS")
print("    => Q8 is the unique Hamiltonian non-abelian group of order <= 8 (Dedekind 1897)  PASS")

# --- Triple identity [Q8,Q8] = Z(Q8) = Phi(Q8) = {+-1} ---
n = 8
# commutator subgroup
def comm(g, h):
    return table[table[inv[g]][inv[h]]][table[g][h]]
gen_comm = {comm(g, h) for g in range(n) for h in range(n)}
# closure of commutators
def closure_set(seed):
    s = set(seed); s.add(e); changed = True
    while changed:
        changed = False
        for a in list(s):
            for b in list(s):
                x = table[a][b]
                if x not in s:
                    s.add(x); changed = True
    return frozenset(s)
commutator_sub = closure_set(gen_comm)
center = frozenset(z for z in range(n) if all(table[z][g] == table[g][z] for g in range(n)))
# Frattini = intersection of maximal subgroups
subs = subgroups(table, inv, e)
maximal = [H for H in subs if len(H) < n and not any(len(H) < len(K) < n for K in subs)]
frattini = frozenset(set.intersection(*[set(H) for H in maximal])) if maximal else frozenset({e})
pm1 = frozenset({idx[(1,0,0,0)], idx[(-1,0,0,0)]})

assert commutator_sub == pm1, commutator_sub
assert center == pm1, center
assert frattini == pm1, frattini
print("[2] EXACT: [Q8,Q8] = Z(Q8) = Phi(Q8) = {+-1} (one Z2)  PASS")

print("\n[STATUS] THE: Omega8 = Q8 forced (unique minimal Hamiltonian non-abelian); triple Z2 identity.")
print("[CERT-CLOSED] PASS_Q8_DEDEKIND_MINIMALITY")
