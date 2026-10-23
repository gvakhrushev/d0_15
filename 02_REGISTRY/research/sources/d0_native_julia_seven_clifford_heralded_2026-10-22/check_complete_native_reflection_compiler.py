#!/usr/bin/env python3
"""Original D0 Fourier CAR16 and ALL 128 old true fine Kraus:
complete 7-work-bit logical circuit Q (H4, 8-way Julia MUX, H4,
one REAL Golden G). Independent full original Kraus owner comparison,
entire coherent old-work inversion Q†, plus mathematically honest
(5/8 Q†) R_blank (5/8 Q) = (25/64)U_full128 success Kraus.

The SEVEN constant 3/5 Julia blocks' one-shot uniform (5/8) factor
is proved exactly over CAR32 by sibling
check_seven_julia_heralded_galois.mjs. The EIGHTH genuinely boosted
Julia block is a *conditional* physically admitted external input.
This checker DOES NOT pretend the abstract 3/4-dimensional quantum
factories/clock/readout are physically compiled or GR closed.
"""
from __future__ import annotations
import importlib.util
import math
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCES = HERE.parent
ORIG = SOURCES/"d0_book_uniform_source_2026-10-21"/"check_uniform_book_source.py"
assert ORIG.exists()
s = importlib.util.spec_from_file_location("native_original_full128", ORIG)
assert s and s.loader
old = importlib.util.module_from_spec(s)
s.loader.exec_module(old)

p = (math.sqrt(5)-1)/2
theta = math.log(5/4)
I = np.eye(16, dtype=complex)
Z0 = np.zeros((16,16),complex)
h16 = np.array([[(-1)**((i&j).bit_count())/4
                 for j in range(16)] for i in range(16)],complex)
G = np.array([[math.sqrt(p),-p],[p,math.sqrt(p)]])
X = np.array([[0,1],[1,0]])
P = X@G
B = np.block([[I,Z0],[Z0,I]])
Nchecks=0
def near(a,b,eps,label):
    global Nchecks
    delta=np.linalg.norm(np.asarray(a)-np.asarray(b))
    assert delta<eps, (label,delta,eps)
    Nchecks+=1
def chk(x,label):
    global Nchecks
    assert bool(x),label
    Nchecks+=1

# Actual original Fourier creators 0,2,3,1; not one synthetic spin.
def creators():
    order=(0,2,3,1)
    out=[]
    for role in range(4):
        c=np.zeros((16,16),complex)
        previous=order[:order.index(role)]
        for bits in range(16):
            if not ((bits>>role)&1):
                c[bits|(1<<role),bits]=(-1)**sum((bits>>j)&1 for j in previous)
        out.append(c)
    return out

def native_julias(boost):
    cs=creators()
    gen=cs[0]@cs[1].conj().T+cs[1]@cs[0].conj().T
    u=I+np.sinh(boost)*gen+(np.cosh(boost)-1)*(gen@gen)
    near(u,old.expm(boost*gen),2e-13,"old native 16-grade boost")
    phases=[1j,1j,-1,-1j]
    result=[]
    for role,c in enumerate(cs):
        base=.6*c
        for flag in (0,1):
            x=(base@(u if role==1 else I)*phases[role]) if flag==0 else base
            L=old.root(I-x@x.conj().T)
            R=old.root(I-x.conj().T@x)
            J=np.block([[L,x],[x.conj().T,-R]])
            near(J,J.conj().T,5e-13,"full old native 2xCAR Julia H=H†")
            near(J@J,np.eye(32),8e-13,"old original Julia exact involution")
            result.append(J)
    return result

