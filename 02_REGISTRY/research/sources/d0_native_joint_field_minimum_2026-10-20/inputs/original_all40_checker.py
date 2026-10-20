#!/usr/bin/env python3
"""EXACT original six-plaquette Lorentz-star 40-Euler theorem, arbitrary H(u,x,y).

Independent site H and independent nilpotent Lorentz link fields K2,K3
until the FULL original link Euler is solved. Standard SymPy only.
No GR physical admission or additional Palatini action asserted.
"""
import itertools
import sympy as s

h=s.symbols("h",positive=True)
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
I=s.eye(4)
pairs=list(itertools.combinations(range(4),2))
Hs,Kas,Kbs={},{},{}
N2=s.zeros(4);N2[1,2]=N2[2,0]=1
N3=s.zeros(4);N3[1,3]=N3[3,0]=1

def sh(z,a,d=1):
    out=list(z);out[a]+=d
    return tuple(out)

def sym(d,p,z):
    key=(z[0],z[2],z[3])
    if key not in d:
        d[key]=s.Symbol(p+"_".join(str(t).replace("-","m") for t in key),real=True)
    return d[key]

def H(z):return sym(Hs,"H",z)
def A(z):return sym(Kas,"A",z)
def B(z):return sym(Kbs,"B",z)

def e(z):
    E=h*I
    E[1,0]=h*H(z)/2
    return E

def U(z,r,back=False):
    if r:return I
    K=A(z)*N2+B(z)*N3
    return I+(-K if back else K)+K*K/2

def edges(z,r,t):
    return ((z,r,False),(sh(z,r),t,False),(sh(z,t),r,True),(z,t,True))
def inv(P):return eta*P.T*eta

def pair(E,u,v,R):
    C=R*eta
    return s.expand(sum(s.LeviCivita(a,b,c,d)
            *(E[a,u]*E[b,v]-E[b,u]*E[a,v])*C[c,d]
            for a,b in pairs
            for c,d in [tuple(k for k in range(4) if k not in (a,b))]))

def plaque(z,r,t):
    P=I
    for at,a,back in edges(z,r,t):P=P*U(at,a,back)
    return P

def solder(z):
    out=s.zeros(4)
    for r,t in pairs:
        u,v=(i for i in range(4) if i not in (r,t))
        P=plaque(z,r,t);R=(P-inv(P))/2
        for a in range(4):
            E=e(z);E[:,u]=I[:,a]
            out[a,u]+=s.LeviCivita(r,t,u,v)*pair(E,u,v,R)
            E=e(z);E[:,v]=I[:,a]
            out[a,v]+=s.LeviCivita(r,t,u,v)*pair(E,u,v,R)
    return out.applyfunc(s.expand)

def links(z):
    out=s.zeros(4,6)
    for axis in range(4):
        for j,(aa,bb) in enumerate(pairs):
            X=s.zeros(4);X[aa,bb]=1;X[bb,aa]=-1;X=X*eta
            val=0
            for r,t in pairs:
                if axis not in (r,t):continue
                other=t if axis==r else r
                for base in (z,sh(z,other,-1)):
                    P=I;dP=s.zeros(4)
                    for at,a,back in edges(base,r,t):
                        W=U(at,a,back)
                        dW=(-W*X if back else X*W) if at==z and a==axis else s.zeros(4)
                        dP=dP*W+P*dW;P=P*W
                    Pi=inv(P);dR=(dP+Pi*dP*Pi)/2
                    u,v=(i for i in range(4) if i not in (r,t))
                    val+=s.LeviCivita(r,t,u,v)*pair(e(base),u,v,dR)
            out[axis,j]=s.expand(val)
    return out

def same(x,y):
    assert s.expand(x-y)==0,s.expand(x-y)

def theorem():
    z=(0,0,0,0)
    density=s.expand(sum(s.LeviCivita(r,t,*[i for i in range(4) if i not in (r,t)])*
         pair(e(z),*[i for i in range(4) if i not in (r,t)],
              (plaque(z,r,t)-inv(plaque(z,r,t)))/2) for r,t in pairs))
    same(density,0)
    Es,El=solder(z),links(z)
    assert all(Es[i,j]==0 for i in range(4) for j in range(4) if(i,j)!=(0,1))
    assert all(El[i,j]==0 for i in range(4) for j in range(6)
               if(i,j) not in ((1,1),(1,2)))
    same(Es[0,1],h*(A(z)-A(sh(z,2))+B(z)-B(sh(z,3))))
    same(El[1,1],h*h*(A(sh(z,0,-1))-(H(z)-H(sh(z,2,-1)))/2))
    same(El[1,2],h*h*(B(sh(z,0,-1))-(H(z)-H(sh(z,3,-1)))/2))
    # Solve ACTUAL Cartan equations for the one-null-step forward link.
    forced={}
    for field,d,ax in (("a",Kas,2),("b",Kbs,3)):
        for key,variable in d.items():
            zp=(key[0]+1,0,key[1],key[2])
            forced[variable]=(H(zp)-H(sh(zp,ax,-1)))/2
    assert all(s.expand(El[i,j].subs(forced))==0 for i in range(4) for j in range(6))
    zp=sh(z,0)
    dif=H(sh(zp,2))+H(sh(zp,2,-1))+H(sh(zp,3))+H(sh(zp,3,-1))-4*H(zp)
    same(Es[0,1].subs(forced),-h*dif/2)
    print("PASS: density=0; 40 unrestricted Euler -> only 3 exact symbolic rows")
    print("PASS: 2 original Cartan rows uniquely fix one-u-step staggering")
    print("PASS: all 24 links zero; other 15 solder zero; remaining = -h^3/2 Lap_H(u+h)")
    print("Symbolic H/independent link unknowns:",len(Hs),len(Kas)+len(Kbs))

def harmonic():
    x,y,hx=s.symbols("x y hx",positive=True)
    d=lambda F:s.expand((F.subs(x,x+hx)+F.subs(x,x-hx)
                       +F.subs(y,y+hx)+F.subs(y,y-hx)-4*F)/hx**2)
    r2=x*x+y*y
    same(d(r2),4)
    same(d(x**3-3*x*y*y),0)
    same(d(x**4-6*x*x*y*y+y**4-hx*hx*r2),0)
    print("PASS: exact arbitrary-coefficient cubic and h^2-corrected quartic discrete harmonic")

if __name__=="__main__":
    theorem();harmonic()
    print("SCOPE: exact geometric carrier; complete native execution/price is a separate input.")
