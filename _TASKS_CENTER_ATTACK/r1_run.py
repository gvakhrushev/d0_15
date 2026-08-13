#!/usr/bin/env python3
"""R1 run — executes the FROZEN criterion (_TASKS_CENTER_ATTACK/R1_FROZEN_CRITERION.md,
commit f6e315e) against d0_gap_labels.json. First data contact."""
import json, math, random
from fractions import Fraction

PHI = (1 + math.sqrt(5)) / 2
ALPHA = 1 / PHI  # ids = (n + m*alpha) mod 1

data = json.load(open("d0_gap_labels.json"))
# discover structure minimally
if isinstance(data, dict):
    keys = list(data.keys())
    print("top-level keys:", keys)
    plats = data.get("plateaux") or data.get("plateaus") or data.get("labels") or data
else:
    plats = data
print("n plateaux:", len(plats))
print("sample entry:", json.dumps(plats[0]) if isinstance(plats, list) else "dict")

entries = []
for d in plats:
    n, m = d["k0_label"]["n"], d["k0_label"]["m"]
    ids = d["ids"]
    entries.append((ids, n, m))
entries.sort()
N = len(entries)

# exact gap arithmetic in the module: gap between consecutive = (dn + dm*alpha) mod 1,
# represented exactly by the integer pair (dn, dm) adjusted so value lies in (0,1)
def exact_val(n, m):
    return n + m * ALPHA

def norm_pair(dn, dm):
    # shift dn by integers so that value in (0,1)
    v = exact_val(dn, dm)
    k = math.floor(v)
    return (dn - k, dm)

gaps = []
for i in range(N):
    a = entries[i]
    b = entries[(i + 1) % N]
    dn, dm = b[1] - a[1], b[2] - a[2]
    if i == N - 1:
        dn += 1  # wrap around the circle
    gaps.append(norm_pair(dn, dm))

distinct = sorted(set(gaps), key=lambda p: exact_val(*p))
print(f"\nR1a: {len(distinct)} distinct exact gap values (as (dn,dm) pairs):")
for p in distinct:
    print(f"  (dn={p[0]}, dm={p[1]})  value={exact_val(*p):.9f}  count={gaps.count(p)}")

r1a_three = len(distinct) == 3
r1a_sum = False
if r1a_three:
    S1, S2, L = distinct
    r1a_sum = (S1[0] + S2[0] == L[0]) and (S1[1] + S2[1] == L[1])
    print(f"L = S1 + S2 exactly in module: {r1a_sum}")
print("R1a data outcome:", "PASS-a" if (r1a_three and r1a_sum) else "FAIL-a")

# R1b: reflection triples in consecutive sorted triples (non-circular interior)
T = 0
for i in range(1, N - 1):
    _, n0, m0 = entries[i - 1]
    _, n1, m1 = entries[i]
    _, n2, m2 = entries[i + 1]
    if n2 == 2 * n1 - n0 and m2 == 2 * m1 - m0:
        T += 1
print(f"\nR1b: reflection triples T = {T} / {N-2}")

# Null controls, seed frozen
rng = random.Random(20260814)
ns = [e[1] for e in entries]; ms = [e[2] for e in entries]
nlo, nhi, mlo, mhi = min(ns), max(ns), min(ms), max(ms)
null_pass_a = 0
null_T = []
TRIALS = 10000
for _ in range(TRIALS):
    seen = set(); pts = []
    while len(pts) < N:
        n = rng.randint(nlo, nhi); m = rng.randint(mlo, mhi)
        v = exact_val(n, m) % 1.0
        key = (round(v, 12))
        if key in seen:
            continue
        seen.add(key); pts.append((v, n, m))
    pts.sort()
    g = []
    for i in range(N):
        a, b = pts[i], pts[(i + 1) % N]
        dn, dm = b[1] - a[1], b[2] - a[2]
        if i == N - 1:
            dn += 1
        g.append(norm_pair(dn, dm))
    ds = set(g)
    if len(ds) == 3:
        s1, s2, l = sorted(ds, key=lambda p: exact_val(*p))
        if s1[0] + s2[0] == l[0] and s1[1] + s2[1] == l[1]:
            null_pass_a += 1
    t = 0
    for i in range(1, N - 1):
        if (pts[i+1][1] == 2*pts[i][1] - pts[i-1][1]
                and pts[i+1][2] == 2*pts[i][2] - pts[i-1][2]):
            t += 1
    null_T.append(t)

frac_a = null_pass_a / TRIALS
null_T.sort()
p99 = null_T[int(0.99 * TRIALS)]
print(f"\nNull N-a: fraction of null sets passing R1a = {frac_a:.4f} (control fires iff < 0.01)")
print(f"Null R1b: 99th percentile of T = {p99}; data T = {T}; PASS-b iff T > p99: {T > p99}")

print("\n=== FROZEN ADJUDICATION ===")
if frac_a >= 0.01:
    print("R1a: CONTROL-FAIL (criterion uninformative)")
else:
    print("R1a:", "PASS" if (r1a_three and r1a_sum) else "FAIL", "(control fired)")
print("R1b (secondary):", "PASS-b" if T > p99 else "FAIL-b")
