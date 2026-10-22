#!/usr/bin/env python3
"""Original full128 CAR16 stationary two-port correlation and exact first source.

Consumes unchanged original constructor AST from #334; no new native gate,
physical Book03 information assignment or reset programme.
"""
from __future__ import annotations
import ast
import json
import math
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from scipy.linalg import expm, solve_sylvester

P = (math.sqrt(5.0) - 1.0) / 2.0
EYE = np.eye(16, dtype=complex)
SOURCE = Path(__file__).resolve().parents[1] / "d0_book_uniform_source_2026-10-21" / "check_uniform_book_source.py"
NAMES = {"adj", "herm", "tr", "root", "creators", "native"}

def require(cond, desc):
    if not cond:
        raise ArithmeticError(desc)

def selected_original():
    src = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(src)
    selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in NAMES]
    require({n.name for n in selected} == NAMES, "missing literal original constructor")
    ns = {"np": np, "expm": expm, "solve_sylvester": solve_sylvester, "P": P, "EYE": EYE}
    exec(compile(ast.fix_missing_locations(ast.Module(body=selected, type_ignores=[])), str(SOURCE), "exec"), ns)
    return ns

# Exact rational original theta=log(5/4), r=tanh(theta/2)=1/9 fixture.
MU = Q(141489, 10240000)
HARM = Q(69399, 5030720)
DMU = Q(-328779, 204800000)
DHARM = Q(-20040939, 9885993640)
DCOV_FACTOR = Q(1470321323030360979, 254636369534058496000000)

def original_direct():
    native = selected_original()["native"]
    theta = math.log(5/4)
    k, dk = native(theta)
    adj = lambda x: x.conj().T
    d = (EYE-k[0])/(2*P*P)
    dd = -dk[0]/(2*P*P)
    d = (d+adj(d))/2
    dd = (dd+adj(dd))/2
    inv = np.linalg.inv(d)
    z = np.trace(inv).real
    rho = inv/z
    drho = -inv@dd@inv/z + inv*np.trace(inv@dd@inv).real/(z*z)
    es = []; des = []; ys = []; dys = []
    for parity in (0,1):
        ids = range(parity, 128, 2)
        e = sum((adj(k[j])@k[j] for j in ids), np.zeros_like(EYE))
        de = sum((adj(dk[j])@k[j]+adj(k[j])@dk[j] for j in ids), np.zeros_like(EYE))
        y = sum((k[j]@rho@adj(k[j]) for j in ids), np.zeros_like(EYE))
        dy = sum((dk[j]@rho@adj(k[j])+k[j]@drho@adj(k[j])+k[j]@rho@adj(dk[j]) for j in ids), np.zeros_like(EYE))
        es.append(e); des.append(de); ys.append(y); dys.append(dy)
    require(np.linalg.norm(es[0]+es[1]-EYE)<5e-13, "complete original128 port effects")
    require(np.linalg.norm(ys[0]+ys[1]-rho)<5e-13, "true stationary native DATA")
    require(np.linalg.norm(es[1]-4*P**3*d)<5e-13, "original port1 effect equals 4p^3 Delta")
    require(np.linalg.norm(ys[1]-(4*P**3/z)*EYE)<5e-13, "stationary port1 prepares I16/16")
    require(np.linalg.norm(drho-drho.conj().T)<5e-13, "moving stationary preparation")
    require(abs(np.trace(drho))<5e-13, "normalization moving preparation")
    drdtheta = (1-(1/9)**2)/2
    pair = np.array([[np.trace(es[j]@ys[i]).real for j in range(2)] for i in range(2)])
    dpair = np.array([[np.trace(des[j]@ys[i]+es[j]@dys[i]).real/drdtheta for j in range(2)] for i in range(2)])
    return {"pair": pair, "dpair": dpair,
            "mu": np.trace(d).real/16, "harm": 16/z,
            "one": np.array([np.trace(y).real for y in ys]),
            "source": np.array([np.trace(dy).real/drdtheta for dy in dys])}

def pair_closed(mu,h,dm,dh):
    c=4*P**3
    q=c*h; dq=c*dh
    cov=c*c*h*(mu-h)
    dcov=c*c*(dh*(mu-h)+h*(dm-dh))
    pair=np.array([[(1-q)**2+cov,q*(1-q)-cov],[q*(1-q)-cov,q*q+cov]])
    dpair=np.array([[-2*(1-q)*dq+dcov,(1-2*q)*dq-dcov],
                    [(1-2*q)*dq-dcov,2*q*dq+dcov]])
    return q,dq,cov,dcov,pair,dpair

