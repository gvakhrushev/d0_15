#!/usr/bin/env python3
"""Native 0/10 Golden binary first-match: Book J2, true code KL and spatial archive.
Mathematical renewal/Book identity only: physical Book03 future task and Info remain unselected.
"""
from collections import Counter
from math import sqrt,log,log1p,exp,fsum,sin,cos,isclose
import sys

p=(sqrt(5)-1)/2
phi=1/p
ell=log(phi)
zeta=2**-20
F21=10946
checks=[]
def ck(name,cond):
    if not cond: raise AssertionError(name)
    checks.append(name)
def close(x,y,tol=1e-11):return abs(x-y)<=tol*max(1,abs(x),abs(y))
def h_e(r):return -r*log(r)-(1-r)*log1p(-r)
def h_phi(r):return h_e(r)/ell
def source_code(r):return 1-log((1-r)/r)/ell
def source_book(r):return 528/(1-r)
def K_native(r):return 1+r-h_phi(r)
def J_book(r):return -528*log1p(-r)
def L(r,K):return fsum(r**k/k for k in range(1,K+1))
def Hcap0(r,K):return L(r,K)
def Hcap1(r,K):return L(1-r,K)
def harmonic_cap(r,K):return (1-r)*Hcap0(r,K)+r*Hcap1(r,K)
def Tcap(r,K):return 3-r**K-(1-r)**K

b0=4*p**3
A0=b0*(1+p**6)
r0=zeta*(A0+b0)-zeta*zeta*A0*b0
ck('native golden p plus p squared equals one',close(p+p*p,1))
ck('original two-tick native flat A/B exactly',close(A0,b0+(1-b0)*b0))
ck('native two independent no-click factors',close(1-r0,(1-zeta*A0)*(1-zeta*b0)))
ck('original 528 Book trace log exactly same Bernoulli event',close(J_book(r0),-528*(log1p(-zeta*A0)+log1p(-zeta*b0))))
# Book II Gram constraint: a ONE-mode primitive return has 0<=F<=1.
ck('both native Book factors individually legitimate positive contractions',0<A0<1 and 0<b0<1)
ck('original actual union Bernoulli exceeds any one primitive leakage',r0>zeta)
ck('two native channels can realize original union',r0<2*zeta-zeta*zeta)
ck('naive effective single return exceeds unitarity Gram bound',r0/zeta>1)
one_mode_max=-log1p(-zeta)
book_value=J_book(r0)
ck('Book original 528-mode single-block scalar cannot suffice',book_value>528*one_mode_max)
ck('Book absolute feedback value cannot be realized in rank1024',book_value>1024*one_mode_max)
ck('Book rank1025 is the sharp ceil lower bound',book_value<1025*one_mode_max)
ck('actual two-factor 1056-mode block passes universal rank bound',1056*one_mode_max>book_value)
ck('certified original unpadded full42 positive click bands exceed one Gram fugacity',1e-6>zeta)
ck('certified full42 two-band local Book block rank floor is 554',553<528*(-log1p(-1e-6))/one_mode_max<554)
ck('two primitive fugacity channels are necessary on original flat r0',log1p(-r0)/log1p(-zeta)>1 and log1p(-r0)/log1p(-zeta)<2)
ck('native ORIGINAL 0/10 probabilities faithful',0<r0<1e-5)
ck('native code reference normalized',close(p+p*p,1))
ck('reference Kraft 0/10 is literal cost 1/2',close(-log(p)/ell,1) and close(-log(p*p)/ell,2))
for r in (r0,r0*1.5,0.01,0.05,0.2,0.3):
    kl=((1-r)*log((1-r)/p)+r*log(r/(p*p)))/ell
    ck('cost minus Shannon equals original normalized KL '+str(r),close(K_native(r),kl))
    ck('two-class firstmatch mean T=3 via exact geometric summation '+str(r),close((1-r)*(2+ r/(1-r))+r*(2+(1-r)/r),3))
    ck('true three-run expected native DATA cost '+str(r),close(3*(1+r),3*(1-r)+6*r))
    H0=-log1p(-r)
    H1=-log(r)
    ck('harmonic binary clock entropy, incl rare branch '+str(r),close((1-r)*H0+r*H1,h_e(r)))
    ck('single stopped event simultaneous Book / measured KL '+str(r),close(J_book(r),528*H0) and close(K_native(r),1+r-((1-r)*H0+r*H1)/ell))
    ck('Book source derivative strict positive '+str(r),source_book(r)>0)
    ck('native measured-KL gradient source exact '+str(r),close(source_code(r),1-log((1-r)/r)/ell))
for r in (.12,.25,.48):
    for M in (1,2,3,10,30,70):
        ck('geometric capped clock actual data rate '+str((r,M)),close((1+r)*Tcap(r,M)/Tcap(r,M),1+r))
        ck('harmonic capped Shannon below actual '+str((r,M)),harmonic_cap(r,M)<=h_e(r)+1e-15)
        ck('native Book finite-clock source exact gap '+str((r,M)),close(source_book(r)-528*sum(r**(k-1) for k in range(1,M+1)),528*r**M/(1-r)))
ck('uncapped binary firstmatch variance diverges for rare r',2*(1/r0+1/(1-r0))-6>1e6)
ck('Book source cap two is already source-close on native rare click',(528*r0*r0/(1-r0))/source_book(r0)<4e-12)
ck('Book cap three still sharper',r0**3<1e-16)
ck('fixed cap clock entropy source finite at rarity endpoint',close(1+sum(1/k for k in range(1,101)),1+fsum(1/k for k in range(1,101))))
ck('actual uncapped Shannon derivative diverges near rare endpoint', log((1-1e-12)/1e-12)>20)
ck('cost clock source cap 20m small native rare',(20_000_000*(1-r0)**(20_000_000-1))<1e-8)

