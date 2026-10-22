#!/usr/bin/env python3
"""ORIGINAL CAR16/full128 Golden Boolean Naimark ALL-OUTCOME causal weld.

Consumes the unchanged original 5 native functions in the existing
d0_native65_causal_source_2026-10-22/native_excerpt.py (original source
Git blob ee8de4635d24c668949ac9a0186616ab7d59f2ed).
No new gates, iid reset, source coefficients or artificial CAR matrices.
Full first noncommuting derivative checked by Sylvester equation. The
matched Book PRE feedback is NOT the full compulsory Book03 H+J+R.
Run with python3 and python3 -O (all checks use explicit exceptions).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import solve_sylvester

sys.path.insert(0, str(
    Path(__file__).resolve().parent.parent /
    "d0_native65_causal_source_2026-10-22"
))
from native_excerpt import native

p = (math.sqrt(5)-1)/2
zeta=2**-20
eye=np.eye(16,dtype=complex)
NTEST=0

def check(cond,desc):
    global NTEST
    NTEST+=1
    if not bool(cond):
        raise ArithmeticError(desc)

def near(a,b,epsilon,desc):
    check(abs(a-b)<epsilon,f"{desc}: {a} vs {b}")

def dagger(a):
    return a.conj().T

def posroot(a):
    evals,u=np.linalg.eigh((a+dagger(a))/2)
    check(float(evals.min())>0,"true strictly positive spectral matrix")
    return (u*np.sqrt(evals))@dagger(u)

def construct(theta):
    K,dK=native(theta,0.6,(1j,1j,-1.0,-1j))
    check(K.shape==(128,16,16),"UNCHANGED original 128 CAR Kraus slots")
    near(np.linalg.norm(
        np.einsum("aij,aik->jk",K.conj(),K,optimize=True)-eye),
        0,1e-11,"all ORIGINAL CP effects sum to identity")
    Delta=(eye-K[0])/(2*p*p)
    Delta=(Delta+dagger(Delta))/2
    ev=np.linalg.eigvalsh(Delta)
    check(float(ev.min())>0 and float(ev.max())<1,
          "original CAR Delta strictly inside Boolean interval")
    root=posroot(Delta@(eye-Delta))
    inverse=np.linalg.inv(root)
    q=np.block([[Delta,root],[root,eye-Delta]])
    near(np.linalg.norm(q@q-q),0,1e-12,
         "minimal Boolean Naimark Q is EXACT projector")
    near(np.linalg.norm(q-dagger(q)),0,1e-12,
         "Q is self-adjoint")
    check(np.count_nonzero(np.linalg.eigvalsh(q)>.5)==16,
          "Naimark projector rank is original DATA dimension16")
    k0=eye-2*p*p*Delta
    k1=-2*p*math.sqrt(p)*Delta
    near(np.max(np.abs(k0-K[0])),0,1e-11,"original blank K0")
    near(np.max(np.abs(k1-K[1])),0,1e-11,"original orphan K1")

    W=np.array([
        -K[2*j]@inverse/(2*p*p)
        for j in range(1,64)
    ])
    near(np.linalg.norm(
        np.einsum("aij,aik->jk",W.conj(),W,optimize=True)-eye
    ),0,1e-10,"63 retained original row refinement maps are ONE isometry")
    predicted=np.zeros_like(K)
    predicted[0]=k0
    predicted[1]=k1
    for j in range(1,64):
        predicted[2*j]=W[j-1]@(-2*p*p*root)
        predicted[2*j+1]=W[j-1]@(-2*p*math.sqrt(p)*root)
        check(np.max(np.abs(predicted[2*j]-K[2*j]))<1e-12,
              "original even CAR channel after Golden projector")
        check(np.max(np.abs(predicted[2*j+1]-K[2*j+1]))<1e-12,
              "original odd CAR channel after Golden projector")

    Golden=np.array([[math.sqrt(p),-p],[p,math.sqrt(p)]])
    bigeye=np.eye(32,dtype=complex)
    D=np.block([[bigeye,np.zeros((32,32))],
                [np.zeros((32,32)),bigeye-2*q]])
    U=np.kron(Golden.T,bigeye)@D@np.kron(Golden,bigeye)
    near(np.linalg.norm(dagger(U)@U-np.eye(64)),0,1e-11,
         "REAL Golden Gdag-reflection-G is a full unitary")
    prepared=U[:,:16]
    four=[prepared[0:16],prepared[16:32],
          prepared[32:48],prepared[48:64]]
    target=[k0,-2*p*p*root,k1,-2*p*math.sqrt(p)*root]
    for a,b in zip(four,target):
        near(np.max(np.abs(a-b)),0,1e-12,
             "original prepared four Golden quantum output amplitudes")

    E_nb=np.einsum("aij,aik->jk",K[2:].conj(),K[2:],optimize=True)
    near(np.linalg.norm(E_nb-4*p*p*Delta@(eye-Delta)),0,1e-11,
         "ALL original j>0 branch effects retained")
    check(float(np.linalg.eigvalsh(E_nb).min())>0.0199,
          "nonblank ORIGINAL event strictly positive on all DATA")

    # Genuine full ORIGINAL noncommuting DATA jets: D sqrt(T) solves
    # Sylvester S dS+dS S=dDelta-dDelta Delta-Delta dDelta.
    dDelta=-(dK[0])/(2*p*p)
    dDelta=(dDelta+dagger(dDelta))/2
    dX=dDelta-dDelta@Delta-Delta@dDelta
    droot=solve_sylvester(root,root,dX)
    near(np.linalg.norm(root@droot+droot@root-dX),0,1e-11,
         "full noncommuting Frechet square-root first source")
    dW=np.array([
        -(dK[2*j]@inverse-K[2*j]@inverse@droot@inverse)/(2*p*p)
        for j in range(1,64)
    ])
    derived=np.zeros_like(dK)
    derived[0]=-2*p*p*dDelta
    derived[1]=-2*p*math.sqrt(p)*dDelta
    for j in range(1,64):
        common=dW[j-1]@root+W[j-1]@droot
        derived[2*j]=-2*p*p*common
        derived[2*j+1]=-2*p*math.sqrt(p)*common
    near(np.max(np.abs(derived-dK)),0,1e-11,
         "ALL 128 genuine original Kraus first source jets match")

    F=eye-dagger(K[0])@K[0]
    near(np.linalg.norm(
        F-4*p*p*Delta@(eye-p*p*Delta)),0,1e-11,
         "completion-invariant PRE Book F from original K0")
    near(np.linalg.norm(
        F-E_nb-dagger(K[1])@K[1]),0,1e-11,
         "PRE Book includes EVERY nonblank PLUS orphan effect")
    Jpre=-float(np.log1p(-zeta*np.linalg.eigvalsh(F)).sum())
    dF=-dagger(dK[0])@K[0]-dagger(K[0])@dK[0]
    dJ=zeta*float(np.trace(
        np.linalg.solve(eye-zeta*F,dF)).real)
    near(dJ,4*p*p*zeta*float(np.trace(
        np.linalg.solve(eye-zeta*F,(eye-2*p*p*Delta)@dDelta)).real),
        1e-12,"literal fixed PRE Book first source")
    Jwide=-16*math.log1p(-4*p**3*zeta)
    return {
       "theta":theta,
       "max_all128_reproduction_error":float(np.max(np.abs(predicted-K))),
       "max_all128_first_source_error":float(np.max(np.abs(derived-dK))),
       "Q_projector_error":float(np.linalg.norm(q@q-q)),
       "row_isometry_error":float(np.linalg.norm(
           np.einsum("aij,aik->jk",W.conj(),W)-eye)),
       "delta_eig_min":float(ev.min()),
       "delta_eig_max":float(ev.max()),
       "J_pre_per_oldRIGHT":Jpre,
       "J_pre_dtheta_per_oldRIGHT":dJ,
       "J_WIDE_per_oldRIGHT_exact_fieldconstant":Jwide,
       "K":K,"Kr":predicted
    }

def main():
    theta=2*math.atanh(1/9)
    mid=construct(theta)
    eps=1e-4
    hi=construct(theta+eps)
    lo=construct(theta-eps)
    centered=(hi["J_pre_per_oldRIGHT"]-
              lo["J_pre_per_oldRIGHT"])/(2*eps)
    near(centered,mid["J_pre_dtheta_per_oldRIGHT"],1e-14,
         "Book PRE source matches independent proper-boost physical secant")
    near(hi["J_WIDE_per_oldRIGHT_exact_fieldconstant"],
         lo["J_WIDE_per_oldRIGHT_exact_fieldconstant"],1e-14,
         "unprepared WIDE Boolean cut has ZERO source")
    check(abs(mid["J_pre_dtheta_per_oldRIGHT"])>1e-9,
          "prepared original Golden feedback source is genuinely nonzero")

    # A true original no-reset two-tick quantum test, not independent bits.
    delta=(eye-mid["K"][0])/(2*p*p)
    rho=np.linalg.inv(delta)
    rho/=np.trace(rho)
    def two_tick_law(arr):
        eff=np.einsum("aij,aik->ajk",arr.conj(),arr,optimize=True)
        states=np.einsum("aij,jk,alk->ail",arr,rho,arr.conj(),optimize=True)
        return np.einsum("aij,bji->ab",states,eff,optimize=True).real
    near(float(np.max(np.abs(
        two_tick_law(mid["K"])-two_tick_law(mid["Kr"])))),
        0,1e-12,"whole 128x128 NO-RESET actual sequential history equals rebuilt")
    def public_values(x):
        return {k:v for k,v in x.items() if k not in ("K","Kr")}
    print(json.dumps({
      "status":"PASS_ORIGINAL_CAR16_FULL128_GOLDEN_MINIMAL_NAIMARK_CAUSAL_WELD",
      "checks":NTEST,
      "original_constructor":"immutable blob ee8de4635d24c668949ac9a0186616ab7d59f2ed",
      "source_is_original_full128_Kraus":True,
      "work_extra_DIM_minimal":16,
      "whole_original_native_Kraus_labels":128,
      "nonblank_17plus_Choi_directions_retained":True,
      "present_prepared_Book_cut_source_nonzero":True,
      "unprepared_full_port_Book_cut_source_zero":True,
      "at_original_proper_boost":public_values(mid),
      "compulsory_Book03_scene_HJR_selected":False,
      "GR_closed":False
    },sort_keys=True,indent=2))

if __name__=="__main__":
    main()
