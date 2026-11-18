#!/usr/bin/env python3
"""Prove real J-commutant corner and test missing-premise counterexamples."""
from pathlib import Path
from hashlib import sha256
import importlib.util,json,sys
import sympy as s
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=P.parent;domain=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py');spec=importlib.util.spec_from_file_location('b52_domain',domain);nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
J=s.Matrix([[0,-1],[1,0]]);I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);K=s.kronecker_product
assert all(x.is_real for x in nt.G_LOCAL) and all(x.is_real for x in nt.SOURCE_I_LOCAL) and nt.SOURCE_I_LOCAL**2==K(Z,s.eye(4))
a,b,c=s.symbols('a b c',real=True);S=s.Matrix([[a,b],[b,c]]);assert S*J-J*S==s.Matrix([[2*b,c-a],[c-a,-2*b]])
sol=s.solve(list(S*J-J*S),(b,c),dict=True);assert sol==[{b:0,c:a}]
# A commuting with J may still entangle WORK and aux, yet its real symmetric
# compressed Z-report corner is scalar on the *full complex* aux space.
R=s.Rational(3,5)*I+s.Rational(4,5)*J;P0=s.diag(1,0);P1=s.diag(0,1);A=K(H,I)*(K(P0,I)+K(P1,R));JW=K(s.Matrix([1,1])/s.sqrt(2),I);ZF=K(Z,I)
assert s.simplify(A.T*A)==s.eye(4) and A*K(I,J)==K(I,J)*A
F=s.simplify(JW.T*A.T*ZF*A*JW);assert F==s.Rational(3,5)*I
state=s.simplify(A*K(s.Matrix([1,1])/s.sqrt(2),s.Matrix([1,0])));schmidt=s.Matrix([[state[0],state[1]],[state[2],state[3]]]);assert s.simplify(schmidt.det())!=0
# If the canonical WORK state is complex, real A and exact J commutation are
# insufficient: the Hermitian corner acquires a nonzero iJ component.
jcomplex=K(s.Matrix([1,s.I])/s.sqrt(2),I);FC=s.simplify(jcomplex.conjugate().T*A.T*ZF*A*jcomplex);assert FC==s.I*s.Rational(4,5)*J and FC!=FC[0,0]*I and FC*J==J*FC and FC.conjugate().T==FC
# Without exact identity on D_other, real symmetric [F,J_aux]=0 does not
# force F = scalar on aux tensor I_other. The auxiliary observable below is
# realized as an actual corner using work-controlled projectors of F.
Fother=K(J,J);assert Fother.T==Fother and Fother*Fother==s.eye(4) and Fother*K(J,I)==K(J,I)*Fother and Fother!=Fother[0,0]*s.eye(4)
plus=(s.eye(4)+Fother)/2;minus=(s.eye(4)-Fother)/2;U=K(I,plus)+K(X,minus);j0=K(s.Matrix([1,0]),s.eye(4));actual=s.simplify(j0.T*U.T*K(Z,s.eye(4))*U*j0);assert U.T*U==s.eye(8) and U*K(I,J,I)==K(I,J,I)*U and actual==Fother
# A fibre bound checked only for aux=0 can fail after shared aux has moved:
# ideal/actual second stage agree on aux0, but a common first X_aux moves it
# to aux1, after which the difference norm is nonzero (orthogonal outputs).
CNOT=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]) # aux first
zero=s.Matrix([1,0]);one=s.Matrix([0,1]);jaux0=K(zero,I);assert CNOT*jaux0==jaux0
v=K(zero,zero);before=K(X,I)*v;actual=CNOT*before;ideal=before;assert s.simplify((actual-ideal).dot(actual-ideal))==2
checks=[O/'round48/AUX_MACRO_COMMUTATION_CHECK.json',O/'round49/SELECT_AUX_ALL_SECTORS_CHECK.json',O/'round49/REPORT_SELECT_AUX_NAMESPACE_CHECK.json',O/'round49/SC6_ACTIVE_PORT_OWNER_CHECK.json',O/'round50/A25_NAMESPACE_BIT_ORDER_CHECK.json',O/'round50/A25_ACTUAL_PROVIDER_REMAP_CHECK.json',O/'round51/A13_A15_ALL_ROWS_REVERSE_CHECK.json',O/'round51/A17_NATIVE_INDEPENDENT_REVERSE_CHECK.json',D/'round25/global_h1.py',D/'round25/H1_NAMESPACE_PLAN.json',domain]
for q in checks:assert q.is_file()
for q in checks[:8]:assert json.loads(q.read_text())['status'].startswith('PASS')
out={'status':'PASS_EXACT_J_CORNER_AND_NECESSARY_PREMISES','input_sha256':{str(q):sha256(q.read_bytes()).hexdigest() for q in checks},'real_native_G_and_SourceI':True,'S_real_symmetric_and_SJ_equals_JS_implies_scalar':True,'commuting_orthogonal_A_entangles_WORK_aux':True,'nontrivial_example_corner':'3/5 I_aux','complex_WORK_counterexample':'i*(4/5)*J_aux; Hermitian non-scalar despite J symmetry','Dother_identity_counterexample':'F=J_aux tensor J_other is real symmetric, involutory, commuting with J_aux and is realised as a report corner','shared_aux_fibre_counterexample':'a component exact only for aux=0 can fail after a previous stage moves aux; squared output difference 2','scope':'Conditional composition of the pinned provider macro proofs, disjoint namespace and declared real RAW embedding. Does not establish global physical admission or marked-history equivalence.','physical_C_or_GR_closed':False}
(P/'SCALAR_CORNER_PREMISE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'complex_WORK_counterexample':out['complex_WORK_counterexample']}))