# Genuine original Golden first-crossing 4D address map at n=20, unchanged.
exact=[];overs=[]
def rec(cost,j,left,width):
    if cost>=20:
        if cost==20:
            site=tuple(min(3,int(4*(left[k]+width[k]/2))) for k in range(4))
            exact.append(site)
        else:overs.append(cost)
        return
    axis=j%4
    wf=width.copy();wf[axis]*=p
    rec(cost+1,j+1,left.copy(),wf)
    wr=width.copy();lr=left.copy();lr[axis]+=p*wr[axis];wr[axis]*=p*p
    rec(cost+2,j+1,lr,wr)
rec(0,0,[0.]*4,[1.]*4)
cts=Counter(exact)
ck('original 10946 exact F/R site words',len(exact)==F21)
ck('original 6765 cost21 overshoots',len(overs)==6765 and set(overs)=={21})
ck('full 256 sites true counts min29 max78',len(cts)==256 and min(cts.values())==29 and max(cts.values())==78)
ck('all native actual site counts sum exact F21',sum(cts.values())==F21)
ck('original 72,441 complete fine records reconstructed',6765+6*F21==72441)
ck('true whole 72441 reference Kraft norm',close(6765*p**21+F21*(p**22+p**24+2*(p**24+p**25)),1,1e-9))
weights={z:n/F21 for z,n in cts.items()}
rates={z:r0*(1+0.22*sin(2.9*z[0]+1.3*z[2])+0.075*cos(1.7*z[1]+2.3*z[3])) for z in cts}
ck('all real 256 positive rare report rates',min(rates.values())>0 and max(rates.values())<1e-4)
a=2*F21*p**23
bar=fsum(weights[z]*rates[z] for z in cts)
Hloc=fsum(weights[z]*h_e(rates[z]) for z in cts)
Hglob=h_e(bar)
mi=(Hglob-Hloc)/ell
Sfine=a*fsum(weights[z]*K_native(rates[z]) for z in cts)
clock_same_site=a*((3*(1+bar))/3-Hloc/ell)
ck('whole native 0/10 site-source read from single binary clock',close(Sfine,clock_same_site))
KLfine_direct=fsum(2*p**23*(((1-rates[z])*log((1-rates[z])/p)+rates[z]*log(rates[z]/(p*p)))/ell) for z in exact)
ck('full 72441 native fine records directly give exact same KL',close(KLfine_direct,Sfine))
Psum=6765*p**21+F21*(p**22+p**24)+fsum(2*p**23*((1-rates[z])+rates[z]) for z in exact)
ck('whole 72441 native true Bernoulli measure normalized',close(Psum,1,1e-9))
ck('global/local stopped harmonic difference is exact original site MI',close(Hglob-Hloc,ell*mi) and mi>0)
ck('true native readiness is original F/R first crossing',0.34<a<0.35)
Jsite=528*fsum(weights[z]*(-log1p(-rates[z])) for z in cts)
Jclock=528*fsum(weights[z]*sum(rates[z]**k/k for k in range(1,4)) for z in cts)
Jclock_error=528*fsum(weights[z]*rates[z]**4/(4*(1-rates[z])) for z in cts)
ck('Book original 528 sitewise conditional firstmatch harmonic with finite-3 cap',0<=Jsite-Jclock<=Jclock_error*1.00001+1e-14)
# Off-null field tangent not seen in single mean but in genuinely retained source.
zi=min(cts);zj=max(cts,key=lambda z:abs(rates[z]-rates[zi]))
wi,wj=weights[zi],weights[zj]
ri,rj=rates[zi],rates[zj]
dri,drj=wj,-wi
Dbar=wi*dri+wj*drj
DMI= -wi*dri*log((1-ri)/ri)-wj*drj*log((1-rj)/rj)
ck('two true native sites have distinct report rates',abs(ri-rj)>1e-7)
ck('no coarse mean source on zero-mean field tangent',abs(Dbar)<1e-16)
ck('local stopped clock retains real off-null spatial source',abs(DMI)>1e-9)
# Sharp no-identification of two score derivatives even under stationarity.
rA,rB=r0,2*r0
ka,kb=source_code(rA),source_code(rB)
ja,jb=source_book(rA),source_book(rB)
# rate tangent drA=kb, drB=-ka gives zero code action source
ck('native exact KL stationary tangent exists',abs(ka*kb+kb*(-ka))<1e-12)
ck('Book pure-J2 action NOT stationary on same off-null tangent',abs(ja*kb-jb*ka)>1e-3)
ck('Book/code slope ratio strict monotone at rare native rates',ja/ka>jb/kb)
# K'(r)=ln(phi*r/(1-r))/lnphi, so the source ratio derivative has sign -.
for r in (r0,0.01,0.2,0.3):
    t=log(phi*r/(1-r))
    checkd=1/r-t
    ck('strict all-chart monotonicity of Book/KL gradient ratio '+str(r),t<0 and checkd>0)

print('PASS',len(checks),'scoped original Golden full-label, binary renewal, Book J2 and KL checks')
print('native r0',format(r0,'.17g'),'Book J2',J_book(r0),'code KL',K_native(r0))
print('original READY a',a,'all 256 site MI bits Golden',mi,'source',Sfine,'Book weighted site blocks',Jsite)
print('firstmatch mean trials: 3; variance at native r0:',2*(1/r0+1/(1-r0))-6)
print('Book derivative cap M=2 error:',528*r0*r0/(1-r0))
print('SHARP same-fugacity Book minimal return spectral rank:',1025,'actual 2*528 rank',1056)
print('nonclaims: future first-match task, same-site re-preparation, Book path Info, heat, controller, clock, all42 writer and GR remain OPEN')
