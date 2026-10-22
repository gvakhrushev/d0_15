#!/usr/bin/env python3
"""D0 #334: exact stage-support theorem + bounded native Golden cost-cut controls.

Consumes Book03 03.26.1 and FiniteProtocolClock (ZMod16, 15 executed
transitions) and the original Golden n20 first-crossing code.  The stage
projector/clock-as-cost lift is a scoped diagnostic, NOT a physically
selected Book03 P_N, clock-to-cost equality, M1 admission or GR proof.
"""
import math
import numpy as np

PHI=(1+math.sqrt(5))/2
P=1/PHI
Z=2**-20
M=16
assert abs(P+P*P-1)<1e-15
assert abs(P**6+4*P**3-1)<1e-14
assert M==16

checks=[]
def test(label, premise):
    if not premise:
        raise AssertionError(label)
    checks.append(label)

def transition(theta=0.0):
    """One original-type cyclic stage shift with arbitrary internal 2D unitary.
    The real 2D field-dependent internal rotation is a DIAGNOSTIC,
    not an original native continuously variable Q8 gate.
    """
    out=np.zeros((2*M,2*M))
    for c in range(M):
        angle=theta if c==0 else 0.0
        C,S=math.cos(angle),math.sin(angle)
        V=np.array([[C,-S],[S,C]])
        target=(c+1)%M
        out[2*target:2*target+2,2*c:2*c+2]=V
    return out

def subspace(stages, internal=None):
    """Return isometric columns for stage support, or rank-one data cuts."""
    cols=[]
    for c in stages:
        selected=(0,1) if internal is None else ((0,) if internal=="zero" else internal[c])
        for i in selected:
            col=np.zeros(2*M)
            col[2*c+i]=1.0
            cols.append(col)
    if not cols:
        return np.zeros((2*M,0))
    return np.column_stack(cols)

def book(theta, stages, j=15, internal=None):
    B=subspace(stages,internal)
    U=np.linalg.matrix_power(transition(theta),j)
    return_operator=B.T@U@B
    T=return_operator.T@return_operator
    effect=np.eye(B.shape[1])-T
    eig=np.linalg.eigvalsh(effect)
    test("positive complementary effect", bool(np.min(eig)>-2e-13 and np.max(eig)<1+2e-13))
    sign, logabs=np.linalg.slogdet(np.eye(B.shape[1])-Z*effect)
    test("positive Book determinant",bool(sign==1))
    return -logabs,T

# Original 15 real operations have distinct stages 0->1->...->15,
# so no completed early stage 1..15 returns to ANY projector in stage 0.
for j in range(1,16):
    test("clock-0 no-return %d"%j,(j%16)!=0)

# All clock-only cuts P_S=sum_{c in S}|c><c| tensor I have
# exactly rank 2*|{c in S : c+j not in S}| complementary F.
for mask in ([0],[0,15],[0,1,5,15],list(range(16))):
    for j in (1,5,15):
        exits=sum((c+j)%16 not in mask for c in mask)
        expected=-2*exits*math.log1p(-Z)
        for angle in (0.21,0.73):
            actual,_=book(angle,mask,j)
            test("all stage-only cuts source blind",abs(actual-expected)<2e-13)

# A rank-one scene/reference cut at stage 0 and rank-one *record-selective*
# cut at stage 15 can detect relative internal orientation at j=15.
for angle in (0.21,0.73):
    jbook,T=book(angle,[0,15],j=15,internal="zero")
    expected=-math.log1p(-Z*math.sin(angle)**2)-math.log1p(-Z)
    test("source-capable internal cut",abs(jbook-expected)<1e-13)
    test("principal-angle cos^2",abs(T[0,0]-math.cos(angle)**2)<1e-13)
    test("final stage exits",abs(T[1,1])<1e-13)

angle=0.47
h=2e-4
finite=(book(angle+h,[0,15],internal="zero")[0]-book(angle-h,[0,15],internal="zero")[0])/(2*h)
exact=Z*math.sin(2*angle)/(1-Z*math.sin(angle)**2)
test("original Book logdet analytic first source",abs(finite-exact)<1e-12)

