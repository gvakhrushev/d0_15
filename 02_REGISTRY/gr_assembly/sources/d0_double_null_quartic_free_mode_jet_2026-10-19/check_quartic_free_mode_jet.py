"""Exact mixed quartic crossed-null Euler jet with free cubic modes.

At h=1 on the original six-plaquette action, parameterize both 134-dimensional
cubic correction families, then solve the [a^2*b^2] equations jointly with all
268 cubic modes and independent degree-at-most-five quartic corrections. The
checker replays all 40 Euler rows at every retained amplitude coefficient.
"""
import importlib.util
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix

ROOT=Path(__file__).resolve().parents[4]
SRC=ROOT/'02_REGISTRY/gr_assembly/sources'
BASE=SRC/'d0_double_null_cubic_uniform_control_2026-10-19/check_cubic_uniform_control.py'
x,y=s.symbols('x y')
orders=((2,1),(1,2))
low=((0,0),(1,0),(0,1),(2,0),(0,2),(1,1))
mons3=tuple((i,d-i) for d in range(4) for i in range(d,-1,-1))
mons5=tuple((i,d-i) for d in range(6) for i in range(d,-1,-1))

def load(name):
 sp=importlib.util.spec_from_file_location(name,BASE); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m

def at(expr,z): return expr.subs({x:z[2],y:z[3]},simultaneous=True)

def rref_integer(matrix):
 dm=DomainMatrix.from_Matrix(matrix)
 _,dm=dm.clear_denoms(convert=True)
 return dm.rref_den(method='FF')

def cubic_general(order):
 m=load(f'cubic_{order[0]}_{order[1]}')
 wvars=[]; wpoly=[]
 for axis in range(4):
  mat=s.zeros(4)
  for gi,G in enumerate(m.G):
   for ix,iy in mons3:
    c=s.symbols(f'w_{order[0]}_{order[1]}_{axis}_{gi}_{ix}_{iy}')
    wvars.append(c); mat+=c*x**ix*y**iy*G
  wpoly.append(mat)
 evars=[]; epoly=s.zeros(4)
 for i in range(4):
  for j in range(4):
   for ix,iy in mons3:
    c=s.symbols(f'e_{order[0]}_{order[1]}_{i}_{j}_{ix}_{iy}')
    evars.append(c); epoly[i,j]+=c*x**ix*y**iy
 variables=wvars+evars
 oldlink,oldframe=m.link,m.coframe; oldhigh=[dict(d) for d in m.CORR_HIGH]
 def link(site,axis,back=False):
  previous=m.CORR_HIGH; m.CORR_HIGH=[dict(d) for d in oldhigh]
  for direction in range(4): m.CORR_HIGH[direction][order]=at(wpoly[direction],site)
  try:return oldlink(site,axis,back)
  finally:m.CORR_HIGH=previous
 def frame(site): return oldframe(site)+m.Jet.co(*order,at(epoly,site))
 m.link,m.coframe=link,frame
 rows=m.link_rows((0,0,x,y))+m.solder_rows((0,0,x,y)); assert len(rows)==40
 for key in low:
  assert all(s.expand(row.coeff(*key))==0 for row in rows),(order,key)
 eqs=[]
 for row in rows:
  p=s.Poly(s.expand(row.coeff(*order)),x,y); assert p.total_degree()<=3
  eqs.extend(p.coeff_monomial(x**ix*y**iy) for ix,iy in mons3)
 A,b=s.linear_eq_to_matrix(eqs,variables); assert A.shape==(400,400)
 rr,den,pivots=rref_integer(A.row_join(b))
 assert len(pivots)==266 and 400 not in pivots,(order,len(pivots),pivots[-3:])
 R=rr.to_Matrix(); den=s.sympify(den); free=[c for c in range(400) if c not in pivots]
 assert len(free)==134
 params=s.symbols(f't_{order[0]}_{order[1]}_0:134')
 values=[s.Integer(0)]*400
 fdict=dict(zip(free,params))
 for c,t in fdict.items(): values[c]=t
 for row,pivot in enumerate(pivots):
  if pivot<400:
   values[pivot]=s.cancel(R[row,400]/den-sum((R[row,c]/den)*fdict[c] for c in free))
 sub=dict(zip(variables,values))
 result={'link':[p.subs(sub) for p in wpoly], 'frame':epoly.subs(sub), 'params':list(params), 'free_variables':[variables[c] for c in free]}
 print(f'cubic [{order[0]},{order[1]}]: exact rank 266, free modes 134',flush=True)
 return result

cubic={o:cubic_general(o) for o in orders}
params=[p for o in orders for p in cubic[o]['params']]
# Evaluate [a^2*b^2] source with the full affine cubic solution families.
m=load('quartic_all_order'); oldlink,oldframe=m.link,m.coframe; oldhigh=[dict(d) for d in m.CORR_HIGH]
def cubic_link(site,axis,back=False):
 previous=m.CORR_HIGH; m.CORR_HIGH=[dict(d) for d in oldhigh]
 for direction in range(4):
  for o in orders:m.CORR_HIGH[direction][o]=at(cubic[o]['link'][direction],site)
 try:return oldlink(site,axis,back)
 finally:m.CORR_HIGH=previous
def cubic_frame(site):
 e=oldframe(site)
 for o in orders:e+=m.Jet.co(*o,at(cubic[o]['frame'],site))
 return e
m.link,m.coframe=cubic_link,cubic_frame
source_rows=m.link_rows((0,0,x,y))+m.solder_rows((0,0,x,y))
source=[s.expand(r.coeff(2,2)) for r in source_rows]
assert len(source)==40
for expr in source:
 p=s.Poly(expr,x,y,*params)
 assert max((sum(mon[2:]) for mon in p.monoms()),default=0)<=1
