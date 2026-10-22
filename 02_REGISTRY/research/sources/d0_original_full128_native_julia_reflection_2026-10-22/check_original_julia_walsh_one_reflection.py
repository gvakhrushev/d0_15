#!/usr/bin/env python3
"""EXACT native full128 -> ONE selfadjoint Julia/Walsh/Golden reflection.

Reads the independently pinned ORIGINAL native CAR16/128 Kraus constructor,
then independently reconstructs each and ALL 128 Kraus columns from just
six output/address qubits (four word bits, one Julia b, one Golden port)
with a *zero* duplicate-Walsh bit. All 64 dark labels are tested, not
discarded from the original measurement alphabet.

Required conditions for a PHYSICAL compiler remain explicitly OPEN:
G0-admitted coherent controlled field-dependent Julia REFLECTIONS and their
native clock/factory costs, complete record work pre-measurement, paid MUX/
inverse, native controlled-zero ancilla sign. This exact Hilbert-space
factorization does NOT identify mandatory Book03 scene Hodge/Info or GR.

Native complex CAR16 r=tanh(theta/2)=1/9, theta=ln(5/4), nu=3/5,
phases (i,i,-1,-i), all actual 128 original matrix labels. This checker
does not change original K0, factor field, native Golden p, or oldRIGHT128.
"""
from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import math

import numpy as np
from scipy.linalg import expm


CHECKS = 0


def check(yes: bool, message: str) -> None:
    global CHECKS
    if not bool(yes):
        raise AssertionError(message)
    CHECKS += 1


def close(x, y, tol: float, message: str) -> None:
    check(np.linalg.norm(np.asarray(x)-np.asarray(y)) <= tol, message)


N = 16
ONE = np.eye(N, dtype=complex)
ZERO = np.zeros((N, N), dtype=complex)
P = (math.sqrt(5.0)-1.0)/2.0
ZETA = 2.0**-20
PHASES = (1j, 1j, -1.0, -1j)
THETA = math.log(5.0/4.0)
NU = 3.0/5.0


def root(matrix):
    hh = (matrix+matrix.conj().T)/2
    ee, vv = np.linalg.eigh(hh)
    check(float(ee.min())>0, "true native Julia root input has strictly positive spectrum")
    return (vv*np.sqrt(ee))@vv.conj().T


def creators() -> list[np.ndarray]:
    order = (0, 2, 3, 1)
    out = []
    for r in range(4):
        c = np.zeros((16, 16), dtype=complex)
        before = order[:order.index(r)]
        for bits in range(16):
            if not ((bits>>r)&1):
                c[bits|(1<<r), bits] = (-1)**sum((bits>>j)&1 for j in before)
        out.append(c)
    return out


def theta_native_native_words(theta: float):
    """Independent explicit CARS16 Julia word parents as in ORIGINAL native()."""
    cc = creators()
    g = cc[0]@cc[1].conj().T+cc[1]@cc[0].conj().T
    # These are ORIGINAL proper SO(1,3) CAR boost lifts. At the exact native
    # original r=1/9: sinh(theta)=9/40 and cosh(theta)-1=1/40.
    check(np.linalg.norm(g@g@g-g)<1e-13, "ORIGINAL CAR16 grade generator satisfies G^3=G")
    u = ONE+math.sinh(theta)*g+(math.cosh(theta)-1)*g@g
    check(np.linalg.norm(u-expm(theta*g))<2e-13, "actual proper boost is exponential of ORIGINAL CAR16 generator")
    words = []
    native_julia = []
    for role, c in enumerate(cc):
        base = NU*c
        x = base@(u if role==1 else ONE)*PHASES[role]
        L = root(ONE-x@x.conj().T)
        R = root(ONE-x.conj().T@x)
        L0 = root(ONE-base@base.conj().T)
        R0 = root(ONE-base.conj().T@base)
        words.extend(((x, L), (x.conj().T,R), (-base,-L0), (-base.conj().T,-R0)))
        native_julia.extend(((x,L,R),(base,L0,R0)))
    return words, native_julia


def original_rows_from_duplicated_32(words):
    repeated = [w for word in words for w in (word,word)]
    check(len(repeated)==32, "unchanged native original 32 repeated Julia word pairs")
    all_rows = []
    for label in range(32):
        signs = [(-1)**((label&j).bit_count()&1) for j in range(32)]
        for b in (0,1):
            all_rows.append(sum((signs[j]*repeated[j][b] for j in range(32)), ZERO.copy())/32)
    check(len(all_rows)==64, "original native Walsh 64 matrix rows")
    return all_rows


