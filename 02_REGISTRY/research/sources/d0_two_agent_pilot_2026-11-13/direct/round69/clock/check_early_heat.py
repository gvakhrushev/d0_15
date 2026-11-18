"""Early-slot heat on a measured H.1 clock. All branch, birth and unused columns remain."""
from functools import lru_cache
from hashlib import sha256
import importlib.util
from math import exp, factorial
from pathlib import Path
import sys

import numpy as np
from scipy import sparse as ss

root = Path(__file__).resolve().parents[7]
path = root / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
assert sha256(path.read_bytes()).hexdigest() == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = importlib.util.spec_from_file_location("clock_native", path)
nt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)
p, a = float(nt.P), float(nt.A)
beta = 2*p*p


@lru_cache(None)
def gate(bits, operation, wires, prime):
    letter = nt.Gate(operation, wires)
    program = nt.Execution(bits, (), (), (letter,), nt.G_CX_SOURCE_I, 2, (0, 1))
    matrix = nt.gate_matrix(program, letter, max_qubits=8)
    table = matrix.todok()
    rows, cols = zip(*table.keys())
    residue = {1:1, -1:-1, nt.A:5, -nt.A:-5, nt.P:3, -nt.P:-3}
    values = [residue[x] for x in table.values()] if prime else [float(x) for x in table.values()]
    return ss.csr_matrix((values, (rows, cols)),
                         shape=(2**bits, 2**bits))


class Clock:
    def __init__(self, prime):
        self.prime = prime
        self.dtype = np.int64 if prime else float
        self.dims = [4]
        self.children = [[]]
        self.last = {}

    def edge(self, parent, reference, actual):
        child = len(self.dims)
        self.dims.append(reference.shape[0])
        self.children.append([])
        self.children[parent].append((child, reference.astype(self.dtype).tocsr(), actual.astype(self.dtype).tocsr()))
        return child

    def birth(self, parent):
        vector = [[5], [3]] if self.prime else [[a], [p]]
        born = ss.kron(ss.eye(self.dims[parent], dtype=self.dtype), np.array(vector))
        return self.edge(parent, born, born)

    def raw(self, parent, operation, wires):
        dim = self.dims[parent]
        return self.edge(parent, ss.eye(dim, dtype=self.dtype), gate(dim.bit_length()-1, operation, wires, self.prime))

    def router(self, parent, labels):
        return [self.edge(parent, ss.diags((labels == i).astype(self.dtype)), ss.diags((labels == i).astype(self.dtype)))
                for i in range(max(labels)+1)]

    def terminal(self, parent):
        node = self.birth(parent)
        bits = self.dims[node].bit_length()-1
        pair = (2, bits-1)
        leaf = self.raw(node, "CX", pair)
        self.last[leaf] = gate(bits, "CX", pair, self.prime)
        return leaf

    def close(self):
        offsets = np.cumsum([0] + self.dims)
        dimension = offsets[-1]
        slots = []
        for n, dim in enumerate(self.dims):
            idx = np.arange(dim)
            slots.append(ss.csr_matrix((np.ones(dim, dtype=self.dtype), (idx, idx+offsets[n])),
                                       shape=(dim, dimension)))
        passive = {}
        rows = {}
        for node in reversed(range(len(slots))):
            if node in self.last:
                passive[node] = self.last[node] @ slots[node]
            else:
                children = self.children[node]
                passive[node] = sum(ref.T @ passive[child] for child, ref, _ in children)
                for child, ref, run in children:
                    rows[child] = run @ slots[node] + passive[child] - ref @ passive[node]
        rows[0] = passive[0]
        tick = ss.vstack([rows[i] for i in range(len(rows))], format="csr")
        if self.prime:
            assert tick.dtype == np.int64
            tick.data %= self.prime
        error = (tick.T @ tick - ss.eye(dimension, dtype=self.dtype)).tocsr()
        if self.prime:
            assert np.all(error.data % self.prime == 0)
        else:
            assert np.max(np.abs(error.data), initial=0.0) < 2e-13
        return tick, slots


