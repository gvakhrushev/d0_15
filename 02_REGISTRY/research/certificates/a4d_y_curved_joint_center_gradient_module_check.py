#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=420
"""Exact folded center-gradient module; the all-torus premise remains open.

Recovered after the execution environment disconnected during publication.
The finite calculations below passed locally before that event. The compact
pinned ledger and this recovered source require independent replay by CI.
The analytic division and conditional consequences are proved in
A4D_Y_CURVED_JOINT_CENTER_GRADIENT_MODULE.md.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys

from flint import nmod_mat
import sympy as sp
import a4d_y_curved_joint_rational_stencil as R

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_curved_joint_center_gradient_module_results.json"
ZERO = (0, 0, 0, 0)
PRIME = 1000000007
DET_J = sp.Rational(-62976744635716940958283670688,
                    206230323499945683191645561081)


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def compile_joint():
    entries = defaultdict(lambda: defaultdict(Fraction))
    for offset, owner in ((0, R.ATERMS), (96, R.QTERMS)):
        for d, values in owner.items():
            for (r, c), value in values.items():
                entries[d][offset + r, c] += value
    return entries, dense(entries, 136, 96)


def dense(entries, nr, nc):
    result = {}
    for d, es in entries.items():
        M = sp.zeros(nr, nc)
        for (r, c), value in es.items():
            if value:
                M[r, c] = sp.Rational(value)
        if M != sp.zeros(nr, nc):
            result[d] = M
    return result


def evaluate(terms, zeta):
    shape = next(iter(terms.values())).shape
    return sum((zeta**sum(d) * M for d, M in terms.items()), sp.zeros(*shape))


def derivative(terms, k):
    shape = next(iter(terms.values())).shape
    return sum((d[k] * M for d, M in terms.items()), sp.zeros(*shape))


def target():
    standard = [j for j in range(96) if j not in {3, 4, 5, 51, 52, 53}]
    B, P, C, A = sp.zeros(96, 94), sp.zeros(94, 96), sp.zeros(96, 2), sp.zeros(2, 96)
    for k, j in enumerate(standard):
        B[j, k] = P[k, j] = 1
    for a, phase in enumerate((0, 2)):
        base, j = 24 * phase + 3, 90 + 2 * a
        B[base, j] = B[base + 1, j] = 1
        B[base + 1, j + 1] = B[base + 2, j + 1] = 1
        P[j, base:base + 3] = sp.Matrix([[2, 1, -1]]) / 3
        P[j + 1, base:base + 3] = sp.Matrix([[-1, 1, 2]]) / 3
        sign = 1 if phase == 0 else -1
        for g, y in enumerate((1, -1, 1)):
            C[base + g, a] = sign * sp.Rational(4, 7) * y
            A[a, base + g] = sign * sp.Rational(7, 12) * y
    ck("EXACT_94_PLUS_TWO_COORDINATE_SPLIT",
       P*B == sp.eye(94) and A*C == sp.eye(2) and P*C == sp.zeros(94, 2)
       and A*B == sp.zeros(2, 94) and B*P + C*A == sp.eye(96))
    terms = defaultdict(lambda: defaultdict(Fraction))
    for (r, c), value in P.todok().items():
        terms[ZERO][r, c] += value
    phases = [R.LABELS[j][0] for j in standard] + [0, 0, 2, 2]
    graph = []
    for a, phase in enumerate((0, 2)):
        for s in (1, 2, 3):
            for step in (-1, 1):
                row = 94 + len(graph)
                d = tuple(step if k == 0 else int(k == s) for k in range(4))
                source = a if step == -1 else 1 - a
                for c in range(96):
                    terms[d][row, c] += A[source, c]
                    terms[ZERO][row, c] -= A[a, c]
                graph.append((row, phase, d, (0, 2)[source]))
                phases.append(phase)
    ck("ACTUAL_GRAPH_PHASE_PLACEMENT",
       all((p + sum(d)) % 4 == src for row, p, d, src in graph))
    ck("TARGET_FOLDED_COVARIANCE",
       all((sum(d) + phases[r] - R.LABELS[c][0]) % 4 == 0
           for d, es in terms.items() for (r, c), v in es.items() if v))
    T = dense(terms, 106, 96)
    lam = sp.symbols("lambda0:4", nonzero=True)
    TC = sum((sp.prod(lam[k]**d[k] for k in range(4))*M*C
              for d, M in T.items()), sp.zeros(106, 2))
    ck("TARGET_COMPLEMENT_KILLS_CENTER", TC[:94, :] == sp.zeros(94, 2))
    for row, phase, d, src in graph:
        expected = sp.zeros(1, 2)
        expected[0, (0, 2).index(phase)] -= 1
        expected[0, (0, 2).index(src)] += sp.prod(lam[k]**d[k] for k in range(4))
        ck("SYMBOLIC_GRAPH_ROW_%d" % row, TC[row:row+1, :] == expected)
    mu = sp.symbols("mu", nonzero=True)
    ck("COMMON_RATIO_TARGET_DETERMINANT",
       sp.Matrix([[-1, mu**2], [mu**2, -1]]).det() == 1 - mu**4)
    dU = R.madd(R.mscale(Fraction(4, 49), R.Y), R.mscale(Fraction(16, 49), R.Y2))
    ck("LITERAL_RIGHT_CAYLEY_TANGENT",
       R.mm(R.linv(R.U), dU) == R.mscale(Fraction(4, 7), R.Y))
    return B, C, T


def inverse_obstruction(entries, B, mode):
    if mode == "axes":
        alphas = [ZERO] + [tuple(s if k == j else 0 for k in range(4))
                           for j in range(4) for s in (-1, 1)]
    elif mode == "stencil":
        alphas = sorted(entries)
    else:
        n = 2 if mode == "degree2" else 3
        alphas = [a for a in product(range(-n, n+1), repeat=4) if sum(abs(x) for x in a) <= n]
    colmap = defaultdict(list)
    for (c, j), value in B.todok().items():
        colmap[c].append((j, int(value)))
    phases = []
    for j in range(94):
        support = {R.LABELS[c][0] for c in range(96) if B[c, j]}
        if len(support) != 1:
            raise AssertionError("complement column phase")
        phases.append(support.pop())
    terms = defaultdict(lambda: defaultdict(int))
    for d, es in entries.items():
        for (r, c), value in es.items():
            z = 14 * value
            if z.denominator != 1:
                raise AssertionError("denominator clearing")
            for j, v in colmap[c]:
                terms[d][r, j] += z.numerator * v
    terms = {d: {rc: v for rc, v in es.items() if v} for d, es in terms.items()}
    betas = sorted({tuple(a[k]+d[k] for k in range(4)) for a in alphas for d in terms})
    bi = {d: i for i, d in enumerate(betas)}
    rowphase = lambda r: r//24 if r < 96 else (r-96)//10
    variables, equations = [[] for _ in range(4)], [[] for _ in range(4)]
    for ai, a in enumerate(alphas):
        for r in range(136):
            variables[(sum(a)-rowphase(r)) % 4].append((ai, r))
    for b, d in enumerate(betas):
        for j in range(94):
            equations[(sum(d)-phases[j]) % 4].append((b, j))
    vi = [{key: i for i, key in enumerate(keys)} for keys in variables]
    ei = [{key: i for i, key in enumerate(keys)} for keys in equations]
    triples = [[] for _ in range(4)]
    for ai, a in enumerate(alphas):
        for d, es in terms.items():
            b = bi[tuple(a[k]+d[k] for k in range(4))]
            for (r, j), value in es.items():
                sector = (sum(a)-rowphase(r)) % 4
                triples[sector].append((ei[sector][b, j], vi[sector][ai, r], value))
    sectors = [0] if mode == "degree3_phase0" else list(range(4))
    nr_total = nc_total = rank_total = aug_total = targets_total = 0
    for sector in sectors:
        nr, nc = len(equations[sector]), len(variables[sector])
        M = nmod_mat(nr, nc, PRIME)
        for r, c, value in triples[sector]:
            M[r, c] = value
        rank = M.rank()
        del M
        targets = [j for j in range(94) if -phases[j] % 4 == sector]
        AM = nmod_mat(nr, nc + len(targets), PRIME)
        for r, c, value in triples[sector]:
            AM[r, c] = value
        for k, j in enumerate(targets):
            AM[ei[sector][bi[ZERO], j], nc+k] = 1
        augmented = AM.rank()
        del AM
        ck(mode.upper()+"_BLOCK_%d_FULL_COLUMN_RANK" % sector, rank == nc)
        ck(mode.upper()+"_BLOCK_%d_INDEPENDENT_TARGETS" % sector,
           augmented == rank + len(targets))
        nr_total += nr
        nc_total += nc
        rank_total += rank
        aug_total += augmented
        targets_total += len(targets)
    if sectors == list(range(4)):
        ck(mode.upper()+"_BLOCK_PARTITION",
           nr_total == 94*len(betas) and nc_total == 136*len(alphas) and targets_total == 94)
    else:
        ck("DEGREE3_PHASE0_HAS_ALL_23_NEEDED_TARGETS", targets_total == 23)
    # Full modular column rank fixes rank over Q to nc. The augmented
    # modular rank is maximal too. This proves rational inconsistency.
    # Degree three needs only its phase-0 sector to exclude a full inverse.
    return {"template": mode, "alpha_count": len(alphas), "beta_count": len(betas),
            "checked_matrix_shape": [nr_total, nc_total],
            "rank_mod_prime": rank_total, "augmented_rank_mod_prime": aug_total,
            "checked_phase_sectors": sectors}


def main():
    entries, Q = compile_joint()
    B, C, T = target()
    ck("LITERAL_JOINT_SUPPORT", len(Q) == 21 and sum(len(es) for es in entries.values()) == 2988)
    owner = json.loads((HERE/"a4d_y_curved_joint_folded_isolation_results.json").read_text())
    rows, frows = owner["square_graph_rows"], owner["reduced_residual_rows"]
    cols = [j for j in range(96) if j != 3]
    Q0, T0 = evaluate(Q, sp.Integer(1)), evaluate(T, sp.Integer(1))
    ck("EXACT_FOLDED_JOINT_RANK95", Q0.to_DM().rank() == 95)
    S = Q0.extract(rows, cols)
    Sinv = S.to_DM().inv().to_Matrix()
    x = -Sinv*Q0.extract(rows, [3])
    v = sp.zeros(96, 1)
    v[3] = 1
    for i, c in enumerate(cols):
        v[c] = x[i]
    ck("GRAPH_KERNEL_IS_PHYSICAL_Y", v == (C[:, 0]+C[:, 1])*sp.Rational(7, 4))
    ck("TARGET_KILLS_FOLDED_KERNEL", T0*v == sp.zeros(106, 1))
    B0 = Q0.extract(frows, cols)
    J, G = sp.zeros(4, 4), sp.zeros(106, 4)
    Ds = []
    for k in range(4):
        D = derivative(Q, k)
        Ds.append(D)
        xd = -Sinv*(D.extract(rows, [3])+D.extract(rows, cols)*x)
        vd = sp.zeros(96, 1)
        for i, c in enumerate(cols):
            vd[c] = xd[i]
        J[:, k] = D.extract(frows, [3])+D.extract(frows, cols)*x+B0*xd
        G[:, k] = derivative(T, k)*v+T0*vd
    ck("OWNED_HOLOMORPHIC_JACOBIAN",
       sp.factor(J.det()) == DET_J == sp.Rational(owner["reduced_J4_determinant"]))
    ck("LOCAL_MAXIMAL_IDEAL", J.rank() == 4)
    selector = sp.zeros(95, 136)
    for i, r in enumerate(rows):
        selector[i, r] = 1
    reduced = sp.zeros(4, 136)
    for i, r in enumerate(frows):
        reduced[i, r] = 1
    reduced -= B0*Sinv*selector
    A0 = T0[:, cols]*Sinv*selector+G*J.inv()*reduced
    ck("LOCAL_DIVISION_CONSTANT_TERM", A0*Q0 == T0)
    for k in range(4):
        ck("LOCAL_DIVISION_KERNEL_FIRST_JET_%d" % k,
           A0*Ds[k]*v == derivative(T, k)*v)
    ranks = []
    for zeta in (sp.Integer(1), sp.I, sp.Integer(-1), -sp.I):
        vz = sp.diag(*[zeta**(-p) for p, role, g in R.LABELS])*v
        Qz, Tz = evaluate(Q, zeta), evaluate(T, zeta)
        rank = Tz.to_DM(extension=True).rank()
        ck("FOLDED_KERNEL_AND_TARGET_"+str(zeta),
           Qz*vz == sp.zeros(136, 1) and Tz*vz == sp.zeros(106, 1) and rank == 95)
        ranks.append(rank)
    bad = T0*sp.diag(*[sp.I**(-p) for p, role, g in R.LABELS])*v
    ck("HOSTILE_PHASE_ERASURE_CHANGES_KERNEL", bad != sp.zeros(106, 1))
    checks = [inverse_obstruction(entries, B, mode)
              for mode in ("axes", "stencil", "degree2", "degree3_phase0")]
    result = {
        "schema": "a4d-y-curved-joint-center-gradient-module-v1",
        "terminal": "A4D-Y-FOLDED-CENTER-GRADIENT-LOCAL-MODULE-CERTIFIED",
        "joint_shape": [136, 96], "target_shape": [106, 96],
        "holomorphic_reduced_jacobian_determinant": str(sp.factor(J.det())),
        "folded_target_ranks": ranks, "prime": PRIME, "denominator_clearing": 14,
        "short_inverse_obstructions": checks,
        "open_premise": "full joint rank on the physical torus outside the four folded characters",
        "scope": "local division unconditional; all-torus norm estimate and flat nonlinear rigidity conditional; curved response terminal open"
    }
    if "--write" in sys.argv:
        OUT.write_text(json.dumps(result, indent=2)+"\n")
        print("WROTE", OUT, flush=True)
    else:
        ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text()) == result)
    print("TERMINAL "+result["terminal"], flush=True)


if __name__ == "__main__":
    main()
