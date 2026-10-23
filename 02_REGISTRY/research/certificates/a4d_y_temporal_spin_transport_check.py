#!/usr/bin/env python3
"""Reduced exact replay for the temporal SO(3)-spin product rigidity result.

The literal Euler elimination that produced the pinned formulas is recorded in
A4D_Y_TEMPORAL_SPIN_PRODUCT_RIGIDITY.md.  This small certificate checks the
decisive exact algebra and exceptional transport rank without numerical input.
"""
import json
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
RESULT=HERE/"a4d_y_temporal_spin_transport_results.json"

def ck(name,cond):
    if not cond: raise AssertionError(name)
    print("PASS_"+name)

a,b,c,d=sp.symbols("a b c d", real=True)
f0,f1,f2,f3=sp.symbols("f0 f1 f2 f3", real=True)
core=3*d**4*(a-b+c+3)**2+4*(a-b+c-4)**2
ck("CORE_IS_SUM_OF_SQUARES", sp.expand(core-3*d**4*(a-b+c+3)**2-4*(a-b+c-4)**2)==0)
# Over the reals core=0 implies both squares vanish.  The second gives
# a-b+c=4; substituting in the first leaves 147*d^4.
ck("EXCEPTION_REDUCES_TO_D_ZERO", sp.factor(core.subs(c,4-a+b))==147*d**4)

rows=sp.Matrix([
 [3,0,-2,-1],[3,0,-1,-2],[0,0,1,-1],
 [-3,2,0,1],[0,1,0,-1],[3,-1,0,-2],
 [0,1,-1,0],[-3,2,1,0],[-3,1,2,0]
])/3
ck("EXCEPTIONAL_TRANSPORT_RANK3", rows.rank()==3)
N=rows.nullspace()
ck("EXCEPTIONAL_KERNEL_CONSTANT", len(N)==1 and N[0]==sp.Matrix([1,1,1,1]))

data=json.loads(RESULT.read_text())
ck("PINNED_CORE", data["boost_row_elimination_core"]=="3*d^4*(a-b+c+3)^2 + 4*(a-b+c-4)^2")
ck("PINNED_EXCEPTION", data["real_exceptional_locus"]=="d=0 and a-b+c=4")
ck("PINNED_RANK", data["exceptional_transport_rank"]==3)
print("TERMINAL A4D-Y-TEMPORAL-SO3-SPIN-PRODUCT-RIGIDITY")
print("SCOPE temporal SO(3) Cayley correction; spatial transverse links remain open")