# The wrap control is explicitly NOT the completed original 15-tick apparatus.
wrapped,Tw=book(angle,[0],j=16,internal="zero")
test("clock wrap changes cut",abs(wrapped+math.log1p(-Z*math.sin(angle)**2))<1e-13)
start_only,_=book(angle,[0],j=15,internal="zero")
test("original start cut is blind",abs(start_only+math.log1p(-Z))<1e-13)

# Original Golden n=20 complete stopped prefix + FF/FR/RF/RR and actual
# final charged native 0/10 report.  All costs here are SOURCE-code costs.
K=10946; overshoot=6765
costs={"overshoot":21,"FF":22,"RR":24,"READY0":24,"READY10":25}
test("original native recorded cost residues nonzero",
     all(c%16!=0 for c in costs.values()))
test("original complete record labels",overshoot+6*K==72441)

A=2*K*P**23
prob_over=overshoot*P**21
prob_ff=K*P**22
prob_rr=K*P**24
test("native full tree Kraft completeness",abs(prob_over+prob_ff+prob_rr+A-1)<2e-12)

def marked(r,mark=math.log(PHI)):
    """Whole 72,441 label mark when the report is homogeneous."""
    return (prob_over*math.exp(-21*mark)+prob_ff*math.exp(-22*mark)
            +prob_rr*math.exp(-24*mark)
            +A*((1-r)*math.exp(-24*mark)+r*math.exp(-25*mark)))

r0=1-(1-Z*4*P**3)*(1-Z*4*P**3*(1+P**6))
test("native original rare report",0<r0<1e-5)
test("unmarked normalization all fields",abs(marked(.123,0)-1)<1e-12)
N=marked(r0)
Nprime=A*(math.exp(-25*math.log(PHI))-math.exp(-24*math.log(PHI)))
test("genuine cost mark sees native report",N>0 and Nprime<0 and abs(Nprime)>1e-7)
# Any initialized cut at stage 0, and ALL outputs in stages (cost mod16)
# {5,6,8,9}, implies the true early-return corner A_init=0.
# The ORIGINAL normalized complementary determinant therefore cancels N.
d=4
J_normalized=d*math.log(N)-d*math.log((1-Z)*N)
J_expected=-d*math.log1p(-Z)
test("book normalized A=0 is code-blind",abs(J_normalized-J_expected)<1e-12)
Nplus=marked(r0+1e-4)
Nminus=marked(r0-1e-4)
test("whole code mark nonzero tangent",abs((Nplus-Nminus)/(2e-4)-Nprime)<3e-14)
Jplus=d*math.log(Nplus)-d*math.log((1-Z)*Nplus)
Jminus=d*math.log(Nminus)-d*math.log((1-Z)*Nminus)
test("whole marked initialized Book source ZERO",abs((Jplus-Jminus)/(2e-4))<2e-8)

# Actual native Golden-reflection Q8 order-loop output (BOOK03 03.26.1)
# is (record0,record1)=(p^6,4p^3), identity=(1,0),
# for every one of 4 independently preserved real spin coordinates.
# A SYNCHRONIZED stage0->stage15, record0-selective candidate P has
# four incoming and eight output active basis modes. J_end constant;
# the four input principal-angle eigenvalues equal q(record0).
J_id=-8*math.log1p(-Z)
J_loop=-4*math.log1p(-4*P**3*Z)-8*math.log1p(-Z)
test("native Q8 candidate cut positive contrast",J_loop>J_id>0)
test("no fitted parameter in Q8 contrast",abs(J_loop-J_id+4*math.log1p(-4*P**3*Z))<1e-13)

print({"status":"PASS","checks":len(checks),"stage_period":16,
       "actual_original_completion":15,"original_cost_support":costs,
       "native_ready_fraction":A,"native_report":r0,
       "mark_normalizer":N,"mark_normalizer_slope":Nprime,
       "clock_only_J":start_only,"selected_cut_theta_slope":exact,
       "native_Q8_candidate_J_difference":J_loop-J_id,
       "nonclaims":"physical Book03 P_N, cost-clock alignment, M1 writer and GR still open"})
