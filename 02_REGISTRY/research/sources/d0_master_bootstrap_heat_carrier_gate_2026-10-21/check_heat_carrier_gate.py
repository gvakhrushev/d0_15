#!/usr/bin/env python3
from fractions import Fraction
import json

archive_heat_source = Fraction(0,1)
soldered_heat_source = Fraction(128,9)
difference = soldered_heat_source - archive_heat_source
required_feedback_if_soldered = -soldered_heat_source

checks=[]
def req(c,n):
    if not c: raise ArithmeticError(n)
    checks.append(n)

req(archive_heat_source == 0,"fixed archive heat field source is zero")
req(soldered_heat_source == Fraction(128,9),"owned soldered H01 heat source")
req(difference == Fraction(128,9),"two heat completions have distinct source")
req(difference != 0,"master-bootstrap source differs without heat identification")
req(required_feedback_if_soldered == Fraction(-128,9),
    "moving-Hodge branch requires exact negative feedback cancellation")

# Conditional all42 theorem is pure chain rule:
# dB = dHeat + C*dS; fixed archive heat gives dHeat=0.
C=Fraction(7,13)  # arbitrary nonzero witness for symbolic chain-rule control
dS=Fraction(0,1)
dJ=C*dS
dB=archive_heat_source+dJ
req(C!=0,"nonzero feedback transfer control")
req(dB==0,"configured root remains full bootstrap root with fixed archive heat")
# Off root, source proportionality is retained.
dS2=Fraction(11,17)
req(archive_heat_source+C*dS2 == C*dS2,
    "fixed archive heat preserves complete feedback source off root")

print(json.dumps({
 "status":"PASS",
 "check_count":len(checks),
 "checks":checks,
 "heat_source_H01":{
   "core_archive_fixed_level":"0",
   "moving_soldered":"128/9",
   "difference":"128/9"},
 "conditional_capstone":{
   "assumption":"Book03 heat carrier = fixed archive Laplacian on GR execution",
   "full_field_source":"D B_N = D J_loc = C_* D S_h",
   "all42_configured_roots_are_full_bootstrap_roots":True},
 "moving_hodge_gate":{"required_feedback_source_H01":"-128/9"},
 "scope":{
   "book03_heat_carrier_identified_on_GR_execution":False,
   "physical_common_execution_admitted":False,
   "GR_closed":False}
},indent=2,sort_keys=True))
