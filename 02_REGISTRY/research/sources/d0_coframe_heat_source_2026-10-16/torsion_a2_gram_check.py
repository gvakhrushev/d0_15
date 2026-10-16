from pathlib import Path
import ast, hashlib, json
from functools import lru_cache
import sympy as s

repo = Path(__file__).resolve().parents[4]
source = repo/'02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
data = source.read_bytes()
expected = 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da'
if hashlib.sha256(data).hexdigest() != expected:
    raise ArithmeticError('owned_creator_source_pin')
tree = ast.parse(data)
nodes = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name == 'creator') or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXTERIOR_ORDER' for t in n.targets))]
scope = {'s':s,'lru_cache':lru_cache}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),scope)
C = [scope['creator'](i) for i in range(4)]
A = [c.T for c in C]
gamma = [C[i]-A[i] for i in range(4)]
coords = [(a,b,c) for a in range(4) for b in range(4) for c in range(b+1,4)]
checks=[]
def eq(actual,expected,name):
    if actual != expected:
        if isinstance(actual,s.MatrixBase):
            if actual.shape != expected.shape or any(s.expand(x)!=0 for x in actual-expected):
                raise ArithmeticError(name)
        elif s.expand(actual-expected)!=0:
            raise ArithmeticError(name)
    checks.append(name)
for i in range(4):
    for j in range(4):
        eq(C[i]*A[j]+A[j]*C[i],int(i==j)*s.eye(16),'actual_CAR_%s_%s'%(i,j))
Z=[]
for a,b,c in coords:
    Q=C[b]*C[c]*A[a]
    Z.append(Q+Q.T)
flat=s.Matrix.hstack(*[z.reshape(256,1) for z in Z])
Gram = -flat.T*flat
for i in range(4):
    anti = s.Matrix.hstack(*[(gamma[i]*z+z*gamma[i]).reshape(256,1) for z in Z])
    Gram += anti.T*anti/4
Gram=s.simplify(Gram)
eq(Gram,Gram.T,'quadratic_form_exact_symmetric')
# Direct trace formula for every entry, independent of flatten/skew shortcut.
for i in range(24):
    for j in range(i,24):
        direct = -s.trace(Z[i]*Z[j])-sum(s.trace((g*Z[i]+Z[i]*g)*(g*Z[j]+Z[j]*g)) for g in gamma)/4
        eq(Gram[i,j],direct,'direct_trace_entry_%s_%s'%(i,j))

def val(row,a,b,c):
    if b==c:return s.Integer(0)
    if b<c:return row[coords.index((a,b,c))]
    return -row[coords.index((a,c,b))]
trace_map=s.Matrix(4,24,lambda j,k:sum(val(s.eye(24)[:,k],a,a,j) for a in range(4)))
triples=[(a,b,c) for a in range(4) for b in range(a+1,4) for c in range(b+1,4)]
axial_map=s.Matrix(4,24,lambda j,k:sum(val(s.eye(24)[:,k],a,b,c) for a,b,c in (triples[j],triples[j][1:]+triples[j][:1],triples[j][2:]+triples[j][:2])))
trace_basis=s.Matrix(24,4,lambda k,j:int(coords[k][0]==coords[k][1])*int(coords[k][2]==j)-int(coords[k][0]==coords[k][2])*int(coords[k][1]==j))
axial_basis=s.Matrix(24,4,lambda k,j:s.LeviCivita(*coords[k],j))
tensor_basis=s.Matrix.hstack(*trace_map.col_join(axial_map).nullspace())
eq(trace_map*trace_basis,3*s.eye(4),'trace_component_exact_projection_factor')
eq(trace_map*axial_basis,s.zeros(4),'axial_has_zero_trace')
eq(axial_map*trace_basis,s.zeros(4),'trace_has_zero_threeform')
eq(trace_basis.T*trace_basis,3*s.eye(4),'trace_basis_natural_norm')
eq(axial_basis.T*axial_basis,3*s.eye(4),'axial_basis_natural_norm')
eq(trace_map*tensor_basis,s.zeros(4,16),'tensor_zero_trace')
eq(axial_map*tensor_basis,s.zeros(4,16),'tensor_zero_threeform')
eq(trace_basis.T*axial_basis,s.zeros(4),'irreps_orthogonal_trace_axial')
eq(trace_basis.T*tensor_basis,s.zeros(4,16),'irreps_orthogonal_trace_tensor')
eq(axial_basis.T*tensor_basis,s.zeros(4,16),'irreps_orthogonal_axial_tensor')
full=trace_basis.row_join(axial_basis).row_join(tensor_basis)
if full.rank()!=24:raise ArithmeticError('complete_irrep_decomposition')
checks.append('complete_irrep_decomposition')
eigenvalues=Gram.eigenvals()
results={}
for name,basis in [('trace4',trace_basis),('threeform4',axial_basis),('tensor16',tensor_basis)]:
    restricted=basis.T*Gram*basis
    value=next((Gram*basis)[i,j]/basis[i,j] for i in range(24) for j in range(basis.cols) if basis[i,j]!=0)
    eq(Gram*basis,value*basis,'SO4_irrep_scalar_'+name)
    results[name]={'dimension':basis.cols,'Gram_eigenvalue_natural_coordinate_norm':str(value),'restricted_Gram':[[str(x) for x in row] for row in restricted.tolist()]}
positive=sum(int(mult) for eig,mult in eigenvalues.items() if eig>0)
negative=sum(int(mult) for eig,mult in eigenvalues.items() if eig<0)
zero=sum(int(mult) for eig,mult in eigenvalues.items() if eig==0)
# named pp-wave first-gradient tangent in natural theta frame:
# theta0=(1+H/2)dt+(H/2)dz, theta3=-(H/2)dt+(1-H/2)dz.
# At H=0, T^0_i0=T^0_i3=Hi/2, T^3_i0=T^3_i3=-Hi/2.
hx,hy=s.symbols('Hx Hy',real=True)
tpp=s.zeros(24,1)
def add_t(a,b,c,v):
    if b<c:tpp[coords.index((a,b,c))]+=v
    elif c<b:tpp[coords.index((a,c,b))]-=v
for i,hi in ((1,hx),(2,hy)):
    add_t(0,i,0,hi/2);add_t(0,i,3,hi/2)
    add_t(3,i,0,-hi/2);add_t(3,i,3,-hi/2)
print(json.dumps({'schema':'d0-torsion-a2-gram-exact/1','status':'PASS_EXACT','coordinates':coords,'Gram':[[str(x) for x in row] for row in Gram.tolist()],'rank':Gram.rank(),'inertia':{'positive':positive,'negative':negative,'zero':zero},'eigenvalues':{str(k):int(v) for k,v in eigenvalues.items()},'irreps':results,'kernel_basis':[[str(x) for x in v] for v in Gram.nullspace()],'ppwave_at_H0_q':str(s.factor((tpp.T*Gram*tpp)[0])),'checks':len(checks),'checks_sha256':hashlib.sha256('\n'.join(checks).encode()).hexdigest(),'owned_source_sha256':expected,'owned_exterior_order':scope['EXTERIOR_ORDER'],'scope':'quadratic no-derivative a2 difference; native operator baseline/LC/source identity remain external hypotheses'},sort_keys=True))
