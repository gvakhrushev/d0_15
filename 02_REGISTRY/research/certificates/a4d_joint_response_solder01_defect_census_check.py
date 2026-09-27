#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=900
"""Complete 0/1-solder census of the L=4 (NF) defect locus.

The eleven-solder family of section 8.9 has exactly two (NF) defects.  This
certificate asks how isolated that phenomenon is inside a complete finite
solder class fixed before any rank is read: the unit-diagonal 0/1 solders,
whose sixteen entries are 0 or 1 and whose diagonal is 1.  The class has
2^12 = 4096 members; unit-diagonal matrices with det S = 0 are excluded
because the metric channel needs a nondegenerate solder.  Exactly 1992
members are nondegenerate.

Findings (the scout/exact split is stated per gate):

  * Gate 1: the numeric mirror of the certified symbol assembly reproduces the
    exact symbolic implementation on the certified family to machine zero.
  * Gate 2 (exact): the census reproduces every certified family datum: the
    flat solder has 20 kernels with all ten moments exactly zero; the upper
    shear and the chain have their cut defect with exact moment -2 on q_11;
    all other family singular pairs have all ten blocks exactly zero.
  * Gate 3 (scout): over the complete nondegenerate class and all 256 L=4
    characters, 11424 singular pairs are found; 1602 of them have a nonzero
    response moment; those 1602 live on 505 solders.  The NF identity fails
    far beyond the two family defects.
  * Gate 4 (exact): every one of the 1602 candidate pairs is verified over
    QQ(i): the exact rank agrees with the scout rank and at least one scout
    moment block is exactly nonzero on the exact kernel.

Boundaries: constant solders, the 0/1 class, the L=4 grid.  This is a
tangent-level statement about the joint symbol; no joint-critical sequence is
produced, no cut is computed for the new defects, no #216 comparator gap is
computed, and no response terminal is claimed.  The zero-moment side of the
scout census (9822 pairs) is exact for the ten declared family/control solders
and scout-level elsewhere.

Dependencies.  The certificate loads the two merged #216 owner modules
directly (a4d_j2_fixed_realization_ir_check.py and
a4d_j2_smooth_resonance_closure_check.py, both on main) and carries
verbatim copies of the four exact assembly functions of the certified
branch module a4d_joint_response_shear_l4_support_check.py (branch
commit d37df8ce), which is not yet on main: family_brackets,
family_connection, family_metric_units, family_metric, and the shear
witness.  Gate 1 validates the numeric mirror against these copies, and
Gate 2 reproduces the certified family census with them.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent

# --- the two merged #216 owner modules, loaded directly from main ---
ir_source = (HERE / "a4d_j2_fixed_realization_ir_check.py").read_text(
    encoding="utf-8")
ir_ns: dict = {}
exec(ir_source.split('check("LORENTZ_GENERATORS"')[0], ir_ns)
owner_source = (HERE / "a4d_j2_smooth_resonance_closure_check.py").read_text(
    encoding="utf-8")
owner_marker = "# Exact diagonal quarter-wave data."
if owner_marker not in owner_source:
    raise RuntimeError("#216 owner symbol-construction boundary changed")
owner_ns: dict = {}
exec(owner_source.split(owner_marker)[0], owner_ns)

ETA = ir_ns["ETA"]
GENERATORS = ir_ns["GENERATORS"]
G2 = ir_ns["G2"]
STAR = ir_ns["STAR"]
wedge = ir_ns["wedge"]
connection_symbol = ir_ns["connection_symbol"]

from sympy.polys.domains import QQ_I  # noqa: E402
from sympy.polys.matrices import DomainMatrix  # noqa: E402


def exact_rank(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(QQ_I).rank()


def exact_nullspace(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(
        QQ_I).nullspace().to_Matrix().T


QPAIRS = [(i, j) for i in range(4) for j in range(i, 4)]
Q_DIRECTIONS = []
for i, j in QPAIRS:
    q = sp.zeros(4)
    q[i, j] = q[j, i] = 1
    Q_DIRECTIONS.append(q)

# --- verbatim copies of the four exact assembly functions of the certified
# branch module a4d_joint_response_shear_l4_support_check.py (branch commit
# d37df8ce).  That module is not yet on main, so the certificate carries its
# own copy; the numeric mirror below is validated against these copies in
# Gate 1 exactly as it was against the branch module.
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
COMPLEMENT = {p: [k for k in range(4) if k not in p] for p in PAIRS}


def family_brackets(solder):
    stored = []
    for r, s in PAIRS:
        u, v = [i for i in range(4) if i not in (r, s)]
        seq = [r, s, u, v]
        sign = (-1) ** sum(seq[i] > seq[j]
                           for i, j in itertools.combinations(range(4), 2))
        pairing = sign * wedge(solder[:, u], solder[:, v]).T * G2 * STAR
        form = []
        for left in GENERATORS:
            row = []
            for right in GENERATORS:
                commutator = (left * right - right * left) * ETA
                coords = sp.Matrix([commutator[a, b] for a, b in PAIRS])
                row.append(sp.together((pairing * coords)[0]))
            form.append(row)
        stored.append((r, s, form))
    return stored


def family_connection(stored, phase):
    result = sp.zeros(24)
    for r, s, form in stored:
        roles = [r, s, r, s]
        direct = [sp.Integer(1), phase[r], -phase[s], sp.Integer(-1)]
        inverse = [sp.Integer(1), 1 / phase[r], -1 / phase[s],
                   sp.Integer(-1)]
        role = sp.zeros(4)
        for i, j in itertools.combinations(range(4), 2):
            role[roles[i], roles[j]] += direct[i] * inverse[j] / 2
            role[roles[j], roles[i]] -= inverse[i] * direct[j] / 2
        result += sp.kronecker_product(role, sp.Matrix(form))
    return result


def family_metric_units(solder):
    gram = solder.T * ETA * solder
    units = []
    for q in Q_DIRECTIONS:
        lift = solder * gram.inv() * q / 2
        faces = []
        for r, s in PAIRS:
            u, v = [k for k in range(4) if k not in (r, s)]
            seq = [r, s, u, v]
            orientation = (-1) ** sum(
                seq[a] > seq[b]
                for a, b in itertools.combinations(range(4), 2))
            d_area = wedge(lift[:, u], solder[:, v]) + wedge(
                solder[:, u], lift[:, v])
            packed = orientation * d_area.T * G2 * STAR
            role_units = []
            for role in (r, s):
                coeffs = []
                for generator in GENERATORS:
                    coords = sp.Matrix([(generator * ETA)[a, b]
                                        for a, b in PAIRS])
                    coeffs.append(sp.together((packed * coords)[0]))
                role_units.append((role, coeffs))
            faces.append((r, s, role_units))
        units.append(faces)
    return units


def family_metric(units, physical):
    rows = []
    for faces in units:
        row = [sp.Integer(0)] * 24
        for r, s, role_units in faces:
            factors = {r: 1 - physical[s], s: physical[r] - 1}
            for role, coeffs in role_units:
                for j, coeff in enumerate(coeffs):
                    row[6 * role + j] += factors[role] * coeff
        rows.append([sp.together(entry) for entry in row])
    return sp.Matrix(rows)


WITNESS = sp.Matrix([
    0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0,
    0, 0, -1, 0, -1, 1,
    2, 1, 0, 1, 0, 0,
])

PSIGN = {}
for (r, s) in PAIRS:
    u, v = COMPLEMENT[(r, s)]
    PSIGN[(r, s)] = (-1) ** sum(
        [r, s, u, v][a] > [r, s, u, v][b]
        for a, b in itertools.combinations(range(4), 2))

ETA_N = np.array(ETA.tolist(), dtype=np.complex128)
G2_N = np.array(G2.tolist(), dtype=np.complex128)
STAR_N = np.array(STAR.tolist(), dtype=np.complex128)
QDIRS_N = [np.array(q.tolist(), dtype=np.complex128) for q in Q_DIRECTIONS]

COORDS = np.zeros((6, 6, 6), np.complex128)
for l, xl in enumerate(GENERATORS):
    for r, xr in enumerate(GENERATORS):
        y = (xl * xr - xr * xl) * ETA
        COORDS[l, r] = [complex(y[a, b]) for a, b in PAIRS]
GENCO = np.zeros((6, 6), np.complex128)
for g, x in enumerate(GENERATORS):
    M = x * ETA
    GENCO[g] = [complex(M[a, b]) for a, b in PAIRS]

ROOTS = (1 + 0j, 1j, -1 + 0j, -1j)
CHARS = list(itertools.product(ROOTS, repeat=4))


def tonp(M):
    return np.array(M.tolist(), dtype=np.complex128)




def wedge_num(a, b):
    return np.array([a[i] * b[j] - a[j] * b[i] for i, j in PAIRS])


def forms_of(S):
    """Numeric mirror of family_brackets, evaluated at one solder."""
    S = np.asarray(S, np.complex128)
    out = []
    for (r, s) in PAIRS:
        u, v = COMPLEMENT[(r, s)]
        pv = PSIGN[(r, s)] * (wedge_num(S[:, u], S[:, v]) @ G2_N @ STAR_N)
        out.append(np.einsum('k,lrk->lr', pv, COORDS))
    return out


def units_K(S):
    """Numeric mirror of family_metric_units under the identity

    C[qi, 6*role+j] = sum_other F[role, other] * K[qi, role, j, other].
    """
    S = np.asarray(S, np.complex128)
    gi = np.linalg.inv(S.T @ ETA_N @ S)
    K = np.zeros((10, 4, 6, 4), np.complex128)
    for qi, q in enumerate(QDIRS_N):
        lift = S @ gi @ q / 2
        for (r, s) in PAIRS:
            u, v = COMPLEMENT[(r, s)]
            d_area = wedge_num(lift[:, u], S[:, v]) + wedge_num(
                S[:, u], lift[:, v])
            packed = PSIGN[(r, s)] * (d_area @ G2_N @ STAR_N)
            for role, other in ((r, s), (s, r)):
                K[qi, role, :, other] += [packed @ GENCO[g]
                                          for g in range(6)]
    return K


def C_num(K, physical):
    F = np.zeros((4, 4), np.complex128)
    for role in range(4):
        for other in range(4):
            if role == other:
                continue
            F[role, other] = (1 - physical[other]) if role < other else (
                physical[other] - 1)
    return np.einsum('ro,qrjo->qrj', F, K).reshape(10, 24)


def H_num(forms, phase):
    H = np.zeros((24, 24), np.complex128)
    for p, (r, s) in enumerate(PAIRS):
        direct = [1.0, phase[r], -phase[s], -1.0]
        inverse = [1.0, 1 / phase[r], -1 / phase[s], -1.0]
        roles = [r, s, r, s]
        role = np.zeros((4, 4), np.complex128)
        for i, j in itertools.combinations(range(4), 2):
            role[roles[i], roles[j]] += direct[i] * inverse[j] / 2
            role[roles[j], roles[i]] -= inverse[i] * direct[j] / 2
        H += np.kron(role, forms[p])
    return H


def J_of(forms, K, phase):
    return np.vstack([H_num(forms, phase), C_num(K, [1 / z for z in phase])])


def joint_rank(J, tol=1e-8):
    w = np.linalg.svd(J, compute_uv=False)
    return int((w > tol * max(1.0, float(w[0]))).sum())


def scout_moments(S, phase, V):
    S = np.asarray(S, np.complex128)
    gi = np.linalg.inv(S.T @ ETA_N @ S)
    vals = []
    for q in QDIRS_N:
        lift = S @ gi @ q / 2
        D = (H_num(forms_of(S + lift), phase)
             - H_num(forms_of(S - lift), phase)) / 2
        vals.append(float(np.max(np.abs(V.conj().T @ D @ V))))
    return vals

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def decode(mask):
    """Unit-diagonal 0/1 solder from its 12-bit mask (row-major, i != j)."""
    S = sp.eye(4)
    bit = 0
    for i in range(4):
        for j in range(4):
            if i != j:
                if (mask >> bit) & 1:
                    S[i, j] += 1
                bit += 1
    return S


#: family/control masks fixed before any rank is read
CONTROL_MASKS = (0, 1, 2, 4, 16, 17, 32, 33, 256, 272)
#: certified singular-pair counts for those solders (family cert / section 8.1)
CONTROL_EXPECTED = {0: 20, 1: 14, 2: 14, 4: 14, 16: 6, 17: 3,
                    32: 6, 33: 3, 256: 6, 272: 4}
SHEAR_CHAR = (-1, 1, -1, 1)
CHAIN_CHAR = (-1, 1, 1, -1)
CHAIN_WITNESS = sp.Matrix([0, 0, 0, 0, 0, 1,
                           0, 0, 0, 0, 0, 0,
                           -2, 0, -1, 0, -1, 0,
                           0, 1, 0, 1, 0, 1])
DEFECT_MOMENT = [0, 0, 0, 0, -2, 0, 0, 0, 0, 0]


def sym_phase(phase):
    """Exact QQ(i) representative of a complex L=4 phase tuple."""
    out = []
    for z in phase:
        z = complex(z)
        if abs(z - 1) < 1e-9:
            out.append(sp.Integer(1))
        elif abs(z + 1) < 1e-9:
            out.append(sp.Integer(-1))
        elif abs(z - 1j) < 1e-9:
            out.append(sp.I)
        elif abs(z + 1j) < 1e-9:
            out.append(-sp.I)
        else:
            raise ValueError("character outside the fourth roots")
    return tuple(out)


def char_label(phase):
    names = {(1, 0): "1", (-1, 0): "-1", (0, 1): "i", (0, -1): "-i"}
    parts = []
    for z in phase:
        z = complex(z)
        parts.append(names[(round(z.real), round(z.imag))])
    return "(" + ",".join(parts) + ")"


def exact_J(S, phase, stored, units):
    H = family_connection(stored, list(phase)).applyfunc(sp.expand)
    C = family_metric(units, [1 / z for z in phase]).applyfunc(sp.expand)
    return H.col_join(C)


def exact_rank_kernel(J):
    rank = exact_rank(J)
    basis = exact_nullspace(J) if rank < 24 else None
    return rank, basis


def exact_blocks(S, phase, basis, q_indices):
    gram = S.T * ETA * S
    out = []
    for qi in q_indices:
        lift = S * gram.inv() * Q_DIRECTIONS[qi] / 2
        D = (connection_symbol(S + lift, list(phase))
             - connection_symbol(S - lift, list(phase))) / 2
        out.append(sp.simplify(sp.conjugate(basis).T * D * basis))
    return out


def witness_moments(S, phase, witness):
    gram = S.T * ETA * S
    values = []
    for q in Q_DIRECTIONS:
        lift = S * gram.inv() * q / 2
        D = (connection_symbol(S + lift, list(phase))
             - connection_symbol(S - lift, list(phase))) / 2
        values.append(sp.simplify(
            (sp.conjugate(witness).T * D * witness)[0]))
    return values


def gaussian_content(vector):
    content = 0
    for e in vector:
        e = sp.expand(sp.together(e))
        content = sp.igcd(content, abs(int(sp.re(e))), abs(int(sp.im(e))))
    return content

def scout_pairs(S):
    """Numeric scout of one solder over the 256 L=4 characters."""
    forms = forms_of(S)
    K = units_K(S)
    found = []
    for ci, phase in enumerate(CHARS):
        J = J_of(forms, K, phase)
        rank = joint_rank(J)
        if rank < 24:
            U, w, Vh = np.linalg.svd(J)
            V = Vh.conj().T[:, rank:]
            patt = scout_moments(S, phase, V)
            qs = [i for i, v in enumerate(patt) if v > 1e-7]
            found.append({'ci': ci, 'phase': phase, 'rank': rank,
                          'kdim': int(V.shape[1]),
                          'mmax': max(patt), 'q': qs})
    return found


def gate1_mirror():
    print("Gate 1: numeric mirror against the exact symbolic assembly",
          flush=True)
    for mask in CONTROL_MASKS:
        S = decode(mask)
        Snum = tonp(S)
        err = 0.0
        for (_r, _s, form_sym), form_num in zip(family_brackets(S),
                                                forms_of(Snum)):
            sym = np.array([[complex(form_sym[l][r]) for r in range(6)]
                            for l in range(6)], np.complex128)
            err = max(err, float(np.max(np.abs(sym - form_num))))
        units = family_metric_units(S)
        K = units_K(Snum)
        cerr = 0.0
        for phase in [(-1, 1, -1, 1j), (1j, -1, 1, -1)]:
            physical = [1 / z for z in phase]
            C_sym = np.array(family_metric(units, physical).tolist(),
                             dtype=np.complex128)
            cerr = max(cerr, float(np.max(np.abs(
                C_sym - C_num(K, physical)))))
        check("MIRROR_FORMS_EXACT_%d" % mask, err == 0.0)
        check("MIRROR_C_MACHINE_ZERO_%d" % mask, cerr < 1e-9)
        pairs = scout_pairs(Snum)
        check("MIRROR_SINGULAR_COUNT_%d" % mask,
              len(pairs) == CONTROL_EXPECTED[mask])
    print("   mirror validated on %d family/control solders" %
          len(CONTROL_MASKS), flush=True)


def gate2_family():
    print("Gate 2: exact reproduction of the certified family census",
          flush=True)
    for mask in CONTROL_MASKS:
        S = decode(mask)
        stored = family_brackets(S)
        units = family_metric_units(S)
        pairs = scout_pairs(tonp(S))
        check("FAMILY_COUNT_%d" % mask, len(pairs) == CONTROL_EXPECTED[mask])
        defects = 0
        for entry in pairs:
            phase = sym_phase(entry['phase'])
            J = exact_J(S, phase, stored, units)
            rank, basis = exact_rank_kernel(J)
            check("FAMILY_RANK_%d_%d" % (mask, entry['ci']),
                  rank == entry['rank'] and basis is not None)
            if mask == 17 and entry['phase'] == (-1.0, 1.0, -1.0, 1.0):
                values = witness_moments(S, phase, WITNESS)
                check("FAMILY_SHEAR_WITNESS_MOMENT", values == DEFECT_MOMENT)
                defects += 1
                continue
            if mask == 33 and entry['phase'] == (-1.0, 1.0, 1.0, -1.0):
                values = witness_moments(S, phase, CHAIN_WITNESS)
                check("FAMILY_CHAIN_WITNESS_MOMENT", values == DEFECT_MOMENT)
                defects += 1
                continue
            blocks = exact_blocks(S, phase, basis, list(range(10)))
            check("FAMILY_ZERO_BLOCKS_%d_%d" % (mask, entry['ci']),
                  all(b == sp.zeros(basis.cols) for b in blocks))
        if mask in (17, 33):
            check("FAMILY_DEFECT_PRESENT_%d" % mask, defects == 1)
    flat = scout_pairs(tonp(decode(0)))
    check("FLAT_KERNEL_STRUCTURE",
          sorted(e['kdim'] for e in flat) == [1] * 18 + [4] * 2)
    shear = scout_pairs(tonp(decode(17)))
    check("SHEAR_DEFECT_MAGNITUDE",
          any(abs(e['mmax'] - 0.2) < 1e-9 for e in shear))
    print("   certified family census reproduced exactly on %d solders"
          % len(CONTROL_MASKS), flush=True)

def gate3_scout():
    print("Gate 3: complete nondegenerate 0/1 solder census (scout)",
          flush=True)
    degenerate = 0
    results = {}
    n_pairs = 0
    t0 = time.time()
    for mask in range(1 << 12):
        S = decode(mask)
        if S.det() == 0:
            degenerate += 1
            continue
        pairs = scout_pairs(tonp(S))
        results[mask] = pairs
        n_pairs += len(pairs)
        if len(results) % 256 == 0:
            print("   %d solders, %d singular pairs, %.0fs"
                  % (len(results), n_pairs, time.time() - t0), flush=True)
    candidates = [(mask, e) for mask in sorted(results)
                  for e in results[mask] if e['q']]
    affected = len({mask for mask, _ in candidates})
    check("CLASS_SIZE", len(results) == 1992)
    check("DEGENERATE_EXCLUDED", degenerate == 2104)
    check("SINGULAR_PAIRS", n_pairs == 11424)
    check("CANDIDATE_PAIRS", len(candidates) == 1602)
    check("AFFECTED_SOLDERS", affected == 505)
    print("   degenerate %d, nondegenerate %d, singular %d, candidates %d,"
          " affected %d" % (degenerate, len(results), n_pairs,
                            len(candidates), affected), flush=True)
    return results, candidates


def gate4_exact(candidates):
    print("Gate 4: exact QQ(i) verification of every candidate", flush=True)
    t0 = time.time()
    cache = {}
    confirmed = []
    unconfirmed = []
    for idx, (mask, entry) in enumerate(candidates):
        S = cache.get(('S', mask))
        if S is None:
            S = decode(mask)
            cache[('S', mask)] = S
            cache[('stored', mask)] = family_brackets(S)
            cache[('units', mask)] = family_metric_units(S)
        stored = cache[('stored', mask)]
        units = cache[('units', mask)]
        phase = sym_phase(entry['phase'])
        J = exact_J(S, phase, stored, units)
        rank, basis = exact_rank_kernel(J)
        if rank != entry['rank'] or basis is None:
            unconfirmed.append((mask, entry['ci'], 'rank', rank))
            continue
        blocks = exact_blocks(S, phase, basis, entry['q'])
        good = None
        for qi, block in zip(entry['q'], blocks):
            if block != sp.zeros(basis.cols):
                good = (qi, block)
                break
        if good is None:
            unconfirmed.append((mask, entry['ci'], 'moments', None))
            continue
        qi, block = good
        record = {'mask': mask, 'char': char_label(entry['phase']),
                  'rank': rank, 'kdim': basis.cols, 'q': qi,
                  'q_scout': entry['q']}
        if basis.cols == 1:
            content = gaussian_content(basis[:, 0]) or 1
            value = sp.simplify(block[0])
            record['block'] = str(value)
            record['content'] = int(content)
            record['prim_moment'] = str(sp.simplify(value / content ** 2))
        else:
            record['block'] = str(block.tolist())
        confirmed.append(record)
        if (idx + 1) % 200 == 0:
            print("   %d/%d processed, %d confirmed, %.0fs"
                  % (idx + 1, len(candidates), len(confirmed),
                     time.time() - t0), flush=True)
    print("   confirmed %d, unconfirmed %d, %.0fs"
          % (len(confirmed), len(unconfirmed), time.time() - t0), flush=True)
    for row in unconfirmed[:10]:
        print("   UNCONFIRMED:", row, flush=True)
    check("ALL_CANDIDATES_EXACTLY_CONFIRMED", not unconfirmed)
    return confirmed, unconfirmed


def main():
    t0 = time.time()
    gate1_mirror()
    gate2_family()
    results, candidates = gate3_scout()
    confirmed, _unconfirmed = gate4_exact(candidates)
    kdim_hist = dict(Counter(r['kdim'] for r in confirmed))
    char_hist = Counter(r['char'] for r in confirmed)
    by_solder = Counter(r['mask'] for r in confirmed)
    payload = {
        'class': 'unit-diagonal 0/1 solders with det != 0, L=4 grid',
        'degenerate_excluded': 2104,
        'nondegenerate': len(results),
        'singular_pairs_scout': sum(len(v) for v in results.values()),
        'candidates_scout': len(candidates),
        'confirmed_exact': len(confirmed),
        'affected_solders': len(by_solder),
        'kdim_histogram': {str(k): v for k, v in kdim_hist.items()},
        'char_multiset': dict(char_hist),
        'top_solders': by_solder.most_common(12),
        'candidates': confirmed,
    }
    with open(HERE / 'a4d_joint_response_solder01_defect_census.json',
              'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=1, sort_keys=True)
    print()
    print("RESULT_CENSUS: 1992 nondegenerate solders, 11424 scout singular "
          "pairs, %d exact NF failures on %d solders"
          % (len(confirmed), len(by_solder)))
    print("RESULT_STRUCTURE: kdim histogram %s; top characters %s"
          % (kdim_hist, char_hist.most_common(4)))
    print("RESULT_FAMILY: the two family defects are reproduced exactly and "
          "the failure set is not confined to them")
    print("TERMINAL: NF-DEFECTS-ARE-NOT-CONFINED-TO-THE-ELEVEN-SOLDER-FAMILY")
    print("BOUNDARY: constant solders, unit-diagonal 0/1 class, L=4 grid, "
          "tangent-level joint symbol only; no joint-critical sequence, no "
          "cut for the new defects, no #216 comparator gap, no response "
          "terminal; the zero-moment side is scout-level outside the ten "
          "declared control solders.")
    print("ELAPSED: %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
