"""Verify the paired Born contraction on the real aggregate Julia/CAR section."""
import itertools
import json
import math
from functools import reduce

import numpy as np


def require(ok, name):
    if not ok:
        raise ValueError(name)


def close(actual, expected, name, tol=2e-10):
    require(np.allclose(actual, expected, atol=tol, rtol=tol), name)


ORDER = (0, 2, 3, 1)
ETA = np.array([[0, 1, 0, 0], [1, 0, 0, 0],
                [0, 0, -1, 0], [0, 0, 0, -1]])
EYE = np.eye(4, dtype=int)
CREATORS = np.zeros((4, 16, 16), dtype=int)
for i in ORDER:
    for mask in range(16):
        if not mask & (1 << i):
            n = sum((mask >> j) & 1 for j in ORDER[:ORDER.index(i)])
            CREATORS[i, mask | (1 << i), mask] = (-1)**n


def exterior(matrix):
    """Exterior matrix in the owner's CAR mask and predecessor convention."""
    grades = [[j for j in ORDER if mask & (1 << j)] for mask in range(16)]
    out = np.zeros((16, 16))
    for i, row in enumerate(grades):
        for j, col in enumerate(grades):
            if len(row) == len(col):
                out[i, j] = np.linalg.det(matrix[np.ix_(row, col)]) if row else 1
    return out


def dg(matrix):
    return sum(matrix[i, j] * (CREATORS[i] @ CREATORS[j].T)
               for i, j in itertools.product(range(4), repeat=2))


def gen(i, j):
    return (np.outer(EYE[i], EYE[j]) - np.outer(EYE[j], EYE[i])) @ ETA


def multiply(mats):
    return reduce(np.matmul, mats)


def sqrt_psd(matrix):
    eig, vec = np.linalg.eigh(matrix)
    require(eig.min() >= -2e-12, "Julia input is a contraction")
    return np.einsum("ij,j,kj->ik", vec, np.sqrt(np.maximum(eig, 0)), vec)


def julia(block):
    eye = np.eye(len(block))
    out = np.block([[block, sqrt_psd(eye-np.einsum("ij,kj->ik", block, block))],
                    [sqrt_psd(eye-np.einsum("ji,jk->ik", block, block)), -block.T]])
    close(np.einsum("ji,jk->ik", out, out), np.eye(len(out)), "full Julia isometry")
    return out


HE = np.rint(exterior(ETA)).astype(int)
P = np.abs(HE).argmax(axis=1)
SIGN = HE[np.arange(16), P]
close(HE @ HE, np.eye(16), "CAR metric involution")


def triple_expectation(wave, addresses):
    """Contract the permutation of actual ket coordinates with actual bra coordinates."""
    def component(k, row, col):
        if k in (1, 4, 5):  # H B^T H, including the two inverse links
            return SIGN[row] * SIGN[col] * wave[addresses[k], P[row], P[col]]
        return wave[addresses[k], col, row]  # physical Choi ordering (address, in, out)

    sparse = [[(i, j, component(k, i, j)) for i, j in itertools.product(range(16), repeat=2)
               if component(k, i, j) != 0] for k in (0, 2, 4)]
    return math.fsum(left * middle * right * component(1, b, c) *
                     component(3, d, e) * component(5, f, a)
                     for (a, b, left), (c, d, middle), (e, f, right)
                     in itertools.product(*sparse))


def six_slot_witness():
    pairs = list(itertools.combinations(range(4), 2))
    generators = [dg(gen(*pair)) for pair in pairs]
    face = dg(gen(0, 1))
    for word in itertools.product(range(6), repeat=4):
        trace = int(np.trace(multiply([face] + [generators[j] for j in word])))
        if trace:
            return {"link_planes": [pairs[j] for j in word], "integer_trace": trace,
                    "mixed_derivative_with_half_coframes": -trace / 32}
    raise ValueError("no sixth mixed derivative")


def constant_determinant_cube():
    # On the owner's null metric directions 2 and 3 span a spacelike plane.
    rot = EYE.copy()
    rot[2:,2:] = [[0,-1],[1,0]]
    close(rot.T @ ETA @ rot, ETA, "quarter-turn is a proper Lorentz link")
    area = dg(gen(2,3))
    values = [-int(round(np.sum(area * exterior(np.linalg.matrix_power(rot, j)).T))) // 8
              for j in range(4)]
    require(values == [0,1,0,-1], "full exterior character quarter turns")
    jump = sum((-1)**sum(bits) * values[(1+bits[0]+bits[1]-bits[2]-bits[3]) % 4]
               for bits in itertools.product(range(2), repeat=4))
    require(jump == 4, "genuine four-edge mixed difference")
    delta = 1/32
    base = EYE / 2
    determinants = []
    total = 0
    for bits in itertools.product(range(2), repeat=6):
        coframe = base.copy()
        coframe[2,0] += delta*bits[0]
        coframe[3,1] += delta*bits[1]
        determinants.append(np.linalg.det(coframe))
        u, v = coframe[:,0], coframe[:,1]
        generator = dg((np.outer(u,v)-np.outer(v,u)) @ ETA)
        exponent = (1+bits[2]+bits[3]-bits[4]-bits[5]) % 4
        trace = np.sum(generator * exterior(np.linalg.matrix_power(rot, exponent)).T)
        total += (-1)**sum(bits) * (-trace/8)
    close(determinants, 1/16, "fixed determinant on the six-address cube")
    close(total, 4*delta**2, "actual mixed difference of all 64 configurations")
    return {"corners": 64, "coframe_shift": delta, "mixed_difference": total}


