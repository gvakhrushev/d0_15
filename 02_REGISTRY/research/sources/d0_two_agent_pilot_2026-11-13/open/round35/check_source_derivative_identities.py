#!/usr/bin/env python3
"""Diagnostic verification of exact half-vector source-derivative identities."""
from pathlib import Path
import math,json,numpy as np
P=Path(__file__).resolve().parent;B=P.parent/'round25';p=(math.sqrt(5)-1)/2;rootp=math.sqrt(p)
# A small full-column Choi toy with A=3, d=2, fixed identity anchor.
def J(theta):return np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]])
def dJ(theta,v):return v*np.array([[-math.sin(theta),-math.cos(theta)],[math.cos(theta),-math.sin(theta)]])
A=3;d=2;c=1/math.sqrt(d*A);angles=[.31,-.27];rates=[.7,-.4]
b=np.stack([np.eye(2),J(angles[0]),J(angles[1])]).transpose(0,2,1).reshape(-1)*c
db=np.stack([np.zeros((2,2)),dJ(angles[0],rates[0]),dJ(angles[1],rates[1])]).transpose(0,2,1).reshape(-1)*c
r=np.zeros(len(b));r[0]=1;u=(r+b)/math.sqrt(2*(1+c));du=db/math.sqrt(2*(1+c));Hr=np.eye(len(b))-2*np.outer(r,r);O=np.eye(len(b))-2*np.outer(u,u);dO=-2*(np.outer(du,u)+np.outer(u,du));dO=np.einsum('ij,jk->ik',dO,Hr)
normalization=sum(np.sum(x*x) for x in (np.zeros((2,2)),dJ(angles[0],rates[0]),dJ(angles[1],rates[1])))/(d*A)
assert abs(np.dot(db,db)-normalization)<1e-14 and abs(np.dot(u,du))<1e-14
choi_expected=math.sqrt(2/(1+c))*np.linalg.norm(db);choi_actual=np.linalg.svd(dO,compute_uv=False)[0];assert abs(choi_expected-choi_actual)<1e-14
# Actual centre CAR amplitudes for every one of the seven banks and sites.
f=np.load(B/'CENTRE_FIELDS.npz');banks=('y+','y-','f','0','x+','x-','q');direction=np.array([.7,-.2]);mx=0;checked=0
for bank in banks:
 for psi in f[bank+'_psi']:
  z=math.sqrt(1-p-np.dot(psi,psi));m=np.zeros(16);m[0]=psi[0];m[1]=rootp;m[14]=z;m[15]=psi[1]
  dm=np.zeros(16);dm[0]=direction[0];dm[15]=direction[1];dm[14]=-np.dot(psi,direction)/z
  r=np.eye(16)[:,1];u=(r+m)/math.sqrt(2*(1+rootp));du=dm/math.sqrt(2*(1+rootp));Rprime=-2*(np.outer(du,u)+np.outer(u,du))
  pred2=np.dot(direction,direction)+(np.dot(psi,direction)**2)/(1-p-np.dot(psi,psi));assert abs(np.dot(dm,dm)-pred2)<1e-14 and abs(np.dot(u,du))<1e-14
  pred=math.sqrt(2/(1+rootp))*math.sqrt(pred2);actual=np.linalg.svd(Rprime,compute_uv=False)[0];err=abs(pred-actual);mx=max(mx,err);assert err<1e-13;checked+=1
out={'status':'PASS_TARGET_DERIVATIVE_NORMALIZATION_DIAGNOSTICS','choi_identity':'||D O||²=2/(1+c) * [sum_a ||D J_a||_F²/(32 A)] for the actual d=32; constant c','toy_full_matrix_norm_difference':abs(choi_actual-choi_expected),'CAR_bank_site_derivative_cases':checked,'max_CAR_derivative_norm_difference':mx,'exact_reason':'u and Du orthogonal; rank-two symmetric derivative has eigenvalues ±2||Du||; right fixed reflections and RAW G^-⊗n are isometries','scope':'diagnostic checks; no derivative bound for a discretely selected native compiler','GR_closed':False}
(P/'SOURCE_DERIVATIVE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
