#!/usr/bin/env python3
"""Exact algebraic scalar-completion positive and negative controls.

Consumes check_source_image.py from this same directory; does NOT certify
physical admission of an additional scalar row in the native D0 action.
"""
import json
from sympy import Matrix, ones, sqrt, simplify
from check_source_image import metric_tangents, symcovector_matrix, bianchi_matrix, Q, check

native = Matrix([symcovector_matrix(x) for x in metric_tangents({0,1,2,3})])
conformal = Matrix([symcovector_matrix(Q)])

k_regular = ones(4, 1)
B_regular = bianchi_matrix(k_regular)
check(native.rank()==5, 'raw native rank')
check(native.col_join(B_regular).rank()==9, 'Bianchi expected codimension one')
check(native.col_join(B_regular).col_join(conformal).rank()==10,
      'conformal row should separate rational fixture residual source')

# Exceptional real full-support momentum: ALL four covector components nonzero.
# Its algebraic value solves 4 t^2-43t-136=0, and makes the one
# Bianchi-compatible invisible Einstein source trace-free.
t=(43+5*sqrt(161))/8
check(simplify(4*t*t-43*t-136)==0, 'exceptional algebraic momentum identity')
k_exception=Matrix([t,1,1,1])
check(all(x!=0 for x in k_exception), 'not a full-support momentum')
B_exception=bianchi_matrix(k_exception)
check(native.col_join(B_exception).rank()==9, 'anomalous Bianchi null dimension')
check(native.col_join(B_exception).col_join(conformal).rank()==9,
      'trace must FAIL to close exceptional source')
residual=native.col_join(B_exception).nullspace()
check(len(residual)==1 and simplify((conformal*residual[0])[0])==0,
      'exceptional source should be conformally invisible')

print(json.dumps({
    'status':'PASS', 'exact':'Q(sqrt161)',
    'native_rank':5,'bianchi_rank':9,
    'regular_conformal_completed_rank':10,
    'exceptional_k0':str(t),
    'exceptional_conformal_completed_rank':9,
    'physical_source_admission':'NOT PROVED',
},sort_keys=True,separators=(',',':')))
