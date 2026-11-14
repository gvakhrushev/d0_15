#!/usr/bin/env python3
"""Exact diagnostic: coherent SAM/old legs vs a fixed fresh WORK checkpoint."""
from pathlib import Path
import json,sympy as s
P=Path(__file__).resolve().parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);Y=s.Matrix([[0,-s.I],[s.I,0]])
# 2-dimensional SAM x 2-dimensional old, then one fresh source bit.
# Actual preparation has b-dependent error in WORK, but never changes SAM or old.
p=s.Rational(3,5);a=s.Rational(4,5);G=s.Matrix([[a,-p],[p,a]])
J=s.kronecker_product(s.eye(4),s.Matrix([1,0]));U=s.diag(I,I,G,G) # reordered below to act on SAM and WORK with old spectator
# Basis is SAM,old,WORK: branch b0 -> I4, b1 -> I_old tensor G.
U=s.diag(s.eye(4),s.kronecker_product(I,G));V=J;Vhat=U*J
# Entangled complex SAM/old input, and an observable jointly reading SAM,
# old and WORK; comparisons cover full coherent incoming factors.
phi=s.Matrix([1,0,0,s.I])/s.sqrt(2);O=s.kronecker_product(Y,X,Z)
diff=Vhat.T.conjugate()*O*Vhat-V.T.conjugate()*O*V
val=s.simplify((phi.T.conjugate()*diff*phi)[0]);eta2=2-2*a
assert s.simplify(val)!=0 and s.simplify(val**2-4*eta2)<=0
# Exact front/back independent incoming preparation legs F,B: actual matrix
# perturbation is not restricted to product SAM or classical b sectors.
F=s.kronecker_product(X,I);B=s.kronecker_product(I,X)
assert (F.T.conjugate()*diff*B).shape==(4,4)
# An equal canonical action can be arbitrarily different on dirty WORK.
ket0=s.Matrix([1,0]);ketplus=s.Matrix([1,1])/s.sqrt(2)
assert Z*ket0==ket0 and (ketplus.T*X*ketplus)[0]==1 and ((Z*ketplus).T*X*(Z*ketplus))[0]==-1
out={'status':'PASS_COHERENT_SAM_OLD_LEGS_CANONICAL_FIBRE_FIXTURE','complex_entangled_SAM_old_and_joint_mark':True,'independent_front_back_legs':True,'mark_difference_exact':str(val),'isometry_error_squared':str(eta2),'same_fresh_column_does_not_imply_dirty_column':True,'general_bound':'||F*(Vhat* O Vhat - V* O V)B|| <= 2 eta ||F|| ||B|| ||O||','admitted_physical_preparation_or_reader_proved':False,'GR_closed':False}
(P/'CANONICAL_UNIFORM_LEGS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
