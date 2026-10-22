#!/usr/bin/env python3
"""D0 #334: exact Golden-controlled SWAP, native n20 fine/three-atom source.
This checks a *conditional fixed finite tester*, NOT physical Book03 admission
or replacement of complete Cost−Info by purity/Renyi-2.
"""
import math
from itertools import product
import numpy as np

phi=(1+math.sqrt(5))/2
p=1/phi
G=np.array([[math.sqrt(p),-p],[p,math.sqrt(p)]])
N=10946; F20=6765; z=2**-20; n=20
L=4*p**3
r0=1-(1-z*L)*(1-z*L*(1+p**6))
a=2*N*p**23
checks=[]
def check(label,condition):
    if not condition:raise AssertionError(label)
    checks.append(label)

check('golden mixer unitary',np.linalg.norm(G.T@G-np.eye(2))<2e-15)
check('original p+p2=1',abs(p+p*p-1)<2e-15)
check('all original fine label probabilities sum to 1',abs(F20*p**21+N*(p**22+p**24+2*p**23)-1)<8e-15)
check('true 72441 labels',F20+6*N==72441)

# ONE Fredkin via two original CNOT and one original Toffoli on each data bit.
# Controls (s,u,v), with s the programme-ancilla. Circuit:
# CNOT(u->v); Toffoli(s,v->u); CNOT(u->v).
def fredkin_native(s,u,v):
    v ^= u
    u ^= s & v
    v ^= u
    return (s,u,v)
for s,u,v in product((0,1),repeat=3):
    check('two-CNOT one-Toffoli Fredkin gate '+str((s,u,v)),fredkin_native(s,u,v)==(s,v,u) if s else fredkin_native(s,u,v)==(s,u,v))

# A single 2-copy SWAP block with original G-CTRL_SWAP-G^{-1} on ancilla.
SWAP=np.zeros((4,4))
for u,v in product((0,1),repeat=2):
    SWAP[2*v+u,2*u+v]=1
U=np.kron(G.T,np.eye(4))@np.block([[np.eye(4),np.zeros((4,4))],[np.zeros((4,4)),SWAP]])@np.kron(G,np.eye(4))
check('two-copy Golden controlled SWAP exact unitary',np.linalg.norm(U.T@U-np.eye(8))<3e-15)

# General identity: p_out(1)=2p^3(1-Tr(rho sigma))
def swap_return(rho,sigma):
    rr=np.kron(rho,sigma)
    both=np.kron(np.array([[1.,0.],[0.,0.]]),rr)
    out=U@both@U.T
    return np.trace(out[4:,4:]).real
for r in (.00000185123958,.1,.25,.6,.9):
    for t in (.1,.4,.8):
        rho=np.diag((1-r,r));sig=np.diag((1-t,t))
        target=2*p**3*(1-(1-r)*(1-t)-r*t)
        check('general classical Golden SWAP target r/t',abs(swap_return(rho,sig)-target)<2e-15)

# Coherent history preparations have purity 1 and zero first source.
for r in (.00000185123958,.1,.37):
    psi=np.array((math.sqrt(1-r),math.sqrt(r)))
    full=np.outer(psi,psi)
    diag=np.diag((1-r,r))
    check('pure coherent global archive SWAP dark',abs(swap_return(full,full))<2e-15)
    check('same original pointer but nonzero decohered SWAP',abs(swap_return(diag,diag)-4*p**3*r*(1-r))<2e-15)

# Original full n20 fine measured code. Entirely unconditioned; every failure/overshoot paid.
def full_purity(rr):
    return F20*p**42 +N*(p**44+p**48) +2*N*p**46*((1-rr)**2+rr**2)
def coarse_purity(rr):
    return (1-a)**2+a*a*((1-rr)**2+rr**2)
def book_swap(q2):return 2*p**3*(1-q2)
full_source=8*p**49*N*(1-2*r0)
coarse_source=4*p**3*a*a*(1-2*r0)
check('true fine and coarse signals positive',book_swap(full_purity(r0))>0 and book_swap(coarse_purity(r0))>0)
check('coarse-to-fine source amplifies by exact 2F21',abs(coarse_source/full_source-2*N)<2e-10)
for d in (1e-4,1e-5,1e-6):
    full_fd=(book_swap(full_purity(r0+d))-book_swap(full_purity(r0-d)))/(2*d)
    coarse_fd=(book_swap(coarse_purity(r0+d))-book_swap(coarse_purity(r0-d)))/(2*d)
    check('analytic full first source finite difference',abs(full_fd-full_source)<1e-10)
    check('analytic coarse first source finite difference',abs(coarse_fd-coarse_source)<1e-9)

