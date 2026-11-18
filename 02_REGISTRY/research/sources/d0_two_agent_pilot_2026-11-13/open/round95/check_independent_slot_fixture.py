#!/usr/bin/env python3
"""Exact fixture: [Q,S]=0 does not force separate Q-source rows to zero."""
from pathlib import Path
import sympy as sp,json
P=Path(__file__).resolve().parent
I=sp.eye(2);Z=sp.diag(1,-1);R=sp.Matrix([[12,-5],[5,12]])/13
B=sp.diag(1,1,1,1);B[2:4,2:4]=R
S=sp.kronecker_product(I,Z);J=sp.Matrix([[0,-1],[1,0]]);X=sp.kronecker_product(J,I)
assert X*S==S*X and X*B!=B*X
chi=sp.Matrix([sp.Rational(3,5),sp.Rational(4,5)]);work=sp.Matrix([1,0]);psi=sp.kronecker_product(chi,work)
M=sp.diag(1,sp.Rational(119,169));v=M*chi;r=sp.sqrt((v.T*v)[0]);u=v/r
# Proper rotation whose first relevant row satisfies chi^T U = u^T.
def rotcol(a):return sp.Matrix([[a[0],-a[1]],[a[1],a[0]]])
post=rotcol(chi)*rotcol(u).T;V=sp.kronecker_product(post,I);assert sp.simplify(chi.T*post-u.T)==sp.zeros(1,2)
cb=sp.simplify((psi.T*V*B.T*X*S*B*psi)[0]);cf=sp.simplify(-(psi.T*V*B.T*S*X*B*psi)[0]);assert sp.simplify(cb+cf)==0 and cb!=0
# An ideal scalar return matrix in the same basis does give each row zero.
assert (chi.T*J*chi)[0]==0
out={'status':'PASS_INDEPENDENT_Q_SLOTS_COUNTEREXAMPLE','SAM_commutes_with_middle':True,'SAM_does_not_commute_with_writer':True,'fixed_nonidentity_post':True,'Qb_source_nonzero':True,'Qf_source_nonzero':True,'independent_analytic_rows_are_opposite':True,'exact_scalar_centre_Q_row_zero':True,'actual_A48_nonzero_or_sign_proved':False,'full_heat_or_marked_price_identified':False,'GR_closed':False}
(P/'FOUR_SLOT_FIXTURE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