print('quartic source assembled; affine in all 268 cubic free modes',flush=True)
# Add arbitrary degree-at-most-five quartic-order corrections to all 40 fields.
n=load('quartic_response')
wvars=[]; wpoly=[]
for axis in range(4):
 mat=s.zeros(4)
 for gi,G in enumerate(n.G):
  for ix,iy in mons5:
   c=s.symbols(f'W_{axis}_{gi}_{ix}_{iy}'); wvars.append(c); mat+=c*x**ix*y**iy*G
 wpoly.append(mat)
evars=[]; epoly=s.zeros(4)
for i in range(4):
 for j in range(4):
  for ix,iy in mons5:
   c=s.symbols(f'E_{i}_{j}_{ix}_{iy}'); evars.append(c); epoly[i,j]+=c*x**ix*y**iy
quartic_vars=wvars+evars

def response_link(site,axis,back=False):
 u=n.Jet(n.I)+n.Jet.co(2,2,at(wpoly[axis],site))
 return u.l_inv() if back else u
def response_frame(site): return n.Jet(n.I)+n.Jet.co(2,2,at(epoly,site))
n.link,n.coframe=response_link,response_frame
response_rows=n.link_rows((0,0,x,y))+n.solder_rows((0,0,x,y)); assert len(response_rows)==40
all_eqs=[]
for src,row in zip(source,response_rows):
 p=s.Poly(s.expand(src+row.coeff(2,2)),x,y); assert p.total_degree()<=5
 all_eqs.extend(p.coeff_monomial(x**ix*y**iy) for ix,iy in mons5)
allvars=quartic_vars+params
assert len(all_eqs)==840 and len(allvars)==1108
A,b=s.linear_eq_to_matrix(all_eqs,allvars)
print('joint system assembled: 840 equations, 1108 quartic/free-mode variables; reducing exactly',flush=True)
augmented= A.row_join(b)
rr,den,pivots=rref_integer(augmented)
augmented_rank=len(pivots)
rhs_is_pivot=(len(allvars) in pivots)
consistent=not rhs_is_pivot
coefficient_rank=augmented_rank if consistent else len(rref_integer(A)[2])
print(f'joint system ranks: coefficient {coefficient_rank}, augmented {augmented_rank}; RHS pivot={rhs_is_pivot}',flush=True)
if not consistent:
 raise AssertionError('quartic system became inconsistent after varying all cubic free modes')
assert coefficient_rank == augmented_rank == 582
R=rr.to_Matrix(); den=s.sympify(den); free=[c for c in range(len(allvars)) if c not in pivots]
values=[s.Integer(0)]*len(allvars)
for row,pivot in enumerate(pivots):
 if pivot<len(allvars): values[pivot]=s.cancel(R[row,len(allvars)]/den)
sub=dict(zip(allvars,values))
assert all(s.simplify(eq.subs(sub))==0 for eq in all_eqs)
nonzero_cubic_modes=sum(sub[p]!=0 for p in params)
nonzero_quartic_coefficients=sum(sub[v]!=0 for v in quartic_vars)
assert nonzero_cubic_modes == 2 and nonzero_quartic_coefficients == 166
print('joint system consistent; nonzero cubic free modes',nonzero_cubic_modes,'nonzero quartic correction coefficients',nonzero_quartic_coefficients,flush=True)
# Replay all checked coefficients through [a^2*b^2] on one combined exact state.
q_link=[poly.subs(sub) for poly in wpoly]
q_frame=epoly.subs(sub)
cubic_solved={o:{'link':[p.subs(sub) for p in cubic[o]['link']], 'frame':cubic[o]['frame'].subs(sub)} for o in orders}
replay=load('quartic_replay_all')
oldlink,oldframe=replay.link,replay.coframe; oldhigh=[dict(d) for d in replay.CORR_HIGH]
def final_link(site,axis,back=False):
 previous=replay.CORR_HIGH; replay.CORR_HIGH=[dict(d) for d in oldhigh]
 for direction in range(4):
  for o in orders: replay.CORR_HIGH[direction][o]=at(cubic_solved[o]['link'][direction],site)
  replay.CORR_HIGH[direction][(2,2)]=at(q_link[direction],site)
 try:return oldlink(site,axis,back)
 finally:replay.CORR_HIGH=previous
def final_frame(site):
 e=oldframe(site)
 for o in orders:e+=replay.Jet.co(*o,at(cubic_solved[o]['frame'],site))
 e+=replay.Jet.co(2,2,at(q_frame,site))
 return e
replay.link,replay.coframe=final_link,final_frame
rows=replay.link_rows((0,0,x,y))+replay.solder_rows((0,0,x,y)); assert len(rows)==40
for order in low+orders+((2,2),):
 for i,row in enumerate(rows):
  assert s.expand(row.coeff(*order))==0,(order,i,s.factor(row.coeff(*order)))
print('PASS: all 40 original Euler rows vanish identically through [a^2*b^2] for an exact cubic representative and degree<=5 quartic corrections',flush=True)
print('selected cubic free modes (actual correction coefficients):')
for order in orders:
 for index,parameter in enumerate(cubic[order]['params']):
  if sub[parameter]!=0:
   print(cubic[order]['free_variables'][index],'=',s.factor(sub[parameter]),flush=True)
for v in quartic_vars:
 if sub[v]!=0: print(v,'=',s.factor(sub[v]),flush=True)
