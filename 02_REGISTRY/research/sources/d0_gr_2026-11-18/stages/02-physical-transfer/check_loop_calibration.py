"""A finite, native set of closed tests for positive monomial edge amplitudes."""
from collections import deque
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import json
import runpy
import sympy as sp

with redirect_stdout(StringIO()):
    orbit = runpy.run_path(str(Path(__file__).with_name("check_orbit.py")))
maps = orbit["maps"]
gates = sorted(maps, key=lambda g:(g.op,g.wires))
vertices = sorted({x for x,_ in orbit["states"]})
root = orbit["base"][0]
edges = [(x,g) for x in vertices for g in gates]
indices = {e:i for i,e in enumerate(edges)}
def end(x,g):
    return maps[g][x][0]
def inverse_path(path):
    return tuple(g for h in reversed(path) for g in (h,)*(3 if h.op=="SourceI" else 1))

paths={root:()}
queue=deque([root])
while queue:
    x=queue.popleft()
    for g in gates:
        y=end(x,g)
        if y not in paths:
            paths[y]=paths[x]+(g,)
            queue.append(y)
assert set(paths)==set(vertices)
rows=[]
lengths=[]
return_signs={-1:0,1:0}
for x,g in edges:
    y=end(x,g)
    loop=paths[x]+(g,)+inverse_path(paths[y])
    pos=root
    phase=1
    row=[0]*len(edges)
    for h in loop:
        row[indices[(pos,h)]]+=1
        phase*=maps[h][pos][1]
        pos=end(pos,h)
    assert pos==root
    return_signs[phase]+=1
    # G^T reads (a,p); G reads (a,-p). The marked component vanishes.
    golden=orbit["native"].G_LOCAL
    read_rotation=golden.T if phase==1 else golden
    prepared=sp.Matrix([orbit["native"].A,phase*orbit["native"].P])
    assert sp.expand((read_rotation*prepared)[1])==0
    rows.append(row)
    lengths.append(len(loop))
# Incidence acts on vertex potentials; the tests act on all edge log weights.
tests=sp.MutableSparseMatrix(rows)
incidence=sp.MutableSparseMatrix(len(edges),len(vertices),{})
for i,(x,g) in enumerate(edges):
    incidence[i,vertices.index(end(x,g))]+=1
    incidence[i,vertices.index(x)]-=1
assert tests*incidence==sp.zeros(len(edges),len(vertices))
rank=tests.to_DM().rank()
assert incidence.to_DM().rank()==len(vertices)-1
assert rank==len(edges)-len(vertices)+1

# An active-bus toll violates some of these actual tests.
toll=sp.Matrix([int(g.op=="SourceI" and bool(x & orbit["bit"](orbit["bus"]))) for x,g in edges])
violations=tests*toll
assert max(violations)>0
print(json.dumps({"status":"PASS","source":"literal forward CX/SourceI graph",
 "vertices":len(vertices),"addressed_generators":len(gates),"edge_slots":len(edges),
 "native_comparison_loops":len(rows),"max_native_loop_length":max(lengths),
 "native_dark_loops_by_sign":return_signs,
 "rational_test_rank":rank,"free_vertex_gauge_dimension":len(vertices)-1,
 "calibration_loops_sensitive_to_active_SourceI_toll":sum(1 for r in violations if r!=0),
 "scope":"Identifiability conditional on positive monomial transfer, common endpoint calibration and native odds. No absolute physical path price inferred."},indent=2))
