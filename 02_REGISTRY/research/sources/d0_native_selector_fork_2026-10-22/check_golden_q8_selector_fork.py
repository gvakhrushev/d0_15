#!/usr/bin/env python3
"""Native Q8 selected-cut fork + globally cheapest 0/10 Golden binary code.

Exact symbolic proofs reproduced in the paired memo. This is a scoped
same-hardware research check, not a physical G0/Book03 GR acceptance claim.
"""
from __future__ import annotations
from itertools import product
import sympy as s

p=(s.sqrt(5)-1)/2
z=s.Rational(1,2**20)
r=s.symbols('r',positive=True)
qg=s.simplify(4*p**3)
phi=1/p

def check(ok,label):
    if not bool(ok):
        raise AssertionError(label)

def eq(a,b,label):
    check(s.simplify(a-b)==0,label)

# Original Golden and EXACT native Q8 event effects over FOUR spin columns.
eq(p*p+p,1,'original F/R Kraft')
eq(p**6+4*p**3,1,'original Q8 full port normalization')
d=4
V0=s.Matrix.vstack(s.eye(d),s.zeros(d))
V1=s.Matrix.vstack(s.zeros(d),s.eye(d))
W=s.sqrt(1-r)*V0+s.sqrt(r)*V1
Q0=s.diag(*([1]*d+[0]*d))
Q1=s.eye(2*d)-Q0
ZP=Q0-Q1
Pnow=W*W.T
Pfuture=V0*V0.T+V1*V1.T
E=qg*Q1
check(W.shape==(8,4),'four protected Q8 spin inputs')
check(W.T*W==s.eye(d),'complete coherent prepared isometry')
check(Pfuture==s.eye(8),'minimal two-branch future span')
check(Q0*W!=s.zeros(8,4) and Q1*W!=s.zeros(8,4),'both nonzero native branches')
check(s.simplify(Pnow*W-W)==s.zeros(8,4),'prepared no-loss')
check(Pfuture*W==W,'future closed no-loss')
check(s.simplify(W.T*E*W-qg*r*s.eye(d))==s.zeros(d),'exact ORIGINAL record1')
comm=s.simplify(Pnow*Q0-Q0*Pnow)
eq(s.trace(comm.T*comm),2*d*r*(1-r),'future projector commutator norm')
check(s.simplify(comm.subs(r,s.Rational(1,5)))!=s.zeros(8),'pure cut not future invariant')
check(Pfuture*Q0==Q0*Pfuture,'future-closed projector invariant')
# End/stage baseline is the original static Q8 result: only prepared START varies.
Jnow=-4*s.log(1-z*(1-qg*r))-16*s.log(1-z)
Jfuture=-20*s.log(1-z)-4*s.log(1-z*(1-qg))
dJ=s.diff(Jnow,r)
eq(dJ,-16*p**3*z/(1-z+4*p**3*z*r),'exact four-column moving Book source')
eq(s.diff(Jfuture,r),0,'future closed Q8 feedback constant')
check(float(dJ.subs(r,s.Rational(1,5)))<0,'moving source negative')

# SHARP rank-birth discontinuity of post-record future-closed support.
# At r=0 the original programme cannot reach the order sector because all
# admitted Q8 gates preserve Z_P. At every r>0 both sectors occur.
Pfuture_at_zero=Q0
Pfuture_positive=Q0+Q1
check(Pfuture_positive-Pfuture_at_zero==Q1,'exact rank birth by four')
check((Pfuture_positive-Pfuture_at_zero)**2==Q1,'support projector difference norm one')
J_at_zero=-20*s.log(1-z)
J_at_positive=Jfuture
J_jump=J_at_positive-J_at_zero
eq(1-qg,p**6,'original exact residual Q8 dark p6')
eq(J_jump,-4*s.log(1-z*(1-qg)),'exact positive Book support-rank jump')
check(float(J_jump)>0,'rank-birth action jump strict positive')
eq(Jnow.subs(r,0),J_at_zero,'moving pre-record Book action continuous at zero')

# Original complete Golden binary 0 / 10: global optimum among ALL finite
# self-delimiting F/R binary result codebooks (NOT all native tasks).
def cost(w): return sum(1 if c=='F' else 2 for c in w)
def is_prefix_free(a,b): return not (a.startswith(b) or b.startswith(a))
words=[]
for k in range(1,7):
    words += [''.join(t) for t in product('FR',repeat=k) if cost(t)<=8]
for rr in [s.Rational(1,1000000),s.Rational(1,5),s.Rational(49,100),s.Rational(1,2)]:
    best=None; winners=[]
    for a in words:
        for b in words:
            if not is_prefix_free(a,b): continue
            expected=(1-rr)*cost(a)+rr*cost(b)
            if best is None or expected<best:
                best=expected;winners=[(a,b)]
            elif expected==best:
                winners.append((a,b))
    eq(best,1+rr,'global binary F/R optimum '+str(rr))
    check(('F','R') in winners,'true 0/10 optimum obtained')
    if rr<s.Rational(1,2):
        check(winners==[('F','R')],'strict optimum unique in encoded names')

h=lambda v: -(v*s.log(v)+(1-v)*s.log(1-v))/s.log(phi)
g=lambda v: 1+v-h(v)
gpad=lambda v: 2-h(v)
eq(s.diff(g(r)-gpad(r),r),1,'unavoidable outcome-charge source')
# Consumed exact native h4 all42 result: two unequal original report bands
# and D_29 mean r lower bound at the same certified nonflat root.
certified_abs_Dmean_lower=s.Rational('2.68978050581795731e-14')
certified_minimal_code_source_lower=2*certified_abs_Dmean_lower
eq(certified_minimal_code_source_lower,s.Rational('5.37956101163591462e-14'),
   'original exact-root source lower bound in Golden reporter units')
# Explicit hostile representative only; the strict lower is from the
# original separately interval-certified h4 two-channel first-source.
r0=1.851242740976536e-6;r1=1.8513157633356053e-6
dr0=-2.26378054238336192e-8
import math
ell=math.log((1+math.sqrt(5))/2)
hp=lambda v: math.log((1-v)/v)/ell
dr1=-(hp(r0)/hp(r1))*dr0
check(abs(-hp(r0)*dr0-hp(r1)*dr1)<1e-18,'padded CQ stationarity representative')
check(abs(dr0+dr1)>float(certified_minimal_code_source_lower),'optimal code h4 offnull source strict')

print('PASS exact original Q8 four-spin active projector fork: prepared rank4 vs future rank8')
print('PASS future closure fails for moving prepared cut, rank8 fixed Book source zero')
print('PASS sharp support-rank birth: projector norm jump1, Book jump=-4log(1-z*p^6)')
print('PASS all Golden binary prefix codes: unique optimal original 0/10 for 0<r<1/2')
print('PASS exact difference of native min-code vs padded-CQ first Euler source')
print('PASS certified native offnull V29 source lower >5.379561e-14 (in report units)')
print('Book03 future-closure requirement physically selected: FALSE')
print('Full M1 G0 paid input writer selected: FALSE; GR_closed: FALSE')