def original_native_128(rows):
    a = rows[0]
    all_k = []
    for j, nj in enumerate(rows):
        v = nj.conj().T@a
        all_k.extend(( (ONE if j==0 else ZERO)-2*P**2*v,
                       -2*P*math.sqrt(P)*v ))
    check(len(all_k)==128, "original unchanged 128 fine Kraus labels")
    return np.asarray(all_k)


def hermitian_julia(x, L, R):
    """TRUE ORIGINAL native Julia square roots, now as one involution."""
    J = np.block([[L,x],[x.conj().T,-R]])
    close(J, J.conj().T, 3e-12, "native Julia block is self-adjoint")
    close(J@J, np.eye(32), 5e-12, "native Julia block is its OWN inverse")
    return J


def new_six_bit_stinespring(theta):
    """Produce the exact W column from one native controlled Julia MUX.
    Original 32 Walsh WORDS are actually duplicated 16 pairs. H4 suffices;
    the old fifth Walsh bit is a permanent zero output label.
    """
    words, jblocks = theta_native_native_words(theta)
    old_rows = original_rows_from_duplicated_32(words)
    for lab in range(16):
        for b in (0,1):
            check(np.linalg.norm(old_rows[4*lab+2+b]) < 3e-14,
                  "original native 128 fine labels with odd duplicated Walsh parity EXACTLY DARK")

    # Original 16 native Julia-pair words obey ∑(w0 w0†+w1 w1†)=16 I.
    total_words = sum((left@left.conj().T+right@right.conj().T
                       for left, right in words), ZERO.copy())
    close(total_words, 16*ONE, 1e-11, "16 ORIGINAL full CAR16 pair completeness from native Julia identity")

    # PREP: four native Hadamards on k=(role 2b,baseflag 1b,tag 1b),
    # copy tag to Julia output bit, one controlled native selfadjoint
    # Julia block J_x; when tag=0 swap its output, when tag=1 Z its output.
    # The native -base/-base† words contribute one Z to baseflag.
    prep = np.zeros((16,2,16,16), dtype=complex)
    for k in range(16):
        role=k//4
        baseflag=(k//2)%2
        tag=k%2
        X,L,R = jblocks[2*role+baseflag]
        J=hermitian_julia(X,L,R)
        # The unitary J gate has columns:
        # tag0: [L, X†] (then output X => [X†,L]).
        # tag1: [X,-R] (then output Z => [X,R]).
        if tag==0:
            a,b=J[16:32,0:16],J[0:16,0:16]
        else:
            a,b=J[0:16,16:32],-J[16:32,16:32]
        sign=(-1)**baseflag
        prep[k,0],prep[k,1]=sign*a/4,sign*b/4
        close(a*sign, words[k][0].conj().T, 4e-12,
              "native controlled JULIA involution+known port gates generates FIRST original Julia word adjoint")
        close(b*sign, words[k][1].conj().T, 4e-12,
              "native controlled JULIA involution+known port gates generates SECOND original Julia word adjoint")

    # Exact Walsh H4 on 16 PREP words produces the 32 original BRIGHT
    # matrices n_(4*ell+b)†. No fabricated new basis or 5bit quotient.
    Wrow = np.zeros_like(prep)
    for ell in range(16):
        signs = [(-1)**((ell&k).bit_count()&1) for k in range(16)]
        Wrow[ell] = sum((signs[k]*prep[k] for k in range(16)),
                         np.zeros((2,16,16), dtype=complex))/4
        for b in (0,1):
            close(Wrow[ell,b],old_rows[4*ell+b].conj().T,4e-12,
                  "FOUR original Walsh Hadamards EXACTLY compile native original bright output row")

    TstarT=sum((Wrow[ell,b].conj().T@Wrow[ell,b]
                for ell in range(16) for b in (0,1)), ZERO.copy())
    close(TstarT,ONE,4e-12,"actual native 4bit Walsh plus Julia selective circuit is ONE DATA16 isometry")
    # Original Book03 Golden matrix on the independent last port;
    # X G |0> = p |0> + sqrt(p)|1>, exactly p²+p=1.
    Ggold=np.array([[math.sqrt(P),-P],[P,math.sqrt(P)]])
    Xport=np.array([[0,1],[1,0]])
    gport=Xport@Ggold[:,0]
    close(gport,np.array([P,math.sqrt(P)]),5e-14,
          "one unchanged Golden gate with a native X sets the EXACT original port vector")
    close(Ggold@Ggold.T,np.eye(2),5e-14,"original Golden port is a literal finite orthogonal gate")
    # Full old 7-bit alpha=8*ell+4*dark+2*b+port. dark=0 ALWAYS.
    WW=np.zeros((128,16,16),complex)
    for ell in range(16):
        for b in (0,1):
            for port in (0,1):
                WW[8*ell+2*b+port]=gport[port]*Wrow[ell,b]
    norm=sum((v.conj().T@v for v in WW),ZERO.copy())
    close(norm,ONE,4e-12,"SINGLE original Walsh/Julia/Golden W isometry on full original 128 fine labels")
    return words,old_rows,WW


def main():
    check(abs(math.tanh(THETA/2)-1/9)<3e-15,
          "REAL original native proper CAR16 r=tanh(theta/2)=1/9")
    words,rows,W = new_six_bit_stinespring(THETA)
    own_K=original_native_128(rows)

    original=Path(__file__).resolve().parent.parent / "d0_book_uniform_source_2026-10-21" / "check_uniform_book_source.py"
    check(original.is_file(), "original independent full128 Kraus owner source file exists unchanged")
    spec=importlib.util.spec_from_file_location("pinned_original_full128_owner",original)
    check(spec is not None and spec.loader is not None, "original native full128 owner import available")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    reference, reference_jet=mod.native(THETA)
    check(reference.shape==(128,16,16) and reference_jet.shape==(128,16,16),
          "original independent live native constructor has ALL 128 untouched CAR16 outcomes/jets")
    for a in range(128):
        close(reference[a],own_K[a],1e-12,
              "EVERY exact original CAR16 128 Kraus matrix vs independent existing owner")

    close(W[0].conj().T, P*rows[0], 4e-14,
          "true native W† prepared blank J = p*original A; no fitted completion")
    # THE single original Hilbert-space reflection I−2WW† has exactly
    # the original 128 forward Kraus columns; hence its inverse is itself.
    for alpha in range(128):
        actual=(ONE if alpha==0 else ZERO)-2*W[alpha]@W[0].conj().T
        close(actual,reference[alpha],1e-12,
              "ORIGINAL TRUE full128 Kα is column of ONE Julia/Walsh/Golden native Householder reflection")
    total=sum((k.conj().T@k for k in reference),ZERO.copy())
    close(total,ONE,4e-12,"complete ORIGINAL 128 Kraus nonpostselected normalization")
    check(sum(np.linalg.norm(v)>1e-12 for v in reference)==64,
          "EXACT original full128 has 64 BRIGHT labels")
    check(sum(np.linalg.norm(v)<1e-12 for v in reference)==64,
          "EXACT original full128 has 64 DARK duplicate-Walsh labels")
    for ell in range(16):
        for b in (0,1):
            for port in (0,1):
                dark=8*ell+4+2*b+port
                check(np.linalg.norm(reference[dark])<1e-13,
                      "original native full128 duplicate Walsh bit always zero independent of CAR input")

    # ACTUAL coherent reflection on random full work amplitudes (all 128
    # original possible fine labels). This independently checks U²=I,
    # U†=U without constructing a 2048×2048 matrix.
    rng=np.random.default_rng(1031)
    def Uref(vec):
        proj=sum((W[j].conj().T@vec[j] for j in range(128)),
                 np.zeros(16,complex))
        return vec-2*np.einsum('aij,j->ai',W,proj,optimize=True)
    for j in range(16):
        v=np.zeros((128,16),complex)
        v[0,j]=1
        uv=Uref(v)
        for alpha in range(128):
            close(uv[alpha],reference[alpha,:,j],2e-12,
                  "true ORIGINAL full Kraus column = physical signal reflection on every DATA basis")
        close(Uref(uv),v,5e-12,
              "FULL COMPLEX ORIGINAL 128 work+CAR16 native Householder is self-inverse")
    for _ in range(6):
        vec=rng.normal(size=(128,16))+1j*rng.normal(size=(128,16))
        va=Uref(vec)
        close(Uref(va),vec,4e-11,
              "arbitrary native field coherent DATA+full 128-register superposition reversed exactly")
        close(np.linalg.norm(va),np.linalg.norm(vec),1e-11,
              "native native signal reflection preserves complete unmeasured work norm")

    # Direct native first source. The exact operator identity gives
    # F_pre=I-(K0†K0) on the original natural PRE-tick input.
    B=reference[0]
    F=ONE-B.conj().T@B
    eig=np.linalg.eigvalsh((F+F.conj().T)/2)
    check(eig.min()>0 and eig.max()<1,
          "native original PRE-tick Book complement has 16 positive source eigenvalues")
    J_native=-128*np.log1p(-ZETA*eig).sum()
    close(J_native,0.000041014328465257154,2e-12,
          "SAME original full128 native oldRIGHT128 one-round Book F not new score")
    heatZ=16*128*128 -2*16*128+2*128*np.exp(-2*P**2*eig).sum()
    H_native=math.log(heatZ)/(2*P**2)
    close(H_native,16.33182036803625,2e-11,
          "TRUE original 262144 FULL 128-work×RIGHT Hodge trace with 258048 zero modes")
    for dir in (-1,+1):
        step=dir*2e-5
        testK,_=mod.native(THETA+step)
        if dir==-1:
            km=testK
        else:
            kp=testK
    jr=lambda kk:-128*np.log1p(-ZETA*np.linalg.eigvalsh(ONE-kk[0].conj().T@kk[0])).sum()
    Dtheta=(jr(kp)-jr(km))/(4e-5)
    Dr=Dtheta*2/(1-(1/9)**2)
    close(Dr,-0.000004746624673257693,1e-9,
          "native proper-Lorentz Book source from SAME original full128 direct gate and ENTIRE oldRIGHT")
    # Independent DIFFERENTIATION of new gate vs the original old K jet.
    km,_,wm=new_six_bit_stinespring(THETA-1e-5)
    kpwords,_,wp=new_six_bit_stinespring(THETA+1e-5)
    Kminus=[(ONE if a==0 else ZERO)-2*wm[a]@wm[0].conj().T for a in range(128)]
    Kplus=[(ONE if a==0 else ZERO)-2*wp[a]@wp[0].conj().T for a in range(128)]
    for alpha in range(128):
        source=(Kplus[alpha]-Kminus[alpha])/(2e-5)
        close(source,reference_jet[alpha],3e-8,
              "TRUE proper-boost first jet all128 from one native reflection equals original Julia Sylvester source")

    # Native exact circuit resources only as a conditional gate-interface.
    # Four H for one 16-address uniform selector, eight 3-bit controlled
    # Julia candidates (one applied coherently per branch), four H Walsh,
    # one Golden G + one X on last port; native conditional X/Z and
    # one multiplexor sign. Q† uses SAME selfadjoint Julia involutions.
    result={
      "status":"PASS_ORIGINAL_FULL128_ONE_JULIA_WALSH_GOLDEN_REFLECTION",
      "checks":CHECKS,
      "original_real_BOOST_r":"1/9",
      "original_theta":"ln(5/4)",
      "original_CAR16_dimension":16,
      "original_fine_Kraus_labels":128,
      "original_nonzero_bright_labels":64,
      "original_exact_dark_labels":64,
      "original_dark_parity_rule":"original alpha = 8*ell+4*dark+2*b+port; dark=1 always K_alpha=0",
      "original_native_16_Julia_word_pairs":16,
      "native_8_controlled_Julia_reflections":"role4 x boosted-or-base2; tag0/1 chooses original two Julia columns",
      "native_bright_register_qubits":6,
      "native_full_original_register_qubits":7,
      "Q_gate_compiler_conditional":"8 Hadamards+one original Golden+one coherent SELECT among 8 native Hermitian Julia involutions+controlled sign/X/Z gates",
      "original_full128_one_reflection":"U_native=Q*(I−2|0^6><0^6|)*(Q†), embedded with one dark parity zero",
      "original_native_inverse":"U_native†=U_native; no new inverse operator/moving spectrum",
      "original_oldRIGHT_required_in_compiler":False,
      "original_oldRIGHT_spectator":128,
      "original_n1_Book_feedback":J_native,
      "original_n1_full_paired_Hodge":H_native,
      "original_n1_real_Lorentz_Book_first_source":Dr,
      "physical_G0_native_coherently_controlled_Julia_gate_compiled":False,
      "physical_own_original_full128_Kraus_factory_ledger_compiled":False,
      "physical_Book03_selected_heat_Info_task":False,
      "original_all42_Einstein_stationarity_proven":False,
      "original_raw216_uniform_refinement_proven":False,
      "GR_closed":False,
    }
    print(json.dumps(result,indent=2))
    return result


if __name__=="__main__":
    main()
