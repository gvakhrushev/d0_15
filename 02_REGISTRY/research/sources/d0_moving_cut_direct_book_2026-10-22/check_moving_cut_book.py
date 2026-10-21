#!/usr/bin/env python3
"""Exact constructive moving-preparation cut and full128 Book-clock identities.

Mathematical effect and tangent checks; no physical Book03 active-cut admission.
No assert statements: Python -O executes all checks.
"""
import json
import hashlib
import math
import sympy as sp
import numpy as np

p=(sp.sqrt(5)-1)/2
z=sp.Rational(1,2**20)
checks=[]
def check(condition,label):
    if not bool(condition):
        raise ArithmeticError(label)
    checks.append(label)

# Exact noncommuting prepared POVM effect in dimension 2.
P=sp.diag(1,1,0,0)
W0=sp.Matrix([[sp.Rational(3,5),0],[0,sp.Rational(4,5)],
              [sp.Rational(4,5),0],[0,sp.Rational(3,5)]])
V=sp.Matrix([[sp.Rational(3,5),-sp.Rational(4,5)],
             [sp.Rational(4,5),sp.Rational(3,5)]])
W=W0*V
Q=W*W.T
E=W.T*P*W
check(W.T*W==sp.eye(2),"prepared W full isometry")
check(E[0,1]!=0,"prepared POVM genuinely nondiagonal")
check(E*E != E,"prepared POVM not a projector")
check(Q*Q==Q and Q.T==Q,"range projector exact")

# Controlled Z onto Pi, with Hadamards before/after: U=I⊗(I-Pi)+X⊗Pi.
I4=sp.eye(4)
I2=sp.eye(2)
X=sp.Matrix([[0,1],[1,0]])
U=sp.kronecker_product(I2,I4-P)+sp.kronecker_product(X,P)
Ppost=sp.kronecker_product(sp.diag(1,0),Q)
T=sp.zeros(8,2)
T[:4,:]=W
F=Ppost*U.T*(sp.eye(8)-Ppost)*U*Ppost
Fcompress=T.T*F*T
Fspectral=2*E-E*E
check(U.T*U==sp.eye(8),"fixed H CZ H exact unitary")
check(Ppost*Ppost==Ppost,"moving Book cut exact projection")
check(Fcompress==Fspectral,"Book complement equals 2E-E²")
check(F*F != F,"nontrivial fractional Book complement")
check(sp.factor((sp.eye(2)-z*Fcompress).det()-
                (sp.eye(2)-z*Fspectral).det())==0,"exact spectral determinant")

# The native Golden reflection comparator uses b=p, not a fitted knob.
# Unlike the H comparator, its moving-cut spectral map is exactly the
# earlier fixed-cut V†CZV reflected-reporter map, with NO physical V†.
a=sp.sqrt(p)
Rg=sp.Matrix([[p,a],[a,-p]])
Zphase=sp.diag(1,1,1,1)
Zphase=sp.eye(4)-2*P
CZ=sp.diag(1,1,1,1,1,1,1,1)
CZ[4:8,4:8]=Zphase
Ugold=sp.kronecker_product(Rg,sp.eye(4))*CZ*sp.kronecker_product(Rg,sp.eye(4))
check(sp.simplify(Rg.T*Rg-sp.eye(2))==sp.zeros(2),"original Golden reflection orthogonal")
check(sp.simplify(Ugold.T*Ugold-sp.eye(8))==sp.zeros(8),"fixed Golden CZ Golden all-column unitary")
Agold=sp.simplify(T.T*Ppost*Ugold*Ppost*T)
Fgold=sp.simplify(T.T*(Ppost*Ugold.T*(sp.eye(8)-Ppost)*Ugold*Ppost)*T)
check(sp.simplify(Agold-(sp.eye(2)-2*p*E))==sp.zeros(2),"Golden prepared return I-2pE")
check(sp.simplify(Fgold-4*p*E*(sp.eye(2)-p*E))==sp.zeros(2),"Golden Book F=4p E(I-pE)")

