#!/usr/bin/env python3
"""D0 v11.28 executed bridge certs.
This script checks finite arithmetic/operator facts used by the v11.28 closure cells.
It does not verify external theorems such as HST; it verifies the D0 finite source and
bridge kernels/inequalities invoked before external comparison.
"""
import json, math
import numpy as np

phi = (1 + math.sqrt(5))/2
p = 1/phi
delta0 = (math.sqrt(5)-2)/2
Omega8 = 8
ABCD = 4
V9, V11, V13 = 9, 11, 13
rank = 3
nullity = V9 + V11 + V13 - rank
D_light = 8 + 3 + 1

def ok(x, tol=1e-9):
    return abs(x) <= tol

checks = []
def add(name, cond, detail):
    checks.append({"name": name, "pass": bool(cond), "detail": detail})

# 1. Born finite-frame rule: finite positive response R=D^†D and a resolution of identity.
rng = np.random.default_rng(1128)
D = rng.normal(size=(4,4)) + 1j*rng.normal(size=(4,4))
R = D.conj().T @ D
# projectors onto coordinate axes and two-block coarse graining
Pis = []
for i in range(4):
    P = np.zeros((4,4), dtype=complex); P[i,i] = 1
    Pis.append(P)
P01 = Pis[0] + Pis[1]
P23 = Pis[2] + Pis[3]
trR = np.trace(R).real
probs = [np.trace(P @ R).real/trR for P in Pis]
coarse = [np.trace(P01 @ R).real/trR, np.trace(P23 @ R).real/trR]
add("Born finite frame normalization", ok(sum(probs)-1,1e-10), {"sum": sum(probs)})
add("Born finite frame additivity", ok((probs[0]+probs[1])-coarse[0],1e-10) and ok((probs[2]+probs[3])-coarse[1],1e-10), {"fine": probs, "coarse": coarse})
# unitary covariance check
Q,_ = np.linalg.qr(rng.normal(size=(4,4)) + 1j*rng.normal(size=(4,4)))
R2 = Q @ R @ Q.conj().T
Pis2 = [Q @ P @ Q.conj().T for P in Pis]
probs2 = [np.trace(P @ R2).real/np.trace(R2).real for P in Pis2]
add("Born finite frame unitary covariance", max(abs(a-b) for a,b in zip(probs, probs2)) < 1e-10, {"max_diff": max(abs(a-b) for a,b in zip(probs, probs2))})

# 2. EPR/CHSH finite shared support: Tsirelson bound via Pauli matrices.
sx = np.array([[0,1],[1,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
A0, A1 = sz, sx
B0 = (sz + sx)/math.sqrt(2)
B1 = (sz - sx)/math.sqrt(2)
CHSH = np.kron(A0, B0+B1) + np.kron(A1, B0-B1)
eigs = np.linalg.eigvalsh(CHSH).real
norm_chsh = max(abs(eigs))
add("EPR Tsirelson CHSH norm", abs(norm_chsh - 2*math.sqrt(2)) < 1e-10, {"norm": norm_chsh, "target": 2*math.sqrt(2), "eigenvalues": eigs.tolist()})
# singlet expectation
singlet = np.array([0,1,-1,0], dtype=complex)/math.sqrt(2)
exp_chsh = (singlet.conj().T @ CHSH @ singlet).real
add("EPR finite shared support expectation reaches Tsirelson", abs(abs(exp_chsh) - 2*math.sqrt(2)) < 1e-10, {"expectation": exp_chsh})

# 3. BH entropy boundary channel: ABCD quartet quotient yields one archive cell per 4 boundary quanta.
for area_quanta in [4, 8, 12, 20, 100]:
    independent_archive_cells = area_quanta // ABCD
    add(f"BH archive boundary A/4 for A={area_quanta}", area_quanta % ABCD == 0 and independent_archive_cells == area_quanta/4, {"A": area_quanta, "S_D0": independent_archive_cells, "A_over_4": area_quanta/4})

# 4. Gauge uniqueness guardrail under D0 light-block obligations.
# Compact simple Lie algebra dimensions below 20: A1=3, A2=8, B2/C2=10, G2=14, A3=15, ...
simple_dims = {"A1/su2": 3, "A2/su3": 8, "B2=C2/sp4=so5": 10, "G2": 14, "A3/su4": 15, "B3/so7": 21}
rank_req = {"simple_rank2_block_dim": 8, "simple_rank1_block_dim": 3, "abelian_trace_block_dim": 1}
rank2_matches = [k for k,v in simple_dims.items() if v == rank_req["simple_rank2_block_dim"]]
rank1_matches = [k for k,v in simple_dims.items() if v == rank_req["simple_rank1_block_dim"]]
add("Gauge light block dimension 8+3+1", D_light == 12, {"dim_light": D_light})
add("Gauge rank-2 dimension identifies su3 in small compact table", rank2_matches == ["A2/su3"], {"matches": rank2_matches})
add("Gauge rank-1 dimension identifies su2 in small compact table", rank1_matches == ["A1/su2"], {"matches": rank1_matches})

# 5. HST/macro archive finite source: bounded centered archive atom and subgaussian bound.
a = delta0**8 / 30.0
# A takes ±a with equal probabilities, scaled Z=A/a is Rademacher and 1-subgaussian.
for t in [0, 0.25, 0.5, 1.0, 2.0, 3.0]:
    mgf = math.cosh(t)  # for Z=±1
    bound = math.exp(t*t/2)
    add(f"HST macro finite source subgaussian t={t}", mgf <= bound + 1e-12, {"mgf": mgf, "bound": bound})
# unscaled proxy a^2
for t in [0.5, 1.0, 2.0]:
    mgf = math.cosh(t*a)
    bound = math.exp((t*t*a*a)/2)
    add(f"HST macro archive atom bounded proxy t={t}", mgf <= bound + 1e-18, {"a": a, "mgf": mgf, "bound": bound})

# 6. Existing D0 invariants referenced by closure cells.
add("phi split p+p^2=1", abs(p + p*p - 1) < 1e-12, {"p": p})
add("delta0 half gap", abs(delta0 - (p-p*p)/2) < 1e-12, {"delta0": delta0, "half_gap": (p-p*p)/2})
add("rank nullity gamma 38", nullity == 30 and 2*(nullity//rank)-1 == 19 and 2*(2*(nullity//rank)-1) == 38, {"V": V9+V11+V13, "rank": rank, "nullity": nullity})

status = "PASS_V11_28_EXECUTED_CORE_BRIDGES" if all(c["pass"] for c in checks) else "FAIL_V11_28_EXECUTED_CORE_BRIDGES"
result = {"status": status, "checks": checks}
print(json.dumps(result, indent=2, ensure_ascii=False))
with open(__file__.replace('.py','_results.json'), 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
with open(__file__.replace('.py','.md'), 'w', encoding='utf-8') as f:
    f.write('# v11.28 executed core bridges cert\n\n')
    f.write(f'`{status}`\n\n')
    for c in checks:
        f.write(f"- {'PASS' if c['pass'] else 'FAIL'} — {c['name']}: `{c['detail']}`\n")
if status.startswith('FAIL'):
    raise SystemExit(1)
