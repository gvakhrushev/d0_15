"""Exact Golden controller and inherited all128 cost-effect controls."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sympy as S


def run():
    root = Path(__file__).resolve()
    while not (root / "AGENTS.md").is_file():
        if root.parent == root:
            raise RuntimeError("repository root not found")
        root = root.parent
    pins = {
        "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md":
            "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d",
        "02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md":
            "ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d",
        "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md":
            "2b26bf2f4c1b128731ccf14a17437ba654c046e82b5e42e55113a8b6053494ea",
    }
    checks = []

    def ok(condition, label):
        if not condition:
            raise RuntimeError(label)
        checks.append(label)

    def eq(left, right, label):
        diff = left-right
        good = (all(S.simplify(x) == 0 for x in diff)
                if isinstance(diff, S.MatrixBase) else S.simplify(diff) == 0)
        ok(good, label)

    for path, sha in pins.items():
        ok(hashlib.sha256((root/path).read_bytes()).hexdigest() == sha, "pin "+path)
    p = (S.sqrt(5)-1)/2
    a = S.sqrt(p)
    g = S.Matrix([[a, -p], [p, a]])
    controller = S.diag(S.kronecker_product(g, S.eye(2)),
                        S.kronecker_product(g, g))
    eq(controller.H*controller, S.eye(8), "full retained Golden controller is unitary")
    eq(controller[0, 0], a, "port0 herald amplitude is sqrt(p)")
    eq(controller[4, 4], p, "port1 herald amplitude is p")
    for port, cost in ((0, 1), (1, 2)):
        col = controller[:, 4*port]
        eq(sum(S.conjugate(v)*v for v in col), 1,
           f"every flag output retained for port{port}")
        success = S.conjugate(col[4*port])*col[4*port]
        eq(success, p**cost, f"native probability cost marker for port{port}")
        eq(sum(S.conjugate(v)*v for j,v in enumerate(col) if j != 4*port),
           1-p**cost, f"complete failure probability for port{port}")
        eq(success**2, p**(2*cost), f"two flag copies implement distinct amplitude type {port}")
    eps = S.Symbol("eps", positive=True)
    delta = S.Matrix([[1, 0], [0, 2]])
    e1 = p*eps*delta
    e0 = S.eye(2)-e1
    gram = p*e0+p**2*e1
    eq(gram, p*S.eye(2)-eps*p**4*delta, "inherited all128 paid-cost Gram")
    eq((1-p)*e0+(1-p**2)*e1, S.eye(2)-gram,
       "all actual rejected flags give the required complement")
    ok(S.simplify(gram[0, 0]-gram[1, 1]) != 0,
       "one scalar cannot normalize a noncentral two-spectrum Gram")
    tangent = S.Matrix([[0, 1], [1, 0]])
    dg = -eps*p**4*tangent
    eq(S.trace(dg), 0, "scalar-shell diagnostic tangent is traceless")
    ok(dg != S.zeros(2), "scalar base normalization fails the transverse first jet")
    energy = S.Symbol("energy", real=True)
    mean_cost = 1+p*eps*energy
    success = p-eps*p**4*energy
    eq(success, p-p**3*(mean_cost-1), "herald calibrates actual known port cost")
    eq(S.diff(mean_cost, energy), -S.diff(success, energy)/p**3,
       "absolute known-cost source calibration")
    entropy = p+2*p**2
    eq(entropy, 2-p, "complete Golden flag entropy coefficient")
    ok(S.simplify(entropy-1) != 0, "entropy and executed gate slots are distinct")
    # Exact chain rule for a variable logical cost on a complete two-history control.
    q = S.Rational(2, 5)
    joint = [q*p, q*p**2,
             (1-q)*p**2, (1-q)*p**3, (1-q)*p**3, (1-q)*p**4]
    eq(sum(joint), 1, "full variable-length flag-pointer control is normalized")
    # Keep log(p) symbolic via exact Golden exponents; conditional entropy is c*h.
    conditional = q*(p+2*p**2)+(1-q)*(2*p**2+6*p**3+4*p**4)
    eq(conditional, entropy*(q+2*(1-q)),
       "all flag branches obey the complete variable-logical-cost entropy identity")
    # Structural inverse of the owned cost distribution, not a new native field.
    x = S.Symbol("x", real=True)
    weights = S.symbols("Q0:3", real=True)
    nodes = [S.Integer(1), p, p**2]
    polynomial = sum(weights[r]*x**r for r in range(3))
    basis = []
    for k in range(3):
        ell = S.prod((x-nodes[j])/(nodes[k]-nodes[j])
                     for j in range(3) if j != k)
        basis.append(ell)
        for j in range(3):
            eq(ell.subs(x, nodes[j]), int(j == k),
               f"Golden interpolation basis {k} at node {j}")
    samples = [p**(2*k)*polynomial.subs(x, nodes[k]) for k in range(3)]
    reconstructed = sum(p**(-2*k)*samples[k]*basis[k] for k in range(3))
    eq(S.expand(reconstructed-polynomial), 0,
       "all three n2 cost sectors recover from native Golden samples")
    eq(S.diff(reconstructed, x).subs(x, 1), weights[1]+2*weights[2],
       "Golden samples recover the exact mean-cost source coefficient")
    direction = [p, -(1+p), S.Integer(1)]
    eq(sum(direction), 0, "single-sample counterdirection preserves normalization")
    eq(sum(direction[r]*p**r for r in range(3)), 0,
       "single-sample counterdirection preserves the Golden herald")
    eq(sum(r*direction[r] for r in range(3)), p**2,
       "single-sample counterdirection has a nonzero mean-cost source")
    for n in range(1, 5):
        eq(sum(2*k*n for k in range(1, n+1)), n**2*(n+1),
           f"complete extra coherent schedule for horizon {n}")
    return {"status":"PASS","input_snapshot":"f7a8a534564be14d3f3f22874e6deb21ea2610d5",
            "source_pins":pins,"checks":checks,"check_count":len(checks),
            "environment":{"python":platform.python_version(),"sympy":S.__version__},
            "scope":{"actual_full128_effect_identity_consumed":True,
                     "original_full128_rows_replayed":False,
                     "coherent_schedule_gate_slots_per_round":2,
                     "interpolation_uses_independent_same_input_experiments":True,
                     "single_probe_determines_every_native_source":False,
                     "native_control_and_flag_supply_admission_assumed":True,
                     "full_Book_Info_derived":False,"GR_closed":False}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2)+"\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8", newline="\n")
    print(result, end="")
