"""Split rigorously interval-checked complex-step derivative into short batches.
Each returned 42-vector is an enclosure of partial derivative plus a Cauchy remainder.
"""
import json, argparse,time
from pathlib import Path
from mpmath import mp,iv
import certified_newton as c
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--start',type=int,required=True);parser.add_argument('--count',type=int,default=7)
a=parser.parse_args();assert 0<=a.start<42
R=mp.mpf('1e-7');t=iv.mpf('1e-20');M=mp.mpf('0.001')
rem=M*mp.mpf('1e-40')/mp.mpf('1e-21')/(1-mp.mpf('1e-26'))
assert rem<mp.mpf('2e-22')
d=json.loads((HERE/'mp_center.json').read_text());center=[iv.mpf(x) for x in d['center']]
h,base=c.own.build();out=[];maxerr=mp.mpf(0);st=time.time()
for j in range(a.start,min(a.start+a.count,42)):
 z=[iv.mpc(x) for x in center];z[j]+=iv.mpc(0,t)
 source=c.own.eval_euler(z,h,base)
 vals=[]
 for x in source:
  v=x.imag/t
  mid=(mp.mpf(v.a)+mp.mpf(v.b))/2
  s=mp.nstr(mid,45)
  maxerr=max(maxerr,c.abs_upper(v-iv.mpf(s)))
  vals.append(s)
 out.append({'column':j,'source_derivative_vector':vals})
print('columns',a.start,'to',a.start+len(out)-1,'time',round(time.time()-st,2),'interval_err_max',mp.nstr(maxerr,12),flush=True)
assert maxerr+rem <mp.mpf('3e-22')
(HERE/f'jac_columns_{a.start:02}.json').write_text(json.dumps({'method':'mpmath.iv complex-step at exact rational root center; Cauchy coeff remainder separately proven','step':'1e-20','complex_disk_R':'1e-7','sup_M':'1e-3','max_rounded_interval_error':mp.nstr(maxerr,50),'derivative_absolute_error_limit':'3e-22','columns':out},indent=2)+'\n')
