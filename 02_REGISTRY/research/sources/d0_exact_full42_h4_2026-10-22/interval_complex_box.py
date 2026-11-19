"""Interval bound of holomorphic 42D source on a complex polydisc."""
import json, time
from pathlib import Path
from mpmath import mp,iv
import interval_point as interval
import mp_euler as own
ROOT=Path(__file__).resolve().parent

def run(R='0.0000001',digits=60):
 iv.dps=digits
 inp=json.loads((ROOT/'mp_center.json').read_text())
 z=[];R=iv.mpf(R)
 for s in inp['center']:
  z.append(iv.mpc([iv.mpf(s)-R,iv.mpf(s)+R],[-R,R]))
 start=time.perf_counter()
 h,b=own.build()
 print('built at',round(time.perf_counter()-start,3))
 source=own.eval_euler(z,h,b)
 M=mp.mpf(0)
 for v in source:
  for x in [v.real.a,v.real.b,v.imag.a,v.imag.b]:
   M=max(M,abs(mp.mpf(x)))
 print('interval complex box enclosure of all F_i, M=',mp.nstr(M,24),'seconds',round(time.perf_counter()-start,3))
 for j in (0,16,40):print(j,source[j])
 return M
if __name__=='__main__':run()
