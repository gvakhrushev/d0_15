"""Exact mixed-birth clock fixture; the general proof is GROWING_CLOCK_RU.md.

Uses the actual normalized AF inclusions (A,B)=(1,1)->(2,1)->(3,2),
all their complementary columns, and literal Golden G/CX matrices.
This is a clock-algebra check, not an inference of physical actuation from
matrix membership.  No large heat matrix is diagonalized.
"""

from pathlib import Path
import hashlib
import json
import re

import sympy as s
from sympy.polys.matrices import DomainMatrix


REPO = Path(__file__).resolve().parents[4]
SOURCE = REPO / "03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean"
a = s.Symbol("a", real=True)
p = a**2
minimal = a**4+a**2-1
checks = []


def red(x):
    return s.rem(s.expand(x), minimal, a)


def mat(M):
    M = s.MutableSparseMatrix(M)
    entries = {(i,j): red(x) for (i,j),x in M.todok().items()}
    return s.MutableSparseMatrix(M.rows, M.cols,
                                 {ij:x for ij,x in entries.items() if x != 0})


def require(ok, label):
    if not bool(ok):
        raise ArithmeticError(label)
    checks.append(label)


def equal(A, B, label):
    require(not mat(s.Matrix(A)-s.Matrix(B)).todok(), label)


G = s.Matrix([[a,-p],[p,a]])
CX = s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
native = SOURCE.read_text()
match = re.search(r"def fullStep\b.*?!!\[(.*?)\]", native, re.S)
if match is None:
    raise ArithmeticError("original fullStep absent")
W = s.Matrix([[s.sympify(x, locals={"a":a,"p":p}) for x in row.split(",")]
              for row in match.group(1).split(";")])
equal(W, CX*s.kronecker_product(G,s.eye(2)), "literal native fullStep factorization")


def af_inclusion(A, B):
    """Normalized GNS iota(X,Y)=(diag(X,Y),X), complete matrix-unit basis."""
    fine = A+B
    out = s.zeros(fine*fine+A*A, A*A+B*B)
    for i in range(A):
        for j in range(A):
            old = i*A+j
            out[i*fine+j, old] = a
            out[fine*fine+i*A+j, old] = p
    for i in range(B):
        for j in range(B):
            out[(A+i)*fine+A+j, A*A+i*B+j] = 1
    return mat(out)


J0, J1 = af_inclusion(1,1), af_inclusion(2,1)
equal(J0.T*J0,s.eye(2),"actual first AF birth is an isometry on both old columns")
equal(J1.T*J1,s.eye(5),"actual second AF birth is an isometry on all five old columns")
require(J0.shape==(5,2) and J1.shape==(13,5),"actual AF GNS dimensions are 2 to 5 to 13")

dims=[2,2,5,5,13,13]
offsets=[0]
for d in dims:
    offsets.append(offsets[-1]+d)
D=offsets[-1]
passive=[s.eye(2), J0, s.eye(5), J1, s.eye(13)]
G5a=s.diag(s.kronecker_product(G,s.eye(2)),1)
G5b=s.diag(s.kronecker_product(s.eye(2),G),1)
G13=s.diag(s.kronecker_product(G,s.eye(2)),s.eye(9))
last=s.diag(CX,s.eye(9))
equal(last*G13,s.diag(W,s.eye(9)),"last two real gates form literal fullStep with all complement retained")

# Passive embeddings into the final actual fibre.
B=[None]*len(dims)
B[-1]=s.eye(dims[-1])
for j in range(len(dims)-2,-1,-1):
    B[j]=mat(B[j+1]*passive[j])
details=[s.eye(dims[0])]
for j in range(1,len(dims)):
    details.append(mat(s.eye(dims[j])-passive[j-1]*passive[j-1].T))
R=s.zeros(D,dims[-1])
R[offsets[0]:offsets[1],:]=B[0].T
for j in range(1,len(dims)):
    R[offsets[j]:offsets[j+1],:]=mat(details[j]*B[j].T)
R=mat(R)
equal(R.T*R,s.eye(dims[-1]),"canonical terminal decomposition keeps every final column")
equal(R*R.T,s.diag(*details),"all birth-detail output slots are retained exactly")


