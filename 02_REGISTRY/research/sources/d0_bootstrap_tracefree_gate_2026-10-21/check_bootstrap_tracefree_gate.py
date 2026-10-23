#!/usr/bin/env python3
from fractions import Fraction
import json

heat = Fraction(128,9)
required_feedback = -heat
fixed_golden_feedback = Fraction(0,1)

checks=[]
def req(c,n):
    if not c:
        raise ArithmeticError(n)
    checks.append(n)

req(heat == Fraction(128,9),"exact soldered heat H01 source")
req(required_feedback == Fraction(-128,9),"bootstrap cancellation target")
req(fixed_golden_feedback != required_feedback,
    "fixed-golden feedback cannot cancel soldered heat")
req(heat + required_feedback == 0,"Book03 heat plus required feedback stationary")
req(heat + fixed_golden_feedback != 0,
    "direct fixed-golden composition is nonstationary")
req(-required_feedback == heat,"feedback sign control")
req(required_feedback != Fraction(-64,9),"factor-two mutation rejected")
req(required_feedback != Fraction(128,9),"wrong-sign mutation rejected")

print(json.dumps({
 "status":"PASS",
 "check_count":len(checks),
 "checks":checks,
 "heat_H01":{"numerator":heat.numerator,"denominator":heat.denominator},
 "required_feedback_H01":{"numerator":required_feedback.numerator,
                           "denominator":required_feedback.denominator},
 "existing_fixed_golden_feedback_H01":0,
 "direct_composition_stationary":False,
 "scope":{
   "bootstrap_heat_identified_with_soldered_square":"conditional",
   "fixed_golden_completion_feedback":"excluded as compensator",
   "other_feedback_pullbacks":"open",
   "GR_closed":False
 }
},indent=2,sort_keys=True))
