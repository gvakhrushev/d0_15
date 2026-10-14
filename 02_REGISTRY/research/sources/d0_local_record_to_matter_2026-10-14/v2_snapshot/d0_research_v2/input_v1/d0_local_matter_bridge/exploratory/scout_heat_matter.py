import numpy as np
from scipy.optimize import root
from scipy.special import logsumexp

def solve(L,beta=np.log(2)):
    k=np.indices((L,)*4).reshape(4,-1).T
    z=L*(np.exp(2j*np.pi*k/L)-1)
    A=(abs(z)**2).sum(axis=1)
    B=(abs(z.sum(axis=1))**2-A) # 2 sum Re(z_i* z_j)
    lam1=4*L*L*np.sin(np.pi/L)**2
    target=np.array([lam1,0.])
    T=np.column_stack([A,B])
    def eval_(x,jac=False):
        vals=T@x
        probs=np.exp(-beta*vals-logsumexp(-beta*vals))
        mean=probs@T
        residual=mean-target
        C=(T-mean).T@(probs[:,None]*(T-mean))
        return (residual,-beta*C) if jac else residual
    answer=root(lambda x:eval_(x,True),np.array([.08,.03]),jac=True,tol=1e-11)
    d,o=answer.x
    vals=T@answer.x
    g=np.full((4,4),o);np.fill_diagonal(g,d)
    eig=np.linalg.eigvalsh(g)
    shellenergy=d*lam1
    print('L',L,'root',answer.success,'g',d,o,'eigG',eig,'res',eval_(answer.x), 'shellenergy',shellenergy,'minpos',np.min(vals[vals>1e-8]),'lower_modes',sum((vals<shellenergy-1e-7)&(vals>1e-8)), 'maxcond',max(eig)/min(eig))
    return answer.x

if __name__=='__main__':
    for L in [2,3,4,5,6,8,12,16]:
        solve(L)