# General nonuniform site law: original n_z cancel against inverse-PF rho_z on common null.
# Synthetic integer distribution controls only the structural identity; native counts are not claimed enumerated here.
sitecounts=[N//256]*256
for j in range(N-sum(sitecounts)):
    sitecounts[j]+=1
check('synthetic structural count sums N',sum(sitecounts)==N)
ratios=[nz/(256*nz/N) for nz in sitecounts]
check('all 256 exact inverse-PF ratios are N/256',max(abs(q-N/256) for q in ratios)<1e-12)

# Whole-input fixed active Book cut P=|0><0| on ancilla: no field source.
# It is an OPERATOR relation, not a state-averaged detector probability.
Fswap=np.eye(4)-(p*np.eye(4)+p*p*SWAP)@(p*np.eye(4)+p*p*SWAP)
check('Book complement exact 2p3(I-SWAP)',np.linalg.norm(Fswap-2*p**3*(np.eye(4)-SWAP))<2e-15)
check('Book complement eigenvalues only 0 and 4p3',max(abs(x) for x in sorted(np.linalg.eigvalsh(Fswap))[:3])<2e-15 and abs(max(np.linalg.eigvalsh(Fswap))-4*p**3)<2e-15)
bookJ=-np.linalg.slogdet(np.eye(4)-z*Fswap)[1]
check('Book fixed-cut trace-log is a constant',abs(bookJ+math.log1p(-4*p**3*z))<4e-15)
# A natural PURE prepared pair |psi>⊗|psi> is SWAP symmetric and yields F=0.
for rr in (.00000185123958,.25,.7):
    psi=np.array([math.sqrt(1-rr),math.sqrt(rr)])
    psi2=np.kron(psi,psi)
    check('pure same-state pair lives in +SWAP sector',np.linalg.norm(SWAP@psi2-psi2)<1e-14)
    check('its prepared pure Book cut has zero complementary feedback',abs(psi2@Fswap@psi2)<1e-14)
# SAME full native readout and SAME Book base projector/value, different cut JETS.
# This is a mathematical valuation fork, not physically admitted two alternate laws.
chi=np.array([1.,0.])
def prepared_j(rr):
    psi=np.array([math.sqrt(1-rr),math.sqrt(rr)])
    prepared=np.kron(np.array([1.,0.]),np.kron(psi,chi))
    book_amp=prepared@U@prepared
    return -math.log1p(-z*(1-book_amp**2)),book_amp
common,amp=prepared_j(r0)
book_amp_expected=p+p*p*(1-r0)
check('same native Golden 8x8 cut amplitude',abs(amp-book_amp_expected)<2e-15)
check('fixed prepared rank-one cut same base value',abs(common+math.log1p(-z*(1-book_amp_expected**2)))<2e-15)
moving_jet=2*z*p*p*book_amp_expected/(1-z*(1-book_amp_expected**2))
check('strictly nonzero moving-cut physical SOURCE candidate',moving_jet>0)
for step in (1e-7,1e-8,1e-9):
    finite=(prepared_j(r0+step)[0]-prepared_j(r0-step)[0])/(2*step)
    check('same-base different first Book source',abs(finite-moving_jet)<2e-12)
for rr in (r0,.1,.7):
    psi=np.array([math.sqrt(1-rr),math.sqrt(rr)])
    qinput=np.kron(psi,chi)
    state=np.kron(np.array([1.,0.]),qinput)
    out=U@state
    measured_flag=float(out[4:]@out[4:])
    check('single same-circuit Born source unaffected by Book cut',abs(measured_flag-2*p**3*rr)<2e-15)

# Strict absence of exact full entropy-source reconstruction by *any finite* polynomial of swap moments:
# h'(r)=log((1-r)/r)/log(phi) diverges as r->0; a finite sum of spectral
# moments has bounded polynomial derivative. This is an analytic proof,
# not inferred from a finite sample.
assert 0<r0<1
print({
 'status':'PASS', 'controls':len(checks),'r_native':r0,
 'original_fine_outcomes':F20+6*N, 'original_ready_probability':a,
 'one_full_fine_swap_click':book_swap(full_purity(r0)),
 'one_three_atom_swap_click':book_swap(coarse_purity(r0)),
 'full_derivative':full_source, 'three_atom_derivative':coarse_source,
 'source_gain_exact':int(round(coarse_source/full_source)),
 'source_asymptotic':'full fine ~p^n per scalar report variation, active fixed-ready ~O(1)',
 'actual_native_admission':'not proved; two fresh copies + global routing, full clock, Book03 Info/P_N/H+J+R open'
})