# Exact field tangent: vary *output* isometry W by A∈so(4).
A=sp.zeros(4)
A[0,2]=sp.Rational(1,7)
A[2,0]=-sp.Rational(1,7)
A[1,3]=-sp.Rational(2,9)
A[3,1]=sp.Rational(2,9)
A[0,3]=sp.Rational(1,8)
A[3,0]=-sp.Rational(1,8)
DW=A*W
DE=DW.T*P*W+W.T*P*DW
DF=2*DE-E*DE-DE*E
Zmat=sp.eye(2)-z*Fspectral
jprime=sp.simplify(z*sp.trace(Zmat.inv()*DF))
simplified=sp.simplify(2*z*sp.trace((sp.eye(2)-E)*Zmat.inv()*DE))
check(sp.simplify(jprime-simplified)==0,"noncommutative source identity")
check(E*DE!=DE*E,"first source genuinely noncommuting")
check(jprime!=0,"genuine output-range source")
Fgf=4*p*E*(sp.eye(2)-p*E)
DFgold=4*p*(DE-p*(E*DE+DE*E))
JGsource=sp.simplify(z*sp.trace((sp.eye(2)-z*Fgf).inv()*DFgold))
JGcompact=sp.simplify(4*p*z*sp.trace((sp.eye(2)-2*p*E)*(sp.eye(2)-z*Fgf).inv()*DE))
check(sp.simplify(JGsource-JGcompact)==0,"Golden noncommuting source functional exact")
check(JGsource!=0,"Golden prepared-cut physical source nonzero")


# Free-Grassmann range theorem and exact quantitative normal gradient.
K=2*z*(sp.eye(2)-E)*Zmat.inv()
normal=(sp.eye(4)-Q)*P*W*K
check(normal!=sp.zeros(4,2),"nonstationary independent prepared range")
check(sp.simplify(sp.trace(normal.T*normal))>0,"strict nonzero gradient squared")
# The chosen transverse direction, normalized to unit HS, has positive J variation.
Xdir=normal
DEnorm=Xdir.T*P*W+W.T*P*Xdir
DJnorm=sp.simplify(sp.trace(K*DEnorm))
check(sp.simplify(DJnorm-2*sp.trace(normal.T*normal))==0,"Grassmann source pairing")

# Scalar rank-one exact input Euler and source gain at half report.
r=sp.symbols('r', real=True)
f=2*r-r**2
jrprime=sp.diff(-sp.log(1-z*f),r)
check(sp.simplify(jrprime-2*z*(1-r)/(1-z*f))==0,"scalar Book derivative")
check(sp.simplify(jrprime.subs(r,sp.Rational(1,2))-z/(1-3*z/4))==0,
      "fair-bit positive source gain")
fGolden=4*p*r*(1-p*r)
JGoldenPrime=sp.simplify(sp.diff(-sp.log(1-z*fGolden),r))
check(sp.simplify(JGoldenPrime-4*p*z*(1-2*p*r)/(1-z*fGolden))==0,
      "Golden prepared-cut derivative")
check(sp.simplify(fGolden.subs(r,sp.Rational(1,2))-(3*p-1))==0,
      "original fair Golden return F0=3p-1")
check(sp.simplify(JGoldenPrime.subs(r,sp.Rational(1,2))-
            4*p**3*z/(1-z*(3*p-1)))==0,
      "same exact source coefficient as previous reflected native route")
rcritical=1/(2*p)
check(sp.simplify(JGoldenPrime.subs(r,rcritical))==0,
      "Golden interior free-input critical reporter root")
check(sp.simplify(fGolden.subs(r,rcritical)-1)==0,
      "Golden interior free-input root saturates feedback F=1")
check(sp.Rational(0)<float(rcritical)<sp.Rational(1),
      "Golden interior critical effect is strictly fractional")

check(sp.simplify((4*z*(1-r)*sp.sqrt(r*(1-r))/(1-z*f)).subs(r,sp.Rational(1,2))-
                  z/(1-3*z/4))==0,"free-preparation nonzero derivative at fair report")
KgoldScalar=4*p*z*(1-2*p*r)/(1-z*fGolden)
check(sp.simplify(KgoldScalar.subs(r,rcritical))==0,
      "Golden principal-angle extra critical set, not [Q,Pi] condition")
check(sp.simplify(KgoldScalar.subs(r,sp.Rational(1,2))-
             4*p**3*z/(1-z*(3*p-1)))==0,
      "Golden fair free-preparation source strictly nonzero")

# A stationary prepared projector can have *fractional* principal angles
# at the Golden sweet spot; all corresponding first sources vanish, not GR.
check(abs(float(rcritical)-0.8090169943749475)<1e-14,
      "Golden additional interior principal-angle critical point")
