#!/usr/bin/env python3
"""Original CAR16 all-128 two-round complete fine Cost−Info: exact r² log r birth.

EXACT SymPy rational/Gaussian integer at native r=tanh(theta/2)=0,
all 64 genuine original Walsh rows, full 16-CAR modes, original φ p+p²=1.
Then NUMERICAL actual unmodified 128 Kraus full 128² two-round fine labels,
their true proper-Lorentz derivatives and native 0/10 output costs.
All original dark/failure labels remain in the complete sample language.

The nonzero rare-event log-monodromy coefficient is EXACT and requires no
floating numerical entropy sign or fitted Info; the numerics are diagnostic.
This does NOT identify compulsory Book03 vertex-Info/scene-Hodge with Shannon.

Run in PR checkout:
 OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_native_minimal_reflection_entropy_2026-10-22/check_native_two_tick_information_birth.py
"""
from __future__ import annotations
import ast
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as S
from sympy.polys.matrices import DomainMatrix
from sympy.polys.domains import QQ
from scipy.linalg import expm,solve_sylvester

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/"02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
SOURCE_BLOB="ee8de4635d24c668949ac9a0186616ab7d59f2ed"
P=(math.sqrt(5)-1)/2
LNPHI=math.log(1/P)
EYE=np.eye(16,dtype=complex)
R=S.Rational
I=S.I
COUNT=0
def require(v,label):
    global COUNT
    COUNT+=1
    if not bool(v):raise ArithmeticError(label)
def close(v,w,tol,label):
    require(abs(v-w)<tol,f"{label}: observed={v}, expected={w}")

