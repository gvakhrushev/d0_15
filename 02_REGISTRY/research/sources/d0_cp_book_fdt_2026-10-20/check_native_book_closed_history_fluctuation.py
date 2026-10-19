#!/usr/bin/env python3
"""Original closed K(9,11,13) scalar Book current fluctuation symmetry.
All finite n by reversal involution; explicit n=2..6 original multiplicity
controls; neither a compulsory full Book03 action nor a neutrino/GR theorem.
"""
import itertools
import sympy as sp

n = (9,11,13)
cycle = {(0,1),(1,2),(2,0)}
d = lambda a,b: 1 if (a,b) in cycle else -1
q = sp.symbols("q", positive=True)  # q=phi^(-epsilon)
T = sp.Matrix([[0,n[1]*q,n[2]/q],
               [n[0]/q,0,n[2]*q],
               [n[0]*q,n[1]/q,0]])
assert sp.simplify(sp.trace(T**3)-3861*(q**3+q**-3))==0
for length in range(2,7):
    counts = {}
    for word in itertools.product(range(3),repeat=length):
        if any(word[t]==word[(t+1)%length] for t in range(length)):
            continue
        current = sum(d(word[t],word[(t+1)%length])
                      for t in range(length))
        multiplicity = 1
        for zone in word: multiplicity *= n[zone]
        counts[current]=counts.get(current,0)+multiplicity
    assert all(counts[s] == counts[-s] for s in counts)
    if length==3:
        assert counts=={3:3861,-3:3861},counts
# Reversal is a bijection on legal closed walks with S->-S and
# weight ratio product(q^d)/product(q^(-d))=q^(2S).
print("PASS ORIGINAL_SCENE_ALL_CLOSED_CP_FLUCTUATION length 2..6")
print("All lengths: Pr(S)/Pr(-S)=q^(2S)=exp(-2 ln(phi) eps S)")
print("Length3: rooted forward and backward 3861 each (1287 unoriented triangles)")
print("All-length generating symmetry: psi_eps(k)=psi_eps(2ln(phi)eps-k)")
