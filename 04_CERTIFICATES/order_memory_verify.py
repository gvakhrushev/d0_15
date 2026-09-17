#!/usr/bin/env python3
"""Independent exact arithmetic for the finite order-memory construction.

Run from any directory. Requires SymPy; reads the current Lean matrix/table
definitions and writes verification.json beside this file. No experimental data.
"""
from pathlib import Path
from cert_runtime import output_path
import hashlib
import json
import re
import sympy as S

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SOURCES = {
    "q8": ROOT / "03_FORMALIZATION/D0/Claims/Q8DedekindMinimality.lean",
    "memory": ROOT / "03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean",
    "golden": ROOT / "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean",
    "terminal": ROOT / "03_FORMALIZATION/D0/UnifiedFiniteCore/Q8Terminal.lean",
}
texts = {key: path.read_text() for key, path in SOURCES.items()}
checks = []


def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)


def equal(a, b):
    if isinstance(a, S.MatrixBase):
        return all(S.simplify(x) == 0 for x in a - b)
    return S.simplify(a - b) == 0


def matrix_after(text, marker):
    body = text.split(marker, 1)[1].split("!![", 1)[1].split("]", 1)[0]
    return S.Matrix([[S.sympify(x) for x in row.split(",")] for row in body.split(";")])


body = texts["q8"].split("def Q8 :", 1)[1].split("/-- Symmetric", 1)[0]
rows = re.findall(r"!\[([\d, ]+)\]", body.split("e :=", 1)[0])
table = [list(map(int, row.split(","))) for row in rows]
inverse = list(map(int, re.search(r"inv := !\[([^]]+)\]", body)[1].split(",")))
check("source table shape", len(table) == 8 and all(len(row) == 8 for row in table))
left = matrix_after(texts["memory"], "def left")
a, b, c, d = S.symbols("a b c d")
spin_body = texts["memory"].split("def spin :", 1)[1].split("theorem spin_multiplicative", 1)[0]
coordinates = re.findall(r"left\s+([0-9() -]+?)(?=,|\])", spin_body)
quadruples = [list(map(int, re.findall(r"-?\d+", entry))) for entry in coordinates]
check("source spin shape", len(quadruples) == 8 and all(len(q) == 4 for q in quadruples))
spin = [left.subs(dict(zip((a, b, c, d), q))) for q in quadruples]
regular = [S.Matrix(8, 8, lambda r, col: int(r == table[g][col])) for g in range(8)]
turn = matrix_after(texts["memory"], "def complexTurn")
to_spin = matrix_after(texts["memory"], "def toSpin")
E4 = matrix_after(texts["terminal"], "def E4 :")
order_sector = (S.eye(8) - regular[1]) / 2
perm = [0, 2, 4, 6, 1, 3, 5, 7]

for g in range(8):
    check(f"inverse/reversal {g}", spin[inverse[g]] == spin[g].T)
    check(f"norm conservation {g}", spin[g].T * spin[g] == S.eye(4))
    check(f"commuting complex turn {g}", turn * spin[g] == spin[g] * turn)
    check(f"regular-to-spin intertwiner {g}", to_spin * regular[g] == spin[g] * to_spin)
    for h in range(8):
        check(f"spin multiplication {g},{h}", spin[table[g][h]] == spin[g] * spin[h])
        check(f"regular multiplication {g},{h}", regular[table[g][h]] == regular[g] * regular[h])
check("eight distinct spin images", len({tuple(m) for m in spin}) == 8)
check("quarter-turn squares to minus identity", turn * turn == -S.eye(4))
check("spin does not retain all algebra sums", spin[0] + spin[1] == S.zeros(4))
check("onto spin carrier", to_spin * to_spin.T == 2*S.eye(4))
check("spin projection metric", to_spin.T * to_spin == 2*order_sector)
check("existing E4 recovered with basis permutation", order_sector.extract(perm, perm) == E4)
coeff = S.symbols("c0:8")
memory = sum((coeff[g] * regular[g] for g in range(8)), S.zeros(8))
check("all algebra coefficients recovered", memory[:, 0] == S.Matrix(coeff))

# Complex coordinates are an explicit repackaging of rational pairs.
pack = S.Matrix([[1, S.I, 0, 0], [0, 0, 1, -S.I]])
rho_i = S.diag(S.I, -S.I)
rho_j = S.Matrix([[0, -1], [1, 0]])
check("complex packaging of i", pack * spin[2] == rho_i * pack)
check("complex packaging of j", pack * spin[4] == rho_j * pack)
check("internal quarter-turn becomes scalar i", pack * turn == S.I * pack)
loop = spin[2] * spin[4] * spin[inverse[2]] * spin[inverse[4]]
check("closed order word gives minus identity", loop == -S.eye(4))

v = S.Matrix(S.symbols("x0:4", real=True))
norm = lambda w: (w.T*w)[0]
check("isolated central sign invisible", equal(norm(v), norm(loop*v)))
check("reference plus port becomes zero", (v + loop*v)/2 == S.zeros(4, 1))
check("reference minus port recovers input", (v - loop*v)/2 == v)
w = S.Matrix(S.symbols("y0:4", real=True))
check("comparison conserves normalized response", equal(norm((v+w)/2)+norm((v-w)/2), (norm(v)+norm(w))/2))

# Use the EXISTING golden splitter instead of adding a balanced splitter.
p = (S.sqrt(5)-1)/2
B = S.Matrix([[S.sqrt(p), -p], [p, S.sqrt(p)]])
check("golden splitter is orthogonal", equal(B.T*B, S.eye(2)))
out_plus = B.T*B*S.Matrix([1, 0])
out_minus = B.T*S.diag(1, -1)*B*S.Matrix([1, 0])
check("golden identity loop returns", equal(out_plus, S.Matrix([1, 0])))
check("golden order-loop amplitudes", equal(out_minus, S.Matrix([p**3, -2*p*S.sqrt(p)])))
check("golden order-loop normalized weights", equal(out_minus[0]**2, p**6) and equal(out_minus[1]**2, 4*p**3))
check("golden weights sum to one", equal(p**6+4*p**3, 1))

# Negative control: erase coherence BETWEEN the arms before recombination.
# The central sign then cancels from each block: both orders have the same result.
prepared = B*S.Matrix([1, 0])
dephased = S.diag(prepared[0]**2, prepared[1]**2)
dephased_minus = S.diag(1, -1)*dephased*S.diag(1, -1)
check("without reference coherence the sign is lost", dephased_minus == dephased)
incoherent_out = B.T*dephased*B
check("incoherent second port weight", equal(incoherent_out[1, 1], 2*p**3))

result = {
    "status": "PASS",
    "scope": "Exact finite representation and conditional quadratic detector protocol; no experimental validation.",
    "checks_passed": len(checks),
    "checks": checks,
    "source_sha256": {str(SOURCES[k].relative_to(ROOT)): hashlib.sha256(t.encode()).hexdigest() for k, t in texts.items()},
    "golden_readout": {
        "identity_second_port": 0,
        "order_loop_second_port_exact": "4*phi^(-3)",
        "order_loop_second_port": float(4*p**3),
        "both_dephased_second_port": float(2*p**3),
        "single_run_false_negative": float(p**6),
        "four_independent_prepared_runs_false_negative": float(p**24),
    },
}
output_path(__file__, "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
print(json.dumps({k: v for k, v in result.items() if k not in ("checks", "source_sha256")}, ensure_ascii=False, indent=2))