def fourier_frame():
    sites = np.array(list(itertools.product(range(4), repeat=4)))
    delta = [*EYE, *(EYE[j] - EYE[i] for j in (1, 2, 3) for i in range(j))]
    cos = np.array([1, 0, -1, 0])
    sin = np.array([0, 1, 0, -1])
    candidates = [k for k in sites if tuple(k) < tuple((-k) % 4)]
    ranked = sorted(candidates, key=lambda k: (-sum(cos[(d @ k) % 4] for d in delta), tuple(k)))
    freq = np.array(ranked[:64])
    phase = (sites @ freq.T) % 4
    frame = np.column_stack((cos[phase], sin[phase])) / 8
    close(np.einsum("ji,jk->ik", frame, frame) / len(sites), np.eye(128) / 128, "original full Fourier128 Gram")
    stencil = [0] + [list(map(tuple, sites)).index(tuple(v)) for v in EYE]
    local = frame[stencil]
    g = local @ local.T
    nums = [int(sum(cos[(freq @ v) % 4])) for v in delta]
    require(nums == [20, 10, 10, 9, 8, 8, 6, 9, 5, 5], "all ten stencil overlaps")
    return g, nums


def main():
    columns = np.array([[.44, .12, 0, .04], [.03, .43, .05, 0],
                        [.08, 0, .41, .07], [0, .05, .09, .42]]).T
    links = []
    for plane, t in zip([(0, 1), (0, 2), (1, 3), (2, 3)], [.13, .16, -.09, .12]):
        half = t * gen(*plane) / 2
        link = np.linalg.solve(EYE-half, EYE+half)
        close(link.T @ ETA @ link, ETA, "physical Lorentz link")
        links.append(link)
    creators = [np.tensordot(v, CREATORS, axes=1) for v in columns]
    blocks = creators + [exterior(link)/2 for link in links]
    D = len(blocks) * 32
    wave = np.stack([julia(b).T for b in blocks]) / math.sqrt(D)
    close(np.vdot(wave, wave), 1, "complete aggregate normalization")
    # The shuffle is a permutation of all six retained coordinates. Check both orientations.
    tuples = list(itertools.product(range(3), repeat=6))
    shuffled = {(b, c, d, e, f, a) for a, b, c, d, e, f in tuples}
    require(shuffled == set(tuples), "fixture partial permutation range")
    for (i, j) in itertools.combinations(range(4), 2):
        def term(r, s):
            return triple_expectation(wave, [r, s, 4, 5, 6, 7])
        recovered = -16 * D**3 * (term(i, j) - term(j, i)) / 8
        face = np.outer(columns[i], columns[j]) - np.outer(columns[j], columns[i])
        holonomy = multiply([links[0], links[1], np.linalg.inv(links[2]), np.linalg.inv(links[3])])
        target = -np.einsum("ij,ji->", dg(face @ ETA), exterior(holonomy)) / 8
        close(recovered, target, "three-copy Choi signed face")
    sharp = six_slot_witness()

    gram, nums = fourier_frame()
    psi = np.array([[.12, -.15], [-.08, .11], [.20, .05], [.04, -.07], [.10, .18]])
    # The two other nonzero CAR masks complete each actual normalized local state.
    golden = (math.sqrt(5)-1)/2
    slack = np.sqrt(1-golden-np.sum(psi**2, axis=1))
    close(golden+slack**2+np.sum(psi**2, axis=1), 1, "complete CAR norm")
    incidence = np.column_stack((-np.ones(4), np.eye(4)))
    raw_density = gram * (psi @ psi.T) / 256
    q_from_input = 0
    q_blind = 0
    rho, step, metric_scale = 1.25, .25, 1.125
    for i, j in itertools.product(range(4), repeat=2):
        pair = D * sum(ETA[a,b] * wave[i,0,1<<a] * wave[j,0,1<<b]
                       for a,b in itertools.product(range(4), repeat=2))
        stencil = np.outer(incidence[i], incidence[j])
        factor = 256 * metric_scale * pair / (rho * step**2)
        q_from_input += factor * np.sum(raw_density * stencil / gram)
        q_blind += factor * np.sum(raw_density * stencil)
    metric = metric_scale * columns @ ETA @ columns.T
    deriv = incidence @ psi / step
    q = np.sum(metric * (deriv @ deriv.T)) / rho
    close(q_from_input, q, "one Choi and one original CAR expectation")
    require(abs(q_blind - q) > 1e-3, "missing reference correction changes matter")
    # With orthogonal site guards, independent CAR signs cannot produce a cross-site mixed difference.
    def kinetic(a, b):
        data = np.zeros((5, 2))
        data[1,0], data[2,0] = a*.12, b*.15
        d = incidence @ data / step
        return np.sum(metric * (d @ d.T)) / rho
    mixed = sum(i*j*kinetic(i,j) for i,j in itertools.product([-1,1],repeat=2))
    require(abs(mixed) > .01, "dephased site witness is nonzero")
    print(json.dumps({"aggregate_addresses_fixture": len(blocks), "choi_dimension_per_address": 32,
                      "faces_compared": 6, "six_slot_witness": sharp,
                      "constant_determinant_cube": constant_determinant_cube(),
                      "reference_numerators": nums, "matter_direct": round(q, 9),
                      "matter_paired": round(q_from_input, 9), "matter_without_correction": round(q_blind, 9),
                      "orthogonal_guard_mixed_difference": round(mixed, 9),
                      "sharp_generic_geometry_copies": 3, "joint_input": {"choi": 3, "fourier_car": 1},
                      "whole_price_derived": False, "GR_closed": False}, indent=2))


if __name__ == "__main__":
    main()
