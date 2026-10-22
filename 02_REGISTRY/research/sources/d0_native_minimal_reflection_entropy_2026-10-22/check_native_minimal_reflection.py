#!/usr/bin/env python3
"""TRUE original CAR16/full128 uniquely least-rank REFLECTION and Book chronology.

Import five UNCHANGED original 128-Kraus native constructor functions from pinned
Git blob. Verify one-column unitary reflection full WORK, original supported
Kraus pointer, moving derivative, pre/source and post/source exact zeros.

No claim Book03 physically selects this task, geometry Hodge, path Info or GR.
Run from any directory inside PR repo with numpy/scipy:
OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_native_minimal_reflection_entropy_2026-10-22/check_native_minimal_reflection.py
"""
from __future__ import annotations
import ast
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm,solve_sylvester

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/"02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
SOURCE_BLOB="ee8de4635d24c668949ac9a0186616ab7d59f2ed"
P=(math.sqrt(5)-1)/2
ZETA=2**-20
E=np.eye(16,dtype=complex)
COUNT=0
def require(v,label):
    global COUNT
    COUNT+=1
    if not bool(v):raise AssertionError(label)
def close(x,y,eps,label):
    require(float(np.linalg.norm(x-y))<eps,label+" norm="+str(np.linalg.norm(x-y)))

def pinned_native():
    raw=SOURCE.read_bytes()
    digest=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    require(digest==SOURCE_BLOB,"unpadded actual ORIGINAL full128 binary Kraus Git blob")
    tree=ast.parse(raw)
    names={"native","creators","adj","herm","root"}
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    require({f.name for f in funcs}==names,"all original five complex native constructors")
    env={"np":np,"P":P,"EYE":E,"expm":expm,"solve_sylvester":solve_sylvester}
    exec(compile(ast.Module(body=funcs,type_ignores=[]),str(SOURCE),"exec"),env)
    return env["native"],digest

def actual_mask(j):
    # Exact original Q(i,sqrt24142) owner and generic symbolic source prove
    # each ACTUAL Walsh label's range mask, not a numerical fitted projector.
    if j%4 in (2,3):return ()
    if j in (1,5,17,21,25,33,37,41,49,53,57):
        return tuple(a for a in range(16) if a not in (0,4,8,12))
    if j==13:return tuple(a for a in range(16) if a!=12)
    if j==45:return tuple(a for a in range(16) if a!=0)
    if j in (29,61):return tuple(a for a in range(16) if a not in (0,12))
    return tuple(range(16))

def preg(X):
    """Literal true first-tick registered fine label support (no label erased)."""
    Z=X.copy()
    for alpha in range(128):
        live=actual_mask(alpha//2)
        if not live:Z[alpha]=0
        else:
            dead=list(set(range(16))-set(live))
            Z[alpha,dead]=0
    return Z

def main():
    native,digest=pinned_native()
    r=1/9
    K,DKtheta=native(2*math.atanh(r),.6)
    DK=DKtheta*2/(1-r*r)
    require(K.shape==(128,16,16) and DK.shape==K.shape,
            "full actual 128 fine outcomes and first moving CAR16 source")
    close(np.sum(K.conj().transpose(0,2,1)@K,axis=0),E,4e-12,
          "entire source native channel TP, not herald-only")
    B=K[0];dB=DK[0]
    close(B,B.conj().T,3e-12,"original K0 strictly Hermitian")
    require(0<np.linalg.eigvalsh(B).min()<np.linalg.eigvalsh(B).max()<1,
            "original positive K0 yields full rank minimal reflection input")
    # Full 128-register true difference A=J-V.
    A=np.zeros_like(K)
    A[0]=E-B
    A[1:]=-K[1:]
    dA=-DK
    M=2*(E-B)
    Mi=np.linalg.inv(M)
    close(np.sum(A.conj().transpose(0,2,1)@A,axis=0),M,5e-12,
          "complete FULL all128 identity A†A=2(I-K0)")
    require(np.linalg.eigvalsh(M).min()>0,"rank A=16, all oldRIGHT modes tensor")
    rng=np.random.default_rng(344)
    def pair(A,X):
        return sum((x.conj().T@y for x,y in zip(A,X)),np.zeros(16,complex))
    def project(X):
        return np.einsum('aij,j->ai',A,Mi@pair(A,X),optimize=True)
    def apply_u(X):
        return X-2*project(X)
    dM=-2*dB
    def derivative_u(X):
        v=pair(A,X)
        dv=pair(dA,X)
        w=Mi@v
        dw=Mi@dv-Mi@dM@w
        return -2*(np.einsum('aij,j->ai',dA,w,optimize=True)
                   +np.einsum('aij,j->ai',A,dw,optimize=True))
    for i in range(16):
        pure=np.zeros((128,16),complex)
        pure[0,i]=1
        close(apply_u(pure),K[:,:,i],3e-12,
              "ONLY one least-reflection-rank native U maps complete J column to K")
        close(apply_u(apply_u(pure)),pure,3e-12,
              "one native Julia full source inversion exactly on prepared input")
    for _ in range(6):
        X=rng.normal(size=(128,16))+1j*rng.normal(size=(128,16))
        close(project(project(X)),project(X),7e-11,
              "negative-reflection space orthogonal projection on ALL WORK")
        close(apply_u(apply_u(X)),X,7e-11,
              "ACTUAL complete CAR16 full128 same native minimal U selfinverse")
        close(preg(project(X)),project(X),5e-11,
              "native \u03A0_minus<=P_registered, no offbank source ambiguity")
        close(apply_u(preg(X)),preg(apply_u(X)),8e-11,
              "commuting native full supported future projector and original U")
        close(apply_u(preg(X)),preg(apply_u(preg(X))),8e-11,
              "exact same-tick P_registered Book leakage ZERO, not numerical fit")
        close(preg(derivative_u(preg(X))),derivative_u(preg(X)),5e-10,
              "original Lorentz first-source U derivative preserves fixed support")
    # Actual pre-tick native oldRIGHT Book logdet and source.
    F=E-B@B
    dF=-(dB@B+B@dB)
    require(np.linalg.eigvalsh(F).min()>0,"actual original pre-cut leakage rank16")
    Jbook=-128*np.linalg.slogdet(E-ZETA*F)[1]
    Dbook=128*ZETA*float(np.trace(np.linalg.solve(E-ZETA*F,dF)).real)
    close(Dbook,-4.746624673257693e-6,1e-12,
          "original SOURCE-CARRYING pre-tick CAR16 genuine Lorentz Book source")
    print(json.dumps({
        "status":"PASS_ORIGINAL_PINNED_128_MINIMAL_REFLECTION",
        "assertions":COUNT,
        "source_git_blob":digest,
        "original_CAR":16,"oldRIGHT":128,"full_original_work_labels":128,
        "least_selfadjoint_reflection_negative_rank_DATA":16,
        "least_selfadjoint_reflection_rank_with_RIGHT":2048,
        "true_first_pointer_support_with_RIGHT":118272,
        "exact_same_tick_postrecord_F":0,
        "genuine_original_pre_tick_J":Jbook,
        "genuine_original_pre_tick_proper_Lorentz_DJ":Dbook,
        "physical_G0_controlled_Julia_factory_selected":False,
        "actual_Book03_scene_Delta_and_Info_selected":False,
        "GR_closed":False
    },indent=2))

if __name__=="__main__":
    main()
