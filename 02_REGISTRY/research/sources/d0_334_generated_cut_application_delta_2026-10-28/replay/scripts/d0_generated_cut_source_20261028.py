"""Exact application of the generated prefix-cut graph to the native QUERY.

All 32 fibre columns and every raw stage are checked in the Golden number
field. No dense clock heat eigensolver, continuous native gate admission or
physical GR selection is asserted.
"""
from pathlib import Path
import hashlib, importlib.util, json, sys
import sympy as S
from sympy.polys.matrices import DomainMatrix

root = Path.cwd()
folder = root / '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24'
expected = {
    'native_execution.py': '222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c',
    'book_price.py': '7c325fe6322298e13c2380522e9645cc228d8d5db2d7741368310690b80b095c',
    'BOOK_MAP.md': '4950d36010bd75bd26df13d9f13ff27843980a4fd35aefaac7dd950059fc21ee',
}
pins = {p: hashlib.sha256((folder / p).read_bytes()).hexdigest() for p in expected}
assert pins == expected
spec = importlib.util.spec_from_file_location('generated_cut_native', folder / 'native_execution.py')
n = importlib.util.module_from_spec(spec); sys.modules[spec.name] = n; spec.loader.exec_module(n)
F = n.GOLDEN_FIELD
def dm(x): return DomainMatrix.from_Matrix(S.Matrix(x)).convert_to(F)
I = dm(S.eye(32)); Z = dm(S.zeros(32))
def mm(*xs):
    y = xs[0]
    for x in xs[1:]: y = y.matmul(x)
    return y
def tr(x):
    a = x.to_dense().rep.to_ddm()
    return sum((a[i][i] for i in range(x.shape[0])), F.zero)
def equal(a, b): return (a-b).is_zero_matrix
def scalar(x): return F.from_sympy(S.sympify(x))
def show(x): return str(S.simplify(F.to_sympy(x)))
def ex(word): return n.Execution(5, (0,1), (4,), tuple(word), n.G_CX_SOURCE_I, 0, (2,3))
def swap(a,b): return (n.Gate('CX',(a,b)), n.Gate('CX',(b,a)), n.Gate('CX',(a,b)))
route = swap(0,1); si = n.Gate('SourceI',(0,2,3))
vword = route + (n.Gate('G',(0,)),) + route
vinv = n.inverse_word(ex(vword), max_qubits=5, max_expanded_stages=100)
query = vinv + route + (si,si) + route + vword
v = (n.Gate('G',(1,)),)
vi = n.inverse_word(ex(v), max_qubits=5, max_expanded_stages=100)
ea, eb = ex(vi+v+query), ex(vi+query+v)
inventories = []
for e in (ea,eb):
    n.validate_execution(e, max_qubits=5, max_expanded_stages=100)
    iv = n.inventory(e, max_qubits=5, max_expanded_stages=100)
    assert (iv.gate_count,iv.g_count,iv.cx_count,iv.source_i_count,iv.cut_rank)==(38,4,24,10,8)
    inventories.append({'G':iv.g_count,'CX':iv.cx_count,'SourceI':iv.source_i_count})
cache = {}
def matrices(e):
    out = []
    for g in e.gates:
        if g not in cache:
            cache[g] = dm(n.gate_matrix(e,g,max_qubits=5,max_expanded_stages=100))
        out.append(cache[g])
    return out
ga,gb = matrices(ea),matrices(eb)
def prefixes(gs):
    a=[I]
    for g in gs: a.append(mm(g,a[-1]))
    return a
xa,xb = prefixes(ga),prefixes(gb)
wa,wb = xa[-1],xb[-1]
vmat = dm(n.gate_matrix(ea,v[0],max_qubits=5,max_expanded_stages=100))
j = dm(n.input_isometry(ea,max_qubits=5,max_expanded_stages=100))
p = mm(j,j.transpose()); q=I-p
c=scalar(n.P**3); f=F.one-c*c; c2=2*c*c-F.one
assert equal(wa,wa.transpose()) and equal(mm(wa,wa),I)
assert equal(wa,dm(S.kronecker_product(S.eye(2),S.Matrix([[n.P**3,2*n.A*n.P],[2*n.A*n.P,-n.P**3]]),S.eye(8))))
assert equal(wb,mm(vmat,wa,vmat.transpose()))
assert equal(mm(p,wa,p),p.mul(c)) and equal(mm(p,wb,p),p.mul(c2))
assert not equal(mm(vmat,p,vmat.transpose()),p)
ew_a=mm(p,wa.transpose(),q,wa,p); ew_b=mm(p,wb.transpose(),q,wb,p)
assert equal(ew_a,p.mul(f)) and equal(ew_b,p.mul(F.one-c2*c2))
# Exact positivity, without a floating sign test: 3/5<p<2/3 implies
# 0<c²=p^6<(2/3)^6<1/4 and c2²-c²=(1-c²)(1-4c²)>0.
assert S.Rational(121,25)<5<S.Rational(49,9)
assert S.Rational(2,3)**6 < S.Rational(1,4)
assert c2*c2-c*c == (F.one-c*c)*(F.one-4*c*c)

