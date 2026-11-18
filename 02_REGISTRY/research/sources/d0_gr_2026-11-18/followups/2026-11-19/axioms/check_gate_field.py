"""Recover the coefficient field from one actual three-step H.1 substring."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType
import sympy as sp

REV = "0716b659d8e62c3fc7b72e3c817a8f7622ace0b4"
NATIVE = "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
NATIVE_SHA = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
WORD = "02_REGISTRY/research/sources/d0_gr_2026-11-18/current/check_return_interval.py"
WORD_SHA = "2107f716ca24c773475fe998be171830eba31761808e9b04201f417839460852"

def check(ok, label):
    if not ok:
        raise ValueError(label)

def git_source(repo, path, checksum):
    raw = subprocess.check_output(["git", "-C",str(repo),"show",REV+":"+path])
    check(hashlib.sha256(raw).hexdigest()==checksum, "unexpected source: "+path)
    return raw

def evaluate(repo):
    raw = git_source(repo,NATIVE,NATIVE_SHA)
    ne=ModuleType("d0_gate_field_native")
    sys.modules[ne.__name__]=ne
    exec(compile(raw,NATIVE,"exec"),ne.__dict__)
    circuit=git_source(repo,WORD,WORD_SHA)
    # Reuse only original gate declarations and the printed word constructor.
    tree=ast.parse(circuit)
    selected=[]
    names={"src","reader","tail","g","switch","swap","z"}
    for node in tree.body:
        if isinstance(node,ast.FunctionDef) and node.name in {"cx","execution","word"}:
            selected.append(node)
        if isinstance(node,ast.Assign):
            writes={n.id for dest in node.targets for n in ast.walk(dest) if isinstance(n,ast.Name)}
            if writes and writes<=names:
                selected.append(node)
    env={"ne":ne}
    exec(compile(ast.Module(body=selected,type_ignores=[]),WORD,"exec"),env)
    gates=env["word"](1,3)
    g=env["g"]
    a,b=env["swap"][:2]
    locations=[j+1 for j in range(len(gates)-2) if gates[j:j+3]==(g,a,b)]
    check(locations,"no contiguous G, CX, reverse CX on this routed word")
    field=ne.GOLDEN_FIELD
    def dm(gate):
        M=ne.gate_matrix(env["execution"]((gate,)),gate)
        return sp.polys.matrices.DomainMatrix.from_Matrix(M).convert_to(field)
    def trace(M):
        return sum((M[i,i].element for i in range(M.shape[0])), field.zero)
    A,B,G=(dm(x) for x in (a,b,g))
    W=B*A*G
    d=W.shape[0]
    acoef=field.from_sympy(ne.A); p=field.from_sympy(ne.P)
    t1=trace(W)/d
    t2=trace(W*W)/d
    check(t1==(acoef+p)/4 and t2==(acoef-p)**2/4,"both 64-column trace moments")
    invariant=t2/t1**2
    check(invariant==4*(1-acoef)**2/(1+acoef)**2,"projective invariant")
    check((1+p)*(4-invariant)/(2*(4+invariant))==acoef,"recover native half-density")
    x,t=sp.symbols("x t")
    monic=x**4+x**2-1
    inv_poly=sp.Poly(sp.resultant(monic,t*(1+x)**2-4*(1-x)**2,x),t)
    cp_poly=sp.Poly(sp.resultant(monic,t*(1+x)**4-16*(1-x)**4,x),t)
    check(inv_poly.is_irreducible and cp_poly.is_irreducible and inv_poly.degree()==cp_poly.degree()==4,
          "minimal polynomials and both orbit sizes")
    check(field.from_sympy(sp.sqrt(ne.P))==acoef,"real positive branch")
    return {"status":"PASS","primary_revision":REV,"word_sha256":WORD_SHA,"native_sha256":NATIVE_SHA,
        "native_word":{"N":3,"n":1,"steps":len(gates),"substring_first_stages_one_based":locations,"checked_columns":d},
        "arithmetic":{"p":"phi^(-1)","a":"sqrt(p)","normalized_trace_W":"(a+p)/4",
        "normalized_trace_W2":"(a-p)^2/4","projective_index":"4*((1-a)/(1+a))^2",
        "index_numerical":str(sp.N(field.to_sympy(invariant),26)),"channel_index":"index^2",
        "index_minpoly":str(inv_poly.as_expr()),"channel_index_minpoly":str(cp_poly.as_expr()),
        "half_density_from_index":"(1+p)*(4-index)/(2*(4+index))"},
        "scope":"No finite golden path spelling by finite role phases on this full carrier, including scalar normalization. Full physical source and normalized prepared-only data remain separate."}

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,default=Path.cwd())
    print(json.dumps(evaluate(ap.parse_args().repo),indent=2))
