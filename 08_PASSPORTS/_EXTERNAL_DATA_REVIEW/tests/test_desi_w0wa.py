#!/usr/bin/env python3
# DESI DR2 BAO: does it prefer evolving DE in the (w0>-1, wa<0) corner? (D0 phason W-Z forced prediction)
# Fast: alpha=c/(H0 r_d) enters linearly -> analytic profiling.
import numpy as np, os, warnings
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
D=os.path.join(os.path.dirname(__file__),"..","cache","desi_dr2_bao")
z=[];val=[];qty=[]
for line in open(os.path.join(D,"desi_gaussian_bao_ALL_GCcomb_mean.txt")):
    s=line.strip()
    if not s or s.startswith("#"): continue
    a,b,c=s.split(); z.append(float(a)); val.append(float(b)); qty.append(c)
z=np.array(z); val=np.array(val); n=len(val)
cov=np.loadtxt(os.path.join(D,"desi_gaussian_bao_ALL_GCcomb_cov.txt")); Cinv=np.linalg.inv(cov)
print(f"DESI DR2 BAO: {n} measurements")

def geom(Om,w0,wa,ng=400):
    # returns the alpha=1 model vector g (so model = alpha*g), vectorized comoving integrals
    zmax=z.max(); zs=np.linspace(0,zmax,ng)
    Ez_grid=np.sqrt(Om*(1+zs)**3+(1-Om)*(1+zs)**(3*(1+w0+wa))*np.exp(-3*wa*zs/(1+zs)))
    invE=1.0/Ez_grid; cum=np.concatenate([[0],np.cumsum((invE[1:]+invE[:-1])/2*np.diff(zs))])
    g=np.zeros(n)
    for i in range(n):
        Dc=np.interp(z[i],zs,cum); Ez=np.sqrt(Om*(1+z[i])**3+(1-Om)*(1+z[i])**(3*(1+w0+wa))*np.exp(-3*wa*z[i]/(1+z[i])))
        if qty[i]=="DM_over_rs": g[i]=Dc
        elif qty[i]=="DH_over_rs": g[i]=1.0/Ez
        elif qty[i]=="DV_over_rs": g[i]=(z[i]*Dc**2/Ez)**(1/3)
    return g
def chi2min_over_alpha(Om,w0,wa):
    g=geom(Om,w0,wa)
    A=g@Cinv@g; B=g@Cinv@val; d=val@Cinv@val
    alpha=B/A; return d-B*B/A, alpha
def profileOm(w0,wa):
    best=1e18; bo=ba=0
    for Om in np.linspace(0.24,0.42,37):
        c,al=chi2min_over_alpha(Om,w0,wa)
        if c<best: best,bo,ba=c,Om,al
    return best,bo,ba

c_lcdm,Om_l,al_l=profileOm(-1.0,0.0)
print(f"LCDM (w0=-1,wa=0): chi2={c_lcdm:.2f}, Om={Om_l:.3f}, alpha=c/(H0 rd)={al_l:.3f}")
best=1e18;bw0=bwa=0
for w0 in np.linspace(-1.3,-0.1,49):
    for wa in np.linspace(-3.2,1.6,49):
        c,_,_=profileOm(w0,wa)
        if c<best: best,bw0,bwa=c,w0,wa
cb,Omb,alb=profileOm(bw0,bwa)
print(f"w0waCDM best: chi2={cb:.2f} at w0={bw0:.3f}, wa={bwa:.3f}, Om={Omb:.3f}")
print(f"Delta chi2 (LCDM - best) = {c_lcdm-cb:.2f}  (2 extra dof)")
corner=(bw0>-1) and (bwa<0)
print(f"\nbest-fit corner: w0>-1 ? {bw0>-1} ; wa<0 ? {bwa<0}  -> (w0>-1, wa<0): {corner}")
print(f"D0 forced prediction (evolving DE, thawing corner w0>-1,wa<0 from convexity D^2 R_n>0):")
print(f"   {'CONFIRMED by DESI DR2 BAO' if corner else 'NOT confirmed (tension)'}")
# also report the w0+wa (phantom-crossing) diagnostic: w(z=0)=w0, w(early)=w0+wa
print(f"   w(z=0)=w0={bw0:.2f} (>-1 => non-phantom today); w(early)=w0+wa={bw0+bwa:.2f} (<-1 => crossed -1: thawing)")
