"""Exact B121 repetition, retaining the full regular Q8 basis and every WORK record."""
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path
import sympy as sp

owner = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "primary" / "B121" / "RESULT.json"
report = json.loads(owner.read_text())
paths = report["chronological_paths_by_initial_port_and_target"]["G_Z_G_Z"]
assert report["native_words"]["G_Z_G_Z"]["expanded_stages"] == 18
assert set(paths) == {"00", "01", "10", "11"}
for address, rows in paths.items():
    x = int(address[1])
    assert len(rows) == 4
    assert sorted(row["central_class"] for row in rows if row["terminal_target"] == x) == [1, 1]
    assert sorted(row["central_class"] for row in rows if row["terminal_target"] != x) == [-1, 1]

def full_step(vector, A, d):
    # Central translation g -> gz exchanges the two four-element sheets.
    return [A[y] * vector[8*y+g] +
            d[1-y] * (vector[8*(1-y)+g] + vector[8*(1-y)+(g^4)])
            for y in range(2) for g in range(8)]

def mass(vec):
    return sum((x*x for x in vec), vec[0]*0)

def compare(A, d, literal=None, depth=5):
    zero, one = A[0]*0, A[0]/A[0]
    for i in range(2):
        v = [zero]*16
        v[8*i] = one
        histories = [v]
        coherent_wrong, measured_wrong = [], []
        even_amplitude = [one if i==j else zero for j in range(2)]
        even_mass = list(even_amplitude)
        for n in range(depth+1):
            half = one/(one+one)
            odd = A[i]**(2*n)
            full_mass = mass(v)
            recorded_mass = sum((mass(h) for h in histories), zero)
            wrong_indices = slice(8*(1-i), 8*(2-i))
            coherent_wrong.append(mass(v[wrong_indices]))
            measured_wrong.append(sum((mass(h[wrong_indices]) for h in histories), zero))
            assert full_mass == half*(mass(even_amplitude)+odd)
            assert recorded_mass == half*(sum(even_mass)+odd)
            if literal is not None:
                p = literal
                assert full_mass == (one+p**(12*n))*half**2 + half*odd
                assert recorded_mass == half*(((one+p**12)*half)**n + odd)
            if n==depth:
                break
            v = full_step(v,A,d)
            next_histories = []
            for h in histories:
                out = full_step(h,A,d)
                for j in range(2):
                    next_histories.append([amp if k//8==j else zero for k,amp in enumerate(out)])
            histories = next_histories
            even_amplitude = [A[j]*even_amplitude[j]+2*d[1-j]*even_amplitude[1-j]
                              for j in range(2)]
            even_mass = [A[j]**2*even_mass[j]+(2*d[1-j])**2*even_mass[1-j]
                         for j in range(2)]
        tr_b = A[0]+A[1]
        det_b = A[0]*A[1]-4*d[0]*d[1]
        tr_t = A[0]**2+A[1]**2
        det_t = (A[0]*A[1])**2-16*(d[0]*d[1])**2
        assert coherent_wrong[1] == measured_wrong[1] == 2*d[i]**2
        assert coherent_wrong[2]/coherent_wrong[1] == tr_b**2
        assert coherent_wrong[3]/coherent_wrong[1] == (tr_b**2-det_b)**2
        assert measured_wrong[2]/measured_wrong[1] == tr_t
        assert measured_wrong[3]/measured_wrong[1] == tr_t**2-det_t

compare([F(4,7),F(2,5)],[F(1,9),F(2,11)],depth=6)
K = sp.QQ.algebraic_field(sp.sqrt(5))
p = K.from_sympy((sp.sqrt(5)-1)/2)
A = p**2+p**4
d = p**3
assert A+2*d == K.one and A-2*d == p**6
compare([A,A],[d,d],literal=p,depth=8)
print("PASS: B121 class table, full regular Q8 propagation, both WORK inputs,"
      " asymmetric rational tariff and exact golden weights, every measured history through n=8.")
print("B121 RESULT sha256", hashlib.sha256(owner.read_bytes()).hexdigest())
