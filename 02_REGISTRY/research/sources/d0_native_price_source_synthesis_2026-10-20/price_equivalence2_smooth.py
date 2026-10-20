import numpy as np
from math import pi
from scipy.integrate import quad
C=[]
for a in range(4):
 c=np.zeros((16,16))
 for m in range(16):
  if not(m>>a)&1:c[m|1<<a,m]=(-1)**((m&((1<<a)-1)).bit_count())
 C.append(c)
I=np.eye(16);N=C[1]@C[2].T+C[2]@C[0].T
nu=.3;ku=2*pi;amplitude=.4

def root(a):
 v,e=np.linalg.eigh((a+a.T.conj())/2);assert min(v)>0.1
 return (e*np.sqrt(v))@e.T.conj()
def fieldmat(m,f):return np.einsum('xij,xjk->xik',m,f)
def adj(m):return np.swapaxes(m.conj(),1,2)
def compute(L,amp=amplitude,lc=True):
 h=1/L;x=np.arange(L)*h;H=amp*np.sin(2*pi*x)
 K=(H-np.roll(H,1))/(2*h) if lc else np.zeros(L)
 lifted=np.array([I+h*k*N+(h*k)**2*(N@N)/2+(h*k)**3*(N@N@N)/6 for k in K])
 assert np.linalg.norm(N@N@N@N)<1e-12
 c=[np.tile(nu*C[1],(L,1,1)),nu*(np.tile(C[0],(L,1,1))-H[:,None,None]*C[1]/2),np.tile(nu*C[2],(L,1,1)),np.tile(nu*C[3],(L,1,1))]
 p=[c[0]@lifted*np.exp(1j*ku*h),c[1],c[2],c[3]]
 def P(r,f):return fieldmat(p[r],np.roll(f,-1,axis=0) if r==2 else f)
 def Pd(r,f):
  z=fieldmat(adj(p[r]),f)
  return np.roll(z,1,axis=0) if r==2 else z
 def D(f):
  out=np.zeros_like(f,dtype=complex)
  for r in range(4):out+=P(r,f)-fieldmat(c[r],f)+Pd(r,f)-fieldmat(adj(c[r]),f)
  return out/h
 psi=np.zeros((L,16,2),complex);psi[:,0,0]=psi[:,2,1]=1/np.sqrt(2*L)
 lam=4*nu**2*np.sin(ku*h/2)**2/h**2
 assert np.linalg.norm(D(D(psi))-lam*psi)<1e-10
 dpsi=D(psi); energy=0.;qenergy=0.;mass=0
 for r in range(4):
  lp=np.array([root(I-a@a.T.conj()) for a in p[r]])
  rp=np.array([root(I-a.T.conj()@a) for a in p[r]])
  # For P_x, right defect is shifted local C*C (constant here).
  if r==2:rp=np.roll(rp,1,axis=0)
  lc0=np.array([root(I-a@a.T) for a in c[r]])
  rc=np.array([root(I-a.T@a) for a in c[r]])
  vals=[P(r,dpsi),Pd(r,dpsi),fieldmat(lp,dpsi),fieldmat(rp,dpsi),fieldmat(c[r],dpsi),fieldmat(adj(c[r]),dpsi),fieldmat(lc0,dpsi),fieldmat(rc,dpsi)]
  for f in vals:
   df=D(f);energy+=np.vdot(df,df).real/16
   ddf=D(df);qenergy+=(np.vdot(df,df).real-h*h*np.vdot(ddf,ddf).real/256)/16
   mass+=np.vdot(f,f).real/16
 assert abs(mass-lam)<1e-11
 drift=energy-lam**2
 qdrift=qenergy-lam**2*(1-h*h*lam/256)
 return dict(L=L,lambda_h=lam,energy_generator_drift=drift,Q_generator_drift=qdrift)
def g(H,lc=True):
 b=np.sqrt(1-nu*nu*(1+H*H/4))
 if lc:return (1-b)*((3*b*b+2*b+1)*H**4+(44*b*b+4)*H*H+32*b**3+64*b*b)/(b*b*(H*H+4)**3)
 return nu*nu/4*(1+nu*nu*H*H/(4*b*b)+nu*nu/(1+b)**2)
def limit(amp,lc=True):
 return (nu*ku)**2*nu**2/8*quad(lambda x:(amp*2*pi*np.cos(2*pi*x))**2*g(amp*np.sin(2*pi*x),lc),0,1,epsabs=1e-12)[0]
if __name__=='__main__':
 for lc in (False,True):
  print('LC=',lc,'continuum=',limit(amplitude,lc))
  target=limit(amplitude,lc);errors=[]
  for L in (8,16,32,64,128):
   r=compute(L,lc=lc);print(r)
   assert r['energy_generator_drift']>0 and r['Q_generator_drift']>0
   errors.append(abs(r['energy_generator_drift']-target))
  assert all(errors[j+1]<errors[j]/3 for j in range(1,len(errors)-1))
  assert errors[-1]<1.1e-5
  da=1e-5
  ds=(compute(64,amplitude+da,lc)['energy_generator_drift']-compute(64,amplitude-da,lc)['energy_generator_drift'])/(2*da)
  dc=(limit(amplitude+da,lc)-limit(amplitude-da,lc))/(2*da)
  assert abs(ds-dc)<2.1e-4
  print('amplitude first source h64=',ds,'continuum=',dc)
 print('PASS exact native identities, positive coefficients and converging first source')