def main():
    require(MU>HARM>0,"original strict spectral mean gap")
    require(DMU<0 and DHARM<0,"original negative arithmetic/harmonic first jets")
    require(DCOV_FACTOR>0,"positive original exact covariance first source")
    require(DCOV_FACTOR==DHARM*(MU-HARM)+HARM*(DMU-DHARM),
            "rational exact covariance derivative identity")
    q,dq,cov,dcov,pair,dpair=pair_closed(float(MU),float(HARM),float(DMU),float(DHARM))
    require(abs(dcov-(4*P**3)**2*float(DCOV_FACTOR))<1e-20,"rational covariance source")
    require(0<q<.5 and 0<cov<q*(1-q),"positive non-iid native binary chart")
    require(dq<0 and dcov>0,"strict original opposite first-source signs")
    direct=original_direct()
    require(abs(direct["mu"]-float(MU))<4e-13,"real original CAR arithmetic mean")
    require(abs(direct["harm"]-float(HARM))<4e-13,"real original CAR harmonic mean")
    require(np.max(abs(direct["pair"]-pair))<5e-13,"all four original ordered probabilities")
    require(np.max(abs(direct["dpair"]-dpair))<2e-12,"all four original field derivatives")
    require(np.linalg.norm(direct["source"]-np.array([-dq,dq]))<1e-12,
            "real moving-stationary-input one-port first source")
    la=math.log1p(cov/(1-q)**2)
    lb=math.log1p(-cov/(q*(1-q)))
    lc=math.log1p(cov/q**2)
    mutual=pair[0,0]*la+2*pair[0,1]*lb+pair[1,1]*lc
    bracket=(1-q)*la-(1-2*q)*lb-q*lc
    Iq=-2*bracket
    Ic=la-2*lb+lc
    require(Iq<0 and Ic>0,"strict analytic q/cov mutual-information signs")
    dmut=Iq*dq+Ic*dcov
    require(dmut>0,"strict original full128 port-memory first source")
    hprime=dq*math.log((1-q)/q)
    h2prime=2*hprime-dmut
    direct_h2prime=-sum(dpair[i,j]*math.log(pair[i,j]) for i in range(2) for j in range(2))
    require(abs(h2prime-direct_h2prime)<1e-11,
            "independent full ordered-pair Shannon first derivative")
    # Exact general sign proof: for 0<q<1/2, 0<cov<q(1-q),
    # B(q,0)=0; derivative B_cov = cov(2q-1)/
    # [(cov+q²)(cov-q(1-q))(cov+(1-q)²)]>0.
    # Also AC-B²=cov>0 implies Ic=log(AC/B²)>0.
    denom=(q*q+cov)*(cov-q*(1-q))*((1-q)**2+cov)
    dbdcov=cov*(2*q-1)/denom
    require(dbdcov>0 and abs(math.log(pair[0,0]*pair[1,1]/pair[0,1]**2)-Ic)<5e-14,
            "algebraic logarithmic sign proof control")
    print(json.dumps({
      "status":"PASS","scope":"original CAR16 full128 stationary COARSE ports; not full Book03",
      "original_input":str(SOURCE),"r":"1/9","theta":"log(5/4)",
      "mean_delta":str(MU),"harmonic_delta":str(HARM),
      "mean_delta_prime":str(DMU),"harmonic_delta_prime":str(DHARM),
      "q1":q,"dq1_dr":dq,"q11":float(pair[1,1]),
      "pair_covariance":cov,"dcovariance_dr":dcov,
      "pair_mutual_info_nats":mutual,
      "pair_mutual_info_derivative_dr":dmut,
      "pair_mutual_info_derivative_Golden":dmut/math.log(1/P),
      "native_pair_matrix":direct["pair"].tolist(),
      "entropy_two_round_source_nats":h2prime,
      "memory_source_sign_certified_from_rational_spectrum":True,
      "stationary_preparation_moved":True,
      "iid_information_source_valid":False,
      "actual_Book03_Info_selected":False,"GR_closed":False
    },indent=2))
if __name__=="__main__": main()