# COMPLETE seven native WORK qubits, label 8*k+4*dark+2*b+port.
# Unused dark=1 branch is the fixed old zero half of the output labels.
# arr shape: k 16, dark 2, JULIA b 2, Golden port 2, DATA 16.
def Q_apply(v,julias,inverse=False):
    a=np.asarray(v,complex).reshape(16,2,2,2,16).copy()
    def four_H():
        nonlocal a
        a=np.einsum('ki,idbpc->kdbpc',h16,a,optimize=True)
    def golden(mat):
        nonlocal a
        a=np.einsum('pq,kdbqc->kdbpc',mat,a,optimize=True)
    def tagged_CNOT():
        for k in range(16):
            if k&1:a[k]=a[k][:,[1,0],:,:]
    def native_mux():
        for k in range(16):
            J=julias[k//2]
            for d in range(2):
                for port in range(2):
                    arr=a[k,d,:,port,:].reshape(32)
                    a[k,d,:,port,:]=(J@arr).reshape(2,16)
    def signed_port():
        for k in range(16):
            if k&1:a[k,:,1,:,:]*=-1
            else:a[k]=a[k][:,[1,0],:,:]
            if k&2:a[k]*=-1
    if not inverse:
        four_H()
        tagged_CNOT()
        native_mux()
        signed_port()
        four_H()
        golden(P)
    else:
        golden(P.conj().T)
        four_H()
        signed_port()
        native_mux()
        tagged_CNOT()
        four_H()
    return a.reshape(128,16)

def make_reflector_kraus(julias):
    # Q|0work> full fine W, where original native H4+Julia has only
    # original 64 BRIGHT labels, native second Walsh duplication DARK.
    out=np.zeros((128,16,16),complex)
    for j in range(16):
        v=np.zeros((128,16),complex);v[0,j]=1
        w=Q_apply(v,julias)
        out[:,:,j]=w
    return out

def native_full_reflect(v,Ws):
    r=np.einsum('aji,aj->i',Ws.conj(),v,optimize=True)
    return v-2*np.einsum('aij,j->ai',Ws,r,optimize=True)

def main():
    chk(abs(math.tanh(theta/2)-1/9)<2e-15,
        "old original Lorentz role-1 r=1/9")
    julias=native_julias(theta)
    W=make_reflector_kraus(julias)
    nor=np.einsum('aji,ajk->ik',W.conj(),W,optimize=True)
    near(nor,I,2e-12,"ALL original 128 Julia/Walsh/Golden 7bit W†W")
    oldK,oldKjet=old.native(theta)
    chk(oldK.shape==(128,16,16),"original 128 Kraus ownership intact")
    chk(sum(np.linalg.norm(k)>1e-11 for k in oldK)==64,
        "old original 64 live 64 dark 7bit alphabet")
    checkmax=0.
    for alpha in range(128):
        kij=(I if alpha==0 else Z0)-2*W[alpha]@W[0].conj().T
        checkmax=max(checkmax,float(np.max(abs(kij-oldK[alpha]))))
        near(kij,oldK[alpha],3e-12,
             "EVERY actual original full128 Kraus is ONE Q zero-reflection column")
        if alpha&4:near(kij,Z0,1e-13,"original fifth duplicated Walsh bit dark")
    rng=np.random.default_rng(124)
    max_inverse=0.
    max_full_ref=0.
    for _ in range(12):
        v=rng.normal(size=(128,16))+1j*rng.normal(size=(128,16))
        q=Q_apply(v,julias)
        rein=Q_apply(q,julias,True)
        max_inverse=max(max_inverse,float(np.linalg.norm(rein-v)))
        near(rein,v,1e-10,"Q†Q=I on arbitrary ORIGINAL old work amplitude")
        b=Q_apply(v,julias,True);b[0]*=-1
        full=Q_apply(b,julias)
        should=native_full_reflect(v,W)
        max_full_ref=max(max_full_ref,float(np.linalg.norm(full-should)))
        near(full,should,1e-10,
             "actual full W reflection = Q sign0 Q† on ALL 128 work states")
    flag_amp=(5/8)**2
    native_flag_probability=(25/64)**2
    for _ in range(8):
        v=rng.normal(size=(128,16,2))+1j*rng.normal(size=(128,16,2))
        v/=np.linalg.norm(v)
        result=np.zeros_like(v)
        for right in range(2):
            b=(5/8)*Q_apply(v[:,:,right],julias,True)
            b[0]*=-1
            result[:,:,right]=(5/8)*Q_apply(b,julias)
        near(np.linalg.norm(result)**2,native_flag_probability,5e-13,
             "TWO honest uniform 25/64 herald flags => total 625/4096 on ANY DATA×oldRIGHT")
        direct=np.stack([native_full_reflect(v[:,:,r],W) for r in range(2)],axis=2)
        near(result,flag_amp*direct,1e-11,
             "Q†+ Q coherent full Julia original echo SUCCESS K=(25/64)U_native on arbitrary oldRIGHT entangled states")
    # Real first native source: every original Kα derivative must be from
    # exactly this ONE moving Julias[role1,base0], all seven other words fixed.
    step=1e-5
    for idx,jets in [(-1,native_julias(theta-step)),(1,native_julias(theta+step))]:
        wj=make_reflector_kraus(jets)
        kj=np.array([(I if k==0 else Z0)-2*wj[k]@wj[0].conj().T
                     for k in range(128)])
        if idx<0:km=kj
        else:kp=kj
    diff=(kp-km)/(2*step)
    for a in range(128):
        near(diff[a],oldKjet[a],3e-8,
             "native old 128 true proper-Lorentz Julia Sylvester first source from ONLY one boosted gate")
    print(__import__('json').dumps({
        "status":"PASS_ORIGINAL_FULL128_Q_GATE_WALSH_JULIA_GOLDEN_ECHO_TWO_FLAGS",
        "checks":Nchecks,
        "old_original_source":"d0_book_uniform_source_2026-10-21/check_uniform_book_source.py",
        "old_native_CAR16":16,
        "old_native_WORK_labels":128,
        "old_native_BRIGHT":64,
        "old_native_DARK":64,
        "golden_p":p,
        "original_r":"1/9",
        "mathematical_native_logic":{
            "Q":"H4 -> copy tag -> eight-way self-adjoint Julia -> tag conditional X/Z and base sign -> H4 -> original XGport",
            "old_Julia_branches_total":8,
            "old_Julia_branches_field_independent":7,
            "only_native_boosted_one_field_dependent":True,
            "old_full_Kraus":"U_native=Q*(I−2|0work><0work|)*Q†",
            "old_oldRIGHT_direct_gate_access_required":False,
            "heralded_Q_amplitude":"5/8",
            "heralded_U_amplitude":"25/64",
            "unconditional_two_herald_success":"625/4096",
            "mathematical_double_herald_success_probability":native_flag_probability,
            "additional_success_flag_first_source":0,
            "two_herald_Hadamard_slots":12,
            "old_Q_Hadamard_slots_2_Q":16,
            "total_simple_H_slots_excluding_factory":28,
            "old_Golden_signal_gate_calls":2,
            "old_real_boosted_Julia_calls":2,
            "other_conditional_native_permutation_sign_and_stage_costs_excluded_from_simple_gate_count":True,
            "max_original_K_matrix_error":checkmax,
            "max_full_U_reflection_error":max_full_ref,
            "max_inversion_error":max_inverse
        },
        "native_G0_coherent_controlled_boosted_Julia_physically_admitted":False,
        "native_factory_clock_full_price_known_for_this_compiled_scheme":False,
        "native_original_Book03_scene_Hodge_and_pathInfo_selected":False,
        "full42_GR_closed":False
    },indent=2))
if __name__=="__main__":
    main()
