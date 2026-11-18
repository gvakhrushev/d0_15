"""Check addressed identity-word relations and their rank on actual native columns."""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType
import sympy as sp

REV="15f5b786ed912a0e91d660e337bf60a7c15c7cfa"
OWNER="02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
SHA="222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"

def ensure(ok,what):
    if not ok:
        raise ValueError(what)

def solve(repo):
    src=subprocess.check_output(["git","-C",str(repo),"show",REV+":"+OWNER])
    ensure(sha256(src).hexdigest()==SHA,"native owner checksum")
    ne=ModuleType("pinned_native_gate_selection")
    sys.modules[ne.__name__]=ne
    exec(compile(src,OWNER,"exec"),ne.__dict__)
    live=(0,3,4)
    def cx(i,j):
        return ne.Gate("CX",(i,j))
    source=ne.Gate("SourceI",(0,1,2))
    gs=[ne.Gate("G",(i,)) for i in live]
    involutions=[cx(i,j) for i,j in permutations(live,2)]+[source]
    letters=involutions+gs
    baseline=cx(0,3)
    def execution(word):
        ex=ne.Execution(5,(),(),tuple(word),ne.G_CX_SOURCE_I,0,(1,2),())
        ne.validate_execution(ex,max_qubits=5,max_expanded_stages=100)
        return ex
    @lru_cache(maxsize=None)
    def operator(g):
        return sp.polys.matrices.DomainMatrix.from_Matrix(ne.gate_matrix(execution((g,)),g)).convert_to(ne.GOLDEN_FIELD)
    ident=sp.polys.matrices.DomainMatrix.eye(32,ne.GOLDEN_FIELD)
    def evaluate(word):
        execution(word)
        total=ident
        for g in word:
            total=operator(g)*total
        return total
    equations=[]; lengths=[]
    def relation(word):
        pair=(baseline,)*len(word)
        ensure(evaluate(word).to_sparse()==ident.to_sparse(),"left all-column identity")
        ensure(evaluate(pair).to_sparse()==ident.to_sparse(),"right all-column identity")
        a,b=Counter(word),Counter(pair)
        equations.append([a[g]-b[g] for g in letters])
        lengths.append(len(word))
    for g in involutions:
        relation((g,)*4)
    for g in gs:
        i=g.wires[0]
        move=() if i==0 else (cx(i,0),cx(0,i),cx(i,0))
        z=move+(source,source)+move
        relation(((g,)+z)*2)
    mat=sp.Matrix(equations)
    kernel=mat.nullspace()
    ensure(len(kernel)==1 and kernel[0]==sp.ones(len(letters),1),"only a common gate charge")
    return {"status":"PASS","commit":REV,"source_sha256":SHA,"native_columns":32,"work_addresses":list(live),
            "tested_pairs":len(equations),"word_lengths":lengths,"named_gate_count":len(letters),
            "relation_rank":mat.rank(),"kernel_generator":list(map(int,kernel[0])),
            "scope":"Fixed numerical addressed gate charges conditional on equal-length same-operator price descent; no assumed or fitted physical charges."}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,default=Path.cwd())
    print(json.dumps(solve(ap.parse_args().repo),indent=2))
