"""Interval-arithmetic inclusion of the 42-component source at a rational center."""
import json,mpmath
from pathlib import Path
from mpmath import mp,iv
import mp_euler as own

iv.dps=100
own.mp=iv
own.I=iv.eye(4)
own.ETA=iv.diag([1,-1,-1,-1])
own.G2=[own.ETA[a,a]*own.ETA[b,b] for a,b in own.PAIRS]
own.STAR=iv.matrix(6)
for a,(b,s) in own.STARMAP.items(): own.STAR[own.PAIRS.index(b),own.PAIRS.index(a)]=s
own.L=[]
for i in (1,2,3):
 X=iv.matrix(4); X[0,i]=X[i,0]=1;own.L.append(X)
for i,j in ((1,2),(1,3),(2,3)):
 X=iv.matrix(4);X[i,j]=1;X[j,i]=-1;own.L.append(X)
own.P=(iv.sqrt(5)-1)/2
own.Z=iv.mpf(1)/2**20
own.LP=iv.log(1/own.P)

def upper(a):
 # iv interval -> upper endpoint enclosing abs(a) at exact working precision
 return max(abs(mp.mpf(a.a)),abs(mp.mpf(a.b)))

def run():
 inp=json.loads((Path(__file__).resolve().parent/'mp_center.json').read_text())
 center=[iv.mpf(x) for x in inp['center']]
 from time import perf_counter
 start=perf_counter()
 h,b=own.build()
 src=own.eval_euler(center,h,b)
 print('seconds',perf_counter()-start)
 bounds=[upper(x) for x in src]
 biggest=max(bounds)
 print('max rigorous point source enclosure',mp.nstr(biggest,30))
 print('first',src[0])
 return biggest
if __name__=='__main__':run()
