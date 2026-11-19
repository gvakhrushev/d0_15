#!/usr/bin/env python3
"""Independent complex-step differentiation of the original COMPLETE cap N=1
Golden CQ report price, against every one of the 42 native Euler rows.
Uses identical real geometry and same rational collar but reconstructs SCALAR
from six based faces and original nonlinear r(x,y), not the Euler recursion.
"""
import json,time
from pathlib import Path
from mpmath import mp
import mp_euler as own
HERE=Path(__file__).resolve().parent
mp.dps=70
h,base=own.build()
P=own.P;Z=own.Z;ell=own.LP;tau=mp.mpf('.05')

def report(f,q):
 x=-tau*f;y=tau*q
 E=P*P*(1+x);t=4*E*(1-E);b=P-P*P*y;B=4*b*b*(1-b*b)
 A=t+(1-t)*B
 return Z*(A+B)-Z*Z*A*B

def entropy(r):return -(r*mp.log(r)+(1-r)*mp.log(1-r))/ell
R0=report(0,0)
E0=P*P;B0=4*P*P*(1-P*P);t0=4*E0*(1-E0)
rx0=Z*(1-Z*B0)*4*P*P*(1-2*E0)*(1-B0)
a=-mp.log((1-R0)/R0)/ell*rx0
assert a<0

def native_original_value(z):
 nodes=own.fields(z,h,base)
 price=mp.mpf(0)
 for j in range(2):
  nd=nodes[j];e=nd['e'];Uj=nd['U'];Un=nodes[j+1]['U']
  f=mp.mpf(0)
  for r,s in own.PAIRS:
   Pm=Uj[r]*(Un[s] if r==0 else Uj[s])*own.v_inv(Uj[r])*own.v_inv(Uj[s])
   F=(Pm-own.v_inv(Pm))/2
   u,v=[k for k in range(4) if k not in (r,s)]
   wedge=own.wedge(e[:,u],e[:,v]);B=own.vec_b(F)
   weights=mp.matrix(1,6)
   for k in range(6):weights[0,k]=wedge[k]*own.G2[k]
   f+=(own.SGNS[r,s]*weights*own.STAR*B)[0]/h**2
  g=e.T*own.ETA*e;gi=g**-1;pp=nd['v']
  q=sum((pp[i,:]*gi*pp[i,:].T)[0] for i in range(2))
  price+=(entropy(R0)-entropy(report(f,q)))/(-tau*a)
 return price

def run():
 from time import perf_counter
 start=perf_counter();inp=json.loads((HERE/'mp_center.json').read_text())
 root=[mp.mpf(x) for x in inp['center']]
 # The exact root checks by value alone are insensitive to missing source
 # components; use a genuinely off-shell 42D test vector on the SAME carrier.
 shift=[mp.mpf(k%7-3)*mp.mpf('0.0001') for k in range(42)]
 x=[root[i]+shift[i] for i in range(42)]
 source=own.eval_euler(x,h,base)
 eps=mp.mpf('1e-22')
 errors=[]
 for i in range(42):
  xx=x.copy();xx[i]+=1j*eps
  deriv=mp.im(native_original_value(xx))/eps
  if i<16:
   expected=source[i]
  elif i<40:
   link,k=divmod(i-16,6)
   Y=mp.matrix(4)
   for b in range(6):Y+=x[16+6*link+b]*own.L[b]
   Cayley=own.cayley(Y)
   dCayley=(own.I-Y/2)**-1*(own.L[k]/2)*(Cayley+own.I)
   Xi=dCayley*(Cayley**-1)
   coefficients=[sum(Xi[u,v]*own.L[b][u,v] for u in range(4) for v in range(4))/2
                 for b in range(6)]
   expected=sum(coefficients[b]*source[16+6*link+b]/h for b in range(6))
  else:
   expected=source[i]/h
  errors.append(abs(deriv-expected))
 maxerr=max(errors)
 print('maxerr',mp.nstr(maxerr,18),'idx',errors.index(maxerr),'coframe',mp.nstr(max(errors[:16]),12),'link',mp.nstr(max(errors[16:40]),12),'matter',mp.nstr(max(errors[40:]),12)); assert maxerr<mp.mpf('1e-35'),mp.nstr(maxerr,30)
 assert max(abs(s) for s in source)>mp.mpf('1e-7')
 print('FULL 42 ORIGINAL CQ SCALAR ↔ EULER PASS',mp.nstr(maxerr,18),'seconds',round(perf_counter()-start,2))
 obj={'status':'PASS_42_ALL_DIRECTIONS_INDEPENDENT_SCALAR_PRICE_COMPLEX_STEP',
      'root_chart':'same fixed rational collar',
      'off_shell_probe':'42 rational shifts 0.0001 * ((k mod 7)-3)',
      'true_complete_CQ_norm':'original N1 Golden click, p=phi^-1 z=2^-20, not Shannon substituted as Book03 Info',
      'max_complex_step_euler_discrepancy':mp.nstr(maxerr,30),
      'complex_step':'1e-22',
      'source_scaling':'coframe=1, link=Cayley differential left-trivialized via exact Lorentz trace Gram, scalar potential=1/h',
      'checks_42':42,'scope':{'compulsory_Book03':False,'GR_closed':False}}
 (HERE/'INDEPENDENT_CQ_SOURCE_REPLAY.json').write_text(json.dumps(obj,indent=2)+'\n')
 return obj
if __name__=='__main__':run()
