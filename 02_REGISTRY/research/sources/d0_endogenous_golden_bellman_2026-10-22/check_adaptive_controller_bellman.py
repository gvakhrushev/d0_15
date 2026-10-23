#!/usr/bin/env python3
"""Bounded high-precision replay: original Golden c, two adaptive
apertures, full moving PF and exact Bellman future-coboundary algebra.

MATHEMATICAL INTERFACE ONLY. No physical Book03 selection or GR closure.
Requires mpmath. Assertions are independent of Python -O.
"""
import itertools
import json
import mpmath as mp

mp.mp.dps = 90
count = 0

def check(condition, desc):
    global count
    if not condition:
        raise RuntimeError("failed: " + desc)
    count += 1

def close(a, b, desc, eps=mp.mpf("1e-58")):
    check(abs(a-b) <= eps * max(1, abs(a), abs(b)), desc)

p = (mp.sqrt(5)-1)/2
phi = 1/p
sigma = p*p
ell = mp.log(phi)
zeta = mp.mpf(2)**(-20)
tau = mp.mpf("0.05")
check(0<p<1, "positive golden p")
close(p+p*p, 1, "Kraft exact normalization")
close(p*sigma+sigma, p, "exact p tau mean")

def report(x, y):
    E = sigma*(1+x)
    L = 4*E*(1-E)
    b = p-sigma*y
    B = 4*b*b*(1-b*b)
    A = L+(1-L)*B
    return 1-(1-zeta*A)*(1-zeta*B)

def entropy(q):
    if q == 0 or q == 1:
        return mp.mpf("0")
    return -(q*mp.log(q)+(1-q)*mp.log(1-q))/ell

ref = report(0,0)
def c(x,y):
    r = report(x,y)
    return r-entropy(r)-(ref-entropy(ref))

a0=mp.diff(lambda x:c(x,0),0)
b0=mp.diff(lambda y:c(0,y),0)
hxx=mp.diff(lambda x:c(x,0),0,2)
hyy=mp.diff(lambda y:c(0,y),0,2)
hxy=mp.diff(lambda x:mp.diff(lambda y:c(x,y),0),0)
check(hxx>0 and hyy>0 and hxx*hyy-hxy*hxy>0,
      "true original two-operand Hessian positive")
K=1/(tau*mp.diff(entropy,ref)*mp.diff(lambda x:report(x,0),0))
check(K>0, "unchanged positive original normalization")

rho0=mp.mpf("1.3")
rho_slope=mp.mpf("0.27")
f_slope=mp.mpf("0.70")
q_slope=mp.mpf("-0.40")
f_accel=mp.mpf("0.12")
q_accel=mp.mpf("-0.06")
def fields(Y):
    f=f_slope*Y+f_accel*Y*Y/2
    q=q_slope*Y+q_accel*Y*Y/2
    rho=rho0+rho_slope*Y
    return f,q,rho

def S(t,Y):
    f,q,rho=fields(Y)
    return K*rho*c(t*f/rho,t*q/rho)/t

def S0(Y):
    f,q,rho=fields(Y)
    return K*(a0*f+b0*q)

ts=[sigma*tau,tau]
weights0=[p,sigma]
def Fstar(Y):
    return -mp.log(sum(
        weights0[j]*mp.exp(-ell*S(ts[j],Y)) for j in range(2)
    ))/ell
def wstar0(Y):
    z=[weights0[j]*mp.exp(-ell*S(ts[j],Y)) for j in range(2)]
    return z[0]/sum(z)

# Field chart includes D rho != 0, D2 f != 0 and D2 q != 0.
close(mp.diff(Fstar,0),mp.diff(S0,0),
      "adaptive controller exact first-source agreement at null")
close(mp.diff(wstar0,0),0,"optimized adaptive controller has no first jet at null")
pred = K*p*tau/rho0*(hxx*f_slope*f_slope
                     +2*hxy*f_slope*q_slope+hyy*q_slope*q_slope)
calculated=mp.diff(Fstar,0,2)-mp.diff(S0,0,2)
close(calculated,pred,"adaptive softmin exact 42-direction Hessian excess")
check(pred>0,"strict positive calibrated Hessian excess")

selector_slope=mp.mpf("0.13")
def Fmoving(Y):
    w=p+selector_slope*Y
    return (w*(1+S(ts[0],Y))+(1-w)*(2+S(ts[1],Y))
            +(w*mp.log(w)+(1-w)*mp.log(1-w))/ell)

