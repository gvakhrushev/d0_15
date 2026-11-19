#!/usr/bin/env python3
"""Exact original full718 oriented CP Book-Hessian vs two-line complete-record Hellinger.
Positive mathematical scene-register theorem only: not full128 physical CAR or GR.
"""
import mpmath as mp

mp.mp.dps=60
q=mp.mpf
phi=(1+mp.sqrt(5))/2
ell=mp.log(phi)
p=1/phi
n=[9,11,13]
labels=[i for i,ni in enumerate(n) for _ in range(ni)]
edges=[(u,v) for u in range(33) for v in range(33) if labels[u]!=labels[v]]
assert len(edges)==718
d={(0,1):1,(1,2):1,(2,0):1,(1,0):-1,(2,1):-1,(0,2):-1}

def complete_chi(epsilon):
    # Perron right eigenvector on the zone-constant 3×3 image of ORIGINAL 33×33 matrix
    M=mp.matrix([[n[j]*p*mp.exp(-ell*epsilon*d[i,j]) if i!=j else q(0)
                  for j in range(3)] for i in range(3)])
    vals,V=mp.eig(M)
    ir=max(range(3),key=lambda i:mp.re(vals[i]))
    lam=mp.re(vals[ir])
    r=[mp.re(V[i,ir]) for i in range(3)]
    if sum(r)<0:r=[-a for a in r]
    # Left per-vertex PF vector equals the right Perron vector of reversed CP bias
    M_left=mp.matrix([[n[j]*p*mp.exp(+ell*epsilon*d[i,j]) if i!=j else q(0)
                       for j in range(3)] for i in range(3)])
    vl,L=mp.eig(M_left)
    il=max(range(3),key=lambda i:mp.re(vl[i]))
    l=[mp.re(L[i,il]) for i in range(3)]
    if sum(l)<0:l=[-a for a in l]
    normalizer=sum(n[z]*l[z]*r[z] for z in range(3))
    chi=[]
    for u,v in edges:
        i,j=labels[u],labels[v]
        mu=l[i]*p*mp.exp(-ell*epsilon*d[i,j])*r[j]/(lam*normalizer)
        chi.append(mp.sqrt(mu))
    assert abs(sum(t*t for t in chi)-1)<q("1e-45")
    return chi

def dot(u,v):
    return sum(a*b for a,b in zip(u,v))

delta=359/phi**2-phi**-5-(q(12288)/5*phi**-6+phi**-3/3)
chi0=complete_chi(q(0))
chip=complete_chi(delta)
chim=complete_chi(-delta)
reversal={e:i for i,e in enumerate(edges)}
assert max(abs(chip[i]-chim[reversal[(v,u)]])
           for i,(u,v) in enumerate(edges))<q("1e-44")
overlap=dot(chip,chim)
assert q(0)<overlap<q(1)
rho=mp.findroot(lambda x:x**3-359*x-2574,q("21.8"))
V_CP=q(23166)/(rho*(3*rho*rho-359))
mixed=ell*ell*V_CP/4
book_hessian=-ell*V_CP
assert abs(book_hessian+4*mixed/ell)<q("1e-48")
# finite differences on ALL 718 true recorded outcomes independently verify the 2-line metric.
for h in (q("0.001"),q("0.0001"),q("0.00001")):
    plus=complete_chi(h)
    minus=complete_chi(-h)
    derivative=[(a-b)/(2*h) for a,b in zip(plus,minus)]
    metric=dot(derivative,derivative)
    assert abs(metric-mixed)<q("1e-7")
    print("CHECK TWO-LINE METRIC h=",mp.nstr(h,7),
          " value=",mp.nstr(metric,21),"target=",mp.nstr(mixed,21))
assert abs((1-overlap)/delta**2-2*mixed)<q("1e-8")
print("PASS ORIGINAL 718 FULL POSITIVE EDGE-RECORD TWO-ARM BOOK HESSIAN")
print("sqrt record full fidelity=",mp.nstr(overlap,25),
      " loss=",mp.nstr(1-overlap,25))
print("Book A''=",mp.nstr(book_hessian,22),
      " same-action two-arm cross metric=",mp.nstr(mixed,22))
print("FIREWALL: a mathematical Hellinger comparison, NOT physical full128/CAR coherent phase or GR")
