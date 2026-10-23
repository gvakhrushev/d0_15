from pathlib import Path
import importlib.util, hashlib, json
from fractions import Fraction as F
import sympy as s
base=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('owner',base/'owned_ir_checker.py')
o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
raw=(base/'COLLAR_HESSIAN_ARB.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()==o.SOURCE_SHA
j=json.loads(raw); intervals=[[o.ball(x) for x in row] for row in j['K9'][0]]
H=[[sum((intervals[i][k][0],intervals[k][i][0]),F(0))/2 for k in range(9)] for i in range(9)]
rad=[[sum((intervals[i][k][1],intervals[k][i][1]),F(0))/2 for k in range(9)] for i in range(9)]
assert max(x for row in rad for x in row)<F(1,10**6)
I=o.PI;J=o.JI
A=[[H[i][k] for k in I] for i in I];B=[[H[i][k] for k in J] for i in I];C=[[H[i][k] for k in J] for i in J]
cmin=min(H[i][i]-rad[i][i]-sum(abs(H[i][k])+rad[i][k] for k in J if k!=i) for i in J)
assert cmin>4
assert max(abs(x) for row in B for x in row)<6
bcb=o.matmul(o.matmul(B,o.inverse_exact(C)),o.transpose(B))
M=[[A[i][k]-bcb[i][k] for k in range(3)] for i in range(3)]
margins=[M[i][i]-sum(abs(M[i][k]) for k in range(3) if k!=i) for i in range(3)]
ea,eb,ec=F(3,10**6),F(4,10**6),F(5,10**6)
err=ea+2*eb*30/4+eb**2/4+30**2*ec/16
assert min(margins)-err>F(2489,1000)
print('PASS pinned original L8 interval source: metric Schur >2489/1000 I')
# Exact algebraic controls; these are not an identification of the physical native action.
M=s.diag(3,4,5);C=s.diag(2,3);T=s.Matrix([[1,2,0],[0,-1,1]])
H0=(M+T.T*C*T).row_join(T.T*C).col_join((C*T).row_join(C))
def schur(H,n):
    A=H[:n,:n];B=H[:n,n:];C=H[n:,n:]
    return s.simplify(A-B*C.inv()*B.T)
assert schur(H0,3)==M
# Moving exact conditional self-code adds all three blocks, and is neutral after honest elimination.
L=s.Matrix([[1,0,1],[0,2,-1],[1,1,0]]);Q=s.diag(2,5,7)
Hbase=s.diag(H0,s.zeros(3))
D=(-L).row_join(s.zeros(3,2)).row_join(s.eye(3))
E=D.T*Q*D
assert schur(Hbase+E,3)==M
# A strict convex positive addition cannot reduce the metric source.
R=s.diag(1,2,3)
assert schur(Hbase+E+s.diag(R,s.zeros(5)),3)==M+R
# Omitting the direct Fisher field block would create a false cancellation.
Ebad=E.copy();Ebad[:3,:3]=s.zeros(3)
assert schur(Hbase+Ebad,3)==M-L.T*Q*L
assert schur(Hbase+Ebad,3)!=M
# Sharp genuine mixed correction: rank-three negative coupling can cancel all three metric directions.
Ec=s.zeros(8);Ec[:3,5:]=-M;Ec[5:,:3]=-M;Ec[5:,5:]=M
assert schur(Hbase+Ec,3)==s.zeros(3)
G=s.eye(3).col_join(-T).col_join(s.eye(3))
assert G.T*Ec*G==-M
# Congruence transform puts correction into diag(-M,0_2,M): precisely 3 negatives,3 positives,2 zeros.
P=s.eye(8);P[5:,:3]=s.eye(3)
assert P.T*Ec*P==s.diag(-M,s.zeros(2),M)
# A rank-two mixing can never supply rank-three compensation (exact witness).
L2=s.Matrix([[1,0,0],[0,1,0]])
assert (L2.T*L2).rank()==2
assert (M-L2.T*L2)[2,2]==5
print('PASS exact moving-KL neutral Schur, PSD monotonic witness, missing-direct-block hostile control')
print('PASS sharp three-negative-direction compensation and rank-two insufficiency controls')
# Four distinct positive-probability score classes attain rank three.
# This is a generic identity/control, not a choice of any native Book prices.
scores=s.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
assert s.ones(1,4)*scores==s.zeros(1,3)
assert scores.T*scores/4==s.eye(3)
beta=s.symbols('beta',positive=True)
y=s.Matrix(s.symbols('y0:3'))
partition=sum(s.exp(-beta*(scores[i,:]*y)[0]) for i in range(4))
free_energy=-s.log(partition)/beta
zero={yi:0 for yi in y}
assert s.Matrix([s.diff(free_energy,yi).subs(zero) for yi in y])==s.zeros(3,1)
assert s.simplify(s.hessian(free_energy,y).subs(zero))==-beta*s.eye(3)
print('PASS exact four-class Gibbs score identity: mean first source zero, negative rank-three covariance')
print('Scope: generic stationary-Hessian theorem + original fixed L8 gap; not full price selection or continuum GR')
