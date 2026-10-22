#!/usr/bin/env python3
"""Finite n=3 diagnostic for the analytic all-n logarithmic birth lower bound.
The proof of C_n >= n*C_1 is in THEOREM.md; floats do not certify all n.
"""
import json, math
import numpy as np
from native_excerpt import native,P,EYE

def dag(A): return A.conj().swapaxes(-1,-2)
def req(x,msg):
    if not bool(x): raise ArithmeticError(msg)
K,Ktheta=native(0.,.6); DK=2*Ktheta
norm=np.linalg.norm(K,axis=(1,2))
live=np.flatnonzero(norm>1e-12); dark=np.flatnonzero(norm<=1e-12)
C1=99*P**2/512000
c1=float(np.sum(np.abs(DK[dark])**2)/16)
req(len(live)==42 and len(dark)==86,'original zero-point live/dark census')
req(abs(c1-C1)<2e-15,'native newborn coefficient agrees with exact owner')
req(np.linalg.norm(sum(K@dag(K))-EYE)<1e-12,'zero-point unital channel')
A=K[live]; DA=DK[live]
L=(A[None,:,:,:]@A[:,None,:,:]).reshape(-1,16,16)
DL=(DA[None,:,:,:]@A[:,None,:,:]+A[None,:,:,:]@DA[:,None,:,:]).reshape(-1,16,16)
minnorm=math.inf; oldzero=0; extra=0.
for k,dk in zip(A,DA):
    W=k@L; DW=dk@L+k@DL
    nw=np.linalg.norm(W,axis=(1,2))
    minnorm=min(minnorm,float(nw.min()))
    missing=nw<1e-13
    oldzero+=int(missing.sum())
    extra+=float(np.sum(np.abs(DW[missing])**2)/16)
req(oldzero==0,'n3 diagnostic: all old-live products remain nonzero')
print(json.dumps({'status':'PASS_NATIVE_BIRTH_N3_NUMERICAL_EXTENSION',
                 'exact_analytical_C1':'99*p^2/512000',
                 'C1_numeric':C1,'C1_from_actual_Kraus_jets':c1,
                 'all_n_proof':'C_n >= n*C1 for each fixed finite n, via first appearance of 22 newborn labels and Phi_0(I/16)=I/16',
                 'n3_old_live_products':len(live)**3,
                 'n3_old_live_zero_products_diagnostic':oldzero,
                 'n3_smallest_product_Frobenius_norm':minnorm,
                 'n3_additional_first_order_birth_from_oldlive':extra,
                 'n3_total_C3_diagnostic':3*C1+extra,
                 'n3_rlogr_source_coefficient_diagnostic':4*(3*C1+extra)/math.log(1/P),
                 'fixed_input':'I16/16; pure rank16 reference purification for fullfine Shannon identification',
                 'n3_interval_certificate':False,'all42_source_test':False,
                 'Book03_selected':False,'GR_closed':False},indent=2))
