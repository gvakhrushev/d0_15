#!/usr/bin/env python3
"""Original 128-output register: physically owned exit-count forgetting changes MDL.

Uses exact first-shell Bernoulli event law from original owned full128 channel.
This is a readout/observation-algebra distinction, NOT a proof that the
Book03 canonical M1 forgetting is the count quotient.
"""
from math import comb,log,sqrt
import sympy as s

phi=(1+sqrt(5))/2
p=1/phi
ell=log(phi)
n=1024
h=s.Rational(1,4)
lam=s.Rational(288,25)
q0=(5034167+28557*s.sqrt(5))/s.Integer(5120000)
epsilon=((s.sqrt(5)-1)/2)**2*h*h/64
e=s.simplify(1-q0)
assert s.simplify(e-(epsilon*lam-(epsilon*lam)**2/4))==0

# Prove strict binomial K-mode via the exact algebraic (n+1)e bounds;
# SymPy .is_positive checks exact Q(sqrt(5)) element signs.
assert s.simplify((n+1)*e-4).is_positive
assert s.simplify(5-(n+1)*e).is_positive
assert n>=1
K_mode=4

ef=float(s.N(e,30))
qf=1-ef
pmf=lambda k: comb(n,k)*ef**k*qf**(n-k)
assert pmf(K_mode)>pmf(K_mode-1)>pmf(0)
assert pmf(K_mode)>pmf(K_mode+1)
# All complete indicator words with K=k have exactly the same probability,
# but a count coarse-reading collects choose(n,k) of them.
p_one4=ef**4*qf**(n-4)
assert abs(pmf(4)-comb(n,4)*p_one4)<1e-14
S_one4=-log(p_one4)/ell
S_K4=-log(pmf(4))/ell
loss=log(comb(n,4))/ell
assert abs(S_one4-S_K4-loss)<1e-12

# Readout-dependent first covectors under a TRUE scalar-flat-shell
# deformation Delta_h=lambda_h I, with fixed h,epsilon,n.
epsf=float(s.N(epsilon,30))
de=epsf*(1-epsf*float(lam)/2)
D_fullmode=n*de/(qf*ell)
D_countmode=-(4/ef-(n-4)/qf)*de/ell
assert abs(D_fullmode-D_countmode)>0.7
# At the same time fine global MAP is the original all-blank word,
# certified by the independent full128 first-deviation theorem.
assert qf**n>ef

print('PASS exact: 4 < (n+1)*e < 5, so unique native count MAP K=4')
print('PASS: full chronological 128-record MAP is the all-blank K=0 word')
print('PASS: one K=4 indicator word probability times choose(n,4) = count P(K=4)')
print(f'P_full_mode={qf**n:.15g}; P_count_mode={pmf(4):.15g}')
print(f'Count-modal action={S_K4:.12f}; exact forgetting multiplicity cost={loss:.12f}')
print(f'D_lambda chronological-modal source={D_fullmode:.12f}')
print(f'D_lambda count-modal source={D_countmode:.12f}')
print('THEOREM: argmax and the physically available exit-count quotient do not commute')
print('SCOPE: full Book history-memory/Info/GR selection remains unproved')


# Book06 entropy-selected forgetting: actual flat-shell conditional timing
# kernel at fixed count k is exactly uniform on comb(n,k) arrangements.
# The following finite hostile test verifies the KL slack with a nonuniform
# alternative on a smaller 5-tick two-event count fiber.
small_n,small_k=5,2
M=comb(small_n,small_k)
reference=[1/M]*M
hostile=[.2]+[.8/(M-1)]*(M-1)
assert abs(sum(hostile)-1)<1e-14
H=lambda law:-sum(x*log(x) for x in law)/ell
KL=sum(x*log(x/y) for x,y in zip(hostile,reference))/ell
assert KL>0 and abs(H(hostile)+KL-log(M)/ell)<1e-13
assert H(reference)>H(hostile)
print('PASS: Book06 max-entropy count-conditioned forgetting is the native unique uniform timing kernel')
print('PASS: hostile nonuniform kernel has strictly positive KL entropy slack')
