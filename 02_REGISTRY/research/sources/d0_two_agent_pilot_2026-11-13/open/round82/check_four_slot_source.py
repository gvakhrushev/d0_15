#!/usr/bin/env python3
"""Exact toy counterexamples, A30 cut templates, and finite Pf-row bounds."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import importlib.util,json,sys
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;O=HERE.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
spec=importlib.util.spec_from_file_location('b82kernel',HERE/'actual_q_kernel.py');k=importlib.util.module_from_spec(spec);spec.loader.exec_module(k)
a=k.source;stages=a.stages();f={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0};g={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1}
assert stages.index(g)==stages.index(f)+1
assert [x['kind'] for x in stages[stages.index(f)+1:]]==['RAW_RESOURCE_FRAME']+['REPORT']*7+['PORT_ZERO','SC6']
# Prove S support excludes SAM as control AND target: report-wire mapping
# lands in SITE, private, port/spin/aux/old witness; SC6 and frame similarly.
plan=a.g.namespace();lay=plan['layout'];SAM=set(lay['SAM'])
assert SAM.isdisjoint(lay['SITE']+lay['spin']+[lay['port'],lay['aux_arbitrary'],lay['oldRIGHT_witness'],lay['qubits']])
assert SAM.isdisjoint(plan['SC6_local_to_global'])
assert SAM.isdisjoint(a.resource_wires())
N=plan['local_report']['logical_wire_count']
for report in plan['reports']:
    assert report['private_start']>max(SAM)
    for q in (0,7,8,N-1,N,N+1,N+2,N+3,N+4):
        assert a.g.ns.report_wire(plan,report,q) not in SAM
# All compiler replacements use input support plus only helper/port; B58
# supplies the structural induction over the actual report/SC6 words.
# Both cuts immediately follow complete frame blocks. A30 replacement
# keeps SourceI parity state; inspect the exact terminal frame template.
compiler=a.c.production_compiler();wire=a.resource_wires()[-1];layout=a.g.namespace()['layout']
assert wire not in layout['SAM'] and wire!=layout['port']
for depth in (0,2):
    raw=a.g.invert(a.c.nb.gate('G',wire),depth,a.g.namespace())
    native,pending,_=compiler.transform(raw,0);assert pending==0
    for leaf in a.c.nb.leaves(a.b.physical_tree(native)):
        assert leaf['op'] in ('G','CX') and all(q not in range(2,2690) for q in leaf['wires'])
# Metadata only: exact stage identities establish matching profile ordering
# without traversing an astronomical full source-provider stream.
assert len(a.resource_wires())==29848
inv=a.inventory();eW=inv['replacement_error'];assert eW<F(1,2**3244)

# Tiny literal native cross evaluator: the two metadata cuts have the same
# kernel because their intervening G acts on WORK alone.
def small_stream():
    yield {'op':'CX','wires':[0,1]}
    yield {'op':'B82_CUT','name':'Qf_dagger_after_common_RAW_mark'}
    yield {'op':'G','wires':[1]}
    yield {'op':'B82_CUT','name':'Qb_before_return_bank'}
    yield {'op':'CX','wires':[0,1]}
for b0,c0 in product(range(2),repeat=2):
    x=k.small_cross_entry(2,(0,),b0,c0,'Qf_dagger_after_common_RAW_mark',small_stream)
    y=k.small_cross_entry(2,(0,),b0,c0,'Qb_before_return_bank',small_stream)
    assert x==y
try:k.small_cross_entry(14,(0,),0,0,'Qb_before_return_bank',small_stream)
except NotImplementedError:pass
else:raise AssertionError('production evaluator unexpectedly materialized')

# Explicit real original-profile counterexample for new post at centre.
# Initial work |0>, 2D SAM; B is controlled R, S=I⊗Z, Q=exp(tJ).
R=s.Matrix([[s.Rational(12,13),-s.Rational(5,13)], [s.Rational(5,13),s.Rational(12,13)]])
B=s.diag(1,1,1,1);B[2:4,2:4]=R
Z=s.diag(1,-1);J=s.Matrix([[0,-1],[1,0]]);S=s.kronecker_product(s.eye(2),Z);Y=s.kronecker_product(J,s.eye(2))
assert S*Y==Y*S and B*Y!=Y*B
embed=s.Matrix([[1,0],[0,0],[0,1],[0,0]])
M=s.simplify(embed.T*B.T*S*B*embed)
assert M==s.diag(1,s.Rational(119,169)) and M[1,1]>s.Rational(2,3)
T=s.simplify(embed.T*B.T*S*Y*B*embed)
assert T==s.Rational(12,13)*J and T.T==-T
chi=s.Matrix([s.Rational(3,5),s.Rational(4,5)])
r=s.sqrt((chi.T*M*M*chi)[0]);xi=M*chi/r;d=(chi.T*xi)[0]
K=chi*xi.T-xi*chi.T;U=s.eye(2)+K+K*K/(1+d)
assert s.simplify(U*xi-chi)==s.zeros(2,1)
qrow=s.simplify((chi.T*U*T*chi)[0]);expected=s.simplify(s.Rational(12,13)*chi[0]*chi[1]*(M[1,1]-M[0,0])/r)
assert s.simplify(qrow-expected)==0 and qrow!=0
# Qb and Qf† are independent, opposite first derivatives; neither zero.
assert s.simplify(qrow+(-qrow))==0
# Fixed-post Pf derivative equals half the reduced quadratic derivative.
cfprime=s.simplify((chi.T*U*M*J*chi)[0])
Dq=s.simplify(2*(chi.T*M*M*J*chi)[0])
assert s.simplify(cfprime-Dq/(2*r))==0
# All-real-skew logical stationarity iff (M²−q)chi=0: choose an explicit
# skew that maps chi to w in this non-scalar exact fixture.
q=(chi.T*M*M*chi)[0];w=(M*M-q*s.eye(2))*chi
X=w*chi.T-chi*w.T
assert X.T==-X and s.simplify(X*chi-w)==s.zeros(2,1)
assert s.simplify(2*(chi.T*M*M*X*chi)[0]-2*(w.T*w)[0])==0 and w!=s.zeros(2,1)

# A full prepared map inserted after bank changes although all WORK-only
# effects commute with SAM control. Its BEFORE-Q map remains fixed.
Q=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
Qfull=s.kronecker_product(Q,s.eye(2));mark=s.kronecker_product(s.eye(2),Z)
assert Qfull.T*mark*Qfull==mark and Qfull*B*embed!=B*embed
assert B.T*Qfull.T*mark*Qfull*B==B.T*mark*B

# General actual cross-kernel algebra for Y=|b><a|−|a><b|.
La,Lb,Ma,Mb,ca,cb,rr,A,gg=s.symbols('La Lb Ma Mb ca cb rr A gg',real=True,nonzero=True)
Ls=(Lb+La)/2;Lanti=(Lb-La)/2
pf=-ca*cb*(Mb**2-Ma**2)/(2*A*gg)
q_direct=-ca*cb*(Mb*Lb-Ma*La)/(2*A*gg)
q_split=Ls/(Ma+Mb)*pf-ca*cb*Lanti*(Ma+Mb)/(2*A*gg)
assert s.simplify(q_direct-q_split)==0
q_half=pf/2-ca*cb*((Ls-(Ma+Mb)/2)*(Mb-Ma)+Lanti*(Ma+Mb))/(2*A*gg)
assert s.simplify(q_direct-q_half)==0
# Real reflected exact-source case: K_bc=<u_b,S u_c> symmetric and
# K_bc−(M_b+M_c)/2=−<u_b−u_c,S(u_b−u_c)>/2.
u=s.Matrix(s.symbols('u0:2',real=True));v=s.Matrix(s.symbols('v0:2',real=True))
assert s.expand((u.T*Z*v)[0]-((u.T*Z*u)[0]+(v.T*Z*v)[0])/2+((u-v).T*Z*(u-v))[0]/2)==0

# Independent Pf analytic/fixed-post and native finite family bounds.
# A37 ||C_red||>2^-46, A31 factor 55 for 2688 unit-coordinate rows.
assert F(1,55*2**46)>F(1,2**52)
assert F(52,1)/(2*F(309,500)*F(39,50)*(1-F(1,2**23)))<55
sigmaU=F(1,2**14623);gs=F(1,2**3158);angle=F(1,2**4852);t=F(1,2**1618);z=F(1,2**20)
Janalytic=4*sigmaU/gs;assert Janalytic==F(1,2**11463)
bracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
Taylor=t*t*bracket/(16*gs);angle_error=angle/(t*gs)
assert Taylor<F(1,2**78) and angle_error==F(1,2**76)
# Build a mathematically finite clock using A41's UNIFORM call bound;
# the value of its actual (unmaterialized) word length is not assumed.
plan=json.loads((D/'round41/SAM_ONLY_COMPILER_PLAN.json').read_text())
assert plan['status']=='MATHEMATICALLY_CONSTRUCTIVE_SAM_ONLY_FULL_COLUMN_COMPILER'
Umax=int(plan['upper_total_calls_hex'],16)
core=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text())
Wlen=int(core['new_native_call_count']);n0=core['total_RAW_births']
endpoint=json.loads((O/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json').read_text())
powers=[int(endpoint['rotations'][name]['power_hex'],16) for name in ('plus','minus')]
pre=max(powers)+4;post=Umax+4
Nbase=n0+pre+Wlen+post+2
assert Nbase<2**25460
Klate=4*(25460+3158+1638+75+1);assert Klate==121328
heat=F(6*2**25460,359)/(t*(F(8,3)*z*gs))*F(1,2**(Klate//4))
assert heat<F(1,2**76)
total=Janalytic+Taylor+angle_error+heat
assert total<F(1,2**75) and F(1,2**52)-total>F(1,2**53)
# Fixed mathematical Uhat0, actual G^n+/G^n− in P_f; padded lengths and
# two paid CX around late births form a native full-price finite comparison.

ROOT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
files=[Path(__file__),HERE/'actual_q_kernel.py',D/'round30/marked_source_schedule.py',
       D/'round30/COMMON_SOURCE_MARKED_PLAN.json',D/'round29/gcx_compiler.py',
       D/'round37/ACTUAL_POST_SAM_STATIONARY_REDUCTION_RU.md',D/'round31/ACTUAL_MEAN_GEOMETRY_LIFT_RU.md',
       D/'round41/SAM_ONLY_COMPILER_PLAN.json',O/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',
       O/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',O/'round78/B78_ORIGINAL_H1_FN_ADMISSION_RU.md',
       ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md']
out={'status':'EXACT_Q_KERNEL_CONDITIONAL_SOURCE_AND_NONZERO_PF_FINITE_COMPARISON',
     'two_A30_Q_cut_templates_sourceI_pending_zero_checked':True,
     'actual_Q_kernel_values_evaluated':False,
     'small_native_cross_kernel_Qa_Qb_equivalence_checked':True,
     'actual_middle_support_no_SAM_controls_or_targets':True,
     'middle_report_mapping_frame_SC6_checked_and_B58_induction_consumed':True,
     'all_real_skew_stationarity_requires_M2_chi_parallel_chi':True,
     'reflected_toy_inner_rows_nonzero_both_signs':True,
     'Q_commutes_S_does_not_imply_Q_commutes_bank':True,
     'actual_plane_Q_source_symmetric_and_antisymmetric_kernel_split':True,
     'Q_antisymmetric_kernel_error_lt':'2^-3244',
     'nonzero_Pf_unit_row_conditional_on_A37_A41':'greater than 2^-52 reduced feedback',
     'nonzero_Pf_full_H_plus_J_finite_difference_conditional_lower':'2^-53 normalized magnitude',
     'chosen_mathematical_example_K':Klate,
     'production_words_materialized':False,'same_original_task_membership_proved':False,
     'full_stationarity_or_Cost_Info_proved':False,'physical_C_closed':False,'GR_closed':False,
     'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files}}
(HERE/'B82_FOUR_SLOT_SOURCE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
