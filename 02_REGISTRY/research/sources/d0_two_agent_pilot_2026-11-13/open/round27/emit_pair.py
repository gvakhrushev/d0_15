#!/usr/bin/env python3
"""Emit fixed-address logical gate list as JSON on stdout; no native claim."""
import argparse,json
import controlled_involution as ci
p=argparse.ArgumentParser();sub=p.add_subparsers(dest='kind',required=True)
c=sub.add_parser('choi');c.add_argument('address',type=int);c.add_argument('input',type=int);c.add_argument('output',type=int)
c=sub.add_parser('car');c.add_argument('site',type=int);c.add_argument('grade',type=int,choices=(0,15))
z=p.parse_args()
if z.kind=='choi':n=22;a=0;b=ci.choi_label(z.address,z.input,z.output)
else:n=12;a=ci.car_label(z.site,1);b=ci.car_label(z.site,z.grade)
result=ci.serial(ci.compile_pair(n,a,b));result['inverse_is_reversed_gate_list']=True;result['basis']='logical X/CX/CCX/Z/CZ';result['native_compiled']=False
print(json.dumps(result,indent=2))