def exact_native_birth():
    nu=R(3,5)
    creators=[]
    order=(0,2,3,1)
    for mode in range(4):
        c=S.zeros(16)
        for bits in range(16):
            if not ((bits>>mode)&1):
                c[bits|(1<<mode),bits]=(-1)**sum(
                    ((bits>>a)&1) for a in order[:order.index(mode)])
        creators.append(c)
    G=creators[0]*creators[1].T+creators[1]*creators[0].T
    require(G**3==G,"actual original CAR16 boost generator G³=G")
    source_words=[]; source_jets=[]
    for mode,c in enumerate(creators):
        base=nu*c
        x=(I,I,-1,-I)[mode]*base
        dx=2*I*nu*c*G if mode==1 else S.zeros(16)
        L=S.eye(16)-R(1,5)*c*c.T
        Rt=S.eye(16)-R(1,5)*c.T*c
        if mode==1:
            sL=-(dx*x.conjugate().T+x*dx.conjugate().T)
            sR=-(dx.conjugate().T*x+x.conjugate().T*dx)
            dL=S.Matrix(16,16,lambda a,b:sL[a,b]/(L[a,a]+L[b,b]))
            dR=S.Matrix(16,16,lambda a,b:sR[a,b]/(Rt[a,a]+Rt[b,b]))
        else:dL=dR=S.zeros(16)
        actual=((x,L),(x.conjugate().T,Rt),(-base,-L),(-base.T,-Rt))
        jets=((dx,dL),(dx.conjugate().T,dR),
              (S.zeros(16),S.zeros(16)),(S.zeros(16),S.zeros(16)))
        for pair,dpair in zip(actual,jets):
            source_words.extend((pair,pair))
            source_jets.extend((dpair,dpair))
    require(len(source_words)==32,"unchanged 32 repeated original CAR Julia words")
    rows=[]; drows=[]
    for lab in range(32):
        signs=[(-1)**(bin(lab&j).count("1")&1) for j in range(32)]
        for bit in range(2):
            rows.append(sum((signs[j]*source_words[j][bit]
                             for j in range(32)),S.zeros(16))/32)
            drows.append(sum((signs[j]*source_jets[j][bit]
                              for j in range(32)),S.zeros(16))/32)
    a=rows[0]; mu=R(9,640)
    require(S.simplify(a.conjugate().T*a-mu*S.eye(16))==S.zeros(16),
            "ORIGINAL K0 r=0 Delta=9/640 I; true Born full trace initial")
    require(S.simplify(a*a.conjugate().T-mu*S.eye(16))==S.zeros(16),
            "ORIGINAL CAR unitality source scalar at zero boost")
    complete=sum((v.conjugate().T*v for v in rows),S.zeros(16))
    require(S.simplify(complete-S.eye(16))==S.zeros(16),
            "the unchanged 64 Walsh rows remain isometric")
    field=QQ.algebraic_field(I)
    ranks=[]
    for j,row in enumerate(rows):
        rank=0 if j//2%2 else DomainMatrix.from_Matrix(row).convert_to(field).rank()
        ranks.append(rank)
    require(Counter(ranks)==Counter({0:43,16:17,10:4}),
            "EXACT original boost-zero 64 rows have 42 active fine ports")
    born=[j for j in range(64) if ranks[j]==0 and j//2%2==0]
    require(born==[1,5,17,21,25,33,37,41,49,53,57],
            "exact 11 new Walsh rows =22 ORIGINAL 128 Kraus fine labels")
    for j in born:
        require(rows[j]==S.zeros(16),"literal newborn original row zero at boost zero")
        require(S.simplify(S.trace(drows[j].conjugate().T*drows[j]))
                ==R(1,200),
                "EXACT original newborn 16-CAR Julia first-jet norm 1/200")
    phi_p=(S.sqrt(5)-1)/2
    require(S.simplify(phi_p**2+phi_p-1)==0,"ORIGINAL GOLDEN p²+p=1")
    c0=9*phi_p**4/R(512000)
    c1=9*phi_p**3/R(512000)
    one=S.simplify(11*(c0+c1))
    total=S.simplify(2*one)
    require(S.simplify(one-99*phi_p**2/R(512000))==0,
            "EXACT all 22 fine first-tick birth coefficient")
    require(S.simplify(total-99*phi_p**2/R(256000))==0,
            "EXACT entire two-tick birth coefficient with actual unital Phi0")
    # Every pair of 42 previously live outcomes has rank≥10, so Sylvester:
    require(min(r for r in ranks if r>0)>=10 and 2*10-16>0,
            "ALL 42² native double-live words positive at r0 by Sylvester rank")
    return dict(active_original_128_at_zero=42,
                dark_original_128_at_zero=86,
                newborn_original_128=22,
                exact_newborn_rows=born,
                newborn_per_even_coefficient=str(c0),
                newborn_per_odd_coefficient=str(c1),
                one_tick_birth=str(one),
                total_two_tick_birth=str(total),
                two_tick_leading_source_coefficient=
                    str(S.simplify(4*total/S.log(1/phi_p))),
                total_numeric=float(total))

def native_constructor():
    raw=SOURCE.read_bytes()
    sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    require(sha==SOURCE_BLOB,"unchanged actual original 128 native Git blob")
    tree=ast.parse(raw)
    needed={"native","creators","adj","herm","root"}
    selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in needed]
    require({n.name for n in selected}==needed,"all five original Kraus constructor functions")
    env={"np":np,"P":P,"EYE":EYE,"expm":expm,"solve_sylvester":solve_sylvester}
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(SOURCE),"exec"),env)
    return env["native"],sha

