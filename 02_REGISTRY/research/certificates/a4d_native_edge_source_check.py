#!/usr/bin/env python3
"""Exact local-source quotient/Riesz controls on the actual simple Role graph.

The all-size proofs and physical scope are in A4D_NATIVE_EDGE_SOURCE_QUOTIENT.md.
Default replay is immutable. A source-readout inverse is not the GR range solve.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy import sparse
import sympy as sp

INPUT_HEAD = "2cba34623e346eb75a7a9ae42a550e4a52178a54"
INPUTS = [
    "03_FORMALIZATION/D0/Geometry/ArchiveLocalLaplacianVariation.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveStressEdgeReadout.lean",
    "03_FORMALIZATION/D0/Geometry/ArchivePhaseEdgeMetricScale.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveFieldEquation.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveVariation.lean",
    "03_FORMALIZATION/D0/Matter/ArchiveStressCoupling.lean",
    "03_FORMALIZATION/D0/Frozen/ConservedStressProjection.lean",
]


def graph(d, L):
    sites = list(product(range(L), repeat=d)); index = {x:i for i,x in enumerate(sites)}
    V = len(sites); edge = set()
    for x in sites:
        for a in range(d):
            y = list(x); y[a] = (y[a]+1)%L
            edge.add(tuple(sorted((index[x],index[tuple(y)]))))
    edges = sorted(edge); E = len(edges); rr = []; cc = []; vv = []; ar = []; ac = []
    for e,(u,v) in enumerate(edges):
        rr += [u*V+u,v*V+v,u*V+v,v*V+u]; cc += [e]*4; vv += [1,1,-1,-1]
        ar += [u,v]; ac += [e,e]
    B = sparse.csc_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(V*V,E))
    A = sparse.csc_matrix((np.ones(2*E,dtype=np.int64),(ar,ac)),shape=(V,E))
    return sites, edges, B, A


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo",type=Path,default=Path(__file__).resolve().parents[3])
    ap.add_argument("--output",type=Path); ap.add_argument("--expect",type=Path)
    args = ap.parse_args(); repo = args.repo.resolve(); checks = []
    sha = lambda p:hashlib.sha256((repo/p).read_bytes()).hexdigest()
    def check(name, value):
        assert bool(value),name
        checks.append(name); print("PASS_"+name,flush=True)
    receipt_path = "02_REGISTRY/research/certificates/a4d_native_edge_source_results.json"
    receipt = json.loads((repo/receipt_path).read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0 and not receipt["sorryAx"]
    assert receipt["printed_axiom_dependencies"] == 11 and len(receipt["transitive_d0_source_sha256"]) == 35
    for p,digest in {**receipt["transitive_d0_source_sha256"],**receipt["toolchain_input_sha256"],
                    receipt["capsule"]:receipt["capsule_sha256"],receipt["output"]:receipt["output_sha256"]}.items():
        assert sha(p) == digest,"LEAN_INPUT_CHANGED: "+p
    check("COMPILED_ACTUAL_LOCAL_SOURCE_QUOTIENT",True)
    spectra = {}
    for d,L in [(1,2),(1,3),(1,4),(2,2),(2,3),(4,2),(4,3),(4,4)]:
        sites,edges,B,A = graph(d,L); V = len(sites); E = len(edges); K = B.T@B
        key = str(d)+"d_L"+str(L); c = L*L
        check("EXACT_SIMPLE_GRAPH_GRAM_"+key,(K-A.T@A-2*sparse.eye(E,dtype=np.int64)).nnz == 0)
        w = np.array([(i%7)-3 for i in range(E)],dtype=np.int64)
        Dw = np.asarray(c*(B@w)).reshape(V,V)
        check("ACTUAL_CONDUCTANCE_FORWARD_AND_POSITIVITY_"+key,
              np.array_equal(Dw,Dw.T) and np.all(Dw.sum(axis=1) == 0)
              and int((Dw*Dw).sum()) == c*c*(2*int(w@w)+int((A@w)@(A@w))))
        T = np.fromfunction(lambda i,j: ((i+1)*(j+1))%11,(V,V),dtype=int).astype(np.int64)
        readout = np.array([c*(T[u,u]+T[v,v]-2*T[u,v]) for u,v in edges],dtype=np.int64)
        check("ALL_NATIVE_EDGE_READOUTS_AND_PACKED_FACTOR_"+key,
              np.array_equal(readout,c*(B.T@T.reshape(-1))) and int((T*Dw).sum()) == int(readout@w))
        for e,(u,v) in enumerate(edges):
            assert Dw[u,v] == -c*w[e]
        check("LITERAL_RECOVER_CONDUCTANCE_"+key,True)
        degree = d if L == 2 else 2*d
        adjval = {2:[1,-1],3:[2,-1,-1],4:[2,0,-2,0]}[L]
        eigen = Counter({2:E-V})
        for k in product(range(L),repeat=d): eigen[2+degree+sum(adjval[x] for x in k)] += 1
        assert min(eigen.values()) >= 0 and sum(eigen.values()) == E
        P = sparse.eye(E,dtype=np.int64,format="csc")
        for power in range(1,5):
            P = P@K
            assert int(P.diagonal().sum()) == sum(v**power*m for v,m in eigen.items()),(key,power)
        check("COMPLETE_SYMBOL_FOUR_EXACT_TRACE_MOMENTS_"+key,True)
        spectra[key] = {"vertices":V,"edges":E,"unscaled_Riesz_eigenvalues":{str(k):v for k,v in sorted(eigen.items()) if v},
                       "scale":c,"symmetric_source_kernel_dimension":V*(V+1)//2-E,
                       "conserved_symmetric_source_kernel_dimension":V*(V-1)//2-E}

    sites,edges,B,A = graph(4,2); V = len(sites); E = len(edges); BB = sp.Matrix(B.toarray()); KK = BB.T*BB
    r = sp.Matrix([(-1)**i*(i+1) for i in range(E)]); weights = KK.inv()*r
    source = BB*weights
    check("EXACT_UNIQUE_LOCAL_SOURCE_RECOVERY",BB.T*source == r and KK.det() != 0)
    T = sp.Matrix(V,V,list(source))
    check("RECOVERED_LOCAL_SOURCE_IS_SYMMETRIC_CONSERVED",T == T.T and T*sp.ones(V,1) == sp.zeros(V,1))
    # A nonlocal conserved matrix remains in the observable kernel. No gauge label.
    u = sites.index((0,0,0,0)); v = sites.index((1,1,0,0)); z = sp.zeros(V,1); z[u]=1; z[v]=-1
    H = z*z.T; h = sp.Matrix(list(H)); invisible = h-BB*(KK.inv()*(BB.T*h))
    TI = sp.Matrix(V,V,list(invisible))
    check("NONZERO_CONSERVED_SOURCE_KERNEL_IS_RETAINED",BB.T*invisible == sp.zeros(E,1)
          and TI == TI.T and TI*sp.ones(V,1) == sp.zeros(V,1) and TI[u,v] == -1)
    check("ALL_ONES_SHIFT_INVISIBLE_BUT_IDENTITY_VISIBLE",BB.T*sp.ones(V*V,1) == sp.zeros(E,1)
          and BB.T*sp.Matrix(list(sp.eye(V))) == 2*sp.ones(E,1))
    nonsymmetric = sp.Matrix([[0,1],[0,0]]); edge_test = sp.Matrix([[1,-1],[-1,1]])
    check("SYMMETRY_HYPOTHESIS_CANNOT_BE_REMOVED",sum(x*y for x,y in zip(nonsymmetric,edge_test)) == -1
          and nonsymmetric[0,0]+nonsymmetric[1,1]-2*nonsymmetric[0,1] == -2)

    phase = {}
    for L in [3,4,5,8,12,16]:
        C = sp.zeros(L)
        for i in range(L):
            C[i,i] = 2; C[i,(i+1)%L] = -1; C[i,(i-1)%L] = -1
        F = sp.zeros(L+1)
        for i in range(L+1):
            F[i,i] = 2; F[i,(i+1)%(L+1)] = -1; F[i,(i-1)%(L+1)] = -1
        J = sp.Matrix(L+1,L,lambda i,j:int(j == i%L)); D = F*J-J*C; G = -2*J.T*D
        basis = []
        for i in range(L):
            z = sp.zeros(L,1);z[i]=1;z[(i+1)%L]=-1;basis.append(z*z.T)
        dot = lambda X,Y:sum(x*y for x,y in zip(X,Y))
        response = sp.Matrix([dot(G,e) for e in basis])
        check("LITERAL_PHASE_TWO_LOCAL_SOURCE_TESTS_"+str(L),
              [dot(G,basis[0]),dot(G,basis[1]),dot(C,basis[0]),dot(C,basis[1])] == [6,0,6,6])
        gram = sp.Matrix(L,L,lambda i,j:dot(basis[i],basis[j])); w = gram.inv()*response
        check("SIGNED_LOCAL_SOURCE_RECOVERY_PROTECTS_WEAK_GATE_"+str(L),
              gram*w == response and any(a<0 for a in w))
        phase[str(L)] = {"edge_response":[str(x) for x in response],"unique_unscaled_local_weights":[str(x) for x in w]}
    alpha = sp.symbols("alpha",real=True)
    check("SHARP_TWO_PROBE_SCALAR_SOURCE_RESIDUAL",sp.expand((6-6*alpha)**2+(6*alpha)**2-18-72*(alpha-sp.Rational(1,2))**2) == 0)
    payload = {"status":"PASS","input_head":INPUT_HEAD,"inputs_sha256":{p:sha(p) for p in INPUTS},
        "lean_receipt_sha256":sha(receipt_path),"checks":checks,"finite_graph_spectra":spectra,"phase_source_controls":phase,
        "scope":"Actual finite local stress quotient and counting Riesz inverse, plus separately stated canonical phase-source obstruction; no physical source action or coupled GR range theorem.",
        "Riesz_Gram":"c^2 (2 I + A^T A)","four_role_sharp_lower_eigenvalue":"2 L^4",
        "four_role_condition_number_L_ge_3":"9","phase_two_probe_residual_squared_minimum":"18",
        "protected_exceptions":["Non-symmetric raw source uses both off-diagonal entries","L=2 simple graph merges plus/minus neighbors",
            "Readout-kernel is not automatically physical gauge","A reconstructed source is not independently generated matter",
            "Counting readout inverse does not solve metric-connection-matter equations","Phase and four-Role carriers and normalizations remain distinct"]}
    out = json.dumps(payload,sort_keys=True,indent=2)+"\n"
    if args.output:args.output.write_text(out)
    else:
        expected = args.expect or Path(__file__).with_name("a4d_native_edge_source_certificate.json")
        assert expected.read_text() == out,"PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER")
    print("PASS_NATIVE_EDGE_SOURCE",len(checks))


if __name__ == "__main__": main()
