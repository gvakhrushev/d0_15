#!/usr/bin/env python3
"""R-A1 run — executes the FROZEN criterion of A1_A2_ACQUISITION_2026_08_14.md (commit
02413ce, BEFORE data contact) on the hash-pinned Potapov-Ong 2017 results.csv.

R-A1: is record fidelity a scalar or a vector? Normalize each sample's 12 off-diagonal
substitution counts to a probability vector. PASS iff mean between-enzyme JSD / mean
within-enzyme JSD = R >= 2.0, null control (10000 enzyme-label permutations, seed
20260814) fires iff permuted R >= 2.0 in < 1%.
R-A1b (secondary, declared underpowered): Deep Vent exo+/exo- JSD vs 99th pct of
within-enzyme replicate JSDs.
"""
import csv, math, random, hashlib, sys

CSV_PATH = "08_PASSPORTS/_EXTERNAL_DATA_CACHE/polymerase_fidelity/results.csv"
PIN = "25b2918010072ab486d782dc172316831fabb4e3862fe3308f35d569303675af"
CELLS = ["AC","AT","AG","CA","CT","CG","TA","TC","TG","GA","GC","GT"]

raw = open(CSV_PATH, "rb").read()
assert hashlib.sha256(raw).hexdigest() == PIN, "results.csv hash mismatch vs manifest pin - ABORT"

rows = list(csv.DictReader(open(CSV_PATH, newline="")))
samples = []
for r in rows:
    counts = [int(r[c]) for c in CELLS]
    tot = sum(counts)
    if tot == 0:
        print(f"sample {r['SampleID']} ({r['Enzyme']}) has zero substitution errors - excluded, recorded")
        continue
    samples.append({"enzyme": r["Enzyme"], "p": [c / tot for c in counts], "id": r["SampleID"]})
print(f"{len(samples)} samples with nonzero substitution counts, {len(set(s['enzyme'] for s in samples))} enzymes")

def kl(p, q):
    s = 0.0
    for a, b in zip(p, q):
        if a > 0:
            s += a * math.log(a / b)
    return s

def jsd(p, q):
    m = [(a + b) / 2 for a, b in zip(p, q)]
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)

def ratio_R(labels):
    within, between = [], []
    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            d = jsd(samples[i]["p"], samples[j]["p"])
            (within if labels[i] == labels[j] else between).append(d)
    return (sum(between) / len(between)) / (sum(within) / len(within)), within, between

labels = [s["enzyme"] for s in samples]
R, within, between = ratio_R(labels)
print(f"mean within-enzyme JSD  = {sum(within)/len(within):.6f}  (n={len(within)} pairs)")
print(f"mean between-enzyme JSD = {sum(between)/len(between):.6f}  (n={len(between)} pairs)")
print(f"R = {R:.4f}  (PASS threshold >= 2.0)")

rng = random.Random(20260814)
TRIALS = 10000
exceed = 0
for _ in range(TRIALS):
    perm = labels[:]
    rng.shuffle(perm)
    r_perm, _, _ = ratio_R(perm)
    if r_perm >= 2.0:
        exceed += 1
null_rate = exceed / TRIALS
print(f"null: {exceed}/{TRIALS} permutations reach R >= 2.0 (rate {null_rate:.4f}; control fires iff < 0.01)")

# R-A1b secondary: Deep Vent exo+ vs exo- (enzyme names per samples.csv)
dv = [s for s in samples if s["enzyme"].lower().replace(" ", "") in ("deepvent", "deepvent(exo-)", "deepventexo-")]
names = sorted(set(s["enzyme"] for s in samples))
print(f"enzymes present: {names}")
dv_plus = [s for s in samples if "deep vent" == s["enzyme"].lower()]
dv_minus = [s for s in samples if "exo" in s["enzyme"].lower() and "vent" in s["enzyme"].lower()]
if dv_plus and dv_minus:
    cross = [jsd(a["p"], b["p"]) for a in dv_plus for b in dv_minus]
    wsorted = sorted(within)
    p99 = wsorted[int(0.99 * len(wsorted))]
    print(f"R-A1b: mean exo+/exo- JSD = {sum(cross)/len(cross):.6f}; within-enzyme 99th pct = {p99:.6f}; "
          f"selective iff mean cross > p99: {sum(cross)/len(cross) > p99}")
else:
    print("R-A1b: Deep Vent pair not matched by name heuristic - listing enzymes above; adjudicate manually")

print("\n=== FROZEN ADJUDICATION (R-A1) ===")
if null_rate >= 0.01:
    print("CONTROL-FAIL: criterion uninformative on this data (recorded)")
else:
    print("R-A1:", "PASS - fidelity is a VECTOR (channel-specific loss)" if R >= 2.0
          else "FAIL - scalar parameterization vindicated", "(control fired)")