fisher=selector_slope**2/ell*(1/p+1/sigma)
close(mp.diff(Fmoving,0,2)-mp.diff(S0,0,2), pred+fisher,
      "entire moving-selector Fisher plus source curvature")
check(fisher>0, "moving selector Fisher positive")

# Golden full 0/10 code pair and complete 33-leaf conditional extension.
P=[sigma,p]
costs=[1,2]
mu=[p,sigma]
Hsum=-(sum(P[j]*mp.log(P[j]) for j in range(2)))/ell
Csum=sum(P[j]*costs[j] for j in range(2))
g=2*Hsum-Csum
close(Hsum, 2-p,"original nonblank Golden entropy")
close(Csum, 1+p,"original nonblank Golden charge")
close(g, 3*sigma,"Golden Bellman surplus")
I_old=[costs[j]+mp.log(P[j])/ell+g for j in range(2)]
close(I_old[0],3*sigma-1,"one-pair original Bellman I0")
close(I_old[1],1+3*sigma,"one-pair original Bellman I1")
N=5
g_suffix=[mp.mpf(0),N*g]
avg_g=sum(P[j]*g_suffix[j] for j in range(2))
I_new=[I_old[j]+avg_g-g_suffix[j] for j in range(2)]
close(I_new[1],1+3*sigma-15*p**4,"five-level signed vertex shift")
check(I_old[0]>0 and I_old[1]>0 and I_new[1]<0,
      "paid conditional suffix flips realised I sign")
close(sum(P[j]*(I_new[j]-I_old[j]) for j in range(2)),0,
      "future-coboundary conditional mean zero")
close(sum(P[j]*I_new[j] for j in range(2)),Hsum,
      "local conditional entropy gain preserved")

leaves=[(sigma,mp.mpf(p),mp.mpf(I_new[0]))]
for seq in itertools.product((0,1), repeat=N):
    prob=p
    cost=mp.mpf(2)
    info=mp.mpf(I_new[1])
    kraft=mp.mpf(sigma)
    for b in seq:
        prob*=P[b]
        cost+=costs[b]
        info+=I_old[b]  # independent identical suffix step
        kraft*=mu[b]
    leaves.append((prob,kraft,info,cost))
# replace the first leaf with same four-column structure
leaves[0]=(sigma,mp.mpf(p),mp.mpf(I_new[0]),mp.mpf(1))
check(len(leaves)==33, "complete finite Golden future leaf count")
close(sum(lf[0] for lf in leaves),1,"entire Born leaf normalization")
close(sum(lf[1] for lf in leaves),1,"entire Golden prefix Kraft reference")
f_root=g+avg_g
bookZ=sum(mp.exp(-ell*(lf[3]-lf[2])) for lf in leaves)
close(bookZ,mp.exp(ell*f_root),"Bellman Book absolute partition")
for lf in leaves:
    P_leaf,kraft,I_leaf,C_leaf=lf
    close(mp.exp(-ell*(C_leaf-I_leaf))/bookZ,P_leaf,
          "complete pathwise Born=normalized Book")
Imean=sum(lf[0]*lf[2] for lf in leaves)
Cmean=sum(lf[0]*lf[3] for lf in leaves)
Hleaf=-sum(lf[0]*mp.log(lf[0]) for lf in leaves)/ell
close(Imean,Hleaf,"complete expected information equals leaf entropy")
close(Cmean-Imean,Csum-Hsum+p*N*(Csum-Hsum),
      "future costs change full net price only by paid continuation")

# Full first-source zero for the coboundary even if root P is field-dependent.
def shift_mean(Y):
    r=report(Y/15,mp.mpf("0.5")*Y)
    changes=[r*N*g,-(1-r)*N*g]
    return (1-r)*changes[0]+r*changes[1]
close(mp.diff(shift_mean,0),0,"zero Bellman coboundary first-source")
close(mp.diff(shift_mean,0,2),0,"zero Bellman coboundary second-source")

print(json.dumps({
    "status":"SCOPED original constitutive/Bellman math only, GR_closed=false",
    "checks_passed":count,
    "golden_mean_aperture_over_tau":mp.nstr(p,30),
    "calibrated_Hxx_excess_if_rho_1":mp.nstr(K*p*tau*hxx,26),
    "moving_rho_adaptive_hessian_excess":mp.nstr(pred,25),
    "moving_selector_fisher_excess":mp.nstr(fisher,25),
    "bellman_original_I1":mp.nstr(I_old[1],25),
    "bellman_five_suffix_I1":mp.nstr(I_new[1],25),
    "complete_future_leaves":len(leaves),
    "original_Book03_physically_selected":False
},indent=2))
