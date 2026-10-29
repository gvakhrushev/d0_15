"""Exact original raw-cylinder realization identities and literal wire admission.

Checks actual G/CX matrices and oldRIGHT guard, canonical raw births,
all-column target transport, the true growing clock, and exact retention.
It does not emit a general GR compiler or assert exact finite stationarity.
"""

from pathlib import Path
import hashlib
import importlib.util
import json
import sys

import sympy as s


REPO=Path(__file__).resolve().parents[4]
NATIVE=REPO/"02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location("raw_cylinder_native_owner",NATIVE)
native=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=native
spec.loader.exec_module(native)
a=s.Symbol("a",real=True)
p=a*a
minimal=a**4+a*a-1
checks=[]


def red(x):
    return s.rem(s.expand(x),minimal,a)


def mat(M):
    return s.Matrix(M).applyfunc(red)


def require(ok,label):
    if not bool(ok):
        raise ArithmeticError(label)
    checks.append(label)


def equal(A,B,label):
    require(all(x==0 for x in mat(s.Matrix(A)-s.Matrix(B))),label)


def actual(M):
    return s.Matrix(M).subs(a,native.A)


G=s.Matrix([[a,-p],[p,a]])
v=s.Matrix([a,p])
e0=s.Matrix([1,0])
CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
W=CX*s.kronecker_product(G,s.eye(2))
equal(G.T*G,s.eye(2),"original Golden gate is orthogonal")
equal(G*e0,v,"canonical born vector is the original Golden column")
equal(v.T*v,s.ones(1),"the entire raw birth has unit norm")
require(native.exact_matrix_equal(actual(G),native.G_LOCAL),
        "Golden matrix agrees with the unchanged actual native owner")

# Literal wire typing: old wire zero is arbitrary protected input, new wire one live.
execution=native.Execution(2,(),(0,),(native.Gate("G",(1,)),))
native.validate_execution(execution,max_qubits=2,max_expanded_stages=1)
require(native.inventory(execution,max_qubits=2,max_expanded_stages=1).g_count==1,
        "retention is one actual admitted G on the newly born binary slot")
gate=native.gate_matrix(execution,execution.gates[0],max_qubits=2,max_expanded_stages=1)
require(native.exact_matrix_equal(gate,actual(s.kronecker_product(s.eye(2),G))),
        "the admitted retention gate acts on all four actual wire columns")
bad=native.Execution(2,(),(0,),(native.Gate("G",(0,)),))
rejected=False
try:
    native.validate_execution(bad,max_qubits=2,max_expanded_stages=1)
except native.DomainError as exc:
    rejected="immutable old_right" in str(exc)
require(rejected,"original validator rejects touching the sealed old RIGHT")

fullstep_execution=native.Execution(3,(),(0,),
    (native.Gate("G",(1,)),native.Gate("CX",(1,2))))
native.validate_execution(fullstep_execution,max_qubits=3,max_expanded_stages=2)
inv=native.inventory(fullstep_execution,max_qubits=3,max_expanded_stages=2)
require(inv.g_count==1 and inv.cx_count==1,
        "fullStep-only variant has the literal admitted two-stage G/CX inventory")
fullstep_actual=native.gate_matrix(fullstep_execution,fullstep_execution.gates[1],
    max_qubits=3,max_expanded_stages=2)*native.gate_matrix(
    fullstep_execution,fullstep_execution.gates[0],max_qubits=3,max_expanded_stages=2)
require(native.exact_matrix_equal(fullstep_actual,
    actual(s.kronecker_product(s.eye(2),W))),
    "literal fullStep acts on all eight columns and preserves the actual old RIGHT")

J=s.kronecker_product(s.eye(2),v)
newG=s.kronecker_product(s.eye(2),G)
equal(J.T*J,s.eye(2),"canonical raw birth preserves both arbitrary old input columns")
for i in range(2):
    for j in range(2):
        E=s.zeros(2);E[i,j]=1
        equal(s.kronecker_product(E,s.eye(2))*J,J*E,
              "all-old-operator naturality for matrix unit "+str((i,j)))
equal(J.T*newG*J,a*s.eye(2),"exact actual born-plus-G corner is sqrt(p) times identity")

# Full target transport on two actual raw bits, without asserting a free inverse gate.
B=s.kronecker_product(G,G)
vv=s.kronecker_product(v,v)
e00=s.Matrix([1,0,0,0])
U=mat(B*W*B.T)
equal(B*e00,vv,"two actual raw births give the complete target input")
equal(U.T*U,s.eye(4),"transported target is unitary on all four work columns")
equal(U*vv,B*W*e00,"entire transported target output agrees with its logical target")
Jq=s.kronecker_product(s.eye(2),vv)
Uq=s.kronecker_product(s.eye(2),U)
equal(Jq.T*Uq*Jq,a*s.eye(2),"target corner transport holds on all unknown old columns")
Pzero=e00*e00.T
Flogical=mat(Pzero*W.T*(s.eye(4)-Pzero)*W*Pzero)
Pref=mat(Jq*Jq.T)
Fraw=mat(Pref*Uq.T*(s.eye(8)-Pref)*Uq*Pref)
equal(Fraw,s.kronecker_product(s.eye(2),B*Flogical*B.T),
      "full eight-column feedback transports the entire logical cut and complement")
