"""Exact non-null Einstein-scalar witness separating existing source carriers.

The metric is an analytical continuum comparison. This is not a finite
native execution, selected field equation, exact discrete root or GR closure.
"""
from pathlib import Path
import hashlib, json
import sympy as s

if not __debug__:
 raise RuntimeError('exact checks require normal Python; assertions must remain enabled')
root=Path.cwd()
expected={
 '02_REGISTRY/research/A4D_DENSITY_INVOLUTION_COMPLETE_PRICE_GENERAL_SOURCE_2026_10_27.md':'320e342c43fd6d4d1f57d3cc288652d1d8b964d577ed55dc580bc3fac556210b',
 '02_REGISTRY/research/A4D_PARITY_RESOLVED_GEOMETRIC_SOURCE_GLOBAL_2026_10_27.md':'43e94708f85630c9c86e92c6b257eadd96f382acd5f2e462ef8fae58095ef6ee',
 '02_REGISTRY/research/A4D_NATIVE_CLOCK_FULL_PRICE_COMPILATION_AND_FINITE_TEST_RECOVERY_2026_10_27.md':'f23ef19ff9c09e51b9091fd5da8b3936d3a66ac243d157c7a016318c778d28af',
 '02_REGISTRY/research/A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md':'10fe4ed60c0796ccd5bd46a2ca2438aaef8be01e0980b39979d77563c8ff5f05',
}
pins={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in expected}
if pins!=expected:
 raise RuntimeError('source input changed: review and repin before replay')
t,k=s.symbols('tau kappa',positive=True)
x,y,z=s.symbols('x y z',real=True);coords=[t,x,y,z]
eta=s.diag(1,-1,-1,-1)
e=s.diag((2*t)**s.Rational(-1,2), *[(2*t)**s.Rational(1,6)]*3)
g=s.simplify(e.T*eta*e); gi=s.simplify(g.inv())
E=s.simplify(e.det()); assert E==1 and s.simplify(g.det())==-1
phi=s.log(2*t)/(2*s.sqrt(3*k)); dp=s.Matrix([s.diff(phi,v) for v in coords])
q=s.simplify((dp.T*gi*dp)[0]); assert q==1/(6*k*t)
Gamma=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in range(4))) for c in range(4)] for b in range(4)] for a in range(4)]
Ric=s.zeros(4)
for a in range(4):
 for b in range(4):
  Ric[a,b]=s.simplify(sum(s.diff(Gamma[c][a][b],coords[c])-s.diff(Gamma[c][a][c],coords[b])+sum(Gamma[c][a][b]*Gamma[d][c][d]-Gamma[d][a][c]*Gamma[c][b][d] for d in range(4)) for c in range(4)))
R=s.simplify(s.trace(gi*Ric)); assert R==1/(3*t)
Ein=s.simplify(Ric-g*R/2);stress=s.simplify(2*dp*dp.T-g*q)
assert all(s.simplify(v)==0 for v in Ein-k*stress)
wave=s.simplify(sum(s.diff(sum(gi[a,b]*dp[b] for b in range(4)),coords[a]) for a in range(4)))
assert wave==0
# The independent Palatini connection equation is retained: the tetrad
# connection associated with Gamma is Lorentz and torsion-free.
ei=s.simplify(e.inv());omega=[]
for mu in range(4):
 om=s.zeros(4)
 for a in range(4):
  for b in range(4):
   om[a,b]=s.simplify(sum((sum(e[a,nu]*Gamma[nu][mu][rho] for nu in range(4))-s.diff(e[a,rho],coords[mu]))*ei[rho,b] for rho in range(4)))
 assert all(s.simplify(v)==0 for v in om.T*eta+eta*om)
 omega.append(om)
for mu in range(4):
 for nu in range(4):
  torsion=s.simplify(e[:,nu].diff(coords[mu])-e[:,mu].diff(coords[nu])+omega[mu]*e[:,nu]-omega[nu]*e[:,mu])
  assert all(v==0 for v in torsion)
curvature=[[s.simplify(omega[nu].diff(coords[mu])-omega[mu].diff(coords[nu])+omega[mu]*omega[nu]-omega[nu]*omega[mu]) for nu in range(4)] for mu in range(4)]
def contract_curvature(left,right):
 return s.simplify(sum(left[mu,a]*right[nu,b]*curvature[mu][nu][a,b]*eta[b,b] for mu in range(4) for nu in range(4) for a in range(4) for b in range(4)))
assert s.simplify(contract_curvature(ei,ei)-R)==0