# Original whole full128: for ALL actual noncommuting B>0, full n-round blank
# effect C=B^(2n), real physical isometry, feedback after moving prepared cut
# uses I-C² = I-B^(4n), i.e. original true blank 2n trace source.
B=sp.Matrix([[sp.Rational(9,10),sp.Rational(1,20)],
             [sp.Rational(1,20),sp.Rational(4,5)]])
dB=sp.Matrix([[sp.Rational(1,13),sp.Rational(1,7)],
              [sp.Rational(1,7),-sp.Rational(1,9)]])
check(B*dB!=dB*B,"geometry jet noncommutes with blank")
for n in (1,2,3,4):
    C=B**(2*n)
    post=2*(sp.eye(2)-C)-(sp.eye(2)-C)**2
    check(post==sp.eye(2)-B**(4*n),f"unmarked doubled-clock complement n={n}")
    Dpower=sum((B**k*dB*B**(4*n-1-k) for k in range(4*n)),sp.zeros(2))
    Qblank=(1-z)*sp.eye(2)+z*B**(4*n)
    dj=-z*sp.trace(Qblank.inv()*Dpower)
    check(dj!=0,f"actual noncommuting doubled-clock source n={n}")

# True operator-marked N: noncommuting positive normalizer. C is allblank
# gram e^-nt B^(2n), 0<C<N. Direct determinant identity removes polar root.
N=sp.Matrix([[sp.Rational(4,5),sp.Rational(1,20)],
             [sp.Rational(1,20),sp.Rational(9,10)]])
C=sp.Matrix([[sp.Rational(1,2),sp.Rational(1,9)],
             [sp.Rational(1,9),sp.Rational(2,5)]])
check(N*C!=C*N,"noncommuting genuine-style normalizer control")
check(all(float(v)>0 for v in N.eigenvals()),"N positive")
check(all(float(v)>0 for v in (N-C).eigenvals()),"C below N")
Krootfree=(1-z)*N+z*C*N.inv()*C
poly_ratio=sp.factor(Krootfree.det()/N.det())
# Similarity identity  det(I-z+z N^-1/2 C N^-1 C N^-1/2)
Knon=sp.eye(2)-z*sp.eye(2)+z*N.inv()*C*N.inv()*C
check(sp.factor(poly_ratio-Knon.det())==0,"noncommuting rootfree determinant")
check(all(float(v)>0 for v in Krootfree.eigenvals()),"rootfree positive")

# Gold-marked (possibly nonscalar) polar normalizer has ONE rootfree
# master determinant for both original comparator primitives b=1/2 and b=p.
G=(1-2*p)*N+2*p*C
Kgold=(1-z)*N+z*G*N.inv()*G
Goldratio=sp.simplify(Kgold.det()/N.det())
Goldnon=sp.det((1-z)*sp.eye(2)+z*N.inv()*G*N.inv()*G)
check(sp.simplify(Goldratio-Goldnon)==0,
      "Golden noncommuting marked root-free source denominator")
check(all(float(v)>0 for v in Kgold.eigenvals()),
      "Golden root-free marked determinant remains positive")
# Moving N,C tangent, including DN contribution, direct derivative vs scalar secant.
t=sp.symbols('t', real=True)
dN=sp.Matrix([[sp.Rational(1,6),sp.Rational(1,17)],
              [sp.Rational(1,17),-sp.Rational(1,10)]])
dC=sp.Matrix([[sp.Rational(1,11),-sp.Rational(1,15)],
              [-sp.Rational(1,15),sp.Rational(1,13)]])
Nt=N+t*dN
Ct=C+t*dC
Kt=(1-z)*Nt+z*Ct*Nt.inv()*Ct
Jdirect=sp.log(Nt.det())-sp.log(Kt.det())
janalytic=sp.simplify(sp.diff(Jdirect,t).subs(t,0))
DK=(1-z)*dN+z*(dC*N.inv()*C+C*N.inv()*dC-C*N.inv()*dN*N.inv()*C)
jsource=sp.simplify(sp.trace(N.inv()*dN)-sp.trace(Krootfree.inv()*DK))
check(sp.simplify(janalytic-jsource)==0,"full noncommuting normalizer jet")
check(jsource!=0,"nontrivial normalization jet")
dG=(1-2*p)*dN+2*p*dC
DKgold=(1-z)*dN+z*(dG*N.inv()*G+G*N.inv()*dG-G*N.inv()*dN*N.inv()*G)
Jgsource=sp.simplify(sp.trace(N.inv()*dN)-sp.trace(Kgold.inv()*DKgold))
Gammat=(1-2*p)*Nt+2*p*Ct
Kgt=(1-z)*Nt+z*Gammat*Nt.inv()*Gammat
Jgdirect=sp.log(Nt.det())-sp.log(Kgt.det())
check(sp.simplify(Jgsource-sp.diff(Jgdirect,t).subs(t,0))==0,
      "full Golden marked noncommuting normalizer and field jet")

