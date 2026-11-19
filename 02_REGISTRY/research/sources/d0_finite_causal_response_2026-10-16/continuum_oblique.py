import numpy as np
from itertools import product

def limit(cut=8,scale=2.,beta=None,z=2**-20,M=128):
 p=(np.sqrt(5)-1)/2
 if beta is None:beta=2*p*p
 q=2*np.pi;ks=np.array(list(product(range(-cut,cut+1),repeat=4)),int);x=q*ks
 l=np.sum(x*x,axis=1)/(scale*scale);y=x.copy();y[:,1:3]+=q;lp=np.sum(y*y,axis=1)/(scale*scale)
 E=np.exp(-beta*l);Ep=np.exp(-beta*lp);Z=16*E.sum();F=1-z+z*E;Fp=1-z+z*Ep
 k=-E/Z+M*z*beta*E/F;kp=-Ep/Z+M*z*beta*Ep/Fp
 deriv=beta*E/Z-M*z*beta*beta*(1-z)*E/(F*F)
 dif=lp-l;eq=abs(dif)<1e-10;dd=np.empty(len(l));dd[eq]=deriv[eq];dd[~eq]=(kp[~eq]-k[~eq])/dif[~eq]
 nnE=4*q*q*(x[:,1]-x[:,2])**2/scale**2
 U=x[:,0]**2+x[:,1]**2+x[:,2]**2+q*(x[:,1]+x[:,2])+q*q
 nnA=8*q*q*(x[:,1]-x[:,2])**2*U/scale**4
 a=2*(k+kp)*nnE;b=2*dd*nnA;terms=a+b
 return dict(cut=cut,Z=float(Z),source=float(terms.sum()),source_parts=[float(a.sum()),float(b.sum())],lowest_mode_positive=float(terms[(ks==np.array([0,-1,0,0])).all(1)][0]),min_term=float(terms.min()),max_term=float(terms.max()),mu=float(M*z*beta*Z/(1-z)))
if __name__=='__main__':
 import json
 for K in [3,4,5,6,8]:print(json.dumps(limit(K)))