# Original direct-star continuum density: E R/2 + lambda q, lambda=-k.
# Metric derivative uses independently varied inverse metric, before
# connection elimination. Standard scalar density instead has E lambda q.
direct=s.simplify(E*Ein/2-k*dp*dp.T)
assert all(s.simplify(v)==0 for v in direct+k*q*g/2)
assert direct!=s.zeros(4)
fstar=s.simplify(E*R/2); assert fstar==1/(6*t)
coframe=s.zeros(4)
for a in range(4):
 for mu in range(4):
  de=s.zeros(4);de[a,mu]=1
  dg=de.T*eta*e+e.T*eta*de
  dgi=-gi*dg*gi
  value=s.simplify(sum(direct[i,j]*dgi[i,j] for i in range(4) for j in range(4)))
  coframe[a,mu]=value
  assert s.simplify(value-fstar*ei[mu,a])==0
  # Independent Palatini variation holds every omega_mu FIXED. It does
  # not silently impose delta omega=delta Levi-Civita before variation.
  dei=-ei*de*ei;dE=E*s.trace(ei*de)
  dR=contract_curvature(dei,ei)+contract_curvature(ei,dei)
  palatini=s.simplify(dE*R/2+E*dR/2-k*(dp.T*dgi*dp)[0])
  assert s.simplify(palatini-value)==0
radial=s.simplify(sum(coframe[a,mu]*e[a,mu] for a in range(4) for mu in range(4)))
assert radial==2/(3*t)

# Fixed-point equality of the two metrics does NOT identify their full
# sources: S_star-S_mom=(1-1/E)fstar, so at E=1 its source is fstar dE.
dd,ff,dff,dE=s.symbols('density f df dE',real=True)
diffjet=(1-1/dd)*dff+ff*dE/dd**2
assert s.simplify(diffjet.subs(dd,1)-ff*dE)==0
# A nonnegative compact smooth radial test with a plateau on
# [2/3,5/6] x [1/3,2/3]^3 has an explicit lower source bound.
margin=s.Rational(4,5)*s.Rational(1,6)*s.Rational(1,27)
assert margin==s.Rational(2,405)>0

# Original fixed Golden ratio, not a fitted cosmological coefficient.
p=(s.sqrt(5)-1)/2;zz=s.Rational(1,2**20)
QE=1-4*zz*p**3;RE=1-4*zz*p**3*(1+p**6)
k_native=s.simplify(2*p**(-5)*(RE/QE+p**6))
# Derive the identical coefficient from the actual sigma-minus report.
xx,yy=s.symbols('x_click y_click',real=True)
event=p**2*(1+xx);ell=4*event*(1-event)
bb=p-p**2*yy;beta_report=4*bb**2*(1-bb**2)
aa=ell+(1-ell)*beta_report
report=zz*(aa+beta_report)-zz**2*aa*beta_report
rf=s.simplify(s.diff(report,xx).subs({xx:0,yy:0}))
rq=s.simplify(s.diff(report,yy).subs({xx:0,yy:0}))
assert s.simplify(rq/rf+k_native)==0
# Rational proof k_native>20 using p<619/1000 and RE/QE>1-10^-6.
assert s.Rational(619,1000)>s.Rational(3,5)
assert s.Rational(5,1)<(2*s.Rational(619,1000)+1)**2
assert 0<zz<s.Rational(1,10**6)
assert 4*s.Rational(619,1000)**9/(1-4*s.Rational(1,10**6))<1
# RE/QE=1-4 z p^9/QE and QE>1-4e-6 establish the latter bound.
assert 2*(s.Rational(1000,619))**5*(1-s.Rational(1,10**6))>20
# On the unit coordinate slab tau in(1/4,5/4), |log(2tau)|<1:
# exp(1)>1+1+1/2+1/6>5/2 and exp(1)>2.
# Hence phi^2<1/(12*k)<1/240<(3/20)^2 while p/4>3/20.
assert s.Rational(5,2)<1+1+s.Rational(1,2)+s.Rational(1,6)
assert s.Rational(1,240)<s.Rational(3,20)**2
assert s.Rational(5,1)>(2*s.Rational(3,5)+1)**2

out={
 'status':'PASS_NON_NULL_DENSITY_SOURCE_SEPARATION',
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'input_sha256':pins,
 'metric':'diag((2tau)^-1,-(2tau)^(1/3),-(2tau)^(1/3),-(2tau)^(1/3))',
 'det_coframe':str(E),'Ricci_scalar':str(R),'matter_kinetic':str(q),
 'Einstein_scalar_components_checked':16,'Klein_Gordon':str(wave),
 'Lorentz_connection_and_torsion':'exact zero for all components',
 'independent_Palatini_variation':'all 16 coframe rows checked at fixed omega from its curvature two-form',
 'direct_star_metric_source':'-kappa*q*g/2',
 'direct_star_coframe_source':'fstar*transpose(inverse(e))',
 'radial_source_density':str(radial),'compact_test_margin':str(margin),
 'native_kappa_for_orientation':str(s.N(k_native,30)),
 'native_ratio':'-r_y(0,0)/r_x(0,0)=kappa_native>20, exact polynomial and rational bounds',
 'density_metric_at_witness':'g_tilde=g but full coframe sources differ',
 'scope':'exact continuum comparison on fixed uniform units/density; no discrete root, emitted GR word, physical source selection or GR closure',
}
print(json.dumps(out,indent=2,sort_keys=True))