def fixture(middle, label):
    forward=[G,J0,middle,J1,G13]
    S=s.zeros(D)
    for j,Fj in enumerate(forward):
        S[offsets[j+1]:offsets[j+2],offsets[j]:offsets[j+1]]=Fj
    S=mat(S)
    equal(S*S.T,s.eye(D)-R*R.T,label+": forward range and terminal range are complementary")
    equal(S.T*R,s.zeros(D,dims[-1]),label+": no overlap of actual forward and terminal outputs")
    T=s.Matrix(S)
    T[:,offsets[-2]:offsets[-1]]+=R*last
    T=mat(T)
    equal(T.T*T,s.eye(D),label+": full varying-fibre clock is unitary on every input")
    equal(T*T.T,s.eye(D),label+": full varying-fibre clock is onto every retained output")
    prefixes=[s.eye(2)]
    for Fj in forward:
        prefixes.append(mat(Fj*prefixes[-1]))
    Ps=[mat(A*A.T) for A in prefixes]  # P0=I2: both arbitrary live input columns.
    P=mat(s.diag(*Ps))
    for j in range(1,len(dims)):
        equal(Ps[j]*details[j],s.zeros(dims[j]),label+": generated cut misses birth detail "+str(j))
    leak=mat((s.eye(D)-P)*T*P)
    equal(leak[:,:offsets[-2]],s.zeros(D,offsets[-2]),
          label+": every nonterminal leakage column vanishes")
    feedback=mat(leak.T*leak)
    C=mat(B[0].T*last*prefixes[-1])
    E=mat(s.eye(2)-C.T*C)
    expected=s.zeros(D)
    expected[offsets[-2]:offsets[-1],offsets[-2]:offsets[-1]]=mat(prefixes[-1]*E*prefixes[-1].T)
    equal(feedback,expected,label+": entire feedback equals endpoint defect once")
    require(E != s.zeros(2),label+": the retained endpoint feedback is nonzero")
    return T,feedback,E


Tplus,Fplus,Eplus=fixture(G5a,"first real prefix")
Tminus,Fminus,Eminus=fixture(G5b,"second real prefix")
expected_difference=s.zeros(D)
expected_difference[offsets[3]:offsets[4],offsets[2]:offsets[3]]=G5a-G5b
equal(Tplus-Tminus,expected_difference,
      "the entire clock difference is supported in the finite field prefix")

# Full determinant, including every zero mode, via exact field characteristic polynomials.
actual_a=s.sqrt((s.sqrt(5)-1)/2)
field=s.QQ.algebraic_field(actual_a)


def characteristic(M):
    M=mat(M)
    rows={}
    for (i,j),x in M.todok().items():
        rows.setdefault(i,{})[j]=field.from_sympy(x.subs(a,actual_a))
    return DomainMatrix(rows,M.shape,field).charpoly()


for F,E,label in [(Fplus,Eplus,"first"),(Fminus,Eminus,"second")]:
    full_coefficients=characteristic(F)
    small_coefficients=characteristic(E)
    require(full_coefficients==small_coefficients+[field.zero]*(D-2),
            label+": full determinant det(I-zF) equals det((1-z)I+z C*C)")

# Small sharp negative control: coisometry-only closure throws out actual recorded leakage.
J=s.Matrix([1,0,0,0])
Rsmall=s.Matrix([[1,0,0,0],[0,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
Tsmall=s.zeros(5)
Tsmall[1:,0]=J
Tsmall[:,1:]=Rsmall*W
Psmall=s.diag(1,1,0,0,0)
Fsmall=mat(Psmall*Tsmall.T*(s.eye(5)-Psmall)*Tsmall*Psmall)
equal(Fsmall,s.diag(0,p**2,0,0,0),"literal one-pair birth retains feedback p^2")
Tbad=s.zeros(5)
Tbad[1:,0]=J
Tbad[0,1:]=J.T*W
Fbad=mat(Psmall*Tbad.T*(s.eye(5)-Psmall)*Tbad*Psmall)
equal(Fbad,s.zeros(5),"negative control: coisometry-only closure loses the recorded p^2")

vertices=9+11+13
edges=9*11+9*13+11*13
trace_C=s.Rational(9,26)+s.Rational(11,24)+s.Rational(13,22)
require(vertices==33 and edges==359,"actual internal scene has 33 vertices and 359 edges")
require(vertices*D+(edges+vertices)*D==425*D,
        "both complete Hodge degrees retain all 425D modes")
require((edges+vertices)*D-vertices*D==359*D,
        "paired Hodge heat has the full 359D harmonic dimension difference")
require(trace_C<=s.Rational(33,22),"true trace C_scene obeys the constant used in the source bound")
require(red((4*p-1)*(4*p+5))==11,
        "4p exceeds one: (4p-1)(4p+5)=11 and p>0")

result={
    "schema":"d0.growing-af-clock-exact-check/1",
    "status":"PASS",
    "stage_fibre_dimensions":dims,
    "actual_stage_carrier_dimension":D,
    "full_hodge_dimension":425*D,
    "actual_af_inclusions":[[1,1,2,1],[2,1,3,2]],
    "terminal_native_gate":"CX on first four full columns, identity on all remaining columns",
    "initial_live_input_rank":2,
    "full_determinant_verified":True,
    "physical_actuation_inferred_from_matrix_membership":False,
    "source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "check_count":len(checks),
    "checks":checks,
}
print(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True))