O=s.diag(0,0,0,1)
Oraw=mat(B*O*B.T)
equal(vv.T*U.T*Oraw*U*vv,e00.T*W.T*O*W*e00,
      "the transported complete readout has the same probability")
equal(Oraw*Oraw,Oraw,"transported readout remains a positive orthogonal effect")


def raw_history(K):
    """Exactly K repetitions of one actual raw birth followed by one actual G."""
    dims=[]; forward=[]; passive=[]; current=2
    for k in range(K):
        dims.append(current)
        birth=s.kronecker_product(s.eye(current),v)
        forward.append(birth);passive.append(birth)
        current*=2
        dims.append(current)
        g=s.kronecker_product(s.eye(current//2),G)
        if k+1<K:
            forward.append(g);passive.append(s.eye(current))
    last=g
    offsets=[0]
    for d in dims:offsets.append(offsets[-1]+d)
    D=offsets[-1]
    backwards=[None]*len(dims);backwards[-1]=s.eye(dims[-1])
    for j in range(len(dims)-2,-1,-1):
        backwards[j]=mat(backwards[j+1]*passive[j])
    details=[s.eye(dims[0])]
    for j in range(1,len(dims)):
        details.append(mat(s.eye(dims[j])-passive[j-1]*passive[j-1].T))
    R=s.zeros(D,dims[-1]);R[:dims[0],:]=backwards[0].T
    for j in range(1,len(dims)):
        R[offsets[j]:offsets[j+1],:]=mat(details[j]*backwards[j].T)
    S=s.zeros(D)
    for j,Fj in enumerate(forward):
        S[offsets[j+1]:offsets[j+2],offsets[j]:offsets[j+1]]=Fj
    T=s.Matrix(S);T[:,offsets[-2]:offsets[-1]]+=R*last;T=mat(T)
    prefixes=[s.eye(2)]
    for Fj in forward:prefixes.append(mat(Fj*prefixes[-1]))
    P=mat(s.diag(*[mat(A*A.T) for A in prefixes]))
    C=mat(backwards[0].T*last*prefixes[-1])
    label=str(K)+" actual raw retention blocks"
    equal(R.T*R,s.eye(dims[-1]),label+": terminal closure retains every final column")
    equal(T.T*T,s.eye(D),label+": true growing clock is unitary")
    equal(T*T.T,s.eye(D),label+": true growing clock is surjective")
    equal(C,a**K*s.eye(2),label+": exact full-history corner product")
    leak=mat((s.eye(D)-P)*T*P)
    equal(leak[:,:offsets[-2]],s.zeros(D,offsets[-2]),
          label+": every nonterminal leakage column is zero")
    F=mat(leak.T*leak)
    expected=s.zeros(D)
    expected[offsets[-2]:offsets[-1],offsets[-2]:offsets[-1]]=mat((1-p**K)*prefixes[-1]*prefixes[-1].T)
    equal(F,expected,label+": full feedback includes all terminal detail exactly once")
    lam=s.Symbol("lambda")
    char=F.charpoly(lam).as_expr()
    wanted=lam**(D-2)*(lam-(1-p**K))**2
    require(all(red(c)==0 for c in s.Poly(char-wanted,lam).all_coeffs()),
            label+": full determinant is (1-z+z p^K)^2")
    require(len(dims)==2*K,label+": birth and G are both counted as actual stages")
    require(dims[-1]==2**K*2 and D>=dims[-1],
            label+": full growing dimension satisfies the exact thermal lower bound")
    return {"K":K,"stage_dimensions":dims,"D":D,"full_hodge_dimension":425*D}


fixtures=[raw_history(1),raw_history(2)]
cstar=red((vv.T*W*vv)[0])
require(red(cstar-(a*p**3+4*p**4))==0,"fullStep-only born-pair corner has the exact stated formula")
require(s.Rational(3,5)**2+s.Rational(3,5)<1,
        "Golden positive root p is greater than three fifths")
require(4*s.Rational(3,5)**4>s.Rational(1,2),
        "fullStep-only dimension times squared return is strictly greater than one")
require(red((2*p-1)*(2*p+3))==1,
        "2p exceeds one: (2p-1)(2p+3)=1 and p>0")

result={
    "schema":"d0.raw-cylinder-realization-exact-check/1",
    "status":"PASS",
    "native_owner":str(NATIVE.relative_to(REPO)),
    "native_owner_sha256":hashlib.sha256(NATIVE.read_bytes()).hexdigest(),
    "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "initial_old_input_rank":2,
    "canonical_raw_birth":"x -> x tensor (sqrt(p),p)",
    "literal_retention":"one admitted G on the newest binary slot",
    "total_stages_per_retained_bit":2,
    "return_square_factor":"p",
    "dimension_factor":2,
    "normalized_heat_decay":"(2*p)^(-K)",
    "fixtures":fixtures,
    "target_conjugation_is_not_a_free_inverse_gate":True,
    "full_regular_fibonacci_gns_identified_with_raw_cylinders":False,
    "general_gr_word_emitted":False,
    "exact_finite_stationarity_claimed":False,
    "check_count":len(checks),
    "checks":checks,
}
print(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True))