check(C*N.inv()*C!=N.inv()*C*C,"reject commuting marked Gram shortcut")
missing_dn=sp.simplify(-sp.trace(Krootfree.inv()*z*(dC*N.inv()*C+C*N.inv()*dC)))
check(sp.simplify(jsource-missing_dn)!=0,"reject frozen normalizer source")

# Native N1 paid reporter source: one same fair reference after full finite
# output with actual h_phi'(r0)>0; exact positive ratio no calibration.
r0=1-(1-z*4*p**3)*(1-z*4*p**3*(1+p**6))
ell=sp.log(1/p)
hprime=sp.log((1-r0)/r0)/ell
check(0<float(r0)<.5,"true Golden N1 report below fair")
check(float(hprime)>0,"true native entropy response positive")
Wcount=sp.Integer(39)
gamma=sp.Rational(2,3)
d=sp.Integer(128)
gain=sp.simplify(d*z/(4*Wcount*gamma*hprime*(1-3*z/4)))
check(float(gain)>0,"Book/CQ source ratio positive all42")
gainGolden=sp.simplify(d*z*p**3/(Wcount*gamma*hprime*(1-z*(3*p-1))))
check(float(gainGolden)>0,"original Golden Book/CQ positive source gain")

du,dv=sp.symbols("du dv",real=True)
dr_mean=(sp.Integer(39)*du+sp.Integer(48)*dv)/Wcount
DJbook=-(d*z/(1-3*z/4))*dr_mean/4
DS_CQ=-gamma*hprime*(sp.Integer(39)*du+sp.Integer(48)*dv)
check(sp.simplify(DJbook-gain*DS_CQ)==0,"all-report first-covector exact positive gain")
DJgold=-d*z*p**3*dr_mean/(1-z*(3*p-1))
check(sp.simplify(DJgold-gainGolden*DS_CQ)==0,
      "Golden fixed-comparator all42 source matches old V† source coefficient")

hsecond=-1/(ell*r0*(1-r0))
defect=gain*gamma*hsecond*(sp.Integer(39)*du**2+sp.Integer(48)*dv**2)
check(float(sp.N(defect.subs({du:1,dv:0})))<0,"Hessian defect negative without inertia shortcut")

# Flat report E=rI2 admits no free prepared-Grassmann stationary point.
rhalf=sp.Rational(1,2)
Ws=sp.Matrix([[sp.Rational(3,5),0],[0,sp.Rational(3,5)],
              [sp.Rational(4,5),0],[0,sp.Rational(4,5)]])
Qs=Ws*Ws.T
Es=Ws.T*P*Ws
rs=sp.Rational(9,25)
check(Es==rs*sp.eye(2),"uniform rank2 protected report fixture")
ks=2*z*(1-rs)/(1-z*(2*rs-rs**2))
Gs=2*(sp.eye(4)-Qs)*P*Ws*ks
pred=4*z*(1-rs)*sp.sqrt(2*rs*(1-rs))/(1-z*(2*rs-rs**2))
check(sp.simplify(sp.trace(Gs.T*Gs)-pred**2)==0,"exact rank2 Grassmann gradient norm")


out={"status":"PASS","check_count":len(checks),"checks":checks,
"noncommuting_effect":str(E),"full128_clock":{"unmarked_exact":"J_post,n=J_blank,2n on common B, NOT same execution","marked_rootfree":"K=(1-z)N+z C N^-1 C"},
"scope":{"no_moving_inverse":True,"fixed_H_CZ_H":True,"active_cut_moves":True,
"physical_active_cut_selected":False,"full_native_Book03_selected":False,
"genuinely_free_preparation_stationary":False,"GR_closed":False},
"native_N1_report_base":float(r0),"native_gain_fixture_H":float(gain),"native_gain_fixture_Golden":float(gainGolden),
"input_E_stationarity":"H: [Q,Pi]=0; Golden: eigen E in {0,1,1/(2p)}"}
print(json.dumps(out,indent=2,sort_keys=True))
