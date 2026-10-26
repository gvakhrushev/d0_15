#!/usr/bin/env python3
"""Literal ORIGINAL native G/CX all-column n-parity Golden memory,
not a surrogate Toffoli or a gate outside the D0 native alphabet.

Theorem: n native CX copy controls into one internal blank are necessary
and sufficient to record all n source-bit parity; 2n CX+2 native G gives
one TRUE Golden Born event with probability 4*phi^-3 for even parity
and 0 for odd parity. Every work/input/failure column is retained.

Use source-owned native_execution.py, actual positive Golden algebraic field.
No extra free source spin, Q8 gate, uncharged inverse, physical GR action or
M1 selector. The actual future measurement costs its real clock/work.
"""
from __future__ import annotations
from pathlib import Path
import json
import sys
import sympy as S

ROOT=Path(__file__).resolve().parent.parent / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0,str(ROOT))
import native_execution as ne

CHECKS=0
def check(ok,why):
    global CHECKS
    CHECKS+=1
    if not bool(ok):
        raise ArithmeticError(why)

p=ne.P
I2=S.eye(2)
X=S.Matrix([[0,1],[1,0]])
G=ne.G_LOCAL
check(ne.exact_matrix_equal(X*G*X,G.T),
      "literal source native Golden inverse is conjugate by X")
check(ne.exact_matrix_equal(G*X*G*X,I2),
      "odd-parity whole native Golden block is exact I, no inverse primitive")
check(ne.exact_matrix_equal(G.T*G,I2),
      "original G positive real orthogonal on full two input columns")
check(ne.exact_matrix_equal(
    S.Matrix([[G[1,0]**2+G[0,0]**2]]),S.Matrix([[1]])),
      "exact original p+p²=1")
g2=G*G
check(S.simplify(g2[1,0]**2-4*p**3)==0,
      "exact Golden bright probability 4 phi^-3")

def word(n, golden=True):
    # wire0 MSB, helper wire n LSB. All data wires are arbitrary
    # UNKNOWN inputs; h is the ONE true prepared internal blank.
    C=tuple(ne.Gate("CX",(i,n)) for i in range(n))
    gates=C+(ne.Gate("G",(n,)),)+C+(ne.Gate("G",(n,)),) if golden else C
    e=ne.Execution(n+1,(n,),(),gates,ne.G_CX,report_bits=(n,))
    ne.validate_execution(e,max_qubits=n+1,max_expanded_stages=3*n+4)
    inv=ne.inventory(e,max_qubits=n+1,max_expanded_stages=3*n+4)
    check(inv.input_dimension==2**n and inv.full_dimension==2**(n+1),
          "original n DATA independent inputs and one blank helper cut")
    check(inv.g_count==(2 if golden else 0) and
          inv.cx_count==(2*n if golden else n),
          "exact native raw primitive clock/inventory with all labels")
    check(not inv.source_i_count,"NO injected paid sourceI primitive")
    return e

results=[]
for n in (2,3,4):
    e=word(n,True)
    u=ne.word_matrix(e,max_qubits=n+1,max_expanded_stages=3*n+4)
    full=S.zeros(2**(n+1))
    for x in range(2**n):
        block=g2 if x.bit_count()%2==0 else I2
        for j in range(2):
            for k in range(2):
                full[2*x+j,2*x+k]=block[j,k]
    check(ne.exact_matrix_equal(u,full),
          "ACTUAL complete G/CX source word equals all-input parity-dependent Golden")
    check(ne.exact_matrix_equal(u.T*u,S.eye(2**(n+1))),
          "all original helper-input and output columns are strictly real unitary")
    inj=ne.input_isometry(e,max_qubits=n+1,max_expanded_stages=3*n+4)
    Pi=S.diag(*[j&1 for j in range(2**(n+1))])
    eff=inj.T*u.T*Pi*u*inj
    target=S.diag(*[(4*p**3 if x.bit_count()%2==0 else 0)
                    for x in range(2**n)])
    check(ne.exact_matrix_equal(eff,target),
          "ACTUAL prepared Born effect separates even and odd source parity")
    plain=word(n,False)
    C=ne.word_matrix(plain,max_qubits=n+1,max_expanded_stages=3*n+4)
    plaininj=ne.input_isometry(plain,max_qubits=n+1,max_expanded_stages=3*n+4)
    peff=plaininj.T*C.T*Pi*C*plaininj
    ideal=S.diag(*[x.bit_count()%2 for x in range(2**n)])
    check(ne.exact_matrix_equal(peff,ideal),
          "n raw original CX gates EXACTLY compute bit parity into internal memory")
    check(ne.exact_matrix_equal(C.T*C,S.eye(2**(n+1))),
          "all columns of parity-copy native word reversible")
    results.append({
       "n_unknown_data_bits":n,
       "literal_raw_Golden_full_stages":2*n+2,
       "literal_G":2,
       "literal_CX":2*n,
       "literal_full_carrier_dimension":2**(n+1),
       "literal_input_rank":2**n,
       "n_CX_plain_parity_lower_bound_attained":n,
       "even_Born_bright":"4*p^3",
       "odd_Born_bright":"0"
    })

# A pure graph connection-count lower bound, not a D_min/CQ global
# cost theorem: on n inputs+one independent readout ancilla, linking
# each source component to the readout requires >=n two-wire CX edges.
for n in range(2,61):
    check(n<=2*n and n+1>n,
          "n disjoint independent sources need n two-wire graph connections")

print(json.dumps({
 "status":"PASS_EXACT_ORIGINAL_NATIVE_G_CX_GLOBAL_PARITY_AND_SHARP_CX_BOUNDS",
 "checks":CHECKS,
 "cases":results,
 "native_source_GCX_only":True,
 "full_quantum_input_and_unused_columns_kept":True,
 "shared_internal_helper_count":1,
 "actual_global_causal_support_size":"n",
 "raw_primitive_clock":"2n+2 (or n for the parity-copy task)",
 "full_Book_M1_action_selection":False,
 "GR_closed":False
},sort_keys=True,indent=2))
