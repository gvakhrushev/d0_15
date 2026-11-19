"""Exact zero-shift observer bridge R_E-R_L=2 R3-4 Delta_h N/N.

Pure differential geometry on a foliated smooth domain; not a native price owner.
The same ADM-sign identity is checked on mixed time/lapse, FRW and curved
spatial controls, with the Ricci tensor rebuilt from Christoffel symbols.
"""
import json
import sympy as s


def scalar(coords,g):
    n=len(coords);inv=g.inv()
    C=[[[s.factor(sum(inv[a,m]*(s.diff(g[m,j],coords[i])+s.diff(g[m,i],coords[j])-s.diff(g[i,j],coords[m]))/2 for m in range(n))) for j in range(n)] for i in range(n)] for a in range(n)]
    R=s.Matrix([[s.factor(sum(s.diff(C[k][i][j],coords[k])-s.diff(C[k][i][k],coords[j])+sum(C[k][k][m]*C[m][i][j]-C[k][j][m]*C[m][i][k] for m in range(n)) for k in range(n))) for j in range(n)] for i in range(n)])
    return s.factor(s.trace(inv*R))

def require(value,tag):
    if not bool(value):raise ArithmeticError(tag)

t,x,y,z=s.symbols('t x y z',real=True)
# Control I: nontrivial mixed time/space lapse and evolving spatial geometry.
N=1+t+x*x;A=1+t*x+x*x
E=scalar([t,x],s.diag(N*N,A*A))
L=scalar([t,x],s.diag(N*N,-A*A))
lap=s.diff(s.diff(N,x)/A,x)/A
K=s.diff(A,t)/(N*A)
trace_time= -2*s.diff(K,t)/N-2*K*K
require(s.factor(E-(-2*lap/N+trace_time))==0,"mixed_E_ADM")
require(s.factor(L-(+2*lap/N+trace_time))==0,"mixed_L_ADM")
require(s.factor(E-L+4*lap/N)==0,"mixed_difference")
# Control II: time evolution with spatially flat slices, three independent spatial coordinates.
a=1+t+t*t
E_FRW=scalar([t,x,y,z],s.diag(1,a*a,a*a,a*a))
L_FRW=scalar([t,x,y,z],s.diag(1,-a*a,-a*a,-a*a))
expect=-6*s.diff(s.diff(a,t),t)/a-6*(s.diff(a,t)/a)**2
require(s.factor(E_FRW-L_FRW)==0 and s.factor(E_FRW-expect)==0,"FRW_time_curvature_common")
# Control III: spatial curvature, product S^2 x S^1.
E_static=scalar([t,x,y,z],s.diag(1,1,s.sin(x)**2,1))
L_static=scalar([t,x,y,z],s.diag(1,-1,-s.sin(x)**2,-1))
require(s.factor(E_static-2)==0 and s.factor(L_static+2)==0,"static_spatial_curvature_sign")
# The full pointwise identity follows from Gauss-Codazzi for ADM zero shift:
# RE=R3-2 Delta_h N/N-2 d_t K/N-KijKij-K^2;
# RL=-R3+2 Delta_h N/N-2 d_t K/N-KijKij-K^2.
# The spatial integral of Delta_h N is a boundary contribution.
print(json.dumps({"controls":"PASS","mixed_lapse_exact":True,"FRW_R_equal":True,"spatial_R_opposite":True,"target":"R_L=R_E-2 R3 +4 Delta_h N/N","domain":"hypersurface-orthogonal observer, zero shift; no native action claim"},sort_keys=True,separators=(',',':')))