# Every raw edge of the two complete clocks is exactly intertwined. The
# intertwiner at stage zero is V, which does NOT preserve the fixed input cut.
hs=[mm(xb[k],vmat,xa[k].transpose()) for k in range(38)]
for k in range(38):
    assert equal(mm(hs[(k+1)%38],ga[k],hs[k].transpose()),gb[k])
    assert equal(mm(hs[k].transpose(),hs[k]),I)

# Apply the full differential to the actual generated history cuts. A smooth
# comparison changes only g0 -> g0 exp(-tK), g_last -> exp(tK)g_last.
# Its endpoints are unitary comparisons, not newly admitted native primitives.
k=mm(wa,p)-mm(p,wa)
assert equal(k.transpose(),k.neg())
dgs=[Z for _ in ga]; dgs[0]=mm(ga[0],k).neg(); dgs[-1]=mm(k,ga[-1])
dx=[Z]
for z,g,dg in zip(xa,ga,dgs): dx.append(mm(dg,z)+mm(g,dx[-1]))
assert equal(dx[-1],mm(k,wa)-mm(wa,k))
ps=[mm(x,p,x.transpose()) for x in xa[:-1]]
dps=[mm(d,p,x.transpose())+mm(x,p,d.transpose()) for x,d in zip(xa[:-1],dx[:-1])]
zeta=scalar(S.Rational(1,2**20)); denominator=F.one-zeta*f
source_gate=F.zero;source_cut=F.zero
for t,g in enumerate(ga):
    nxt=(t+1)%38; pj,pn=ps[t],ps[nxt]; dpj,dpn=dps[t],dps[nxt]
    cc=mm(I-pn,g,pj)
    dc_gate=mm(I-pn,dgs[t],pj)
    dc_cut=mm(dpn,g,pj).neg()+mm(I-pn,g,dpj)
    if t<37:
        assert cc.is_zero_matrix and (dc_gate+dc_cut).is_zero_matrix
    ff=mm(cc.transpose(),cc)
    assert equal(mm(ff,ff),ff.mul(f))
    resolvent=I+ff.mul(zeta/denominator)
    source_gate+=2*zeta*tr(mm(resolvent,cc.transpose(),dc_gate))
    source_cut+=2*zeta*tr(mm(resolvent,cc.transpose(),dc_cut))
    if t==37:
        assert equal(ff,mm(xa[t],ew_a,xa[t].transpose()))
        df=mm((dc_gate+dc_cut).transpose(),cc)+mm(cc.transpose(),dc_gate+dc_cut)
        dew=mm(p,dx[-1].transpose(),q,wa,p)+mm(p,wa.transpose(),q,dx[-1],p)
        lift=mm(xa[t],dew,xa[t].transpose())
        connection=mm(dx[t],xa[t].transpose())
        assert equal(df,lift+mm(connection,ff)-mm(ff,connection))
half=2*8*zeta*c*f/denominator
assert source_gate==half and source_cut==half
assert source_gate+source_cut==4*8*zeta*c*f/denominator
assert equal(dew,p.mul(4*c*f))

out={
    'status':'PASS_GENERATED_CUT_SOURCE_AND_LITERAL_WORD_COMPARISON',
    'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'input_sha256':pins,
    'native_clock':38, 'full_fibre_dimension':32, 'input_rank':8,
    'bare_clock_heat_dimension':2*38*32, 'generated_history_cut_rank':38*8,
    'feedback_nonzero_rank':8, 'inventories':inventories,
    'all_clock_edges_intertwined':38, 'all_nonclosing_leakage_jets_zero':37,
    'cold_corners':['p^3 I_8','(2 p^6 - 1) I_8'],
    'initial_cut_transported_by_heat_intertwiner':False,
    'feedback_finite_gap':'J_A-J_B=8 log[(1-z+z(2p^6-1)^2)/(1-z+zp^6)]>0',
    'heat_gap':'0 exactly on the bare paired clock; same intertwining applies to homogeneous INTERNAL 501/502',
    'query_comparison_full_source':'4*8*z*c*(1-c^2)/(1-z+z*c^2)',
    'raw_gate_source_fraction':'1/2', 'generated_cut_source_fraction':'1/2',
    'zeta':'2^-20', 'source_value_for_orientation':str(S.N(F.to_sympy(source_gate+source_cut),20)),
    'scope':'all-column exact native finite words; smooth source is an ambient comparison on the causal graph, not a continuous native primitive or same-task admission theorem; no GR closure',
}
print(json.dumps(out,indent=2,sort_keys=True))
