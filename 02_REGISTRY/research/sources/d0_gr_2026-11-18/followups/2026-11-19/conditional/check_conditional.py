"""Verify registered finite-word cylinder obstructions and H.1 score identities."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


def require(test, reason):
    if not test:
        raise ValueError(reason)


def source(root, path, digest):
    name = root / path
    require(hashlib.sha256(name.read_bytes()).hexdigest() == digest, f"pin failed: {name.name}")
    return name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    root = parser.parse_args().repo
    prefix = Path("02_REGISTRY/research/sources")
    native = source(root, prefix / "d0_native_execution_domain_2026-10-24/native_execution.py",
                    "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c")
    file = source(root, prefix / "d0_gr_2026-11-18/stages/04-absolute-calibration/primary/B121/check_book03_identity_pair.py",
                  "78f94decaf1ed6c54201e1e83032b9311ac708c077b79065398422c1141b66f9")
    spec = importlib.util.spec_from_file_location("native_cylinder_test", native)
    ne = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = ne
    spec.loader.exec_module(ne)
    # Reuse the two frozen word constructors without importing their separate historical Git audit.
    nodes = [n for n in ast.parse(file.read_text()).body
             if isinstance(n, ast.FunctionDef) and n.name in ("cx", "actual_words")]
    require(len(nodes) == 2, "two B121 constructors required")
    ns = {"ne": ne}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(file), "exec"), ns)
    words = ns["actual_words"]()
    p, a = ne.P, ne.A
    same = ne.exact_matrix_equal

    def full(w):
        ex = ne.Execution(4, (), (), tuple(w), ne.G_CX_SOURCE_I, 0, (2, 3))
        return ne.word_matrix(ex, max_qubits=4, max_expanded_stages=18)

    def proj(i):
        return sp.diag(*[int((k >> 2) % 2 == i) for k in range(16)])

    identity = sp.eye(16)
    tested = []
    for name, word in words.items():
        require(len(word) == 18 and same(full(word), identity), name)
        U, T = full(word[:1]), full(word[1:])
        for i in (0, 1):
            # Input restricted on target only: covers the eight remaining dimensions.
            P, Q = proj(i), proj(1 - i)
            A = Q*T*proj(0)*U*P
            B = Q*T*proj(1)*U*P
            require(same(A+B,sp.zeros(16)), "unread dark terminal")
            power = p**3 if name == "G_Z_G_Z" else 0
            require(same(A.H*A,power*P) and same(B.H*B,power*P), "dark origin")
            require(same(A.H*B,-power*P), "dark interference")
            tested.append([name,i,int(P.rank())])

    X = sp.Matrix([[0,1],[1,0]])
    v = sp.Matrix([a,p])
    Z = sp.diag(1,-1)
    require(same(Z*ne.G_LOCAL*Z,ne.G_LOCAL.T), "native inverse")
    require(same(ne.SOURCE_I_LOCAL**2,sp.kronecker_product(Z,sp.eye(4))), "native Z")
    require(same(ne.G_LOCAL.T*v,sp.Matrix([1,0])), "registered true zero")
    k = (v.T*X*v)[0]
    require(same(sp.Matrix([1-k*k]),sp.Matrix([p**6])), "physical marker distinguishability")
    err = 2*p**3*(1-k)
    read = sp.kronecker_product(ne.G_LOCAL.T,sp.eye(2))*sp.diag(sp.eye(2),X)*sp.kronecker_product(v,v)
    require(same(read[2:,:].T*read[2:,:],sp.Matrix([err])), "true CX then native inverse read")
    # The strong marker can be initialized by the paid native inverse and then copied by CX.
    read_orth = sp.kronecker_product(ne.G_LOCAL.T,sp.eye(2))*sp.diag(sp.eye(2),X)*sp.kronecker_product(v,sp.Matrix([1,0]))
    require(same(read_orth[2:,:].T * read_orth[2:,:],sp.Matrix([2*p**3])), "orthogonal marker")
    q,dq=sp.symbols("q dq",positive=True)
    u0,u1=-dq/(1-q),dq/q
    require(sp.factor((1-q)*u0+q*u1)==0,"centered binary score")
    require(sp.factor((1-q)*u0*u0+q*u1*u1-dq**2/(q*(1-q)))==0,"full binary score AF")
    print(json.dumps(dict(complete_native_input_supports=tested,
                          rank_per_input_target=8,canonical_marker_trace_distance=str(p**3),
                          canonical_marker_wrong_terminal=float(err),
                          orthogonal_marker_wrong_terminal=float(2*p**3),
                          unmarked_wrong_terminal=0,
                          both_B121_words_equal_identity=True,
                          noisy_H1_record_score_gram="dq squared / [q(1-q)]",
                          scope="No physical monetary weights or GR closure selected."),indent=2))


if __name__ == "__main__":
    main()