def build_clock(pairs, reverse, prime=0):
    assert prime in (0,11)
    clock = Clock(prime)
    port = clock.birth(0)
    flag = clock.birth(port)
    early, active = clock.router(flag, np.arange(16) % 2)
    early_leaf = clock.terminal(early)
    # Source Spin wires 0,1; port 2; immutable flag 3; WORK 4, report 5, tail 6.
    node = clock.birth(active)
    for _ in range(2*pairs):
        node = clock.raw(node, "CX", (2, 4))
    node = clock.birth(clock.birth(node))
    acted = (4, 2) if reverse else (2, 4)
    word = [("CX", acted), ("CX", (2, 5)), ("SourceI", (2, 0, 1)),
            ("SourceI", (2, 0, 1)), ("CX", acted), ("CX", (5, 6)),
            ("G", (6,)), ("CX", (5, 6))]
    for kind, wires in word:
        node = clock.raw(node, kind, wires)
    low = np.arange(128) % 4
    for child in clock.router(node, np.where(low < 2, 0, low - 1)):
        clock.terminal(child)
    return clock, early_leaf


def make_clock(pairs, reverse, prime=0):
    clock, early_leaf = build_clock(pairs, reverse, prime)
    t, slots = clock.close()
    # Original prepared Spin on the early leaf: actual endpoint is the identity CX pair.
    born = [5,3] if prime else [a,p]
    j = np.kron(np.eye(4, dtype=clock.dtype), np.kron(born, np.kron([1,0], born))[:, None])
    return t, slots[early_leaf], j


def early_moments(tick, slot, j, count, prime=0):
    columns = (slot.T @ j)
    result = []
    for _ in range(count+1):
        value = j.T @ (slot @ columns)
        result.append(value % prime if prime else value)
        columns = tick @ columns
        if prime:
            columns %= prime
    return np.asarray(result)


def spatial_taylor(order):
    # Fourier coefficients of the degree-order Taylor polynomial; 2n+1 points suffice.
    groups = np.repeat([0, 1, 2], [9, 11, 13])
    adj = (groups[:,None] != groups[None,:]).astype(float)
    radius = 1 / np.sqrt(np.sum(adj, axis=1) + 2)
    scene = radius[:,None] * adj * radius[None,:]
    angles = 2*np.pi*np.arange(2*order+1)/(2*order+1)
    samples = []
    for theta in angles:
        vals = np.linalg.eigvalsh(scene + 2*np.diag(radius**2)*np.cos(theta))
        series = np.polynomial.polynomial.polyval(vals, [beta**i/factorial(i) for i in range(order+1)])
        samples.append(np.sum(series)*exp(-beta))
    return np.fft.fft(samples).real / len(samples)


if __name__ == "__main__":
    pairs = 6
    degree = 2*pairs
    clocks = [make_clock(pairs, reverse) for reverse in (False, True)]
    moments = [early_moments(t, s, j, 80) for t, s, j in clocks]
    diffs = np.max(np.abs(moments[0] - moments[1]), axis=(1,2))
    assert np.max(diffs[:degree+1]) < 2e-13
    first = next((i for i, err in enumerate(diffs) if err > 1e-9), None)
    # a=5, p=3 solve the integral defining relations mod 11: a^2=p, p+p^2=1.
    assert 5**2 % 11 == 3 and (3 + 3**2) % 11 == 1
    mod = [early_moments(*make_clock(pairs, reverse, 11), 32, 11) for reverse in (False, True)]
    residue = (mod[0][32] - mod[1][32]) % 11
    assert np.all(residue == np.eye(4, dtype=int)*residue[0,0]) and residue[0,0] != 0
    coeff = spatial_taylor(degree)
    trace = np.trace(moments[0], axis1=1, axis2=2)
    local_heat = 359*4 + 2*(coeff[0]*trace[0] + 2*np.dot(coeff[1:degree+1], trace[1:degree+1]))
    absolute_error = 66*4 * beta**(degree+1)/factorial(degree+1)
    log_error = 2*exp(2*beta)*beta**(degree+1)/factorial(degree+1)
    print(f"PASS full branch matrices (D={clocks[0][0].shape[0]}) and all-column RC unitarity")
    print(f"earliest numerically different prepared moment through 80: {first}")
    print(f"exact difference at moment 32 mod 11: {residue[0,0]} times I4")
    print(f"absolute full two-degree early heat {local_heat:.12f}; Taylor truncation <= {absolute_error:.3g} plus floating roundoff")
    print(f"analytic bound on two-geometry log change: {log_error:.3g}")
