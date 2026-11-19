#!/usr/bin/env python3
"""EXACT ORIGINAL full128 CAR16/Julia/Walsh/Golden hidden Choi Info source.

An independent Q(i) exact 13-dimensional Gram reduction computes the genuine
four-mode Choi birth coefficient from ALL 128 original Kraus first jets. The
original Golden port weights are NOT replaced by a synthetic detector.

In an actual PR checkout, reads the UNCHANGED original native() constructor
whose Git blob is ee8de4635d24c668949ac9a0186616ab7d59f2ed,
and numerically crosschecks the exact coefficient by projecting the real
128x256 Kraus-Choi first derivative in its 13-dimensional physical support.

  OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_full128_choi_information_birth_2026-10-22/check_exact_coherence_source_coefficient.py

When no full upstream checkout exists, an explicitly marked local mathematical
transcription may be used solely for a separate numeric smoke (never a Git pin):
  python3 check_exact_coherence_source_coefficient.py --transcription-smoke PATH

No physical selected Book03 Info, Hodge, factory cost, all42 Einstein or GR.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import sympy as S
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix as DM
from scipy.linalg import expm, solve_sylvester

P = (math.sqrt(5)-1)/2
PS = (S.sqrt(5)-1)/2
SOURCE_BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
I16 = np.eye(16, dtype=complex)
CHECKS = 0

def check(cond, message):
    global CHECKS
    CHECKS += 1
    if not bool(cond):
        raise AssertionError(message)

def build_exact_native_zero_boost():
    """The unchanged native CAR16 32 repeated Walsh/Julia matrix-source words."""
    I = S.I
    R = S.Rational
    NU = R(3,5)
    eye = S.eye(16)
    order=(0,2,3,1)
    creators=[]
    for role in range(4):
        c=S.zeros(16)
        for bits in range(16):
            if not ((bits>>role)&1):
                c[bits|(1<<role),bits]=(-1)**sum(
                    (bits>>j)&1 for j in order[:order.index(role)])
        creators.append(c)
    gen=creators[0]*creators[1].T+creators[1]*creators[0].T
    check(gen**3==gen, "original CAR16 Lorentz G³=G EXACT")
    words=[]; dwords=[]
    for role,c in enumerate(creators):
        base=NU*c
        x=base*(I,I,-1,-I)[role]
        dx=2*I*NU*c*gen if role==1 else S.zeros(16)
        # At r=0 every native Julia root is I - (1/5) creator projector.
        L=eye-R(1,5)*c*c.T
        Rt=eye-R(1,5)*c.T*c
        if role==1:
            sl=-(dx*x.conjugate().T+x*dx.conjugate().T)
            sr=-(dx.conjugate().T*x+x.conjugate().T*dx)
            dl=S.Matrix(16,16,lambda a,b:sl[a,b]/(L[a,a]+L[b,b]))
            dr=S.Matrix(16,16,lambda a,b:sr[a,b]/(Rt[a,a]+Rt[b,b]))
        else:
            dl=dr=S.zeros(16)
        old=((x,L),(x.conjugate().T,Rt),(-base,-L),(-base.T,-Rt))
        jets=((dx,dl),(dx.conjugate().T,dr),
              (S.zeros(16),S.zeros(16)),(S.zeros(16),S.zeros(16)))
        for w,dw in zip(old,jets):
            words.extend((w,w))
            dwords.extend((dw,dw))
    check(len(words)==len(dwords)==32, "32 ORIGINAL doubled Julia input words")
    rows=[]; jets=[]
    for label in range(32):
        signs=[(-1)**(bin(label&j).count("1")&1) for j in range(32)]
        for b in (0,1):
            rows.append(sum((signs[j]*words[j][b] for j in range(32)),S.zeros(16))/32)
            jets.append(sum((signs[j]*dwords[j][b] for j in range(32)),S.zeros(16))/32)
    a=rows[0]
    check(S.simplify(a.conjugate().T*a-S.Rational(9,640)*eye)==S.zeros(16),
          "original native zero-boost Delta=9/640 I")
    newborn=[j for j in range(64) if j%4 in (0,1) and rows[j]==S.zeros(16)]
    check(newborn==[1,5,17,21,25,33,37,41,49,53,57],
          "exact 11 original newborn Walsh rows, 22 fine native Kraus labels")
    for j in newborn:
        check(S.simplify(S.trace(jets[j].conjugate().T*jets[j]))
              ==S.Rational(1,200), "each true newborn Walsh jet squared=1/200")
    return rows,jets,a

def conjdm(A):
    rows=A.to_list()
    return DM([[QQ_I(rows[i][j].x,-rows[i][j].y)
                for i in range(len(rows))] for j in range(len(rows[0]))],
              (len(rows[0]),len(rows)),QQ_I)

def dm_matrices(mats):
    rows=[[QQ_I.from_sympy(S.expand(x)) for x in list(m)] for m in mats]
    return DM(rows,(len(rows),len(rows[0])),QQ_I)

def trdm(A):
    return sum((A[i,i].element for i in range(A.shape[0])),QQ_I.zero)

def exact_christened_coherence_coefficient():
    native,dnative,a=build_exact_native_zero_boost()
    ids=[j for j in range(64) if j%4 in (0,1)]
    eye=S.eye(16)
    zero=S.zeros(16)
    # Physical u=(p,sqrt(p)) Golden port rotation:
    # u*K_j=p*(delta_j0 I -2 N_j†a), w*K_j=sqrt(p)*delta_j0 I.
    B_j=[(eye if j==0 else zero)-2*native[j].conjugate().T*a
         for j in ids]
    D_j=[-2*(dnative[j].conjugate().T*a
               +native[j].conjugate().T*dnative[0])
         for j in ids]
    B=dm_matrices(B_j)
    D=dm_matrices(D_j)
    e=dm_matrices([eye])
    # ORIGINAL fixed 13 genuine old Walsh positions, not SVD-selected.
    idx=[0,2,4,5,6,7,8,10,12,14,15,23,31]
    basis=DM([B.to_list()[i] for i in idx],(13,256),QQ_I)
    Gr=(basis*conjdm(basis)).inv()          # EXACT Q(i)
    check((basis*conjdm(basis)*Gr).to_Matrix()==S.eye(13),
          "full old CAR Choi operator basis has EXACT dimension13")
    U=B*conjdm(basis)*Gr
    c=e*conjdm(basis)*Gr
    Dproj=D*conjdm(basis)
    H=D*conjdm(D)-Dproj*Gr*conjdm(Dproj)
    Ni=(conjdm(U)*U).inv()
    R=conjdm(U)*H*U
    alpha=trdm(H)-trdm(Ni*R)
    sigma=(c*Ni*conjdm(c))[0,0].element
    tau=(c*Ni*R*Ni*conjdm(c))[0,0].element
    exact=[S.Rational(27794439,1935392000),
           S.Rational(64000,60481),
           S.Rational(144197172,91448784025)]
    for name,result,target in zip(("alpha","sigma","tau"),
                                  (alpha,sigma,tau),exact):
        check(result==QQ_I.from_sympy(target),
              "EXACT original native Q(i) 13-Gram coefficient "+name)
    cq=S.simplify(PS**2/16*(exact[0]+exact[2]/(PS+exact[1])))
    cq_goal=(9*(S.sqrt(5)-1)**2 *
        (10254021120*S.sqrt(5)+163834523471))/S.Integer(7030242019328000)
    check(S.simplify(cq-cq_goal)==0,
          "original full128 four-mode Choi coefficient in Q(sqrt5) EXACT")
    cclass=S.Rational(99,512000)*PS**2
    hidden=S.simplify(cq-cclass)
    hidden_goal=S.Rational(1701,175756050483200)*(
        86495555-25214913*S.sqrt(5))
    check(S.simplify(hidden-hidden_goal)==0,
          "original quantum-versus-classical source GAP exact algebraic")
    # Use rational upper sqrt5<9/4 for a true OUTWARD sign certificate.
    rational_floor=S.Rational(1701,175756050483200)*(
        86495555-S.Rational(9,4)*25214913)
    check(rational_floor>S.Rational(288,1000000),
          "strict exact hidden quantum memory first source >0.000288")
    return dict(cquant=cq,cclass=cclass,chidden=hidden,
        alpha=alpha,sigma=sigma,tau=tau,
        strict_rational_floor=rational_floor)

def numerical_direct_original(pinned_path):
    raw=pinned_path.read_bytes()
    sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    pinned=(sha==SOURCE_BLOB)
    smoke=(len(sys.argv)==3 and sys.argv[1]=="--transcription-smoke")
    if not smoke:
        check(pinned,"byte-identical original native source pinned Git blob")
    tree=ast.parse(raw)
    wanted={"adj","herm","root","creators","native"}
    items=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
    check({n.name for n in items}==wanted,"five original full128 native CAR functions")
    env={"np":np,"P":P,"EYE":I16,"expm":expm,
         "solve_sylvester":solve_sylvester}
    exec(compile(ast.Module(body=items,type_ignores=[]),str(pinned_path),"exec"),
         env)
    K,DKtheta=env["native"](0.0,0.6)
    DK=2*DKtheta           # r=tanh(theta/2), at zero dtheta/dr=2
    check(K.shape==(128,16,16) and DK.shape==K.shape,
          "original full128 16-CAR K and real boost first jet")
    check(np.linalg.norm(np.sum(K.conj().transpose(0,2,1)@K,axis=0)-I16)
          <4e-12,"complete actual all128 Kraus fine-work CPTP")
    A0=K.reshape(128,256)/4
    A1=DK.reshape(128,256)/4
    u,vals,vh=np.linalg.svd(A0,full_matrices=False)
    rank=int(np.sum(vals>1e-10))
    check(rank==13,"original actual r0 Choi operator rank exactly13, numeric replay")
    L=u[:,:13]; T=vh[:13]
    projected=A1-(A1@T.conj().T)@T
    projected=projected-L@(L.conj().T@projected)
    cm=float(np.linalg.norm(projected)**2)
    dark=[i for i in range(128) if np.linalg.norm(A0[i])<1e-13]
    birth=[i for i in dark if np.linalg.norm(A1[i])>1e-13]
    check(len(dark)==86 and len(birth)==22,
          "original 86 r0 dark / 22 born true fine labels")
    cc=float(sum(np.linalg.norm(A1[i])**2 for i in birth))
    sig=np.linalg.svd(projected,compute_uv=False)
    check(np.sum(sig>1e-9)==4,
          "exact-old proof quantum rank4 replicated independently by full128")
    return dict(blob=sha,pinned=pinned,original_births=len(birth),
                projected_quantum=cm,classical_birth=cc,
                Choi_new_eigenvalue_coefficients=list((sig[:4]**2).tolist()))

def main():
    exact=exact_christened_coherence_coefficient()
    if len(sys.argv)==1:
        path=SOURCE
    elif len(sys.argv)==3 and sys.argv[1]=="--transcription-smoke":
        path=Path(sys.argv[2])
    else:
        raise SystemExit("usage: script.py [--transcription-smoke /path/to/native_transcription.py]")
    actual=numerical_direct_original(path)
    cq=float(exact["cquant"])
    cc=float(exact["cclass"])
    ch=float(exact["chidden"])
    check(abs(actual["projected_quantum"]-cq)<3e-14,
          "TRUE all128 original Kraus projected quantum SOURCE equals exact Qsqrt5")
    check(abs(actual["classical_birth"]-cc)<3e-14,
          "TRUE original 22 fine births match exact Golden Born coefficient")
    check(abs(cq-cc-ch)<1e-15,
          "physical registered/coherent first-source gap nonzero and fixed")
    print(json.dumps({
      "status":"PASS_PINNED_ORIGINAL" if actual["pinned"]
               else "LOCAL_TRANSCRIPTION_SMOKE_PASS",
      "checks":CHECKS,
      "original_Git_blob_sha":SOURCE_BLOB,
      "actual_local_source_Git_blob":actual["blob"],
      "blob_verified":actual["pinned"],
      "exact_Q_i_Gram_basis_dimension":13,
      "exact_Q_i_alpha":str(QQ_I.to_sympy(exact["alpha"])),
      "exact_Q_i_sigma":str(QQ_I.to_sympy(exact["sigma"])),
      "exact_Q_i_tau":str(QQ_I.to_sympy(exact["tau"])),
      "exact_Q_sqrt5_Cquantum":str(exact["cquant"]),
      "exact_Q_sqrt5_Chidden":str(exact["chidden"]),
      "strict_hidden_lower_bound":str(exact["strict_rational_floor"]),
      "Cquantum":cq,"Cclassical":cc,"Chidden":ch,
      "relative_coherent_to_classical":cq/cc,
      "rlnr_Golden_source_gap":4*ch/math.log(1/P),
      "original_all128_direct_replay":actual,
      "compulsory_Book03_Info_selected":False,
      "original_h0_full42_Euler_source_equivalence":False,
      "GR_closed":False
    },indent=2))

if __name__=="__main__":
    main()
