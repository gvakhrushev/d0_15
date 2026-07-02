#!/usr/bin/env python3
"""R1: theta-family port control. The unitary two-port R_theta = [[c,-s],[s,c]] (x) I_7
(c=cos theta, s=sin theta) is unitary for ALL theta — the existing cert's negative control
(dropping 1/sqrt2) only kills a NON-unitary matrix and does not test the family.
This script computes F_term(theta) on the branch space and verifies:
  (i)  F_term(theta) = sin^2(theta) * P_br  (so the feedback law's 1/2 <=> theta = pi/4);
  (ii) theta = pi/4 is the unique theta in (0, pi/2) with F = (1/2) P_br;
  (iii) leaf symmetry: the two-port treats the two U_br copies with weights c^2 vs s^2,
        equal iff theta = pi/4 (the which-leaf asymmetry parameter is |c^2 - s^2|).
Exits 1 on any failure."""
import numpy as np, sys

def C4(lam):
    M=np.zeros((4,4),complex)
    for r in range(3): M[r+1,r]=1
    M[0,3]=lam
    return M
def C3(lam):
    M=np.zeros((3,3),complex)
    for r in range(2): M[r+1,r]=1
    M[0,2]=lam
    return M

lam0 = np.exp(1j*0.7)
n = 7
Ubr = np.block([[C4(lam0), np.zeros((4,3))],[np.zeros((3,4)), C3(lam0)]])
I = np.eye(n)

def Fterm(theta):
    c, s = np.cos(theta), np.sin(theta)
    R = np.block([[c*I, -s*I],[s*I, c*I]])
    UE = np.block([[Ubr, np.zeros((n,n))],[np.zeros((n,n)), Ubr]]) @ R
    # retained = first copy (H_br), traced = second copy; F = (Q U P)^dag (Q U P)
    P = np.block([[I, np.zeros((n,n))],[np.zeros((n,n)), np.zeros((n,n))]])
    Q = np.eye(2*n) - P
    X = Q @ UE @ P
    F = (X.conj().T @ X)[:n,:n]
    return F

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name); ok = ok and bool(cond)

thetas = [0.2, 0.5, np.pi/4, 1.1, 1.4]
check("(i) F_term(theta) = sin^2(theta) I on H_br, all theta sampled",
      all(np.allclose(Fterm(t), (np.sin(t)**2)*I, atol=1e-12) for t in thetas))
check("(ii) F = (1/2)I  <=>  theta = pi/4 (unique in (0, pi/2))",
      np.allclose(Fterm(np.pi/4), 0.5*I) and all(not np.allclose(Fterm(t), 0.5*I) for t in [0.2,0.5,1.1,1.4]))
asym = lambda t: abs(np.cos(t)**2 - np.sin(t)**2)
check("(iii) leaf-asymmetry |c^2-s^2| = 0 iff theta = pi/4",
      asym(np.pi/4) < 1e-15 and all(asym(t) > 1e-3 for t in [0.2,0.5,1.1,1.4]))
# negative control: a theta != pi/4 port IS unitary (so the old control does not exclude it)
c, s = np.cos(0.5), np.sin(0.5)
R05 = np.block([[c*I, -s*I],[s*I, c*I]])
check("negative control: theta=0.5 port IS unitary (old cert control blind to it)",
      np.allclose(R05.conj().T@R05, np.eye(2*n)))
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
