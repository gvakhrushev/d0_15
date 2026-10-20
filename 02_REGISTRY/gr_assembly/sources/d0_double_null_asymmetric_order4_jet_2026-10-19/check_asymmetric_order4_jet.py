import contextlib, io, runpy, importlib.util
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'02_REGISTRY/gr_assembly/sources/d0_double_null_quartic_free_mode_jet_2026-10-19/check_quartic_free_mode_jet.py'
print('replaying registered mixed-quartic certificate before extending the amplitude ring',flush=True)
with contextlib.redirect_stdout(io.StringIO()): state=runpy.run_path(str(SOURCE))
print('base mixed-quartic replay passed; extending MAX to 3',flush=True)
replay=state['replay']; replay.MAX=3
x,y=state['x'],state['y']; orders=state['orders']; cubic_solved=state['cubic_solved']
q_link=state['q_link']; q_frame=state['q_frame']; oldlink=state['oldlink']; oldframe=state['oldframe']
base_high=[dict(d) for d in state['oldhigh']]
new_orders=((3,0),(0,3),(3,1),(1,3))
for direction in range(4):
 for order in new_orders: base_high[direction][order]=replay.O
new_corrections={}

def at(expr,z): return expr.subs({x:z[2],y:z[3]},simultaneous=True)

def state_link(z,axis,back=False):
 previous=replay.CORR_HIGH; replay.CORR_HIGH=[dict(d) for d in base_high]
 for direction in range(4):
  for order in orders: replay.CORR_HIGH[direction][order]=at(cubic_solved[order]['link'][direction],z)
  replay.CORR_HIGH[direction][(2,2)]=at(q_link[direction],z)
  for order,corr in new_corrections.items(): replay.CORR_HIGH[direction][order]=at(corr['link'][direction],z)
 try:return oldlink(z,axis,back)
 finally:replay.CORR_HIGH=previous

def state_frame(z):
 e=oldframe(z)
 for order in orders: e+=replay.Jet.co(*order,at(cubic_solved[order]['frame'],z))
 e+=replay.Jet.co(2,2,at(q_frame,z))
 for order,corr in new_corrections.items(): e+=replay.Jet.co(*order,at(corr['frame'],z))
 return e
replay.link,replay.coframe=state_link,state_frame


def load_response(name):
 base=ROOT/'02_REGISTRY/gr_assembly/sources/d0_double_null_cubic_uniform_control_2026-10-19/check_cubic_uniform_control.py'
 spec=importlib.util.spec_from_file_location(name,base); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); mod.MAX=3; return mod

def solve_order(order,degree):
 source_rows=replay.link_rows((0,0,x,y))+replay.solder_rows((0,0,x,y)); assert len(source_rows)==40
 source=[s.expand(row.coeff(*order)) for row in source_rows]
 source_degree=max((s.Poly(r,x,y).total_degree() for r in source if r!=0),default=0)
 print(f'[{order[0]},{order[1]}] source: max spatial degree {source_degree}',flush=True)
 if all(r==0 for r in source):
  result={'link':[s.zeros(4) for _ in range(4)],'frame':s.zeros(4)}
  print(f'[{order[0]},{order[1]}] source is identically zero; zero correction selected',flush=True)
  return result
 assert source_degree<=degree,(order,source_degree,degree)
 monomials=tuple((i,d-i) for d in range(degree+1) for i in range(d,-1,-1))
 response=load_response(f'response_{order[0]}_{order[1]}')
 link_vars=[]; link_polys=[]
 for axis in range(4):
  mat=s.zeros(4)
  for gi,G in enumerate(response.G):
   for ix,iy in monomials:
    c=s.symbols(f'w_{order[0]}_{order[1]}_{axis}_{gi}_{ix}_{iy}')
    link_vars.append(c); mat+=c*x**ix*y**iy*G
  link_polys.append(mat)
 frame_vars=[]; frame_poly=s.zeros(4)
 for i in range(4):
  for j in range(4):
   for ix,iy in monomials:
    c=s.symbols(f'e_{order[0]}_{order[1]}_{i}_{j}_{ix}_{iy}')
    frame_vars.append(c); frame_poly[i,j]+=c*x**ix*y**iy
 variables=link_vars+frame_vars
 def response_link(z,axis,back=False):
  u=response.Jet(response.I)+response.Jet.co(*order,at(link_polys[axis],z))
  return u.l_inv() if back else u
 def response_frame(z): return response.Jet(response.I)+response.Jet.co(*order,at(frame_poly,z))
 response.link,response.coframe=response_link,response_frame
 response_rows=response.link_rows((0,0,x,y))+response.solder_rows((0,0,x,y)); assert len(response_rows)==40
 equations=[]
 for src,row in zip(source,response_rows):
  p=s.Poly(s.expand(src+row.coeff(*order)),x,y); assert p.total_degree()<=degree,(order,p.total_degree())
  equations.extend(p.coeff_monomial(x**ix*y**iy) for ix,iy in monomials)
 assert len(variables)==len(equations)==40*len(monomials)
 A,b=s.linear_eq_to_matrix(equations,variables)
 dm=DomainMatrix.from_Matrix(A.row_join(b)); _,dm=dm.clear_denoms(convert=True)
 rr,den,pivots=dm.rref_den(method='FF'); aug_rank=len(pivots); rhs_pivot=len(variables) in pivots
 if rhs_pivot:
  coeff=DomainMatrix.from_Matrix(A); _,coeff=coeff.clear_denoms(convert=True)
  coeff_rank=len(coeff.rref_den(method='FF')[2])
  print(f'[{order[0]},{order[1]}] inconsistent: coefficient rank {coeff_rank}, augmented rank {aug_rank}',flush=True)
  raise AssertionError(f'no degree-{degree} correction exists for {order}')
 print(f'[{order[0]},{order[1]}] consistent: exact rank {aug_rank}, rhs non-pivot, variables {len(variables)}',flush=True)
 R=rr.to_Matrix(); den=s.sympify(den); free=[j for j in range(len(variables)) if j not in pivots]
 solution=[s.Integer(0)]*len(variables)
 for row,pivot in enumerate(pivots):
  if pivot<len(variables): solution[pivot]=s.cancel(R[row,len(variables)]/den)
 substitution=dict(zip(variables,solution))
 assert all(s.simplify(eq.subs(substitution))==0 for eq in equations)
 result={'link':[mat.subs(substitution) for mat in link_polys], 'frame':frame_poly.subs(substitution)}
 print(f'[{order[0]},{order[1]}] selected correction: {sum(v!=0 for v in solution)} nonzero coefficients, {len(free)} free coefficients set to zero',flush=True)
 return result

# Pure cubic coefficients, then the asymmetric mixed quartic coefficients.
for order in new_orders:
 degree=3 if order in ((3,0),(0,3)) else 5
 new_corrections[order]=solve_order(order,degree)
# Combined exact replay on every checked coefficient in the expanded rectangle.
rows=replay.link_rows((0,0,x,y))+replay.solder_rows((0,0,x,y)); assert len(rows)==40
check_orders=state['low']+orders+((2,2),)+new_orders
for order in check_orders:
 for i,row in enumerate(rows):
  assert s.expand(row.coeff(*order))==0,(order,i,s.factor(row.coeff(*order)))
print('PASS: all 40 original Euler rows vanish identically for the retained coefficients through [a^3*b] and [a*b^3], including [a^2*b^2].',flush=True)
for order,corr in new_corrections.items():
 print(f'[{order[0]},{order[1]}] nonzero field coefficients: {sum(v!=0 for mat in corr["link"] for v in mat)+sum(v!=0 for v in corr["frame"])}',flush=True)