def numerical_original_two_tape(native,exact):
    r=1/9
    K,DKtheta=native(2*math.atanh(r),.6)
    DK=DKtheta*2/(1-r*r)
    require(K.shape==(128,16,16),"full original 128 Kraus CAR16 source")
    eye=np.eye(16)
    require(np.linalg.norm(np.sum(K.conj().transpose(0,2,1)@K,axis=0)-eye)<3e-12,
            "ORIGINAL all128 complete CPTP, failures included")
    measured=np.zeros((128,128))
    derivative=np.zeros((128,128))
    for a in range(128):
        K_a=K[a]; dKa=DK[a]
        T=K_a@K_a.conj().T/16
        dT=(dKa@K_a.conj().T+K_a@dKa.conj().T)/16
        for b in range(128):
            kb=K[b];dkb=DK[b]
            measured[a,b]=float(np.trace(kb@T@kb.conj().T).real)
            derivative[a,b]=float(np.trace(dkb@T@kb.conj().T
                              +kb@dT@kb.conj().T+kb@T@dkb.conj().T).real)
    close(float(measured.sum()),1.,1e-11,"ALL 128² sequential probabilities normalize")
    close(float(derivative.sum()),0.,3e-10,"ALL 128² actual native CAR source conserved")
    live=measured>1e-20
    require(int(live.sum())==4096,"64 original live output labels squared (all other cases retained)")
    costs=2+(np.arange(128)%2)[:,None]+(np.arange(128)%2)[None,:]
    costs=np.broadcast_to(costs,measured.shape)
    score=float((measured*costs).sum()
          +(measured[live]*np.log(measured[live])).sum()/LNPHI)
    dscore=float((derivative*costs).sum()
           +(derivative[live]*(np.log(measured[live])+1)).sum()/LNPHI)
    require(dscore>.04,"diagnostic native Cost−Info has positive field source")
    # independently evaluate full native first-rare-event second-jet,
    # including all original 86 zero-event labels at r=0.
    K0,DK0t=native(0,.6)
    DK0=DK0t*2
    dark=[j for j in range(128) if np.linalg.norm(K0[j])<1e-12]
    require(len(dark)==86,"at original r=0 native 128 Kraus has 86 zero labels")
    birth=sum((np.linalg.norm(DK0[j])**2/16 for j in dark))
    close(float(birth),float(exact["total_numeric"]/2),2e-14,
          "all original 22 newborn one-round Born coefficient EXACT CAR count")
    require(np.linalg.norm(np.sum(K0@K0.conj().transpose(0,2,1),axis=0)-eye)<4e-12,
            "original CAR16 stationary point truly unital at boost zero")
    # Direct independent two-tick newborn coefficient without dropping ANY
    # 128² zero paths; the right and left branch share previous DATA.
    fullbirth=0.
    positive_derivative_words=0
    for a in range(128):
        for b in range(128):
            existing=K0[b]@K0[a]
            if np.linalg.norm(existing)<1e-11:
                dword=DK0[b]@K0[a]+K0[b]@DK0[a]
                coef=np.linalg.norm(dword)**2/16
                fullbirth+=coef
                if coef>1e-17:positive_derivative_words+=1
    close(float(fullbirth),float(exact["total_numeric"]),3e-13,
          "EXACT native two-tick all-fine birth coefficient from independent matrices")
    return {
        "r":"1/9","nu":"3/5","all_fine_histories":128**2,
        "fine_positive_histories":int(live.sum()),
        "fine_dark_histories":int((~live).sum()),
        "true_measured_code_price":score,
        "true_measured_code_price_source":dscore,
        "source_type":"NUMERICAL native 2-tick FULL measured fine Cost−Info, NOT compulsory Book03",
        "first_boost_zero_birth_numeric":birth,
        "two_boost_zero_birth_numeric":fullbirth,
        "positive_derivative_paths_at_boost_zero":positive_derivative_words
    }

def main():
    exact=exact_native_birth()
    native,digest=native_constructor()
    numeric=numerical_original_two_tape(native,exact)
    print(json.dumps({
        "status":"PASS_PINNED_ORIGINAL_NATIVE_TWO_TICK_LOG_MONODROMY",
        "checks":COUNT,
        "original_upstream_git_blob":digest,
        "exact_algebraic_native_birth":exact,
        "original_native_all_128_squared_numerics":numeric,
        "full_twotick_cost_source_equals_only_paired_Hodge_J":False,
        "compulsory_Book03_Info_and_scene_Hodge_selected":False,
        "GR_closed":False
    },indent=2))

if __name__=="__main__":
    main()
