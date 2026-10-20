import numpy as np
from scipy.special import logsumexp
from scipy.optimize import root

def run(L,theta=2.4):
    ks=np.indices((L,)*4).reshape(4,-1).T
    # Folded momenta give exactly the same phases as periodic labels.
    z=L*np.expm1(1j*(2*np.pi*ks+theta)/L)
    A=(abs(z)**2).sum(1);B=abs(z.sum(1))**2-A
    T=np.column_stack([A,B]);beta=np.log(2)
    modes=[]
    for r in range(4):
        k=[0]*4;k[r]=L-1;modes.append(np.ravel_multi_index(k,(L,)*4))
    target=T[modes].mean(0)
    def f(x):
        w=np.exp(-beta*T@x-logsumexp(-beta*T@x));e=w@T;t=T-e
        return e-target,-beta*t.T@(w[:,None]*t)
    sol=root(f,[.08,.005],jac=True,tol=1e-10)
    d,o=sol.x;eps=T@sol.x;em=eps[modes][0]
    print('L',L,'theta',theta,'success',sol.success,'d o',d,o,'eigG',d-o,d+3*o,'target',target,'res',f(sol.x)[0],'matter',em,'min',min(eps),'below modes',np.sum(eps<em-1e-7),'nextgap',min(eps[eps>em+1e-7])-em)
    return sol
if __name__=='__main__':
    for L in [4,8,12,16,24]:run(L)
