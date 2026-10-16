#!/usr/bin/env python3
"""General homogeneous critical leading solder: exact range classification.

For germs A=A0+eps*v+..., Theta=eps*T+..., with T nondegenerate and
H0*T=0, the solder order-two range condition forces both residual-active
amplitudes to be opposite and all mixed active role directions to vanish.
Their survival requires the lower critical 2x2 block to be conformal.
Seven of the eight minimum supports are thus killed at link order two.
The remaining support is NOT retired: its conformal critical-solder locus
survives this gate. No finite-amplitude or sitewise-solder no-go is asserted.
"""
from __future__ import annotations
import contextlib,importlib.util,io
from pathlib import Path
import sympy as sp

def check(name,c):
 if not c:raise AssertionError(name)
 print('PASS_'+name,flush=True)
here=Path(__file__).resolve().parent
p=here/'a4d_resolved_curved_stationary_e2_support7_joint_linear_gate_check.py'
s=importlib.util.spec_from_file_location('critical_owner',p);f=importlib.util.module_from_spec(s)
with contextlib.redirect_stdout(io.StringIO()):s.loader.exec_module(f)
o=f.owner;H0=f.hessian;L=sp.Matrix.vstack(*[v.T for v in H0.nullspace()]);T=f.theta;z=f.z_names
A=z[0]-z[2];B=z[1]-z[2];C=f.complement
check('NONDEGENERACY_EXACT_THREE_FACTOR_WALL',sp.expand(T.det()-A*B*C)==0)

def hessian(response):
 H=sp.zeros(16)
 for face,rr in response.items():
  u,v=[i for i in range(4)if i not in face]
  for a in range(4):
   for b in range(4):
    val=16*o.orientation(face)*(o.wedge(sp.eye(4)[:,a],sp.eye(4)[:,b]).T*rr)[0]
    H[4*a+u,4*b+v]+=val;H[4*b+v,4*a+u]+=val
 return H
specs=[(f'{name}_{r}',r,g)for name,g in o.COMPLEMENT for r in range(4)]
names=[a for a,_,_ in specs];HS=[hessian(f.curvature_responses(r,g))for _,r,g in specs]
P=sp.Matrix.hstack(*[L*Hi*sp.Matrix(list(T))for Hi in HS])/16
selected=[names.index(name)for name in o.SELECTED_NAMES]
check('GENERAL_TENSOR_SPECIALIZES_TO_OWNED_ETA_MIXED_PARTIALS',
 P[:,selected].subs(f.eta_coordinates)==L*f.j_solder/16)
# Only differences of the role-0/1 generators occur; the three common
# directions and K1@roles2,3 are free blind moduli at this range gate.
dk,d2,d3,alpha,u,w,gamma=sp.symbols('dk d2 d3 alpha u w gamma')
v=sp.Matrix([dk,0,0,0,d2,0,alpha,u,d3,0,w,gamma])
r=(P*v).applyfunc(sp.expand)
block=sp.Matrix([[sp.diff(r[row],d)for d in (d2,d3)]for row in (5,7)])
check('TWO_BY_TWO_DIFFERENCE_MINOR_IS_TWO_C',sp.expand(block.det()-2*C)==0)
check('DIFFERENCE_ROWS_HAVE_NO_OTHER_VARIABLES',(sp.Matrix([r[5],r[7]])-block*sp.Matrix([d2,d3])).applyfunc(sp.expand)==sp.zeros(2,1))
# det T !=0 implies A,B,C !=0; hence d2=d3=0.
r=[sp.expand(e.subs({d2:0,d3:0}))for e in r]
check('ACTIVE_OPPOSITION_RANGE_IDENTITY',sp.expand(r[8]-(r[6]-r[9])-4*B*(alpha+gamma))==0)
check('K1_DIFFERENCE_RANGE_IDENTITY',sp.expand(r[8]-A*dk-4*B*gamma)==0)
check('MIXED_ROLE_DIFFERENCE_RANGE_IDENTITY',sp.expand(r[9]-2*B*(alpha+u-w+gamma))==0)
# alpha=-gamma, dk=-4 B gamma/A, u=w. The remaining two rows imply
# (z6+z8)*gamma=0, then u=w=0, with no real-root or rank sampling.
r0=sp.cancel(r[0].subs({alpha:-gamma,dk:-4*B*gamma/A,w:u}))
r1=sp.cancel(r[1].subs({alpha:-gamma,dk:-4*B*gamma/A,w:u}))
check('CONFORMAL_LOWER_BLOCK_RANGE_IDENTITY',sp.cancel(r1-A*r0/B-8*(z[6]+z[8])*gamma)==0)
check('MIXED_ROLE_RANGE_IDENTITY',sp.cancel(r0+4*B*(z[6]+z[8])*gamma/A-4*B*u)==0)
sol=sp.Matrix([-4*B*gamma/A,0,0,0,0,0,-gamma,0,0,0,0,gamma])
check('SURVIVING_ACTIVE_KERNEL_SUFFICIENT_ON_CONFORMAL_LOCUS',
 (P*sol).subs(z[8],-z[6]).applyfunc(sp.cancel)==sp.zeros(10,1))
check('CONFORMAL_LOCUS_SOLDER_DETERMINANT',
 sp.expand(T.det().subs(z[8],-z[6])+A*B*(z[6]**2+z[9]**2))==0)
check('INACTIVE_LINK_SOURCE_SUM_EXACT_NONZERO_WALL',
 sp.expand(f.euler_polynomials[17]+f.euler_polynomials[22]-64*A*B)==0)
# Both tests N3@role2 and N2@role3 have first residual zero (owned
# all-support channel gate). If R1(v)=0 their channel EL2 vanishes, even
# with arbitrary second amplitudes and translations. Their source sum
# 64 A B cannot vanish for nondegenerate T.
for role,gen in ((2,o.N3),(3,o.N2)):
 aa=[o.MJet(base,gen if i==role else sp.zeros(4))for i,base in enumerate(o.generators0)]
 uu=[o.cayley_jet(a)for a in aa]
 for r0,s0 in o.PAIRS:
  pp=uu[r0]*uu[s0]*uu[r0].inv()*uu[s0].inv()
  mm=o.constant_jet(o.I4)-pp
  check(f'INACTIVE_TEST_{role}_{r0}_{s0}_FIRST_DET_ADJ_ZERO',
        o.det_direction(mm.v,mm.d)==0 and o.adj_direction(mm.v,mm.d)==sp.zeros(4))
for index,support in enumerate(o.MINIMUM_SUPPORTS):
 if index!=5:
  check(f'SUPPORT_{index}_LACKS_ONE_OF_REQUIRED_ACTIVE_PAIR',
        'N2_2' not in support or 'N3_3' not in support)
print('EXACT_RESULT: seven supports blocked for every nondegenerate homogeneous critical leading solder. Support 5 can survive only z8=-z6, with tangent (-4*(B/A)*gamma, q1, -gamma, q2, q2, 0, gamma).',flush=True)
print('SCOPE: necessary germ range/link equations; surviving support-5 conformal locus, finite amplitudes, and sitewise solder remain open',flush=True)
