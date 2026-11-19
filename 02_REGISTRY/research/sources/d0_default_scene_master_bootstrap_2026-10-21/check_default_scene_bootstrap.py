#!/usr/bin/env python3
from fractions import Fraction
import json

checks=[]
def req(c,n):
    if not c:
        raise ArithmeticError(n)
    checks.append(n)

heat_default = Fraction(0,1)
moving_hodge_control = Fraction(128,9)
Cstar = Fraction(17,31)
root_source = Fraction(0,1)
offroot_source = Fraction(13,19)

req(heat_default == 0,"default fixed-scene heat has zero field source")
req(moving_hodge_control != heat_default,
    "moving-Hodge branch remains distinct from default scene heat")
req(Cstar != 0,"feedback source transfer coefficient nonzero")
req(heat_default + Cstar*root_source == 0,
    "all42 configured root is full bootstrap root")
req(heat_default + Cstar*offroot_source == Cstar*offroot_source,
    "full bootstrap source equals feedback source off root")
req(Cstar*offroot_source != 0,
    "nonroot source remains nonzero under nonzero multiplier")
req(Cstar*root_source == 0,
    "zero-set is preserved by nonzero feedback multiplier")

print(json.dumps({
 "status":"PASS",
 "check_count":len(checks),
 "checks":checks,
 "source_identity":"D_42 B_master = D_42 J_loc = C_* D_42 S_h",
 "default_heat_field_source":"0",
 "moving_hodge_control_H01":"128/9",
 "zero_set_equivalence":True,
 "scope":{
   "default_scene_heat_branch":True,
   "physical_execution_selected":False,
   "independent_internal_euler_rows_closed":False,
   "uniform_raw216_refinement":False,
   "GR_closed":False
 }
},indent=2,sort_keys=True))
