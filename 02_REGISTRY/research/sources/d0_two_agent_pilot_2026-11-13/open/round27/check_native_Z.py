#!/usr/bin/env python3
"""Exact native source-I² Z on port and routed Z with unknown spin/port."""
from pathlib import Path
import importlib.util,sys,json,hashlib
import sympy as s
P=Path(__file__).resolve().parent;ROOT=P.parents[5]
source=ROOT/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
spec=importlib.util.spec_from_file_location('b27_native',source);nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
G=nt.Gate;port=1;spin=(2,3);q=0;src=G('SourceI',(port,*spin))
swap=[G('CX',(q,port)),G('CX',(port,q)),G('CX',(q,port))]
word=swap+[src,src]+swap
ex=nt.Execution(4,(),(),tuple(word),nt.G_CX_SOURCE_I,port,spin)
nt.validate_execution(ex,max_qubits=4,max_expanded_stages=8)
actual=nt.word_matrix(ex,max_qubits=4,max_expanded_stages=8)
Z=s.diag(1,-1);expected=s.kronecker_product(Z,s.eye(8));assert nt.exact_matrix_equal(actual,expected)
# Source spin is exactly restored for every port/spin column; at word boundaries
# the routed port is restored even when entangled with the target.
local=nt.SOURCE_I_LOCAL**2;assert local==s.kronecker_product(Z,s.eye(4))
# The owned exact inverse G uses Z G Z on the physical port.
core=[src,src,G('G',(port,)),src,src];invword=swap+core+swap
invex=nt.Execution(4,(),(),tuple(invword),nt.G_CX_SOURCE_I,port,spin)
nt.validate_execution(invex,max_qubits=4,max_expanded_stages=11)
inverse=nt.word_matrix(invex,max_qubits=4,max_expanded_stages=11)
assert nt.exact_matrix_equal(inverse,s.kronecker_product(nt.G_LOCAL.T,s.eye(8)))
assert nt.exact_matrix_equal(nt.G_LOCAL.T*nt.G_LOCAL,s.eye(2))
assert nt.exact_matrix_equal(nt.G_LOCAL.T*s.Matrix([nt.A,nt.P]),s.Matrix([1,0]))
res={'status':'PASS_EXACT_NATIVE_Z_ROUTING_ALL_COLUMNS','profile':'G_CX_SOURCE_I','tested_qubits':4,'source_port':port,'source_spin':spin,'spin_dimension':4,'spin_basis':['1','i','j','k'],'L_i_matrix':[[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]],'target_q':q,
 'word':[{'op':g.op,'wires':g.wires} for g in word], 'inventory':{'CX':6,'SourceI':2,'total':8},
 'Z_on_port_direct':{'CX':0,'SourceI':2,'total':2},'full_16_columns_exact':True,'unknown_port_and_spin_preserved':True,
 'applicability':'one distinct ordinary q, declared source port and untouched oldRIGHT; routing port must not be protected',
 'routed_G_inverse_for_fresh_v_to_zero':{'CX':6,'SourceI':4,'G':1,'total':11,'full_16_columns_exact':True,'operator':'G_q^-1 tensor I_port tensor I_spin','requires':'fresh RAW v on q, an accessible declared port, both distinct from protected oldRIGHT; each birth and gate paid','optional_return_zero_to_v':'one separately paid G(q)'},'on_port_G_inverse':{'CX':0,'SourceI':4,'G':1,'total':5},'logical_CX_native_direct':True,'logical_X_CCX_CZ_native_compiled':False,'full_controlled_involution_native':False,
 'native_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'GR_closed':False}
(P/'NATIVE_Z_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
